# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Read-only source probe checks before native experimental packaging."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from governed_fixtures import GovernedHarness

ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / 'apps/fabric-explorer/experiments/helper/probe.py'
FINDINGS = ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl'


def _smoke_module():
    path = PROBE.with_name('smoke_probe.py')
    specification = importlib.util.spec_from_file_location('tested_reader_smoke', path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def _run(*arguments):
    environment = {**os.environ, 'PATH': '', 'FINDINGS_MAX_ROUNDS': '1'}
    completed = subprocess.run([sys.executable, '-I', '-B', str(PROBE), *arguments],
                               capture_output=True, text=True, env=environment, timeout=30)
    return completed.returncode, json.loads(completed.stdout)


def _manifest(root):
    return {p.relative_to(root).as_posix(): 'directory' if p.is_dir()
            else hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*'))}


def test_source_probe_replays_ordinary_history_without_modifying_inputs(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path / 'source', monkeypatch)
    host.bootstrap()
    host.qualified_answer(text='Synthetic reader source probe only.')
    before = _manifest(host.directory)
    expected = host.store.read()
    code, result = _run('fabric', '--journal', str(host.path), '--engagement', host.engagement)
    assert code == 0 and result['history_verified']
    assert result['head'] == expected.head
    assert result['transactions'] == len(expected.transactions)
    assert result['versions'] == len(expected.versions)
    assert set(result['families']) == {'delivery.' + name for name in (
        'source', 'profile', 'assignment', 'context', 'product', 'assessment', 'decision')}
    assert not result['authority_granted'] and not result['current_assessment']
    assert _manifest(host.directory) == before
    assert host._human_signer is None


def test_findings_configuration_is_explicit_and_unknown_when_omitted():
    before = FINDINGS.read_bytes()
    code, unknown = _run('findings', '--journal', str(FINDINGS))
    assert code == 0 and unknown['round_configuration'] == 'unknown'
    assert unknown['recorded_states'] is None and not unknown['history_verified']
    code, configured = _run('findings', '--journal', str(FINDINGS), '--max-rounds', '3')
    assert code == 0 and configured['chain_verified']
    assert configured['recorded_states'] == {name: 1 for name in (
        'open', 'resolved', 'verified', 'stuck', 'withdrawn', 'accepted')}
    assert FINDINGS.read_bytes() == before


def test_diagnostic_format_never_claims_canonical_history(tmp_path):
    source = tmp_path / 'archive.jsonl'
    source.write_text('{"format":8}\n')
    code, diagnostic = _run('diagnostic', '--journal', str(source))
    assert code == 0 and diagnostic['decoded_rows'] == 1
    assert not diagnostic['history_verified'] and diagnostic['semantic_state'] == 'unknown'
    code, rejected = _run('fabric', '--journal', str(source), '--engagement', 'synthetic')
    assert code == 2 and not rejected['history_verified']
    assert source.read_text() == '{"format":8}\n'


@pytest.mark.parametrize('mode', ['fabric', 'findings', 'diagnostic'])
def test_missing_sources_are_not_initialized(tmp_path, mode):
    source = tmp_path / 'missing.jsonl'
    arguments = ['--engagement', 'synthetic'] if mode == 'fabric' else []
    code, result = _run(mode, '--journal', str(source), *arguments)
    assert code == 2 and result['status'] == 'rejected'
    assert not source.exists() and list(tmp_path.iterdir()) == []


def test_tampered_findings_are_rejected_without_repair(tmp_path):
    source = tmp_path / 'tampered.jsonl'
    raw = FINDINGS.read_bytes().replace(b'Synthetic example 1', b'Tampered example 1')
    source.write_bytes(raw)
    code, result = _run('findings', '--journal', str(source), '--max-rounds', '3')
    assert code == 2 and not result['history_verified']
    assert source.read_bytes() == raw


@pytest.mark.parametrize('target', ['new-report', 'existing-journal', 'ancestor-symlink', 'file-symlink'])
def test_smoke_report_cannot_write_selected_fixture_tree(tmp_path, target):
    fixtures = tmp_path / 'selected'
    fixtures.mkdir()
    journal = fixtures / 'source.jsonl'
    journal.write_text('Synthetic immutable source\n')
    if target == 'new-report':
        report = fixtures / 'new-observation.json'
    elif target == 'existing-journal':
        report = journal
    elif target == 'ancestor-symlink':
        alias = tmp_path / 'alias'
        try:
            alias.symlink_to(fixtures, target_is_directory=True)
        except OSError as error:
            pytest.skip(f'Host cannot create a directory symlink: {error}')
        report = alias / 'new-observation.json'
    else:
        report = tmp_path / 'report-alias.json'
        try:
            report.symlink_to(journal)
        except OSError as error:
            pytest.skip(f'Host cannot create a file symlink: {error}')
    before = _manifest(fixtures)
    with pytest.raises(ValueError, match='Report output must be outside selected fixtures'):
        _smoke_module().main(['--executable', str(tmp_path / 'not-needed'),
                              '--fixtures', str(fixtures), '--report', str(report)])
    assert _manifest(fixtures) == before
    assert journal.read_text() == 'Synthetic immutable source\n'


def test_smoke_report_rejects_hardlinked_source_alias(tmp_path):
    fixtures = tmp_path / 'selected'
    fixtures.mkdir()
    journal = fixtures / 'source.jsonl'
    journal.write_text('Synthetic immutable source\n')
    report = tmp_path / 'report.json'
    os.link(journal, report)
    before = _manifest(fixtures)
    with pytest.raises(ValueError, match='singly-linked regular file'):
        _smoke_module().main(['--executable', str(tmp_path / 'not-needed'),
                              '--fixtures', str(fixtures), '--report', str(report)])
    assert _manifest(fixtures) == before
    assert report.read_bytes() == journal.read_bytes()


def test_smoke_report_allows_a_distinct_sibling_output_tree(tmp_path):
    fixtures = tmp_path / 'selected'
    fixtures.mkdir()
    report = tmp_path / 'selected-results' / 'report.json'
    assert _smoke_module()._report_destination(report, fixtures) == report.resolve()
    assert not report.parent.exists()


@pytest.mark.skipif(os.name != 'nt', reason='Windows case-insensitive path behavior requires native Windows')
def test_smoke_report_rejects_case_aliased_fixture_path(tmp_path):
    fixtures = tmp_path / 'SelectedFixture'
    fixtures.mkdir()
    report = Path(str(fixtures).swapcase()) / 'report.json'
    with pytest.raises(ValueError, match='Report output must be outside selected fixtures'):
        _smoke_module().main(['--executable', str(tmp_path / 'not-needed.exe'),
                              '--fixtures', str(fixtures), '--report', str(report)])
    assert list(fixtures.iterdir()) == []
