# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""A retained genuine fixture resumes one stage without fabricating prior work."""
import hashlib
import pytest

from governed_stage_checkpoint import save_checkpoint, resume_checkpoint
from test_governed_local_layer import _LocalHarness, _worker, WORKERS
import governed_workflow
import lifecycle as lc


def test_explicit_checkpoint_cold_audits_and_runs_only_its_unfinished_native_stage(tmp_path, monkeypatch):
    host = _LocalHarness(tmp_path / 'engagement', monkeypatch, engagement='checkpoint-stage')
    host.bootstrap(include_neighbor=True)
    # Substitution faults affect a private copy, never workers enrolled by an
    # independently running integration scenario.
    copied_worker = tmp_path / 'copied-layer-worker.py'
    worker_bytes = (WORKERS / 'layer_worker.py').read_bytes()
    copied_worker.write_bytes(worker_bytes)
    config = {'protocol': 'jai.host-dispatch/1',
              'workers': [_worker(WORKERS / 'selection_worker.py'), _worker(copied_worker)],
              'destinations': [], 'tools': [],
              'limits': {'packet_bytes': 1000000, 'total_bytes': 8000000}}
    workflow = governed_workflow.Workflow(host.store, config)
    entry = workflow.entry('default', 'service-controls',
        [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 60000}],
        int(lc.time.time() * 1000) + 120000)
    assignment = entry['assignment']
    checkpoint = save_checkpoint(tmp_path / 'stage-checkpoint.json', host, workflow,
        assignment, stage='local-question-delegation', refs={'root': assignment})
    before = host.path.read_bytes()
    before_transactions = lc._parse_transactions(before)
    original_hashes = {transaction['hash'] for transaction in before_transactions}
    calls = []
    verify = lc._verify_transaction

    def observe_actual_verification(state, transaction, live=False):
        calls.append(transaction['hash'])
        return verify(state, transaction, live=live)

    monkeypatch.setattr(lc, '_verify_transaction', observe_actual_verification)
    result = resume_checkpoint(checkpoint)
    assert result['qualification'] == 'resumed-stage-only'
    assert result['stage'] == 'local-question-delegation'
    assert result['result']['completion']['status'] == 'committed'
    assert result['verified_prefix_transactions'] == len(before_transactions)
    assert result['new_transactions'] > 0
    assert all(calls.count(identifier) == 1 for identifier in original_hashes)
    after = host.path.read_bytes()
    assert after.startswith(before)
    assert result['before_head'] == before_transactions[-1]['hash']
    state = host.store.read()
    children = [value['content']['record'] for value in state.versions.values()
                if value['kind'] == 'delivery.assignment'
                and value['content']['record']['issued_under'] == assignment]
    assert {child['owner']['question'] for child in children} == {'what', 'why', 'how', 'who', 'where', 'when'}
    assert all(child['responsibility'] == 'setter' for child in children)
    assert state.assignment_states[assignment['version_id']] == 'open'

    # Setters remain logically open, so the authenticated successful work tail
    # must prevent advancing their next branch under the guise of retrying.
    with pytest.raises(lc.ERROR) as duplicate:
        resume_checkpoint(checkpoint)
    assert duplicate.value.code == 'P_IDEMPOTENCY'
    assert host.path.read_bytes() == after

    copied_worker.write_bytes(worker_bytes + b'\n# Changed governed worker.\n')
    try:
        with pytest.raises(ValueError, match='governed worker changed'):
            resume_checkpoint(checkpoint)
        assert host.path.read_bytes() == after
    finally:
        copied_worker.write_bytes(worker_bytes)
    assert hashlib.sha256(copied_worker.read_bytes()).hexdigest() == config['workers'][1]['files'][0]['sha256']

    host.path.write_bytes(before[:-1])
    try:
        with pytest.raises(ValueError, match='changed or truncated'):
            resume_checkpoint(checkpoint)
        assert host.path.read_bytes() == before[:-1]
    finally:
        host.path.write_bytes(after)
