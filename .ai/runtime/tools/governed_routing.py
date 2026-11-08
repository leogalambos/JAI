#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Validate immutable routing snapshots without ambient catalogues or overrides."""
from __future__ import annotations

import copy
import hashlib

import lifecycle as lc
import model_router
import execution_profiles

PROTOCOL = 'jai.role-routing/1'
_RESPONSIBILITIES = {'setter', 'author', 'reviewer', 'integrator', 'integration_reviewer', 'receiver', 'measurement'}
_QUESTIONS = {'what', 'why', 'how', 'who', 'where', 'when'}
_TIERS = {'advise': {'read', 'propose'}, 'route': {'read', 'propose'},
          'research': {'read', 'propose'}, 'orchestrate': {'read', 'propose'},
          'author': {'read', 'propose', 'materialize'},
          'inspect': {'read', 'propose', 'measure'},
          'execute': {'read', 'propose', 'materialize', 'measure'}}


def _closed(value, fields):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise lc.ERROR('P_SCHEMA', 'Closed captured routing contract required')


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def capture_policy(policy_id, catalogue_bytes, models_bytes, instructions, bootstrap, capabilities, put_blob):
    """Capture explicit host-resolved inputs as existing immutable source material.

    Args:
        policy_id: Profile-enrolled routing policy identifier.
        catalogue_bytes: Exact canonical role catalogue bytes selected by L0.
        models_bytes: Explicit resolved model registry bytes, including local mappings.
        instructions: Selected catalogue slug to exact instruction byte mapping.
        bootstrap: Explicit functional chooser provider, workload and model.
        capabilities: Global broker templates and finite resource ceilings.
        put_blob: Existing Store immutable blob writer; never an authority action.
    Returns:
        Source material identities, descriptor first followed by captured inputs.
    Raises:
        ValueError: Snapshot bytes or descriptor content are malformed.
    """
    descriptor = {'protocol': PROTOCOL, 'policy_id': policy_id,
                  'catalogue_blob_id': put_blob(catalogue_bytes),
                  'instruction_blobs': {slug: put_blob(raw) for slug, raw in sorted(instructions.items())},
                  'models_blob_id': put_blob(models_bytes), 'bootstrap': copy.deepcopy(bootstrap),
                  'capabilities': copy.deepcopy(capabilities)}
    descriptor_id = put_blob(lc.canonical(descriptor))
    material = [descriptor_id, descriptor['catalogue_blob_id'], descriptor['models_blob_id'],
                *descriptor['instruction_blobs'].values()]
    return list(dict.fromkeys(material))


def load_policy(source, blob_reader):
    """Resolve and validate a complete immutable captured routing snapshot.

    Args:
        source: Existing L0-owned policy source record with descriptor-first material.
        blob_reader: Exact immutable-byte reader for the journal's captured inputs.
    Returns:
        Parsed descriptor, catalogue, models and selected instruction byte identities.
    Raises:
        ProtocolError: Missing, corrupt, unavailable or unsupported captured inputs.
    """
    if (source.get('source_role') != 'policy' or source['owner'].get('kind') != 'authority'
            or source['origin'] != source['owner'] or not source.get('material')):
        raise lc.ERROR('P_SCOPE', 'Routing requires an attributable L0 policy source')
    material = source['material']

    def read(identifier):
        if identifier not in material:
            raise lc.ERROR('P_CONTEXT', 'Routing snapshot is not contained in its exact source material')
        try:
            raw = blob_reader(identifier)
            if lc.blob(raw) != identifier:
                raise ValueError('identity')
            return raw
        except (OSError, ValueError) as error:
            raise lc.ERROR('P_CONTEXT', 'Required immutable routing snapshot is unavailable') from error

    descriptor = lc.loads(read(material[0]))
    _closed(descriptor, ('protocol', 'policy_id', 'catalogue_blob_id', 'instruction_blobs', 'models_blob_id', 'bootstrap', 'capabilities'))
    if descriptor['protocol'] != PROTOCOL or not _text(descriptor['policy_id']):
        raise lc.ERROR('P_SCHEMA', 'Unsupported routing policy descriptor')
    catalogue = lc.loads(read(descriptor['catalogue_blob_id']))
    models = lc.loads(read(descriptor['models_blob_id']))
    rows = catalogue.get('roles') if isinstance(catalogue, dict) else None
    if (not isinstance(rows, list) or not rows or catalogue.get('count') != len(rows)
            or any(not isinstance(row, dict) or not _text(row.get('slug'))
                   or row['slug'] in {'.', '..'} or '/' in row['slug'] or '\\' in row['slug'] for row in rows)
            or len({row['slug'] for row in rows}) != len(rows)):
        raise lc.ERROR('P_PROOF', 'Captured role catalogue identities and count must be exact')
    by_slug = {row['slug']: row for row in rows}
    mapping = descriptor['instruction_blobs']
    if not isinstance(mapping, dict) or set(mapping) != set(by_slug):
        raise lc.ERROR('P_PROOF', 'Instructions must identify existing captured catalogue specialties')
    expected = {material[0], descriptor['catalogue_blob_id'], descriptor['models_blob_id'], *mapping.values()}
    if len(material) != len(set(material)) or set(material) != expected:
        raise lc.ERROR('P_PROOF', 'Routing material must contain exactly its structural snapshot assets')
    instructions = {}
    for slug, identifier in mapping.items():
        try:
            text = read(identifier).decode('utf-8')
        except UnicodeError as error:
            raise lc.ERROR('P_SCHEMA', 'Captured specialty instructions must be UTF-8') from error
        if not text.strip():
            raise lc.ERROR('P_PROOF', 'Selected specialty instructions cannot be empty')
        instructions[slug] = {'slug': slug, 'blob_id': identifier, 'text': text}
    problems = model_router.validate_registry(models)
    if problems:
        raise lc.ERROR('P_PROOF', 'Captured model registry is invalid: ' + '; '.join(problems))
    _closed(descriptor['bootstrap'], ('provider', 'workload_class', 'model_selector'))
    _execution(models, descriptor['bootstrap'])
    capabilities = descriptor['capabilities']
    _closed(capabilities, ('effects', 'limits'))
    if not isinstance(capabilities['effects'], list) or not isinstance(capabilities['limits'], list):
        raise lc.ERROR('P_PROOF', 'Global finite capability templates are required')
    for effect in capabilities['effects']:
        _closed(effect, ('operation', 'tool_policy', 'destination_handle'))
        if effect['operation'] not in {'read', 'propose', 'materialize', 'measure'}:
            raise lc.ERROR('P_PROOF', 'Unknown global broker capability')
    units = set()
    for limit in capabilities['limits']:
        _closed(limit, ('metric', 'unit', 'ceiling'))
        if (not _text(limit['metric']) or not _text(limit['unit']) or type(limit['ceiling']) is not int
                or limit['ceiling'] <= 0 or (limit['metric'], limit['unit']) in units):
            raise lc.ERROR('P_PROOF', 'Global resource bounds must be finite and unambiguous')
        units.add((limit['metric'], limit['unit']))
    return {'descriptor': descriptor, 'catalogue': catalogue, 'models': models, 'instructions': instructions}


def _execution(models, choice, responsibility=None):
    try:
        selector, model = model_router.resolve_snapshot(models, choice['provider'], choice['workload_class'])
        preference = models.get('execution_profile')
        if preference and responsibility and preference['provider'] == choice['provider']:
            _, model = execution_profiles.mapping(preference, responsibility, choice['workload_class'], models)
            selector = model['model_selector']
    except (ValueError, KeyError, TypeError) as error:
        raise lc.ERROR('P_PROOF', 'No exact globally available workload/model capability exists') from error
    if selector != choice['model_selector']:
        raise lc.ERROR('P_PROOF', 'Exact captured model choice required')
    if choice['provider'] in {'codex', 'claude'}:
        model = copy.deepcopy(model)
        model['execution'] = {'provider': choice['provider'], 'transport': 'native-subagent'}
        return selector, model
    if choice['provider'] != 'json-process/1':
        raise lc.ERROR('P_PROOF', 'The captured provider has no implemented execution contract')
    execution = model.get('execution')
    _closed(execution, ('provider', 'argv', 'files'))
    if (execution['provider'] != 'json-process/1' or not isinstance(execution['argv'], list)
            or not execution['argv'] or any(not _text(value) for value in execution['argv'])
            or not execution['argv'][0].startswith('/') or not isinstance(execution['files'], list)):
        raise lc.ERROR('P_PROOF', 'Exact enrolled local process execution descriptor required')
    names = set()
    for asset in execution['files']:
        _closed(asset, ('name', 'sha256'))
        if (not _text(asset['name']) or asset['name'] in {'.', '..'} or '/' in asset['name'] or '\\' in asset['name']
                or asset['name'] in names or not isinstance(asset['sha256'], str) or len(asset['sha256']) != 64
                or any(character not in '0123456789abcdef' for character in asset['sha256'])):
            raise lc.ERROR('P_PROOF', 'Exact flat execution asset identities required')
        names.add(asset['name'])
    return selector, model


def validate_assignment(assignment, snapshot, policy_id):
    """Validate global availability without selecting a layer's professionals.

    Args:
        assignment: Existing immutable local functional mandate.
        snapshot: Exact captured global capability snapshot.
        policy_id: Profile-enrolled global policy identity.
    Returns:
        Global bootstrap and capabilities; no staffing choice is made.
    Raises:
        ProtocolError: Identity, broker availability or resource ceilings disagree.
    """
    descriptor = snapshot['descriptor']
    _closed(assignment['routing'], ('policy',))
    if descriptor['policy_id'] != policy_id:
        raise lc.ERROR('P_SCOPE', 'Global capability policy differs from the governing profile')
    capabilities = descriptor['capabilities']
    if assignment['issued_under'] is None and capabilities['limits'] and not assignment['limits']:
        raise lc.ERROR('P_BUDGET', 'An explicit global capability cap cannot be omitted from its root mandate')
    for effect in assignment['effects']:
        template = {key: effect[key] for key in ('operation', 'tool_policy', 'destination_handle')}
        if template not in capabilities['effects']:
            raise lc.ERROR('P_SCOPE', 'Functional mandate exceeds global broker availability')
    for limit in assignment['limits']:
        bounds = [item['ceiling'] for item in capabilities['limits']
                  if item['metric'] == limit['metric'] and item['unit'] == limit['unit']]
        if capabilities['limits'] and (not bounds or limit['ceiling'] > min(bounds)):
            raise lc.ERROR('P_BUDGET', 'Functional mandate exceeds a genuine global resource ceiling')
    selector, model = _execution(snapshot['models'], descriptor['bootstrap'])
    return {'bootstrap': copy.deepcopy(descriptor['bootstrap']), 'capabilities': copy.deepcopy(capabilities),
            'model_selector': selector, 'model': model}


def select_execution(assignment, snapshot, choice):
    """Validate an entity's captured local professional choice, never a neighbor's.

    Args:
        assignment: Exact current functional mandate whose entity made the choice.
        snapshot: Verified global catalogue/model/capability snapshot.
        choice: Existing select_execution decision payload from that entity's return.
    Returns:
        Selected professionals, model, exact execution descriptor and broker intersection.
    Raises:
        ProtocolError: Unknown staff, model, duties or execution capability fails closed.
    """
    _closed(choice, ('action', 'assignment', 'specialties', 'provider', 'workload_class', 'model_selector', 'reason', 'authority_proof', 'previous'))
    if choice['action'] != 'select_execution' or choice['authority_proof'] is not None or not _text(choice['reason']):
        raise lc.ERROR('P_SCOPE', 'Only an explicit local professional choice is supported')
    specialties = choice['specialties']
    if (not isinstance(specialties, list) or not specialties or any(not _text(slug) for slug in specialties)
            or len(set(specialties)) != len(specialties)
            or any(slug not in snapshot['instructions'] for slug in specialties)):
        raise lc.ERROR('P_PROOF', 'Selected professionals must exist in the complete global catalogue')
    roles = {row['slug']: row for row in snapshot['catalogue']['roles']}
    allowed = {'read', 'propose', 'materialize', 'measure'}
    for slug in specialties:
        tier = roles[slug].get('tool_tier')
        if tier not in _TIERS:
            raise lc.ERROR('P_PROOF', 'Selected professional has no supported tool tier')
        allowed &= _TIERS[tier]
    if assignment['responsibility'] in {'reviewer', 'integration_reviewer', 'receiver', 'measurement'}:
        allowed.discard('materialize')
    if assignment['responsibility'] == 'measurement' and 'measure' not in allowed:
        raise lc.ERROR('P_PROOF', 'Measurement work requires a measurement-capable professional')
    selector, model = _execution(snapshot['models'], choice, assignment['responsibility'])
    return {'specialties': copy.deepcopy(specialties), 'model_selector': selector, 'model': model,
            'instructions': [copy.deepcopy(snapshot['instructions'][slug]) for slug in specialties],
            'allowed_operations': sorted(allowed)}
