# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Physical invocation controls for the existing lifecycle Store.

This module derives ordinary Store effects. It owns no journal, queue, worker,
acceptance policy or alternative admission engine.
"""
from __future__ import annotations

import copy
import json

import lifecycle as lc


def _controls(state, context, live=True):
    execution = state._context_execution(context, live=live)
    assigned = state.resolve(context['assignment'], 'assignment')
    provider = (execution['snapshot']['descriptor']['bootstrap']['provider']
                if execution['phase'] == 'selection' else
                state.resolve(execution['selection'])['message']['payload']['provider'])
    effects = [{key: item[key] for key in ('operation', 'tool_policy', 'destination_handle')}
               for item in context['effects'] if item['operation'] in execution['allowed_operations']]
    effects = list({lc.canonical(item): item for item in effects}.values())
    effects.sort(key=lc.canonical)
    return {'provider': provider, 'scope': assigned['use_scope'],
            'root_generation': state._generation(context['assignment'])[0],
            'layer': assigned['owner']['layer'], 'responsibility': assigned['responsibility'],
            'phase': execution['phase'],
            'model_controls': {'model_selector': execution['model_selector'], 'model': execution['model']},
            'tool_controls': {'allowed_operations': execution['allowed_operations'], 'effects': effects}}


def _issue(state, message, origin, live):
    payload = message['payload']
    identifier = payload['invocation_id']
    if identifier in state.invocations:
        raise lc.ERROR('P_IDEMPOTENCY', 'Physical invocation identity already exists')
    contexts, common, points = [], None, {}
    bound = payload['bound_ms']
    deadline = message['expires_at_ms']
    keys, assignments = set(), set()
    for member in payload['members']:
        record = member['record']
        if member['member_key'] in keys or record['assignment']['version_id'] in assignments:
            raise lc.ERROR('P_CONFLICT', 'Invocation members require distinct exact jobs and member keys')
        keys.add(member['member_key'])
        assignments.add(record['assignment']['version_id'])
        actual = _controls(state, record, live)
        if common is not None and actual != common:
            raise lc.ERROR('P_SCOPE', 'Physical invocation members have incompatible controls or ownership')
        common = actual
        if actual['provider'] not in {'codex', 'claude'}:
            raise lc.ERROR('P_SCOPE', 'Native invocation requires the actual selected native provider')
        allowance = state._execution_allowance(record['assignment'], message['issued_at_ms'])
        if any(item['metric'] != 'elapsed_ms' or item['unit'] != 'ms' for item in allowance):
            raise lc.ERROR('P_BUDGET', 'Native calls require actual elapsed-time bounds, not invented token totals')
        bound = min(bound, *(item['ceiling'] for item in allowance),
                    record['expires_at_ms'] - message['issued_at_ms'])
        deadline = min(deadline, record['expires_at_ms'])
        assigned = state.resolve(record['assignment'], 'assignment')
        for point in state._dependencies(assigned):
            points[lc.canonical(point)] = point
        contexts.append(member)
    if not contexts or bound <= 0:
        raise lc.ERROR('P_BUDGET', 'Physical invocation requires a positive shared finite allowance')
    effects, members = [], []
    # Validate each exact grant against the same pre-call state. Root reservation
    # is emitted once, while every member receives its own whole-call lease.
    for member in contexts:
        record = copy.deepcopy(member['record'])
        record['expires_at_ms'] = min(record['expires_at_ms'], message['issued_at_ms'] + bound)
        registered, reference = state._registration(message, origin, None, 'context',
            member['logical_id'], record, live)
        for effect in registered:
            if effect['op'] == 'run':
                effect.update(invocation_id=identifier, member_key=member['member_key'])
                effect['limits'] = [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': bound}]
        effects.extend(registered)
        members.append({'member_key': member['member_key'], 'context': reference,
                        'assignment': record['assignment']})
    manifest = {**common, 'invocation_id': identifier, 'members': members,
                'input_union': [points[key] for key in sorted(points)],
                'deadline_ms': min(deadline, message['issued_at_ms'] + bound), 'bound_ms': bound,
                'state': 'issued', 'issued_at_ms': message['issued_at_ms'], 'requested_bound_ms': payload['bound_ms'],
                'limits': [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': bound}],
                'usage': {}, 'reservation_released': False}
    return effects + [{'op': 'invocation', 'invocation_id': identifier, 'value': manifest}]


def _prepare(state, message, invocation, live):
    raw = state._validation_bytes(message['payload']['manifest_blob_id'], live)
    manifest = lc.loads(raw)
    if lc.canonical(manifest) != raw:
        raise lc.ERROR('P_PARSE', 'Physical preparation requires exact canonical manifest bytes')
    fields = {'invocation_id', 'provider', 'root_generation', 'scope', 'layer', 'responsibility', 'phase',
              'model_controls', 'tool_controls', 'members', 'input_union', 'deadline_ms', 'bound_ms',
              'prompt_blob_id', 'delivery_manifest_blob_id'}
    if set(manifest) != fields:
        raise lc.ERROR('P_SCHEMA', 'Closed physical invocation manifest required')
    for key in fields - {'members', 'prompt_blob_id', 'delivery_manifest_blob_id'}:
        if manifest[key] != invocation[key]:
            raise lc.ERROR('P_ORIGIN', 'Prepared controls differ from actual issued member grants')
    expected = {item['member_key']: item for item in invocation['members']}
    if len(manifest['members']) != len(expected):
        raise lc.ERROR('P_CONFLICT', 'Preparation must pin every issued member exactly once')
    seen = set()
    for member in manifest['members']:
        if set(member) != {'member_key', 'context', 'assignment', 'packet_blob_id', 'manifest_hash'}:
            raise lc.ERROR('P_SCHEMA', 'Closed prepared member identity required')
        key = member['member_key']
        if key not in expected or key in seen or any(member[field] != expected[key][field] for field in ('context', 'assignment')):
            raise lc.ERROR('P_ORIGIN', 'Prepared member differs from issued grant')
        seen.add(key)
        packet_raw = state._validation_bytes(member['packet_blob_id'], live)
        packet = lc.loads(packet_raw)
        if (lc.canonical(packet) != packet_raw or packet.get('context') != member['context']
                or packet.get('assignment') != member['assignment'] or packet.get('member_key') != key
                or packet.get('manifest_hash') != member['manifest_hash']
                or lc._hash({name: value for name, value in packet.items() if name != 'manifest_hash'}) != member['manifest_hash']):
            raise lc.ERROR('P_ORIGIN', 'Prepared packet differs from its exact member grant')
    state._validation_bytes(manifest['prompt_blob_id'], live)
    delivery = lc.loads(state._validation_bytes(manifest['delivery_manifest_blob_id'], live))
    if (set(delivery) != {'invocation_id', 'members'} or delivery['invocation_id'] != invocation['invocation_id']
            or len(delivery['members']) != len(expected)
            or {item['member_key'] for item in delivery['members']} != set(expected)):
        raise lc.ERROR('P_ORIGIN', 'Delivery must pin the exact physical member set')
    effects = []
    for item in delivery['members']:
        if set(item) != {'member_key', 'manifest_blob_id', 'prompt_blob_id'}:
            raise lc.ERROR('P_SCHEMA', 'Closed member delivery identities required')
        state._validation_bytes(item['manifest_blob_id'], live)
        state._validation_bytes(item['prompt_blob_id'], live)
        member = next(value for value in manifest['members'] if value['member_key'] == item['member_key'])
        context = state.resolve(member['context'], 'context')
        packet_raw = state._validation_bytes(member['packet_blob_id'], live)
        packet = lc.loads(packet_raw)
        limits = packet.get('transport_limits')
        if (not isinstance(limits, dict) or set(limits) != {'packet_bytes', 'total_bytes'}
                or any(type(value) is not int for value in limits.values())
                or not 256 <= limits['packet_bytes'] <= 8388608
                or not limits['packet_bytes'] <= limits['total_bytes'] <= 33554432):
            raise lc.ERROR('P_BUDGET', 'Prepared packet requires the actual finite enrolled transport bounds')
        binding = {'provider': invocation['provider'], 'packet_blob_id': member['packet_blob_id'],
                   'manifest_hash': member['manifest_hash'], **limits, 'transferred_bytes': len(packet_raw) + 1}
        facts = state._native_packet(member['context'], context, binding,
            state._context_execution(context, live=live),
            {key: item[key] for key in ('manifest_blob_id', 'prompt_blob_id')}, live)
        effects.append({'op': 'prepared-packet', 'run_id': context['run_id'],
                        'value': {'packet_blob_id': member['packet_blob_id'],
                                  'manifest_hash': member['manifest_hash'], 'facts': facts,
                                  'transport_limits': limits, 'transferred_bytes': len(packet_raw) + 1}})
    return effects + [{'op': 'invocation-update', 'invocation_id': invocation['invocation_id'],
             'value': {'state': 'prepared', 'manifest_blob_id': message['payload']['manifest_blob_id']}}]


def derive(state, message, origin, at, live):
    """Derive one physical control event using the existing Store validators.

    Args:
        state: Existing lifecycle State under its current transaction assessment.
        message: Exact closed controller event at the normal Store boundary.
        origin: Already authenticated local controller identity.
        at: Trusted assessment time in milliseconds.
        live: Read current material for a new action; archive facts on audit replay.
    Returns:
        Atomic existing-engine effects, including one physical accounting record.
    Raises:
        ProtocolError: Issuance, compatibility, presentation, provenance or current
            member checks fail. No journal mutation occurs here.
    """
    event, payload = message['payload']['event'], message['payload']
    if event == 'invocation_issued':
        return _issue(state, message, origin, live)
    invocation = state.invocations.get(payload['invocation_id'])
    if invocation is None or invocation['scope'] != message['scope']:
        raise lc.ERROR('P_SCOPE', 'Exact issued physical invocation required')
    if event == 'invocation_prepared':
        if invocation['state'] != 'issued':
            raise lc.ERROR('P_STATE', 'Preparation is immutable and precedes any provider call')
        return _prepare(state, message, invocation, live)
    if payload['observed_at_ms'] < invocation.get('started_at_ms', invocation['issued_at_ms']) or payload['observed_at_ms'] > at + state._profile(message)['max_clock_skew_ms']:
        raise lc.ERROR('P_EXPIRED', 'Physical observation is outside its actual invocation interval')
    if event == 'invocation_started':
        return _start(state, message, origin, invocation, at, live)
    if event == 'invocation_finished':
        return _finish(state, message, origin, invocation, at, live)
    if event == 'invocation_cancelled':
        return _cancel(state, message, invocation, live)
    raise lc.ERROR('P_SCHEMA', 'Unknown physical invocation event')


def _start(state, message, origin, invocation, at, live):
    payload = message['payload']
    if ((invocation['state'] not in {'prepared', 'uncertain'} or 'started_at_ms' in invocation) or payload['provider'] != invocation['provider']
            or at >= invocation['deadline_ms']):
        raise lc.ERROR('P_STATE', 'Only a current prepared invocation may bind an actual provider handle')
    existing = state.native_handles.get((payload['provider'], payload['handle']))
    if existing is not None:
        previous_details = state.run_details[existing['run_id']]
        previous = state.invocations.get(previous_details.get('invocation_id'))
        same_jobs = previous is not None and {lc.canonical(item['assignment']) for item in previous['members']} == {
            lc.canonical(item['assignment']) for item in invocation['members']}
        controls = ('provider', 'scope', 'root_generation', 'layer', 'responsibility', 'phase',
                    'model_controls', 'tool_controls')
        if (not same_jobs or previous['state'] != 'returned'
                or any(previous[field] != invocation[field] for field in controls)):
            raise lc.ERROR('P_ORIGIN', 'Physical handle belongs to incompatible or unresolved work')
    manifest = lc.loads(state._validation_bytes(invocation['manifest_blob_id'], live))
    delivery = lc.loads(state._validation_bytes(manifest['delivery_manifest_blob_id'], live))
    capture = json.loads(state._validation_bytes(payload['capture_blob_id'], live))
    if (not isinstance(capture, dict) or 'provider_observation' not in capture
            or capture.get('host_delivery') != {'manifest_blob_id': manifest['delivery_manifest_blob_id'],
                                               'prompt_blob_id': manifest['prompt_blob_id']}):
        raise lc.ERROR('P_ORIGIN', 'Actual physical observation must bind the pinned host delivery')
    effects = []
    for member in manifest['members']:
        context = state.resolve(member['context'], 'context')
        details = state.run_details[context['run_id']]
        actual_controls = _controls(state, context, live)
        if actual_controls != {key: invocation[key] for key in actual_controls}:
            raise lc.ERROR('P_CONTEXT', 'Issued member controls changed before physical start')
        native = {'provider': payload['provider'], 'handle': payload['handle'],
                  'packet_blob_id': member['packet_blob_id'], 'capture_blob_id': payload['capture_blob_id'],
                  'manifest_hash': member['manifest_hash'], **details['prepared_packet']['transport_limits'],
                  'transferred_bytes': details['prepared_packet']['transferred_bytes']}
        local_delivery = next(item for item in delivery['members'] if item['member_key'] == member['member_key'])
        event = {**message, 'payload': {'event': 'run_started', 'run_context': member['context'],
            'run_id': context['run_id'], 'observed_at_ms': payload['observed_at_ms'], 'native': native}}
        effects.extend(state._control(event, origin, at, live,
            invocation={'invocation_id': invocation['invocation_id'], 'delivery': local_delivery}))
    effects.append({'op': 'invocation-update', 'invocation_id': invocation['invocation_id'],
                    'value': {'state': 'running', 'provider': payload['provider'], 'handle': payload['handle'],
                              'capture_blob_id': payload['capture_blob_id'], 'started_at_ms': payload['observed_at_ms']}})
    return effects


def _parse_semantic(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate semantic JSON key')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite semantic JSON')))


def _finish(state, message, origin, invocation, at, live):
    import governed_semantic
    payload = message['payload']
    if invocation['state'] not in {'running', 'uncertain', 'cancelled'} or 'started_at_ms' not in invocation or payload['codec'] != governed_semantic.CODEC:
        raise lc.ERROR('P_STATE', 'Semantic completion requires the actual running invocation and codec')
    state._validation_bytes(payload['capture_blob_id'], live)
    raw = state._validation_bytes(payload['raw_return_blob_id'], live)
    manifest = lc.loads(state._validation_bytes(invocation['manifest_blob_id'], live))
    encoded = {item['member_key']: item for item in payload['encoded_returns']}
    members = {item['member_key']: item for item in manifest['members']}
    if len(encoded) != len(payload['encoded_returns']) or set(encoded) != set(members):
        raise lc.ERROR('P_ORIGIN', 'Physical completion must account for every exact issued member once')
    attribution_error = False
    try:
        value = _parse_semantic(raw)
        if not lc.wire.validator('semantic-return.schema.json', 'attribution').is_valid(value):
            raise ValueError('Malformed semantic attribution envelope')
        keys = [item['member'] for item in value['results']]
        if len(keys) != len(set(keys)) or not set(keys) <= set(members):
            raise ValueError('Ambiguous or missing issued member attribution')
    except (ValueError, TypeError, KeyError):
        attribution_error = True
        value = None
    terminal_at = invocation['finished_at_ms'] if invocation['state'] == 'cancelled' else payload['observed_at_ms']
    elapsed = max(0, terminal_at - invocation['started_at_ms'])
    effects = []
    for key, member in members.items():
        context = state.resolve(member['context'], 'context')
        details = state.run_details[context['run_id']]
        candidate = encoded[key]['return_blob_id']
        reason = encoded[key]['error']
        if not attribution_error:
            try:
                if len(raw) > details['prepared_packet']['transport_limits']['packet_bytes']:
                    raise ValueError('Semantic physical frame exceeds the original enrolled member packet bound')
                packet = lc.loads(state._validation_bytes(member['packet_blob_id'], live))
                inline_material = set()
                def captured_material(raw_bytes):
                    identity = lc.blob(raw_bytes)
                    inline_material.add(identity)
                    return identity
                compiled = governed_semantic.compile_semantic(packet, value, captured_material)
                permitted = set(state._native_packet_facts[context['run_id']]['allowed_blobs'])
                permitted.update(details.get('broker_allowed_blobs', []))
                permitted.update(inline_material)
                if any(identifier not in permitted for proposal in compiled['records']
                       for identifier in proposal['record'].get('material', [])):
                    raise ValueError('Returned material is outside this exact member input or actual authored capture')
                expected = lc.canonical(compiled)
                if candidate is None or lc.blob(expected) != candidate:
                    raise ValueError('Encoded member is not the exact semantic compilation')
                actual = state._validation_bytes(candidate, live)
                if actual != expected:
                    raise ValueError('Encoded member bytes differ from actual semantic result')
            except (ValueError, TypeError, KeyError, lc.ERROR) as error:
                candidate, reason = None, str(error)
        else:
            candidate, reason = None, 'Ambiguous physical semantic attribution'
        local = {**message, 'request_id': message['request_id'] + ':member:' + key,
            'payload': {'event': 'run_completed', 'run_context': member['context'],
                'run_id': context['run_id'], 'observed_at_ms': payload['observed_at_ms'],
                'usage': [{'metric': 'elapsed_ms', 'unit': 'ms', 'total': elapsed}],
                'return_blob_id': candidate, 'native_handle': invocation['handle']}}
        local['message_id'] = lc.message_id(local)
        try:
            member_effects = state._control(local, origin, at, live,
                invocation={'invocation_id': invocation['invocation_id']})
        except (ValueError, OSError, lc.ERROR) as error:
            member_effects = [state._usage_effect(local['payload'], details, True),
                {'op': 'run', 'run_id': context['run_id'], 'state': 'quarantined'},
                {'op': 'quarantine', 'run_id': context['run_id'], 'return_blob_id': candidate,
                 'reason': 'Member admission failed: ' + str(error)}]
        effects.extend(member_effects)
        effects.append({'op': 'semantic-capture', 'run_id': context['run_id'], 'value': {
            'invocation_id': invocation['invocation_id'], 'member_key': key, 'codec': payload['codec'],
            'raw_return_blob_id': payload['raw_return_blob_id'], 'encoded_return_blob_id': candidate,
            'packet_blob_id': member['packet_blob_id'], 'capture_blob_id': payload['capture_blob_id'],
            'error': reason}})
    effects.append({'op': 'invocation-update', 'invocation_id': invocation['invocation_id'],
        'value': {'state': 'cancelled' if invocation['state'] == 'cancelled' else 'returned',
                  'finished_at_ms': terminal_at,
                  'capture_blob_id': payload['capture_blob_id'], 'raw_return_blob_id': payload['raw_return_blob_id'],
                  'codec': payload['codec'], 'encoded_returns': payload['encoded_returns']}})
    return effects


def _cancel(state, message, invocation, live):
    if invocation['state'] not in {'issued', 'prepared', 'running', 'uncertain'}:
        raise lc.ERROR('P_STATE', 'A terminal physical invocation cannot be cancelled')
    payload = message['payload']
    raw_capture = state._validation_bytes(payload['capture_blob_id'], live)
    try:
        observation = _parse_semantic(raw_capture)
    except (ValueError, TypeError):
        observation = {}
    confirmed = (observation.get('state') == 'terminated' if 'started_at_ms' in invocation
                 else observation.get('state') == 'not-dispatched') if isinstance(observation, dict) else False
    if not confirmed:
        return [{'op': 'invocation-update', 'invocation_id': invocation['invocation_id'],
            'value': {'state': 'uncertain', 'capture_blob_id': payload['capture_blob_id'],
                      'uncertain_at_ms': payload['observed_at_ms'], 'reason': payload['reason']}}]
    elapsed = max(0, payload['observed_at_ms'] - invocation.get('started_at_ms', payload['observed_at_ms']))
    effects = []
    for member in invocation['members']:
        context = state.resolve(member['context'], 'context')
        details = state.run_details[context['run_id']]
        observation = {'run_id': context['run_id'], 'observed_at_ms': payload['observed_at_ms'],
                       'usage': [{'metric': 'elapsed_ms', 'unit': 'ms', 'total': elapsed}]}
        effects.extend([state._usage_effect(observation, details, True),
                        {'op': 'run', 'run_id': context['run_id'], 'state': 'cancelled'}])
    return effects + [{'op': 'invocation-update', 'invocation_id': invocation['invocation_id'],
        'value': {'state': 'cancelled', 'capture_blob_id': payload['capture_blob_id'],
                  'finished_at_ms': payload['observed_at_ms'], 'reason': payload['reason']}}]
