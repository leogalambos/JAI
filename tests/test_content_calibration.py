# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Verify generated observations never imply approved numerical quality gates."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from generate_content_calibration import build


def test_candidates_derive_three_complexities_per_priority_family():
    report = build()
    assert len(report['candidates']) == 10
    assert report['calibration_status'] == 'synthetic-only'
    assert not report['human_gold']
    assert not report['production_ready']
    assert not report['automatically_applied_to_policy']
    for family, candidate in report['candidates'].items():
        samples = candidate['samples']
        assert {sample['complexity'] for sample in samples} == {'simple', 'medium', 'complex'}
        assert len({sample['project_id'] for sample in samples}) == 3
        assert candidate['size_budget']['target'] == [min(sample['observed'] for sample in samples),
                                                    max(sample['observed'] for sample in samples)]
        assert not candidate['size_budget']['minimum_is_quality_gate']
        assert candidate['size_budget']['target_is_informational']
        assert candidate['status'] == 'proposed'
        assert candidate['human_approval_required']
        assert not candidate['production_ready']
        trend = report['trend_examples'][family]
        assert trend['delta']['critical_findings'] < 0
        assert trend['observations'][-1]['gate_verdict'] == 'DRAFT_INCOMPLETE'
        assert not trend['qualification_evidence']
