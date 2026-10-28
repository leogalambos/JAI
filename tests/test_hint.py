# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Deterministic advisory selection, failure boundaries and installed CLI tests."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.ai/runtime'


def selector(path=RUNTIME / 'demo/hint.py'):
    spec = importlib.util.spec_from_file_location('hint', path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.pop(0)
    return mod


def test_assessment_and_remediation_are_both_covered():
    result = selector().select_candidates(['assess architecture security', 'track remediation'])
    ids = [c['id'] for c in result['candidates']]
    assert 'security-assessment' in ids and 'vulnerability-remediation' in ids
    assert result['unmatched_goals'] == []
    assert all(c['reasons'] and c['applicability_limits'] for c in result['candidates'])
    assert result['interpretation'] == 'Active provider supplies structured English goals; no translation executed.'


def test_no_match_does_not_use_domain_filter_as_a_reason_to_force_results():
    result = selector().select_candidates(['bake sourdough bread'], domains=['security'])
    assert result['status'] == 'NO_MATCH'
    assert result['candidates'] == []
    assert result['unmatched_goals'] == ['bake sourdough bread']


def test_partial_match_preserves_uncovered_goal():
    result = selector().select_candidates(['assess architecture security', 'bake sourdough bread'])
    assert result['status'] == 'PARTIAL_MATCH'
    assert result['unmatched_goals'] == ['bake sourdough bread']


def test_limit_filters_and_tie_order_are_stable():
    mod = selector()
    result = mod.select_candidates(['review architecture'], limit=1, domains=['architecture'], phases=['review'])
    assert len(result['candidates']) == 1
    assert result == mod.select_candidates(['review architecture'], limit=1, domains=['architecture'], phases=['review'])
    tied = mod._rank(mod.load_catalog(require_discovery=True), ['security'], [], [], 10)
    ordering = [(c['score'], c['id']) for c in tied]
    assert ordering == sorted(ordering, key=lambda x: (-x[0], x[1]))


@pytest.mark.parametrize('kwargs', [
    {'goals': []}, {'goals': ['']}, {'goals': ['x'] * 9},
    {'goals': ['x' * 301]}, {'goals': ['proposal'], 'limit': 0},
    {'goals': ['proposal'], 'limit': 11}, {'goals': ['proposal'], 'limit': True},
    {'goals': ['proposal'], 'domains': ['made-up']},
    {'goals': ['proposal'], 'phases': ['made-up']},
])
def test_invalid_queries_fail_explicitly(kwargs):
    with pytest.raises(ValueError):
        selector().select_candidates(**kwargs)


def test_malformed_catalog_is_not_silently_replaced(tmp_path):
    mod = selector()
    path = tmp_path / 'scenarios.json'
    path.write_text('{broken')
    mod.CATALOG = path
    with pytest.raises(ValueError, match='catalog'):
        mod.select_candidates(['proposal'])


def test_main_emits_json_and_explicit_error(capsys):
    mod = selector()
    assert mod.main(['--goal', 'supplier proposal']) == 0
    assert json.loads(capsys.readouterr().out)['candidates'][0]['id'] == 'proposal'
    assert mod.main(['--goal', 'proposal', '--domain', 'unknown']) == 2
    assert json.loads(capsys.readouterr().out)['status'] == 'ERROR'


def test_installed_cli_is_read_only_without_docs_from_any_cwd(tmp_path):
    target = tmp_path / 'house'
    shutil.copytree(RUNTIME / 'demo', target / 'demo', ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copy2(RUNTIME / 'workflows.json', target / 'workflows.json')
    before = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
    marker = tmp_path / 'must-not-exist'
    # Relative targets keep all shell forms within the goal-length contract
    # regardless of pytest's temporary-root length; execution uses that cwd.
    hostile = f'bake bread; touch {marker.name}; $(touch {marker.name}) `touch {marker.name}`'
    assert len(hostile) <= 300
    cmd = [sys.executable, '-B', str(target / 'demo/hint.py'), '--goal', hostile]
    proc = subprocess.run(cmd, cwd=tmp_path, text=True, capture_output=True, check=True)
    assert json.loads(proc.stdout)['status'] == 'NO_MATCH'
    assert not marker.exists()
    assert before == {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
    proc = subprocess.run([sys.executable, '-B', str(target / 'demo/hint.py'), '--goal', 'supplier proposal'], cwd=tmp_path, text=True, capture_output=True, check=True)
    assert json.loads(proc.stdout)['candidates'][0]['id'] == 'proposal'
    (target / 'workflows.json').write_text('{broken')
    proc = subprocess.run(cmd, cwd=tmp_path, text=True, capture_output=True)
    assert proc.returncode == 2
    error = json.loads(proc.stdout)
    assert error['status'] == 'ERROR' and 'candidates' not in error


def test_truncation_does_not_claim_discarded_goal_coverage():
    result = selector().select_candidates(['assess architecture security', 'track remediation'], limit=1)
    assert result['status'] == 'PARTIAL_MATCH'
    assert result['unmatched_goals'] == ['track remediation']


def test_cli_does_not_accept_arbitrary_catalog_paths(tmp_path):
    proc = subprocess.run([sys.executable, '-B', str(RUNTIME / 'demo/hint.py'),
                           '--goal', 'proposal', '--catalog', str(tmp_path / 'other.json')],
                          text=True, capture_output=True)
    assert proc.returncode == 2
    assert 'unrecognized arguments' in proc.stderr
    assert not proc.stdout
