# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Routine pipelines select semantic controls while publication stays explicit."""
from pathlib import Path
import fnmatch
import shlex

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _workflow(name):
    return yaml.load((ROOT / '.github/workflows' / name).read_text(), Loader=yaml.BaseLoader)


def test_source_validation_uses_one_bounded_python_control_profile():
    workflow = _workflow('validate-library.yml')
    commands = [step['run'] for step in workflow['jobs']['policy']['steps'] if 'run' in step]
    selected = [command for command in commands if 'scripts/run_tests.py' in command]
    assert len(selected) == 1
    tokens = shlex.split(selected[0])
    assert tokens[-5:] == ['scripts/run_tests.py', '--profile', 'control', '--scope', 'python']
    assert 'offline_guard.py' in selected[0]
    assert '--timeout' in tokens
    assert not any('-m pytest' in command for command in commands)
    for path in ('pytest.ini', 'conftest.py', 'ci/**', 'scripts/**', 'tests/**'):
        assert path in workflow['on']['pull_request']['paths']


def test_native_and_desktop_pipelines_use_contract_controls_with_built_verification():
    validation = _workflow('validate-library.yml')
    contracts = '\n'.join(step.get('run', '') for step in
                          validation['jobs']['fabric-explorer-contracts']['steps'])
    assert 'packages/contracts run test:control' in contracts
    assert 'packages/contracts run test:built' in contracts
    desktop = _workflow('fabric-explorer-desktop.yml')
    commands = '\n'.join(step.get('run', '') for step in
                         desktop['jobs']['linux-build-and-read-boundaries']['steps'])
    assert 'desktop run test:control' in commands
    assert 'node --test apps/fabric-explorer/tools/test-selection.test.mjs' in commands
    assert '-m pytest -q -m control apps/fabric-explorer/reader/test' in commands
    assert 'desktop run build:native-smoke' in commands
    assert 'desktop test\n' not in commands
    for event in ('push', 'pull_request'):
        for path in ('apps/fabric-explorer/test-categories.json',
                     'ci/test-catalog.json', 'conftest.py', 'pytest.ini'):
            assert path in desktop['on'][event]['paths']
        for changed in ('apps/fabric-explorer/tools/test-selection.mjs',
                        'apps/fabric-explorer/tools/test-selection.test.mjs'):
            assert any(fnmatch.fnmatchcase(changed, pattern)
                       for pattern in desktop['on'][event]['paths']), changed


def test_manual_platform_qualification_remains_explicit_and_does_not_run_every_push():
    native = _workflow('fabric-explorer-native-readers.yml')
    assert set(native['on']) == {'workflow_dispatch'}
    commands = '\n'.join(step.get('run', '') for step in native['jobs']['native-readers']['steps'])
    assert 'test_windows_readonly.py' in commands
    assert 'Skipped Windows cases on POSIX are not native Windows evidence.' in commands
    release = _workflow('release.yml')
    assert release['on'] == {'push': {'tags': ['release@*']}}
    commands = '\n'.join(step.get('run', '') for step in release['jobs']['validate']['steps'])
    assert 'scripts/run_tests.py' not in commands
    assert '-m pytest' not in commands
