# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Actual isolated helper checks for the development-only cap observer."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[4]
WRAPPER = ROOT / 'apps/fabric-explorer/reader/dev/cap_diagnostic.py'
CORE = ROOT / '.ai/runtime/tools'
spec = importlib.util.spec_from_file_location('cap_diagnostic', WRAPPER)
diag = importlib.util.module_from_spec(spec); spec.loader.exec_module(diag)


def run_helper(tmp_path, script, budget):
    """Run a real admitted fixture through the fixed isolated helper protocol."""
    source = tmp_path / 'source'; source.mkdir()
    app = tmp_path / 'app'; app.mkdir()
    raw = (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes()
    path = source / 'review.jsonl'; path.write_bytes(raw)
    process = subprocess.Popen([sys.executable, '-I', '-B', str(script), str(CORE)], cwd=app, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    def call(index, operation, args):
        process.stdin.write(json.dumps({'id': index, 'operation': operation, 'args': args}) + '\n'); process.stdin.flush()
        return json.loads(process.stdout.readline())
    try:
        assert call(1, 'configure', {'writeRoots': [str(app)]})['ok']
        admitted = call(2, 'admit', {'selections': [{'projectPath': str(source), 'path': str(path), 'family': 'findings'}]})['result']
        result = call(3, 'semantic.begin', {'group': admitted['token'], 'sources': [{'token': admitted['sources'][0]['token'], 'sourceId': 'synthetic-findings'}], 'limits': {'maxVertices': 100000, 'maxEdges': 500000, 'maxEncodedGraphBytes': budget}})
        process.stdin.close(); assert process.wait(timeout=10) == 0
        assert path.read_bytes() == raw
        record = app / diag.NAME
        return result, json.loads(record.read_text()) if record.exists() else None
    finally:
        if process.poll() is None: process.kill(); process.wait()


@pytest.mark.parametrize('budget', [1, 512 * 1024 * 1024])
def test_actual_wrapper_preserves_helper_outcome_and_records_only_cap(tmp_path, budget):
    baseline = tmp_path / 'baseline'; baseline.mkdir()
    observed = tmp_path / 'observed'; observed.mkdir()
    original, _ = run_helper(baseline, WRAPPER.parents[1] / 'raw_reader.py', budget)
    wrapped, record = run_helper(observed, WRAPPER, budget)
    assert original['ok'] == wrapped['ok']
    if budget == 1:
        assert original['error']['diagnostic']['code'] == wrapped['error']['diagnostic']['code'] == 'resource-limit'
        frames = [frame for chain in record['exceptions'] for frame in chain['frames']]
        check = next(frame for frame in frames if frame['function'] == 'check')
        assert check['proposedEncoded'] > check['limits']['maxEncodedGraphBytes'] == 1
        assert check['committedEncoded'] <= check['limits']['maxEncodedGraphBytes']
        assert any(frame['function'] == 'append' for frame in frames)
        text = json.dumps(record)
        assert str(tmp_path) not in text and 'synthetic-findings' not in text
    else:
        assert record is None


def test_observer_preserves_exception_when_record_already_exists(tmp_path, monkeypatch):
    sys.path.insert(0, str(WRAPPER.parents[1]))
    import semantic_reader as module
    monkeypatch.chdir(tmp_path)
    marker = tmp_path / diag.NAME; marker.write_text('owned-marker')
    failure = module.SemanticReadError('resource-limit')
    def fail(self, *args, **kwargs): raise failure
    monkeypatch.setattr(module.SemanticReader, 'begin', fail)
    diag.install(module)
    with pytest.raises(module.SemanticReadError) as caught:
        module.SemanticReader.begin(object())
    assert caught.value is failure
    assert marker.read_text() == 'owned-marker'


@pytest.mark.parametrize('depth', [0, 1, 6])
def test_observe_bounds_causes_without_serializing_untrusted_error_values(depth):
    sys.path.insert(0, str(WRAPPER.parents[1]))
    import semantic_reader as module
    error = None
    for _ in range(depth):
        current = ValueError('private source value must never be serialized')
        current.__cause__ = error; error = current
    record = diag.observe(error, module)
    assert len(record['exceptions']) == min(depth, 4)
    assert all(chain == {'type': 'ValueError', 'frames': []} for chain in record['exceptions'])
    assert 'private source value' not in json.dumps(record)
