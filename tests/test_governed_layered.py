# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Layered front-door ingress and resume preserve the existing governed facts."""
import copy
import base64
import io
import json
from pathlib import Path
import sys
import time

import pytest
from test_governed_native_session import prepared

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import governed_layered as layered
import governed_native_provider as producer
import lifecycle as lc


def _start(tmp_path, **overrides):
    values = {'home': tmp_path / '.fabric', 'engagement': 'service',
        'task': b'Explain who can update an internal incident-status service.',
        'provider_name': 'codex', 'work_item': 'incident-status',
        'deadline_ms': int(time.time() * 1000) + 180000, 'limit_ms': 60000}
    values.update(overrides)
    return layered.LayeredSession.create(**values)


def test_verbatim_intent_defaults_to_same_criteria_and_next_exposes_unbound_uncertainty(tmp_path):
    session, created = _start(tmp_path)
    state = session.store.read()
    request = state.resolve(created['inputs']['request'], 'source')
    criteria = state.resolve(created['inputs']['criteria'], 'source')
    assert session.store._blob(request['material'][0]) == session.store._blob(criteria['material'][0])
    assert created['criteria_basis'] == 'same-verbatim-request'
    first = session.next()
    assert first['status'] == 'invoke'
    assert first['prepared']['members'][0]['packet']['execution']['phase'] == 'selection'
    prepared = session.prepare(first['invocation_id'])
    view = prepared['model_view']['members'][0]
    inputs = _resource_json(session, view['resources']['inputs'])
    assert {item['ref']['version_id'] for item in inputs['records']} == {
        created['inputs']['request']['version_id'], created['inputs']['criteria']['version_id']}
    head = session.store.read().head
    again = session.next()
    assert again['status'] == 'reconcile'
    assert again['members'][0]['context'] == first['members'][0]['context']
    assert again['task_name'] == first['prepared']['invocation']['arguments']['task_name']
    assert session.store.read().head == head
    checkpoint = session.checkpoint()
    assert checkpoint['inflight'][0]['context'] == first['members'][0]['context']
    assert checkpoint['inflight'][0]['native'] is None
    assert checkpoint['inflight'][0]['pending_effects'] == []
    assert 'readiness' not in json.loads(Path(created['locator']).read_bytes())


def test_cold_resume_retains_exact_context_and_head_without_new_input_or_execution(tmp_path):
    session, created = _start(tmp_path, criteria=b'Attribute every update to its individual operator.')
    issued = session.next()
    before = session.checkpoint()
    resumed = layered.LayeredSession.open(created['locator'])
    after = resumed.checkpoint()
    assert after['head'] == before['head']
    assert after['inputs'] == before['inputs']
    assert after['inflight'] == before['inflight']
    assert resumed.next()['members'][0]['context'] == issued['members'][0]['context']
    assert resumed.store.read().head == before['head']
    with pytest.raises(ValueError, match='requires resume'):
        _start(tmp_path)


def test_pinned_enrollment_drift_denies_but_explicit_new_input_gets_distinct_locator(tmp_path):
    session, created = _start(tmp_path)
    locator = json.loads(Path(created['locator']).read_bytes())
    config_path = Path(locator['host_config'])
    original = json.loads(config_path.read_bytes())
    changed = copy.deepcopy(original)
    changed['limits']['packet_bytes'] += 1024
    config_path.write_bytes(lc.canonical(changed))
    with pytest.raises(ValueError, match='Pinned host enrollment changed'):
        layered.LayeredSession.open(created['locator'])
    resumed = layered.LayeredSession.open(created['locator'], config=changed)
    assert resumed.locator != Path(created['locator'])
    assert resumed.store.read().head == session.store.read().head
    new_locator = json.loads(resumed.locator.read_bytes())
    assert new_locator['host_config_digest'] != locator['host_config_digest']
    assert Path(new_locator['journal']).name == 'service.jsonl'


def test_uncommitted_invalid_start_can_take_explicit_new_enrollment_without_history_replacement(tmp_path):
    with pytest.raises(ValueError, match='nonempty'):
        _start(tmp_path, task=b'')
    original_locator = tmp_path / '.fabric/service.session.json'
    assert original_locator.exists()
    original = json.loads(original_locator.read_bytes())
    config = json.loads(Path(original['host_config']).read_bytes())
    config['limits']['packet_bytes'] += 1024
    session, created = _start(tmp_path, config=config)
    assert Path(created['locator']) != original_locator
    assert session.store.read().initialized
    assert json.loads(Path(created['locator']).read_bytes())['journal'] == original['journal']


def test_invalid_external_gateway_requests_do_not_create_mandates_or_complete_a_layer(tmp_path):
    session, created = _start(tmp_path)
    point = {'ref': created['inputs']['request'], 'use_scope': 'default'}
    head = session.store.read().head
    with pytest.raises((ValueError, KeyError)):
        session.local_entry(point, 'receiver')
    with pytest.raises((ValueError, KeyError)):
        session.handling_entry(point['ref'], 'resolve')
    assert session.output_status(point)['complete_layer'] is False
    assert session.store.read().head == head


def test_keyless_dossier_is_readable_and_never_invents_a_human_signer(tmp_path, monkeypatch):
    session, _ = _start(tmp_path)
    monkeypatch.setattr(layered.operator, 'trusted_key', lambda *args: (_ for _ in ()).throw(ValueError('not enrolled')))
    dossier = session.human_handoff(None)
    assert dossier['episodes'] == []
    assert dossier['authority_granted'] is False
    proposed = session.prepare_human({'action': 'terminate', 'reason': 'Operator choice required',
        'subjects': dossier['checkpoint']['roots'], 'authority_proof': None}, 'delivery-change')
    assert proposed['status'] == 'unavailable'
    assert proposed['message'] is None and proposed['request'] is None
    assert proposed['required_purpose'] == 'delivery-change'
    assert proposed['authority_granted'] is False


def _working(session):
    issued = session.next()
    packet = issued['prepared']['members'][0]['packet']
    model = next(item['model_selector'] for item in packet['execution']['availability']
                 if item['provider'] == 'codex' and item['workload_class'] == 'standard')
    session.start(issued['invocation_id'], 'codex', 'fixture-choice', {'fixture': 'controlled native observation'})
    value = {'format': 'jai.semantic-return/1', 'results': [{
        'member': packet['member_key'], 'kind': 'selection', 'specialties': ['software-engineer'],
        'provider': 'codex', 'workload_class': 'standard', 'model_selector': model,
        'reason': 'Controlled mechanics fixture, not native professional evidence.'}]}
    session.complete(issued['invocation_id'], json.dumps(value), {'fixture': True})
    return session.next()


def _resource_json(session, reference):
    """Inspect a prepared immutable presentation resource without a worker claim."""
    return lc.loads(session.store._blob(reference['handle'].removeprefix('resource:')))


def test_small_delivery_retains_every_catalogue_role_and_scoped_inputs(tmp_path):
    session, created = _start(tmp_path)
    issued = session.next()
    prepared_view = issued['prepared']
    packet = copy.deepcopy(issued['prepared']['members'][0]['packet'])
    base = prepared_view['model_view']['members'][0]
    assert len(prepared_view['invocation']['arguments']['message'].encode()) < 8192
    assert prepared_view['members'][0]['packet'] == packet
    assignment = session.store.read().resolve(packet['assignment'])
    assert base['responsibility'] == 'setter' and base['owner']['work_kind'] == 'integration'
    assert base['phase'] == 'selection'
    assert base['purpose'] == producer._response_contract(packet, assignment,
        session.store.read().resolve(assignment['profile']))['purpose']
    assert base['bounds']['limits'] == assignment['limits']
    assert base['bounds']['deadline_ms'] == assignment['deadline_ms']
    inputs = _resource_json(session, base['resources']['inputs'])
    assert {item['ref']['version_id'] for item in inputs['records']} == {
        created['inputs']['request']['version_id'], created['inputs']['criteria']['version_id']}
    machine = _resource_json(session, base['resources']['optional_machine_index'])
    assert {(item['ref']['version_id'], item['use_scope']) for item in [*inputs['records'], *machine['records']]} == {
        (item['ref']['version_id'], item['use_scope']) for item in packet['manifest']}
    assert {item['source_role'] for item in inputs['records'] if 'source_role' in item} >= {'input', 'criteria'}
    originals = {item['ref']['version_id']: item['record'] for item in packet['manifest']}
    for item in [*inputs['records'], *machine['records']]:
        parts = _resource_json(session, item['parts'])
        assert {name: _resource_json(session, reference) for name, reference in parts.items()} == originals[item['ref']['version_id']]
    catalogue = _resource_json(session, base['resources']['catalogue'])
    rows = []
    for category in catalogue['categories']:
        for page in _resource_json(session, category)['pages']:
            for row in _resource_json(session, page)['roles']:
                rows.append(_resource_json(session, row['details']))
                assert row['instruction_handle'] == 'instruction:' + row['slug']
    assert len(rows) == catalogue['count'] == 286
    captured = session._run(issued['members'][0]['context']).execution['snapshot']['catalogue']['roles']
    assert {row['slug']: row for row in rows} == {row['slug']: row for row in captured}
    capture = {'provider_observation': {'fixture': 'actual controlled handle'},
               'host_delivery': prepared_view['host_delivery']}
    session.start(issued['invocation_id'], 'codex', 'resource-reader', capture)
    result = session.request(issued['invocation_id'], issued['members'][0]['member_key'], {
        'id': 'catalogue-navigation', 'operation': 'read',
        'handle': base['resources']['catalogue']['handle']})['result']
    assert lc.loads(base64.b64decode(result['data'])) == catalogue
    unknown = session.store.put_blob(b'Not an entitled input merely because it exists.')
    with pytest.raises((ValueError, lc.ERROR)):
        session.request(issued['invocation_id'], issued['members'][0]['member_key'], {
            'id': 'unknown-resource', 'operation': 'read', 'handle': 'resource:' + unknown})
    facts = session.store.read()._native_packet_facts[packet['run_id']]
    assert unknown not in facts['allowed_blobs']


def test_delivery_binding_rejects_unentitled_resource_without_advancing_history(tmp_path, monkeypatch):
    session, created = _start(tmp_path)
    issued = session.issue_batch([{'assignment': created['entry']['assignment'], 'phase': 'selection'}])
    invocation = issued['invocation_id']
    proposal = {}
    with monkeypatch.context() as patch:
        def retain_preparation(identifier, event, **payload):
            assert identifier == invocation and event == 'invocation_prepared'
            proposal.update(payload)
            return {'status': 'proposal-only'}
        patch.setattr(session.workflow, 'invocation_event', retain_preparation)
        descriptor = session.prepare(invocation)
    original = lc.loads(session.store._blob(proposal['manifest_blob_id']))
    global_delivery = lc.loads(session.store._blob(original['delivery_manifest_blob_id']))
    member_delivery = global_delivery['members'][0]
    original_member = lc.loads(session.store._blob(member_delivery['manifest_blob_id']))
    packet = descriptor['members'][0]['packet']
    head = session.store.read().head
    for field in ('source_handles', 'context', 'manifest_hash'):
        changed_member = copy.deepcopy(original_member)
        if field == 'source_handles':
            next(item for item in changed_member['resources'] if item['kind'] == 'data')['source_handles'] = ['record:not-delivered']
        elif field == 'context':
            changed_member['context'] = {**packet['context'], 'logical_id': 'another-context'}
        else:
            changed_member['manifest_hash'] = '0' * 64
        changed_delivery = copy.deepcopy(global_delivery)
        changed_delivery['members'][0]['manifest_blob_id'] = session.store.put_blob(lc.canonical(changed_member))
        view = lc.loads(session.store._blob(member_delivery['prompt_blob_id']))
        view['delivery_manifest'] = 'resource:' + changed_delivery['members'][0]['manifest_blob_id']
        changed_delivery['members'][0]['prompt_blob_id'] = session.store.put_blob(lc.canonical(view))
        changed = {**original, 'delivery_manifest_blob_id': session.store.put_blob(lc.canonical(changed_delivery))}
        with pytest.raises(ValueError):
            session.workflow.invocation_event(invocation, 'invocation_prepared',
                manifest_blob_id=session.store.put_blob(lc.canonical(changed)))
        assert session.store.read().head == head
        assert session.status(invocation)['state'] == 'issued'
    session.workflow.invocation_event(invocation, 'invocation_prepared', **proposal)
    session.start(invocation, 'codex', 'valid-after-rejections', {'fixture': 'Actual controlled observation.'})
    facts = session.store.read()._native_packet_facts[packet['run_id']]
    assert facts['host_delivery'] == {key: member_delivery[key] for key in ('manifest_blob_id', 'prompt_blob_id')}
    reference = descriptor['model_view']['members'][0]['resources']['inputs']
    result = session.request(invocation, issued['members'][0]['member_key'], {
        'id': 'valid-after-rejections-read', 'operation': 'read', 'handle': reference['handle']})['result']
    assert base64.b64decode(result['data']) == session.store._blob(reference['handle'].removeprefix('resource:'))


def test_bound_resume_uses_original_delivery_bytes_without_current_renderer(tmp_path, monkeypatch):
    session, created = _start(tmp_path)
    issued = session.next()
    original = issued['prepared']
    observed = {'handle': 'original-platform-observation', 'nested': {'unchanged': True}}
    session.start(issued['invocation_id'], 'codex', 'pinned-view', observed)
    def unavailable(*args, **kwargs):
        raise AssertionError('Historical delivery must not use current rendering or operator files')
    monkeypatch.setattr(producer, '_delivery_resources', unavailable)
    monkeypatch.setattr(producer, '_operator_projections', unavailable)
    resumed = layered.LayeredSession.open(created['locator'])
    restored = resumed.prepare(issued['invocation_id'])
    assert restored['invocation'] == original['invocation']
    assert restored['host_delivery'] == original['host_delivery']
    assert restored['members'][0]['packet'] == original['members'][0]['packet']
    reference = original['model_view']['members'][0]['resources']['inputs']
    result = resumed.request(issued['invocation_id'], issued['members'][0]['member_key'], {
        'id': 'original-input-index', 'operation': 'read', 'handle': reference['handle']})['result']
    assert base64.b64decode(result['data']) == session.store._blob(reference['handle'].removeprefix('resource:'))
    native = resumed.store.read().run_details[issued['prepared']['members'][0]['packet']['run_id']]['native']
    assert lc.loads(resumed.store._blob(native['capture_blob_id']))['provider_observation'] == observed


def test_work_view_reports_consumed_selection_budget_and_original_deadline(tmp_path, monkeypatch):
    clock = [time.time()]
    monkeypatch.setattr(time, 'time', lambda: clock[0])
    session, created = _start(tmp_path)
    original_complete = session.complete
    def consume_selection(*args, **kwargs):
        clock[0] += 12
        return original_complete(*args, **kwargs)
    monkeypatch.setattr(session, 'complete', consume_selection)
    issued = _working(session)
    bounds = issued['prepared']['model_view']['members'][0]['bounds']
    assert bounds['limits'] == [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 60000}]
    assert next(value for value in session.store.read().invocations.values()
                if value['state'] == 'returned')['usage']['elapsed_ms:ms'] == 12000
    assert bounds['context_limits'] == [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 48000}]
    assert bounds['current_elapsed_ms'] == 0
    assert bounds['remaining_ms'] == 48000
    assert bounds['effective_deadline_ms'] == bounds['as_of_ms'] + 48000
    assert bounds['effective_deadline_ms'] <= bounds['deadline_ms']
    state = session.store.read()
    details = state.run_details[issued['prepared']['members'][0]['packet']['run_id']]
    context = state.resolve(issued['members'][0]['context'])
    assignment = state.resolve(issued['prepared']['members'][0]['packet']['assignment'])
    assert session._budget(state, context, assignment, details)['remaining_ms'] == bounds['remaining_ms']
    session.start(issued['invocation_id'], 'codex', 'truthful-budget', {
        'provider_observation': {'fixture': 'controlled clock'},
        'host_delivery': issued['prepared']['host_delivery']})
    clock[0] += 3
    resumed = layered.LayeredSession.open(created['locator'])
    assert resumed.prepare(issued['invocation_id'])['model_view']['members'][0]['bounds'] == bounds


def test_gateway_criteria_and_six_local_setter_mandates_admit_through_native_return(tmp_path):
    session, created = _start(tmp_path)
    offered = _working(session)
    packet = offered['prepared']['members'][0]['packet']
    parent = session.store.read().resolve(packet['assignment'], 'assignment')
    session.start(offered['invocation_id'], 'codex', 'gateway-fixture', {'fixture': 'Controlled actual owner.'})
    semantic = {'member': packet['member_key'], 'kind': 'setter', 'logical_id': 'gateway-local-criteria',
        'materials': [{'text': 'Identify the authorized updater and explicitly report unknowns.'}],
        'criteria': [{'id': 'C1', 'requirement': created['inputs']['request'],
            'statement': 'Identify the authorized updater and unresolved requirements.', 'evidence_slots': []}],
        'inherited': parent['inherited'], 'procedure': {'kind': 'layer',
            'reason': 'Actual controlled local owner procedure.', 'specification': {
                'framing': 'Define accountability for the incident-status service.',
                'question_tasks': {question: 'Resolve ' + question + ' for this service.' for question in producer.QUESTIONS},
                'integration_task': 'Integrate the six actual answers.',
                'review_task': 'Review their integration.', 'interface_criterion': 'C1'}}}
    result = session.complete(offered['invocation_id'],
        json.dumps({'format': 'jai.semantic-return/1', 'results': [semantic]}), {'fixture': 'Actual controlled return.'})
    assert result['status'] == 'returned'
    state = session.store.read()
    procedure = state.procedures[(packet['assignment']['version_id'], 'default')]
    criteria_ref = state.resolve(procedure)['message']['payload']['criteria']
    assert state.resolve(criteria_ref)['source_role'] == 'criteria'
    assert state.resolve(criteria_ref)['owner'] == parent['owner']
    children = []
    for _ in producer.QUESTIONS:
        completed = session.workflow.advance(procedure)
        children.extend(completed['completion']['receipt']['created_versions'])
    state = session.store.read()
    children = [ref for ref in children if state.versions[ref['version_id']]['kind'] == 'delivery.assignment']
    assert len(children) == 6
    for child in children:
        record = state.resolve(child)
        assert record['criteria'] == criteria_ref
        assert record['issued_under'] == packet['assignment']
        assert record['owner']['question'] in producer.QUESTIONS
        assert state.provenance[child['version_id']]['origin']['kind'] == 'controller'
    assert {item['assignment']['version_id'] for item in session.workflow.ready() if item['ready']} >= {
        child['version_id'] for child in children}
    assert not any(value['kind'] in {'delivery.product', 'delivery.assessment'} for value in state.versions.values())


def test_neighbor_part_navigation_is_lossless_across_question_labels(tmp_path):
    parts = {'interface_parts': {'why': {'requirements': ['Preserve the rationale.']},
                                'where': {'constraints': ['Preserve the deployment boundary.']}}}
    task = lc.canonical(parts)
    session, created = _start(tmp_path, task=task)
    offered = session.next()
    view = offered['prepared']['model_view']['members'][0]
    inputs = _resource_json(session, view['resources']['inputs'])
    material = next(item for item in inputs['material'] if item['blob_id'] == lc.blob(task))
    session.start(offered['invocation_id'], 'codex', 'neighbor-resource-reader', {'fixture': 'Controlled actual observation.'})
    returned = session.request(offered['invocation_id'], offered['members'][0]['member_key'],
        {'id': 'neighbor-parts', 'operation': 'read', 'handle': material['handle']})['result']
    assert lc.loads(base64.b64decode(returned['data'])) == parts
    request = session.store.read().resolve(created['inputs']['request'], 'source')
    assert request['material'] == [lc.blob(task)]


def test_producer_stencil_preserves_explicit_content_and_rejects_conflicting_metadata(tmp_path):
    session, created = _start(tmp_path)
    issued = _working(session)
    request_ref = created['inputs']['request']
    material = session.store.read().resolve(request_ref)['material']
    fields = {'source_role': 'assumption', 'material': material,
              'criteria': [], 'inherited': [request_ref]}
    proposal = session.stencil(issued['members'][0]['context'], 'source', 'actual-producer-source', fields, [])
    assert proposal['record']['source_role'] == fields['source_role']
    assert proposal['record']['material'] == material
    assert proposal['record']['origin'] == {'kind': 'assignment', 'ref': issued['prepared']['members'][0]['packet']['assignment']}
    assert 'owner' not in fields
    with pytest.raises(ValueError, match='Conflicting structural metadata'):
        session.stencil(issued['members'][0]['context'], 'source', 'wrong-owner',
            {**fields, 'owner': {'kind': 'authority', 'id': 'invented-human'}}, [])
    with pytest.raises(ValueError):
        session.stencil(issued['members'][0]['context'], 'source', 'invented-verdict', {**fields, 'verdict': 'supported'}, [])
    with pytest.raises(ValueError):
        session.stencil(issued['members'][0]['context'], 'source', 'missing-content', {}, [])


def test_unbound_expired_context_can_cancel_without_native_identity_or_new_permissions(tmp_path, monkeypatch):
    session, _ = _start(tmp_path)
    issued = session.next()
    context = issued['members'][0]['context']
    before = session.store.read().resolve(context, 'context')
    bound, _ = _start(tmp_path / 'bound')
    bound_issued = bound.next()
    bound.start(bound_issued['invocation_id'], 'codex', 'actual-bound-handle', {'fixture': 'Actual controlled handle.'})
    bound.stop(bound_issued['invocation_id'], {'state': 'not-dispatched', 'observed': 'Cannot erase an actual running handle.'})
    assert bound.status(bound_issued['invocation_id'])['state'] == 'uncertain'
    assert bound.store.read().native_handles
    stamp = time.time()
    monkeypatch.setattr(layered.time, 'time', lambda: stamp + 3600)
    assert session.next()['members'][0]['context'] == context
    session.stop(issued['invocation_id'], {'state': 'not-dispatched', 'observed': 'Actual controlled host lookup found no dispatch.'})
    state = session.store.read()
    assert state.run_states[before['run_id']] == 'cancelled'
    assert state.resolve(context, 'context')['expires_at_ms'] == before['expires_at_ms']
    assert not state.native_handles
    with pytest.raises(ValueError):
        session.start(issued['invocation_id'], 'codex', 'late-unconfirmed-agent', {'late': True})


def test_resume_finishes_interrupted_initial_entry_from_the_actual_bootstrap(tmp_path, monkeypatch):
    with monkeypatch.context() as patch:
        def interrupted(*args, **kwargs):
            raise RuntimeError('Interrupted after committed inputs, before structural entry')
        patch.setattr(layered.native.governed_workflow.Workflow, 'entry', interrupted)
        with pytest.raises(RuntimeError, match='Interrupted after committed inputs'):
            _start(tmp_path)
    locator = tmp_path / '.fabric/service.session.json'
    resumed = layered.LayeredSession.open(locator)
    roots = resumed.checkpoint()['roots']
    assert len(roots) == 1
    head = resumed.store.read().head
    assert layered.LayeredSession.open(locator).checkpoint()['roots'] == roots
    assert resumed.store.read().head == head


def test_front_door_main_uses_shared_carrier_without_handwritten_bootstrap(tmp_path, monkeypatch, capsys):
    task = tmp_path / 'intent.txt'
    task.write_text('Identify accountable operators for an incident-status service.')
    monkeypatch.setattr(sys, 'stdin', io.TextIOWrapper(io.BytesIO(b'{"id":"close","operation":"close"}\n')))
    result = layered.main(['start', '--home', str(tmp_path / '.fabric'), '--engagement', 'ordinary',
        '--task', str(task), '--provider', 'codex', '--work-item', 'status-service',
        '--deadline-ms', str(int(time.time() * 1000) + 180000), '--limit-ms', '60000'])
    outputs = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert result == 0
    assert outputs[0]['result']['next']['status'] == 'invoke'
    assert outputs[0]['result']['created']['criteria_basis'] == 'same-verbatim-request'
    assert outputs[-1]['result'] == {'closed': True}


@pytest.mark.parametrize('key_selection', ['default', 'override'])
def test_human_binding_uses_existing_real_disposable_proof_without_submitting(tmp_path, monkeypatch, key_selection):
    from governed_fixtures import HumanSigner
    signer = HumanSigner(tmp_path / 'disposable-human-fixture', monkeypatch)
    session, _ = _start(tmp_path / 'project')
    issued = session.next()
    proposed = session.prepare_human({'action': 'terminate', 'reason': 'Explicit synthetic operator choice',
        'subjects': [issued['prepared']['members'][0]['packet']['assignment']], 'authority_proof': None}, 'delivery-change')
    assert proposed['status'] == 'prepared'
    package = Path(proposed['package'])
    commands = proposed['external_actions']
    assert commands['sign_command'] == ['python3', str(Path(layered.operator.__file__).resolve()),
        'sign', str(package / 'request.json'), '--workspace', str(session.store.path.parent.parent)]
    private = signer.keys['human']['private']
    monkeypatch.setattr(layered.operator, 'default_private_key', lambda: private if key_selection == 'default' else tmp_path / 'missing.pem')
    argv = commands['sign_command'][1:]
    if key_selection == 'override':
        argv += ['--key', str(private)]
    monkeypatch.setattr(sys, 'argv', argv)
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
    monkeypatch.setattr('builtins.input', lambda prompt: 'APPROVE ' + proposed['request']['request_id'])
    assert layered.operator.main() == 0
    receipt = package / 'receipts' / (proposed['request']['request_id'] + '.json')
    wrapper = {'request': proposed['request'], 'receipt': json.loads(receipt.read_bytes())}
    assert layered.operator.verify_receipt(wrapper['request'], wrapper['receipt'])['accepted'] is True
    before = session.store.read().head
    bound = layered.bind_human(package, receipt)
    message = json.loads(Path(bound['message']).read_bytes())
    assert message['payload']['authority_proof'] == lc.blob(layered.operator.canonical(wrapper))
    assert session.store.read().head == before
    assert bound['journal_submitted'] is False


def _history_session(tmp_path, monkeypatch):
    from governed_scheduling_fixtures import SchedulingHarness
    class NativeHistory(SchedulingHarness):
        def _routing_source(self):
            source = super()._routing_source()
            snapshot = producer.routing.load_policy(source, self.store._blob)
            descriptor = snapshot['descriptor']
            capabilities = copy.deepcopy(descriptor['capabilities'])
            capabilities['effects'] = [item for item in capabilities['effects']
                                       if item['operation'] in {'read', 'propose'}]
            source['material'] = producer.routing.capture_policy('host-routing',
                self.store._blob(descriptor['catalogue_blob_id']),
                self.store._blob(descriptor['models_blob_id']),
                {slug: self.store._blob(blob) for slug, blob in descriptor['instruction_blobs'].items()},
                {'provider': 'codex', 'workload_class': 'light',
                 'model_selector': snapshot['models']['providers']['codex']['classes']['light']['model_selector']},
                capabilities, self.store.put_blob)
            return source
    host = NativeHistory(tmp_path / '.fabric', monkeypatch, engagement='changed-inputs')
    host.bootstrap(include_neighbor=True)
    config = {'protocol': 'jai.host-dispatch/1', 'workers': [], 'destinations': [], 'tools': [],
              'limits': {'packet_bytes': 2097152, 'total_bytes': 8388608}}
    locator = layered._save_locator(host.path.parent, host.engagement, config)
    return host, layered.LayeredSession(host.store, config, locator)


def test_actual_owner_input_change_reenters_current_basis_without_old_pass_fallback(tmp_path, monkeypatch):
    host, session = _history_session(tmp_path, monkeypatch)
    _, candidate, proof = host.qualified_answer(text='Explicit controlled fixture answer over version A.')
    assert session.output_status({'ref': candidate, 'use_scope': 'default'})['qualified']
    before = session.checkpoint()
    _, previous, replacement = host.transition_inputs('Owner-approved version B requires new verification.')
    changed = session.checkpoint()
    assert changed['head'] != before['head']
    assert replacement in [item['ref'] for item in changed['inputs']]
    assert previous not in [item['ref'] for item in changed['inputs']]
    assert not session.output_status({'ref': candidate, 'use_scope': 'default'})['qualified']
    entry = session.entry('default', 'service-controls',
        [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 10000}],
        int(time.time() * 1000) + 120000)
    assigned = session.store.read().resolve(entry['assignment'], 'assignment')
    assert replacement in assigned['inherited'] and previous not in assigned['inherited']
    next_phase = session.next()
    assert next_phase['status'] == 'invoke' and next_phase['prepared']['members'][0]['packet']['execution']['phase'] == 'selection'
    assert next_phase['members'][0]['assignment'] == entry['assignment']
    assert proof not in [item['ref'] for item in next_phase['prepared']['members'][0]['packet']['manifest']]


def test_actual_open_episode_remains_readable_without_any_signing_enrollment(tmp_path, monkeypatch):
    from governed_scheduling_fixtures import open_episode
    host, session = _history_session(tmp_path, monkeypatch)
    episode = open_episode(host, [], suffix='real-open-episode')
    monkeypatch.setattr(layered.operator, 'trusted_key', lambda *args: (_ for _ in ()).throw(ValueError('not enrolled')))
    head = session.store.read().head
    dossier = session.human_handoff(episode)
    item, = dossier['episodes']
    assert item['episode'] == episode and item['state'] == 'open'
    assert item['conflicts'] and item['material'] and item['requires_l0']
    assert item['requested_decisions'] == ['Decide the exact scoped requirement and its affected work.']
    assert dossier['signing_readiness']['available'] is False
    assert 'signer' not in dossier['signing_readiness']
    assert not any(item['ready'] for item in dossier['checkpoint']['readiness'])
    assert session.store.read().head == head


def test_pending_physical_ack_survives_front_door_cold_resume_without_repeating_effect(prepared, monkeypatch):
    import governed_dispatch as dispatch
    host, actor, config, output, _, issued, _ = prepared
    locator = layered._save_locator(host.path.parent, host.engagement, config)
    session = layered.LayeredSession(host.store, config, locator)
    proposed = session.request(issued['invocation_id'], issued['members'][0]['member_key'],
        producer.request_frame('propose', {'data': b'One actual materialized output'}))
    request = {'id': 'pending-write', 'operation': 'materialize', 'subject': host.input_a,
               'blob_id': proposed['result']['blob_id'], 'destination_handle': 'owned-output'}
    original = dispatch.Dispatcher._broker_observation
    def interrupted(self, context, event, request_blob, result_blob=None):
        if event == 'broker_observed' and result_blob is not None:
            raise RuntimeError('Interrupted after physical write before ACK')
        return original(self, context, event, request_blob, result_blob)
    with monkeypatch.context() as patch:
        patch.setattr(dispatch.Dispatcher, '_broker_observation', interrupted)
        with pytest.raises(RuntimeError, match='Interrupted after physical write'):
            session.request(issued['invocation_id'], issued['members'][0]['member_key'], request)
    files = [path for path in output.rglob('*') if path.is_file()]
    assert len(files) == 1 and files[0].read_bytes() == b'One actual materialized output'
    resumed = layered.LayeredSession.open(locator)
    checkpoint = resumed.checkpoint()
    pending = next(item for item in checkpoint['inflight'] if item['context'] == issued['members'][0]['context'])
    assert pending['pending_effects'] == ['pending-write']
    with pytest.raises(ValueError) as denied:
        resumed.request(issued['invocation_id'], issued['members'][0]['member_key'], request)
    assert denied.value.code == 'P_UNCERTAIN'
    assert [path.read_bytes() for path in output.rglob('*') if path.is_file()] == [b'One actual materialized output']
