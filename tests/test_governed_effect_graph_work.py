# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Bound graph work to changed edges, using actual in-memory State primitives.

These probes isolate graph construction and traversal cost; they do not establish
signed origin, accepted journal history or human authority. Signed Store tests
independently cover ingress, replay, concurrency and atomic persistence.
"""
import copy

import pytest

from governed_fixtures import HUMAN, delivery, lc


ENGAGEMENT = 'bounded-graph-probe'
MESSAGE = {'scope': 'default'}


def _source(name, inherited=()):
    record = {'owner': HUMAN, 'source_role': 'input', 'origin': HUMAN,
              'material': [lc.blob(('Fictional graph input ' + name).encode())],
              'criteria': [], 'inherited': copy.deepcopy(list(inherited))}
    return lc.record_manifest(ENGAGEMENT, 'default', name, 'source', record)


def _registration(value, dependencies=()):
    return {'op': 'register', 'manifest': value, 'dependencies': list(dependencies),
            'use_scope': 'default', 'origin': HUMAN, 'context': None}


def _prefix(size=100):
    state = lc.State(ENGAGEMENT)
    effects = []
    for index in range(size):
        value = _source('existing-' + str(index))
        effects.extend([_registration(value),
                        {'op': 'qualify', 'subject': lc.version_id(value)}])
    state._apply(effects, MESSAGE, {}, None)
    return state


def test_no_edge_effects_do_not_walk_the_existing_dependency_prefix(monkeypatch):
    state = _prefix()
    graph = copy.deepcopy(state.reliance)
    statuses = copy.deepcopy(state.states)
    versions = copy.deepcopy(state.versions)
    calls = []
    closure = state._closure

    def observed_closure(reference, scope=None):
        calls.append((reference, scope))
        return closure(reference, scope)

    monkeypatch.setattr(state, '_closure', observed_closure)
    state._apply([], MESSAGE, {}, None)
    assert calls == [], 'An empty effect batch must not revalidate an unchanged graph.'
    state._apply([{'op': 'counter', 'key': 'local-work-count', 'count': 1}], MESSAGE, {}, None)
    assert state.counters['local-work-count'] == 1
    assert calls == [], 'An effect adding no edge must not scan the accepted prefix.'
    assert state.reliance == graph and state.states == statuses and state.versions == versions


def test_new_scoped_import_visits_its_dependencies_and_rejects_an_active_cycle(monkeypatch):
    state = _prefix()
    parent = state._reference(next(iter(state.versions)))
    value = _source('new-dependent', [parent])
    child = lc._ref(value)
    state._apply([_registration(value, [state._point(parent, 'default')])], MESSAGE, {}, None)
    assert state.reliance[state._key(child, 'default')] == [state._point(parent, 'default')]
    calls = []
    resolve = state.resolve

    def observed_resolve(reference, kind=None):
        calls.append(reference['version_id'])
        return resolve(reference, kind)

    monkeypatch.setattr(state, 'resolve', observed_resolve)
    previous = copy.deepcopy(state.states)
    state._ensure_use(state._point(child, 'imported'))
    assert set(calls) == {child['version_id'], parent['version_id']}
    assert len(calls) == 2, 'An import must not revisit unrelated existing points.'
    assert set(state.states) - set(previous) == {('imported', child['version_id']),
                                                ('imported', parent['version_id'])}
    assert state.reliance[state._key(child, 'imported')] == [state._point(parent, 'imported')]

    # Build a separate NEW graph probe; admitted prefix records remain immutable.
    probe = lc.State(ENGAGEMENT)
    probe.versions = {parent['version_id']: _source(parent['logical_id'], [child]),
                      child['version_id']: value}
    probe._identities = {reference['version_id']: (ENGAGEMENT, 'default', reference['logical_id'])
                         for reference in (parent, child)}
    previous = copy.deepcopy(probe.states)
    with pytest.raises(lc.ERROR) as cycle:
        probe._ensure_use(probe._point(child, 'cycle-probe'))
    assert cycle.value.code == 'P_CONFLICT'
    assert probe.states == previous



def test_new_edge_prerequisites_must_exist_before_either_immutable_index_changes():
    state = _prefix(1)
    parent = state._reference(next(iter(state.versions)))
    missing = {**parent, 'logical_id': 'future-parent', 'version_id': 'f' * 64}
    value = _source('unavailable-parent', [missing])
    versions, identities, statuses = (copy.deepcopy(state.versions),
                                      copy.deepcopy(state._identities), copy.deepcopy(state.states))
    with pytest.raises(lc.ERROR) as unavailable:
        state._apply([_registration(value, [state._point(missing, 'default')])], MESSAGE, {}, None)
    assert unavailable.value.code == 'P_CONTEXT'
    assert state.versions == versions and state._identities == identities and state.states == statuses

    message = {'protocol': delivery.PROTOCOL, 'message_type': 'decision',
               'engagement': ENGAGEMENT, 'scope': 'default', 'request_id': 'self-reference',
               'sender': HUMAN, 'context': None, 'message_id': '0' * 64,
               'payload': {'action': 'terminate', 'reason': 'Graph boundary probe only.',
                           'subjects': [], 'authority_proof': None}}
    message['message_id'] = delivery.message_id(message)
    value = state._decision_manifest(message)
    with pytest.raises(lc.ERROR) as self_reference:
        state._apply([{'op': 'decision-record', 'manifest': value,
                       'dependencies': [state._point(lc._ref(value), 'default')]}], message, {}, None)
    assert self_reference.value.code == 'P_CONTEXT'
    assert state.versions == versions and state._identities == identities and state.states == statuses
