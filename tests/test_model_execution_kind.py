# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Captured process capability declarations do not relabel native AI execution."""
import copy

import pytest

from governed_fixtures import ROOT
import execution_profiles
import model_router


def _registry(kind='deterministic'):
    registry = model_router.load(model_router.BASE)
    process = {'display_name': 'Explicit process capability', 'adapter': 'json-process/1',
        'selection_strategy': 'explicit', 'strategy_scope': 'project-internal', 'classes': {}}
    for workload in registry['workload_classes']:
        process['classes'][workload] = {'model_selector': 'process-resource-' + workload,
            'model_kind': kind, 'execution': {'provider': 'json-process/1',
                'argv': ['/usr/bin/python3', '/worker/main.py'], 'files': []}}
    registry['providers']['json-process/1'] = process
    return registry


def test_explicit_deterministic_process_declaration_is_valid_without_artificial_ai_identity():
    registry = _registry()
    assert model_router.validate_registry(registry) == []


def test_wrapped_ai_requires_backend_identity_separate_from_process_resource_label():
    registry = _registry('ai')
    assert any('wrapped AI requires' in problem for problem in model_router.validate_registry(registry))
    for mapping in registry['providers']['json-process/1']['classes'].values():
        mapping.update(model_provider='codex', model_identity='gpt-6.1-sol')
    assert model_router.validate_registry(registry) == []
    assert registry['providers']['json-process/1']['classes']['standard']['model_selector'] != 'gpt-6.1-sol'


@pytest.mark.parametrize('bad', [None, False, [], 'automatic'])
def test_invalid_process_kind_is_rejected_without_guessing(bad):
    registry = _registry()
    registry['providers']['json-process/1']['classes']['standard']['model_kind'] = bad
    assert any('model_kind' in problem for problem in model_router.validate_registry(registry))


@pytest.mark.parametrize('provider', ['codex', 'claude'])
def test_native_ai_cannot_be_relabelled_as_deterministic(provider):
    registry = model_router.load(model_router.BASE)
    registry['providers'][provider]['classes']['standard']['model_kind'] = 'deterministic'
    assert any('cannot be relabeled' in problem for problem in model_router.validate_registry(registry))


def test_native_profile_model_override_updates_requested_identity_consistently(tmp_path):
    registry = model_router.load(model_router.BASE)
    mapping = registry['providers']['codex']['classes']['standard']
    mapping.update(model_kind='ai', model_provider='codex', model_identity=mapping['model_selector'])
    (tmp_path / '.jai').mkdir()
    (tmp_path / '.jai/config.json').write_text('{"schema_version":1,"execution_profile":"standard",'
        '"overrides":{"providers":{"codex":{"author":{"model_selector":"explicit-new-model"}}}}}')
    snapshot = execution_profiles.resolve(tmp_path, registry, 'codex')
    assert execution_profiles.validate_snapshot(snapshot, registry) == []
    assert snapshot['responsibilities']['author']['model']['model_identity'] == 'explicit-new-model'
    wrong = copy.deepcopy(snapshot)
    wrong['responsibilities']['author']['model']['model_identity'] = 'other-backend'
    assert execution_profiles.validate_snapshot(wrong, registry)


def test_published_schema_accepts_real_process_execution_and_rejects_malformed_assets():
    import json
    import jsonschema

    schema = json.loads((ROOT / '.ai/runtime/schema/26.10.4/model-registry.schema.json').read_text())
    registry = _registry('ai')
    for mapping in registry['providers']['json-process/1']['classes'].values():
        mapping.update(model_provider='codex', model_identity='gpt-6.1-sol')
        mapping['execution']['files'] = [{'name': 'main.py', 'sha256': 'a' * 64}]
    jsonschema.validate(registry, schema)
    assert model_router.validate_registry(registry) == []
    registry['providers']['json-process/1']['classes']['standard']['execution']['files'][0]['name'] = '../main.py'
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(registry, schema)
