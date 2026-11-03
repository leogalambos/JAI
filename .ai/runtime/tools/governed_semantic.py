#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Encode actual professional semantics using an issued immutable work packet.

The codec stages materials but grants no authority. Exact issued metadata comes
from the shared proposal builder; professional meaning comes only from the
explicit role result. Domain JSON is never passed through core canonicalization.
"""
from __future__ import annotations

import copy
import json

import governed_delivery as wire
import governed_native_provider as provider
import governed_records
import lifecycle as lc

FORMAT = 'jai.semantic-return/1'
CODEC = 'jai.semantic-encoder/2'


def _exact(packet, reference):
    matches = [item['record'] for item in packet['manifest'] if item['ref'] == reference]
    if len(matches) != 1:
        raise ValueError('Issued packet must contain each structural record exactly once')
    return matches[0]


def _aliases(packet, assignment):
    values = {'assignment': packet['assignment'], 'context': packet['context'],
              'profile': assignment['profile'], 'criteria': assignment['criteria']}
    if packet.get('assessment_basis'):
        values['subject'] = packet['assessment_basis']['subject']
    for item in packet['manifest']:
        handle = item.get('handle')
        if not isinstance(handle, str):
            continue
        if handle in values and values[handle] != item['ref']:
            raise ValueError('Ambiguous issued reference alias')
        values[handle] = item['ref']
    return values


def _reference(value, aliases, validator):
    if isinstance(value, dict) and set(value) == {'alias'}:
        if value['alias'] not in aliases:
            raise ValueError('Unknown or forward semantic reference alias')
        return copy.deepcopy(aliases[value['alias']])
    if not validator.is_valid(value):
        raise ValueError('An exact reference or declared reference alias is required')
    return copy.deepcopy(value)


def _materials(values, writer):
    result = []
    for value in values:
        if 'blob' in value:
            result.append(value['blob'])
            continue
        raw = (value['text'].encode('utf-8') if 'text' in value else json.dumps(
            value['json'], ensure_ascii=False, sort_keys=True, separators=(',', ':'),
            allow_nan=False).encode('utf-8'))
        expected = lc.blob(raw)
        if writer(raw) != expected:
            raise ValueError('Staged material identity differs from its exact bytes')
        result.append(expected)
    return result


def _proposal(packet, family, logical_id, fields):
    proposal = governed_records.build_proposal(packet, family, logical_id, fields)
    reference = lc._ref(lc.record_manifest(packet['assignment']['engagement'],
        packet['assignment']['scope'], logical_id, family, proposal['record']))
    return proposal, reference


def _declared_references(value, schema, reference, documents, document='decision.schema.json'):
    target = schema.get('$ref')
    if target:
        if target == 'common.schema.json#/$defs/reference':
            return reference(value)
        name, _, fragment = target.partition('#')
        document = name or document
        if document not in documents:
            documents[document] = json.loads((wire.PACKAGE / document).read_bytes())
        selected = documents[document]
        for segment in fragment.lstrip('/').split('/') if fragment else []:
            selected = selected[segment.replace('~1', '/').replace('~0', '~')]
        return _declared_references(value, selected, reference, documents, document)
    alternatives = schema.get('anyOf', schema.get('oneOf', []))
    if alternatives:
        if value is None and any(item.get('type') == 'null' for item in alternatives):
            return None
        for item in alternatives:
            if item.get('$ref') == 'common.schema.json#/$defs/reference':
                return reference(value)
        if isinstance(value, dict):
            candidates = [item for item in alternatives if 'properties' in item
                and set(item.get('required', ())).issubset(value)
                and all('const' not in field or value.get(key) == field['const']
                        for key, field in item['properties'].items())]
            if len(candidates) == 1:
                return _declared_references(value, candidates[0], reference, documents, document)
    if isinstance(value, dict):
        properties = schema.get('properties', {})
        return {key: _declared_references(child, properties.get(key, {}), reference, documents, document)
                for key, child in value.items()}
    if isinstance(value, list):
        return [_declared_references(child, schema.get('items', {}), reference, documents, document)
                for child in value]
    return copy.deepcopy(value)


def compile_semantic(packet, value, material_writer):
    """Compile one exact member's actual semantic result into an existing RunReturn.

    Args:
        packet: Issued immutable packet including its opaque member_key. Assignment,
            recipient, profile, dependency bindings and assessment closure are exact.
        value: Parsed jai.semantic-return/1 envelope, with one result per member.
            The host separately enforces the complete issued batch member set.
        material_writer: Callable accepting exact bytes and returning their existing
            lifecycle CAS identity. Staging is not semantic admission or acceptance.
    Returns:
        Deterministic schema-valid singleton RunReturn for this member. Inputs are
        unchanged. Professional IDs, materials, criteria and verdicts remain explicit.
    Raises:
        ValueError, ProtocolError: Missing semantics, duplicate or unknown member,
            responsibility mismatch, unknown reference alias, nonfinite material,
            conflicting metadata or a material writer returning a forged identity.
        OSError: Material staging failed. The ordinary Store alone admits effects.
    """
    if not wire.validator('semantic-return.schema.json', 'attribution').is_valid(value):
        raise ValueError('Attributable semantic member envelope required')
    keys = [item['member'] for item in value['results']]
    if len(keys) != len(set(keys)):
        raise ValueError('Duplicate semantic member result')
    matches = [item for item in value['results'] if item['member'] == packet['member_key']]
    if len(matches) != 1:
        raise ValueError('No unique semantic result for the exact issued member')
    result = matches[0]
    kind = result.get('kind')
    if kind not in {'selection', 'setter', 'owner_action', 'author', 'integrator', 'measurement',
                    'reviewer', 'integration_reviewer', 'receiver'} or not wire.validator(
                        'semantic-return.schema.json', kind).is_valid(result):
        raise ValueError('Complete closed role-specific semantic return required')
    assignment = _exact(packet, packet['assignment'])
    recipient = _exact(packet, assignment['profile'])['owner']
    expected = 'selection' if packet['execution']['phase'] == 'selection' else assignment['responsibility']
    if kind != expected and not (kind == 'owner_action' and expected == 'setter'):
        raise ValueError('Semantic result differs from the exact issued responsibility')
    aliases = _aliases(packet, assignment)
    records, intents = [], []
    reference_validator = wire.validator('common.schema.json', 'reference')

    def reference(value):
        return _reference(value, aliases, reference_validator)

    def references(items):
        return [reference(item) for item in items]

    def intent(message_type, payload):
        intents.append({'message_type': message_type, 'recipient': copy.deepcopy(recipient), 'payload': payload})

    def previous(value, expected):
        if 'previous' in value:
            actual = None if value['previous'] is None else reference(value['previous'])
            if actual != expected:
                raise ValueError('Explicit previous selection conflicts with the issued packet')
        return copy.deepcopy(expected)

    if kind == 'selection':
        payload = {name: copy.deepcopy(result[name]) for name in (
            'specialties', 'provider', 'workload_class', 'model_selector', 'reason')}
        payload.update(action='select_execution', assignment=packet['assignment'], authority_proof=None,
                       previous=previous(result, packet['execution'].get('previous')))
        intent('decision', payload)
    elif kind == 'owner_action':
        source_value = result.get('criteria_source')
        if source_value:
            criteria = copy.deepcopy(source_value['criteria'])
            for item in criteria:
                item['requirement'] = reference(item['requirement'])
            source, source_ref = _proposal(packet, 'source', source_value['logical_id'], {
                'source_role': 'criteria', 'material': _materials(source_value['materials'], material_writer),
                'criteria': criteria, 'inherited': references(source_value['inherited'])})
            records.append(source)
            aliases['replacement_criteria'] = source_ref
        decision_schema = json.loads((wire.PACKAGE / 'decision.schema.json').read_bytes())
        action = result['decision']['action']
        clause = next(item for item in decision_schema['oneOf']
                      if item.get('properties', {}).get('action', {}).get('const') == action)
        payload = _declared_references(result['decision'], clause, reference,
                                        {'decision.schema.json': decision_schema})
        if 'authority_proof' in clause['properties']:
            payload['authority_proof'] = None
        wire.validate(payload, 'decision.schema.json')
        intent('decision', payload)
    elif kind == 'setter':
        criteria = copy.deepcopy(result['criteria'])
        for item in criteria:
            item['requirement'] = reference(item['requirement'])
        source, source_ref = _proposal(packet, 'source', result['logical_id'], {
            'source_role': 'criteria', 'material': _materials(result['materials'], material_writer),
            'criteria': criteria, 'inherited': references(result['inherited'])})
        records.append(source)
        procedure = result['procedure']
        intent('decision', {'action': 'configure_procedure', 'assignment': packet['assignment'],
            'criteria': source_ref, 'kind': procedure['kind'],
            'specification': copy.deepcopy(procedure['specification']),
            'previous': previous(procedure, packet.get('current_procedure')),
            'reason': procedure['reason'], 'authority_proof': None})
    elif kind in {'reviewer', 'integration_reviewer', 'receiver'}:
        subject = packet['assessment_basis']['subject']
        findings = []
        for finding in result['findings']:
            if 'logical_id' not in finding or 'materials' not in finding:
                findings.append(reference(finding))
                continue
            related = [{'slot_id': 'subject', 'refs': [copy.deepcopy(subject)]},
                       {'slot_id': 'criterion:' + finding['criterion'],
                        'refs': [copy.deepcopy(assignment['criteria'])]}]
            product, product_ref = _proposal(packet, 'product', finding['logical_id'], {
                'product_kind': 'finding', 'inputs': copy.deepcopy(assignment['inputs']),
                'material': _materials([*finding['materials'], {'text': finding['observation']}], material_writer),
                'evidence': references(finding['evidence']), 'related': related,
                'limitations': copy.deepcopy(finding['limitations'])})
            records.append(product)
            findings.append(product_ref)
        conditions = references(result['conditions'])
        assessment, assessment_ref = _proposal(packet, 'assessment', result['logical_id'], {
            'assessment_kind': {'reviewer': 'professional', 'integration_reviewer': 'integration',
                                'receiver': 'receiving'}[kind],
            'subject': subject, 'criteria': assignment['criteria'], 'verdict': result['verdict'],
            'findings': findings, 'conditions': conditions})
        records.append(assessment)
        if kind == 'receiver':
            intent('handoff_acceptance', {'assessment': assessment_ref, 'handoff': subject,
                'interface': assignment['criteria'], 'verdict': result['verdict'], 'findings': findings})
        else:
            intent('review', {'assignment': packet['assignment'], 'assessment': assessment_ref,
                'subject': subject, 'criteria': assignment['criteria'], 'verdict': result['verdict'],
                'findings': findings, 'conditions': conditions})
    else:
        material = _materials(result['materials'], material_writer)
        evidence = references(result.get('evidence', []))
        related = []
        if kind == 'integrator':
            related = [{'slot_id': item['slot_id'], 'refs': references(item['refs'])}
                       for item in result['related']]
            related.append({'slot_id': 'answers', 'refs': references(result['answers'])})
        product, product_ref = _proposal(packet, 'product', result['logical_id'], {
            'product_kind': {'author': 'answer', 'integrator': 'bundle', 'measurement': 'observation'}[kind],
            'inputs': copy.deepcopy(assignment['inputs']), 'material': material,
            'evidence': evidence, 'related': related, 'limitations': copy.deepcopy(result['limitations'])})
        records.append(product)
        if kind == 'measurement':
            intent('observation', {'assignment': packet['assignment'], 'observation': product_ref,
                                  'inputs': references(result['inputs']), 'material': material})
        else:
            intent('submission', {'assignment': packet['assignment'], 'candidate': product_ref,
                                 'evidence': evidence, 'limitations': copy.deepcopy(result['limitations'])})
    return provider.producer_return(packet, records, intents)
