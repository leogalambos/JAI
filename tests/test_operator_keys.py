# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Confirmed installer key provisioning uses disposable local crypto material."""
import io
import os
import shlex
import shutil
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import operator_keys as keys


@pytest.fixture
def host_key(tmp_path, monkeypatch):
    target = tmp_path / 'operator/private.pem'
    monkeypatch.setattr(keys, 'default_private_key', lambda: target)
    monkeypatch.setattr(keys.sys, 'stdin', io.StringIO())
    monkeypatch.setattr(keys.sys.stdin, 'isatty', lambda: True)
    return target


def test_default_private_key_is_only_a_locator(tmp_path, monkeypatch):
    monkeypatch.setattr(keys.Path, 'home', lambda: tmp_path / 'home with spaces')
    assert keys.default_private_key() == tmp_path / 'home with spaces/.local/share/jai-operator/private.pem'
    assert not (tmp_path / 'home with spaces').exists()


def test_confirmed_generation_and_explicit_replacement_preserve_private_backup(host_key, monkeypatch, capsys):
    answers = iter(['', 'yes'])
    prompts = []
    def answer(prompt):
        prompts.append(prompt)
        return next(answers)
    monkeypatch.setattr('builtins.input', answer)
    first = keys.provision_operator_key()
    original = host_key.read_bytes()
    assert first['status'] == 'created' and '[Y/n]' in prompts[0]
    assert host_key.stat().st_mode & 0o777 == 0o600
    assert host_key.parent.stat().st_mode & 0o777 == 0o700
    checked = subprocess.run([shutil.which('openssl'), 'pkey', '-in', str(host_key), '-pubout'],
                             capture_output=True, check=True)
    assert checked.stdout.startswith(b'-----BEGIN PUBLIC KEY-----')
    previous = host_key.stat()
    assert keys.provision_operator_key()['status'] == 'existing'
    assert (host_key.read_bytes(), host_key.stat().st_mtime_ns) == (original, previous.st_mtime_ns)
    second = keys.provision_operator_key(force=True)
    backup = Path(second['backup'])
    assert second['status'] == 'replaced' and host_key.read_bytes() != original
    assert backup.read_bytes() == original and backup.stat().st_mode & 0o777 == 0o600
    assert 'already exists' in capsys.readouterr().out
    assert len(prompts) == 2


@pytest.mark.parametrize('mode', ['decline', 'eof', 'no-terminal', 'dry-run'])
def test_unconfirmed_or_preview_setup_never_creates_key(host_key, monkeypatch, mode, capsys):
    def answer(prompt):
        if mode == 'eof':
            raise EOFError
        if mode in {'no-terminal', 'dry-run'}:
            pytest.fail('noninteractive and dry-run setup must not prompt')
        return 'n'
    monkeypatch.setattr('builtins.input', answer)
    monkeypatch.setattr(keys.sys.stdin, 'isatty', lambda: mode != 'no-terminal')
    result = keys.provision_operator_key(dry_run=mode == 'dry-run')
    assert result['status'] in {'declined', 'unavailable', 'dry-run'}
    assert not host_key.parent.exists()
    if mode == 'no-terminal':
        assert 'not created' in capsys.readouterr().out


def test_forced_generation_failure_preserves_original_and_cleans_staging(host_key, monkeypatch):
    host_key.parent.mkdir()
    host_key.write_bytes(b'disposable prior key fixture')
    original = host_key.read_bytes()
    monkeypatch.setattr('builtins.input', lambda prompt: 'Y')
    monkeypatch.setattr(keys.subprocess, 'run', lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 1))
    with pytest.raises(ValueError, match='generation failed'):
        keys.provision_operator_key(force=True)
    assert host_key.read_bytes() == original
    assert list(host_key.parent.iterdir()) == [host_key]


def test_force_still_requires_confirmation_and_backup_failure_preserves_key(host_key, monkeypatch):
    host_key.parent.mkdir()
    host_key.write_bytes(b'disposable prior key fixture')
    monkeypatch.setattr('builtins.input', lambda prompt: 'n')
    assert keys.provision_operator_key(force=True)['status'] == 'declined'
    original = host_key.read_bytes()
    monkeypatch.setattr('builtins.input', lambda prompt: '')
    def unavailable_backup(*args, **kwargs):
        raise OSError('synthetic backup unavailable')
    monkeypatch.setattr(keys.shutil, 'copyfileobj', unavailable_backup)
    with pytest.raises(OSError, match='backup unavailable'):
        keys.provision_operator_key(force=True)
    assert host_key.read_bytes() == original
    assert not list(host_key.parent.glob('.private-*'))


@pytest.mark.parametrize('candidate', ['missing', 'not-executable'])
def test_missing_openssl_never_creates_key_directory(host_key, monkeypatch, tmp_path, candidate):
    tools = tmp_path / 'unavailable tools'
    tools.mkdir()
    if candidate == 'not-executable':
        (tools / 'openssl').write_text('not an executable')
    monkeypatch.setenv('PATH', str(tools))
    monkeypatch.setattr('builtins.input', lambda prompt: 'yes')
    with pytest.raises(ValueError, match='OpenSSL.*PATH'):
        keys.openssl_executable()
    with pytest.raises(ValueError, match='OpenSSL.*PATH'):
        keys.provision_operator_key()
    assert not host_key.parent.exists()
    assert keys.default_private_key() == host_key
    assert keys.provision_operator_key(dry_run=True)['status'] == 'dry-run'
    host_key.parent.mkdir()
    host_key.write_bytes(b'disposable existing key')
    prior = host_key.stat()
    assert keys.provision_operator_key()['status'] == 'existing'
    with pytest.raises(ValueError, match='OpenSSL.*PATH'):
        keys.provision_operator_key(force=True)
    assert host_key.read_bytes() == b'disposable existing key'
    assert host_key.stat().st_mtime_ns == prior.st_mtime_ns
    assert list(host_key.parent.iterdir()) == [host_key]


def test_generation_and_export_select_inherited_path_without_crypto_environment_leak(host_key, monkeypatch, tmp_path, capsys):
    real = shutil.which('openssl')
    assert real, 'OpenSSL is required for disposable crypto integration tests'
    tools = tmp_path / 'host tools with spaces'
    tools.mkdir()
    selected = tools / 'openssl'
    selected.symlink_to(real)
    monkeypatch.setenv('PATH', str(tools))
    assert keys.openssl_executable() == str(selected)
    monkeypatch.setenv('OPENSSL_CONF', str(tmp_path / 'untrusted configuration'))
    monkeypatch.setattr('builtins.input', lambda prompt: 'yes')
    run = subprocess.run
    calls = []
    def observed(command, **kwargs):
        calls.append((command, kwargs))
        assert command[0] == str(selected)
        assert kwargs['env']['OPENSSL_CONF'] == '/dev/null'
        return run(command, **kwargs)
    monkeypatch.setattr(keys.subprocess, 'run', observed)
    assert keys.provision_operator_key()['status'] == 'created'
    assert len(calls) == 1
    assert os.environ['PATH'] == str(tools)
    exported = shlex.split(capsys.readouterr().out.strip().splitlines()[-1])
    assert exported == [str(selected), 'pkey', '-in', str(host_key), '-pubout']
    assert run(exported, capture_output=True, check=True, env=calls[0][1]['env']).stdout.startswith(b'-----BEGIN PUBLIC KEY-----')


def test_openssl_lookup_absolutizes_relative_path_and_remains_lazy(tmp_path, monkeypatch):
    import importlib.util
    tools = tmp_path / 'relative tools'
    tools.mkdir()
    executable = tools / 'openssl'
    executable.write_text('#!/bin/sh\nexit 0\n')
    executable.chmod(0o755)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv('PATH', tools.name)
    assert keys.openssl_executable() == str(executable)
    monkeypatch.setenv('PATH', str(tmp_path / 'no tools'))
    spec = importlib.util.spec_from_file_location('isolated_operator_keys', keys.__file__)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.default_private_key().name == 'private.pem'
    with pytest.raises(ValueError, match='OpenSSL.*PATH'):
        module.openssl_executable()
