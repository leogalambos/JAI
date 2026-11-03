# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Verified policy values may share within one history, never across callers."""
import copy

import pytest

from governed_fixtures import GovernedHarness, lc, op


@pytest.fixture
def history(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='policy-snapshot-values')
    host.bootstrap()
    host.assignment('snapshot-root', 'setter')
    raw = host.path.read_bytes()
    transactions = lc._parse_transactions(raw)
    assert len(transactions) == 2
    return host, raw, transactions


def _encoded(transactions):
    return b''.join(op.canonical(transaction) + b'\n' for transaction in transactions)


def test_adjacent_verified_policy_values_share_without_changing_journal_bytes_or_caller_ownership(history):
    host, raw, incoming = history
    state = lc.replay(incoming, host.engagement, blob_reader=host.store._blob)
    first, second = state.transactions
    assert first['policy_snapshot'] is second['policy_snapshot']
    assert first['policy_snapshot'] is not incoming[0]['policy_snapshot']
    assert second['policy_snapshot'] is not incoming[1]['policy_snapshot']
    assert first['policy_snapshot'] is not state.versions[host.profile['version_id']]['content']['record']
    assert first['trust_snapshot'] is not second['trust_snapshot']
    assert _encoded(state.transactions) == raw
    assert [lc._transaction_hash(value) for value in state.transactions] == [value['hash'] for value in incoming]

    incoming[0]['policy_snapshot']['profile_id'] = 'caller-mutated-input'
    incoming[0]['operations'][0]['data']['message']['request_id'] = 'caller-mutated-message'
    incoming[1]['trust_snapshot']['signer'] = 'caller-mutated-trust'
    incoming[1]['hash'] = '0' * 64
    assert _encoded(state.transactions) == raw
    assert host.path.read_bytes() == raw


def test_separate_public_reads_and_private_checkpoint_keep_policy_values_isolated(history):
    host, raw, _ = history
    store = lc.Store(host.path, host.engagement)
    first, second = store.read(), store.read()
    expected = second.transactions[0]['policy_snapshot']['profile_id']
    assert first.transactions[0]['policy_snapshot'] is first.transactions[1]['policy_snapshot']
    assert second.transactions[0]['policy_snapshot'] is second.transactions[1]['policy_snapshot']
    assert first.transactions[0]['policy_snapshot'] is not second.transactions[0]['policy_snapshot']

    first.versions[host.profile['version_id']]['content']['record']['profile_id'] = 'caller-profile-body'
    assert first.transactions[0]['policy_snapshot']['profile_id'] == expected
    first.transactions[0]['policy_snapshot']['profile_id'] = 'caller-history-only'
    assert first.transactions[1]['policy_snapshot']['profile_id'] == 'caller-history-only'
    assert second.transactions[0]['policy_snapshot']['profile_id'] == expected
    fresh = store.read()
    assert _encoded(fresh.transactions) == raw
    assert fresh.resolve(host.profile, 'profile')['profile_id'] == expected
    assert fresh.transactions[0]['policy_snapshot'] is not second.transactions[0]['policy_snapshot']
    assert host.path.read_bytes() == raw


def test_canonically_changed_snapshot_is_rejected_before_append_or_value_sharing(history):
    host, raw, transactions = history
    state = lc.replay(transactions[:1], host.engagement, blob_reader=host.store._blob)
    altered = copy.deepcopy(transactions[1])
    assert altered['policy_snapshot']['obligations'][0]['allow_exclusion'] is False
    altered['policy_snapshot']['obligations'][0]['allow_exclusion'] = 0
    # Python equality conflates these values; their canonical policy commitments differ.
    assert altered['policy_snapshot'] == transactions[1]['policy_snapshot']
    assert lc.canonical(altered['policy_snapshot']) != lc.canonical(transactions[1]['policy_snapshot'])
    altered['hash'] = lc._transaction_hash(altered)
    before, versions, head = copy.deepcopy(state.transactions), copy.deepcopy(state.versions), state.head
    with pytest.raises(lc.ERROR) as mismatch:
        lc._verify_transaction(state, altered)
    assert mismatch.value.code == 'P_INTEGRITY'
    assert state.transactions == before and state.versions == versions and state.head == head
    lc._verify_transaction(state, transactions[1])
    assert state.transactions[0]['policy_snapshot'] is state.transactions[1]['policy_snapshot']
    assert _encoded(state.transactions) == raw


def test_canonically_changed_derived_effect_is_rejected_with_original_signed_inputs(history):
    host, _, transactions = history
    original = transactions[0]
    altered = copy.deepcopy(original)
    effects = altered['operations'][0]['data']['effects']
    profile = next(effect['manifest']['content']['record'] for effect in effects
                   if effect.get('manifest', {}).get('kind') == 'delivery.profile')
    assert profile['obligations'][0]['allow_exclusion'] is False
    profile['obligations'][0]['allow_exclusion'] = 0
    original_effects = original['operations'][0]['data']['effects']
    assert effects == original_effects
    assert lc.canonical(effects) != lc.canonical(original_effects)
    assert op.canonical(altered['dispatch_proof']) == op.canonical(original['dispatch_proof'])
    assert lc.canonical(altered['policy_snapshot']) == lc.canonical(original['policy_snapshot'])
    assert lc.canonical(altered['operations'][0]['data']['message']) == lc.canonical(original['operations'][0]['data']['message'])
    altered['hash'] = lc._transaction_hash(altered)
    state = lc.State(host.engagement, blob_reader=host.store._blob)
    with pytest.raises(lc.ERROR) as mismatch:
        lc._verify_transaction(state, altered)
    assert mismatch.value.code == 'P_ORIGIN'
    assert state.transactions == [] and state.versions == {} and state.head == lc.ZERO
