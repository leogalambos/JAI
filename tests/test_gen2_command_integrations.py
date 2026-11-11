# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Native command contracts and the unexecuted Gen2 practice fixture remain usable."""
from argparse import Namespace
import importlib.util
import json
from pathlib import Path
import shlex
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import provider_projection as projection


COMMANDS = {
    'layered', 'fabric-report', 'analyse', 'commercial', 'criteria', 'demo',
    'develop', 'diagnose', 'govern', 'guide', 'hint', 'publish', 'repository',
    'research', 'review', 'rework', 'sabsa', 'profile', 'stats',
}
HANDOFF = ROOT / '.ai/skills/layered-justifiable-delivery/references/domain-handoff.md'


def test_all_commands_preserve_provider_bodies_and_complete_role_resources():
    registry = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_bytes())
    sources = {path.stem: path for path in (ROOT / '.ai/commands').glob('*.md')}
    assert set(sources) == COMMANDS
    for name, path in sources.items():
        _, body = projection.split_frontmatter(path.read_text())
        projected = projection.render_codex_skill(path, 'command', name, registry).decode()
        assert f'name: workflow-{name}' in projected
        assert body.replace('$ARGUMENTS', 'the user-provided workflow arguments') in projected
        # Claude's canonical command body is copied directly by the shared installer.
        assert body.strip() and 'description:' in path.read_text().split('---')[1]
    roles = json.loads((ROOT / '.ai/runtime/roles.json').read_bytes())
    assert roles['count'] == len(roles['roles']) == 286
    assert len({role['slug'] for role in roles['roles']}) == 286
    for role in roles['roles']:
        assert (ROOT / '.ai/skills' / role['skill'] / 'SKILL.md').is_file()
        assert (ROOT / '.ai' / role['path']).is_file()
    workflow = yaml.safe_load((ROOT / '.github/workflows/validate-library.yml').read_text())
    runtime_steps = [step for step in workflow['jobs']['policy']['steps']
                     if step.get('name') == 'P0 runtime security application regression (host coverage reported separately)']
    assert len(runtime_steps) == 1, 'The named runtime security group must exist exactly once'
    runtime_step = runtime_steps[0]['run']
    assert isinstance(runtime_step, str)
    test_paths = {token for token in shlex.split(runtime_step)
                  if token.startswith('tests/') and token.endswith('.py')}
    assert test_paths == {
        'tests/test_agent_runtime.py', 'tests/test_integration_adapters.py',
        'tests/test_guard_library_write.py', 'tests/test_fabric_authority_boundary.py',
        'tests/test_governed_domain.py', 'tests/test_gen2_command_integrations.py',
    }
    assert all((ROOT / path).is_file() for path in test_paths)


def test_consequential_branches_reach_one_native_handoff_and_preserve_ordinary_scope():
    handoff = HANDOFF.read_text()
    assert 'Ordinary bounded' in handoff
    assert 'exact selected criteria' in handoff
    assert 'A neighbour does not hire its author' in handoff
    assert 'Only L0 signs reserved decisions' in handoff
    for name in ('library-lifecycle', 'research-and-development', 'sabsa-library', 'it-role-workflows'):
        body = (ROOT / '.ai/skills' / name / 'SKILL.md').read_text()
        assert 'references/domain-handoff.md' in body
        assert 'governed_workflow.py' not in body
        assert 'remains unavailable until' not in body
    workflow = (ROOT / '.ai/skills/it-role-workflows/SKILL.md').read_text()
    assert '`receiving_assignments` host map' in workflow
    assert 'never derived from selected professional specialties' in workflow
    for name in ('analyse', 'develop', 'diagnose', 'govern', 'review', 'rework', 'criteria', 'repository'):
        body = (ROOT / '.ai/commands' / (name + '.md')).read_text()
        assert 'domain-handoff.md' in body
        assert 'Ordinary' in body or 'lookup' in body
    for provider, filename, entry in (
        ('claude', 'CLAUDE.snippet.md', '/layered'),
        ('codex', 'AGENTS.snippet.md', '$workflow-layered'),
    ):
        body = (ROOT / '.ai/adapters' / provider / filename).read_text()
        assert entry in body and 'references/domain-handoff.md' in body
        assert 'Ordinary bounded' in body and 'runtime transport' in body


def test_commercial_and_publication_contracts_preserve_specialisms_and_current_basis():
    commercial = (ROOT / '.ai/skills/commercial-delivery/SKILL.md').read_text()
    coordinator = (ROOT / '.ai/agents/commercial-coordinator.md').read_text()
    for slug in ('bid-proposal-manager', 'commercial-pricing-deal-finance-specialist',
                 'estimation-cost-engineering-specialist',
                 'independent-commercial-assurance-reviewer', 'supplier-commercial-deal-manager'):
        assert slug in commercial and slug in coordinator
    assert 'reserve_consultation' in coordinator and 'expected episode revision' in coordinator
    for body in (commercial, coordinator, (ROOT / '.ai/commands/commercial.md').read_text()):
        assert 'governed_domain.GovernedDomain' in body
        assert 'not_run' not in body
        assert 'unverified' in body
        assert 'policy' in body
    publish = (ROOT / '.ai/commands/publish.md').read_text()
    assert 'governed_domain.GovernedDomain' in publish
    assert 'exact product UsePoint' in publish
    assert 'existing current audience/permission' in publish
    assert 'actual DCS unit reviews' in publish
    assert 'successful render is not a content pass' in publish


def test_existing_demo_setup_list_and_reset_keep_gen2_inputs_unexecuted(tmp_path, capsys):
    path = ROOT / '.ai/runtime/demo/demo.py'
    spec = importlib.util.spec_from_file_location('g06_demo', path)
    demo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(demo)
    target = tmp_path / 'practice'
    demo.cmd_setup(Namespace(to=str(target), force=False))
    project = target / 'policy-docs'
    exercise = (project / 'GEN2-EXERCISE.md').read_text()
    brief = project / 'gen2-inputs/brief.md'
    criteria = project / 'gen2-inputs/criteria.md'
    assert 'NOT_EXECUTED' in exercise and 'fictional' in exercise
    assert '/layered ' in exercise and '$workflow-layered ' in exercise
    assert '/fabric-report ' in exercise and '$workflow-fabric-report ' in exercise
    assert 'Fictional' in brief.read_text() and 'Fictional' in criteria.read_text()
    assert not (project / '.fabric').exists() and not (project / '.findings').exists()
    expected = (brief.read_bytes(), criteria.read_bytes())
    brief.write_text('Changed practice input, not historical evidence.')
    demo.cmd_reset(Namespace(name='policy-docs', to=str(target)))
    assert (brief.read_bytes(), criteria.read_bytes()) == expected
    assert not (project / '.fabric').exists()
    demo.cmd_list(Namespace())
    assert 'GEN2-EXERCISE.md' in capsys.readouterr().out
    assert {child.name for child in target.iterdir()} == {'invoice-service', 'policy-docs', 'acme-pay'}
