# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Real-filesystem retained-root snapshot boundaries; no source ledger mutation."""
from pathlib import Path
import os
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import readonly_files as ro


def test_capture_pages_eof_and_full_snapshot_are_exact(tmp_path):
    source = tmp_path / 'journal.jsonl'
    source.write_bytes(b'0123456789')
    with ro.ReadOnlyRoot(tmp_path) as root:
        with root.capture('journal.jsonl', maximum=10) as captured:
            identity = captured.info.identity
            assert captured.read_page(2, 4) == b'2345'
            assert captured.read_page(10, 4) == b''
            assert captured.read_all() == source.read_bytes()
            assert captured.read_all() == source.read_bytes()
        with root.capture('journal.jsonl', expected_identity=identity) as captured:
            assert captured.info.size == 10
        assert root.identity in root.observe_ancestry()
    assert source.read_bytes() == b'0123456789'


def test_append_between_captures_preserves_leaf_identity(tmp_path):
    source = tmp_path / 'journal.jsonl'; source.write_bytes(b'old\n')
    with ro.ReadOnlyRoot(tmp_path) as root:
        with root.capture(source.name) as first:
            identity = first.info.identity
            assert first.read_all() == b'old\n'
        with source.open('ab') as stream:
            stream.write(b'new\n')
        with root.capture(source.name, expected_identity=identity) as second:
            assert second.read_all() == b'old\nnew\n'


@pytest.mark.parametrize('relative', ['', '.', '..', '../outside', 'nested/../file', '/absolute', 'nested//file'])
def test_relative_traversal_or_ambiguous_components_are_denied(tmp_path, relative):
    with ro.ReadOnlyRoot(tmp_path) as root:
        with pytest.raises(ValueError):
            root.capture(relative)


def test_hardlinks_symlinks_and_nonregular_files_are_denied(tmp_path):
    source = tmp_path / 'regular'; source.write_bytes(b'unchanged')
    (tmp_path / 'link').symlink_to(source)
    os.link(source, tmp_path / 'alias')
    (tmp_path / 'directory').mkdir()
    with ro.ReadOnlyRoot(tmp_path) as root:
        for name in ['regular', 'alias', 'link', 'directory']:
            with pytest.raises((ValueError, OSError)):
                root.capture(name)


def test_expected_leaf_replacement_is_denied_before_read(tmp_path, monkeypatch):
    source = tmp_path / 'journal'; source.write_bytes(b'original')
    with ro.ReadOnlyRoot(tmp_path) as root:
        with root.capture(source.name) as initial:
            identity = initial.info.identity
        replacement = tmp_path / 'replacement'; replacement.write_bytes(b'replacement')
        replacement.replace(source)
        monkeypatch.setattr(ro.os, 'pread', lambda *_args: pytest.fail('Replacement must not return bytes'))
        with pytest.raises(ValueError, match='identity'):
            root.capture(source.name, expected_identity=identity)


@pytest.mark.skipif(os.name == 'nt', reason='POSIX descriptor race; native Windows sharing tested separately')
def test_root_replacement_revokes_capture_and_existing_snapshot(tmp_path):
    directory = tmp_path / 'selected'; directory.mkdir()
    (directory / 'journal').write_bytes(b'original')
    with ro.ReadOnlyRoot(directory) as root:
        with root.capture('journal') as captured:
            directory.rename(tmp_path / 'old')
            directory.mkdir(); (directory / 'journal').write_bytes(b'other')
            with pytest.raises(ValueError, match='root'):
                captured.read_page(0, 8)
            with pytest.raises(ValueError, match='root'):
                root.capture('journal')


@pytest.mark.skipif(os.name == 'nt', reason='POSIX descriptor race; native Windows sharing tested separately')
def test_intermediate_substitution_cannot_redirect_capture(tmp_path, monkeypatch):
    selected = tmp_path / 'selected'; selected.mkdir()
    nested = selected / 'nested'; nested.mkdir(); (nested / 'journal').write_bytes(b'original')
    outside = tmp_path / 'outside'; outside.mkdir(); (outside / 'journal').write_bytes(b'outside')
    original_open = ro.os.open
    swapped = False
    def opening(path, flags, *args, **kwargs):
        nonlocal swapped
        if path == 'journal' and kwargs.get('dir_fd') is not None and not swapped:
            swapped = True
            nested.rename(selected / 'retained')
            nested.symlink_to(outside, target_is_directory=True)
        return original_open(path, flags, *args, **kwargs)
    with ro.ReadOnlyRoot(selected) as root:
        monkeypatch.setattr(ro.os, 'open', opening)
        with root.capture('nested/journal') as captured:
            assert captured.read_all() == b'original'
        with pytest.raises((ValueError, OSError)):
            root.capture('nested/journal')


@pytest.mark.skipif(os.name == 'nt', reason='POSIX descriptor race; native Windows sharing tested separately')
def test_in_place_change_during_page_is_denied(tmp_path, monkeypatch):
    source = tmp_path / 'journal'; source.write_bytes(b'original')
    original_pread = ro.os.pread
    with ro.ReadOnlyRoot(tmp_path) as root:
        with root.capture(source.name) as captured:
            def changing(fd, length, offset):
                data = original_pread(fd, length, offset)
                source.write_bytes(b'changed!')
                info = source.stat(); os.utime(source, ns=(info.st_atime_ns, info.st_mtime_ns + 1_000_000_000))
                return data
            monkeypatch.setattr(ro.os, 'pread', changing)
            with pytest.raises(ValueError, match='changed'):
                captured.read_page(0, 8)


@pytest.mark.parametrize('maximum', [-1, True, 1.5])
def test_invalid_bounds_fail_before_file_capture(tmp_path, maximum):
    with ro.ReadOnlyRoot(tmp_path) as root:
        with pytest.raises(ValueError):
            root.capture('missing', maximum=maximum)


def test_closed_handles_reject_reuse_and_close_is_idempotent(tmp_path):
    source = tmp_path / 'journal'; source.write_bytes(b'bytes')
    root = ro.ReadOnlyRoot(tmp_path); captured = root.capture(source.name)
    captured.close(); captured.close()
    with pytest.raises(ValueError):
        captured.read_all()
    root.close(); root.close()
    with pytest.raises(ValueError):
        root.capture(source.name)


@pytest.mark.skipif(os.name == 'nt', reason='POSIX descriptor race; native Windows sharing tested separately')
def test_legacy_snapshot_retains_original_bytes_after_atomic_replacement(tmp_path, monkeypatch):
    source = tmp_path / 'journal'; source.write_bytes(b'original')
    replacement = tmp_path / 'replacement'; replacement.write_bytes(b'new generation')
    original = ro._PosixRoot.read_all
    def reading(self, handle, size):
        replacement.replace(source)
        return original(self, handle, size)
    monkeypatch.setattr(ro._PosixRoot, 'read_all', reading)
    assert ro.read_snapshot(source) == b'original'
    assert source.read_bytes() == b'new generation'


def test_fifo_is_rejected_without_waiting_for_a_writer(tmp_path):
    if os.name == 'nt': pytest.skip('POSIX FIFO boundary')
    os.mkfifo(tmp_path / 'fifo')
    with ro.ReadOnlyRoot(tmp_path) as root:
        with pytest.raises(ValueError): root.capture('fifo')


@pytest.mark.skipif(os.name == 'nt', reason='Actual POSIX descriptor acquisition boundary')
@pytest.mark.parametrize('stage', ['initial', 'child', 'last-child', 'public-constructor', 'capture', 'read', 'verify'])
def test_metadata_failure_closes_acquired_descriptors(tmp_path, monkeypatch, stage):
    """Inject a native metadata error at ownership boundaries and inspect actual FDs."""
    source = tmp_path / 'journal'; source.write_bytes(b'unchanged')
    saved_fstat = os.fstat
    root_calls = len(tmp_path.absolute().parts)
    fail_at = {'initial': 1, 'child': 2, 'last-child': root_calls,
               'public-constructor': root_calls + 1}.get(stage)
    calls = 0; failed = []
    def metadata(fd):
        nonlocal calls
        calls += 1
        if calls == fail_at:
            failed.append(fd)
            raise OSError('controlled metadata acquisition failure')
        return saved_fstat(fd)
    monkeypatch.setattr(ro.os, 'fstat', metadata)
    try:
        with pytest.raises(OSError, match='controlled metadata'):
            with ro.ReadOnlyRoot(tmp_path) as root:
                if stage == 'capture':
                    # Root verification inspects a fresh ancestry then the
                    # retained root; fail final leaf inspection after that.
                    fail_at = calls + root_calls + 3
                    root.capture(source.name)
                elif stage == 'read':
                    with root.capture(source.name) as captured:
                        fail_at = calls + root_calls + 3
                        captured.read_page(0, 4)
                elif stage == 'verify':
                    fail_at = calls + 1
                    root.observe_ancestry()
        assert failed, 'The controlled metadata boundary must execute'
        for descriptor in set(failed):
            with pytest.raises(OSError) as error:
                saved_fstat(descriptor)
            assert error.value.errno == 9
    finally:
        # Failed-first runs close their own leaked test descriptors, ensuring
        # deterministic isolation without weakening the liveness assertion.
        for descriptor in set(failed):
            try: saved_fstat(descriptor)
            except OSError: pass
            else: os.close(descriptor)
    assert source.read_bytes() == b'unchanged'
