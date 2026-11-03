# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Protect exact canonical workflow coverage without pinning a stale step total."""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('workflow_generator_tests', ROOT / 'tools/generate_content_workflows.py')
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


def test_current_complete_catalogue_covers_all_explicit_stages():
    catalog = generator.build(ROOT)
    assert catalog['workflow_count'] == 24
    assert catalog['handoff_count'] == 215
    assert len({row['handoff_id'] for row in catalog['bindings']}) == 215


@pytest.mark.parametrize('mutation', ['missing-selection', 'extra-selection', 'missing-stage'])
def test_editorial_selection_drift_is_rejected(monkeypatch, mutation):
    selections = copy.deepcopy(generator.SELECTIONS)
    key = next(iter(selections))
    if mutation == 'missing-selection':
        selections.pop(key)
    elif mutation == 'extra-selection':
        selections['unregistered-workflow'] = ['1']
    else:
        selections[key] = selections[key][1:]
    monkeypatch.setattr(generator, 'SELECTIONS', selections)
    with pytest.raises(ValueError, match='WORKFLOW_'):
        generator.build(ROOT)


@pytest.mark.parametrize('mutation', ['unknown-key', 'duplicate-key', 'missing-source-stage'])
def test_canonical_workflow_drift_is_rejected(tmp_path, mutation):
    runtime = tmp_path / '.ai/runtime'
    (runtime / 'artifacts/contracts').mkdir(parents=True)
    contracts = ROOT / '.ai/runtime/artifacts/contracts/role-deliverables.v3.json'
    (runtime / 'artifacts/contracts/role-deliverables.v3.json').write_bytes(contracts.read_bytes())
    source = json.loads((ROOT / '.ai/runtime/workflows.json').read_text())
    if mutation == 'unknown-key':
        source['workflows'][0]['key'] = 'unregistered-workflow'
    elif mutation == 'duplicate-key':
        source['workflows'].append(copy.deepcopy(source['workflows'][0]))
    else:
        source['workflows'][0]['steps'].pop()
    (runtime / 'workflows.json').write_text(json.dumps(source))
    with pytest.raises(ValueError, match='WORKFLOW_'):
        generator.build(tmp_path)
