# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Committed routing bytes remain exact and cannot be added or replayed twice."""
import copy
import json

import pytest

from test_governed_routing_runtime import host
from governed_fixtures import lc, op


@pytest.mark.parametrize('fault', ['changed-bytes', 'missing-file', 'duplicate-reference', 'unused-asset',
                                  'missing-artifact', 'repeated-artifact'])
def test_rehashed_history_rejects_inexact_or_unconsumed_routing_artifacts(host, fault):
    host.setup_author()
    transactions = [json.loads(line) for line in host.path.read_text().splitlines()]
    index = next(index for index, item in enumerate(transactions) if item['validation_artifacts'])
    entry = copy.deepcopy(transactions[index]['validation_artifacts'])
    if fault == 'repeated-artifact':
        index += 1
        transactions[index]['validation_artifacts'] = entry
    elif fault == 'missing-artifact':
        transactions[index]['validation_artifacts'] = []
    else:
        assets = transactions[index]['validation_artifacts']
        identifier = next(iter(assets))
        if fault == 'changed-bytes':
            (host.store.material / identifier).write_bytes(b'altered captured bytes')
        elif fault == 'missing-file':
            (host.store.material / identifier).unlink()
        elif fault == 'duplicate-reference':
            assets.append(identifier)
        else:
            assets.append(host.store.put_blob(b'unused asset'))
            assets.sort()
    # Rehash the changed terminal transaction so this exercises artifact
    # validation independently of the ordinary journal hash mismatch guard.
    transactions = transactions[:index + 1]
    transactions[-1]['hash'] = lc._transaction_hash(transactions[-1])
    raw = b''.join(op.canonical(item) + b'\n' for item in transactions)
    host.path.write_bytes(raw)
    with pytest.raises(lc.ERROR):
        lc.Store(host.path, host.store.engagement).read()
    assert host.path.read_bytes() == raw


def test_validation_assets_are_exact_file_references_with_equal_warm_and_cold_state(host):
    """Journal rows name existing CAS bytes; a fresh reader verifies the same head."""
    host.setup_author()
    warm = host.store.read()
    references = [identifier for row in warm.transactions for identifier in row['validation_artifacts']]
    assert references and len(references) == len(set(references))
    assert all(row['format'] == 9 and row['validation_artifacts'] == sorted(row['validation_artifacts'])
               for row in warm.transactions)
    assert all(lc.blob(host.store._blob(identifier)) == identifier for identifier in references)
    cold = lc.Store(host.path, host.store.engagement).read()
    assert cold.head == warm.head and cold.transactions == warm.transactions
    assert cold.validation_assets == warm.validation_assets
    rows = [json.loads(line) for line in host.path.read_text().splitlines()]
    rows[0]['format'] = 8
    with pytest.raises(lc.ERROR, match='Unsupported historical journal format'):
        lc.replay(rows, engagement=host.store.engagement, blob_reader=host.store._blob)
