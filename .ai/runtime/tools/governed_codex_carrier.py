#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Carry singleton layered invocations over the local Codex App Server protocol."""
from __future__ import annotations

import argparse
import base64
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import selectors
import subprocess
import tempfile
import time

import governed_delivery as wire
import governed_layered as layered
import lifecycle as lc
import operator_actions as operator

TOOL = 'jai_member_broker'
FRAME_LIMIT = 16 * 1024 * 1024
DISABLED_FEATURES = ('apps', 'browser_use', 'browser_use_external', 'hooks', 'image_generation',
                     'in_app_browser', 'memories', 'multi_agent', 'multi_agent_v2', 'plugins',
                     'remote_plugin', 'shell_tool', 'skill_mcp_dependency_install', 'skill_search',
                     'unified_exec', 'view_image')


class CarrierError(ValueError):
    """A failed or uncertain transport operation that never requests automatic redispatch."""


class CarrierDeadline(CarrierError):
    """A local RPC deadline expired."""


class InvocationError(CarrierError):
    """One invocation cannot proceed on this otherwise usable connection."""


def _encode(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False).encode('utf-8')


def _decode(raw):
    """Decode transport JSON without canonicalizing its embedded text."""
    def pairs(items):
        result = dict(items)
        if len(result) != len(items):
            raise CarrierError('Duplicate keys in App Server JSON')
        return result

    def reject_constant(_):
        raise CarrierError('Nonfinite App Server JSON number')

    return json.loads(raw.decode('utf-8', errors='strict'), object_pairs_hook=pairs, parse_constant=reject_constant)


class Stdio:
    """One initialized App Server process with bounded local JSON-line exchanges."""

    def __init__(self, binary, directory):
        self.binary = str(Path(binary).resolve(strict=True))
        self.directory = directory
        self.process = None
        self.sequence = 0
        self.buffer = bytearray()

    @contextmanager
    def open(self):
        """Start stdio and close only this owned process at exit."""
        restrictions = [flag for feature in DISABLED_FEATURES for flag in ('--disable', feature)]
        self.process = subprocess.Popen(
            [self.binary, 'app-server', '--stdio', '-c', 'mcp_servers={}',
             '-c', 'web_search="disabled"', *restrictions], cwd=self.directory,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            os.set_blocking(self.process.stdin.fileno(), False)
            self.call('initialize', {'clientInfo': {'name': 'jai_layered', 'version': '1'},
                                     'capabilities': {'experimentalApi': True}}, time.monotonic() + 30)
            self.send({'method': 'initialized'}, time.monotonic() + 30)
            yield self
        finally:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            self.process.stdin.close()
            self.process.stdout.close()

    def send(self, frame, deadline):
        """Send one complete UTF-8 frame within the same monotonic RPC deadline."""
        raw = _encode(frame) + b'\n'
        if len(raw) > FRAME_LIMIT:
            raise CarrierError('App Server output frame exceeds its bound')
        descriptor = self.process.stdin.fileno()
        data = memoryview(raw)
        with selectors.DefaultSelector() as selector:
            selector.register(descriptor, selectors.EVENT_WRITE)
            while data:
                if time.monotonic() >= deadline or not selector.select(max(0, deadline - time.monotonic())):
                    if len(data) != len(raw):
                        raise CarrierError('App Server write deadline elapsed after partial frame')
                    raise CarrierDeadline('App Server write deadline elapsed')
                try:
                    sent = os.write(descriptor, data)
                except BlockingIOError:
                    continue
                if sent == 0:
                    raise CarrierError('App Server pipe closed during write')
                data = data[sent:]

    def receive(self, deadline):
        """Read a complete UTF-8 JSON object within the monotonic deadline."""
        if time.monotonic() >= deadline:
            raise CarrierDeadline('App Server response deadline elapsed')
        with selectors.DefaultSelector() as selector:
            selector.register(self.process.stdout, selectors.EVENT_READ)
            while b'\n' not in self.buffer:
                if time.monotonic() >= deadline or not selector.select(max(0, deadline - time.monotonic())):
                    raise CarrierDeadline('App Server response deadline elapsed')
                chunk = self.process.stdout.read1(65536)
                if not chunk:
                    raise CarrierError('App Server closed before its response')
                self.buffer.extend(chunk)
                if len(self.buffer) > FRAME_LIMIT:
                    raise CarrierError('App Server input frame exceeds its bound')
        line, _, self.buffer = self.buffer.partition(b'\n')
        value = _decode(line)
        if not isinstance(value, dict):
            raise CarrierError('App Server frame is not an object')
        return value

    def deny(self, frame, deadline):
        """Reject host requests for unregistered tools and elevated privileges.

        Args:
            frame: Incoming RPC frame. Only requests receive an error response.
            deadline: Absolute monotonic deadline for writing the response.
        """
        if 'id' in frame and 'method' in frame:
            self.send({'id': frame['id'], 'error': {'code': -32601, 'message': 'Request denied by JAI'}}, deadline)

    def call(self, method, params, deadline, observe=None):
        """Send one RPC and return the result matching its request identifier.

        Args:
            method: App Server RPC method to invoke.
            params: Parameters sent with the request.
            deadline: Absolute monotonic deadline shared by the write and reads.
            observe: Optional handler for interleaved frames. By default,
                unsolicited requests are denied.
        """
        self.sequence += 1
        identifier = self.sequence
        self.send({'id': identifier, 'method': method, 'params': params}, deadline)
        while True:
            frame = self.receive(deadline)
            if frame.get('id') == identifier and 'method' not in frame:
                if 'error' in frame:
                    raise InvocationError(f'App Server denied {method}')
                return frame['result']
            if observe is None:
                self.deny(frame, deadline)
            else:
                observe(frame)


def _save(path, value):
    """Atomically persist a private correlation receipt before the next external effect."""
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.receipt-')
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(_encode(value))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        Path(temporary).unlink(missing_ok=True)


@lru_cache(maxsize=1)
def _tool():
    """Expose the maintained nonterminal broker request shapes with local references resolved."""
    schema = json.loads((wire.PACKAGE / 'broker-request.schema.json').read_bytes())
    common = json.loads((wire.PACKAGE / 'common.schema.json').read_bytes())['$defs']

    def inline(value):
        if isinstance(value, list):
            return [inline(item) for item in value]
        if not isinstance(value, dict):
            return value
        if '$ref' in value:
            return inline(common[value['$ref'].removeprefix('common.schema.json#/$defs/')])
        return {key: inline(item) for key, item in value.items()}

    requests = [inline(shape) for shape in schema['oneOf'] if shape['properties']['operation']['const'] != 'return']
    requests.append({'type': 'object', 'properties': {
        'id': {'type': 'string', 'minLength': 1},
        'operation': {'type': 'string', 'const': 'read_role_instruction'},
        'role': {'type': 'string', 'minLength': 1},
    }, 'required': ['id', 'operation', 'role'], 'additionalProperties': False})
    return {'type': 'function', 'name': TOOL,
            'description': 'Relay a closed JAI request. For read include id, operation=read and the exact handle.',
            'inputSchema': {'type': 'object', 'properties': {'request': {'anyOf': requests}},
                            'required': ['request'], 'additionalProperties': False}}


def worker_thread(rpc, deadline, model=None, *, observe=None):
    """Open a worker and require host acknowledgments before sending task text.

    Args:
        rpc: App Server peer bound to the worker directory.
        deadline: Shared absolute monotonic deadline for both requests.
        model: Optional explicit model identifier.
        observe: Optional observer forwarded to the peer.

    Returns:
        The acknowledged thread-start response after checking the MCP inventory.

    Raises:
        InvocationError: Worker isolation or absence of ambient MCP is unconfirmed.
    """
    params = {'cwd': str(rpc.directory), 'approvalPolicy': 'never', 'sandbox': 'read-only',
              'environments': [], 'dynamicTools': [_tool()], 'baseInstructions': (
                  'Follow the exact JAI task. Request resources only via jai_member_broker. '
                  'The host binds the sole member; omit member_key from tool calls. '
                  'For reads use request={id: a unique nonempty string, operation: read, handle: the exact handle}. '
                  'Use the handle from the resource descriptor, not its label, path or index. '
                  'When selection_context is present, read that handle first. It includes the exact local mandate, '
                  'model availability and handles for exact business inputs. Request only the material needed. '
                  'Use the catalogue category and page handles to discover candidate roles when needed. '
                  'Call jai_member_broker with {"request":{"id":"role-1","operation":"read_role_instruction",'
                  '"role":"<exact candidate slug>"}}. Replace the placeholder with the chosen slug. '
                  'Use the same exact slug in specialties. '
                  'Read the candidate professional instruction before returning the selection. '
                  'For the semantic envelope copy the exact member value from the sole prepared member. '
                  'Return the complete semantic envelope as the final message.')}
    if model:
        params['model'] = model
    result = rpc.call('thread/start', params, deadline, observe)
    thread = result['thread']
    sandbox = result.get('sandbox', {})
    if (thread.get('environments') != [] or result.get('approvalPolicy') != 'never'
            or sandbox.get('type') != 'readOnly' or sandbox.get('networkAccess') is not False):
        raise InvocationError('App Server did not confirm an environment-free, network-denied worker')
    inventory = rpc.call('mcpServerStatus/list', {'threadId': thread['id']}, deadline, observe)
    if inventory.get('data') != [] or inventory.get('nextCursor') is not None:
        raise InvocationError('An ambient MCP server is available to the worker')
    return result

def _matches(params, thread, turn):
    return params.get('threadId') == thread and params.get('turnId') == turn


def _role_choices(execution):
    """Use the enrolled catalogue for selection and the admitted specialties for work."""
    enrolled = execution['snapshot']['descriptor']['instruction_blobs']
    scoped = execution.get('workflow_selection')
    choices = execution.get('specialties', [])
    if execution['phase'] == 'selection':
        choices = scoped['eligible'] if scoped is not None else enrolled
    if not choices or any(role not in enrolled for role in choices):
        raise InvocationError('Worker roles must belong to the invocation catalogue')
    return tuple(sorted(choices))


def _response(session, invocation, member, params):
    arguments = params.get('arguments')
    if (params.get('tool') != TOOL or params.get('namespace') is not None or not isinstance(arguments, dict)
            or set(arguments) != {'request'}):
        raise CarrierError('Broker request does not belong to the bound member')
    request = arguments['request']
    if isinstance(request, dict) and request.get('operation') == 'read_role_instruction':
        role = request.get('role')
        if set(request) != {'id', 'operation', 'role'} or not isinstance(role, str):
            raise CarrierError('Exact role selection request required')
        run, _ = session._member(invocation, member)
        if role not in _role_choices(run.execution):
            raise CarrierError('Role is outside the choices for this invocation phase')
        request = {'id': request['id'], 'operation': 'read', 'handle': 'instruction:' + role}
    return session.request(invocation, member, request)



def _relay_items(reply, request):
    """Relay entitled UTF-8 read bytes directly and preserve the encoded result for binary data."""
    if request.get('operation') in {'read', 'read_role_instruction'}:
        raw = base64.b64decode(reply['result']['data'], validate=True)
        try:
            text = raw.decode('utf-8', errors='strict')
        except UnicodeDecodeError:
            pass
        else:
            return [
                {'type': 'inputText', 'text': 'Exact UTF-8 resource for the requested handle follows.'},
                {'type': 'inputText', 'text': text},
            ]
    return [{'type': 'inputText', 'text': _encode(reply).decode('utf-8')}]

def _handle(receipt):
    return receipt['thread'] + '/' + receipt['turn']


def _bind(session, invocation, receipt):
    status = session.status(invocation)
    if status['state'] == 'prepared':
        session.start(invocation, 'codex', _handle(receipt), {
            'transport': 'codex-app-server', 'thread_id': receipt['thread'], 'turn_id': receipt['turn']})
    elif status['handle'] != _handle(receipt):
        raise InvocationError('Store binding differs from the observed App Server turn')


def _terminal(items):
    finals = [item for item in items if item.get('type') == 'agentMessage' and item.get('phase') == 'final_answer']
    if len(finals) != 1 or not isinstance(finals[0].get('text'), str) or not isinstance(finals[0].get('id'), str):
        raise InvocationError('Exactly one typed final App Server message required')
    return finals[0]


def _finish(session, invocation, receipt, path, items, usage):
    final = _terminal(items)
    receipt.update(stage='terminal', raw=final['text'], capture={
        'transport': 'codex-app-server', 'thread_id': receipt['thread'], 'turn_id': receipt['turn'],
        'item_id': final['id'], 'app_server_usage': usage})
    _save(path, receipt)
    return session.complete(invocation, receipt['raw'], receipt['capture'])



def _stop_observed(session, invocation, receipt, path, status):
    receipt.update(stage='stopped', capture={'transport': 'codex-app-server',
                   'thread_id': receipt['thread'], 'turn_id': receipt['turn'], 'turn_status': status, 'state': 'terminated'})
    _save(path, receipt)
    return _replay_stop(session, invocation, receipt)


def _replay_stop(session, invocation, receipt):
    _bind(session, invocation, receipt)
    if session.status(invocation)['state'] != 'cancelled':
        session.stop(invocation, receipt['capture'])
    return {'status': session.status(invocation)['state']}

@dataclass
class LiveTurn:
    """Exact parent-owned Store member and App Server turn correlation."""

    invocation: str
    member: str
    receipt: dict
    path: Path
    deadline: float
    early: list
    items: list = field(default_factory=list)
    usage: dict | None = None


def _dispatch(session, invocation, member, receipt, path, rpc, prompt, args, deadline, *, route=None):
    turn_params = {'threadId': receipt['thread'], 'input': [{'type': 'text', 'text': prompt, 'textElements': []}]}
    if args.get('reasoning_effort'):
        turn_params['effort'] = args['reasoning_effort']
    run, _ = session._member(invocation, member, running=False)
    run._current(run.context_ref, issued=True)
    if time.monotonic() >= deadline:
        raise InvocationError('Prepared grant expired before App Server dispatch')
    receipt['stage'] = 'sending'
    _save(path, receipt)
    early = []

    def on_early(frame):
        if route is not None and route(frame):
            return
        params = frame.get('params', {})
        if (params.get('threadId') != receipt['thread']
                or frame.get('method') not in {'item/tool/call', 'item/completed',
                                               'thread/tokenUsage/updated', 'turn/completed'}):
            rpc.deny(frame, deadline)
            return
        if len(early) >= 64:
            raise InvocationError('Too many frames before App Server turn acknowledgment')
        early.append(frame)

    started = rpc.call('turn/start', turn_params, deadline, on_early)
    receipt.update(stage='bound', turn=started['turn']['id'])
    _save(path, receipt)
    _bind(session, invocation, receipt)
    return LiveTurn(invocation, member, receipt, path, min(deadline, session._deadline(*session._member(
        invocation, member))), early)


def _frame(session, rpc, live, frame):
    """Apply an observed frame only to its exact active turn and broker grant."""
    method, params = frame.get('method'), frame.get('params', {})
    receipt, deadline = live.receipt, live.deadline
    if method == 'item/tool/call' and 'id' in frame and _matches(params, receipt['thread'], receipt['turn']):
        try:
            result = _response(session, live.invocation, live.member, params)
            reply = {'success': True, 'contentItems': _relay_items(result, params['arguments']['request'])}
        except (ValueError, KeyError, TypeError, lc.ERROR) as error:
            code = getattr(error, 'code', 'P_SCOPE')
            arguments = params.get('arguments')
            request = arguments.get('request') if isinstance(arguments, dict) else None
            message = code
            if code == 'P_SCOPE' and isinstance(request, dict) and request.get('operation') == 'read':
                message += ': Copy a handle verbatim from the current member’s resource descriptor or role index.'
            reply = {'success': False, 'contentItems': [{'type': 'inputText', 'text': message}]}
        rpc.send({'id': frame['id'], 'result': reply}, deadline)
    elif method == 'item/completed' and _matches(params, receipt['thread'], receipt['turn']):
        item = params['item']
        if item.get('type') == 'agentMessage' and item.get('phase') == 'final_answer':
            if live.items:
                raise InvocationError('Multiple final items for one App Server turn')
            live.items.append(item)
    elif method == 'thread/tokenUsage/updated' and _matches(params, receipt['thread'], receipt['turn']):
        live.usage = params['tokenUsage']
    elif (method == 'turn/completed' and params.get('threadId') == receipt['thread']
          and params['turn']['id'] == receipt['turn']):
        if params['turn']['status'] in {'failed', 'interrupted'}:
            return _stop_observed(session, live.invocation, receipt, live.path, params['turn']['status'])
        if params['turn']['status'] != 'completed':
            raise InvocationError('App Server turn has no recognized terminal disposition')
        return _finish(session, live.invocation, receipt, live.path, live.items, live.usage)
    else:
        rpc.deny(frame, deadline)
    return None


def _observe_live(session, invocation, member, receipt, path, rpc, prompt, args, deadline):
    live = _dispatch(session, invocation, member, receipt, path, rpc, prompt, args, deadline)
    for frame in live.early:
        result = _frame(session, rpc, live, frame)
        if result is not None:
            return result
    while True:
        result = _frame(session, rpc, live, rpc.receive(live.deadline))
        if result is not None:
            return result


def _recover(session, invocation, receipt, path, rpc, prompt, deadline):
    result = rpc.call('thread/read', {'threadId': receipt['thread'], 'includeTurns': True}, deadline)
    thread = result['thread']
    if thread['id'] != receipt['thread'] or len(thread['turns']) != 1:
        raise InvocationError('Dispatch is uncertain; history does not identify exactly one turn')
    turn = thread['turns'][0]
    inputs = [item['content'] for item in turn['items'] if item.get('type') == 'userMessage']
    if (len(inputs) != 1 or len(inputs[0]) != 1 or inputs[0][0].get('type') != 'text'
            or inputs[0][0].get('text') != prompt or receipt.get('turn', turn['id']) != turn['id']):
        raise InvocationError('Recovered turn is not the exact prepared input and binding')
    receipt.update(stage='bound', turn=turn['id'])
    _save(path, receipt)
    _bind(session, invocation, receipt)
    if turn['status'] in {'failed', 'interrupted'}:
        return _stop_observed(session, invocation, receipt, path, turn['status'])
    if turn['status'] != 'completed':
        raise InvocationError('Recovered turn retains its binding and has no completed terminal result')
    return _finish(session, invocation, receipt, path, turn['items'], None)


def carry(session, invocation, rpc, directory, *, route=None):
    """Advance one pinned singleton in a fresh thread or reconcile its exact observed turn.

    The caller owns the engagement carrier lock. A sending receipt is never
    retried by dispatch. Recovery uses only the original thread and exact bytes.

    Args:
        session: Active governed singleton session.
        invocation: Exact identifier of the prepared or recorded invocation.
        rpc: App Server peer used for dispatch or reconciliation.
        directory: Private directory holding carrier correlation receipts.
        route: Optional callback that returns true for frames it handles on
            behalf of other active turns.
    """
    status = session.status(invocation)
    if not session.single_member or status['provider'] != 'codex' or len(status['members']) != 1:
        raise InvocationError('Active Codex singleton enrollment required')
    prepared = session.prepare(invocation)
    args = prepared['invocation']['arguments']
    prompt = args['message']
    prompt_id = hashlib.sha256(b'jai.lifecycle.blob.v2\0' + prompt.encode('utf-8')).hexdigest()
    if prompt_id != prepared['host_delivery']['prompt_blob_id']:
        raise InvocationError('Prepared prompt digest does not match its capture')
    path = directory / (hashlib.sha256(invocation.encode()).hexdigest() + '.json')
    try:
        receipt = _decode(operator.regular(path))
    except FileNotFoundError:
        receipt = None
    if receipt is not None and (not isinstance(receipt, dict) or receipt.get('invocation') != invocation
            or receipt.get('prompt_id') != prompt_id or receipt.get('stage') not in {'staged', 'sending', 'bound', 'terminal', 'stopped'}
            or not isinstance(receipt.get('thread'), str) or not receipt['thread']):
        raise InvocationError('Existing carrier receipt does not match prepared invocation')
    if receipt and receipt['stage'] == 'stopped':
        return _replay_stop(session, invocation, receipt)
    if receipt and receipt['stage'] == 'terminal':
        _bind(session, invocation, receipt)
        return session.complete(invocation, receipt['raw'], receipt['capture'])
    if receipt and receipt['stage'] in {'sending', 'bound'}:
        return _recover(session, invocation, receipt, path, rpc, prompt, time.monotonic() + 30)
    if status['state'] != 'prepared':
        raise InvocationError('Dispatch without a matching prepared receipt is uncertain')
    _, physical = session._invocation(invocation)
    remaining = physical['deadline_ms'] / 1000 - time.time()
    if remaining <= 0:
        raise InvocationError('Prepared grant expired before App Server dispatch')
    deadline = time.monotonic() + remaining
    # A staged thread has no dispatched turn and need not survive process exit.
    if not receipt or receipt['stage'] == 'staged':
        def observe(frame):
            if not route(frame):
                rpc.deny(frame, deadline)
        run, _ = session._member(invocation, status['members'][0]['member_key'], running=False)
        _role_choices(run.execution)
        thread = worker_thread(rpc, deadline, args.get('model'),
                               observe=observe if route else None)
        receipt = {'invocation': invocation, 'prompt_id': prompt_id, 'thread': thread['thread']['id'], 'stage': 'staged'}
        _save(path, receipt)
    member = status['members'][0]['member_key']
    if route is not None:
        return _dispatch(session, invocation, member, receipt, path, rpc, prompt, args, deadline, route=route)
    return _observe_live(session, invocation, member, receipt, path, rpc, prompt, args, deadline)



def drive_parallel(session, rpc, directory, limit, publish):
    """Fill a parent-owned FIFO with live singleton turns and serialize Store effects.

    Args:
        session: Singleton layered session owned by the launcher.
        rpc: Initialized local App Server connection.
        directory: Private receipt directory under the engagement carrier lock.
        limit: Maximum concurrent physical turns from two to six.
        publish: Callback for detached progress or a reconciliation boundary.
    Returns:
        Zero when scoped work is waiting; two when observed work needs reconciliation.
    Raises:
        CarrierError: The peer or Store cannot preserve the exact transport boundary.
    """
    if type(limit) is not int or not 2 <= limit <= 6:
        raise ValueError('Parallel carrier requires a limit between two and six')
    fifo = []
    active = {}
    blocked = []

    def report(invocation, result):
        publish({'invocation_id': invocation, 'status': result['status'],
                 'progress': session.checkpoint()['progress']})

    def route(frame):
        params = frame.get('params', {})
        thread, turn = params.get('threadId'), params.get('turnId')
        if frame.get('method') == 'turn/completed':
            turn = params.get('turn', {}).get('id')
        key = (thread, turn)
        live = active.get(key)
        if live is None:
            return False
        if time.monotonic() >= live.deadline:
            return False
        try:
            result = _frame(session, rpc, live, frame)
        except (InvocationError, CarrierDeadline, lc.ERROR):
            del active[key]
            blocked.append(live.invocation)
            return True
        if result is not None:
            del active[key]
            report(live.invocation, result)
            if result['status'] != 'returned':
                blocked.append(live.invocation)
        return True

    def expire():
        now = time.monotonic()
        for key, live in list(active.items()):
            if live.deadline <= now:
                del active[key]
                blocked.append(live.invocation)

    # A cold parent has no active handles. Consult each ambiguous receipt
    # before using capacity. Dispatch of a merely issued call remains deferred.
    prior = [row['invocation_id'] for row in session.checkpoint()['invocations']
             if row['state'] in {'prepared', 'uncertain', 'running'}]
    for invocation in prior:
        path = directory / (hashlib.sha256(invocation.encode()).hexdigest() + '.json')
        try:
            receipt = _decode(operator.regular(path))
        except FileNotFoundError:
            continue
        if receipt.get('stage') in {'sending', 'bound', 'terminal', 'stopped'}:
            try:
                result = carry(session, invocation, rpc, directory)
            except (InvocationError, CarrierDeadline, lc.ERROR):
                blocked.append(invocation)
                continue
            report(invocation, result)
            if result['status'] != 'returned':
                blocked.append(invocation)

    while True:
        expire()
        offered = None
        if not blocked:
            handles = {live.invocation: _handle(live.receipt) for live in active.values()}
            offered = session.next(observed_running=handles, max_parallel=limit, ready_queue=fifo)
            if offered['status'] == 'reconcile':
                # A prepared single turn without a sending receipt is safe to
                # stage; the carry routine still has the dispatch boundary.
                if offered.get('physical_state') != 'prepared':
                    blocked.append(offered['invocation_id'])
                else:
                    offered = {**offered, 'status': 'invoke'}
            if offered['status'] == 'invoke' and not blocked:
                invocation = offered['invocation_id']
                try:
                    live = carry(session, invocation, rpc, directory, route=route)
                except (InvocationError, CarrierDeadline, lc.ERROR):
                    blocked.append(invocation)
                    continue
                if isinstance(live, LiveTurn):
                    key = live.receipt['thread'], live.receipt['turn']
                    if key in active:
                        raise CarrierError('Duplicate active App Server binding')
                    active[key] = live
                    for frame in live.early:
                        if not route(frame):
                            rpc.deny(frame, live.deadline)
                else:
                    report(invocation, live)
                    if live['status'] != 'returned':
                        blocked.append(invocation)
                continue
        if not active:
            if blocked:
                publish({'status': 'reconcile', 'invocations': blocked,
                         'reason': 'App Server turns need exact reconciliation'})
                return 2
            publish(offered)
            return 0
        deadline = min(live.deadline for live in active.values())
        try:
            frame = rpc.receive(deadline)
        except CarrierDeadline:
            if time.monotonic() < deadline:
                raise
            expire()
            continue
        if not route(frame):
            rpc.deny(frame, max(live.deadline for live in active.values()))


def main(argv=None):
    """Start or resume an ordinary JAI engagement using the singleton Codex transport.

    Args:
        argv: Command arguments without the program name. Defaults to the
            current process arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', required=True, type=Path)
    parser.add_argument('--parallel', type=int, choices=range(1, 7), default=1)
    actions = parser.add_subparsers(dest='action', required=True)
    start = actions.add_parser('start')
    start.add_argument('--home', type=Path, default=Path('.fabric'))
    start.add_argument('--engagement', required=True)
    start.add_argument('--work-item', required=True)
    start.add_argument('--task', required=True, type=Path)
    start.add_argument('--limit-ms', type=int)
    start.add_argument('--sabsa-row-mode', choices=lc.ROW_MODES)
    start.add_argument('--sabsa-row-modes', type=Path)
    start.add_argument('--question-dependencies', type=Path)
    resume = actions.add_parser('resume')
    resume.add_argument('--session', required=True, type=Path)
    args = parser.parse_args(argv)
    binary = args.codex.resolve(strict=True)
    if args.action == 'start':
        session, _ = layered.LayeredSession.create(
            args.home, args.engagement, operator.regular(args.task), 'codex', args.work_item,
            limit_ms=args.limit_ms, single_member=True, sabsa_row_mode=args.sabsa_row_mode,
            sabsa_row_modes=lc.loads(operator.regular(args.sabsa_row_modes)) if args.sabsa_row_modes else None,
            question_dependencies=lc.loads(operator.regular(args.question_dependencies)) if args.question_dependencies else None)
    else:
        session = layered.LayeredSession.open(args.session)
    if not session.single_member:
        raise CarrierError('App Server launcher requires an existing singleton session')
    directory = session.locator.with_suffix('.app-server')
    directory.mkdir(mode=0o700, exist_ok=True)
    if directory.is_symlink() or directory.stat().st_mode & 0o077:
        raise CarrierError('Private carrier receipt directory required')
    # Lock the private carrier, rather than the Store journal. Ordinary Store
    # transactions keep their own short locks and check the current grants.
    with lc.store_lock(directory / 'driver'), tempfile.TemporaryDirectory(prefix='jai-codex-worker-') as work:
        with Stdio(binary, work).open() as rpc:
            if args.parallel > 1:
                return drive_parallel(session, rpc, directory, args.parallel,
                                      lambda value: print(_encode(value).decode(), flush=True))
            while True:
                offered = session.next()
                if offered['status'] not in {'invoke', 'reconcile'}:
                    print(_encode(offered).decode(), flush=True)
                    return 0
                invocation = offered['invocation_id']
                outcome = carry(session, invocation, rpc, directory)
                print(_encode({'invocation_id': invocation, 'status': outcome['status'],
                               'progress': session.checkpoint()['progress']}).decode(), flush=True)
                if outcome['status'] != 'returned':
                    return 2


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(_encode({'status': 'reconcile', 'error': str(error)}).decode(), flush=True)
        raise SystemExit(2)
