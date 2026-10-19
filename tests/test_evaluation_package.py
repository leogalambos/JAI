# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Local evaluation packaging, missing-data and digest isolation regressions."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from content_spec import canonical_hash
from evaluation_package import build_package, validate_package
from content_eval import evaluate_corpus
from release_bundle import files


def package_source(tmp_path):
    root = tmp_path / 'runtime'
    fixture = root / 'evals/content_quality/enterprise/example.json'
    fixture.parent.mkdir(parents=True)
    fixture.write_text('{"synthetic":true}\n')
    key = fixture.relative_to(root).as_posix()
    manifest = root / 'evals/content_quality/manifest.json'
    manifest.write_text(json.dumps({'enterprise_cases': [key]}))
    descriptor = {'schema_version': '1.0.0', 'package_kind': 'optional-extended-synthetic-evaluation',
                  'release': '26.10.9', 'files': {key: hashlib.sha256(fixture.read_bytes()).hexdigest()}}
    descriptor['payload_hash'] = canonical_hash(descriptor['files'])
    (root / 'content').mkdir()
    (root / 'content/evaluation-package.json').write_text(json.dumps(descriptor))
    return root, fixture


def test_extended_package_is_byte_reproducible_and_pinned(tmp_path):
    root, fixture = package_source(tmp_path)
    assert validate_package(root)['state'] == 'AVAILABLE'
    first, second = tmp_path / 'a.zip', tmp_path / 'b.zip'
    result = build_package(root, first)
    build_package(root, second)
    assert first.read_bytes() == second.read_bytes()
    assert result['file_count'] == 1
    assert not result['professional_approval']
    assert result['sha256'] in Path(str(first) + '.sha256').read_text()
    with zipfile.ZipFile(first) as archive:
        assert archive.namelist() == [fixture.relative_to(root).as_posix()]
        archive.extractall(tmp_path / 'unpacked')
    assert validate_package(root, tmp_path / 'unpacked')['state'] == 'AVAILABLE'
    with pytest.raises(FileExistsError):
        build_package(root, first)


def test_missing_changed_symlink_data_is_explicit_nonpassing(tmp_path):
    root, fixture = package_source(tmp_path)
    absent = validate_package(root, tmp_path / 'missing')
    assert absent['state'] == 'UNAVAILABLE'
    assert absent['missing_count'] == 1
    fixture.write_text('changed')
    assert validate_package(root)['state'] == 'INVALID'
    fixture.unlink()
    fixture.symlink_to(root / 'content/evaluation-package.json')
    assert validate_package(root)['state'] == 'INVALID'
    with pytest.raises(ValueError):
        build_package(root, tmp_path / 'bad.zip')


def test_descriptor_path_traversal_and_manifest_drift_fail(tmp_path):
    root, _ = package_source(tmp_path)
    path = root / 'content/evaluation-package.json'
    descriptor = json.loads(path.read_text())
    descriptor['files'] = {'evals/content_quality/enterprise/../../private': '0' * 64}
    descriptor['payload_hash'] = canonical_hash(descriptor['files'])
    path.write_text(json.dumps(descriptor))
    with pytest.raises(ValueError):
        validate_package(root)


def test_full_evaluation_missing_data_is_not_executed_and_does_not_fallback(tmp_path):
    report = evaluate_corpus(ROOT, extended_root=tmp_path)
    assert report['qualification_state'] == 'NOT_EXECUTED'
    assert report['qualification_profile'] == 'full-source'
    assert not report['pilot_pass']
    assert report['cases'] == []
    assert report['missing_case_count'] > 1000
    assert str(tmp_path) not in json.dumps(report)


def test_core_distribution_retains_small_fixtures_and_expert_data_but_not_extended(tmp_path):
    root = tmp_path / 'source'
    wanted = ['.ai/runtime/content/expert_references/adr/simple.md',
              '.ai/runtime/content/evaluation-package.json',
              '.ai/runtime/evals/content_quality/adr-simple.json',
              '.ai/runtime/tools/optional_provider_eval.py']
    excluded = ['.ai/runtime/evals/content_quality/enterprise/large.json',
                'AGENTS.md', 'JAI.zip', 'execution.log', 'build/report.json', '.pytest_cache/v/cache/nodeids',
                '.cache/tool/state', '.ruff_cache/report', '.mypy_cache/report']
    for name in wanted + excluded:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('fixture')
    assert {path.relative_to(root).as_posix() for path in files(root)} == set(wanted)
