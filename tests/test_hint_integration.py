# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Verify experimental hint provider projection and real installed tool boundaries."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _installer():
    spec = importlib.util.spec_from_file_location('hint_installer', ROOT / '.ai/setup/installer.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_hint_projects_identical_advisory_body_to_both_providers(tmp_path):
    installer = _installer()
    source = ROOT / '.ai/commands/hint.md'
    text = source.read_text()
    _, body = installer.split_frontmatter(text)
    package = tmp_path / 'package'
    for section in ('runtime', 'skills', 'agents', 'commands'):
        (package / '.ai' / section).mkdir(parents=True)
    # Scope validation needs both canonical resources, without checkout fallback.
    for relative in ('RELEASE-SCOPE.json', '.ai/runtime/schema/release-scope.schema.json'):
        destination = package / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)
    shutil.copy2(source, package / '.ai/commands/hint.md')
    registry = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_text())
    house, claude, codex = (tmp_path / name for name in ('house', 'claude', 'codex'))
    outputs, _ = installer.desired_outputs(package, {'claude', 'codex'}, house, claude, codex, registry)
    assert outputs[str(house / 'RELEASE-SCOPE.json')] == (ROOT / 'RELEASE-SCOPE.json').read_bytes()
    assert outputs[str(house / 'schema/release-scope.schema.json')] == (
        ROOT / '.ai/runtime/schema/release-scope.schema.json').read_bytes()
    assert outputs[str(claude / 'commands/hint.md')].decode() == text
    projected = outputs[str(codex / 'skills/workflow-hint/SKILL.md')].decode()
    assert body in projected
    assert 'name: workflow-hint' in projected
    assert not house.exists() and not claude.exists() and not codex.exists()
    assert '$ARGUMENTS' not in text
    for required in ('Experimental hint — AI-generated advisory guidance. Requires project-specific verification.',
                     'Working interpretation', 'Source selection', 'Preparation', 'Ordered procedure',
                     'Adaptation', 'Boundaries', 'NO_MATCH', 'PARTIAL_MATCH', 'ERROR',
                     'argument array', 'independent review', 'No nested', 'selected', 'read', 'delivered'):
        assert required in body

    schema = package / '.ai/runtime/schema/release-scope.schema.json'
    schema.unlink()
    with pytest.raises(FileNotFoundError):
        installer.desired_outputs(package, {'claude', 'codex'}, house, claude, codex, registry)
    shutil.copy2(ROOT / '.ai/runtime/schema/release-scope.schema.json', schema)
    (package / 'RELEASE-SCOPE.json').write_text('{}')
    # The maintained resolver's standard-library validator rejects this exact
    # missing-properties case without depending on a third-party exception type.
    with pytest.raises(ValueError, match='missing or unexpected release scope properties'):
        installer.desired_outputs(package, {'claude', 'codex'}, house, claude, codex, registry)
    assert not house.exists() and not claude.exists() and not codex.exists()


def test_installed_hint_then_selected_description_works_without_docs_or_project_reads(tmp_path):
    runtime = tmp_path / 'house'
    shutil.copytree(ROOT / '.ai/runtime/demo', runtime / 'demo', ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copy2(ROOT / '.ai/runtime/workflows.json', runtime / 'workflows.json')
    working = tmp_path / 'unrelated'
    working.mkdir()
    marker = working / 'preserve.txt'
    marker.write_text('untouched')
    result = subprocess.run([sys.executable, str(runtime / 'demo/hint.py'), '--goal',
                             'assess architecture security'], cwd=working, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    selected = json.loads(result.stdout)['candidates']
    assert selected
    description = subprocess.run([sys.executable, str(runtime / 'demo/demo.py'), 'describe', selected[0]['id']],
                                 cwd=working, capture_output=True, text=True)
    assert description.returncode == 0, description.stderr
    assert '/analyse' in description.stdout and '$workflow-analyse' in description.stdout
    assert not (runtime / 'docs').exists()
    assert marker.read_text() == 'untouched'
    assert list(working.iterdir()) == [marker]


def test_literal_hostile_goal_is_data_and_no_match_does_not_create_workspace(tmp_path):
    marker = tmp_path / 'must-not-exist'
    # Relative targets preserve shell-injection sensitivity without coupling the
    # bounded goal to pytest's temporary-directory path length.
    query = 'unrelated $(touch ' + marker.name + ') `touch ' + marker.name + '`'
    assert len(query) <= 300
    result = subprocess.run([sys.executable, str(ROOT / '.ai/runtime/demo/hint.py'), '--goal', query],
                            cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0
    assert json.loads(result.stdout)['status'] == 'NO_MATCH'
    assert not marker.exists()
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize('installed', [False, True])
def test_hint_guide_and_demo_explicit_handoff_preserves_prior_work(tmp_path, installed):
    guide = (ROOT / '.ai/commands/guide.md').read_text()
    demo = (ROOT / '.ai/commands/demo.md').read_text()
    assert '/hint' in guide and '$workflow-hint' in guide
    assert '/hint' in demo and '$workflow-hint' in demo
    assert 'Do not execute' in guide and 'Do not execute' in demo
    runtime = ROOT / '.ai/runtime'
    if installed:
        runtime = tmp_path / 'house'
        shutil.copytree(ROOT / '.ai/runtime/demo', runtime / 'demo', ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copy2(ROOT / '.ai/runtime/workflows.json', runtime / 'workflows.json')
    selected = subprocess.run([sys.executable, str(runtime / 'demo/hint.py'),
                               '--goal', 'assess architecture security'], capture_output=True, text=True)
    assert selected.returncode == 0
    scenario_id = json.loads(selected.stdout)['candidates'][0]['id']
    script = runtime / 'demo/demo.py'
    destination = tmp_path / 'explicit-practice'
    described = subprocess.run([sys.executable, str(script), 'describe', scenario_id, '--step', '1'],
                                capture_output=True, text=True)
    assert described.returncode == 0
    assert not destination.exists()
    created = subprocess.run([sys.executable, str(script), 'scenario', scenario_id, '--to', str(destination)],
                              capture_output=True, text=True)
    assert created.returncode == 0, created.stderr
    assert (destination / 'START.md').is_file()
    work = destination / 'operator-notes.md'
    work.write_text('Preserve the operator work')
    repeated = subprocess.run([sys.executable, str(script), 'scenario', scenario_id, '--to', str(destination)],
                               capture_output=True, text=True)
    assert repeated.returncode != 0 and work.read_text() == 'Preserve the operator work'
    reset = subprocess.run([sys.executable, str(script), 'reset-scenario', scenario_id, '--to', str(destination)],
                            capture_output=True, text=True)
    assert reset.returncode == 0, reset.stderr
    copies = list(tmp_path.glob('explicit-practice.backup-*/operator-notes.md'))
    assert len(copies) == 1 and copies[0].read_text() == 'Preserve the operator work'
    legacy = subprocess.run([sys.executable, str(script), 'list'], capture_output=True, text=True)
    assert legacy.returncode == 0
    assert all(name in legacy.stdout for name in ('invoice-service', 'policy-docs', 'acme-pay'))
