# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Three real signed histories for pause, bounded risk, and productive readiness."""
import copy
import time

import pytest

from governed_fixtures import delivery, op
from governed_scheduling_fixtures import (
    SchedulingHarness, workflow, open_episode, affected_refs, owner_resolution,
    reconciliation, signed_grant, captured_choice, decision_ref, info_request,
)
import lifecycle as lc
from governed_dispatch import DispatchError


def _ready(state, reference):
    return next(item for item in state.readiness(reference['scope']) if item['assignment'] == reference)


class _EightStepHarness(SchedulingHarness):
    def bootstrap_message(self, **kwargs):
        """Declare the measured eight-step attempt bound before any state exists."""
        message = super().bootstrap_message(**kwargs)
        profile = message['payload']['profile']['record']
        profile['scheduling']['max_search_steps'] = 8
        self.profile = self.ref('profile', 'profile', profile)
        self._remember_proposal(self.profile, 'profile', profile)
        message['message_id'] = delivery.message_id(message)
        return message


def _handling_integrator(host, consumer, episode, *, suffix):
    entry = consumer.handling_entry(episode, 'collect')
    reference = entry['assignment']
    body = host.store.read().resolve(reference, 'assignment')
    context = host.context(suffix + '-issuer', reference, body)
    child, assigned = host.assignment(suffix, 'integrator', owner=body['owner'], token_limit=1000,
        creator={'kind': 'assignment', 'ref': reference}, creator_context=context)
    return {'owner': assigned['owner'], 'setter': reference, 'setter_record': body,
            'author': child, 'author_record': assigned,
            'author_context': host.context(suffix + '-context', child, assigned),
            'principal': {'kind': 'assignment', 'ref': child}}


def test_episode_revisions_pause_future_work_and_current_owner_resolves_changed_inputs_without_deadlock(tmp_path, monkeypatch):
    host = SchedulingHarness(tmp_path, monkeypatch, engagement='episode-owner-change')
    host.bootstrap(include_neighbor=True)
    consumer = workflow(host)
    actor = host.setup_author(suffix='paused-author', author_token_limit=1000)
    candidate, body = host.product('obsolete-late-candidate', actor)
    late = copy.deepcopy(host.outbound(host.submission(actor, candidate, body)))
    episode = open_episode(host, [actor['author']], decisive=False)
    state = host.store.read()
    original_package = copy.deepcopy(state.resolve(episode))
    conflicts = next(binding['refs'] for binding in original_package['related'] if binding['slot_id'] == 'conflicts')
    assert state.assignment_states[actor['author']['version_id']] == 'paused'
    assert not any(item['ready'] for item in consumer.ready())
    before = host.path.read_bytes()
    with pytest.raises(AssertionError) as future:
        host.assignment('future-productive-setter', 'setter', owner=host.owner('why'))
    assert future.value.args[0]['error']['code'] == 'P_STATE'
    assert host.path.read_bytes() == before

    late.update(request_id='actual-obsolete-late-return', expected_head=host.store.read().head)
    late['payload']['observed_at_ms'] = int(time.time() * 1000)
    late['message_id'] = delivery.message_id(late)
    assert host.send(late)['status'] == 'committed'
    state = host.store.read()
    run = state.resolve(actor['author_context'], 'context')['run_id']
    assert state.run_states[run] == 'quarantined'
    assert candidate['version_id'] not in state.versions
    first_resolution = owner_resolution(host, episode)

    collector = _handling_integrator(host, consumer, episode, suffix='actual-collector')
    current = host.store.read()._episode(episode)['current']
    revision, _ = host.product('collected-episode-revision', collector, kind='escalation',
        related=[{'slot_id': 'conflicts', 'refs': conflicts}],
        episode={'root': episode, 'previous': current, 'collection_head': host._proposal_head(),
                 'unfinished': [actor['author']], 'decisive': False})
    host.commit(host.message('escalation', {'assignment': collector['author'], 'package': revision,
        'conflicts': conflicts, 'affected': [actor['author']],
        'requested_decisions': ['Assess the complete collected local requirement conflict.']},
        sender=collector['principal'], context=collector['author_context']))
    state = host.store.read()
    assert state.resolve(episode) == original_package
    assert state._episode(episode)['current'] == revision
    assert len(state._episode(episode)['revisions']) == 2
    stale = reconciliation(host, episode, first_resolution)
    before = host.path.read_bytes()
    uncovered = host.send(host.message('decision', stale))
    assert uncovered['status'] == 'rejected' and uncovered['error']['code'] == 'P_PROOF'
    assert host.path.read_bytes() == before

    deadline = state._episode(episode)['collect_until_ms']
    with monkeypatch.context() as clock:
        clock.setattr(lc.time, 'time', lambda: (deadline + 1) / 1000)
        assert any(token.startswith('collection:closed:')
                   for token in host.store.read().ready_basis(collector['setter']))
        receipt, old_input, new_input = host.transition_inputs(
            'The actual owner revised the service requirement.', remove_old_material=True)
        owner_change = decision_ref(host, receipt, 'continue')
        control = consumer.handling_entry(episode, 'reconcile')['assignment']
        assert host.store.read().resolve(control, 'assignment')['criteria'] == host.criteria
        assert host.store.read().resolve(old_input, 'source')['material'] != host.store.read().resolve(new_input, 'source')['material']
        outcomes = {reference['version_id']: 'changed' for reference in affected_refs(host.store.read(), episode)}
        resolved = owner_resolution(host, episode, outcomes=outcomes, decisions=[owner_change])
        resume = reconciliation(host, episode, resolved,
            outcomes={identifier: 'discard' for identifier in outcomes})
        missing = copy.deepcopy(resume)
        missing['reconciliation'].pop()
        before = host.path.read_bytes()
        with pytest.raises(DispatchError) as incomplete:
            consumer.submit_decision(consumer.prepare_decision(missing)['message'])
        assert incomplete.value.code == 'P_STATE'
        assert host.path.read_bytes() == before
        assert consumer.submit_decision(consumer.prepare_decision(resume)['message'])['status'] == 'committed'
        state = host.store.read()
        assert state.escalations[episode['version_id']] == 'resolved'
        assert state.assignment_states[actor['author']['version_id']] == 'cancelled'
        fresh, assigned = host.assignment('new-current-input-root', 'setter')
        assert new_input in assigned['inherited'] and old_input not in assigned['inherited']
        assert state.resolve(episode) == original_package
        assert host.store.read().assignment_states[fresh['version_id']] == 'open'


def test_real_l0_speculation_shares_one_budget_accounts_late_cost_and_retains_only_explicit_unchanged_work(tmp_path, monkeypatch):
    host = SchedulingHarness(tmp_path, monkeypatch, engagement='signed-speculation')
    host.bootstrap(include_neighbor=True)
    actors = [host.setup_author(question=question, suffix=question, author_token_limit=1000,
                               start_author=False) for question in ('what', 'why', 'how')]
    episode = open_episode(host, [actor['author'] for actor in actors])
    consumer = workflow(host)
    state = host.store.read()
    before_usage = copy.deepcopy(state.usage)
    expiry = int(time.time() * 1000) + 30000
    grant, message, proof = signed_grant(host, episode,
        [actor['author'] for actor in actors], ceiling=1000, expires_at_ms=expiry, consumer=consumer)
    assert host.store.read().usage == before_usage, 'A grant is a ceiling, not a second reservation'
    assert host.store.read().assignment_states[actors[0]['author']['version_id']] == 'paused'
    unsigned = copy.deepcopy(message)
    unsigned.update(request_id='missing-human-speculative-risk', expected_head=host.store.read().head)
    unsigned['payload']['authority_proof'] = '0' * 64
    unsigned['message_id'] = delivery.message_id(unsigned)
    before = host.path.read_bytes()
    with pytest.raises(DispatchError) as no_consent:
        consumer.submit_decision(unsigned)
    assert no_consent.value.code == 'P_SCOPE'
    assert host.path.read_bytes() == before
    unsupported = copy.deepcopy(message['payload'])
    unsupported['limits'] = [{'metric': 'tokens', 'unit': 'governed-token', 'ceiling': 1000}]
    unsupported = consumer.prepare_decision(unsupported)
    unsupported_proof = host.human_proof(unsupported['message'], 'delivery-change')
    op.validate_human_intent_request(unsupported_proof['request'])
    with pytest.raises(DispatchError) as unknown_meter:
        consumer.submit_decision(unsupported['message'], unsupported_proof)
    assert unknown_meter.value.code == 'P_BUDGET'
    assert host.path.read_bytes() == before
    first = actors[0]
    selected_context = host.context('reserved-speculative-selection', first['author'], first['author_record'],
                                    phase='selection', speculation=grant)
    before = host.path.read_bytes()
    with pytest.raises(AssertionError) as contention:
        host.context('contended-speculative-selection', actors[1]['author'], actors[1]['author_record'],
                     phase='selection', speculation=grant)
    assert contention.value.args[0]['error']['code'] == 'P_BUDGET'
    assert host.path.read_bytes() == before
    choice = captured_choice(host, first, selected_context)
    first['author_context'] = host.context('first-speculative-work', first['author'], first['author_record'],
                                          selection=choice, speculation=grant)
    produced = []
    for index, actor in enumerate(actors[:2]):
        if index:
            actor['author_context'] = host.context('second-speculative-work', actor['author'],
                                                  actor['author_record'], speculation=grant)
        result, record = host.product('speculative-answer-' + str(index), actor)
        host.commit(host.submission(actor, result, record))
        produced.append(result)
    state = host.store.read()
    assert all((host.scope, reference['version_id']) in state.holds for reference in produced)
    assert all(not state.evaluate(reference)['qualified'] for reference in produced)
    assert all(state.assignment_states[actor['author']['version_id']] == 'completed' for actor in actors[:2])

    late_actor = actors[2]
    late_actor['author_context'] = host.context('late-speculative-work', late_actor['author'],
                                               late_actor['author_record'], speculation=grant)
    late_result, late_body = host.product('late-unauthorized-speculative-answer', late_actor)
    late = copy.deepcopy(host.outbound(host.submission(late_actor, late_result, late_body)))
    state = host.store.read()
    run = state.resolve(late_actor['author_context'])['run_id']
    before_spent = state.usage[(host.scope, 'elapsed_ms', 'ms')]['spent']
    with monkeypatch.context() as clock:
        clock.setattr(lc.time, 'time', lambda: (expiry + 1) / 1000)
        with pytest.raises(AssertionError) as expired:
            host.context('expired-grant-new-context', late_actor['author'], late_actor['author_record'],
                         phase='selection', speculation=grant)
        assert expired.value.args[0]['error']['code'] == 'P_EXPIRED'
        late.update(request_id='late-expired-grant-return', expected_head=host.store.read().head,
                    issued_at_ms=expiry + 1, expires_at_ms=expiry + 60001)
        late['payload']['observed_at_ms'] = expiry + 1
        late['payload']['usage'][0]['total'] = 2
        late['message_id'] = delivery.message_id(late)
        assert host.send(late)['status'] == 'committed'
        state = host.store.read()
        assert state.run_states[run] == 'quarantined'
        assert late_result['version_id'] not in state.versions
        assert state.usage[(host.scope, 'elapsed_ms', 'ms')]['spent'] == before_spent + 2
        assert state.usage[(host.scope, 'elapsed_ms', 'ms')]['reserved'] == 0
        impacts = {produced[0]['version_id']: 'changed'}
        resolution = owner_resolution(host, episode, outcomes=impacts)
        retain = reconciliation(host, episode, resolution)
        before = host.path.read_bytes()
        changed = host.send(host.message('decision', retain))
        assert changed['status'] == 'rejected' and changed['error']['code'] == 'P_CONTEXT'
        assert host.path.read_bytes() == before
        outcomes = {produced[0]['version_id']: 'discard'}
        resume = reconciliation(host, episode, resolution, outcomes=outcomes)
        conflicting = copy.deepcopy(resume)
        parent = next(item for item in conflicting['reconciliation'] if item['subject'] == actors[1]['setter'])
        parent['outcome'] = 'discard'
        child = next(item for item in conflicting['reconciliation'] if item['subject'] == produced[1])
        assert child['outcome'] == 'retain'
        conflicting['reconciliation'] = [child] + [item for item in conflicting['reconciliation']
            if item['subject'] not in (produced[1], actors[1]['setter'])] + [parent]
        before = host.path.read_bytes()
        holds_before = copy.deepcopy(host.store.read().holds)
        with pytest.raises(DispatchError) as inconsistent:
            consumer.submit_decision(consumer.prepare_decision(conflicting)['message'])
        assert inconsistent.value.code == 'P_CONTEXT'
        assert host.path.read_bytes() == before
        rejected = host.store.read()
        assert rejected.holds == holds_before
        assert rejected.escalations[episode['version_id']] == 'open'
        assert rejected.assignment_states[actors[1]['setter']['version_id']] == 'paused'
        assert consumer.submit_decision(consumer.prepare_decision(resume)['message'])['status'] == 'committed'
        state = host.store.read()
        assert not state.holds
        assert state._status(produced[0])['validity'] == 'invalid'
        assert state.resolve(produced[1])['assignment'] == actors[1]['author']
        assert state.assignment_states[actors[1]['author']['version_id']] == 'completed'
        assert not state.evaluate(produced[1])['qualified']
        assert not state.evaluate(produced[1])['accepted']
        review, _ = host.review(actors[1], produced[1], suffix='normal-post-reconciliation-review')
        host.select_proof(produced[1], review)
        host.select_basis(actors[1], produced[1])
        assert host.store.evaluate(produced[1])['qualified']
        assert not host.store.evaluate(produced[1])['accepted']


def test_readiness_consumes_delivered_facts_only_and_outcomes_do_not_claim_impossibility(tmp_path, monkeypatch):
    host = _EightStepHarness(tmp_path, monkeypatch, engagement='productive-readiness')
    host.bootstrap(include_neighbor=True)
    first = host.setup_author(question='what', suffix='first', start_author=False)
    other = host.setup_author(question='why', suffix='other', start_author=False)
    consumer = workflow(host)
    assert not _ready(host.store.read(), first['setter'])['ready']
    assert _ready(host.store.read(), first['author'])['ready']
    source = copy.deepcopy(host.store.read().resolve(host.input_a))
    source['material'] = [host.material('Unrelated unselected current source.')]
    host.record('unrelated-source-no-new-task', 'source', source)
    assert not _ready(host.store.read(), first['setter'])['ready']
    first['author_context'] = host.context('first-author-work', first['author'], first['author_record'])
    candidate, body = host.product('published-child-answer', first)
    host.commit(host.submission(first, candidate, body))
    state = host.store.read()
    assert _ready(state, first['setter'])['ready']
    root_context = host.context('parent-processing-delivered-facts', first['setter'], first['setter_record'])
    delivered = host.store.read().resolve(root_context)['ready_basis']
    other['author_context'] = host.context('other-author-work', other['author'], other['author_record'])
    incoming = info_request(host, other['author'], other['author_context'],
        recipient={'kind': 'assignment', 'ref': first['setter']}, question='A new relevant fact arrived during the parent run.')
    host.commit(incoming)
    assert host.store.read().ready_basis(first['setter']) != delivered
    host.commit(info_request(host, first['setter'], root_context))
    state = host.store.read()
    assert state.consumed_basis[first['setter']['version_id']] == delivered
    assert _ready(state, first['setter'])['ready'], 'A concurrent delivered fact must not be consumed retroactively'
    followup = host.context('parent-processing-new-fact', first['setter'], first['setter_record'])
    host.commit(info_request(host, first['setter'], followup))
    state = host.store.read()
    assert not _ready(state, first['setter'])['ready'], 'Own context/choice/audit noise must not create a busy loop'
    assert not next(item for item in consumer.ready() if item['assignment'] == first['setter'])['ready']
    with pytest.raises(lc.ERROR) as unbounded:
        consumer.drive(0)
    assert unbounded.value.code == 'P_BUDGET'
    exhausted = consumer.attempt_status(first['setter'])
    assert exhausted['steps'] == exhausted['step_limit'] == 8
    assert int(time.time() * 1000) < exhausted['deadline_ms']
    assert exhausted['outcome']['kind'] == 'search_exhausted'
    assert not host.store.evaluate(candidate)['qualified']
    before = host.path.read_bytes()
    with pytest.raises(DispatchError) as ninth_step:
        consumer.run(first['setter'], 'selection')
    assert ninth_step.value.code == 'P_STATE'
    assert host.path.read_bytes() == before
    assert consumer.attempt_status(first['setter'])['steps'] == 8

    final_actor = host.setup_author(suffix='honest-terminal', responsibility='integrator', work_kind='integration')
    attempt = final_actor['setter']
    assert consumer.attempt_status(attempt)['outcome'] is None
    result, result_body = host.product('honest-insufficient-information', final_actor, kind='final_result',
        outcome={'kind': 'insufficient_information', 'attempt': attempt, 'evidence': [host.criteria]})
    host.commit(host.submission(final_actor, result, result_body))
    assert consumer.attempt_status(attempt)['outcome']['kind'] == 'insufficient_information'
    claimant = host.setup_author(suffix='unproved-contradiction', responsibility='integrator', work_kind='integration')
    claim, claim_body = host.product('unproved-contradiction', claimant, kind='final_result',
        outcome={'kind': 'demonstrated_contradiction', 'attempt': attempt, 'evidence': [host.criteria]})
    before = host.path.read_bytes()
    unproved = host.send(host.submission(claimant, claim, claim_body))
    assert unproved['status'] == 'rejected' and unproved['error']['code'] == 'P_PROOF'
    assert host.path.read_bytes() == before
    assert claim['version_id'] not in host.store.read().versions
    assert consumer.attempt_status(attempt)['outcome']['kind'] == 'insufficient_information'
    host.cancel_run(claimant['author_context'])
    # Enroll the disposable human only when preparing the first reserved intent.
    _ = host.signers
    prepared = consumer.prepare_decision({'action': 'terminate', 'reason': 'The human ended this bounded attempt.',
                                          'subjects': [attempt]})
    proof = host.human_proof(prepared['message'], 'delivery-change')
    op.validate_human_intent_request(proof['request'])
    consumer.submit_decision(prepared['message'], proof)
    assert consumer.attempt_status(attempt)['outcome']['kind'] == 'human_termination'
