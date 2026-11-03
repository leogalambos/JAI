# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Journal resource snapshots retain input-file safety without a history-size cap.

These are real filesystem/descriptor tests, not signature or journal-semantic
qualification. Deterministic read interleavings perform actual file changes.
"""
from contextlib import contextmanager
import hashlib
import os
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import operator_actions as op


def test_journal_snapshot_reads_exact_known_bytes_above_the_material_file_limit(tmp_path):
    path = tmp_path / 'large-journal-resource'
    digest = hashlib.sha256()
    block = b'Fictional finite journal resource bytes.\n' * 2048
    size = 0
    with path.open('wb') as stream:
        while size <= 32 * 1024 * 1024:
            stream.write(block)
            digest.update(block)
            size += len(block)
        tail = b'Exact captured end marker.\n'
        stream.write(tail)
        digest.update(tail)
        size += len(tail)
    captured = op.journal_snapshot(path)
    assert len(captured) == size > 32 * 1024 * 1024
    assert hashlib.sha256(captured).digest() == digest.digest()
    assert captured.endswith(tail)
    with pytest.raises(ValueError, match='bounded single-link regular file'):
        op.regular(path)


def test_journal_snapshot_rejects_final_parent_and_hard_links(tmp_path):
    directory = tmp_path / 'real-directory'
    directory.mkdir()
    source = directory / 'journal'
    source.write_bytes(b'Single-link descriptor fixture.\n')
    final_alias = tmp_path / 'final-alias'
    final_alias.symlink_to(source)
    parent_alias = tmp_path / 'parent-alias'
    parent_alias.symlink_to(directory, target_is_directory=True)
    for alias in (final_alias, parent_alias / source.name):
        with pytest.raises((OSError, ValueError)):
            op.journal_snapshot(alias)
    hard_alias = tmp_path / 'hard-alias'
    os.link(source, hard_alias)
    for linked in (source, hard_alias):
        with pytest.raises(ValueError, match='single-link'):
            op.journal_snapshot(linked)


def test_journal_snapshot_rejects_in_place_changes_but_keeps_a_coherent_replaced_descriptor(tmp_path, monkeypatch):
    path = tmp_path / 'journal'
    original = b'Original finite descriptor content.\n'
    fdopen = op.os.fdopen

    def interleaving(action, *, before=False):
        @contextmanager
        def opened(fd, mode, closefd=False):
            with fdopen(fd, mode, closefd=closefd) as stream:
                class Reader:
                    def read(self, size):
                        assert size == len(original), 'Read only the captured descriptor length.'
                        if before:
                            action()
                        raw = stream.read(size)
                        if not before:
                            action()
                        return raw
                yield Reader()
        return opened

    for change in ('grow', 'truncate', 'same-size-rewrite'):
        path.write_bytes(original)
        captured_info = path.stat()

        def mutate():
            if change == 'grow':
                with path.open('ab') as stream:
                    stream.write(b'Concurrent append.\n')
            elif change == 'truncate':
                path.write_bytes(b'Short')
            else:
                path.write_bytes(b'X' * len(original))
                os.utime(path, ns=(captured_info.st_atime_ns, captured_info.st_mtime_ns + 1000000))

        with monkeypatch.context() as patch:
            patch.setattr(op.os, 'fdopen', interleaving(mutate, before=change == 'truncate'))
            with pytest.raises(ValueError, match='changed while reading'):
                op.journal_snapshot(path)

    path.write_bytes(original)
    replacement = tmp_path / 'next-journal'
    replacement_bytes = b'A later atomic replacement is a distinct snapshot.\n'
    replacement.write_bytes(replacement_bytes)
    with monkeypatch.context() as patch:
        patch.setattr(op.os, 'fdopen', interleaving(lambda: replacement.replace(path)))
        assert op.journal_snapshot(path) == original
    assert path.read_bytes() == replacement_bytes
    assert op.journal_snapshot(path) == replacement_bytes
