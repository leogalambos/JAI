# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Discovery metadata validation and installed-runtime compatibility."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.ai/runtime'


def engine(path=RUNTIME / 'demo/scenario_demo.py'):
    spec = importlib.util.spec_from_file_location('scenario_demo', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_catalog(tmp_path, mutate):
    data = json.loads((RUNTIME / 'demo/scenarios.json').read_text())
    mutate(data)
    path = tmp_path / 'scenarios.json'
    path.write_text(json.dumps(data))
    return path


def test_all_scenarios_have_valid_shared_discovery():
    entries = engine().load_catalog(require_discovery=True)
    assert len(entries) == 29
    assert all(e['discovery']['goals'] and e['discovery']['applicability_limits'] for e in entries)


@pytest.mark.parametrize('mutation', [
    lambda d: d.update(discovery_version=True),
    lambda d: d['entries'][0]['discovery'].update(goals=[]),
    lambda d: d['entries'][0]['discovery'].update(workflow_keys=['invented-workflow']),
    lambda d: d['entries'][0]['discovery'].update(related_scenarios=['unknown']),
    lambda d: d['entries'][0]['discovery'].update(phases=['invented-phase']),
    lambda d: d['entries'][0]['discovery'].update(domains=['security', 'security']),
])
def test_rejects_invalid_discovery_before_use(tmp_path, mutation):
    path = write_catalog(tmp_path, mutation)
    with pytest.raises(ValueError):
        engine().load_catalog(path, require_discovery=True)


def test_legacy_catalog_remains_demo_compatible_but_not_hint_ready(tmp_path):
    def legacy(data):
        data.pop('discovery_version')
        for entry in data['entries']:
            entry.pop('discovery')
    path = write_catalog(tmp_path, legacy)
    assert len(engine().load_catalog(path)) == 29
    with pytest.raises(ValueError, match='discovery'):
        engine().load_catalog(path, require_discovery=True)


def test_discovery_does_not_alter_scenario_content():
    mod = engine()
    entries = mod.load_catalog(require_discovery=True)
    legacy = copy.deepcopy(entries)
    for entry in legacy:
        entry.pop('discovery')
    for entry in entries:
        assert mod.describe_scenario(entries, entry['id']) == mod.describe_scenario(legacy, entry['id'])


def test_installed_metadata_uses_packaged_workflow_registry(tmp_path):
    target = tmp_path / 'house'
    shutil.copytree(RUNTIME / 'demo', target / 'demo')
    shutil.copy2(RUNTIME / 'workflows.json', target / 'workflows.json')
    mod = engine(target / 'demo/scenario_demo.py')
    assert len(mod.load_catalog(require_discovery=True)) == 29
    (target / 'workflows.json').unlink()
    with pytest.raises(ValueError, match='registry'):
        mod.load_catalog(require_discovery=True)
