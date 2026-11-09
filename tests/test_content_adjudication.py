# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Measure independent professional review without converting scores to authority."""
import copy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import content_adjudication as adjudication
from content_spec import canonical_hash


def test_prepare_blinds_variants_and_preserves_exact_case_and_spec_bindings():
    bundle = adjudication.prepare_adjudication(ROOT, ['software-engineer:1'], ['medium'])
    public = bundle['reviewer_packet']
    truth = bundle['coordinator']
    assert len(public['cases']) == 2
    assert all('expected' not in case and 'author' not in case for case in public['cases'])
    assert {case['seed_class'] for case in truth['cases']} == {'reference', 'seeded-defect'}
    assert all(case['compiled_spec_hash'] and case['material_hash'] for case in public['cases'])
    assert not public['professional_approval']
    assert public['packet_hash'] == canonical_hash({k: v for k, v in public.items() if k != 'packet_hash'})
    with pytest.raises(ValueError, match='EMPTY'):
        adjudication.prepare_adjudication(ROOT, [], ['medium'])
    with pytest.raises(ValueError, match='COMPLEXITY'):
        adjudication.prepare_adjudication(ROOT, ['software-engineer:1'], ['unsupported'])


def test_full_adjudication_inventory_covers_every_output_domain_and_complexity():
    bundle = adjudication.prepare_adjudication(ROOT)
    cases = bundle['reviewer_packet']['cases']
    assert len(cases) == 1139 * 3 * 2
    assert len({case['contract_id'] for case in cases}) == 1139
    assert len({case['domain_index'] for case in cases}) == 17
    assert {case['complexity'] for case in cases} == {'simple', 'medium', 'complex'}
    report = adjudication.assess_adjudication(bundle, [])
    assert report['status'] == 'PENDING_INDEPENDENT_REVIEW'
    assert report['verified_review_count'] == 0
    assert len(report['coverage']['outputs']) == 1139
    assert len(report['coverage']['domains']) == 17
    assert all(not row['independent_pair_complete'] for row in report['coverage']['outputs'].values())


def reviews_for(bundle):
    packet = bundle['reviewer_packet']
    truth = {case['case_id']: case for case in bundle['coordinator']['cases']}
    records, host, assignments = [], {}, {}
    for principal in ('reviewer-a', 'reviewer-b'):
        assignments[principal] = [5]
        for case in packet['cases']:
            subject = {
                'packet_hash': packet['packet_hash'], 'case_id': case['case_id'],
                'material_hash': case['material_hash'], 'compiled_spec_hash': case['compiled_spec_hash'],
                'reviewed_digest': case['material_hash'],
                'context_manifest': {'domain': 5},
                'verdict': 'REWORK' if truth[case['case_id']]['seed_class'] == 'seeded-defect' else 'ACCEPTABLE',
                'criteria': [{'criterion': criterion, 'score': 3,
                              'rationale': 'Bounded synthetic judgement for this exact case.',
                              'evidence': 'Case conclusion and cited source unit were compared.'}
                             for criterion in adjudication.RUBRIC],
                'findings': []}
            if subject['verdict'] == 'REWORK':
                subject['findings'] = [{'severity': 'critical', 'location': 'conclusion',
                                       'criterion': truth[case['case_id']]['expected_criterion'],
                                       'evidence': 'Unsupported conclusion exceeds the stated evidence.'}]
            token = principal + ':' + case['case_id']
            host[token] = {'principal': principal, 'reviewer': True,
                           'subject_digest': canonical_hash(subject),
                           'snapshot_digest': case['material_hash'],
                           'context_digest': canonical_hash(subject['context_manifest'])}
            records.append({**subject, 'attestation': token})
    return records, host.get, assignments


def test_authenticated_reviews_measure_recall_agreement_and_coverage_without_approval():
    bundle = adjudication.prepare_adjudication(ROOT, ['software-engineer:1'], ['medium'])
    records, verifier, assignments = reviews_for(bundle)
    result = adjudication.assess_adjudication(bundle, records, verifier, assignments,
                                            author_principals=['source-author'])
    assert result['verified_review_count'] == 4
    assert result['seeded_critical_recall'] == 1.0
    assert result['pairwise_agreement'] == 1.0
    assert result['coverage']['outputs']['software-engineer:1']['independent_pair_complete']
    assert result['false_positive_rate'] is None
    assert not result['professional_approval'] and not result['production_ready']
    assert result['human_gold'] is False


def test_names_forged_scores_self_review_and_wrong_domain_do_not_establish_coverage():
    bundle = adjudication.prepare_adjudication(ROOT, ['software-engineer:1'], ['medium'])
    records, verifier, assignments = reviews_for(bundle)
    assert adjudication.assess_adjudication(bundle, records)['verified_review_count'] == 0
    forged = copy.deepcopy(records)
    forged[0]['criteria'][0]['score'] = 4
    result = adjudication.assess_adjudication(bundle, forged, verifier, assignments,
                                            author_principals=['source-author'])
    assert result['verified_review_count'] == 3
    assert result['rejected_reviews']
    result = adjudication.assess_adjudication(bundle, records, verifier, {'reviewer-a': [4], 'reviewer-b': [4]})
    assert result['verified_review_count'] == 0
    result = adjudication.assess_adjudication(bundle, records, verifier, assignments,
                                            author_principals=['reviewer-a'])
    assert result['verified_review_count'] == 2
    unknown_authors = adjudication.assess_adjudication(bundle, records, verifier, assignments)
    assert unknown_authors['verified_review_count'] == 0
    assert unknown_authors['status'] == 'PENDING_INDEPENDENT_REVIEW'
    assert any('AUTHORSHIP_UNVERIFIED' in review['reason'] for review in unknown_authors['rejected_reviews'])


def test_malformed_review_does_not_abort_other_independent_observations():
    bundle = adjudication.prepare_adjudication(ROOT, ['software-engineer:1'], ['medium'])
    records, verifier, assignments = reviews_for(bundle)
    malformed = [{'case_id': []}, {'case_id': records[0]['case_id'], 'criteria': [{'criterion': []}] * 9},
                 {'case_id': records[0]['case_id'], 'findings': [{'criterion': [], 'severity': 'critical'}]}]
    result = adjudication.assess_adjudication(
        bundle, malformed + records, verifier, assignments, author_principals=['source-author'])
    assert result['verified_review_count'] == 4
    assert len(result['rejected_reviews']) == 3


def test_recall_counts_the_seeded_professional_criterion_not_an_unrelated_critical_finding():
    bundle = adjudication.prepare_adjudication(ROOT, ['software-engineer:1'], ['medium'])
    records, verifier, assignments = reviews_for(bundle)
    host = verifier.__self__
    for record in records:
        if record['findings']:
            record['findings'][0]['criterion'] = 'C5'
            subject = {key: value for key, value in record.items() if key != 'attestation'}
            host[record['attestation']]['subject_digest'] = canonical_hash(subject)
    result = adjudication.assess_adjudication(
        bundle, records, verifier, assignments, author_principals=['source-author'])
    assert result['verified_review_count'] == 4
    assert result['seeded_critical_recall'] == 0.0


def test_changed_packet_and_coordinator_binding_are_rejected():
    bundle = adjudication.prepare_adjudication(ROOT, ['software-engineer:1'], ['medium'])
    broken = copy.deepcopy(bundle)
    broken['reviewer_packet']['cases'][0]['complexity'] = 'complex'
    with pytest.raises(ValueError, match='PACKET'):
        adjudication.assess_adjudication(broken, [])
    broken = copy.deepcopy(bundle)
    broken['coordinator']['packet_hash'] = '0' * 64
    with pytest.raises(ValueError, match='COORDINATOR'):
        adjudication.assess_adjudication(broken, [])
    broken = copy.deepcopy(bundle)
    answer = broken['coordinator']['cases'][0]
    answer['seed_class'] = 'seeded-defect' if answer['seed_class'] == 'reference' else 'reference'
    answer['expected_criterion'] = 'C1' if answer['seed_class'] == 'seeded-defect' else None
    broken['coordinator']['coordinator_hash'] = canonical_hash(
        {k: v for k, v in broken['coordinator'].items() if k != 'coordinator_hash'})
    with pytest.raises(ValueError, match='COORDINATOR'):
        adjudication.assess_adjudication(broken, [])


def test_cli_prepares_separate_blind_and_coordinator_files_and_refuses_overwrite(tmp_path, capsys):
    import json
    from content_eval import main
    packet = tmp_path / 'reviewer.json'
    key = tmp_path / 'coordinator.json'
    args = ['prepare-adjudication', '--root', str(ROOT), '--contract', 'software-engineer:1',
            '--complexity', 'medium', '--output', str(packet), '--coordinator-output', str(key)]
    assert main(args) == 0
    assert 'seed_class' not in packet.read_text()
    assert 'seed_class' in key.read_text()
    original = packet.read_bytes()
    with pytest.raises(SystemExit):
        main(args)
    assert packet.read_bytes() == original
    reviews = tmp_path / 'reviews.json'
    reviews.write_text('[]')
    output = tmp_path / 'measurement.json'
    assert main(['assess-adjudication', '--packet', str(packet), '--coordinator', str(key),
                 '--reviews', str(reviews), '--output', str(output)]) == 1
    result = json.loads(output.read_text())
    assert result['status'] == 'PENDING_INDEPENDENT_REVIEW'
    assert result['verified_review_count'] == 0
    assert not result['professional_approval']


def test_existing_native_domain_verifier_supplies_review_identity_without_new_authority(tmp_path, monkeypatch):
    from test_governed_domain import _fixture, _qualified
    from governed_domain import GovernedDomain
    bundle = adjudication.prepare_adjudication(ROOT, ['software-engineer:1'], ['medium'])
    case = bundle['reviewer_packet']['cases'][0]
    host = _fixture(tmp_path, monkeypatch)
    def source(actor, token, manifest):
        return {'case_id': case['case_id'],
                'content': bundle['reviewer_packet']['materials'][case['material_hash']],
                'producer': {'attestation': token, 'context_manifest': manifest}}
    def review(model, token, manifest):
        return {'attestation': token, 'context_manifest': manifest,
                'reviewed_digest': case['material_hash'],
                'packet_hash': bundle['reviewer_packet']['packet_hash'],
                'case_id': case['case_id'], 'material_hash': case['material_hash'],
                'compiled_spec_hash': case['compiled_spec_hash'], 'verdict': 'INSUFFICIENT_EVIDENCE',
                'criteria': [{'criterion': criterion, 'score': 2,
                              'rationale': 'Controlled native captured fixture judgement.',
                              'evidence': 'Synthetic teaching material; no professional approval.'}
                             for criterion in adjudication.RUBRIC], 'findings': []}
    subject, producer_token, _, review_token, observation = _qualified(
        host, 'adjudication-case', model_factory=source, review_factory=review)
    adapter = GovernedDomain(host.store, [{'ref': subject, 'use_scope': host.scope}])
    actual = adapter.verify(review_token)
    producer = adapter.verify(producer_token)
    assert actual and producer and actual['principal'] != producer['principal']
    result = adjudication.assess_adjudication(
        bundle, [observation], adapter, {actual['principal']: [5]},
        author_principals=[producer['principal']])
    assert result['verified_review_count'] == 1
    assert result['status'] == 'PENDING_INDEPENDENT_REVIEW'
    assert not result['professional_approval'] and not result['production_ready']
