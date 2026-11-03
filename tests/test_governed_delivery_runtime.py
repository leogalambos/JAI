# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Actual signed governed transitions, separate from structural P02 examples."""
import copy
import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

from governed_fixtures import GovernedHarness, CONTROLLER, HUMAN, delivery
import lifecycle as lc


@pytest.fixture
def harness(tmp_path, monkeypatch):
    instance = GovernedHarness(tmp_path, monkeypatch)
    instance.bootstrap()
    return instance


def _bytes(path):
    return path.read_bytes() if path.exists() else b''


def _error(response, code):
    assert response['status'] == 'rejected', response
    assert response['error']['code'] == code, response


def _reject_invalid(harness, message, code):
    before = _bytes(harness.path)
    response = harness.send(message)
    assert _bytes(harness.path) == before
    _error(response, code)
    return True


def test_signed_bootstrap_records_exact_material_and_replays(harness):
    state = harness.store.read()
    assert state.versions[harness.input_a['version_id']]['content']['record']['source_role'] == 'input'
    assert lc.version_id(state.versions[harness.input_a['version_id']]) == harness.input_a['version_id']
    assert harness.controller_context['version_id'] in state.versions
    assert json.loads(harness.path.read_text().splitlines()[0])['format'] == 9


def test_assignment_access_locators_do_not_create_unpinned_governing_dependencies(harness):
    # Projection alone is exercised here; the neighbor scenario separately
    # establishes and verifies a legally issued cross-scope receiver mandate.
    state = harness.store.read()
    before = _bytes(harness.path)
    assignment = {
        'issued_under': None, 'use_scope': 'receiving',
        'inputs': [{'slot_id': 'incoming_handoff', 'refs': [harness.input_a]}],
        'input_uses': [{'at': '/inputs/0/refs/0', 'use_scope': harness.scope}],
        'effects': [{'operation': 'read',
                     'targets': [harness.input_a, harness.controller_context]}],
    }
    assert state._dependencies(assignment) == [
        {'ref': harness.input_a, 'use_scope': harness.scope},
    ]
    assert _bytes(harness.path) == before


def test_derive_is_only_a_preview_and_cannot_supply_a_verified_origin(harness):
    empty = lc.State(harness.engagement, blob_reader=harness.store._blob)
    bootstrap = copy.deepcopy(harness.last_message)
    before = _bytes(harness.path)
    effects = empty.derive(bootstrap, CONTROLLER, bootstrap['issued_at_ms'])
    assert effects and not empty.initialized and not empty.versions
    with pytest.raises(delivery.ProtocolError) as failure:
        empty.derive(bootstrap, {'kind': 'controller', 'id': 'forged-origin'},
                     bootstrap['issued_at_ms'])
    assert failure.value.code == 'P_ORIGIN'
    with pytest.raises(delivery.ProtocolError) as failure:
        empty.derive(bootstrap, CONTROLLER, bootstrap['expires_at_ms'])
    assert failure.value.code == 'P_EXPIRED'
    assert _bytes(harness.path) == before


def test_current_basis_assesses_exact_scope_without_mutating_or_requiring_read_proof(harness):
    query = {'protocol': delivery.PROTOCOL, 'subject': harness.input_a, 'assessment_scope': harness.scope}
    before = _bytes(harness.path)
    basis = harness.store.current_basis(query)
    assert basis['subject'] == harness.input_a
    assert {'ref': harness.input_a, 'use_scope': harness.scope} in basis['closure']
    assert basis['eligibility']['qualified']
    tampered = dict(query, assessment_scope='not-authorized')
    scoped = harness.store.current_basis(tampered)
    assert scoped['assessment_scope'] == 'not-authorized'
    assert not any(scoped['eligibility'][key] for key in ('qualified', 'accepted', 'release_eligible'))
    assert scoped['selected'] == []
    assert scoped['closure'] == [{'ref': harness.input_a, 'use_scope': 'not-authorized'}]
    assert _bytes(harness.path) == before




def test_same_immutable_input_survives_independently_and_lower_layer_cannot_self_authorize_a_foreign_pin(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, use_scopes=('default', 'retained'))
    host.bootstrap()
    shared = copy.deepcopy(host.input_a)
    _, output_a, _ = host.qualified_answer(suffix='scope-a')
    host.accept(output_a)
    host.accept(output_a, release=True)
    host.enter_scope('retained')
    assert host.input_a == shared
    actor_b, output_b, _ = host.qualified_answer(suffix='scope-b')
    host.accept(output_b)
    host.accept(output_b, release=True)
    bound = copy.deepcopy(actor_b['author_record']['inputs'])
    bound.append({'slot_id': 'explicit-governing-pin', 'refs': [shared]})
    context = host.context('pin-attempt-setter', actor_b['setter'], actor_b['setter_record'])
    child = copy.deepcopy(actor_b['author_record'])
    child.update(assigned_actor='unmandated-pin-author', inputs=bound,
                 input_uses=[{'at': f'/inputs/{len(bound)-1}/refs/0', 'use_scope': 'default'}])
    creator = {'kind': 'assignment', 'ref': actor_b['setter']}
    proposal = host.record('author-pinned', 'assignment', child, sender=creator, context=context)
    locators = []
    for binding in child['inputs']:
        for reference in binding['refs']:
            if reference not in locators:
                locators.append(reference)
    message = host.message('assignment', {'assignment': proposal, 'owner': child['owner'],
                                          'responsibility': 'author', 'inputs': locators,
                                          'criteria': child['criteria']},
                           sender=creator, context=context)
    before = host.path.read_bytes()
    assert _reject_invalid(host, message, 'P_SCOPE')
    assert 'author-pinned' not in {value['logical_id'] for value in host.store.read().versions.values()}
    assert host.path.read_bytes() == before
    host.cancel_run(context)
    state = host.store.read()
    assert ('default', shared['version_id']) in state.states
    assert ('retained', shared['version_id']) in state.states
    assert len([version for version in state.versions if version == shared['version_id']]) == 1
    host.enter_scope('default')
    receipt, _, replacement = host.transition_inputs('Owner approved changed requirements in scope A.\n')
    assert replacement != shared
    assert {'ref': shared, 'use_scope': 'default'} in receipt['affected_uses']
    assert {'ref': shared, 'use_scope': 'retained'} not in receipt['affected_uses']
    assert not host.store.evaluate(output_a, scope='default')['release_eligible']
    independent = host.store.evaluate(output_b, scope='retained')
    assert independent['qualified'] and independent['accepted'] and independent['release_eligible']
    assert host.store.read().resolve(shared, 'source')['source_role'] == 'input'




def test_recording_a_candidate_does_not_inherit_review_or_acceptance(harness):
    actor = harness.setup_author()
    candidate, record = harness.product('candidate-A', actor)
    assert candidate['version_id'] not in harness.store.read().versions
    harness.commit(harness.submission(actor, candidate, record))
    after = harness.store.evaluate(candidate)
    assert not after['qualified']
    assert not after.get('accepted', False)
    assert not after.get('release_eligible', False)


def test_pending_subject_can_acquire_independent_review_before_governing_selection(harness):
    _, candidate, review = harness.qualified_answer(select_basis=False)
    result = harness.store.evaluate(candidate)
    assert result['qualified'], result
    assert {'ref': review, 'use_scope': harness.scope} in result['proofs']
    assert not result['accepted']
    assert not result['release_eligible']
    assert candidate not in harness.store.read().selections.values()


def test_same_inputs_allow_distinct_claims_without_automatic_pass(harness):
    actor = harness.setup_author()
    first, _ = harness.product('claim', actor, material=[harness.material('First conclusion')])
    second, second_body = harness.product('claim', actor, material=[harness.material('Contradictory conclusion')])
    harness.commit(harness.submission(actor, second, second_body))
    assert first['logical_id'] == second['logical_id']
    assert first['version_id'] != second['version_id']
    assert first['version_id'] in harness.store.read().versions
    assert second['version_id'] in harness.store.read().versions
    assert not harness.store.evaluate(first)['qualified']
    assert not harness.store.evaluate(second)['qualified']


def test_same_layer_rejects_delivery_of_another_owners_legitimately_registered_result(tmp_path, monkeypatch):
    layer = 1
    harness = GovernedHarness(tmp_path, monkeypatch, layer=layer)
    harness.bootstrap()
    actor = harness.setup_author(layer=layer, suffix='own-' + str(layer))
    own_candidate, own_record = harness.product('own-result-' + str(layer), actor)
    foreign = harness.setup_author(layer=layer, work_item='foreign-service', suffix='foreign-' + str(layer))
    candidate, record = harness.product('foreign-result-' + str(layer), foreign)
    harness.commit(harness.submission(foreign, candidate, record))
    stolen = harness.submission(actor, candidate, record)
    before = _bytes(harness.path)
    assert _reject_invalid(harness, stolen, 'P_SCOPE')
    assert _bytes(harness.path) == before


@pytest.mark.parametrize('layer', range(2, 7))
def test_controller_cannot_invent_an_arbitrary_layer_entry_assignment(tmp_path, monkeypatch, layer):
    host = GovernedHarness(tmp_path, monkeypatch, additional_layers=(layer,))
    host.bootstrap()
    _, record = host.assignment('legal-entry', 'setter')
    record = copy.deepcopy(record)
    record['owner']['layer'] = layer
    record['assigned_actor'] = 'unmandated-layer-actor'
    proposal = host.message('record_proposal', {'logical_id': 'invented-layer-entry',
                                               'record_type': 'assignment', 'record': record})
    assert _reject_invalid(host, proposal, 'P_SCOPE')


def test_controller_cannot_replace_the_bootstrap_profile_to_create_new_semantic_owners(harness):
    profile = copy.deepcopy(harness.store.read().resolve(harness.profile, 'profile'))
    for obligation in profile['obligations']:
        obligation['owner']['work_item'] = 'invented-ownership'
    proposal = harness.message('record_proposal', {'logical_id': 'changed-profile',
                                                  'record_type': 'profile', 'record': profile})
    assert _reject_invalid(harness, proposal, 'P_SCOPE')


def test_question_setter_cannot_issue_another_questions_author_reviewer_or_setter(harness):
    actor = harness.setup_author(question='how')
    harness.cancel_run(actor['author_context'])
    target = harness.owner(question='why')
    for responsibility in ('author', 'reviewer', 'setter'):
        context = harness.context('foreign-question-' + responsibility, actor['setter'], actor['setter_record'])
        child = copy.deepcopy(actor['author_record'])
        child.update(owner=target, responsibility=responsibility,
                     assigned_actor='unowned-why-' + responsibility)
        for binding in child['inputs']:
            if binding['slot_id'] == 'L1:service-controls:how-input':
                binding['slot_id'] = 'L1:service-controls:why-input'
        for effect in child['effects']:
            effect['owner'] = copy.deepcopy(target)
        creator = {'kind': 'assignment', 'ref': actor['setter']}
        reference = harness.record('foreign-question-' + responsibility, 'assignment', child,
                                    sender=creator, context=context)
        locators = []
        for binding in child['inputs']:
            for item in binding['refs']:
                if item not in locators:
                    locators.append(item)
        attempt = harness.message('assignment', {'assignment': reference, 'owner': target,
            'responsibility': responsibility, 'inputs': locators, 'criteria': child['criteria']},
            sender=creator, context=context)
        assert _reject_invalid(harness, attempt, 'P_SCOPE')
        harness.cancel_run(context)


def test_entry_generation_cannot_be_reissued_under_a_different_logical_label(harness):
    _, record = harness.assignment('entry-once', 'setter')
    alias = copy.deepcopy(record)
    alias['assigned_actor'] = 'another-actor-does-not-change-the-mandate'
    proposal = harness.message('record_proposal', {'logical_id': 'entry-alias',
                                                  'record_type': 'assignment', 'record': alias})
    assert _reject_invalid(harness, proposal, 'P_STATE')






def test_stale_head_rejects_without_partial_application(harness):
    actor = harness.setup_author()
    candidate, record = harness.product('candidate-A', actor)
    pending = harness.submission(actor, candidate, record)
    harness.setup_author(question='why', suffix='independent')
    before = _bytes(harness.path)
    _error(harness.send(pending), 'P_HEAD')
    assert _bytes(harness.path) == before


def test_expired_new_request_is_not_a_historical_retry(harness):
    actor = harness.setup_author()
    candidate, record = harness.product('candidate-A', actor)
    message = harness.submission(actor, candidate, record)
    message['issued_at_ms'] -= 120000
    message['expires_at_ms'] = message['issued_at_ms'] + 60000
    message['message_id'] = delivery.message_id(message)
    before = _bytes(harness.path)
    _error(harness.send(message), 'P_EXPIRED')
    assert _bytes(harness.path) == before


def test_substituted_context_does_not_become_the_authors_context(harness):
    actor = harness.setup_author(suffix='A', author_token_limit=1000, start_author=False)
    other = harness.setup_author(suffix='B', author_token_limit=1000, start_author=False)
    for item, suffix in ((actor, 'A'), (other, 'B')):
        item['author_context'] = harness.context('author-context-' + suffix, item['author'], item['author_record'])
    candidate, record = harness.product('candidate-A', actor)
    message = harness.submission(actor, candidate, record)
    message['context'] = other['author_context']
    message['message_id'] = delivery.message_id(message)
    assert _reject_invalid(harness, message, 'P_ORIGIN')


def test_substituted_result_from_same_owner_still_requires_its_actual_producing_run(harness):
    actor = harness.setup_author(suffix='A', author_token_limit=1000, start_author=False)
    other = harness.setup_author(suffix='B', author_token_limit=1000, start_author=False)
    for item, suffix in ((actor, 'A'), (other, 'B')):
        item['author_context'] = harness.context('author-context-' + suffix, item['author'], item['author_record'])
    candidate, record = harness.product('candidate-B', other)
    harness.commit(harness.submission(other, candidate, record))
    assert _reject_invalid(harness, harness.submission(actor, candidate, record), 'P_ORIGIN')


def test_unavailable_supporting_source_does_not_authorize_new_work(harness):
    actor = harness.setup_author()
    candidate, record = harness.product('candidate-A', actor)
    message = harness.submission(actor, candidate, record)
    source = harness.store.read().resolve(harness.input_a, 'source')
    (harness.store.material / source['material'][0]).unlink()
    harness.commit(message)
    state = harness.store.read()
    assert candidate['version_id'] in state.versions
    assert not state.evaluate(candidate)['accepted']
    assert not state.evaluate(candidate)['release_eligible']
    with pytest.raises(OSError):
        harness.store._blob(source['material'][0])


def test_declared_required_evidence_cannot_be_omitted(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch)
    host.bootstrap(require_evidence=True)
    actor = host.setup_author()
    candidate, record = host.product('candidate-A', actor, evidence=[])
    host.commit(host.submission(actor, candidate, record))
    assert not host.store.evaluate(candidate)['qualified']
    assert not host.store.evaluate(candidate)['release_eligible']


def test_author_cannot_return_its_own_independent_assessment(harness):
    actor = harness.setup_author()
    candidate, record = harness.product('candidate-A', actor)
    harness.commit(harness.submission(actor, candidate, record))
    attempt = harness.prepare_review(actor, candidate, actor_id=actor['author_record']['assigned_actor'])
    _, message = harness.assessment_delivery(attempt, candidate, logical_id='self-review')
    assert _reject_invalid(harness, message, 'P_PROOF')


def test_a_reviewer_cannot_relabel_its_assessment_as_another_layers_review(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, additional_layers=[2])
    host.bootstrap()
    actor = host.setup_author()
    candidate, record = host.product('candidate-A', actor)
    host.commit(host.submission(actor, candidate, record))
    attempt = host.prepare_review(actor, candidate, suffix='wrong-layer-review')
    attempt['record']['owner']['layer'] = 2
    _, message = host.assessment_delivery(attempt, candidate, logical_id='wrong-layer-review')
    assert _reject_invalid(host, message, 'P_SCOPE')


def test_source_record_cannot_be_selected_or_delivered_as_a_layerless_review(harness):
    actor = harness.setup_author()
    candidate, record = harness.product('candidate-A', actor)
    harness.commit(harness.submission(actor, candidate, record))
    reviewer = harness.prepare_review(actor, candidate)
    message = harness.message('review', {'assignment': reviewer['assignment'],
                                         'assessment': harness.input_a, 'subject': candidate,
                                         'criteria': harness.criteria, 'verdict': 'supported',
                                         'findings': [], 'conditions': []},
                              sender=reviewer['principal'], context=reviewer['context'])
    assert _reject_invalid(harness, message, 'P_PROOF')


def test_cancelling_the_selected_proof_does_not_fall_back_to_an_older_pass(harness):
    actor, candidate, first = harness.qualified_answer()
    review_assignment = harness.store.read().resolve(first, 'assessment')['assignment']
    reviewer_id = harness.store.read().resolve(review_assignment, 'assignment')['assigned_actor']
    second, _ = harness.review(actor, candidate, suffix='second-review', actor_id=reviewer_id)
    harness.select_proof(candidate, second, previous=first)
    invalidation = harness.owner_decision(actor['owner'], {'action': 'invalidate',
                                                          'reason': 'Selected review found unsupported',
                                                          'subjects': [second]})
    harness.commit(invalidation)
    current = harness.store.evaluate(candidate)
    assert not current['qualified']
    slot = {'kind': 'basis', 'owner': actor['owner'],
            'slot_id': f'L{actor["owner"]["layer"]}:service-controls:how-answer'}
    attempt = harness.owner_decision(actor['owner'],
                                      {'action': 'select', 'reason': 'Must not inherit old PASS',
                                       'slot': slot, 'candidate': candidate, 'previous': candidate})
    assert _reject_invalid(harness, attempt, 'P_PROOF')


def test_old_formats_and_raw_low_level_operations_cannot_be_reactivated(tmp_path):
    archive = tmp_path / 'archive.jsonl'
    for old_format in range(7):
        raw = (json.dumps({'format': old_format, 'engagement': 'archive', 'operations': []}) + '\n').encode()
        archive.write_bytes(raw)
        with pytest.raises(ValueError):
            lc.Store(archive, 'archive').read()
        assert archive.read_bytes() == raw
    target = tmp_path / 'raw.jsonl'
    with pytest.raises((ValueError, TypeError)):
        lc.commit(target, 'raw', '0' * 64,
                  [{'op': 'version', 'data': {'manifest': lc.manifest('forged', 'source', {})}}])
    assert not target.exists()


def test_posthoc_verification_qualifies_exact_pending_subject_without_a_causal_cycle(tmp_path, monkeypatch):
    """Code exists before its execution evidence; selected review supplies that evidence."""
    host = GovernedHarness(tmp_path, monkeypatch)
    host.bootstrap(require_evidence=True)
    actor = host.setup_author(suffix='B')
    program = b'print(6 * 7)\n'
    candidate, body = host.product('candidate-B', actor,
                                   material=[host.store.put_blob(program)])
    host.commit(host.submission(actor, candidate, body))
    assert not host.store.evaluate(candidate)['qualified']
    exact_program = host.store._blob(body['material'][0])
    execution = subprocess.run([sys.executable, '-I', '-c', exact_program.decode('utf-8')],
                               capture_output=True, text=True, timeout=10, check=False)
    assert execution.returncode == 0 and execution.stdout == '42\n'
    observed = lc.canonical({'subject': candidate, 'program_blob': body['material'][0],
                             'returncode': execution.returncode, 'stdout': execution.stdout,
                             'stderr': execution.stderr}).decode('utf-8')
    observation, _, returned = host.observation(actor, observed, subject=candidate, suffix='execute-B')
    host.commit(returned)
    review, _ = host.review(actor, candidate, suffix='review-B',
                           evidence=[{'slot_id': f'L{host.layer}:service-controls:how-evidence',
                                      'refs': [observation]}])
    host.select_proof(candidate, review)
    current = host.store.evaluate(candidate)
    assert current['qualified'], current
    assert {'ref': observation, 'use_scope': host.scope} in current['closure']
    assert {'ref': review, 'use_scope': host.scope} in current['proofs']
    host.select_basis(actor, candidate)
    host.accept(candidate)
    host.accept(candidate, release=True)
    assert host.store.evaluate(candidate)['release_eligible']
    changed_actor = host.setup_author(suffix='B-prime')
    changed, changed_body = host.product('candidate-B', changed_actor,
                                         material=[host.store.put_blob(b'print(6 * 8)\n')])
    host.commit(host.submission(changed_actor, changed, changed_body))
    assert changed['version_id'] != candidate['version_id']
    changed_result = host.store.evaluate(changed)
    assert not changed_result['qualified']
    assert not changed_result['accepted']
    assert not changed_result['release_eligible']
    assert host.store.evaluate(candidate)['release_eligible']




def test_revoked_human_permission_blocks_its_output_without_corrupting_history(harness):
    _, subject, _ = harness.qualified_answer()
    harness.accept(subject)
    assert harness.store.evaluate(subject)['accepted']
    harness.signers.rotate('human', previous_state='revoked')
    current = harness.store.evaluate(subject)
    assert current['qualified']
    assert not current['accepted']
    assert not current['release_eligible']
    assert subject['version_id'] in harness.store.read().versions
    harness.accept(subject)
    renewed = harness.store.evaluate(subject)
    assert renewed['qualified']
    assert renewed['accepted']


def test_completed_run_cannot_return_another_semantic_result(harness):
    actor, subject, _ = harness.qualified_answer()
    late = harness.message('control_event', {'event': 'run_completed',
                                             'run_context': actor['author_context'],
                                             'run_id': harness.store.read().resolve(actor['author_context'])['run_id'],
                                             'observed_at_ms': int(time.time() * 1000),
                                             'return_blob_id': None,
                                             'usage': [{'metric': 'tokens', 'unit': 'governed-token', 'total': 1}]})
    assert _reject_invalid(harness, late, 'P_STATE')
    assert harness.store.evaluate(subject)['qualified']


def test_usage_audit_is_monotonic_and_cannot_reopen_a_completed_assignment(harness):
    actor, subject, _ = harness.qualified_answer()
    context = harness.store.read().resolve(actor['author_context'])
    payload = {'event': 'usage_audit', 'run_context': actor['author_context'],
               'run_id': context['run_id'], 'observed_at_ms': int(time.time() * 1000),
               'usage': [{'metric': 'tokens', 'unit': 'governed-token', 'total': 2}]}
    harness.commit(harness.message('control_event', payload))
    assert harness.store.evaluate(subject)['qualified']
    payload['usage'][0]['total'] = 1
    assert _reject_invalid(harness, harness.message('control_event', payload), 'P_BUDGET')


def test_exact_committed_retry_after_expiry_is_read_only_and_changed_content_is_not_replayed(harness, monkeypatch):
    actor = harness.setup_author()
    subject, body = harness.product('retry-answer', actor)
    logical = harness.submission(actor, subject, body)
    wire = harness.outbound(logical)
    first = harness.send(logical)
    assert first['status'] == 'committed'
    before = _bytes(harness.path)
    later = wire['expires_at_ms'] / 1000 + 180
    monkeypatch.setattr(time, 'time', lambda: later)
    replayed = harness.store.submit(lc.canonical(wire))
    assert replayed['status'] == 'already_committed', replayed
    assert replayed['receipt'] == first['receipt']
    assert _bytes(harness.path) == before
    changed = copy.deepcopy(wire)
    changed['payload']['return_blob_id'] = None
    changed['message_id'] = delivery.message_id(changed)
    response = harness.store.submit(lc.canonical(changed))
    _error(response, 'P_IDEMPOTENCY')
    assert _bytes(harness.path) == before




def test_human_signature_for_another_scope_cannot_authorize_an_exact_current_transition(harness):
    prepared = harness.stage_input_transition('Otherwise exact staged replacement input B.\n')
    message, _, replacement, _ = prepared
    harness.signers.rotate('human', previous_state='retired')
    harness.signers.keys['human']['entry']['scopes'] = ['other-scope']
    proof = harness.human_proof(message, 'delivery-change')
    before = _bytes(harness.path)
    response = harness.send(message, authority_proof=proof)
    _error(response, 'P_SCOPE')
    assert _bytes(harness.path) == before
    assert not harness.store.evaluate(replacement)['qualified']


def test_signed_input_update_cancels_old_basis_then_renews_and_verifies_fresh_output(harness):
    actor_a, output_a, review_a = harness.qualified_answer(suffix='A')
    harness.accept(output_a)
    harness.accept(output_a, release=True)
    old_bytes = _bytes(harness.path)
    _, input_a, input_b = harness.transition_inputs('Explicit replacement governing requirements B.\n',
                                                   remove_old_material=True)
    state = harness.store.read()
    assert input_a['version_id'] in state.versions
    assert input_b['version_id'] in state.versions
    assert input_a['version_id'] != input_b['version_id']
    assert _bytes(harness.path).startswith(old_bytes)
    obsolete = harness.store.evaluate(output_a)
    assert not obsolete['qualified']
    assert not obsolete['accepted']
    assert not obsolete['release_eligible']
    actor_b = harness.setup_author(suffix='B')
    output_b, body_b = harness.product('current-output', actor_b)
    harness.commit(harness.submission(actor_b, output_b, body_b))
    pending = harness.store.evaluate(output_b)
    assert not pending['qualified']
    assert not pending['accepted']
    review_b, _ = harness.review(actor_b, output_b, suffix='current-review')
    assert review_b != review_a
    harness.select_proof(output_b, review_b)
    harness.select_basis(actor_b, output_b)
    harness.accept(output_b)
    harness.accept(output_b, release=True)
    assert harness.store.evaluate(output_b)['release_eligible']
    assert not harness.store.evaluate(output_a)['release_eligible']


def test_human_transition_recovers_from_invalid_source_and_expired_controller_context(harness, monkeypatch):
    _, old_output, _ = harness.qualified_answer(suffix='before-invalid-source')
    harness.accept(old_output)
    harness.accept(old_output, release=True)
    old_context = copy.deepcopy(harness.controller_context)
    context = harness.store.read().resolve(old_context, 'context')
    withdraw = harness.message('decision', {'action': 'terminate',
        'reason': 'The actual L0 owner withdraws applicability of this exact governing source',
        'subjects': [harness.input_a], 'authority_proof': '0' * 64},
        sender={'kind': 'authority', 'id': 'human-owner'})
    proof = harness.human_proof(withdraw, 'delivery-change')
    harness.commit(withdraw, authority_proof=proof)
    invalid = harness.store.read()
    assert invalid.states[(harness.scope, old_context['version_id'])]['validity'] == 'invalid'
    assert not harness.store.evaluate(old_output)['release_eligible']
    expired_clock = context['expires_at_ms'] / 1000 + 1
    monkeypatch.setattr(lc.time, 'time', lambda: expired_clock)
    prepared = harness.stage_input_transition('Replacement L0 requirements after withdrawn input.\n')
    message, old_input, new_input, new_criteria = prepared
    assert not harness.store.evaluate(new_input)['qualified']
    assert not harness.store.evaluate(new_criteria)['qualified']
    stale = copy.deepcopy(message)
    stale['expected_head'] = '0' * 64
    stale['request_id'] += '-stale'
    stale_proof = harness.human_proof(stale, 'delivery-change')
    before = _bytes(harness.path)
    rejected = harness.send(stale, authority_proof=stale_proof)
    _error(rejected, 'P_HEAD')
    assert _bytes(harness.path) == before
    harness.apply_input_transition(prepared)
    assert harness.controller_context != old_context
    actor, current_output, current_review = harness.qualified_answer(suffix='recovered-current')
    assert actor['author_record']['inputs'][0]['refs'] == [new_input]
    assert current_review['version_id'] in harness.store.read().versions
    harness.accept(current_output)
    harness.accept(current_output, release=True)
    assert harness.store.evaluate(current_output)['release_eligible']
    assert not harness.store.evaluate(old_output)['release_eligible']
    assert harness.store.read().resolve(old_input, 'source')['source_role'] == 'input'


def test_human_continuation_cannot_replace_derived_answers_or_create_acceptance(harness):
    actor_a, first, _ = harness.qualified_answer(suffix='A')
    actor_b = harness.setup_author(suffix='B')
    second, body = harness.product('replacement-answer', actor_b)
    harness.commit(harness.submission(actor_b, second, body))
    message = harness.message('decision', {'action': 'continue',
                                           'reason': 'A valid signature cannot widen source-only continuation',
                                           'replacements': [{'previous': first, 'replacement': second}],
                                           'verification_path': harness.criteria,
                                           'authority_proof': '0' * 64},
                              sender={'kind': 'authority', 'id': 'human-owner'})
    authority = harness.human_proof(message, 'delivery-change')
    before = _bytes(harness.path)
    response = harness.send(message, authority_proof=authority)
    _error(response, 'P_SCOPE')
    assert _bytes(harness.path) == before
    assert not harness.store.evaluate(second)['accepted']
    assert not harness.store.evaluate(second)['release_eligible']


def test_staging_an_authority_source_cannot_supply_a_setters_extra_governing_input(harness):
    actor = harness.setup_author(start_author=False)
    source = copy.deepcopy(harness.store.read().resolve(harness.input_a, 'source'))
    source['material'] = [harness.material('A staged suggestion is not an approved L0 condition.')]
    staged = harness.record('staged-unapproved-condition', 'source', source)
    assert staged['version_id'] in harness.store.read().versions
    assert not harness.store.evaluate(staged)['qualified']
    context = harness.context('staged-attempt-setter-context', actor['setter'], actor['setter_record'])
    child = copy.deepcopy(actor['author_record'])
    child['assigned_actor'] = 'staged-condition-author'
    child['inputs'].append({'slot_id': 'unapproved-extra-condition', 'refs': [staged]})
    next(effect for effect in child['effects'] if effect['operation'] == 'read')['targets'].append(staged)
    creator = {'kind': 'assignment', 'ref': actor['setter']}
    reference = harness.record('staged-condition-assignment', 'assignment', child,
                               sender=creator, context=context)
    message = harness.message('assignment', {'assignment': reference, 'owner': child['owner'],
                                             'responsibility': child['responsibility'],
                                             'inputs': [ref for binding in child['inputs'] for ref in binding['refs']],
                                             'criteria': child['criteria']},
                              sender=creator, context=context)
    before = _bytes(harness.path)
    response = harness.send(message)
    assert response['status'] == 'rejected'
    assert response['error']['code'] == 'P_SCOPE'
    assert _bytes(harness.path) == before
    assert reference['version_id'] not in harness.store.read().versions


def test_explicit_product_reinstatement_requires_post_cancellation_review_and_new_acceptance(harness):
    actor, subject, old_proof = harness.qualified_answer(suffix='restorable')
    harness.accept(subject)
    harness.accept(subject, release=True)
    cancel = harness.owner_decision(actor['owner'], {'action': 'invalidate',
        'reason': 'Withdraw this output while its exact governing inputs remain unchanged',
        'subjects': [subject]})
    harness.commit(cancel)
    assert not harness.store.evaluate(subject)['qualified']
    stale = harness.owner_decision(actor['owner'], {'action': 'reinstate',
        'reason': 'A historical PASS is not fresh reinstatement evidence',
        'subjects': [subject], 'fresh_proofs': [old_proof], 'authority_proof': None})
    assert _reject_invalid(harness, stale, 'P_PROOF')
    harness.cancel_run(stale['context'])
    state = harness.store.read()
    reviewer = state.resolve(state.resolve(old_proof, 'assessment')['assignment'], 'assignment')['assigned_actor']
    fresh_proof, _ = harness.review(actor, subject, suffix='post-cancellation-review', actor_id=reviewer)
    assert fresh_proof != old_proof
    before_restore = harness.store.evaluate(subject)
    assert not before_restore['qualified']
    assert not before_restore['accepted'] and not before_restore['release_eligible']
    restore = harness.owner_decision(actor['owner'], {'action': 'reinstate',
        'reason': 'Explicitly restore only this exact output using fresh applicable review',
        'subjects': [subject], 'fresh_proofs': [fresh_proof], 'authority_proof': None})
    prior_establishments = [event for event in harness.store.read().events
                            if event['kind'] == 'selection' and event['category'] == 'applicability'
                            and event['subject'] == subject]
    receipt = harness.commit(restore)
    assert [event for event in harness.store.read().events
            if event['kind'] == 'selection' and event['category'] == 'applicability'
            and event['subject'] == subject] == prior_establishments
    assert not harness.store.read()._status(subject, harness.scope)['applicable']
    assert {'ref': subject, 'use_scope': harness.scope} in receipt['affected_uses']
    restored = harness.store.evaluate(subject)
    assert not restored['accepted'] and not restored['release_eligible']
    harness.select_proof(subject, fresh_proof, previous=old_proof)
    harness.select_basis(actor, subject)
    assert harness.store.evaluate(subject)['qualified']
    harness.accept(subject)
    harness.accept(subject, release=True)
    assert harness.store.evaluate(subject)['release_eligible']


def test_source_and_root_restoration_uses_one_exact_grant_without_resetting_lifetime_bounds(harness):
    actor, old_output, _ = harness.qualified_answer(suffix='before-root-restoration')
    harness.accept(old_output)
    harness.accept(old_output, release=True)
    old_root, old_record = actor['setter'], actor['setter_record']
    old_run = harness.store.read().resolve(actor['author_context'], 'context')['run_id']
    local_context = harness.context('local-criteria-declaration', old_root, old_record)
    local_principal = {'kind': 'assignment', 'ref': old_root}
    local_criteria = copy.deepcopy(harness.store.read().resolve(harness.criteria, 'source'))
    local_criteria.update(owner=copy.deepcopy(actor['owner']), origin=local_principal,
        material=[harness.material('Owned local C1 interpretation preserves the inherited requirement.')])
    local = harness.record('owned-local-criteria', 'source', local_criteria,
                            sender=local_principal, context=local_context)
    harness.commit(harness.message('decision', {'action': 'select',
        'reason': 'Retain the exact current output while declaring owned local criteria',
        'slot': {'kind': 'basis', 'owner': actor['owner'], 'slot_id': 'L1:service-controls:how-answer'},
        'candidate': old_output, 'previous': old_output},
        sender=local_principal, context=local_context))
    invalidate_local = harness.owner_decision(actor['owner'], {'action': 'invalidate',
        'reason': 'Withdraw only the locally owned criteria use', 'subjects': [local]})
    harness.commit(invalidate_local)
    assert harness.store.read().states[(harness.scope, local['version_id'])]['validity'] == 'invalid'
    restore_local = harness.owner_decision(actor['owner'], {'action': 'reinstate',
        'reason': 'The same actual setter restores its exact primitive criteria with current dependencies',
        'subjects': [local], 'fresh_proofs': [], 'authority_proof': None})
    harness.commit(restore_local)
    assert harness.store.read().states[(harness.scope, local['version_id'])]['validity'] == 'valid'

    def owner_act(action, subjects, reason):
        payload = {'action': action, 'reason': reason, 'subjects': subjects, 'authority_proof': '0' * 64}
        if action == 'reinstate':
            payload['fresh_proofs'] = []
        message = harness.message('decision', payload,
            sender={'kind': 'authority', 'id': 'human-owner'})
        authority = harness.human_proof(message, 'delivery-change')
        receipt = harness.commit(message, authority_proof=authority)
        state = harness.store.read()
        decision = next(reference for reference in receipt['created_versions']
                        if state.versions[reference['version_id']]['kind'] == 'delivery.decision')
        return decision, receipt

    owner_act('terminate', [harness.input_a], 'Withdraw this exact governing source and its dependencies')
    assert harness.store.read().assignment_states[old_root['version_id']] == 'cancelled'
    source_grant, _ = owner_act('reinstate', [harness.input_a],
                                'The source owner explicitly restores these exact input bytes')
    owner_act('reinstate', [harness.criteria],
               'Restore exact criteria only after their governing source is restored')
    assert not harness.store.evaluate(old_output)['release_eligible']
    root_grant, _ = owner_act('reinstate', [old_root],
                              'Permit one new root instance within its original lifetime allowances')
    restored_root = copy.deepcopy(old_record)
    restored_root['inputs'].append({'slot_id': 'root_reinstatement', 'refs': [root_grant]})
    for label in ('deadline', 'allowance'):
        excessive = copy.deepcopy(restored_root)
        if label == 'deadline':
            excessive['deadline_ms'] += 1
        else:
            excessive['limits'][0]['ceiling'] += 1
        proposal = harness.message('record_proposal', {'logical_id': 'excessive-root-' + label,
            'record_type': 'assignment', 'record': excessive})
        assert _reject_invalid(harness, proposal, 'P_BUDGET')
    new_root = harness.record('explicitly-restored-root', 'assignment', restored_root)
    state = harness.store.read()
    assert state.assignment_states[old_root['version_id']] == 'cancelled'
    assert state.run_states[old_run] == 'returned'
    assert new_root != old_root
    before_context = state.usage[(harness.scope, 'tokens', 'governed-token')]['spent']
    new_context = harness.context('restored-root-first-run', new_root, restored_root)
    state = harness.store.read()
    run = state.resolve(new_context, 'context')['run_id']
    remaining = state.run_details[run]['limits'][0]['ceiling']
    assert 0 < remaining < old_record['limits'][0]['ceiling']
    assert before_context + remaining <= old_record['limits'][0]['ceiling']
    assert state.resolve(new_context, 'context')['expires_at_ms'] <= old_record['deadline_ms']
    repeated = harness.message('record_proposal', {'logical_id': 'reused-root-restoration-grant',
        'record_type': 'assignment', 'record': copy.deepcopy(restored_root)})
    assert _reject_invalid(harness, repeated, 'P_STATE')
    harness.cancel_run(new_context)
    harness.setters[(harness.scope, json.dumps(actor['owner'], sort_keys=True))] = (new_root, restored_root)
    _, current, _ = harness.qualified_answer(suffix='after-root-restoration')
    harness.accept(current)
    harness.accept(current, release=True)
    assert harness.store.evaluate(current)['release_eligible']
    assert not harness.store.evaluate(old_output)['release_eligible']
    assert harness.store.read().states[(harness.scope, local['version_id'])]['validity'] == 'invalid'
    query = {'protocol': delivery.PROTOCOL, 'subject': current, 'assessment_scope': harness.scope}
    basis = harness.store.current_basis(query)
    assert {'ref': source_grant, 'use_scope': harness.scope} in basis['established_by']
    assert {'ref': root_grant, 'use_scope': harness.scope} in basis['established_by']
    _, revoked = owner_act('terminate', [source_grant],
                           'Explicitly withdraw the grant establishing the current source use')
    assert {'ref': current, 'use_scope': harness.scope} in revoked['affected_uses']
    assert not harness.store.evaluate(current)['qualified']
    assert not harness.store.evaluate(current)['accepted']
    assert not harness.store.evaluate(current)['release_eligible']
    assert harness.store.read().run_states[old_run] == 'returned'


def test_current_negative_review_retires_old_pass_and_cancels_permissions_permanently(harness):
    actor, subject, first_pass = harness.qualified_answer(suffix='initial-pass')
    harness.accept(subject)
    harness.accept(subject, release=True)
    state = harness.store.read()
    reviewer = state.resolve(state.resolve(first_pass, 'assessment')['assignment'], 'assignment')['assigned_actor']
    negative, _ = harness.review(actor, subject, suffix='current-rework-review',
                                  verdict='rework_required', actor_id=reviewer)
    harness.select_proof(subject, negative, previous=first_pass)
    query = {'protocol': delivery.PROTOCOL, 'subject': subject, 'assessment_scope': harness.scope}
    basis = harness.store.current_basis(query)
    assert not basis['eligibility']['qualified']
    assert not basis['eligibility']['accepted']
    assert not basis['eligibility']['release_eligible']
    assert {'subject': {'ref': subject, 'use_scope': harness.scope},
            'assessment': {'ref': negative, 'use_scope': harness.scope},
            'verdict': 'rework_required'} in basis['review_dispositions']
    assert any(reason['code'] == 'P_PROOF' for reason in basis['eligibility']['reasons'])
    old_selection = harness.owner_decision(actor['owner'], {'action': 'select',
        'reason': 'A retired PASS cannot silently replace the governing negative review',
        'slot': {'kind': 'proof', 'subject': subject, 'role': 'professional_review',
                 'slot_id': 'L1:service-controls:how-professional_review'},
        'candidate': first_pass, 'previous': negative})
    assert _reject_invalid(harness, old_selection, 'P_PROOF')
    harness.cancel_run(old_selection['context'])
    fresh, _ = harness.review(actor, subject, suffix='fresh-supported-review', actor_id=reviewer)
    harness.select_proof(subject, fresh, previous=negative)
    harness.select_basis(actor, subject)
    current = harness.store.evaluate(subject)
    assert current['qualified']
    assert not current['accepted'] and not current['release_eligible']
    assert first_pass['version_id'] in harness.store.read().versions
    harness.accept(subject)
    harness.accept(subject, release=True)
    assert harness.store.evaluate(subject)['release_eligible']


def test_superseded_output_cannot_authorize_use_without_an_explicit_current_basis(harness):
    actor_a, first, first_review = harness.qualified_answer(suffix='basis-A')
    harness.accept(first)
    harness.accept(first, release=True)
    prior_acceptance = harness.store.evaluate(first)['acceptances'][0]
    state = harness.store.read()
    reviewer = state.resolve(state.resolve(first_review, 'assessment')['assignment'], 'assignment')['assigned_actor']
    actor_b, second, _ = harness.qualified_answer(suffix='basis-B', reviewer_actor=reviewer)
    assert first != second
    historical = harness.store.evaluate(first)
    assert not historical['qualified']
    assert harness.store.read()._status(first, harness.scope)['validity'] == 'valid'
    assert harness.store.read().resolve(first) == state.resolve(first)
    assert not historical['accepted'] and not historical['release_eligible']
    for action in ('accept', 'release'):
        payload = {'action': action, 'reason': 'Exact human signatures cannot substitute for governing selection',
                   'subject': first, 'closure_hash': historical['closure_hash'], 'authority_proof': '0' * 64}
        if action == 'release':
            payload['acceptance'] = prior_acceptance
        message = harness.message('decision', payload,
            sender={'kind': 'authority', 'id': 'human-owner'})
        authority = harness.human_proof(message, 'delivery-' + action)
        before = _bytes(harness.path)
        response = harness.send(message, authority_proof=authority)
        _error(response, 'P_PROOF')
        assert _bytes(harness.path) == before
    context = harness.context('superseded-input-attempt', actor_b['setter'], actor_b['setter_record'])
    child = copy.deepcopy(actor_b['author_record'])
    child['assigned_actor'] = 'superseded-input-author'
    child['inputs'].append({'slot_id': 'superseded-output-as-input', 'refs': [first]})
    next(effect for effect in child['effects'] if effect['operation'] == 'read')['targets'].append(first)
    creator = {'kind': 'assignment', 'ref': actor_b['setter']}
    candidate = harness.record('superseded-input-assignment', 'assignment', child,
                                sender=creator, context=context)
    locators = []
    for binding in child['inputs']:
        for reference in binding['refs']:
            if reference not in locators:
                locators.append(reference)
    message = harness.message('assignment', {'assignment': candidate, 'owner': child['owner'],
        'responsibility': 'author', 'inputs': locators, 'criteria': child['criteria']},
        sender=creator, context=context)
    assert _reject_invalid(harness, message, 'P_CONTEXT')
    harness.cancel_run(context)
    inspection = harness.prepare_review(actor_a, first, suffix='historical-inspection', actor_id=reviewer)
    inspected = harness.store.read().resolve(inspection['assignment'], 'assignment')
    assert any(first in binding['refs'] for binding in inspected['inputs'])
    harness.cancel_run(inspection['context'])
    preserved = harness.store.read()
    assert preserved._status(first_review, harness.scope) == {'validity': 'valid', 'applicable': True}
    harness.select_basis(actor_a, first)
    assert not harness.store.evaluate(first)['accepted']
    assert not harness.store.evaluate(first)['release_eligible']
    harness.accept(first)
    harness.accept(first, release=True)
    assert harness.store.evaluate(first)['release_eligible']


def test_cancelled_physical_run_late_completion_accounts_usage_without_registering_result(harness):
    actor = harness.setup_author()
    candidate, body = harness.product('late-result', actor)
    completion = copy.deepcopy(harness.outbound(harness.submission(actor, candidate, body)))
    context = harness.store.read().resolve(actor['author_context'])
    cancelled = harness.message('control_event', {'event': 'run_cancelled',
                                                  'run_context': actor['author_context'],
                                                  'run_id': context['run_id'],
                                                  'observed_at_ms': int(time.time() * 1000),
                                                  'reason': 'Actual host cancellation acknowledgement',
                                                  'usage': [{'metric': 'tokens', 'unit': 'governed-token', 'total': 1}]})
    harness.commit(cancelled)
    completion['request_id'] = 'late-audit-completion'
    completion['expected_head'] = harness.store.read().head
    completion['payload']['observed_at_ms'] = int(time.time() * 1000)
    completion['payload']['usage'][0]['total'] = 2
    completion['message_id'] = delivery.message_id(completion)
    response = harness.send(completion)
    assert response['status'] == 'committed', response
    state = harness.store.read()
    assert state.run_states[context['run_id']] == 'cancelled'
    assert candidate['version_id'] not in state.versions
    assert state.assignment_states[actor['author']['version_id']] != 'completed'


def test_layer_escalation_pauses_work_rejects_budget_overflow_and_quarantines_late_return(harness):
    actor = harness.setup_author(author_token_limit=1000, start_author=False)
    integrator = harness.setup_author(suffix='escalation', responsibility='integrator',
                                      author_token_limit=1000, start_author=False)
    for item, suffix in ((actor, 'author'), (integrator, 'integrator')):
        item['author_context'] = harness.context(suffix + '-context', item['author'], item['author_record'])
    candidate, body = harness.product('paused-return', actor)
    completion = copy.deepcopy(harness.outbound(harness.submission(actor, candidate, body)))
    conflict_author = harness.setup_author(suffix='conflict-answer', author_token_limit=1000)
    subject, subject_body = harness.product('conflict-answer', conflict_author,
        material=[harness.material('The local requirement remains unfulfilled.')])
    harness.commit(harness.submission(conflict_author, subject, subject_body))
    prepared = harness.prepare_review(conflict_author, subject, suffix='local-conflict-review',
                                     assessment_kind='professional', verdict='rework_required')
    diagnostic = {'owner': prepared['record']['owner'], 'author': prepared['assignment'],
                  'author_record': harness.store.read().resolve(prepared['assignment'], 'assignment'),
                  'author_context': prepared['context'], 'principal': prepared['principal']}
    finding, _ = harness.product('local-conflict-finding', diagnostic, kind='finding',
        related=[{'slot_id': 'subject', 'refs': [subject]},
                 {'slot_id': 'criterion:C1', 'refs': [harness.criteria]}])
    prepared['record']['findings'] = [finding]
    _, review_message = harness.assessment_delivery(prepared, subject)
    harness.commit(review_message)
    escalation, _ = harness.product('escalation', integrator, kind='escalation',
                                    related=[{'slot_id': 'conflicts', 'refs': [finding]}])
    harness.commit(harness.message('escalation', {
        'assignment': integrator['author'], 'package': escalation,
        'conflicts': [finding], 'affected': [actor['author']],
        'requested_decisions': ['Resolve the exact inherited requirements conflict'],
    }, sender=integrator['principal'], context=integrator['author_context']))
    context = harness.store.read().resolve(actor['author_context'])
    assert harness.store.read().assignment_states[actor['author']['version_id']] == 'paused'
    state = harness.store.read()
    inputs = sorted({lc.canonical(point): point for point in
                     state._dependencies(actor['author_record'])}.values(), key=lc.canonical)
    speculation = harness.message('decision', {'action': 'speculate',
        'reason': 'Explicit L0 control cannot enlarge the original task allowance.',
        'escalation': escalation, 'assignments': [actor['author']], 'inputs': inputs,
        'limits': [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 10001}],
        'expires_at_ms': actor['author_record']['deadline_ms'], 'authority_proof': None}, sender=HUMAN)
    proof = harness.human_proof(speculation, 'delivery-change')
    before = _bytes(harness.path)
    _error(harness.send(speculation, authority_proof=proof), 'P_BUDGET')
    assert _bytes(harness.path) == before
    completion['request_id'] = 'paused-physical-completion'
    completion['expected_head'] = harness.store.read().head
    completion['payload']['observed_at_ms'] = int(time.time() * 1000)
    completion['message_id'] = delivery.message_id(completion)
    audited = harness.send(completion)
    assert audited['status'] == 'committed', audited
    state = harness.store.read()
    assert state.run_states[context['run_id']] == 'quarantined'
    assert state.assignment_states[actor['author']['version_id']] == 'paused'
    assert candidate['version_id'] not in state.versions


def test_named_criterion_observations_are_distinct_from_the_answer_under_review(tmp_path, monkeypatch):
    """An authored answer/reference cannot substitute for an observation prerequisite."""
    host = GovernedHarness(tmp_path, monkeypatch)
    host.bootstrap(require_evidence=True)
    actor = host.setup_author(suffix='observation-contract')
    candidate, body = host.product('observation-contract-answer', actor)
    host.commit(host.submission(actor, candidate, body))
    observation, _, returned = host.observation(actor, 'Controlled actual observation.',
        subject=candidate, suffix='observation-contract-measurement')
    host.commit(returned)
    state = host.store.read()
    slot = f'L{host.layer}:service-controls:how-evidence'
    answered = {**copy.deepcopy(body), 'related': [{'slot_id': slot, 'refs': [candidate]}]}
    with pytest.raises(lc.ERROR, match='qualified exact observation') as failure:
        state._product_requirements(answered)
    assert failure.value.code == 'P_PROOF'
    observed = {**copy.deepcopy(body), 'related': [{'slot_id': slot, 'refs': [observation]}]}
    state._product_requirements(observed)
    cited_source = {**copy.deepcopy(observed), 'evidence': [host.input_a]}
    with pytest.raises(lc.ERROR, match='wrong type') as source_failure:
        state._product_requirements(cited_source)
    assert source_failure.value.code == 'P_CONTEXT'
    declared_observation = {**copy.deepcopy(observed), 'evidence': [observation]}
    state._product_requirements(declared_observation)
    assert state._status(candidate, host.scope)['validity'] == 'pending'
    assert state._status(observation, host.scope)['validity'] == 'valid'
    assert not host.store.evaluate(candidate)['qualified']
