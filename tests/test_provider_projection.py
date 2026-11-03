# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""The installer and installed native bridge share one projection renderer."""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import provider_projection as projection


def test_installer_reexports_same_shared_renderers_and_preserves_role_bodies():
    spec = importlib.util.spec_from_file_location('installer_projection_test', ROOT / '.ai/setup/installer.py')
    installer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(installer)
    assert installer.render_claude_agent is projection.render_claude_agent
    assert installer.render_codex_skill is projection.render_codex_skill
    registry = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_bytes())
    for name in ('role-router', 'role-author', 'role-engineer', 'role-advisor'):
        source = ROOT / '.ai/agents' / (name + '.md')
        fm, body = projection.split_frontmatter(source.read_text())
        claude = projection.render_claude_agent(source, registry).decode()
        codex = projection.render_codex_skill(source, 'agent', name, registry).decode()
        assert body in claude
        assert body in codex
        assert projection.model_selector(registry, 'codex', fm['model_class']) == projection.model_mapping(registry, 'codex', fm['model_class'])['model_selector']
    assert projection.split_frontmatter('plain') == ({}, 'plain')
    assert 'Unchanged body' in projection.skill_doc('example', '', 'Unchanged body', 'skill', 'example').decode()
    with pytest.raises(SystemExit):
        projection.model_mapping(registry, 'unknown', 'standard')


def test_explicit_workload_uses_selected_model_and_installed_layout_has_no_setup_dependency(tmp_path):
    source = tmp_path / 'canonical-agent.md'
    source.write_text('---\nname: example\nmodel_class: standard\ntools: Read\n---\nExact role body\n')
    registry = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_bytes())
    assert 'Workload class: `heavy`' in projection.render_codex_skill(source, 'agent', 'example', registry, workload_class='heavy').decode()
    claude = projection.render_claude_agent(source, registry, workload_class='heavy').decode()
    assert 'model: ' + registry['providers']['claude']['classes']['heavy']['model_selector'] in claude
    installed = tmp_path / 'runtime' / 'tools' / 'provider_projection.py'
    installed.parent.mkdir(parents=True)
    installed.write_bytes(Path(projection.__file__).read_bytes())
    spec = importlib.util.spec_from_file_location('installed_projection_test', installed)
    detached = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(detached)
    assert detached.render_codex_skill(source, 'agent', 'example', registry) == projection.render_codex_skill(source, 'agent', 'example', registry)
