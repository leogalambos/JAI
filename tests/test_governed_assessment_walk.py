# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""A recursive assessment shares work, never current permission across operations."""
from collections import Counter
import copy

import pytest

from governed_fixtures import GovernedHarness, lc


@pytest.fixture
def assessment(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='assessment-walk')
    host.bootstrap()
    reference, record = host.assignment('assessment-root', 'setter')
    return host, host.store.read(), reference, record


def test_accepted_assignment_checks_are_memoized_per_assessment_without_history_reads(assessment, monkeypatch):
    host, state, _, record = assessment
    reads, walks = Counter(), Counter()
    reader, walk = state.blob_reader, state._walk_closure
    checked = []
    check = state._check_assignment_requirements

    def counted_check(value, live):
        checked.append((lc.canonical(value), live))
        return check(value, live)

    def counted_read(identifier):
        reads[identifier] += 1
        return reader(identifier)

    def counted_walk(point):
        walks[state._key(point)] += 1
        return walk(point)

    state.blob_reader = counted_read
    monkeypatch.setattr(state, '_walk_closure', counted_walk)
    monkeypatch.setattr(state, '_check_assignment_requirements', counted_check)

    @lc._within_assessment
    def assess(current):
        current._assignment_requirements(record)
        current._assignment_requirements(copy.deepcopy(record))

    original_states = copy.deepcopy(state.states)
    assess(state)
    assert len(checked) == 1
    assert reads == walks == Counter()
    assert state._assessment_walk is None
    assess(state)
    assert len(checked) == 2
    assert reads == walks == Counter()
    assert state.states == original_states
    assert state._assessment_walk is None
    assert host.store.read().states == original_states

    # Unit-state cancellation changes a direct governing fact, not the accepted
    # assignment's immutable admission evidence.
    state.states[(host.scope, host.input_a['version_id'])] = {'validity': 'invalid', 'applicable': False}
    with pytest.raises(lc.ERROR) as failure:
        assess(state)
    assert failure.value.code == 'P_CONTEXT'
    assert len(checked) == 3
    assert reads == walks == Counter()
    assert state._assessment_walk is None


def test_accepted_assignment_reuses_admission_but_explicit_material_and_expiry_checks_remain_live(assessment):
    host, state, _, record = assessment
    state._assignment_requirements(record)
    assert state.evaluate(host.input_a)['qualified']
    source = state.resolve(host.input_a, 'source')
    identifier = source['material'][0]
    path = host.store.material / identifier
    raw = path.read_bytes()
    path.unlink()
    try:
        state._assignment_requirements(record)
        assert state._assessment_walk is None
        with pytest.raises(lc.ERROR) as failure:
            state._material(source, True)
        assert failure.value.code == 'P_CONTEXT'
        assert state._assessment_walk is None
    finally:
        assert host.store.put_blob(raw) == identifier
    path.write_bytes(b'Changed current assessment input.')
    try:
        state._assignment_requirements(record)
        assert state._assessment_walk is None
        with pytest.raises(lc.ERROR) as failure:
            state._material(source, True)
        assert failure.value.code == 'P_CONTEXT'
        assert state._assessment_walk is None
    finally:
        path.unlink()
        assert host.store.put_blob(raw) == identifier
    state._assignment_requirements(record)
    message = copy.deepcopy(state.transactions[-1]['operations'][0]['data']['message'])
    with pytest.raises(lc.ERROR) as failure:
        state.derive(message, message['sender'], message['expires_at_ms'])
    assert failure.value.code == 'P_EXPIRED'
    assert state._assessment_walk is None


def test_inline_material_cannot_replace_current_cas_and_apply_discards_inflight_work(assessment):
    host, state, _, _ = assessment
    source = state.resolve(host.input_a, 'source')
    identifier = source['material'][0]
    path = host.store.material / identifier
    raw = path.read_bytes()
    archived = {identifier: raw}

    @lc._within_assessment
    def archived_then_current(target):
        assert target._material_bytes(identifier, archived.__getitem__) == raw
        target._material(source, True)

    path.unlink()
    try:
        with pytest.raises(lc.ERROR) as failure:
            archived_then_current(state)
        assert failure.value.code == 'P_CONTEXT'
        assert state._assessment_walk is None
    finally:
        assert host.store.put_blob(raw) == identifier

    message = state.transactions[-1]['operations'][0]['data']['message']

    @lc._within_assessment
    def checked_then_apply(target):
        target._material(source, True)
        path.unlink()
        # Even an empty application is a state boundary: no previously completed
        # check may satisfy subsequent processing in the same caller frame.
        target._apply([], message, {}, None)
        target._material(source, True)

    try:
        with pytest.raises(lc.ERROR) as failure:
            checked_then_apply(state)
        assert failure.value.code == 'P_CONTEXT'
        assert state._assessment_walk is None
    finally:
        assert host.store.put_blob(raw) == identifier
    state._material(source, True)
