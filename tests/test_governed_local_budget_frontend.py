# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Native front-door local budgets without a fabricated aggregate task deadline."""
import io
import json
from pathlib import Path
import sys
import time

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import governed_layered as layered
import governed_native as native
import governed_native_provider as provider
import governed_semantic as semantic
import lifecycle as lc


def _question_session(home, engagement):
    """Build a synthetic exact question root through ordinary bootstrap/admission."""
    home = Path(home).resolve()
    work_item = 'status-communication'
    store = lc.Store(home / (engagement + '.jsonl'), engagement)
    initialized = provider.bootstrap(store, b'Describe minimal incident-status information without personal data.',
        b'Identify the required information and state genuine uncertainty.', 'codex', work_item, [], None)
    config = initialized['config']
    locator = layered._save_locator(home, engagement, config)
    session = layered.LayeredSession(store, config, locator)
    state = store.read()
    profile = initialized['profile']
    policy = state.capability_policy(profile)
    owner = {'layer': 1, 'work_kind': 'question', 'question': 'what', 'work_item': work_item}
    slots = [item for item in state.resolve(profile, 'profile')['obligations']
             if item['owner'] == owner and item['role'] == 'input']
    if len(slots) != 1:
        raise ValueError('The actual profile must declare one exact L1 What input slot')
    inputs = [reference for (scope, _), reference in state.sources.items()
              if scope == 'default' and state.resolve(reference, 'source')['source_role'] != 'policy']
    inputs.append(policy['ref'])
    record = {'owner': owner, 'responsibility': 'setter', 'assigned_actor': 'c4-local-question-setter',
        'profile': profile, 'routing': {'policy': policy['ref']}, 'inherited': inputs,
        'inputs': [{'slot_id': slots[0]['slot_id'] if reference == initialized['sources']['request']
                    else 'l0:' + reference['logical_id'], 'refs': [reference]} for reference in inputs],
        'criteria': initialized['sources']['criteria'], 'effects': [], 'limits': [],
        'deadline_ms': None, 'use_scope': 'default', 'issued_under': None, 'input_uses': []}
    for path, reference in lc._reference_paths(record):
        if path.startswith(('/inherited/', '/inputs/')) or path == '/criteria':
            record['input_uses'].append({'at': path, 'use_scope': policy['use_scope']
                                        if reference == policy['ref'] else 'default'})
        elif path == '/routing/policy':
            record['input_uses'].append({'at': path, 'use_scope': policy['use_scope']})
    available = state.assignment_routing(record, live=True)
    record['effects'] = [{**effect, 'owner': owner,
        'targets': [] if effect['operation'] == 'propose' else list(inputs)}
        for effect in available['capabilities']['effects']]
    # Admission remains the existing controller record-proposal/root-basis gate.
    assignment, receipt = session.workflow._record('default', profile,
        {'record_type': 'assignment', 'logical_id': 'c4-l1-what-setter', 'record': record})
    return session, {'locator': str(locator), 'assignment': assignment, 'receipt': receipt,
                     'inputs': initialized['sources'], 'scope': 'one controlled question fixture only'}


def _session(tmp_path, local_budget=None):
    return layered.LayeredSession.create(tmp_path, 'local-front',
        b'Describe the business information needed for a status event.', 'codex', 'status',
        local_budget=local_budget)


def test_default_front_door_has_local_allowance_and_only_finite_grants(tmp_path):
    session, created = _session(tmp_path)
    root = created['entry']['assignment']
    state = session.store.read()
    assignment = state.resolve(root, 'assignment')
    profile = state.resolve(assignment['profile'], 'profile')
    assert assignment['deadline_ms'] is None and assignment['limits'] == []
    assert profile['local_budget'] == {'iteration_ms': 600000, 'max_reworks': 3}
    assert profile['scheduling']['initial_deadline_ms'] is None
    assert profile['scheduling']['max_search_steps'] is None
    assert 'rework_limit' not in profile and 'reformulation_limit' not in profile
    offered = session.next()
    packet = offered['prepared']['members'][0]['packet']
    context = session.store.read().resolve(packet['context'], 'context')
    assert isinstance(context['expires_at_ms'], int)
    budget = session.local_budget_status(root)
    assert budget['remaining_ms'] == 600000 and budget['deadline_ms'] is None
    view = offered['prepared']['model_view']['members'][0]
    assert view['bounds']['deadline_ms'] is None and view['bounds']['limits'] == []
    assert view['bounds']['effective_deadline_ms'] == context['expires_at_ms']


def test_timeout_notice_extension_and_operational_stop_use_actual_instruction(tmp_path, monkeypatch):
    clock = [time.time()]
    monkeypatch.setattr(time, 'time', lambda: clock[0])
    session, created = _session(tmp_path, {'iteration_ms': 1000, 'max_reworks': 1})
    consumer = native.NativeSession(session.store, session.workflow.dispatcher.config)
    root = created['entry']['assignment']
    offered = session.next()
    invocation = offered['invocation_id']
    pending = consumer.local_budget_status(root)
    session.start(invocation, 'codex', 'controlled-local-window', {'observed': 'Actual controlled physical start.'})
    active = consumer.local_budget_status(root)
    assert active['deadline_ms'] == int(clock[0] * 1000) + 1000
    clock[0] += 2
    notice = session.next()
    assert notice['operator_notices']
    paused = consumer.local_budget_status(root)
    assert paused['state'] == 'paused'
    assert not session.store.read().episodes
    session.stop(invocation, {'state': 'terminated', 'observed': 'Controlled actual stop after timeout.'})
    instruction = session.store.put_blob(b'The operator explicitly grants one additional second to this paused local unit.')
    with pytest.raises(ValueError):
        consumer.extend_local_budget(paused['unit_id'], paused['revision'] - 1, 1000, instruction)
    consumer.extend_local_budget(paused['unit_id'], paused['revision'], 1000, instruction)
    extended = consumer.local_budget_status(root)
    assert extended['deadline_ms'] is None and extended['remaining_ms'] == 1000
    assert extended['iteration'] == pending['iteration'] and extended['reworks_used'] == 0
    with pytest.raises(ValueError):
        session.start(invocation, 'codex', 'revived-expired-context', {'observed': 'No new grant.'})
    stop_instruction = session.store.put_blob(b'The operator explicitly stops this local unit without a business verdict.')
    consumer.stop_local_budget(extended['unit_id'], extended['revision'], 'unit', 'Actual operational stop.', stop_instruction)
    assert consumer.local_budget_status(root)['state'] == 'terminated'
    assert consumer.pause_due('default')['notices']


def test_cli_optional_global_bounds_and_explicit_local_configuration(tmp_path, monkeypatch, capsys):
    task = tmp_path / 'task.txt'
    task.write_text('Describe the business information needed for a status event.')
    monkeypatch.setattr(sys, 'stdin', io.TextIOWrapper(io.BytesIO(b'{"id":"close","operation":"close"}\n')))
    assert layered.main(['start', '--home', str(tmp_path / 'host'), '--engagement', 'cli-local',
        '--task', str(task), '--provider', 'codex', '--work-item', 'status',
        '--iteration-ms', '10000', '--max-reworks', '1']) == 0
    startup = json.loads(capsys.readouterr().out.splitlines()[0])
    locator = startup['result']['created']['locator']
    session = layered.LayeredSession.open(locator)
    root = startup['result']['created']['entry']['assignment']
    assigned = session.store.read().resolve(root, 'assignment')
    profile = session.store.read().resolve(assigned['profile'], 'profile')
    assert assigned['deadline_ms'] is None and assigned['limits'] == []
    assert profile['local_budget'] == {'iteration_ms': 10000, 'max_reworks': 1}


def test_operational_cli_captures_exact_user_instruction_without_a_signature(tmp_path, monkeypatch, capsys):
    clock = [time.time()]
    monkeypatch.setattr(time, 'time', lambda: clock[0])
    session, created = _session(tmp_path / 'case', {'iteration_ms': 1000, 'max_reworks': 1})
    offered = session.next()
    session.start(offered['invocation_id'], 'codex', 'controlled-cli-window', {'observed': 'Actual controlled start.'})
    clock[0] += 2
    session.pause_due('default')
    session.stop(offered['invocation_id'], {'state': 'terminated', 'observed': 'Actual controlled termination.'})
    unit = session.local_budget_status(created['entry']['assignment'])
    actual = b'The operator grants exactly one additional second to this paused local unit.'
    instruction = tmp_path / 'operator-instruction.txt'
    instruction.write_bytes(actual)
    assert layered.main(['budget-status', '--session', created['locator'], '--unit-id', unit['unit_id']]) == 0
    assert json.loads(capsys.readouterr().out)['result']['state'] == 'paused'
    assert layered.main(['extend-budget', '--session', created['locator'], '--unit-id', unit['unit_id'],
        '--expected-revision', str(unit['revision']), '--additional-ms', '1000',
        '--operator-instruction', str(instruction)]) == 0
    assert json.loads(capsys.readouterr().out)['result']['status'] == 'committed'

    resumed = layered.LayeredSession.open(created['locator'])
    extended = resumed.local_budget_status(unit['unit_id'])
    payload = next(message['payload'] for message in resumed.store.read().messages.values()
                   if message['payload'].get('event') == 'local_budget_extend')
    assert payload['operator_instruction_ref'] == lc.blob(actual)
    assert 'authority_proof' not in payload
    instruction.write_bytes(b'The operator explicitly stops this task without declaring a business outcome.')
    assert layered.main(['stop-budget', '--session', created['locator'], '--unit-id', unit['unit_id'],
        '--expected-revision', str(extended['revision']), '--target', 'task', '--reason', 'Actual operator stop.',
        '--operator-instruction', str(instruction)]) == 0
    assert json.loads(capsys.readouterr().out)['result']['status'] == 'committed'


def test_public_owner_issue_after_substantive_denial_preserves_exact_question_root(tmp_path):
    from test_governed_native_batches import _choice, _role_result
    session, created = _question_session(tmp_path / 'case', 'controlled-owner-handoff')
    root = created['assignment']
    before = session.store.read().head
    resumed = layered.LayeredSession.open(created['locator'])
    assert resumed.store.read().head == before
    assert resumed.checkpoint()['roots'] == [root]
    with pytest.raises(ValueError, match='empty engagement'):
        _question_session(tmp_path / 'case', 'controlled-owner-handoff')
    denied, owner_plan = None, None
    for _ in range(8):
        try:
            offered = session.next()
        except ValueError as error:
            assert getattr(error, 'code', None) == 'P_PROOF'
            assert 'Required named criterion evidence' in str(error)
            denied = error
            break
        assert offered['status'] == 'invoke', offered
        packets = [member['packet'] for member in offered['prepared']['members']]
        results = []
        for packet in packets:
            assigned = session.store.read().resolve(packet['assignment'], 'assignment')
            if packet['execution']['phase'] == 'selection':
                result = _choice(packet)
            elif assigned['responsibility'] == 'setter':
                result = {'member': packet['member_key'], 'kind': 'setter', 'logical_id': 'actual-fixture-criteria',
                    'materials': [{'text': 'A controlled criterion deliberately requires an unavailable observation.'}],
                    'criteria': [{'id': 'unit', 'requirement': created['inputs']['request'],
                        'statement': 'Supply the named exact observation.', 'evidence_slots': ['missing-observation']}],
                    'inherited': assigned['inherited'], 'procedure': {'kind': 'question',
                        'reason': 'Controlled owner procedure for substantive qualification feedback.',
                        'specification': {'question': 'What information is required?',
                            'author_task': 'Produce the controlled answer and identify limitations.',
                            'reviewer_task': 'Assess the exact controlled answer.'}}}
            else:
                result = _role_result(session, packet)
            results.append(result)
        session.start(offered['invocation_id'], 'codex', offered['invocation_id'], {'observed': 'Controlled offline native start.'})
        completed = session.complete(offered['invocation_id'], json.dumps({'format': 'jai.semantic-return/1', 'results': results}),
                                     {'observed': 'Controlled offline response; no actual native professional claim.'})
        if packets[0]['assignment'] == root and packets[0]['execution']['phase'] == 'selection':
            state = session.store.read()
            owner_plan = next(reference for reference in completed['completion']['receipt']['created_versions']
                              if state.versions[reference['version_id']]['kind'] == 'delivery.decision')
    assert denied is not None
    checkpoint = session.checkpoint()
    owner = next(item for item in checkpoint['readiness'] if item['assignment'] == root)
    assert not owner['ready'] and owner['reason'] == 'owner_procedure_advances_or_waits'
    state = session.store.read()
    assert owner_plan is not None and owner_plan == state.execution_plans[(root['version_id'], 'default')]
    criteria = state.resolve(state.procedures[(root['version_id'], 'default')])['message']['payload']['criteria']
    actual = state.resolve(criteria, 'source')
    local = session.local_budget_status(root)
    issued = session.issue_batch([{'assignment': root, 'phase': 'work', 'selection': owner_plan}])
    assert session.store.read().execution_eligible(issued['members'][0]['context'])
    assert session.store.read().resolve(criteria, 'source') == actual
    assert session.local_budget_status(root)['unit_id'] == local['unit_id']
    assert session.local_budget_status(root)['deadline_ms'] == local['deadline_ms']
    assert session.local_budget_status(root)['reworks_used'] == local['reworks_used']
    prepared = session.prepare(issued['invocation_id'])
    owner_packet = prepared['members'][0]['packet']
    predecessor = state.procedures[(root['version_id'], 'default')]
    assert owner_packet['current_procedure'] == predecessor
    assert 'current_procedure' not in owner_packet['execution']
    correction = {'member': owner_packet['member_key'], 'kind': 'setter',
        'logical_id': 'actual-corrected-criteria',
        'materials': [{'text': 'Inspect the actual answer without a separate observation prerequisite.'}],
        'criteria': [{'id': 'unit', 'requirement': created['inputs']['request'],
            'statement': 'Describe the requested information and limitations.', 'evidence_slots': []}],
        'inherited': state.resolve(root, 'assignment')['inherited'],
        'procedure': {'kind': 'question', 'reason': 'Actual owner correction of the prerequisite.',
            'specification': {'question': 'What information is required?',
                'author_task': 'Produce the answer and identify limitations.',
                'reviewer_task': 'Assess the exact answer.'}}}
    envelope = {'format': 'jai.semantic-return/1', 'results': [correction]}
    encoded = semantic.compile_semantic(owner_packet, envelope, session.store.put_blob)
    assert encoded['intents'][0]['payload']['previous'] == predecessor
    correction['procedure']['previous'] = None
    with pytest.raises(ValueError, match='previous'):
        semantic.compile_semantic(owner_packet, envelope, session.store.put_blob)
    correction['procedure'].pop('previous')
    session.start(issued['invocation_id'], 'codex', 'controlled-owner-replacement',
                  {'observed': 'Controlled offline owner correction dispatch.'})
    session.complete(issued['invocation_id'], json.dumps(envelope),
                     {'observed': 'Controlled actual-shape owner correction; no live model claim.'})
    warm = session.store.read()
    assert warm.run_states[owner_packet['run_id']] == 'returned'
    replacement = warm.procedures[(root['version_id'], 'default')]
    assert replacement != predecessor
    assert warm.resolve(replacement)['message']['payload']['previous'] == predecessor
    cold = lc.Store(session.store.path, session.store.engagement).read()
    assert cold.head == warm.head
    assert cold.procedures == warm.procedures
    assert cold.transactions == warm.transactions
    assert warm.invocations[issued['invocation_id']]['codec'] == semantic.CODEC
    # Unsupported encoder histories fail before reinterpretation or asset comparison.
    for old_codec in ('jai.semantic-return/1', None):
        rows = lc.loads(lc.canonical(list(warm.transactions)))
        last = rows[-1]
        payload = last['operations'][0]['data']['message']['payload']
        if old_codec is None:
            payload.pop('codec')
        else:
            payload['codec'] = old_codec
        last['hash'] = lc._transaction_hash(last)
        with pytest.raises(lc.ERROR, match='Unsupported historical semantic encoder') as unsupported:
            lc.replay(rows, engagement=session.store.engagement, blob_reader=session.store._blob)
        assert unsupported.value.code == 'P_SCHEMA'

