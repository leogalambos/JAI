# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Explicit workload routing is reversible, scoped and independently captured."""
import copy
import json

import pytest

from governed_fixtures import ROOT
import execution_profiles as profiles
import model_router


@pytest.fixture(autouse=True)
def isolated_user_settings(tmp_path, monkeypatch):
    monkeypatch.setenv('XDG_CONFIG_HOME', str(tmp_path / 'isolated-user'))


def _registry():
    return model_router.load(model_router.BASE)


def _write(root, value, name='config.json'):
    target = root / '.jai' / name
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(value))
    return target


@pytest.mark.parametrize('snapshot,expected', [
    ({'routing_mode': 'workload', 'configured': True}, 'workload'),
    ({'routing_mode': 'profile', 'configured': True}, 'profile'),
    ({'configured': True}, 'profile'),
    ({'configured': False}, 'workload'),
])
def test_routing_mode_preserves_legacy_semantics_and_explicit_selection(snapshot, expected):
    before = copy.deepcopy(snapshot)
    assert profiles.routing_mode(snapshot) == expected
    assert snapshot == before


@pytest.mark.parametrize('mode', [None, False, [], 'automatic', ''])
def test_routing_mode_rejects_invalid_explicit_values(mode):
    with pytest.raises(ValueError, match='routing_mode'):
        profiles.routing_mode({'routing_mode': mode, 'configured': True})


def test_routing_observation_compares_selected_tuple_without_claiming_served_model(tmp_path):
    registry = _registry()
    preference = profiles.resolve(tmp_path, registry, 'codex', 'standard')
    actual = copy.deepcopy(preference['responsibilities']['author']['model'])
    same = profiles.routing_observation(preference, 'author', 'standard', actual)
    assert same['differs'] is False and same['served_model'] is None
    # An alternative class remains a deviation even if an administrator maps
    # both classes to the same model and effort.
    changed = profiles.routing_observation(preference, 'author', 'heavy', actual)
    assert changed['differs'] is True
    assert changed['selected']['model_selector'] == changed['preference']['model_selector']
    workload = profiles.resolve(tmp_path, registry, 'codex', 'workload')
    unconstrained = profiles.routing_observation(workload, 'author', 'heavy', actual)
    assert unconstrained['preference'] is None and unconstrained['differs'] is None
    review = profiles.routing_observation(preference, 'integration_reviewer', 'standard', actual)
    assert review['differs'] is False
    with pytest.raises(ValueError, match='Selected model'):
        profiles.routing_observation(preference, 'author', 'standard', {})
    with pytest.raises(ValueError, match='captured workload'):
        profiles.routing_observation(preference, 'author', None, actual)


@pytest.mark.parametrize('provider', ['codex', 'claude'])
def test_workload_selection_bypasses_fixed_preferences_and_keeps_context_and_cohorts(tmp_path, provider):
    original = {'schema_version': 1, 'execution_profile': 'stronger-author',
        'context_policy': 'manual', 'analytics': {'task_class': 'architecture', 'review_scope': 'substantive'},
        'profiles': {'team': {'extends': 'standard'}},
        'overrides': {'responsibilities': {'author': {'model_selector': 'fixed-author', 'reasoning_effort': 'high'}}}}
    path = _write(tmp_path, original)
    named = profiles.resolve(tmp_path, _registry(), provider)
    assert named['routing_mode'] == 'profile'
    receipt = profiles.select(tmp_path, 'workload')
    assert receipt['effective_routing_mode'] == 'workload'
    assert not receipt['shadowed']
    stored = json.loads(path.read_text())
    assert stored == {**original, 'execution_profile': 'workload'}
    active = profiles.resolve(tmp_path, _registry(), provider)
    assert active['configured'] is True and active['routing_mode'] == 'workload'
    assert active['responsibilities'] == {}
    assert active['context_policy'] == 'manual'
    assert active['analytics'] == named['analytics']
    for workload, mapping in _registry()['providers'][provider]['classes'].items():
        assert profiles.mapping(active, 'author', workload, _registry()) == (workload, mapping)
    profiles.select(tmp_path, 'standard')
    restored = profiles.resolve(tmp_path, _registry(), provider)
    assert restored['routing_mode'] == 'profile'
    assert restored['responsibilities']['author']['model']['model_selector'] == 'fixed-author'
    assert restored['context_policy'] == 'manual'
    assert named['execution_profile'] == 'stronger-author'


@pytest.mark.parametrize('local', [False, True])
def test_persistent_workload_transition_preserves_inherited_profile_context(tmp_path, local):
    _write(tmp_path, {'schema_version': 1, 'execution_profile': 'team',
        'profiles': {'team': {'extends': 'standard', 'context_policy': 'task-isolated'}}})
    receipt = profiles.select(tmp_path, 'workload', local=local)
    active = profiles.resolve(tmp_path, _registry(), 'codex')
    assert active['context_policy'] == 'task-isolated'
    assert receipt['context_policy'] == 'task-isolated'
    path = tmp_path / '.jai' / ('config.local.json' if local else 'config.json')
    assert json.loads(path.read_text())['context_policy'] == 'task-isolated'


def test_session_workload_wins_over_local_named_profile_without_modifying_files(tmp_path):
    _write(tmp_path, {'schema_version': 1, 'execution_profile': 'standard'})
    local = _write(tmp_path, {'schema_version': 1, 'execution_profile': 'team',
        'profiles': {'team': {'extends': 'research', 'context_policy': 'manual'}},
        'overrides': {'responsibilities': {'author': {'model_selector': 'inactive-fixed'}}}}, 'config.local.json')
    before = local.read_bytes()
    receipt = profiles.select(tmp_path, 'workload', session=True)
    snapshot = profiles.resolve(tmp_path, _registry(), 'codex', receipt['execution_profile'])
    assert receipt['routing_mode'] == snapshot['routing_mode'] == 'workload'
    assert receipt['context_policy'] == snapshot['context_policy'] == 'manual'
    assert local.read_bytes() == before
    assert profiles.available(tmp_path)['active'] == 'team'
    assert profiles.mapping(snapshot, 'author', 'research', _registry())[1]['model_selector'] != 'inactive-fixed'


def test_project_workload_reports_shadowing_and_local_selection_can_override_it(tmp_path):
    _write(tmp_path, {'schema_version': 1, 'execution_profile': 'research'}, 'config.local.json')
    receipt = profiles.select(tmp_path, 'workload')
    assert receipt['shadowed'] and receipt['effective_profile'] == 'research'
    assert receipt['effective_routing_mode'] == 'profile'
    assert profiles.select(tmp_path, 'workload', local=True)['effective_routing_mode'] == 'workload'


def test_higher_precedence_role_overrides_do_not_reactivate_workload_preferences(tmp_path):
    _write(tmp_path, {'schema_version': 1, 'execution_profile': 'workload'})
    _write(tmp_path, {'schema_version': 1, 'context_policy': 'manual', 'overrides': {
        'responsibilities': {'author': {'model_selector': 'inactive-fixed'}}}}, 'config.local.json')
    snapshot = profiles.resolve(tmp_path, _registry(), 'claude')
    assert snapshot['configured'] is True and snapshot['routing_mode'] == 'workload'
    assert profiles.mapping(snapshot, 'author', 'standard', _registry())[1]['model_selector'] == 'sonnet'


def test_legacy_snapshots_keep_their_old_routing_and_validate_without_rewriting(tmp_path):
    registry = _registry()
    old = profiles.resolve(tmp_path, registry, 'codex', 'stronger-author')
    del old['routing_mode']
    original = copy.deepcopy(old)
    assert profiles.validate_snapshot(old, registry) == []
    assert profiles.mapping(old, 'author', 'heavy', registry)[1] == old['responsibilities']['author']['model']
    old['configured'] = False
    assert profiles.validate_snapshot(old, registry) == []
    assert profiles.mapping(old, 'author', 'heavy', registry)[1] == registry['providers']['codex']['classes']['heavy']
    assert original['configured'] is True


@pytest.mark.parametrize('bad', [
    {'profiles': {'workload': {'responsibilities': {'author': {'model_selector': 'fixed'}}}}},
    {'profiles': {'custom': {'extends': 'workload'}}},
    {'execution_profile': 'work-load'},
    {'execution_profile': []},
])
def test_invalid_workload_mode_configuration_fails_closed(tmp_path, bad):
    _write(tmp_path, {'schema_version': 1, **bad})
    with pytest.raises(ValueError):
        profiles.resolve(tmp_path, _registry(), 'codex')


def test_workload_mode_is_visible_in_native_list_effective_and_session_receipts(tmp_path, capsys):
    base = ['--project', str(tmp_path)]
    assert profiles.main(base) == 0
    listing = json.loads(capsys.readouterr().out)
    assert listing['active'] == listing['routing_mode'] == 'workload'
    assert listing['configured'] is False
    assert next(row for row in listing['profiles'] if row['name'] == 'workload')['routing_mode'] == 'workload'
    assert profiles.main([*base, 'use', 'standard']) == 0
    assert json.loads(capsys.readouterr().out)['effective_routing_mode'] == 'profile'
    assert profiles.main([*base, 'use', 'workload', '--session']) == 0
    assert json.loads(capsys.readouterr().out)['routing_mode'] == 'workload'
    assert profiles.main([*base, 'effective']) == 0
    assert json.loads(capsys.readouterr().out)['routing_mode'] == 'profile'
