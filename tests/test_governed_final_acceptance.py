# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Reviewed final reports require separate exact human acceptance and release."""
import io
import shutil

import pytest

from governed_fixtures import GovernedHarness, HUMAN, delivery
import lifecycle as lc
import operator_actions as op


class _FinalReportHouse(GovernedHarness):
    """Require independent final-report review without inventing a basis slot."""

    def bootstrap_message(self, **kwargs):
        kwargs['include_neighbor'] = True
        message = super().bootstrap_message(**kwargs)
        profile = message['payload']['profile']['record']
        profile['obligations'].append({'slot_id': 'final-report-independent-review',
            'owner': self.owner(work_kind='integration'), 'subject_kind': 'final_result',
            'role': 'integration_review', 'required_kind': 'assessment',
            'minimum': 1, 'maximum': 1, 'allow_exclusion': False, 'exclusion_owner': None})
        self.profile = self.ref('profile', 'profile', profile)
        message['message_id'] = delivery.message_id(message)
        return message


def _unsigned_human_request(host, subject, *, action='accept', acceptance=None):
    """Exercise the real signing-console preflight without producing a signature."""
    state = host.store.read()
    payload = {'action': action, 'reason': 'Exact final-report console regression',
               'subject': subject, 'closure_hash': state.evaluate(subject)['closure_hash'],
               'authority_proof': '0' * 64}
    if action == 'release':
        payload['acceptance'] = acceptance
    message = host.message('decision', payload, sender=HUMAN)
    intent = delivery.action_descriptor(message, state.policy_digest(message))
    source = host.directory / f'console-intent-{host.sequence}.json'
    source.write_bytes(lc.canonical(intent))
    request = op.request('delivery-' + action, 'Review exact final report', source,
                         host.path, {'intent': intent, 'intent_digest': op.sha(lc.canonical(intent))})
    return request, intent


def test_reviewed_honest_final_report_can_be_accepted_then_released(tmp_path, monkeypatch):
    host = _FinalReportHouse(tmp_path, monkeypatch, engagement='final-report-acceptance')
    host.bootstrap()
    actor = host.setup_author(suffix='honest-final-report', responsibility='integrator', work_kind='integration')
    subject, record = host.product('insufficient-information-report', actor, kind='final_result',
        material=[host.material('The assigned requirements remain unanswered; no solution is claimed.')],
        outcome={'kind': 'insufficient_information', 'attempt': actor['setter'], 'evidence': [host.criteria]})
    host.commit(host.submission(actor, subject, record))
    before = host.path.read_bytes()
    with pytest.raises(AssertionError) as pending:
        host.accept(subject)
    assert pending.value.args[0]['error']['code'] == 'P_PROOF'
    assert host.path.read_bytes() == before
    request, _ = _unsigned_human_request(host, subject)
    with pytest.raises(ValueError):
        op.validate_human_intent_request(request)
    assert host.path.read_bytes() == before
    proof, _ = host.review(actor, subject, suffix='final-report-review',
        assessment_kind='integration', actor_id='independent-final-report-reviewer')
    host.select_proof(subject, proof, role='integration_review')
    current = host.store.evaluate(subject)
    assert current['qualified'] and not current['accepted'] and not current['release_eligible']
    request, intent = _unsigned_human_request(host, subject)
    before = host.path.read_bytes()
    assert op.validate_human_intent_request(request) == intent
    tools = tmp_path / 'operator crypto tools with spaces'
    tools.mkdir()
    (tools / 'openssl').symlink_to(shutil.which('openssl'))
    with monkeypatch.context() as console:
        console.setenv('PATH', str(tools))
        console.setattr(op.sys, 'stdin', io.StringIO())
        console.setattr(op.sys.stdin, 'isatty', lambda: True)
        console.setattr('builtins.input', lambda prompt: 'APPROVE ' + request['request_id'])
        receipt = op.sign(request, host.signers.keys['human']['private'])
        assert op.verify_receipt(request, receipt)['accepted']
        with pytest.raises(ValueError, match='signature invalid'):
            op.verify_receipt(request, dict(receipt, accepted=False))
    assert host.path.read_bytes() == before
    assert host.store.read().assess_output_decision(intent['decision'], host.scope)['closure_hash'] == current['closure_hash']
    assert host.path.read_bytes() == before

    material = record['material'][0]
    raw = host.store._blob(material)
    (host.store.material / material).unlink()
    try:
        with pytest.raises(ValueError):
            op.validate_human_intent_request(request)
        assert host.path.read_bytes() == before
    finally:
        assert host.store.put_blob(raw) == material

    release, _ = _unsigned_human_request(host, subject, action='release', acceptance=proof)
    with pytest.raises(ValueError):
        op.validate_human_intent_request(release)
    host.accept(subject)
    assert host.store.evaluate(subject)['accepted']
    assert not host.store.evaluate(subject)['release_eligible']
    release, _ = _unsigned_human_request(host, subject, action='release', acceptance=proof)
    before = host.path.read_bytes()
    with pytest.raises(ValueError):
        op.validate_human_intent_request(release)
    assert host.path.read_bytes() == before
    acceptance = host.store.evaluate(subject)['acceptances'][0]
    release, intent = _unsigned_human_request(host, subject, action='release', acceptance=acceptance)
    assert op.validate_human_intent_request(release) == intent
    host.accept(subject, release=True)
    assert host.store.evaluate(subject)['release_eligible']
    assert host.store.read().resolve(subject, 'product')['outcome']['kind'] == 'insufficient_information'
    # An applicable source remains a prerequisite, not an acceptable product.
    before = host.path.read_bytes()
    with pytest.raises(AssertionError) as nonproduct:
        host.accept(host.input_a)
    assert nonproduct.value.args[0]['error']['code'] == 'P_PROOF'
    assert host.path.read_bytes() == before
    request, _ = _unsigned_human_request(host, host.input_a)
    with pytest.raises(ValueError):
        op.validate_human_intent_request(request)
    assert host.path.read_bytes() == before
