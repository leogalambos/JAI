# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Actual local entities for a transport-only, independently reviewed layer chain."""
import base64
import copy
import hashlib
import json
from pathlib import Path
import sys


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


sequence = 0


def broker(operation, **fields):
    global sequence
    sequence += 1
    print(json.dumps({'id': 'transport-' + str(sequence), 'operation': operation, **fields}), flush=True)
    return json.loads(sys.stdin.readline())


def proposed(raw):
    response = broker('propose', data=base64.b64encode(raw).decode())
    assert response['ok'], response
    return response['result']['blob_id']


packet = json.loads(sys.stdin.readline())
assignment = next(item['record'] for item in packet['manifest'] if item['ref'] == packet['assignment'])
context = next(item['record'] for item in packet['manifest'] if item['ref'] == packet['context'])
owner = assignment['owner']
controller = {'kind': 'controller', 'id': 'trusted-controller'}
records = []
intents = []


def stage(logical_id, family, body):
    manifest = {'schema': 'jai.lifecycle.manifest/2', 'logical_id': logical_id,
                'kind': 'delivery.' + family,
                'content': {'engagement': packet['assignment']['engagement'],
                            'scope': packet['context']['scope'], 'record': body},
                'bindings': {}, 'members': []}
    reference = {'engagement': packet['assignment']['engagement'], 'scope': packet['context']['scope'],
                 'logical_id': logical_id,
                 'version_id': hashlib.sha256(b'jai.lifecycle.version.v2\0' + canonical(manifest)).hexdigest()}
    records.append({'logical_id': logical_id, 'record_type': family, 'record': body})
    return reference


def intent(kind, payload):
    intents.append({'message_type': kind, 'recipient': controller, 'payload': payload})


def issue(responsibility, subject=None):
    child = copy.deepcopy(assignment)
    child['responsibility'] = responsibility
    child['assigned_actor'] = assignment['assigned_actor'] + ':' + responsibility
    child['issued_under'] = packet['assignment']
    child['limits'] = [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 60000}]
    if subject is not None:
        child['inputs'].append({'slot_id': 'assessed-subject', 'refs': [subject]})
    if responsibility == 'integration_reviewer':
        child['effects'] = [effect for effect in child['effects'] if effect['operation'] in {'read', 'propose'}]
    targets = []
    for binding in child['inputs']:
        for reference in binding['refs']:
            if reference not in targets:
                targets.append(reference)
    locators = copy.deepcopy(targets)
    if child['criteria'] not in targets:
        targets.append(child['criteria'])
    for effect in child['effects']:
        if effect['operation'] == 'read':
            effect['targets'] = copy.deepcopy(targets)
    reference = stage('transport-' + responsibility + '-L' + str(owner['layer']), 'assignment', child)
    intent('assignment', {'assignment': reference, 'owner': owner,
                         'responsibility': responsibility, 'inputs': locators,
                         'criteria': child['criteria']})


def select(subject, assessment, role):
    profile = next(item['record'] for item in packet['manifest'] if item['ref'] == assignment['profile'])
    obligation = next(item for item in profile['obligations'] if item['owner'] == owner and item['role'] == role)
    intent('decision', {'action': 'select', 'reason': 'Select this actual independent transport assessment.',
        'slot': {'kind': 'proof', 'subject': subject, 'role': role, 'slot_id': obligation['slot_id']},
        'candidate': assessment, 'previous': None})


catalogue = json.loads(Path('/catalogue/catalogue.json').read_text())
assert catalogue['count'] > 100
assert Path('/catalogue/instructions/internal-it-auditor.md').read_text()
for attachment in packet['attachments']:
    assert broker('read', handle=attachment['handle'])['ok']

if assignment['responsibility'] == 'integrator':
    value = canonical({'layer': owner['layer'], 'work_item': owner['work_item'],
                       'scope': packet['context']['scope'], 'transport': 'worker-created exact bytes'})
    payload = proposed(value)
    subject = next(binding['refs'][0] for binding in assignment['inputs']
                   if binding['slot_id'].startswith('l0:') and binding['refs'][0] != assignment['routing']['policy'])
    own = broker('materialize', subject=subject, blob_id=payload, destination_handle='owned-output')
    same = broker('materialize', subject=subject, blob_id=payload, destination_handle='foreign-output')
    other = broker('materialize', subject=subject, blob_id=payload, destination_handle='foreign-layer-output')
    assert own['ok'] and not same['ok'] and not other['ok'], (own, same, other)
    report = proposed(canonical({'layer': owner['layer'], 'material': payload, 'owned': own,
                                 'foreign_same_layer': same, 'foreign_layer': other,
                                 'catalogue_count': catalogue['count'],
                                 'unselected_instruction_readable': True}))
    body = {'owner': owner, 'product_kind': 'bundle', 'assignment': packet['assignment'],
            'profile': assignment['profile'], 'inputs': assignment['inputs'],
            'material': [payload, report], 'evidence': [], 'related': [],
            'limitations': ['Transport boundary evidence only; no six-question architecture completion.']}
    reference = stage('transport-bundle-L' + str(owner['layer']), 'product', body)
    intent('submission', {'assignment': packet['assignment'], 'candidate': reference,
                          'evidence': [], 'limitations': body['limitations']})
elif assignment['responsibility'] in {'integration_reviewer', 'receiver'}:
    basis = packet['assessment_basis']
    subject = next(item['record'] for item in packet['manifest'] if item['ref'] == basis['subject'])
    receiving = assignment['responsibility'] == 'receiver'
    assert subject['product_kind'] == ('handoff' if receiving else 'bundle') and subject['material']
    if not receiving:
        materials = {attachment['blob_id']: attachment['handle'] for attachment in packet['attachments']}
        report = broker('read', handle=materials[subject['material'][1]])
        facts = json.loads(base64.b64decode(report['result']['data']))
        assert facts['owned']['ok'] and not facts['foreign_same_layer']['ok'] and not facts['foreign_layer']['ok']
    body = {'owner': owner, 'assessment_kind': 'receiving' if receiving else 'integration',
            'assignment': packet['assignment'], 'subject': basis['subject'], 'criteria': assignment['criteria'],
            'profile': assignment['profile'], 'assessed_closure': basis['closure'], 'assessed_hash': basis['hash'],
            'verdict': 'accepted' if receiving else 'supported', 'findings': [], 'conditions': []}
    reference = stage('transport-review-L' + str(owner['layer']) + ('-receiving' if receiving else '-integration'), 'assessment', body)
    if receiving:
        intent('handoff_acceptance', {'assessment': reference, 'handoff': basis['subject'],
                                     'interface': assignment['criteria'], 'verdict': body['verdict'], 'findings': []})
    else:
        intent('review', {'assignment': packet['assignment'], 'assessment': reference, 'subject': basis['subject'],
                         'criteria': assignment['criteria'], 'verdict': body['verdict'], 'findings': [], 'conditions': []})
elif assignment['responsibility'] == 'setter':
    outcomes = [record for returned in packet['owned_returns'] for record in returned['records']]
    receiving = next((item for item in reversed(outcomes) if 'assessment_kind' in item['record']
                      and item['record']['assessment_kind'] == 'receiving'), None)
    bundle = next((item for item in outcomes if item['record'].get('product_kind') == 'bundle'), None)
    review = next((item for item in outcomes if item['record'].get('assessment_kind') == 'integration'), None)
    if receiving is not None:
        select(receiving['record']['subject'], receiving['ref'], 'receiving_acceptance')
    elif bundle is None:
        issue('integrator')
    elif review is None:
        issue('integration_reviewer', bundle['ref'])
    else:
        assert review['record']['subject'] == bundle['ref'] and review['record']['verdict'] == 'supported'
        select(bundle['ref'], review['ref'], 'integration_review')
        payload = proposed(canonical({'layer': owner['layer'], 'bundle': bundle['ref'],
                                     'interface': assignment['criteria'], 'scope': 'transport only'}))
        body = {'owner': owner, 'product_kind': 'handoff', 'assignment': packet['assignment'],
                'profile': assignment['profile'], 'inputs': assignment['inputs'], 'material': [payload],
                'evidence': [], 'related': [{'slot_id': 'bundle', 'refs': [bundle['ref']]},
                                          {'slot_id': 'interface', 'refs': [assignment['criteria']]}],
                'limitations': ['An interface offer, not a completed SABSA layer.']}
        reference = stage('transport-handoff-L' + str(owner['layer']), 'product', body)
        intent('handoff', {'assignment': packet['assignment'], 'handoff': reference, 'bundle': bundle['ref'],
                           'interface': assignment['criteria'], 'obligations': assignment['inherited']})
else:
    raise AssertionError('Unsupported transport responsibility')

print(json.dumps({'id': 'return-transport', 'operation': 'return', 'value': {
    'assignment': packet['assignment'], 'context': packet['context'], 'records': records, 'intents': intents}}), flush=True)
