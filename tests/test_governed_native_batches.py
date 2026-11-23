# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Physical invocation contracts through the real Store and semantic codec."""
import base64
from concurrent.futures import ThreadPoolExecutor
import json
import io
import re
from pathlib import Path
import sys
from threading import Barrier, Event
import time

import pytest
import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
from governed_dispatch import DispatchError
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
    view = offered['prepared']['model_view']
    bindings = view['members'][0]['resources']
    resources = view['resource_descriptors']
    inputs = _projected_json(session, resources[bindings['inputs']])
    machine = _projected_json(session, resources[bindings['optional_machine_index']])
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


def _layer_session(tmp_path, local_budget=None, aggregate_limit_ms=60000, *, single_member=False,
                   question_dependencies=None, sabsa_row_mode=None, operator_dependencies=None):
    session, created = layered.LayeredSession.create(tmp_path, 'layer-batch',
        b'Define a bounded backup service.', 'codex', 'backup',
        None if aggregate_limit_ms is None else int(time.time() * 1000) + 180000,
        aggregate_limit_ms, b'Identify the business boundary, restore requirements and uncertainty.',
        local_budget=local_budget, single_member=single_member, sabsa_row_mode=sabsa_row_mode,
        question_dependencies=operator_dependencies)
    if question_dependencies is None and single_member and sabsa_row_mode is None:
        question_dependencies = {question: [] for question in provider.QUESTIONS}
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
                    **({'question_dependencies': question_dependencies} if question_dependencies is not None else {}),
                    'integration_task': 'Integrate the six actual answers.',
                    'review_task': 'Review their actual integration.', 'interface_criterion': 'boundary'}}}
    _controlled_result(session, root, 'work', procedure, choice)
    return session



def test_layer_procedure_issues_only_questions_with_selected_prerequisites(tmp_path, monkeypatch):
    """Bind both selected predecessor versions and leave independent cells ready."""
    dependencies = dict.fromkeys(provider.QUESTIONS, ())
    dependencies.update(how=['why', 'who'], where=['when'])
    dependencies = {question: list(required) for question, required in dependencies.items()}
    session = _layer_session(tmp_path, aggregate_limit_ms=None, question_dependencies=dependencies)

    for _ in range(40):
        offered = session.next()
        assert offered['status'] == 'invoke'
        state = session.store.read()
        assignments = [state.resolve(member['assignment']) for member in offered['members']]
        if all(assignment['responsibility'] == 'setter' for assignment in assignments):
            initial = {assignment['owner']['question'] for assignment in assignments}
            if 'how' in initial:
                how = next(assignment for assignment in assignments if assignment['owner']['question'] == 'how')
                bindings = {item['slot_id']: item['refs'] for item in how['inputs']}
                for question in ('why', 'who'):
                    ref, = bindings['prerequisite-' + question]
                    answer = state.resolve(ref, 'product')
                    assert answer['owner']['question'] == question and answer['product_kind'] == 'answer'
                    assert state._governing_input(state._point(ref, 'default'), True)
                prior, = [member['assignment'] for member, assignment in zip(offered['members'], assignments)
                          if assignment['owner']['question'] == 'how']
                old_why, = bindings['prerequisite-why']
                changed = state._fork()
                accepted = dict(state.resolve(old_why, 'product'), limitations=['Controlled replacement evidence.'])
                manifest = lc.record_manifest(session.store.engagement, 'default', old_why['logical_id'],
                                              'product', accepted)
                version = lc.version_id(manifest)
                changed._index_version(version, manifest)
                changed.provenance[version] = state.provenance[old_why['version_id']]
                replacement = changed._reference(version)
                changed.states[changed._key(changed._point(replacement, 'default'))] = {
                    'validity': 'valid', 'applicable': True}
                for key, ref in state.selections.items():
                    if ref == old_why:
                        changed.selections[key] = replacement
                procedure, = [ref for ref in changed.procedures.values()
                              if changed.resolve(ref)['message']['payload']['kind'] == 'layer']
                rebound = changed.procedure_next(procedure)
                assert rebound['step'].startswith('question:how:')
                assert rebound['superseded_assignments'] == [prior]
                assert replacement in rebound['triggers'] and old_why not in rebound['triggers']
                controller, _ = session.workflow.dispatcher._controller(changed, 'default')
                with monkeypatch.context() as isolated:
                    isolated.setattr(session.workflow.dispatcher, '_submit', lambda message: message)
                    message = session.workflow._commit_procedure_step(changed, procedure, rebound)['completion']
                effects = changed._control(message, controller, message['issued_at_ms'], True)
                cancelled = next(effect['subjects'] for effect in effects if effect['op'] == 'cancel')
                assert changed._point(prior, 'default') in cancelled
                assert all(changed.resolve(point['ref'])['owner'].get('question') != 'what'
                           for point in cancelled if changed.versions[point['ref']['version_id']]['kind'] == 'delivery.assignment')
                assert not changed._current_inputs(how, True)
                changed._apply(effects, message, {}, None)
                assert changed.assignment_states[prior['version_id']] == 'cancelled'
                issued_step = changed.procedure_steps[procedure['version_id']][rebound['step']]
                new_setter, = issued_step['resolved']
                new_assignment = changed.resolve(new_setter, 'assignment')
                assert new_setter != prior and changed._current_inputs(new_assignment, True)
                assert changed.procedure_next(procedure).get('step') != rebound['step']
                break
            if not state.selections:
                assert initial == {'what', 'why', 'who', 'when'}
        _finish_offered(session, offered)
    else:
        pytest.fail('Dependent question never became eligible')


def test_serial_reverse_display_edge_uses_the_same_prerequisite(tmp_path):
    """Serial capacity preserves the reverse displayed prerequisite."""
    graph = {question: [] for question in provider.QUESTIONS}
    graph.update(how=['why', 'who'], where=['when'])
    session = _layer_session(tmp_path, aggregate_limit_ms=None, single_member=True,
                             question_dependencies=graph)
    for _ in range(65):
        offered = session.next()
        assert offered['status'] == 'invoke', offered
        member, = offered['prepared']['members']
        state = session.store.read()
        body = state.resolve(member['assignment'], 'assignment')
        if body['owner']['question'] == 'where':
            predecessor, = next(item['refs'] for item in body['inputs'] if item['slot_id'] == 'prerequisite-when')
            assert state.resolve(predecessor, 'product')['owner']['question'] == 'when'
            assert state._governing_input(state._point(predecessor, 'default'), True)
            break
        _finish_offered(session, offered)
    else:
        pytest.fail('Serial scheduler did not advance Where after When')


def test_parallel_reverse_display_edge_waits_without_delaying_independent_work(tmp_path):
    """Where waits for When even with another question still in flight."""
    graph = {question: [] for question in provider.QUESTIONS}
    graph.update(how=['why', 'who'], where=['when'])
    session = _layer_session(tmp_path, aggregate_limit_ms=None, single_member=True,
                             question_dependencies=graph)
    active = {}
    initial = {}
    for _ in range(4):
        offered = session.next(observed_running=active, max_parallel=6)
        member, = offered['prepared']['members']
        body = session.store.read().resolve(member['assignment'], 'assignment')
        question = body['owner']['question']
        invocation = offered['invocation_id']
        session.start(invocation, 'codex', invocation, {'observed': 'Controlled initial wave'})
        active[invocation] = invocation
        initial[question] = offered
    assert set(initial) == {'what', 'why', 'who', 'when'}
    assert session.next(observed_running=active, max_parallel=6)['status'] == 'waiting'

    when = initial['when']
    member, = when['prepared']['members']
    invocation = when['invocation_id']
    session.complete(invocation, json.dumps({
        'format': 'jai.semantic-return/1', 'results': [_choice(member['packet'])]}),
        {'observed': 'Controlled When selection completed first'})
    active.pop(invocation)
    for _ in range(8):
        offered = session.next(observed_running=active, max_parallel=6)
        assert offered['status'] == 'invoke', offered
        member, = offered['prepared']['members']
        state = session.store.read()
        body = state.resolve(member['assignment'], 'assignment')
        if body['owner']['question'] == 'where':
            predecessor, = next(item['refs'] for item in body['inputs'] if item['slot_id'] == 'prerequisite-when')
            assert state.resolve(predecessor, 'product')['owner']['question'] == 'when'
            assert state._governing_input(state._point(predecessor, 'default'), True)
            assert all(session.status(item)['state'] == 'running' for item in active)
            break
        assert body['owner']['question'] == 'when'
        _finish_offered(session, offered)
    else:
        pytest.fail('Where did not become ready after When')


def test_replaced_question_input_rebinds_after_cold_journal_replay(tmp_path):
    """Replan Why through its actual setter while its first dependent turn is running."""
    dependencies = {question: [] for question in provider.QUESTIONS}
    dependencies['how'] = ['why']
    session = _layer_session(tmp_path, aggregate_limit_ms=None, single_member=True,
                             question_dependencies=dependencies)

    def find_how():
        for _ in range(65):
            offered = session.next()
            assert offered['status'] == 'invoke', offered
            member, = offered['prepared']['members']
            body = session.store.read().resolve(member['assignment'], 'assignment')
            if body['owner']['question'] == 'how' and body['responsibility'] == 'setter':
                return offered, member, body
            _finish_offered(session, offered)
        pytest.fail('How did not become ready')

    original, member, body = find_how()
    old_input, = next(binding['refs'] for binding in body['inputs']
                      if binding['slot_id'] == 'prerequisite-why')
    original_id = original['invocation_id']
    state = session.store.read()
    what_owner = {**body['owner'], 'question': 'what'}
    independent, = [state._reference(version) for version, record in state.versions.items()
                    if record['kind'] == 'delivery.assignment'
                    and record['content']['record']['owner'] == what_owner
                    and record['content']['record']['responsibility'] == 'setter']
    independent_answers = state._procedure_question_answers(what_owner, 'default', True)
    prefix = session.store.path.read_bytes()
    session.start(original_id, 'codex', 'controlled-old-dependent', {'observed': 'Controlled running dependent'})
    late_result = json.dumps({'format': 'jai.semantic-return/1', 'results': [_choice(member['packet'])]})
    state = session.store.read()
    old_author = state.resolve(state.resolve(old_input, 'product')['assignment'], 'assignment')
    setter = old_author['issued_under']
    choice = state.execution_plans[(setter['version_id'], 'default')]

    def revise(packet):
        result = _role_result(session, packet)
        result['logical_id'] += '-replacement'
        result['materials'] = [{'text': 'Controlled revised recovery rationale.'}]
        return result

    packet = _controlled_result(session, setter, 'work', revise, choice)
    assert session.store.read().run_states[packet['run_id']] == 'returned'
    session.complete(original_id, late_result, {'observed': 'Controlled late completion'})
    assert session.status(original_id)['members'][0]['state'] == 'quarantined'
    session = layered.LayeredSession.open(session.locator)
    _, new_member, new_body = find_how()
    new_input, = next(binding['refs'] for binding in new_body['inputs']
                      if binding['slot_id'] == 'prerequisite-why')
    assert new_input != old_input
    assert new_member['assignment'] != member['assignment']
    resumed = layered.LayeredSession.open(session.locator)
    reopened = resumed.store.read()
    assert resumed.store.path.read_bytes().startswith(prefix)
    assert resumed.status(original_id)['members'][0]['state'] == 'quarantined'
    assert [key for key, invocation in reopened.invocations.items()
            if any(item['assignment'] == member['assignment'] for item in invocation['members'])] == [original_id]
    assert reopened.assignment_states[member['assignment']['version_id']] == 'cancelled'
    assert reopened._status(independent, 'default') == {'validity': 'valid', 'applicable': True}
    assert reopened.assignment_states[independent['version_id']] != 'cancelled'
    if independent_answers:
        assert reopened._procedure_question_answers(what_owner, 'default', True) == independent_answers
    else:
        assert reopened._current_inputs(reopened.resolve(independent, 'assignment'), True)
    assert reopened._current_inputs(new_body, True)


def test_layer_question_dependency_cycle_is_rejected(tmp_path):
    """A cyclic blocking declaration cannot produce any ordinary work order."""
    dependencies = {question: [] for question in provider.QUESTIONS}
    dependencies.update(how=['why'], why=['how'])
    session = _layer_session(tmp_path, aggregate_limit_ms=None, question_dependencies=dependencies)
    state = session.store.read()
    assert not state.procedures
    assert not any(value['kind'] == 'delivery.assignment'
                   and value['content']['record']['owner']['work_kind'] == 'question'
                   for value in state.versions.values())
    assert 'quarantined' in state.run_states.values()


@pytest.mark.parametrize(('mode', 'proposal', 'expected'), [
    ('deterministic', None, {'what', 'who', 'where'}),
    ('left-to-right', None, {'what'}),
    ('llm-assisted', {'what': [], 'why': [], 'how': [], 'who': ['where'], 'where': [], 'when': []},
     {'what', 'where'}),
])
def test_enrolled_sabsa_modes_control_issuance(tmp_path, mode, proposal, expected):
    """Cold resume preserves mode and combines model proposals with mandatory SABSA edges."""
    session = _layer_session(tmp_path, aggregate_limit_ms=None, sabsa_row_mode=mode,
                             question_dependencies=proposal)
    session = layered.LayeredSession.open(session.locator)
    offered = session.next()
    assert offered['status'] == 'invoke'
    state = session.store.read()
    assert {state.resolve(member['assignment'])['owner']['question'] for member in offered['members']} == expected


def test_left_to_right_reports_a_required_backwards_edge(tmp_path):
    """Serial display order cannot override a hard requirement."""
    session = _layer_session(tmp_path, sabsa_row_mode='left-to-right',
                             operator_dependencies={'1': {'what': ['where']}})
    state = session.store.read()
    procedure, = state.procedures.values()
    assert state.procedure_next(procedure) == {
        'waiting': 'question_order_conflict', 'questions': ['what'], 'procedure': procedure}
    waiting = session.next()
    assert waiting['status'] == 'waiting'
    assert waiting['procedure_waits'][0]['questions'] == ['what']
    instruction = session.store.put_blob(b'Use dependency order for this blocked row.')
    assert session.workflow.change_blocked_row_order(procedure, instruction)['status'] == 'committed'
    reopened = layered.LayeredSession.open(session.locator)
    offered = reopened.next()
    state = reopened.store.read()
    assert {state.resolve(member['assignment'])['owner']['question'] for member in offered['members']} == {'who', 'where'}
    with pytest.raises(lc.ERROR, match='Cyclic'):
        lc._row_policy('deterministic', {'1': {'what': ['how']}})


def test_layered_batches_compatible_jobs_and_admits_independent_members_once(tmp_path):
    session = _layer_session(tmp_path)
    offered = session.next()
    assert offered['status'] == 'invoke'
    invocation = offered['invocation_id']
    descriptor = offered['prepared']
    assert len(descriptor['members']) == 6
    progress = session.checkpoint()['progress']
    assert len(progress) == 7
    questions = [row for row in progress if row['dimension'] in provider.QUESTIONS]
    assert all(row['stage'] == 'setter:selection' and row['disposition'] == 'prepared'
               and row['result_ref'] is None for row in questions)
    assert session.checkpoint()['progress'] == progress
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
    progress = session.checkpoint()['progress']
    [quarantined] = [row for row in progress if row['disposition'] == 'quarantined']
    assert quarantined['dimension'] in provider.QUESTIONS
    assert quarantined['wait_reason'] == 'no-admissible-return' and quarantined['result_ref'] is None
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


def test_single_member_carrier_pins_scheduling_across_resume(tmp_path):
    """Separate the six actual ready setters and reject direct multi-member issuance."""
    session = _layer_session(tmp_path, aggregate_limit_ms=None, single_member=True)
    first = session.next()
    assert len(first['members']) == 1
    assert sum(row['dimension'] in provider.QUESTIONS for row in session.checkpoint()['progress']) == 6
    resumed = layered.LayeredSession.open(session.locator)
    assert resumed.single_member
    assert resumed.next()['invocation_id'] == first['invocation_id']
    assert resumed.next()['status'] == 'reconcile'
    member = first['members'][0]
    job = {'assignment': member['assignment'], 'phase': 'selection'}
    before = resumed.store.read().head
    with pytest.raises(lc.ERROR) as denied:
        resumed.issue_batch([job, job])
    assert denied.value.code == 'P_SCOPE'
    assert resumed.store.read().head == before
    seen = set()
    offered = first
    for _ in range(12):
        assert offered['status'] == 'invoke'
        assert len(offered['members']) == 1
        packet = offered['prepared']['members'][0]['packet']
        if packet['execution']['phase'] == 'selection':
            seen.add(offered['members'][0]['assignment']['version_id'])
        _finish_offered(resumed, offered)
        if len(seen) == 6:
            break
        offered = resumed.next()
    assert len(seen) == 6
    assert all(len(call['members']) == 1 for call in resumed.store.read().invocations.values())


def test_parallel_scheduler_waits_for_legacy_dependency_classification(tmp_path):
    """Historical unclassified layer procedures replay without parallel issuance."""
    session = _layer_session(tmp_path, aggregate_limit_ms=None)
    locator = layered._save_locator(tmp_path, session.store.engagement,
                                   session.workflow.dispatcher.config, versioned=True, single_member=True)
    reopened = layered.LayeredSession.open(locator)
    head = reopened.store.read().head
    offered = reopened.next(max_parallel=6)
    assert offered['reason'] == 'unclassified-question-dependencies'
    assert len(offered['procedures']) == 1
    assert reopened.store.read().head == head
    assert reopened.next()['status'] == 'invoke'


def test_singleton_parallel_readiness_requires_each_actual_active_handle(tmp_path):
    """Issue exact independent grants up to the cap and retain uncertain work."""
    session = _layer_session(tmp_path, aggregate_limit_ms=None, single_member=True)
    first = session.next()
    first_id = first['invocation_id']
    session.start(first_id, 'codex', 'observed-first', {'observed': 'Controlled first start'})
    assert session.next(max_parallel=6)['invocation_id'] == first_id
    assert session.next(observed_running={first_id: 'wrong'}, max_parallel=6)['status'] == 'reconcile'
    active = {first_id: 'observed-first'}
    assert session.next(observed_running=active)['reason'] == 'parallel-capacity'
    assignments = {first['members'][0]['assignment']['version_id']}
    for index in range(1, 6):
        offered = session.next(observed_running=active, max_parallel=6)
        assert offered['status'] == 'invoke' and len(offered['members']) == 1
        invocation = offered['invocation_id']
        ref = offered['members'][0]['assignment']['version_id']
        assert ref not in assignments
        assignments.add(ref)
        assert session.next(observed_running=active, max_parallel=6)['invocation_id'] == invocation
        handle = f'observed-{index}'
        session.start(invocation, 'codex', handle, {'observed': 'Controlled sibling start'})
        active[invocation] = handle
    assert len(assignments) == 6
    assert session.next(observed_running=active, max_parallel=6)['reason'] == 'parallel-capacity'
    reopened = layered.LayeredSession.open(session.locator)
    assert reopened.next(max_parallel=6)['status'] == 'reconcile'
    packet = offered['prepared']['members'][0]['packet']
    raw = json.dumps({'format': 'jai.semantic-return/1', 'results': [_choice(packet)]})
    assert session.complete(invocation, raw, {'observed': 'Last dispatched completed first'})['status'] == 'returned'
    del active[invocation]
    assert session.status(first_id)['state'] == 'running'
    followup = session.next(observed_running=active, max_parallel=6)
    assert followup['status'] == 'invoke'
    assert followup['members'][0]['assignment']['version_id'] == ref
    assert followup['prepared']['model_view']['members'][0]['phase'] == 'work'


def test_concurrent_native_completions_commit_both_exact_returns(tmp_path, monkeypatch):
    """Overlapping returns wait for the writer and independently advance the journal."""
    session = _layer_session(tmp_path, aggregate_limit_ms=None, single_member=True)
    first = session.next()
    first_id = first['invocation_id']
    session.start(first_id, 'codex', 'parallel-first', {'observed': 'First dispatch'})
    second = session.next(observed_running={first_id: 'parallel-first'}, max_parallel=2)
    second_id = second['invocation_id']
    session.start(second_id, 'codex', 'parallel-second', {'observed': 'Second dispatch'})
    resumed = layered.LayeredSession.open(session.locator)
    before = session.store.read()
    begin = Barrier(3)
    release = Event()
    submit = lc.Store.submit_invocation_completion

    def synchronized_submit(store, build_message):
        begin.wait(timeout=10)
        assert release.wait(timeout=10)
        return submit(store, build_message)

    monkeypatch.setattr(lc.Store, 'submit_invocation_completion', synchronized_submit)
    first_raw, second_raw = (
        json.dumps({'format': 'jai.semantic-return/1',
                    'results': [_choice(offer['prepared']['members'][0]['packet'])]})
        for offer in (first, second))
    first_capture = {'observed': 'First return'}
    second_capture = {'observed': 'Second return'}
    with ThreadPoolExecutor(max_workers=2) as pool:
        first_return = pool.submit(session.complete, first_id, first_raw, first_capture)
        second_return = pool.submit(resumed.complete, second_id, second_raw, second_capture)
        begin.wait(timeout=10)
        with lc.store_lock(session.store.path):
            release.set()
            assert not first_return.done() and not second_return.done()
        for completion in (first_return.result(timeout=15), second_return.result(timeout=15)):
            assert completion['status'] == 'returned'
            assert completion['completion']['status'] == 'committed'

    state = lc.Store(session.store.path, session.store.engagement).read()
    assert len(state.transactions) == len(before.transactions) + 2
    for offered, raw in ((first, first_raw), (second, second_raw)):
        invocation = offered['invocation_id']
        assert state.invocations[invocation]['raw_return_blob_id'] == lc.blob(raw.encode())
        assert state.invocations[invocation]['state'] == 'returned'
        assignment = offered['members'][0]['assignment']
        assert (assignment['version_id'], 'default') in state.execution_plans
    duplicate = session.complete(first_id, first_raw, first_capture)
    assert duplicate['completion']['status'] == 'already_committed'
    # A publisher that already captured the same return before learning it
    # committed may have a different observation time.
    monkeypatch.setattr(lc.Store, 'submit_invocation_completion', submit)
    committed = next(message for message in state.messages.values()
                     if message['request_id'] == f'invocation_finished:{first_id}')
    payload = dict(committed['payload'])
    payload.pop('event')
    payload.pop('invocation_id')
    payload['observed_at_ms'] += 1
    retried = session.workflow.invocation_event(first_id, 'invocation_finished', **payload)
    assert retried == duplicate['completion']
    assert session.store.read().head == state.head


def test_single_member_carrier_rejects_unresolved_legacy_batch(tmp_path):
    """An App Server enrollment cannot attach to already prepared shared grants."""
    session = _layer_session(tmp_path)
    locator = layered._save_locator(tmp_path, session.store.engagement,
                                   session.workflow.dispatcher.config, versioned=True, single_member=True)
    attached = layered.LayeredSession.open(locator)
    assert len(session.next()['members']) == 6
    with pytest.raises(lc.ERROR, match='unresolved multi-member work'):
        attached.next()
    with pytest.raises(ValueError, match='unresolved multi-member work'):
        layered.LayeredSession.open(locator)


def test_batch_prompt_interns_resources_without_widening_member_reads(tmp_path):
    """Share descriptors in the actual prompt and exercise each member's unchanged broker."""
    session = _layer_session(tmp_path, aggregate_limit_ms=None)
    offered = session.next()
    descriptor = offered['prepared']
    invocation = offered['invocation_id']
    prompt = descriptor['invocation']['arguments']['message'].encode('utf-8')
    view = json.loads(prompt)
    resources = view['resource_descriptors']
    assert len(view['members']) == 6
    assert len({lc.canonical(item) for item in resources}) == len(resources)
    assert len({member['resources']['catalogue'] for member in view['members']}) == 1
    assert sum(item['handle'] == resources[view['members'][0]['resources']['catalogue']]['handle']
               for item in resources) == 1
    reopened = layered.LayeredSession.open(session.locator)
    assert reopened.prepare(invocation)['invocation'] == descriptor['invocation']
    reopened.start(invocation, 'codex', 'controlled-compact-batch', {'fixture': 'Observed start.'})
    entitled = {}
    for member, projected in zip(descriptor['members'], view['members'], strict=True):
        original = lc.loads(session.store._blob(member['host_delivery']['prompt_blob_id']))
        assert {name: resources[index] for name, index in projected['resources'].items()} == original['resources']
        assert set(view['mandatory'] + projected['mandatory']) == set(original['mandatory'])
        assert 'Read candidate professional instructions' in ' '.join(projected['mandatory'])
        for key in ('owner', 'phase', 'bounds', 'tool_ceiling', 'governed_operations'):
            assert projected[key] == original[key]
        member_key = member['member_key']
        entitled[member_key] = set()
        for name, resource in original['resources'].items():
            handle = resource['handle']
            response = reopened.request(invocation, member_key, {
                'id': 'same-resource-' + name, 'operation': 'read', 'handle': handle})
            assert base64.b64decode(response['result']['data']) == Path(resource['path']).read_bytes()
            entitled[member_key].add(handle)
    first, second = [member['member_key'] for member in descriptor['members'][:2]]
    foreign = next(iter(entitled[second] - entitled[first]))
    with pytest.raises(DispatchError, match='Read handle is outside the exact input manifest') as denied:
        reopened.request(invocation, first, {'id': 'foreign-resource', 'operation': 'read', 'handle': foreign})
    assert denied.value.code == 'P_SCOPE'


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


def _finish_offered(session, offered, conditional_question=None, display_summary=None):
    invocation = offered['invocation_id']
    packets = [member['packet'] for member in offered['prepared']['members']]
    session.start(invocation, 'codex', invocation, {'observed': 'Controlled offline native-tool fixture.'})
    results = [_role_result(session, packet, conditional_question) for packet in packets]
    if display_summary is not None:
        for result in results:
            if result['kind'] in {'author', 'integrator'}:
                assert 'Include display_summary' in offered['prepared']['model_view']['return']['rule']
                result['display_summary'] = display_summary
    completed = session.complete(invocation, json.dumps({'format': 'jai.semantic-return/1', 'results': results}),
                                {'observed': 'Controlled offline terminal native-tool fixture.'})
    assert completed['status'] == 'returned'
    assert all(session.store.read().run_states[packet['run_id']] == 'returned' for packet in packets)
    return packets


def test_replay_preserves_legacy_quarantine_for_summary_field(tmp_path, monkeypatch):
    """Replay an encoder-2 batch whose old writer rejected the unknown field."""
    session = _layer_session(tmp_path, aggregate_limit_ms=None)
    for _ in range(12):
        offered = session.next()
        first = offered['prepared']['model_view']['members'][0]
        if (first['responsibility'], first['phase']) == ('author', 'work'):
            break
        _finish_offered(session, offered)
    else:
        pytest.fail('The controlled engagement did not reach author work.')
    invocation = offered['invocation_id']
    packets = [member['packet'] for member in offered['prepared']['members']]
    results = [_role_result(session, packet) for packet in packets]
    results[-1]['display_summary'] = 'Previously unknown field.'
    raw = json.dumps({'format': 'jai.semantic-return/1', 'results': results})
    session.start(invocation, 'codex', invocation, {'fixture': 'Controlled legacy start.'})
    with monkeypatch.context() as legacy:
        legacy.setattr(semantic, 'capture_codec', lambda envelope: semantic.CODEC)
        completed = session.complete(invocation, raw, {'fixture': 'Controlled legacy terminal capture.'})
    assert completed['status'] == 'returned'

    state = layered.LayeredSession.open(session.locator).store.read()
    assert state.head == completed['completion']['receipt']['after_head']
    assert [state.run_states[packet['run_id']] for packet in packets] == ['returned'] * 5 + ['quarantined']
    capture = state.run_details[packets[-1]['run_id']]['semantic_capture']
    assert capture['codec'] == semantic.CODEC
    assert capture['error'] == 'Complete closed role-specific semantic return required'


def test_invalid_review_member_leaves_sibling_answers_selected_and_integration_waiting(tmp_path):
    """Admit valid reviews independently and keep recovery on the exact owner mandate."""
    session = _layer_session(tmp_path, aggregate_limit_ms=None)
    for _ in range(16):
        offered = session.next()
        assert offered['status'] == 'invoke'
        packets = [member['packet'] for member in offered['prepared']['members']]
        state = session.store.read()
        if (packets[0]['execution']['phase'] == 'work'
                and state.resolve(packets[0]['assignment'], 'assignment')['responsibility'] == 'reviewer'):
            break
        _finish_offered(session, offered)
    else:
        pytest.fail('Did not reach the physical reviewer work batch.')
    assert len(packets) == 6
    invalid = packets[-1]
    assignment = state.resolve(invalid['assignment'], 'assignment')
    question = assignment['owner']['question']
    invocation = offered['invocation_id']
    session.start(invocation, 'codex', invocation, {'fixture': 'Controlled review batch start.'})
    results = [_role_result(session, packet) for packet in packets]
    del results[-1]['verdict']
    raw = json.dumps({'format': 'jai.semantic-return/1', 'results': results})
    assert session.complete(invocation, raw, {'fixture': 'Controlled review batch return.'})['status'] == 'returned'
    state = session.store.read()
    assert [state.run_states[packet['run_id']] for packet in packets] == ['returned'] * 5 + ['quarantined']

    retry = session.next()
    checkpoint = session.checkpoint()
    progress = {row['dimension']: row for row in checkpoint['progress']}
    assert progress[question]['result_ref'] is None
    assert progress[None]['result_ref'] is None
    siblings = {name: progress[name]['result_ref'] for name in set(provider.QUESTIONS) - {question}}
    assert all(progress[name]['disposition'] == 'selected' and reference
               for name, reference in siblings.items())
    state = session.store.read()
    assert not any(value['content']['record']['product_kind'] in {'bundle', 'handoff'}
                   for value in state.versions.values() if value['kind'] == 'delivery.product')
    assert not any(state.resolve(item['assignment'])['owner']['layer'] == 2
                   for item in checkpoint['readiness'])
    [member] = retry['prepared']['members']
    packet = member['packet']
    assert packet['assignment'] == invalid['assignment']
    assert packet['execution'] == invalid['execution']
    assert packet['assessment_basis'] == invalid['assessment_basis']
    assert packet['context'] != invalid['context']
    _finish_offered(session, retry)
    integration = session.next()
    [member] = integration['prepared']['members']
    state = session.store.read()
    assert state.resolve(member['assignment'], 'assignment')['responsibility'] == 'integrator'
    final_rows = {row['dimension']: row for row in session.checkpoint()['progress']}
    assert all(final_rows[name]['result_ref'] == reference for name, reference in siblings.items())
    assert final_rows[question]['disposition'] == 'selected'


def test_procedure_proposal_cannot_commit_after_another_writer_advances(tmp_path):
    """Reject a stale scheduling snapshot at the current journal boundary."""
    session = _layer_session(tmp_path, aggregate_limit_ms=None)
    _finish_offered(session, session.next())
    _finish_offered(session, session.next())
    snapshot = session.store.read()
    procedures = [reference for reference in snapshot.procedures.values()
                  if snapshot.resolve(reference)['message']['payload']['kind'] == 'question']
    first, other = procedures[:2]
    expected = snapshot.procedure_next(first)
    assert expected['step'] == 'author'
    writer = layered.LayeredSession.open(session.locator)
    current = writer.workflow.advance(other)['completion']['receipt']['after_head']

    with pytest.raises(DispatchError) as stale:
        session.workflow._commit_procedure_step(snapshot, first, expected)
    assert stale.value.code == 'P_HEAD'
    assert session.store.read().head == current
    assert session.workflow.advance(first)['completion']['status'] == 'committed'


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
    summary = 'The office service boundary covers individual files.'
    for ordinal in range(96):
        offered = session.next()
        if offered['status'] == 'waiting':
            break
        assert offered['status'] == 'invoke', (ordinal, offered)
        owner = offered['prepared']['model_view']['members'][0]['owner']
        packets = _finish_offered(session, offered, display_summary=summary if owner['layer'] == 1 else None)
        state = session.store.read()
        assignment = state.resolve(packets[0]['assignment'], 'assignment')
        if assignment['responsibility'] == 'receiver' and packets[0]['execution']['phase'] == 'work':
            sending_layer = assignment['owner']['layer'] - 1
            sender = next(row for row in session.checkpoint()['progress']
                          if row['dimension'] is None and row['layer'] == sending_layer)
            assert sender['stage'] == 'handoff' and sender['disposition'] == 'pending'
            assert sender['wait_reason'] == 'receiving-acceptance-required'
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
    assert all((body.get('display_summary') == summary) == (body['owner']['layer'] == 1)
               for _, body in answers)
    assert state.resolve(bundles[1], 'product')['display_summary'] == summary
    assert 'display_summary' not in state.resolve(bundles[2], 'product')
    for physical in state.invocations.values():
        if physical['phase'] == 'work' and physical['responsibility'] in {'author', 'integrator'}:
            assert physical['codec'] == (semantic.SUMMARY_CODEC if physical['layer'] == 1 else semantic.CODEC)
    progress = session.checkpoint()['progress']
    assert len(progress) == 42
    assert all(row['display_summary'] == summary for row in progress
               if row['layer'] == 1 and row['dimension'] is not None)
    integration = {row['layer']: row for row in progress if row['dimension'] is None}
    assert all(integration[layer]['disposition'] == 'accepted' for layer in range(1, 6))
    assert integration[6]['disposition'] == 'reviewed'
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
    progress = {row['dimension']: row for row in session.checkpoint()['progress']}
    assert progress[conditional]['review_state'] == 'returned'
    assert progress[conditional]['result_ref'] is None
    assert progress[conditional]['disposition'] == 'prepared'
    for question in set(provider.QUESTIONS) - {conditional}:
        selected = progress[question]
        assert selected['disposition'] == 'selected'
        assert selected['candidate_state'] == selected['review_state'] == 'returned'
        assert session.store.read().resolve(selected['result_ref'], 'product')['owner']['question'] == question
        assert 'display_summary' not in selected
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
