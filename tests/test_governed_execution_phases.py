# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""A real local chooser produces the intrinsic choice consumed by fresh work."""
import json
import pytest

from test_governed_dispatch import host, _worker_config, _dispatcher, _answer
import lifecycle as lc
from governed_dispatch import DispatchError


def test_real_functional_entity_chooses_from_full_catalogue_then_executes_own_result(host, tmp_path):
    # Setter preparation is synthetic Store scaffolding; the author choice and
    # work below are captured from two actual independently confined processes.
    actor = host.setup_author(start_author=False)
    config, _, _ = _worker_config(tmp_path / 'worker', host, actor)
    selection_context = host.context('actual-author-choice', actor['author'], actor['author_record'],
                                      phase='selection', start=False)
    selected = _dispatcher(host, config).dispatch(selection_context)
    assert selected['completion']['status'] == 'committed', selected
    state = host.store.read()
    choice = next(reference for reference in selected['completion']['receipt']['created_versions']
                  if state.versions[reference['version_id']]['kind'] == 'delivery.decision')
    assert lc.version_id(state.versions[choice['version_id']]) == choice['version_id']
    physical = state.resolve(selection_context, 'context')
    assert state.run_states[physical['run_id']] == 'returned'
    assert state.assignment_states[actor['author']['version_id']] == 'open'
    assert not any(value['logical_id'] == 'worker-generated-answer' for value in state.versions.values())
    audit = json.loads(host.store._blob(selected['audit_blob_id']))
    assert any(item.get('request', {}).get('operation') == 'propose' and 'error' in item for item in audit['events'])
    work_context = host.context('actual-author-work', actor['author'], actor['author_record'],
                                selection=choice, start=False)
    execution = host.store.read().context_execution(host.store.read().resolve(work_context, 'context'))
    assert execution['selection'] == choice
    assert execution['specialties'] == ['software-engineer']
    completed = _dispatcher(host, config).dispatch(work_context)
    assert completed['completion']['status'] == 'committed', completed
    record, report = _answer(host)
    assert report['scratch_write']
    assert record['assignment'] == actor['author']
    assert report['catalogue_count'] > 100
    assert report['unselected_instruction_readable']
    assert report['catalogue_readonly']
    assert report['protected_task_denied']
    assert report['selected_specialties'] == ['software-engineer']
    assert report['selected_instruction_slugs'] == ['software-engineer']
    state = host.store.read()
    feedback = _dispatcher(host, config)._owned_returns(state, actor['setter'],
        state.resolve(actor['setter'], 'assignment'), state.ready_basis(actor['setter']))
    returned = next(item for item in feedback if item['assignment'] == actor['author'])
    assert returned['records'][0]['record'] == record
    assert returned['intents'][0]['message_type'] == 'submission'
    assert returned['intents'][0]['payload']['candidate'] == returned['records'][0]['ref']


def test_captured_choice_cannot_be_substituted_and_can_staff_fresh_work_contexts(host, tmp_path):
    actor = host.setup_author(suffix='choice-owner', start_author=False)
    other = host.setup_author(suffix='other-entity', start_author=False)
    config, _, _ = _worker_config(tmp_path / 'worker', host, actor)
    selection_context = host.context('actual-choice', actor['author'], actor['author_record'], phase='selection', start=False)
    result = _dispatcher(host, config).dispatch(selection_context)
    state = host.store.read()
    assert state.context_execution(state.resolve(selection_context, 'context'))['phase'] == 'selection'
    choice = next(reference for reference in result['completion']['receipt']['created_versions']
                  if state.versions[reference['version_id']]['kind'] == 'delivery.decision')
    before = host.path.read_bytes()
    with pytest.raises(AssertionError) as failure:
        host.context('foreign-choice', other['author'], other['author_record'], selection=choice, start=False)
    assert failure.value.args[0]['error']['code'] == 'P_ORIGIN'
    assert host.path.read_bytes() == before
    context = host.context('first-use', actor['author'], actor['author_record'], selection=choice, start=False)
    state = host.store.read()
    with pytest.raises(lc.ERROR) as failure:
        state.context_execution({**state.resolve(context, 'context'), 'execution': None})
    assert failure.value.code == 'P_CONTEXT'
    host.cancel_run(context)
    second = host.context('second-use', actor['author'], actor['author_record'], selection=choice, start=False)
    assert second != context
    assert host.store.read().context_execution(host.store.read().resolve(second, 'context'))['selection'] == choice
    host.cancel_run(second)


def test_actual_local_choice_of_unavailable_model_never_grants_work(host, tmp_path):
    actor = host.setup_author(suffix='unsupported-model', start_author=False)
    config, _, output = _worker_config(tmp_path / 'worker', host, actor)
    context = host.context('unsupported-local-choice', actor['author'], actor['author_record'], phase='selection', start=False)
    with pytest.raises(DispatchError) as failure:
        _dispatcher(host, config).dispatch(context)
    assert failure.value.code == 'P_PROOF'
    state = host.store.read()
    assert state.run_states[state.resolve(context, 'context')['run_id']] == 'cancelled'
    assert not any(value['kind'] == 'delivery.decision' and
                   value['content']['record']['message']['payload'].get('assignment') == actor['author']
                   for value in state.versions.values())
    assert list(output.iterdir()) == []
