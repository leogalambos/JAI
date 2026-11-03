# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Signed L1 semantic qualification, exact reviews, and audience projections."""
import copy
import json

import pytest

from governed_fixtures import GovernedHarness, HUMAN, delivery
from test_governed_sabsa_content import _example
from governed_scheduling_fixtures import WORKERS, worker
import governed_workflow
import lifecycle as lc
import governed_sabsa as content

CANARY = 'PRIVATE-CONTENT-CANARY'
OPPORTUNITY = 'private-opportunity-' + CANARY


class ContentHarness(GovernedHarness):
    """Enroll one bounded semantic policy through the real L0 bootstrap."""

    def bootstrap_message(self, **kwargs):
        message = super().bootstrap_message(**kwargs)
        self.semantic_policy = self.content_profile()
        source = {'owner': HUMAN, 'source_role': 'policy', 'origin': HUMAN,
                  'material': [self.store.put_blob(lc.canonical(self.semantic_policy))],
                  'criteria': [], 'inherited': []}
        self.semantic_policy_ref = self.ref('sabsa-content-policy', 'source', source)
        self._remember_proposal(self.semantic_policy_ref, 'source', source)
        self.l0_sources.append(self.semantic_policy_ref)
        message['payload']['l0_inputs'].append({'logical_id': 'sabsa-content-policy', 'record': source})
        profile = message['payload']['profile']['record']
        profile['content_profile'] = {'logical_id': 'sabsa-content-policy', 'use_scope': self.scope}
        self.profile = self.ref('profile', 'profile', profile)
        message['message_id'] = delivery.message_id(message)
        return message

    def content_profile(self):
        """Declare only contextual WHY; the example makes no six-layer claim."""
        return {'format': 'jai-sabsa-content-profile/1',
                'catalogue_id': 'jai-sabsa-minimum', 'catalogue_version': '1',
                'method_sources': _example('sabsa-content-profile')['method_sources'],
                'scope': {'purpose': 'Fictional contextual business justification', 'layers': [1],
                          'questions': ['why'], 'depth': 'Contextual rationale only',
                          'audiences': ['Business sponsor'], 'classification': 'public'},
                'required_units': [{'key': key, 'owner': self.owner('why'), 'group': 'contextual.why'}
                                   for key in ('driver', 'quality', OPPORTUNITY)],
                'required_relations': [{'key': key + '-basis', 'type': 'justifies',
                                       'from_obligation': key, 'to_obligation': 'driver'}
                                      for key in ('quality', OPPORTUNITY)],
                'required_views': [{'view': 'architecture',
                                    'unit_obligations': ['driver', 'quality', OPPORTUNITY],
                                    'relation_obligations': ['quality-basis', OPPORTUNITY + '-basis']}],
                'exclusions': [], 'claim': 'Contextual rationale only. Private sponsor note ' + CANARY}

    def semantic(self, *, private=True, missing_quality=False):
        """Build exact local locators; a target is never an observation."""
        units = [
            {'key': 'driver', 'group': 'contextual.why', 'title': 'Service continuity',
             'statements': ['The fictional sponsor needs a dependable service.'],
             'properties': {'business_role': 'driver'}, 'classification': 'public'},
            {'key': 'quality', 'group': 'contextual.why', 'title': 'Availability objective',
             'statements': ['Availability is a business quality objective, not an achieved result.'],
             'properties': {'business_role': 'quality_attribute', 'target': '99.5'}, 'classification': 'public'},
            {'key': OPPORTUNITY, 'group': 'contextual.why',
             'title': CANARY if private else 'Improvement opportunity',
             'statements': [CANARY + ' /private/client-seed.txt' if private else 'Reduce recovery delay.'],
             'properties': {}, 'classification': 'private' if private else 'public'}]
        if missing_quality:
            units = [unit for unit in units if unit['key'] != 'quality']
        relations = [{'key': unit['key'] + '-basis', 'type': 'justifies',
                      'from': {'product': None, 'unit': unit['key']},
                      'to': {'product': None, 'unit': 'driver'},
                      'rationale': CANARY if private and unit['key'] == OPPORTUNITY else 'Supports the sponsor driver.'}
                     for unit in units if unit['key'] != 'driver']
        return {'format': 'jai-sabsa-content/1', 'units': units, 'relations': relations,
                'view_bindings': [{'view': 'architecture',
                                   'units': [{'product': None, 'unit': unit['key']} for unit in units],
                                   'relations': [{'product': None, 'relation': item['key']} for item in relations]}]}

    def deliver_content(self, suffix, **kwargs):
        """Submit real owner-authored semantic material without manufacturing a review."""
        actor = self.setup_author(question='why', suffix=suffix)
        payload = self.semantic(**kwargs)
        subject, record = self.product('semantic-' + suffix, actor,
                                      material=[self.store.put_blob(lc.canonical(payload))])
        self.commit(self.submission(actor, subject, record))
        return actor, subject

    def qualify_content(self, actor, subject, suffix):
        """Select independent exact-subject review and the owner's current basis."""
        proof, _ = self.review(actor, subject, suffix=suffix, actor_id='semantic-independent-reviewer')
        self.select_proof(subject, proof)
        self.select_basis(actor, subject)
        self.accept(subject)
        self.accept(subject, release=True)
        return proof


def test_real_semantic_basis_reviews_and_publication_do_not_transfer_between_versions(tmp_path, monkeypatch):
    host = ContentHarness(tmp_path, monkeypatch, engagement='semantic-current-basis')
    host.bootstrap()
    assert host.store.read().content_policy(host.profile) == {
        'ref': host.semantic_policy_ref, 'use_scope': host.scope}
    draft_actor, draft = host.deliver_content('draft', missing_quality=True)
    report = content.assess(host.store.read(), draft)
    assert report['status'] == 'incomplete'
    assert any(row['key'] == 'quality' and row['status'] == 'missing' for row in report['obligations'])
    before = host.path.read_bytes()
    with pytest.raises(AssertionError) as incomplete:
        host.accept(draft)
    assert incomplete.value.args[0]['error']['code'] == 'P_PROOF'
    assert host.path.read_bytes() == before

    actor_a, output_a = host.deliver_content('A')
    proof_a = host.qualify_content(actor_a, output_a, 'semantic-review-A')
    private = content.render(host.store.read(), output_a)
    assert private['report']['substantive_complete']
    assert private['publication']['eligible']
    assert CANARY in json.dumps(private)
    private_edges = private['views'][0]['json']['relations']
    assert {edge['type'] for edge in private_edges} == {'justifies'}
    assert len(private_edges) == 2
    public = content.render(host.store.read(), output_a, audience='public')
    assert public['report']['status'] == 'incomplete'
    assert not public['publication']['eligible']
    assert CANARY not in json.dumps(public)
    assert '/private/' not in json.dumps(public)
    assert output_a['version_id'] not in json.dumps(public)

    actor_b, output_b = host.deliver_content('B', private=False)
    state = host.store.read()
    assert output_a != output_b
    assert not content.assess(state, output_b)['substantive_complete']
    before = host.path.read_bytes()
    with pytest.raises(AssertionError) as unreviewed:
        host.accept(output_b)
    assert unreviewed.value.args[0]['error']['code'] == 'P_PROOF'
    assert host.path.read_bytes() == before
    proof_b = host.qualify_content(actor_b, output_b, 'semantic-review-B')
    assert proof_a != proof_b
    unrelated_blob = host.material('Unselected historical draft outside the current output closure.\n')
    host.record('unselected-obsolete-source', 'source', {
        'owner': HUMAN, 'source_role': 'input', 'origin': HUMAN,
        'material': [unrelated_blob], 'criteria': [], 'inherited': []})
    (host.store.material / unrelated_blob).unlink()
    config = {'protocol': 'jai.host-dispatch/1',
              'workers': [worker(WORKERS / 'worker.py', ['/usr/bin/python3', '/worker/main.py', 'author']),
                          worker(WORKERS / 'selection_worker.py')],
              'destinations': [], 'tools': [],
              'limits': {'packet_bytes': 1000000, 'total_bytes': 4000000}}
    consumer = governed_workflow.Workflow(host.store, config)
    point = {'ref': output_b, 'use_scope': host.scope}
    assert consumer.content_status(point)['status'] == 'complete'
    before = host.path.read_bytes()
    rendered = content.render(host.store.read(), output_b, audience='public')
    assert rendered['report']['status'] == 'complete'
    assert rendered['publication']['eligible']
    public_edges = rendered['views'][0]['json']['relations']
    assert len(public_edges) == 2
    assert all(edge['from'].startswith('unit-') and edge['to'].startswith('unit-') for edge in public_edges)
    assert CANARY not in json.dumps(rendered)
    assert rendered == content.render(host.store.read(), output_b, audience='public')
    assert rendered == consumer.content_views(point, audience='public')
    assert rendered['report'] == consumer.content_status(point, audience='public')
    assert host.path.read_bytes() == before, 'Rendering must not grant or modify authority'


def _select_policy(host, policy):
    """Apply one real L0 source-slot revision and renew bounded host control."""
    previous = host.semantic_policy_ref
    source = host._known_record(previous, 'source')
    source['material'] = [host.store.put_blob(lc.canonical(policy))]
    replacement = host.record('sabsa-content-policy', 'source', source)
    message = host.message('decision', {'action': 'continue',
        'reason': 'Select the explicitly bounded revised semantic policy',
        'replacements': [{'previous': previous, 'replacement': replacement}],
        'verification_path': replacement, 'authority_proof': '0' * 64}, sender=HUMAN)
    proof = host.human_proof(message, 'delivery-change')
    host.commit(message, authority_proof=proof)
    host.semantic_policy_ref = replacement
    host.semantic_policy = copy.deepcopy(policy)
    host.l0_sources = [replacement if ref == previous else ref for ref in host.l0_sources]
    host.setters = {key: value for key, value in host.setters.items() if key[0] != host.scope}
    renewal = host.message('control_event', {'event': 'renew_control',
        'previous_context': host.controller_context,
        'profile_use': {'ref': host.profile, 'use_scope': host.scope}})
    renewal['context'] = None
    renewal['expires_at_ms'] = renewal['issued_at_ms'] + host.control_duration_ms
    renewal['message_id'] = delivery.message_id(renewal)
    receipt = host.commit(renewal)
    host.controller_context = next(ref for ref in receipt['created_versions']
                                   if ref['logical_id'].startswith('controller-context:'))
    host.scope_contexts[host.scope] = copy.deepcopy(host.controller_context)
    return previous, replacement


def test_typed_l0_exclusion_survives_policy_revision_but_not_reused_key_meaning(tmp_path, monkeypatch):
    host = ContentHarness(tmp_path, monkeypatch, engagement='semantic-explicit-exclusion')
    host.bootstrap()
    policy_a = host.semantic_policy_ref
    message = host.message('decision', {'action': 'exclude_content',
        'reason': 'The sponsor bounds this delivery to driver and opportunity rationale',
        'content_policy': policy_a, 'obligations': ['quality', 'quality-basis'],
        'authority_proof': '0' * 64}, sender=HUMAN)
    proof = host.human_proof(message, 'delivery-change')
    receipt = host.commit(message, authority_proof=proof)
    state = host.store.read()
    decision = next(ref for ref in receipt['created_versions']
                    if state.versions[ref['version_id']]['kind'] == 'delivery.decision')
    revised = copy.deepcopy(host.semantic_policy)
    revised['claim'] = 'Contextual driver and opportunity rationale; quality explicitly excluded.'
    revised['exclusions'] = [{'obligations': ['quality', 'quality-basis'], 'decision': decision,
        'rationale': 'The sponsor bounds this delivery to driver and opportunity rationale', 'consequences': 'No quality assurance claim',
        'use_scope': host.scope, 'expires_at_ms': None}]
    revised['required_views'][0]['unit_obligations'].remove('quality')
    revised['required_views'][0]['relation_obligations'].remove('quality-basis')
    old, selected = _select_policy(host, revised)
    assert old == policy_a and selected != old
    actor, output = host.deliver_content('excluded', private=False, missing_quality=True)
    host.qualify_content(actor, output, 'excluded-independent-review')
    report = content.assess(host.store.read(), output)
    assert report['status'] == 'complete'
    assert next(row for row in report['obligations'] if row['key'] == 'quality')['status'] == 'excluded'
    assert next(row for row in report['relations'] if row['key'] == 'quality-basis')['status'] == 'excluded'

    changed = copy.deepcopy(revised)
    changed['scope']['questions'].append('what')
    obligation = next(row for row in changed['required_units'] if row['key'] == 'quality')
    obligation['group'] = 'contextual.what'
    obligation['owner'] = host.owner('what')
    _select_policy(host, changed)
    _, current = host.deliver_content('changed-meaning', private=False, missing_quality=True)
    report = content.assess(host.store.read(), current)
    assert report['status'] == 'incomplete'
    assert next(row for row in report['obligations'] if row['key'] == 'quality')['status'] != 'excluded'
    before = host.path.read_bytes()
    with pytest.raises(AssertionError) as incomplete:
        host.accept(current)
    assert incomplete.value.args[0]['error']['code'] == 'P_PROOF'
    assert host.path.read_bytes() == before
