# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Prove process-tree network denial and explicit provider-call rejection."""
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))


def test_python_audit_allows_local_ipc_and_rejects_network_and_real_provider(monkeypatch):
    from offline_guard import install_python_audit
    hooks = []
    monkeypatch.setattr(sys, 'addaudithook', hooks.append)
    install_python_audit()
    audit = hooks[0]
    audit('socket.__new__', (None, 1, 1, 0))
    audit('subprocess.Popen', ('fake-provider', ['fake-provider'], None, {}))
    with pytest.raises(PermissionError):
        audit('socket.__new__', (None, 2, 1, 0))
    with pytest.raises(RuntimeError, match='OFFLINE_PROVIDER_EXECUTION_DENIED'):
        audit('subprocess.Popen', ('codex', ['codex', 'exec'], None, {}))


def test_static_scan_rejects_direct_and_shell_hidden_provider_calls(tmp_path):
    from offline_guard import scan_sources
    tests = tmp_path / 'tests'
    tests.mkdir()
    (tests / 'test_bad.py').write_text("import subprocess\nsubprocess.run(['codex', 'exec', 'hello'])\n")
    (tests / 'test_shell.py').write_text("import subprocess\nsubprocess.run('claude -p hello', shell=True)\n")
    (tests / 'test_good.py').write_text("provider = 'codex'\n# A provider selector is not a CLI invocation.\n")
    findings = scan_sources(tmp_path)
    assert {item['path'] for item in findings} == {'tests/test_bad.py', 'tests/test_shell.py'}
    assert all(item['rule'] == 'MANDATORY_LIVE_PROVIDER_CALL' for item in findings)


def test_network_denial_is_inherited_by_non_python_children(tmp_path):
    from offline_guard import run_offline
    script = tmp_path / 'network_probe.py'
    script.write_text("import errno,socket\ntry:\n socket.socket(socket.AF_INET,socket.SOCK_STREAM)\nexcept OSError as e:\n assert e.errno == errno.EPERM\n print('NETWORK_DENIED')\nelse:\n raise SystemExit(9)\n")
    # Isolated Python ignores sitecustomize; success proves the kernel filter,
    # rather than only a Python monkeypatch, denies networking in descendants.
    result = run_offline([sys.executable, '-I', str(script)], ROOT)
    if result['status'] == 'NOT_EXECUTED':
        assert result['reason'] == 'OS_NETWORK_DENIAL_UNAVAILABLE'
        assert result['returncode'] != 0
    else:
        assert result['status'] == 'PASS', result
        assert result['network_control'] == 'linux-seccomp-inherited'
        assert 'NETWORK_DENIED' in result['stdout']


def test_live_provider_is_rejected_without_looking_up_or_executing_it():
    from offline_guard import run_offline
    result = run_offline(['codex', 'exec', 'never run this'], ROOT)
    assert result['status'] == 'FAIL'
    assert result['reason'] == 'LIVE_PROVIDER_FORBIDDEN'


def test_shell_chains_cannot_hide_provider_after_a_benign_command(monkeypatch):
    from offline_guard import run_offline
    import subprocess
    def must_not_spawn(*args, **kwargs):
        raise AssertionError('Forbidden provider command must be rejected before process creation.')
    monkeypatch.setattr(subprocess, 'Popen', must_not_spawn)
    for command in ('echo harmless; codex exec forbidden', 'echo harmless && claude -p forbidden', 'echo $(codex exec forbidden)'):
        result = run_offline(['/bin/sh', '-c', command], ROOT)
        assert result['reason'] == 'LIVE_PROVIDER_FORBIDDEN'


def test_guard_timeout_is_nonpassing_and_terminates_process_group():
    from offline_guard import run_offline
    result = run_offline([sys.executable, '-I', '-c', 'while True: pass'], ROOT, timeout=.2)
    assert result['status'] in ('FAIL', 'NOT_EXECUTED')
    assert result['reason'] in ('OFFLINE_TIMEOUT', 'OS_NETWORK_DENIAL_UNAVAILABLE')


def test_missing_execution_is_not_executed_and_invalid_timeouts_are_rejected():
    from offline_guard import run_offline
    result = run_offline(['/nonexistent-jai-offline-executable'], ROOT)
    assert result['status'] == 'NOT_EXECUTED'
    assert result['returncode'] != 0
    for timeout in (True, 0, -1, float('inf'), float('nan')):
        with pytest.raises(ValueError, match='INVALID_OFFLINE'):
            run_offline([sys.executable, '-c', 'pass'], ROOT, timeout=timeout)


def test_guard_does_not_forward_credential_environment_values(monkeypatch):
    from offline_guard import safe_environment
    monkeypatch.setenv('OPENAI_API_KEY', 'synthetic-credential-sentinel')
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'synthetic-credential-sentinel')
    environment = safe_environment(ROOT)
    assert 'OPENAI_API_KEY' not in environment
    assert 'ANTHROPIC_API_KEY' not in environment
    assert 'synthetic-credential-sentinel' not in str(environment)


def test_python_child_audit_blocks_shell_wrapped_provider(tmp_path):
    from offline_guard import run_offline
    script = tmp_path / 'wrapped.py'
    script.write_text("import subprocess\nsubprocess.run('codex exec must-not-run',shell=True,check=True)\n")
    result = run_offline([sys.executable, str(script)], ROOT)
    assert result['status'] in ('FAIL', 'NOT_EXECUTED')
    if result['status'] == 'FAIL':
        assert 'OFFLINE_PROVIDER_EXECUTION_DENIED' in result['stderr']


def test_cli_reports_missing_execution_and_scan_success(tmp_path,capsys):
    from offline_guard import main
    (tmp_path / 'tests').mkdir()
    assert main(['scan', '--root', str(tmp_path)]) == 0
    assert main(['run', '--root', str(ROOT)]) == 1
    assert 'FAIL' in capsys.readouterr().out


def test_timeout_preserves_partial_stdout_and_stderr(monkeypatch):
    import offline_guard
    import subprocess
    class Process:
        pid = 12345
        calls = 0
        def communicate(self, timeout=None):
            self.calls += 1
            if self.calls == 1:
                raise subprocess.TimeoutExpired('fixture', timeout)
            return 'completed test before timeout\n', 'last diagnostic\n'
    process = Process()
    monkeypatch.setattr(offline_guard.subprocess, 'Popen', lambda *a, **k: process)
    monkeypatch.setattr(offline_guard.os, 'killpg', lambda *a: None)
    result = offline_guard.run_offline(['fixture'], ROOT, timeout=1)
    assert result['status'] == 'FAIL' and result['returncode'] == 124
    assert result['stdout'] == 'completed test before timeout\n'
    assert result['stderr'] == 'last diagnostic\n'


def test_cli_accepts_explicit_finite_timeout_without_changing_default(monkeypatch):
    import offline_guard
    calls = []
    def execute(command, root, timeout=900):
        calls.append(timeout)
        return {'stdout': '', 'stderr': '', 'status': 'PASS', 'returncode': 0}
    monkeypatch.setattr(offline_guard, 'run_offline', execute)
    assert offline_guard.main(['run', '--timeout', '13320', '--', 'fixture']) == 0
    assert offline_guard.main(['run', '--', 'fixture']) == 0
    assert calls == [13320, 900]
    for value in ('0', '-1', 'nan', 'inf'):
        with pytest.raises(SystemExit):
            offline_guard.main(['run', '--timeout', value, '--', 'fixture'])
