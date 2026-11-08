# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Honest incremental model-time analytics and private project history."""
import copy
import json
from types import SimpleNamespace

import pytest

from governed_fixtures import ROOT
import execution_stats as stats
from test_governed_native_session import prepared


def _transaction(*effects):
    return {'operations': [{'data': {'effects': list(effects)}}]}


def _state():
    return SimpleNamespace(transactions=[], invocations={})


def _summary(profile='standard', **changes):
    accumulator = stats.Accumulator('internal engagement identity', profile, task_class='code', review_scope='substantive', config_version='a' * 64)
    value = accumulator.summary('accepted')
    observation = stats.execution_profiles.routing_observation(_preferences(), 'author', 'standard',
                       {'model_selector': 'test-model', 'reasoning_effort': 'medium'})
    value.update(invocations=1, routing_deviations=0, routing_observations=[{**observation, 'occurrences': 1}])
    value.update(changes)
    return value


def test_new_effect_suffix_counts_reworks_findings_and_physical_time_once():
    state = _state()
    state.invocations['call'] = {'responsibility': 'author', 'started_at_ms': 100, 'finished_at_ms': 500,
                                 'model_controls': {'model_selector': 'test-model'}, 'members': [{}, {}]}
    finding = {'version_id': 'finding-version'}
    assessment = {'kind': 'delivery.assessment', 'content': {'record': {'findings': [finding]}}}
    state.transactions.extend([
        _transaction({'op': 'invocation', 'invocation_id': 'call'}),
        _transaction({'op': 'local-update', 'unit_id': 'local', 'value': {'reworks_used': 2}}),
        _transaction({'op': 'register', 'manifest': assessment}),
        _transaction({'op': 'register', 'manifest': assessment}),
    ])
    accumulator = stats.Accumulator('run')
    assert accumulator.update(state)
    initial = accumulator.summary()
    assert initial['elapsed_ms'] == 400
    assert initial['role_elapsed_ms'] == {'author': 400}
    assert initial['invocations'] == 1
    assert initial['rework_rounds'] == 2
    assert initial['findings'] == 1
    assert initial['reviews'] == 1
    assert initial['observed_models'] == []
    assert initial['requested_models'] == ['test-model']
    assert not accumulator.update(state)
    assert accumulator.summary() == initial
    # Already-consumed prefix is never read again on normal progress.
    state.transactions[0] = None
    state.transactions.append(_transaction({'op': 'local-update', 'unit_id': 'local', 'value': {'reworks_used': 3}}))
    assert accumulator.update(state)
    assert accumulator.summary()['rework_rounds'] == 3
    assert accumulator.summary()['recommendation']['action'] == 'inspect-rework-causes'


def test_start_is_not_completion_and_compact_table_cannot_claim_acceptance():
    state = _state()
    state.invocations['call'] = {'responsibility': 'reviewer', 'started_at_ms': 10}
    state.transactions.append(_transaction({'op': 'invocation', 'invocation_id': 'call'}))
    accumulator = stats.Accumulator('run')
    accumulator.update(state)
    assert accumulator.summary()['elapsed_ms'] == 0
    state.invocations['call']['finished_at_ms'] = 310
    state.transactions.append(_transaction({'op': 'invocation-update', 'invocation_id': 'call'}))
    accumulator.update(state)
    summary = accumulator.summary('returned')
    table = stats.compact_table(summary)
    assert len(table.splitlines()) == 3
    assert 'returned' in table and 'accepted' not in table
    assert '0.3s' in table and 'Model time' in table
    assert 'cost' not in table.lower() and 'tokens' not in table.lower()
    with pytest.raises(ValueError, match='outcome'):
        accumulator.summary('model says approved')
    state.transactions.clear()
    with pytest.raises(ValueError, match='history shrank'):
        accumulator.update(state)


@pytest.mark.parametrize('field,value', [('profile', '../escape'), ('task_class', 'secret task text'), ('review_scope', '| injected |')])
def test_untrusted_display_labels_are_rejected(field, value):
    with pytest.raises(ValueError):
        stats.Accumulator('run', **{field: value})


def test_project_history_atomic_upsert_filter_and_no_task_content(tmp_path):
    first = _summary()
    path = stats.record(tmp_path, first)
    assert path.parent == tmp_path / '.jai' / 'stats'
    before = path.stat().st_mtime_ns
    assert stats.record(tmp_path, first) == path
    assert path.stat().st_mtime_ns == before
    assert stats.history(tmp_path) == [first]
    assert stats.history(tmp_path, 'research') == []
    second = _summary('research')
    second['run_id'] = 'b' * 64
    stats.record(tmp_path, second)
    assert stats.history(tmp_path, 'research') == [second]
    raw = path.read_text()
    assert 'internal engagement identity' not in raw
    assert 'prompt' not in raw and 'material' not in raw
    assert not list(path.parent.glob('.stats-*'))
    contaminated = dict(first, task='confidential request')
    with pytest.raises(ValueError, match='Closed'):
        stats.record(tmp_path, contaminated)


def test_project_storage_rejects_directory_and_record_symlinks(tmp_path):
    outside = tmp_path / 'outside'
    outside.mkdir()
    project = tmp_path / 'project'
    project.mkdir()
    (project / '.jai').symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match='symbolic'):
        stats.record(project, _summary())
    with pytest.raises(ValueError, match='symbolic'):
        stats.history(project)
    (project / '.jai').unlink()
    (project / '.jai' / 'stats').mkdir(parents=True)
    record = project / '.jai' / 'stats' / (_summary()['run_id'] + '.json')
    record.symlink_to(outside / 'private.json')
    with pytest.raises(ValueError, match='symbolic'):
        stats.record(project, _summary())
    with pytest.raises(ValueError, match='symbolic'):
        stats.history(project)


def test_history_rejects_tampered_records_and_cli_reports_empty(tmp_path, capsys):
    assert stats.main(['--project', str(tmp_path), 'last']) == 0
    assert 'No execution statistics' in capsys.readouterr().out
    path = stats.record(tmp_path, _summary())
    value = json.loads(path.read_text())
    value['observed_models'] = ['unverified-served-model']
    path.write_text(json.dumps(value))
    with pytest.raises(ValueError, match='served-model'):
        stats.history(tmp_path)
    with pytest.raises(SystemExit):
        stats.main(['--project', str(tmp_path)])


def test_comparison_requires_explicit_cohorts_and_keeps_incomplete_tasks_out():
    first, second = _summary(), _summary('stronger-author', elapsed_ms=3000)
    second['run_id'] = 'b' * 64
    comparison = stats.compare([first, second], ['standard', 'stronger-author'])
    assert len(comparison['cohorts']) == 2
    assert comparison['cohorts'][1]['mean_model_ms'] == 3000
    assert comparison['recommendation'] == 'advisory-only'
    for field in ('task_class', 'review_scope'):
        changed = dict(second, **{field: 'unspecified'})
        assert not stats.compare([first, changed], ['standard', 'stronger-author'])['cohorts']
    assert not stats.compare([first, dict(second, outcome='returned')], ['standard', 'stronger-author'])['cohorts']
    assert not stats.compare([first, dict(second, provider='claude')], ['standard', 'stronger-author'])['cohorts']
    with pytest.raises(ValueError):
        stats.compare([first], ['standard', 'standard'])


def test_native_verified_store_suffix_is_consumed_without_replay(prepared):
    host, actor, config, output, session, issued, selection = prepared
    accumulator = stats.Accumulator('actual store integration')
    state = host.store.read()
    assert accumulator.update(state)
    summary = accumulator.summary()
    assert summary['invocations'] == 1
    assert summary['elapsed_ms'] == 0
    assert summary['observed_models'] == []
    assert not accumulator.update(host.store.read())


def test_configuration_version_changes_with_model_effort_fallback_and_context():
    snapshot = {'provider': 'codex', 'configured': True, 'context_policy': 'isolated-handoffs',
                'context': {'workers': 'fresh-bounded'}, 'responsibilities': {
                    'author': {'workload_class': 'standard', 'model': {'model_selector': 'example',
                              'reasoning_effort': 'medium', 'fallbacks': [{'model_selector': 'fallback'}]}}},
                'sources': ['/private/source.json'], 'analytics': {'task_class': 'code'}}
    original = stats.configuration_version(snapshot)
    unrelated = copy.deepcopy(snapshot)
    unrelated['sources'] = ['/different/private.json']
    unrelated['execution_profile'] = 'different-name'
    unrelated['analytics'] = {'task_class': 'docs'}
    assert stats.configuration_version(unrelated) == original
    for field, value in [('model_selector', 'stronger'), ('reasoning_effort', 'high'),
                         ('fallbacks', [{'model_selector': 'other'}])]:
        changed = copy.deepcopy(snapshot)
        changed['responsibilities']['author']['model'][field] = value
        assert stats.configuration_version(changed) != original
    changed = copy.deepcopy(snapshot)
    changed['context_policy'] = 'manual'
    assert stats.configuration_version(changed) != original
    assert stats.configuration_version(None) is None
    with pytest.raises(ValueError):
        stats.configuration_version({})


def test_comparison_refuses_same_named_profile_with_mixed_or_unknown_configurations():
    first = _summary()
    second = _summary('stronger-author', elapsed_ms=3000, config_version='b' * 64)
    second['run_id'] = 'b' * 64
    changed = dict(second, config_version='c' * 64, run_id='c' * 64)
    comparison = stats.compare([first, second, changed], ['standard', 'stronger-author'])
    assert not comparison['cohorts']
    assert 'mixed effective configuration' in comparison['limitation']
    comparison = stats.compare([first, second], ['standard', 'stronger-author'])
    assert {row['config_version'] for row in comparison['cohorts']} == {'a' * 64, 'b' * 64}
    legacy = dict(second)
    legacy.pop('config_version')
    assert not stats.compare([first, legacy], ['standard', 'stronger-author'])['cohorts']
    with pytest.raises(ValueError, match='Configuration version'):
        stats.Accumulator('run', config_version='not-a-version')


def _preferences(mode='profile'):
    return {'provider': 'codex', 'configured': mode == 'profile', 'routing_mode': mode,
            'responsibilities': {'author': {'workload_class': 'standard',
                  'model': {'model_selector': 'test-model', 'reasoning_effort': 'medium'}}}}


def _routing_state(workload='standard', selector='test-model', effort='medium', phase='work', members=1):
    state = _state()
    records = {'selection': {'message': {'payload': {'workload_class': workload}}},
               'context': {'execution': {'phase': phase, 'selection': 'selection'}}}
    def resolve(reference, kind=None):
        return records[reference]
    state.resolve = resolve
    state.invocations['call'] = {'phase': phase, 'responsibility': 'author', 'started_at_ms': 100,
             'model_controls': {'model_selector': selector, 'model': {'model_selector': selector,
                                 'reasoning_effort': effort}},
             'members': [{'context': 'context'} for index in range(members)]}
    state.transactions.append(_transaction({'op': 'invocation', 'invocation_id': 'call'}))
    return state


def test_work_routing_deviation_is_physical_once_and_preferences_are_pinned(tmp_path):
    preferences = _preferences()
    accumulator = stats.Accumulator('routing', preferences=preferences)
    preferences['responsibilities']['author']['model']['reasoning_effort'] = 'high'
    state = _routing_state(effort='high', members=2)
    accumulator.update(state)
    summary = accumulator.summary('returned')
    assert summary['routing_deviations'] == 1
    assert len(summary['routing_observations']) == 1
    row = summary['routing_observations'][0]
    assert row['occurrences'] == 1 and row['differs']
    assert row['preference']['reasoning_effort'] == 'medium'
    assert row['selected']['reasoning_effort'] == 'high'
    assert row['served_model'] is None
    assert summary['recommendation']['action'] == 'inspect-routing'
    table = stats.compact_table(summary)
    assert len(table.splitlines()) == 3 and '| standard* |' in table
    assert 'Routing differs; inspect details' in table
    stats.record(tmp_path, summary)
    assert stats.history(tmp_path) == [summary]
    state.transactions[0] = None
    def prohibit_repeated_selection_read(reference, kind=None):
        raise AssertionError('Immutable captured routing must not be reread on completion')
    state.resolve = prohibit_repeated_selection_read
    state.transactions.append(_transaction({'op': 'invocation-update', 'invocation_id': 'call'}))
    accumulator.update(state)
    assert accumulator.summary()['routing_deviations'] == 1
    assert accumulator.summary()['routing_observations'][0]['occurrences'] == 1


def test_matching_work_routing_is_known_zero_but_different_class_counts_deviation():
    accumulator = stats.Accumulator('matching', preferences=_preferences())
    accumulator.update(_routing_state())
    summary = accumulator.summary()
    assert summary['routing_deviations'] == 0
    assert summary['routing_observations'][0]['differs'] is False
    assert '| standard |' in stats.compact_table(summary)
    accumulator = stats.Accumulator('different-workload', preferences=_preferences())
    accumulator.update(_routing_state(workload='heavy'))
    assert accumulator.summary()['routing_deviations'] == 1
    row = accumulator.summary()['routing_observations'][0]
    assert row['selected']['model_selector'] == row['preference']['model_selector']
    assert row['selected']['reasoning_effort'] == row['preference']['reasoning_effort']


def test_known_deviation_remains_visible_when_other_work_has_unknown_attribution():
    state = _routing_state(effort='high')
    state.invocations['unknown-call'] = copy.deepcopy(state.invocations['call'])
    state.invocations['unknown-call']['members'] = [{'context': 'missing-context'}]
    state.transactions.append(_transaction({'op': 'invocation', 'invocation_id': 'unknown-call'}))
    accumulator = stats.Accumulator('mixed-coverage', preferences=_preferences())
    accumulator.update(state)
    summary = accumulator.summary()
    assert summary['routing_deviations'] is None
    assert any(row['differs'] for row in summary['routing_observations'])
    assert summary['recommendation']['action'] == 'inspect-routing'
    table = stats.compact_table(summary)
    assert len(table.splitlines()) == 3
    assert '| standard* |' in table and 'Routing differs' in table
    assert 'incomplete' in table


@pytest.mark.parametrize('preferences,phase', [(None, 'work'), (_preferences(), 'selection'),
                                             (_preferences('workload'), 'work')])
def test_legacy_selection_and_workload_mode_do_not_claim_fixed_role_matches(preferences, phase):
    accumulator = stats.Accumulator('unknown', preferences=preferences)
    accumulator.update(_routing_state(phase=phase))
    summary = accumulator.summary()
    assert summary['routing_deviations'] is None
    assert summary['routing_observations'] == []
    assert 'standard*' not in stats.compact_table(summary)


def test_missing_and_unsafe_work_attribution_stays_unknown_and_private(tmp_path):
    for state in (_routing_state(selector='/private/secret-model'), _routing_state()):
        if state.invocations['call']['model_controls']['model_selector'] == 'test-model':
            state.invocations['call']['members'] = [{'context': 'missing-private-context'}]
        accumulator = stats.Accumulator('unsafe', preferences=_preferences())
        accumulator.update(state)
        summary = accumulator.summary()
        assert summary['routing_deviations'] is None
        assert summary['routing_observations'] == []
        path = stats.record(tmp_path, summary)
        assert 'private' not in path.read_text()


def test_comparison_refuses_mixed_actual_routing_and_legacy_telemetry_unknown():
    first, second = _summary(), _summary('stronger-author')
    divergent = copy.deepcopy(second)
    divergent['routing_deviations'] = 1
    divergent['routing_observations'][0]['selected']['reasoning_effort'] = 'high'
    divergent['routing_observations'][0]['differs'] = True
    comparison = stats.compare([first, second, divergent], ['standard', 'stronger-author'])
    assert not comparison['cohorts']
    assert 'routing signatures' in comparison['limitation']
    # Both profiles may have their own consistent actual routing; occurrence
    # counts do not change routing identity when rework repeats the same choice.
    repeated = copy.deepcopy(second)
    repeated['invocations'] = 2
    repeated['routing_observations'][0]['occurrences'] = 2
    assert stats.compare([first, second, repeated], ['standard', 'stronger-author'])['cohorts']
    legacy = copy.deepcopy(second)
    legacy.pop('routing_deviations')
    legacy.pop('routing_observations')
    assert not stats.compare([first, legacy], ['standard', 'stronger-author'])['cohorts']
    assert 'stronger-author*' not in stats.compact_table(legacy)


@pytest.mark.parametrize('change', [{'served_model': 'unverified'}, {'extra': '/private/path'},
                                   {'occurrences': 0}, {'differs': True}])
def test_private_history_rejects_invented_or_open_routing_rows(tmp_path, change):
    value = _summary()
    value['routing_observations'][0].update(change)
    with pytest.raises(ValueError):
        stats.record(tmp_path, value)
