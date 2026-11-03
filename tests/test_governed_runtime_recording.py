# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Local runtime recording is keyless; explicit L0 decisions remain signed."""
import base64
import copy
import inspect
import json

import pytest

from governed_fixtures import CONTROLLER, HUMAN, GovernedHarness, delivery, lc, op
import governed_dispatch
import governed_workflow


TRANSACTION_FIELDS = {'format', 'protocol', 'engagement', 'sequence', 'previous',
                      'transaction_id', 'timestamp', 'operations', 'authority_proof',
                      'return_artifact', 'validation_artifacts', 'hash'}


def test_ordinary_work_and_reads_need_no_keys_signing_or_second_derivation(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError('Ordinary runtime work consulted a signing or keyring service')

    host = GovernedHarness(tmp_path, monkeypatch, engagement='keyless-runtime')
    bootstrap_calls = []
    derive = lc.State.derive

    def observed(state, message, *args, **kwargs):
        if message['message_type'] == 'bootstrap':
            bootstrap_calls.append(message['message_id'])
        return derive(state, message, *args, **kwargs)

    with monkeypatch.context() as ordinary:
        ordinary.setattr(op, 'trusted_keys', forbidden)
        ordinary.setattr(op, 'trusted_key', forbidden)
        ordinary.setattr(delivery, 'verify_proof', forbidden)
        ordinary.setattr('subprocess.run', forbidden)
        ordinary.setattr(lc.State, 'derive', observed)
        # Live recording must not replay a second candidate to authenticate itself.
        ordinary.setattr(lc, '_verify_transaction', forbidden)
        host.bootstrap()
        _, subject, _ = host.qualified_answer()
        basis = host.store.current_basis({'protocol': delivery.PROTOCOL,
            'subject': subject, 'assessment_scope': host.scope})
        state = host.store.read()
    assert len(bootstrap_calls) == 1
    assert basis['eligibility']['qualified']
    assert not basis['eligibility']['accepted']
    assert host._human_signer is None
    assert not (tmp_path / 'external-human-key').exists()
    assert all(set(row) == TRANSACTION_FIELDS and row['format'] == 9
               and row['authority_proof'] is None for row in state.transactions)
    assert all('key_id' not in item and 'purpose' not in item for item in state.provenance.values())
    cold = lc.Store(host.path, host.engagement).read()
    assert cold.head == state.head and cold.versions == state.versions


def test_direct_assignment_ingress_and_substituted_captured_context_cannot_record_work(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='recorded-origin')
    host.bootstrap()
    actor = host.setup_author(suffix='owned')
    subject, record = host.product('owned-result', actor)
    message = host.submission(actor, subject, record)
    before = host.path.read_bytes()
    rejected = host.store.submit(lc.canonical(message))
    assert rejected['status'] == 'rejected' and rejected['error']['code'] == 'P_ORIGIN'
    assert host.path.read_bytes() == before

    other = host.setup_author(question='why', suffix='different-context')
    message['context'] = other['author_context']
    message['expected_head'] = host.store.read().head
    message['message_id'] = delivery.message_id(message)
    before = host.path.read_bytes()
    rejected = host.send(message)
    assert rejected['status'] == 'rejected'
    assert rejected['error']['code'] in {'P_ORIGIN', 'P_SCOPE'}
    assert host.path.read_bytes() == before
    assert subject['version_id'] not in host.store.read().versions


def test_only_actual_l0_signature_accepts_and_releases_exact_output_and_preserves_pretty_proof_bytes(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='human-only-authority')
    host.bootstrap()
    _, subject, _ = host.qualified_answer()
    basis = host.store.evaluate(subject)
    message = host.message('decision', {'action': 'accept', 'reason': 'Explicit disposable L0 acceptance.',
        'subject': subject, 'closure_hash': basis['closure_hash'], 'authority_proof': '0' * 64}, sender=HUMAN)
    before = host.path.read_bytes()
    refused = host.send(message)
    assert refused['status'] == 'rejected'
    assert host.path.read_bytes() == before
    proof = host.human_proof(message, 'delivery-accept')
    forged = copy.deepcopy(proof)
    forged['receipt']['signature'] = 'Zm9yZ2Vk'
    message['payload']['authority_proof'] = lc.blob(op.canonical(forged))
    message['message_id'] = delivery.message_id(message)
    refused = host.send(message, authority_proof=forged)
    assert refused['status'] == 'rejected'
    assert host.path.read_bytes() == before

    pretty = json.dumps(proof, indent=2).encode() + b'\n'
    message['payload']['authority_proof'] = lc.blob(pretty)
    message['message_id'] = delivery.message_id(message)
    host.commit(message, authority_proof=pretty)
    accepted = host.store.evaluate(subject)
    assert accepted['accepted'] and not accepted['release_eligible']
    host.accept(subject, release=True)
    assert host.store.evaluate(subject)['release_eligible']
    transactions = lc._parse_transactions(host.path.read_bytes())
    row = next(row for row in transactions if row['operations'][0]['data']['message']['message_id'] == message['message_id'])
    assert base64.b64decode(row['authority_proof'], validate=True) == pretty
    replayed = lc.Store(host.path, host.engagement).read()
    assert replayed.head == transactions[-1]['hash']
    assert replayed.evaluate(subject)['release_eligible']


def test_removed_internal_credentials_are_not_runtime_api_arguments():
    assert set(inspect.signature(lc.Store.submit).parameters) == {'self', 'raw_message', 'authority_proof'}
    assert set(inspect.signature(lc.Store.current_basis).parameters) == {'self', 'query'}
    assert set(inspect.signature(governed_dispatch.Dispatcher).parameters) == {'store', 'config'}
    assert set(inspect.signature(governed_workflow.Workflow).parameters) == {'store', 'host_config'}
    assert {'delivery-dispatch', 'delivery-control', 'delivery-read'}.isdisjoint(op.PURPOSE_CAPABILITIES)
