# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Lawful same-setter decisions batch atomically under the shared interpreter."""
import time

from governed_fixtures import GovernedHarness, CONTROLLER, lc


def _criteria(host, context, setter, owner, name):
    return host.record(name, 'source', {'owner': owner, 'source_role': 'criteria',
        'origin': {'kind': 'assignment', 'ref': setter},
        'material': [host.material('Owned local criterion ' + name)],
        'criteria': [{'id': 'C1', 'requirement': host.input_a,
                      'statement': 'Preserve the exact inherited input.', 'evidence_slots': []}],
        'inherited': host.l0_sources}, sender={'kind': 'assignment', 'ref': setter}, context=context)


def _completion(host, setter, context, subjects):
    returned = {'assignment': setter, 'context': context,
        'records': host.pending[context['version_id']],
        'intents': [{'message_type': 'decision', 'recipient': CONTROLLER,
                    'payload': {'action': 'invalidate', 'reason': 'Retire the exact owned local criterion.',
                                'subjects': [subject]}} for subject in subjects]}
    issued = host.store.read().resolve(context, 'context')
    return host.message('control_event', {'event': 'run_completed', 'run_context': context,
        'run_id': issued['run_id'], 'observed_at_ms': int(time.time() * 1000),
        'return_blob_id': host.store.put_blob(lc.canonical(returned)),
        'usage': [{'metric': 'tokens', 'unit': 'governed-token', 'total': 1}]})


def test_owned_decisions_batch_but_a_foreign_second_decision_cannot_partially_commit(tmp_path, monkeypatch):
    # This is an explicitly synthetic producer boundary for the Store contract;
    # real native professional execution is tested in the local-layer scenario.
    host = GovernedHarness(tmp_path, monkeypatch, engagement='owned-setter-batch')
    host.bootstrap()
    setter, body = host.assignment('local-setter', 'setter')
    context = host.context('owned-batch', setter, body)
    first = _criteria(host, context, setter, body['owner'], 'first-local-criterion')
    second = _criteria(host, context, setter, body['owner'], 'second-local-criterion')
    host.commit(_completion(host, setter, context, [first, second]))
    state = host.store.read()
    assert state._status(first)['validity'] == 'invalid'
    assert state._status(second)['validity'] == 'invalid'
    assert state.assignment_states[setter['version_id']] == 'open'
    context = host.context('foreign-second', setter, body)
    third = _criteria(host, context, setter, body['owner'], 'third-local-criterion')
    message = _completion(host, setter, context, [third, host.input_a])
    before = host.path.read_bytes()
    response = host.send(message)
    assert response['status'] == 'rejected', response
    assert response['error']['code'] == 'P_SCOPE', response
    assert host.path.read_bytes() == before
    state = host.store.read()
    assert third['version_id'] not in state.versions
    assert state._status(host.input_a)['validity'] == 'valid'
