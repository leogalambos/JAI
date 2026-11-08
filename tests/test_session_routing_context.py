# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Session profile/context transport reaches real new-run capture and cold resume."""
import io
import json
import sys
from pathlib import Path

import pytest

from governed_fixtures import ROOT
import execution_profiles as profiles
import governed_layered as layered
import governed_native as native
import governed_native_provider as producer
import lifecycle as lc
import model_router


@pytest.fixture
def project(tmp_path, monkeypatch):
    monkeypatch.setenv('XDG_CONFIG_HOME', str(tmp_path / 'user-config'))
    root = tmp_path / 'project'
    (root / '.jai').mkdir(parents=True)
    (root / '.jai' / 'config.json').write_text(json.dumps({'schema_version': 1, 'profiles': {
        'team': {'extends': 'standard', 'context_policy': 'manual'}}}))
    return root


def _session_choice(project):
    team = profiles.select(project, 'team', session=True)
    assert team['context_policy'] == 'manual'
    workload = profiles.select(project, 'workload', session=True, context_policy=team['context_policy'])
    assert workload['context_policy'] == 'manual'
    return workload


def test_session_receipts_preserve_context_without_persisting_preferences(project):
    path = project / '.jai' / 'config.json'
    original = path.read_bytes()
    receipt = _session_choice(project)
    assert receipt['routing_mode'] == 'workload'
    assert receipt['scope'] == 'session'
    assert path.read_bytes() == original
    assert not (path.parent / 'config.local.json').exists()
    registry = model_router.load(model_router.BASE)
    captured = profiles.resolve(project, registry, 'codex', profile=receipt['execution_profile'],
                                context_policy=receipt['context_policy'])
    assert captured['context_policy'] == 'manual'
    assert captured['context']['main_compaction'] == 'manual'
    assert captured['routing_mode'] == 'workload'
    assert profiles.validate_snapshot(captured, registry) == []
    # No receipt means persisted project/default context still applies.
    unchanged = profiles.resolve(project, registry, 'codex', profile='workload')
    assert unchanged['context_policy'] == 'isolated-handoffs'


@pytest.mark.parametrize('provider', ['codex', 'claude'])
def test_session_context_is_captured_by_new_layered_run_and_survives_cold_resume(project, provider):
    choice = _session_choice(project)
    session, created = layered.LayeredSession.create(project / '.fabric', 'session-' + provider,
        b'Design an internal service accountability map.', provider, 'accountability',
        execution_profile=choice['execution_profile'], execution_context_policy=choice['context_policy'])
    before = session.execution_profile
    assert before['routing_mode'] == 'workload' and before['context_policy'] == 'manual'
    issued = session.next()
    assert issued['status'] == 'invoke'
    assert issued['prepared']['context_controls']['policy'] == 'manual'
    head = session.store.read().head
    # Subsequent preferences affect new runs; a cold resume keeps captured bytes.
    (project / '.jai' / 'config.json').write_text(json.dumps({'schema_version': 1,
        'execution_profile': 'research', 'context_policy': 'task-isolated'}))
    resumed = layered.LayeredSession.open(created['locator'])
    assert resumed.store.read().head == head
    assert resumed.execution_profile == before
    assert resumed.prepare(issued['invocation_id'])['context_controls']['policy'] == 'manual'


@pytest.mark.parametrize('provider', ['codex', 'claude'])
def test_original_native_bootstrap_captures_session_context(project, provider):
    receipt = _session_choice(project)
    store = lc.Store(project / '.fabric' / ('native-' + provider + '.jsonl'), 'native-' + provider)
    initialized = producer.bootstrap(store, b'Design accountability.', b'Name each accountable role.',
        provider, 'accountability', [], None, project=project,
        execution_profile=receipt['execution_profile'], execution_context_policy=receipt['context_policy'])
    session = native.NativeSession(store, initialized['config'], project)
    assert session.execution_profile['context_policy'] == 'manual'
    assert session.execution_profile['routing_mode'] == 'workload'
    assert session.execution_profile['provider'] == provider


@pytest.mark.parametrize('invalid', ['unknown-policy', '', ['manual']])
def test_invalid_context_cannot_enter_new_run_or_be_silently_persisted(project, invalid):
    original = (project / '.jai' / 'config.json').read_bytes()
    with pytest.raises(ValueError, match='context policy'):
        profiles.select(project, 'workload', session=True, context_policy=invalid)
    registry = model_router.load(model_router.BASE)
    with pytest.raises(ValueError, match='context policy'):
        profiles.resolve(project, registry, 'codex', 'workload', context_policy=invalid)
    store = lc.Store(project / '.fabric' / 'rejected.jsonl', 'rejected')
    with pytest.raises(ValueError, match='context policy'):
        producer.bootstrap(store, b'Request.', b'Criteria.', 'codex', 'task', [], None,
            project=project, execution_profile='workload', execution_context_policy=invalid)
    assert not store.read().initialized and not store.read().transactions
    assert (project / '.jai' / 'config.json').read_bytes() == original
    with pytest.raises(ValueError, match='session selection'):
        profiles.select(project, 'workload', context_policy='manual')


def test_native_profile_commands_transport_session_context_in_the_active_conversation(project, capsys):
    base = ['--project', str(project)]
    assert profiles.main([*base, 'use', 'team', '--session']) == 0
    team = json.loads(capsys.readouterr().out)
    assert profiles.main([*base, 'use', 'workload', '--session', '--context-policy', team['context_policy']]) == 0
    workload = json.loads(capsys.readouterr().out)
    assert workload['context_policy'] == 'manual'
    assert profiles.main([*base, 'effective', '--session-profile', workload['execution_profile'],
                          '--context-policy', workload['context_policy']]) == 0
    effective = json.loads(capsys.readouterr().out)
    assert effective['context_policy'] == 'manual' and effective['routing_mode'] == 'workload'
    assert effective['workload_mappings']


def test_layered_cli_transports_context_only_at_new_start_and_rejects_resume_override(project, monkeypatch, capsys):
    task = project / 'request.txt'
    task.write_text('Identify accountable operators for an internal service.')
    monkeypatch.setattr(sys, 'stdin', io.TextIOWrapper(io.BytesIO(b'{"id":"close","operation":"close"}\n')))
    assert layered.main(['start', '--home', str(project / '.fabric'), '--engagement', 'cli',
        '--task', str(task), '--provider', 'codex', '--work-item', 'accountability',
        '--execution-profile', 'workload', '--execution-context-policy', 'manual']) == 0
    outputs = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    locator = outputs[0]['result']['created']['locator']
    session = layered.LayeredSession.open(locator)
    assert session.execution_profile['context_policy'] == 'manual'
    head = session.store.read().head
    with pytest.raises(SystemExit):
        layered.main(['resume', '--session', locator, '--execution-context-policy', 'task-isolated'])
    assert layered.LayeredSession.open(locator).store.read().head == head


def test_original_native_cli_transports_new_context_and_refuses_existing_config_override(project, monkeypatch, capsys):
    task, criteria = project / 'task.txt', project / 'criteria.txt'
    task.write_text('Identify accountable operators.')
    criteria.write_text('Assign each responsibility to a role.')
    monkeypatch.setattr(sys, 'stdin', io.TextIOWrapper(io.BytesIO(b'{"id":"close","operation":"close"}\n')))
    path = project / '.fabric' / 'cli-native.jsonl'
    base = ['--store', str(path), '--engagement', 'cli-native', '--project', str(project)]
    assert native.main([*base, '--task', str(task), '--criteria', str(criteria), '--provider', 'claude',
        '--work-item', 'accountability', '--execution-profile', 'workload', '--execution-context-policy', 'manual']) == 0
    outputs = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    config = outputs[0]['result']['config']
    store = lc.Store(path, 'cli-native')
    assert native.NativeSession(store, config, project).execution_profile['context_policy'] == 'manual'
    head = store.read().head
    with pytest.raises(SystemExit):
        native.main([*base, '--config', str(project / 'unused-config.json'),
                     '--execution-context-policy', 'task-isolated'])
    assert store.read().head == head
