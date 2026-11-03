# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Native probes must observe real denial, rather than declare confinement."""
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import governed_probe


def test_governed_record_probe_checks_real_immutable_identity_and_missing_proof_denial():
    assert governed_probe.governed_record_probe()


def test_maintained_policy_probe_cli_reports_actual_read_only_check():
    result = subprocess.run([sys.executable, governed_probe.__file__],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == 'Governed identity and missing human-proof probe: PASS'


def test_probe_detects_a_verifier_that_reports_missing_proof_success(monkeypatch):
    monkeypatch.setattr(governed_probe.lifecycle, '_verify_human',
                        lambda *args, **kwargs: None)
    assert not governed_probe.governed_record_probe()


def test_probe_detects_a_changed_record_identity_contract(monkeypatch):
    original = governed_probe.lifecycle.record_manifest

    def changed_identity(engagement, scope, logical_id, kind, record):
        manifest = original(engagement, scope, logical_id, kind, record)
        manifest['logical_id'] += '-altered-identity'
        return manifest

    monkeypatch.setattr(governed_probe.lifecycle, 'record_manifest', changed_identity)
    assert not governed_probe.governed_record_probe()
