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
    assert catalog['workflow_count'] == 26
    assert catalog['handoff_count'] == 240
    assert len({row['handoff_id'] for row in catalog['bindings']}) == 240


def test_mobile_delivery_inserts_automation_before_independent_verdict():
    catalog = generator.build(ROOT)
    workflow = 'idea-to-production'
    paths = {path['id']: path['steps'] for path in catalog['profiles'][workflow]['paths']}
    assert paths['new-product'] == paths['existing-service-change'] == list(range(1, 14))
    assert paths['mobile-delivery'] == [1, 2, 3, 4, 5, 6, 7, 14, 8, 9, 10, 11, 12, 13]
    rows = {row['step']: row for row in catalog['bindings'] if row['workflow_id'] == workflow}
    build, automation, verdict = (rows[step]['variant_bindings']['mobile-delivery'] for step in (7, 14, 8))
    assert (build['producer_role'], build['receiving_role'], build['contract_ids'], build['next_step']) == (
        'mobile-engineer', 'test-automation-engineer', ['mobile-engineer:1'], 14)
    assert (automation['producer_role'], automation['receiving_role'], automation['contract_ids'],
            automation['next_step']) == ('test-automation-engineer', 'test-analyst', ['test-automation-engineer:1'], 8)
    assert verdict['producer_role'] == 'test-analyst' and verdict['next_step'] == 9
    assert rows[13]['receiving_role'] == 'engagement:named-authority'
    assert set(rows[14]['variant_bindings']) == {'mobile-delivery'}


def test_abap_cloud_evidence_precedes_existing_change_authority():
    catalog = generator.build(ROOT)
    workflow = 'production-change'
    paths = {path['id']: path['steps'] for path in catalog['profiles'][workflow]['paths']}
    assert paths['normal/application'] == list(range(1, 9))
    assert paths['normal/abap-cloud'] == [1, 2, 3, 4, 9, 5, 6, 7, 8]
    rows = {row['step']: row for row in catalog['bindings'] if row['workflow_id'] == workflow}
    release, evidence, approval = (rows[step]['variant_bindings']['normal/abap-cloud'] for step in (4, 9, 5))
    assert release['next_step'] == 9
    assert evidence['contract_ids'] == ['erp-and-crm-consultant-developer:2']
    assert evidence['receiving_role'] == approval['producer_role'] == 'change-manager'
    assert evidence['next_step'] == 5 and approval['next_step'] == 6
    assert approval['contract_ids'] == rows[5]['variant_bindings']['normal/application']['contract_ids']
    assert set(rows[9]['variant_bindings']) == {'normal/abap-cloud'}


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
    assert len(document['workflows']) == 26
    assert sum(len(workflow['steps']) for workflow in document['workflows']) == 240
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


def test_technical_security_assessment_has_exact_consecutive_handoffs():
    catalogue = generator.build(ROOT)
    key = 'technical-security-evidence-assessment'
    rows = [row for row in catalogue['bindings'] if row['workflow_id'] == key]
    assert [row['step'] for row in rows] == [1, 2, 3, 4]
    path = catalogue['profiles'][key]['paths']
    assert [(row['id'], row['steps']) for row in path] == [('supplied-evidence', [1, 2, 3, 4])]
    assert [row['receiving_role'] for row in rows] == [
        'security-architect', 'application-security-engineer', 'control-owner',
        'engagement:named-authority',
    ]
    assert all(row['source_content_contract'] for row in rows)


def test_specialist_discovery_groups_are_disjoint_and_leave_staged_siem_out():
    registered = generator.professional_workflows(ROOT)['workflows']
    groups = generator.workflow_discovery_groups(registered)
    assert {row['key'] for row in groups['Specialist workflows']} == {
        'dast-control-assurance', 'technical-security-evidence-assessment',
    }
    flattened = [row['key'] for members in groups.values() for row in members]
    assert len(flattened) == len(set(flattened)) == len(registered)
    assert 'siem-log-source-integration' not in flattened


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
    workflow_ids = {workflow['key'] for workflow in generator.professional_workflows(ROOT)['workflows']}
    assert set(projections) == {
        f'{folder}/{workflow_id}.md'
        for workflow_id in workflow_ids
        for folder in ('.ai/skills/it-role-workflows/references', 'docs/workflow-library')
    }
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


def test_staged_siem_registration_loads_without_changing_ordinary_bindings(tmp_path, capsys):
    from content_spec import canonical_hash
    from content_workflow import load_bindings, main

    scopes = tmp_path / 'scopes.json'
    fact = {'edition': 'synthetic', 'version': 'fixture', 'deployment': 'offline'}
    scopes.write_text(json.dumps({product: [fact] for product in
        ('splunk-enterprise-security', 'ibm-qradar-siem')}))
    artifact = tmp_path / 'siem-registration.json'
    generator.main(['--stage-siem-pilot', str(artifact), '--product-scopes', str(scopes)])
    baseline = load_bindings(ROOT)
    assert main(['--root', str(ROOT), 'list', '--staged-siem', str(artifact)]) == 0
    candidate = json.loads(capsys.readouterr().out)
    assert candidate['bindings'][:-2] == baseline['bindings']
    assert all(candidate['profiles'][key] == value for key, value in baseline['profiles'].items())
    producer, terminal = candidate['bindings'][-2:]
    assert producer['contract_ids'] == ['security-engineer:4']
    assert terminal['producer_role'] == producer['receiving_role']
    assert terminal['receiving_role'] == 'engagement:named-acceptance-authority'
    assert terminal['variant_bindings']['bounded-validation']['next_step'] is None
    assert load_bindings(ROOT) == baseline
    registration = json.loads(artifact.read_text())
    registration['catalogue']['bindings'][-1]['receiving_role'] = 'security-engineer'
    changed = registration['catalogue']
    changed.pop('catalog_hash')
    changed['catalog_hash'] = canonical_hash(changed)
    artifact.write_text(json.dumps(registration))
    with pytest.raises(ValueError, match='WORKFLOW_PILOT_REGISTRATION'):
        load_bindings(ROOT, pilot=artifact)


def test_stage_siem_workflow_preserves_exact_authority_and_contract():
    import yaml
    from compose_role_library import _ClosedLoader
    from workflow_role_selection import stage_siem_workflow

    source = ROOT / '.ai/role-library/workflows/siem-log-source-integration.yaml'
    draft = yaml.load(source.read_bytes(), Loader=_ClosedLoader)
    rows = json.loads((ROOT / '.ai/runtime/artifacts/contracts/role-deliverables.v3.json').read_bytes())['contracts']
    contracts = {row['id']: row for row in rows}
    deployments = {product: [{'edition': 'synthetic', 'version': '1', 'deployment': 'offline'}]
                   for product in ('splunk-enterprise-security', 'ibm-qradar-siem')}
    baseline = generator.build(ROOT)
    result = stage_siem_workflow(draft, deployments, baseline, contracts)
    assert result['catalogue']['bindings'][:-2] == baseline['bindings']
    assert result['catalogue']['bindings'][-1]['receiving_role'] == 'engagement:named-acceptance-authority'

    wrong_receiver = copy.deepcopy(draft)
    wrong_receiver['steps'][1]['receiving_role'] = 'security-engineer'
    with pytest.raises(ValueError, match='WORKFLOW_PILOT_BOUNDARY'):
        stage_siem_workflow(wrong_receiver, deployments, baseline, contracts)

    wrong_contract = copy.deepcopy(draft)
    wrong_contract['steps'][0]['role_requirement']['contract']['version'] = '0.0.0'
    with pytest.raises(ValueError, match='WORKFLOW_PILOT_CONTRACT'):
        stage_siem_workflow(wrong_contract, deployments, baseline, contracts)


def test_infrastructure_routes_preserve_exact_boundaries():
    from infrastructure_workflow_definitions import DELIVERY, PROVIDERS

    catalogue = generator.build(ROOT)
    readiness, change = 'design-to-operational-readiness', 'production-change'
    paths = {key: {path['id']: path for path in catalogue['profiles'][key]['paths']}
             for key in (readiness, change)}
    rows = {(row['workflow_id'], row['step']): row['variant_bindings'] for row in catalogue['bindings']}
    for provider in PROVIDERS:
        for intent in ('greenfield', 'migration', 'assessment'):
            path = f'{provider}-{intent}'
            assert paths[readiness][path]['steps'][0] == 1
            receiver = rows[readiness, 1][path]['receiving_role']
            assert receiver == ('security-assurance-and-measurement-architect' if intent == 'assessment'
                                else 'cloud-architect')
        assert provider in DELIVERY
        path = f'normal/{provider}'
        assert paths[change][path]['steps'] == list(range(1, 9))
        assert rows[change, 5][path]['producer_role'] == 'change-manager'
        assert rows[change, 5][path]['receiving_role'] == 'gitops-and-continuous-delivery-engineer'
        assert rows[change, 6][path]['receiving_role'] == 'site-reliability-engineer'
        for step in range(1, 8):
            assert rows[change, step][path]['next_step'] == step + 1
            assert rows[change, step][path]['receiving_role'] == rows[change, step + 1][path]['producer_role']
    assert paths[readiness]['zero-trust-migration']['steps'] == list(range(1, 8))
    assert rows[readiness, 3]['zero-trust-migration']['receiving_role'] == (
        'security-assurance-and-measurement-architect')


def test_dast_integration_requires_implemented_workstreams_before_acceptance():
    """Protect implementation dependencies and separate human decisions."""
    catalog = generator.build(ROOT)
    workflow = 'dast-control-assurance'
    rows = {row['step']: row for row in catalog['bindings'] if row['workflow_id'] == workflow}
    paths = {path['id']: path['steps'] for path in catalog['profiles'][workflow]['paths']}
    assert paths['integration'] == [9, 1, 2, 10, 11, 12, 13, 14, 15, 16, 17, 18, 3, 4, 5, 19]
    assert paths['qualification'] == [1, 2, 3, 4, 5, 19]
    assert paths['release-evidence'] == [6, 7]
    assert paths['continuous-assurance'] == [8]
    for step, following in zip(paths['integration'], paths['integration'][1:]):
        binding = rows[step]['variant_bindings']['integration']
        assert binding['next_step'] == following
        assert binding['receiving_role'] == rows[following]['producer_role']
    assert rows[9]['producer_role'] == rows[5]['producer_role'] == rows[19]['producer_role'] == 'engagement:named-authority'
    assert rows[16]['producer_role'] == 'ci-cd-platform-engineer'
    assert rows[17]['producer_role'] == 'release-engineer'
    assert rows[18]['producer_role'] == 'test-manager'
    assert rows[4]['producer_role'] == 'internal-it-auditor'
    assert 'workstream_refs' in rows[18]['handoff_content_contract']['units'][0]['required_fields']
    for row in rows.values():
        for binding in row['variant_bindings'].values():
            criterion = binding['handoff_content_contract']['units'][0]['acceptance_criterion']
            assert 'dast-methodology.md' in criterion


def test_dast_stages_link_to_the_complete_requirement_and_acceptance_catalogues():
    """Keep the technical criteria and stage references available in both views."""
    import re

    relative = '.ai/skills/it-role-workflows/references'
    source = (ROOT / relative / 'dast-methodology.md').read_text()
    assert source == (ROOT / 'docs/reference/dast-methodology.md').read_text()
    for prefix, limit in (('SR', 28), ('AC', 12)):
        expected = [f'{prefix}-{number:02}' for number in range(1, limit + 1)]
        assert re.findall(rf'^\| ({prefix}-\d{{2}}) \|', source, re.MULTILINE) == expected
    anchors = {re.sub(r'[^a-z0-9 -]', '', heading.lower()).replace(' ', '-')
               for heading in re.findall(r'^#{2,3} (.+)$', source, re.MULTILINE)}
    for path in (f'{relative}/dast-control-assurance.md',
                 'docs/workflow-library/dast-control-assurance.md'):
        document = (ROOT / path).read_text()
        assert re.findall(r'^\| (\d+) \|', document, re.MULTILINE) == [
            str(step) for step in range(1, 20)]
        stage_map = document.split('## Read the methodology for the current stage')[1]
        references = re.findall(r'dast-methodology\.md#([a-z0-9-]+)', stage_map)
        assert set(references) <= anchors
        assert {'security-requirements-catalogue', 'qualification-and-coverage',
                'output-security-gate-and-exceptions'} <= set(references)
