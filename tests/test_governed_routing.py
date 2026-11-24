# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Global professional availability does not dictate any layer's local staff."""
import copy

import pytest

from governed_fixtures import GovernedHarness, QUESTIONS, lc, routing
import model_router


@pytest.fixture
def captured(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch)
    prepared = host.bootstrap_message()
    source = prepared['payload']['l0_inputs'][-1]['record']
    snapshot = routing.load_policy(source, host.store._blob)
    return host, source, snapshot, host.routing_policy


def _assignment(host, reference, layer=1, question='how', responsibility='author'):
    return {'owner': host.owner(question, layer=layer), 'responsibility': responsibility,
            'routing': {'policy': reference}, 'issued_under': None,
            'effects': [{'operation': name, 'tool_policy': None, 'destination_handle': None}
                        for name in ('read', 'propose')],
            'limits': [{'metric': 'tokens', 'unit': 'governed-token', 'ceiling': 10000}]}


def _choice(reference, specialties):
    return {'action': 'select_execution', 'assignment': reference, 'previous': None, 'specialties': specialties,
            'provider': 'json-process/1', 'workload_class': 'fixture-author',
            'model_selector': 'fixture-author', 'reason': 'Local functional entity chooses its own professionals.',
            'authority_proof': None}


def test_global_catalogue_allows_local_professional_choice_in_all_36_cells(captured, monkeypatch):
    host, _, snapshot, reference = captured
    monkeypatch.setenv('AI_HOUSE_MODEL_CONFIG', '/unavailable/ambient-override.json')
    assert len(snapshot['instructions']) == snapshot['catalogue']['count']
    for layer in range(1, 7):
        for question in QUESTIONS:
            assignment = _assignment(host, reference, layer, question)
            global_policy = routing.validate_assignment(assignment, snapshot, 'host-routing')
            assert 'specialties' not in global_policy
            for specialty in ('software-engineer', 'internal-it-auditor'):
                selected = routing.select_execution(assignment, snapshot, _choice(reference, [specialty]))
                selector, mapping = model_router.resolve_snapshot(snapshot['models'], 'json-process/1', 'fixture-author')
                assert selected['model_selector'] == selector
                assert selected['model'] == mapping
                assert selected['specialties'] == [specialty]
    combined = routing.select_execution(_assignment(host, reference), snapshot,
                                         _choice(reference, ['software-engineer', 'internal-it-auditor']))
    assert combined['allowed_operations'] == ['propose', 'read']


def test_capture_replay_is_deterministic_and_requires_the_full_intrinsic_catalogue(captured):
    host, source, snapshot, _ = captured
    descriptor = snapshot['descriptor']
    assert routing.capture_policy(descriptor['policy_id'],
        host.store._blob(descriptor['catalogue_blob_id']), host.store._blob(descriptor['models_blob_id']),
        {slug: host.store._blob(identifier) for slug, identifier in descriptor['instruction_blobs'].items()},
        descriptor['bootstrap'], descriptor['capabilities'], host.store.put_blob) == source['material']
    assert routing.load_policy(source, host.store._blob) == snapshot
    missing = copy.deepcopy(source)
    missing['material'].remove(descriptor['instruction_blobs']['internal-it-auditor'])
    with pytest.raises(lc.ERROR) as failure:
        routing.load_policy(missing, host.store._blob)
    assert failure.value.code == 'P_PROOF'


def test_global_bounds_and_unknown_capabilities_fail_without_staffing_whitelists(captured):
    host, _, snapshot, reference = captured
    assignment = _assignment(host, reference)
    with pytest.raises(lc.ERROR) as failure:
        routing.validate_assignment(assignment, snapshot, 'another-policy')
    assert failure.value.code == 'P_SCOPE'
    oversized = copy.deepcopy(assignment)
    oversized['limits'][0]['ceiling'] += 1
    with pytest.raises(lc.ERROR) as failure:
        routing.validate_assignment(oversized, snapshot, 'host-routing')
    assert failure.value.code == 'P_BUDGET'
    with pytest.raises(lc.ERROR) as failure:
        routing.select_execution(assignment, snapshot, _choice(reference, ['not-a-catalogue-professional']))
    assert failure.value.code == 'P_PROOF'
    unavailable = _choice(reference, ['software-engineer'])
    unavailable['model_selector'] = 'unavailable-worker'
    with pytest.raises(lc.ERROR) as failure:
        routing.select_execution(assignment, snapshot, unavailable)
    assert failure.value.code == 'P_PROOF'


def _pilot_policy(host, snapshot, work_item, *, exact=False, row_policy=None, procedural=False, deferred=False):
    from pathlib import Path

    import content_workflow
    from content_spec import canonical_hash
    from tools.generate_content_workflows import stage_siem_pilot
    from workflow_role_selection import PROTOCOL
    from tools.compose_role_library import compose

    root = Path(__file__).resolve().parents[1]
    deployment = {'edition': 'synthetic-test-only', 'version': 'fixture-1', 'deployment': 'offline'}
    scopes = host.directory / 'synthetic-product-scopes.json'
    scopes.write_bytes(lc.canonical({key: [deployment] for key in
        ('splunk-enterprise-security', 'ibm-qradar-siem')}))
    registration = stage_siem_pilot(root, scopes)
    registration_path = host.directory / 'staged-siem-workflow.json'
    registration_path.write_bytes(lc.canonical(registration))
    catalogue = content_workflow.load_bindings(root, pilot=registration_path)
    binding = registration['mapping_candidate']
    handoff, path, artifact = binding['handoff'], binding['path'], binding['contract']
    version = artifact['version']
    mappings = binding['mappings']
    if exact:
        row = next(item for item in catalogue['bindings'] if item['handoff_id'] == handoff)
        del row['variant_bindings'][path]['workflow_role_requirement']
        catalogue.pop('catalog_hash')
        catalogue['catalog_hash'] = canonical_hash(catalogue)
    reviewed = {'protocol': PROTOCOL, 'workflow_catalogue': catalogue['catalog_hash'],
                'requirements': [] if exact else [binding]}
    composition = compose(root)
    ancestry = {mapping['slug']: composition.manifest['roles'][mapping['slug']]['ancestry']
                for mapping in mappings}
    policy = {'catalogue': catalogue, 'reviewed': reviewed, 'ancestry': ancestry,
              'contract_versions': {artifact['id']: version}}
    if procedural:
        policy['procedure_scope_protocol'] = routing.PROCEDURE_SCOPE_PROTOCOL
    registry = composition.registry
    bodies = composition.instructions
    descriptor = snapshot['descriptor']
    models = host.store._blob(descriptor['models_blob_id'])
    if row_policy is not None:
        models = lc.canonical({**snapshot['models'], 'sabsa_row_policy': row_policy})
    references = None
    if deferred:
        reference_path = next(name for name in composition.files if name.endswith('/qradar-source-evidence.md'))
        references = {'qradar-siem-specialist': {reference_path.split('/references/', 1)[1]: composition.files[reference_path]}}
    material = routing.capture_policy(descriptor['policy_id'], lc.canonical(registry),
        models, bodies, descriptor['bootstrap'],
        descriptor['capabilities'], host.store.put_blob, workflow_policy=lc.canonical(policy), references=references)
    scope = {'workflow_catalogue': catalogue['catalog_hash'], 'work_item': work_item, 'handoff': handoff,
             'path': path, 'endpoint': 'producer', 'mode': 'exact' if exact else 'compatible-specialization',
             'product_scope': deployment}
    return material, scope, mappings


@pytest.mark.parametrize('product_index', [0, 1])
def test_versioned_workflow_scope_uses_actual_role_selection(captured, product_index):
    host, source, snapshot, policy_ref = captured
    assignment = _assignment(host, policy_ref)
    material, scope, mappings = _pilot_policy(host, snapshot, assignment['owner']['work_item'])
    scope['product_scope']['product'] = mappings[product_index]['product']
    scope_ref = host.ref('workflow-scope', 'source', {'owner': source['owner'],
        'source_role': 'input', 'origin': source['origin'],
        'material': [host.store.put_blob(lc.canonical(scope))], 'criteria': [], 'inherited': []})
    assignment['routing']['workflow_scope'] = scope_ref
    versioned_source = {**source, 'material': material}
    versioned = routing.load_policy(versioned_source, host.store._blob)
    with pytest.raises(lc.ERROR, match='captured workflow policy'):
        routing.validate_assignment(assignment, snapshot, 'host-routing')
    routing.validate_assignment(assignment, versioned, 'host-routing')
    evidence = routing.workflow_eligibility(assignment, versioned, scope, scope_ref)
    slug = mappings[product_index]['slug']
    assert evidence['eligible'] == [slug]
    chosen = routing.select_execution(assignment, versioned, _choice(policy_ref, [slug]),
                                      workflow_selection=evidence)
    assert chosen['specialties'] == [slug]
    assert chosen['workflow_selection']['scope_ref'] == scope_ref
    assert chosen['allowed_operations'] == ['materialize', 'measure', 'propose', 'read']
    for other in (['security-engineer'], [slug, 'security-engineer']):
        with pytest.raises(lc.ERROR, match='One eligible role'):
            routing.select_execution(assignment, versioned, _choice(policy_ref, other),
                                     workflow_selection=evidence)
    with pytest.raises(lc.ERROR, match='exact captured routing policy'):
        routing.workflow_eligibility(assignment, versioned, {**scope, 'work_item': 'different'}, scope_ref)
    with pytest.raises(lc.ERROR, match='cannot fall back'):
        routing.workflow_eligibility(assignment, versioned, {**scope, 'endpoint': 'receiver'}, scope_ref)
    missing = {**versioned_source, 'material': material[:-1]}
    with pytest.raises(lc.ERROR, match='exactly its structural snapshot assets'):
        routing.load_policy(missing, host.store._blob)


def test_native_entry_captures_explicit_workflow_policy_and_references(captured, tmp_path, monkeypatch):
    from pathlib import Path

    import governed_layered
    import governed_native_provider
    from tools.compose_role_library import compose

    host, _, snapshot, _ = captured
    material, scope, mappings = _pilot_policy(host, snapshot, 'backup', deferred=True, procedural=True)
    owner = {'layer': 1, 'work_kind': 'question', 'question': 'how', 'work_item': 'backup'}
    scope['procedure_owner'] = owner
    scope['product_scope']['product'] = mappings[1]['product']
    descriptor = lc.loads(host.store._blob(material[0]))
    policy = host.store._blob(descriptor['workflow_policy_blob_id'])
    root = Path(__file__).resolve().parents[1]
    package = tmp_path / 'package'
    for name, raw in compose(root).files.items():
        output = package / name
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(raw)
    monkeypatch.setattr(governed_native_provider, 'ROOT', package / '.ai/runtime')

    with pytest.raises(lc.ERROR):
        governed_layered.LayeredSession.create(tmp_path / 'invalid', 'invalid', b'Backup evidence.',
            'codex', 'backup', workflow_policy=b'{}')
    assert not (tmp_path / 'invalid/invalid.jsonl').exists()
    with pytest.raises(ValueError, match='checked specialist profile policy'):
        governed_layered.LayeredSession.create(tmp_path / 'unchecked', 'unchecked',
            b'Backup evidence.', 'codex', 'backup', workflow_policy=policy,
            workflow_scopes=[lc.canonical(scope)])
    assert not (tmp_path / 'unchecked/unchecked.jsonl').exists()
    session, created = governed_layered.LayeredSession.create(tmp_path / 'valid', 'valid',
        b'Backup evidence.', 'codex', 'backup', workflow_policy=policy)
    cold = lc.Store(session.store.path, session.store.engagement)
    state = cold.read()
    source = state.resolve(created['inputs']['role-routing'], 'source')
    combined = routing.load_policy(source, cold._blob)
    descriptor = combined['descriptor']
    assert descriptor['protocol'] == routing.CONTEXT_PROTOCOL
    assert cold._blob(descriptor['workflow_policy_blob_id']) == policy
    assert descriptor['reference_blobs']['qradar-siem-specialist']

    references = {slug: {name: cold._blob(identifier) for name, identifier in items.items()}
                  for slug, items in descriptor['reference_blobs'].items()}
    without_workflow = routing.capture_policy(descriptor['policy_id'],
        cold._blob(descriptor['catalogue_blob_id']), cold._blob(descriptor['models_blob_id']),
        {slug: cold._blob(item['blob_id']) for slug, item in combined['instructions'].items()},
        descriptor['bootstrap'], descriptor['capabilities'], cold.put_blob, references=references)
    reference_only = routing.load_policy({**source, 'material': without_workflow}, cold._blob)
    assignment = _assignment(host, host.routing_policy)
    assignment['routing']['workflow_scope'] = created['inputs']['request']
    with pytest.raises(lc.ERROR, match='captured workflow policy'):
        routing.validate_assignment(assignment, reference_only, 'host-routing')


def _enroll_fixture_scope(host, message, work_item, product_index, *, exact=False, owner=None, row_policy=None, product_version=None, deferred=False):
    from governed_fixtures import delivery

    source = next(item['record'] for item in message['payload']['l0_inputs']
                  if item['logical_id'] == 'role-routing')
    old_policy = host.routing_policy
    snapshot = routing.load_policy(source, host.store._blob)
    material, scope, mappings = _pilot_policy(host, snapshot, work_item, exact=exact, row_policy=row_policy, procedural=owner is not None, deferred=deferred)
    source['material'] = material
    mapping = mappings[product_index]
    scope['product_scope']['product'] = mapping['product']
    if product_version is not None:
        scope['product_scope']['version'] = product_version
    logical_id = 'workflow-scope'
    if owner is not None:
        logical_id = routing.procedure_scope_id(owner)
        scope['procedure_owner'] = owner
    fact = {'source_role': 'input', 'owner': source['owner'], 'origin': source['origin'],
            'material': [host.store.put_blob(lc.canonical(scope))], 'criteria': [], 'inherited': []}
    scope_ref = host.ref(logical_id, 'source', fact)
    host.routing_policy = host.ref('role-routing', 'source', source)
    host._remember_proposal(host.routing_policy, 'source', source)
    host._remember_proposal(scope_ref, 'source', fact)
    host.l0_sources = [host.routing_policy if ref == old_policy else ref for ref in host.l0_sources] + [scope_ref]
    message['payload']['l0_inputs'].append({'logical_id': logical_id, 'record': fact})
    message['message_id'] = delivery.message_id(message)
    return scope_ref, 'security-engineer' if exact else mapping['slug']


def test_workflow_choice_is_admitted_once_and_recovered_from_the_actual_journal(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch)
    bootstrap = host.bootstrap_message
    record = host.record
    scope_ref = None
    specialist = None

    def prepare(**kwargs):
        nonlocal scope_ref, specialist
        message = bootstrap(**kwargs)
        scope_ref, specialist = _enroll_fixture_scope(host, message, 'service-controls', 1)
        return message

    def scope_author(logical_id, record_type, body, **kwargs):
        if record_type == 'assignment' and body['responsibility'] == 'author':
            body['routing']['workflow_scope'] = scope_ref
        return record(logical_id, record_type, body, **kwargs)

    monkeypatch.setattr(host, 'bootstrap_message', prepare)
    monkeypatch.setattr(host, 'record', scope_author)
    host.bootstrap()
    actor = host.setup_author(start_author=False)
    assignment = actor['author']
    chooser = host.context('workflow-chooser', assignment, actor['author_record'], phase='selection')
    state = host.store.read()
    eligibility = state.context_execution(state.resolve(chooser, 'context'))['workflow_selection']
    assert eligibility['eligible'] == [specialist]

    rejected = host.message('decision', _choice(assignment, ['security-engineer']),
                            sender=actor['principal'], context=chooser)
    with pytest.raises(AssertionError, match='One eligible role'):
        host.commit(rejected)
    accepted = host.message('decision', _choice(assignment, [specialist]),
                            sender=actor['principal'], context=chooser)
    receipt = host.commit(accepted)
    state = host.store.read()
    selected = next(ref for ref in receipt['created_versions']
                    if state.versions[ref['version_id']]['kind'] == 'delivery.decision')
    context = host.context('workflow-work', assignment, actor['author_record'], selection=selected, start=False)
    cold = lc.Store(host.store.path, host.store.engagement).read()
    execution = cold.context_execution(cold.resolve(context, 'context'))
    assert execution['specialties'] == [specialist]
    assert execution['workflow_selection'] == eligibility
    assert execution['selection'] == selected


@pytest.mark.parametrize('target', ['one-platform', 'another-platform', None])
def test_classified_sections_project_exact_instruction_and_broker_reads(captured, target):
    """Capture one role and keep its text and broker handles scoped together."""
    import hashlib

    host, source, snapshot, reference = captured
    descriptor = snapshot['descriptor']
    slug = 'software-engineer'
    instructions = {name: host.store._blob(identifier)
                    for name, identifier in descriptor['instruction_blobs'].items()}
    base = instructions[slug]
    sections, references = [], {}
    raw = base
    for name in ('one-platform', 'another-platform'):
        path = f'knowledge/example/{name}.md'
        section = f'\n{name} setup: ({path})\n'.encode()
        sections.append({'id': name, 'scope': {'task': [name]}, 'reference': path,
                         'start': len(raw), 'end': len(raw) + len(section),
                         'sha256': hashlib.sha256(section).hexdigest()})
        references[path] = f'Details for {name}'.encode()
        raw += section
    instructions[slug] = raw
    source = {**source, 'material': routing.capture_policy(
        descriptor['policy_id'], host.store._blob(descriptor['catalogue_blob_id']),
        host.store._blob(descriptor['models_blob_id']), instructions, descriptor['bootstrap'],
        descriptor['capabilities'], host.store.put_blob, references={slug: references},
        context_sections={slug: sections})}
    scoped = routing.load_policy(source, host.store._blob)
    assignment = _assignment(host, reference)
    workflow = None
    if target:
        assignment['routing']['workflow_scope'] = reference
        workflow = {'eligible': [slug], 'binding': {'path': target}, 'scope_ref': reference}
    execution = routing.select_execution(assignment, scoped, _choice(reference, [slug]),
                                         workflow_selection=workflow)
    execution.update(phase='work', snapshot=scoped)
    instruction, = execution['instructions']
    for name in ('one-platform', 'another-platform'):
        assert (name in instruction['text']) == (name == target)
    handles = routing.deferred_reference_handles(execution)
    assert set(handles) == ({f'role-reference:{slug}:knowledge/example/{target}.md'} if target else set())
    broker = routing.instruction_handles(execution, host.store.put_blob)
    assert broker == {f'instruction:{slug}': instruction['blob_id']}
    assert host.store._blob(instruction['blob_id']) == instruction['text'].encode()
    assert routing.load_policy(source, host.store._blob) == scoped


def test_attributable_workflow_scope_validates_knowledge_dimensions(captured):
    """Bind knowledge selectors to the same versioned workflow input as staffing."""
    import hashlib

    host, source, snapshot, policy_ref = captured
    assignment = _assignment(host, policy_ref)
    material, scope, mappings = _pilot_policy(host, snapshot, assignment['owner']['work_item'])
    catalogue = routing.load_policy({**source, 'material': material}, host.store._blob)
    slug = mappings[0]['slug']
    scope['product_scope']['product'] = mappings[0]['product']
    scope['knowledge_scope'] = {'provider': ['new-platform'], 'product': [mappings[0]['product']],
                                'activity': ['java-api-documentation']}
    descriptor = catalogue['descriptor']
    bodies = {name: host.store._blob(identifier) for name, identifier in descriptor['instruction_blobs'].items()}
    block = b'\nFixture-specific knowledge.\n'
    start = len(bodies[slug])
    bodies[slug] += block
    sections = {slug: [{
        'id': 'fixture/knowledge',
        'scope': {'provider': ['new-platform'], 'activity': ['java-api-documentation']},
        'reference': None,
        'start': start, 'end': start + len(block), 'sha256': hashlib.sha256(block).hexdigest(),
    }]}
    scoped_material = routing.capture_policy(
        descriptor['policy_id'], host.store._blob(descriptor['catalogue_blob_id']),
        host.store._blob(descriptor['models_blob_id']), bodies, descriptor['bootstrap'],
        descriptor['capabilities'], host.store.put_blob,
        workflow_policy=host.store._blob(descriptor['workflow_policy_blob_id']), context_sections=sections)
    scoped = routing.load_policy({**source, 'material': scoped_material}, host.store._blob)
    scope_ref = host.ref('workflow-scope', 'source', {'owner': source['owner'],
        'source_role': 'input', 'origin': source['origin'],
        'material': [host.store.put_blob(lc.canonical(scope))], 'criteria': [], 'inherited': []})
    assignment['routing']['workflow_scope'] = scope_ref
    evidence = routing.workflow_eligibility(assignment, scoped, scope, scope_ref)
    choice = routing.select_execution(assignment, scoped, _choice(policy_ref, [slug]),
                                      workflow_selection=evidence)
    assert block in choice['instructions'][0]['text'].encode()
    conflict = {**scope, 'knowledge_scope': {'product': ['another-product']}}
    with pytest.raises(lc.ERROR, match='contradicts the governing workflow scope'):
        routing.workflow_eligibility(assignment, scoped, conflict, scope_ref)

    legacy_mixed = {**scope, 'knowledge_scope': {'provider': ['new-platform', 'other-platform']}}
    with pytest.raises(lc.ERROR, match='one product and provider'):
        routing.workflow_eligibility(assignment, scoped, legacy_mixed, scope_ref)
    separated = {key: value for key, value in scope.items() if key != 'knowledge_scope'}
    separated['knowledge_targets'] = [
        {'provider': ['new-platform']},
        {'provider': ['other-platform'], 'effects': ['java-public-api-change']},
    ]
    decision = routing.workflow_eligibility(assignment, scoped, separated, scope_ref)
    choice = routing.select_execution(assignment, scoped, _choice(policy_ref, [slug]),
                                      workflow_selection=decision)
    assert block not in choice['instructions'][0]['text'].encode()
    separated['knowledge_targets'][0]['effects'] = ['java-public-api-change']
    decision = routing.workflow_eligibility(assignment, scoped, separated, scope_ref)
    assert decision['binding']['knowledge_targets'][0]['activity'] == ['java-api-documentation']
    choice = routing.select_execution(assignment, scoped, _choice(policy_ref, [slug]),
                                      workflow_selection=decision)
    assert block in choice['instructions'][0]['text'].encode()


@pytest.mark.parametrize('target', ['aws', 'azure', 'google-cloud'])
def test_classified_cloud_delivery_keeps_only_the_chosen_vendor(captured, target):
    """Project the real installed supplement and its common reference for one vendor."""
    import json
    from pathlib import Path

    host, source, snapshot, reference = captured
    root = Path(__file__).resolve().parents[1] / '.ai'
    guidance = json.loads((root / 'runtime/knowledge/infrastructure-role-guidance.json').read_bytes())
    slug = 'ci-cd-platform-engineer'
    overlay = next(entry for path, entry in guidance['roles'].items() if path.endswith(f'/{slug}.md'))
    descriptor = snapshot['descriptor']
    instructions = {name: host.store._blob(identifier)
                    for name, identifier in descriptor['instruction_blobs'].items()}
    instructions[slug] += overlay['supplement'].encode()
    folder = next(path.rsplit('/', 1)[0] for path in guidance['roles'] if path.endswith(f'/{slug}.md'))
    references = {name: guidance['references'][f'{folder}/{name}'].encode() for name in overlay['references']}
    material = routing.capture_policy(
        descriptor['policy_id'], host.store._blob(descriptor['catalogue_blob_id']),
        host.store._blob(descriptor['models_blob_id']), instructions, descriptor['bootstrap'],
        descriptor['capabilities'], host.store.put_blob, references={slug: references},
        context_sections={slug: overlay['context_sections']})
    policy = routing.load_policy({**source, 'material': material}, host.store._blob)
    assignment = _assignment(host, reference)
    assignment['routing']['workflow_scope'] = reference
    workflow = {'eligible': [slug], 'binding': {'path': f'normal/{target}'}, 'scope_ref': reference}
    execution = routing.select_execution(assignment, policy, _choice(reference, [slug]),
                                         workflow_selection=workflow)
    execution.update(phase='work', snapshot=policy)
    instruction, = execution['instructions']
    vendors = {'aws': 'AWS', 'azure': 'Azure', 'google-cloud': 'Google Cloud'}
    for key, label in vendors.items():
        assert (label in instruction['text']) == (key == target)
    handles = routing.deferred_reference_handles(execution)
    assert {handle.rsplit('/', 1)[1] for handle in handles} == {
        'delivery-pipelines.md', f'delivery-pipelines-{target}.md'}
    shared_handle = next(handle for handle in handles if handle.endswith('/delivery-pipelines.md'))
    shared = host.store._blob(handles[shared_handle]).decode()
    assert all(vendor not in shared for vendor in vendors.values())
    specific_handle = next(handle for handle in handles if handle.endswith(f'/delivery-pipelines-{target}.md'))
    specific = host.store._blob(handles[specific_handle]).decode()
    assert vendors[target] in specific
    assert all(label not in specific for key, label in vendors.items() if key != target)

    standalone_assignment = _assignment(host, reference)
    standalone_ref = {**reference,
                      'logical_id': routing.question_knowledge_scope_id(standalone_assignment['owner'])}
    standalone = {'owner': standalone_assignment['owner'],
                  'knowledge_targets': [{'task': [f'normal/{target}']}]}
    scope = routing.standalone_knowledge_scope(standalone_assignment['owner'], standalone, standalone_ref, policy)
    projected = routing.select_execution(standalone_assignment, policy, _choice(reference, [slug]),
                                         knowledge_scope=scope)
    projected.update(phase='work', snapshot=policy)
    assert projected['instructions'] == execution['instructions']
    assert routing.deferred_reference_handles(projected) == handles
    assert 'workflow_selection' not in projected
    standalone['knowledge_targets'] = [{'task': ['normal/unknown-platform']}]
    with pytest.raises(lc.ERROR, match='exact normalized dimensions'):
        routing.standalone_knowledge_scope(standalone_assignment['owner'], standalone, standalone_ref, policy)
