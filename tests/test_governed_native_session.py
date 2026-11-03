# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Actual shared Store, native-origin and durable physical-effect boundaries."""
import base64
import json
import io
import subprocess
import sys

import pytest

from governed_fixtures import lc, ROOT
from test_governed_dispatch import _ElapsedHarness, _worker_config
import governed_native as native
import governed_dispatch as dispatch


@pytest.fixture
def prepared(tmp_path, monkeypatch):
    host = _ElapsedHarness(tmp_path / 'engagement', monkeypatch, engagement='native-contract')
    host.dispatch_directory, host.dispatch_case, host.dispatch_mode = tmp_path, 'native_contract', None
    host.bootstrap()
    actor = host.setup_author(start_author=False)
    selection = _selection(host, actor)
    config, _, output = _worker_config(tmp_path / 'host-tools', host, actor)
    config['limits'] = {'packet_bytes': 2000000, 'total_bytes': 8000000}
    session = native.NativeSession(host.store, config)
    issued = _issue(session, actor['author'], selection)
    session.start(issued['invocation_id'], 'codex', 'actual-native-handle', {'tool': 'spawn_agent', 'agent_id': 'actual-native-handle', 'observed_seconds': 0.25})
    return host, actor, config, output, session, issued, selection


def _selection(host, actor):
    context = host.context('choice-' + str(host.sequence), actor['author'], actor['author_record'], phase='selection')
    models = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_bytes())
    choice = {'action': 'select_execution', 'assignment': actor['author'],
        'previous': host.store.read().execution_plans.get((actor['author']['version_id'], host.scope)),
        'specialties': ['software-engineer'], 'provider': 'codex', 'workload_class': 'standard',
        'model_selector': models['providers']['codex']['classes']['standard']['model_selector'],
        'reason': 'Use the active provider native subagent for the assigned work.', 'authority_proof': None}
    receipt = host.commit(host.message('decision', choice, sender=actor['principal'], context=context))
    state = host.store.read()
    selection = next(ref for ref in receipt['created_versions'] if state.versions[ref['version_id']]['kind'] == 'delivery.decision')
    return selection


def _issue(session, assignment, selection):
    issued = session.issue_batch([{'assignment': assignment, 'phase': 'work', 'selection': selection}], bound_ms=5000)
    descriptor = session.prepare(issued['invocation_id'])
    member = descriptor['members'][0]
    return {**issued, 'context': member['context'], 'packet': member['packet'], 'member_key': member['member_key']}


def _request(session, issued, identifier, operation, **fields):
    return session.request(issued['invocation_id'], issued['member_key'],
                           {'id': identifier, 'operation': operation, **fields})['result']


def _body(host, actor, issued, blob, identifier='native-answer'):
    product = {'owner': actor['owner'], 'product_kind': 'answer', 'assignment': actor['author'],
        'profile': host.profile, 'inputs': actor['author_record']['inputs'], 'material': [blob],
        'evidence': [], 'related': [], 'limitations': []}
    ref = host.ref(identifier, 'product', product)
    value = {'format': 'jai.semantic-return/1', 'results': [{'member': issued['member_key'],
        'kind': 'author', 'logical_id': identifier, 'materials': [{'blob': blob}],
        'evidence': [], 'limitations': []}]}
    return json.dumps(value), product, ref


def test_intrinsic_full_catalogue_reference_and_exact_native_return(prepared):
    host, actor, config, output, session, issued, _ = prepared
    catalogue = json.loads(base64.b64decode(_request(session, issued, 'catalogue', 'read', handle='catalogue')['data']))
    row = next(item for item in catalogue['roles'] if item['slug'] != 'software-engineer' and 'sabsa' not in item['slug'])
    instruction = base64.b64decode(_request(session, issued, 'instruction', 'read', handle='instruction:' + row['slug'])['data'])
    assert instruction == (ROOT / '.ai/skills' / row['skill'] / 'references' / (row['slug'] + '.md')).read_bytes()
    proposed = _request(session, issued, 'propose', 'propose', data=base64.b64encode(b'Actual native output').decode())
    body, product, ref = _body(host, actor, issued, proposed['blob_id'])
    built = _request(session, issued, 'reference', 'reference', logical_id='native-answer', record_type='product', record=product)
    assert built['ref'] == ref
    assert ref['version_id'] not in host.store.read().versions
    result = session.complete(issued['invocation_id'], body, {'tool': 'wait', 'status': 'completed'})
    assert result['status'] == 'returned'
    assert host.store.read().resolve(ref, 'product') == product
    head = host.store.read().head
    duplicate = session.complete(issued['invocation_id'], body, {'tool': 'wait', 'status': 'completed'})
    assert duplicate['completion']['status'] == 'already_committed' and host.store.read().head == head
    assert not host.store.evaluate(ref)['accepted']
    state = host.store.read()
    parent = state.resolve(actor['setter'], 'assignment')
    feedback = session.workflow.dispatcher._owned_returns(state, actor['setter'], parent,
                                                          state.ready_basis(actor['setter']))
    returned = next(item for item in feedback if item['assignment'] == actor['author'])
    assert returned['records'][0]['ref'] == ref
    assert returned['records'][0]['record'] == product
    assert base64.b64decode(returned['records'][0]['material'][0]['data']) == b'Actual native output'
    assert returned['intents'][0]['message_type'] == 'submission'
    assert returned['intents'][0]['payload']['candidate'] == ref


def test_origin_isolation_interleaved_contexts_and_terminal_validation(prepared):
    host, actor, config, output, session, issued, selection = prepared
    other_actor = host.setup_author(suffix='B', start_author=False)
    other = _issue(session, other_actor['author'], _selection(host, other_actor))
    with pytest.raises((lc.ERROR, dispatch.DispatchError)):
        session.start(other['invocation_id'], 'codex', 'actual-native-handle', {'tool': 'spawn_agent'})
    session.start(other['invocation_id'], 'codex', 'second-handle', {'tool': 'spawn_agent'})
    one = _request(session, issued, 'same-id', 'propose', data=base64.b64encode(b'First run only').decode())
    two = session.request(other['invocation_id'], other['member_key'], {'id': 'same-id', 'operation': 'propose', 'data': base64.b64encode(b'Second run only').decode()})['result']
    assert one['blob_id'] != two['blob_id']
    with pytest.raises(dispatch.DispatchError, match='Member'):
        session.request(issued['invocation_id'], 'not-issued', {'id': 'wrong', 'operation': 'read', 'handle': 'catalogue'})
    body, _, ref = _body(host, actor, issued, two['blob_id'])
    rejected = session.complete(issued['invocation_id'], body, {'tool': 'wait'})
    assert rejected['status'] == 'returned'
    assert host.store.read().run_states[issued['packet']['run_id']] == 'quarantined'
    assert ref['version_id'] not in host.store.read().versions
    with pytest.raises((lc.ERROR, dispatch.DispatchError, ValueError)):
        session.complete(issued['invocation_id'], '{"not":"a return"}', {'tool': 'wait'})
    assert session.status(issued['invocation_id'])['state'] == 'returned'


def test_physical_intent_ack_exact_retry_and_cold_resume_without_reexecution(prepared, monkeypatch):
    host, actor, config, output, session, issued, selection = prepared
    proposed = _request(session, issued, 'bytes', 'propose', data=base64.b64encode(b'Physical output').decode())
    calls = []
    original = dispatch.Dispatcher._materialize
    def materialize(self, assignment, request):
        details = host.store.read().run_details[issued['packet']['run_id']]
        assert details['broker_requests']['write']['status'] == 'pending'
        calls.append(request['blob_id'])
        return original(self, assignment, request)
    monkeypatch.setattr(dispatch.Dispatcher, '_materialize', materialize)
    request = {'id': 'write', 'operation': 'materialize', 'subject': host.input_a,
               'blob_id': proposed['blob_id'], 'destination_handle': 'owned-output'}
    result = session.request(issued['invocation_id'], issued['member_key'], request)
    files = [path for path in output.rglob('*') if path.is_file()]
    assert len(files) == 1 and files[0].read_bytes() == b'Physical output'
    cold = native.NativeSession(lc.Store(host.path, host.engagement), config)
    assert cold.request(issued['invocation_id'], issued['member_key'], request) == result
    assert calls == [proposed['blob_id']]
    with pytest.raises(dispatch.DispatchError) as conflict:
        cold.request(issued['invocation_id'], issued['member_key'], {**request, 'blob_id': '0' * 64})
    assert conflict.value.code == 'P_IDEMPOTENCY'
    counter = []
    def measure(self, request, packet, deadline):
        assert self.store.read().run_details[packet['run_id']]['broker_requests']['measure']['status'] == 'pending'
        counter.append(1)
        return {'blob_id': self.store.put_blob(b'Actual measurement result'), 'status': 0}
    monkeypatch.setattr(dispatch.Dispatcher, '_measure', measure)
    measurement = {'id': 'measure', 'operation': 'measure', 'tool_policy': host.criteria, 'targets': [host.input_a]}
    first = cold.request(issued['invocation_id'], issued['member_key'], measurement)
    assert cold.request(issued['invocation_id'], issued['member_key'], measurement) == first
    assert counter == [1]
    assert cold.request(issued['invocation_id'], issued['member_key'], request) == result
    assert calls == [proposed['blob_id']]
    before = cold.store.read().run_details[issued['packet']['run_id']]['broker_bytes']
    assert before >= session.store.read().run_details[issued['packet']['run_id']]['broker_bytes']


def test_unacknowledged_effect_never_repeats_and_cancel_allows_fresh_work(prepared, monkeypatch):
    host, actor, config, output, session, issued, selection = prepared
    blob = _request(session, issued, 'bytes', 'propose', data=base64.b64encode(b'One actual write').decode())['blob_id']
    observe = dispatch.Dispatcher._broker_observation
    def interrupted(self, context, event, request_blob, result_blob=None):
        if event == 'broker_observed' and result_blob is not None:
            raise RuntimeError('Simulated host death after the physical effect')
        return observe(self, context, event, request_blob, result_blob)
    request = {'id': 'write', 'operation': 'materialize', 'subject': host.input_a, 'blob_id': blob, 'destination_handle': 'owned-output'}
    with monkeypatch.context() as scoped:
        scoped.setattr(dispatch.Dispatcher, '_broker_observation', interrupted)
        with pytest.raises(RuntimeError):
            session.request(issued['invocation_id'], issued['member_key'], request)
    assert [p.read_bytes() for p in output.rglob('*') if p.is_file()] == [b'One actual write']
    resumed = native.NativeSession(lc.Store(host.path, host.engagement), config)
    with pytest.raises(dispatch.DispatchError) as uncertain:
        resumed.request(issued['invocation_id'], issued['member_key'], request)
    assert uncertain.value.code == 'P_UNCERTAIN'
    resumed.stop(issued['invocation_id'], {'state': 'terminated', 'tool': 'close_agent', 'status': 'observed'})
    fresh = _issue(resumed, actor['author'], selection)
    with pytest.raises((lc.ERROR, dispatch.DispatchError)):
        resumed.start(fresh['invocation_id'], 'codex', 'actual-native-handle', {'tool': 'spawn_agent'})
    resumed.start(fresh['invocation_id'], 'codex', 'fresh-handle', {'tool': 'spawn_agent'})
    assert resumed.request(fresh['invocation_id'], fresh['member_key'], {'id': 'new', 'operation': 'propose', 'data': base64.b64encode(b'Reconciled next work').decode()})['ok']


def test_late_cancelled_return_records_history_without_semantic_admission(prepared):
    host, actor, config, output, session, issued, selection = prepared
    blob = _request(session, issued, 'bytes', 'propose', data=base64.b64encode(b'Late output').decode())['blob_id']
    body, product, ref = _body(host, actor, issued, blob)
    session.stop(issued['invocation_id'], {'state': 'terminated', 'tool': 'close_agent', 'status': 'observed'})
    result = session.complete(issued['invocation_id'], body, {'tool': 'wait', 'status': 'completed'})
    state = host.store.read()
    assert ref['version_id'] not in state.versions
    assert any(event['kind'] == 'quarantine' for event in state.events) and result['completion']['status'] == 'committed'
    fresh = _issue(session, actor['author'], selection)
    session.start(fresh['invocation_id'], 'codex', 'bounded-handle', {'tool': 'spawn_agent'})
    head = host.store.read().head
    with pytest.raises(dispatch.DispatchError) as oversized:
        session.request(fresh['invocation_id'], fresh['member_key'],
            {'id': 'oversized', 'operation': 'propose', 'data': 'A' * config['limits']['packet_bytes']})
    assert oversized.value.code == 'P_BUDGET' and host.store.read().head == head
    proposed = session.request(fresh['invocation_id'], fresh['member_key'],
        {'id': 'bounded', 'operation': 'propose', 'data': base64.b64encode(b'Bounded actual output').decode()})['result']
    large, _, large_ref = _body(host, actor, fresh, proposed['blob_id'], 'oversized-terminal')
    large += ' ' * config['limits']['packet_bytes']
    captured = session.complete(fresh['invocation_id'], large,
                               {'tool': 'wait', 'status': 'completed'})
    state = host.store.read()
    assert captured['status'] == 'returned' and state.run_states[fresh['packet']['run_id']] == 'quarantined'
    assert large_ref['version_id'] not in state.versions
    assert state.run_details[fresh['packet']['run_id']]['reservation_released']


def test_foreground_stdio_retains_store_and_releases_lock_between_commands(prepared, tmp_path):
    host, actor, config, output, session, issued, selection = prepared
    config_path = tmp_path / 'host-config.json'
    config_path.write_text(json.dumps(config))
    process = subprocess.Popen([sys.executable, str(ROOT / '.ai/runtime/tools/governed_native.py'),
        '--store', str(host.path), '--engagement', host.engagement, '--config', str(config_path)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    def command(identifier, operation, **fields):
        process.stdin.write(json.dumps({'id': identifier, 'operation': operation, **fields}) + '\n')
        process.stdin.flush()
        return json.loads(process.stdout.readline())
    try:
        first = command('state', 'status', invocation=issued['invocation_id'])
        assert first['ok'] and first['result']['state'] == 'running'
        session.stop(issued['invocation_id'], {'state': 'terminated', 'tool': 'close_agent', 'status': 'observed'})
        second = command('state-2', 'status', invocation=issued['invocation_id'])
        assert second['ok'] and second['result']['state'] == 'cancelled'
        assert command('close', 'close')['ok']
        assert process.wait(timeout=10) == 0
    finally:
        if process.poll() is None:
            process.kill()
        process.communicate(timeout=10)

    source = io.BytesIO(b'x' * (config['limits']['packet_bytes'] + 1) + b'\n' +
                        b'{"id":"suffix","operation":"close"}\n')
    responses = io.StringIO()
    assert native.serve(session, source, responses) == 1
    frames = [json.loads(line) for line in responses.getvalue().splitlines()]
    assert len(frames) == 1 and frames[0]['error']['code'] == 'P_BUDGET'
