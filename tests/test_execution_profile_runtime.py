# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Profiles cross real bootstrap, selection, provider and analytics boundaries."""
import copy
import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import execution_profiles
import governed_layered
import governed_native
import governed_native_provider as provider
import lifecycle as lc


def _project(tmp_path, active='codex', settings=None):
    (tmp_path / '.jai').mkdir()
    (tmp_path / '.jai/config.json').write_text(json.dumps(settings or {
        'schema_version': 1, 'execution_profile': 'stronger-setter',
        'context_policy': 'task-isolated',
        'analytics': {'task_class': 'bounded-design', 'review_scope': 'substantive'},
        'overrides': {'providers': {active: {'setter': {'model_selector': 'test-setter'}}}}}))
    session, created = governed_layered.LayeredSession.create(tmp_path / '.fabric',
        'profile-runtime', b'Design bounded backups.', active, 'backup')
    issued = session.issue_batch([{'assignment': created['entry']['assignment'], 'phase': 'selection'}])
    return session, created, issued


@pytest.mark.parametrize('active', ['codex', 'claude'])
def test_profile_is_selected_from_real_availability_and_passed_to_work_host(tmp_path, active):
    session, created, issued = _project(tmp_path, active)
    descriptor = session.prepare(issued['invocation_id'])
    packet = descriptor['members'][0]['packet']
    choice = next(row for row in packet['execution']['availability']
                  if row['provider'] == active and row['workload_class'] == 'heavy')
    assert choice['model_selector'] == 'test-setter'
    assert choice['reasoning_effort'] == 'high'
    session.start(issued['invocation_id'], active, 'selection-handle', {'id': 'selection-handle'})
    raw = json.dumps({'format': 'jai.semantic-return/1', 'results': [{
        'member': descriptor['members'][0]['member_key'], 'kind': 'selection',
        'specialties': ['software-engineer'], 'provider': active,
        'workload_class': 'heavy', 'model_selector': choice['model_selector'],
        'reason': 'Use the captured preferred setter model.', 'previous': None}]})
    session.complete(issued['invocation_id'], raw, {'observed': 'returned'})
    state = session.store.read()
    selection = state.execution_plans[(created['entry']['assignment']['version_id'], 'default')]
    work = session.issue_batch([{'assignment': created['entry']['assignment'],
                                'phase': 'work', 'selection': selection}])
    prepared = session.prepare(work['invocation_id'])
    args = prepared['invocation']['arguments']
    assert args['model'] == 'test-setter'
    assert args['reasoning_effort' if active == 'codex' else 'effort'] == 'high'
    assert prepared['context_controls']['policy'] == 'task-isolated'
    assert prepared['context_controls']['main_conversation_action'] == 'request-fresh-task-chat'
    assert 'not performed' in prepared['context_controls']['main_action_status']
    projections = session._run(prepared['members'][0]['context']).execution['model']
    assert projections['model_selector'] == args['model']
    if active == 'codex':
        assert args['fork_turns'] == 'none'
    else:
        delivered = lc.loads(session.store._blob(prepared['members'][0]['host_delivery']['manifest_blob_id']))
        agents = [session.store._blob(row['blob_id']).decode() for row in delivered['resources']
                  if row['label'].startswith('Canonical operator:')]
        assert any('model: test-setter' in agent and 'effort: high' in agent for agent in agents)


def test_resume_uses_pinned_profile_and_warm_statistics_do_not_write_twice(tmp_path, monkeypatch):
    session, created, issued = _project(tmp_path)
    original = copy.deepcopy(session.execution_profile)
    (tmp_path / '.jai/config.json').write_text('{"schema_version":1,"execution_profile":"economy"}')
    reopened = governed_layered.LayeredSession.open(created['locator'])
    assert reopened.execution_profile == original
    assert reopened.prepare(issued['invocation_id'])['context_controls']['policy'] == 'task-isolated'
    first = reopened.efficiency()
    assert first['summary']['task_class'] == 'bounded-design'
    assert first['summary']['outcome'] == 'in progress'
    monkeypatch.setattr(governed_native.execution_stats, 'record', lambda *args: pytest.fail('unchanged journal wrote history'))
    assert reopened.efficiency() == first


def test_analytics_failure_does_not_disguise_successful_primary_operation(tmp_path, monkeypatch):
    session, created, issued = _project(tmp_path)
    monkeypatch.setattr(session, 'efficiency', lambda: (_ for _ in ()).throw(OSError('unavailable')))
    source = io.BytesIO((json.dumps({'id': 'checkpoint', 'operation': 'checkpoint', 'scope': 'default'}) + '\n').encode())
    destination = io.StringIO()
    assert governed_native.serve(session, source, destination, governed_layered.OPERATIONS) == 0
    response = json.loads(destination.getvalue())
    assert response['ok'] is True
    assert response['result']['engagement'] == 'profile-runtime'
    assert response['efficiency']['status'] == 'unavailable'


def test_customizing_active_default_profile_activates_effective_mapping(tmp_path):
    session, created, issued = _project(tmp_path, settings={
        'schema_version': 1, 'profiles': {'standard': {'providers': {
            'codex': {'setter': {'model_selector': 'custom-default'}}}}}})
    assert session.execution_profile['configured'] is True
    packet = session.prepare(issued['invocation_id'])['members'][0]['packet']
    mapping = next(row for row in packet['execution']['availability']
                   if row['provider'] == 'codex' and row['workload_class'] == 'standard')
    assert mapping['model_selector'] == 'custom-default'


def test_installer_exposes_native_conversation_names_without_external_cli(tmp_path):
    spec = importlib.util.spec_from_file_location('profile_installer', ROOT / '.ai/setup/installer.py')
    installer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(installer)
    registry = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_bytes())
    outputs, modes = installer.desired_outputs(ROOT, {'codex', 'claude'},
        tmp_path / 'house', tmp_path / 'claude', tmp_path / 'codex', registry)
    for name in ('profile', 'stats'):
        claude = str(tmp_path / 'claude/commands' / ('jai-' + name + '.md'))
        codex = str(tmp_path / 'codex/skills' / ('workflow-' + name) / 'SKILL.md')
        assert claude in outputs and codex in outputs
        assert str(tmp_path / 'claude/commands' / (name + '.md')) not in outputs
        assert ('name: workflow-' + name).encode() in outputs[codex]


def test_captured_snapshot_rejects_changed_isolation_invariant(tmp_path):
    registry = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_bytes())
    snapshot = execution_profiles.resolve(tmp_path, registry, 'codex', 'standard')
    snapshot['context']['reviewer'] = 'shared'
    registry['execution_profile'] = snapshot
    assert provider.model_router.validate_registry(registry)


def test_final_outcome_survives_cold_reopen_and_reacts_to_actual_invalidation(tmp_path, monkeypatch):
    from test_governed_final_acceptance import _FinalReportHouse
    from test_governed_dispatch import _worker_config

    host = _FinalReportHouse(tmp_path / 'facts', monkeypatch, engagement='durable-final')
    host.bootstrap()
    actor = host.setup_author(suffix='actual-final', responsibility='integrator', work_kind='integration')
    subject, record = host.product('final-report', actor, kind='final_result',
        outcome={'kind': 'insufficient_information', 'attempt': actor['setter'], 'evidence': [host.criteria]})
    host.commit(host.submission(actor, subject, record))
    proof, _ = host.review(actor, subject, suffix='independent-final', assessment_kind='integration')
    host.select_proof(subject, proof, role='integration_review')
    config, _, _ = _worker_config(tmp_path / 'tools', host, actor)
    session = governed_native.NativeSession(host.store, config, project=tmp_path)
    result = session.efficiency()
    assert result['summary']['outcome'] == 'completed'
    host.accept(subject)
    assert session.efficiency()['summary']['outcome'] == 'accepted'
    reopened = governed_native.NativeSession(lc.Store(host.path, host.engagement), config, project=tmp_path)
    assert reopened.efficiency()['summary']['outcome'] == 'accepted'
    host.commit(host.owner_decision(actor['owner'], {'action': 'invalidate',
        'reason': 'Withdraw the exact independent proof.', 'subjects': [proof]}))
    assert reopened.efficiency()['summary']['outcome'] == 'in progress'


def test_alternative_available_workload_changes_configuration_comparison_identity(tmp_path):
    import execution_stats

    registry = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_bytes())
    preference = execution_profiles.resolve(tmp_path, registry, 'codex', 'standard')
    original = execution_stats.configuration_version(preference, registry)
    registry['providers']['codex']['classes']['research']['model_selector'] = 'changed-research'
    assert execution_stats.configuration_version(preference, registry) != original
