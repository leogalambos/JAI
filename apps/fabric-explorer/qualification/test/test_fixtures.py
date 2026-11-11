# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Actual owned filesystem/ACL fixture tests; no product or GUI qualification is inferred."""
import importlib.util
import json
import os
from pathlib import Path
import sys

import pytest

MODULE = Path(__file__).resolve().parents[1] / 'fixtures.py'
SPEC = importlib.util.spec_from_file_location('security_fixtures', MODULE)
fixtures = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fixtures)
ROOT = Path(__file__).resolve().parents[4]
PYTHON = ROOT / 'build/fabric-explorer/helper-venv/bin/python'


@pytest.fixture
def prepared(tmp_path):
    """Create real canonical data and restore only owned permissions after each test."""
    path = fixtures.prepare_fixture(tmp_path, PYTHON, Path('/usr/bin/true'), ROOT / 'apps/fabric-explorer/desktop')
    manifest = fixtures.load_manifest(path)
    yield path, manifest
    fixtures.restore_fixture(manifest)


def test_real_acl_preparation_proves_denials_and_read_integrity(prepared):
    path, manifest = prepared
    assert path.name == 'security-input.json'
    assert str(PYTHON) not in manifest['trustedExecutables']
    assert str(PYTHON.resolve()) not in manifest['trustedExecutables']
    assert {probe['operation'] for probe in manifest['negativeWriteProbes']} == {'file-write', 'directory-create', 'source-rename', 'source-unlink'}
    assert all(probe['denied'] and probe['errno'] == 13 for probe in manifest['negativeWriteProbes'])
    assert fixtures.check_fixture(manifest)['unchanged']
    rows = fixtures.snapshot_source(Path(manifest['sourceRoot']))
    assert rows == manifest['sourceSnapshotBefore']
    assert any(row['kind'] == 'file' and '.blobs/' in row['path'] for row in rows)
    with pytest.raises(FileExistsError):
        fixtures.prepare_fixture(path.parent, PYTHON, Path('/usr/bin/true'), ROOT)


def test_empty_snapshot_and_nonregular_or_linked_entries(tmp_path):
    assert fixtures.snapshot_source(tmp_path)[0]['path'] == '.'
    target = tmp_path / 'record'
    target.write_bytes(b'synthetic')
    for kind in ('symlink', 'hardlink', 'fifo'):
        bad = tmp_path / 'bad'
        if kind == 'symlink':
            bad.symlink_to(target)
        elif kind == 'hardlink':
            os.link(target, bad)
        else:
            os.mkfifo(bad)
        with pytest.raises(ValueError):
            fixtures.snapshot_source(tmp_path)
        bad.unlink()
    with pytest.raises(ValueError):
        fixtures.snapshot_source(target)


def test_manifest_schema_and_owned_root_checks(prepared, tmp_path):
    path, manifest = prepared
    original = path.read_text()
    for replacement in ({**manifest, 'sourceRoot': '/outside'}, {**manifest, 'extra': True}):
        path.write_text(json.dumps(replacement))
        with pytest.raises(ValueError):
            fixtures.load_manifest(path)
    path.write_text(original)
    alias = path.parent / 'alias.json'
    alias.symlink_to(path)
    with pytest.raises(ValueError):
        fixtures.load_manifest(alias)


def test_check_cli_and_restore_do_not_delete_sources(prepared, monkeypatch):
    path, manifest = prepared
    output = path.parent / 'integrity.json'
    monkeypatch.setattr(sys, 'argv', ['fixtures.py', 'check', '--manifest', str(path), '--output', str(output)])
    assert fixtures.main() == 0
    assert json.loads(output.read_text())['unchanged']
    before = {row['path'] for row in manifest['sourceSnapshotBefore']}
    fixtures.restore_fixture(manifest)
    assert {row['path'] for row in fixtures.snapshot_source(Path(manifest['sourceRoot']))} == before
    assert not fixtures.check_fixture(manifest)['unchanged']  # Explicit driver mode restoration is outside the product interval.


def test_restore_refuses_a_replaced_owned_entry(prepared):
    _path, manifest = prepared
    fixtures.restore_fixture(manifest)
    journal = Path(manifest['fabric'])
    original = journal.with_name('original-retained')
    journal.rename(original)
    journal.write_bytes(b'replacement')
    try:
        with pytest.raises(ValueError):
            fixtures.restore_fixture(manifest)
    finally:
        journal.unlink()
        original.rename(journal)


def test_native_runtime_sidecar_is_separate_and_preserves_observed_owners(prepared):
    path, manifest = prepared
    sidecar = json.loads((path.parent / 'native-runtime-identities.json').read_text())
    assert sidecar['format'] == 'jai.fabric-explorer.native-runtime-identities/1'
    true = next(row for row in sidecar['executables'] if row['path'] == '/usr/bin/true')
    assert true['status'] == 'observed'
    assert true['lstat']['uid'] == str(Path('/usr/bin/true').lstat().st_uid)
    assert len(true['resolved']['sha256']) == 64
    assert '/usr/bin/bwrap' not in manifest['trustedExecutables']
    assert fixtures.check_fixture(manifest)['runtimeIdentities']['unchanged']


def test_native_identity_missing_symlink_and_config_bounds(tmp_path, monkeypatch):
    executable = tmp_path / 'executable'
    executable.write_bytes(b'fixed synthetic executable')
    alias = tmp_path / 'alias'
    alias.symlink_to(executable)
    config = tmp_path / 'configs'
    monkeypatch.setattr(fixtures, 'NATIVE_EXECUTABLES', (alias, tmp_path / 'absent'))
    monkeypatch.setattr(fixtures, 'NATIVE_CONFIG', config)
    report = fixtures.native_runtime_identities()
    assert report['executables'][0]['resolvedPath'] == str(executable)
    assert report['executables'][0]['linkTarget'] == str(executable)
    assert report['executables'][1]['status'] == report['configs']['status'] == 'missing'
    config.mkdir()
    entry = config / 'loader.conf'
    entry.write_bytes(b'x' * (64 * 1024))
    assert len(fixtures.native_runtime_identities()['configs']['entries']) == 1
    entry.write_bytes(b'x' * (64 * 1024 + 1))
    with pytest.raises(ValueError):
        fixtures.native_runtime_identities()
    entry.unlink()
    for number in range(33):
        (config / str(number)).write_bytes(b'')
    with pytest.raises(ValueError):
        fixtures.native_runtime_identities()
    for entry in config.iterdir():
        entry.unlink()
    config.rmdir()
    config.symlink_to(tmp_path, target_is_directory=True)
    with pytest.raises(ValueError):
        fixtures.native_runtime_identities()
