# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exercise exhaustive source projection and immutable-contract compatibility."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import artifacts


def test_all_outputs_have_effective_delivery_forms_and_non_generic_acceptance():
    from generate_role_output_guidance import build_guidance
    document = build_guidance(ROOT)
    assert len(document['outputs']) == 1139
    assert document['role_count'] == 286 and document['domain_count'] == 17
    for record in document['outputs']:
        assert len(record['acceptance_criteria']) >= 3
        assert record['delivery_form']['primary_artifact']
        assert 'complete, dated and attributable' not in record['effective_deliverable']['acceptance_criterion']
        assert record['legacy_source_fingerprint']
        assert record['source_contract_hash']


def test_every_authored_correction_and_domain_basis_has_an_exact_source():
    from generate_role_output_guidance import build_guidance
    from professional_output_refinements import OUTPUT_REFINEMENTS
    from content_catalog_definitions import (PROFESSIONAL_REFERENCES,
        ROLE_DOMAIN_PROFESSIONAL_REFERENCES, ROLE_DOMAIN_METHOD_FOCUS)
    document = build_guidance(ROOT)
    ids = {row['id'] for row in document['outputs']}
    assert set(OUTPUT_REFINEMENTS) <= ids
    assert set(ROLE_DOMAIN_PROFESSIONAL_REFERENCES) == set(range(1, 18))
    assert set(ROLE_DOMAIN_METHOD_FOCUS) == set(range(1, 18))
    for sources in ROLE_DOMAIN_PROFESSIONAL_REFERENCES.values():
        assert sources
        for source in sources:
            assert PROFESSIONAL_REFERENCES[source]['url'].startswith('https://')


def test_factual_and_native_outputs_do_not_inherit_an_option_appraisal():
    from generate_role_output_guidance import build_guidance
    rows = {row['id']: row for row in build_guidance(ROOT)['outputs']}
    for cid in ('digital-forensics-examiner:2', 'incident-responder:4',
                'major-incident-manager:4', 'research-scientist:3',
                'delivery-manager:3', 'service-level-analyst:1',
                'integration-developer:4', 'engineering-manager:2'):
        assert rows[cid]['semantic_family'] == 'analysis-report'
        assert 'Compare viable options' not in rows[cid]['effective_deliverable']['acceptance_criterion']
        assert 'No evidence needed' not in rows[cid]['effective_deliverable']['acceptance_criterion']
    for cid in ('network-operations-centre-analyst:2', 'network-operations-centre-analyst:3'):
        assert rows[cid]['semantic_family'] == 'register'
    for cid in ('detection-engineer:1', 'malware-analyst:4', 'exploit-developer:1', 'cloud-operations-engineer:3'):
        assert rows[cid]['semantic_family'] in ('software-change', 'prototype', 'deployment-automation')
        assert rows[cid]['delivery_form']['primary_artifact'] not in ('decision-paper', 'professional-document')


def test_source_projection_drift_is_checked_at_ci_build_boundaries():
    for name, executable in [('validate-library.yml', 'python3'), ('release.yml', 'python3'), ('pages.yml', 'python')]:
        text = (ROOT / '.github/workflows' / name).read_text()
        assert executable + ' tools/generate_role_output_guidance.py --root . --check' in text
        assert executable + ' tools/generate_content_catalog.py --check' in text


def test_all_role_sources_follow_effective_records_without_erasing_legacy_identity():
    from generate_role_output_guidance import build_guidance
    document = build_guidance(ROOT)
    raw = {row['id']: row for row in json.loads((ROOT / '.ai/runtime/artifacts/contracts/role-deliverables.v3.json').read_text())['contracts']}
    roles = json.loads((ROOT / '.ai/runtime/roles.json').read_text())['roles']
    live = artifacts.live_deliverables({'skills': ROOT / '.ai/skills'}, roles)
    selected = artifacts._projection_policies(ROOT / '.ai/runtime', set(raw))
    assert len(live) == 1139
    for record in document['outputs']:
        assert artifacts.guidance_source_matches(raw[record['id']], live[record['id']], record, selected[record['id']])


def test_role_projection_preserves_all_gates_inputs_and_only_changes_delivery_rows(tmp_path):
    from generate_role_output_guidance import project_role
    role = ROOT / '.ai/skills/it-roles-software-development-and-engineering/references/software-engineer.md'
    original = role.read_text()
    record = {'deliverable_number': 1, 'effective_deliverable': {
        'name': 'Reviewed and merged code', 'format': 'Actual versioned source',
        'acceptance_criterion': 'Trace the revision, actual checks and independent review.'}}
    projected = project_role(original, [record])
    before = artifacts.sections(original)
    after = artifacts.sections(projected)
    assert before[3] == after[3] and before[7] == after[7]
    assert before[15] == after[15]
    assert 'Actual versioned source' in projected
    assert project_role(projected, [record]) == projected
    with pytest.raises(ValueError, match='missing'):
        project_role(original, [dict(record, deliverable_number=99)])


def test_framework_projection_is_owned_conditional_and_preserves_manual_sections():
    from generate_role_output_guidance import project_framework_guidance
    path = ROOT / '.ai/skills/it-roles-sabsa-security-architecture/references/sabsa-and-togaf-integration-architect.md'
    original = path.read_text()
    result = project_framework_guidance(original)
    sections = artifacts.sections(result)
    before = artifacts.sections(original)
    assert before[3] == sections[3] and before[7] == sections[7]
    assert before[15] == sections[15]
    assert '- SABSA\n' in result and '- ArchiMate 3.2\n' in result
    assert 'professional source candidates' in result
    assert 'ArchiMate 3.2 is opt-in' in result
    assert 'No external EA application is required' in result
    assert 'architecture review under SABSA' not in result
    assert project_framework_guidance(result) == result
    assert result.count('JAI:FRAMEWORK-APPLICABILITY:START') == 1
    with pytest.raises(ValueError, match='marker'):
        project_framework_guidance(result + '\n<!-- JAI:FRAMEWORK-APPLICABILITY:START -->\n')
    with pytest.raises(ValueError, match='section 14'):
        project_framework_guidance(original.replace('## 14. Reference frameworks', '## 114. Reference frameworks'))


def test_framework_projection_does_not_add_notation_to_unrelated_roles():
    from generate_role_output_guidance import project_framework_guidance
    original = (ROOT / '.ai/skills/it-roles-service-management-and-support/references/service-desk-analyst.md').read_text()
    projected = project_framework_guidance(original)
    assert 'professional source candidates' in projected
    assert artifacts.sections(original)[1] == artifacts.sections(projected)[1]
    assert artifacts.sections(original)[4] == artifacts.sections(projected)[4]
    assert 'ArchiMate 3.2 is opt-in' not in artifacts.sections(projected)[14]


def test_guidance_cannot_authorize_unrelated_source_drift():
    from generate_role_output_guidance import build_guidance
    document = build_guidance(ROOT)
    record = next(row for row in document['outputs'] if row['id'] == 'software-engineer:1')
    raw = next(row for row in json.loads((ROOT / '.ai/runtime/artifacts/contracts/role-deliverables.v3.json').read_text())['contracts'] if row['id'] == record['id'])
    live = {'fingerprint': record['effective_fingerprint']}
    assert artifacts.guidance_source_matches(raw, live, record)
    wrong = copy.deepcopy(record)
    wrong['source_contract_hash'] = '0' * 64
    assert not artifacts.guidance_source_matches(raw, live, wrong)
    wrong = copy.deepcopy(live)
    wrong['fingerprint'] = '0' * 64
    assert not artifacts.guidance_source_matches(raw, wrong, record)


def test_rehashed_guidance_cannot_contradict_selected_professional_policy():
    from generate_role_output_guidance import build_guidance
    document = build_guidance(ROOT)
    record = next(row for row in document['outputs'] if row['id'] == 'software-engineer:1')
    raw = next(row for row in json.loads((ROOT / '.ai/runtime/artifacts/contracts/role-deliverables.v3.json').read_text())['contracts'] if row['id'] == record['id'])
    record['semantic_family'] = 'not-registered'
    record['delivery_form']['primary_artifact'] = 'invented-paper'
    record['acceptance_criteria'] = ['No evidence needed']
    record['effective_deliverable']['acceptance_criterion'] = 'No evidence needed'
    record['effective_fingerprint'] = artifacts.fingerprint(record['effective_deliverable'])
    live = {'fingerprint': record['effective_fingerprint']}
    assert not artifacts.guidance_source_matches(raw, live, record)


def test_generation_roundtrip_and_check_mode_leave_sources_unchanged(tmp_path):
    from generate_role_output_guidance import generate, main
    roles = json.loads((ROOT / '.ai/runtime/roles.json').read_text())['roles']
    relatives = ['.ai/runtime/roles.json', '.ai/runtime/artifacts/contracts/role-deliverables.v3.json']
    relatives += ['.ai/' + role['path'] for role in roles]
    for relative in relatives:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    frozen = (tmp_path / relatives[1]).read_bytes()
    assert generate(tmp_path, check=True) == 1
    assert not (tmp_path / '.ai/runtime/content/role-output-guidance.json').exists()
    assert generate(tmp_path) == 0
    assert main(['--root', str(tmp_path), '--check']) == 0
    assert (tmp_path / relatives[1]).read_bytes() == frozen
    target = tmp_path / '.ai' / roles[0]['path']
    target.write_text(target.read_text().replace('## 6. Deliverables', '## 16. Deliverables'))
    with pytest.raises(ValueError, match='missing'):
        generate(tmp_path)
    target.unlink()
    outside = tmp_path / 'outside.md'
    outside.write_text('Unrelated document\n')
    target.symlink_to(outside)
    with pytest.raises(ValueError, match='Unsafe'):
        generate(tmp_path)
    assert outside.read_text() == 'Unrelated document\n'
