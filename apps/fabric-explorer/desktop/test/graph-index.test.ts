// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Synthetic S04 graph ground truth; these DTO fixtures do not claim canonical journal admission. */
import { createHash } from 'node:crypto';
import { describe, expect, it, vi } from 'vitest';
import { assertProjection, assertResponseForRequest, assertVertex, assertEdge, edgeKey, elementKey, PROTOCOL, queryKey } from '@jai/fabric-explorer-contracts';
import type { Edge, ElementIdentity, Filter, RecordFamily, Request, SourceLocator, SourceReference, SourceRevision, Vertex } from '@jai/fabric-explorer-contracts';
import { DEFAULT_QUERY_LIMITS, DEFAULT_RELATIONS, QueryIndex } from '../src/graph/query-index.js';
import { CompactGraphStore } from '../src/import/compact-store.js';
import type { GraphBinding, GraphData, GraphReply, GraphRequest } from '../src/graph/types.js';
const binding: GraphBinding = { sessionId: 'synthetic-session', capability: 'synthetic-capability', generation: '1' };
const empty: Filter = { projectIds: [], families: [], findingStates: [], relations: [] };
const digest = (value: string) => createHash('sha256').update(value).digest('hex');
const attrs = { kind: 'inline' as const, value: { type: 'null' as const } };
function revision(project: string, family: 'fabric' | 'findings'): SourceRevision { return { revisionId: `revision-${project}-${family}`, projectId: project, rootId: `root-${project}`, sourceId: `source-${project}-${family}`, family, relativePath: `${family}.jsonl`, adapterVersion: 'synthetic-adapter/1', byteLength: '4096', digest: digest(project + family), head: digest(project), sequence: '100', observedAt: '2030-01-01T00:00:00Z', verification: { mode: 'canonical', decoded: 'decoded', chain: 'verified', replay: family === 'fabric' ? 'verified' : 'unknown', publicTrust: 'not-required', material: 'not-observed', recordedApplicability: null, authorityGranted: false, freshAssessment: false } }; }
function source(project = 'p', family: 'fabric' | 'findings' = 'fabric'): SourceLocator { const row = revision(project, family); return { projectId: project, rootId: row.rootId, sourceId: row.sourceId, family, relativePath: row.relativePath, pointer: '/synthetic-record', sequence: '1', revisionId: row.revisionId, adapterVersion: row.adapterVersion }; }
function ref(name: string, project = 'p'): SourceReference { return { engagement: `synthetic-${project}`, scope: 'origin', logical_id: name, version_id: digest(name) }; }
function version(name: string, label = name, family: RecordFamily = 'source', project = 'p'): Vertex { const identity = { kind: 'version' as const, projectId: project, ref: ref(name, project) }; return { kind: 'version', id: elementKey(identity), identity, family, label, source: source(project), attributes: attrs }; }
function use(vertex: Vertex): Vertex { if (vertex.identity.kind !== 'version') throw new Error('Version fixture required'); const identity = { kind: 'use' as const, projectId: vertex.identity.projectId, ref: vertex.identity.ref, useScope: 'selected-use' }; return { kind: 'use', id: elementKey(identity), identity, label: `${vertex.label} use`, source: vertex.source, attributes: attrs }; }
function finding(name: string, state: 'open' | 'verified'): Vertex { const identity = { kind: 'finding' as const, projectId: 'p', ledgerId: 'source-p-findings', findingId: name }; return { kind: 'finding', id: elementKey(identity), identity, label: name, state, severity: 'medium', findingKind: 'defect', rounds: '0', recordedExpiry: null, source: source('p', 'findings'), attributes: attrs }; }
function unresolved(name: string): Vertex { const identity = { kind: 'version' as const, projectId: 'p', ref: ref(name) }; return { kind: 'unresolved', id: elementKey(identity), identity, reason: 'missing-reference', label: name, source: source(), attributes: attrs }; }
function participant(): Vertex { const identity = { kind: 'participant' as const, projectId: 'p', participant: { kind: 'controller' as const, id: 'synthetic-controller' } }; return { kind: 'participant', id: elementKey(identity), identity, label: 'Controller', source: source(), attributes: attrs }; }
function edge(name: string, from: Vertex, to: Vertex, relation: Edge['relation'] = 'causal-dependency', causal = true): Edge { const identity = { kind: 'occurrence' as const, projectId: from.identity.projectId, origin: from.identity, pointer: `/synthetic/${name}`, occurrence: 0, from: from.identity, to: to.identity }; return { id: edgeKey(identity), identity, from: from.id, to: to.id, relation, label: name, source: from.source, basis: causal ? 'canonical-dependency' : 'exact-reference', causal, attributes: attrs }; }
function graph(vertices: Vertex[], edges: Edge[], generation = '1'): Extract<GraphData, { records: Iterable<Vertex | Edge> }> {
  vertices.forEach(assertVertex); edges.forEach(assertEdge);
  const sources = new Map([...vertices.map(vertex => vertex.source), ...edges.map(item => item.source)].map(item => [item.revisionId, revision(item.projectId, item.family === 'findings' ? 'findings' : 'fabric')]));
  return { snapshot: { format: 'jai.fabric-explorer.snapshot/1', sessionId: binding.sessionId, generation, sources: [...sources.values()], counts: { vertices: String(vertices.length), edges: String(edges.length), findings: String(vertices.filter(vertex => vertex.kind === 'finding').length) }, authorityGranted: false, freshAssessment: false }, records: [...vertices, ...edges] };
}
function fixture() {
  const a = version('A', 'Build Z', 'product'); const b = version('B', 'build a', 'profile'); const c = version('C', 'Build A'); const d = version('D', 'Other');
  const edges = [edge('a1', a, b), edge('a2', a, b), edge('bc', b, c, 'profile'), edge('ca', c, a), edge('cc', c, c)]; const data = graph([a, b, c, d], edges);
  const store = CompactGraphStore.fromRecords(data.snapshot, data.records);
  return { a, b, c, d, edges, data, store, index: new QueryIndex({ snapshot: data.snapshot, store }, binding) };
}
function request<K extends GraphRequest['operation']>(operation: K, payload: Extract<GraphRequest, { operation: K }>['payload'], context = binding): Extract<GraphRequest, { operation: K }> { return { protocol: PROTOCOL, kind: 'request', requestId: 'synthetic-query', binding: context, operation, payload } as Extract<GraphRequest, { operation: K }>; }
function run(index: QueryIndex, input: GraphRequest): GraphReply {
  const result = index.execute(input);
  assertResponseForRequest({ protocol: PROTOCOL, kind: 'response', requestId: input.requestId, binding: input.binding, operation: result.operation, status: 'ok', payload: result.value }, input, input.binding);
  if (result.operation === 'graph.neighbours' || result.operation === 'graph.path') assertProjection(result.value.projection);
  return result;
}
const neighbours = (identity: ElementIdentity, limits = DEFAULT_QUERY_LIMITS, direction: 'forward' | 'reverse' | 'both' = 'forward') => request('graph.neighbours', { identity, direction, relations: DEFAULT_RELATIONS, causalOnly: false, limits });
const path = (from: ElementIdentity, to: ElementIdentity, limits = DEFAULT_QUERY_LIMITS, direction: 'forward' | 'reverse' | 'both' = 'forward') => request('graph.path', { from, to, direction, relations: DEFAULT_RELATIONS, causalOnly: false, limits });

describe('worker-local immutable graph query index', () => {
  it('keeps finding-only cursor membership and authentication separate from ordinary search', () => {
    const a = finding('F-1', 'open'); const b = finding('F-2', 'verified'); const other = version('not-a-finding'); const index = new QueryIndex(graph([a, b, other], []), binding);
    const input = request('search.page', { text: '', filter: empty, order: 'identity', limit: 1, cursor: null });
    const first = index.searchFindings(input); expect(first.value.items.every(vertex => vertex.kind === 'finding')).toBe(true); expect(first.value.hidden).toBe('1');
    expect(first.value.nextCursor!.queryKey).toBe(queryKey(input));
    const next = request('search.page', { ...input.payload, cursor: first.value.nextCursor });
    expect(index.searchFindings(next).value).toMatchObject({ hidden: '0', complete: true, nextCursor: null });
    expect(() => index.execute(next)).toThrow(expect.objectContaining({ code: 'cursor-mismatch' }));
    const all = index.execute(input); if (all.operation !== 'search.page') throw new Error('Wrong fixture operation');
    expect(() => index.searchFindings(request('search.page', { ...input.payload, cursor: all.value.nextCursor }))).toThrow(expect.objectContaining({ code: 'cursor-mismatch' }));
  });
  it('filters retained projections by exact off-projection family and restores every original parallel edge', () => {
    const product = version('outside', 'Outside', 'product'); const used = use(product); const target = version('target', 'Target', 'profile'); const edges = [edge('first', used, target), edge('parallel', used, target)];
    const index = new QueryIndex(graph([product, used, target], edges), binding);
    const projected = index.execute(neighbours(used.identity)); if (!('handles' in projected)) throw new Error('Wrong fixture operation');
    expect(projected.value.projection.vertices.map(vertex => vertex.id)).not.toContain(product.id);
    const selected = index.filterProjection(projected.handles, { ...empty, families: ['product'] });
    expect(selected.handles.vertices.map(handle => index.vertex(handle).id)).toEqual([used.id]); expect(selected.handles.edges).toEqual([]); expect(selected.hiddenVertices).toBe('2'); expect(selected.hiddenEdges).toBe('2');
    expect(Buffer.from(selected.vertexMask, 'base64').length).toBe(Math.ceil(projected.handles.vertices.length / 8));
    const restored = index.filterProjection(projected.handles, empty); expect(restored.handles).toEqual(projected.handles); expect(restored.filtered).toBe(false);
    expect(() => index.filterProjection({ vertices: projected.handles.vertices, edges: [{ ...projected.handles.edges[0]!, from: 999 }] }, empty)).toThrow();
    expect(() => index.filterProjection(projected.handles, empty, { cancelled: () => true })).toThrow(expect.objectContaining({ code: 'cancelled' }));
  });
  it('indexes forward/reverse directions, every parallel edge and self-loop without layout inference', () => {
    const { index, a, b, c, edges } = fixture(); const result = run(index, neighbours(a.identity));
    if (result.operation !== 'graph.neighbours') throw new Error('Unexpected operation');
    expect(result.value.projection.vertices.map(vertex => vertex.id)).toEqual([a.id, b.id, c.id].sort());
    expect(new Set(result.value.projection.edges.map(item => item.id))).toEqual(new Set(edges.map(item => item.id)));
    expect(result.work).toEqual({ visitedVertices: 3, scannedEdges: 5 }); expect(result.value.projection).toMatchObject({ hiddenVertices: '1', hiddenEdges: '0', complete: true, omissions: ['filter'] });
    for (const item of result.handles.edges) { expect(index.edge(item.handle).from).toBe(index.vertex(item.from).id); expect(index.edge(item.handle).to).toBe(index.vertex(item.to).id); }
    const reverse = run(index, path(a.identity, c.identity, DEFAULT_QUERY_LIMITS, 'reverse'));
    if (reverse.operation !== 'graph.path') throw new Error('Unexpected operation');
    expect(reverse.value.found).toBe(true); expect(reverse.value.projection.edges.map(item => item.label)).toEqual(['ca']); expect(reverse.value.projection.edges[0]!.from).toBe(c.id);
    const both = run(index, neighbours(a.identity, DEFAULT_QUERY_LIMITS, 'both')); if (both.operation === 'graph.neighbours') expect(both.work.scannedEdges).toBe(5);
  });
  it('resolves exact detached lookup/details without allowing callers to mutate accepted data', () => {
    const { index, a } = fixture(); const lookup = run(index, request('element.lookup', { identity: a.identity })); const details = run(index, request('element.details', { identity: a.identity }));
    if (lookup.operation === 'element.lookup') { expect(lookup.value.vertex).toEqual(a); expect(lookup.value.vertex).not.toBe(a); }
    if (details.operation === 'element.details') { expect(details.value.attributes).toEqual(a.attributes); expect(details.value.attributes).not.toBe(a.attributes); }
    if (lookup.operation === 'element.lookup' && lookup.value.vertex) Object.assign(lookup.value.vertex, { label: 'caller mutation' });
    if (details.operation === 'element.details') Object.assign(details.value.attributes, { value: { type: 'string', value: 'caller mutation' } });
    const again = run(index, request('element.lookup', { identity: a.identity }));
    if (again.operation === 'element.lookup') expect(again.value.vertex?.label).toBe(a.label);
    const detailsAgain = run(index, request('element.details', { identity: a.identity }));
    if (detailsAgain.operation === 'element.details') expect(detailsAgain.value.attributes).toEqual(a.attributes);
    const absent = version('missing'); const missing = run(index, request('element.lookup', { identity: absent.identity })); if (missing.operation === 'element.lookup') expect(missing.value.vertex).toBeNull();
    expect(() => index.execute(request('element.details', { identity: absent.identity }))).toThrow(expect.objectContaining({ code: 'not-found' }));
    expect(() => index.vertex(-1)).toThrow(); expect(() => index.edge(0.5)).toThrow();
  });
  it('selects, counts, filters and groups using scalar getters without reconstructing full records', () => {
    const { index, a, store } = fixture(); const vertices = vi.spyOn(store, 'vertex'); const edges = vi.spyOn(store, 'edge');
    const selected = index.select(neighbours(a.identity));
    if (selected.operation !== 'graph.neighbours') throw new Error('Wrong operation');
    expect(selected.handles.edges).toHaveLength(5);
    index.select(request('graph.counts', { filter: empty })); index.groups(empty, 'kind'); index.filterProjection(selected.handles, empty);
    expect(vertices).not.toHaveBeenCalled(); expect(edges).not.toHaveBeenCalled();
  });
  it('returns deterministic shortest observed path, proven empty absence and zero-length success', () => {
    const { index, a, b, c, d } = fixture();
    const found = run(index, path(a.identity, c.identity)); if (found.operation === 'graph.path') { expect(found.value.found).toBe(true); expect(found.value.projection.edges.map(item => item.label)).toEqual(['a1', 'bc']); expect(found.value.complete).toBe(true); }
    const absence = run(index, path(a.identity, d.identity)); if (absence.operation === 'graph.path') { expect(absence.value).toMatchObject({ found: false, complete: true }); expect(absence.value.projection.vertices).toEqual([]); }
    const zero = run(index, path(b.identity, b.identity, { ...DEFAULT_QUERY_LIMITS, maxHops: 0, maxEdges: 0 })); if (zero.operation === 'graph.path') expect(zero.value).toMatchObject({ found: true, complete: true, projection: { edges: [] } });
    const missing = run(index, path(a.identity, version('missing').identity)); if (missing.operation === 'graph.path') expect(missing.value).toMatchObject({ found: false, complete: true });
  });
  it.each(['maxHops', 'maxVisitedVertices', 'maxScannedEdges'] as const)('never asserts absence after %s bounds stop exploration', dimension => {
    const { index, a, c } = fixture(); const limits = { ...DEFAULT_QUERY_LIMITS, [dimension]: dimension === 'maxHops' ? 0 : 1 };
    const result = run(index, path(a.identity, c.identity, limits)); if (result.operation !== 'graph.path') throw new Error('Unexpected operation');
    expect(result.value.found).toBeNull(); expect(result.value.complete).toBe(false); expect(result.value.projection.omissions).toContain('work-limit');
    expect(result.work.visitedVertices).toBeLessThanOrEqual(limits.maxVisitedVertices); expect(result.work.scannedEdges).toBeLessThanOrEqual(limits.maxScannedEdges);
  });
  it('distinguishes visible truncation from traversal work and preserves true path discovery with zero edge budget', () => {
    const { index, a, c } = fixture(); const result = run(index, path(a.identity, c.identity, { ...DEFAULT_QUERY_LIMITS, maxEdges: 0, maxVertices: 1 }));
    if (result.operation === 'graph.path') { expect(result.value).toMatchObject({ found: true, complete: false }); expect(result.value.projection.omissions).toContain('visible-limit'); expect(result.value.projection.edges).toEqual([]); expect(result.value.projection.vertices).toHaveLength(1); }
    const visible = run(index, neighbours(a.identity, { ...DEFAULT_QUERY_LIMITS, maxVertices: 2, maxEdges: 1 })); if (visible.operation === 'graph.neighbours') { expect(visible.value.projection.vertices).toHaveLength(2); expect(visible.value.projection.edges).toHaveLength(1); expect(visible.value.projection.omissions).toContain('visible-limit'); expect(visible.value.projection.omissions).not.toContain('work-limit'); }
  });
  it('charges filtered edges before predicates and handles exact scan and hop boundaries', () => {
    const { index, a } = fixture(); const input = request('graph.neighbours', { ...neighbours(a.identity, { ...DEFAULT_QUERY_LIMITS, maxScannedEdges: 1 }).payload, relations: ['ownership'] });
    const result = run(index, input); if (result.operation === 'graph.neighbours') { expect(result.work.scannedEdges).toBe(1); expect(result.value.projection.omissions).toContain('work-limit'); expect(result.value.projection.edges).toEqual([]); }
    const exact = run(index, neighbours(a.identity, { ...DEFAULT_QUERY_LIMITS, maxScannedEdges: 5, maxHops: 2 })); if (exact.operation === 'graph.neighbours') { expect(exact.work.scannedEdges).toBe(5); expect(exact.value.projection.complete).toBe(true); }
    const one = version('only'); const loop = edge('loop', one, one); const singleton = new QueryIndex(graph([one], [loop]), binding); const closed = run(singleton, neighbours(one.identity, { ...DEFAULT_QUERY_LIMITS, maxHops: 0, maxScannedEdges: 1 })); if (closed.operation === 'graph.neighbours') expect(closed.value.projection.complete).toBe(true);
  });
  it('preserves explicit unresolved uncertainty and unavailable neighbour identity', () => {
    const a = version('A'); const missing = unresolved('unknown'); const end = version('end'); const index = new QueryIndex(graph([a, missing, end], [edge('unknown-edge', a, missing)]), binding);
    const result = run(index, neighbours(a.identity)); if (result.operation === 'graph.neighbours') { expect(result.value.projection.complete).toBe(false); expect(result.value.projection.omissions).toContain('unresolved'); }
    const unknown = run(index, path(a.identity, end.identity)); if (unknown.operation === 'graph.path') expect(unknown.value).toMatchObject({ found: null, complete: false });
    const unavailable = run(index, neighbours(version('not-indexed').identity)); if (unavailable.operation === 'graph.neighbours') expect(unavailable.value.projection.omissions).toEqual(['unavailable']);
  });
  it('uses conditional family/state selectors and eligible incident relations consistently', () => {
    const a = version('A', 'A', 'product'); const b = version('B', 'B', 'profile'); const used = use(a); const open = finding('F-open', 'open'); const verified = finding('F-done', 'verified'); const unknown = unresolved('unknown'); const owner = participant(); const other = version('Q', 'Q', 'source', 'q');
    const index = new QueryIndex(graph([a, b, used, open, verified, unknown, owner, other], [edge('use-profile', used, b, 'profile'), edge('open-subject', open, a, 'finding-subject', false), edge('done-subject', verified, a, 'finding-subject', false), edge('actor', a, owner, 'participant', false), edge('cross', a, other, 'other-reference', false)]), binding);
    const counts = (filter: Filter) => { const result = run(index, request('graph.counts', { filter })); if (result.operation !== 'graph.counts') throw new Error('Unexpected operation'); return result.value; };
    expect(counts(empty)).toEqual({ vertices: '8', edges: '5', findings: '2' });
    expect(counts({ ...empty, families: ['product'] })).toEqual({ vertices: '5', edges: '3', findings: '2' });
    expect(counts({ ...empty, findingStates: ['open'] })).toEqual({ vertices: '7', edges: '4', findings: '1' });
    expect(counts({ ...empty, families: ['product'], findingStates: ['open'] })).toEqual({ vertices: '4', edges: '2', findings: '1' });
    expect(counts({ ...empty, findingStates: ['open'], relations: ['finding-subject'] })).toEqual({ vertices: '2', edges: '1', findings: '1' });
    const selected = { ...empty, families: ['product' as const], relations: ['profile' as const] }; expect(counts(selected)).toEqual({ vertices: '0', edges: '0', findings: '0' });
    const search = run(index, request('search.page', { text: '', filter: selected, order: 'identity', limit: 10, cursor: null })); if (search.operation === 'search.page') expect(search.value.items).toEqual([]);
    expect(counts({ ...empty, projectIds: ['p'] })).toEqual({ vertices: '7', edges: '4', findings: '2' });
    const groups = index.groups(empty, 'family'); expect(groups.ungroupedVertices).toBe('4'); expect(groups.crossGroupEdges).toBe('2'); expect(groups.ungroupedEdges).toBe('3'); expect(groups.groups.map(group => [group.value, group.vertices])).toEqual([['product', '2'], ['profile', '1'], ['source', '1']]);
    const states = index.groups(empty, 'finding-state'); expect(states.ungroupedVertices).toBe('6'); expect(states.ungroupedEdges).toBe('5'); expect(states.groups).toHaveLength(2);
    const projects = index.groups(empty, 'project'); expect(projects.crossGroupEdges).toBe('1'); expect(projects.groups.reduce((sum, group) => sum + BigInt(group.edges), 0n) + BigInt(projects.crossGroupEdges) + BigInt(projects.ungroupedEdges)).toBe(5n);
    expect(index.groups(empty, 'kind').groups.every(group => JSON.parse(group.id)[0] === 'jai.fabric-explorer.group/1')).toBe(true);
  });
  it('searches literal case-insensitive labels/identities in deterministic order with remaining hidden counts', () => {
    const { index, a, b, c } = fixture(); const firstRequest = request('search.page', { text: 'BUILD', filter: empty, order: 'label', limit: 1, cursor: null });
    const first = run(index, firstRequest); if (first.operation !== 'search.page') throw new Error('Unexpected operation');
    expect(first.value.items.map(vertex => vertex.id)).toEqual([b.id]); expect(first.value.hidden).toBe('2'); expect(first.value.nextCursor!.queryKey).toBe(queryKey(firstRequest)); expect(first.value.nextCursor!.offset).toBe('1');
    const second = run(index, request('search.page', { ...firstRequest.payload, cursor: first.value.nextCursor })); if (second.operation !== 'search.page') throw new Error('Unexpected operation'); expect(second.value.items.map(vertex => vertex.id)).toEqual([c.id]); expect(second.value.hidden).toBe('1');
    const last = run(index, request('search.page', { ...firstRequest.payload, cursor: second.value.nextCursor })); if (last.operation === 'search.page') { expect(last.value.items.map(vertex => vertex.id)).toEqual([a.id]); expect(last.value).toMatchObject({ hidden: '0', complete: true, nextCursor: null }); }
    const identity = run(index, request('search.page', { text: ref('A').version_id, filter: empty, order: 'identity', limit: 10, cursor: null })); if (identity.operation === 'search.page') expect(identity.value.items.map(vertex => vertex.id)).toEqual([a.id]);
  });
  it('authenticates cursor offsets, exact raw query key, operation order and work generation without retention', () => {
    const { index, data } = fixture(); const base = request('search.page', { text: '', filter: empty, order: 'identity', limit: 1, cursor: null }); const first = run(index, base); if (first.operation !== 'search.page') throw new Error('Unexpected operation'); const cursor = first.value.nextCursor!;
    for (const changed of [{ ...cursor, offset: '0' }, { ...cursor, token: '0'.repeat(64) }, { ...cursor, token: 'invalid' }]) expect(() => index.execute(request('search.page', { ...base.payload, cursor: changed }))).toThrow(expect.objectContaining({ code: 'cursor-mismatch' }));
    expect(() => index.execute(request('search.page', { ...base.payload, text: 'other', cursor }))).toThrow(expect.objectContaining({ code: 'cursor-mismatch' }));
    expect(() => index.execute(request('search.page', { ...base.payload, order: 'label', cursor }))).toThrow(expect.objectContaining({ code: 'cursor-mismatch' }));
    const another = new QueryIndex(data, binding); expect(() => another.execute(request('search.page', { ...base.payload, cursor }))).toThrow(expect.objectContaining({ code: 'cursor-mismatch' }));
    expect(() => index.execute({ ...base, binding: { ...binding, generation: '2' } })).toThrow(expect.objectContaining({ code: 'stale-generation' }));
    expect(() => index.execute({ ...base, binding: { ...binding, sessionId: 'foreign' } })).toThrow(expect.objectContaining({ code: 'session-mismatch' }));
    expect(() => index.execute({ ...base, binding: { ...binding, capability: 'foreign' } })).toThrow(expect.objectContaining({ code: 'capability-mismatch' }));
    expect(run(index, request('search.page', { ...base.payload, cursor })).value).toEqual(run(index, request('search.page', { ...base.payload, cursor })).value);
  });
  it('cancels scan loops through a live atomic observer without disposing the accepted index', () => {
    const { index, a } = fixture(); const flag = new Int32Array(new SharedArrayBuffer(4)); let calls = 0;
    const control = { cancelled: () => { if (++calls === 4) Atomics.store(flag, 0, 1); return Atomics.load(flag, 0) !== 0; } };
    expect(() => index.execute(neighbours(a.identity), control)).toThrow(expect.objectContaining({ code: 'cancelled' }));
    Atomics.store(flag, 0, 0); expect(run(index, neighbours(a.identity)).operation).toBe('graph.neighbours');
    expect(() => index.execute(request('graph.counts', { filter: empty }), { cancelled: () => true })).toThrow(expect.objectContaining({ code: 'cancelled' }));
    let checks = 0; expect(() => index.groups({ ...empty, families: ['source'] }, 'kind', { cancelled: () => ++checks > 3 })).toThrow(expect.objectContaining({ code: 'cancelled' }));
    const counts = run(index, request('graph.counts', { filter: empty })); if (counts.operation === 'graph.counts') expect(counts.value.vertices).toBe('4');
  });
  it('is independent of input record order and revokes lookup/layout handles/cursors on disposal', () => {
    const { index, data, a } = fixture(); const reversed = new QueryIndex({ ...data, records: [...data.records].reverse() }, binding);
    expect(run(index, neighbours(a.identity))).toEqual(run(reversed, neighbours(a.identity)));
    expect(index.groups(empty, 'kind')).toEqual(reversed.groups(empty, 'kind'));
    index.dispose(); index.dispose(); expect(() => index.execute(neighbours(a.identity))).toThrow(expect.objectContaining({ code: 'stale-generation' })); expect(() => index.vertex(0)).toThrow(); expect(() => index.edge(0)).toThrow(); expect(() => index.groups(empty, 'kind')).toThrow();
  });
  it('handles empty graphs and zero-result search without fabricated cursors', () => {
    const index = new QueryIndex(graph([], []), binding); const search = run(index, request('search.page', { text: '', filter: empty, order: 'identity', limit: 5000, cursor: null }));
    if (search.operation === 'search.page') expect(search.value).toEqual({ items: [], hidden: '0', complete: true, nextCursor: null });
    const counts = run(index, request('graph.counts', { filter: empty })); if (counts.operation === 'graph.counts') expect(counts.value).toEqual({ vertices: '0', edges: '0', findings: '0' });
    expect(index.groups(empty, 'project')).toEqual({ by: 'project', groups: [], ungroupedVertices: '0', ungroupedEdges: '0', crossGroupEdges: '0' });
    expect(() => index.execute(request('graph.neighbours', { identity: version('missing').identity, direction: 'forward', relations: [], causalOnly: false, limits: DEFAULT_QUERY_LIMITS }))).toThrow();
  });
  it('enforces the actual 50k distinct-edge ceiling on a filtered high-degree hub', () => {
    const a = version('hub'); const b = version('target'); const edges = Array.from({ length: 50001 }, (_, index) => edge(`parallel-${String(index).padStart(6, '0')}`, a, b));
    const data = graph([a, b], edges); const index = new QueryIndex(data, binding);
    const input = request('graph.neighbours', { ...neighbours(a.identity).payload, relations: ['ownership'] });
    const limited = run(index, input); if (limited.operation !== 'graph.neighbours') throw new Error('Unexpected operation');
    expect(limited.work).toEqual({ visitedVertices: 1, scannedEdges: 50000 }); expect(limited.value.projection.complete).toBe(false); expect(limited.value.projection.omissions).toContain('work-limit'); expect(limited.value.projection.edges).toEqual([]);
    const exact = new QueryIndex(graph([a, b], edges.slice(0, 50000)), binding); const complete = run(exact, input); if (complete.operation === 'graph.neighbours') { expect(complete.work.scannedEdges).toBe(50000); expect(complete.value.projection.complete).toBe(true); }
    for (const maxEdges of [8000, 20000]) { const visible = run(exact, neighbours(a.identity, { ...DEFAULT_QUERY_LIMITS, maxVertices: 2, maxEdges })); if (visible.operation !== 'graph.neighbours') throw new Error('Unexpected operation'); expect(visible.value.projection.edges).toHaveLength(maxEdges); expect(visible.value.projection.hiddenEdges).toBe(String(50000 - maxEdges)); expect(visible.value.projection.omissions).toContain('visible-limit'); expect(visible.value.projection.omissions).not.toContain('work-limit'); }
  }, 20000);
  it('honours visible hard bounds on a broad observed component without an edge endpoint escape', () => {
    const a = version('root'); const children = Array.from({ length: 5000 }, (_, index) => version(`child-${index}`)); const edges = children.map((child, index) => edge(`child-${index}`, a, child));
    const index = new QueryIndex(graph([a, ...children], edges), binding); const result = run(index, neighbours(a.identity, { ...DEFAULT_QUERY_LIMITS, maxVertices: 5000, maxEdges: 20000 }));
    if (result.operation !== 'graph.neighbours') throw new Error('Unexpected operation');
    expect(result.value.projection.vertices).toHaveLength(5000); expect(result.value.projection.edges).toHaveLength(4999); expect(result.value.projection).toMatchObject({ hiddenVertices: '1', hiddenEdges: '1', complete: false });
    expect(result.value.projection.omissions).toContain('visible-limit'); expect(result.work).toEqual({ visitedVertices: 5001, scannedEdges: 5000 });
    const defaults = run(index, neighbours(a.identity)); if (defaults.operation === 'graph.neighbours') expect(defaults.value.projection.vertices).toHaveLength(2000);
  }, 20000);
  it.each([['maxVertices', 0], ['maxVertices', 5001], ['maxEdges', -1], ['maxEdges', 20001], ['maxVisitedVertices', 0], ['maxVisitedVertices', 10001], ['maxScannedEdges', 0], ['maxScannedEdges', 50001], ['maxHops', -1], ['maxHops', 33]] as const)('rejects out-of-contract work/visible limit %s=%s', (key, value) => {
    const { index, a } = fixture(); expect(() => index.execute(neighbours(a.identity, { ...DEFAULT_QUERY_LIMITS, [key]: value }))).toThrow();
  });
  it('rejects duplicate/missing endpoints, cardinality mismatch, malformed limits and unrelated operations', () => {
    const { a, b, data, edges, index } = fixture(); expect(() => new QueryIndex({ ...data, records: [a, a] }, binding)).toThrow();
    expect(() => new QueryIndex(graph([a], []), { ...binding, generation: '2' })).toThrow();
    const bad = { ...edges[0]!, to: 'absent' }; expect(() => new QueryIndex({ ...graph([a, b], [edges[0]!]), records: [a, b, bad] }, binding)).toThrow();
    expect(() => index.execute(neighbours(a.identity, { ...DEFAULT_QUERY_LIMITS, maxVertices: 5001 }))).toThrow();
    expect(() => index.execute({ protocol: PROTOCOL, kind: 'request', requestId: 'no-import', binding, operation: 'snapshot.refresh', payload: {} } as Request as GraphRequest)).toThrow(expect.objectContaining({ code: 'unknown-operation' }));
    expect(() => index.groups(empty, 'unsupported' as 'kind')).toThrow();
  });
});
