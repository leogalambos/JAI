# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Deterministic professionals formulate and review one fictional local layer."""
import base64
import copy
import hashlib
import json
import sys


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def _request(operation, **fields):
    global sequence
    sequence += 1
    print(json.dumps({'id': str(sequence), 'operation': operation, **fields}), flush=True)
    response = json.loads(sys.stdin.readline())
    if not response['ok']:
        raise RuntimeError(response)
    return response['result']


def _material(text):
    return _request('propose', data=base64.b64encode(text.encode()).decode())['blob_id']


def _document(reference):
    record = next(item['record'] for item in packet['manifest'] if item['ref'] == reference)
    identifier = record['material'][0]
    attachment = next(item for item in packet['attachments'] if item['blob_id'] == identifier)
    return json.loads(base64.b64decode(_request('read', handle=attachment['handle'])['data']))


def _record(kind, logical_id, body):
    manifest = {'schema': 'jai.lifecycle.manifest/2', 'logical_id': logical_id, 'kind': 'delivery.' + kind,
                'content': {'engagement': assignment_ref['engagement'], 'scope': assignment_ref['scope'],
                            'record': body}, 'bindings': {}, 'members': []}
    reference = {**assignment_ref, 'logical_id': logical_id,
                 'version_id': hashlib.sha256(b'jai.lifecycle.version.v2\0' + _canonical(manifest)).hexdigest()}
    records.append({'logical_id': logical_id, 'record_type': kind, 'record': body})
    return reference


def _intent(kind, payload):
    intents.append({'message_type': kind, 'recipient': {'kind': 'controller', 'id': 'trusted-controller'},
                    'payload': payload})


def _child(name, responsibility, owner=None, inputs=None, criteria=None, actor=None):
    target_owner = copy.deepcopy(owner or assignment['owner'])
    bindings = copy.deepcopy(inputs if inputs is not None else assignment['inputs'])
    if target_owner['work_kind'] == 'question':
        required = next(item for item in profile['obligations']
                        if item['owner'] == target_owner and item['role'] == 'input')
        if not any(item['slot_id'] == required['slot_id'] for item in bindings):
            domain_input = next(item['ref'] for item in packet['manifest']
                                if item['record'].get('source_role') == 'input')
            bindings.append({'slot_id': required['slot_id'], 'refs': [domain_input]})
    criterion = criteria or assignment['criteria']
    targets = []
    for reference in [ref for binding in bindings for ref in binding['refs']] + [criterion]:
        if reference not in targets:
            targets.append(reference)
    parent_limit = assignment['limits'][0]['ceiling']
    limit = min(parent_limit // 6, 600000) if responsibility == 'setter' else min(parent_limit // 2, 300000)
    body = {'owner': target_owner, 'responsibility': responsibility, 'assigned_actor': actor or name,
            'profile': assignment['profile'], 'routing': assignment['routing'],
            'inherited': assignment['inherited'], 'use_scope': assignment['use_scope'],
            'issued_under': assignment_ref, 'input_uses': copy.deepcopy(assignment['input_uses']),
            'inputs': bindings, 'criteria': criterion,
            'effects': [{'operation': 'read', 'owner': target_owner, 'targets': targets,
                         'destination_handle': None, 'tool_policy': None},
                        {'operation': 'propose', 'owner': target_owner, 'targets': [],
                         'destination_handle': None, 'tool_policy': None}],
            'limits': [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': limit}],
            'deadline_ms': assignment['deadline_ms']}
    reference = _record('assignment', name, body)
    locators = []
    for binding in bindings:
        for item in binding['refs']:
            if item not in locators:
                locators.append(item)
    _intent('assignment', {'assignment': reference, 'owner': target_owner, 'responsibility': responsibility,
                           'inputs': locators, 'criteria': criterion})
    return reference, body


def _criterion(name, refined=False):
    requirement = next(item['ref'] for item in packet['manifest'] if item['record'].get('source_role') == 'input')
    statement = 'Satisfy the exact inherited service requirement.'
    if refined:
        statement += ' Explicitly state the local operating boundary.'
    body = {'owner': assignment['owner'], 'source_role': 'criteria',
            'origin': {'kind': 'assignment', 'ref': assignment_ref},
            'material': [_material(statement)], 'criteria': [{'id': 'C1', 'requirement': requirement,
            'statement': statement, 'evidence_slots': []}], 'inherited': assignment['inherited']}
    return _record('source', name, body)


def _product(name, kind, text, related=None):
    body = {'owner': assignment['owner'], 'product_kind': kind, 'assignment': assignment_ref,
            'profile': assignment['profile'], 'inputs': assignment['inputs'],
            'material': [_material(text)], 'evidence': [], 'related': related or [], 'limitations': []}
    return _record('product', name, body)


def _select(subject, proof, role, subject_kind, basis=False):
    obligation = next(item for item in profile['obligations'] if item['owner'] == assignment['owner']
                      and item['role'] == role and item['subject_kind'] == subject_kind)
    slot = {'kind': 'basis' if basis else 'proof', 'slot_id': obligation['slot_id']}
    if basis:
        slot['owner'] = assignment['owner']
    else:
        slot.update({'subject': subject, 'role': role})
    _intent('decision', {'action': 'select', 'reason': 'Select the actual independently returned current result.',
                        'slot': slot, 'candidate': subject if basis else proof, 'previous': None})


packet = json.loads(sys.stdin.readline())
assignment_ref = packet['assignment']
assignment = next(item['record'] for item in packet['manifest'] if item['ref'] == assignment_ref)
profile = next(item['record'] for item in packet['manifest'] if item['ref'] == assignment['profile'])
sequence, records, intents = 0, [], []
role, question = assignment['responsibility'], assignment['owner']['question']
returns = packet.get('owned_returns', [])
published = [(entry, item) for entry in returns for item in entry['records']]
products = [(entry, item) for entry, item in published if 'product_kind' in item['record']]
assessments = [(entry, item) for entry, item in published if 'assessment_kind' in item['record']]
contract_ref = next(item['ref'] for item in packet['manifest'] if item['record'].get('source_role') == 'input')
contract = _document(contract_ref)

if role == 'author':
    generation = '2' if packet.get('historical_feedback') else '1'
    content = {'question': question, 'zone': 'west' if question == 'where' else 'east'}
    if question not in {'what', 'why'} or packet.get('historical_feedback'):
        content['boundary'] = contract['required_boundary']
    candidate = _product(question + ':answer:' + generation, 'answer',
                         json.dumps(content))
    _intent('submission', {'assignment': assignment_ref, 'candidate': candidate, 'evidence': [], 'limitations': []})
elif role in {'reviewer', 'integration_reviewer', 'receiver'}:
    basis = packet['assessment_basis']
    subject = basis['subject']
    if packet.get('historical_feedback'):
        assert packet.get('historical_feedback')
        assert any(base64.b64decode(material['data']) for item in packet['historical_feedback']
                   for finding in item['findings'] for material in finding['material'])
    content = _document(subject)
    negative = content.get('boundary') != contract['required_boundary']
    if role == 'reviewer':
        negative |= content.get('question') != question or content.get('zone') not in contract['valid_zones']
    elif role == 'integration_reviewer':
        answer_refs = next(binding['refs'] for binding in assignment['inputs'] if binding['slot_id'] == 'question-answers')
        answers = {document['question']: document for document in map(_document, answer_refs)}
        assert set(answers) == set(contract['questions'])
        source, target = answers['what']['zone'], answers['where']['zone']
        negative |= not (source == target and content.get('mode') == 'colocated' or
                         content.get('mode') == 'explicit_link' and content.get('link') == {'from': source, 'to': target})
    findings = []
    if negative:
        findings.append(_product(subject['logical_id'] + ':finding', 'finding',
            'The fictional candidate needs a precise local boundary; preserve this finding during revision.',
            [{'slot_id': 'subject', 'refs': [subject]}, {'slot_id': 'criterion:C1', 'refs': [assignment['criteria']]}]))
    kind = {'reviewer': 'professional', 'integration_reviewer': 'integration', 'receiver': 'receiving'}[role]
    verdict = 'rework_required' if negative else 'accepted' if role == 'receiver' else 'supported'
    body = {'owner': assignment['owner'], 'assessment_kind': kind, 'assignment': assignment_ref,
            'subject': subject, 'criteria': assignment['criteria'], 'profile': assignment['profile'],
            'assessed_closure': basis['closure'], 'assessed_hash': basis['hash'],
            'verdict': verdict, 'findings': findings, 'conditions': []}
    result = _record('assessment', subject['logical_id'] + ':assessment', body)
    if role == 'receiver':
        _intent('handoff_acceptance', {'assessment': result, 'handoff': subject,
            'interface': assignment['criteria'], 'verdict': verdict, 'findings': findings})
    else:
        _intent('review', {'assignment': assignment_ref, 'assessment': result, 'subject': subject,
            'criteria': assignment['criteria'], 'verdict': verdict, 'findings': findings, 'conditions': []})
elif role == 'integrator':
    answers = next((binding['refs'] for binding in assignment['inputs'] if binding['slot_id'] == 'question-answers'), [])
    if assignment['assigned_actor'] == 'integration-publisher':
        bundle = next(binding['refs'][0] for binding in assignment['inputs'] if binding['slot_id'] == 'bundle')
        review = next(binding['refs'][0] for binding in assignment['inputs'] if binding['slot_id'] == 'integration-review')
        _intent('integration', {'assignment': assignment_ref, 'bundle': bundle, 'answers': answers, 'integration_review': review})
    elif assignment['assigned_actor'] == 'handoff-author':
        bundle = next(binding['refs'][0] for binding in assignment['inputs'] if binding['slot_id'] == 'bundle')
        handoff = _product('local-layer-handoff', 'handoff', json.dumps({'boundary': contract['required_boundary']}),
            [{'slot_id': 'bundle', 'refs': [bundle]}, {'slot_id': 'interface', 'refs': [assignment['criteria']]}])
        _intent('handoff', {'assignment': assignment_ref, 'handoff': handoff, 'bundle': bundle,
            'interface': assignment['criteria'], 'obligations': assignment['inherited']})
    else:
        generation = '2' if packet.get('historical_feedback') else '1'
        documents = {document['question']: document for document in map(_document, answers)}
        content = {'boundary': contract['required_boundary'], 'mode': 'colocated'}
        if packet.get('historical_feedback'):
            content.update({'mode': 'explicit_link', 'link': {'from': documents['what']['zone'], 'to': documents['where']['zone']}})
        bundle = _product('local-bundle:' + generation, 'bundle', json.dumps(content),
                           [{'slot_id': 'answers', 'refs': answers}])
        _intent('submission', {'assignment': assignment_ref, 'candidate': bundle, 'evidence': [], 'limitations': []})
elif role == 'setter':
    if question is not None:
        reviews = [(entry, item) for entry, item in assessments if item['record']['assessment_kind'] == 'professional']
        answers = [(entry, item) for entry, item in products if item['record']['product_kind'] == 'answer']
        latest = reviews[-1] if reviews else None
        if latest and latest[1]['record']['verdict'] == 'rework_required' and not any(item['ref']['logical_id'].endswith(':2') for _, item in answers):
            old = next(entry for entry, item in answers if item['ref'] == latest[1]['record']['subject'])
            if question == 'why':
                criterion = _criterion(question + ':criteria:2', refined=True)
                inputs = copy.deepcopy(assignment['inputs']) + [{'slot_id': 'local-criteria', 'refs': [criterion]}]
                replacement, _ = _child(question + ':author:2', 'author', inputs=inputs, criteria=criterion,
                                         actor=old['mandate']['assigned_actor'])
                previous, target, action = old['mandate']['criteria'], criterion, 'reformulate'
            else:
                inputs = copy.deepcopy(old['mandate']['inputs']) + [{'slot_id': 'revision-focus', 'refs': [assignment['criteria']]}]
                replacement, _ = _child(question + ':author:2', 'author', inputs=inputs,
                    criteria=old['mandate']['criteria'], actor=old['mandate']['assigned_actor'])
                previous, target, action = old['assignment'], replacement, 'rework'
            revision = {'action': action, 'reason': 'Resolve the actual independent finding within local ownership.',
                        'replacement': target, 'findings': latest[1]['record']['findings']}
            revision['assignment' if action == 'rework' else 'subject'] = previous
            if action == 'reformulate':
                revision['authority_proof'] = None
            _intent('decision', revision)
        elif latest and latest[1]['record']['verdict'] == 'supported':
            subject = latest[1]['record']['subject']
            _select(subject, latest[1]['ref'], 'professional_review', 'answer')
            _select(subject, latest[1]['ref'], 'answer', 'answer', basis=True)
        elif answers:
            entry, answer = answers[-1]
            _child(question + ':reviewer:' + answer['ref']['logical_id'][-1], 'reviewer',
                inputs=copy.deepcopy(entry['mandate']['inputs']) + [{'slot_id': 'assessed-subject', 'refs': [answer['ref']]}],
                criteria=entry['mandate']['criteria'], actor=question + ':stable-reviewer')
            if question == 'what' and answer['ref']['logical_id'].endswith(':2'):
                aliases = copy.deepcopy(entry['mandate']['inputs']) + [
                    {'slot_id': 'assessed-subject', 'refs': [answer['ref']]},
                    {'slot_id': 'input-alias', 'refs': [contract_ref]},
                    {'slot_id': 'input-copy', 'refs': [contract_ref]}]
                _child('what:unapproved-reviewer', 'reviewer', inputs=aliases,
                       criteria=entry['mandate']['criteria'], actor='what:unapproved-reviewer')
        else:
            criterion = _criterion(question + ':criteria:1')
            _child(question + ':author:1', 'author',
                inputs=copy.deepcopy(assignment['inputs']) + [{'slot_id': 'local-criteria', 'refs': [criterion]}],
                criteria=criterion, actor=question + ':author')
    else:
        answers = [item['ref'] for _, item in products if item['record']['product_kind'] == 'answer']
        bundles = [(entry, item) for entry, item in products if item['record']['product_kind'] == 'bundle']
        reviews = [(entry, item) for entry, item in assessments if item['record']['assessment_kind'] == 'integration']
        handoffs = [(entry, item) for entry, item in products if item['record']['product_kind'] == 'handoff']
        receiving = [item for _, item in assessments if item['record']['assessment_kind'] == 'receiving']
        integration_done = any(intent['message_type'] == 'integration' for entry in returns for intent in entry['intents'])
        base = copy.deepcopy(assignment['inputs'])
        if receiving:
            _select(receiving[-1]['record']['subject'], receiving[-1]['ref'], 'receiving_acceptance', 'handoff')
        elif integration_done:
            _child('handoff-author', 'integrator', inputs=base + [{'slot_id': 'bundle', 'refs': [bundles[-1][1]['ref']]}], actor='handoff-author')
        elif reviews and reviews[-1][1]['record']['verdict'] == 'supported':
            bundle = reviews[-1][1]['record']['subject']
            review = reviews[-1][1]['ref']
            selected = any(fact['slot']['kind'] == 'proof'
                           and fact['slot'].get('subject') == bundle
                           and fact['slot'].get('role') == 'integration_review'
                           and fact['selected_ref'] == review and fact['applicable']
                           for fact in packet.get('current_slots', []))
            if selected:
                _child('integration-publisher', 'integrator', inputs=base + [{'slot_id': 'bundle', 'refs': [bundle]},
                    {'slot_id': 'integration-review', 'refs': [review]}, {'slot_id': 'question-answers', 'refs': answers}], actor='integration-publisher')
            else:
                # Returned records are admitted before intents, so dependent
                # work must wait for the proof-selection transaction to commit.
                _select(bundle, review, 'integration_review', 'bundle')
        elif reviews and reviews[-1][1]['record']['verdict'] == 'rework_required' and not any(
                item['ref']['logical_id'].endswith(':2') for _, item in bundles):
            old = bundles[-1][0]
            replacement, _ = _child('bundle-author:2', 'integrator',
                inputs=copy.deepcopy(old['mandate']['inputs']) + [{'slot_id': 'revision-focus', 'refs': [assignment['criteria']]}], actor=old['mandate']['assigned_actor'])
            _intent('decision', {'action': 'rework', 'reason': 'Repair the independently identified integration contradiction.',
                'assignment': old['assignment'], 'replacement': replacement, 'findings': reviews[-1][1]['record']['findings']})
        elif bundles:
            replacing = bundles[-1][1]['ref']['logical_id'].endswith(':2')
            reviewer, _ = _child('integration-reviewer:' + bundles[-1][1]['ref']['logical_id'][-1], 'integration_reviewer',
                inputs=base + [{'slot_id': 'assessed-subject', 'refs': [bundles[-1][1]['ref']]},
                               {'slot_id': 'question-answers', 'refs': answers}],
                actor='integration:replacement-reviewer' if replacing else 'integration:stable-reviewer')
            if replacing:
                _intent('decision', {'action': 'rework',
                    'reason': 'Explicitly replace the integration reviewer while preserving its independent findings.',
                    'assignment': reviews[-1][0]['assignment'], 'replacement': reviewer,
                    'findings': reviews[-1][1]['record']['findings']})
        elif len(answers) == 6:
            _child('bundle-author:1', 'integrator', inputs=base + [{'slot_id': 'question-answers', 'refs': answers}], actor='bundle-author')
        else:
            for question_name in ('what', 'why', 'how', 'who', 'where', 'when'):
                owner = {**assignment['owner'], 'work_kind': 'question', 'question': question_name}
                _child(question_name + ':setter', 'setter', owner=owner, actor=question_name + ':local-setter')
else:
    raise RuntimeError('Unsupported fixture responsibility')

print(json.dumps({'id': 'return', 'operation': 'return', 'value': {
    'assignment': assignment_ref, 'context': packet['context'], 'records': records, 'intents': intents}}), flush=True)
