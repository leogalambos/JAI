# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Prepare bounded canonical performance corpora, never projection-only inputs.

Usage: pinned-python -I -B corpus.py --output ABSENT_ABSOLUTE_DIRECTORY --tier pilot|S|M|L.
Every fixed tier still requires actual viewer admission before qualification.
Only maintained writers produce valid transactions; malformed tails are explicit
negative variants. No existing source directory is opened for mutation.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import random
import shutil
import sys
import tempfile
import uuid
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
SEED = 20261109
CLOCK = 1794225600.0
MAX_PILOT_BYTES = 64 * 1024 * 1024
TARGETS = {'S': (1000, 3000, 100, 10 * 1024 * 1024),
           'M': (25000, 100000, 5000, 250 * 1024 * 1024),
           'L': (100000, 500000, 20000, 1024 * 1024 * 1024)}
# bulk records, findings, degree, shards, referenced material padding, references
PARAMETERS = {'S': (175, 100, 4, 1, 1024 * 1024, 643),
              'M': (4804, 5000, 8, 8, 1024 * 1024, 32653),
              'L': (19732, 20000, 10, 32, 1024 * 1024, 180273)}
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / '.ai/runtime/tools'), str(ROOT / 'tests')]
from governed_fixtures import GovernedHarness, CONTROLLER, HUMAN
import lifecycle
import governed_delivery
import findings


def _digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def _findings(home, count):
    events = []
    records = []
    for index in range(count):
        records.append({'op': 'add', 'reviewer': 'synthetic-reviewer',
                        'target': 'unresolved synthetic subject ' + str(index % 3),
                        'findings': [{'id': f'F-{index + 1:05d}', 'title': f'Synthetic finding {index} — Ω',
                                      'severity': ('low', 'medium', 'high')[index % 3], 'kind': 'gap',
                                      'location': f'synthetic/document-{index % 4}.md:{index + 1}',
                                      'criterion': 'Synthetic canonical performance input',
                                      'evidence': 'Deterministic synthetic evidence.',
                                      'recommendation': 'Inspect the exact synthetic subject.'}]})
    with patch.object(findings, 'HOME', str(home)):
        findings.append('review', events, records)
    return home / 'review.jsonl'



class _ObservedStore(lifecycle.Store):
    """Measure only material actually read by the unchanged canonical replay."""

    def _blob(self, identifier):
        raw = super()._blob(identifier)
        self.observed_material[identifier] = len(raw)
        return raw


def _set_info(root):
    selected = [('fabric', root / 'rich/synthetic-rich.jsonl')]
    selected.extend(('fabric', path) for path in sorted(root.glob('bulk*/synthetic-bulk*.jsonl')))
    selected.append(('findings', root / 'findings/review.jsonl'))
    sources = []
    versions = uses = transactions = 0
    material = {}
    for family, path in selected:
        row = {'family': family, 'path': path.relative_to(root).as_posix(),
               'projectRoot': '.', 'byteLength': path.stat().st_size, 'sha256': _digest(path)}
        raw = path.read_bytes()
        if family == 'fabric':
            store = _ObservedStore(path, path.stem)
            store.observed_material = {}
            state = store.read()
            versions += len(state.versions); uses += len(state.states); transactions += len(state.transactions)
            row.update(sequence=len(state.transactions), head=state.head)
            for identifier, length in store.observed_material.items():
                material[(str(store.material.relative_to(root)), identifier)] = length
        else:
            events = findings._parse_events(raw, 'synthetic-performance')
            reduced = findings.state(events)
            row.update(sequence=len(events), head=events[-1]['hash'], findings=len(reduced))
        sources.append(row)
    return {'sourcePaths': sources, 'canonicalAdmission': {'status': 'passed', 'versions': versions,
            'uses': uses, 'transactions': transactions, 'findings': len(reduced)},
            'countsExpected': {'vertices': None, 'edges': None, 'findings': str(len(reduced))},
            'byteDimensions': {'selectedMetadataBytes': sum(row['byteLength'] for row in sources),
                               'uniqueReferencedMaterialBytes': sum(material.values()),
                               'explicitPaddingBytes': 0, 'materialPaddingBytes': 0, 'metadataPaddingBytes': 0,
                               'totalReferencedInputBytes': sum(row['byteLength'] for row in sources) + sum(material.values())}}


def _pad_metadata(root: Path, padding: int) -> None:
    """Distribute legal JSON whitespace over owned single-row bulk journals.

    Args:
        root: Newly created private staging variant, never an existing user source.
        padding: Exact additional bytes, spread over existing bulk transactions.
    Raises:
        ValueError: Negative padding, absent journals or a 100 MiB row overflow.
        OSError: A staged journal cannot be updated before publication.
    """
    if type(padding) is not int or padding < 0:
        raise ValueError('Nonnegative exact metadata padding required.')
    journals = sorted(root.glob('bulk*/synthetic-bulk*.jsonl'))
    if not journals:
        raise ValueError('Owned bulk journals required for metadata padding.')
    per_journal, remainder = divmod(padding, len(journals))
    allocations = [(path, per_journal + (index < remainder)) for index, path in enumerate(journals)]
    if any(path.stat().st_size + extra > 100 * 1024 * 1024 for path, extra in allocations):
        raise ValueError('Metadata padding would exceed the physical record limit.')
    for path, extra in allocations:
        if not extra:
            continue
        with path.open('r+b') as stream:
            stream.seek(-1, os.SEEK_END)
            if stream.read(1) != b'\n':
                raise ValueError('Generated journal must end with a newline.')
            stream.seek(-1, os.SEEK_END)
            remaining = extra
            while remaining:
                chunk = min(remaining, 64 * 1024)
                stream.write(b' ' * chunk)
                remaining -= chunk
            stream.write(b'\n')


def _generate(output: Path, *, bulk_records: int, finding_count: int, degree: int, bulk_shards: int, material_padding_bytes: int, tier: str = 'pilot', exact_references: int | None = None, input_bytes: int | None = None, versioned: bool = False) -> dict:
    """Generate canonical base/append and malformed variants for bounded calibration.

    Args:
        output: Absent normalized absolute destination; parent must exist.
        bulk_records: Pilot 1..100, or the exact fixed-tier input count.
        finding_count: Pilot 1..10, or the fixed-tier count; one add event each.
        degree: Pilot 0..8 earlier references, or the fixed-tier degree.
        bulk_shards: Pilot 1..4 nonempty engagements, or the fixed-tier shard count.
        material_padding_bytes: Referenced once per shard; 0..1 MiB per object.
        versioned: Add a separate canonical source-version proposal to the rich journal.
    Returns:
        Published manifest; graph counts remain unknown until the actual model oracle.
    Raises:
        ValueError: Input bounds/path contract or bounded storage envelope is violated.
        OSError: Exclusive generation or publication fails.
        AssertionError: The unchanged canonical writer rejects a prepared fixture.
    """
    output = Path(output)
    if not output.is_absolute() or output != Path(os.path.abspath(output)) or output.exists() or output.is_symlink() or not output.parent.is_dir():
        raise ValueError('An absent normalized absolute output with existing parent is required.')
    values = (bulk_records, finding_count, degree, bulk_shards, material_padding_bytes)
    pilot_valid = all(type(value) is int for value in values) and 1 <= bulk_records <= 100 and 1 <= finding_count <= 10 and 0 <= degree <= 8 and 1 <= bulk_shards <= min(4, bulk_records) and 0 <= material_padding_bytes <= 1024 * 1024
    fixed_valid = tier in PARAMETERS and values == PARAMETERS[tier][:5] and exact_references == PARAMETERS[tier][5] and input_bytes == TARGETS[tier][3]
    if type(versioned) is not bool or (tier == 'pilot' and not pilot_valid) or (tier != 'pilot' and (not fixed_valid or not versioned)):
        raise ValueError('Only bounded pilot parameters or fixed calibrated tier constructions are supported.')
    def progress(stage, message):
        if tier in TARGETS:
            print(f'Corpus {tier}: stage {stage}/5 — {message}', file=sys.stderr, flush=True)
    staging = Path(tempfile.mkdtemp(prefix='.corpus-', dir=output.parent))
    random_source = random.Random(SEED)
    def next_uuid():
        return uuid.UUID(int=random_source.getrandbits(128), version=4)
    try:
        with patch('time.time', return_value=CLOCK), patch('uuid.uuid4', side_effect=next_uuid), patch('time.strftime', return_value='2026-11-09T12:00:00+0000'):
            progress(1, f'Prepare canonical sources; {bulk_shards} bulk shards, {bulk_records} bulk records total.')
            base = staging / 'base'; base.mkdir()
            rich = GovernedHarness(base / 'rich', None, engagement='synthetic-rich')
            rich.bootstrap(); actor = rich.setup_author()
            product, record = rich.product('synthetic-result', actor)
            rich.commit(rich.submission(actor, product, record)); rich.review(actor, product)
            if versioned:
                previous = copy.deepcopy(rich.input_a)
                replacement = copy.deepcopy(rich.store.read().resolve(previous, 'source'))
                replacement['inherited'] = [previous]
                rich.record(previous['logical_id'], 'source', replacement)
            profile = copy.deepcopy(rich.store.read().resolve(rich.profile, 'profile'))
            per_shard, remainder = divmod(bulk_records, bulk_shards)
            remaining_references = exact_references
            reference_count = 0
            for shard in range(bulk_shards):
                progress(1, f'Bulk shard {shard + 1}/{bulk_shards}.')
                suffix = '' if shard == 0 else '-' + str(shard)
                count = per_shard + (shard < remainder)
                bulk = GovernedHarness(base / ('bulk' + suffix), None, engagement='synthetic-bulk' + suffix)
                material = bulk.material('Synthetic shared material — Ω.\n')
                padding = None
                if material_padding_bytes:
                    prefix = ('Synthetic padding seed ' + str(SEED) + ' shard ' + str(shard) + '\n').encode()
                    body = (prefix + bytes(range(256)) * ((material_padding_bytes + 255) // 256))[:material_padding_bytes]
                    padding = bulk.store.put_blob(body)
                items, references = [], []
                for index in range(count):
                    logical = f'synthetic-source-{index:04d}' + ('-Ω-λ-東京' if index % 7 == 0 else '')
                    if index % 97 == 0:
                        logical += '-' + 'Ωλ東京' * 20
                    width = min(index, degree)
                    if remaining_references is not None:
                        width = min(width, remaining_references)
                        remaining_references -= width
                    inherited = references[index - width:index]
                    if index > 2 and width and references[0] not in inherited:
                        inherited = [references[0], *inherited[:width - 1]]
                    reference_count += len(inherited)
                    record = {'owner': HUMAN, 'origin': HUMAN, 'source_role': 'input',
                              'material': [material, padding] if index == 0 and padding is not None else [material],
                              'criteria': [], 'inherited': copy.deepcopy(inherited)}
                    references.append(bulk.ref(logical, 'source', record))
                    items.append({'logical_id': logical, 'record': record})
                message = bulk.message('bootstrap', {'controller_id': CONTROLLER['id'], 'use_scopes': ['default'],
                                      'profile': {'logical_id': 'profile', 'record': profile}, 'l0_inputs': items})
                message['message_id'] = governed_delivery.message_id(message)
                bulk.commit(message)
            if remaining_references not in (None, 0):
                raise ValueError('Exact reference target cannot fit the bounded source records.')
            progress(2, f'Write {finding_count} finding events and verify canonical base sources.')
            _findings(base / 'findings', finding_count)
            base_info = _set_info(base)
            metadata_padding = 0
            if input_bytes is not None:
                progress(3, f'Prepare exact {input_bytes}-byte input workload and recheck canonical values.')
                metadata_padding = input_bytes - base_info['byteDimensions']['totalReferencedInputBytes']
                if metadata_padding < 0:
                    raise ValueError('Canonical metadata/material exceeds the fixed tier byte target.')
                _pad_metadata(base, metadata_padding)
                base_info = _set_info(base)
                if base_info['byteDimensions']['totalReferencedInputBytes'] != input_bytes:
                    raise ValueError('Prepared input accounting differs from its exact tier target.')
            base_info['byteDimensions'].update(materialPaddingBytes=material_padding_bytes * bulk_shards,
                                                metadataPaddingBytes=metadata_padding,
                                                explicitPaddingBytes=metadata_padding + material_padding_bytes * bulk_shards)
            expected = dict(zip(('vertices', 'edges', 'findings'), map(str, TARGETS[tier][:3]))) if tier in TARGETS else base_info['countsExpected']
            base_info['countsExpected'] = expected
            progress(4, 'Prepare separate append variant and verify its canonical sources.')
            shutil.copytree(base, staging / 'append')
            appended = staging / 'append/findings/review.jsonl'
            events = findings._parse_events(appended.read_bytes(), 'synthetic-performance')
            with patch.object(findings, 'HOME', str(appended.parent)):
                findings.append('review', events, [{'op': 'resolve', 'id': 'F-00001', 'by': 'synthetic-author',
                                                  'note': 'Separate immutable append candidate.'}])
            append_info = _set_info(staging / 'append')
            append_info['byteDimensions'].update(materialPaddingBytes=material_padding_bytes * bulk_shards,
                                                  metadataPaddingBytes=metadata_padding,
                                                  explicitPaddingBytes=metadata_padding + material_padding_bytes * bulk_shards)
            append_info['countsExpected'] = expected
            progress(5, 'Prepare separate malformed variant, check storage envelope and publish manifest.')
            shutil.copytree(base, staging / 'malformed')
            bad = staging / 'malformed/bulk/synthetic-bulk.jsonl'
            with bad.open('ab') as stream:
                stream.write(b'{"incomplete":')
            malformed_sources = copy.deepcopy(base_info['sourcePaths'])
            bad_row = next(row for row in malformed_sources if row['path'] == 'bulk/synthetic-bulk.jsonl')
            bad_row.update(byteLength=bad.stat().st_size, sha256=_digest(bad))
            size = sum(path.stat().st_size for path in staging.rglob('*') if path.is_file())
            preparation_limit = MAX_PILOT_BYTES if tier in ('pilot', 'S') else 4 * TARGETS[tier][3]
            if size > preparation_limit:
                raise ValueError('Corpus exceeds its preparation envelope (64 MiB for pilot/S; four input sets for M/L).')
            manifest = {'format': 'jai.fabric-explorer.performance-corpus/1', 'generatorVersion': 'corpus/5',
                        'tier': tier, 'seed': SEED, 'fixedClockSeconds': int(CLOCK),
                        'requestedCounts': expected if tier in TARGETS else None, 'requestedInputBytes': input_bytes, 'observedCounts': None,
                        'parameters': {'bulkRecords': bulk_records, 'findings': finding_count, 'degree': degree, 'bulkShards': bulk_shards, 'materialPaddingBytesPerShard': material_padding_bytes, 'inheritedReferences': reference_count,
                                       **({'versionedSourceProposals': 1} if versioned else {})},
                        'sourceSets': {'base': base_info, 'append': append_info,
                                       'malformed': {'sourcePaths': malformed_sources, 'canonicalAdmission': {'status': 'expected-rejection'}, 'countsExpected': None}},
                        'preparationBytes': size, 'admissionOracle': 'Canonical writers/readers passed; shipped ImportModel count oracle pending.',
                        'topology': {'bulkCausalReferences': 'Earlier exact versions only; no claimed causal cycle.',
                                     'directedAssociationCycles': 'Requires actual mapped cycle witness; no causal cycle is fabricated.',
                                     'multipleVersions': 'One exact input-A replacement registered separately; actual mapped proof required.' if versioned else 'not-established',
                                     'longUnicodeLabels': 'Every 97th bootstrap input has at least 96 Unicode code points; mapped proof required.',
                                     'components': 'Separate synthetic engagements and unresolved finding locations.',
                                     'parallelRelations': 'Distinct field occurrences are preserved by the mapper.'},
                        'provenance': [{'path': str(path.relative_to(ROOT)), 'sha256': _digest(path)} for path in
                                       [Path(__file__), ROOT / 'tests/governed_fixtures.py', ROOT / '.ai/runtime/tools/lifecycle.py', ROOT / '.ai/runtime/tools/findings.py']]}
            (staging / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        staging.rename(output)
        return manifest
    except BaseException:
        shutil.rmtree(staging)
        raise



def generate_pilot(output: Path, *, bulk_records: int = 24, finding_count: int = 10, degree: int = 2, bulk_shards: int = 1, material_padding_bytes: int = 0, versioned: bool = False) -> dict:
    """Publish a bounded canonical pilot without asserting unmeasured graph counts.

    Args:
        output: Absent normalized absolute directory with an existing parent.
        bulk_records: Total ordinary inputs, 1..100.
        finding_count: Findings, 1..10.
        degree: Maximum earlier inheritance references per record, 0..8.
        bulk_shards: Nonempty independent engagements, 1..4 and at most bulk_records.
        material_padding_bytes: One referenced object per shard, 0..1 MiB each.
        versioned: Register an additional exact version of the rich journal's input-A.
    Returns:
        Manifest with canonical admission and graph dimensions pending actual oracle.
    Raises:
        ValueError: Bounds, publication path or preparation envelope is invalid.
        OSError: Canonical fixture preparation or publication fails.
    """
    return _generate(output, bulk_records=bulk_records, finding_count=finding_count, degree=degree,
                     bulk_shards=bulk_shards, material_padding_bytes=material_padding_bytes, versioned=versioned)


def generate_fixed(output: Path, tier: str) -> dict:
    """Prepare one fixed canonical S/M/L candidate with exact input/count targets.

    Args:
        output: Absent normalized absolute directory with an existing parent.
        tier: S, M or L; construction parameters cannot be overridden.
    Returns:
        Manifest with expected counts; actual viewer admission remains required.
    Raises:
        ValueError: Unsupported tier or exhausted input/preparation/record envelope.
        OSError: Exclusive preparation/publication fails.
    """
    if tier not in PARAMETERS:
        raise ValueError('Supported fixed corpus tier required.')
    records, findings_count, degree, shards, material_padding, references = PARAMETERS[tier]
    return _generate(output, tier=tier, bulk_records=records, finding_count=findings_count,
                     degree=degree, bulk_shards=shards, material_padding_bytes=material_padding,
                     exact_references=references, input_bytes=TARGETS[tier][3], versioned=True)


def generate_small_s(output: Path) -> dict:
    """Prepare the fixed S candidate; see generate_fixed for output and error contracts.

    Args:
        output: Absent normalized absolute directory with an existing parent.
    Returns:
        S manifest with exact expected counts and a 10 MiB input target.
    Raises:
        ValueError: Input or preparation bounds are exhausted.
        OSError: Exclusive preparation/publication fails.
    """
    return generate_fixed(output, 'S')


def main() -> int:
    """Publish a bounded pilot or fixed S/M/L canonical candidate.

    Returns:
        Zero after successful exclusive pilot publication.
    Raises:
        ValueError: Requested tier is not yet supported or input is invalid.
        OSError: Fixture generation/publication fails.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--tier', required=True, choices=['pilot', *TARGETS])
    parser.add_argument('--bulk-records', type=int, default=24)
    parser.add_argument('--findings', type=int, default=10)
    parser.add_argument('--degree', type=int, default=2)
    parser.add_argument('--bulk-shards', type=int, default=1)
    parser.add_argument('--material-padding-bytes', type=int, default=0)
    args = parser.parse_args()
    if args.tier in TARGETS:
        if any(value != default for value, default in ((args.bulk_records, 24), (args.findings, 10), (args.degree, 2), (args.bulk_shards, 1), (args.material_padding_bytes, 0))):
            raise ValueError('Fixed tiers use calibrated parameters, without pilot overrides.')
        result = generate_fixed(args.output, args.tier)
    else:
        result = generate_pilot(args.output, bulk_records=args.bulk_records, finding_count=args.findings, degree=args.degree, bulk_shards=args.bulk_shards, material_padding_bytes=args.material_padding_bytes)
    print(json.dumps({'manifest': str(args.output / 'manifest.json'), 'tier': result['tier'], 'preparationBytes': result['preparationBytes']}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
