# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Accepted scoped facts advance work; explicit changes withdraw their use."""
import copy
import json

import pytest

from governed_fixtures import HUMAN, lc
from test_governed_sabsa_runtime import ContentHarness
import governed_sabsa as content


def _host(directory, monkeypatch, *, scopes=('default',)):
    host = ContentHarness(directory, monkeypatch, engagement='accepted-use', use_scopes=scopes)
    host.bootstrap(include_neighbor=True)
    return host


def _coordinator(host):
    inputs = [{'slot_id': 'l0:' + reference['logical_id'], 'refs': [reference]}
              for reference in host.l0_sources]
    uses = []
    if host.scope != 'default':
        for index, reference in enumerate(host.l0_sources):
            if reference in (host.routing_policy, host.semantic_policy_ref):
                uses.extend([{'at': '/inherited/' + str(index), 'use_scope': 'default'},
                             {'at': '/inputs/' + str(index) + '/refs/0', 'use_scope': 'default'}])
    return host.assignment('coordinator-' + host.scope, 'setter',
        owner=host.owner(work_kind='integration'), inputs=inputs, input_uses=uses)


def _scope(host, scope):
    host.enter_scope(scope)
    # The ordinary base harness restores domain sources; this semantic fixture
    # also retains its already bootstrapped common content-policy reference.
    if host.semantic_policy_ref not in host.l0_sources:
        host.l0_sources.append(host.semantic_policy_ref)


def _local(host, question, suffix, prerequisites=()):
    parent, body = _coordinator(host)
    inputs = copy.deepcopy(body['inputs'])
    inputs.append({'slot_id': f'L1:service-controls:{question}-input', 'refs': [host.input_a]})
    inputs.extend({'slot_id': 'provided-result-' + str(index), 'refs': [reference]}
                  for index, reference in enumerate(prerequisites))
    issuer = host.context(suffix + '-issuer', parent, body)
    try:
        setter, record = host.assignment(suffix + '-setter', 'setter', owner=host.owner(question),
            inputs=inputs, creator={'kind': 'assignment', 'ref': parent}, creator_context=issuer)
    except AssertionError:
        host.cancel_run(issuer)
        raise
    host.setters[(host.scope, json.dumps(record['owner'], sort_keys=True))] = (setter, record)
    return host.setup_author(question=question, suffix=suffix)


def _delivered(host, question, suffix, prerequisites=()):
    actor = _local(host, question, suffix, prerequisites)
    material = (lc.canonical(host.semantic(private=False)) if question == 'why'
                else ('Actual owned answer ' + suffix).encode())
    subject, record = host.product(suffix + '-answer', actor,
                                  material=[host.store.put_blob(material)])
    host.commit(host.submission(actor, subject, record))
    return actor, subject


def _qualify(host, actor, subject, suffix):
    proof, _ = host.review(actor, subject, suffix=suffix, actor_id=host.scope + '-reviewer-' + actor['owner']['question'])
    host.select_proof(subject, proof)
    host.select_basis(actor, subject)
    return proof


def test_ordinary_work_uses_accepted_parent_fact_without_revalidating_its_content(tmp_path, monkeypatch):
    host = _host(tmp_path, monkeypatch)
    parent_actor, parent = _delivered(host, 'why', 'accepted-parent')
    _qualify(host, parent_actor, parent, 'parent-positive-review')
    state = host.store.read()
    parent_record = state.resolve(parent, 'product')
    parent_material = set(parent_record['material'])
    evaluate, validate, payload, read = lc.State.evaluate, content.validate_product, content._payload, lc.State._validation_bytes

    def forbid_parent_evaluation(current, subject, *args, **kwargs):
        assert subject != parent, 'Ordinary work recursively evaluated an already accepted parent'
        return evaluate(current, subject, *args, **kwargs)

    def forbid_parent_validation(current, record, *args, **kwargs):
        assert record != parent_record, 'Ordinary work revalidated an accepted parent record'
        return validate(current, record, *args, **kwargs)

    def forbid_parent_payload(current, record, *args, **kwargs):
        assert record != parent_record, 'Ordinary work reparsed accepted semantic material'
        return payload(current, record, *args, **kwargs)

    def forbid_parent_read(current, identifier, *args, **kwargs):
        assert identifier not in parent_material, 'Ordinary work reread accepted ancestor material'
        return read(current, identifier, *args, **kwargs)

    with monkeypatch.context() as traps:
        traps.setattr(lc.State, 'evaluate', forbid_parent_evaluation)
        traps.setattr(content, 'validate_product', forbid_parent_validation)
        traps.setattr(content, '_payload', forbid_parent_payload)
        traps.setattr(lc.State, '_validation_bytes', forbid_parent_read)
        actor, pending = _delivered(host, 'how', 'pending-dependent', [parent])
        current = host.store.read()
        assert not current._status(pending, host.scope)['applicable']
        assert not current._governing_input({'ref': pending, 'use_scope': host.scope}, live=True)
        profile = current.resolve(host.profile, 'profile')
        obligation = next(item for item in profile['obligations']
                          if item['owner'] == actor['owner'] and item['role'] == 'answer')
        slot = {'kind': 'basis', 'owner': actor['owner'], 'slot_id': obligation['slot_id']}
        unreviewed = host.owner_decision(actor['owner'], {'action': 'select',
            'reason': 'A newly delivered result cannot govern work before independent review.',
            'slot': slot, 'candidate': pending,
            'previous': current.selections.get(lc._proof_key(host.scope, slot))})
        before = host.path.read_bytes()
        rejected = host.send(unreviewed)
        assert rejected['status'] == 'rejected' and rejected['error']['code'] == 'P_PROOF'
        assert host.path.read_bytes() == before
        host.cancel_run(unreviewed['context'])
        _qualify(host, actor, pending, 'dependent-positive-review')
        assert host.store.read()._status(pending, host.scope)['applicable']
        invalid = _local(host, 'how', 'reviewed-input', [pending])
        wrong_question = host.semantic(private=False)
        wrong_question['units'][0]['statements'] = [
            'This distinct new WHY statement is still outside the HOW assignment.']
        subject, record = host.product('foreign-question-units', invalid,
            material=[host.store.put_blob(lc.canonical(wrong_question))])
        before = host.path.read_bytes()
        rejected = host.send(host.submission(invalid, subject, record))
        assert rejected['status'] == 'rejected' and rejected['error']['code'] == 'P_SCOPE'
        assert host.path.read_bytes() == before
        assert subject['version_id'] not in host.store.read().versions


def test_negative_review_withdraws_dependent_use_without_rewriting_truth_or_reviving_descendants(tmp_path, monkeypatch):
    host = _host(tmp_path, monkeypatch, scopes=('default', 'retained'))
    actor, parent = _delivered(host, 'why', 'parent')
    old_pass = _qualify(host, actor, parent, 'parent-pass')
    child_actor, child = _delivered(host, 'how', 'dependent', [parent])
    _qualify(host, child_actor, child, 'dependent-pass')
    host.accept(child)
    host.accept(child, release=True)
    before = host.store.read()
    history = {ref['version_id']: copy.deepcopy(before.resolve(ref)) for ref in (parent, child, old_pass)}
    permissions = [event['decision_id'] for event in before.events
                   if event['kind'] in {'accept', 'release'} and event['subject'] == child]
    _scope(host, 'retained')
    other_actor, other = _delivered(host, 'why', 'independent-scope')
    _qualify(host, other_actor, other, 'independent-pass')
    host.accept(other)
    host.accept(other, release=True)
    _scope(host, 'default')
    negative, _ = host.review(actor, parent, suffix='parent-negative', verdict='rework_required',
                              actor_id='default-reviewer-why')
    receipt = host.select_proof(parent, negative, previous=old_pass)
    withdrawn = host.store.read()
    selection = next(reference for reference in receipt['created_versions']
                     if withdrawn.versions[reference['version_id']]['kind'] == 'delivery.decision'
                     and withdrawn.resolve(reference)['message']['payload'].get('candidate') == negative)
    assert withdrawn._status(negative, host.scope) == {'validity': 'valid', 'applicable': True}
    finding_basis = host.store.current_basis({'protocol': lc.PROTOCOL,
                                             'subject': negative, 'assessment_scope': host.scope})
    assert finding_basis['eligibility']['qualified']
    assert {'ref': parent, 'use_scope': host.scope} not in finding_basis['closure']
    for ref in (parent, child):
        assert {'ref': ref, 'use_scope': host.scope} in receipt['affected_uses']
        assert not withdrawn._status(ref, host.scope)['applicable']
        assert withdrawn.resolve(ref) == history[ref['version_id']]
        basis = host.store.current_basis({'protocol': lc.PROTOCOL,
                                         'subject': ref, 'assessment_scope': host.scope})
        assert {'ref': selection, 'use_scope': host.scope} in basis['cancelled_by']
    assert withdrawn.resolve(old_pass) == history[old_pass['version_id']]
    assert all(identifier in withdrawn.decisions['cancelled'] for identifier in permissions)
    assert not withdrawn.evaluate(child, host.scope)['release_eligible']
    assert withdrawn.evaluate(other, 'retained')['release_eligible']

    fresh, _ = host.review(actor, parent, suffix='parent-fresh-positive', actor_id='default-reviewer-why')
    host.select_proof(parent, fresh, previous=negative)
    assert not host.store.read()._status(parent, host.scope)['applicable']
    host.select_basis(actor, parent)
    restored = host.store.read()
    assert restored._status(parent, host.scope)['applicable']
    assert not restored._status(child, host.scope)['applicable']
    assert not restored.evaluate(child, host.scope)['accepted']
    assert not restored.evaluate(child, host.scope)['release_eligible']
    assert all(identifier in restored.decisions['cancelled'] for identifier in permissions)
    assert restored.evaluate(other, 'retained')['release_eligible']


def test_missing_current_material_blocks_final_decisions_without_blocking_metadata_use(tmp_path, monkeypatch):
    host = _host(tmp_path, monkeypatch)
    parent_actor, parent = _delivered(host, 'why', 'material-parent')
    _qualify(host, parent_actor, parent, 'material-parent-pass')
    actor, output = _delivered(host, 'how', 'material-dependent', [parent])
    _qualify(host, actor, output, 'material-dependent-pass')
    host.accept(output)
    host.accept(output, release=True)
    basis = host.store.evaluate(output)
    identifier = host.store.read().resolve(parent, 'product')['material'][0]
    raw = host.store._blob(identifier)
    (host.store.material / identifier).unlink()
    try:
        # A new assignment consumes the accepted dependency fact, not its entire
        # ancestral file closure. Actual file consumption and final gates differ.
        _local(host, 'when', 'metadata-only-next-work', [output])
        current = host.store.evaluate(output)
        assert not current['qualified'] and not current['accepted'] and not current['release_eligible']
        for action in ('accept', 'release'):
            message = host.message('decision', {'action': action,
                'reason': 'A valid signature cannot replace missing current supporting material.',
                'subject': output, 'closure_hash': basis['closure_hash'], 'authority_proof': '0' * 64,
                **({'acceptance': basis['acceptances'][0]} if action == 'release' else {})}, sender=HUMAN)
            proof = host.human_proof(message, 'delivery-' + action)
            before = host.path.read_bytes()
            rejected = host.send(message, authority_proof=proof)
            assert rejected['status'] == 'rejected' and rejected['error']['code'] == 'P_PROOF'
            assert host.path.read_bytes() == before
        rendered = content.render(host.store.read(), output, audience='public')
        assert not rendered['publication']['eligible']
        assert not rendered['publication']['release_eligible']
        assert all(not view['json']['units'] for view in rendered['views'])
    finally:
        assert host.store.put_blob(raw) == identifier
