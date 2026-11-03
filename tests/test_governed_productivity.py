# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Standing local plans retain history without granting future stale work."""
import copy
import time
import json

import pytest

from governed_fixtures import GovernedHarness
import lifecycle as lc


@pytest.fixture
def host(tmp_path, monkeypatch):
    instance = GovernedHarness(tmp_path, monkeypatch)
    instance.bootstrap()
    return instance


def test_standing_execution_plan_is_future_only_and_context_grants_remain_single_use(tmp_path):
    from test_governed_invocations import _workflow
    import governed_native
    workflow, assignment = _workflow(tmp_path)
    session = governed_native.NativeSession(workflow.store, workflow.dispatcher.config)

    def choose(handle):
        issued = session.issue_batch([{'assignment': assignment, 'phase': 'selection'}], bound_ms=5000)
        descriptor = session.prepare(issued['invocation_id'])
        packet = descriptor['members'][0]['packet']
        available = next(item for item in packet['execution']['availability']
                         if item['provider'] == 'codex' and item['workload_class'] == 'standard')
        choice = {'member': packet['member_key'], 'kind': 'selection', 'specialties': ['software-engineer'],
                  'provider': 'codex', 'workload_class': 'standard',
                  'model_selector': available['model_selector'],
                  'reason': 'Controlled offline local staffing decision; no professional evidence claim.'}
        session.start(issued['invocation_id'], 'codex', handle, {'state': 'controlled-start'})
        session.complete(issued['invocation_id'], json.dumps({'format': 'jai.semantic-return/1',
                         'results': [choice]}), {'state': 'controlled-result'})
        return workflow.store.read().execution_plans[(assignment['version_id'], 'default')]

    first = choose('controlled-planning-one')
    active = session.issue_batch([{'assignment': assignment, 'phase': 'work', 'selection': first}], bound_ms=5000)
    second = choose('controlled-planning-two')
    state = workflow.store.read()
    assert second != first
    assert state.execution_plans[(assignment['version_id'], 'default')] == second
    old_context = active['members'][0]['context']
    assert state.context_execution(state.resolve(old_context, 'context'))['selection'] == first
    before = workflow.store.path.read_bytes()
    with pytest.raises(ValueError) as failure:
        session.issue_batch([{'assignment': assignment, 'phase': 'work', 'selection': first}], bound_ms=5000)
    assert failure.value.code == 'P_CONFLICT'
    assert workflow.store.path.read_bytes() == before
    # Earlier bounded authority still starts after a future staffing preference changes.
    session.prepare(active['invocation_id'])
    session.start(active['invocation_id'], 'codex', 'controlled-old-active', {'state': 'controlled-start'})
    session.stop(active['invocation_id'], {'state': 'terminated', 'observation': 'Controlled stop confirmation.'})
    for label in ('current', 'reuse'):
        issued = session.issue_batch([{'assignment': assignment, 'phase': 'work', 'selection': second}], bound_ms=5000)
        session.stop(issued['invocation_id'], {'state': 'not-dispatched', 'observation': label})
    state = workflow.store.read()
    replay = lc.replay(state.transactions, engagement=workflow.store.engagement, blob_reader=workflow.store._blob)
    assert replay.execution_plans == state.execution_plans
    assert all(transaction['format'] == 9 for transaction in state.transactions)


def test_owner_procedure_requires_actual_local_criteria_and_exact_predecessor(host):
    setter, assigned = host.assignment('setter', 'setter')
    context = host.context('setter', setter, assigned)
    criteria = copy.deepcopy(host.store.read().resolve(host.criteria, 'source'))
    criteria['owner'] = assigned['owner']
    criteria['origin'] = {'kind': 'assignment', 'ref': setter}
    local = host.record('local-criteria', 'source', criteria,
                        sender={'kind': 'assignment', 'ref': setter}, context=context)
    payload = {'action': 'configure_procedure', 'assignment': setter, 'criteria': local,
               'kind': 'question', 'specification': {'question': 'What service is required?',
               'author_task': 'Describe the service.', 'reviewer_task': 'Review the service description.'},
               'previous': None, 'reason': 'Ordinary positive continuation under local criteria.',
               'authority_proof': None}
    receipt = host.commit(host.message('decision', payload, sender={'kind': 'assignment', 'ref': setter}, context=context))
    state = host.store.read()
    current = state.procedures[(setter['version_id'], host.scope)]
    assert current in receipt['created_versions']
    assert state.resolve(current)['message']['payload']['specification'] == payload['specification']
    assert state._status(local, host.scope)['validity'] == 'valid'
    expected = state.procedure_next(current)
    assert expected['step'] == 'author'
    assert expected['assignment']['record']['procedure_task'] == {'procedure': current, 'path': '/author_task'}
    assert expected['assignment']['record']['criteria'] == local
    wrong = host.message('control_event', {'event': 'procedure_step', 'procedure': current,
                         'step': expected['step'], 'triggers': [local]})
    before = host.path.read_bytes()
    rejected = host.send(wrong)
    assert rejected['error']['code'] == 'P_CONFLICT'
    assert host.path.read_bytes() == before
    receipt = host.commit(host.message('control_event', {'event': 'procedure_step', 'procedure': current,
                          'step': expected['step'], 'triggers': expected['triggers']}))
    state = host.store.read()
    child = next(ref for ref in receipt['created_versions'] if state.versions[ref['version_id']]['kind'] == 'delivery.assignment')
    assert state.resolve(child, 'assignment')['issued_under'] == setter
    assert state.provenance[child['version_id']]['origin']['kind'] == 'controller'
    assert state.procedure_steps[current['version_id']]['author']['resolved'] == [child]
    assert state.procedure_next(current)['waiting'] == 'author_result'
    unrelated, _ = host.assignment('unrelated-owner', 'setter', owner=host.owner(question='why'))
    update_context = host.context('updated-owner-policy', setter, assigned)
    replacement_payload = {**payload, 'previous': current,
        'specification': {**payload['specification'], 'author_task': 'Describe the service and its explicit boundary.'}}
    host.commit(host.message('decision', replacement_payload,
        sender={'kind': 'assignment', 'ref': setter}, context=update_context))
    state = host.store.read()
    replacement = state.procedures[(setter['version_id'], host.scope)]
    assert replacement != current
    assert state._status(current, host.scope)['validity'] == 'invalid'
    assert state._status(child, host.scope)['validity'] == 'invalid'
    assert state._status(unrelated, host.scope)['validity'] == 'valid'
    assert state._status(setter, host.scope)['validity'] == 'valid'
    with pytest.raises(lc.ERROR) as failure:
        state.procedure_next(current)
    assert failure.value.code == 'P_CONTEXT'
    assert state.procedure_next(replacement)['step'] == 'author'
