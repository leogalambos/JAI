# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Viewer-owned real-reader parity and retained-capture negative integration cases."""
import hashlib
import json
from pathlib import Path
import struct
import sys

import pytest

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / 'apps/fabric-explorer/reader'), str(ROOT / '.ai/runtime/tools'), str(ROOT / 'tests')]
import findings
import lifecycle as lc
from readonly_files import ReadOnlyRoot
from governed_fixtures import GovernedHarness
from raw_reader import Reader
from semantic_reader import SemanticReader, SemanticReadError, _tag, _preflight

LIMITS = {'maxVertices': 100000, 'maxEdges': 500000, 'maxEncodedGraphBytes': 512 * 1024 * 1024}


def test_preflight_padding_does_not_expand_python_scanner_work():
    """Legal outer JSON padding must not add one Python iteration per byte."""
    def work(raw):
        events = 0
        def trace(frame, event, _argument):
            nonlocal events
            if frame.f_code is _preflight.__code__ and event == 'line':
                events += 1
            return trace
        previous = sys.gettrace()
        try:
            sys.settrace(trace)
            _preflight(raw)
        finally:
            sys.settrace(previous)
        return events
    body = json.dumps({'text': 'quoted [ { } ] and escaped " text'}).encode()
    assert work(b' \t' + body + b' ' * 65536 + b'\r\n') <= 2 * work(body) + 8


def test_preflight_keeps_raw_size_and_quoted_depth_guards_before_padding_trim(monkeypatch):
    import semantic_reader as module
    monkeypatch.setattr(module, 'RECORD', 128)
    _preflight(b'{}' + b' ' * 126)
    with pytest.raises(SemanticReadError):
        _preflight(b'{}' + b' ' * 127)
    monkeypatch.setattr(module, 'RECORD', 1024)
    _preflight(b' ' * 16 + b'[' * 64 + b'0' + b']' * 64 + b'\t\r\n')
    with pytest.raises(SemanticReadError):
        _preflight(b'\t' + b'[' * 65 + b'0' + b']' * 65 + b' ' * 16)
    quoted = json.dumps({'text': ' [ ] { } \\"' * 100 + '   '}).encode()
    monkeypatch.setattr(module, 'RECORD', len(quoted) + 64)
    _preflight(b'\t' + quoted + b' ' * 32)
    assert json.loads(b'\t' + quoted + b' ' * 32)['text'].endswith('   ')


@pytest.fixture
def environment(tmp_path, monkeypatch):
    data = tmp_path / 'data'; data.mkdir()
    app = tmp_path / 'app'; app.mkdir()
    monkeypatch.chdir(app)
    reader = Reader(ReadOnlyRoot, [app]); semantic = SemanticReader(reader, lc, findings); reader.semantic = semantic
    yield data, app, reader, semantic
    reader.close()


def admitted(reader, path, family):
    raw = reader.admit([{'projectPath': str(path.parent), 'path': str(path), 'family': family}])
    return raw['token'], [{'token': raw['sources'][0]['token'], 'sourceId': 'synthetic-' + family}]


def all_facts(semantic, group, lease):
    result = []; cursor = None; sequence = 0
    while True:
        chunk = semantic.chunk(group, lease, cursor)
        assert chunk['sequence'] == str(sequence)
        result.extend(chunk['facts']); cursor = chunk['next']; sequence += 1
        if cursor is None: return result
        assert chunk['facts']


def test_fabric_matches_canonical_versions_scopes_dependencies_and_exact_capture(environment, monkeypatch):
    data, _, reader, semantic = environment
    harness = GovernedHarness(data, monkeypatch, engagement='viewer-parity'); harness.bootstrap(); actor = harness.setup_author()
    product, product_record = harness.product('viewer-result', actor)
    harness.commit(harness.submission(actor, product, product_record)); harness.review(actor, product)
    before = {p.relative_to(data).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in data.rglob('*') if p.is_file()}
    group, sources = admitted(reader, harness.path, 'fabric'); result = semantic.begin(group, sources, LIMITS)
    facts = all_facts(semantic, group, result['leaseId']); canonical = harness.store.read()
    versions = [fact for fact in facts if fact['kind'] == 'version']; uses = [fact for fact in facts if fact['kind'] == 'use']
    assert {fact['ref']['version_id'] for fact in versions} == set(canonical.versions)
    assert {fact['family'] for fact in versions} == {'source', 'profile', 'assignment', 'context', 'product', 'assessment', 'decision'}
    historical_assignment = [fact for fact in facts if fact['kind'] == 'reference' and fact['originRef'] == product and fact['fieldPointer'] == '/assignment' and fact['originUseScope'] is not None]
    assert historical_assignment and all(fact['historicalCausal'] and not fact['governing'] for fact in historical_assignment)
    assert {(fact['point']['use_scope'], fact['point']['ref']['version_id']) for fact in uses} == set(canonical.states)
    references = [fact for fact in facts if fact['kind'] == 'reference' and fact['originUseScope'] is not None]
    for fact in references:
        record = canonical.resolve(fact['originRef'])
        assert fact['historicalCausal'] == (fact['fieldPointer'] in dict(lc._causal_reference_paths(record)))
        previous = canonical.scope; canonical.scope = fact['originUseScope']
        try: point = canonical._dependency_point(record, fact['fieldPointer'], fact['targetRef'])
        finally: canonical.scope = previous
        assert point == {'ref': fact['targetRef'], 'use_scope': fact['targetUseScope']}
    summary = result['sources'][0]; raw = harness.path.read_bytes()
    assert summary['digest'] == hashlib.sha256(raw).hexdigest() and summary['head'] == canonical.head
    assert summary['sequence'] == str(len(canonical.transactions))
    assert summary['verification']['replay'] == 'recorded' and summary['verification']['authorityGranted'] is False
    for fact in versions:
        origin = fact['origin']; line = raw[int(origin['byteOffset']):int(origin['byteOffset']) + int(origin['byteLength'])]
        row = json.loads(line); selected = row
        for part in origin['pointer'].strip('/').split('/'): selected = selected[int(part)] if isinstance(selected, list) else selected[part]
        assert lc.version_id(selected) == fact['ref']['version_id']
    capture = summary['captureToken']; harness.path.write_bytes(b'changed after immutable capture')
    rebuilt = b''
    while len(rebuilt) < len(raw):
        page, eof = semantic.page(group, result['leaseId'], capture, str(len(rebuilt)), 262144)
        rebuilt += page
        assert eof == (len(rebuilt) == len(raw))
    assert rebuilt == raw
    harness.path.write_bytes(raw)
    assert before == {p.relative_to(data).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in data.rglob('*') if p.is_file()}


def test_exact_prefix_projection_reuses_parsed_history_and_projects_only_appended_suffix(environment, monkeypatch):
    data, _, reader, semantic = environment
    harness = GovernedHarness(data, monkeypatch, engagement='viewer-prefix'); harness.bootstrap()
    selected = data / 'selected.jsonl'; original_bytes = harness.path.read_bytes(); selected.write_bytes(original_bytes)
    # Canonical writer uses atomic publication; this case deliberately tests
    # byte-prefix append on an independently admitted unchanged leaf identity.
    (data / 'selected.jsonl.blobs').mkdir()
    for material in (data / (harness.path.name + '.blobs')).iterdir():
        (data / 'selected.jsonl.blobs' / material.name).write_bytes(material.read_bytes())
    group, sources = admitted(reader, selected, 'fabric')
    first = semantic.begin(group, sources, LIMITS); semantic.release(group, first['leaseId'])
    from recorded_projection import _RecordedProjection
    original = _RecordedProjection.append; calls = []
    def project(state, transaction):
        calls.append(transaction['sequence']); return original(state, transaction)
    monkeypatch.setattr(_RecordedProjection, 'append', project)
    unchanged = semantic.begin(group, sources, LIMITS); semantic.release(group, unchanged['leaseId']); assert calls == []
    prior = len(harness.store.read().transactions); harness.setup_author(); calls.clear()
    complete = harness.path.read_bytes(); assert complete.startswith(original_bytes)
    for material in (data / (harness.path.name + '.blobs')).iterdir():
        target = data / 'selected.jsonl.blobs' / material.name
        if not target.exists(): target.write_bytes(material.read_bytes())
    with selected.open('ab') as stream: stream.write(complete[len(original_bytes):])
    result = semantic.begin(group, sources, LIMITS)
    assert calls == list(range(prior + 1, int(result['sources'][0]['sequence']) + 1))


def test_findings_match_canonical_states_tags_and_historical_round_uncertainty(environment):
    data, _, reader, semantic = environment
    raw = (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes()
    path = data / 'review.jsonl'; path.write_bytes(raw)
    group, sources = admitted(reader, path, 'findings'); result = semantic.begin(group, sources, LIMITS)
    facts = all_facts(semantic, group, result['leaseId']); expected = findings.state(findings._parse_events(raw, 'fixture'))
    assert {fact['findingId']: fact['state'] for fact in facts} == {key: value['state'] for key, value in expected.items()}
    assert all(fact['effectiveMaxRounds'] == findings.MAX_ROUNDS and not fact['historicalMaxRoundsKnown'] for fact in facts)
    assert {fact['state'] for fact in facts} == {'open', 'resolved', 'verified', 'stuck', 'withdrawn', 'accepted'}
    assert path.read_bytes() == raw
    assert _tag(9007199254740993) == {'type': 'integer', 'value': '9007199254740993'}
    assert _tag(-0.0) == {'type': 'float64', 'bits': struct.pack('>d', -0.0).hex()}


@pytest.mark.parametrize('mutation', ['unknown-format', 'truncated', 'duplicate-json', 'depth'])
def test_failed_candidate_keeps_previous_capture_and_reports_source(environment, monkeypatch, mutation):
    data, _, reader, semantic = environment
    harness = GovernedHarness(data, monkeypatch, engagement='viewer-reject'); harness.bootstrap()
    group, sources = admitted(reader, harness.path, 'fabric'); accepted = semantic.begin(group, sources, LIMITS)
    original = harness.path.read_bytes()
    if mutation == 'unknown-format':
        rows = [json.loads(line) for line in original.splitlines()]; rows[0]['format'] = 8
        altered = b'\n'.join(json.dumps(row).encode() for row in rows) + b'\n'
    elif mutation == 'truncated': altered = original[:-3]
    elif mutation == 'duplicate-json': altered = b'{"format":9,"format":9}\n'
    else: altered = b'[' * 65 + b'0' + b']' * 65
    harness.path.write_bytes(altered)
    with pytest.raises(SemanticReadError) as failed:
        semantic.begin(group, sources, LIMITS)
    assert failed.value.report['accepted'] == '0' and failed.value.report['rejected'] == '1'
    assert failed.value.diagnostic['sourceId'] == 'synthetic-fabric'
    if mutation == 'unknown-format':
        assert failed.value.diagnostic['code'] == 'source-changed'
        # Reopening is an explicit fresh grant, so unknown-format reporting
        # is tested independently of the already-detected history rewrite.
        fresh_group, fresh_sources = admitted(reader, harness.path, 'fabric')
        with pytest.raises(SemanticReadError) as incompatible: semantic.begin(fresh_group, fresh_sources, LIMITS)
        assert incompatible.value.diagnostic['code'] == 'incompatible-source'
        assert incompatible.value.compatibility[0]['declaredFormat'] == '8' and not incompatible.value.compatibility[0]['supported']
    old = accepted['sources'][0]
    assert semantic.page(group, accepted['leaseId'], old['captureToken'], '0', 262144)[0] == original
    assert harness.path.read_bytes() == altered


def test_source_replacement_rejected_and_missing_material_explicit(environment, monkeypatch):
    data, _, reader, semantic = environment
    harness = GovernedHarness(data, monkeypatch, engagement='viewer-material'); harness.bootstrap()
    group, sources = admitted(reader, harness.path, 'fabric')
    entry = reader.groups[group][1][0]
    with pytest.raises(SemanticReadError) as missing: semantic._material({**entry, '_sourceId': 'synthetic-fabric'}, '0' * 64)
    assert missing.value.diagnostic['code'] == 'missing-material'
    replacement = data / 'replacement'; replacement.write_bytes(harness.path.read_bytes()); replacement.replace(harness.path)
    with pytest.raises(SemanticReadError): semantic.begin(group, sources, LIMITS)


def test_bounded_chunks_cursors_release_and_limits(environment):
    data, _, reader, semantic = environment
    path = data / 'findings.jsonl'; path.write_bytes((ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes())
    group, sources = admitted(reader, path, 'findings'); result = semantic.begin(group, sources, LIMITS)
    all_facts(semantic, group, result['leaseId'])
    with pytest.raises(SemanticReadError): semantic.chunk(group, result['leaseId'], None)
    with pytest.raises(SemanticReadError): semantic.page('foreign', result['leaseId'], result['sources'][0]['captureToken'], '0', 1)
    semantic.release(group, result['leaseId']); semantic.release(group, result['leaseId'])
    with pytest.raises(KeyError): semantic.page(group, result['leaseId'], result['sources'][0]['captureToken'], '0', 1)
    with pytest.raises(SemanticReadError) as limited: semantic.begin(group, sources, {**LIMITS, 'maxVertices': 1})
    assert limited.value.diagnostic['code'] == 'resource-limit'
    with pytest.raises(SemanticReadError): _preflight(b'x' * (100 * 1024 * 1024 + 1))


def test_optional_audit_is_explicit_saved_projection_or_rejected(environment):
    data, _, reader, semantic = environment
    path = data / 'audit.json'; report = {'format': 'jai.gen2-audit/1', 'read_only': True, 'authority_granted': False, 'head': '0' * 64}
    path.write_text(json.dumps(report)); group, sources = admitted(reader, path, 'audit')
    result = semantic.begin(group, sources, LIMITS); facts = all_facts(semantic, group, result['leaseId'])
    assert facts[0]['kind'] == 'audit' and result['sources'][0]['verification']['freshAssessment'] is False
    path.write_text('{"format":"unsupported"}')
    with pytest.raises(SemanticReadError) as failed: semantic.begin(group, sources, LIMITS)
    assert failed.value.diagnostic['code'] == 'incompatible-source'


def test_source_change_during_semantic_work_rejects_before_lease_publication(environment, monkeypatch):
    import semantic_reader as module
    data, _, reader, semantic = environment
    path = data / 'review.jsonl'; original = (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes(); path.write_bytes(original)
    group, sources = admitted(reader, path, 'findings')
    checked = module._preflight; changed = []
    def at_preflight(line):
        checked(line)
        if not changed:
            changed.append(True)
            with path.open('ab') as stream: stream.write(b'new bytes during import')
    monkeypatch.setattr(module, '_preflight', at_preflight)
    with pytest.raises(SemanticReadError) as failed: semantic.begin(group, sources, LIMITS)
    assert failed.value.diagnostic['code'] == 'source-changed' and not semantic.leases
    assert path.read_bytes() == original + b'new bytes during import'


@pytest.mark.parametrize('target', [1.5, float('nan'), {'counter': 9007199254740993}])
def test_arbitrary_canonical_findings_target_is_preserved_without_text_coercion(environment, target):
    data, _, reader, semantic = environment
    events = [json.loads(line) for line in (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes().splitlines()]
    previous = '0' * 64
    for event in events:
        if event['data']['op'] == 'add': event['data']['target'] = target
        event['prev'] = previous
        event['hash'] = hashlib.sha256((previous + findings.canonical(event['data']) + str(event['seq'])).encode()).hexdigest()
        previous = event['hash']
    raw = b''.join(findings.canonical(event).encode() + b'\n' for event in events)
    path = data / 'targets.jsonl'; path.write_bytes(raw)
    expected = findings.state(findings._parse_events(raw, 'fixture'))
    assert expected
    group, sources = admitted(reader, path, 'findings'); result = semantic.begin(group, sources, LIMITS)
    facts = all_facts(semantic, group, result['leaseId'])
    assert all(fact['target'] is None for fact in facts)
    for fact in facts:
        attrs = fact['attributes']; assert attrs['kind'] == 'inline'
        wrapped = {entry['key']: entry['value'] for entry in attrs['value']['entries']}
        record = {entry['key']: entry['value'] for entry in wrapped['record']['entries']}
        assert record['target'] == _tag(target)
    assert path.read_bytes() == raw


def test_valid_prefix_truncation_is_not_a_silent_state_regression(environment):
    data, _, reader, semantic = environment
    path = data / 'history.jsonl'; raw = (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes()
    path.write_bytes(raw); group, sources = admitted(reader, path, 'findings'); prior = semantic.begin(group, sources, LIMITS)
    shortened = raw.splitlines(keepends=True)[0]; path.write_bytes(shortened)
    assert findings.state(findings._parse_events(shortened, 'fixture'))
    with pytest.raises(SemanticReadError) as failed: semantic.begin(group, sources, LIMITS)
    assert failed.value.diagnostic['code'] == 'source-changed'
    old = prior['sources'][0]
    assert semantic.page(group, prior['leaseId'], old['captureToken'], '0', 262144)[0] == raw
    assert path.read_bytes() == shortened


def _history_with_large_evidence(size):
    events = [json.loads(line) for line in (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes().splitlines()[:2]]
    events[0]['data']['findings'] = [events[0]['data']['findings'][1]]
    events[0]['data']['findings'][0]['evidence'] = 'x' * size
    events[1]['data']['note'] = 'Complete later resolve note must remain accessible.'
    previous = '0' * 64
    for event in events:
        event['prev'] = previous; event['hash'] = hashlib.sha256((previous + findings.canonical(event['data']) + str(event['seq'])).encode()).hexdigest(); previous = event['hash']
    return b''.join(findings.canonical(event).encode() + b'\n' for event in events)


def test_large_derived_finding_preserves_complete_history_inline(environment):
    data, _, reader, semantic = environment
    path = data / 'large.jsonl'; raw = _history_with_large_evidence(300 * 1024); path.write_bytes(raw)
    group, sources = admitted(reader, path, 'findings'); result = semantic.begin(group, sources, LIMITS)
    fact = all_facts(semantic, group, result['leaseId'])[0]
    assert fact['state'] == 'resolved' and fact['attributes']['kind'] == 'inline'
    assert 'Complete later resolve note must remain accessible.' in json.dumps(fact['attributes'])
    assert path.read_bytes() == raw


def test_unrepresentable_complete_finding_rejects_instead_of_lossy_paging(environment):
    data, _, reader, semantic = environment
    path = data / 'oversized.jsonl'; raw = _history_with_large_evidence(600 * 1024); path.write_bytes(raw)
    group, sources = admitted(reader, path, 'findings')
    with pytest.raises(SemanticReadError) as failed: semantic.begin(group, sources, LIMITS)
    assert failed.value.diagnostic['code'] == 'resource-limit' and not semantic.leases
    assert path.read_bytes() == raw


def test_cold_empty_fabric_does_not_invent_a_declared_format(environment):
    data, _, reader, semantic = environment
    path = data / 'empty.jsonl'; path.write_bytes(b''); group, sources = admitted(reader, path, 'fabric')
    result = semantic.begin(group, sources, LIMITS); source = result['sources'][0]
    assert source['byteLength'] == '0' and source['sequence'] == '0' and source['head'] == '0' * 64
    assert source['compatibility']['declaredFormat'] is None and source['compatibility']['declaredProtocol'] is None
    assert source['compatibility']['supported'] is True and all_facts(semantic, group, result['leaseId']) == []
    assert list(data.iterdir()) == [path] and path.read_bytes() == b''


@pytest.mark.parametrize('mode', ['subsets', 'combined'])
def test_raw_budget_is_checked_before_read_and_bounds_retained_subset_cache(tmp_path, monkeypatch, mode):
    import semantic_reader as module
    data = tmp_path / 'data'; data.mkdir(); app = tmp_path / 'app'; app.mkdir(); reads = []
    raw = (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes()
    one = data / 'one.jsonl'; two = data / 'two.jsonl'; one.write_bytes(raw); two.write_bytes(raw)
    class Capture:
        def __init__(self, inner): self.inner = inner; self.info = inner.info
        def __enter__(self): return self
        def __exit__(self, *_): self.inner.close()
        def read_all(self): reads.append(self.info.size); return self.inner.read_all()
    class Root:
        def __init__(self, path): self.inner = ReadOnlyRoot(path); self.identity = self.inner.identity
        def capture(self, *args, **kwargs): return Capture(self.inner.capture(*args, **kwargs))
        def observe_ancestry(self): return self.inner.observe_ancestry()
        def close(self): self.inner.close()
    reader = Reader(Root, [app]); semantic = SemanticReader(reader, lc, findings); reader.semantic = semantic
    try:
        group = reader.admit([{'projectPath': str(data), 'path': str(path), 'family': 'findings'} for path in (one, two)])
        sources = [{'token': item['token'], 'sourceId': 'synthetic-' + str(index)} for index, item in enumerate(group['sources'])]
        monkeypatch.setattr(module, 'TOTAL', len(raw) + 10)
        if mode == 'subsets':
            first = semantic.begin(group['token'], sources[:1], LIMITS); semantic.release(group['token'], first['leaseId']); reads.clear()
            with pytest.raises(SemanticReadError) as failed: semantic.begin(group['token'], sources[1:], LIMITS)
            assert failed.value.diagnostic['code'] == 'resource-limit' and reads == []
            assert sum(len(cached[0]) for cached in semantic.preflight.values()) <= module.TOTAL
        else:
            with pytest.raises(SemanticReadError) as failed: semantic.begin(group['token'], sources, LIMITS)
            assert failed.value.diagnostic['code'] == 'resource-limit' and reads == [len(raw)]
    finally: reader.close()


@pytest.mark.parametrize('raw', [b'\n', b'[]\n', b'[1]\n'])
def test_malformed_cold_fabric_rows_fail_with_typed_diagnostic(environment, raw):
    data, _, reader, semantic = environment
    path = data / 'bad.jsonl'; path.write_bytes(raw); group, sources = admitted(reader, path, 'fabric')
    with pytest.raises(SemanticReadError) as failed: semantic.begin(group, sources, LIMITS)
    assert failed.value.diagnostic['code'] == 'read-failed' and failed.value.diagnostic['sourceId'] == 'synthetic-fabric'
    assert not semantic.leases and path.read_bytes() == raw


def test_recorded_unknown_semantic_encoder_is_displayed_without_re_adjudication(environment, monkeypatch):
    data, _, reader, semantic = environment
    harness = GovernedHarness(data, monkeypatch, engagement='viewer-codec'); harness.bootstrap()
    row = json.loads(harness.path.read_bytes().splitlines()[0])
    message = row['operations'][0]['data']['message']
    message['message_type'] = 'control_event'; message['payload'] = {'event': 'invocation_finished', 'codec': 'jai.semantic-tree/999'}
    message['message_id'] = lc.message_id(message); row['hash'] = lc._transaction_hash(row)
    raw = json.dumps(row).encode() + b'\n'; path = data / 'unknown-codec.jsonl'; path.write_bytes(raw)
    with pytest.raises(ValueError, match='Unsupported historical semantic encoder'):
        lc.replay(lc._parse_transactions(raw))
    group, sources = admitted(reader, path, 'fabric')
    candidate = semantic.begin(group, sources, LIMITS)
    assert candidate['sources'][0]['verification']['replay'] == 'recorded'
    assert all_facts(semantic, group, candidate['leaseId'])
    assert path.read_bytes() == raw


def test_release_group_is_owned_idempotent_and_drops_all_semantic_cache(environment):
    data, _, reader, semantic = environment
    path = data / 'release.jsonl'; raw = (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes(); path.write_bytes(raw)
    group, sources = admitted(reader, path, 'findings'); result = semantic.begin(group, sources, LIMITS)
    semantic.release_group('foreign')
    assert result['leaseId'] in semantic.leases and semantic.preflight and semantic.findings_cache
    semantic.release_group(group); semantic.release_group(group)
    assert not semantic.leases and not semantic.preflight and not semantic.findings_cache and not semantic.projections
    with pytest.raises(KeyError): semantic.chunk(group, result['leaseId'], None)
    assert path.read_bytes() == raw


def test_two_leases_share_immutable_findings_with_independent_serialized_offsets(environment, monkeypatch):
    import semantic_reader as module
    data, _, reader, semantic = environment
    raw = (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes()
    path = data / 'review.jsonl'; path.write_bytes(raw)
    group, sources = admitted(reader, path, 'findings')
    first = semantic.begin(group, sources, LIMITS); second = semantic.begin(group, sources, LIMITS)
    one = semantic.leases[first['leaseId']]['facts'][0]; two = semantic.leases[second['leaseId']]['facts'][0]
    assert one is two and one.refs == 3 and one.sealed
    # Force multiple frames after generation, without changing the stored fact guard.
    monkeypatch.setattr(module, 'CHUNK', one.encoded // 3)
    first_chunk = semantic.chunk(group, first['leaseId'], None)
    assert first_chunk['next'] is not None
    second_chunk = semantic.chunk(group, second['leaseId'], None)
    assert first_chunk['facts'] == second_chunk['facts']
    first_facts = first_chunk['facts']; cursor = first_chunk['next']
    while cursor is not None:
        chunk = semantic.chunk(group, first['leaseId'], cursor); first_facts.extend(chunk['facts']); cursor = chunk['next']
    second_facts = second_chunk['facts']; cursor = second_chunk['next']
    while cursor is not None:
        chunk = semantic.chunk(group, second['leaseId'], cursor); second_facts.extend(chunk['facts']); cursor = chunk['next']
    assert first_facts == second_facts and len(first_facts) == one.count
    assert first['sources'][0]['digest'] == hashlib.sha256(raw).hexdigest()
    capture = first['sources'][0]['captureToken']
    assert semantic.page(group, first['leaseId'], capture, '0', min(len(raw), 256 * 1024))[0] == raw
    with pytest.raises(SemanticReadError): semantic.release('foreign', first['leaseId'])
    semantic.release(group, first['leaseId']); assert one.refs == 2
    semantic.release_group(group)
    assert one.closed and not semantic._pool.objects and semantic._pool.physical == 0
    assert path.read_bytes() == raw


def test_full_findings_cache_owned_by_first_lease_never_rejects_second_lease(environment):
    data, _, reader, semantic = environment
    raw = (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes()
    selections = []
    for index in range(128):
        path = data / ('review-' + str(index) + '.jsonl'); path.write_bytes(raw)
        selections.append({'projectPath': str(data), 'path': str(path), 'family': 'findings'})
    admitted_set = reader.admit(selections); group = admitted_set['token']
    sources = [{'token': item['token'], 'sourceId': 'synthetic-' + str(index)} for index, item in enumerate(admitted_set['sources'])]
    first = semantic.begin(group, sources, LIMITS)
    old = semantic.leases[first['leaseId']]['facts'][:]
    assert len(semantic.findings_cache) == 128 and all(facts.refs == 2 for facts in old)
    path = data / 'new-review.jsonl'; path.write_bytes(raw)
    second_group, second_sources = admitted(reader, path, 'findings')
    second = semantic.begin(second_group, second_sources, LIMITS)
    assert len(semantic.leases) == 2 and len(semantic.findings_cache) == 128
    assert len(semantic._pool.objects) == 129 and old[0].refs == 1 and not old[0].closed
    assert all_facts(semantic, second_group, second['leaseId'])
    assert all_facts(semantic, group, first['leaseId'])
    semantic.release_group(second_group); semantic.release_group(group)
    assert not semantic._pool.objects and semantic._pool.physical == 0


@pytest.mark.parametrize('cancel', [False, True])
def test_candidate_failure_or_cancellation_releases_all_staging_without_harming_existing_lease(environment, monkeypatch, cancel):
    data, _, reader, semantic = environment
    raw = (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes()
    path = data / 'review.jsonl'; path.write_bytes(raw)
    group, sources = admitted(reader, path, 'findings'); accepted = semantic.begin(group, sources, LIMITS)
    baseline = set(semantic._pool.objects), semantic._pool.physical
    other = data / 'other.jsonl'; other.write_bytes(raw)
    bad = data / 'bad.json'; bad.write_text('{"format":"unsupported"}')
    admitted_set = reader.admit([{'projectPath': str(data), 'path': str(other), 'family': 'findings'},
                                 {'projectPath': str(data), 'path': str(bad), 'family': 'audit'}])
    candidate_group = admitted_set['token']
    selected = [{'token': item['token'], 'sourceId': 'synthetic-candidate-' + str(index)} for index, item in enumerate(admitted_set['sources'])]
    if cancel:
        check = reader._check; calls = 0
        def cancellation(roots):
            nonlocal calls
            calls += 1
            if calls == 3: raise KeyboardInterrupt()
            return check(roots)
        monkeypatch.setattr(reader, '_check', cancellation)
    with pytest.raises(KeyboardInterrupt if cancel else SemanticReadError): semantic.begin(candidate_group, selected, LIMITS)
    assert (set(semantic._pool.objects), semantic._pool.physical) == baseline
    assert len(semantic.leases) == 1 and len(semantic.findings_cache) == 1
    assert not semantic._building and not semantic._pending_cache
    assert all_facts(semantic, group, accepted['leaseId'])
    assert path.read_bytes() == other.read_bytes() == raw


def test_findings_cache_replacement_keeps_old_lease_object_alive(environment):
    data, _, reader, semantic = environment
    path = data / 'review.jsonl'
    raw = (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes(); path.write_bytes(raw)
    group, sources = admitted(reader, path, 'findings'); first = semantic.begin(group, sources, LIMITS)
    old = semantic.leases[first['leaseId']]['facts'][0]
    old_facts = all_facts(semantic, group, first['leaseId'])
    # MAX_ROUNDS is an existing canonical cache input; it creates a different
    # immutable semantic revision without changing the admitted source bytes.
    maximum = semantic.findings.MAX_ROUNDS
    try:
        semantic.findings.MAX_ROUNDS += 1
        second = semantic.begin(group, sources, LIMITS)
        new = semantic.leases[second['leaseId']]['facts'][0]
        assert new is not old and old.refs == 1 and new.refs == 2
        assert old_facts[0]['effectiveMaxRounds'] == maximum
        assert all_facts(semantic, group, second['leaseId'])[0]['effectiveMaxRounds'] == maximum + 1
    finally: semantic.findings.MAX_ROUNDS = maximum
    semantic.release(group, first['leaseId']); assert old.closed and not new.closed
    semantic.release_group(group); assert new.closed and not semantic._pool.objects


def test_contradictory_private_record_count_rejects_terminal_chunk(environment):
    data, _, reader, semantic = environment
    path = data / 'audit.json'; path.write_text('{"format":"jai.gen2-audit/1","read_only":true,"authority_granted":false}')
    group, sources = admitted(reader, path, 'audit'); candidate = semantic.begin(group, sources, LIMITS)
    spool = semantic.leases[candidate['leaseId']]['facts'][0]
    spool.count += 1
    with pytest.raises(SemanticReadError): semantic.chunk(group, candidate['leaseId'], None)
    semantic.release_group(group)
    assert not semantic._pool.objects


@pytest.mark.parametrize('fault', ['write', 'cache'])
def test_memoryerror_candidate_preserves_old_lease_and_releases_all_new_ownership(environment, monkeypatch, fault):
    import facts_spool
    data, _, reader, semantic = environment
    raw = (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes()
    path = data / 'accepted.jsonl'; path.write_bytes(raw)
    group, sources = admitted(reader, path, 'findings'); accepted = semantic.begin(group, sources, LIMITS)
    baseline = set(semantic._pool.objects), semantic._pool.physical
    new_path = data / 'candidate.jsonl'; new_path.write_bytes(raw)
    candidate_group, selected = admitted(reader, new_path, 'findings')
    original_factory = facts_spool.tempfile.TemporaryFile
    original_cache = semantic.findings_cache
    if fault == 'write':
        class BrokenWrite:
            def __init__(self, handle): self.handle = handle
            def seek(self, *args): return self.handle.seek(*args)
            def write(self, _data): raise MemoryError('controlled write failure')
            def close(self): return self.handle.close()
        monkeypatch.setattr(facts_spool.tempfile, 'TemporaryFile', lambda **options: BrokenWrite(original_factory(**options)))
    else:
        class BrokenCache(dict):
            def __setitem__(self, _key, _value): raise MemoryError('controlled cache insertion failure')
        semantic.findings_cache = BrokenCache(original_cache)
    with pytest.raises(SemanticReadError) as failed: semantic.begin(candidate_group, selected, LIMITS)
    assert failed.value.diagnostic['code'] == 'resource-limit'
    assert (set(semantic._pool.objects), semantic._pool.physical) == baseline
    assert len(semantic.leases) == 1 and not semantic._building and not semantic._pending_cache
    assert all_facts(semantic, group, accepted['leaseId'])
    monkeypatch.setattr(facts_spool.tempfile, 'TemporaryFile', original_factory)
    semantic.findings_cache = original_cache
    candidate = semantic.begin(candidate_group, selected, LIMITS)
    assert all_facts(semantic, candidate_group, candidate['leaseId'])


def test_candidate_original_failure_survives_close_memoryerror_and_all_staging_is_released(environment, monkeypatch):
    import facts_spool
    data, _, reader, semantic = environment
    raw = (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes()
    selections = []
    for index in range(2):
        path = data / ('review-' + str(index) + '.jsonl'); path.write_bytes(raw)
        selections.append({'projectPath': str(data), 'path': str(path), 'family': 'findings'})
    bad = data / 'bad.json'; bad.write_text('{"format":"unsupported"}')
    selections.append({'projectPath': str(data), 'path': str(bad), 'family': 'audit'})
    admitted_set = reader.admit(selections)
    selected = [{'token': item['token'], 'sourceId': 'synthetic-' + str(index)} for index, item in enumerate(admitted_set['sources'])]
    original_factory = facts_spool.tempfile.TemporaryFile
    class BrokenClose:
        def __init__(self, handle): self.handle = handle
        def __getattr__(self, name): return getattr(self.handle, name)
        def close(self):
            self.handle.close()
            raise MemoryError('controlled close failure')
    monkeypatch.setattr(facts_spool.tempfile, 'TemporaryFile', lambda **options: BrokenClose(original_factory(**options)))
    with pytest.raises(SemanticReadError) as failed: semantic.begin(admitted_set['token'], selected, LIMITS)
    assert failed.value.diagnostic['code'] == 'incompatible-source'
    assert not semantic._pool.objects and semantic._pool.physical == 0
    assert not semantic._building and not semantic._pending_cache and not semantic.leases


def _oracle_value(value):
    if isinstance(value, list): return [_oracle_value(item) for item in value]
    if isinstance(value, dict):
        result = {key: _oracle_value(item) for key, item in value.items()}
        if result.get('type') == 'object' and isinstance(result.get('entries'), list):
            result['entries'] = sorted(result['entries'], key=lambda item: item['key'])
        return result
    return value


def test_direct_recorded_adapter_never_invokes_canonical_verification_and_preserves_valid_fact_oracle(environment, monkeypatch):
    import base64
    from semantic_reader import _encoded
    data, _, reader, semantic = environment
    oracle = json.loads((Path(__file__).parent / 'fixtures/recorded-projection.json').read_bytes())
    raw = base64.b64decode(oracle['rawBase64'])
    path = data / 'recorded.jsonl'; path.write_bytes(raw)
    material = data / 'recorded.jsonl.blobs'; material.mkdir()
    # Availability means bounded readable material, not a fresh digest verdict.
    for identifier in oracle['materialIds']: (material / identifier).write_bytes(b'readable recorded material')
    def forbidden(*_args, **_kwargs): raise AssertionError('Viewer invoked canonical verification')
    monkeypatch.setattr(lc.Store, '_verified', forbidden)
    monkeypatch.setattr(lc, '_verify_transaction', forbidden)
    monkeypatch.setattr(lc, 'replay', forbidden)
    monkeypatch.setattr(lc.State, 'derive', forbidden)
    monkeypatch.setattr(lc.State, '_apply', forbidden)
    monkeypatch.setattr(findings, '_parse_events', forbidden)
    group, sources = admitted(reader, path, 'fabric')
    candidate = semantic.begin(group, sources, LIMITS)
    digest = hashlib.sha256(); facts = all_facts(semantic, group, candidate['leaseId'])
    for fact in facts:
        encoded = json.dumps(_oracle_value(fact), sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode('utf-8', 'backslashreplace')
        digest.update(len(encoded).to_bytes(4, 'big')); digest.update(encoded)
    assert len(facts) == oracle['factCount'] and digest.hexdigest() == oracle['factDigest']
    assert candidate['sources'][0]['verification'] == {'mode': 'recorded', 'decoded': 'decoded', 'chain': 'unknown', 'replay': 'recorded', 'publicTrust': 'unknown', 'material': 'not-observed', 'recordedApplicability': None, 'authorityGranted': False, 'freshAssessment': False}
    assert candidate['sources'][0]['digest'] == hashlib.sha256(raw).hexdigest()
    assert path.read_bytes() == raw


def test_oracle_normalization_preserves_arrays_members_multiplicity_values_and_unknown_fields():
    tagged = {'type': 'object', 'entries': [{'key': 'z', 'value': {'type': 'array', 'items': [3, 1, 2]}},
                                            {'key': 'a', 'value': 9}, {'key': 'a', 'value': 8}], 'extra': ['z', 'a']}
    result = _oracle_value([tagged, {'plain': [2, 1]}])
    assert result[0]['entries'] == [tagged['entries'][1], tagged['entries'][2], tagged['entries'][0]]
    assert result[0]['extra'] == ['z', 'a'] and result[1] == {'plain': [2, 1]}
    assert tagged['entries'][0]['key'] == 'z'


@pytest.mark.parametrize('family', ['fabric', 'findings'])
def test_recorded_chain_and_signature_claims_are_not_reverified(environment, monkeypatch, family):
    import base64
    data, _, reader, semantic = environment
    if family == 'fabric':
        oracle = json.loads((Path(__file__).parent / 'fixtures/recorded-projection.json').read_bytes())
        rows = [json.loads(line) for line in base64.b64decode(oracle['rawBase64']).splitlines()]
        for row in rows:
            row['hash'] = 'e' * 64; row['previous_hash'] = 'd' * 64; row['authority_proof'] = 'not-a-signed-proof'
        rows[0]['sequence'] = 40; rows[-1]['sequence'] = 77
        expected_sequence = '77'
    else:
        rows = [json.loads(line) for line in (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes().splitlines()]
        for row in rows: row['hash'] = 'e' * 64; row['prev'] = 'd' * 64
        rows[-1]['seq'] = 77; expected_sequence = '77'
    raw = b''.join(json.dumps(row).encode() + b'\n' for row in rows)
    path = data / 'recorded.jsonl'; path.write_bytes(raw)
    def forbidden(*_args, **_kwargs): raise AssertionError('Canonical adjudication called')
    monkeypatch.setattr(lc.Store, '_verified', forbidden); monkeypatch.setattr(findings, '_parse_events', forbidden)
    group, sources = admitted(reader, path, family); candidate = semantic.begin(group, sources, LIMITS)
    facts = all_facts(semantic, group, candidate['leaseId']); summary = candidate['sources'][0]
    assert facts and summary['head'] == 'e' * 64 and summary['sequence'] == expected_sequence
    assert summary['verification']['chain'] == 'unknown' and summary['verification']['publicTrust'] == 'unknown'
    assert summary['verification']['mode'] == summary['verification']['replay'] == 'recorded'
    if family == 'fabric':
        first = next(fact for fact in facts if fact['kind'] == 'version')
        assert first['origin']['byteOffset'] == '0' and first['origin']['sequence'] == '40'
    capture = summary['captureToken']; rebuilt = b''
    while len(rebuilt) < len(raw):
        page, eof = semantic.page(group, candidate['leaseId'], capture, str(len(rebuilt)), 256 * 1024)
        rebuilt += page
        assert eof == (len(rebuilt) == len(raw))
    assert rebuilt == raw == path.read_bytes()


@pytest.mark.parametrize('mutation', ['effects-container', 'effect-container', 'manifest-container', 'manifest-record', 'message-scope', 'sequence-type'])
def test_direct_projection_rejects_unreadable_structure_with_named_diagnostic(environment, mutation):
    import base64
    data, _, reader, semantic = environment
    oracle = json.loads((Path(__file__).parent / 'fixtures/recorded-projection.json').read_bytes())
    row = json.loads(base64.b64decode(oracle['rawBase64']).splitlines()[0]); content = row['operations'][0]['data']
    if mutation == 'effects-container': content['effects'] = {}
    elif mutation == 'effect-container': content['effects'][0] = []
    elif mutation == 'manifest-container': content['effects'][0]['manifest'] = []
    elif mutation == 'manifest-record': content['effects'][0]['manifest']['content']['record'] = []
    elif mutation == 'message-scope': content['message']['scope'] = []
    else: row['sequence'] = []
    raw = json.dumps(row).encode() + b'\n'; path = data / 'bad.jsonl'; path.write_bytes(raw)
    group, sources = admitted(reader, path, 'fabric')
    with pytest.raises(SemanticReadError) as failed: semantic.begin(group, sources, LIMITS)
    assert failed.value.diagnostic['code'] == 'read-failed'
    assert not semantic.leases and not semantic._pool.objects and path.read_bytes() == raw


def test_recorded_effects_and_unresolved_references_are_projected_without_business_validation(environment):
    import base64
    data, _, reader, semantic = environment
    oracle = json.loads((Path(__file__).parent / 'fixtures/recorded-projection.json').read_bytes())
    row = json.loads(base64.b64decode(oracle['rawBase64']).splitlines()[0])
    target = {'engagement': 'recorded-external', 'scope': 'other-origin', 'logical_id': 'unresolved', 'version_id': 'f' * 64}
    effect = row['operations'][0]['data']['effects'][0]
    effect['manifest']['content']['record']['unresolved_recorded_reference'] = target
    identifier = semantic.lc.version_id(effect['manifest'])
    row['operations'][0]['data']['effects'].append({'op': 'qualify', 'subject': identifier, 'applicable': False})
    raw = json.dumps(row).encode() + b'\n'; path = data / 'recorded-effects.jsonl'; path.write_bytes(raw)
    group, sources = admitted(reader, path, 'fabric'); candidate = semantic.begin(group, sources, LIMITS)
    facts = all_facts(semantic, group, candidate['leaseId'])
    reference = next(fact for fact in facts if fact['kind'] == 'reference' and fact['targetRef'] == target)
    assert reference['fieldPointer'] == '/unresolved_recorded_reference'
    use = next(fact for fact in facts if fact['kind'] == 'use' and fact['point']['ref']['version_id'] == identifier)
    assert use['state'] == _tag({'validity': 'valid', 'applicable': False})
    assert candidate['sources'][0]['verification']['freshAssessment'] is False


def test_pure_recorded_identifier_codec_and_reference_scan_match_published_fixture_values():
    from recorded_projection import _RecordedFormat
    value = {'schema': 'jai.lifecycle.manifest/2', 'logical_id': 'cafe\u0301', 'kind': 'delivery.source',
             'content': {'engagement': 'synthetic', 'scope': 'origin', 'record': {'number': 2 ** 80}}, 'bindings': {}, 'members': []}
    assert _RecordedFormat.version_id(value) == lc.version_id(value)
    reference = {'engagement': 'synthetic', 'scope': 'origin', 'logical_id': 'x', 'version_id': 'a' * 64}
    record = {'z': [reference, reference], 'handling': {'episode': reference}}
    assert list(_RecordedFormat._reference_paths(record)) == list(lc._reference_paths(record))
    assert list(_RecordedFormat._causal_reference_paths(record)) == list(lc._causal_reference_paths(record))
    with pytest.raises(ValueError): _RecordedFormat.version_id({'normalized': {'é': 1, 'e\u0301': 2}})
