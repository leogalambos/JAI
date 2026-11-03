# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Local operator access does not substitute for explicit signed L0 decisions."""
import copy
import hashlib
import hmac
import sys
from unittest.mock import patch

import pytest

from governed_fixtures import GovernedHarness, HUMAN, lc, op, delivery


def _acceptance(host, subject):
    return host.message('decision', {'action': 'accept', 'reason': 'Explicit L0 decision boundary.',
        'subject': subject, 'closure_hash': host.store.evaluate(subject)['closure_hash'],
        'authority_proof': '0' * 64}, sender=HUMAN)


def test_environment_tty_and_declared_approval_cannot_authorize_l0_acceptance(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch)
    host.bootstrap()
    _, subject, _ = host.qualified_answer()
    message = _acceptance(host, subject)
    before = host.path.read_bytes()
    with patch.dict('os.environ', {'FABRIC_TEST_AUTHORITY': '1', 'JAI_FORCE_APPROVE': '1'}), \
            patch.object(sys.stdin, 'isatty', return_value=True), \
            patch.object(sys.stdout, 'isatty', return_value=True):
        result = host.store.submit(lc.canonical(message),
            authority_proof={'origin': message['sender'], 'approved': True})
    assert result['status'] == 'rejected'
    assert host.path.read_bytes() == before
    assert not host.store.evaluate(subject)['accepted']


def test_caller_chosen_hmac_cannot_substitute_for_the_enrolled_human_ed25519_key(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch)
    host.bootstrap()
    _, subject, _ = host.qualified_answer()
    message = _acceptance(host, subject)
    signed = host.human_proof(message, 'delivery-accept')
    altered = copy.deepcopy(signed)
    body = dict(altered['receipt']); body.pop('signature')
    altered['receipt']['signature'] = hmac.new(b'caller-selected-key', op.canonical(body), hashlib.sha256).hexdigest()
    message['payload']['authority_proof'] = lc.blob(op.canonical(altered))
    message['message_id'] = delivery.message_id(message)
    before = host.path.read_bytes()
    result = host.store.submit(lc.canonical(message), authority_proof=altered)
    assert result['status'] == 'rejected'
    assert host.path.read_bytes() == before
    assert not host.store.evaluate(subject)['accepted']


def test_missing_human_key_blocks_current_grant_and_cold_proof_verification_not_warm_history(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch)
    host.bootstrap()
    _, subject, _ = host.qualified_answer()
    host.accept(subject)
    before = host.path.read_bytes()
    head = host.store.read().head

    def missing(purpose=None):
        raise ValueError('Human public enrollment is unavailable')

    monkeypatch.setattr(op, 'trusted_keys', missing)
    assert host.store.read().head == head
    assert not host.store.evaluate(subject)['accepted']
    with pytest.raises(ValueError):
        lc.Store(host.path, host.engagement).read()
    assert host.path.read_bytes() == before
