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


def test_every_boundary_has_source_specific_content_and_current_route_obligations():
    catalog = generator.build(ROOT)
    source = json.loads((ROOT / '.ai/runtime/workflows.json').read_text())['workflows']
    for workflow in source:
        assert workflow['operating_profile']['entry_inputs'], workflow['key']
        assert {route['id'] for route in workflow['operating_profile']['routes']} >= {'continue', 'rework', 'stop', 'exit'}
    for row in catalog['bindings']:
        contract = row.get('handoff_content_contract')
        assert contract and contract['units'], row['handoff_id']
        assert any(unit['semantic_field'] != 'workflow_context' for unit in contract['units'])
        assert contract['workflow_profile_hash']
        assert all(unit['required_fields'] for unit in contract['units'])
        assert row['handover'] in contract['subject']


def test_professional_workflows_selects_exact_intake_and_handoff_definitions():
    document = generator.professional_workflows(ROOT)
    assert len(document['workflows']) == 24
    assert sum(len(workflow['steps']) for workflow in document['workflows']) == 215
    assert set(generator.professional_projection(ROOT)) == {'.ai/runtime/workflows.json'}
    assert json.loads(generator.professional_projection(ROOT)['.ai/runtime/workflows.json']) == document


def test_all_profiles_have_authored_scope_paths_and_variant_contracts():
    document = generator.professional_workflows(ROOT)
    for workflow in document['workflows']:
        profile = workflow['operating_profile']
        assert profile['scope_assessment'], workflow['key']
        for path in profile['paths']:
            assert path['terminal_step'] == path['steps'][-1]
            for step in workflow['steps']:
                assert (path['id'] in step['variant_bindings']) == (step['step'] in path['steps'])
    onboarding = next(workflow for workflow in document['workflows'] if workflow['key'] == 'new-service-onboarding')
    assert 'pipeline' not in onboarding['outcome']
    assert 'codified infrastructure' not in onboarding['outcome']
    for step in onboarding['steps']:
        selected = step['variant_bindings']['data-ai/saas-cots']
        if step['step'] in (1, 6, 8):
            assert len(selected['handoff_content_contract']['units']) == 3


def test_professional_workflows_refuses_unregistered_source_or_step(tmp_path):
    runtime = tmp_path / '.ai/runtime'
    runtime.mkdir(parents=True)
    source = json.loads((ROOT / '.ai/runtime/workflows.json').read_text())
    source['workflows'].pop()
    (runtime / 'workflows.json').write_text(json.dumps(source))
    with pytest.raises(ValueError, match='PROFILE_COVERAGE'):
        generator.professional_workflows(tmp_path)
    with pytest.raises(ValueError, match='PROFILE_COVERAGE'):
        generator.professional_projection(tmp_path)
    source = json.loads((ROOT / '.ai/runtime/workflows.json').read_text())
    source['workflows'][0]['steps'].pop()
    (runtime / 'workflows.json').write_text(json.dumps(source))
    with pytest.raises(ValueError, match='STEP_COVERAGE'):
        generator.professional_workflows(tmp_path)


def test_workflow_and_domain_summaries_match_canonical_counts():
    workflows = json.loads((ROOT / '.ai/runtime/workflows.json').read_text())['workflows']
    summary = (ROOT / '.ai/skills/it-role-workflows/SKILL.md').read_text()
    for workflow in workflows:
        row = next(line for line in summary.splitlines()
                   if f"references/{workflow['key']}.md)" in line)
        assert int(row.split('|')[2].strip()) == len(workflow['steps']), workflow['key']
    roles = json.loads((ROOT / '.ai/runtime/roles.json').read_text())['roles']
    for skill in {role['skill'] for role in roles}:
        text = (ROOT / '.ai/skills' / skill / 'SKILL.md').read_text()
        selected = [role for role in roles if role['skill'] == skill]
        assert f'role skills: {len(selected)} defined roles' in text, skill
        assert f'`roles: {len(selected)}`' in text, skill
        advises = sum(role['tool_tier'] == 'advise' for role in selected)
        if advises:
            assert f'{advises} of the {len(selected)} roles here' in text, skill


def test_summary_generation_preserves_manual_text_and_is_idempotent():
    projections = generator.summary_projections(ROOT)
    assert len(projections) == 18
    for path, text in projections.items():
        original = (ROOT / path).read_text()
        assert text.split('## Response contract')[-1].split('## Tool restriction')[0] == original.split('## Response contract')[-1].split('## Tool restriction')[0]
        assert all(role['slug'] in text for role in
                   json.loads((ROOT / '.ai/runtime/roles.json').read_text())['roles']
                   if path == f".ai/skills/{role['skill']}/SKILL.md")


def test_summary_generation_rejects_a_missing_domain_projection(tmp_path):
    runtime = tmp_path / '.ai/runtime'
    runtime.mkdir(parents=True)
    for name in ('roles.json', 'workflows.json'):
        (runtime / name).write_bytes((ROOT / '.ai/runtime' / name).read_bytes())
    with pytest.raises(ValueError, match='SUMMARY_PROJECTION_MISSING'):
        generator.summary_projections(tmp_path)


def test_applicability_projections_preserve_invariants_for_each_service_context():
    projections = generator.applicability_projections(ROOT)
    assert len(projections) == 48
    for path, text in projections.items():
        assert '**Entry information (selected once per actual context version):**' in text
        assert '**Continuation, rework, stop and exit:**' in text
    for path, text in projections.items():
        if 'new-service-onboarding' not in path:
            continue
        for context in ('SaaS/COTS', 'cloud-native', 'on-premises/existing-platform', 'data/AI overlay', 'critical/regulated overlay'):
            assert context in text
        assert 'not a waiver of security, legal or acceptance obligations' in text
        assert 'Unknown applicability remains pending' in text
        assert (ROOT / path).read_text() == text
    public = projections['docs/workflow-library/new-service-onboarding.md']
    assert public.index('## Context and mechanism applicability') < public.index('## Workflow steps and gates')


def test_applicability_projection_detects_bad_markers_and_retains_manual_prose(tmp_path):
    runtime = tmp_path / '.ai/runtime'
    runtime.mkdir(parents=True)
    source = {'workflows': [{'key': 'sample', 'applicability': {
        'selection_rule': 'Use observed context.', 'invariant_outcomes': ['Retain owner.'],
        'variants': [], 'disposition_rule': 'Return changed work to its owner.'}}]}
    (runtime / 'workflows.json').write_text(json.dumps(source))
    reference = tmp_path / '.ai/skills/it-role-workflows/references/sample.md'
    reference.parent.mkdir(parents=True)
    reference.write_text('Manual task guidance.\n')
    public = tmp_path / 'docs/workflow-library/sample.md'
    public.parent.mkdir(parents=True)
    public.write_text('Public guidance.\n\n## Workflow steps and gates\n\nManual step table.\n')
    generated = next(iter(generator.applicability_projections(tmp_path).values()))
    assert generated.startswith('Manual task guidance.\n')
    reference.write_text(generated)
    assert next(iter(generator.applicability_projections(tmp_path).values())) == generated
    reference.write_text('<!-- BEGIN workflow-applicability -->\nIncomplete block.')
    with pytest.raises(ValueError, match='WORKFLOW_APPLICABILITY_MARKERS'):
        generator.applicability_projections(tmp_path)
    (runtime / 'workflows.json').write_text(json.dumps({'workflows': [{'key': 'sample'}]}))
    assert generator.applicability_projections(tmp_path) == {}


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
