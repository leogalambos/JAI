# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Semantic return encoding contracts, without native calls or Store admission."""
import copy
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import governed_semantic as semantic
import lifecycle as lc


def _packet(phase='work'):
    ref = lambda name: {'engagement': 'encoding', 'scope': 'default', 'logical_id': name,
                        'version_id': ('a' if name == 'assignment' else 'b') * 64}
    assignment, profile = ref('assignment'), ref('profile')
    return {'member_key': 'issued-member', 'assignment': assignment, 'context': ref('context'),
            'execution': {'phase': phase}, 'manifest': [
                {'ref': assignment, 'use_scope': 'default', 'record': {
                    'owner': {'layer': 1, 'work_kind': 'question', 'question': 'what', 'work_item': 'service'},
                    'profile': profile, 'routing': profile, 'use_scope': 'default', 'criteria': ref('criteria'),
                    'responsibility': 'author', 'inputs': []}},
                {'ref': profile, 'use_scope': 'default', 'record': {
                    'owner': {'kind': 'controller', 'id': 'host'}}}]}


def _answer():
    return {'format': 'jai.semantic-return/1', 'results': [{
        'member': 'issued-member', 'kind': 'author', 'logical_id': 'answer',
        'evidence': [], 'limitations': ['A controlled codec fixture.'],
        'materials': [{'json': {'price': 12.5, 'business_id': 'unchanged',
                                'reference_like': {'alias': 'assignment'},
                                'body': 'Keep {alias: assignment} as authored.'}}]}]}


def test_compile_semantic_preserves_material_and_derives_only_structural_metadata():
    packet, value, blobs = _packet(), _answer(), {}
    original = copy.deepcopy(value)
    def writer(raw):
        identity = lc.blob(raw)
        blobs[identity] = raw
        return identity
    encoded = semantic.compile_semantic(packet, value, writer)
    product = encoded['records'][0]
    assert encoded['assignment'] == packet['assignment']
    assert encoded['context'] == packet['context']
    assert product['record']['owner'] == packet['manifest'][0]['record']['owner']
    assert json.loads(blobs[product['record']['material'][0]]) == value['results'][0]['materials'][0]['json']
    assert encoded['intents'][0]['payload']['candidate']['logical_id'] == 'answer'
    assert value == original
    assert semantic.compile_semantic(packet, value, writer) == encoded


def test_compile_semantic_requires_unique_exact_member_and_complete_semantics():
    packet, value = _packet(), _answer()
    writer = lc.blob
    with pytest.raises(ValueError):
        semantic.compile_semantic(packet, {'format': 'jai.semantic-return/1', 'results': []}, writer)
    duplicated = {**value, 'results': value['results'] * 2}
    with pytest.raises(ValueError, match='member'):
        semantic.compile_semantic(packet, duplicated, writer)
    for field in ('limitations', 'evidence'):
        missing = copy.deepcopy(value)
        del missing['results'][0][field]
        with pytest.raises(ValueError):
            semantic.compile_semantic(packet, missing, writer)
    conflicting = copy.deepcopy(value)
    conflicting['results'][0]['owner'] = {'layer': 6}
    with pytest.raises(ValueError, match='semantic'):
        semantic.compile_semantic(packet, conflicting, writer)


def test_compile_semantic_rejects_unknown_alias_and_material_identity_forgery():
    value = _answer()
    value['results'][0]['evidence'] = [{'alias': 'unissued'}]
    with pytest.raises(ValueError, match='alias'):
        semantic.compile_semantic(_packet(), value, lc.blob)
    with pytest.raises(ValueError, match='material'):
        semantic.compile_semantic(_packet(), _answer(), lambda raw: 'f' * 64)
    nonfinite = _answer()
    nonfinite['results'][0]['materials'][0]['json']['price'] = float('nan')
    with pytest.raises(ValueError):
        semantic.compile_semantic(_packet(), nonfinite, lc.blob)


def test_compile_semantic_keeps_positive_finding_and_requires_actual_verdict():
    packet = _packet()
    assignment = packet['manifest'][0]['record']
    assignment['responsibility'] = 'reviewer'
    packet['assessment_basis'] = {'subject': packet['assignment'], 'closure': [], 'hash': 'c' * 64}
    finding = {'logical_id': 'review-observation', 'criterion': 'boundary',
               'observation': 'The declared evidence supports the criterion.',
               'materials': [{'json': {'verdict': 'supported', 'unit_id': 'actual-unit', 'ratio': 0.5}}],
               'evidence': [], 'limitations': []}
    result = {'member': packet['member_key'], 'kind': 'reviewer', 'logical_id': 'review',
              'verdict': 'supported', 'rationale': 'Actual explicit assessment.',
              'findings': [finding], 'conditions': []}
    envelope = {'format': 'jai.semantic-return/1', 'results': [result]}
    encoded = semantic.compile_semantic(packet, envelope, lc.blob)
    assert encoded['records'][0]['record']['product_kind'] == 'finding'
    assert encoded['records'][1]['record']['verdict'] == 'supported'
    assert len(encoded['records'][1]['record']['findings']) == 1
    assert encoded['intents'][0]['payload']['findings'] == encoded['records'][1]['record']['findings']
    missing = copy.deepcopy(envelope)
    del missing['results'][0]['verdict']
    with pytest.raises(ValueError, match='semantic'):
        semantic.compile_semantic(packet, missing, lc.blob)


def test_compile_semantic_selection_is_actual_choice_not_a_work_result():
    packet = _packet('selection')
    selection = {'member': packet['member_key'], 'kind': 'selection',
                 'specialties': ['software-engineer'], 'provider': 'codex',
                 'workload_class': 'standard', 'model_selector': 'configured-model',
                 'reason': 'Actual professional choice for this fixture.', 'previous': None}
    value = {'format': 'jai.semantic-return/1', 'results': [selection]}
    result = semantic.compile_semantic(packet, value, lc.blob)
    assert result['records'] == []
    assert result['intents'][0]['payload']['specialties'] == selection['specialties']
    assert result['intents'][0]['payload']['previous'] is None
    with pytest.raises(ValueError, match='responsibility'):
        semantic.compile_semantic(packet, _answer(), lc.blob)


def test_compile_semantic_material_boundary_and_declared_handle_alias():
    packet, value, written = _packet(), _answer(), []
    reference = copy.deepcopy(packet['assignment'])
    reference['logical_id'] = 'evidence'
    packet['manifest'].append({'ref': reference, 'handle': 'issued-evidence', 'record': {}, 'use_scope': 'default'})
    value['results'][0]['evidence'] = [{'alias': 'issued-evidence'}]
    value['results'][0]['materials'] = [{'text': 'Actual text.'}, {'blob': 'd' * 64}]
    def writer(raw):
        written.append(raw)
        return lc.blob(raw)
    result = semantic.compile_semantic(packet, value, writer)
    assert written == [b'Actual text.']
    assert result['records'][0]['record']['material'] == [lc.blob(b'Actual text.'), 'd' * 64]
    assert result['intents'][0]['payload']['evidence'] == [reference]
    value['results'][0]['materials'] = []
    with pytest.raises(ValueError, match='semantic'):
        semantic.compile_semantic(packet, value, writer)


def test_compile_semantic_setter_preserves_actual_question_and_owned_criteria():
    packet = _packet()
    packet['manifest'][0]['record']['responsibility'] = 'setter'
    specification = {'question': 'What service boundary is required?',
                     'author_task': 'Describe the service boundary.',
                     'reviewer_task': 'Assess the described boundary against the criterion.'}
    result = {'member': packet['member_key'], 'kind': 'setter', 'logical_id': 'owned-criteria',
              'materials': [{'text': 'Actual local requirement.'}],
              'criteria': [{'id': 'boundary', 'requirement': {'alias': 'assignment'},
                            'statement': 'State the service boundary.', 'evidence_slots': []}],
              'inherited': [{'alias': 'assignment'}],
              'procedure': {'kind': 'question', 'specification': specification,
                            'previous': None, 'reason': 'Actual local setter procedure.'}}
    value = {'format': 'jai.semantic-return/1', 'results': [result]}
    encoded = semantic.compile_semantic(packet, value, lc.blob)
    assert encoded['records'][0]['record']['criteria'][0]['statement'] == result['criteria'][0]['statement']
    assert encoded['intents'][0]['payload']['action'] == 'configure_procedure'
    assert encoded['intents'][0]['payload']['specification'] == specification
    missing = copy.deepcopy(value)
    del missing['results'][0]['procedure']['specification']['reviewer_task']
    with pytest.raises(ValueError, match='semantic'):
        semantic.compile_semantic(packet, missing, lc.blob)


def test_compile_semantic_independent_member_failure_does_not_poison_valid_member():
    packet, value = _packet(), _answer()
    value['results'].append({'member': 'other-issued-member', 'kind': 'author'})
    result = semantic.compile_semantic(packet, value, lc.blob)
    assert result['records'][0]['logical_id'] == 'answer'
    other_packet = {**packet, 'member_key': 'other-issued-member'}
    with pytest.raises(ValueError, match='semantic'):
        semantic.compile_semantic(other_packet, value, lc.blob)
    with pytest.raises(ValueError, match='member'):
        semantic.compile_semantic({**packet, 'member_key': 'absent-member'}, value, lc.blob)


@pytest.mark.parametrize('kind,product_kind,message_type', [
    ('integrator', 'bundle', 'submission'), ('measurement', 'observation', 'observation')])
def test_compile_semantic_integration_and_measurement_keep_actual_choices(kind, product_kind, message_type):
    packet = _packet()
    packet['manifest'][0]['record']['responsibility'] = kind
    result = {'member': packet['member_key'], 'kind': kind, 'logical_id': 'actual-result',
              'materials': [{'text': 'Actual producer result.'}], 'limitations': []}
    if kind == 'integrator':
        result.update(answers=[{'alias': 'assignment'}], related=[])
    else:
        result.update(inputs=[], evidence=[])
    encoded = semantic.compile_semantic(packet, {'format': 'jai.semantic-return/1', 'results': [result]}, lc.blob)
    assert encoded['records'][0]['record']['product_kind'] == product_kind
    assert encoded['intents'][0]['message_type'] == message_type
    if kind == 'integrator':
        assert encoded['records'][0]['record']['related'] == [{'slot_id': 'answers', 'refs': [packet['assignment']]}]


def test_compile_semantic_receiver_never_infers_acceptance():
    packet = _packet()
    packet['manifest'][0]['record']['responsibility'] = 'receiver'
    packet['assessment_basis'] = {'subject': packet['assignment'], 'closure': [], 'hash': 'c' * 64}
    result = {'member': packet['member_key'], 'kind': 'receiver', 'logical_id': 'receiving-review',
              'verdict': 'information_required', 'rationale': 'Required external information is absent.',
              'findings': [], 'conditions': []}
    encoded = semantic.compile_semantic(packet, {'format': 'jai.semantic-return/1', 'results': [result]}, lc.blob)
    assert encoded['records'][0]['record']['verdict'] == 'information_required'
    assert encoded['intents'][0]['payload']['verdict'] == 'information_required'
    assert encoded['intents'][0]['payload']['interface'] == packet['manifest'][0]['record']['criteria']


def test_compile_semantic_owner_reformulation_keeps_actual_new_criteria_and_targets():
    packet = _packet()
    packet['manifest'][0]['record']['responsibility'] = 'setter'
    source = {'logical_id': 'revised-criteria', 'materials': [{'text': 'Revised owner requirement.'}],
              'criteria': [{'id': 'boundary', 'requirement': {'alias': 'assignment'},
                            'statement': 'Describe the revised boundary.', 'evidence_slots': []}],
              'inherited': [{'alias': 'assignment'}]}
    action = {'member': packet['member_key'], 'kind': 'owner_action', 'criteria_source': source,
              'decision': {'action': 'reformulate', 'subject': {'alias': 'criteria'},
                           'replacement': {'alias': 'replacement_criteria'},
                           'reason': 'Actual owner changes the local criterion.'}}
    value = {'format': 'jai.semantic-return/1', 'results': [action]}
    encoded = semantic.compile_semantic(packet, value, lc.blob)
    assert encoded['records'][0]['logical_id'] == 'revised-criteria'
    decision = encoded['intents'][0]['payload']
    assert decision['subject'] == packet['manifest'][0]['record']['criteria']
    assert decision['replacement']['logical_id'] == source['logical_id']
    assert decision['authority_proof'] is None
    assert decision['reason'] == action['decision']['reason']
    assert action['decision']['replacement'] == {'alias': 'replacement_criteria'}


def test_compile_semantic_owner_action_rejects_reserved_actions_and_foreign_responsibility():
    packet = _packet()
    packet['manifest'][0]['record']['responsibility'] = 'setter'
    action = {'member': packet['member_key'], 'kind': 'owner_action',
              'decision': {'action': 'invalidate', 'subjects': [{'alias': 'assignment'}],
                           'reason': 'Actual local owner cancellation.'}}
    envelope = {'format': 'jai.semantic-return/1', 'results': [action]}
    encoded = semantic.compile_semantic(packet, envelope, lc.blob)
    assert 'authority_proof' not in encoded['intents'][0]['payload']
    for responsibility in ('author', 'reviewer'):
        foreign = copy.deepcopy(packet)
        foreign['manifest'][0]['record']['responsibility'] = responsibility
        with pytest.raises(ValueError, match='responsibility'):
            semantic.compile_semantic(foreign, envelope, lc.blob)
    action['decision']['action'] = 'accept'
    with pytest.raises(ValueError, match='semantic'):
        semantic.compile_semantic(packet, envelope, lc.blob)


def test_compile_semantic_owner_selection_resolves_only_typed_nested_reference():
    packet = _packet()
    packet['manifest'][0]['record']['responsibility'] = 'setter'
    decision = {'action': 'select', 'candidate': {'alias': 'subject'}, 'previous': None,
                'slot': {'kind': 'proof', 'subject': {'alias': 'subject'},
                         'role': 'professional_review', 'slot_id': 'review'},
                'reason': 'The phrase {alias: subject} remains actual rationale.'}
    packet['assessment_basis'] = {'subject': packet['assignment']}
    value = {'format': 'jai.semantic-return/1', 'results': [{
        'member': packet['member_key'], 'kind': 'owner_action', 'decision': decision}]}
    encoded = semantic.compile_semantic(packet, value, lc.blob)
    payload = encoded['intents'][0]['payload']
    assert payload['slot']['subject'] == packet['assignment']
    assert payload['reason'] == decision['reason']
    assert payload['previous'] is None


def test_compile_semantic_uses_packet_previous_plan_and_rejects_conflicting_claim():
    packet = _packet('selection')
    packet['execution']['previous'] = packet['assignment']
    result = {'member': packet['member_key'], 'kind': 'selection',
              'specialties': ['software-engineer'], 'provider': 'codex',
              'workload_class': 'standard', 'model_selector': 'configured-model',
              'reason': 'Actual reselection with host-derived identity.'}
    value = {'format': 'jai.semantic-return/1', 'results': [result]}
    encoded = semantic.compile_semantic(packet, value, lc.blob)
    assert encoded['intents'][0]['payload']['previous'] == packet['assignment']
    result['previous'] = None
    with pytest.raises(ValueError, match='previous'):
        semantic.compile_semantic(packet, value, lc.blob)
