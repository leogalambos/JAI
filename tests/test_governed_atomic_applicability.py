# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""A replacement cannot consume support that its own transition withdraws."""
import copy

from governed_fixtures import GovernedHarness
import lifecycle as lc


def test_replacement_rejects_a_condition_depending_on_its_superseded_proof(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='atomic-local-support')
    host.bootstrap()
    actor, subject, previous = host.qualified_answer(suffix='supported-answer')
    dependent_actor = copy.deepcopy(actor)
    dependent_actor['author_record']['inputs'].append({'slot_id': 'proof-observed', 'refs': [previous]})
    condition, _, observation = host.observation(dependent_actor, 'An observation of this exact review.', suffix='dependent-condition')
    host.commit(observation)
    state = host.store.read()
    old_review = state.resolve(previous, 'assessment')
    reviewer = state.resolve(old_review['assignment'], 'assignment')['assigned_actor']
    prepared = host.prepare_review(actor, subject, suffix='conditional-replacement', actor_id=reviewer,
        verdict='supported_with_conditions', evidence=[{'slot_id': 'replacement-condition', 'refs': [condition]}])
    prepared['record']['conditions'] = [condition]
    replacement, review = host.assessment_delivery(prepared, subject)
    host.commit(review)
    slot = {'kind': 'proof', 'subject': subject, 'role': 'professional_review',
            'slot_id': 'L1:service-controls:how-professional_review'}
    message = host.owner_decision(actor['owner'], {'action': 'select',
        'reason': 'Replace the exact local proof with a conditional review.',
        'slot': slot, 'candidate': replacement, 'previous': previous},
        inputs=[{'slot_id': 'assessed-subject', 'refs': [subject]},
                {'slot_id': 'assessed-proof', 'refs': [replacement]}])
    before = host.path.read_bytes()
    response = host.send(message)
    assert response['status'] == 'rejected' and response['error']['code'] == 'P_PROOF', response
    assert host.path.read_bytes() == before
    current = host.store.read()
    assert current.proofs[lc._proof_key(host.scope, slot)]['proof'] == previous
    assert current._status(subject, host.scope)['applicable']
    assert current._status(condition, host.scope)['applicable']
