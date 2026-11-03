# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Accepted routing views stay detached; material access checks exact current bytes."""
import pytest

from governed_fixtures import GovernedHarness
import lifecycle as lc


def test_warm_policy_reuses_admission_and_returns_unpoisoned_projections(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='parsed-policy-guards')
    host.bootstrap()
    reference, assignment = host.assignment('policy-guard-root', 'setter')
    context_ref = host.context('policy-guard-selection', reference, assignment, phase='selection', start=False)
    state = host.store.read()
    projection = state.assignment_routing(assignment)
    descriptor = projection['snapshot']['descriptor']
    identifier = descriptor['instruction_blobs']['software-engineer']
    path = host.store.material / identifier
    raw = path.read_bytes()
    path.unlink()
    try:
        assert state.assignment_routing(assignment) == projection
        with pytest.raises(OSError):
            host.store._blob(identifier)
    finally:
        assert host.store.put_blob(raw) == identifier
    path.write_bytes(b'Corrupted current instruction bytes.')
    try:
        assert state.assignment_routing(assignment) == projection
        with pytest.raises(lc.ERROR) as failure:
            host.store._blob(identifier)
        assert failure.value.code == 'P_INTEGRITY'
    finally:
        path.unlink()
        assert host.store.put_blob(raw) == identifier
    original_count = projection['snapshot']['catalogue']['count']
    original_model = projection['bootstrap']['model_selector']
    projection['snapshot']['instructions'].clear()
    projection['snapshot']['catalogue']['roles'].clear()
    projection['bootstrap']['model_selector'] = 'caller-poisoned-model'
    projection['capabilities']['limits'].clear()
    fresh = state.assignment_routing(assignment)
    assert len(fresh['snapshot']['instructions']) == original_count
    assert len(fresh['snapshot']['catalogue']['roles']) == original_count
    assert fresh['bootstrap']['model_selector'] == original_model
    assert fresh['capabilities']['limits']
    context = state.resolve(context_ref, 'context')
    execution = state.context_execution(context)
    execution['snapshot']['instructions'].clear()
    execution['snapshot']['catalogue']['roles'].clear()
    execution['bootstrap']['model_selector'] = 'caller-poisoned-chooser'
    execution['allowed_operations'].append('materialize')
    isolated = state.context_execution(context)
    assert len(isolated['snapshot']['instructions']) == original_count
    assert len(isolated['snapshot']['catalogue']['roles']) == original_count
    assert isolated['bootstrap']['model_selector'] == original_model
    assert isolated['allowed_operations'] == ['read']
    assert state.assignment_routing(assignment)['snapshot'] == fresh['snapshot']
    assert host.store.read().assignment_routing(assignment)['snapshot'] == fresh['snapshot']
