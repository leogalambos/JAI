# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""One validated runtime transition must survive exact serialized persistence."""
import base64
import copy
import json
import time

import pytest

from governed_fixtures import CONTROLLER, GovernedHarness, delivery, op
import lifecycle as lc


@pytest.fixture
def host(tmp_path, monkeypatch):
    instance = GovernedHarness(tmp_path, monkeypatch)
    instance.bootstrap()
    return instance


def _root_request(host):
    owner = host.owner()
    inputs = [{'slot_id': 'L1:service-controls:how-input', 'refs': [host.input_a]},
              {'slot_id': 'l0-criteria', 'refs': [host.criteria]},
              {'slot_id': 'l0-capabilities', 'refs': [host.routing_policy]}]
    record = {'owner': owner, 'responsibility': 'setter',
              'routing': {'policy': host.routing_policy}, 'assigned_actor': 'guard-root-actor',
              'use_scope': host.scope, 'issued_under': None, 'input_uses': [],
              'profile': host.profile, 'inherited': copy.deepcopy(host.l0_sources),
              'inputs': inputs, 'criteria': host.criteria,
              'effects': [{'operation': 'read', 'owner': owner, 'targets': host.l0_sources,
                           'destination_handle': None, 'tool_policy': None},
                          {'operation': 'propose', 'owner': owner, 'targets': [],
                           'destination_handle': None, 'tool_policy': None}],
              'limits': [{'metric': 'tokens', 'ceiling': 10000, 'unit': 'governed-token'}],
              'deadline_ms': int(time.time() * 1000) + 240000}
    message = host.message('record_proposal', {'logical_id': 'guard-root',
                                              'record_type': 'assignment', 'record': record})
    return message, record


def _reverse_object_keys(value):
    if isinstance(value, dict):
        return {key: _reverse_object_keys(value[key]) for key in reversed(value)}
    if isinstance(value, list):
        return [_reverse_object_keys(item) for item in value]
    return value


def test_reordered_semantic_json_commits_same_identity_and_retries_without_a_write(host):
    message, record = _root_request(host)
    reordered = json.dumps(_reverse_object_keys(message), indent=2).encode()
    assert reordered != lc.canonical(message) and lc.loads(reordered) == message
    response = host.store.submit(reordered)
    assert response['status'] == 'committed', response
    reference = host.ref('guard-root', 'assignment', record)
    state = host.store.read()
    assert state.resolve(reference, 'assignment') == record
    assert state.head == response['receipt']['after_head']
    before = host.path.read_bytes()
    retried = host.store.submit(lc.canonical(message))
    assert retried['status'] == 'already_committed'
    assert retried['receipt'] == response['receipt']
    assert host.path.read_bytes() == before


@pytest.mark.parametrize('field', ['message', 'effects', 'return_artifact', 'authority_proof'])
def test_serializer_cannot_substitute_validated_content_even_with_a_recomputed_hash(host, monkeypatch, field):
    message, _ = _root_request(host)
    before = host.path.read_bytes()
    head = host.store.read().head
    serialize, derive = op.canonical, lc.State.derive
    injected, derived = [], []

    def observed(state, candidate, *args, **kwargs):
        if candidate['message_id'] == message['message_id']:
            derived.append(candidate['message_id'])
        return derive(state, candidate, *args, **kwargs)

    def substituted(value):
        if isinstance(value, dict) and value.get('format') == 9 and 'hash' in value:
            value = copy.deepcopy(value)
            if field == 'message':
                changed = value['operations'][0]['data']['message']
                changed['payload']['logical_id'] += '-substituted'
                changed['message_id'] = delivery.message_id(changed)
            elif field == 'effects':
                registration = next(item for item in value['operations'][0]['data']['effects'] if item['op'] == 'register')
                registration['manifest']['content']['record']['assigned_actor'] = 'serialization-only-actor'
            elif field == 'return_artifact':
                value[field] = '{}'
            else:
                value[field] = base64.b64encode(b'{}').decode()
            value['hash'] = lc._transaction_hash(value)
            injected.append(value['transaction_id'])
        return serialize(value)

    monkeypatch.setattr(lc.State, 'derive', observed)
    monkeypatch.setattr(op, 'canonical', substituted)
    response = host.store.submit(lc.canonical(message))
    assert injected and response['status'] == 'rejected', response
    assert response['error']['code'] == 'P_INTEGRITY', response
    assert len(derived) == 1
    assert host.path.read_bytes() == before
    assert host.store.read().head == head


def test_expired_runtime_message_is_rejected_without_any_signature_layer(host, monkeypatch):
    message, _ = _root_request(host)
    before = host.path.read_bytes()
    monkeypatch.setattr(lc.time, 'time', lambda: (message['expires_at_ms'] + 1) / 1000)
    response = host.store.submit(lc.canonical(message))
    assert response['status'] == 'rejected' and response['error']['code'] == 'P_EXPIRED'
    assert host.path.read_bytes() == before


@pytest.mark.parametrize('unsupported', ['selector-quorum', 'duplicate-selector', 'management-activity'])
def test_bootstrap_rejects_semantic_obligations_the_runtime_cannot_enforce(tmp_path, monkeypatch, unsupported):
    instance = GovernedHarness(tmp_path, monkeypatch)
    message = instance.bootstrap_message()
    profile = message['payload']['profile']['record']
    review = next(item for item in profile['obligations'] if item['role'] == 'professional_review')
    if unsupported == 'selector-quorum':
        review.update(minimum=2, maximum=2)
    elif unsupported == 'duplicate-selector':
        duplicate = copy.deepcopy(review)
        duplicate['slot_id'] += '-second-selector'
        profile['obligations'].append(duplicate)
    else:
        activity = copy.deepcopy(next(item for item in profile['obligations'] if item['role'] == 'answer'))
        activity.update(slot_id='unsupported-management-role', role='management_activity')
        profile['obligations'].append(activity)
    message['message_id'] = delivery.message_id(message)
    response = instance.store.submit(lc.canonical(message))
    assert response['status'] == 'rejected' and response['error']['code'] == 'P_PROOF'
    assert not instance.path.exists()
