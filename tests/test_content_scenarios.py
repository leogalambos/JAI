# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exercise deterministic multistep delivery and rejection without providers."""
import copy
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))


def test_resolved_semantic_family_is_inside_the_compiled_hash():
    from content_spec import ContentSpec
    from content_lint import _compiled_hash
    engine = ContentSpec(ROOT)
    for contract in ('business-relationship-manager:2', 'enterprise-applications-architect:2'):
        resolved = engine.resolve(contract)
        assert _compiled_hash(resolved) == resolved['compiled_spec_hash']
        altered = copy.deepcopy(resolved)
        altered['semantic_family'] = 'unregistered-family'
        assert _compiled_hash(altered) != resolved['compiled_spec_hash']


def test_seven_scenarios_execute_real_checks_and_end_at_external_authority():
    from content_scenarios import run_scenarios, verify_result
    report = run_scenarios(ROOT)
    assert report['status'] == 'PASS'
    assert report['scenario_count'] == 7
    assert report['qualification_class'] == 'synthetic-regression'
    assert report['live_provider_calls'] == 0
    assert not report['production_release_authorized']
    assert not report['professional_approval']
    assert verify_result(report) == []
    for case in report['scenarios']:
        assert case['status'] == 'PASS', case['scenario_id']
        assert len(case['trace']) >= 6
        assert case['trace'][-1]['acceptance'] == 'EXPECTED_L0_ESCALATION'
        assert all(case['negative_checks'].values())
        assert set(case['negative_checks']) == {
            'forged_receiver_rejected', 'self_review_rejected',
            'changed_snapshot_rejected', 'empty_source_rejected',
            'orphan_handoff_rejected', 'rollback_preserves_original',
            'unassigned_receiver_rejected', 'human_approval_not_fabricated',
        }


def test_unknown_scenario_is_an_error_not_a_zero_case_pass():
    from content_scenarios import run_scenarios
    with pytest.raises(ValueError, match='UNKNOWN_SCENARIO'):
        run_scenarios(ROOT, ['not-a-registered-scenario'])
    with pytest.raises(ValueError, match='EMPTY_SCENARIO_SELECTION'):
        run_scenarios(ROOT, [])


def test_report_hash_and_chained_handoff_identity_detect_rehashed_tamper():
    from content_scenarios import run_scenarios, verify_result
    from content_spec import canonical_hash
    report = run_scenarios(ROOT, ['cloud-migration'])
    broken = copy.deepcopy(report)
    broken['scenarios'][0]['trace'][1]['previous_record_hash'] = '0' * 64
    broken['report_hash'] = canonical_hash({k: v for k, v in broken.items() if k != 'report_hash'})
    assert 'TRACE_CHAIN_INVALID' in verify_result(broken)
    broken = copy.deepcopy(report)
    broken['live_provider_calls'] = 1
    assert 'REPORT_HASH_MISMATCH' in verify_result(broken)


def test_cli_output_is_immutable_and_never_invokes_a_provider(tmp_path, capsys, monkeypatch):
    from content_scenarios import main
    import subprocess
    def forbidden(*args, **kwargs):
        raise AssertionError('Scenario execution must not launch external processes.')
    monkeypatch.setattr(subprocess, 'run', forbidden)
    output = tmp_path / 'scenario.json'
    args = ['run', '--root', str(ROOT), '--scenario', 'application-delivery', '--output', str(output)]
    assert main(args) == 0
    original = output.read_bytes()
    assert main(args) == 1
    assert output.read_bytes() == original
    assert 'private' not in capsys.readouterr().out.lower()
