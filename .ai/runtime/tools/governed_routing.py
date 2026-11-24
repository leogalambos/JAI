#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Validate immutable routing snapshots without ambient catalogues or overrides."""
from __future__ import annotations

import copy
import hashlib
import re

import lifecycle as lc
import model_router
import execution_profiles
from role_context_contract import INSTRUCTION_BYTES, SECTION_BYTES, alias_key

PROTOCOL = 'jai.role-routing/1'
WORKFLOW_PROTOCOL = 'jai.role-routing/2'
REFERENCE_PROTOCOL = 'jai.role-routing/3'
CONTEXT_PROTOCOL = 'jai.role-routing/4'
QUESTION_KNOWLEDGE_PREFIX = 'question-knowledge-scope:'
PROCEDURE_SCOPE_PROTOCOL = 'jai.procedure-workflow-scope/1'
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


def capture_policy(policy_id, catalogue_bytes, models_bytes, instructions, bootstrap, capabilities, put_blob, *, workflow_policy=None, references=None, context_sections=None):
    """Capture explicit host-resolved inputs as existing immutable source material.

    Args:
        policy_id: Profile-enrolled routing policy identifier.
        catalogue_bytes: Exact canonical role catalogue bytes selected by L0.
        models_bytes: Explicit resolved model registry bytes, including local mappings.
        instructions: Selected catalogue slug to exact instruction byte mapping.
        bootstrap: Explicit functional chooser provider, workload and model.
        capabilities: Global broker templates and finite resource ceilings.
        put_blob: Existing Store immutable blob writer; never an authority action.
        workflow_policy: Optional exact independently reviewed workflow routing policy
            bytes admitted by the host for a new version-two routing snapshot.
        references: Optional role-to-named-reference byte mapping for new snapshots.
        context_sections: Optional classified byte ranges for exact role instructions.
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
    workflow_assets = []
    if workflow_policy is not None:
        descriptor['protocol'] = WORKFLOW_PROTOCOL
        descriptor['workflow_policy_blob_id'] = put_blob(workflow_policy)
        workflow_assets.append(descriptor['workflow_policy_blob_id'])
    reference_assets = []
    if references:
        descriptor['protocol'] = REFERENCE_PROTOCOL
        descriptor['reference_blobs'] = {
            slug: {name: put_blob(raw) for name, raw in sorted(items.items())}
            for slug, items in sorted(references.items())}
        reference_assets = [identifier for items in descriptor['reference_blobs'].values()
                            for identifier in items.values()]
    if context_sections:
        descriptor['protocol'] = CONTEXT_PROTOCOL
        descriptor.setdefault('reference_blobs', {})
        descriptor['context_sections'] = copy.deepcopy(context_sections)
    descriptor_id = put_blob(lc.canonical(descriptor))
    material = [descriptor_id, descriptor['catalogue_blob_id'], descriptor['models_blob_id'],
                *descriptor['instruction_blobs'].values(), *workflow_assets, *reference_assets]
    return list(dict.fromkeys(material))


def load_policy(source, blob_reader, *, current_workflows=None, current_contracts=None, current_ancestry=None):
    """Resolve and validate a complete immutable captured routing snapshot.

    Args:
        source: Existing L0-owned policy source record with descriptor-first material.
        blob_reader: Exact immutable-byte reader for the journal's captured inputs.
        current_workflows: Canonical bindings for explicit new profile enrollment.
        current_contracts: Canonical artifact contracts for that enrollment.
        current_ancestry: Current composition ancestry for that enrollment.
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
    fields = ('protocol', 'policy_id', 'catalogue_blob_id', 'instruction_blobs',
              'models_blob_id', 'bootstrap', 'capabilities')
    version = descriptor.get('protocol') if isinstance(descriptor, dict) else None
    scoped = version == CONTEXT_PROTOCOL
    has_references = version == REFERENCE_PROTOCOL or scoped
    workflow = version == WORKFLOW_PROTOCOL or (has_references and 'workflow_policy_blob_id' in descriptor)
    _closed(descriptor, fields + (('workflow_policy_blob_id',) if workflow else ())
            + (('reference_blobs',) if has_references else ())
            + (('context_sections',) if scoped else ()))
    if version not in {PROTOCOL, WORKFLOW_PROTOCOL, REFERENCE_PROTOCOL, CONTEXT_PROTOCOL} or not _text(descriptor['policy_id']):
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
    if workflow:
        expected.add(descriptor['workflow_policy_blob_id'])
    if has_references:
        reference_blobs = descriptor['reference_blobs']
        if not isinstance(reference_blobs, dict) or (not scoped and not reference_blobs) or not reference_blobs.keys() <= by_slug.keys():
            raise lc.ERROR('P_PROOF', 'Deferred references require exact captured role slugs')
        for entries in reference_blobs.values():
            if not isinstance(entries, dict) or not entries:
                raise lc.ERROR('P_SCHEMA', 'Named deferred reference entries are required')
            for name, identifier in entries.items():
                if (not re.fullmatch(r'knowledge/(?:[a-z0-9][a-z0-9-]*/)+[a-z0-9][a-z0-9-]*\.md', name)
                        or not isinstance(identifier, str) or not re.fullmatch(r'[0-9a-f]{64}', identifier)):
                    raise lc.ERROR('P_SCHEMA', 'Invalid deferred reference identity')
                expected.add(identifier)
                try:
                    if not read(identifier).decode('utf-8').strip():
                        raise lc.ERROR('P_PROOF', 'Deferred reference is empty')
                except UnicodeError as error:
                    raise lc.ERROR('P_SCHEMA', 'Deferred references must be UTF-8') from error
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
        if has_references and any(f'({name})' not in text for name in reference_blobs.get(slug, {})):
            raise lc.ERROR('P_PROOF', 'Deferred reference is absent from the captured role instructions')
        instructions[slug] = {'slug': slug, 'blob_id': identifier, 'text': text}
    if scoped:
        for row in rows:
            aliases = row.get('aliases')
            if (not isinstance(aliases, list) or any(not isinstance(alias, str) for alias in aliases)
                    or any(not key or key in by_slug and key != row['slug'] for key in map(alias_key, aliases))):
                raise lc.ERROR('P_PROOF', 'Scoped role aliases shadow an exact identity or lack lookup text')
            if len(instructions[row['slug']]['text'].encode('utf-8')) > INSTRUCTION_BYTES:
                raise lc.ERROR('P_BUDGET', 'Scoped role exceeds its exact instruction byte limit')
        _validate_context_sections(descriptor, instructions)
    problems = model_router.validate_registry(models)
    if problems:
        raise lc.ERROR('P_PROOF', 'Captured model registry is invalid: ' + '; '.join(problems))
    row_policy = models.get('sabsa_row_policy')
    if 'sabsa_row_policy' in models:
        lc._validate_row_policy(row_policy)
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
    snapshot = {'descriptor': descriptor, 'catalogue': catalogue, 'models': models, 'instructions': instructions}
    if scoped:
        snapshot['knowledge_task_paths'] = sorted({
            path for sections in descriptor['context_sections'].values()
            for section in sections for path in section['scope'].get('task', ())
        })
    if workflow:
        import workflow_role_selection as selection
        policy = lc.loads(read(descriptor['workflow_policy_blob_id']))
        fields = ('catalogue', 'reviewed', 'ancestry', 'contract_versions')
        scoped_procedures = isinstance(policy, dict) and 'procedure_scope_protocol' in policy
        profiles = isinstance(policy, dict) and 'specialist_profiles' in policy
        _closed(policy, fields + (('procedure_scope_protocol',) if scoped_procedures else ())
                + (('specialist_profiles',) if profiles else ()))
        if scoped_procedures:
            if policy['procedure_scope_protocol'] != PROCEDURE_SCOPE_PROTOCOL:
                raise lc.ERROR('P_SCHEMA', 'Unsupported layered specialty scope protocol')
            snapshot['procedure_scope_protocol'] = PROCEDURE_SCOPE_PROTOCOL
        try:
            body = dict(policy['catalogue'])
            digest = body.pop('catalog_hash')
            from content_spec import canonical_hash
            if canonical_hash(body) != digest:
                raise ValueError('Workflow catalogue digest mismatch')
            if profiles:
                from workflow_specialist_profiles import verify_policy
                if current_ancestry is not None and any(current_ancestry.get(slug) != ancestors
                        for slug, ancestors in policy['ancestry'].items()):
                    raise ValueError('WORKFLOW_PROFILE_ANCESTRY_DRIFT')
                snapshot['workflow_roles'] = verify_policy(policy, by_slug, mapping,
                    catalogue=current_workflows, contracts=current_contracts)
            else:
                snapshot['workflow_roles'] = selection.compile_requirements(
                    policy['catalogue'], policy['reviewed'], by_slug, policy['ancestry'],
                    policy['contract_versions'])
        except (ValueError, TypeError, KeyError) as error:
            raise lc.ERROR('P_PROOF', 'Captured workflow role policy is invalid') from error
        snapshot['workflow_catalogue'] = policy['catalogue']
    return snapshot


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
    workflow_scope = 'workflow_scope' in assignment['routing']
    _closed(assignment['routing'], ('policy', 'workflow_scope') if workflow_scope else ('policy',))
    if workflow_scope and 'workflow_roles' not in snapshot:
        raise lc.ERROR('P_SCOPE', 'Workflow role selection requires a captured workflow policy')
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


def procedure_scope_id(owner):
    """Return the reserved source ID for one exact question owner.

    Args:
        owner: Existing canonical question owner record.
    Returns:
        An engagement-local source identifier with no embedded operator data.
    """
    return 'procedure-workflow-scope:' + hashlib.sha256(lc.canonical(owner)).hexdigest()


def question_knowledge_scope_id(owner):
    """Return the reserved standalone scope identity for the exact question owner.

    Args:
        owner: Existing canonical question owner record.
    Returns:
        The engagement-local logical ID of its scope source.
    """
    return QUESTION_KNOWLEDGE_PREFIX + hashlib.sha256(lc.canonical(owner)).hexdigest()


_KNOWLEDGE_DIMENSIONS = {'provider', 'method', 'product', 'activity'}
_DISCOVERY_HANDLE = 'role-knowledge:discover'
_TARGET_LIMIT = 16
_DISCOVERY_BYTES = 2048
_DISCOVERY_ENTRIES = 8
_EFFECT_ACTIVITIES = {
    'conditional-access-lockout-risk': 'conditional-access-recovery',
    'java-public-api-change': 'java-api-documentation',
    'android-release-bound-change': 'android-release',
}


def _knowledge_dimensions(value, product_scope, generic, *, target=False, task_paths=()):
    dimensions = _KNOWLEDGE_DIMENSIONS | ({'effects'} if target else set())
    if task_paths:
        dimensions = dimensions | {'task'}
    if (not isinstance(value, dict) or not value or not value.keys() <= dimensions
            or any(not isinstance(values, list) or not values
                   or any(not isinstance(item, str) or (
                       item not in task_paths if key == 'task' else not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', item)
                   ) for item in values)
                   or sorted(set(values)) != values for key, values in value.items())):
        raise lc.ERROR('P_SCOPE', 'Knowledge scope must declare exact normalized dimensions')
    if 'product' in value and (generic or product_scope is not None and (
            not isinstance(product_scope, dict) or value['product'] != [product_scope.get('product')])):
        raise lc.ERROR('P_SCOPE', 'Knowledge product scope contradicts the governing workflow scope')
    if any(len(value.get(key, ())) > 1 for key in ('product', 'provider', 'task')):
        raise lc.ERROR('P_SCOPE', 'Each knowledge target must identify one product and provider at most, with one task path')
    effects = value.get('effects', ())
    if set(effects) - _EFFECT_ACTIVITIES.keys():
        raise lc.ERROR('P_SCOPE', 'Knowledge target contains an unsupported observed effect')
    result = {key: list(items) for key, items in value.items() if key != 'effects'}
    if effects:
        result['activity'] = sorted(set(result.get('activity', ())) |
                                    {_EFFECT_ACTIVITIES[effect] for effect in effects})
        result['effects'] = list(effects)
    return result


def standalone_knowledge_scope(owner, scope, reference, snapshot):
    """Validate a standalone question scope previously attributed by the host.

    Args:
        owner: The exact assignment owner.
        scope: Decoded, versioned current source supplied by an authority.
        reference: Its exact input reference.
        snapshot: Captured role policy defining eligible knowledge task paths.
    Returns:
        Normalized target evidence used for reproducible context selection.
    Raises:
        ProtocolError: Owner, dimensions or discovery request is invalid.
    """
    discovery = isinstance(scope, dict) and 'discover_knowledge' in scope
    _closed(scope, ('owner', 'knowledge_targets') + (('discover_knowledge',) if discovery else ()))
    values = scope['knowledge_targets']
    if (owner != scope['owner'] or reference['logical_id'] != question_knowledge_scope_id(owner)
            or not isinstance(values, list) or not 1 <= len(values) <= _TARGET_LIMIT
            or discovery and scope['discover_knowledge'] is not True):
        raise lc.ERROR('P_SCOPE', 'Standalone knowledge scope must identify its exact assignment owner and targets')
    paths = snapshot.get('knowledge_task_paths', ())
    return {'scope_ref': copy.deepcopy(reference),
            'knowledge_targets': [_knowledge_dimensions(
                value, None, False, target=True, task_paths=paths) for value in values],
            'discover_knowledge': discovery}


def workflow_eligibility(assignment, snapshot, scope, scope_ref):
    """Evaluate the routing policy against an already admitted workflow scope.

    Args:
        assignment: Exact current functional assignment.
        snapshot: Validated immutable workflow-capable routing snapshot.
        scope: Typed facts resolved from a current attributable host input.
        scope_ref: Exact reference to that source in the assignment.
    Returns:
        Eligible exact slugs and the scope and mapping evidence for replay.
    Raises:
        ProtocolError: A scope is malformed or outside its pinned workflow policy.
    """
    import workflow_role_selection as selection

    fields = ('workflow_catalogue', 'work_item', 'handoff', 'path', 'endpoint', 'mode', 'product_scope')
    procedure_task = assignment.get('procedure_task')
    generic = 'generic_applicable' in scope
    scoped = snapshot['descriptor']['protocol'] == CONTEXT_PROTOCOL
    knowledge = 'knowledge_scope' in scope and scoped
    targets = 'knowledge_targets' in scope and scoped
    discovery = 'discover_knowledge' in scope and scoped
    if discovery and (scope['discover_knowledge'] is not True or not (knowledge or targets)):
        raise lc.ERROR('P_SCOPE', 'Discovery requires an explicit partially known knowledge scope')
    if knowledge and targets:
        raise lc.ERROR('P_SCOPE', 'Use one knowledge scope representation')
    _closed(scope, fields + (('procedure_owner',) if procedure_task is not None else ())
            + (('generic_applicable',) if generic else ())
            + (('knowledge_scope',) if knowledge else ())
            + (('knowledge_targets',) if targets else ())
            + (('discover_knowledge',) if discovery else ()))
    if generic and type(scope['generic_applicable']) is not bool:
        raise lc.ERROR('P_SCOPE', 'Generic applicability must be an exact admitted fact')
    if procedure_task is not None and (snapshot.get('procedure_scope_protocol') != PROCEDURE_SCOPE_PROTOCOL
            or scope['procedure_owner'] != assignment['owner']
            or scope_ref['logical_id'] != procedure_scope_id(assignment['owner'])):
        raise lc.ERROR('P_SCOPE', 'Workflow scope differs from the exact layered question owner')
    compiled = snapshot.get('workflow_roles')
    if (compiled is None or scope['workflow_catalogue'] != compiled['workflow_catalogue']
            or assignment['routing'].get('workflow_scope') != scope_ref
            or scope['work_item'] != assignment['owner']['work_item']):
        raise lc.ERROR('P_SCOPE', 'Workflow scope requires its exact captured routing policy')
    try:
        eligible, evidence = selection.eligible_roles(
            snapshot['workflow_catalogue'], compiled,
            handoff=scope['handoff'], path=scope['path'], endpoint=scope['endpoint'],
            responsibility=assignment['responsibility'], scope=scope['product_scope'],
            available=snapshot['instructions'],
            independent=scope['endpoint'] == 'producer' and assignment['responsibility'] == 'author',
            generic_applicable=scope.get('generic_applicable', False))
    except (ValueError, TypeError, KeyError) as error:
        raise lc.ERROR('P_SCOPE', 'Workflow scope does not resolve to an exact policy binding') from error
    if generic and 'profile' not in evidence:
        raise lc.ERROR('P_SCOPE', 'Generic applicability requires an exact compatibility profile')
    if scope['mode'] != evidence['mode']:
        raise lc.ERROR('P_SCOPE', 'Workflow scope requirements cannot fall back to an exact role')
    if knowledge:
        evidence['knowledge_scope'] = _knowledge_dimensions(
            scope['knowledge_scope'], scope['product_scope'], scope.get('generic_applicable'))
    if targets:
        values = scope['knowledge_targets']
        if not isinstance(values, list) or not values or len(values) > _TARGET_LIMIT:
            raise lc.ERROR('P_SCOPE', 'Knowledge targets require one to sixteen exact scopes')
        evidence['knowledge_targets'] = [
            _knowledge_dimensions(value, scope['product_scope'], scope.get('generic_applicable'), target=True)
            for value in values
        ]
    if discovery:
        evidence['discover_knowledge'] = True
    return {'eligible': eligible, 'scope_ref': copy.deepcopy(scope_ref), 'binding': evidence}


def _validate_context_sections(descriptor, instructions):
    roles = descriptor['context_sections']
    if not isinstance(roles, dict) or not roles or not roles.keys() <= instructions.keys():
        raise lc.ERROR('P_PROOF', 'Scoped sections must identify captured roles')
    for slug, sections in roles.items():
        if not isinstance(sections, list) or not sections:
            raise lc.ERROR('P_SCHEMA', 'Scoped sections require ordered ranges')
        previous = 0
        recorded = set()
        instruction = instructions[slug]['text'].encode('utf-8')
        references = descriptor['reference_blobs'].get(slug, {})
        for section in sections:
            _closed(section, ('id', 'scope', 'reference', 'start', 'end', 'sha256'))
            start, end = section['start'], section['end']
            scope, identity, reference = section['scope'], section['id'], section['reference']
            if (type(start) is not int or type(end) is not int
                    or not previous <= start < end <= len(instruction) or end - start > SECTION_BYTES
                    or hashlib.sha256(instruction[start:end]).hexdigest() != section['sha256']
                    or not _text(identity) or identity in recorded
                    or reference is not None and (not isinstance(reference, str) or reference not in references
                                                  or f'({reference})'.encode() not in instruction[start:end])
                    or not isinstance(scope, dict) or not scope.keys() <=
                    {'provider', 'product', 'method', 'responsibility', 'task', 'activity'}
                    or any(not isinstance(values, list) or not values
                           or any(not _text(value) for value in values) for values in scope.values())):
                raise lc.ERROR('P_PROOF', 'Invalid scoped role section or reference binding')
            if any(boundary < len(instruction) and instruction[boundary] & 0xc0 == 0x80
                   for boundary in (start, end)):
                raise lc.ERROR('P_PROOF', 'Scoped section splits UTF-8')
            previous = end
            recorded.add(identity)


def _project_instructions(snapshot, specialties, assignment, workflow_selection, knowledge_scope):
    binding = knowledge_scope or (workflow_selection or {}).get('binding', {})
    common = {'responsibility': [assignment['responsibility']]}
    if binding.get('path') is not None:
        common['task'] = [binding['path']]
    product = (binding.get('scope') or {}).get('product')
    if product is not None:
        common['product'] = [product]
    targets = binding.get('knowledge_targets', [binding.get('knowledge_scope', {})])
    candidates = [{**target, **common} for target in targets]
    sections_by_role = snapshot['descriptor'].get('context_sections', {})
    instructions, excluded, discovery = [], {}, {}
    for slug in specialties:
        instruction = copy.deepcopy(snapshot['instructions'][slug])
        sections = sections_by_role.get(slug)
        if not sections:
            instructions.append(instruction)
            continue
        raw = instruction['text'].encode('utf-8')
        blocked = []
        admitted = set()
        chunks = []
        cursor = 0
        for section in sections:
            reference = section['reference']
            if any(all(set(dimensions.get(key, ())).intersection(values)
                       for key, values in section['scope'].items()) for dimensions in candidates):
                if reference:
                    admitted.add(reference)
                continue
            if reference and binding.get('discover_knowledge') and any(
                section['scope'].keys() & (target.keys() | ({'product'} if product else set()))
                and all(dimensions.get(key) in (None, [None])
                        or set(dimensions[key]).intersection(values)
                        for key, values in section['scope'].items())
                for target, dimensions in zip(targets, candidates)
            ):
                discovery[f'role-reference:{slug}:{reference}'] = {
                    'section': section['id'], 'scope': section['scope'],
                }
            chunks.append(raw[cursor:section['start']])
            cursor = section['end']
            if reference:
                blocked.append(reference)
        if chunks:
            projected = b''.join([*chunks, raw[cursor:]])
            instruction.update(text=projected.decode('utf-8'), blob_id=lc.blob(projected))
        instructions.append(instruction)
        if blocked:
            excluded[slug] = sorted(set(blocked) - admitted)
    entries = []
    for handle, entry in sorted(discovery.items()):
        slug, reference = handle.split(':', 2)[1:]
        if reference not in excluded.get(slug, ()):
            continue
        candidate = {'handle': handle, **entry}
        if len(entries) == _DISCOVERY_ENTRIES or len(lc.canonical({'references': [*entries, candidate]})) > _DISCOVERY_BYTES:
            break
        entries.append(candidate)
    return instructions, excluded, entries


def select_execution(assignment, snapshot, choice, *, workflow_selection=None, knowledge_scope=None):
    """Validate an entity's captured local professional choice, never a neighbor's.

    Args:
        assignment: Exact current functional mandate whose entity made the choice.
        snapshot: Verified global catalogue/model/capability snapshot.
        choice: Existing select_execution decision payload from that entity's return.
        knowledge_scope: Host-validated standalone scope linked to this exact assignment.
        workflow_selection: Host-evaluated exact workflow eligibility when the
            assignment cites a current attributable workflow-scope source.
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
    if 'workflow_scope' in assignment['routing']:
        if (workflow_selection is None or len(specialties) != 1
                or specialties[0] not in workflow_selection['eligible']):
            raise lc.ERROR('P_SCOPE', 'One eligible role is required for this exact workflow assignment')
    elif workflow_selection is not None:
        raise lc.ERROR('P_SCOPE', 'Workflow selection requires an explicit assignment scope')
    if knowledge_scope is not None and (workflow_selection is not None
            or snapshot['descriptor']['protocol'] != CONTEXT_PROTOCOL
            or knowledge_scope['scope_ref']['logical_id'] != question_knowledge_scope_id(assignment['owner'])):
        raise lc.ERROR('P_SCOPE', 'Standalone knowledge scope requires its exact validated input')
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
    instructions, excluded, discovery = _project_instructions(snapshot, specialties, assignment, workflow_selection, knowledge_scope)
    result = {'specialties': copy.deepcopy(specialties), 'model_selector': selector, 'model': model,
            'instructions': instructions,
            'allowed_operations': sorted(allowed)}
    if excluded:
        result['excluded_references'] = excluded
    if discovery and 'read' in allowed:
        result['knowledge_discovery'] = discovery
    if workflow_selection is not None:
        result['workflow_selection'] = copy.deepcopy(workflow_selection)
    return result


def deferred_reference_handles(execution):
    """Return scoped read handles for exact selected work, using only captured bytes."""
    if execution['phase'] != 'work' or 'read' not in execution['allowed_operations']:
        return {}
    entries = execution['snapshot']['descriptor'].get('reference_blobs', {})
    return {'role-reference:' + slug + ':' + name: identifier
            for slug in execution['specialties'] for name, identifier in entries.get(slug, {}).items()
            if name not in execution.get('excluded_references', {}).get(slug, ())}


def discovered_knowledge_handles(execution):
    """Return the optional captured lookup page and exact eligible reference handles.

    Args:
        execution: Validated work selection and its immutable routing snapshot.
    Returns:
        A mapping of lookup or reference handles to content IDs and the lookup
        bytes to persist, or empty results when discovery was not requested.
    """
    entries = execution.get('knowledge_discovery', ())
    if not entries:
        return {}, None
    payload = lc.canonical({'references': entries})
    references = execution['snapshot']['descriptor']['reference_blobs']
    handles = {_DISCOVERY_HANDLE: lc.blob(payload)}
    for entry in entries:
        handle = entry['handle']
        slug, name = handle.split(':', 2)[1:]
        handles[handle] = references[slug][name]
    return handles, payload


def instruction_handles(execution, put_blob):
    """Return broker handles for the captured phase and effective instructions.

    Args:
        execution: Validated context execution with its immutable routing snapshot.
        put_blob: Immutable blob writer for the exact projected instruction bytes.
    Returns:
        Handle-to-blob map for the phase.
    Raises:
        OSError: An effective instruction blob cannot be stored.
    """
    descriptor = execution['snapshot']['descriptor']
    if execution['phase'] == 'work' and descriptor['protocol'] == CONTEXT_PROTOCOL:
        return {'instruction:' + item['slug']: put_blob(item['text'].encode('utf-8'))
                for item in execution['instructions']}
    return {'catalogue': descriptor['catalogue_blob_id'],
            **{'instruction:' + slug: identifier
               for slug, identifier in descriptor['instruction_blobs'].items()}}
