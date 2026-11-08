#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Prepare existing native agents over the sole governed Store, never invoke LLMs.

The trusted active-session parent executes returned native invocation intent and
records actual handles/results through NativeSession. Input attribution records
the operator's supplied request; it is neither enrollment nor an L0 decision.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import time
import uuid
from pathlib import Path

import agent_runtime
import governed_delivery as wire
import governed_routing as routing
import lifecycle as lc
import model_router
import execution_profiles
import provider_projection

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ('what', 'why', 'how', 'who', 'where', 'when')


def _task_name(invocation):
    """Map an exact opaque invocation to a deterministic native-safe correlation name."""
    return 'jai_' + hashlib.sha256(invocation.encode('utf-8')).hexdigest()[:24]


def _reference(store, logical_id, family, record):
    value = lc.record_manifest(store.engagement, 'default', logical_id, family, record)
    return {'engagement': store.engagement, 'scope': 'default',
            'logical_id': logical_id, 'version_id': lc.version_id(value)}


def _profile(controller, work_item, request_ttl_ms, limits, deadline_ms, local_budget):
    obligations = []
    for layer in range(1, 7):
        for question in QUESTIONS:
            owner = {'layer': layer, 'work_kind': 'question', 'question': question,
                     'work_item': work_item}
            for role, family in (('input', 'source'), ('answer', 'product'),
                                 ('professional_review', 'assessment')):
                obligations.append({'slot_id': f'L{layer}:{work_item}:{question}-{role}',
                    'owner': owner, 'subject_kind': 'answer', 'role': role,
                    'required_kind': family, 'minimum': 1, 'maximum': 1,
                    'allow_exclusion': False, 'exclusion_owner': None})
        owner = {'layer': layer, 'work_kind': 'integration', 'question': None,
                 'work_item': work_item}
        for role, subject in (('integration_review', 'bundle'), ('receiving_acceptance', 'handoff')):
            obligations.append({'slot_id': f'L{layer}:{work_item}:integration-{role}',
                'owner': owner, 'subject_kind': subject, 'role': role,
                'required_kind': 'assessment', 'minimum': 1, 'maximum': 1,
                'allow_exclusion': False, 'exclusion_owner': None})
    return {'owner': controller, 'profile_id': 'native-layered', 'protocol': wire.PROTOCOL,
            'source_profiles': [], 'obligations': obligations, 'max_clock_skew_ms': 5000,
            'max_request_duration_ms': request_ttl_ms, 'local_budget': copy.deepcopy(local_budget),
            'authority_policy_id': 'host-authority', 'routing_policy_id': 'host-routing',
            'content_profile': None, 'scheduling': {'collection_window_ms': min(60000, request_ttl_ms),
                'control_limits': copy.deepcopy(limits), 'initial_deadline_ms': deadline_ms, 'max_search_steps': None,
                'max_escalation_rounds': 10}}


def bootstrap(store, task_bytes, criteria_bytes, provider, work_item, limits,
              deadline_ms, model_config=None, *, human_id='L0-operator',
              destinations=(), tools=(), packet_bytes=2097152, total_bytes=8388608, local_budget=None,
              project=None, execution_profile=None, execution_context_policy=None):
    """Start a new-format engagement from the actual operator's explicit inputs.

    Args:
        store: Sole empty engagement Store; existing history is never replaced.
        task_bytes: Exact nonempty UTF-8 user request bytes.
        criteria_bytes: Exact nonempty UTF-8 operator acceptance criteria bytes.
        provider: Active session, codex or claude; no client is launched.
        work_item: Stable explicit outcome identity, not a staffing choice.
        limits: Optional aggregate elapsed_ms/ms bounds; [] imposes no task cap.
        deadline_ms: Explicit future aggregate stop, or None for no global deadline.
        model_config: Optional existing model-registry override path, captured once.
        project: Project root for optional execution preferences, otherwise cwd.
        execution_profile: Explicit new-run profile selection, never a resume override.
        execution_context_policy: Explicit context from a current session selection;
            captured once at new-run entry, never applied on resume.
        human_id: Attribution of the current input supplier, not a verified signer.
        destinations: Existing explicit host destination enrollments, if needed.
        tools: Existing explicit measurement enrollments, if needed.
        packet_bytes: Existing per-packet byte ceiling.
        total_bytes: Existing per-run logical transfer ceiling.
        local_budget: Optional exact iteration_ms/max_reworks configuration; defaults
            to 600000 milliseconds per local iteration and three actual reworks.
    Returns:
        Bootstrap receipt, exact source/profile references and default host config.
    Raises:
        ValueError, ProtocolError, OSError: Invalid input, unavailable resources,
            existing engagement, or rejection by the unchanged bootstrap boundary.
    """
    now = int(time.time() * 1000)
    if (provider not in {'codex', 'claude'} or not work_item or not human_id
            or deadline_ms is not None and (type(deadline_ms) is not int or deadline_ms <= now)):
        raise ValueError('Explicit active provider, identities and future deadline required')
    for raw in (task_bytes, criteria_bytes):
        if not isinstance(raw, bytes) or not raw.decode('utf-8').strip():
            raise ValueError('Exact nonempty UTF-8 task and criteria bytes required')
    if any(set(item) != {'metric', 'unit', 'ceiling'}
            or item['metric'] != 'elapsed_ms' or item['unit'] != 'ms'
            or type(item['ceiling']) is not int or item['ceiling'] <= 0 for item in limits):
        raise ValueError('Native accounting requires finite elapsed_ms/ms limits')
    local_budget = {'iteration_ms': 600000, 'max_reworks': 3} if local_budget is None else copy.deepcopy(local_budget)
    if (set(local_budget) != {'iteration_ms', 'max_reworks'} or type(local_budget['iteration_ms']) is not int
            or local_budget['iteration_ms'] <= 0 or type(local_budget['max_reworks']) is not int
            or local_budget['max_reworks'] < 0):
        raise ValueError('Local budgets require positive iteration_ms and a nonnegative max_reworks')
    if store.read().initialized:
        raise ValueError('Native bootstrap requires an empty engagement')
    controller = {'kind': 'controller', 'id': 'native-controller'}
    human = {'kind': 'authority', 'id': human_id}
    task = {'owner': human, 'source_role': 'input', 'origin': human,
            'material': [store.put_blob(task_bytes)], 'criteria': [], 'inherited': []}
    task_ref = _reference(store, 'request', 'source', task)
    criteria = {'owner': human, 'source_role': 'criteria', 'origin': human,
        'material': [store.put_blob(criteria_bytes)], 'criteria': [{'id': 'operator-criteria',
            'requirement': task_ref, 'statement': criteria_bytes.decode('utf-8'),
            'evidence_slots': []}], 'inherited': [task_ref]}
    models, _ = model_router.effective_registry(model_config)
    models['execution_profile'] = execution_profiles.resolve(
        Path.cwd() if project is None else project, models, provider, execution_profile,
        context_policy=execution_context_policy)
    selector, _ = model_router.resolve_snapshot(models, provider, 'light')
    catalogue = (ROOT / 'roles.json').read_bytes()
    rows = lc.loads(catalogue)['roles']
    skills = ROOT.parent / 'skills' if (ROOT.parent / 'skills').is_dir() else ROOT / 'skills'
    instructions = {row['slug']: (skills / row['skill'] / 'references' /
                    (row['slug'] + '.md')).read_bytes() for row in rows}
    capabilities = {'effects': [
        {'operation': operation, 'tool_policy': None, 'destination_handle': None}
        for operation in ('read', 'propose')], 'limits': copy.deepcopy(limits)}
    capabilities['effects'].extend({'operation': 'materialize', 'tool_policy': None,
        'destination_handle': item['handle']} for item in destinations)
    capabilities['effects'].extend({'operation': 'measure', 'tool_policy': item['policy'],
        'destination_handle': None} for item in tools)
    policy = {'owner': human, 'source_role': 'policy', 'origin': human,
        'material': routing.capture_policy('host-routing', catalogue, lc.canonical(models),
            instructions, {'provider': provider, 'workload_class': 'light',
                           'model_selector': selector}, capabilities, store.put_blob),
        'criteria': [], 'inherited': []}
    request_ttl_ms = local_budget['iteration_ms']
    profile = _profile(controller, work_item, request_ttl_ms, limits, deadline_ms, local_budget)
    bootstrap_expiry = now + request_ttl_ms
    if deadline_ms is not None:
        bootstrap_expiry = min(bootstrap_expiry, deadline_ms)
    message = {'protocol': wire.PROTOCOL, 'message_type': 'bootstrap', 'message_id': '0' * 64,
        'request_id': str(uuid.uuid4()), 'correlation_id': work_item,
        'engagement': store.engagement, 'scope': 'default', 'sender': controller,
        'recipient': controller, 'context': None, 'profile': None,
        'expected_head': lc.ZERO, 'issued_at_ms': now, 'expires_at_ms': bootstrap_expiry,
        'causes': [], 'attachments': [], 'payload': {'controller_id': controller['id'],
            'use_scopes': ['default'], 'profile': {'logical_id': 'profile', 'record': profile},
            'l0_inputs': [{'logical_id': name, 'record': record} for name, record in
                          (('request', task), ('criteria', criteria), ('role-routing', policy))]}}
    message['message_id'] = wire.message_id(message)
    config = {'protocol': 'jai.host-dispatch/1', 'workers': [],
              'destinations': list(destinations), 'tools': list(tools),
              'limits': {'packet_bytes': packet_bytes, 'total_bytes': total_bytes}}
    # Validate host assets before committing initial state, using its existing gate.
    import governed_dispatch
    governed_dispatch.Dispatcher(store, config)
    response = store.submit(lc.canonical(message))
    if response['status'] != 'committed':
        raise lc.ERROR(response['error']['code'], response['error']['message'])
    return {'receipt': response['receipt'], 'profile': _reference(store, 'profile', 'profile', profile),
            'sources': {name: _reference(store, name, 'source', record) for name, record in
                        (('request', task), ('criteria', criteria), ('role-routing', policy))},
            'config': config}


def _response_contract(packet, assignment, profile):
    """Describe actual role semantics without asking a model to author wire metadata."""
    role = 'selection' if packet['execution']['phase'] == 'selection' else assignment['responsibility']
    purposes = {
        'selection': 'Choose actual catalogue specialties and an available model for your own professional mandate.',
        'setter': 'Formulate actual local requirements and a closed question or layer procedure. On discretionary returns make an explicit ordinary owner_action; never invent a review. Criterion evidence_slots names additional separately qualified observation prerequisites. Use [] for ordinary candidate-content review. The answer slot, assessed subject and review/proof slots are not observation bindings; do not list them as evidence_slots.',
        'author': 'Produce the actual answer, chosen evidence and limitations against your exact local mandate.',
        'reviewer': 'Independently assess the actual assigned candidate. Supply your explicit verdict, rationale, findings and conditions; never fix it.',
        'integration_reviewer': 'Independently assess the actual integration bundle with an explicit verdict, rationale, findings and conditions.',
        'receiver': 'Independently assess the exact adjacent handoff. Explicit acceptance is a professional verdict, not a release or human authority.',
        'integrator': 'Integrate actual assigned answers, preserving chosen answer relationships and limitations. Do not fabricate approval.',
        'measurement': 'Report actual observations, evidence and unavailable or failed measurements honestly.'}
    if role in {'author', 'measurement', 'reviewer', 'integration_reviewer', 'receiver'}:
        purposes[role] += (' Evidence references denote additional observation products qualified before use, '
                           'not request, criteria, assignment or source citations. Use [] when none are needed; '
                           'the host already binds input and criteria provenance. Keep source citations in actual material.')
    if role == 'integrator':
        purposes[role] += (' Use the declared answers and related relationships; do not add an evidence field. '
                           'The host binds input and criteria provenance. Keep source citations in actual material.')
    owners = [item for item in profile['obligations'] if item['owner'] == assignment['owner']
              or (role == 'setter' and assignment['owner']['work_kind'] == 'integration'
                  and item['owner']['layer'] == assignment['owner']['layer']
                  and item['owner']['work_item'] == assignment['owner']['work_item'])]
    return {'purpose': purposes[role], 'mandate': purposes[assignment['responsibility']],
        'recipient': profile['owner'], 'profile_obligations': owners,
        'semantic_kind': role,
        'mechanics': ('Return exactly {format,results} using format jai.semantic-return/1. '
            'Complete the issued member/kind skeleton with specialties, provider, workload_class, '
            'model_selector and your actual reason. specialties are exact catalogue row.slug values, '
            'never display labels. Match the model selector to its provider/workload availability entry.'
            if role == 'selection' else
            'Return jai.semantic-return/1 with one actual role result per issued member. '
            'Use only declared aliases in reference fields. Domain materials and business identifiers '
            'remain your actual content. The host fills exact structural metadata; do not calculate '
            'hashes, construct wire records, copy context fields or invent a verdict. '
            'Every entity chooses its own specialties from the complete catalogue.')}


def _operator_projections(execution, responsibility, provider, models, workload):
    """Preserve each selected specialty's canonical operator under common ceilings."""
    models = copy.deepcopy(models)
    # Projections must describe the exact validated selection, including effort.
    selected = copy.deepcopy(execution['model'])
    selected.pop('execution', None)
    models['providers'][provider]['classes'][workload] = selected
    groups = {}
    if execution['phase'] == 'selection':
        groups['role-router'] = []
    else:
        rows = {row['slug']: row for row in execution['snapshot']['catalogue']['roles']}
        for slug in execution['specialties']:
            groups.setdefault(rows[slug]['operator_agent'], []).append(slug)
    contracts = agent_runtime.contracts()
    operators, ceilings, sources = [], [], {}
    for name in groups:
        source = model_router.agent_root() / (name + '.md')
        frontmatter, _ = provider_projection.split_frontmatter(source.read_text(encoding='utf-8'))
        ceiling = {tool.strip() for tool in frontmatter.get('tools', '').split(',') if tool.strip()}
        if responsibility in {'reviewer', 'integration_reviewer', 'receiver', 'measurement'}:
            ceiling -= {'Write', 'Edit'}
        ceilings.append(ceiling)
        sources[name] = source, ceiling
    common_tools = set.intersection(*ceilings)
    for name, specialties in groups.items():
        source, tools = sources[name]
        contract = copy.deepcopy(contracts.get(name))
        if contract is not None:
            contract['workload_class'] = workload
        projection = (provider_projection.render_codex_skill(source, 'agent', name, models, workload_class=workload, tool_ceiling=common_tools)
            if provider == 'codex' else provider_projection.render_claude_agent(source, models, workload_class=workload, tool_ceiling=common_tools))
        operators.append({'agent': name, 'specialties': specialties,
            'source_tools': sorted(tools), 'projection': projection.decode('utf-8'),
            'provider_config': agent_runtime.provider_config(contract, provider, registry=models, tool_ceiling=common_tools) if contract is not None else None,
            'contract_status': 'registered-contract' if contract is not None else 'canonical-source-only'})
    operations = set(execution.get('allowed_operations', ['read', 'propose']))
    if responsibility in {'reviewer', 'integration_reviewer', 'receiver', 'measurement'}:
        operations.discard('materialize')
    return operators, sorted(common_tools), sorted(operations)


def _project_schema(definition, documents, document='semantic-return.schema.json'):
    """Copy only the referenced definitions required by one actual semantic role."""
    definitions = {}
    def project(value, current):
        if isinstance(value, list):
            return [project(item, current) for item in value]
        if not isinstance(value, dict):
            return value
        result = {}
        for key, child in value.items():
            if key != '$ref':
                result[key] = project(child, current)
                continue
            filename, _, fragment = child.partition('#')
            filename = filename or current
            parts = fragment.lstrip('/').split('/')
            if len(parts) != 2 or parts[0] != '$defs' or filename not in documents:
                raise ValueError('Only maintained exact semantic schema definitions may be projected')
            name = filename.removesuffix('.schema.json').replace('-', '_') + '__' + parts[1]
            if name not in definitions:
                definitions[name] = {}
                definitions[name] = project(documents[filename]['$defs'][parts[1]], filename)
            result[key] = '#/$defs/' + name
        return result
    selected = project(definition, document)
    return {'$schema': 'https://json-schema.org/draft/2020-12/schema', **selected, '$defs': definitions}


def _delivery_resources(session, run, assignment, profile, response_contract, operators,
                        tools, operations):
    """Snapshot exact navigable delivery resources without enlarging domain rights."""
    store, packet = session.store, run.packet
    resources = {}
    def add(label, value, sources=(), procedure=False):
        raw = value if isinstance(value, bytes) else lc.canonical(value)
        identifier = store.put_blob(raw)
        handle = 'resource:' + identifier
        item = {'handle': handle, 'blob_id': identifier, 'label': label,
            'kind': 'procedure' if procedure else 'data', 'source_handles': list(sources),
            'runtime': 'jai.governed-native' if procedure else None,
            'path': str(store.material / identifier), 'byte_length': len(raw)}
        prior = resources.get(handle)
        if prior is None:
            resources[handle] = item
        elif prior['kind'] != item['kind'] or prior['source_handles'] != item['source_handles']:
            # Identical presentation bytes can originate from several entitled
            # records; the manifest retains every actual provenance source.
            prior['source_handles'] = sorted(set(prior['source_handles']) | set(item['source_handles']))
            if prior['kind'] != item['kind']:
                raise ValueError('Presentation resource has conflicting procedural/domain provenance')
        return {'handle': handle, 'path': item['path'], 'byte_length': len(raw)}

    instructions = {}
    categories = {}
    for row in run.execution['snapshot']['catalogue']['roles']:
        detail = add('Complete catalogue record: ' + row['slug'], row, ['catalogue'])
        entry = {key: copy.deepcopy(row[key]) for key in
                 ('slug', 'name', 'aliases', 'tool_tier', 'operator_agent')}
        slug = row['slug']
        instructions[slug] = add('Exact professional instruction: ' + slug,
            run.execution['snapshot']['instructions'][slug]['text'].encode('utf-8'), ['instruction:' + slug])
        entry.update(details=detail, instruction_handle='instruction:' + slug, instruction=instructions[slug])
        categories.setdefault(row['category'], []).append(entry)
    navigation = []
    for category, rows in categories.items():
        pages = [add(category + ' page ' + str(index // 6 + 1),
                     {'category': category, 'roles': rows[index:index + 6]}, ['catalogue'])
                 for index in range(0, len(rows), 6)]
        category_ref = add(category, {'category': category, 'count': len(rows), 'pages': pages}, ['catalogue'])
        navigation.append({'category': category, 'count': len(rows), **category_ref})
    catalogue = add('Complete catalogue navigation', {
        'count': sum(len(rows) for rows in categories.values()), 'categories': navigation,
        'meaning': 'Discovery navigation, not a ranking or permission boundary. '
            'Every full row and instruction remains accessible; read candidate instructions before selection.'}, ['catalogue'])
    record_index, machine_index, business_material = [], [], set()
    for item in packet['manifest']:
        parts = {key: add(item['ref']['logical_id'] + ' /' + key, value, [item['handle']])
                 for key, value in item['record'].items()}
        parts_ref = add(item['ref']['logical_id'] + ' parts', parts, [item['handle']])
        entry = {'handle': item['handle'], 'ref': item['ref'],
            'use_scope': item['use_scope'], 'parts': parts_ref,
            **({'source_role': item['record']['source_role']} if 'source_role' in item['record'] else {})}
        record = item['record']
        business = (('source_role' in record and item['ref'] != assignment['routing']['policy'])
                    or 'product_kind' in record or 'assessment_kind' in record)
        (record_index if business else machine_index).append(entry)
        if business:
            business_material.update(record.get('material', []))
    actual_sources = [item['handle'] for item in packet['manifest']]
    optional_machine = add('Optional exact machine records', {'records': machine_index}, actual_sources)
    material_index = [{**item, 'resource': add('Exact entitled material: ' + item['handle'],
                       store._blob(item['blob_id']), [item['handle']])}
                      for item in packet['attachments'] if item['blob_id'] in business_material]
    def with_material_files(value):
        if isinstance(value, list):
            return [with_material_files(item) for item in value]
        if not isinstance(value, dict):
            return value
        result = {key: with_material_files(child) for key, child in value.items()}
        if value.get('status') == 'available' and 'blob_id' in value:
            result['resource'] = add('Exact entitled returned material', store._blob(value['blob_id']), actual_sources)
        return result
    task = assignment.get('procedure_task')
    mandate = None
    if task is not None:
        owner_record = next((item for item in packet['manifest'] if item['ref'] == task['procedure']), None)
        if owner_record is None:
            raise ValueError('Actual owner task requires its exact entitled procedure record')
        try:
            text = owner_record['record']['message']['payload']['specification']
            for part in task['path'].lstrip('/').split('/'):
                text = text[part.replace('~1', '/').replace('~0', '~')]
        except (KeyError, TypeError):
            raise ValueError('Actual owner task does not resolve in its exact entitled procedure') from None
        if not isinstance(text, str) or not text.strip():
            raise ValueError('Actual owner task must resolve to nonempty authored text')
        mandate = add('Exact owner-authored local task', text.encode('utf-8'), [owner_record['handle']])
    inputs = add('Exact delivered inputs and parts', {
        'records': record_index, 'material': material_index, 'mandate': mandate,
        'owned_returns': [add('Actual owned return ' + str(index), with_material_files(value), actual_sources)
                          for index, value in enumerate(packet.get('owned_returns', []))],
        'current_slots': [add('Actual current slot ' + str(index), value, actual_sources)
                          for index, value in enumerate(packet.get('current_slots', []))],
        'historical_feedback': add('Historical feedback', packet.get('historical_feedback', []), actual_sources),
        'handling': add('Actual handling basis', with_material_files(packet.get('handling')), actual_sources),
        'assessment_basis': add('Exact assessment subject and closure', packet.get('assessment_basis'), actual_sources),
        'rule': 'All already-entitled neighboring parts are available across question labels. '
                'The local producer chooses its dependencies; navigation grants no additional read rights.'}, actual_sources)
    scoped_profile = {'obligations': copy.deepcopy(response_contract['profile_obligations'])}
    constraints = add('Applicable profile constraints', scoped_profile,
        [item['handle'] for item in packet['manifest'] if item['ref'] == assignment['profile']])
    semantic = lc.loads((wire.PACKAGE / 'semantic-return.schema.json').read_bytes())
    decisions = lc.loads((wire.PACKAGE / 'decision.schema.json').read_bytes())
    common = lc.loads((wire.PACKAGE / 'common.schema.json').read_bytes())
    documents = {'semantic-return.schema.json': semantic,
                 'decision.schema.json': decisions, 'common.schema.json': common}
    kind = response_contract['semantic_kind']
    definition = copy.deepcopy(semantic['$defs'][kind])
    if kind == 'selection':
        definition['properties'].pop('previous', None)
        definition['properties']['specialties']['description'] = 'Use exact catalogue row.slug values, never display names.'
        definition['properties']['model_selector']['description'] = 'Copy the exact selector from the chosen provider/workload availability entry.'
    elif kind == 'setter':
        procedure_kind = 'question' if assignment['owner']['work_kind'] == 'question' else 'layer'
        procedure_schema = definition['properties']['procedure']
        procedure_schema['properties'].pop('previous', None)
        procedure_schema['properties']['kind'] = {'const': procedure_kind}
        procedure_schema['properties']['specification'] = {
            '$ref': 'decision.schema.json#/$defs/' + procedure_kind + '_procedure'}
        procedure_schema.pop('allOf', None)
    envelope = {'type': 'object', 'properties': {'format': {'const': 'jai.semantic-return/1'},
        'results': {'type': 'array', 'minItems': 1, 'items': definition}},
        'required': ['format', 'results'], 'additionalProperties': False}
    declarations = add('Closed actual role semantic envelope', _project_schema(envelope, documents), procedure=True)
    procedure_body = {'purpose': response_contract['purpose'], 'mechanics': response_contract['mechanics'],
        'semantic_contract': declarations,
        'required_result_fields': definition['required'],
        'operators': [add('Canonical operator: ' + item['agent'], item['projection'].encode(), procedure=True)
                      for item in operators]}
    if kind != 'selection':
        procedure_body.update(aliases={'assignment': packet['assignment'], 'context': packet['context'],
                'profile': assignment['profile'], 'criteria': assignment['criteria'],
                **({'subject': packet['assessment_basis']['subject']} if packet.get('assessment_basis') else {}),
                **{item['handle']: item['ref'] for item in packet['manifest']}},
            rule='Aliases resolve only in declared reference fields. Free text and JSON material stay unchanged.')
        if kind == 'setter':
            ordinary = {'rework', 'reformulate', 'select', 'invalidate', 'reinstate', 'terminate', 'resolve_escalation'}
            owner_actions = []
            for clause in decisions['oneOf']:
                if clause.get('properties', {}).get('action', {}).get('const') in ordinary:
                    body = copy.deepcopy(clause)
                    body['properties'].pop('authority_proof', None)
                    body['required'] = [name for name in body['required'] if name != 'authority_proof']
                    owner_actions.append(body)
            procedure_body['exceptional_owner_action'] = add('Actual ordinary owner decisions', {
                'result_contract': _project_schema(semantic['$defs']['owner_action'], documents),
                'ordinary_decisions': [_project_schema(body, documents, 'decision.schema.json') for body in owner_actions],
                'rule': 'Use only for an actual permitted owner decision. The same exact member may use kind owner_action; core authority checks remain decisive.'}, procedure=True)
    procedure = add('Actual local responsibility and semantic return', procedure_body, procedure=True)
    workforce_body = {'phase': packet['execution']['phase']}
    if kind == 'selection':
        workforce_body.update(availability=packet['execution'].get('availability', []),
            execution_preference=packet['execution'].get('execution_preference'),
            rule='Choose your actual profession using exact catalogue row.slug values, not name/display labels. '
                'Choose the model from the actual matching active-provider/workload availability entry. '
                'Assess the mandate locally and state the reason for your class/model choice; no automatic difficulty score is supplied. '
                'Profile preferences never waive professional independence requirements, including any domain-specific different-model obligation.')
    else:
        workforce_body.update(selected_specialties=packet['execution']['specialties'],
            selected_instructions=[{'slug': slug, **instructions[slug]} for slug in packet['execution']['specialties']])
    workforce = add('Exact staffing/model availability', workforce_body, ['catalogue'])
    manifest = {'context': packet['context'], 'manifest_hash': packet['manifest_hash'],
                'resources': list(resources.values())}
    manifest_blob = store.put_blob(lc.canonical(manifest))
    state = store.read()
    context = state.resolve(packet['context'], 'context')
    details = state.run_details[packet['run_id']]
    budget = session._budget(state, context, assignment, details)
    budget = {**budget, 'local_budget': {key: budget['local_budget'][key] for key in (
        'phase', 'state', 'iteration', 'reworks_used', 'max_reworks', 'remaining_ms', 'deadline_ms', 'stage')}}
    base = {'context': packet['context'], 'assignment': packet['assignment'],
        'canonical_manifest_hash': packet['manifest_hash'], 'owner': assignment['owner'],
        'responsibility': assignment['responsibility'], 'phase': packet['execution']['phase'],
        'assigned_actor': assignment['assigned_actor'],
        'active_provider': run.execution['model']['execution']['provider'],
        'context_policy': run.execution['snapshot']['models'].get('execution_profile', {}).get('context_policy', 'isolated-handoffs'),
        'operator_agents': [item['agent'] for item in operators],
        'purpose': response_contract['purpose'],
        **({'mandate': response_contract['mandate']} if packet['execution']['phase'] == 'selection' else {}),
        'bounds': {'limits': assignment['limits'], 'deadline_ms': assignment['deadline_ms'],
                   'expires_at_ms': context['expires_at_ms'], **budget,
                   'meaning': 'limits are original ceilings, not a fresh allowance; remaining_ms is shared-budget time as of preparation. Finish before effective_deadline_ms.'},
        'tool_ceiling': tools, 'governed_operations': operations,
        'mandatory': ['Use only exact delivered references and their use scopes.',
            'Preserve inherited L0 requirements; request changes from their owner.',
            'Local entities choose their own specialties and models; reviewers never fix or self-approve.',
            'Return actual work; do not invent evidence, verdicts, native handles or human authority.',
            'Read actual business material through inputs.material resource paths and any exact local mandate. '
                'The optional_machine_index contains host controls, not required business reading.',
            ('Read candidate professional instructions before choosing exact catalogue slugs.' if kind == 'selection'
                else 'Read the selected professional instructions and the actual role semantic contract before work.'),
            'Request resources with existing read(handle); the parent relays actual bytes when native Read is absent.',
            'When Codex exposes no dedicated Read tool, semantic Read may use its read-only execution wrapper '
                'solely to retrieve exact delivered paths. This grants no general shell, mutation, model or '
                'client subprocess, network, or unrelated files authority.',
            'Return the actual semantic envelope or an entitled member broker request; the host encodes structural metadata.',
            'Only the actual tool ceiling and L0 sandbox apply; no Bash or Write permission is inferred.'],
        'resources': {'procedure': procedure, 'inputs': inputs, 'constraints': constraints,
                      'catalogue': catalogue, 'workforce': workforce, 'optional_machine_index': optional_machine},
        'delivery_manifest': 'resource:' + manifest_blob}
    prompt_raw = lc.canonical(base)
    prompt_blob = store.put_blob(prompt_raw)
    return base, prompt_raw.decode('utf-8'), {
        'manifest_blob_id': manifest_blob, 'prompt_blob_id': prompt_blob}


def prepare(session, invocation):
    """Pin one physical call's exact presentation, including singleton calls.

    Args:
        session: Warm native session over the sole authoritative Store.
        invocation: Exact already issued physical invocation identity.
    Returns:
        Durable immutable descriptor with one actual native call intent and each
        logical member's packet/resources. Cold reads restore the same presentation.
    Raises:
        ProtocolError, ValueError, OSError: Current preparation, controls or stored
            resources fail. Preparation never launches a model or grants acceptance.
    """
    state, physical = session._invocation(invocation)
    if physical.get('manifest_blob_id'):
        manifest = lc.loads(session.store._blob(physical['manifest_blob_id']))
        prompt_raw = session.store._blob(manifest['prompt_blob_id'])
        view = lc.loads(prompt_raw)
        delivery = lc.loads(session.store._blob(manifest['delivery_manifest_blob_id']))
        members = []
        for item in manifest['members']:
            member_delivery = next(row for row in delivery['members'] if row['member_key'] == item['member_key'])
            packet = lc.loads(session.store._blob(item['packet_blob_id']))
            members.append({'member_key': item['member_key'], 'context': item['context'],
                'assignment': item['assignment'], 'packet': packet,
                'host_delivery': {key: member_delivery[key] for key in ('manifest_blob_id', 'prompt_blob_id')}})
    else:
        if physical['state'] != 'issued':
            raise lc.ERROR('P_CONTEXT', 'Unpinned physical dispatch requires reconciliation')
        members, deliveries, views, operators = [], [], [], set()
        for member in physical['members']:
            run = session._run(member['context'])
            assignment = state.resolve(member['assignment'], 'assignment')
            profile = state.resolve(assignment['profile'], 'profile')
            execution = run.execution
            contract = _response_contract(run.packet, assignment, profile)
            models = execution['snapshot']['models']
            workload = (execution['snapshot']['descriptor']['bootstrap']['workload_class']
                if execution['phase'] == 'selection' else
                state.resolve(execution['selection'])['message']['payload']['workload_class'])
            projections, tools, operations = _operator_projections(execution,
                assignment['responsibility'], physical['provider'], models, workload)
            operators.update(item['agent'] for item in projections)
            member_view, _, member_delivery = _delivery_resources(session, run, assignment,
                profile, contract, projections, tools, operations)
            packet_blob = session.store.put_blob(lc.canonical(run.packet))
            members.append({'member_key': member['member_key'], 'context': member['context'],
                'assignment': member['assignment'], 'packet': copy.deepcopy(run.packet),
                'packet_blob_id': packet_blob, 'manifest_hash': run.packet['manifest_hash'],
                'host_delivery': member_delivery})
            deliveries.append({'member_key': member['member_key'], **member_delivery})
            views.append({'member': member['member_key'], **{key: member_view[key] for key in (
                'owner', 'responsibility', 'phase', 'purpose', 'bounds', 'tool_ceiling',
                'governed_operations', 'mandatory', 'resources')}})
        kind = 'selection' if physical['phase'] == 'selection' else physical['responsibility']
        semantic = lc.loads((wire.PACKAGE / 'semantic-return.schema.json').read_bytes())
        fields = [name for name in semantic['$defs'][kind]['required'] if name not in {'member', 'kind'}]
        view = {'operator_agents': sorted(operators), 'members': views,
            'context_policy': models.get('execution_profile', {}).get('context_policy', 'isolated-handoffs'),
            'return': {'envelope': {'format': 'jai.semantic-return/1', 'results': [
                {'member': item['member_key'], 'kind': kind} for item in members]},
                'required_result_fields': fields,
                'rule': 'Complete this deliberately incomplete skeleton with your actual required semantic fields. '
                    'Return exactly the top-level keys format and results; never add invocation or invocation_id. '
                    + ('Use specialties from exact catalogue row.slug values, never display labels; use the matching actual model availability entry. '
                       if kind == 'selection' else '') +
                    'Return one actual closed role result per preissued member. '
                    'A batch is one physical context; no member may depend on a future result of another member. '
                    'Member aliases and broker rights remain local. Never invent missing work or PASS.'},
            'requests': {
                'member_key': 'The exact requesting member key',
                'request': 'Existing closed broker request; read(handle), propose, tools and effect ACKs remain governed.'}}
        prompt_raw = lc.canonical(view)
        prompt_blob = session.store.put_blob(prompt_raw)
        delivery_blob = session.store.put_blob(lc.canonical({'invocation_id': invocation, 'members': deliveries}))
        manifest = {key: copy.deepcopy(physical[key]) for key in (
            'invocation_id', 'provider', 'root_generation', 'scope', 'layer', 'responsibility',
            'phase', 'model_controls', 'tool_controls', 'input_union', 'deadline_ms', 'bound_ms')}
        manifest.update(prompt_blob_id=prompt_blob, delivery_manifest_blob_id=delivery_blob,
            members=[{key: item[key] for key in ('member_key', 'context', 'assignment', 'packet_blob_id', 'manifest_hash')}
                     for item in members])
        manifest_blob = session.store.put_blob(lc.canonical(manifest))
        session.workflow.invocation_event(invocation, 'invocation_prepared', manifest_blob_id=manifest_blob)
    provider = physical['provider']
    selected = physical['model_controls']['model']
    selector = physical['model_controls']['model_selector']
    arguments = {'message': prompt_raw.decode('utf-8'), 'fork_turns': 'none',
                 'task_name': _task_name(invocation)} if provider == 'codex' else {
                     **({'agent': view['operator_agents'][0]} if len(view['operator_agents']) == 1
                        else {'agents': view['operator_agents']}), 'prompt': prompt_raw.decode('utf-8')}
    if selector != 'inherit':
        arguments['model'] = selector
    if selected.get('reasoning_effort'):
        arguments['reasoning_effort' if provider == 'codex' else 'effort'] = selected['reasoning_effort']
    observations = []
    if physical['phase'] == 'work':
        for member in members:
            context = state.resolve(member['context'], 'context')
            choice = state.resolve(context['execution']['selection'])['message']['payload']
            execution = session._run(member['context']).execution
            preference = execution['snapshot']['models'].get('execution_profile')
            if preference is not None:
                observations.append({'member': member['member_key'], **execution_profiles.routing_observation(
                    preference, physical['responsibility'], choice['workload_class'], selected)})
    return {'invocation_id': invocation, 'provider': provider, 'members': members,
        'routing_observations': observations,
        'professional_constraint_verification': 'Routing comparison alone does not verify professional constraints or served-model identity.',
        'model_view': view,
        'context_controls': {'worker_history': 'isolated',
            'policy': view.get('context_policy', 'isolated-handoffs'),
            'main_conversation_action': ('request-fresh-task-chat' if view.get('context_policy') == 'task-isolated'
                else 'operator-controlled' if view.get('context_policy') == 'manual' else 'provider-managed-compaction'),
            'main_action_status': 'not performed by preparation; host must execute or report unavailable',
            'author_reviewer_separation': 'required'},
        'host_requirements': ({'claude_effort': 'Load the delivered agent effort field or use a supported per-invocation effort parameter; report unsupported host controls explicitly. Session environment overrides may take precedence.'} if provider == 'claude' and selected.get('reasoning_effort') else {}),
        'host_delivery': {
            'manifest_blob_id': manifest['delivery_manifest_blob_id'], 'prompt_blob_id': manifest['prompt_blob_id']},
        'generic_agent': view['operator_agents'][0] if len(view['operator_agents']) == 1 else None,
        'invocation': {'tool': 'collaboration.spawn_agent' if provider == 'codex' else 'native-agent-intent',
                       'arguments': arguments},
        'model_observation': {'requested': selector, 'reasoning_effort': selected.get('reasoning_effort'),
                              'observed': None},
        'permission_observation': 'Canonical projections and inherited L0 sandbox; no new per-child confinement is claimed.'}


def request_frame(operation, fields):
    """Package exact producer fields with deterministic identity, never semantics.

    Args:
        operation: Existing broker operation.
        fields: Producer-supplied operation fields; propose may use raw bytes as data.
    Returns:
        Closed schema-validated broker frame with content-derived replay identity.
    Raises:
        ProtocolError, ValueError: Unknown or malformed existing operation shape.
    """
    values = copy.deepcopy(fields)
    if operation == 'propose' and isinstance(values.get('data'), bytes):
        values['data'] = base64.b64encode(values['data']).decode('ascii')
    frame = {'operation': operation, **values}
    frame['id'] = 'native:' + hashlib.sha256(lc.canonical(frame)).hexdigest()
    wire.validator('broker-request.schema.json').validate(frame)
    return frame


def producer_return(packet, records, intents):
    """Attach exact context metadata to actual producer records/intents.

    Args:
        packet: Issued packet delivered to this producer.
        records: Actual typed producer proposals, copied without semantic changes.
        intents: Actual typed producer intents including its own review verdicts.
    Returns:
        Schema-validated existing RunReturn; no registration or acceptance occurs.
    Raises:
        ProtocolError: Producer data does not satisfy the existing wire contract.
    """
    value = {'assignment': copy.deepcopy(packet['assignment']),
             'context': copy.deepcopy(packet['context']), 'records': copy.deepcopy(records),
             'intents': copy.deepcopy(intents)}
    wire.validator('run-return.schema.json').validate(value)
    return value
