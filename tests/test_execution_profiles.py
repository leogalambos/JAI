# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Execution preferences are explicit, pinned and independent of authority."""
import copy
import json

import pytest

from governed_fixtures import ROOT
import execution_profiles as profiles
import model_router


@pytest.fixture
def registry():
    """Use the shipped registry, with no ambient administrator overrides."""
    return model_router.load(ROOT / '.ai/runtime/models/model-registry.json')


@pytest.fixture(autouse=True)
def private_user_config(tmp_path, monkeypatch):
    """Keep tests independent of the developer's installed configuration."""
    monkeypatch.setenv('XDG_CONFIG_HOME', str(tmp_path / 'user-config'))


def _write(project, name, value):
    path = project / '.jai' / name
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(value), encoding='utf-8')
    return path


def test_available_lists_builtins_without_writing_and_keeps_legacy_routing(tmp_path, registry):
    result = profiles.available(tmp_path)
    assert result['active'] == 'workload'
    assert {entry['name'] for entry in result['profiles']} == {
        'standard', 'stronger-reviewer', 'stronger-author', 'stronger-setter',
        'high-assurance', 'economy', 'research', 'workload'}
    assert not (tmp_path / '.jai').exists()
    snapshot = profiles.resolve(tmp_path, registry, 'codex')
    assert snapshot['configured'] is False
    workload, selected = profiles.mapping(snapshot, 'author', 'research', registry)
    assert workload == 'research'
    assert selected['model_selector'] == registry['providers']['codex']['classes']['research']['model_selector']


@pytest.mark.parametrize('provider', ['codex', 'claude'])
@pytest.mark.parametrize('name,role,workload,effort', [
    ('standard', 'setter', 'standard', 'medium'),
    ('stronger-reviewer', 'reviewer', 'heavy', 'high'),
    ('stronger-author', 'author', 'heavy', 'high'),
    ('stronger-setter', 'setter', 'heavy', 'high'),
    ('high-assurance', 'author', 'heavy', 'high'),
    ('economy', 'author', 'light', 'medium'),
    ('research', 'author', 'research', 'xhigh'),
])
def test_profile_resolves_same_intent_for_each_provider(tmp_path, registry, provider, name, role, workload, effort):
    snapshot = profiles.resolve(tmp_path, registry, provider, profile=name)
    actual, mapping = profiles.mapping(snapshot, role, workload, registry)
    assert actual == workload
    assert mapping['reasoning_effort'] == effort
    assert snapshot['context']['workers'] == 'fresh-bounded'
    assert snapshot['context']['reviewer'] == 'independent'
    assert snapshot['configured'] is True


def test_integration_selection_is_atomic_preserves_fields_and_pins_snapshot(tmp_path, registry):
    _write(tmp_path, 'config.json', {'schema_version': 1, 'context_policy': 'manual'})
    receipt = profiles.select(tmp_path, 'stronger-reviewer')
    assert receipt['scope'] == 'project'
    assert receipt['active_runs_changed'] is False
    before = profiles.resolve(tmp_path, registry, 'codex')
    assert before['context_policy'] == 'manual'
    assert before['responsibilities']['reviewer']['workload_class'] == 'heavy'
    profiles.select(tmp_path, 'economy')
    after = profiles.resolve(tmp_path, registry, 'codex')
    assert after['execution_profile'] == 'economy'
    assert before['execution_profile'] == 'stronger-reviewer'
    assert before['responsibilities']['author']['workload_class'] == 'standard'
    assert not list((tmp_path / '.jai').glob('.profile-*'))
    assert json.loads(json.dumps(before)) == before


def test_integration_scope_precedence_and_custom_inheritance(tmp_path, registry):
    user = tmp_path / 'user.json'
    user.write_text(json.dumps({'schema_version': 1, 'execution_profile': 'stronger-reviewer',
        'profiles': {'custom': {'extends': 'stronger-author', 'providers': {'codex': {
            'author': {'model_selector': 'custom-model', 'reasoning_effort': 'xhigh'}}}}}}))
    _write(tmp_path, 'config.json', {'schema_version': 1, 'execution_profile': 'custom'})
    _write(tmp_path, 'config.local.json', {'schema_version': 1, 'context_policy': 'task-isolated'})
    result = profiles.resolve(tmp_path, registry, 'codex', user_config=user)
    assert result['sources'] == ['bundled', 'user', 'project', 'local']
    assert result['responsibilities']['author']['model']['model_selector'] == 'custom-model'
    assert result['responsibilities']['author']['model']['reasoning_effort'] == 'xhigh'
    assert result['context_policy'] == 'task-isolated'
    assert result['responsibilities']['setter']['model']['reasoning_effort'] == 'high'
    explicit = profiles.resolve(tmp_path, registry, 'codex', profile='research', user_config=user)
    assert explicit['execution_profile'] == 'research'
    assert explicit['sources'][-1] == 'invocation'


def test_integration_session_choice_does_not_persist_and_local_choice_wins(tmp_path):
    receipt = profiles.select(tmp_path, 'research', session=True)
    assert receipt['scope'] == 'session'
    assert profiles.available(tmp_path)['active'] == 'workload'
    assert not (tmp_path / '.jai').exists()
    profiles.select(tmp_path, 'stronger-author')
    profiles.select(tmp_path, 'economy', local=True)
    assert profiles.available(tmp_path)['active'] == 'economy'


@pytest.mark.parametrize('value,match', [
    ({'schema_version': 2}, 'schema_version'),
    ({'schema_version': True}, 'schema_version'),
    ({'schema_version': 1, 'budget': 10}, 'expected object'),
    ({'schema_version': 1, 'context_policy': 'erase-authority'}, 'context_policy'),
    ({'schema_version': 1, 'context_policy': []}, 'context_policy'),
    ({'schema_version': 1, 'execution_profile': '../escape'}, 'identifier'),
    ({'schema_version': 1, 'execution_profile': 'missing'}, 'Unknown execution profile'),
    ({'schema_version': 1, 'profiles': {'a': {'extends': 'b'}, 'b': {'extends': 'a'}}}, 'cycle'),
    ({'schema_version': 1, 'profiles': {'a': {'extends': 'missing'}}}, 'Unknown execution profile'),
    ({'schema_version': 1, 'overrides': {'responsibilities': {'author': {'reasoning_effort': 'ultra'}}}}, 'unsupported reasoning_effort'),
    ({'schema_version': 1, 'overrides': {'responsibilities': {'author': {'reasoning_effort': []}}}}, 'unsupported reasoning_effort'),
    ({'schema_version': 1, 'overrides': {'responsibilities': {'author': {'workload_class': None}}}}, 'unknown workload_class'),
    ({'schema_version': 1, 'overrides': {'responsibilities': {'router': {}}}}, 'expected object'),
    ({'schema_version': 1, 'overrides': {'extends': 'standard'}}, 'cannot extend'),
])
def test_invalid_config_is_rejected_before_resolution(tmp_path, registry, value, match):
    _write(tmp_path, 'config.json', value)
    with pytest.raises(ValueError, match=match):
        profiles.resolve(tmp_path, registry, 'codex')


def test_integration_malformed_config_is_not_silently_ignored(tmp_path):
    path = tmp_path / '.jai'
    path.mkdir()
    (path / 'config.json').write_text('{')
    with pytest.raises(ValueError, match='Invalid execution configuration'):
        profiles.available(tmp_path)


def test_integration_project_configuration_rejects_external_symlinks(tmp_path):
    external = tmp_path / 'external'
    external.mkdir()
    project = tmp_path / 'project'
    project.mkdir()
    (project / '.jai').symlink_to(external, target_is_directory=True)
    with pytest.raises(ValueError, match='symlinks'):
        profiles.select(project, 'standard')
    assert not list(external.iterdir())


def test_unknown_selection_and_provider_fail_without_writes(tmp_path, registry):
    with pytest.raises(ValueError, match='Unknown execution profile'):
        profiles.select(tmp_path, 'unknown')
    with pytest.raises(ValueError, match='Unsupported execution provider'):
        profiles.resolve(tmp_path, registry, 'unknown')
    assert not (tmp_path / '.jai').exists()


def test_mapping_returns_copies_and_requires_explicit_fallback_registry(tmp_path, registry):
    snapshot = profiles.resolve(tmp_path, registry, 'codex', profile='stronger-reviewer')
    workload, selected = profiles.mapping(snapshot, 'integration_reviewer', 'heavy', registry)
    assert workload == 'heavy'
    selected['reasoning_effort'] = 'low'
    assert snapshot['responsibilities']['reviewer']['model']['reasoning_effort'] == 'high'
    with pytest.raises(ValueError, match='Captured registry required'):
        profiles.mapping(snapshot, 'unmapped-role', 'light')


def test_cli_lists_shows_selects_and_reports_effective_config(tmp_path, capsys):
    base = ['--project', str(tmp_path)]
    assert profiles.main(base) == 0
    assert json.loads(capsys.readouterr().out)['active'] == 'workload'
    assert profiles.main([*base, 'show', 'research']) == 0
    assert json.loads(capsys.readouterr().out)['execution_profile'] == 'research'
    assert profiles.main([*base, 'use', 'economy', '--session']) == 0
    assert json.loads(capsys.readouterr().out)['scope'] == 'session'
    assert profiles.main([*base, 'effective']) == 0
    assert json.loads(capsys.readouterr().out)['execution_profile'] == 'workload'
    with pytest.raises(SystemExit) as error:
        profiles.main([*base, 'show', 'missing'])
    assert error.value.code == 2
    assert 'Unknown execution profile' in capsys.readouterr().err


def test_invalid_registry_does_not_resolve_preferences(tmp_path, registry):
    broken = copy.deepcopy(registry)
    del broken['providers']['claude']
    with pytest.raises(ValueError, match='required provider claude missing'):
        profiles.resolve(tmp_path, broken, 'codex', profile='standard')


def test_local_alternate_workload_keeps_full_model_selection_autonomy(tmp_path, registry):
    snapshot = profiles.resolve(tmp_path, registry, 'codex', profile='stronger-author')
    workload, selected = profiles.mapping(snapshot, 'author', 'research', registry)
    assert workload == 'research'
    assert selected == registry['providers']['codex']['classes']['research']


def test_snapshot_validation_preserves_isolation_and_uses_no_ambient_files(tmp_path, registry):
    snapshot = profiles.resolve(tmp_path, registry, 'codex', profile='standard')
    assert profiles.validate_snapshot(snapshot, registry) == []
    profiles.select(tmp_path, 'research')
    assert profiles.validate_snapshot(snapshot, registry) == []
    changed = copy.deepcopy(snapshot)
    changed['context']['reviewer'] = 'inherit-author'
    assert 'isolation invariant' in profiles.validate_snapshot(changed, registry)[0]
    assert profiles.validate_snapshot(None, registry)
    changed = copy.deepcopy(snapshot)
    changed['responsibilities']['author']['model']['reasoning_effort'] = 'unsupported'
    assert profiles.validate_snapshot(changed, registry)


def test_explicit_missing_user_config_fails(tmp_path):
    with pytest.raises(FileNotFoundError):
        profiles.available(tmp_path, user_config=tmp_path / 'missing.json')


def test_shared_selection_reports_shadowing_by_local_preference(tmp_path):
    profiles.select(tmp_path, 'economy', local=True)
    receipt = profiles.select(tmp_path, 'research')
    assert receipt['effective_profile'] == 'economy'
    assert receipt['shadowed'] is True


def test_analytics_cohort_is_explicit_and_pinned(tmp_path, registry):
    assert profiles.resolve(tmp_path, registry, 'codex')['analytics'] == {
        'task_class': 'unspecified', 'review_scope': 'unspecified'}
    _write(tmp_path, 'config.json', {'schema_version': 1, 'analytics': {
        'task_class': 'architecture', 'review_scope': 'substantive'}})
    snapshot = profiles.resolve(tmp_path, registry, 'codex')
    assert snapshot['analytics'] == {'task_class': 'architecture', 'review_scope': 'substantive'}
    assert snapshot['configured'] is False
    assert profiles.validate_snapshot(snapshot, registry) == []
    _write(tmp_path, 'config.local.json', {'schema_version': 1, 'analytics': {'task_class': 'documentation'}})
    assert profiles.resolve(tmp_path, registry, 'codex')['analytics']['task_class'] == 'documentation'
    assert snapshot['analytics']['task_class'] == 'architecture'


@pytest.mark.parametrize('analytics', [
    {'task_class': '../private'}, {'review_scope': ''}, {'task_class': 'x' * 65},
    {'task_class': ['architecture']}, {'cost': 12}, None,
])
def test_invalid_analytics_cohort_is_rejected(tmp_path, registry, analytics):
    _write(tmp_path, 'config.json', {'schema_version': 1, 'analytics': analytics})
    with pytest.raises(ValueError):
        profiles.resolve(tmp_path, registry, 'codex')
