# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""State owns mutable data, not the external material-reader capability."""
from governed_fixtures import GovernedHarness
import lifecycle as lc
import copy
import pytest


class _ExternalReader:
    """A resource-ownership collaborator, not a qualified Store or authority."""

    def __deepcopy__(self, memo):
        raise AssertionError('A State fork must not copy its external reader provider')

    def read(self, identifier):
        return identifier.encode('ascii')


def test_state_fork_retains_reader_capability_and_detaches_owned_mutable_data():
    # These synthetic fields exercise ownership only, never journal qualification.
    provider = _ExternalReader()
    reader = provider.read
    state = lc.State('fork-ownership', blob_reader=reader)
    point = ('default', 'a' * 64)
    state.states[point] = {'validity': 'pending', 'applicable': False}
    state.versions['a' * 64] = lc._freeze({'content': {'notes': ['original']}})
    state.transactions.append(lc._freeze({'nested': {'values': ['accepted']}}))
    state.requests['request'] = lc._freeze({'receipt': {'items': ['original']}})

    fork = state._fork()

    assert fork is not state
    assert fork.blob_reader is reader
    assert fork.blob_reader.__self__ is provider
    assert fork.blob_reader('material') == b'material'
    fork.states[point]['validity'] = 'invalid'
    assert fork.versions['a' * 64] is state.versions['a' * 64]
    with pytest.raises(TypeError):
        fork.versions['a' * 64]['content']['notes'].append('fork-only')
    with pytest.raises(TypeError):
        fork.transactions[0]['nested']['values'].clear()
    with pytest.raises(TypeError):
        fork.requests['request']['receipt']['items'].append('fork-only')
    proposal = copy.deepcopy(fork.versions['a' * 64])
    proposal['content']['notes'].append('proposed')
    fork.transactions.clear()
    fork.versions.clear()
    assert state.states[point] == {'validity': 'pending', 'applicable': False}
    assert state.versions['a' * 64]['content']['notes'] == ['original']
    assert state.transactions[0]['nested']['values'] == ['accepted']
    assert state.requests['request']['receipt']['items'] == ['original']


def test_signed_return_never_copies_store_provider_or_leaks_public_mutations(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='fork-signed-return')
    host.bootstrap()
    before = host.path.read_bytes()

    def reject_provider_copy(provider, memo):
        raise AssertionError('A semantic State fork copied the external Store checkpoint')

    # The real planner, signed return, candidate verifier and public read still run.
    monkeypatch.setattr(lc.Store, '__deepcopy__', reject_provider_copy, raising=False)
    actor = host.setup_author(suffix='fork-owned-result')
    subject, record = host.product('fork-owned-result', actor)
    receipt = host.commit(host.submission(actor, subject, record))
    public = host.store.read()
    assert public.head == receipt['after_head']
    assert host.path.read_bytes().startswith(before)
    run = public.resolve(actor['author_context'], 'context')['run_id']
    assert public.run_states[run] == 'returned'
    assert public.resolve(subject, 'product')['owner'] == actor['owner']
    assert public.blob_reader.__self__ is host.store

    expected_validity = public.states[(host.scope, subject['version_id'])]['validity']
    public.states[(host.scope, subject['version_id'])]['validity'] = 'caller-invalidated'
    with pytest.raises(TypeError):
        public.resolve(subject, 'product')['limitations'].append('Detached caller note')
    public.transactions.clear()
    fresh = host.store.read()
    assert fresh.head == receipt['after_head']
    assert fresh.transactions
    assert fresh.states[(host.scope, subject['version_id'])]['validity'] == expected_validity
    assert fresh.resolve(subject, 'product')['limitations'] == []
    assert fresh.blob_reader.__self__ is host.store
