# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Real production bootstrap and existing projection/native packaging contracts."""
import base64
import copy
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import governed_native as native
import governed_native_provider as provider
import lifecycle as lc


def _start(tmp_path, active='codex', model_config=None):
    store = lc.Store(tmp_path / 'native.jsonl', 'native-defaults')
    limits = [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 60000}]
    deadline = int(time.time() * 1000) + 180000
    result = provider.bootstrap(store, b'Explain a bounded backup service.',
        b'Address restore readiness and identify uncertainty.', active, 'backup', limits,
        deadline, model_config)
    session = native.NativeSession(store, result['config'])
    entry = session.workflow.entry('default', 'backup', limits, deadline)
    issued = session.issue_batch([{'assignment': entry['assignment'], 'phase': 'selection'}])
    return store, result, session, issued


def test_real_bootstrap_preserves_exact_inputs_full_catalogue_and_rejects_overwrite(tmp_path):
    store, result, session, issued = _start(tmp_path)
    state = store.read()
    task = state.resolve(result['sources']['request'], 'source')
    assert store._blob(task['material'][0]) == b'Explain a bounded backup service.'
    snapshot = state.assignment_routing(state.resolve(issued['members'][0]['assignment'], 'assignment'), live=True)['snapshot']
    assert len(snapshot['instructions']) == json.loads((ROOT / '.ai/runtime/roles.json').read_bytes())['count']
    assert snapshot['models']['providers']['codex']['classes']['standard']['model_selector']
    assert len(state.transactions) == 3
    with pytest.raises(ValueError, match='empty engagement'):
        provider.bootstrap(store, b'new', b'new', 'codex', 'backup',
            [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 1}], int(time.time() * 1000) + 10000)


@pytest.mark.parametrize('active', ['codex', 'claude'])
def test_prepare_uses_existing_projection_and_exact_supported_call_intent(tmp_path, active):
    store, result, session, issued = _start(tmp_path, active)
    before = store.read().head
    descriptor = provider.prepare(session, issued['invocation_id'])
    member = descriptor['members'][0]
    assert member['packet']['assignment'] == issued['members'][0]['assignment']
    assert descriptor['generic_agent'] == 'role-router'
    delivery = lc.loads(store._blob(member['host_delivery']['manifest_blob_id']))
    projections = [store._blob(item['blob_id']).decode() for item in delivery['resources']
                   if item['label'] == 'Canonical operator: role-router']
    assert len(projections) == 1
    assert 'Role Skill Router' in projections[0]
    assert descriptor['model_observation']['observed'] is None
    assert store.read().head != before
    pinned_head = store.read().head
    assert provider.prepare(session, issued['invocation_id'])['invocation'] == descriptor['invocation']
    assert store.read().head == pinned_head
    args = descriptor['invocation']['arguments']
    if active == 'codex':
        assert args['fork_turns'] == 'none'
        assert re.fullmatch(r'[A-Za-z0-9_]+', args['task_name'])
        assert set(args) <= {'task_name', 'message', 'fork_turns', 'model', 'reasoning_effort'}
        assert descriptor['invocation']['tool'] == 'collaboration.spawn_agent'
    else:
        assert descriptor['invocation']['tool'] == 'native-agent-intent'
        assert args['agent'] == 'role-router'
        assert 'model: haiku' in projections[0]


def test_captured_model_override_is_not_reread_during_prepare(tmp_path):
    override = tmp_path / 'models.json'
    override.write_text(json.dumps({'providers': {'codex': {'classes': {
        'light': {'model_selector': 'explicit-model', 'reasoning_effort': 'high'}}}}}))
    store, result, session, issued = _start(tmp_path, model_config=override)
    override.write_text('{}')
    descriptor = provider.prepare(session, issued['invocation_id'])
    assert descriptor['invocation']['arguments']['model'] == 'explicit-model'
    assert descriptor['invocation']['arguments']['reasoning_effort'] == 'high'


def test_deterministic_transport_packaging_never_rewrites_producer_content(tmp_path):
    raw = 'A measured limitation: caf\u00e9.\n'.encode()
    frame = provider.request_frame('propose', {'data': raw})
    assert base64.b64decode(frame['data']) == raw
    assert frame == provider.request_frame('propose', {'data': raw})
    assert frame['id'] != provider.request_frame('propose', {'data': raw + b'!'})['id']
    with pytest.raises(Exception):
        provider.request_frame('propose', {'data': raw, 'unexpected': True})
    store, result, session, issued = _start(tmp_path)
    packet = session.prepare(issued['invocation_id'])['members'][0]['packet']
    records = []
    intents = [{'message_type': 'decision', 'recipient': {'kind': 'controller', 'id': 'native-controller'},
        'payload': {'action': 'select_execution', 'assignment': issued['members'][0]['assignment'],
            'specialties': ['software-engineer'], 'provider': 'codex', 'workload_class': 'standard',
            'model_selector': 'gpt-6.1-sol', 'reason': 'Actual producer selection test.', 'previous': None, 'authority_proof': None}}]
    value = provider.producer_return(packet, records, intents)
    assert value == {'assignment': issued['members'][0]['assignment'], 'context': issued['members'][0]['context'],
                     'records': [], 'intents': intents}
    value['records'].append({'not': 'producer data'})
    assert records == []
    with pytest.raises(Exception):
        provider.producer_return(packet, [], [{'message_type': 'invented'}])


def test_bootstrap_rejects_nonproductive_or_unbounded_input_before_journal(tmp_path):
    store = lc.Store(tmp_path / 'native.jsonl', 'invalid')
    with pytest.raises(ValueError):
        provider.bootstrap(store, b'', b'criteria', 'codex', 'backup', [], 0)
    assert not store.read().initialized


def test_default_full_catalogue_read_fits_while_explicit_small_ceiling_still_denies(tmp_path):
    store, result, session, issued = _start(tmp_path / 'default')
    member = session.prepare(issued['invocation_id'])['members'][0]
    session.start(issued['invocation_id'], 'codex', 'catalogue-default', {'agent_id': 'catalogue-default'})
    response = session.request(issued['invocation_id'], member['member_key'],
                               provider.request_frame('read', {'handle': 'catalogue'}))
    catalogue = json.loads(base64.b64decode(response['result']['data']))
    assert len(catalogue['roles']) == catalogue['count'] == 286
    assert result['config']['limits']['packet_bytes'] == 2097152
    store, result, session, issued = _start(tmp_path / 'small')
    config = copy.deepcopy(result['config'])
    config['limits']['packet_bytes'] = 1048576
    bounded = native.NativeSession(store, config)
    member = bounded.prepare(issued['invocation_id'])['members'][0]
    bounded.start(issued['invocation_id'], 'codex', 'catalogue-small', {'agent_id': 'catalogue-small'})
    with pytest.raises(Exception, match='acknowledgement exceeds'):
        bounded.request(issued['invocation_id'], member['member_key'],
                        provider.request_frame('read', {'handle': 'catalogue'}))


def test_default_foreground_startup_needs_actual_files_not_fixture_or_manual_packet(tmp_path):
    task, criteria = tmp_path / 'task.txt', tmp_path / 'criteria.txt'
    task.write_text('Describe a bounded backup service.')
    criteria.write_text('Identify restore readiness and uncertainty.')
    run = subprocess.run([sys.executable, str(ROOT / '.ai/runtime/tools/governed_native.py'),
        '--store', str(tmp_path / 'live.jsonl'), '--engagement', 'ordinary-start',
        '--task', str(task), '--criteria', str(criteria), '--provider', 'codex',
        '--work-item', 'backup', '--deadline-ms', str(int(time.time() * 1000) + 180000),
        '--limit-ms', '60000'], input='{"id":"close","operation":"close"}\n',
        text=True, capture_output=True, timeout=30, check=True)
    startup, closed = [json.loads(line) for line in run.stdout.splitlines()]
    assert startup['id'] == 'startup'
    assert startup['result']['prepared']['invocation']['tool'] == 'collaboration.spawn_agent'
    assert startup['result']['prepared']['members'][0]['packet']['execution']['phase'] == 'selection'
    assert closed['result'] == {'closed': True}


def test_response_contract_distinguishes_coordinating_setter_question_author_and_review(tmp_path):
    store, result, session, issued = _start(tmp_path)
    descriptor = session.prepare(issued['invocation_id'])
    state = store.read()
    assignment = copy.deepcopy(state.resolve(issued['members'][0]['assignment'], 'assignment'))
    profile = state.resolve(result['profile'], 'profile')
    packet = copy.deepcopy(descriptor['members'][0]['packet'])
    packet['execution']['phase'] = 'work'
    gateway = provider._response_contract(packet, assignment, profile)
    assert gateway['semantic_kind'] == 'setter'
    slots = [item for item in gateway['profile_obligations'] if item['role'] == 'input']
    assert {item['owner']['question'] for item in slots} == set(provider.QUESTIONS)
    assert all(item['minimum'] == item['maximum'] == 1 for item in slots)
    assert gateway['recipient'] == profile['owner']
    assignment['owner'] = {'layer': 1, 'work_kind': 'question', 'question': 'what', 'work_item': 'backup'}
    question = provider._response_contract(packet, assignment, profile)
    assert question['semantic_kind'] == 'setter'
    assert all(item['owner'] == assignment['owner'] for item in question['profile_obligations'])
    assignment['responsibility'] = 'author'
    author = provider._response_contract(packet, assignment, profile)
    assert author['semantic_kind'] == 'author'
    assignment['responsibility'] = 'reviewer'
    review = provider._response_contract(packet, assignment, profile)
    assert review['semantic_kind'] == 'reviewer'
    assert author['purpose'] != review['purpose']
    assert 'wire records' in review['mechanics']
    assert 'jai.semantic-return/1' in descriptor['invocation']['arguments']['message']


def test_selected_canonical_operator_tiers_preserve_advice_inspection_and_mixed_ceilings(tmp_path):
    store, result, session, issued = _start(tmp_path)
    snapshot = session._run(issued['members'][0]['context']).execution['snapshot']
    models = snapshot['models']
    assignment = copy.deepcopy(store.read().resolve(issued['members'][0]['assignment'], 'assignment'))

    def project(specialties, responsibility):
        assignment['responsibility'] = responsibility
        choice = {'action': 'select_execution', 'assignment': issued['members'][0]['assignment'],
            'specialties': specialties, 'provider': 'codex', 'workload_class': 'standard',
            'model_selector': models['providers']['codex']['classes']['standard']['model_selector'],
            'reason': 'Exercise exact retained catalogue operator mapping.', 'previous': None, 'authority_proof': None}
        execution = provider.routing.select_execution(assignment, snapshot, choice)
        execution.update(phase='work', snapshot=snapshot)
        return provider._operator_projections(execution, responsibility, 'codex', models, 'standard')

    advice, tools, operations = project(['chief-information-security-officer'], 'author')
    assert [(item['agent'], item['specialties']) for item in advice] == [
        ('role-advisor', ['chief-information-security-officer'])]
    assert 'Role Advisor' in advice[0]['projection']
    assert 'Write' not in tools and 'Edit' not in tools and 'Bash' not in tools
    assert operations == ['propose', 'read']
    execute_review, tools, operations = project(['software-engineer'], 'reviewer')
    assert execute_review[0]['agent'] == 'role-engineer'
    assert 'Write' not in execute_review[0]['provider_config']['allowed_tools']
    assert 'Edit' not in execute_review[0]['provider_config']['allowed_tools']
    assert execute_review[0]['provider_config']['workspace_write'] is False
    claude_review, _, _ = provider._operator_projections({
        **provider.routing.select_execution({**assignment, 'responsibility': 'reviewer'}, snapshot, {
            'action': 'select_execution', 'assignment': issued['members'][0]['assignment'],
            'specialties': ['software-engineer'], 'provider': 'claude', 'workload_class': 'standard',
            'model_selector': models['providers']['claude']['classes']['standard']['model_selector'],
            'reason': 'Retain execute professional without review mutation.', 'previous': None, 'authority_proof': None}),
        'phase': 'work', 'snapshot': snapshot}, 'reviewer', 'claude', models, 'standard')
    native_tools = provider.provider_projection.split_frontmatter(claude_review[0]['projection'])[0]['tools']
    assert 'Write' not in native_tools and 'Edit' not in native_tools
    inspected, tools, operations = project(['codebase-reviewer'], 'reviewer')
    assert inspected[0]['agent'] == 'codebase-reviewer'
    assert 'Bash' in tools and 'Write' not in tools and 'Edit' not in tools
    assert 'measure' in operations and 'materialize' not in operations
    mixed, tools, operations = project(['chief-information-security-officer', 'software-engineer'], 'author')
    assert {item['agent'] for item in mixed} == {'role-advisor', 'role-engineer'}
    assert {item['agent']: item['specialties'] for item in mixed} == {
        'role-advisor': ['chief-information-security-officer'], 'role-engineer': ['software-engineer']}
    engineer_config = next(item['provider_config'] for item in mixed if item['agent'] == 'role-engineer')
    assert engineer_config['local_execution']['shell_available'] is False
    assert 'Write' not in tools and 'Edit' not in tools and 'Bash' not in tools
    assert operations == ['propose', 'read']
