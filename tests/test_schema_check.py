# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Current catalogue validation without retired migration requirements."""
import copy
import json
from pathlib import Path
import sys

import pytest
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import schema_check


def _workflow_schema_and_sample():
    runtime = schema_check.runtime(ROOT)
    registry = schema_check.load(runtime / 'schema/schema-registry.json')
    path = next(row['path'] for row in registry['schemas'] if row['name'] == 'Workflow')
    schema = schema_check.load(runtime / path)
    workflow = next(row for row in schema_check.load(runtime / 'workflows.json')['workflows']
                    if row['key'] == 'new-service-onboarding')
    return jsonschema.Draft202012Validator(schema), workflow


def test_workflow_applicability_is_supported_without_loosening_the_workflow_schema():
    validator, workflow = _workflow_schema_and_sample()
    assert validator.is_valid(workflow)
    without = copy.deepcopy(workflow)
    without.pop('applicability')
    assert validator.is_valid(without)


@pytest.mark.parametrize('mutation', ['extra-field', 'missing-invariants', 'empty-invariants', 'bad-variant', 'extra-variant-field', 'empty-disposition'])
def test_malformed_workflow_applicability_is_rejected(mutation):
    validator, workflow = _workflow_schema_and_sample()
    profile = workflow['applicability']
    if mutation == 'extra-field':
        profile['allow_gate_bypass'] = True
    elif mutation == 'missing-invariants':
        profile.pop('invariant_outcomes')
    elif mutation == 'empty-invariants':
        profile['invariant_outcomes'] = []
    elif mutation == 'bad-variant':
        profile['variants'][0].pop('evidence')
    elif mutation == 'extra-variant-field':
        profile['variants'][0]['automatically_approved'] = True
    else:
        profile['disposition_rule'] = ''
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(workflow)


def test_current_registry_validates_without_retired_migration_contracts(capsys):
    runtime = schema_check.runtime(ROOT)
    registry = schema_check.load(runtime / 'schema/schema-registry.json')
    assert 'migration_rules' not in registry
    assert 'backward_compatibility_policy' not in registry
    assert schema_check.self_test(ROOT) == 0
    assert 'references resolve' in capsys.readouterr().out


@pytest.mark.parametrize('missing', [False, True], ids=['malformed', 'missing'])
def test_registered_schema_fault_is_reported_without_migration_fallback(tmp_path, monkeypatch, missing):
    runtime = schema_check.runtime(ROOT)
    registry_path = runtime / 'schema/schema-registry.json'
    load = schema_check.load
    registry = copy.deepcopy(load(registry_path))
    schema = tmp_path / 'registered-schema.json'
    if not missing:
        schema.write_text(json.dumps({'type': 'not-a-json-schema-type'}))
    registry['schemas'].append({'name': 'FaultProbe', 'path': str(schema)})
    monkeypatch.setattr(schema_check, 'load', lambda path: registry if Path(path) == registry_path else load(path))
    problems, actual_runtime, _ = schema_check.check(ROOT)
    assert actual_runtime == runtime
    expected = 'schema path missing' if missing else 'invalid schema'
    assert any(problem.startswith('FaultProbe: ' + expected) for problem in problems), problems
