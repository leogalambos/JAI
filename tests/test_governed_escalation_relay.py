# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""One genuine transport entry precedes an L2–L1–L0 escalation relay."""
import copy
import hashlib
import json

import pytest

from governed_scheduling_fixtures import (
    WORKERS, worker, owner_resolution, reconciliation, affected_refs,
)
from test_governed_transport_layers import _TransportHarness
import lifecycle as lc
import governed_workflow


class _RelayUnitHarness(_TransportHarness):
    def context(self, *args, **kwargs):
        """Record genuine starts for Store-only returns, unlike native launch scaffolding."""
        kwargs.setdefault('start', True)
        return super().context(*args, **kwargs)


def _consumer(host):
    config = {'protocol': 'jai.host-dispatch/1',
              'workers': [worker(WORKERS / 'transport_worker.py'), worker(WORKERS / 'selection_worker.py')],
              'destinations': [], 'tools': [],
              'limits': {'packet_bytes': 1000000, 'total_bytes': 4000000}}
    return governed_workflow.Workflow(host.store, config)


def _incoming_layer_two(host, consumer):
    actor = host.setup_author(suffix='transport-bundle', responsibility='integrator', work_kind='integration')
    bundle, body = host.product('transport-only-bundle', actor, kind='bundle', related=[{'slot_id': 'answers', 'refs': []}])
    host.commit(host.submission(actor, bundle, body))
    reviewed, _ = host.review(actor, bundle, suffix='transport-integration-review', assessment_kind='integration')
    host.select_proof(bundle, reviewed, role='integration_review')
    # This is the reviewed transport path, not complete-layer integration.
    # A governing bundle is sufficient for its explicit adjacent handoff.
    author = host.setup_author(suffix='transport-offer', responsibility='integrator', work_kind='integration',
        inputs=[{'slot_id': 'bundle', 'refs': [bundle]}, {'slot_id': 'interface', 'refs': [host.criteria]}])
    handoff, _ = host.product('actual-layer-two-offer', author, kind='handoff',
        related=[{'slot_id': 'bundle', 'refs': [bundle]}, {'slot_id': 'interface', 'refs': [host.criteria]}])
    host.commit(host.message('handoff', {'assignment': author['author'], 'handoff': handoff, 'bundle': bundle,
        'interface': host.criteria, 'obligations': host.l0_sources}, sender=author['principal'], context=author['author_context']))
    offered = {'ref': handoff, 'use_scope': host.scope}
    receiver = consumer.local_entry(offered, 'receiver')['assignment']
    state = host.store.read()
    assigned = state.resolve(receiver, 'assignment')
    context = host.context('actual-layer-two-receiver', receiver, assigned)
    state = host.store.read()
    closure = state.assessment_closure(handoff, receiver)
    assessment = {'owner': assigned['owner'], 'assessment_kind': 'receiving', 'assignment': receiver,
        'subject': handoff, 'criteria': assigned['criteria'], 'profile': host.profile,
        'assessed_closure': closure, 'assessed_hash': hashlib.sha256(lc.canonical(closure)).hexdigest(),
        'verdict': 'accepted', 'findings': [], 'conditions': []}
    principal = {'kind': 'assignment', 'ref': receiver}
    accepted = host.record('actual-layer-two-receiving', 'assessment', assessment, sender=principal, context=context)
    host.commit(host.message('handoff_acceptance', {'assessment': accepted, 'handoff': handoff,
        'interface': assigned['criteria'], 'verdict': 'accepted', 'findings': []}, sender=principal, context=context))
    host.select_proof(handoff, accepted, role='receiving_acceptance')
    entry = consumer.local_entry(offered, 'setter', acceptance=accepted)['assignment']
    body = host.store.read().resolve(entry, 'assignment')
    # Cache only the immutable body from the actual accepted adjacent entry.
    # No State, ownership or hypothetical lower-layer root is injected.
    host.setters[(host.scope, json.dumps(body['owner'], sort_keys=True))] = (entry, body)
    return entry


def _lower_conflict(host):
    author = host.setup_author(layer=2, suffix='lower-incomplete', responsibility='integrator', work_kind='integration')
    subject, body = host.product('lower-incomplete-bundle', author, kind='bundle',
        material=[host.material(json.dumps({'requirement_satisfied': False}))], related=[{'slot_id': 'answers', 'refs': []}])
    host.commit(host.submission(author, subject, body))
    prepared = host.prepare_review(author, subject, suffix='lower-independent-review',
        assessment_kind='integration', verdict='rework_required')
    observed = json.loads(host.store._blob(host.store.read().resolve(subject)['material'][0]))
    assert observed['requirement_satisfied'] is False
    reviewer = {'owner': prepared['record']['owner'], 'author': prepared['assignment'],
                'author_record': host.store.read().resolve(prepared['assignment'], 'assignment'),
                'author_context': prepared['context'], 'principal': prepared['principal']}
    finding, _ = host.product('lower-local-finding', reviewer, kind='finding',
        material=[host.material('The delivered bundle explicitly leaves the governing requirement unfulfilled.')],
        related=[{'slot_id': 'subject', 'refs': [subject]}, {'slot_id': 'criterion:C1', 'refs': [host.criteria]}])
    prepared['record']['findings'] = [finding]
    _, message = host.assessment_delivery(prepared, subject)
    host.commit(message)
    return finding


def test_actual_lower_entry_relays_to_human_owner_without_skipping_or_claiming_local_authority(tmp_path, monkeypatch):
    host = _RelayUnitHarness(tmp_path, monkeypatch, engagement='adjacent-escalation-owner')
    host.bootstrap(include_neighbor=True)
    consumer = _consumer(host)
    lower_root = _incoming_layer_two(host, consumer)
    finding = _lower_conflict(host)
    author = host.setup_author(layer=2, suffix='lower-escalation', responsibility='integrator', work_kind='integration')
    episode, _ = host.product('lower-explicit-escalation', author, kind='escalation',
        related=[{'slot_id': 'conflicts', 'refs': [finding]}],
        episode={'root': None, 'previous': None, 'collection_head': host._proposal_head(),
                 'unfinished': [lower_root], 'decisive': True})
    host.commit(host.message('escalation', {'assignment': author['author'], 'package': episode,
        'conflicts': [finding], 'affected': [lower_root],
        'requested_decisions': ['Ask the actual owner of the inherited L0 requirement.']},
        sender=author['principal'], context=author['author_context']))
    before = host.path.read_bytes()
    with pytest.raises(AssertionError) as skipped:
        owner_resolution(host, episode)
    assert skipped.value.args[0]['error']['code'] == 'P_SCOPE'
    assert host.path.read_bytes() == before

    local = consumer.handling_entry(episode, 'resolve', layer=2)['assignment']
    state = host.store.read()
    local_body = state.resolve(local, 'assignment')
    local_context = host.context('unentitled-local-owner-response', local, local_body)
    impacts = [{'subject': {'ref': reference, 'use_scope': host.scope}, 'outcome': 'unchanged',
                'reason': 'An originating layer cannot make this owner decision itself.'}
               for reference in affected_refs(host.store.read(), episode)]
    payload = {'action': 'resolve_escalation', 'reason': 'Attempted originating-layer self-resolution.',
               'escalation': episode, 'package': episode, 'conflicts': [finding],
               'impacts': impacts, 'decisions': [], 'authority_proof': None}
    before = host.path.read_bytes()
    self_resolved = host.send(host.message('decision', payload, sender={'kind': 'assignment', 'ref': local}, context=local_context))
    assert self_resolved['status'] == 'rejected' and self_resolved['error']['code'] == 'P_SCOPE'
    assert host.path.read_bytes() == before
    host.cancel_run(local_context)

    relay = consumer.handling_entry(episode, 'relay')['assignment']
    state = host.store.read()
    relay_body = state.resolve(relay, 'assignment')
    assert relay_body['owner']['layer'] == 1
    context = host.context('actual-adjacent-relay', relay, relay_body)
    original = next(message for message in host.store.read().messages.values()
                    if message['message_type'] == 'escalation' and message['payload']['package'] == episode)
    host.commit(host.message('relay', {'original_message': original['message_id'],
        'original_origin': original['sender'], 'route': host.routing_policy},
        sender={'kind': 'assignment', 'ref': relay}, context=context))
    state = host.store.read()
    event = next(event for event in reversed(state.events) if event['kind'] == 'relay')
    assert event['payload']['episode'] == episode
    assert event['payload']['from_layer'] == 1 and event['payload']['to_layer'] == 0
    assert event['payload']['original_origin'] == original['sender']
    resolution = owner_resolution(host, episode)
    resumed = consumer.submit_decision(consumer.prepare_decision(reconciliation(host, episode, resolution))['message'])
    assert resumed['status'] == 'committed'
    assert host.store.read().escalations[episode['version_id']] == 'resolved'
    assert host.store.read().assignment_states[lower_root['version_id']] == 'open'
