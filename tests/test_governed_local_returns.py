# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""A coordinator consumes profile-governed local outputs, including observations."""
import copy

import pytest

from governed_fixtures import GovernedHarness, delivery
import lifecycle as lc


class _MeasurementHouse(GovernedHarness):
    """Declare one local measurement work item in the real bootstrap profile."""

    def bootstrap_message(self, **kwargs):
        kwargs['include_neighbor'] = True
        message = super().bootstrap_message(**kwargs)
        profile = message['payload']['profile']['record']
        owner = self.owner(work_kind='measurement')
        owner['question'] = None
        for role, kind in [('answer', 'product'), ('professional_review', 'assessment')]:
            profile['obligations'].append({'slot_id': 'local-measurement-' + role,
                'owner': owner, 'subject_kind': 'observation', 'role': role,
                'required_kind': kind, 'minimum': 1, 'maximum': 1,
                'allow_exclusion': False, 'exclusion_owner': None})
        self.profile = self.ref('profile', 'profile', profile)
        message['message_id'] = delivery.message_id(message)
        return message


def test_coordinator_accepts_only_selected_actual_local_measurement_return(tmp_path, monkeypatch):
    host = _MeasurementHouse(tmp_path, monkeypatch, engagement='local-measurement-return')
    host.bootstrap()
    coordinator, root = host.assignment('integration-coordinator', 'setter',
        owner=host.owner(work_kind='integration'))
    issuer = host.context('measurement-issuer', coordinator, root)
    owner = host.owner(work_kind='measurement')
    owner['question'] = None
    setter, assigned = host.assignment('measurement-setter', 'setter', owner=owner,
        creator={'kind': 'assignment', 'ref': coordinator}, creator_context=issuer,
        inputs=copy.deepcopy(root['inputs']))
    actor = host.setup_author(question=None, work_kind='measurement', responsibility='measurement', suffix='actual-probe')
    assert actor['setter'] == setter
    subject, record = host.product('actual-observation', actor, kind='observation',
        material=[host.material('Actual deterministic fixture probe: successful=1; scheduled=1.')])
    host.commit(host.message('observation', {'assignment': actor['author'], 'observation': subject,
        'inputs': lc._input_locators(record['inputs']), 'material': record['material']},
        sender=actor['principal'], context=actor['author_context']))
    inputs = copy.deepcopy(root['inputs']) + [{'slot_id': 'local-observation', 'refs': [subject]}]
    consumer_context = host.context('pending-observation-consumer', coordinator, root)
    with pytest.raises(AssertionError) as pending:
        host.assignment('unreviewed-observation-consumer', 'integrator', owner=root['owner'],
            creator={'kind': 'assignment', 'ref': coordinator}, creator_context=consumer_context, inputs=inputs)
    assert pending.value.args[0]['error']['code'] == 'P_SCOPE'
    host.cancel_run(consumer_context)
    review, _ = host.review(actor, subject, suffix='actual-probe-review', actor_id='independent-probe-reviewer')
    host.select_proof(subject, review)
    host.select_basis(actor, subject)
    consumer_context = host.context('selected-observation-consumer', coordinator, root)
    consumer, record = host.assignment('reviewed-observation-consumer', 'integrator', owner=root['owner'],
        creator={'kind': 'assignment', 'ref': coordinator}, creator_context=consumer_context, inputs=inputs)
    state = host.store.read()
    assert state.resolve(consumer, 'assignment') == record
    assert state._governing_input(state._point(subject), live=True)
    assert state._produced_under(subject, coordinator, root['owner'])
