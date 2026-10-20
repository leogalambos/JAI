# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Missing mandatory execution dependencies are explicit non-passing states."""
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import qualification_core as qualification


def test_missing_executable_is_not_executed_and_never_passes():
    result = qualification.command('fixture dependency', ['jai-unavailable-fixture-executable'])
    assert not result['ok']
    assert result['state'] == 'NOT_EXECUTED'
    assert 'jai-unavailable' not in result['detail']


def test_missing_renderer_does_not_execute_or_pass():
    with patch.object(qualification.shutil, 'which', return_value=None), patch.object(
            qualification, 'run_offline', side_effect=AssertionError('unavailable renderer')):
        result = qualification.publication_renderer_check()
    assert not result['ok']
    assert result['state'] == 'NOT_EXECUTED'
    assert 'LibreOffice' in result['detail']


def test_renderer_presence_still_requires_successful_execution():
    with patch.object(qualification.shutil, 'which', return_value='/fake/renderer'), patch.object(
            qualification, 'run_offline', return_value={'status':'FAIL', 'returncode':1, 'stdout':'fixture failure', 'stderr':''}):
        result = qualification.publication_renderer_check()
    assert not result['ok']
    assert result['state'] == 'FAIL'


def test_offline_timeout_remains_failed_without_direct_subprocess_fallback():
    with patch.object(qualification, 'run_offline', return_value={
            'status':'FAIL', 'returncode':124, 'stdout':'', 'stderr':'', 'reason':'OFFLINE_TIMEOUT'}):
        result = qualification.command('timeout fixture', ['fixture'], timeout=1)
    assert not result['ok']
    assert result['state'] == 'FAIL'
    assert 'TIMEOUT' in result['detail']
    assert result['timeout_seconds'] == 1
    assert result['duration_seconds'] >= 0


def test_success_state_requires_executed_zero_exit():
    result = qualification.command('deterministic fixture', [sys.executable, '-c', 'print("done")'])
    assert result['ok']
    assert result['state'] == 'PASS'


def test_ci_runs_new_regressions_and_qualification_under_offline_guard():
    import yaml
    required = {'test_expert_references.py', 'test_optional_provider_eval.py',
                'test_evaluation_package.py', 'test_content_scenarios.py',
                'test_offline_guard.py', 'test_qualification_dependencies.py',
                'test_qualification_core.py', 'test_release_ga.py', 'test_release_bundle.py',
                'test_reference_bindings.py', 'test_commercial_proposal.py'}
    assert required <= set(qualification.REGRESSION_MODULES)
    for filename, jobs in [('release.yml', ('qualification',)),
                           ('validate-library.yml', ('release-preflight',))]:
        document = yaml.safe_load((ROOT / '.github/workflows' / filename).read_text())
        for name in jobs:
            job = document['jobs'][name]
            assert job['timeout-minutes'] == 360
            runs = [step.get('run', '') for step in job['steps']]
            assert not any('qualification_core.py regression' in run for run in runs)
            assert not any('unittest discover' in run for run in runs)
            qualification_run = next(run for run in runs if 'release_ga.py qualify' in run)
            assert 'qualification_core.py budget --scope qualification' in qualification_run
            assert 'offline_guard.py run --stream --root . --timeout "$qualification_budget" -- python3 -u .ai/runtime/tools/release_ga.py qualify' in qualification_run
            assert any('ci_test_plan.py supplementary' in run and 'offline_guard.py run' in run for run in runs)


def test_standalone_command_always_applies_offline_runner_and_preserves_unavailable():
    with patch.object(qualification, 'run_offline', return_value={
            'status':'NOT_EXECUTED', 'returncode':77, 'stdout':'', 'stderr':'',
            'reason':'OS_NETWORK_DENIAL_UNAVAILABLE'}) as runner:
        result = qualification.command('guard fixture', [sys.executable, '-c', 'pass'], timeout=4)
    runner.assert_called_once_with([sys.executable, '-c', 'pass'], qualification.PACKAGE, timeout=4)
    assert not result['ok']
    assert result['state'] == 'NOT_EXECUTED'
