# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Bounded actual-helper retention comparison; never imported by production.

Usage: pinned-python -I -B facts_memory_pilot.py ABS_MANIFEST ABS_CORE_TOOLS drop|hold.
Output is private JSON evidence. Hold deliberately retains actual appended
dictionaries; it is not the former reader implementation. Neither mode qualifies
Electron RSS, large-corpus timing or source authority.
"""
import collections
import gc
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time
try:
    import resource
except ImportError:
    resource = None


def reachable(value, maximum=200000, shared=None):
    """Measure a bounded identity-deduplicated Python object graph, excluding opaque internals.

    Args:
        value: One diagnostic ownership root after chunk temporaries are released.
        maximum: Positive diagnostic object ceiling; fixed at 200,000 in actual pilots.
        shared: Optional identity set enforcing the same ceiling across diagnostic categories.
    Returns:
        Identity-to-size map and unsupported leaf counts; file contents are not traversed.
    Raises:
        RuntimeError: The small-pilot object ceiling is exceeded.
    """
    seen = {}; unsupported = collections.Counter(); pending = [value]
    while pending:
        item = pending.pop(); identity = id(item)
        if identity in seen: continue
        if len(seen) >= maximum: raise RuntimeError('Small pilot object bound exceeded')
        if shared is not None and identity not in shared:
            if len(shared) >= maximum: raise RuntimeError('Small pilot shared object bound exceeded')
            shared.add(identity)
        seen[identity] = sys.getsizeof(item)
        if isinstance(item, dict): pending.extend(item.keys()); pending.extend(item.values())
        elif isinstance(item, (list, tuple, set, frozenset)): pending.extend(item)
        elif type(item).__module__ in {'recorded_projection', 'semantic_reader', 'facts_spool'} and hasattr(item, '__dict__'): pending.append(vars(item))
        elif not isinstance(item, (str, bytes, int, float, bool, type(None))): unsupported[type(item).__name__] += 1
    return seen, dict(unsupported)


def memory(statm=Path('/proc/self/statm')):
    """Return Linux process RSS before diagnostic object walks, without baseline subtraction.

    Args:
        statm: Trusted Linux process record, or a bounded filesystem fixture in tests.
    Returns:
        Current and kernel-lifetime peak bytes; this helper has no Electron descendants.
    """
    if sys.platform != 'linux' or resource is None: return {'supported': False, 'currentBytes': None, 'peakBytes': None}
    resident = int(statm.read_text().split()[1]) * os.sysconf('SC_PAGE_SIZE')
    return {'supported': True, 'currentBytes': resident, 'peakBytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024}


def main():
    """Run one bounded condition against exact prepared recorded sources.

    Returns:
        Zero after exact revision checks, stream measurement and explicit cleanup.
    Raises:
        ValueError: Invocation or fixed small-input manifest is invalid.
        RuntimeError: Diagnostic or cleanup invariants fail.
    """
    if len(sys.argv) != 4 or sys.argv[3] not in {'drop', 'hold'}: raise ValueError('Explicit manifest, core tools and drop|hold required')
    manifest = Path(sys.argv[1]); core = Path(sys.argv[2]); mode = sys.argv[3]
    if not manifest.is_absolute() or not core.is_absolute() or manifest.stat().st_size > 1048576: raise ValueError('Fixed absolute bounded inputs required')
    reader_dir = Path(__file__).resolve().parents[1]
    sys.path[:0] = [str(reader_dir), str(core)]; os.environ['PATH'] = ''
    import semantic_reader as sm
    import facts_spool
    import raw_reader
    from readonly_files import ReadOnlyRoot
    source_files = [manifest, Path(__file__), reader_dir / 'raw_reader.py', reader_dir / 'semantic_reader.py', reader_dir / 'facts_spool.py', reader_dir / 'recorded_projection.py']
    input_digests = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in source_files}
    data = json.loads(manifest.read_bytes()); base = manifest.parent / 'base'; rows = data['sourceSets']['base']['sourcePaths']
    if not 1 <= len(rows) <= 128: raise ValueError('Bounded prepared selections required')
    selected_paths = []; input_bytes = 0; material_digests = {}; directories = {base}
    for row in rows:
        path = (base / row['path']).resolve()
        if not path.is_relative_to(base.resolve()) or row['family'] not in {'fabric', 'findings'}: raise ValueError('Prepared child selection required')
        input_bytes += row['byteLength']
        if input_bytes > 16 * 1024 * 1024: raise ValueError('Small pilot input bound exceeded')
        payload = path.read_bytes()
        if len(payload) != row['byteLength'] or hashlib.sha256(payload).hexdigest() != row['sha256']: raise ValueError('Prepared source revision differs')
        selected_paths.append(path); directories.add(path.parent)
        blobs = Path(str(path) + '.blobs')
        if blobs.exists():
            if blobs.is_symlink() or not blobs.is_dir() or not blobs.resolve().is_relative_to(base.resolve()): raise ValueError('Prepared material directory required')
            directories.add(blobs)
            for item in blobs.iterdir():
                if len(item.name) != 64 or any(char not in '0123456789abcdef' for char in item.name): continue
                if item.is_symlink() or not item.is_file(): raise ValueError('Prepared regular material required')
                input_bytes += item.stat().st_size
                if input_bytes > 16 * 1024 * 1024: raise ValueError('Small pilot input bound exceeded')
                material_digests[item] = hashlib.sha256(item.read_bytes()).hexdigest()
    directory_names = {path: sorted(item.name for item in path.iterdir()) for path in directories}
    held = []; original = facts_spool._Spool.append
    def append(spool, fact):
        original(spool, fact)
        if spool.pool.physical > 16 * 1024 * 1024 + 4 * 5000 or sum(item.encoded for item in spool.pool.objects) > 16 * 1024 * 1024 or sum(item.count for item in spool.pool.objects) > 5000: raise RuntimeError('Small pilot fact bound exceeded')
        if mode == 'hold': held.append(fact)
    facts_spool._Spool.append = append
    previous = Path.cwd(); result = None
    try:
        with tempfile.TemporaryDirectory(prefix='jai-facts-pilot-', dir='/tmp') as app_name:
            app = Path(app_name); os.chdir(app)
            reader = raw_reader.Reader(ReadOnlyRoot, [app]); semantic = sm.SemanticReader(reader); reader.semantic = semantic
            try:
                opened = reader.admit([{'projectPath': str(base), 'path': str(path), 'family': row['family']} for row, path in zip(rows, selected_paths)])
                selections = [{'token': item['token'], 'sourceId': 'synthetic-' + str(index)} for index, item in enumerate(opened['sources'])]
                started = time.perf_counter(); lease = semantic.begin(opened['token'], selections, {'maxVertices': 100000, 'maxEdges': 500000, 'maxEncodedGraphBytes': 512 * 1024 * 1024}); begin_ms = (time.perf_counter() - started) * 1000
                expected = sorted(json.dumps([row['family'], str(row['byteLength']), row['sha256'], row['head'], str(row['sequence'])]) for row in rows)
                observed = sorted(json.dumps([item['family'], item['byteLength'], item['digest'], item['head'], item['sequence']]) for item in lease['sources'])
                if observed != expected: raise RuntimeError('Captured recorded revisions differ from manifest')
                state = semantic.leases[lease['leaseId']]; digest = hashlib.sha256(); count = encoded = 0; cursor = None; started = time.perf_counter()
                while True:
                    chunk = semantic.chunk(opened['token'], lease['leaseId'], cursor)
                    for fact in chunk['facts']:
                        raw = sm._encoded(fact); digest.update(len(raw).to_bytes(4, 'big')); digest.update(raw); count += 1; encoded += len(raw)
                    cursor = chunk['next']; del chunk
                    fact = raw = None
                    if cursor is None: break
                drain_ms = (time.perf_counter() - started) * 1000; gc.collect(); before_walk = memory()
                roots = {'rawCaptures': [item['raw'] for item in state['captures'].values()], 'recordedProjectionIndexes': list(semantic.projections.values()), 'facts': state['facts'], 'preflight': semantic.preflight, 'findingsCache': semantic.findings_cache, 'heldControl': held}
                graphs = {}; categories = {}; identities = set()
                for name, value in roots.items():
                    graph, opaque = reachable(value, shared=identities); graphs[name] = graph; categories[name] = {'reachableBytes': sum(graph.values()), 'objects': len(graph), 'unsupportedLeaves': opaque}
                union = {identity: size for graph in graphs.values() for identity, size in graph.items()}
                result = {'mode': mode, 'readerMode': 'recorded-projection', 'control': 'actual append plus deliberate dictionary retention; not historical implementation', 'beginMs': begin_ms, 'drainMs': drain_ms, 'factCount': count, 'encodedFactBytes': encoded, 'factDigest': digest.hexdigest(), 'heldDictionaries': len(held), 'rssBeforeWalk': before_walk, 'rssAfterWalk': memory(), 'categories': categories, 'unionReachableBytes': sum(union.values()), 'spool': {'objects': len(semantic._pool.objects), 'physicalBytes': semantic._pool.physical}, 'sources': [{key: item[key] for key in ('family', 'byteLength', 'digest', 'head', 'sequence')} for item in lease['sources']], 'inputDigests': input_digests, 'limits': 'One small controlled pair only; no prior RSS reconstruction, L projection or native qualification. Object-walk memory is observer overhead; opaque internals are excluded.'}
                semantic.release(opened['token'], lease['leaseId'])
            finally:
                reader.close()
                if semantic._pool.objects or semantic._pool.physical: raise RuntimeError('Live private facts remain after reader close')
                os.chdir(previous)
    finally:
        facts_spool._Spool.append = original; os.chdir(previous)
    for row, path in zip(rows, selected_paths):
        if hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']: raise RuntimeError('Source changed during pilot')
    if any(hashlib.sha256(path.read_bytes()).hexdigest() != digest for path, digest in material_digests.items()): raise RuntimeError('Material changed during pilot')
    if any(hashlib.sha256(path.read_bytes()).hexdigest() != input_digests[str(path)] for path in source_files): raise RuntimeError('Pilot composition changed during measurement')
    if any(sorted(item.name for item in path.iterdir()) != names for path, names in directory_names.items()): raise RuntimeError('Source directory entries changed during pilot')
    result['cleanup'] = 'zero live spool objects/bytes; selected source/material digests and source directory entries unchanged'
    print(json.dumps(result, indent=2)); return 0


if __name__ == '__main__':
    raise SystemExit(main())
