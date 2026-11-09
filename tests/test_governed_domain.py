# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Actual Store/native-capture fixtures qualify mechanics, not professional truth."""
import copy
import base64
import argparse
import json
from pathlib import Path
import sys

import pytest

from governed_fixtures import GovernedHarness

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import governed_domain as domain
import governed_native as native
import governed_native_provider as provider
import lifecycle as lc
import content_spec
import content_lint
import content_workflow
import projection
import publication
import commercial
import commercial_core
import commercial_proposal as proposal


class DomainHarness(GovernedHarness):
    def record(self, logical_id, record_type, record, **kwargs):
        if record_type == 'product' and record['product_kind'] == 'finding':
            observation = self.material('Controlled exact criterion observation.')
            if observation not in record['material']:
                record['material'].append(observation)
        if record_type == 'assignment':
            record['limits'] = [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 60000}]
        return super().record(logical_id, record_type, record, **kwargs)

    def _routing_source(self):
        source = super()._routing_source()
        snapshot = provider.routing.load_policy(source, self.store._blob)
        descriptor = snapshot['descriptor']
        capabilities = copy.deepcopy(descriptor['capabilities'])
        capabilities['effects'] = [item for item in capabilities['effects']
                                   if item['operation'] in {'read', 'propose'}]
        source['material'] = provider.routing.capture_policy('host-routing',
            self.store._blob(descriptor['catalogue_blob_id']),
            self.store._blob(descriptor['models_blob_id']),
            {slug: self.store._blob(blob) for slug, blob in descriptor['instruction_blobs'].items()},
            {'provider': 'codex', 'workload_class': 'light',
             'model_selector': snapshot['models']['providers']['codex']['classes']['light']['model_selector']},
            capabilities, self.store.put_blob)
        return source

    def message(self, kind, payload, **kwargs):
        payload = copy.deepcopy(payload)
        if kind == 'decision' and payload.get('action') == 'select_execution':
            payload['provider'] = 'codex'
            payload['model_selector'] = self.store.read().assignment_routing(
                self._known_record(payload['assignment'], 'assignment'), live=True
            )['snapshot']['models']['providers']['codex']['classes'][payload['workload_class']]['model_selector']
        return super().message(kind, payload, **kwargs)

    def context(self, logical_id, assignment, record, *, start=True, **kwargs):
        # Setter construction and selection are ordinary synthetic Store scaffolding.
        # Domain producer/reviewer captures use the production uniform native API.
        phase = kwargs.get('phase', 'work')
        if record['responsibility'] == 'setter' or phase == 'selection':
            return super().context(logical_id, assignment, record, start=start, **kwargs)
        selection = kwargs.get('selection')
        if selection is None:
            context = super().context(logical_id + '-choice', assignment, record, phase='selection')
            choice = {'action': 'select_execution', 'assignment': assignment,
                'previous': self.store.read().execution_plans.get((assignment['version_id'], self.scope)),
                'specialties': ['software-engineer'], 'provider': 'codex',
                'workload_class': 'fixture-' + record['responsibility'],
                'model_selector': 'filled-from-exact-fixture-registry',
                'reason': 'Controlled native domain fixture staffing; no professional truth claim.',
                'authority_proof': None}
            receipt = self.commit(self.message('decision', choice,
                sender={'kind': 'assignment', 'ref': assignment}, context=context))
            selection = self.store.read().execution_plans[(assignment['version_id'], self.scope)]
        issued = self.native.issue_batch([{'assignment': assignment, 'phase': 'work',
                                          'selection': selection}], bound_ms=5000)
        prepared = self.native.prepare(issued['invocation_id'])
        member = prepared['members'][0]
        reference = member['context']
        self.domain_members = getattr(self, 'domain_members', {})
        self.domain_members[reference['version_id']] = (issued['invocation_id'], member)
        if start:
            self.native.start(issued['invocation_id'], 'codex', 'fixture-' + reference['version_id'],
                              {'fixture': 'Controlled native capture, not a real LLM invocation.'})
        return reference

    def send(self, message, *, authority_proof=None):
        context = message.get('context')
        member_data = getattr(self, 'domain_members', {}).get(context['version_id']) if context else None
        if message['sender']['kind'] != 'assignment' or member_data is None:
            return super().send(message, authority_proof=authority_proof)
        invocation, member = member_data
        assigned = self.store.read().resolve(message['sender']['ref'], 'assignment')
        proposals = self.pending.get(context['version_id'], [])
        # These bytes are the controlled fixture's actual proposed materials.
        # Preserve original JSON bytes and hashes, rather than rewriting bodies.
        for proposal_value in proposals:
            for index, identifier in enumerate(proposal_value['record'].get('material', [])):
                self.native.request(invocation, member['member_key'], {
                    'id': 'material:' + identifier, 'operation': 'propose',
                    'data': base64.b64encode(self.store._blob(identifier)).decode('ascii')})
        role = assigned['responsibility']
        if role == 'author':
            proposal_value = next(item for item in proposals if item['record_type'] == 'product'
                                  and item['record']['product_kind'] == 'answer')
            record = proposal_value['record']
            result = {'member': member['member_key'], 'kind': 'author',
                'logical_id': proposal_value['logical_id'],
                'materials': [{'blob': identifier} for identifier in record['material']],
                'evidence': record['evidence'], 'limitations': record['limitations']}
        else:
            assessment = next(item for item in proposals if item['record_type'] == 'assessment')
            record = assessment['record']
            new_findings = {}
            for proposal_value in proposals:
                if proposal_value['record_type'] != 'product':
                    continue
                finding = proposal_value['record']
                criterion = next(item['slot_id'][10:] for item in finding['related']
                                 if item['slot_id'].startswith('criterion:'))
                finding_ref = self.ref(proposal_value['logical_id'], 'product', finding)
                new_findings[finding_ref['version_id']] = {'logical_id': proposal_value['logical_id'], 'criterion': criterion,
                    'observation': 'Controlled exact criterion observation.',
                    'materials': [{'blob': identifier} for identifier in finding['material'][:-1]],
                    'evidence': finding['evidence'], 'limitations': finding['limitations']}
            findings = [new_findings.get(reference['version_id'], reference) for reference in record['findings']]
            result = {'member': member['member_key'], 'kind': role, 'logical_id': assessment['logical_id'],
                'verdict': record['verdict'], 'findings': findings, 'conditions': record['conditions'],
                'rationale': 'Controlled actual fixture review; not native professional evidence.'}
        raw = json.dumps({'format': 'jai.semantic-return/1', 'results': [result]})
        completed = self.native.complete(invocation, raw, {'fixture': 'Controlled exact domain return.'})
        response = completed['completion']
        self._observe_commit(response)
        self.last_message = copy.deepcopy(message)
        return response


def _fixture(tmp_path, monkeypatch):
    host = DomainHarness(tmp_path, monkeypatch)
    host.bootstrap()
    host.native = native.NativeSession(host.store, {'protocol': 'jai.host-dispatch/1',
        'workers': [], 'destinations': [], 'tools': [],
        'limits': {'packet_bytes': 2097152, 'total_bytes': 8388608}})
    return host


def _manifest(host, context):
    state = host.store.read()
    body = state.resolve(context, 'context')
    return {'context': context, 'manifest_hash': state.run_details[body['run_id']]['native']['manifest_hash']}


def _qualified(host, suffix='source', model_factory=None, review_factory=None, sidecar=False, question='how'):
    actor = host.setup_author(suffix=suffix,question=question)
    token = {'context': actor['author_context'], 'logical_id': suffix}
    model = {'title': 'Controlled source', 'audience': ['internal'],
             'producer': {'attestation': token, 'context_manifest': _manifest(host, actor['author_context'])},
             'claims': [{'statement': 'Fixture-only explicit assumption.', 'basis': 'assumed'}]}
    if model_factory is not None:
        model = model_factory(actor, token, _manifest(host, actor['author_context']))
    material = [host.material(json.dumps(model,sort_keys=True,separators=(',', ':'),ensure_ascii=False,allow_nan=False))]
    if sidecar:
        material.append(host.material('{"supporting_note":"Unrelated JSON must not shadow the actual identity body."}'))
        material.append(host.material('# Supporting Markdown\nOpaque supporting material remains available.\n'))
    subject, body = host.product(suffix, actor, material=material)
    host.commit(host.submission(actor, subject, body))
    prepared = host.prepare_review(actor, subject, suffix=suffix + '-review',actor_id='independent-domain-reviewer')
    review_token = {'context': prepared['context'], 'logical_id': suffix + '-review-detail'}
    review = {'attestation': review_token, 'context_manifest': _manifest(host, prepared['context']),
              'semantic_hash': domain._digest(model), 'unit_reviews': [
                  {'unit_id': 'actual-unit', 'verdict': 'PASS', 'rationale': 'Explicit fixture rationale.',
                   'evidence': 'Exact controlled source, not a real professional verdict.'}], 'findings': []}
    if model.get('contract_id'):
        spec = content_spec.ContentSpec(ROOT).resolve(model['contract_id'], model.get('context', {}))
        review.update(compiled_spec_hash=spec['compiled_spec_hash'], context_hash=spec['context_hash'],
            unit_reviews=[{'unit_id': unit['id'], 'verdict': 'PASS',
                'rationale': 'Explicit controlled review of this exact fixture unit.',
                'evidence': 'The actual fixture content is present; this is not native professional evidence.'}
                for unit in spec['blueprint']['semantic_units']])
    if review_factory is not None:
        review = review_factory(model, review_token, _manifest(host, prepared['context']))
    state = host.store.read()
    assignment = state.resolve(prepared['assignment'], 'assignment')
    criterion = state.resolve(host.criteria, 'source')['criteria'][0]['id']
    finding = {'owner': assignment['owner'], 'product_kind': 'finding',
        'assignment': prepared['assignment'], 'profile': host.profile, 'inputs': assignment['inputs'],
        'material': [host.material(lc.canonical(review).decode())], 'evidence': [],
        'related': [{'slot_id': 'subject', 'refs': [subject]},
                    {'slot_id': 'criterion:' + criterion, 'refs': [host.criteria]}], 'limitations': []}
    finding_ref = host.record(review_token['logical_id'], 'product', finding,
                              sender=prepared['principal'], context=prepared['context'])
    prepared['record']['findings'] = [finding_ref]
    proof, message = host.assessment_delivery(prepared, subject)
    host.commit(message)
    host.select_proof(subject, proof)
    host.select_basis(actor, subject)
    return subject, token, model, review_token, review


def _append_finding(host, subject, body_factory, logical_id):
    state = host.store.read()
    product = state.resolve(subject, 'product')
    old_proof = next(value['proof'] for value in state.proofs.values() if value['subject'] == subject)
    old_finding = state.resolve(old_proof, 'assessment')['findings'][0]
    actor = {'owner': product['owner'], 'author_record': state.resolve(product['assignment'], 'assignment')}
    prepared = host.prepare_review(actor, subject, suffix=logical_id,
        actor_id='independent-domain-reviewer', evidence=[{'slot_id': 'prior-dcs-review', 'refs': [old_finding]}])
    token = {'context': prepared['context'], 'logical_id': logical_id}
    body = body_factory(token, _manifest(host, prepared['context']))
    assignment = host.store.read().resolve(prepared['assignment'], 'assignment')
    criterion = host.store.read().resolve(host.criteria, 'source')['criteria'][0]['id']
    record = {'owner': assignment['owner'], 'product_kind': 'finding', 'assignment': prepared['assignment'],
        'profile': host.profile, 'inputs': assignment['inputs'],
        'material': [host.material(json.dumps(body))], 'evidence': [], 'limitations': [],
        'related': [{'slot_id': 'subject', 'refs': [subject]},
                    {'slot_id': 'criterion:' + criterion, 'refs': [host.criteria]}]}
    finding = host.record(token['logical_id'], 'product', record,
                          sender=prepared['principal'], context=prepared['context'])
    prepared['record']['findings'] = [old_finding, finding]
    proof, message = host.assessment_delivery(prepared, subject)
    host.commit(message)
    host.select_proof(subject, proof, previous=old_proof)
    host.select_basis(actor, subject)
    principal = host.engagement + ':' + assignment['assigned_actor']
    return body, principal, old_finding, finding


def _receiving(host, subject, model, qa):
    from test_content_workflow import _selected_handoff_fixture
    catalog = content_workflow.load_bindings(ROOT)
    row = next(item for item in catalog['bindings'] if item['handoff_id'] == 'semantic-to-enterprise-publication:1')
    selected = _selected_handoff_fixture(row, model)
    context = next(item['payload'] for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
    def body(token,manifest):
        return {'attestation': token, 'context_manifest': manifest,
            'handoff_id': row['handoff_id'], 'semantic_hash': domain._digest(model),
            'report_hash': qa['report_hash'], 'catalog_hash': catalog['catalog_hash'],
            'criterion': selected['acceptance_criterion'], 'receiving_role': selected['receiving_role'],
            'path_id': context['selected_path'],
            'handoff_content_hash': content_spec.canonical_hash(selected['handoff_content_contract']),
            'unit_reviews': [{'unit_id': unit['id'], 'verdict': 'PASS',
                'rationale': 'Controlled fixture review of the exact selected boundary and intake reference.',
                'evidence': 'Actual native-captured synthetic semantic source; no professional or human approval claimed.'}
                for unit in selected['handoff_content_contract']['units']],
            'verdict': 'PASS', 'evidence': 'Controlled actual receiving body binds this exact source and prior QA report.'}
    acceptance, principal, old_finding, _ = _append_finding(host,subject,body,'actual-receiving-body')
    return acceptance, {principal: [selected['receiving_role']]}, old_finding


def test_exact_native_material_and_selected_review_identity_reject_foreign_tokens(tmp_path, monkeypatch):
    host = _fixture(tmp_path, monkeypatch)
    subject, token, model, review_token, review = _qualified(host, sidecar=True)
    adapter = domain.GovernedDomain(host.store, [{'ref': subject, 'use_scope': host.scope}])
    original_read = host.store.read
    reads = []
    def read():
        reads.append(True)
        return original_read()
    monkeypatch.setattr(host.store, 'read', read)
    with adapter.action():
        maker, checker = adapter.verify(token), adapter.verify(review_token)
        assert maker['principal'] != checker['principal']
        assert maker['invocation'] != checker['invocation']
        assert maker['physical_context'] != checker['physical_context']
        assert maker['physical_context']['provider'] == 'codex'
        assert maker['raw_capture'] == adapter._state.run_details[
            adapter._state.resolve(token['context'], 'context')['run_id']]['semantic_capture']['raw_return_blob_id']
        assert maker['reviewer'] is False and checker['reviewer'] is True
        assert checker['subject_digest'] == domain._digest({k: v for k, v in review.items() if k != 'attestation'})
        assert maker['snapshot_digest'] != domain._digest(model)
        assert adapter.verify(dict(token, logical_id='foreign')) is None
        assert adapter.commercial_callbacks()['identity_verifier'](token) == maker
    assert len(reads) == 1
    source_assignment = original_read().resolve(subject, 'product')['assignment']
    source_record = original_read().resolve(source_assignment, 'assignment')
    setter = source_record['issued_under']
    setter_record = original_read().resolve(setter, 'assignment')
    setter_context = host.context('physical-separation-setter', setter, setter_record)
    reviewer, reviewer_record = host.assignment('physical-separation-reviewer', 'reviewer',
        owner=source_record['owner'], actor='independent-domain-reviewer',
        inputs=[*source_record['inputs'], {'slot_id': 'assessed-subject', 'refs': [subject]}],
        creator={'kind': 'assignment', 'ref': setter}, creator_context=setter_context)
    chooser = host.context('physical-separation-choice', reviewer, reviewer_record, phase='selection')
    host.commit(host.message('decision', {'action': 'select_execution', 'assignment': reviewer, 'previous': None,
        'specialties': ['software-engineer'], 'provider': 'codex', 'workload_class': 'fixture-reviewer',
        'model_selector': 'filled-from-exact-fixture-registry', 'reason': 'Controlled independent reviewer test.',
        'authority_proof': None}, sender={'kind': 'assignment', 'ref': reviewer}, context=chooser))
    choice = original_read().execution_plans[(reviewer['version_id'], host.scope)]
    issued = host.native.issue_batch([{'assignment': reviewer, 'phase': 'work', 'selection': choice}], bound_ms=5000)
    host.native.prepare(issued['invocation_id'])
    author_details = original_read().run_details[original_read().resolve(token['context'], 'context')['run_id']]
    before = host.path.read_bytes()
    with pytest.raises(ValueError) as denied:
        host.native.start(issued['invocation_id'], 'codex', author_details['native']['handle'],
                          {'fixture': 'Attempted reuse of the author physical context.'})
    assert denied.value.code == 'P_ORIGIN'
    assert host.path.read_bytes() == before
    host.native.stop(issued['invocation_id'], {'state': 'not-dispatched', 'fixture': 'Rejected before dispatch.'})
    expires = original_read().resolve(token['context'], 'context')['expires_at_ms']
    with monkeypatch.context() as clock:
        clock.setattr(lc.time, 'time', lambda: (expires + 1) / 1000)
        assert adapter.verify(token)['principal'] == maker['principal']
    with pytest.raises(ValueError):
        domain.GovernedDomain(host.store, [])


def test_current_publication_changes_do_not_inherit_permissions_or_mutate_history(tmp_path, monkeypatch):
    host = _fixture(tmp_path, monkeypatch)
    from test_content_publication import fixture
    from test_content_workflow import _handoff_content_fixture
    source, profile, out = fixture(tmp_path)
    original = json.loads(source.read_text())
    row = next(item for item in content_workflow.load_bindings(ROOT)['bindings']
               if item['handoff_id'] == 'semantic-to-enterprise-publication:1')
    # Admit the complete selected source before native capture. Adding a handoff
    # after qualification would invalidate the exact-material identity being tested.
    original = _handoff_content_fixture(row, copy.deepcopy(original), path_id='draft')
    def semantic(_, token, manifest):
        return dict(original, producer={'attestation': token, 'context_manifest': manifest})
    subject, token, model, _, review = _qualified(host, model_factory=semantic)
    adapter = domain.GovernedDomain(host.store, [{'ref': subject, 'use_scope': host.scope}])
    before = host.path.read_bytes()
    status = adapter.publication_status(model, model['audience'])
    assert status['eligible'] and status['qualified'] and not status['accepted']
    assert not adapter.publication_status(model, model['audience'], 'release')['eligible']
    assert host.path.read_bytes() == before
    with pytest.raises(ValueError, match='audience'):
        adapter.publication_status(model, ['public'])
    with pytest.raises(ValueError, match='exact admitted'):
        adapter.publication_status(dict(model, title='Changed source'))
    with pytest.raises(ValueError, match='operation'):
        adapter.publication_status(model, operation='force')
    source.write_text(json.dumps(model))
    problems, pub, manifest = projection.build(source, profile, out, reviewer=review, governed=adapter)
    assert not problems, problems
    qa = json.loads((out / 'content-qa.json').read_text())
    assert qa['reviewer']['status'] == 'verified-independent-review'
    result = content_workflow.check('semantic-to-enterprise-publication:1', model, qa, ROOT,
        governed=adapter)
    assert result['status'] == 'ACCEPTANCE_PENDING'
    assert 'RECEIVER_ROLE_UNASSIGNED' in result['findings']
    acceptance, receiving, prior_finding = _receiving(host, subject, model, qa)
    result = content_workflow.check('semantic-to-enterprise-publication:1', model, qa, ROOT,
        acceptance=acceptance, receiving_assignments=receiving, governed=adapter)
    assert result['status'] == 'ACCEPTANCE_VERIFIED', result['findings']
    assert result['production_release_authorized'] is False
    destination = tmp_path / 'actual-draft.html'
    publication.render(pub, 'html', destination, {}, manifest, out, governed=adapter)
    assert destination.is_file() and 'DRAFT' in destination.read_text()
    owner = host.store.read().resolve(subject, 'product')['owner']
    host.commit(host.owner_decision(owner, {'action': 'invalidate',
        'reason': 'Explicitly withdraw the reused independent DCS finding.', 'subjects': [prior_finding]}))
    with pytest.raises(ValueError, match='Current Gen2'):
        content_workflow.check('semantic-to-enterprise-publication:1', model, qa, ROOT,
            acceptance=acceptance, receiving_assignments=receiving, governed=adapter)
    host.transition_inputs('New governing input, no inherited review.')
    assert not adapter.publication_status(model)['eligible']
    assert adapter.verify(token) is None
    problems, _, _ = projection.build(source, profile, tmp_path / 'blocked', reviewer=review, governed=adapter)
    assert problems and not (tmp_path / 'blocked').exists()
    with pytest.raises(ValueError, match='Current Gen2'):
        publication.render(pub, 'html', tmp_path / 'forbidden.html', {}, manifest, out, governed=adapter)
    assert not (tmp_path / 'forbidden.html').exists()


def test_missing_material_and_unbound_commercial_mapping_fail_without_authority(tmp_path, monkeypatch):
    host = _fixture(tmp_path, monkeypatch)
    subject, token, model, _, _ = _qualified(host)
    adapter = domain.GovernedDomain(host.store, [{'ref': subject, 'use_scope': host.scope}])
    with pytest.raises(ValueError, match='current Gen2 pin'):
        projection.build(tmp_path/'unread-source',tmp_path/'profile',tmp_path/'forbidden-build',operation='accepted')
    with pytest.raises(ValueError, match='supported publication'):
        projection.build(tmp_path/'unread-source',tmp_path/'profile',tmp_path/'unknown-build',operation='force')
    with pytest.raises(ValueError, match='current Gen2 pin'):
        publication.render_verified({}, {}, tmp_path, 'html', tmp_path/'forbidden-render', {}, operation='release')
    with pytest.raises(ValueError, match='current Gen2 pin'):
        proposal.publication_handoff(tmp_path/'unread-package','client-proposal',tmp_path/'forbidden-handoff',operation='release')
    assert not any((tmp_path/name).exists() for name in ('forbidden-build','unknown-build','forbidden-render','forbidden-handoff'))
    assert not adapter.fabric_resolver({'data': {}}, {'entities': []})
    material = host.store.read().resolve(subject, 'product')['material'][0]
    (host.store.material / material).unlink()
    assert adapter.verify(token) is None
    with pytest.raises(OSError):
        adapter.publication_status(model)


def _commercial_fixture(tmp_path, monkeypatch):
    host = _fixture(tmp_path, monkeypatch)
    from test_commercial_core import complete_snapshot
    snapshot, _ = complete_snapshot()
    claim = next(item for item in snapshot['entities'] if item['type'] == 'Claim')
    def claim_model(_, token, manifest):
        value = copy.deepcopy(claim)
        value['data']['producer_attestation'] = token
        value['data']['context_manifest'] = manifest
        return value
    def claim_review(model, token, manifest):
        value = copy.deepcopy(next(item for item in snapshot['entities'] if item['type'] == 'Review'))
        value['data'].update(attestation=token, context_manifest=manifest, reviewed_digest=domain._digest(model))
        return value
    output, _, exact_claim, _, exact_review = _qualified(host, model_factory=claim_model, review_factory=claim_review)
    snapshot['entities'] = [exact_claim if item['type'] == 'Claim' else exact_review if item['type'] == 'Review'
                            else item for item in snapshot['entities']]
    point = {'ref': output, 'use_scope': host.scope}
    assignment = host.store.read().resolve(output, 'product')['assignment']
    domain_contract = next(item for item in snapshot['entities'] if item['type'] == 'DomainContract')
    fragment = next(item for item in snapshot['entities'] if item['type'] == 'Fragment')
    fragment['data']['governed_output'] = point
    contract = next(item for item in snapshot['entities'] if item['type'] == 'ExecutionContract')
    removed = {item['version_id'] for item in snapshot['entities']
               if item['type'] == 'ExecutionContract' and item is not contract}
    snapshot['entities'] = [item for item in snapshot['entities'] if item['version_id'] not in removed]
    snapshot['relations'] = [edge for edge in snapshot['relations']
                             if edge['input'] not in removed and edge['output'] not in removed]
    snapshot['relations'].append({'type': 'derives', 'input': contract['version_id'], 'output': fragment['version_id']})
    mapping = domain.commercial_mapping(snapshot, domain_contract['version_id'], assignment, 1, [point])
    _, _, _, binding = _append_finding(host,output,lambda *_: mapping,'commercial-binding')
    contract['data'].update(governed_assignment=assignment,
        governed_binding={'ref': binding, 'use_scope': host.scope})
    adapter = domain.GovernedDomain(host.store, [point, contract['data']['governed_binding']])
    return host, snapshot, contract, adapter


def test_commercial_binding_matches_actual_domain_claim_output_and_owner(tmp_path, monkeypatch):
    host, snapshot, contract, adapter = _commercial_fixture(tmp_path,monkeypatch)
    assignment = contract['data']['governed_assignment']
    domain_contract = next(item for item in snapshot['entities'] if item['type'] == 'DomainContract')
    assert adapter.fabric_resolver(contract, snapshot)
    with adapter.action():
        ready = commercial_core.readiness(snapshot, **adapter.commercial_callbacks())
    assert ready['ready'], ready['blockers']
    assert ready['authority_granted'] is False and ready['assurance']['unmeasured_claims']
    changed = copy.deepcopy(snapshot)
    next(item for item in changed['entities'] if item['type'] == 'Claim')['data']['scope'] = 'Changed claim.'
    assert not adapter.fabric_resolver(contract, changed)
    assert not adapter.fabric_resolver(dict(data=dict(contract['data'], layer=2)), snapshot)
    with pytest.raises(ValueError):
        domain.commercial_mapping(snapshot, domain_contract['version_id'], assignment, 1, [])


@pytest.mark.parametrize('preparation_elapsed_ms', [0, 5001])
def test_prepared_proposal_handoff_uses_actual_component_provenance_and_current_gates(
        tmp_path, monkeypatch, preparation_elapsed_ms):
    from test_commercial_proposal import fixture
    # This checks provenance and gates, not CPU scheduling. Advance the issued
    # five-second native allowance explicitly to exercise expiry deterministically.
    clock_ms = [int(lc.time.time() * 1000)]
    monkeypatch.setattr(lc.time, 'time', lambda: clock_ms[0] / 1000)
    host, snapshot, _, existing = _commercial_fixture(tmp_path,monkeypatch)
    data = fixture()
    plain = tmp_path / 'plain-draft'
    proposal.prepare_package(data,plain,ROOT)
    markdown = (plain / 'client-proposal.md').read_text()
    publication_entity = next(item for item in snapshot['entities'] if item['version_id'] == 'publication@1')
    publication_entity['classification'] = 'client-contract'
    publication_entity['data'].update({key: 'Controlled contractual disclosure; no real approval or deployment.'
                                      for key in commercial_core.MANDATORY})
    publication_entity['data']['proposal_markdown'] = markdown
    data['canonical_snapshot'] = snapshot
    data['disclosure_policy'] = {'version': 'controlled', 'mandatory_disclosure': sorted(commercial_core.MANDATORY),
        'surfaces': ['json-payload'], 'fields': {'Publication': [*sorted(commercial_core.MANDATORY),'proposal_markdown']}}
    staged = tmp_path / 'actual-prepared'
    def component(_, token, manifest):
        data['documents']['client-proposal']['producer'] = {'attestation': token, 'context_manifest': manifest}
        result = proposal.prepare_package(data,staged,ROOT)
        assert result['prepared_documents'] == len(proposal.CORE_KINDS)
        clock_ms[0] += preparation_elapsed_ms
        return json.loads((staged / 'client-proposal.semantic.json').read_text())
    if preparation_elapsed_ms:
        with pytest.raises(ValueError) as rejected:
            _qualified(host,'client-component',model_factory=component,question='why')
        assert rejected.value.code == 'P_STATE'
        assert 'no current productive, handling or speculative execution right' in str(rejected.value)
        return
    subject, token, model, _, review = _qualified(host,'client-component',model_factory=component,question='why')
    assert model['producer']['attestation'] == token
    package = json.loads((staged / 'proposal-package.json').read_text())
    assert {item['kind'] for item in package['documents']} == set(proposal.CORE_KINDS)
    assert all((staged / item['semantic_ref']).is_file() for item in package['documents'])
    adapter = domain.GovernedDomain(host.store,[*existing.producers,{'ref': subject,'use_scope':host.scope}])
    output = tmp_path / 'actual-projection'
    result = proposal.publication_handoff(staged / 'proposal-package.json','client-proposal',output,ROOT,
        reviewer=review,governed=adapter)
    assert result['status'] == 'DRAFT_PROJECTED', result
    assert not result['authority_granted'] and not result['release_ready']
    assert (output / 'projection-manifest.json').is_file()
    source = staged / 'client-proposal.semantic.json'
    exact = source.read_bytes()
    source.write_text(json.dumps(dict(model,title='Unadmitted edited component')))
    result = proposal.publication_handoff(staged / 'proposal-package.json','client-proposal',tmp_path/'edited',ROOT,
        reviewer=review,governed=adapter)
    assert result['status'] == 'BLOCKED' and not (tmp_path/'edited').exists()
    source.write_bytes(exact)
    owner = host.store.read().resolve(subject,'product')['owner']
    host.commit(host.owner_decision(owner,{'action':'invalidate','subjects':[subject],
        'reason':'Withdraw only this exact governed proposal component.'}))
    result = proposal.publication_handoff(staged / 'proposal-package.json','client-proposal',tmp_path/'withdrawn',ROOT,
        reviewer=review,governed=adapter)
    assert result['status'] == 'BLOCKED' and not (tmp_path/'withdrawn').exists()


def test_internal_locator_arguments_open_existing_store_without_source_selected_trust(tmp_path, monkeypatch, capsys):
    parser = argparse.ArgumentParser()
    domain.add_arguments(parser)
    assert domain.from_arguments(parser.parse_args([])) == (None, None)
    with pytest.raises(ValueError):
        domain.from_arguments(parser.parse_args(['--governed-engagement', 'missing']))
    with pytest.raises(ValueError, match='exact host pin'):
        domain.from_arguments(parser.parse_args(['--governed-operation', 'release']))
    host = _fixture(tmp_path, monkeypatch)
    subject, _, model, _, _ = _qualified(host)
    uses = tmp_path / 'uses.json'
    uses.write_text(json.dumps([{'ref': subject, 'use_scope': host.scope}]))
    args = parser.parse_args(['--governed-journal', str(host.path),
        '--governed-engagement', host.engagement, '--governed-uses', str(uses)])
    adapter, authority = domain.from_arguments(args)
    assert authority is None and adapter.publication_status(model)['qualified']
    from test_commercial_core import snapshot
    data = tmp_path / 'commercial.json'
    data.write_text(json.dumps(snapshot()))
    assert commercial.main(['--profile', 'commercial-delivery/1', 'readiness', str(data),
        '--governed-journal', str(host.path), '--governed-engagement', host.engagement,
        '--governed-uses', str(uses)]) == 2
    assert json.loads(capsys.readouterr().out)['authority_granted'] is False
    with pytest.raises(SystemExit):
        commercial.main(['--profile','commercial-delivery/1','readiness',str(data),
            '--governed-operation','release'])
    with pytest.raises(SystemExit):
        content_workflow.main(['check','semantic-to-enterprise-publication:1',str(data),str(data),
            '--governed-operation','accepted'])
    required = commercial_core.readiness(snapshot(), required_controls=('mount_isolation',))
    assert any('mount_isolation unverified' in reason for reason in required['blockers'])
