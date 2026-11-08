# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Policy-validator text parsing must preserve safely quoted role metadata."""
import importlib.util
import json
from pathlib import Path

import pytest

_PATH = Path(__file__).resolve().parents[1] / '.ai/runtime/scripts/check_agent_policy.py'
_SPEC = importlib.util.spec_from_file_location('tested_agent_policy', _PATH)
policy = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(policy)


@pytest.mark.parametrize('text,needs_quotes', [('plain text', False), ('', True),
                                              ('yes', True), ('5', True),
                                              ('risk: boundary', True)])
def test_yaml_needs_quotes_preserves_plain_text_and_yaml_boundaries(text, needs_quotes):
    assert policy.yaml_needs_quotes(text) is needs_quotes


def test_yaml_value_distinguishes_quoted_text_and_malformed_metadata():
    assert policy.yaml_value('plain') == ('plain', None)
    assert policy.yaml_value('"risk: boundary"') == ('risk: boundary', None)
    assert policy.yaml_value("'owner''s role'") == ("owner's role", None)
    assert policy.yaml_value('') == ('', None)
    assert policy.yaml_value('"unterminated')[1]
    assert policy.yaml_value("'unterminated")[1]
    assert policy.yaml_value('risk: boundary')[1]


def test_frontmatter_retains_body_and_reports_invalid_description(tmp_path):
    path = tmp_path / 'agent.md'
    path.write_text('body without metadata')
    assert policy.frontmatter(path) == (None, 'body without metadata')
    path.write_text('---\nname: role\ndescription: "Bounded: role"\n---\nbody')
    assert policy.frontmatter(path) == ({'name': 'role', 'description': 'Bounded: role'}, '\nbody')
    before = len(policy.FRONTMATTER_PROBLEMS)
    path.write_text('---\ndescription: bad: value\n---\nbody')
    assert policy.frontmatter(path)[0]['description'] == 'bad: value'
    assert len(policy.FRONTMATTER_PROBLEMS) == before + 1


def test_toolset_ignores_empty_items_without_inventing_a_tool():
    assert policy.toolset('Read, Bash, Read') == {'Read', 'Bash'}
    assert policy.toolset(' , ') == set()
    assert policy.toolset(None) == set()


@pytest.mark.parametrize('step,agents,valid', [
    ({'skill': 'external', 'operator_agent': 'human'}, {}, True),
    ({'skill': 'external', 'operator_agent': 'role-advisor'}, {'role-advisor': {}}, False),
    ({'skill': 'agent', 'operator_agent': 'human'}, {}, False),
    ({'skill': 'agent', 'operator_agent': 'human'}, {'human': {}}, False),
    ({'skill': 'agent', 'operator_agent': 'missing'}, {}, False),
    ({'skill': 'agent', 'operator_agent': 'role-author'}, {'role-author': {}}, True),
])
def test_workflow_operator_problem_preserves_external_human_authority(step, agents, valid):
    assert (policy.workflow_operator_problem(step, agents) is None) is valid


def test_current_resource_policy_preserves_read_only_audit_and_human_publication():
    root = _PATH.parents[3]
    runtime = root / '.ai/runtime'
    policy_data = json.loads((runtime / 'policy.json').read_text())
    audit, _ = policy.frontmatter(root / '.ai/agents/fabric-auditor.md')
    tier = policy_data['agent_tier']['fabric-auditor']
    assert policy.toolset(audit['tools']) == policy.toolset(policy_data['tiers'][tier])
    assert not policy.toolset(audit['tools']) & {'Write', 'Edit', 'Bash'}
    assert policy_data['write_scope']['fabric-auditor'] == {'allow': [], 'deny': ['**']}
    skill, body = policy.frontmatter(root / '.ai/skills/layered-justifiable-delivery/SKILL.md')
    assert 'tool-tier: orchestrate' in body
    assert policy.toolset(skill['allowed-tools']) == policy.toolset(policy_data['tiers']['orchestrate'])
    command, _ = policy.frontmatter(root / '.ai/commands/fabric-report.md')
    assert command['argument-hint'] == '[engagement] [output or requested audit scope]'
    workflows = json.loads((runtime / 'workflows.json').read_text())['workflows']
    publication = next(item for item in workflows if item['key'] == 'semantic-to-enterprise-publication')
    approval = publication['steps'][-1]
    assert approval['skill'] == 'external' and approval['operator_agent'] == 'human'
    assert approval['role'] == 'Named authority'
    assert 'human release decision' in approval['does']
    assert 'completed semantic, publication and actual visual evidence' in approval['does']
    assert 'Explicit exact human approval precedes release' in approval['gate']
    assert 'required independence is preserved' in approval['gate']
    assert 'agents cannot approve or issue waivers' in approval['gate']
    assert {'tools/lifecycle.py', 'tools/governed_delivery.py'} <= set(policy.ENFORCEMENT_ASSETS)
    assert not any(name.startswith('jai/migrations/') for name in policy.ENFORCEMENT_ASSETS)
    assert len(workflows) == 24



def test_source_validator_resolves_provider_command_aliases_in_maintained_guide():
    import subprocess
    import sys

    root = _PATH.parents[3]
    result = subprocess.run([sys.executable, str(_PATH), '--fast', str(root)],
                            capture_output=True, text=True, check=False, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "no section '### /profile'" not in result.stdout
    assert "no section '### /stats'" not in result.stdout
