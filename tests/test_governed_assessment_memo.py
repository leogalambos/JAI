# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Completed checks are reused only inside one stable recursive assessment."""
import copy

import pytest

from governed_fixtures import GovernedHarness
from test_governed_sabsa_runtime import ContentHarness
import governed_sabsa as content
import lifecycle as lc


def test_product_requirements_success_failure_and_context_are_walk_local(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='product-walk-memo')
    host.bootstrap()
    actor = host.setup_author(suffix='walk-author')
    subject, record = host.product('walk-answer', actor)
    state = host.store.read()
    checked = []
    original = state._check_product_requirements

    def observed(value, live):
        checked.append((lc.canonical(value), state.scope, live))
        return original(value, live)

    monkeypatch.setattr(state, '_check_product_requirements', observed)

    @lc._within_assessment
    def assess(current):
        current._product_requirements(record)
        current._product_requirements(copy.deepcopy(record))
        assert len(checked) == 1
        current._product_requirements(record, live=False)
        assert len(checked) == 2
        bad = copy.deepcopy(record)
        bad['evidence'] = [subject]  # An answer cannot serve as an observation.
        for _ in range(2):
            with pytest.raises(lc.ERROR):
                current._product_requirements(bad)
        assert len(checked) == 4

    assess(state)
    assert state._assessment_walk is None
    state._product_requirements(record)
    assert len(checked) == 5
    # Cancellation must be observed by a new assessment, not inherited as PASS.
    state.states[(host.scope, host.input_a['version_id'])] = {'validity': 'invalid', 'applicable': False}
    with pytest.raises(lc.ERROR):
        state._product_requirements(record)
    assert len(checked) == 6


def test_content_validation_copies_payload_and_rechecks_new_walk_material(tmp_path, monkeypatch):
    host = ContentHarness(tmp_path, monkeypatch, engagement='content-walk-memo')
    host.bootstrap()
    actor, subject = host.deliver_content('memo-content')
    state = host.store.read()
    record = copy.deepcopy(state.resolve(subject, 'product'))
    # This is NEW local material, not a request to revalidate an admitted parent.
    record['material'] = [host.store.put_blob(lc.canonical(host.semantic(private=False)))]
    checked = []
    original = content._validate_product

    def observed(current, value, scope, live):
        checked.append((scope, current.scope, live))
        return original(current, value, scope, live)

    monkeypatch.setattr(content, '_validate_product', observed)

    @lc._within_assessment
    def assess(current):
        payload = content.validate_product(current, record, host.scope)
        payload['units'].clear()
        assert content.validate_product(current, record, host.scope)['units']
        assert len(checked) == 1
        content.validate_product(current, record, host.scope, live=False)
        content.validate_product(current, record, 'other-content-scope')
        current.scope = 'other-ambient-scope'
        content.validate_product(current, record, host.scope)
        assert len(checked) == 4
        current.scope = host.scope

    assess(state)
    assert state._assessment_walk is None
    material = host.store.material / record['material'][0]
    material.unlink()
    # Both attempts are new assessments; neither may inherit the successful read.
    for _ in range(2):
        with pytest.raises(lc.ERROR):
            content.validate_product(state, record, host.scope)
    assert len(checked) == 6


def test_active_assessment_fork_reassesses_changed_holds_without_copying_walk(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='fork-assessment-boundary')
    host.bootstrap()
    _, subject, _ = host.qualified_answer(suffix='fork-current-answer')
    state = host.store.read()
    point = (host.scope, subject['version_id'])

    class AssessmentScratch:
        """An active assessment is ephemeral work, never snapshot-owned data."""

        def __deepcopy__(self, memo):
            raise AssertionError('A fork must not copy active assessment scratch')

    @lc._within_assessment
    def assess(current):
        assert current.evaluate(subject, host.scope)['qualified']
        current._assessment_walk['scratch'] = AssessmentScratch()
        changed = current._fork()
        assert changed._assessment_walk is None
        changed.holds[point] = {'episode': None, 'grant': None}
        assert not changed.evaluate(subject, host.scope)['qualified']
        assert current.evaluate(subject, host.scope)['qualified']
        changed.holds.pop(point)
        assert changed.evaluate(subject, host.scope)['qualified']

    assess(state)
    assert state._assessment_walk is None
