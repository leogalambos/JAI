# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Portable handle-contract checks and separately marked native Windows tests.

Fake WinAPI collaborators exercise the acquisition algorithm on any test host;
only the native tests provide evidence about actual Windows filesystem behavior.
"""
from dataclasses import replace
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import windows_readonly as win


class FakeAPI:
    def __init__(self, raw=b'captured bytes', *, final=None, after=None, failure=None):
        self.raw, self.offset, self.closed, self.opened = raw, 0, [], []
        self.final = final or win._Info(0, len(raw), 1, (1, 2, 3), (4, 5))
        self.after, self.failure, self.final_infos = after, failure, 0

    def root(self, drive):
        assert drive == 'C:\\'
        self.opened.append(('root', drive))
        return 1

    def child(self, parent, component, directory):
        self.opened.append((parent, component, directory))
        if self.failure == component:
            raise OSError('native open refused')
        return 2 if directory else 3

    def info(self, handle):
        if handle != 3:
            return win._Info(win._DIRECTORY, 0, 1, (1, 0, handle), (0, 0))
        self.final_infos += 1
        return self.after if self.final_infos > 1 and self.after else self.final

    def read(self, handle, size):
        assert handle == 3 and size <= win._CHUNK
        # Short successful native reads are permitted and must be accumulated.
        result = self.raw[self.offset:self.offset + min(size, 3)]
        self.offset += len(result)
        return result

    def close(self, handle):
        self.closed.append(handle)


@pytest.mark.parametrize('path', [
    None, b'C:\\dir\\file', 'relative.txt', 'C:relative.txt', '\\root-relative', '\\\\server\\share\\file',
    '\\\\?\\C:\\file', '\\\\.\\PhysicalDrive0', 'C:\\dir\\..\\file',
    'C:\\dir\\.\\file', 'C:\\dir\\file:stream', 'C:\\dir\\file.',
    'C:\\dir\\file ', 'C:\\dir\\CON.txt', 'C:\\dir\\COM¹', 'C:\\dir\\CONIN$',
    'C:\\dir\\bad*name', 'C:\\dir\\', 'C:\\dir\\\\file',
    'C:/dir/file', 'C:\\dir\\bad\x00name', 'C:\\dir\\bad\ud800name',
])
def test_unsafe_path_is_rejected_before_native_api_acquisition(path, monkeypatch):
    def forbidden():
        pytest.fail('Unsafe path must not open native handles')
    monkeypatch.setattr(win, '_WinAPI', forbidden)
    with pytest.raises(ValueError):
        win.read_snapshot(path)


@pytest.mark.parametrize('raw', [b'', b'a', b'finite bytes with short native reads'])
def test_portable_snapshot_contract_reads_exact_length_and_closes_reverse_order(raw, monkeypatch):
    api = FakeAPI(raw)
    monkeypatch.setattr(win, '_WinAPI', lambda: api)
    assert win.read_snapshot('C:\\dir\\file', maximum=len(raw)) == raw
    assert api.closed == [3, 2, 1]
    assert api.opened == [('root', 'C:\\'), (1, 'dir', True), (2, 'file', False)]


@pytest.mark.parametrize('maximum', [-1, True, 1.5, '10'])
def test_invalid_resource_bound_fails_without_windows_api(maximum):
    with pytest.raises(ValueError, match='nonnegative'):
        win.read_snapshot('C:\\dir\\file', maximum)


@pytest.mark.parametrize('kind', ['oversize', 'hardlink', 'reparse', 'directory',
                                  'size-change', 'rewrite', 'identity', 'short-read'])
def test_portable_snapshot_contract_rejects_unsafe_or_changed_final_handle(kind, monkeypatch):
    api = FakeAPI()
    if kind == 'oversize':
        maximum = 1
    else:
        maximum = None
    if kind == 'hardlink':
        api.final = replace(api.final, links=2)
    elif kind == 'reparse':
        api.final = replace(api.final, attributes=win._REPARSE)
    elif kind == 'directory':
        api.final = replace(api.final, attributes=win._DIRECTORY)
    elif kind == 'size-change':
        api.after = replace(api.final, size=api.final.size + 1)
    elif kind == 'rewrite':
        api.after = replace(api.final, modified=(8, 9))
    elif kind == 'identity':
        api.after = replace(api.final, identity=(2, 2, 3))
    elif kind == 'short-read':
        api.final = replace(api.final, size=api.final.size + 1)
    monkeypatch.setattr(win, '_WinAPI', lambda: api)
    with pytest.raises(ValueError):
        win.read_snapshot('C:\\dir\\file', maximum)
    assert api.closed == [3, 2, 1]


@pytest.mark.parametrize('failure,closed', [('dir', [1]), ('file', [2, 1])])
def test_open_failure_releases_already_acquired_handles(failure, closed, monkeypatch):
    api = FakeAPI(failure=failure)
    monkeypatch.setattr(win, '_WinAPI', lambda: api)
    with pytest.raises(OSError, match='native open refused'):
        win.read_snapshot('C:\\dir\\file')
    assert api.closed == closed


def test_portable_snapshot_can_retain_coherent_unlinked_descriptor(monkeypatch):
    api = FakeAPI()
    api.after = replace(api.final, links=0)
    monkeypatch.setattr(win, '_WinAPI', lambda: api)
    assert win.read_snapshot('C:\\dir\\file') == api.raw
    assert api.closed == [3, 2, 1]


def test_parent_reparse_is_rejected_and_both_handles_close(monkeypatch):
    api = FakeAPI()
    info = api.info
    api.info = lambda handle: (replace(info(handle), attributes=win._DIRECTORY | win._REPARSE)
                              if handle == 2 else info(handle))
    monkeypatch.setattr(win, '_WinAPI', lambda: api)
    with pytest.raises(ValueError, match='nonreparse'):
        win.read_snapshot('C:\\dir\\file')
    assert api.closed == [2, 1]


def test_viewer_windows_adapter_keeps_path_validation_and_resource_bounds(monkeypatch):
    api = FakeAPI()
    monkeypatch.setattr(win, '_WinAPI', lambda: api)
    assert win.read_snapshot('C:\\dir\\file', 32 * 1024 * 1024) == api.raw
    with pytest.raises(ValueError, match='absolute local-drive'):
        win.read_snapshot('C:drive-relative')
    with pytest.raises(ValueError, match='nontraversing'):
        win.read_snapshot('C:\\dir\\..\\file')


def test_native_api_is_not_silently_available_on_another_os():
    if os.name == 'nt':
        pytest.skip('Non-Windows fail-closed contract only')
    with pytest.raises(ValueError, match='unavailable on this OS'):
        win.read_snapshot('C:\\dir\\file')


native = pytest.mark.skipif(os.name != 'nt', reason='Requires native Windows filesystem/API')


@native
def test_native_windows_regular_empty_size_boundary_and_material_cap(tmp_path):
    source = tmp_path / 'finite-journal'
    source.write_bytes(b'')
    assert win.read_snapshot(source, maximum=0) == b''
    source.write_bytes(b'exact snapshot')
    assert win.read_snapshot(source, maximum=14) == b'exact snapshot'
    assert win.read_snapshot(source) == b'exact snapshot'
    with pytest.raises(ValueError, match='bounded single-link'):
        win.read_snapshot(source, maximum=13)
    with source.open('wb') as stream:
        stream.truncate(32 * 1024 * 1024 + 1)
    with pytest.raises(ValueError, match='bounded single-link'):
        win.read_snapshot(source, 32 * 1024 * 1024)
    assert len(win.read_snapshot(source)) == 32 * 1024 * 1024 + 1


@native
def test_native_windows_unicode_components_preserve_exact_names(tmp_path):
    source = tmp_path / 'é-𝄞-input'
    source.write_bytes(b'Unicode filename fixture')
    assert win.read_snapshot(source) == b'Unicode filename fixture'


@native
def test_native_windows_hardlinks_and_directories_are_rejected(tmp_path):
    source = tmp_path / 'source'
    source.write_bytes(b'not copied')
    alias = tmp_path / 'hardlink'
    os.link(source, alias)
    for path in (source, alias):
        with pytest.raises(ValueError, match='single-link'):
            win.read_snapshot(path)
    with pytest.raises((OSError, ValueError)):
        win.read_snapshot(tmp_path)


@native
def test_native_windows_final_and_parent_symlinks_are_rejected(tmp_path):
    directory = tmp_path / 'actual'
    directory.mkdir()
    source = directory / 'source'
    source.write_bytes(b'actual source')
    parent_alias, final_alias = tmp_path / 'parent-link', tmp_path / 'final-link'
    try:
        parent_alias.symlink_to(directory, target_is_directory=True)
        final_alias.symlink_to(source)
    except OSError as error:
        if getattr(error, 'winerror', None) == 1314:
            pytest.skip('Windows symlink privilege/developer mode is unavailable')
        raise
    for path in (parent_alias / 'source', final_alias):
        with pytest.raises((OSError, ValueError)):
            win.read_snapshot(path)
    assert source.read_bytes() == b'actual source'


@native
def test_native_windows_junction_parent_is_rejected(tmp_path):
    directory, junction = tmp_path / 'actual', tmp_path / 'junction'
    directory.mkdir()
    source = directory / 'source'
    source.write_bytes(b'junction target')
    command = Path(os.environ['SystemRoot']) / 'System32/cmd.exe'
    result = subprocess.run([str(command), '/d', '/c', 'mklink /J junction actual'],
                             cwd=tmp_path, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr.decode(errors='replace')
    try:
        with pytest.raises((OSError, ValueError)):
            win.read_snapshot(junction / 'source')
    finally:
        junction.rmdir()
    assert source.read_bytes() == b'junction target'


@native
@pytest.mark.parametrize('mutation', ['grow', 'truncate', 'rewrite'])
def test_native_windows_new_writer_is_rejected_during_snapshot(tmp_path, monkeypatch, mutation):
    source = tmp_path / 'source'
    original = b'Captured original bytes.'
    source.write_bytes(original)
    api = win._WinAPI()
    original_read = api.read
    mutated = []

    def read(handle, size):
        if not mutated:
            mutated.append(True)
            with pytest.raises(OSError) as rejected:
                if mutation == 'truncate':
                    source.write_bytes(b'x')
                elif mutation == 'grow':
                    with source.open('ab') as stream:
                        stream.write(b'appended')
                else:
                    with source.open('r+b') as stream:
                        stream.write(b'X' * len(original))
            assert rejected.value.winerror == 32
        return original_read(handle, size)

    api.read = read
    monkeypatch.setattr(win, '_WinAPI', lambda: api)
    assert win.read_snapshot(source) == original
    assert mutated == [True]
    assert source.read_bytes() == original
    # A subsequent ordinary mutation proves completed snapshots released handles.
    source.rename(tmp_path / 'after-snapshot')


@native
def test_native_windows_existing_live_writer_prevents_snapshot(tmp_path):
    source = tmp_path / 'source'
    source.write_bytes(b'original')
    with source.open('r+b') as writer:
        writer.write(b'updated!')
        writer.flush()
        with pytest.raises(OSError) as rejected:
            win.read_snapshot(source)
        assert rejected.value.winerror == 32
    assert win.read_snapshot(source) == b'updated!'


@native
def test_native_windows_replacement_keeps_original_descriptor_snapshot(tmp_path, monkeypatch):
    source, replacement = tmp_path / 'source', tmp_path / 'replacement'
    source.write_bytes(b'captured before replacement')
    replacement.write_bytes(b'new path generation')
    api = win._WinAPI()
    original_read = api.read
    replaced = []

    def read(handle, size):
        result = original_read(handle, size)
        if not replaced:
            replaced.append(True)
            replacement.replace(source)
        return result

    api.read = read
    monkeypatch.setattr(win, '_WinAPI', lambda: api)
    assert win.read_snapshot(source) == b'captured before replacement'
    assert source.read_bytes() == b'new path generation'


@native
def test_native_windows_ancestor_rename_cannot_swap_a_checked_prefix(tmp_path, monkeypatch):
    directory, moved = tmp_path / 'actual', tmp_path / 'moved'
    directory.mkdir()
    source = directory / 'source'
    source.write_bytes(b'original directory binding')
    api = win._WinAPI()
    original_child = api.child
    attempts = []

    def child(parent, component, directory_flag):
        if component == 'source':
            with pytest.raises(OSError) as rejected:
                directory.rename(moved)
            assert rejected.value.winerror in {5, 32}
            attempts.append(True)
        return original_child(parent, component, directory_flag)

    api.child = child
    monkeypatch.setattr(win, '_WinAPI', lambda: api)
    assert win.read_snapshot(source) == b'original directory binding'
    assert attempts == [True] and not moved.exists()
    directory.rename(moved)


def test_portable_retained_windows_root_pages_identity_and_close(monkeypatch):
    """Exercise retained-root adapter contracts without claiming native OS evidence."""
    import readonly_files as ro
    api = FakeAPI(b'0123456789')
    api.seek = lambda handle, offset: setattr(api, 'offset', offset)
    monkeypatch.setattr(win, '_WinAPI', lambda: api)
    native_root = ro._WindowsRoot('C:\\dir')
    root = object.__new__(ro.ReadOnlyRoot)
    root._native = native_root; root._closed = False
    root.identity = native_root.info(native_root.handle).identity
    with root:
        with root.capture('file') as captured:
            identity = captured.info.identity
            assert captured.read_page(3, 4) == b'3456'
            assert captured.read_all() == b'0123456789'
        with pytest.raises(ValueError, match='identity'):
            root.capture('file', expected_identity=('windows', 9, 9, 9))
        assert identity == ('windows', 1, 2, 3)
    assert api.closed[-2:] == [2, 1]


@native
def test_native_windows_retained_root_append_between_captures_and_final_replacement(tmp_path):
    """Prepared native evidence: short leaf handles permit append after capture ends."""
    import readonly_files as ro
    source = tmp_path / 'journal.jsonl'; source.write_bytes(b'first\n')
    with ro.ReadOnlyRoot(tmp_path) as root:
        with root.capture(source.name) as captured:
            identity = captured.info.identity
            assert captured.read_page(1, 3) == b'irs'
        with source.open('ab') as stream: stream.write(b'next\n')
        with root.capture(source.name, expected_identity=identity) as captured:
            assert captured.read_all() == b'first\nnext\n'
        replacement = tmp_path / 'replacement'; replacement.write_bytes(b'new generation')
        replacement.replace(source)
        with pytest.raises(ValueError, match='identity'):
            root.capture(source.name, expected_identity=identity)
    source.rename(tmp_path / 'released.jsonl')


def test_portable_public_root_constructor_rolls_back_windows_handles(monkeypatch):
    """Public generic construction owns and closes a fully acquired native chain on info failure."""
    import readonly_files as ro
    api = FakeAPI(); original_info = api.info; calls = 0
    def metadata(handle):
        nonlocal calls
        calls += 1
        if calls == 3: raise OSError('controlled final root metadata failure')
        return original_info(handle)
    api.info = metadata
    monkeypatch.setattr(win, '_WinAPI', lambda: api)
    monkeypatch.setattr(ro, '_PosixRoot', lambda _path: ro._WindowsRoot('C:\\dir'))
    with pytest.raises(OSError, match='controlled final root metadata'):
        ro.ReadOnlyRoot('C:\\dir')
    assert api.closed == [2, 1]
