# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Compile reviewed compatibility profiles into exact workflow requirements."""

from copy import deepcopy
import re

from content_spec import canonical_hash
from workflow_role_selection import PROTOCOL, _binding, _fields

PROFILE_PROTOCOL = 'jai.workflow-specialist-profiles/1'
CONTROL_FIELDS = ('operator_agent', 'tool_tier', 'allowed_tools')
MODES = {'preferred-specialist', 'required-specialist'}


def _digest(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9a-f]{64}', value):
        raise ValueError('WORKFLOW_PROFILE_DIGEST')
    return value


def _text(value):
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError('WORKFLOW_PROFILE_IDENTITY')
    return value


def _keyed(entries, fields, key):
    if not isinstance(entries, list):
        raise ValueError('WORKFLOW_PROFILE_SCHEMA')
    result = {}
    for entry in entries:
        _fields(entry, fields)
        identity = key(entry)
        if identity in result:
            raise ValueError('WORKFLOW_PROFILE_DUPLICATE')
        result[identity] = entry
    return result


def role_revision(role, instruction_blob):
    """Pin the exact role registry row and its immutable instruction identity."""
    return canonical_hash({'role': role, 'instruction_blob': _digest(instruction_blob)})


def effective_obligations(row, binding):
    """Pin effective requirements, ignoring only the local namespacing of unit IDs."""
    content = deepcopy(binding['handoff_content_contract'])
    prefix = 'handoff/' + row['handoff_id']
    if content['id'] == prefix:
        content['id'] = 'local-handoff'
    units = {}
    for unit in content['units']:
        identity = unit['id']
        local = identity.removeprefix(prefix + '.')
        if local in units.values():
            raise ValueError('WORKFLOW_PROFILE_UNIT_COLLISION')
        units[identity] = local
        unit['id'] = local
    return {'content': content, 'receiver': binding['receiving_role'],
            'receiver_checks': row['receiver_checks'],
            'acceptance_criterion': binding['acceptance_criterion'],
            'handover': row['handover'], 'contract_selection': row['contract_selection'],
            'required_contracts': binding['contract_ids']}, units


def profile_for(row, binding, base, contract):
    """Return the exact comparable profile obligations for an effective author endpoint."""
    obligations, _ = effective_obligations(row, binding)
    if (binding['contract_ids'] != [contract['id']]
            or row['contract_selection'] != 'registered-contracts'
            or not contract['id'].startswith(binding['producer_role'] + ':')):
        raise ValueError('WORKFLOW_PROFILE_CONTRACT')
    return {'base': binding['producer_role'], 'responsibility': 'author', 'endpoint': 'producer',
            'contract': {'id': contract['id'], 'version': contract['version'], 'digest': canonical_hash(contract)},
            'controls': {field: base[field] for field in CONTROL_FIELDS}, 'obligations': obligations}


def compile_profiles(catalogue, document, roles, instruction_blobs, contracts):
    """Resolve closed reviewed source into exact per-endpoint requirements and pins.

    The workflow catalogue and authoritative contracts come from the existing
    checked inputs. A profile match does not approve a deployment or reviewer.
    """
    _fields(document, 'protocol profiles mappings endpoints receipts')
    if document['protocol'] != PROFILE_PROTOCOL:
        raise ValueError('WORKFLOW_PROFILE_PROTOCOL')
    profiles = _keyed(document['profiles'], 'id version definition',
                      lambda entry: (_text(entry['id']), _text(entry['version'])))
    mappings = _keyed(document['mappings'],
        'profile version profile_digest slug role_revision author review_receipt product deployments covered_units',
        lambda entry: (_text(entry['profile']), _text(entry['version']), _text(entry['slug'])))
    receipts = _keyed(document['receipts'], 'reviewer decision mapping_digest', canonical_hash)
    endpoints = _keyed(document['endpoints'], 'handoff path endpoint profile version mode',
                      lambda entry: tuple(_text(entry[key]) for key in ('handoff', 'path', 'endpoint')))
    by_profile = {identity: [] for identity in profiles}
    for (name, version, slug), mapping in sorted(mappings.items()):
        identity = (name, version)
        if (identity not in profiles or slug not in roles
                or mapping['profile_digest'] != canonical_hash(profiles[identity])
                or mapping['role_revision'] != role_revision(roles[slug], instruction_blobs[slug])):
            raise ValueError('WORKFLOW_PROFILE_UNREVIEWED_REVISION')
        receipt = receipts.get(_digest(mapping['review_receipt']))
        reviewed = {key: value for key, value in mapping.items() if key != 'review_receipt'}
        if (receipt is None or receipt['decision'] != 'approved'
                or _text(receipt['reviewer']) == _text(mapping['author'])
                or receipt['mapping_digest'] != canonical_hash(reviewed)):
            raise ValueError('WORKFLOW_PROFILE_REVIEW_RECEIPT')
        by_profile[identity].append(mapping)
    requirements, pins = [], []
    for key, endpoint in sorted(endpoints.items()):
        identity = (_text(endpoint['profile']), _text(endpoint['version']))
        if key[2] != 'producer' or endpoint['mode'] not in MODES or identity not in profiles:
            raise ValueError('WORKFLOW_PROFILE_ENDPOINT')
        row, binding = _binding(catalogue, *key)
        profile = profiles[identity]
        definition = profile['definition']
        if not isinstance(definition, dict) or set(definition) != {
                'base', 'responsibility', 'endpoint', 'contract', 'controls', 'obligations'}:
            raise ValueError('WORKFLOW_PROFILE_SCHEMA')
        _fields(definition['contract'], 'id version digest')
        contract_id = _text(definition['contract']['id'])
        base = binding['producer_role']
        if base not in roles or contract_id not in contracts:
            raise ValueError('WORKFLOW_PROFILE_CONTRACT')
        if profile_for(row, binding, roles[base], contracts[contract_id]) != definition:
            raise ValueError('WORKFLOW_PROFILE_OBLIGATIONS')
        _, units = effective_obligations(row, binding)
        ids = list(units.values())
        exact_mappings, mapping_pins = [], {}
        for mapping in by_profile[identity]:
            if not isinstance(mapping['covered_units'], list) or sorted(mapping['covered_units']) != sorted(ids):
                raise ValueError('WORKFLOW_PROFILE_OBLIGATIONS')
            slug = mapping['slug']
            exact_mappings.append({'slug': slug, 'product': mapping['product'], 'deployments': mapping['deployments'],
                'covered_units': list(units), 'handoff_contract_hash': canonical_hash(binding['handoff_content_contract'])})
            mapping_pins[slug] = {field: mapping[field] for field in ('role_revision', 'review_receipt')}
        requirement = {'handoff': key[0], 'path': key[1], 'endpoint': key[2], 'base': base,
                       'responsibility': 'author',
                       'contract': {field: definition['contract'][field] for field in ('id', 'version')},
                       'mappings': exact_mappings}
        requirements.append(requirement)
        pins.append({'handoff': key[0], 'path': key[1], 'endpoint': key[2], 'mode': endpoint['mode'],
                     'profile': profile['id'], 'version': profile['version'],
                     'profile_digest': canonical_hash(profile), 'mappings': mapping_pins})
    return {'protocol': PROTOCOL, 'workflow_catalogue': catalogue['catalog_hash'],
            'requirements': requirements}, pins


def _stage_policy(catalogue, document, roles, instructions, contracts, ancestry):
    from governed_routing import PROCEDURE_SCOPE_PROTOCOL
    from workflow_role_selection import compile_requirements

    reviewed, pins = compile_profiles(catalogue, document, roles, instructions, contracts)
    target = deepcopy(catalogue)
    for requirement, pin in zip(reviewed['requirements'], pins, strict=True):
        _, binding = _binding(target, pin['handoff'], pin['path'], pin['endpoint'])
        if 'workflow_role_requirement' in binding:
            raise ValueError('WORKFLOW_PROFILE_EXISTING_BINDING')
        binding['workflow_role_requirement'] = {'mode': 'compatible-specialization',
            'contract': requirement['contract'], 'requirement_hash': canonical_hash(requirement),
            'profile': pin}
    target.pop('catalog_hash')
    target['catalog_hash'] = canonical_hash(target)
    reviewed['workflow_catalogue'] = target['catalog_hash']
    versions = {requirement['contract']['id']: requirement['contract']['version']
                for requirement in reviewed['requirements']}
    used_ancestry = {mapping['slug']: ancestry[mapping['slug']] for mapping in document['mappings']}
    compiled = compile_requirements(target, reviewed, roles, used_ancestry, versions)
    policy = {'catalogue': target, 'reviewed': reviewed, 'ancestry': used_ancestry, 'contract_versions': versions,
            'procedure_scope_protocol': PROCEDURE_SCOPE_PROTOCOL,
            'specialist_profiles': {'source': document, 'contracts': {key: contracts[key] for key in versions}}}


    return policy, compiled


def stage_policy(catalogue, document, roles, instructions, contracts, ancestry):
    """Generate a complete candidate policy without changing its source catalogue."""
    return _stage_policy(catalogue, document, roles, instructions, contracts, ancestry)[0]


def verify_policy(policy, roles, instructions, *, catalogue=None, contracts=None):
    """Rebuild an overlay against its captured or current authoritative inputs."""
    source = policy['specialist_profiles']
    _fields(source, 'source contracts')
    if catalogue is None:
        catalogue = deepcopy(policy['catalogue'])
        for endpoint in source['source']['endpoints']:
            _, binding = _binding(catalogue, endpoint['handoff'], endpoint['path'], endpoint['endpoint'])
            del binding['workflow_role_requirement']
        catalogue.pop('catalog_hash')
        catalogue['catalog_hash'] = canonical_hash(catalogue)
    expected, compiled = _stage_policy(catalogue, source['source'], roles, instructions,
                                       source['contracts'] if contracts is None else contracts, policy['ancestry'])
    if policy != expected:
        raise ValueError('WORKFLOW_PROFILE_POLICY_DRIFT')
    return compiled
