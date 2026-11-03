# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Real ledger/material integrity boundaries, beyond message-level signature tests."""
import copy
import json
from pathlib import Path

import pytest

from governed_fixtures import GovernedHarness
import lifecycle as lc


def test_committed_history_cannot_be_rehashed_to_hide_substituted_effects(tmp_path, monkeypatch):
    harness = GovernedHarness(tmp_path, monkeypatch)
    harness.bootstrap()
    original = harness.path.read_bytes()
    transaction = json.loads(original.splitlines()[0])
    assert lc.replay([transaction], harness.engagement, blob_reader=harness.store._blob).head == transaction['hash']
    changed = copy.deepcopy(transaction)
    changed['operations'][0]['data']['effects'] = []
    changed['hash'] = lc._transaction_hash(changed)
    harness.path.write_text(json.dumps(changed) + '\n')
    tampered = harness.path.read_bytes()
    with pytest.raises(ValueError):
        lc.replay([changed], harness.engagement, blob_reader=harness.store._blob)
    with pytest.raises(ValueError):
        harness.store.read()
    assert harness.path.read_bytes() == tampered
    assert tampered != original


def test_store_blob_identity_and_nofollow_protect_supporting_material(tmp_path, monkeypatch):
    harness = GovernedHarness(tmp_path, monkeypatch)
    identifier = harness.store.put_blob(b'Exact supporting execution bytes\n')
    assert harness.store.put_blob(b'Exact supporting execution bytes\n') == identifier
    assert harness.store._blob(identifier) == b'Exact supporting execution bytes\n'
    blob_path = harness.store.material / identifier
    blob_path.write_bytes(b'Substituted supporting material\n')
    with pytest.raises(ValueError):
        harness.store._blob(identifier)
    external = tmp_path / 'outside-source'; external.write_bytes(b'Exact supporting execution bytes\n')
    blob_path.unlink(); blob_path.symlink_to(external)
    with pytest.raises(OSError):
        harness.store._blob(identifier)
    assert external.read_bytes() == b'Exact supporting execution bytes\n'


def test_blank_duplicate_and_nonfinite_transaction_json_fail_closed(tmp_path, monkeypatch):
    harness = GovernedHarness(tmp_path, monkeypatch)
    for raw in (b'\n', b'{"format":3,"format":3}\n', b'{"format":NaN}\n'):
        harness.path.write_bytes(raw)
        with pytest.raises(ValueError):
            harness.store.read()
        assert harness.path.read_bytes() == raw
