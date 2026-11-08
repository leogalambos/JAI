# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Real native selection/dispatch and telemetry obey explicit routing semantics."""
import copy
import json

import pytest

from governed_fixtures import ROOT
import execution_profiles as profiles
import execution_stats
import governed_layered
import model_router


@pytest.fixture(autouse=True)
def isolated_preferences(tmp_path, monkeypatch):
    monkeypatch.setenv('XDG_CONFIG_HOME', str(tmp_path / 'isolated-user'))


def _run_work(root, provider, mode, workload='research', *, legacy=False, monkeypatch=None):
    (root / '.jai').mkdir(parents=True)
    (root / '.jai/config.json').write_text(json.dumps({'schema_version': 1,
        'execution_profile': mode, 'context_policy': 'manual',
        'analytics': {'task_class': 'bounded-design', 'review_scope': 'substantive'},
        'overrides': {'responsibilities': {'setter': {
            'model_selector': 'inactive-fixed-setter', 'reasoning_effort': 'high'}}}
            if mode == 'workload' else {}}))
    model_config = root / 'model-overrides.json'
    model_config.write_text(json.dumps({'providers': {provider: {'classes': {workload: {
        'model_selector': 'selected-' + provider + '-' + workload, 'reasoning_effort': 'medium'}}}}}))
    if legacy:
        original = profiles.resolve
        def legacy_resolve(*args, **kwargs):
            result = original(*args, **kwargs)
            result.pop('routing_mode')
            return result
        monkeypatch.setattr(profiles, 'resolve', legacy_resolve)
    session, created = governed_layered.LayeredSession.create(root / '.fabric', 'workload-mode',
        b'Design bounded backups.', provider, 'backup', model_config=model_config)
    choice_call = session.issue_batch([{'assignment': created['entry']['assignment'], 'phase': 'selection'}])
    prepared = session.prepare(choice_call['invocation_id'])
    member = prepared['members'][0]
    choice = next(row for row in member['packet']['execution']['availability']
                  if row['provider'] == provider and row['workload_class'] == workload)
    session.start(choice_call['invocation_id'], provider, 'selection-handle', {'id': 'selection-handle'})
    assert session.efficiency()['summary']['routing_deviations'] is None
    session.complete(choice_call['invocation_id'], json.dumps({'format': 'jai.semantic-return/1', 'results': [{
        'member': member['member_key'], 'kind': 'selection', 'specialties': ['software-engineer'],
        'provider': provider, 'workload_class': workload, 'model_selector': choice['model_selector'],
        'reason': 'Actual locally chosen class for this exact fixture mandate.', 'previous': None}]}),
        {'status': 'returned'})
    selection = session.store.read().execution_plans[(created['entry']['assignment']['version_id'], 'default')]
    issued = session.issue_batch([{'assignment': created['entry']['assignment'], 'phase': 'work', 'selection': selection}])
    work = session.prepare(issued['invocation_id'])
    return session, created, issued, work


@pytest.mark.parametrize('provider', ['codex', 'claude'])
@pytest.mark.parametrize('workload', ['standard', 'research'])
def test_workload_mode_dispatches_actual_registry_override_for_both_providers(tmp_path, provider, workload):
    session, created, issued, work = _run_work(tmp_path, provider, 'workload', workload)
    args = work['invocation']['arguments']
    assert args['model'] == 'selected-' + provider + '-' + workload
    assert args['reasoning_effort' if provider == 'codex' else 'effort'] == 'medium'
    assert session.execution_profile['routing_mode'] == 'workload'
    assert session.execution_profile['configured'] is True
    assert work['routing_observations'][0]['preference'] is None
    session.start(issued['invocation_id'], provider, 'work-handle', {'id': 'work-handle'})
    assert session.efficiency()['summary']['routing_deviations'] is None


@pytest.mark.parametrize('provider', ['codex', 'claude'])
def test_actual_alternative_workload_is_visible_as_profile_deviation(tmp_path, provider):
    session, created, issued, work = _run_work(tmp_path, provider, 'standard')
    compared = work['routing_observations'][0]
    assert compared['differs'] is True
    assert compared['preference']['workload_class'] == 'standard'
    assert compared['selected']['workload_class'] == 'research'
    assert compared['selected']['model_selector'] == 'selected-' + provider + '-research'
    assert compared['served_model'] is None
    session.start(issued['invocation_id'], provider, 'work-handle', {'id': 'work-handle'})
    notice = session.efficiency()
    assert notice['summary']['routing_deviations'] == 1
    assert '| standard* |' in notice['table']
    assert 'Routing differs' in notice['table']
    assert len(notice['table'].splitlines()) == 3
    assert execution_stats.history(tmp_path)[-1]['routing_observations'][0]['selected'] == compared['selected']


def test_matching_work_and_cold_resume_preserve_recorded_mode_and_actual_routing(tmp_path):
    session, created, issued, work = _run_work(tmp_path, 'codex', 'standard', 'standard')
    assert work['routing_observations'][0]['differs'] is False
    session.start(issued['invocation_id'], 'codex', 'work-handle', {'id': 'work-handle'})
    assert session.efficiency()['summary']['routing_deviations'] == 0
    before = copy.deepcopy(session.execution_profile)
    profiles.select(tmp_path, 'workload')
    reopened = governed_layered.LayeredSession.open(created['locator'])
    assert reopened.execution_profile == before
    assert reopened.prepare(issued['invocation_id'])['invocation'] == work['invocation']
    assert reopened.efficiency()['summary']['routing_deviations'] == 0


def test_legacy_missing_mode_field_stays_missing_and_keeps_original_semantics_on_resume(tmp_path, monkeypatch):
    session, created, issued, work = _run_work(tmp_path, 'codex', 'standard', legacy=True, monkeypatch=monkeypatch)
    assert 'routing_mode' not in session.execution_profile
    before = copy.deepcopy(session.execution_profile)
    with monkeypatch.context() as local:
        local.setattr(profiles, 'resolve', lambda *args, **kwargs: pytest.fail('resume reread preferences'))
        reopened = governed_layered.LayeredSession.open(created['locator'])
        assert reopened.execution_profile == before
        assert reopened.prepare(issued['invocation_id'])['routing_observations'][0]['differs'] is True
