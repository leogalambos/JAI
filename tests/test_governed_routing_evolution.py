# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Signed routing-policy evolution preserves exact historical control bytes."""
import copy
import json
import unicodedata
import pytest

from test_governed_routing_runtime import host
from governed_fixtures import HUMAN, delivery, routing, lc


def test_signed_policy_replacement_replays_archived_nfd_bytes_without_reusing_old_authority(host):
    actor = host.setup_author()
    host.cancel_run(actor['author_context'])
    old_policy = host.routing_policy
    state = host.store.read()
    original = state.resolve(old_policy, 'source')
    snapshot = routing.load_policy(original, host.store._blob)
    descriptor = snapshot['descriptor']
    instruction = unicodedata.normalize('NFD', snapshot['instructions']['software-engineer']['text'] +
                                         '\nReference example: café.\n').encode()
    replacement = copy.deepcopy(original)
    capabilities = copy.deepcopy(descriptor['capabilities'])
    capabilities['effects'] = [item for item in capabilities['effects'] if item['operation'] != 'materialize']
    replacement['material'] = routing.capture_policy(descriptor['policy_id'],
        host.store._blob(descriptor['catalogue_blob_id']), host.store._blob(descriptor['models_blob_id']),
        {slug: instruction if slug == 'software-engineer' else host.store._blob(blob_id)
         for slug, blob_id in descriptor['instruction_blobs'].items()},
        descriptor['bootstrap'], capabilities, host.store.put_blob)
    new_policy = host.record(old_policy['logical_id'], 'source', replacement)
    change = host.message('decision', {'action': 'continue',
        'reason': 'Explicit L0 replacement of captured routing instructions.',
        'replacements': [{'previous': old_policy, 'replacement': new_policy}],
        'verification_path': host.criteria, 'authority_proof': '0' * 64}, sender=HUMAN)
    host.commit(change, authority_proof=host.human_proof(change, 'delivery-change'))
    host.routing_policy = new_policy
    host.l0_sources = [host.input_a, host.criteria, new_policy]
    host.setters.clear()
    previous = host.controller_context
    renewal = host.message('control_event', {'event': 'renew_control', 'previous_context': previous,
                           'profile_use': {'ref': host.profile, 'use_scope': host.scope}})
    renewal['context'] = None
    renewal['expires_at_ms'] = renewal['issued_at_ms'] + host.control_duration_ms
    renewal['message_id'] = delivery.message_id(renewal)
    receipt = host.commit(renewal)
    host.controller_context = next(ref for ref in receipt['created_versions']
                                   if ref['logical_id'].startswith('controller-context:'))
    # Historical first-use references remain portable with their reachable CAS bytes.
    renewed = host.setup_author(suffix='new-policy-generation')
    state = host.store.read()
    current = state.assignment_routing(renewed['author_record'])
    assert current['policy_use']['ref'] == new_policy
    assert current['snapshot']['descriptor']['instruction_blobs']['software-engineer'] != descriptor['instruction_blobs']['software-engineer']
    assert not any(item['operation'] == 'materialize' for item in current['capabilities']['effects'])
    old_right = copy.deepcopy(renewed['author_record'])
    old_right['effects'].append({'operation': 'materialize', 'owner': old_right['owner'],
                                'targets': [host.input_a], 'destination_handle': 'owned-output', 'tool_policy': None})
    with pytest.raises(lc.ERROR) as failure:
        state.assignment_routing(old_right)
    assert failure.value.code == 'P_SCOPE'
    assert not state._status(old_policy)['applicable']
    transactions = [json.loads(line) for line in host.path.read_text().splitlines()]
    exact = next(identifier for item in transactions for identifier in item['validation_artifacts']
                 if host.store._blob(identifier) == instruction)
    assert host.store._blob(exact) == instruction
    assert instruction != unicodedata.normalize('NFC', instruction.decode()).encode()
    instruction_id = snapshot['descriptor']['instruction_blobs']['software-engineer']
    assert instruction_id in state.validation_assets
    new_snapshot = routing.load_policy(replacement, host.store._blob)
    (host.store.material / new_snapshot['descriptor']['instruction_blobs']['software-engineer']).unlink()
    before = host.path.read_bytes()
    # An already verified policy lookup reuses its immutable snapshot. Missing
    # archive material matters at cold reconstruction, not every warm lookup.
    assert state.assignment_routing(renewed['author_record']) == current
    assert host.store.read().head == state.head
    with pytest.raises(lc.ERROR, match='historical validation material is unavailable') as failure:
        lc.Store(host.path, host.store.engagement).read()
    assert failure.value.code == 'P_INTEGRITY'
    assert host.path.read_bytes() == before
