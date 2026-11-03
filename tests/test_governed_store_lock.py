# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""A killed writer releases native ownership without deleting lock sentinels."""
from pathlib import Path
import select
import subprocess
import sys

from governed_fixtures import GovernedHarness
import lifecycle as lc
from test_governed_incremental_store import _selection_request


def test_actual_writer_excludes_concurrent_submit_and_death_releases_ownership(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='native-lock-lifetime')
    host.bootstrap()
    assignment, record = host.assignment('next-local-task', 'setter')
    message = _selection_request(host, assignment, record, 'after-writer-death')
    before = host.path.read_bytes()
    sentinel = Path(str(host.path) + '.lock')
    identity = sentinel.stat().st_ino
    code = ('import sys; sys.path.insert(0, sys.argv[1]); import lifecycle as lc; '
            'lock=lc.store_lock(sys.argv[2]); lock.__enter__(); '
            'print("LOCKED", flush=True); sys.stdin.readline()')
    process = subprocess.Popen([sys.executable, '-B', '-c', code,
        str(Path(lc.__file__).parent), str(host.path)], stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        assert select.select([process.stdout], [], [], 10)[0]
        assert process.stdout.readline().strip() == 'LOCKED'
        blocked = lc.Store(host.path, host.engagement).submit(lc.canonical(message))
        assert blocked['status'] == 'rejected' and blocked['error']['code'] == 'P_HEAD'
        assert host.path.read_bytes() == before
        process.kill()
        process.wait(timeout=10)
        assert sentinel.is_file() and sentinel.stat().st_ino == identity
        # A new Store must acquire the same inode after death, without a PID/TTL
        # cleanup path or manual deletion of anything in the accepted history.
        result = lc.Store(host.path, host.engagement).submit(lc.canonical(message))
        assert result['status'] == 'committed', result
        assert host.path.read_bytes().startswith(before)
        assert sentinel.stat().st_ino == identity
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=10)
        for stream in (process.stdin, process.stdout, process.stderr):
            stream.close()
