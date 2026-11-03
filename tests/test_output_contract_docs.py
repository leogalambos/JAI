# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Exercise generated public contracts, ownership boundaries and explicit bindings."""
import importlib.util
import json
from pathlib import Path
import re
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('output_docs', ROOT / 'tools/generate_output_contract_docs.py')
docs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(docs)


def test_block_replacement_preserves_manual_prose_and_rejects_ambiguous_ownership():
    text = 'Manual introduction\n' + docs.START + '\nOld\n' + docs.END + '\nManual ending\n'
    updated = docs.replace_block(text, 'Current\n')
    assert updated == 'Manual introduction\n' + docs.START + '\nCurrent\n' + docs.END + '\nManual ending\n'
    assert docs.replace_block(updated, 'Current') == updated
    for malformed in ('', docs.END + docs.START, text + docs.START):
        with pytest.raises(ValueError, match='marker pair'):
            docs.replace_block(malformed, 'replacement')


def test_generation_checks_without_writes_and_removes_only_obsolete_owned_sections(tmp_path):
    directory = tmp_path / docs.DIRECTORY
    directory.mkdir(parents=True)
    stale = directory / 'spec-obsolete.md'
    stale.write_text(docs._owned('Obsolete'))
    retained = directory / 'manual.md'
    retained.write_text('Manual documentation\n')
    current = directory / 'index.md'
    current.write_text(docs._owned('Old index') + 'Manual suffix\n')
    fixture = {docs.DIRECTORY + '/index.md': 'New index'}
    with patch.object(docs.Projection, '__init__', return_value=None), patch.object(docs.Projection, 'render', return_value=fixture):
        before = {p.name: p.read_bytes() for p in directory.iterdir()}
        assert docs.main(['--root', str(tmp_path), '--check']) == 1
        assert {p.name: p.read_bytes() for p in directory.iterdir()} == before
        assert docs.generate(tmp_path) == 0
        assert not stale.exists()
        assert retained.read_text() == 'Manual documentation\n'
        assert current.read_text() == docs._owned('New index') + 'Manual suffix\n'
        assert docs.generate(tmp_path, check=True) == 0
        current.write_text('Unowned page\n')
        with pytest.raises(ValueError, match='unowned page'):
            docs.generate(tmp_path)
        assert current.read_text() == 'Unowned page\n'


@pytest.fixture(scope='module')
def projection():
    return docs.Projection(ROOT)


def test_all_role_outputs_and_workflow_handoffs_resolve_to_public_contracts(projection):
    pages = projection.render()
    role_catalogue = pages['docs/reference/roles.md']
    workflow_catalogue = pages['docs/reference/workflows.md']
    for role in projection.roles:
        role_page = pages[f'{docs.DIRECTORY}/role-{role["slug"]}.md']
        contracts = [contract for contract in projection.contracts.values() if contract['role_slug'] == role['slug']]
        assert len(contracts) == len(role['primary_deliverables'])
        for contract in contracts:
            cid = contract['id']
            assert f'id="{docs.Projection.anchor(cid)}"' in role_page
            assert f'output-contracts/role-{role["slug"]}.md#{docs.Projection.anchor(cid)}' in role_catalogue
            binding = projection.catalogue.bindings[cid]
            compiled = projection.compiled_for(binding['content_spec_ref'], binding.get('overlays', []))
            for ancestor in compiled['inheritance']:
                target = projection.spec_paths[ancestor['id']].split('#')[0]
                assert f'{docs.DIRECTORY}/{target}' in pages
    for handoff in projection.handoffs.values():
        assert handoff['acceptance_criterion'] in workflow_catalogue
        for cid in handoff['contract_ids']:
            role = projection.contracts[cid]['role_slug']
            assert f'output-contracts/role-{role}.md#{docs.Projection.anchor(cid)}' in workflow_catalogue
    assert not any('INBOX/' in text or '/home/' in text for text in pages.values())


def test_conditions_prohibitions_sources_and_approval_limits_remain_explicit(projection):
    rendered = projection.spec_body('type/risk-assessment')
    specification = projection.catalogue.specs['type/risk-assessment']
    for group in docs.GROUPS:
        for unit in specification.get(group, []):
            assert unit['id'] in rendered
            if 'when' in unit:
                assert json.dumps(unit['when'], sort_keys=True) in rendered
    assert 'Unknown applicability stays unresolved' in rendered
    assert 'Prohibited content (MUST NOT)' in rendered
    assert 'does not approve it' in rendered
    assert 'not a claim that an external standard mandates it' in rendered
    assert 'professional' in rendered.lower()
    for source in specification.get('sources', {}).get('professional_references', []):
        assert source['title'] in rendered
        assert source['basis'] in rendered
        assert source['scope'] in rendered
        assert source['limits'] in rendered
    assert projection.compiled_for('type/risk-assessment') is projection.compiled_for('type/risk-assessment')
    with pytest.raises(ValueError, match='UNREGISTERED_REFERENCE'):
        projection.compiled_for('missing/specification')


def test_obsolete_owned_block_is_removed_while_manual_prefix_and_suffix_survive(tmp_path):
    directory = tmp_path / docs.DIRECTORY
    directory.mkdir(parents=True)
    stale = directory / 'spec-obsolete.md'
    stale.write_text('Manual prefix\n' + docs._owned('Obsolete') + 'Manual suffix\n')
    with patch.object(docs.Projection, '__init__', return_value=None), patch.object(docs.Projection, 'render', return_value={}):
        assert docs.generate(tmp_path, check=True) == 1
        assert docs.generate(tmp_path) == 0
        assert stale.read_text() == 'Manual prefix\n\nManual suffix\n'
        assert docs.generate(tmp_path, check=True) == 0


def test_obsolete_symlink_is_rejected_without_changing_its_target(tmp_path):
    directory = tmp_path / docs.DIRECTORY
    directory.mkdir(parents=True)
    target = tmp_path / 'manual.md'
    target.write_text(docs._owned('Must not be replaced') + 'Manual suffix\n')
    stale = directory / 'spec-obsolete.md'
    stale.symlink_to(target)
    with patch.object(docs.Projection, '__init__', return_value=None), patch.object(docs.Projection, 'render', return_value={}):
        for check in (True, False):
            with pytest.raises(ValueError, match='symbolic-link candidate'):
                docs.generate(tmp_path, check=check)
        assert target.read_text() == docs._owned('Must not be replaced') + 'Manual suffix\n'
        assert stale.is_symlink()


def test_source_owned_handoffs_have_real_content_contracts(projection):
    pages = projection.render()
    source_owned = [row for row in projection.handoffs.values() if not row['contract_ids']]
    assert {row['handoff_id'] for row in source_owned} == {
        'ai-system-approval:6',
        *(f'semantic-to-enterprise-publication:{n}' for n in range(1,6)),
    }
    for handoff in source_owned:
        source = handoff['source_content_contract']
        page = pages[f'{docs.DIRECTORY}/workflow-{handoff["workflow_id"]}.md']
        assert f'id="{docs.Projection.anchor(source["id"])}"' in page
        assert source['basis'] in page
        for criterion in source['required']:
            assert criterion in page
        for condition in source['conditional']:
            assert condition['when'] in page
            assert condition['requirement'] in page
        assert handoff['acceptance_criterion'] in page


def test_professional_sources_are_explicit_scoped_and_never_claim_normative_approval(projection):
    for specification in projection.catalogue.specs.values():
        sources = specification['sources']['professional_references']
        assert sources
        for source in sources:
            assert source['title'] and source['scope'] and source['limits']
            assert source['basis'] in ('informed-by', 'jai-practice')
            assert source.get('url') or source['basis'] == 'jai-practice'
        for group in docs.GROUPS:
            for unit in specification.get(group, []):
                assert unit.get('provenance', {}).get('normative_claim') is False


def test_executable_outputs_and_specialist_obligations_keep_specific_meaning(projection):
    for cid, expected in {
        'blockchain-and-smart-contract-developer:1': 'software-change',
        'data-privacy-engineer:2': 'software-change',
        'privacy-analyst:1': 'risk-assessment',
    }.items():
        assert projection.catalogue.bindings[cid]['semantic_family'] == expected
    for cid, field in {
        'privacy-analyst:1': 'data_subject_risks',
        'chief-information-officer:4': 'budget_allocation',
        'contract-manager:1': 'contract_obligation_records',
        'contract-manager:3': 'obligation_remedies',
        'contract-manager:4': 'notice_remedy_control',
        'blockchain-and-smart-contract-developer:2': 'verification_method_limits',
        'it-financial-management-tbm-manager:1': 'cost_allocation_model',
        'commercial-pricing-deal-finance-specialist:1': 'deal_model_calculations',
    }.items():
        selected = projection.catalogue.bindings[cid]['content_spec_ref']
        units = projection.catalogue.specs[selected]['required_information']
        matching = [unit for unit in units if field in unit['semantic_fields']]
        assert len(matching) == 1
        assert matching[0]['acceptance_criteria']


def test_reader_summary_is_generated_from_effective_rules_and_keeps_full_contract(projection):
    binding = projection.catalogue.bindings['software-engineer:1']
    summary = projection.reader_summary(binding['content_spec_ref'], binding.get('overlays', []))
    assert '**At a glance**' in summary
    assert '**Mandatory examples:**' in summary
    assert 'Unknown applicability remains unresolved' in summary
    assert 'selected examples' in summary
    assert 'complete local and linked foundation requirements' in summary
    assert 'acceptance and release remain separate' in summary
    full = projection.render()[f'{docs.DIRECTORY}/role-software-engineer.md']
    assert full.index('**At a glance**') < full.index('**Contract ID:**')
    assert '### Prohibited content (MUST NOT)' in full


@pytest.mark.parametrize('reference,expected_condition', [
    ('global/invariants', 'No additional conditional trigger is declared.'),
    ('type/architecture-definition',
     'personal data are processed; an applicable regulatory requirement exists.'),
])
def test_reader_summary_separates_conditions_from_uncertainty(reference, expected_condition, projection):
    summary = projection.reader_summary(reference)
    condition = next(line for line in summary.splitlines()
                     if line.startswith('- **Conditions to resolve:**'))
    assert condition == ('- **Conditions to resolve:** ' + expected_condition
                         + ' Unknown applicability remains unresolved.')
    assert not re.search(r'\.\.+\s+Unknown', condition)


def test_framework_context_does_not_duplicate_terminal_punctuation(projection):
    body = projection.spec_body('kind/role/bid-proposal-manager:1')
    framework = next(line for line in body.splitlines() if line.startswith('- **Bid / Proposal Manager:**'))
    assert '.;' not in framework
    assert '..' not in framework
