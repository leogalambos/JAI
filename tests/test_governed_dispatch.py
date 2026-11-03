# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Real process containment and exact captured governed completion contracts."""
import copy
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import socket
import time

import pytest

from governed_fixtures import GovernedHarness, lc
import governed_dispatch as dispatch


WORKER = Path(__file__).parent / 'fixtures/governed_dispatch/worker.py'


class _ElapsedHarness(GovernedHarness):
    """Use finite process-time assignments and leave leaf execution to the host."""

    def assignment(self, *args, **kwargs):
        kwargs['token_limit'] = 60000 if args[1] == 'setter' else 20000
        reference, _ = super().assignment(*args, **kwargs)
        return reference, self._known_record(reference, 'assignment')

    def _routing_source(self):
        name = self.dispatch_case
        mode = self.dispatch_mode or 'author'
        settings = {}
        directory = self.dispatch_directory / 'worker'
        if 'native_boundary' in name:
            mode = 'attack'
        if 'real_worker_generates' in name:
            settings = {'materialize': True, 'measure': True}
        if 'materialization_followed' in name:
            settings = {'materialize': True}
        if 'reviewer_receives' in name:
            directory = self.dispatch_directory / 'author-worker'
        config, _, _ = _worker_config(directory, self, {'owner': self.owner()}, mode=mode, settings=settings)
        if 'raw_measurements' in name:
            _measurement_config(config)
        self.route_executions['author'] = _execution(config['workers'][0])
        if 'reviewer_receives' in name:
            config, _, _ = _worker_config(self.dispatch_directory / 'reviewer-worker', self,
                                          {'owner': self.owner()}, mode='information')
            self.route_executions['reviewer'] = _execution(config['workers'][0])
        return super()._routing_source()

    def record(self, logical_id, record_type, record, **kwargs):
        record = copy.deepcopy(record)
        if record_type == 'assignment':
            record['limits'] = [{'metric': 'elapsed_ms', 'unit': 'ms',
                                 'ceiling': record['limits'][0]['ceiling']}]
            for operation in ('materialize', 'measure'):
                if operation == 'materialize' and record['responsibility'] in {
                        'reviewer', 'integration_reviewer', 'receiver', 'measurement'}:
                    continue
                record['effects'].append({'operation': operation, 'owner': record['owner'],
                    'targets': [self.input_a],
                    'destination_handle': 'owned-output' if operation == 'materialize' else None,
                    'tool_policy': self.criteria if operation == 'measure' else None})
        return super().record(logical_id, record_type, record, **kwargs)

    def context(self, logical_id, assignment, record, **kwargs):
        start = kwargs.pop('start', record['responsibility'] == 'setter' or kwargs.get('phase') == 'selection')
        return super().context(logical_id, assignment, record, start=start, **kwargs)


@pytest.fixture
def host(tmp_path, monkeypatch, request):
    fixture = _ElapsedHarness(tmp_path / 'engagement', monkeypatch, engagement='confined-dispatch')
    fixture.dispatch_directory = tmp_path
    fixture.dispatch_case = request.node.originalname
    fixture.dispatch_mode = getattr(request.node, 'callspec', None)
    fixture.dispatch_mode = fixture.dispatch_mode.params.get('mode') if fixture.dispatch_mode else None
    fixture.bootstrap()
    return fixture


def _worker_config(directory, host, actor, *, mode='author', settings=None):
    directory.mkdir(parents=True, exist_ok=True)
    protected = directory / 'protected.txt'
    protected.write_text('host bytes must remain unchanged')
    secret = directory / 'host-only-secret.txt'
    secret.write_text('Host-only fixture data, not a signing key.')
    values = {'protected_file': str(protected), 'host_secret': str(secret),
              'ledger': str(host.path), 'controller': str(Path(dispatch.__file__).resolve()),
              'inherited_fd': 250, 'subject': host.input_a, 'tool_policy': host.criteria,
              **(settings or {})}
    parameters = directory / 'settings.json'
    parameters.write_text(json.dumps(values))
    files = [{'path': str(path.resolve()), 'name': name,
              'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
             for path, name in ((WORKER, 'main.py'), (parameters, 'settings.json'))]
    worker = {'provider': 'json-process/1', 'argv': ['/usr/bin/python3', '/worker/main.py', mode],
              'files': files}
    destination = directory / 'output'
    destination.mkdir(exist_ok=True)
    chooser = WORKER.with_name('selection_worker.py')
    chooser_worker = {'provider': 'json-process/1', 'argv': ['/usr/bin/python3', '/worker/main.py'],
                      'files': [{'path': str(chooser.resolve()), 'name': 'main.py',
                                 'sha256': hashlib.sha256(chooser.read_bytes()).hexdigest()}]}
    config = {'protocol': 'jai.host-dispatch/1', 'workers': [worker, chooser_worker],
              'destinations': [{'handle': 'owned-output', 'owner': actor['owner'], 'root': str(destination)}],
              'tools': [{'policy': host.criteria, 'worker': {**worker,
                         'argv': ['/usr/bin/python3', '/worker/main.py', 'measure']}}],
              'limits': {'packet_bytes': 100000, 'total_bytes': 1000000}}
    return config, protected, destination


def _execution(worker):
    return {'provider': worker['provider'], 'argv': copy.deepcopy(worker['argv']),
            'files': [{key: asset[key] for key in ('name', 'sha256')} for asset in worker['files']]}


def _measurement_config(config):
    probe = WORKER.with_name('measurement_probe.py')
    asset = {'path': str(probe.resolve()), 'name': 'main.py',
             'sha256': hashlib.sha256(probe.read_bytes()).hexdigest()}
    config['workers'][0] = {'provider': 'json-process/1',
                        'argv': ['/usr/bin/python3', '/worker/main.py', 'worker'], 'files': [asset]}
    config['tools'][0]['worker'] = {**config['workers'][0],
                                    'argv': ['/usr/bin/python3', '/worker/main.py', 'tool']}
    config['limits'] = {'packet_bytes': 30000, 'total_bytes': 50000}


def _dispatcher(host, config):
    return dispatch.Dispatcher(host.store, config)


def _answer(host):
    state = host.store.read()
    matches = [value for value in state.versions.values()
               if value['logical_id'] == 'worker-generated-answer']
    assert len(matches) == 1
    record = matches[0]['content']['record']
    return record, json.loads(host.store._blob(record['material'][0]))


def test_real_worker_generates_captured_bytes_and_runtime_completion_with_measurement(host, tmp_path):
    actor = host.setup_author()
    config, _, output = _worker_config(tmp_path / 'worker', host, actor,
                                       settings={'materialize': True, 'measure': True})
    started = time.monotonic()
    result = _dispatcher(host, config).dispatch(actor['author_context'])
    elapsed = (time.monotonic() - started) * 1000
    assert result['usage_ms'] > 0
    assert result['usage_ms'] <= elapsed
    assert result['completion']['status'] == 'committed', result
    record, report = _answer(host)
    assert report['scratch_write']
    assert report['measurement']['ok'], report
    assert report['measurement']['result']['status'] == 0
    assert all(item['reply']['ok'] for item in report['attachments'])
    material = host.store._blob(record['material'][0])
    assert material in [path.read_bytes() for path in output.rglob('*') if path.is_file()]
    assert not host.store.evaluate(next(item['ref'] for item in report['manifest']
                                       if item['ref'] == actor['author']))['accepted']


def test_native_boundary_denies_each_host_operation_and_inherited_capability(host, tmp_path, monkeypatch):
    # Socket creation works outside the boundary; confinement must cause denial.
    with socket.socket():
        pass
    actor = host.setup_author()
    config, protected, _ = _worker_config(tmp_path / 'worker', host, actor, mode='attack')
    monkeypatch.setenv('JAI_TEST_SECRET', 'must-not-reach-worker')
    descriptor = os.open(protected, os.O_RDONLY)
    os.dup2(descriptor, 250, inheritable=True)
    try:
        result = _dispatcher(host, config).dispatch(actor['author_context'])
    finally:
        os.close(250)
        os.close(descriptor)
    assert result['completion']['status'] == 'committed', result
    _, report = _answer(host)
    assert report['allowed_shell_scratch']
    for name in ('read', 'edit', 'delete', 'rename', 'replace', 'socket', 'socketpair',
                 'shell_read', 'shell_edit', 'child_socket'):
        assert report['denials'][name], name
    for name in ('environment_secret_absent', 'inherited_fd_closed', 'host_secret_absent',
                 'ledger_absent', 'controller_absent'):
        assert report[name], name
    assert not report['unknown_read']['ok']
    assert not report['foreign_materialize']['ok']
    assert protected.read_text() == 'host bytes must remain unchanged'


def test_reviewer_receives_own_packet_without_author_transcript_and_can_request_information(host, tmp_path):
    actor = host.setup_author()
    config, _, _ = _worker_config(tmp_path / 'author-worker', host, actor)
    _dispatcher(host, config).dispatch(actor['author_context'])
    state = host.store.read()
    candidate = next({'engagement': host.engagement, 'scope': host.scope,
                      'logical_id': value['logical_id'], 'version_id': identifier}
                     for identifier, value in state.versions.items()
                     if value['logical_id'] == 'worker-generated-answer')
    review = host.prepare_review(actor, candidate)
    reviewer = {'owner': actor['owner']}
    config, _, _ = _worker_config(tmp_path / 'reviewer-worker', host, reviewer, mode='information')
    result = _dispatcher(host, config).dispatch(review['context'])
    assert result['completion']['status'] == 'committed', result
    reports = []
    for path in host.store.material.iterdir():
        if path.is_file():
            try:
                value = json.loads(path.read_bytes())
            except (ValueError, UnicodeDecodeError):
                continue
            if isinstance(value, dict) and value.get('scratch_write'):
                reports.append(value)
    reviewer_report = next(value for value in reports
                           if any(item['ref'] == review['context'] for item in value['manifest']))
    references = [item['ref'] for item in reviewer_report['manifest']]
    assert review['context'] in references
    assert review['assignment'] in references
    assert candidate in references
    assert actor['author_context'] not in references
    assert actor['author'] not in references
    run = host.store.read().resolve(review['context'], 'context')['run_id']
    assert host.store.read().run_states[run] == 'returned'


@pytest.mark.parametrize('mode', ['wrong-context', 'unavailable-material'])
def test_worker_cannot_substitute_context_or_claim_uncaptured_output(host, tmp_path, mode):
    actor = host.setup_author()
    config, _, _ = _worker_config(tmp_path / 'worker', host, actor, mode=mode)
    with pytest.raises(dispatch.DispatchError):
        _dispatcher(host, config).dispatch(actor['author_context'])
    assert not any(value['logical_id'] == 'worker-generated-answer'
                   for value in host.store.read().versions.values())


def test_unsupported_provider_and_protected_asset_fail_before_launch(host, tmp_path):
    actor = host.setup_author()
    config, _, _ = _worker_config(tmp_path / 'worker', host, actor)
    original = host.path.read_bytes()
    config['workers'][0]['provider'] = 'unsupported-provider'
    with pytest.raises(dispatch.DispatchError):
        _dispatcher(host, config).dispatch(actor['author_context'])
    assert host.path.read_bytes() == original
    config['workers'][0]['provider'] = 'json-process/1'
    protected = host.path
    config['workers'][0]['files'].append({'path': str(protected), 'name': 'journal.jsonl',
                                      'sha256': hashlib.sha256(protected.read_bytes()).hexdigest()})
    with pytest.raises(dispatch.DispatchError):
        _dispatcher(host, config).dispatch(actor['author_context'])
    assert host.path.read_bytes() == original


def test_missing_declared_material_prevents_launch_without_fabricating_input(host, tmp_path):
    actor = host.setup_author()
    config, _, output = _worker_config(tmp_path / 'worker', host, actor)
    source = host.store.read().resolve(host.input_a, 'source')
    (host.store.material / source['material'][0]).unlink()
    with pytest.raises(dispatch.DispatchError) as failure:
        _dispatcher(host, config).dispatch(actor['author_context'])
    assert failure.value.code == 'P_CONTEXT'
    state = host.store.read()
    context = state.resolve(actor['author_context'], 'context')
    assert state.run_states[context['run_id']] == 'cancelled'
    assert not any(value['logical_id'] == 'worker-generated-answer' for value in state.versions.values())
    assert not (host.store.material / source['material'][0]).exists()
    assert list(output.iterdir()) == []


@pytest.mark.parametrize('mode', ['sleep', 'overflow'])
def test_real_blocked_or_excessive_process_is_terminated_without_result(host, tmp_path, mode):
    actor = host.setup_author()
    config, _, output = _worker_config(tmp_path / 'worker', host, actor, mode=mode)
    if mode == 'overflow':
        config['limits']['packet_bytes'] = 50000
    started = time.monotonic()
    with pytest.raises(dispatch.DispatchError):
        _dispatcher(host, config).dispatch(actor['author_context'])
    assert time.monotonic() - started < 40
    assert not any(value['logical_id'] == 'worker-generated-answer'
                   for value in host.store.read().versions.values())
    assert list(output.iterdir()) == []


def test_materialization_followed_by_unrelated_commit_keeps_current_run_and_signed_audit(host, tmp_path, monkeypatch):
    actor = host.setup_author()
    config, _, output = _worker_config(tmp_path / 'worker', host, actor,
                                       settings={'materialize': True})
    source = copy.deepcopy(host.store.read().resolve(host.input_a, 'source'))
    source['material'] = [host.material('Concurrent immutable proposal, not a new governing input.')]
    original_lock = dispatch.lc.store_lock
    changed = []

    @contextmanager
    def concurrent_commit(path):
        with original_lock(path):
            yield
        if path == host.path and not changed and any(item.is_file() for item in output.rglob('*')):
            changed.append(True)
            host.record('concurrent-staged-input', 'source', source)

    monkeypatch.setattr(dispatch.lc, 'store_lock', concurrent_commit)
    result = _dispatcher(host, config).dispatch(actor['author_context'])
    assert result['completion']['status'] == 'committed', result
    assert changed
    assert any(item.is_file() for item in output.rglob('*'))
    state = host.store.read()
    context = state.resolve(actor['author_context'], 'context')
    assert state.run_states[context['run_id']] == 'returned'
    answer, _ = _answer(host)
    assert answer['assignment'] == actor['author']
    assert any(value['logical_id'] == 'concurrent-staged-input' for value in state.versions.values())
    terminal = json.loads(host.path.read_text().splitlines()[-1])['operations'][0]['data']['message']
    assert terminal['payload']['event'] == 'run_completed'
    assert terminal['payload']['usage'][0]['total'] > 0
    attachment = next(item for item in terminal['attachments'] if item['access_handle'] == 'dispatch-audit')
    audit = json.loads(host.store._blob(attachment['blob_id']))
    assert any(event['request']['operation'] == 'materialize' for event in audit['events'])


def test_raw_measurements_share_the_existing_total_byte_bound(host, tmp_path):
    actor = host.setup_author()
    config, _, _ = _worker_config(tmp_path / 'worker', host, actor)
    _measurement_config(config)
    # Measure the fixture's own input footprint, rather than assuming that an
    # evolving valid packet still fits an unrelated historical 30 kB constant.
    config['limits'] = {'packet_bytes': 1000000, 'total_bytes': 2000000}
    probe = _dispatcher(host, config)
    _, _, _, _, packet, _, _ = probe._prepare(actor['author_context'])
    initial = len(lc.canonical(packet)) + 1
    output_size = max(20000, initial, sum(map(len, probe.handles.values())))
    config['tools'][0]['worker']['argv'].append(str(output_size))
    config['limits'] = {'packet_bytes': max(initial, output_size) + 1024,
                        'total_bytes': initial + output_size + output_size // 2 + 4096}
    consumer = _dispatcher(host, config)
    with pytest.raises(dispatch.DispatchError) as failure:
        consumer.dispatch(actor['author_context'])
    assert failure.value.code == 'P_BUDGET'
    assert consumer.transferred > consumer.total_limit
    assert any(item['request']['operation'] == 'measure'
               and item.get('error', {}).get('code') == 'P_BUDGET'
               and 'aggregate' in item['error']['message'] for item in consumer.audit)
    state = host.store.read()
    context = state.resolve(actor['author_context'], 'context')
    assert state.run_states[context['run_id']] == 'cancelled'
    assert any(path.is_file() and path.read_bytes() == b'm' * output_size
               for path in host.store.material.iterdir())


def test_explicit_attachment_requires_readable_input_membership_before_launch(host, tmp_path):
    actor = host.setup_author(start_author=False)
    config, _, output = _worker_config(tmp_path / 'worker', host, actor)
    source = host.store.read().resolve(host.input_a, 'source')
    authorized = source['material'][0]
    ungranted = host.material('Stored bytes are not automatically authorized input.')

    def issued_context(identifier, blob_id):
        content = host.store._blob(blob_id)
        reference = host.context(identifier + '-issued', actor['author'], actor['author_record'], start=False)
        context = copy.deepcopy(host.store.read().resolve(reference, 'context'))
        host.cancel_run(reference)
        context['run_id'] = identifier + '-run'
        context['attachments'] = [{'blob_id': blob_id, 'byte_length': len(content), 'media_type': 'text/plain',
                                   'classification': 'internal', 'access_handle': identifier + '-attachment'}]
        return host.record(identifier, 'context', context)

    bad = issued_context('ungranted-context', ungranted)
    with pytest.raises(dispatch.DispatchError) as failure:
        _dispatcher(host, config).dispatch(bad)
    assert failure.value.code == 'P_SCOPE'
    state = host.store.read()
    assert state.run_states[state.resolve(bad, 'context')['run_id']] == 'cancelled'
    assert not any(value['logical_id'] == 'worker-generated-answer' for value in state.versions.values())
    assert list(output.iterdir()) == []
    good = issued_context('authorized-context', authorized)
    result = _dispatcher(host, config).dispatch(good)
    assert result['completion']['status'] == 'committed', result
    _, report = _answer(host)
    assert any(item['blob_id'] == authorized and item['reply']['ok'] for item in report['attachments'])


def test_current_worker_slots_project_facts_without_reassessing_accepted_results(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch, engagement='packet-current-facts')
    host.bootstrap()
    actor, subject, proof = host.qualified_answer(suffix='packet-accepted-answer')
    state = host.store.read()
    consumer = object.__new__(dispatch.Dispatcher)

    def forbid_reassessment(*args, **kwargs):
        raise AssertionError('Worker slot projection must use established current facts')

    monkeypatch.setattr(lc.State, 'evaluate', forbid_reassessment)
    monkeypatch.setattr(lc.State, '_governing_grants', forbid_reassessment)
    slots = consumer._current_slots(state, actor['setter'], state.resolve(actor['setter'], 'assignment'), [], [])
    selected = {item['selected_ref']['version_id']: item for item in slots if item['selected_ref'] is not None}
    assert selected[subject['version_id']]['applicable']
    assert selected[proof['version_id']]['applicable']
    state.states[(host.scope, subject['version_id'])] = {'validity': 'valid', 'applicable': False}
    slots = consumer._current_slots(state, actor['setter'], state.resolve(actor['setter'], 'assignment'), [], [])
    assert not next(item for item in slots if item['selected_ref'] == subject)['applicable']
