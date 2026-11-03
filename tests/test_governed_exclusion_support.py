# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Only a necessary explicit content exception governs a qualified output."""
import copy

from governed_fixtures import HUMAN, delivery
from test_governed_sabsa_runtime import ContentHarness, _select_policy
import lifecycle as lc


def test_revoked_needed_exclusion_withdraws_its_output_but_not_unwaived_work(tmp_path, monkeypatch):
    host = ContentHarness(tmp_path, monkeypatch, engagement='needed-exclusion-support')
    host.bootstrap()
    rationale = 'Bound this result to the driver and opportunity; do not claim a quality target.'
    message = host.message('decision', {'action': 'exclude_content', 'reason': rationale,
        'content_policy': host.semantic_policy_ref, 'obligations': ['quality', 'quality-basis'],
        'authority_proof': '0' * 64}, sender=HUMAN)
    receipt = host.commit(message, authority_proof=host.human_proof(message, 'delivery-change'))
    decision = next(ref for ref in receipt['created_versions']
                    if host.store.read().versions[ref['version_id']]['kind'] == 'delivery.decision')
    policy = copy.deepcopy(host.semantic_policy)
    policy['exclusions'] = [{'obligations': ['quality', 'quality-basis'], 'decision': decision,
        'rationale': rationale, 'consequences': 'No quality assurance claim.',
        'use_scope': host.scope, 'expires_at_ms': None}]
    policy['required_views'][0]['unit_obligations'].remove('quality')
    policy['required_views'][0]['relation_obligations'].remove('quality-basis')
    _select_policy(host, policy)
    actor, output = host.deliver_content('waived-result', missing_quality=True, private=False)
    host.qualify_content(actor, output, 'waived-independent-review')
    _, unwaived, _ = host.qualified_answer(suffix='unwaived-result', question='how')
    host.accept(unwaived)
    host.accept(unwaived, release=True)
    prior = host.store.evaluate(output)
    assert prior['release_eligible']
    assert {'ref': decision, 'use_scope': host.scope} in prior['closure']
    assert {'ref': decision, 'use_scope': host.scope} not in host.store.evaluate(unwaived)['closure']
    message = host.message('decision', {'action': 'terminate',
        'reason': 'Withdraw this exact exception while leaving the current policy and other work intact.',
        'subjects': [decision], 'authority_proof': '0' * 64}, sender=HUMAN)
    receipt = host.commit(message, authority_proof=host.human_proof(message, 'delivery-change'))
    assert {'ref': output, 'use_scope': host.scope} in receipt['affected_uses']
    state = host.store.read()
    assert state._status(host.semantic_policy_ref, host.scope)['applicable']
    assert not state._status(output, host.scope)['applicable']
    assert state.evaluate(unwaived)['release_eligible']
    query = host.store.current_basis({'protocol': delivery.PROTOCOL, 'subject': output, 'assessment_scope': host.scope})
    assert not query['eligibility']['qualified'] and not query['eligibility']['release_eligible']
    for action in ('accept', 'release'):
        payload = {'action': action, 'reason': 'A signature cannot replace a withdrawn necessary exception.',
            'subject': output, 'closure_hash': state.evaluate(output)['closure_hash'], 'authority_proof': '0' * 64}
        if action == 'release':
            payload['acceptance'] = prior['acceptances'][0]
        message = host.message('decision', payload, sender=HUMAN)
        proof = host.human_proof(message, 'delivery-' + action)
        before = host.path.read_bytes()
        response = host.send(message, authority_proof=proof)
        assert response['status'] == 'rejected' and response['error']['code'] == 'P_PROOF', response
        assert host.path.read_bytes() == before


def test_selected_review_condition_deadline_limits_subject_without_a_direct_input(tmp_path, monkeypatch):
    host = ContentHarness(tmp_path, monkeypatch, engagement='review-condition-validity')
    host.bootstrap()
    expires = int(lc.time.time() * 1000) + 120000
    rationale = 'This bounded observation makes no design-definition claim; retain its raw execution fact.'
    waived = [item['key'] for item in host.semantic_policy['required_units'] + host.semantic_policy['required_relations']]
    message = host.message('decision', {'action': 'exclude_content', 'reason': rationale,
        'content_policy': host.semantic_policy_ref, 'obligations': waived,
        'authority_proof': '0' * 64}, sender=HUMAN)
    receipt = host.commit(message, authority_proof=host.human_proof(message, 'delivery-change'))
    decision = next(ref for ref in receipt['created_versions']
                    if host.store.read().versions[ref['version_id']]['kind'] == 'delivery.decision')
    policy = copy.deepcopy(host.semantic_policy)
    policy['exclusions'] = [{'obligations': waived, 'decision': decision,
        'rationale': rationale, 'consequences': 'The observation establishes no architectural definitions.',
        'use_scope': host.scope, 'expires_at_ms': expires}]
    _select_policy(host, policy)
    measured = host.setup_author(question='why', suffix='condition-observer', responsibility='measurement')
    payload = {'format': 'jai-sabsa-content/1', 'units': [], 'relations': [], 'view_bindings': []}
    execution = {'fixture_condition': True, 'observed_at_ms': int(lc.time.time() * 1000)}
    condition, record = host.product('conditional-observation', measured, kind='observation',
        material=[host.store.put_blob(lc.canonical(payload)), host.store.put_blob(lc.canonical(execution))])
    inputs = [reference for binding in record['inputs'] for reference in binding['refs']]
    host.commit(host.message('observation', {'assignment': measured['author'], 'observation': condition,
        'inputs': list({lc.canonical(ref): ref for ref in inputs}.values()), 'material': record['material']},
        sender=measured['principal'], context=measured['author_context']))
    actor, output = host.deliver_content('complete-conditional-answer', private=False)
    prepared = host.prepare_review(actor, output, suffix='conditional-answer-review',
        verdict='supported_with_conditions', evidence=[{'slot_id': 'review-condition', 'refs': [condition]}])
    prepared['record']['conditions'] = [condition]
    proof, review = host.assessment_delivery(prepared, output)
    host.commit(review)
    host.select_proof(output, proof)
    host.select_basis(actor, output)
    host.accept(output)
    host.accept(output, release=True)
    state = host.store.read()
    assert state._governing_input(state._point(output), live=True)
    assert condition not in [point['ref'] for point in state._governing_dependencies(state._point(output))]
    assert state._use_changes[(host.scope, output['version_id'])]['requirements'] == []
    assert state._use_changes[(host.scope, output['version_id'])]['use_until_ms'] == expires
    with monkeypatch.context() as clock:
        clock.setattr(lc.time, 'time', lambda: expires / 1000)
        assert not state._governing_input(state._point(output), live=True)
        assert not state.evaluate(output)['release_eligible']
