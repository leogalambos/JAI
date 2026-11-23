# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Ordinary recording advances a verified prefix without internal credentials."""
import copy

import pytest

from governed_fixtures import GovernedHarness, delivery, op
import lifecycle as lc


def _observe_verification(monkeypatch):
    calls = []
    verify = lc._verify_transaction

    def observed(state, transaction, live=False):
        calls.append((transaction['sequence'], transaction['hash']))
        return verify(state, transaction, live=live)

    monkeypatch.setattr(lc, '_verify_transaction', observed)
    return calls


def _same_semantics(actual, expected):
    for field in ('head', 'transactions', 'versions', 'states', 'selections',
                  'proofs', 'reliance', 'assignment_states', 'run_states',
                  'requests', 'messages', 'usage', 'events', 'sources', 'counters'):
        assert getattr(actual, field) == getattr(expected, field), field


def _selection_request(host, assignment, record, label):
    context = {'owner': record['owner'], 'assignment': assignment,
               'profile': host.profile, 'purpose': record['responsibility'],
               'run_id': label + '-run', 'issued_to': record['assigned_actor'],
               'inputs': record['inputs'], 'attachments': [],
               'effects': record['effects'], 'execution': {'phase': 'selection'},
               'expires_at_ms': record['deadline_ms'], 'speculation': None,
               'ready_basis': host.store.read().ready_basis(assignment)}
    return host.message('record_proposal', {'logical_id': label,
                        'record_type': 'context', 'record': context})


def test_warm_reads_and_new_writes_do_not_replay_accepted_transactions(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='incremental-equivalence')
    host.bootstrap()
    store = lc.Store(host.path, host.engagement)
    calls = _observe_verification(monkeypatch)
    initial = store.read()
    assert [sequence for sequence, _ in calls] == list(range(1, len(initial.transactions) + 1))
    calls.clear()
    isolated = store.read()
    assert calls == []
    isolated.transactions.clear()
    with pytest.raises(TypeError):
        isolated.resolve(host.profile, 'profile')['obligations'].clear()
    isolated.states.clear()
    _same_semantics(store.read(), initial)
    assert calls == []

    assignment, record = host.assignment('incremental-root', 'setter')
    calls.clear()
    extended = store.read()
    assert [sequence for sequence, _ in calls] == list(range(len(initial.transactions) + 1,
                                                            len(extended.transactions) + 1))
    message = _selection_request(host, assignment, record, 'incremental-selection')
    calls.clear()
    response = store.submit(lc.canonical(message))
    assert response['status'] == 'committed', response
    assert calls == [], 'A live transition is validated once, not replayed as its own credential'
    warm = store.read()
    assert calls == []
    assert warm.head == response['receipt']['after_head']
    cold = lc.Store(host.path, host.engagement).read()
    assert len(calls) == len(warm.transactions)
    _same_semantics(warm, cold)


def test_changed_or_truncated_prefix_loses_trust_without_rewriting_history(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='incremental-prefix-guards')
    host.bootstrap()
    assignment, _ = host.assignment('guarded-root', 'setter')
    store = lc.Store(host.path, host.engagement)
    expected = store.read()
    original = host.path.read_bytes()
    calls = _observe_verification(monkeypatch)
    shortened = b''.join(original.splitlines(keepends=True)[:-1])
    host.path.write_bytes(shortened)
    state = store.read()
    assert len(calls) == len(state.transactions)
    assert assignment['version_id'] not in state.versions
    host.path.write_bytes(original)
    _same_semantics(store.read(), expected)
    altered = lc._parse_transactions(original)
    altered[0]['hash'] = 'f' * 64
    corrupt = b''.join(op.canonical(row) + b'\n' for row in altered)
    host.path.write_bytes(corrupt)
    calls.clear()
    with pytest.raises(lc.ERROR) as failure:
        store.read()
    assert failure.value.code == 'P_INTEGRITY'
    assert calls
    assert host.path.read_bytes() == corrupt


def test_serialization_admitted_metadata_expiry_and_head_boundaries(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='incremental-live-guards')
    host.bootstrap()
    assignment, record = host.assignment('live-root', 'setter')
    store = host.store
    message = _selection_request(host, assignment, record, 'live-selection')
    before = host.path.read_bytes()
    expected = store.read()
    serialize = op.canonical
    injected = []

    def corrupt_transaction(value):
        if isinstance(value, dict) and value.get('format') == 9 and 'hash' in value:
            value = copy.deepcopy(value)
            value['hash'] = 'f' * 64
            injected.append(value['sequence'])
        return serialize(value)

    with monkeypatch.context() as fault:
        fault.setattr(op, 'canonical', corrupt_transaction)
        response = store.submit(lc.canonical(message))
    assert injected and response['status'] == 'rejected', response
    assert host.path.read_bytes() == before
    _same_semantics(store.read(), expected)
    policy = expected.resolve(host.routing_policy, 'source')
    path = store.material / policy['material'][0]
    material = path.read_bytes()
    path.unlink()
    try:
        import governed_routing

        def forbid_admitted_policy_reload(*args, **kwargs):
            raise AssertionError('Metadata-only continuation must reuse the admitted routing snapshot')

        with monkeypatch.context() as metadata:
            metadata.setattr(governed_routing, 'load_policy', forbid_admitted_policy_reload)
            response = store.submit(lc.canonical(message))
        assert response['status'] == 'committed', response
    finally:
        assert store.put_blob(material) == policy['material'][0]
    # Expiry and concurrency apply to a NEW action, not replay of the committed one.
    message = _selection_request(host, assignment, record, 'fresh-live-selection')
    with monkeypatch.context() as clock:
        clock.setattr(lc.time, 'time', lambda: (message['expires_at_ms'] + 1) / 1000)
        response = store.submit(lc.canonical(message))
    assert response['status'] == 'rejected' and response['error']['code'] == 'P_EXPIRED', response
    host.assignment('concurrent-root', 'setter', owner=host.owner('why'))
    advanced = host.path.read_bytes()
    response = store.submit(lc.canonical(message))
    assert response['status'] == 'rejected' and response['error']['code'] == 'P_HEAD', response
    assert host.path.read_bytes() == advanced


def test_warm_commit_reads_no_prefix_and_recovers_a_partial_owned_append(tmp_path, monkeypatch):
    """Preserve the verified prefix across a short write and a fresh Store."""
    host = GovernedHarness(tmp_path, monkeypatch, engagement='append-recovery')
    host.bootstrap()
    assignment, record = host.assignment('append-root', 'setter')
    store = host.store
    message = _selection_request(host, assignment, record, 'recoverable-context')
    original = host.path.read_bytes()
    inode = host.path.stat().st_ino
    warm = store.read()
    read_span = lc.Store._read_span
    operations = []

    def observe(fd, offset, length):
        operations.append((offset, length))
        return read_span(fd, offset, length)

    monkeypatch.setattr(lc.Store, '_read_span', staticmethod(observe))
    real_write = lc.os.write

    def fail_after_partial(fd, payload):
        if lc.os.fstat(fd).st_ino == inode:
            real_write(fd, payload[:27])
            raise OSError('Injected short append')
        return real_write(fd, payload)

    with monkeypatch.context() as fault:
        fault.setattr(lc.os, 'write', fail_after_partial)
        assert store.submit(lc.canonical(message))['status'] == 'rejected'
    assert operations == [(len(original) - 1, 1)]
    assert len(host.path.read_bytes()) == len(original) + 27
    assert host.path.stat().st_ino == inode

    cold = lc.Store(host.path, host.engagement)
    assert cold.read().head == warm.head
    committed = cold.submit(lc.canonical(message))
    assert committed['status'] == 'committed', committed
    raw = host.path.read_bytes()
    assert raw.startswith(original)
    assert len(lc._parse_transactions(raw[len(original):])) == 1
    assert not cold._pending_path.exists()
    assert host.path.stat().st_ino == inode
    operations.clear()
    assert cold.read().head == committed['receipt']['after_head']
    assert cold.submit(lc.canonical(message))['status'] == 'already_committed'
    assert operations == []


def test_complete_but_unsynced_append_is_invisible_until_exclusive_recovery(tmp_path, monkeypatch):
    """Recover a fully written row before returning its original commit receipt."""
    host = GovernedHarness(tmp_path, monkeypatch, engagement='append-sync-recovery')
    host.bootstrap()
    assignment, record = host.assignment('sync-root', 'setter')
    store = host.store
    message = _selection_request(host, assignment, record, 'sync-context')
    original = host.path.read_bytes()
    before = store.read().head
    inode = host.path.stat().st_ino
    fsync = lc.os.fsync

    def fail_journal_sync(fd):
        if lc.os.fstat(fd).st_ino == inode:
            raise OSError('Injected journal sync failure')
        fsync(fd)

    with monkeypatch.context() as fault:
        fault.setattr(lc.os, 'fsync', fail_journal_sync)
        assert store.submit(lc.canonical(message))['status'] == 'rejected'
    raw = host.path.read_bytes()
    assert raw.startswith(original) and raw.endswith(b'\n') and len(raw) > len(original)
    fresh = lc.Store(host.path, host.engagement)
    assert fresh.read().head == before
    response = fresh.submit(lc.canonical(message))
    assert response['status'] == 'already_committed', response
    assert fresh.read().head == response['receipt']['after_head']
    assert host.path.read_bytes() == raw
    assert not fresh._pending_path.exists()
