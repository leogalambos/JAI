# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Packet assembly preserves the exact material availability/error boundary."""
import pytest

import lifecycle as lc
import governed_dispatch as dispatch


class _PacketState:
    """Supply only the state facts consumed before the material boundary."""

    def __init__(self, record):
        self.record = record

    def context_execution(self, context, live):
        return {'policy_use': {'ref': None}}

    def resolve(self, reference):
        return self.record


@pytest.mark.parametrize('condition', ['missing', 'corrupt'])
def test_assembly_translates_missing_material_but_preserves_integrity(tmp_path, condition):
    store = lc.Store(tmp_path / 'journal.jsonl', 'material-test')
    identifier = store.put_blob(b'Exact input')
    path = store.material / identifier
    if condition == 'missing':
        path.unlink()
    else:
        path.write_bytes(b'Changed input')
    runner = object.__new__(dispatch.Dispatcher)
    runner.store = store
    reference = {'scope': 'default', 'version_id': 'a' * 64}
    context = {'assignment': reference, 'effects': [], 'attachments': []}
    state = _PacketState({'material': [identifier]})
    expected = dispatch.DispatchError if condition == 'missing' else lc.ERROR
    with pytest.raises(expected) as failure:
        runner._assemble(state, reference, context, {'use_scope': 'default'})
    assert failure.value.code == ('P_CONTEXT' if condition == 'missing' else 'P_INTEGRITY')
    assert not store.path.exists()
