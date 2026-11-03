# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Explicit captured model resolution remains separate from ambient preparation."""
import copy
import json

import pytest

from governed_fixtures import ROOT
import model_router


def test_explicit_snapshot_does_not_follow_later_ambient_override(tmp_path, monkeypatch):
    original = model_router.load(ROOT / '.ai/runtime/models/model-registry.json')
    override = {'providers': {'codex': {'classes': {'standard': {'model_selector': 'explicit-local-override'}}}}}
    path = tmp_path / 'models.json'
    path.write_text(json.dumps(override))
    monkeypatch.setenv('AI_HOUSE_MODEL_CONFIG', str(path))
    assert model_router.default_override_path(original) == path
    effective, selected_path = model_router.effective_registry()
    assert selected_path == path
    assert effective == model_router.merge(original, override)
    assert model_router.validate_registry(effective) == []
    assert model_router.candidates('codex', 'standard')[0]['model_selector'] == 'explicit-local-override'
    selector, mapping = model_router.resolve_snapshot(original, 'codex', 'standard')
    assert selector == original['providers']['codex']['classes']['standard']['model_selector']
    mapping['model_selector'] = 'mutated-return'
    assert original['providers']['codex']['classes']['standard']['model_selector'] == selector
    with pytest.raises(ValueError, match='unsupported provider'):
        model_router.resolve_snapshot(original, 'missing-provider', 'standard')
    invalid = copy.deepcopy(original)
    invalid['workload_classes'] = {}
    with pytest.raises(ValueError):
        model_router.resolve_snapshot(invalid, 'codex', 'standard')


def test_canonical_agent_metadata_and_existing_public_self_test_remain_consistent(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('AI_HOUSE_MODEL_CONFIG', str(tmp_path / 'no-ambient-override.json'))
    assert model_router.agent_root().is_dir()
    agents, problems = model_router.agent_classes()
    assert agents and problems == []
    assert model_router.self_test() == 0
    assert 'FAIL' not in capsys.readouterr().out
