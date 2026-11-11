// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Presentation boundary tests use real indexed queries/transport and controlled owned bridge promises. */
import { describe, expect, it, vi } from 'vitest';
import { PROTOCOL, edgeKey, elementKey } from '@jai/fabric-explorer-contracts';
import type { Binding, Edge, RequestPayloads, Vertex } from '@jai/fabric-explorer-contracts';
import type { DesktopBridge } from '../src/shell/bridge.js';
import type { ShellState } from '../src/shell/controller.js';
import { DEFAULT_PREFERENCES } from '../src/shell/preferences.js';
import { ExploreController } from '../src/renderer/presentation/controller.js';
import { ExploreService } from '../src/explore/service.js';
import { QueryTransfer } from '../src/explore/transport.js';
import type { GraphRequest } from '../src/graph/types.js';
import { QueryIndex } from '../src/graph/query-index.js';
import { ImportModel } from '../src/import/model.js';
import { modelInput, versionFact, revision } from './import-fixtures.js';
function deferred<T>() { let resolve!: (value: T) => void; const promise = new Promise<T>(done => { resolve = done; }); return { promise, resolve }; }
function fixture(versionCount = 1) {
  const model = new ImportModel(modelInput()); const fact = versionFact(); if (fact.kind !== 'version') throw new Error('Version fixture required');
  model.consume({ sequence: '0', facts: Array.from({ length: versionCount }, (_, index) => ({ ...fact, ref: { ...fact.ref, logical_id: `record-${index}` } })), next: null }); const ready = model.finish();
  const versions = [...model.records()] as Vertex[]; const vertex = versions[0]!;
  const identity = { kind: 'finding' as const, projectId: 'project', ledgerId: 'ledger', findingId: 'F-1' };
  const finding: Vertex = { identity, id: elementKey(identity), kind: 'finding', label: 'Finding', source: { ...vertex.source, family: 'findings', sourceId: 'findings', rootId: 'root-findings', relativePath: 'findings.jsonl', revisionId: 'revision-findings', adapterVersion: 'jai.fabric-explorer.findings/1', pointer: '/0', sequence: '1' }, attributes: vertex.attributes, state: 'open', severity: 'high', findingKind: 'defect', rounds: '0', recordedExpiry: null };
  const edgeIdentity = { kind: 'occurrence' as const, projectId: 'project', origin: finding.identity, pointer: '/subject', occurrence: 0, from: finding.identity, to: vertex.identity };
  const edge: Edge = { id: edgeKey(edgeIdentity), identity: edgeIdentity, from: finding.id, to: vertex.id, label: 'Complete subject relation', relation: 'finding-subject', source: finding.source, attributes: vertex.attributes, causal: false, basis: 'exact-reference' };
  const snapshot = { ...ready.descriptor, sources: [...ready.descriptor.sources, revision('findings')], counts: { vertices: String(versionCount + 1), edges: '1', findings: '1' } };
  const binding: Binding = { sessionId: 'session', capability: 'capability', generation: '1' };
  const service = new ExploreService(new QueryIndex({ snapshot, records: [...versions, finding, edge] }, binding), binding);
  const query = async (operation: GraphRequest['operation'], context: Binding, requestId: string, value: unknown, findingsOnly = false) => {
    const request = { protocol: PROTOCOL, kind: 'request', operation, binding: context, requestId, payload: value } as GraphRequest;
    const transfer = new QueryTransfer(request, true); let page = service.start(request, undefined, findingsOnly ? 'findings' : 'all');
    for (;;) { const view = transfer.accept(page, context); if (view) return view; page = service.next({ binding: context, requestId, continuationToken: page.continuationToken! }); }
  };
  const shell: ShellState = { sessionId: 'session', capability: 'capability', sources: [], preferences: DEFAULT_PREFERENCES, warning: null, snapshot, report: null, stale: false };
  const bridge: DesktopBridge = {
    getState: async () => shell, pickRoots: async () => undefined, closeRoots: async () => undefined, importSnapshot: async () => undefined, refreshSnapshot: async () => undefined,
    lookup: (b, id, value) => query('element.lookup', b, id, value), details: (b, id, value) => query('element.details', b, id, value),
    search: vi.fn((b, id, value) => query('search.page', b, id, value)), searchFindings: (b, id, value) => query('search.page', b, id, value, true),
    counts: (b, id, value) => query('graph.counts', b, id, value), neighbours: (b, id, value) => query('graph.neighbours', b, id, value), path: (b, id, value) => query('graph.path', b, id, value),
    dropQuery: vi.fn(async input => { service.drop(input); }),
    layout: (b, id, token, options) => service.layout({ binding: b, requestId: id, projectionToken: token, options }),
    filterProjection: (b, id, baseProjectionToken, filter) => Promise.resolve(service.filterProjection({ binding: b, requestId: id, baseProjectionToken, filter })),
    groups: (b, id, filter, by) => Promise.resolve(service.groups({ binding: b, requestId: id, filter, by })),
    pageSource: vi.fn(async (_b, _id, { length: _length, ...value }) => ({ operation: 'source.page', status: 'ok', payload: { ...value, bytesBase64: Buffer.from('é').toString('base64'), byteLength: 2, eof: true } })),
    cancelRequest: vi.fn(async () => undefined), cancelSelection: async () => false, updatePreferences: async value => value,
  };
  return { controller: new ExploreController(bridge), bridge, shell, vertex, finding, edge, service };
}
describe('immutable read-only exploration presentation', () => {
  it('forgets retired ownership locally before cancelling old jobs or releasing their projection tokens', async () => {
    const f = fixture(); await f.controller.setShell(f.shell);
    const original = f.bridge.lookup; const held = deferred<Awaited<ReturnType<DesktopBridge['lookup']>>>(); f.bridge.lookup = () => held.promise;
    const pending = f.controller.select(f.vertex.identity);
    vi.mocked(f.bridge.dropQuery).mockClear(); vi.mocked(f.bridge.cancelRequest).mockClear();
    await f.controller.setShell({ ...f.shell, capability: null, snapshot: null });
    held.resolve(await original({ sessionId: 'session', capability: 'capability', generation: '1' }, 'retired-selection', { identity: f.vertex.identity })); await pending;
    expect(f.bridge.dropQuery).not.toHaveBeenCalled(); expect(f.bridge.cancelRequest).not.toHaveBeenCalled(); expect(f.controller.getSnapshot().selection).toBeNull();
    await f.controller.dispose();
  });
  it('automatically loads one overview, immutable full attributes and a true findings-only page', async () => {
    const f = fixture(); const listener = vi.fn(); const unsubscribe = f.controller.subscribe(listener); const initial = f.controller.getSnapshot(); expect(f.controller.getSnapshot()).toBe(initial);
    await f.controller.setShell(f.shell); const state = f.controller.getSnapshot();
    expect(state.projection?.vertices).toHaveLength(2); expect(state.findings?.items.map(v => v.id)).toEqual([f.finding.id]); expect(state.layout?.positions).toHaveLength(2); expect(Object.isFrozen(state.projection?.vertices)).toBe(true); expect(listener).toHaveBeenCalled();
    await f.controller.setShell({ ...f.shell, stale: true }); expect(f.bridge.search).toHaveBeenCalledTimes(1); expect(f.controller.getSnapshot().projection).toBe(state.projection);
    unsubscribe(); await f.controller.dispose();
  });
  it('inspects exact parallel edge endpoints, finding subjects and original byte offsets without numeric coercion', async () => {
    const f = fixture(); await f.controller.setShell(f.shell); await f.controller.selectElement(f.edge.id);
    expect(f.controller.getSnapshot().selection?.element.label).toBe('Complete subject relation'); expect(f.controller.getSnapshot().selection?.endpoints.map(v => v.id)).toEqual([f.finding.id, f.vertex.id]);
    expect(f.controller.getSnapshot().selection?.attributes).toEqual({ kind: 'inline', value: { type: 'integer', value: '9007199254740993' } });
    await f.controller.pageSource('7', 2); expect(f.controller.getSnapshot().sourcePage).toMatchObject({ text: 'é', page: { offset: '7', byteLength: 2 } });
    await f.controller.select(f.finding.identity); expect(f.controller.getSnapshot().selection?.subjectCandidates.map(v => v.id)).toEqual([f.vertex.id]); await f.controller.dispose();
  });
  it('reverses exact filters without importing and releases every base and derived projection using its owner', async () => {
    const f = fixture(); await f.controller.setShell(f.shell); const original = f.controller.getSnapshot().projection!;
    await f.controller.setFilter({ projectIds: [], families: [], findingStates: ['verified'], relations: [] }); expect(f.controller.getSnapshot().projection?.vertices.map(v => v.id)).toEqual([f.vertex.id]); expect(f.controller.getSnapshot().projection?.hiddenVertices).toBe('1');
    await f.controller.setFilter({ projectIds: [], families: [], findingStates: [], relations: [] }); expect(f.controller.getSnapshot().projection?.vertices).toEqual(original.vertices); expect(f.controller.getSnapshot().projection?.edges).toEqual(original.edges);
    await f.controller.dispose(); const drops = vi.mocked(f.bridge.dropQuery).mock.calls.map(([input]) => input); expect(drops).toHaveLength(4); expect(new Set(drops.map(drop => drop.projectionToken)).size).toBe(4);
  });
  it('drops late selections after a generation is closed and preserves the prior graph on failed refresh', async () => {
    const f = fixture(); await f.controller.setShell(f.shell); const before = f.controller.getSnapshot().projection; const pending = deferred<Awaited<ReturnType<DesktopBridge['lookup']>>>(); const lookup = f.bridge.lookup; f.bridge.lookup = () => pending.promise;
    const selecting = f.controller.select(f.vertex.identity); await f.controller.setShell({ ...f.shell, stale: true }); expect(f.controller.getSnapshot().projection).toBe(before);
    await f.controller.setShell({ ...f.shell, capability: null, snapshot: null }); pending.resolve(await lookup({ sessionId: 'session', capability: 'capability', generation: '1' }, 'controlled-late', { identity: f.vertex.identity })); await selecting;
    expect(f.controller.getSnapshot().selection).toBeNull(); expect(f.controller.getSnapshot().projection).toBeNull(); expect(f.bridge.cancelRequest).not.toHaveBeenCalled(); await f.controller.dispose();
  });
  it('retains an old nonempty page during an asynchronous search, so a capture must await the requested result and exact identity', async () => {
    const f = fixture(2); await f.controller.setShell(f.shell);
    const before = f.controller.getSnapshot().search!; const expected = before.items.find(item => item.identity.kind === 'version' && item.identity.ref.logical_id === 'record-1')!;
    const waiting = deferred<Awaited<ReturnType<DesktopBridge['search']>>>(); const original = f.bridge.search;
    f.bridge.search = (_binding, _id, input) => input.text === 'record-1' ? waiting.promise : original(_binding, _id, input);
    const searching = f.controller.search('record-1');
    expect(f.controller.getSnapshot().busy).toContain('search');
    expect(f.controller.getSnapshot().search).toBe(before);
    expect(before.items.some(item => item.kind === expected.kind)).toBe(true);
    expect(before.items.find(item => item.kind === expected.kind)!.id).not.toBe(expected.id);
    waiting.resolve(await original({ sessionId: 'session', capability: 'capability', generation: '1' }, 'requested-capture-search', { text: 'record-1', filter: { projectIds: [], families: [], findingStates: [], relations: [] }, order: 'identity', limit: 50, cursor: null }));
    await searching;
    expect(f.controller.getSnapshot().busy).toEqual([]);
    expect(f.controller.getSnapshot().search?.text).toBe('record-1');
    expect(f.controller.getSnapshot().search?.items.map(item => item.id)).toEqual([expected.id]);
    await f.controller.select(expected.identity);
    expect(f.controller.getSnapshot().selection?.element.id).toBe(expected.id);
    await f.controller.dispose();
  });
  it('supersedes search promises, keeps bounded intent history and never exposes arbitrary native errors', async () => {
    const f = fixture(); await f.controller.setShell(f.shell); const original = f.bridge.search; const waiting = deferred<Awaited<ReturnType<DesktopBridge['search']>>>(); f.bridge.search = (_b, _id, input) => input.text === 'old' ? waiting.promise : original(_b, _id, input);
    const old = f.controller.search('old'); await f.controller.search('new'); waiting.resolve(await original({ sessionId: 'session', capability: 'capability', generation: '1' }, 'late-search', { text: '', filter: { projectIds: [], families: [], findingStates: [], relations: [] }, order: 'identity', limit: 50, cursor: null })); await old;
    expect(f.controller.getSnapshot().search?.text).toBe('new'); for (let i = 0; i < 52; i++) await f.controller.select(i % 2 ? f.vertex.identity : f.finding.identity);
    for (let i = 0; i < 49; i++) await f.controller.back(); expect(f.controller.getSnapshot().history.canBack).toBe(false); expect(f.controller.getSnapshot().history.canForward).toBe(true);
    f.bridge.search = async () => { throw new Error('/secret/native/path'); }; await f.controller.search('bad'); expect(f.controller.getSnapshot().error).not.toContain('/secret'); await f.controller.dispose();
  });
  it('rejects malformed masks and endpoint removals without replacing the prior view or leaking derived tokens', async () => {
    const f = fixture(); await f.controller.setShell(f.shell); const original = f.controller.getSnapshot().projection; const valid = f.bridge.filterProjection;
    for (const vertexMask of ['AA==', '/w==', '']) {
      f.bridge.filterProjection = async (...args) => ({ ...await valid(...args), vertexMask });
      await f.controller.setFilter({ projectIds: [], families: [], findingStates: [], relations: [] });
      expect(f.controller.getSnapshot().projection).toBe(original); expect(f.controller.getSnapshot().error).toBeTruthy();
    }
    await f.controller.dispose(); expect(f.bridge.dropQuery).toHaveBeenCalledTimes(5);
  });
  it('cancels owned requests and drops a late projection before it can replace the accepted view', async () => {
    const f = fixture(); await f.controller.setShell(f.shell); const before = f.controller.getSnapshot().projection; const started = deferred<void>(); const pending = deferred<Awaited<ReturnType<DesktopBridge['neighbours']>>>(); const original = f.bridge.neighbours;
    let captured!: Parameters<DesktopBridge['neighbours']>; f.bridge.neighbours = (...args) => { captured = args; started.resolve(); return pending.promise; };
    const work = f.controller.neighbours({ identity: f.vertex.identity }); await started.promise; await f.controller.cancel(); pending.resolve(await original(...captured)); await work;
    expect(f.controller.getSnapshot().projection).toBe(before); expect(f.controller.getSnapshot().busy).toEqual([]); expect(f.bridge.cancelRequest).toHaveBeenCalled();
    await f.controller.dispose(); expect(f.bridge.dropQuery).toHaveBeenCalledTimes(3);
  });
  it('advances a real authenticated page without retaining an unbounded history of search DTOs', async () => {
    const f = fixture(60); await f.controller.setShell(f.shell); const first = f.controller.getSnapshot().search!; expect(first.items).toHaveLength(50); expect(first.hidden).toBe('11');
    await f.controller.search('', 'identity', true); const next = f.controller.getSnapshot().search!; expect(next.items).toHaveLength(11); expect(next.complete).toBe(true); expect(next.items.some(item => first.items.some(previous => previous.id === item.id))).toBe(false);
    await f.controller.dispose();
  });
  it('reconstructs the exact edge graph context when Back crosses a different neighbourhood', async () => {
    const f = fixture(); await f.controller.setShell(f.shell); await f.controller.selectElement(f.edge.id);
    await f.controller.neighbours({ identity: f.vertex.identity, limits: { maxVertices: 2000, maxEdges: 8000, maxVisitedVertices: 10000, maxScannedEdges: 50000, maxHops: 0 } }); await f.controller.select(f.vertex.identity);
    await f.controller.back(); expect(f.controller.getSnapshot().selection?.element.id).toBe(f.edge.id); expect(f.controller.getSnapshot().projection?.vertices.map(vertex => vertex.id)).toEqual([f.vertex.id]); await f.controller.back();
    expect(f.controller.getSnapshot().selection?.element.id).toBe(f.edge.id); expect(f.controller.getSnapshot().projection?.edges.map(edge => edge.id)).toContain(f.edge.id);
    await f.controller.dispose();
  });
  it('does not roll back the latest graph base when a newer filter wins before graph filtering returns', async () => {
    const f = fixture(); await f.controller.setShell(f.shell); const original = f.bridge.filterProjection;
    const started = deferred<void>(); const held = deferred<Awaited<ReturnType<DesktopBridge['filterProjection']>>>(); let first = true; let result!: Awaited<ReturnType<DesktopBridge['filterProjection']>>;
    f.bridge.filterProjection = async (...args) => { const value = await original(...args); if (first) { first = false; result = value; started.resolve(); return held.promise; } return value; };
    const graph = f.controller.neighbours({ identity: f.vertex.identity, limits: { maxVertices: 2000, maxEdges: 8000, maxVisitedVertices: 10000, maxScannedEdges: 50000, maxHops: 0 } });
    await started.promise; await f.controller.setFilter({ projectIds: [], families: [], findingStates: ['verified'], relations: [] }); held.resolve(result); await graph;
    await f.controller.setFilter({ projectIds: [], families: [], findingStates: [], relations: [] }); expect(f.controller.getSnapshot().projection?.vertices.map(vertex => vertex.id)).toEqual([f.vertex.id]);
    await f.controller.dispose();
  });
  it('restores query and filter intents without recursively adding history, then truncates forward on a fresh action', async () => {
    const f = fixture(); await f.controller.setShell(f.shell); await f.controller.search('Record'); await f.controller.findings('Finding'); await f.controller.setFilter({ projectIds: [], families: [], findingStates: ['verified'], relations: [] });
    await f.controller.back(); expect(f.controller.getSnapshot().filter.findingStates).toEqual([]); expect(f.controller.getSnapshot().findings?.text).toBe('Finding');
    await f.controller.back(); expect(f.controller.getSnapshot().search?.text).toBe('Record'); expect(f.controller.getSnapshot().findings?.text).toBe('');
    await f.controller.back(); expect(f.controller.getSnapshot().search?.text).toBe(''); expect(f.controller.getSnapshot().history.canBack).toBe(false);
    await f.controller.forward(); expect(f.controller.getSnapshot().search?.text).toBe('Record'); await f.controller.search('fresh'); expect(f.controller.getSnapshot().history.canForward).toBe(false); await f.controller.dispose();
  });
  it('lets a fresh user query supersede an in-flight historical graph reconstruction', async () => {
    const f = fixture(); await f.controller.setShell(f.shell); await f.controller.selectElement(f.edge.id);
    await f.controller.neighbours({ identity: f.vertex.identity, limits: { maxVertices: 2000, maxEdges: 8000, maxVisitedVertices: 10000, maxScannedEdges: 50000, maxHops: 0 } }); await f.controller.select(f.vertex.identity); await f.controller.back();
    const original = f.bridge.neighbours; const started = deferred<void>(); const held = deferred<Awaited<ReturnType<DesktopBridge['neighbours']>>>(); let result!: Awaited<ReturnType<DesktopBridge['neighbours']>>;
    f.bridge.neighbours = async (...args) => { result = await original(...args); started.resolve(); return held.promise; };
    const returning = f.controller.back(); await started.promise; await f.controller.search('fresh'); held.resolve(result); await returning;
    expect(f.controller.getSnapshot().search?.text).toBe('fresh'); expect(f.controller.getSnapshot().projection?.vertices.map(vertex => vertex.id)).toEqual([f.vertex.id]); await f.controller.dispose();
  });
  it('retains a committed fallback token while a newer staged graph fails after an older graph completes', async () => {
    const f = fixture(); await f.controller.setShell(f.shell); const original = f.bridge.filterProjection; let calls = 0;
    const firstStarted = deferred<void>(); const secondStarted = deferred<void>(); const first = deferred<Awaited<ReturnType<DesktopBridge['filterProjection']>>>(); const second = deferred<void>(); let firstResult!: Awaited<ReturnType<DesktopBridge['filterProjection']>>;
    f.bridge.filterProjection = async (...args) => {
      calls++;
      if (calls === 3) { secondStarted.resolve(); await second.promise; throw new Error('Controlled candidate filter rejection.'); }
      const result = await original(...args); if (calls === 1) { firstResult = result; firstStarted.resolve(); return first.promise; } return result;
    };
    const controls = { limits: { maxVertices: 2000, maxEdges: 8000, maxVisitedVertices: 10000, maxScannedEdges: 50000, maxHops: 0 } };
    const graph1 = f.controller.neighbours({ identity: f.vertex.identity, ...controls }); await firstStarted.promise;
    await f.controller.setFilter({ projectIds: [], families: [], findingStates: ['verified'], relations: [] });
    const graph2 = f.controller.neighbours({ identity: f.finding.identity, ...controls }); await secondStarted.promise;
    first.resolve(firstResult); await graph1; second.resolve(); await graph2;
    await f.controller.setFilter({ projectIds: [], families: [], findingStates: [], relations: [] });
    expect(f.controller.getSnapshot().error).toBeNull(); expect(f.controller.getSnapshot().filter.findingStates).toEqual([]); expect(f.controller.getSnapshot().projection?.vertices.map(vertex => vertex.id)).toEqual([f.vertex.id]); await f.controller.dispose();
    // Disposal must release both staged and committed ownership, restoring the full token capacity.
    const pages = Array.from({ length: 8 }, (_, index) => f.service.start({ protocol: PROTOCOL, kind: 'request', binding: { sessionId: 'session', capability: 'capability', generation: '1' }, requestId: `after-dispose-${index}`, operation: 'graph.neighbours', payload: { identity: f.vertex.identity, direction: 'both', relations: ['finding-subject'], causalOnly: false, limits: controls.limits } }));
    pages.forEach((page, index) => f.service.drop({ binding: { sessionId: 'session', capability: 'capability', generation: '1' }, requestId: `after-dispose-${index}`, projectionToken: page.projectionToken, continuationToken: page.continuationToken }));
  });
});
