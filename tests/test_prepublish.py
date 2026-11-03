# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Local prepublication entry preserves the complete pytest selection and result."""
import importlib.util
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('tested_prepublish', ROOT / 'scripts/prepublish.py')
prepublish = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prepublish)


def test_pytest_command_selects_the_complete_maintained_directory_even_when_empty(tmp_path):
    (tmp_path / 'tests').mkdir()
    command = prepublish.pytest_command(tmp_path)
    assert command == [sys.executable, '-u', '-m', 'pytest', '-vv', '-x',
                       '--tb=short', '--durations=20', 'tests']
    with pytest.raises(ValueError, match='tests directory is missing'):
        prepublish.pytest_command(tmp_path / 'unavailable')


@pytest.mark.parametrize('status', [0, 1, 5])
def test_main_preserves_test_status_and_uses_checkout_without_changing_selection(tmp_path, monkeypatch, status):
    root = tmp_path / 'checkout with spaces'
    (root / 'tests').mkdir(parents=True)
    observed = []
    def run(command, *, cwd):
        observed.append((command, cwd))
        return subprocess.CompletedProcess(command, status)
    monkeypatch.setattr(prepublish.subprocess, 'run', run)
    assert prepublish.main(['--root', str(root)]) == status
    assert observed == [(prepublish.pytest_command(root), root)]


def test_real_local_entry_reports_first_failure_and_does_not_publish(tmp_path):
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'tests/test_sample.py').write_text(
        'def test_first():\n    assert True\n'
        'def test_failure():\n    assert False\n'
        'def test_not_reached():\n    raise AssertionError("should stop earlier")\n')
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/prepublish.py'),
                             '--root', str(tmp_path)], capture_output=True, text=True)
    assert result.returncode == 1
    assert 'test_first PASSED' in result.stdout
    assert 'test_failure FAILED' in result.stdout
    assert 'test_not_reached FAILED' not in result.stdout
    assert not (tmp_path / 'dist').exists()
