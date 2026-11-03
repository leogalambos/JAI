# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Retained projection utility contracts, including negative coverage decisions."""
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import projection


def test_load_preserves_utf8_and_null_and_reports_unreadable_or_malformed_json(tmp_path):
    source = tmp_path / 'source.json'
    value = {'title': 'Café recovery plan', 'items': [None, True, 0.25]}
    source.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
    assert projection.load(source) == value
    source.write_text('null', encoding='utf-8')
    assert projection.load(source) is None
    source.write_text('{invalid JSON', encoding='utf-8')
    with pytest.raises(json.JSONDecodeError):
        projection.load(source)
    with pytest.raises(FileNotFoundError):
        projection.load(tmp_path / 'missing.json')


def test_evidence_refs_normalizes_and_deduplicates_global_and_claim_references():
    model = {'evidence': ['source:contract-1', 'E2', {'id': 'E1'}, {'id': 'E2'}],
             'claims': [{'evidence': ['E1', {'id': 'E3'}, {'id': 'source:contract-1'}]}]}
    assert projection.evidence_refs(model) == [
        'evidence:E1', 'evidence:E2', 'evidence:E3', 'source:contract-1']
    assert projection.evidence_refs({}) == []
    assert projection.evidence_refs({'evidence': [], 'claims': []}) == []
    assert projection.evidence_refs({'evidence': [{'locator': 'page:1'}, {'id': ''}, {'id': None}],
                                     'claims': [{'evidence': [{}]}]}) == []


def test_jai_lineage_preserves_overrides_and_generates_deterministic_identifiers():
    digest = 'a' * 64
    profile = {'id': 'decision-paper'}
    defaults = projection.jai_lineage({'artifact_id': 'RECOVERY-1'}, profile, digest)
    assert defaults == {
        'intent_ref': 'intent:RECOVERY-1',
        'semantic_snapshot_ref': 'semantic-snapshot:sha256:' + digest,
        'policy_ref': 'policy:publication:decision-paper',
        'design_ref': 'publication-design:decision-paper',
        'realisation_ref': 'renderer:tools/publication.py@' + projection.RELEASE,
        'evidence_refs': []}
    assert projection.jai_lineage({'artifact_id': 'RECOVERY-1'}, dict(profile), digest) == defaults
    supplied = {'intent_ref': 'intent:original', 'semantic_snapshot_ref': 'snapshot:original',
                'policy_ref': 'policy:original', 'design_ref': 'design:original',
                'realisation_ref': 'renderer:original', 'evidence_refs': ['evidence:E2', 'note:policy']}
    model = {'jai': supplied, 'evidence': ['E1', 'E2']}
    assert projection.jai_lineage(model, profile, digest) == dict(
        supplied, evidence_refs=['evidence:E1', 'evidence:E2', 'note:policy'])
    assert projection.jai_lineage({'jai': None}, profile, digest)['intent_ref'] == 'intent:UNKNOWN'
    with pytest.raises(KeyError, match='id'):
        projection.jai_lineage({}, {}, digest)


def test_section_content_requires_actual_body_bullets_rows_or_diagram_labels():
    assert not projection.section_has_content({})
    assert not projection.section_has_content({'heading': 'Context', 'table': {'headers': ['Criterion']}})
    assert not projection.section_has_content({'body': ' \n', 'bullets': [' ', ''],
        'table': {'headers': ['Criterion'], 'rows': [['', ' ']]},
        'diagram': {'nodes': [{'id': 'service', 'label': ' '}]}})
    assert projection.section_has_content({'body': 'Recovery applies to the inventory service.'})
    assert projection.section_has_content({'bullets': ['', 'State the remaining uncertainty.']})
    assert projection.section_has_content({'table': {'headers': ['Retries'], 'rows': [[0]]}})
    assert projection.section_has_content({'diagram': {'nodes': [{'id': 'service', 'label': 'Inventory'}]}})
    assert not projection.section_has_content({'diagram': {'nodes': [{'id': 'service'}]}})


def test_self_test_runs_actual_positive_and_negative_projection_checks(capsys):
    assert projection.self_test() == 0
    assert capsys.readouterr().out.splitlines() == [
        'PASS good-coverage', 'PASS hashes', 'PASS jai-lineage',
        'PASS schema-and-policy-valid', 'PASS bad-fails', 'PASS omissions-recorded',
        '6/6 PASS']
