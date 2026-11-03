# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Pure cohort identity ignores aliases without admitting any professional work."""
import copy

from governed_fixtures import GovernedHarness


def test_scoped_generation_deduplicates_aliases_but_retains_meaningful_input_versions(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='review-cohort')
    host.bootstrap()
    state = host.store.read()
    # The identity projection treats references as opaque; this is not an
    # assignment admission or an assertion that an assessment is authorized.
    record = {'owner': host.owner(), 'responsibility': 'reviewer', 'profile': host.profile,
              'criteria': host.criteria, 'use_scope': host.scope, 'input_uses': [],
              'inherited': [host.input_a, host.criteria],
              'inputs': [{'slot_id': 'assessed-subject', 'refs': [host.profile]},
                         {'slot_id': 'task-input', 'refs': [host.input_a]}]}
    original = state._review_generation(record)
    aliased = copy.deepcopy(record)
    aliased['inputs'][1]['slot_id'] = 'renamed-input'
    aliased['inputs'].extend([{'slot_id': 'duplicate-input', 'refs': [host.input_a]},
                              {'slot_id': 'subject-alias', 'refs': [host.profile]}])
    aliased['inherited'].extend([host.input_a, host.profile])
    assert state._review_generation(aliased) == original
    source = copy.deepcopy(state.resolve(host.input_a, 'source'))
    source['material'] = [host.material('A genuinely different governing input version.')]
    changed_ref = host.ref(host.input_a['logical_id'], 'source', source)
    changed = copy.deepcopy(record)
    changed['inherited'][0] = changed_ref
    changed['inputs'][1]['refs'] = [changed_ref]
    assert state._review_generation(changed) != original
