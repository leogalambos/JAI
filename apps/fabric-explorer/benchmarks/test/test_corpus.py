# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Canonical generator pilot boundaries; no performance thresholds are measured here."""
import importlib.util
import json
from pathlib import Path
import subprocess

import pytest

MODULE = Path(__file__).resolve().parents[1] / 'corpus.py'
SPEC = importlib.util.spec_from_file_location('performance_corpus', MODULE)
corpus = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(corpus)
PYTHON = corpus.ROOT / 'build/fabric-explorer/helper-venv/bin/python'


@pytest.fixture(scope='module')
def pilot(tmp_path_factory):
    """Prepare one real bounded canonical pilot shared by immutable assertions."""
    root = tmp_path_factory.mktemp('canonical-performance') / 'pilot'
    return root, corpus.generate_pilot(root, bulk_records=5, finding_count=3, degree=2)


def test_pilot_uses_canonical_sources_and_preserves_separate_variant_states(pilot):
    root, manifest = pilot
    assert manifest['tier'] == 'pilot' and manifest['seed'] == 20261109
    assert manifest['observedCounts'] is None and manifest['requestedCounts'] is None
    assert manifest['sourceSets']['base']['canonicalAdmission']['status'] == 'passed'
    assert manifest['sourceSets']['base']['countsExpected']['findings'] == '3'
    assert len(manifest['sourceSets']['base']['sourcePaths']) == 3
    base = root / 'base/findings/review.jsonl'
    appended = root / 'append/findings/review.jsonl'
    before = corpus.findings._parse_events(base.read_bytes(), 'test')
    after = corpus.findings._parse_events(appended.read_bytes(), 'test')
    assert len(before) == 3 and len(after) == 4
    assert corpus.findings.state(before)['F-00001']['state'] == 'open'
    assert corpus.findings.state(after)['F-00001']['state'] == 'resolved'
    assert appended.read_bytes().startswith(base.read_bytes())
    bad = root / 'malformed/bulk/synthetic-bulk.jsonl'
    with pytest.raises(ValueError):
        corpus.lifecycle.Store(bad, 'synthetic-bulk').read()
    accounting = manifest['sourceSets']['base']['byteDimensions']
    assert accounting['totalReferencedInputBytes'] == accounting['selectedMetadataBytes'] + accounting['uniqueReferencedMaterialBytes']
    assert accounting['explicitPaddingBytes'] == 0
    assert manifest['preparationBytes'] <= corpus.MAX_PILOT_BYTES


def test_seed_and_clock_make_source_snapshots_reproducible(pilot, tmp_path):
    _root, first = pilot
    second = corpus.generate_pilot(tmp_path / 'other', bulk_records=5, finding_count=3, degree=2)
    assert second['sourceSets'] == first['sourceSets']


def test_pilot_parameter_and_destination_failures_are_bounded(tmp_path):
    for values in [(0, 1, 0), (101, 1, 0), (1, 0, 0), (1, 11, 0), (1, 1, -1), (1, 1, 9), (True, 1, 0)]:
        with pytest.raises(ValueError):
            corpus.generate_pilot(tmp_path / 'absent', bulk_records=values[0], finding_count=values[1], degree=values[2])
    with pytest.raises(ValueError):
        corpus.generate_pilot(tmp_path)
    with pytest.raises(ValueError):
        corpus.generate_pilot(Path('relative'))
    assert list(tmp_path.iterdir()) == []


def test_cli_refuses_large_tier_parameter_overrides_before_generating(tmp_path):
    result = subprocess.run([str(PYTHON), '-I', '-B', str(MODULE), '--output', str(tmp_path / 'large'), '--tier', 'L', '--bulk-records', '1'],
                            capture_output=True, text=True, check=False)
    assert result.returncode != 0 and 'without pilot overrides' in result.stderr
    assert not (tmp_path / 'large').exists()


def test_largest_pilot_and_failed_publication_cleanup(tmp_path, monkeypatch):
    result = corpus.generate_pilot(tmp_path / 'boundary', bulk_records=100, finding_count=10, degree=8)
    assert result['sourceSets']['base']['canonicalAdmission']['findings'] == 10
    assert result['parameters'] == {'bulkRecords': 100, 'findings': 10, 'degree': 8, 'bulkShards': 1, 'materialPaddingBytesPerShard': 0, 'inheritedReferences': 764}
    monkeypatch.setattr(corpus, 'MAX_PILOT_BYTES', 1)
    with pytest.raises(ValueError, match='64 MiB'):
        corpus.generate_pilot(tmp_path / 'rejected', bulk_records=1, finding_count=1, degree=0)
    assert not (tmp_path / 'rejected').exists()
    assert not list(tmp_path.glob('.corpus-*'))


def test_material_accounting_excludes_unreferenced_files(pilot, tmp_path):
    root, manifest = pilot
    import shutil
    scratch = tmp_path / 'copy'
    shutil.copytree(root / 'base', scratch)
    unused = scratch / 'bulk/synthetic-bulk.jsonl.blobs' / ('f' * 64)
    unused.write_bytes(b'Unreferenced synthetic bytes do not qualify input size.' * 100)
    observed = corpus._set_info(scratch)
    assert observed['byteDimensions'] == manifest['sourceSets']['base']['byteDimensions']


def test_independent_bulk_shards_remain_bounded_canonical_sources(tmp_path):
    manifest = corpus.generate_pilot(tmp_path / 'sharded', bulk_records=4, finding_count=1, degree=1, bulk_shards=4)
    sources = manifest['sourceSets']['base']['sourcePaths']
    assert len(sources) == 6
    assert len({source['path'] for source in sources}) == 6
    assert manifest['sourceSets']['base']['canonicalAdmission']['status'] == 'passed'
    assert manifest['parameters']['bulkShards'] == 4
    for shards in (0, 5, 2, True):
        with pytest.raises(ValueError):
            corpus.generate_pilot(tmp_path / 'absent', bulk_records=1, bulk_shards=shards)


def test_padding_is_bounded_and_referenced_exactly_once(tmp_path):
    output = tmp_path / 'padding'
    manifest = corpus.generate_pilot(output, bulk_records=2, finding_count=1, degree=0, material_padding_bytes=4096)
    state = corpus.lifecycle.Store(output / 'base/bulk/synthetic-bulk.jsonl', 'synthetic-bulk').read()
    sources = [value['content']['record'] for value in state.versions.values() if value['kind'] == 'delivery.source']
    assert [len(source['material']) for source in sources] == [2, 1]
    identifier = sources[0]['material'][1]
    assert (output / 'base/bulk/synthetic-bulk.jsonl.blobs' / identifier).stat().st_size == 4096
    assert manifest['sourceSets']['base']['byteDimensions']['materialPaddingBytes'] == 4096
    for value in (-1, 1024 * 1024 + 1, True):
        with pytest.raises(ValueError):
            corpus.generate_pilot(tmp_path / 'absent', material_padding_bytes=value)


def test_fixed_s_candidate_has_exact_input_bytes_and_explicit_count_expectations(tmp_path):
    output = tmp_path / 'small'
    manifest = corpus.generate_small_s(output)
    expected = {'vertices': '1000', 'edges': '3000', 'findings': '100'}
    assert manifest['tier'] == 'S' and manifest['requestedCounts'] == expected
    assert manifest['observedCounts'] is None
    assert manifest['sourceSets']['base']['countsExpected'] == expected
    assert manifest['sourceSets']['append']['countsExpected'] == expected
    dimensions = manifest['sourceSets']['base']['byteDimensions']
    assert dimensions['totalReferencedInputBytes'] == 10 * 1024 * 1024
    assert dimensions['totalReferencedInputBytes'] == dimensions['selectedMetadataBytes'] + dimensions['uniqueReferencedMaterialBytes']
    assert dimensions['materialPaddingBytes'] == 1024 * 1024
    assert dimensions['metadataPaddingBytes'] > 0
    assert dimensions['explicitPaddingBytes'] == dimensions['materialPaddingBytes'] + dimensions['metadataPaddingBytes']
    state = corpus.lifecycle.Store(output / 'base/bulk/synthetic-bulk.jsonl', 'synthetic-bulk').read()
    sources = [value['content']['record'] for value in state.versions.values() if value['kind'] == 'delivery.source']
    assert len(sources) == 175 and sum(len(value['inherited']) for value in sources) == 643
    assert any(len(value['logical_id']) >= 96 and not value['logical_id'].isascii() for value in state.versions.values() if value['kind'] == 'delivery.source')
    assert max(len(value['inherited']) for value in sources) == 4
    assert manifest['preparationBytes'] <= corpus.MAX_PILOT_BYTES


def test_fixed_s_cli_rejects_pilot_overrides_before_io(tmp_path):
    result = subprocess.run([str(PYTHON), '-I', '-B', str(MODULE), '--output', str(tmp_path / 'invalid'),
                             '--tier', 'S', '--bulk-records', '1'], capture_output=True, text=True, check=False)
    assert result.returncode != 0 and 'without pilot overrides' in result.stderr
    assert not (tmp_path / 'invalid').exists()


def test_metadata_padding_is_distributed_without_changing_canonical_values(tmp_path):
    output = tmp_path / 'distributed'
    manifest = corpus.generate_pilot(output, bulk_records=4, finding_count=1, degree=0, bulk_shards=4)
    before = manifest['sourceSets']['base']
    paths = sorted((output / 'base').glob('bulk*/synthetic-bulk*.jsonl'))
    original = {path: path.read_bytes() for path in paths}
    padding = 1024 * 1024 + 7
    corpus._pad_metadata(output / 'base', padding)
    after = corpus._set_info(output / 'base')
    assert after['canonicalAdmission'] == before['canonicalAdmission']
    before_heads = [(row['head'], row['sequence']) for row in before['sourcePaths']]
    assert [(row['head'], row['sequence']) for row in after['sourcePaths']] == before_heads
    deltas = [path.stat().st_size - len(original[path]) for path in paths]
    assert sum(deltas) == padding and max(deltas) - min(deltas) == 1
    for path in paths:
        assert json.loads(path.read_bytes()) == json.loads(original[path])
    frozen = {path: corpus._digest(path) for path in paths}
    corpus._pad_metadata(output / 'base', 0)
    for invalid in (-1, True, 4 * 100 * 1024 * 1024):
        with pytest.raises(ValueError):
            corpus._pad_metadata(output / 'base', invalid)
    assert {path: corpus._digest(path) for path in paths} == frozen
    with pytest.raises(ValueError):
        corpus.generate_fixed(tmp_path / 'unsupported', 'XL')
    assert not (tmp_path / 'unsupported').exists()


def test_reference_pilot_preserves_distinct_versions_of_the_same_logical_source(tmp_path):
    output = tmp_path / 'versioned'
    corpus.generate_pilot(output, bulk_records=2, finding_count=1, degree=1, versioned=True)
    state = corpus.lifecycle.Store(output / 'base/rich/synthetic-rich.jsonl', 'synthetic-rich').read()
    sources = [(identifier, value) for identifier, value in state.versions.items() if value['kind'] == 'delivery.source' and value['logical_id'] == 'input-A']
    assert len(sources) == 2 and sources[0][1]['logical_id'] == sources[1][1]['logical_id']
    assert sources[0][0] != sources[1][0]
