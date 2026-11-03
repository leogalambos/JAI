# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Pending root qualification must not establish governing use or permissions."""
import copy

import pytest

from governed_fixtures import GovernedHarness


@pytest.mark.parametrize('barrier', ['none', 'unknown_scope', 'held', 'invalid', 'expired', 'withdrawn', 'superseded'])
def test_pending_root_qualification_respects_exact_use_barriers(tmp_path, monkeypatch, barrier):
    host = GovernedHarness(tmp_path, monkeypatch)
    host.bootstrap()
    _, candidate, _ = host.qualified_answer(select_basis=False)
    state = host.store.read()
    scope = host.scope
    key = state._key(candidate, scope)
    if barrier == 'unknown_scope':
        scope = 'unregistered'
    elif barrier == 'held':
        state.holds[key] = {'reason': 'review hold'}
    elif barrier == 'invalid':
        state.states[key] = {'validity': 'invalid', 'applicable': False}
    elif barrier == 'expired':
        state._use_changes[key] = {'use_until_ms': 0}
    elif barrier == 'withdrawn':
        state._use_changes[key] = {'withdrawn_at': 1}
    elif barrier == 'superseded':
        state.events.append({'kind': 'selection', 'category': 'basis', 'scope': scope,
                             'slot': {'kind': 'basis', 'owner': state.resolve(candidate)['owner'],
                                      'slot_id': 'retired'}, 'subject': candidate})
    before = copy.deepcopy((state.states, state.selections, state.decisions))
    result = state.evaluate(candidate, scope, live=False)
    assert result['qualified'] == (barrier == 'none'), result
    assert not result['accepted']
    assert not result['release_eligible']
    assert (state.states, state.selections, state.decisions) == before
