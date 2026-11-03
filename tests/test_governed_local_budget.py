# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Local operational windows preserve accepted work and exact operator decisions."""
import copy
import time

import pytest

from governed_fixtures import GovernedHarness, delivery
import governed_local_budget
import governed_routing
import governed_workflow
import lifecycle as lc


class _UncappedHarness(GovernedHarness):
    def _routing_source(self):
        source = super()._routing_source()
        snapshot = governed_routing.load_policy(source, self.store._blob)
        descriptor = snapshot['descriptor']
        source['material'] = governed_routing.capture_policy('host-routing',
            self.store._blob(descriptor['catalogue_blob_id']), self.store._blob(descriptor['models_blob_id']),
            {slug: self.store._blob(identifier) for slug, identifier in descriptor['instruction_blobs'].items()},
            {'provider': 'codex', 'workload_class': 'light',
             'model_selector': snapshot['models']['providers']['codex']['classes']['light']['model_selector']},
            {**descriptor['capabilities'], 'limits': []}, self.store.put_blob)
        return source

    def bootstrap_message(self, **kwargs):
        message = super().bootstrap_message(**kwargs)
        profile = message['payload']['profile']['record']
        profile['local_budget'] = {'iteration_ms': 1000, 'max_reworks': 3}
        profile['scheduling'].update(initial_deadline_ms=None, control_limits=[], max_search_steps=None)
        self.profile = self.ref('profile', 'profile', profile)
        message['message_id'] = delivery.message_id(message)
        return message

    def record(self, logical_id, record_type, record, **kwargs):
        if record_type == 'assignment':
            record['deadline_ms'], record['limits'] = None, []
        return super().record(logical_id, record_type, record, **kwargs)

    def outbound(self, message):
        completed = super().outbound(message)
        if message['sender']['kind'] == 'assignment':
            completed = copy.deepcopy(completed)
            context = self.store.read().resolve(message['context'], 'context')
            limits = self.store.read().run_details[context['run_id']]['limits']
            completed['payload']['usage'] = [{'metric': item['metric'], 'unit': item['unit'], 'total': 1}
                                             for item in limits]
            completed['message_id'] = delivery.message_id(completed)
            self.outbound_messages[message['message_id']] = completed
        return completed


def _workflow(host):
    return governed_workflow.Workflow(host.store, {'protocol': 'jai.host-dispatch/1',
        'workers': [], 'destinations': [], 'tools': [],
        'limits': {'packet_bytes': 2097152, 'total_bytes': 8388608}})


def _owner_work(host, workflow, assignment):
    state = host.store.read()
    plan = state.execution_plans.get((assignment['version_id'], host.scope))
    if plan is None:
        selected = workflow.issue(assignment, 'selection')['context']
        workflow.dispatcher._control(selected, 'run_started')
        record = host.store.read().resolve(assignment, 'assignment')
        host.commit(host.message('decision', {'action': 'select_execution', 'assignment': assignment,
            'previous': None, 'specialties': ['software-engineer'], 'provider': 'json-process/1',
            'workload_class': 'fixture-' + record['responsibility'],
            'model_selector': 'fixture-' + record['responsibility'],
            'reason': 'Controlled local-budget fixture choice.', 'authority_proof': None},
            sender={'kind': 'assignment', 'ref': assignment}, context=selected))
        plan = host.store.read().execution_plans[(assignment['version_id'], host.scope)]
    issued = workflow.issue(assignment, 'work', plan)['context']
    workflow.dispatcher._control(issued, 'run_started')
    return issued


def _downstream_work(host, workflow, owner, name, responsibility='author'):
    context = _owner_work(host, workflow, owner)
    record = copy.deepcopy(host.store.read().resolve(owner, 'assignment'))
    record.update(responsibility=responsibility, assigned_actor=name, issued_under=owner)
    reference = host.record(name, 'assignment', record,
                            sender={'kind': 'assignment', 'ref': owner}, context=context)
    host.commit(host.message('assignment', {'assignment': reference, 'owner': record['owner'],
        'responsibility': record['responsibility'], 'inputs': lc._input_locators(record['inputs']),
        'criteria': record['criteria']}, sender={'kind': 'assignment', 'ref': owner}, context=context))
    child = _owner_work(host, workflow, reference)
    workflow.dispatcher._control(child, 'run_cancelled', total=1)
    return reference


def _criterion(host, assignment, context, name):
    record = copy.deepcopy(host.store.read().resolve(host.criteria, 'source'))
    record.update(owner=host.store.read().resolve(assignment, 'assignment')['owner'],
                  origin={'kind': 'assignment', 'ref': assignment},
                  material=[host.material('Controlled criterion revision ' + name)])
    return host.record(name, 'source', record,
                       sender={'kind': 'assignment', 'ref': assignment}, context=context)


def _configure(host, assignment, context, criteria, previous=None, kind='question', suffix='initial'):
    specification = ({'question': 'Describe the bounded service.', 'author_task': 'Describe ' + suffix,
                      'reviewer_task': 'Review the exact candidate.'} if kind == 'question' else
        {'framing': 'Describe the bounded service.', 'question_tasks': {question: 'Address ' + question
            for question in ('what', 'why', 'how', 'who', 'where', 'when')},
         'integration_task': 'Integrate actual reviewed answers.', 'review_task': 'Review actual integration.',
         'interface_criterion': 'C1'})
    return host.commit(host.message('decision', {'action': 'configure_procedure', 'assignment': assignment,
        'criteria': criteria, 'kind': kind, 'specification': specification, 'previous': previous,
        'reason': 'Actual controlled owner procedure ' + suffix, 'authority_proof': None},
        sender={'kind': 'assignment', 'ref': assignment}, context=context))


def test_actual_start_pause_exact_extension_and_cold_restart_do_not_reset_local_time(tmp_path, monkeypatch):
    clock = [int(time.time() * 1000)]
    monkeypatch.setattr(lc.time, 'time', lambda: clock[0] / 1000)
    host = _UncappedHarness(tmp_path, monkeypatch)
    host.bootstrap()
    assignment, _ = host.assignment('incoming-question', 'setter')
    workflow = _workflow(host)
    state = host.store.read()
    assert state.resolve(assignment, 'assignment')['deadline_ms'] is None
    assert state.resolve(assignment, 'assignment')['limits'] == []
    initial = state.local_budget_status(assignment)
    assert initial['state'] == 'ready' and initial['deadline_ms'] is None
    assert initial['remaining_ms'] == 1000
    issued = workflow.issue(assignment, 'selection')
    context = host.store.read().resolve(issued['context'], 'context')
    clock[0] += 200
    assert host.store.read().local_budget_status(assignment)['remaining_ms'] == 1000
    host.commit(host.message('control_event', {'event': 'run_started', 'run_context': issued['context'],
        'run_id': context['run_id'], 'observed_at_ms': clock[0]}))
    active = host.store.read().local_budget_status(assignment)
    assert active['deadline_ms'] == clock[0] + 1000
    assert active['started_at_ms'] == clock[0]
    clock[0] += 700
    host.commit(host.message('control_event', {'event': 'run_cancelled', 'run_context': issued['context'],
        'run_id': context['run_id'], 'observed_at_ms': clock[0],
        'reason': 'Controlled fixture process stop before local timeout.',
        'usage': [{'metric': 'elapsed_ms', 'unit': 'ms', 'total': 700}]}))
    later = _owner_work(host, workflow, assignment)
    assert host.store.read().local_budget_status(assignment)['deadline_ms'] == active['deadline_ms']
    clock[0] += 100
    later_record = host.store.read().resolve(later, 'context')
    host.commit(host.message('control_event', {'event': 'run_cancelled', 'run_context': later,
        'run_id': later_record['run_id'], 'observed_at_ms': clock[0], 'reason': 'Controlled work stop.',
        'usage': [{'metric': 'elapsed_ms', 'unit': 'ms', 'total': 100}]}))
    clock[0] = active['deadline_ms'] + 1
    notice = workflow.pause_due()
    paused = notice['notices'][0]
    assert paused['state'] == 'paused' and paused['remaining_ms'] == 0
    assert paused['iteration'] == 0 and paused['reworks_used'] == 0
    assert paused['stage'] == 'setter:work'
    assert [item['state'] for item in paused['progress']] == ['cancelled', 'returned', 'cancelled']
    assert not any(event['kind'] == 'escalation' for event in host.store.read().events)
    instruction = host.store.put_blob(b'Actual fixture operator: allow 800 ms more for this paused iteration.')
    extended = workflow.extend_local_budget(paused['unit_id'], paused['revision'], 800, instruction)
    before = host.path.read_bytes()
    assert workflow.extend_local_budget(paused['unit_id'], paused['revision'], 800, instruction)['receipt'] == extended['receipt']
    assert host.path.read_bytes() == before
    with pytest.raises(ValueError) as stale:
        workflow.extend_local_budget(paused['unit_id'], paused['revision'], 900, instruction)
    assert stale.value.code == 'P_CONFLICT'
    clock[0] += 3600000
    pending = host.store.read().local_budget_status(assignment)
    assert pending['remaining_ms'] == 800 and pending['deadline_ms'] is None
    with pytest.raises(lc.ERROR):
        host.store.read().execution_eligible(issued['context'])
    fresh = workflow.issue(assignment, 'selection')
    fresh_context = host.store.read().resolve(fresh['context'], 'context')
    assert fresh_context['expires_at_ms'] > context['expires_at_ms']
    assert host.store.read().local_budget_status(assignment)['deadline_ms'] is None
    clock[0] += 100
    host.commit(host.message('control_event', {'event': 'run_started', 'run_context': fresh['context'],
        'run_id': fresh_context['run_id'], 'observed_at_ms': clock[0]}))
    restarted = lc.Store(host.path, host.engagement).read()
    current = restarted.local_budget_status(assignment)
    assert current['deadline_ms'] == clock[0] + 800
    assert current['iteration'] == 0 and current['reworks_used'] == 0
    assert restarted.usage[(host.scope, 'elapsed_ms', 'ms')]['spent'] == 801
    invalid = {'scope': host.scope, 'payload': {'event': 'local_budget_extend',
               'unit_id': '0' * 64, 'expected_revision': 0, 'additional_ms': 1,
               'operator_instruction_ref': instruction}}
    with pytest.raises(lc.ERROR) as unknown:
        governed_local_budget.derive(restarted, invalid, {'kind': 'controller', 'id': 'actual-host'}, clock[0], True)
    assert unknown.value.code == 'P_CONFLICT'


def test_shared_rework_cap_preserves_local_identity_and_new_incoming_task_gets_new_unit(tmp_path, monkeypatch):
    clock = [int(time.time() * 1000)]
    monkeypatch.setattr(lc.time, 'time', lambda: clock[0] / 1000)
    host = _UncappedHarness(tmp_path, monkeypatch)
    host.bootstrap(include_neighbor=True)
    workflow = _workflow(host)
    owner, _ = host.assignment('question-owner', 'setter')
    context = _owner_work(host, workflow, owner)
    criteria = _criterion(host, owner, context, 'local-criteria-initial')
    _configure(host, owner, context, criteria)
    initial = host.store.read().local_budget_status(owner)
    procedure = host.store.read().procedures[(owner['version_id'], host.scope)]
    # Rework and reformulation use the same incoming unit and one counter.
    for number in range(1, 4):
        _downstream_work(host, workflow, owner, 'downstream-' + str(number))
        context = _owner_work(host, workflow, owner)
        if number == 2:
            replacement = _criterion(host, owner, context, 'local-criteria-revised')
            host.commit(host.message('decision', {'action': 'reformulate', 'subject': criteria,
                'replacement': replacement, 'reason': 'Actual controlled criterion correction.',
                'authority_proof': None, 'findings': []}, sender={'kind': 'assignment', 'ref': owner}, context=context))
            criteria = replacement
            repaired = host.store.read().local_budget_status(owner)
            assert repaired['iteration'] == number
            preparation = _owner_work(host, workflow, owner)
            preparation_window = host.store.read().local_budget_status(owner)['deadline_ms']
            _configure(host, owner, preparation, criteria, previous=procedure, suffix='same-repair')
            procedure = host.store.read().procedures[(owner['version_id'], host.scope)]
            assert host.store.read().local_budget_status(owner)['deadline_ms'] == preparation_window
        else:
            _configure(host, owner, context, criteria, previous=procedure, suffix=str(number))
            procedure = host.store.read().procedures[(owner['version_id'], host.scope)]
        current = host.store.read().local_budget_status(owner)
        assert current['unit_id'] == initial['unit_id']
        assert current['iteration'] == number and current['reworks_used'] == number
        assert current['remaining_ms'] <= 1000
    _downstream_work(host, workflow, owner, 'downstream-fourth')
    context = _owner_work(host, workflow, owner)
    replacement = _criterion(host, owner, context, 'over-limit-criteria')
    before = host.path.read_bytes()
    rejected = host.send(host.message('decision', {'action': 'reformulate', 'subject': criteria,
        'replacement': replacement, 'reason': 'A fourth actual correction must not gain a new allowance.',
        'authority_proof': None, 'findings': []}, sender={'kind': 'assignment', 'ref': owner}, context=context))
    assert rejected['error']['code'] == 'P_STATE'
    assert 'Maximum local reworks' in rejected['error']['message']
    assert host.path.read_bytes() == before
    assert not any(event['kind'] == 'escalation' for event in host.store.read().events)
    # A genuinely different incoming work item has independent local progress.
    other, _ = host.assignment('other-incoming', 'setter', owner=host.owner(work_item='foreign-service'))
    separate = host.store.read().local_budget_status(other)
    assert separate['unit_id'] != initial['unit_id']
    assert separate['reworks_used'] == 0 and separate['iteration'] == 0
    replayed = lc.Store(host.path, host.engagement).read()
    assert replayed.local_budget_status(owner)['reworks_used'] == 3
    # An actual upstream-owned input version creates a fresh incoming mandate,
    # rather than resetting the old unit by editing its own criteria.
    coordinator, _ = host.assignment('new-upstream-owner', 'setter', owner=host.owner(work_kind='integration'))
    framing = _owner_work(host, workflow, coordinator)
    upstream_criteria = _criterion(host, coordinator, framing, 'new-upstream-criteria')
    _configure(host, coordinator, framing, upstream_criteria, kind='layer')
    upstream_procedure = host.store.read().procedures[(coordinator['version_id'], host.scope)]
    for _ in range(6):
        workflow.advance(upstream_procedure)
    state = host.store.read()
    incoming = next(state._reference(identifier) for identifier, value in state.versions.items()
        if value['kind'] == 'delivery.assignment' and value['content']['record']['issued_under'] == coordinator
        and value['content']['record']['owner'] == state.resolve(owner, 'assignment')['owner'])
    assert state.resolve(incoming, 'assignment')['criteria'] == upstream_criteria
    fresh = state.local_budget_status(incoming)
    assert fresh['unit_id'] != initial['unit_id'] and fresh['reworks_used'] == 0
    # Explicit current owner invalidation makes its old clock historical, not a blocker.
    workflow.dispatcher._control(context, 'run_cancelled', total=1)
    context = _owner_work(host, workflow, owner)
    host.commit(host.message('decision', {'action': 'invalidate', 'subjects': [owner],
        'reason': 'The actual owner explicitly retires this incoming work.'},
        sender={'kind': 'assignment', 'ref': owner}, context=context))
    clock[0] += 2000
    assert host.store.read().local_budget_status(initial['unit_id'])['state'] == 'obsolete'
    assert workflow.pause_due()['notices'] == []
    assert host.store.read().local_budget_status(other)['state'] == 'ready'
    assert host.store.read().local_budget_status(incoming)['state'] == 'ready'
    import governed_layered
    resumed = governed_layered.LayeredSession(host.store, workflow.dispatcher.config, tmp_path / 'test-only-locator')
    offered = resumed.next()
    assert offered['status'] == 'invoke'
    current_jobs = [member['assignment'] for member in offered['members']]
    assert current_jobs
    assert all(host.store.read().local_budget_status(reference)['applicable'] for reference in current_jobs)
    assert any(reference in current_jobs for reference in (incoming, other))
    assert owner not in [member['assignment'] for member in offered['members']]
    resumed.stop(offered['invocation_id'], {'state': 'not-dispatched', 'fixture': 'No native call is made.'})
    # Existing typed collection work gets its own finite incoming unit even when
    # an ordinary solving unit has used all three repair rounds.
    collector = _downstream_work(host, workflow, coordinator, 'actual-escalation-collector', 'integrator')
    collector_context = _owner_work(host, workflow, collector)
    collector_record = host.store.read().resolve(collector, 'assignment')
    actor = {'owner': collector_record['owner'], 'author': collector, 'author_record': collector_record,
             'author_context': collector_context, 'principal': {'kind': 'assignment', 'ref': collector}}
    episode, _ = host.product('actual-bounded-dossier', actor, kind='escalation',
        material=[host.material('Actual controlled dossier: a prior local search exhausted its repair rounds.')],
        related=[{'slot_id': 'conflicts', 'refs': [upstream_criteria]}],
        episode={'root': None, 'previous': None, 'collection_head': host._proposal_head(),
                 'unfinished': [coordinator], 'decisive': True})
    before_pause = host.store.read().local_budget_status(coordinator)
    host.commit(host.message('escalation', {'assignment': collector, 'package': episode,
        'conflicts': [upstream_criteria], 'affected': [coordinator],
        'requested_decisions': ['Decide the current unresolved requirement using the retained bounded-search history.']},
        sender=actor['principal'], context=collector_context))
    suspended = host.store.read().local_budget_status(coordinator)
    assert suspended['state'] == 'idle' and suspended['remaining_ms'] == before_pause['remaining_ms']
    clock[0] += 3600000
    assert workflow.pause_due()['notices'] == []
    handling = workflow.handling_entry(episode, 'collect')['assignment']
    handling_unit = host.store.read().local_budget_status(handling)
    assert handling_unit['unit_id'] != suspended['unit_id']
    assert handling_unit['reworks_used'] == 0 and handling_unit['remaining_ms'] == 1000
    handling_grant = workflow.issue(handling, 'selection')['context']
    assert host.store.read().resolve(handling_grant, 'context')['expires_at_ms'] > clock[0]
    assert host.store.read().local_budget_status(coordinator)['remaining_ms'] == suspended['remaining_ms']


def test_planning_wait_retains_remaining_and_ready_integration_has_its_own_clock(tmp_path, monkeypatch):
    clock = [int(time.time() * 1000)]
    monkeypatch.setattr(lc.time, 'time', lambda: clock[0] / 1000)
    host = _UncappedHarness(tmp_path, monkeypatch)
    host.bootstrap(include_neighbor=True)
    workflow = _workflow(host)
    owner, _ = host.assignment('layer-owner', 'setter', owner=host.owner(work_kind='integration'))
    context = _owner_work(host, workflow, owner)
    clock[0] += 200
    criteria = _criterion(host, owner, context, 'layer-criteria')
    _configure(host, owner, context, criteria, kind='layer')
    planning = host.store.read().local_budget_status(owner)
    assert planning['phase'] == 'planning' and planning['state'] == 'idle'
    assert planning['remaining_ms'] == 800 and planning['deadline_ms'] is None
    clock[0] += 3600000
    assert workflow.pause_due()['notices'] == []
    assert host.store.read().local_budget_status(owner)['remaining_ms'] == 800
    # Only an actual ready integration mandate allocates the separate local unit.
    context = _owner_work(host, workflow, owner)
    parent = host.store.read().resolve(owner, 'assignment')
    child = copy.deepcopy(parent)
    child.update(responsibility='integrator', assigned_actor='actual-local-integrator', issued_under=owner)
    integration = host.record('ready-integration', 'assignment', child,
        sender={'kind': 'assignment', 'ref': owner}, context=context)
    host.commit(host.message('assignment', {'assignment': integration, 'owner': child['owner'],
        'responsibility': child['responsibility'], 'inputs': lc._input_locators(child['inputs']),
        'criteria': child['criteria']}, sender={'kind': 'assignment', 'ref': owner}, context=context))
    state = host.store.read()
    ready = state.local_budget_status(integration)
    assert ready['phase'] == 'integration' and ready['remaining_ms'] == 1000
    assert ready['deadline_ms'] is None and ready['unit_id'] != planning['unit_id']
    grant = workflow.issue(integration, 'selection')['context']
    assert host.store.read().local_budget_status(integration)['deadline_ms'] is None
    workflow.dispatcher._control(grant, 'run_started')
    active = host.store.read().local_budget_status(integration)
    assert active['deadline_ms'] == clock[0] + 1000
    assert host.store.read().local_budget_status(planning['unit_id'])['remaining_ms'] == 800


@pytest.mark.parametrize('aggregate_limit', [None, 800])
def test_batch_bound_uses_local_windows_optional_global_cap_and_once_physical_usage(tmp_path, monkeypatch, aggregate_limit):
    import json
    from test_governed_native_batches import _layer_session, _controlled_result, _choice, _role_result
    clock = [int(time.time() * 1000)]
    monkeypatch.setattr(lc.time, 'time', lambda: clock[0] / 1000)
    session = _layer_session(tmp_path, local_budget={'iteration_ms': 1000, 'max_reworks': 3},
                             aggregate_limit_ms=aggregate_limit)
    state = session.store.read()
    procedure = next(iter(state.procedures.values()))
    for _ in range(6):
        session.workflow.advance(procedure)
    state = session.store.read()
    questions = [state._reference(identifier) for identifier, value in state.versions.items()
                 if value['kind'] == 'delivery.assignment'
                 and value['content']['record']['owner']['work_kind'] == 'question'
                 and value['content']['record']['responsibility'] == 'setter'][:2]
    for assignment, elapsed in zip(questions, (200, 100)):
        def selection(packet):
            clock[0] += elapsed
            return _choice(packet)
        _controlled_result(session, assignment, 'selection', selection)
    state = session.store.read()
    before_local = [state.local_budget_status(assignment) for assignment in questions]
    assert [item['remaining_ms'] for item in before_local] == [700, 900]
    jobs = [{'assignment': assignment, 'phase': 'work',
             'selection': state.execution_plans[(assignment['version_id'], 'default')]} for assignment in questions]
    issued = session.issue_batch(jobs)
    physical = session.store.read().invocations[issued['invocation_id']]
    assert physical['bound_ms'] == (700 if aggregate_limit is None else 500)
    prepared = session.prepare(issued['invocation_id'])
    session.start(issued['invocation_id'], 'codex', 'controlled-local-batch', {'state': 'controlled-start'})
    results = [_role_result(session, member['packet']) for member in prepared['members']]
    clock[0] += 50
    session.complete(issued['invocation_id'], json.dumps({'format': 'jai.semantic-return/1', 'results': results}),
                     {'state': 'controlled-finish'})
    state = session.store.read()
    assert state.usage[('default', 'elapsed_ms', 'ms')]['spent'] == 350
    for member in prepared['members']:
        details = state.run_details[member['packet']['run_id']]
        assert details['usage']['elapsed_ms:ms'] == 50
        assert state.run_states[member['packet']['run_id']] == 'returned'
    assert [state.local_budget_status(assignment)['deadline_ms'] for assignment in questions] == [
        item['deadline_ms'] for item in before_local]
    replayed = lc.Store(session.store.path, session.store.engagement).read()
    assert replayed.usage == state.usage
