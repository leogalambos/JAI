# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Retained professional review prerequisites bind exact executed producer pairs."""
import copy
import json

import pytest

from governed_fixtures import ROOT
from test_governed_dispatch import _ElapsedHarness, _worker_config
from test_governed_native_session import _issue, _request, _body
import governed_native as native
import lifecycle as lc

SABSA = 'business-security-architect-sabsa-contextual-layer'


def _choose(host, assignment, record, workload, *, specialty='software-engineer', provider='codex', context=None):
    context = context or host.context('choice-' + str(host.sequence), assignment, record, phase='selection')
    selector = host.capture_models['providers'][provider]['classes'][workload]['model_selector']
    choice = {'action': 'select_execution', 'assignment': assignment,
        'previous': host.store.read().execution_plans.get((assignment['version_id'], host.scope)),
        'specialties': [specialty], 'provider': provider, 'workload_class': workload,
        'model_selector': selector, 'reason': 'Exact professional-pair test selection.', 'authority_proof': None}
    response = host.send(host.message('decision', choice, sender={'kind': 'assignment', 'ref': assignment}, context=context))
    if response['status'] != 'committed':
        return response, None
    state = host.store.read()
    selected = next(ref for ref in response['receipt']['created_versions']
                    if state.versions[ref['version_id']]['kind'] == 'delivery.decision')
    return response, selected


class _PairHouse(_ElapsedHarness):
    def _routing_source(self):
        import governed_routing

        source = super()._routing_source()
        descriptor = lc.loads(self.store._blob(source['material'][0]))
        models = lc.loads(self.store._blob(descriptor['models_blob_id']))
        if getattr(self, 'configure_models', None):
            self.configure_models(models)
        self.capture_models = models
        source['material'] = governed_routing.capture_policy('host-routing',
            self.store._blob(descriptor['catalogue_blob_id']), lc.canonical(models),
            {slug: self.store._blob(identifier) for slug, identifier in descriptor['instruction_blobs'].items()},
            descriptor['bootstrap'], descriptor['capabilities'], self.store.put_blob)
        return source


def _pair(tmp_path, monkeypatch, *, specialty=SABSA, configure_models=None):
    host = _PairHouse(tmp_path / 'facts', monkeypatch, engagement='professional-pair')
    host.dispatch_directory, host.dispatch_case, host.dispatch_mode = tmp_path, 'professional_pair', None
    host.configure_models = configure_models
    host.bootstrap()
    actor = host.setup_author(start_author=False)
    response, selection = _choose(host, actor['author'], actor['author_record'], 'standard', specialty=specialty)
    assert response['status'] == 'committed'
    config, _, _ = _worker_config(tmp_path / 'tools', host, actor)
    session = native.NativeSession(host.store, config)
    issued = _issue(session, actor['author'], selection)
    session.start(issued['invocation_id'], 'codex', 'actual-author-context', {'id': 'actual-author-context'})
    proposed = _request(session, issued, 'material', 'propose', data='QWN0dWFsIHNjb3BlZCBjYW5kaWRhdGUu')
    raw, product, subject = _body(host, actor, issued, proposed['blob_id'])
    session.complete(issued['invocation_id'], raw, {'status': 'returned'})
    setter, setter_record = host.assignment('review-setter', 'setter', owner=actor['owner'])
    setter_context = host.context('review-setter-context', setter, setter_record)
    review, review_record = host.assignment('exact-review', 'reviewer', owner=actor['owner'],
        actor='independent-reviewer', inputs=actor['author_record']['inputs'] + [
            {'slot_id': 'assessed-subject', 'refs': [subject]}],
        creator={'kind': 'assignment', 'ref': setter}, creator_context=setter_context)
    return host, session, actor, subject, review, review_record


def test_same_model_sabsa_review_is_blocked_before_work_even_when_effort_differs(tmp_path, monkeypatch):
    def different_effort_same_model(models):
        models['providers']['codex']['classes']['heavy']['model_selector'] = models['providers']['codex']['classes']['standard']['model_selector']
    host, session, actor, subject, review, record = _pair(tmp_path, monkeypatch, configure_models=different_effort_same_model)
    response, selection = _choose(host, review, record, 'heavy')
    assert response['status'] == 'rejected'
    assert selection is None
    assert response['error']['code'] == 'P_PROOF'
    assert 'different effort' in response['error']['message'].lower() and 'insufficient' in response['error']['message']
    assert not any(value.get('responsibility') == 'reviewer' for value in host.store.read().invocations.values())
    message = response['error']['message']
    assert 'gpt-6.1-sol' in message and 'gpt-6-astra' in message
    assert 'same pending reviewer assignment' in message
    assert 'registry-declared only' in message and 'Changing a profile does not repair' in message
    # The rejected selection has not consumed or replaced a review work choice.
    assert (review['version_id'], host.scope) not in host.store.read().execution_plans


def test_distinct_model_sabsa_review_can_execute_and_survives_cold_store(tmp_path, monkeypatch):
    host, session, actor, subject, review, record = _pair(tmp_path, monkeypatch)
    response, selection = _choose(host, review, record, 'heavy')
    assert response['status'] == 'committed'
    issued = _issue(session, review, selection)
    prepared = session.prepare(issued['invocation_id'])
    assert prepared['invocation']['arguments']['model'] == 'gpt-6-astra'
    assert prepared['invocation']['arguments']['model'] != host.capture_models['providers']['codex']['classes']['standard']['model_selector']
    reopened = native.NativeSession(lc.Store(host.path, host.engagement), session.workflow.dispatcher.config)
    assert reopened.prepare(issued['invocation_id'])['invocation'] == prepared['invocation']


def test_generic_profession_can_use_same_model_with_independent_actor_context(tmp_path, monkeypatch):
    host, session, actor, subject, review, record = _pair(tmp_path, monkeypatch, specialty='software-engineer')
    response, selection = _choose(host, review, record, 'standard')
    assert response['status'] == 'committed'
    issued = _issue(session, review, selection)
    assert session.prepare(issued['invocation_id'])['invocation']['arguments']['model'] == 'gpt-6.1-sol'


@pytest.mark.parametrize('model', ['inherit', 'unknown'])
def test_unknown_author_model_blocks_affected_review_with_recovery(tmp_path, monkeypatch, model):
    def unknown_author(models):
        models['providers']['codex']['classes']['standard']['model_selector'] = model
    host, session, actor, subject, review, record = _pair(tmp_path, monkeypatch, configure_models=unknown_author)
    response, selection = _choose(host, review, record, 'heavy')
    assert response['status'] == 'rejected' and selection is None
    assert model in response['error']['message'] and 'blocked' in response['error']['message']


def test_no_compatible_model_holds_review_pending_and_retains_journal(tmp_path, monkeypatch):
    def only_one_model(models):
        for mapping in models['providers']['codex']['classes'].values():
            mapping['model_selector'] = 'only-model'
    host, session, actor, subject, review, record = _pair(tmp_path, monkeypatch, configure_models=only_one_model)
    response, selection = _choose(host, review, record, 'heavy')
    assert response['status'] == 'rejected'
    assert 'No compatible captured alternative exists' in response['error']['message']
    assert 'no in-place registry replacement API' in response['error']['message']
    assert host.store.read().resolve(subject, 'product')['assignment'] == actor['author']
    assert not any(value.get('responsibility') == 'reviewer' for value in host.store.read().invocations.values())


@pytest.mark.parametrize('metadata', [None, [], 'weakened'])
def test_legacy_or_weakened_metadata_cannot_waive_live_sabsa_prerequisite(tmp_path, monkeypatch, metadata):
    def captured_legacy(models):
        if metadata is None:
            models.pop('professional_review_constraints', None)
        elif metadata == 'weakened':
            models['professional_review_constraints'] = [{
                'id': 'sabsa-independent-review-model', 'kind': 'different-model',
                'author_categories': ['Other category'], 'author_operators': [], 'source_contract': 'agent:other'}]
        else:
            models['professional_review_constraints'] = metadata
    host, session, actor, subject, review, record = _pair(tmp_path, monkeypatch, configure_models=captured_legacy)
    response, selection = _choose(host, review, record, 'standard')
    assert response['status'] == 'rejected' and selection is None
    # Reconstruction of the immutable already accepted author prefix remains valid.
    assert lc.Store(host.path, host.engagement).read().resolve(subject, 'product')['assignment'] == actor['author']


def test_wrapped_ai_help_route_can_be_selected_and_admitted_for_the_same_review(tmp_path, monkeypatch):
    import professional_review

    def wrapped_choices(models):
        author_model = models['providers']['codex']['classes']['standard']['model_selector']
        for workload, backend in [('standard', author_model), ('heavy', 'distinct-review-backend')]:
            mapping = models['providers']['json-process/1']['classes'][workload]
            mapping.update(model_selector='review-wrapper-' + workload, model_kind='ai',
                           model_provider='codex', model_identity=backend, reasoning_effort='high')
    host, session, actor, subject, review, record = _pair(tmp_path, monkeypatch, configure_models=wrapped_choices)
    choice_context = host.context('wrapped-choice', review, record, phase='selection')
    rejected, _ = _choose(host, review, record, 'standard', provider='json-process/1', context=choice_context)
    assert rejected['status'] == 'rejected'
    snapshot = host.store.read().assignment_routing(record, live=True)['snapshot']
    alternatives = professional_review._alternatives(snapshot, 'json-process/1', 'reviewer')
    suggestion = next(row for row in alternatives if row['workload_class'] == 'heavy')
    assert suggestion['model_selector'] == 'distinct-review-backend'
    assert suggestion['routing_provider'] == 'json-process/1'
    assert suggestion['routing_model_selector'] == 'review-wrapper-heavy'
    accepted, selection = _choose(host, review, record, suggestion['workload_class'],
                                  provider=suggestion['routing_provider'], context=choice_context)
    assert accepted['status'] == 'committed'
    context = host.context('actual-wrapped-review', review, record, selection=selection)
    execution = host.store.read().context_execution(host.store.read().resolve(context, 'context'))
    assert execution['model_selector'] == suggestion['routing_model_selector']
    assert execution['model']['model_identity'] == suggestion['model_selector']
    assert host.store.read().resolve(subject, 'product')['assignment'] == actor['author']


def test_completed_author_cannot_reopen_selection_or_replace_candidate_controls(tmp_path, monkeypatch):
    host, session, actor, subject, review, record = _pair(tmp_path, monkeypatch)
    original = copy.deepcopy(host.store.read().execution_plans[(actor['author']['version_id'], host.scope)])
    with pytest.raises(AssertionError, match='P_STATE'):
        _choose(host, actor['author'], actor['author_record'], 'heavy', specialty=SABSA)
    state = host.store.read()
    assert state.execution_plans[(actor['author']['version_id'], host.scope)] == original
    assert state.resolve(subject, 'product')['assignment'] == actor['author']
