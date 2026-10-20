# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Offline practical proposal authoring and independent-component consistency."""
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.ai/runtime'
sys.path.insert(0, str(RUNTIME / 'tools'))
import commercial_proposal as proposal
import commercial


def fixture(level='simple'):
    return json.loads((RUNTIME / 'commercial/fixtures' / ('proposal-' + level + '.json')).read_text())


def rules(data):
    return {item['rule_id'] for item in proposal.validate_package(data)['findings']}


@pytest.mark.parametrize('level,total', [('simple','140000'),('medium','1250000'),('complex','6800000')])
def test_complete_synthetic_inputs_are_consistent_without_becoming_approval(level, total):
    data = fixture(level)
    result = proposal.validate_package(data)
    assert result['consistency_pass'], result['findings']
    assert data['pricing']['programme_total'] == total
    assert result['professional_acceptance'] == 'NOT_APPROVED'
    assert result['execution_evidence'] == 'NOT_EXECUTED'
    assert not result['release_ready']
    assert not result['authority_granted']


@pytest.mark.parametrize('field,value,expected', [
    ('supplier_fee','84001','proposal.pricing.supplier_fee_mismatch'),
    ('programme_total','158000','proposal.pricing.programme_total_mismatch'),
    ('supplier_fee',84000,'proposal.input.schema'),
    ('supplier_fee','NaN','proposal.input.schema'),
    ('supplier_fee','Infinity','proposal.input.schema')])
def test_material_price_and_decimal_mutations_fail(field, value, expected):
    data = fixture()
    data['pricing'][field] = value
    assert expected in rules(data)


def test_day_rate_currency_and_milestone_calculations_are_independent():
    data = fixture()
    data['pricing']['labour'][0]['day_rate'] = '701'
    assert 'proposal.pricing.day_rate_mismatch' in rules(data)
    data = fixture()
    data['pricing']['labour'][0]['currency'] = 'EUR'
    assert 'proposal.pricing.currency_mismatch' in rules(data)
    data = fixture()
    data['milestones'][0]['payment_amount'] = '1'
    assert 'proposal.pricing.milestone_amount_mismatch' in rules(data)
    assert 'proposal.pricing.milestone_total_mismatch' in rules(data)


@pytest.mark.parametrize('kind,field,value,expected', [
    ('commercial-proposal','supplier_fee','99999','supplier_fee'),
    ('statement-of-work','deliverable_ids',['D1'],'deliverable_ids'),
    ('technical-proposal','technical_commitments',[],'technical_commitments'),
    ('delivery-proposal','milestones',[],'milestones'),
    ('rfp-response','rfp_answers',[],'rfp_answers'),
    ('proposal-compliance-matrix','acceptance',[],'acceptance')])
def test_independently_reported_component_claims_cannot_disagree(kind, field, value, expected):
    data = fixture()
    data['documents'][kind][field] = value
    assert 'proposal.document.inconsistent_' + expected in rules(data)


def test_missing_component_and_scope_commitment_dangling_refs_fail():
    data = fixture()
    del data['documents']['statement-of-work']
    assert 'proposal.document.package_membership' in rules(data)
    data = fixture()
    data['technical_commitments'][0]['deliverable_ids'].append('UNSCOPED')
    assert 'proposal.traceability.missing_or_unknown' in rules(data)
    data = fixture()
    data['scope']['deliverable_ids'].pop()
    assert 'proposal.scope.deliverables_mismatch' in rules(data)


def test_schedule_dependencies_and_acceptance_must_be_deliverable_specific():
    data = fixture()
    data['dependencies'][0]['required_by_day'] = 9999
    assert 'proposal.schedule.dependency_after_start' in rules(data)
    data = fixture()
    data['milestones'][0]['acceptance_ids'] = ['A5']
    assert 'proposal.acceptance.milestone_mismatch' in rules(data)
    data = fixture()
    data['acceptance'][0]['status'] = 'PASS'
    assert 'proposal.acceptance.unverified_execution' in rules(data)
    data = fixture()
    data['milestones'][1]['start_day'] = 0
    assert 'proposal.schedule.predecessor_not_complete' in rules(data)


def test_rfp_coverage_conditions_and_execution_evidence_are_not_fabricated():
    data = fixture()
    data['rfp_answers'].pop()
    assert 'proposal.rfp.unanswered' in rules(data)
    data = fixture()
    data['rfp_answers'][0]['conditions'] = []
    assert 'proposal.rfp.condition_missing' in rules(data)
    data = fixture()
    data['rfp_answers'][0]['status'] = 'COMPLY'
    data['evidence'][0]['status'] = 'OBSERVED'
    assert 'proposal.rfp.unverified_comply' in rules(data)
    data = fixture()
    data['rfp_answers'][0]['evidence_ids'] = ['missing']
    assert 'proposal.rfp.evidence_missing' in rules(data)


def test_optional_security_offer_is_excluded_even_when_selected():
    data = fixture()
    data['optional_offerings'][0]['selected'] = True
    data['documents']['cybersecurity-transformation-proposal'] = proposal._claims(data)
    assert proposal.validate_package(data)['consistency_pass']
    assert data['pricing']['programme_total'] == '140000'
    data['optional_offerings'][0]['included_in_base'] = True
    assert 'proposal.optional.base_scope_conflict' in rules(data)


def test_open_inputs_and_unsupported_assurance_remain_nonpassing():
    data = fixture()
    data['narrative']['situation'] = {'text':'','knowledge_status':'unknown','source_ids':[]}
    assert 'proposal.narrative.open' in rules(data)
    data = fixture()
    data['narrative']['security_constraints']['text'] = 'The supplier is certified and fully compliant.'
    assert 'proposal.claim.unsupported_assurance' in rules(data)
    data = fixture()
    data['sources'][0]['classification'] = 'confidential'
    assert 'proposal.classification.synthetic_source_conflict' in rules(data)


def test_actual_reference_selection_uses_context_and_audience(tmp_path):
    data = fixture()
    source = RUNTIME / 'content/expert_references/client-proposal/simple.md'
    text = source.read_text()
    text = text.replace('language: en', "target_audiences: ['buying sponsor and procurement']\napplicability_context: {industry: 'fictional enterprise services'}\nlanguage: en")
    override = tmp_path / 'client-proposal/simple.md'
    override.parent.mkdir()
    override.write_text(text)
    result = proposal.plan_package(data, ROOT, engagement_root=tmp_path)
    assert len(result['documents']) == 8
    selection = result['documents'][0]['selection']
    assert selection['scope'] == 'engagement'
    assert selection['selection_context']['context_supplied']
    assert selection['selection_context']['audience_supplied']
    data['selection_context']['industry'] = 'unrelated industry'
    result = proposal.plan_package(data, ROOT, engagement_root=tmp_path)
    assert result['documents'][0]['selection']['scope'] == 'bundled'


@pytest.fixture(scope='module')
def prepared(tmp_path_factory):
    directory = tmp_path_factory.mktemp('proposal-draft')
    data = fixture()
    result = proposal.prepare_package(data, directory, ROOT)
    return directory, result


def test_actual_markdown_pack_is_tailored_and_contains_only_explicit_case_inputs(prepared):
    directory, result = prepared
    assert result['prepared_documents'] == 8
    assert result['consistency']['consistency_pass']
    text = (directory / 'commercial-proposal.md').read_text()
    assert 'GBP 84,000.00' in text and 'GBP 140,000.00' in text
    assert '| W1 | 15 | GBP 700.00 | GBP 10,500.00 |' in text
    assert 'NOT FOR SUBMISSION' in text
    assert 'Harborline' not in text and 'Meridian' not in text and 'Orion' not in text
    technical = (directory / 'technical-proposal.md').read_text()
    assert 'duplicate-safe connector' in technical
    assert technical != text
    assert 'Acceptance and receiving authority' in technical
    assert 'RFP1' in (directory / 'rfp-response.md').read_text()
    assert proposal.validate_prepared(directory / 'proposal-package.json', ROOT)['draft_integrity'] == 'PASS'


def test_edited_draft_is_rejected_even_if_unsigned_manifest_is_rehashed(prepared, tmp_path):
    import shutil
    directory, _ = prepared
    target = tmp_path / 'edited'
    shutil.copytree(directory, target)
    path = target / 'commercial-proposal.md'
    path.write_text(path.read_text().replace('84,000.00','99,000.00'))
    manifest_path = target / 'proposal-package.json'
    manifest = json.loads(manifest_path.read_text())
    record = next(item for item in manifest['documents'] if item['kind'] == 'commercial-proposal')
    record['markdown_hash'] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest))
    assert not proposal.validate_prepared(manifest_path, ROOT)['consistency_pass']


def test_changed_semantic_claim_is_not_accepted_after_rehash(prepared, tmp_path):
    import shutil
    directory, _ = prepared
    target = tmp_path / 'edited'
    shutil.copytree(directory,target)
    path = target / 'statement-of-work.semantic.json'
    model = json.loads(path.read_text())
    model['proposal_claims']['supplier_fee'] = '99999'
    path.write_text(json.dumps(model))
    manifest_path = target / 'proposal-package.json'
    manifest = json.loads(manifest_path.read_text())
    next(item for item in manifest['documents'] if item['kind']=='statement-of-work')['semantic_hash'] = proposal._digest(model)
    manifest_path.write_text(json.dumps(manifest))
    assert proposal.validate_prepared(manifest_path, ROOT)['draft_integrity'] == 'FAIL'


def test_handoff_uses_existing_hard_gates_and_never_infers_authority(prepared,tmp_path):
    directory, _ = prepared
    result = proposal.publication_handoff(directory/'proposal-package.json','client-proposal',tmp_path/'projection',ROOT)
    assert result['status'] == 'BLOCKED'
    assert any('canonical commercial snapshot' in item for item in result['blockers'])
    assert any('host-authenticated' in item for item in result['blockers'])
    assert not result['authority_granted']
    assert not (tmp_path/'projection').exists()


def test_prepare_refuses_overwrite_and_cli_distinguishes_consistency_from_approval(prepared,capsys):
    directory, _ = prepared
    with pytest.raises(ValueError):
        proposal.prepare_package(fixture(),directory,ROOT)
    status = commercial.main(['--profile','commercial-delivery/1','proposal-validate',str(RUNTIME/'commercial/fixtures/proposal-simple.json')])
    assert status == 0
    result = json.loads(capsys.readouterr().out)
    assert result['consistency_pass'] and not result['release_ready']


@pytest.mark.parametrize('level,totals,rate,days,duration', [
    ('simple',('84,000','42,000','14,000','140,000'),'700',120,'10 weeks'),
    ('medium',('780,000','270,000','200,000','1,250,000'),'1,000',780,'32 weeks'),
    ('complex',('4,500,000','1,500,000','800,000','6,800,000'),'1,500',3000,'18 months')])
def test_actual_bundled_reference_pack_numeric_baselines(level,totals,rate,days,duration):
    from decimal import Decimal
    for kind in proposal.CORE_KINDS:
        text = (RUNTIME/'content/expert_references'/kind/(level+'.md')).read_text()
        if kind not in ('technical-proposal','delivery-proposal'):
            assert totals[0] in text, kind
            assert totals[3] in text, kind
        elif kind == 'technical-proposal':
            assert not re.findall(r'[£€][0-9]', text), 'Technical reference contains no financial assertions to reconcile.'
    commercial_text = (RUNTIME/'content/expert_references/commercial-proposal'/(level+'.md')).read_text()
    matches = re.findall(r'\|[^\n|]+\|\s*(\d+) days × [£€]([\d,]+)/day\s*\|\s*[£€]([\d,]+)\s*\|',commercial_text)
    assert matches
    assert sum(int(item[0]) for item in matches) == days
    for effort,sell_rate,total in matches:
        assert Decimal(effort)*Decimal(sell_rate.replace(',','')) == Decimal(total.replace(',',''))
    assert sum(Decimal(total.replace(',','')) for _,_,total in matches) == Decimal(totals[0].replace(',',''))
    assert all(value in commercial_text for value in totals)
    assert 'not included' in commercial_text.lower() and 'optional' in commercial_text.lower()
    delivery_text = (RUNTIME/'content/expert_references/delivery-proposal'/(level+'.md')).read_text()
    assert duration in delivery_text
    delivery_lines = re.findall(r'\|[^\n|]+\|\s*(\d+)\s*\|\s*[£€]([\d,]+)\s*\|\s*[£€]([\d,]+)\s*\|', delivery_text)
    assert delivery_lines
    assert sum(Decimal(total.replace(',','')) for _,_,total in delivery_lines) == Decimal(totals[0].replace(',',''))
    for effort,sell_rate,total in delivery_lines:
        assert Decimal(effort)*Decimal(sell_rate.replace(',','')) == Decimal(total.replace(',',''))


def test_optional_offering_has_own_acceptance_and_missing_boundary_is_open():
    data = fixture()
    data['optional_offerings'][0]['selected'] = True
    data['documents']['cybersecurity-transformation-proposal'] = proposal._claims(data)
    assert proposal.validate_package(data)['consistency_pass']
    text = '\n'.join(section['body'] for section in proposal._sections(data,'cybersecurity-transformation-proposal'))
    assert 'Base-programme acceptance records do not accept' in text
    assert '| A1 |' not in text
    del data['optional_offerings'][0]['response_clock']
    assert 'proposal.optional.own_boundaries_open' in rules(data)


def test_draft_document_control_and_currency_presentation(prepared):
    directory,_ = prepared
    text = (directory/'client-proposal.md').read_text()
    assert '**Document control:**' in text
    assert 'Revision' in text and 'Audience:' in text and 'Classification:' in text
    assert 'Proposed owner:' in text
    assert 'GBP 140,000.00' in text
    assert 'confirmation..' not in text


def test_existing_credential_blocker_prevents_any_draft_files(tmp_path):
    data = fixture()
    data['narrative']['technical_approach']['text'] += ' api_key=synthetic-secret-abcdef12345678901234567890'
    target = tmp_path/'blocked'
    with pytest.raises(ValueError,match='security or governance'):
        proposal.prepare_package(data,target,ROOT)
    assert not target.exists()


def test_existing_trusted_host_can_project_exact_draft_without_granting_authority(prepared,tmp_path):
    from test_commercial_core import complete_snapshot
    from test_content_lint import authenticated_dispatcher_review
    from content_spec import ContentSpec
    import commercial_core as core
    directory,_ = prepared
    data = fixture()
    markdown = (directory/'client-proposal.md').read_text()
    snapshot, trusted = complete_snapshot()
    publication = next(entity for entity in snapshot['entities'] if entity['version_id']=='publication@1')
    publication['classification'] = 'client-contract'
    publication['data'].update({field:'Synthetic contractual disclosure; no real authority or deployment claim.' for field in core.MANDATORY})
    publication['data']['proposal_markdown'] = markdown
    policy = {'version':'synthetic-test-1','mandatory_disclosure':sorted(core.MANDATORY),
              'surfaces':['json-payload'],'fields':{'Publication':[*sorted(core.MANDATORY),'proposal_markdown']}}
    data['canonical_snapshot'],data['disclosure_policy'] = snapshot,policy
    staged = tmp_path/'source'
    proposal.prepare_package(data,staged,ROOT)
    model = json.loads((staged/'client-proposal.semantic.json').read_text())
    spec = ContentSpec(ROOT).resolve(model['contract_id'],model['context'])
    signed,review,dispatcher = authenticated_dispatcher_review(model,spec)
    # Existing commercial fixture models a trusted host boundary only; it is not
    # evidence of live isolation, professional human acceptance or JAI L0 action.
    callbacks = {'identity_verifier':trusted.get,
                 'fabric_resolver':lambda contract,graph: contract['data']['layer'] in range(1,7),
                 'enforcement_verifier':lambda control,record: True}
    assert core.readiness(snapshot,**callbacks)['ready']
    result = proposal.publication_handoff(staged/'proposal-package.json','client-proposal',tmp_path/'projection',ROOT,
        reviewer=review,trusted_executions=dispatcher.verify,readiness_verifiers=callbacks,producer=signed['producer'])
    assert result['status'] == 'DRAFT_PROJECTED',result
    assert (tmp_path/'projection/projection-manifest.json').is_file()
    assert not result['authority_granted'] and not result['release_ready']


def test_validate_reuses_existing_secret_policy_and_redacts_diagnostics():
    data = fixture()
    data['narrative']['technical_approach']['text'] += ' api_key=synthetic-secret-abcdef12345678901234567890'
    report = proposal.validate_package(data)
    assert not report['consistency_pass']
    assert 'global.secret_disclosure' in {item['rule_id'] for item in report['findings']}
    assert 'abcdef12345678901234567890' not in json.dumps(report)


def test_unknown_customer_input_is_not_promoted_to_an_assumption_or_known_fact():
    data = fixture()
    data['narrative']['situation'] = {'text':'','knowledge_status':'unknown','source_ids':[]}
    value = proposal._unit_value('customer_need','object',data,[])
    assert value['knowledge_status'] == 'unknown'
    assert 'OPEN' in value['text']


@pytest.mark.parametrize('level,supplier,programme,recurring,onboarding,first_year', [
    ('simple',84000,140000,28800,4500,33300),
    ('medium',780000,1250000,180000,45000,225000),
    ('complex',4500000,6800000,780000,210000,990000)])
def test_reviewed_optional_security_prices_reconcile_without_entering_baseline(
        level,supplier,programme,recurring,onboarding,first_year):
    """Check actual illustrative source amounts, retaining their synthetic status."""
    from decimal import Decimal
    assert recurring + onboarding == first_year
    texts={kind:(RUNTIME/'content/expert_references'/kind/(level+'.md')).read_text()
           for kind in ('commercial-proposal','managed-security-services-proposal')}
    for kind,text in texts.items():
        for amount in (supplier,programme,onboarding,first_year):
            assert f'{amount:,}' in text,kind
        assert 'optional' in text.lower()
        assert 'separate' in text.lower()
        assert 'not-human-approved' in text
        assert 'NOT_EXECUTED if no actual test or review' in text
    commercial_text=texts['commercial-proposal']
    payments=re.findall(r'\|[^\n|]+\|\s*(\d+)%\s*\|\s*[£€]([\d,]+)\s*\|',commercial_text)
    assert payments, 'The actual commercial reference must retain its milestone schedule.'
    assert sum(int(percent) for percent,_ in payments)==100
    assert sum(Decimal(amount.replace(',','')) for _,amount in payments)==Decimal(supplier)
    for percent,amount in payments:
        assert Decimal(percent)*Decimal(supplier)/100==Decimal(amount.replace(',',''))
    service_text=texts['managed-security-services-proposal']
    if level=='complex':
        assert f'{recurring:,}' in service_text
        assert 'annual recurring' in service_text
    else:
        assert f'{recurring//12:,}' in service_text
        assert '12-month' in service_text
    data=fixture(level)
    for offer in data['optional_offerings']:
        offer['selected']=True
        data['documents'][offer['kind']]=proposal._claims(data)
    result=proposal.validate_package(data)
    assert result['consistency_pass'],result['findings']
    assert Decimal(data['pricing']['programme_total'])==Decimal(programme)
    assert result['execution_evidence']=='NOT_EXECUTED'
    assert result['professional_acceptance']=='NOT_APPROVED'
    assert not result['authority_granted']
