# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Indexed selectors preserve the historical scan's precise applicability rules."""
import copy

import lifecycle as lc


def _scan(state, point):
    """The pre-index algorithm, retained only as an independent parity oracle."""
    result = []
    for event in state.events:
        if event['kind'] != 'selection':
            continue
        category = event['category']
        latest = next((other for other in reversed(state.events)
                       if other['kind'] == 'selection' and other['category'] == category
                       and other['scope'] == event['scope'] and other['slot'] == event['slot']
                       and other['subject'] == event['subject']), None)
        if category != 'review-lineage' and latest != event:
            continue
        if category == 'basis' and state.selections.get(lc._proof_key(event['scope'], event['slot'])) != event['subject']:
            continue
        if category in {'proof', 'review-lineage'}:
            current = state.proofs.get(lc._proof_key(event['scope'], event['slot']))
            if current is None or current['proof'] != event['subject'] or current['proof_use_scope'] != event['use_scope']:
                continue
        if category == 'source' and state.sources.get((event['scope'], event['slot']['logical_id'])) != event['subject']:
            continue
        if state._point(event['subject'], event['use_scope']) == point:
            result.append(event)
    if state.versions[point['ref']['version_id']]['kind'] == 'delivery.decision':
        result.extend(event for event in state.events if event['kind'] == 'selection'
                      and event['decision_ref'] == point['ref'] and event['scope'] == point['use_scope']
                      and event not in result)
    return result


def test_index_preserves_scope_latest_lineage_decision_order_and_fork_isolation():
    state = lc.State('selection-index')
    def ref(name):
        return {'engagement': state.engagement, 'scope': 'origin', 'logical_id': name, 'version_id': name}
    subject, other, decision = ref('subject'), ref('other'), ref('decision')
    for item, kind in [(subject, 'product'), (other, 'product'), (decision, 'decision')]:
        state.versions[item['version_id']] = lc._freeze({'kind': 'delivery.' + kind})
    slot = {'kind': 'basis', 'owner': {'layer': 1}, 'slot_id': 'answer'}
    proof_slot = {'kind': 'proof', 'subject': subject}
    for category, use_scope, selected_slot in [('basis', 'old', slot), ('basis', 'current', slot),
            ('proof', 'current', proof_slot), ('review-lineage', 'current', proof_slot),
            ('review-lineage', 'current', proof_slot), ('applicability', 'current', {'kind': 'use'})]:
        state._selection_event(category, 'current', selected_slot, subject, use_scope, decision, {}, None)
    state._selection_event('source', 'current', {'logical_id': 'input'}, other, 'current', decision, {}, None)
    state.selections[lc._proof_key('current', slot)] = subject
    state.proofs[lc._proof_key('current', proof_slot)] = {'proof': subject, 'proof_use_scope': 'current'}
    state.sources[('current', 'input')] = other
    for item in [subject, other, decision]:
        for scope in ['current', 'old']:
            point = {'ref': item, 'use_scope': scope}
            assert state._point_establishments(point) == _scan(state, point)
    fork = state._fork()
    before = copy.deepcopy(state._point_establishments({'ref': subject, 'use_scope': 'current'}))
    fork._selection_event('applicability', 'current', {'kind': 'use'}, subject, 'current', other, {}, None)
    assert state._point_establishments({'ref': subject, 'use_scope': 'current'}) == before
    assert len(fork.events) == len(state.events) + 1
    assert fork.events[0] is state.events[0]
