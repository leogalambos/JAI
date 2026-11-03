# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Physical invocation contracts through the real Store and semantic codec."""
import json
import io
import re
from pathlib import Path
import sys
import time

import pytest
import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import governed_native as native
import governed_native_provider as provider
import governed_layered as layered
import governed_semantic as semantic
import operator_actions as operator
import lifecycle as lc


def _session(tmp_path):
    store = lc.Store(tmp_path / 'batch.jsonl', 'native-batch')
    limits = [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 60000}]
    deadline = int(time.time() * 1000) + 180000
    result = provider.bootstrap(store, b'Explain a bounded backup service.',
        b'Identify restore requirements and uncertainty.', 'codex', 'backup', limits, deadline)
    session = native.NativeSession(store, result['config'])
    entry = session.workflow.entry('default', 'backup', limits, deadline)
    return session, entry['assignment']


def _choice(packet):
    model = next(item for item in packet['execution']['availability']
                 if item['provider'] == 'codex' and item['workload_class'] == 'standard')
    return {'member': packet['member_key'], 'kind': 'selection',
            'specialties': ['software-engineer'], 'provider': 'codex',
            'workload_class': 'standard', 'model_selector': model['model_selector'],
            'reason': 'Controlled transport mechanics, not native professional evidence.'}


def test_native_singleton_uses_durable_physical_manifest_and_semantic_capture(tmp_path):
    session, assignment = _session(tmp_path)
    issued = session.issue_batch([{'assignment': assignment, 'phase': 'selection'}])
    invocation = issued['invocation_id']
    descriptor = session.prepare(invocation)
    packet = descriptor['members'][0]['packet']
    assert packet['member_key'] == issued['members'][0]['member_key']
    assert session.status(invocation)['state'] == 'prepared'
    assert descriptor['invocation']['tool'] == 'collaboration.spawn_agent'
    assert descriptor['invocation']['arguments']['fork_turns'] == 'none'
    assert len(descriptor['members']) == 1
    assert packet['transport_limits'] == session.workflow.dispatcher.config['limits']
    resumed = native.NativeSession(lc.Store(session.store.path, session.store.engagement), session.workflow.dispatcher.config)
    assert resumed.prepare(invocation)['invocation'] == descriptor['invocation']
    session.start(invocation, 'codex', 'controlled-platform-handle', {'observed': 'controlled start'})
    context = session.store.read().resolve(packet['context'], 'context')
    bound = session.store.read().run_details[context['run_id']]['native']
    assert bound['packet_bytes'] == packet['transport_limits']['packet_bytes']
    assert bound['total_bytes'] == packet['transport_limits']['total_bytes']
    raw = json.dumps({'format': 'jai.semantic-return/1', 'results': [_choice(packet)]})
    completed = session.complete(invocation, raw, {'observed': 'controlled terminal result'})
    assert completed['status'] == 'returned'
    state = session.store.read()
    assert state.invocations[invocation]['codec'] == semantic.CODEC
    assert state.invocations[invocation]['raw_return_blob_id'] == lc.blob(raw.encode())
    before = state.head
    repeated = session.complete(invocation, raw, {'observed': 'controlled terminal result'})
    assert repeated['completion']['receipt'] == completed['completion']['receipt']
    assert session.store.read().head == before
    with pytest.raises(ValueError):
        session.complete(invocation, raw + ' ', {'observed': 'different capture'})


def test_codex_projection_uses_valid_task_name_and_semantic_read_transport(tmp_path):
    session, assignment = _session(tmp_path)
    issued = session.issue_batch([{'assignment': assignment, 'phase': 'selection'}],
                                invocation_id='invocation:controlled-transport-case')
    descriptor = session.prepare(issued['invocation_id'])
    arguments = descriptor['invocation']['arguments']
    assert re.fullmatch(r'[A-Za-z0-9_]+', arguments['task_name'])
    assert session.prepare(issued['invocation_id'])['invocation']['arguments'] == arguments
    instruction = ' '.join(descriptor['model_view']['members'][0]['mandatory'])
    assert 'read-only execution wrapper' in instruction
    assert 'exact delivered paths' in instruction
    assert 'general shell' in instruction and 'mutation' in instruction
    assert 'network' in instruction and 'unrelated files' in instruction


def _projected_json(session, reference):
    return lc.loads(Path(reference['path']).read_bytes())


def test_native_projection_exposes_exact_entitled_material_and_instruction_files(tmp_path):
    session, assignment = _session(tmp_path)
    unrelated = session.store.put_blob(b'An unrelated immutable blob is not a delivered resource.')
    issued = session.issue_batch([{'assignment': assignment, 'phase': 'selection'}])
    descriptor = session.prepare(issued['invocation_id'])
    member, view = descriptor['members'][0], descriptor['model_view']['members'][0]
    inputs = _projected_json(session, view['resources']['inputs'])
    assert inputs['material']
    for item in inputs['material']:
        resource = item['resource']
        raw = Path(resource['path']).read_bytes()
        assert raw == session.store._blob(item['blob_id'])
        assert resource['handle'] == 'resource:' + item['blob_id']
        assert resource['byte_length'] == len(raw)
    catalogue = _projected_json(session, view['resources']['catalogue'])
    rows = [row for category in catalogue['categories']
            for page in _projected_json(session, category)['pages']
            for row in _projected_json(session, page)['roles']]
    assert len(rows) == catalogue['count'] == 286
    snapshot = session._run(member['context']).execution['snapshot']
    for row in rows:
        expected = snapshot['instructions'][row['slug']]['text'].encode('utf-8')
        assert Path(row['instruction']['path']).read_bytes() == expected
    delivery = lc.loads(session.store._blob(member['host_delivery']['manifest_blob_id']))
    assert unrelated not in {item['blob_id'] for item in delivery['resources']}


def test_native_selection_and_work_contracts_are_phase_scoped_and_semantically_incomplete(tmp_path):
    session, assignment = _session(tmp_path)
    issued = session.issue_batch([{'assignment': assignment, 'phase': 'selection'}])
    descriptor = session.prepare(issued['invocation_id'])
    view = descriptor['model_view']
    packet = descriptor['members'][0]['packet']
    local_keys = {'phase', 'state', 'iteration', 'reworks_used', 'max_reworks', 'remaining_ms', 'deadline_ms', 'stage'}
    assert set(view['members'][0]['bounds']['local_budget']) == local_keys
    operator_status = session.local_budget_status(packet['assignment'])
    assert {'unit_id', 'anchor', 'root_generation', 'pending'} <= set(operator_status)
    assert set(operator_status) > local_keys
    procedure = _projected_json(session, view['members'][0]['resources']['procedure'])
    assert not {'aliases', 'ordinary_owner_actions', 'exceptional_owner_action'} & set(procedure)
    schema = _projected_json(session, procedure['semantic_contract'])
    assert not any(name in json.dumps(schema) for name in ('owner_action', 'question_procedure', 'layer_procedure'))
    skeleton = view['return']['envelope']
    assert set(skeleton) == {'format', 'results'}
    assert skeleton['results'] == [{'member': packet['member_key'], 'kind': 'selection'}]
    validator = jsonschema.Draft202012Validator(schema)
    assert not validator.is_valid(skeleton)
    value = {'format': 'jai.semantic-return/1', 'results': [_choice(packet)]}
    assert validator.is_valid(value)
    assert 'invocation_id' not in view and 'invocation' not in view['requests']
    session.start(issued['invocation_id'], 'codex', 'controlled-phase-contract', {'observed': 'Controlled offline start.'})
    session.complete(issued['invocation_id'], json.dumps(value), {'observed': 'Controlled offline selection.'})
    choice = session.store.read().execution_plans[(assignment['version_id'], 'default')]
    work = session.issue_batch([{'assignment': assignment, 'phase': 'work', 'selection': choice}])
    prepared = session.prepare(work['invocation_id'])
    work_view = prepared['model_view']['members'][0]
    contract = _projected_json(session, work_view['resources']['procedure'])
    assert contract['exceptional_owner_action']
    work_schema = _projected_json(session, contract['semantic_contract'])
    assert 'layer_procedure' in json.dumps(work_schema) and 'question_procedure' not in json.dumps(work_schema)
    workforce = _projected_json(session, work_view['resources']['workforce'])
    assert 'availability' not in workforce
    instruction = workforce['selected_instructions'][0]
    assert Path(instruction['path']).read_bytes() == session._run(work['members'][0]['context']).execution[
        'snapshot']['instructions'][instruction['slug']]['text'].encode('utf-8')


def test_native_business_inputs_preserve_optional_machine_records_and_exact_owner_task(tmp_path):
    session = _layer_session(tmp_path)
    offered = session.next()
    member = offered['prepared']['members'][0]
    view = offered['prepared']['model_view']['members'][0]
    inputs = _projected_json(session, view['resources']['inputs'])
    machine = _projected_json(session, view['resources']['optional_machine_index'])
    packet = member['packet']
    state = session.store.read()
    assignment = state.resolve(packet['assignment'], 'assignment')
    assert assignment['routing']['policy'] not in [item['ref'] for item in inputs['records']]
    assert packet['context'] in [item['ref'] for item in machine['records']]
    assert packet['assignment'] in [item['ref'] for item in machine['records']]
    assert sorted(lc.canonical(item['ref']) for item in [*inputs['records'], *machine['records']]) == sorted(
        lc.canonical(item['ref']) for item in packet['manifest'])
    task = assignment['procedure_task']
    declared = state.resolve(task['procedure'])['message']['payload']['specification']
    expected = declared['question_tasks'][assignment['owner']['question']]
    assert Path(inputs['mandate']['path']).read_bytes().decode() == expected


def test_native_unbound_cancel_and_member_resource_boundary(tmp_path):
    session, assignment = _session(tmp_path)
    issued = session.issue_batch([{'assignment': assignment, 'phase': 'selection'}])
    invocation = issued['invocation_id']
    with pytest.raises(ValueError):
        session.request(invocation, 'unissued-member', {'id': 'bad', 'operation': 'read', 'handle': 'catalogue'})
    session.stop(invocation, {'state': 'not-dispatched', 'observed': 'Controlled host cancellation before preparation.'})
    assert session.status(invocation)['state'] == 'cancelled'


def test_native_unknown_stop_retains_physical_uncertainty_until_actual_confirmation(tmp_path):
    session, assignment = _session(tmp_path)
    issued = session.issue_batch([{'assignment': assignment, 'phase': 'selection'}])
    invocation = issued['invocation_id']
    session.prepare(invocation)
    session.start(invocation, 'codex', 'controlled-stopping-handle', {'observed': 'controlled start'})
    session.stop(invocation, {'state': 'unknown', 'observed': 'Platform termination was not confirmed.'})
    physical = session.store.read().invocations[invocation]
    assert session.status(invocation)['state'] == 'uncertain'
    assert physical['reservation_released'] is False
    session.stop(invocation, {'state': 'terminated', 'observed': 'Controlled actual terminal observation.'})
    assert session.status(invocation)['state'] == 'cancelled'
    assert session.store.read().invocations[invocation]['reservation_released'] is True


def _controlled_result(session, assignment, phase, produce, selection=None):
    issued = session.issue_batch([{'assignment': assignment, 'phase': phase, 'selection': selection}], bound_ms=5000)
    invocation = issued['invocation_id']
    packet = session.prepare(invocation)['members'][0]['packet']
    session.start(invocation, 'codex', invocation, {'observed': 'Controlled offline platform fixture.'})
    value = {'format': 'jai.semantic-return/1', 'results': [produce(packet)]}
    result = session.complete(invocation, json.dumps(value), {'observed': 'Controlled offline terminal fixture.'})
    assert result['status'] == 'returned'
    return packet


def _layer_session(tmp_path, local_budget=None, aggregate_limit_ms=60000):
    session, created = layered.LayeredSession.create(tmp_path, 'layer-batch',
        b'Define a bounded backup service.', 'codex', 'backup',
        None if aggregate_limit_ms is None else int(time.time() * 1000) + 180000,
        aggregate_limit_ms, b'Identify the business boundary, restore requirements and uncertainty.',
        local_budget=local_budget)
    root = created['entry']['assignment']
    _controlled_result(session, root, 'selection', _choice)
    state = session.store.read()
    choice = state.execution_plans[(root['version_id'], 'default')]
    assigned = state.resolve(root, 'assignment')
    input_ref = next(ref for ref in assigned['inherited']
                     if state.resolve(ref, 'source')['source_role'] == 'input')
    def procedure(packet):
        return {'member': packet['member_key'], 'kind': 'setter', 'logical_id': 'layer-criteria',
            'materials': [{'text': 'Controlled actual layer framing.'}],
            'criteria': [{'id': 'boundary', 'requirement': input_ref,
                          'statement': 'Describe the backup service boundary.', 'evidence_slots': []}],
            'inherited': assigned['inherited'],
            'procedure': {'kind': 'layer', 'reason': 'Controlled actual owner procedure.',
                'specification': {'framing': 'Describe the bounded backup service.',
                    'question_tasks': {question: 'Resolve ' + question + ' for the backup service.'
                                       for question in provider.QUESTIONS},
                    'integration_task': 'Integrate the six actual answers.',
                    'review_task': 'Review their actual integration.', 'interface_criterion': 'boundary'}}}
    _controlled_result(session, root, 'work', procedure, choice)
    return session


def test_layered_batches_compatible_jobs_and_admits_independent_members_once(tmp_path):
    session = _layer_session(tmp_path)
    offered = session.next()
    assert offered['status'] == 'invoke'
    invocation = offered['invocation_id']
    descriptor = offered['prepared']
    assert len(descriptor['members']) == 6
    assert session.next()['status'] == 'reconcile'
    assert len([item for item in session.store.read().invocations.values() if item['state'] == 'prepared']) == 1
    session.start(invocation, 'codex', 'controlled-six-setters', {'observed': 'Controlled single physical call.'})
    member = descriptor['members'][0]
    response = session.request(invocation, member['member_key'],
        {'id': 'catalogue-read', 'operation': 'read', 'handle': 'catalogue'})
    assert response['ok'] is True
    results = [_choice(item['packet']) for item in descriptor['members']]
    light = next(item for item in descriptor['members'][0]['packet']['execution']['availability']
                 if item['provider'] == 'codex' and item['workload_class'] == 'light')
    results[0].update(workload_class='light', model_selector=light['model_selector'])
    results.pop()
    raw = json.dumps({'format': 'jai.semantic-return/1', 'results': results})
    completed = session.complete(invocation, raw, {'observed': 'Actual controlled partial result.'})
    assert completed['status'] == 'returned'
    state = session.store.read()
    assert sum((item['assignment']['version_id'], 'default') in state.execution_plans
               for item in descriptor['members']) == 5
    assert state.run_states[state.resolve(descriptor['members'][-1]['context'], 'context')['run_id']] == 'quarantined'
    physical = state.invocations[invocation]
    elapsed = physical['finished_at_ms'] - physical['started_at_ms']
    assert physical['usage']['elapsed_ms:ms'] == elapsed
    for item in descriptor['members']:
        details = state.run_details[state.resolve(item['context'], 'context')['run_id']]
        assert details['usage']['elapsed_ms:ms'] == elapsed
    before = state.head
    session.complete(invocation, raw, {'observed': 'Actual controlled partial result.'})
    assert session.store.read().head == before
    jobs = [{'assignment': item['assignment'], 'phase': 'work',
             'selection': state.execution_plans[(item['assignment']['version_id'], 'default')]}
            for item in descriptor['members'][:2]]
    with pytest.raises(ValueError):
        session.issue_batch(jobs, bound_ms=5000)
    assert session.store.read().head == before
    replayed = lc.Store(session.store.path, session.store.engagement).read()
    assert replayed.invocations[invocation]['usage'] == physical['usage']
    assert replayed.execution_plans == state.execution_plans


def test_native_forged_encoding_cannot_replace_actual_semantic_capture(tmp_path):
    session, assignment = _session(tmp_path)
    issued = session.issue_batch([{'assignment': assignment, 'phase': 'selection'}], bound_ms=5000)
    invocation = issued['invocation_id']
    packet = session.prepare(invocation)['members'][0]['packet']
    session.start(invocation, 'codex', 'controlled-forgery-fixture', {'observed': 'Controlled actual start.'})
    value = {'format': 'jai.semantic-return/1', 'results': [_choice(packet)]}
    raw = json.dumps(value).encode()
    encoded = semantic.compile_semantic(packet, value, session.store.put_blob)
    encoded['intents'][0]['payload']['reason'] = 'This text was never in the actual captured semantic result.'
    session.workflow.invocation_event(invocation, 'invocation_finished',
        observed_at_ms=int(time.time() * 1000),
        capture_blob_id=session.store.put_blob(operator.canonical({'observed': 'Controlled actual terminal capture.'})),
        raw_return_blob_id=session.store.put_blob(raw), codec=semantic.CODEC,
        encoded_returns=[{'member_key': packet['member_key'],
                         'return_blob_id': session.store.put_blob(lc.canonical(encoded)), 'error': None}])
    state = session.store.read()
    run_id = state.resolve(packet['context'], 'context')['run_id']
    assert state.run_states[run_id] == 'quarantined'
    assert (assignment['version_id'], 'default') not in state.execution_plans
    assert state.invocations[invocation]['raw_return_blob_id'] == lc.blob(raw)
    capture = state.run_details[run_id]['semantic_capture']
    assert capture['encoded_return_blob_id'] is None
    assert capture['error']
    replayed = lc.Store(session.store.path, session.store.engagement).read()
    assert replayed.run_states[run_id] == 'quarantined'
    assert replayed.execution_plans == state.execution_plans


def test_native_host_commands_keep_one_uniform_closed_invocation_contract(tmp_path):
    session, assignment = _session(tmp_path)
    invocation = 'controlled-host-invocation'
    commands = [
        {'id': 'issue', 'operation': 'issue_batch', 'jobs': [{'assignment': assignment, 'phase': 'selection'}],
         'bound_ms': 5000, 'invocation_id': invocation},
        {'id': 'prepare', 'operation': 'prepare', 'invocation': invocation},
        {'id': 'status', 'operation': 'status', 'invocation': invocation},
        {'id': 'invalid', 'operation': 'prepare', 'invocation': invocation, 'force': True},
        {'id': 'close', 'operation': 'close'}]
    source = io.BytesIO(b''.join(lc.canonical(item) + b'\n' for item in commands))
    destination = io.StringIO()
    assert native.serve(session, source, destination) == 0
    responses = [json.loads(line) for line in destination.getvalue().splitlines()]
    assert responses[0]['result']['invocation_id'] == invocation
    assert responses[1]['ok'] is True
    assert responses[2]['result']['state'] == 'prepared'
    assert responses[3]['ok'] is False
    assert responses[4]['result'] == {'closed': True}


def _role_result(session, packet, conditional_question=None):
    state = session.store.read()
    assigned = state.resolve(packet['assignment'], 'assignment')
    role = assigned['responsibility']
    base = {'member': packet['member_key'], 'kind': role,
            'logical_id': 'controlled:' + packet['context']['logical_id']}
    if packet['execution']['phase'] == 'selection':
        return _choice(packet)
    if role == 'setter' and assigned['owner']['work_kind'] == 'integration':
        return {**base, 'materials': [{'text': 'Synthetic layer framing for offline runtime progression.'}],
            'criteria': [{'id': 'boundary', 'requirement': assigned['criteria'],
                'statement': 'Preserve the inherited backup-service boundary.', 'evidence_slots': []}],
            'inherited': assigned['inherited'],
            'procedure': {'kind': 'layer', 'reason': 'Synthetic owner procedure, not a live architecture claim.',
                'specification': {'framing': 'Refine the backup service at this content layer.',
                    'question_tasks': {question: 'Resolve ' + question + ' in this layer.'
                                       for question in provider.QUESTIONS},
                    'integration_task': 'Integrate all six synthetic local answers.',
                    'review_task': 'Review the exact synthetic integration.', 'interface_criterion': 'boundary'}}}
    if role == 'setter':
        question = assigned['owner']['question']
        inherited = list(assigned['inherited'])
        if assigned['criteria'] not in inherited:
            inherited.append(assigned['criteria'])
        return {**base, 'materials': [{'text': 'Controlled actual question requirement.'}],
            'criteria': [{'id': 'unit', 'requirement': assigned['criteria'],
                          'statement': 'Address ' + question + ' for the backup service.', 'evidence_slots': []}],
            'inherited': inherited, 'procedure': {'kind': 'question', 'reason': 'Controlled owner procedure.',
                'specification': {'question': 'What does ' + question + ' require for this service?',
                    'author_task': 'Produce the actual ' + question + ' answer.',
                    'reviewer_task': 'Independently review that answer against its unit criterion.'}}}
    if role in {'reviewer', 'integration_reviewer', 'receiver'}:
        conditional = role == 'reviewer' and assigned['owner']['question'] == conditional_question
        return {**base, 'verdict': ('supported_with_conditions' if conditional else
                    'accepted' if role == 'receiver' else 'supported'),
            'rationale': 'Controlled offline verdict, not a native professional assessment.',
            'findings': [], 'conditions': [assigned['criteria']] if conditional else []}
    if role == 'integrator':
        answers = [reference for binding in assigned['inputs'] if binding['slot_id'] == 'reviewed_answers'
                   for reference in binding['refs']]
        return {**base, 'materials': [{'text': 'Controlled integration of the six actual fixture answers.'}],
                'answers': answers, 'related': [], 'limitations': ['Synthetic transport fixture only.']}
    return {**base, 'materials': [{'json': {'observation': 'Controlled actual answer.', 'ratio': 0.5}}],
            'evidence': [], 'limitations': ['Synthetic transport fixture only.']}


def _finish_offered(session, offered, conditional_question=None):
    invocation = offered['invocation_id']
    packets = [member['packet'] for member in offered['prepared']['members']]
    session.start(invocation, 'codex', invocation, {'observed': 'Controlled offline native-tool fixture.'})
    results = [_role_result(session, packet, conditional_question) for packet in packets]
    completed = session.complete(invocation, json.dumps({'format': 'jai.semantic-return/1', 'results': results}),
                                {'observed': 'Controlled offline terminal native-tool fixture.'})
    assert completed['status'] == 'returned'
    assert all(session.store.read().run_states[packet['run_id']] == 'returned' for packet in packets)
    return packets


def test_layered_complete_local_triads_and_adjacent_receiving_without_bookkeeping_models(tmp_path, monkeypatch):
    """Synthetic role returns exercise all six runtime layers, not model quality."""
    # Catalogue completeness has its own tests. This flow uses one complete real
    # specialty and unchanged instruction bytes through the actual enrollment.
    catalogue = lc.loads((provider.ROOT / 'roles.json').read_bytes())
    role = next(row for row in catalogue['roles'] if row['slug'] == 'software-engineer')
    original_skills = (provider.ROOT.parent / 'skills' if (provider.ROOT.parent / 'skills').is_dir()
                       else provider.ROOT / 'skills')
    instruction = (original_skills / role['skill'] / 'references' / (role['slug'] + '.md')).read_bytes()
    fixture_root = tmp_path / 'flow-catalogue'
    fixture_root.mkdir()
    (fixture_root / 'roles.json').write_bytes(lc.canonical({**catalogue, 'count': 1, 'roles': [role]}))
    target = fixture_root / 'skills' / role['skill'] / 'references' / (role['slug'] + '.md')
    target.parent.mkdir(parents=True)
    target.write_bytes(instruction)
    monkeypatch.setattr(provider, 'ROOT', fixture_root)
    session = _layer_session(tmp_path, aggregate_limit_ms=None)
    seen = []
    for ordinal in range(96):
        offered = session.next()
        if offered['status'] == 'waiting':
            break
        assert offered['status'] == 'invoke', (ordinal, offered)
        packets = _finish_offered(session, offered)
        state = session.store.read()
        seen.extend((packet['execution']['phase'],
                     state.resolve(packet['assignment'], 'assignment')['responsibility'])
                    for packet in packets)
    else:
        pytest.fail('Six-layer progression exceeded 96 physical steps: ' + repr(session.checkpoint()))
    state = session.store.read()
    assert seen.count(('work', 'author')) == 36
    assert seen.count(('work', 'reviewer')) == 36
    assert seen.count(('work', 'integrator')) == 6
    assert seen.count(('work', 'integration_reviewer')) == 6
    assert seen.count(('work', 'receiver')) == 5
    # Initial L1 coordinator was configured by _layer_session; no semantic
    # owner turns are needed for mechanical assignment/proof/basis operations.
    assert seen.count(('work', 'setter')) == 36 + 5
    products = [(state._reference(identifier), value['content']['record'])
                for identifier, value in state.versions.items() if value['kind'] == 'delivery.product']
    answers = [(ref, body) for ref, body in products if body['product_kind'] == 'answer']
    assert len(answers) == 36
    assert {(body['owner']['layer'], body['owner']['question']) for _, body in answers} == {
        (layer, question) for layer in range(1, 7) for question in provider.QUESTIONS}
    bundles = {body['owner']['layer']: ref for ref, body in products if body['product_kind'] == 'bundle'}
    assert set(bundles) == set(range(1, 7))
    for reference in [ref for ref, _ in answers] + list(bundles.values()):
        assert state._governing_input(state._point(reference), live=False)
        proofs = [proof for proof in state.proofs.values() if proof['subject'] == reference]
        assert len(proofs) == 1
        assessment = state.resolve(proofs[0]['proof'], 'assessment')
        assert assessment['verdict'] == 'supported'
        assert state._status(proofs[0]['proof'], proofs[0]['proof_use_scope']) == {
            'validity': 'valid', 'applicable': True}
        author_context = state.provenance[reference['version_id']]['context']
        reviewer_context = state.provenance[proofs[0]['proof']['version_id']]['context']
        author_run = state.resolve(author_context, 'context')['run_id']
        reviewer_run = state.resolve(reviewer_context, 'context')['run_id']
        assert state.run_details[author_run]['invocation_id'] != state.run_details[reviewer_run]['invocation_id']
    receiving = [proof for proof in state.proofs.values()
                 if state.resolve(proof['proof'], 'assessment')['assessment_kind'] == 'receiving']
    assert len(receiving) == 5
    for proof in receiving:
        handoff = state.resolve(proof['subject'], 'product')
        layer = handoff['owner']['layer']
        assert layer in range(1, 6)
        assert next(binding['refs'] for binding in handoff['related'] if binding['slot_id'] == 'bundle') == [bundles[layer]]
        assessment = state.resolve(proof['proof'], 'assessment')
        assert assessment['verdict'] == 'accepted'
        receiver = state.resolve(assessment['assignment'], 'assignment')
        assert receiver['owner']['layer'] == layer + 1
        receiver_unit = state.local_budget_status(assessment['assignment'])
        assert receiver_unit['state'] == 'idle' and receiver_unit['stage'] == 'receiver_complete'
        assert receiver_unit['remaining_ms'] > 0 and receiver_unit['deadline_ms'] is None
        future = state.local_budget_status(assessment['assignment'],
            receiver_unit['started_at_ms'] + receiver_unit['policy']['iteration_ms'] + 1)
        assert not future['due'] and future['remaining_ms'] == receiver_unit['remaining_ms']
        assert any(proof['subject'] in binding['refs'] for binding in receiver['inputs'])
        assert state._governing_input(state._point(proof['subject']), live=False)
    assert all(value['state'] == 'returned' for value in state.invocations.values())
    final = state.evaluate(bundles[6])
    assert final['qualified'] and not final['accepted'] and not final['release_eligible']
    head = state.head
    replayed = lc.Store(session.store.path, session.store.engagement).read()
    assert replayed.head == head
    assert replayed.evaluate(bundles[6]) == final


def test_layered_conditional_review_routes_actual_owner_without_positive_transfer(tmp_path):
    session = _layer_session(tmp_path)
    conditional = 'what'
    reviewed = False
    for _ in range(16):
        offered = session.next()
        assert offered['status'] == 'invoke', offered
        packets = _finish_offered(session, offered, conditional)
        if any(packet['execution']['phase'] == 'work'
               and session.store.read().resolve(packet['assignment'], 'assignment')['responsibility'] == 'reviewer'
               for packet in packets):
            reviewed = True
            break
    assert reviewed
    owner_work = session.next()
    assert owner_work['status'] == 'invoke', owner_work
    members = owner_work['prepared']['members']
    assert len(members) == 1
    packet = members[0]['packet']
    assigned = session.store.read().resolve(packet['assignment'], 'assignment')
    assert assigned['responsibility'] == 'setter'
    assert assigned['owner']['question'] == conditional
    assert packet['execution']['phase'] == 'work'
    procedure = session.store.read().procedures[(packet['assignment']['version_id'], 'default')]
    assert session.store.read().procedure_next(procedure)['waiting'] == 'owner_required'
    session.stop(owner_work['invocation_id'], {'state': 'not-dispatched', 'observed': 'Actual owner discretion is required.'})


def test_work_evidence_projection_distinguishes_observations_from_source_citations():
    """The exact model-facing schema and purpose preserve the evidence/provenance split."""
    schema = lc.loads((provider.wire.PACKAGE / 'semantic-return.schema.json').read_bytes())
    documents = {'semantic-return.schema.json': schema,
                 'common.schema.json': lc.loads((provider.wire.PACKAGE / 'common.schema.json').read_bytes())}
    owner = {'layer': 1, 'work_item': 'backup', 'work_kind': 'question', 'question': 'what'}
    for role in ('author', 'measurement', 'reviewer', 'integration_reviewer', 'receiver'):
        assignment = {'responsibility': role, 'owner': owner}
        contract = provider._response_contract({'execution': {'phase': 'work'}}, assignment,
                                               {'owner': {'kind': 'controller', 'id': 'parent'}, 'obligations': []})
        assert 'observation products qualified before use' in contract['purpose']
        assert 'not request, criteria, assignment or source citations' in contract['purpose']
        assert 'Use []' in contract['purpose']
    for kind in ('author', 'measurement'):
        projected = provider._project_schema(schema['$defs'][kind], documents)
        description = projected['properties']['evidence']['description']
        assert 'observation products' in description and 'qualified before use' in description
        assert 'request, criteria, assignment or other source records' in description
        assert 'uses []' in description and 'provenance is already bound by the host' in description
    integrated = provider._project_schema(schema['$defs']['integrator'], documents)
    assert 'evidence' not in integrated['properties']
    contract = provider._response_contract({'execution': {'phase': 'work'}},
        {'responsibility': 'integrator', 'owner': owner},
        {'owner': {'kind': 'controller', 'id': 'parent'}, 'obligations': []})
    assert 'do not add an evidence field' in contract['purpose']
    assert 'Keep source citations in actual material' in contract['purpose']
    finding = provider._project_schema(schema['$defs']['reviewer'], documents)
    assert 'observation products' in json.dumps(finding)
