# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Controlled App Server frames against the real singleton Store and broker."""
import base64
import json
import time
from textwrap import dedent
from unittest.mock import Mock

import pytest

from test_governed_native_batches import _choice, _layer_session, lc, layered

import governed_codex_carrier as carrier


@pytest.fixture
def worker_peer(tmp_path):
    """Supply an isolated worker acknowledgment and an empty MCP inventory."""
    peer = Mock(directory=tmp_path)
    started = {'thread': {'id': 'acknowledged-thread', 'environments': []},
               'approvalPolicy': 'never', 'sandbox': {'type': 'readOnly', 'networkAccess': False}}
    inventory = {'data': [], 'nextCursor': None}
    peer.call.side_effect = [started, inventory]
    return peer, started, inventory


def test_worker_thread_opens_isolated_worker_with_explicit_model(worker_peer):
    """Return the acknowledged thread after checking its exact inventory."""
    peer, started, _ = worker_peer
    observe = Mock()
    result = carrier.worker_thread(peer, 12, 'selected-model', role_choices=['software-engineer'], observe=observe)
    assert result == started
    start, inventory = [request.args for request in peer.call.call_args_list]
    method, params, deadline, callback = start
    assert (method, deadline, callback) == ('thread/start', 12, observe)
    assert params['cwd'] == str(peer.directory)
    assert (params['model'], params['approvalPolicy'], params['sandbox'], params['environments']) == (
        'selected-model', 'never', 'read-only', [])
    tool, = params['dynamicTools']
    assert tool['name'] == carrier.TOOL
    role_shape = tool['inputSchema']['properties']['request']['anyOf'][-1]
    assert role_shape['properties']['role']['enum'] == ['software-engineer']
    assert inventory == ('mcpServerStatus/list', {'threadId': 'acknowledged-thread'}, 12, observe)


def test_worker_thread_rejects_empty_but_paginated_inventory(worker_peer):
    """An empty first page does not establish an empty MCP inventory."""
    peer, _, inventory = worker_peer
    inventory['nextCursor'] = 'another-page'
    with pytest.raises(carrier.InvocationError, match='ambient MCP'):
        carrier.worker_thread(peer, 12, role_choices=['software-engineer'])
    assert 'model' not in peer.call.call_args_list[0].args[1]
    assert peer.call.call_count == 2


def test_worker_thread_rejects_unconfirmed_network_denial(worker_peer):
    """Stop after thread creation if the host omits network denial."""
    peer, started, _ = worker_peer
    del started['sandbox']['networkAccess']
    with pytest.raises(carrier.InvocationError, match='network-denied'):
        carrier.worker_thread(peer, 12, role_choices=['software-engineer'])
    peer.call.assert_called_once()


class AppServer:
    """Owned fake stdio peer with explicit response and interruption boundaries."""

    def __init__(self, directory, prepared, *, interrupt=None, malformed=False, status='completed'):
        self.directory = directory
        self.prepared = prepared
        self.interrupt = interrupt
        self.status = status
        self.thread = 'thread-exact'
        self.turn = 'turn-exact'
        self.methods = []
        self.sent = []
        self.frames = []
        self.prompt = prepared['invocation']['arguments']['message']
        self.member = prepared['members'][0]['member_key']
        self.raw = ('not semantic JSON: cafe\u0301' if malformed else json.dumps({
            'format': 'jai.semantic-return/1', 'results': [_choice(prepared['members'][0]['packet'])]
        }, ensure_ascii=False))
        self.final = {'id': 'item-exact', 'type': 'agentMessage', 'phase': 'final_answer', 'text': self.raw}
        self.history = []
        self.role_reads = ()

    def call(self, method, params, deadline, observe=None):
        self.methods.append(method)
        if method == 'thread/start':
            assert params['environments'] == []
            assert params['approvalPolicy'] == 'never'
            assert [item['name'] for item in params['dynamicTools']] == [carrier.TOOL]
            choices = params['dynamicTools'][0]['inputSchema']['properties']['request']['anyOf'][-1]
            self.advertised_roles = choices['properties']['role']['enum']
            return {'thread': {'id': self.thread, 'environments': []}, 'approvalPolicy': 'never',
                    'sandbox': {'type': 'readOnly', 'networkAccess': False}}
        if method == 'mcpServerStatus/list':
            assert params == {'threadId': self.thread}
            return {'data': [], 'nextCursor': None}
        if method == 'thread/read':
            return {'thread': {'id': self.thread, 'turns': self.history}}
        assert method == 'turn/start' and params['threadId'] == self.thread
        assert params['input'][0]['text'].encode('utf-8') == self.prompt.encode('utf-8')
        text = {'type': 'text', 'text': self.prompt}
        turn = {'id': self.turn, 'status': self.status,
                'items': [{'type': 'userMessage', 'content': [text]}, self.final]}
        self.history = [turn]
        if self.interrupt == 'after_send':
            raise carrier.CarrierError('Controlled loss before acknowledgment')
        ids = {'threadId': self.thread, 'turnId': self.turn}
        request = {'id': 'bounded-read', 'operation': 'read', 'handle': 'catalogue'}
        for identifier, thread, member in [(11, self.thread, 'foreign'),
                                           (12, 'foreign-thread', self.member),
                                           (13, self.thread, self.member)]:
            self.frames.append({'id': identifier, 'method': 'item/tool/call',
                                'params': {**ids, 'threadId': thread, 'tool': carrier.TOOL,
                                           'arguments': {'request': request, **({'member_key': member} if member == 'foreign' else {})}}})
        for identifier, role in enumerate(self.role_reads, 20):
            self.frames.append({'id': identifier, 'method': 'item/tool/call', 'params': {
                **ids, 'tool': carrier.TOOL, 'arguments': {'request': {
                    'id': role, 'operation': 'read_role_instruction', 'role': role}}}})
        self.frames.extend([
            {'method': 'item/completed', 'params': {**ids, 'item': {
                'id': 'commentary', 'type': 'agentMessage', 'phase': 'commentary', 'text': 'ignored'}}},
            {'method': 'item/completed', 'params': {**ids, 'item': self.final}},
            {'method': 'turn/completed', 'params': {**ids, 'turn': turn}},
        ])
        return {'turn': {'id': self.turn}}

    def receive(self, deadline):
        if self.interrupt == 'after_ack':
            raise carrier.CarrierError('Controlled loss after acknowledgment')
        return self.frames.pop(0)

    def send(self, frame, deadline):
        self.sent.append(frame)

    def deny(self, frame, deadline):
        if 'id' in frame:
            self.sent.append({'id': frame['id'], 'error': 'denied'})


@pytest.fixture
def ready(tmp_path):
    session = _layer_session(tmp_path, aggregate_limit_ms=None, single_member=True)
    offered = session.next()
    directory = tmp_path / 'receipts'
    directory.mkdir()
    return session, offered, directory


def test_carrier_binds_tools_and_admits_exact_final_once(ready):
    session, offered, directory = ready
    invocation = offered['invocation_id']
    peer = AppServer(directory, offered['prepared'])
    result = carrier.carry(session, invocation, peer, directory)
    assert result['status'] == 'returned'
    replies = {item['id']: item for item in peer.sent}
    assert replies[11]['result']['success'] is False
    assert 'error' in replies[12]
    assert replies[13]['result']['success'] is True
    read_reply = replies[13]['result']['contentItems']
    assert len(read_reply) == 2
    assert read_reply[1]['text'].encode('utf-8') == (carrier.wire.PACKAGE.parents[2] / 'roles.json').read_bytes()
    actual = session.store.read().invocations[invocation]
    assert session.store._blob(actual['raw_return_blob_id']) == peer.raw.encode('utf-8')
    head = session.store.read().head
    assert carrier.carry(session, invocation, peer, directory)['completion']['status'] == 'already_committed'
    assert session.store.read().head == head
    assert peer.methods == ['thread/start', 'mcpServerStatus/list', 'turn/start']


@pytest.mark.parametrize('point', ['after_send', 'after_ack'])
def test_carrier_recovers_observed_turn_without_redispatch(ready, point):
    session, offered, directory = ready
    peer = AppServer(directory, offered['prepared'], interrupt=point)
    invocation = offered['invocation_id']
    with pytest.raises(carrier.CarrierError, match='Controlled loss'):
        carrier.carry(session, invocation, peer, directory)
    resumed = layered.LayeredSession.open(session.locator)
    peer.history, history = [], peer.history
    with pytest.raises(carrier.CarrierError, match='uncertain'):
        carrier.carry(resumed, invocation, peer, directory)
    peer.history = history
    assert carrier.carry(resumed, invocation, peer, directory)['status'] == 'returned'
    assert peer.methods == ['thread/start', 'mcpServerStatus/list', 'turn/start', 'thread/read', 'thread/read']


def test_carrier_replaces_unused_staged_thread_and_replays_cached_terminal(ready, monkeypatch):
    session, offered, directory = ready
    invocation = offered['invocation_id']
    peer = AppServer(directory, offered['prepared'])
    observe = carrier._observe_live
    with monkeypatch.context() as patch:
        def interrupted(*args):
            raise carrier.CarrierError('Before dispatch')
        patch.setattr(carrier, '_observe_live', interrupted)
        with pytest.raises(carrier.CarrierError, match='Before dispatch'):
            carrier.carry(session, invocation, peer, directory)
    assert peer.methods == ['thread/start', 'mcpServerStatus/list']
    assert carrier._observe_live is observe
    with monkeypatch.context() as patch:
        def interrupted(*args):
            raise carrier.CarrierError('After terminal capture')
        patch.setattr(session, 'complete', interrupted)
        with pytest.raises(carrier.CarrierError, match='After terminal capture'):
            carrier.carry(session, invocation, peer, directory)
    resumed = layered.LayeredSession.open(session.locator)
    assert carrier.carry(resumed, invocation, peer, directory)['status'] == 'returned'
    assert peer.methods == ['thread/start', 'mcpServerStatus/list', 'thread/start', 'mcpServerStatus/list', 'turn/start']


def test_carrier_retains_malformed_terminal_without_semantic_admission(ready):
    session, offered, directory = ready
    invocation = offered['invocation_id']
    peer = AppServer(directory, offered['prepared'], malformed=True)
    carrier.carry(session, invocation, peer, directory)
    physical = session.store.read().invocations[invocation]
    assert session.store._blob(physical['raw_return_blob_id']) == peer.raw.encode()
    assert not physical['members'][0].get('return_blob_id')
    assert session.status(invocation)['members'][0]['state'] != 'returned'


def test_stdio_roundtrips_utf8_and_rejects_unsolicited_tools(tmp_path):
    """Exercise actual local wire bytes against a disposable stdio executable."""
    executable = tmp_path / 'fake-codex'
    executable.write_text(dedent("""\
        #!/usr/bin/env python3
        import json
        import sys
        assert sys.argv[1:3] == ['app-server', '--stdio']
        assert 'mcp_servers={}' in sys.argv and 'shell_tool' in sys.argv
        def read():
            return json.loads(sys.stdin.buffer.readline())
        def send(value):
            print(json.dumps(value, ensure_ascii=False), flush=True)
        init = read()
        assert init['method'] == 'initialize' and init['params']['capabilities']['experimentalApi']
        send({'id': init['id'], 'result': {}})
        assert read() == {'method': 'initialized'}
        request = read()
        assert request['method'] == 'turn/start'
        send({'id': 991, 'method': 'unknown/tool', 'params': {}})
        denied = read()
        assert denied['id'] == 991 and 'error' in denied
        send({'id': request['id'], 'result': {'exact': request['params']['text']}})
        read()
    """), encoding='utf-8')
    executable.chmod(0o700)
    phrase = 'Exact cafe\u0301 🛠\nSecond line Ω'
    with carrier.Stdio(executable, tmp_path).open() as rpc:
        response = rpc.call('turn/start', {'text': phrase}, time.monotonic() + 5)
    assert response == {'exact': phrase}

def test_carrier_stops_an_exact_failed_turn_without_retry(ready):
    """Record a real terminal disposition, while declining semantic admission."""
    session, offered, directory = ready
    invocation = offered['invocation_id']
    peer = AppServer(directory, offered['prepared'], status='failed')
    assert carrier.carry(session, invocation, peer, directory)['status'] == 'cancelled'
    assert session.status(invocation)['state'] == 'cancelled'
    assert carrier.carry(session, invocation, peer, directory)['status'] == 'cancelled'
    assert peer.methods == ['thread/start', 'mcpServerStatus/list', 'turn/start']

def test_stdio_write_is_bounded_when_peer_stops_reading(tmp_path):
    """An unread pipe cannot strand the launcher before dispatch acknowledgment."""
    executable = tmp_path / 'stalled-codex'
    executable.write_text(dedent("""\
        #!/usr/bin/env python3
        import json
        import sys
        from threading import Event
        request = json.loads(sys.stdin.buffer.readline())
        print(json.dumps({'id': request['id'], 'result': {}}), flush=True)
        Event().wait()
    """), encoding='utf-8')
    executable.chmod(0o700)
    with carrier.Stdio(executable, tmp_path).open() as rpc:
        with pytest.raises(carrier.CarrierError, match='write deadline elapsed after partial frame') as error:
            rpc.call('turn/start', {'text': 'a' * 1048576}, time.monotonic() + 0.3)
    assert not isinstance(error.value, carrier.CarrierDeadline)


@pytest.mark.parametrize('gap', ['environment', 'mcp'])
def test_worker_controls_fail_closed_before_dispatch(ready, gap):
    """Refuse task delivery when the actual host acknowledges weaker controls."""
    session, offered, directory = ready

    class WeakHost(AppServer):
        def call(self, method, params, deadline, observe=None):
            result = super().call(method, params, deadline, observe)
            if gap == 'environment' and method == 'thread/start':
                result['thread']['environments'] = [{'id': 'ambient'}]
            if gap == 'mcp' and method == 'mcpServerStatus/list':
                result['data'] = [{'name': 'ambient'}]
            return result

    peer = WeakHost(directory, offered['prepared'])
    before = session.store.read().head
    with pytest.raises(carrier.CarrierError):
        carrier.carry(session, offered['invocation_id'], peer, directory)
    assert 'turn/start' not in peer.methods
    assert session.store.read().head == before

def test_dynamic_broker_schema_advertises_exact_closed_read():
    """A worker sees the same closed read shape that semantic admission validates."""
    from jsonschema import Draft202012Validator
    schema = carrier._tool(('software-engineer',))['inputSchema']
    validator = Draft202012Validator(schema)
    valid = {'request': {'id': 'catalogue-1', 'operation': 'read', 'handle': 'catalogue'}}
    assert not validator.is_valid({**valid, 'member_key': 'foreign'})
    assert validator.is_valid(valid)
    role_read = {'id': 'role-1', 'operation': 'read_role_instruction', 'role': 'software-engineer'}
    assert validator.is_valid({'request': role_read})
    assert not validator.is_valid({'request': {**role_read, 'role': 'unlisted'}})
    assert not validator.is_valid({'request': {**role_read, 'handle': 'instruction:software-engineer'}})
    assert not validator.is_valid({**valid, 'request': {'operation': 'read', 'handle': 'catalogue'}})
    assert not validator.is_valid({**valid, 'request': {**valid['request'], 'path': '/synthetic'}})
    assert not validator.is_valid({**valid, 'request': {'id': 'return', 'operation': 'return', 'value': {}}})

@pytest.mark.parametrize('raw', [b'cafe\xcc\x81\n', b'\xff'])
def test_read_relay_preserves_exact_text_or_binary_encoding(raw):
    """The App Server gets exact literal text without asking the model to decode base64."""
    reply = {'id': 'actual', 'ok': True, 'result': {'data': base64.b64encode(raw).decode('ascii')}}
    content = carrier._relay_items(reply, {'operation': 'read'})
    assert content == carrier._relay_items(reply, {'operation': 'read_role_instruction'})
    if raw == b'\xff':
        assert json.loads(content[0]['text']) == reply
    else:
        assert content[1]['text'].encode('utf-8') == raw

def test_selection_context_groups_exact_grants_and_preserves_full_catalogue(ready):
    """The worker gets the local mandate and model availability in one scoped read."""
    session, offered, _ = ready
    invocation = offered['invocation_id']
    member = offered['members'][0]['member_key']
    resources = offered['prepared']['model_view']['members'][0]['resources']
    session.start(invocation, 'codex', 'controlled-selection-resource', {'observed': 'controlled fixture'})
    result = session.request(invocation, member, {'id': 'selection-context', 'operation': 'read',
                                                  'handle': resources['selection_context']['handle']})
    bundled = json.loads(base64.b64decode(result['result']['data'], validate=True))
    assert 'slugs_by_category' not in bundled
    run, _ = session._member(invocation, member)
    snapshot = run.execution['snapshot']
    roles = carrier._role_choices(run.execution)
    assert roles == tuple(sorted(row['slug'] for row in snapshot['catalogue']['roles']))
    assert len(roles) == 286
    assert bundled['role_choices'] == list(roles)
    request_schema = carrier._tool(roles)['inputSchema']
    assert request_schema['properties']['request']['anyOf'][-1]['properties']['role']['enum'] == list(roles)
    assert carrier._tool(roles)['inputSchema'] is request_schema
    for slug in ('software-engineer', 'business-analyst', 'systems-analyst'):
        reply = carrier._response(session, invocation, member, {'tool': carrier.TOOL, 'arguments': {
            'request': {'id': 'instruction-' + slug, 'operation': 'read_role_instruction', 'role': slug}}})
        assert base64.b64decode(reply['result']['data'], validate=True) == snapshot['instructions'][slug]['text'].encode()
    with pytest.raises(carrier.CarrierError, match='outside the choices for this invocation phase'):
        carrier._response(session, invocation, member, {'tool': carrier.TOOL, 'arguments': {
            'request': {'id': 'unknown-role', 'operation': 'read_role_instruction', 'role': 'systems-engineer'}}})
    assert bundled['workforce']['availability']
    assert any('Exact owner-authored local task' == item['label'] for item in bundled['material_text'])
    for i, item in enumerate(bundled['material_text']):
        original = session.request(invocation, member, {'id': f'material-{i}', 'operation': 'read', 'handle': item['handle']})
        assert base64.b64decode(original['result']['data'], validate=True) == item['text'].encode()


def test_work_thread_advertises_only_the_admitted_role(ready):
    """A work thread uses the admitted role and denies unselected enum choices."""
    session, offered, directory = ready
    selection = offered['invocation_id']
    assignment = offered['members'][0]['assignment']
    carrier.carry(session, selection, AppServer(directory, offered['prepared']), directory)
    state = session.store.read()
    admitted = state.execution_plans[(assignment['version_id'], 'default')]
    issued = session.issue_batch([{'assignment': assignment, 'phase': 'work', 'selection': admitted}])
    work = issued['invocation_id']
    prepared = session.prepare(work)
    peer = AppServer(directory, prepared, malformed=True)
    peer.role_reads = ('software-engineer', 'business-analyst')
    peer.thread = 'thread-controlled-work'
    carrier.carry(session, work, peer, directory)
    assert peer.advertised_roles == ['software-engineer']
    responses = {frame['id']: frame['result'] for frame in peer.sent if frame['id'] in {20, 21}}
    assert responses[20]['success'] is True
    assert responses[21]['success'] is False


class ParallelServer:
    """Controlled App Server peer capable of multiple observed live threads."""

    def __init__(self, directory, session):
        self.directory = directory
        self.session = session
        self.thread_count = 0
        self.calls = {}
        self.sent = []
        self.methods = []
        self.frames = []
        self.quarantine_thread = None
        self.omit_final = None
        self.interleave = False

    def call(self, method, params, deadline, observe=None):
        self.methods.append(method)
        if method == 'thread/start':
            self.thread_count += 1
            if self.interleave and self.thread_count == 3:
                assert observe is not None
                observe(self.receive(deadline))
                observe(self.receive(deadline))
            return {'thread': {'id': f'thread-{self.thread_count}', 'environments': []},
                    'approvalPolicy': 'never', 'sandbox': {'type': 'readOnly', 'networkAccess': False}}
        if method == 'mcpServerStatus/list':
            return {'data': [], 'nextCursor': None}
        thread = params['threadId']
        if method == 'thread/read':
            return {'thread': {'id': thread, 'turns': [self.calls[thread]['history']]}}
        assert method == 'turn/start'
        state = self.session.store.read()
        identifier, = [key for key, row in state.invocations.items() if row['state'] == 'prepared']
        prepared = self.session.prepare(identifier)
        prompt = params['input'][0]['text']
        assert prompt == prepared['invocation']['arguments']['message']
        member = prepared['members'][0]
        turn = f'turn-{self.thread_count}'
        selection = member['packet']['execution']['phase'] == 'selection'
        raw = json.dumps({'format': 'jai.semantic-return/1', 'results': [_choice(member['packet'])]}) if selection else ''
        if thread == self.quarantine_thread:
            raw = 'invalid semantic result'
        final = {'id': f'item-{self.thread_count}', 'type': 'agentMessage', 'phase': 'final_answer', 'text': raw}
        history = {'id': turn, 'status': 'completed' if selection else 'failed',
                   'items': [{'type': 'userMessage', 'content': [{'type': 'text', 'text': prompt}]}, final]}
        self.calls[thread] = {'invocation': identifier, 'prepared': prepared, 'history': history, 'emitted': False}
        return {'turn': {'id': turn}}

    def receive(self, deadline):
        if not self.frames:
            candidates = [(thread, call) for thread, call in self.calls.items() if not call['emitted']]
            thread, call = next((item for item in reversed(candidates) if int(item[0].split('-')[1]) <= 6),
                                candidates[-1])
            call['emitted'] = True
            history = call['history']
            ids = {'threadId': thread, 'turnId': history['id']}
            if len(self.calls) == 6 and not self.sent:
                foreign = self.calls['thread-1']['prepared']['model_view']['members'][0]['resources']['selection_context']['handle']
                for request_id, handle in [(91, foreign), (92, 'catalogue')]:
                    self.frames.append({'id': request_id, 'method': 'item/tool/call',
                                        'params': {**ids, 'tool': carrier.TOOL, 'arguments': {
                                            'request': {'id': str(request_id), 'operation': 'read', 'handle': handle}}}})
            if thread != self.omit_final:
                self.frames.append({'method': 'item/completed', 'params': {**ids, 'item': history['items'][-1]}})
            self.frames.append({'method': 'turn/completed', 'params': {**ids, 'turn': history}})
        return self.frames.pop(0)

    def send(self, frame, deadline):
        self.sent.append(frame)

    def deny(self, frame, deadline):
        if 'id' in frame:
            self.sent.append({'id': frame['id'], 'error': 'denied'})


def test_parallel_driver_fills_six_slots_and_admits_out_of_order(ready):
    """Overlapping turns keep their own broker grants and independent result order."""
    session, first, directory = ready
    rpc = ParallelServer(directory, session)
    rpc.quarantine_thread = 'thread-5'
    completed = []

    class FinishedSelections(Exception):
        """The six originally ready selections reached the intended test boundary."""

    def publish(value):
        if value['status'] != 'returned':
            return
        invocation = value['invocation_id']
        member = session.prepare(invocation)['members'][0]
        if member['packet']['execution']['phase'] == 'selection':
            completed.append(invocation)
        if len(completed) == 6:
            raise FinishedSelections

    with pytest.raises(FinishedSelections):
        carrier.drive_parallel(session, rpc, directory, 6, publish)
    six_initial = [rpc.calls[f'thread-{index}']['invocation'] for index in range(1, 7)]
    assert six_initial[0] == first['invocation_id']
    assert completed == list(reversed(six_initial))
    failed = session.status(six_initial[4])['members'][0]
    assert failed['state'] == 'quarantined'
    assert all(session.status(invocation)['members'][0]['state'] == 'returned'
               for invocation in six_initial if invocation != six_initial[4])
    assert rpc.thread_count > 6
    responses = {frame['id']: frame['result'] for frame in rpc.sent}
    assert responses[91]['success'] is False and responses[92]['success'] is True
    assert responses[91]['contentItems'][0]['text'].startswith('P_SCOPE: Copy a handle verbatim')
    assert all(len(row['members']) == 1 for row in session.store.read().invocations.values())


def test_parallel_driver_cold_recovers_multiple_turns_before_new_dispatch(ready, monkeypatch):
    """After restart both original threads are observed individually without retransmission."""
    session, first, directory = ready
    rpc = ParallelServer(directory, session)
    live = carrier.carry(session, first['invocation_id'], rpc, directory, route=lambda _: False)
    second = session.next(observed_running={live.invocation: carrier._handle(live.receipt)}, max_parallel=2)
    carrier.carry(session, second['invocation_id'], rpc, directory, route=lambda _: False)
    assert rpc.methods.count('turn/start') == 2
    restarted = layered.LayeredSession.open(session.locator)
    rpc.session = restarted
    published = []
    monkeypatch.setattr(restarted, 'next', lambda **kwargs: {'status': 'waiting'})
    assert carrier.drive_parallel(restarted, rpc, directory, 2, published.append) == 0
    assert rpc.methods.count('thread/read') == 2
    assert rpc.methods.count('turn/start') == 2
    assert [row['status'] for row in published] == ['returned', 'returned', 'waiting']

def test_parallel_driver_drains_independent_turn_after_other_expires(ready, monkeypatch):
    """An expired observation blocks new work while the remaining peer can complete."""
    session, first, directory = ready
    rpc = ParallelServer(directory, session)
    original = carrier._dispatch
    live_turns = []

    def dispatch(*args, **kwargs):
        live = original(*args, **kwargs)
        live_turns.append(live)
        if len(live_turns) == 2:
            live_turns[0].deadline = time.monotonic() - 1
        return live

    monkeypatch.setattr(carrier, '_dispatch', dispatch)
    results = []
    assert carrier.drive_parallel(session, rpc, directory, 2, results.append) == 2
    assert rpc.methods.count('turn/start') == 2
    assert session.status(first['invocation_id'])['state'] == 'running'
    assert results[0]['status'] == 'returned'
    assert results[-1]['invocations'] == [first['invocation_id']]


def test_parallel_driver_routes_sibling_completion_during_thread_start(ready):
    """A pending thread RPC must not discard a completion from another thread."""
    session, _, directory = ready
    rpc = ParallelServer(directory, session)
    rpc.interleave = True

    class ObservedSibling(Exception):
        """The second turn finished during the request to create the third thread."""

    def publish(value):
        assert value['invocation_id'] == rpc.calls['thread-2']['invocation']
        assert value['status'] == 'returned' and 'thread-3' not in rpc.calls
        raise ObservedSibling

    with pytest.raises(ObservedSibling):
        carrier.drive_parallel(session, rpc, directory, 3, publish)


def test_parallel_driver_drains_independent_turn_after_missing_final(ready):
    """An incomplete transport capture preserves reconciliation for only its own turn."""
    session, first, directory = ready
    rpc = ParallelServer(directory, session)
    rpc.omit_final = 'thread-2'
    results = []
    assert carrier.drive_parallel(session, rpc, directory, 2, results.append) == 2
    assert rpc.methods.count('turn/start') == 2
    assert session.status(first['invocation_id'])['state'] == 'returned'
    assert results[-1]['invocations'] == [rpc.calls['thread-2']['invocation']]
