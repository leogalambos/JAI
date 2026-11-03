# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""One actual acyclic adjacent-layer receiving and assignment transfer."""
import copy
import hashlib
import json

import pytest

from governed_fixtures import GovernedHarness, QUESTIONS, lc


def test_reviewed_layer_one_handoff_receives_layer_two_acceptance_before_next_setter(tmp_path, monkeypatch):
    # This single integration scenario deliberately declares a finite workload
    # allowance; ordinary expiry regressions retain their short default leases.
    host = GovernedHarness(tmp_path, monkeypatch, use_scopes=('default', 'receiving'),
                            scenario_duration_ms=90 * 60 * 1000)
    host.bootstrap(include_neighbor=True)
    shared_input = copy.deepcopy(host.input_a)
    _, independent_output, _ = host.qualified_answer(suffix='independent-default-scope')
    host.accept(independent_output)
    host.accept(independent_output, release=True)
    host.enter_scope('receiving')
    coordinator_owner = host.owner(layer=1, work_kind='integration')
    upstream, upstream_body = host.assignment('layer-one-coordinator', 'setter',
                                               owner=coordinator_owner)
    answers = []
    for question in QUESTIONS:
        issuer_context = host.context('question-' + question + '-issuer', upstream, upstream_body)
        question_inputs = [{'slot_id': 'L1:service-controls:' + question + '-input',
                            'refs': [host.input_a]},
                           {'slot_id': 'inherited-l0-criteria', 'refs': [host.criteria]}]
        host.assignment('owned-question-setter-' + question, 'setter', owner=host.owner(question),
            creator={'kind': 'assignment', 'ref': upstream}, creator_context=issuer_context,
            inputs=question_inputs)
        _, answer, _ = host.qualified_answer(question=question, suffix='question-' + question)
        answers.append(answer)
    standard = [{'slot_id': 'L1:service-controls:how-input', 'refs': [host.input_a]}]
    integrator = host.setup_author(suffix='bundle-author', responsibility='integrator', work_kind='integration',
        inputs=standard + [{'slot_id': 'question-answers', 'refs': answers}])
    bundle, body = host.product('integrated-bundle', integrator, kind='bundle',
                               related=[{'slot_id': 'answers', 'refs': answers}])
    host.commit(host.submission(integrator, bundle, body))
    integration_review, _ = host.review(integrator, bundle, suffix='independent-integration',
                                        assessment_kind='integration')
    host.select_proof(bundle, integration_review, role='integration_review')
    integration_task = host.setup_author(suffix='integration-delivery', responsibility='integrator', work_kind='integration',
        inputs=standard + [{'slot_id': 'bundle', 'refs': [bundle]},
                           {'slot_id': 'integration-review', 'refs': [integration_review]}])
    host.commit(host.message('integration', {'assignment': integration_task['author'],
                                            'bundle': bundle, 'answers': answers,
                                            'integration_review': integration_review},
                             sender=integration_task['principal'],
                             context=integration_task['author_context']))
    assert host.store.evaluate(bundle, scope='receiving')['qualified']
    handoff_actor = host.setup_author(suffix='handoff-author', responsibility='integrator', work_kind='integration',
        inputs=standard + [{'slot_id': 'bundle', 'refs': [bundle]},
                           {'slot_id': 'interface', 'refs': [host.criteria]}])
    handoff, _ = host.product('offered-handoff', handoff_actor, kind='handoff',
        related=[{'slot_id': 'bundle', 'refs': [bundle]},
                 {'slot_id': 'interface', 'refs': [host.criteria]}])
    host.commit(host.message('handoff', {'assignment': handoff_actor['author'], 'handoff': handoff,
                                        'bundle': bundle, 'interface': host.criteria,
                                        'obligations': host.l0_sources},
                             sender=handoff_actor['principal'], context=handoff_actor['author_context']))
    assert not host.store.evaluate(handoff, scope='receiving')['qualified']
    offered = {'ref': handoff, 'use_scope': host.scope}
    before = host.path.read_bytes()
    with pytest.raises(lc.ERROR) as premature:
        host.store.read().local_entry(offered, 'setter', integration_review)
    assert premature.value.code == 'P_PROOF'
    assert host.path.read_bytes() == before
    proposal = host.store.read().local_entry(offered, 'receiver')
    receiver_body = proposal['record']
    receiver = host.record(proposal['logical_id'], 'assignment', receiver_body)
    owner = receiver_body['owner']
    receiver_context = host.context('actual-receiver', receiver, receiver_body)
    closure = host.store.read().assessment_closure(handoff, receiver)
    assessment = {'owner': owner, 'assessment_kind': 'receiving', 'assignment': receiver,
                  'subject': handoff, 'criteria': host.criteria, 'profile': host.profile,
                  'assessed_closure': closure,
                  'assessed_hash': hashlib.sha256(lc.canonical(closure)).hexdigest(),
                  'verdict': 'accepted', 'findings': [], 'conditions': []}
    principal = {'kind': 'assignment', 'ref': receiver}
    acceptance = host.record('receiving-acceptance', 'assessment', assessment,
                             sender=principal, context=receiver_context)
    host.commit(host.message('handoff_acceptance', {'assessment': acceptance, 'handoff': handoff,
                                                   'interface': host.criteria, 'verdict': 'accepted',
                                                   'findings': []},
                             sender=principal, context=receiver_context))
    assert {'ref': handoff, 'use_scope': 'receiving'} in closure
    host.select_proof(handoff, acceptance, role='receiving_acceptance')
    assert host.store.evaluate(handoff, scope='receiving')['qualified']
    proposal = host.store.read().local_entry(offered, 'setter', acceptance)
    next_body = proposal['record']
    next_setter = host.record(proposal['logical_id'], 'assignment', next_body)
    host.setters[(host.scope, json.dumps(next_body['owner'], sort_keys=True))] = (next_setter, next_body)
    assert host.store.read().assignment_states[upstream['version_id']] == 'open'
    clarification_context = host.context('bounded-upper-clarification', upstream, upstream_body)
    assert clarification_context != receiver_context
    assert host.store.read().resolve(clarification_context, 'context')['expires_at_ms'] <= upstream_body['deadline_ms']
    host.cancel_run(clarification_context)
    assert host.store.read().assignment_states[upstream['version_id']] == 'open'
    host.enter_scope('receiving')
    next_context = host.context('layer-two-work', next_setter, next_body)
    state = host.store.read()
    assert state.resolve(next_context, 'context')['assignment'] == next_setter
    assert state.assignment_states[next_setter['version_id']] == 'open'
    assert next_body['issued_under'] == receiver_body['issued_under']
    assert next_body['use_scope'] == offered['use_scope']
    assert next_body['inputs'][-1]['refs'] == [acceptance]
    assert state.run_states[state.resolve(next_context, 'context')['run_id']] == 'running'
    question_inputs = copy.deepcopy(next_body['inputs']) + [
        {'slot_id': 'L2:service-controls:how-input', 'refs': [next_body['criteria']]}]
    criteria_scope = next(item['use_scope'] for item in next_body['input_uses'] if item['at'] == '/criteria')
    question_uses = copy.deepcopy(next_body['input_uses']) + [
        {'at': f'/inputs/{len(next_body["inputs"])}/refs/0', 'use_scope': criteria_scope}]
    host.assignment('layer-two-question-how-setter', 'setter', owner=host.owner(layer=2),
        creator={'kind': 'assignment', 'ref': next_setter}, creator_context=next_context,
        inputs=question_inputs, input_uses=question_uses)
    lower_actor = host.setup_author(layer=2, suffix='dependent-layer-two')
    child_ref, child = lower_actor['author'], lower_actor['author_record']
    child_context = lower_actor['author_context']
    foreign = host.store.read().resolve(answers[0], 'product')
    stolen = host.submission(lower_actor, answers[0], foreign)
    before = host.path.read_bytes()
    response = host.send(stolen)
    assert response['status'] == 'rejected' and response['error']['code'] == 'P_SCOPE'
    assert host.path.read_bytes() == before
    host.cancel_run(child_context)
    lower_actor['author_context'] = host.context('fresh-layer-two-author-run', child_ref, child)
    dependent_output, dependent_body = host.product('dependent-layer-two-output', lower_actor)
    host.commit(host.submission(lower_actor, dependent_output, dependent_body))
    wrong_layer = host.prepare_review(lower_actor, dependent_output, suffix='wrong-upstream-review')
    wrong_layer['record']['subject'] = answers[0]
    _, wrong_review = host.assessment_delivery(wrong_layer, answers[0])
    before = host.path.read_bytes()
    response = host.send(wrong_review)
    assert response['status'] == 'rejected' and response['error']['code'] == 'P_PROOF'
    assert host.path.read_bytes() == before
    host.cancel_run(wrong_layer['context'])
    reviewer_id = host.store.read().resolve(wrong_layer['assignment'], 'assignment')['assigned_actor']
    lower_review, _ = host.review(lower_actor, dependent_output, suffix='independent-layer-two-review',
                                 actor_id=reviewer_id)
    host.select_proof(dependent_output, lower_review)
    host.select_basis(lower_actor, dependent_output)
    host.accept(dependent_output)
    host.accept(dependent_output, release=True)
    assert host.store.evaluate(dependent_output, scope='receiving')['release_eligible']
    receipt, _, _ = host.transition_inputs('The upstream owner changed the received conditions.\n')
    assert {'ref': dependent_output, 'use_scope': 'receiving'} in receipt['affected_uses']
    assert {'ref': independent_output, 'use_scope': 'default'} not in receipt['affected_uses']
    assert not host.store.evaluate(dependent_output, scope='receiving')['release_eligible']
    assert host.store.evaluate(independent_output, scope='default')['release_eligible']
    assert host.store.read().resolve(shared_input, 'source')['source_role'] == 'input'
