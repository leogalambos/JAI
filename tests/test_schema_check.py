# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Current catalogue validation without retired migration requirements."""
import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import schema_check


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
