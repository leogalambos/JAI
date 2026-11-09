# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Regression checks for professional meaning in canonical role deliverables."""
from pathlib import Path
import importlib.util
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def content_engine():
    sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
    from content_spec import ContentSpec
    return ContentSpec(ROOT)


def deliverable(role, number):
    """Return the exact canonical deliverable row for a role and ordinal."""
    matches = list((ROOT / '.ai/skills').glob(f'it-roles-*/references/{role}.md'))
    assert len(matches) == 1
    section = matches[0].read_text().split('## 6. Deliverables', 1)[1].split('## 7.', 1)[0]
    return next(line for line in section.splitlines() if line.startswith(f'| {number} |'))


@pytest.mark.parametrize('role,number,forbidden', [
    ('integration-developer', 3, 'liability'),
    ('frontend-engineer', 4, 'Financial model'),
    ('game-developer', 2, 'Financial model'),
    ('technical-recruiter', 2, 'Declarative pipeline'),
    ('business-relationship-manager', 2, 'Declarative pipeline'),
    ('grc-analyst', 1, 'Executable suite'),
    ('cloud-architect', 1, 'Loading, empty'),
    ('research-scientist', 1, 'Loading, empty'),
    ('test-analyst', 1, 'Executable suite'),
    ('application-security-engineer', 2, 'Executable suite'),
    ('third-party-risk-manager', 3, 'Executed document'),
])
def test_deliverable_uses_its_professional_meaning(role, number, forbidden):
    assert forbidden not in deliverable(role, number)


def test_software_tests_remain_executable_and_ux_design_retains_states():
    assert 'Executable tests in version control' in deliverable('software-engineer', 2)
    assert 'loading, empty, error' in deliverable('ux-designer', 1)


@pytest.mark.parametrize('contract_id,family', [
    ('accessibility-specialist:1', 'document'),
    ('security-domain-authority:1', 'document'),
    ('project-manager:1', 'roadmap'),
    ('network-engineer:2', 'configuration-baseline'),
    ('finops-engineer:1', 'software-change'),
    ('business-relationship-manager:2', 'register'),
    ('binary-reverse-engineer:4', 'software-change'),
    ('ai-governance-officer:3', 'register'),
    ('request-fulfilment-manager:4', 'register'),
    ('technical-design-authority-member:1', 'assurance-report'),
    ('policy-author:1', 'document'),
    ('policy-author:2', 'document'),
    ('policy-author:4', 'roadmap'),
    ('it-governance-manager:3', 'document'),
    ('pmo-lead:1', 'document'),
    ('knowledge-manager:1', 'document'),
])
def test_exact_sidecar_family_supports_the_actual_output(contract_id, family):
    spec = importlib.util.spec_from_file_location('fitness_definitions', ROOT / 'tools/content_catalog_definitions.py')
    definitions = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(definitions)
    assert definitions.SEMANTIC_REFINEMENTS.get(contract_id) == family


@pytest.mark.parametrize('contract_id,unrelated_prefix', [
    ('accessibility-specialist:1', 'type/implementation-specification.'),
    ('policy-author:1', 'type/implementation-specification.'),
    ('policy-author:2', 'type/implementation-specification.'),
    ('policy-author:4', 'type/implementation-specification.'),
    ('it-governance-manager:3', 'type/implementation-specification.'),
    ('pmo-lead:1', 'type/implementation-specification.'),
    ('knowledge-manager:1', 'type/implementation-specification.'),
    ('project-manager:1', 'type/implementation-specification.'),
    ('security-domain-authority:1', 'type/implementation-specification.'),
    ('request-fulfilment-manager:4', 'type/prototype.'),
    ('network-engineer:2', 'type/prototype.'),
    ('finops-engineer:1', 'type/prototype.'),
    ('technical-design-authority-member:1', 'type/solution-design.'),
])
def test_effective_contract_excludes_unrelated_mandatory_content(contract_id, unrelated_prefix, content_engine):
    result = content_engine.resolve(contract_id)
    units = result['blueprint']['semantic_units']
    assert not any(unit['id'].startswith(unrelated_prefix) for unit in units)
    assert any(unit['id'].startswith('global.') for unit in units)
    assert any('role_gate_observations' in unit['id'] for unit in units)
    assert not result['production_ready']


@pytest.mark.parametrize('contract_id', [
    'chief-information-security-officer:2','vp-of-engineering:3','technical-product-manager:2',
    'technical-lead:3','domain-architect:4','data-architect:4','integration-architect:2',
    'network-architect:4','staff-engineer:4','api-developer:2','integration-developer:3',
    'build-engineer:3','gitops-and-continuous-delivery-engineer:3','open-source-program-office-engineer:1',
    'performance-test-engineer:4','database-reliability-engineer:3','data-modeller:4',
    'data-owner:2','data-governance-lead:2','ai-governance-officer:4','kubernetes-platform-engineer:2',
    'container-platform-engineer:2','container-platform-engineer:4','environment-manager:4',
    'observability-engineer:1','observability-engineer:4','sd-wan-and-edge-engineer:3',
    'change-manager:4','configuration-manager:1','cryptography-and-pki-engineer:4',
    'cloud-security-engineer:1','application-security-engineer:1','purple-team-lead:4',
    'bug-bounty-programme-manager:1','interaction-designer:1','it-procurement-specialist:1',
    'high-performance-computing-engineer:1','physical-security-solution-builder-sabsa-builder-s-view:2',
])
def test_complete_nonimplementation_population_does_not_require_component_build_details(contract_id, content_engine):
    units = content_engine.resolve(contract_id)['blueprint']['semantic_units']
    assert not any(unit['id'].startswith('type/implementation-specification.') for unit in units)
    assert any('role_gate_observations' in unit['id'] for unit in units)


@pytest.mark.parametrize('contract_id', [
    'erp-and-crm-consultant-developer:1','integration-developer:2',
    'physical-security-solution-builder-sabsa-builder-s-view:4',
    'secure-delivery-devsecops-architect:4','security-component-specialist-sabsa-tradesman-s-view:1',
])
def test_actual_implementation_specifications_keep_component_verification(contract_id, content_engine):
    units = content_engine.resolve(contract_id)['blueprint']['semantic_units']
    assert any(unit['id']=='type/implementation-specification.implementation_acceptance' for unit in units)


@pytest.mark.parametrize('contract_id', [
    'end-user-computing-engineer:3','security-engineer:1','adversary-emulation-engineer:2',
    'mobile-engineer:4','ux-designer:1','product-designer:2','interaction-designer:4','service-designer:4',
])
def test_operational_outputs_and_noncoding_designs_are_not_mandatory_code_experiments(contract_id, content_engine):
    units = content_engine.resolve(contract_id)['blueprint']['semantic_units']
    assert not any(unit['id'].startswith('type/prototype.') for unit in units)


@pytest.mark.parametrize('contract_id', ['staff-engineer:3','research-engineer:1','quantum-computing-engineer:1'])
def test_actual_experimental_code_keeps_reproducibility_and_nonproduction_scope(contract_id, content_engine):
    units = content_engine.resolve(contract_id)['blueprint']['semantic_units']
    assert any(unit['id']=='type/prototype.prototype_hypothesis' for unit in units)
    assert any(unit['id']=='type/prototype.prototype_reproduction' for unit in units)


@pytest.mark.parametrize('contract_id,required_unit', [
    ('mlops-engineer:3','family/software-change.change_verification'),
    ('machine-learning-engineer:2','type/configuration-baseline.baseline_verification'),
    ('machine-learning-engineer:4','family/software-change.change_verification'),
])
def test_ml_operational_artifacts_keep_actual_packaging_and_implementation_evidence(contract_id, required_unit, content_engine):
    units = content_engine.resolve(contract_id)['blueprint']['semantic_units']
    assert any(unit['id']==required_unit for unit in units)


@pytest.mark.parametrize('role,wrong', [
    ('process-analyst','models has'), ('data-modeller','models has'),
    ('ux-researcher','guides has'), ('test-automation-engineer','suites distinguishes'),
    ('adversary-emulation-engineer','controls distinguishes'),
    ('localisation-qa-analyst','results distinguishes'),
])
def test_gate_and_handover_sentences_use_a_grammatical_subject(role, wrong):
    path = next((ROOT / '.ai/skills').glob(f'it-roles-*/references/{role}.md'))
    text = path.read_text()
    assert wrong not in text
    assert 'has been accepted by the named receiving role' in text


@pytest.mark.parametrize('contract_id', ['ux-designer:1', 'product-designer:2', 'interaction-designer:4'])
def test_interaction_prototypes_preserve_native_design_states_without_code_experiments(contract_id):
    """Noncoding prototypes retain actual editable assets and observable interaction coverage."""
    sys.path.insert(0, str(ROOT / 'tools'))
    from professional_output_refinements import OUTPUT_REFINEMENTS, OUTPUT_REQUIREMENTS, delivery_form_for
    assert OUTPUT_REFINEMENTS[contract_id] == 'document'
    form = delivery_form_for('document', contract_id)
    assert form['primary_artifact'] == 'interactive-design-prototype'
    assert 'editable' in form['representation']
    requirements = ' '.join(row[2] for row in OUTPUT_REQUIREMENTS[contract_id])
    for observable in ('loading', 'empty', 'error', 'transitions', 'keyboard', 'not-tested'):
        assert observable in requirements
