// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Real compiled worker, session publication, controller ownership and named preload integration. */
import { describe, expect, it } from 'vitest';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { PROTOCOL, encodeFrame, decodeResponseFrame } from '@jai/fabric-explorer-contracts';
import type { Binding, Vertex } from '@jai/fabric-explorer-contracts';
import { NativeImportWorker } from '../src/import/worker-client.js';
import { ImportSession } from '../src/import/session.js';
import { ShellController } from '../src/shell/controller.js';
import { createBridge, CHANNELS } from '../src/shell/bridge.js';
import { DEFAULT_PREFERENCES } from '../src/shell/preferences.js';
import type { PreferenceStore } from '../src/shell/preferences.js';
import type { QueryContinuation, QueryDrop, LayoutSelection, GroupSelection, ProjectionFilterSelection } from '../src/explore/types.js';
import { QueryTransfer } from '../src/explore/transport.js';
import { DEFAULT_QUERY_LIMITS, DEFAULT_RELATIONS } from '../src/graph/query-index.js';
import type { GraphRequest } from '../src/graph/types.js';
import { lease, modelInput, versionFact, ref } from './import-fixtures.js';
const entry = resolve(dirname(fileURLToPath(import.meta.url)), '../dist/import-worker.cjs');
const filter = { projectIds: [], families: [], findingStates: [], relations: [] };
function fixture() {
  const admitted = { projectId: 'project', rootId: 'root-fabric', sourceId: 'fabric', family: 'fabric' as const, relativePath: 'fabric.jsonl', readHandle: 'read' };
  const controller = new ShellController({ open: async () => ({ capability: 'capability', sources: [admitted] }), close: async () => {}, disposeSession: async () => {} }, { project: async () => '/synthetic', files: async () => ['/synthetic/fabric.jsonl'] }, { load: () => ({ preferences: DEFAULT_PREFERENCES, warning: null }) } as unknown as PreferenceStore,
    input => new ImportSession({ ...input, broker: { capture: async () => lease() }, workerFactory: () => new NativeImportWorker(entry) }));
  const invoke = async (channel: string, value?: unknown): Promise<unknown> => {
    if (channel === CHANNELS.state) return controller.state();
    if (channel === CHANNELS.request) return controller.request(value);
    if (channel === CHANNELS.queryStart) return controller.queryStart(value);
    if (channel === CHANNELS.searchFindings) return controller.searchFindings(value);
    if (channel === CHANNELS.filterProjection) return controller.filterProjection(value as ProjectionFilterSelection);
    if (channel === CHANNELS.queryNext) return controller.queryNext(value as QueryContinuation);
    if (channel === CHANNELS.queryDrop) return controller.queryDrop(value as QueryDrop);
    if (channel === CHANNELS.layout) return controller.layout(value as LayoutSelection);
    if (channel === CHANNELS.groups) return controller.groups(value as GroupSelection);
    throw new Error('Unexpected channel');
  };
  const bridge = createBridge({ invoke });
  const binding = (): Binding => ({ sessionId: controller.sessionId, capability: controller.state().capability, generation: controller.state().snapshot?.generation ?? null });
  const initialize = async () => { await bridge.pickRoots(binding(), 'open', ['fabric']); await bridge.importSnapshot(binding(), 'import', ['fabric']); };
  return { controller, bridge, binding, initialize, invoke };
}
describe('accepted-worker exploration composition', () => {
  it('routes six named queries, numeric layout and groups without exposing a full graph transport', async () => {
    const f = fixture();
    try {
      await f.initialize(); const binding = f.binding(); const identity = { kind: 'version' as const, projectId: 'project', ref };
      const lookup = await f.bridge.lookup(binding, 'lookup', { identity }); expect(lookup.response).toMatchObject({ status: 'ok', payload: { vertex: { identity } } });
      expect((await f.bridge.details(binding, 'details', { identity })).response).toMatchObject({ payload: { attributes: { kind: 'inline', value: { value: '9007199254740993' } } } });
      expect((await f.bridge.counts(binding, 'counts', { filter })).response).toMatchObject({ payload: { vertices: '1' } });
      expect((await f.bridge.search(binding, 'search', { text: 'record', filter, order: 'label', limit: 10, cursor: null })).response).toMatchObject({ payload: { items: [{ identity }] } });
      const selection = { identity, direction: 'both' as const, relations: DEFAULT_RELATIONS, causalOnly: false, limits: DEFAULT_QUERY_LIMITS };
      const graph = await f.bridge.neighbours(binding, 'neighbours', selection); expect(graph.handles).toEqual([0]);
      expect((await f.bridge.searchFindings(binding, 'findings', { text: '', filter, order: 'identity', limit: 10, cursor: null })).response).toMatchObject({ payload: { items: [] } });
      const filtered = await f.bridge.filterProjection(binding, 'filtered', graph.projectionToken!, { ...filter, projectIds: ['elsewhere'] });
      expect(filtered).toMatchObject({ vertexMask: 'AA==', edgeMask: '', handles: [], omissions: ['filter'] });
      await f.bridge.dropQuery({ binding, requestId: 'filtered', continuationToken: null, projectionToken: filtered.projectionToken });
      const coordinates = await f.bridge.layout(binding, 'layout', graph.projectionToken!, { algorithm: 'force', iterations: 2 });
      expect(coordinates.positions).toEqual([{ handle: 0, x: expect.any(Number), y: expect.any(Number) }]);
      const path = await f.bridge.path(binding, 'path', { ...selection, from: identity, to: identity, identity: undefined } as never).catch(() => null);
      expect(path).toBeNull(); // Closed S04 payload rejects an unrelated identity field before dispatch.
      expect((await f.bridge.path(binding, 'path-valid', { from: identity, to: identity, direction: 'both', relations: DEFAULT_RELATIONS, causalOnly: false, limits: DEFAULT_QUERY_LIMITS })).response).toMatchObject({ payload: { found: true } });
      expect(await f.bridge.groups(binding, 'groups', filter, 'kind')).toMatchObject({ groups: [{ value: 'version', vertices: '1' }] });
      await f.bridge.dropQuery({ binding, requestId: 'neighbours', continuationToken: null, projectionToken: graph.projectionToken });
      await expect(f.bridge.layout(binding, 'released', graph.projectionToken!, {})).rejects.toThrow();
    } finally { await f.controller.dispose(); }
  });
  it('cancels accepted-worker work atomically and keeps the sealed model available', async () => {
    const f = fixture();
    try {
      await f.initialize(); const binding = f.binding(); const identity = { kind: 'version' as const, projectId: 'project', ref };
      const view = await f.bridge.neighbours(binding, 'projection', { identity, direction: 'both', relations: DEFAULT_RELATIONS, causalOnly: false, limits: DEFAULT_QUERY_LIMITS });
      const work = f.bridge.layout(binding, 'cancel-layout', view.projectionToken!, { algorithm: 'force', iterations: 200 });
      const rejected = expect(work).rejects.toThrow();
      expect(await f.bridge.cancelRequest(binding, 'cancel', 'cancel-layout')).toMatchObject({ status: 'ok', payload: { acknowledgement: 'accepted' } });
      await rejected;
      expect((await f.bridge.counts(binding, 'after-cancel', { filter })).response).toMatchObject({ payload: { vertices: '1' } });
    } finally { await f.controller.dispose(); }
  });
  it('drops staged preload results after controlled generation replacement and rejects stale tokens', async () => {
    const f = fixture(); let release!: () => void; let entered!: () => void;
    const waiting = new Promise<void>(resolve => { release = resolve; }); const started = new Promise<void>(resolve => { entered = resolve; });
    try {
      await f.initialize(); const binding = f.binding();
      const bridge = createBridge({ invoke: async (channel, value) => { const result = await f.invoke(channel, value); if (channel === CHANNELS.queryStart) { entered(); await waiting; } return result; } });
      const work = bridge.search(binding, 'stale-search', { text: '', filter, order: 'identity', limit: 10, cursor: null }); const rejected = expect(work).rejects.toThrow();
      await started; await f.bridge.refreshSnapshot(binding, 'refresh'); release(); await rejected;
      await expect(f.bridge.counts(binding, 'old-counts', { filter })).rejects.toThrow();
      expect((await f.bridge.counts(f.binding(), 'new-counts', { filter })).response).toMatchObject({ payload: { vertices: '1' } });
    } finally { release?.(); await f.controller.dispose(); }
  });
  it('releases worker-staged projection tokens when cancellation precedes main response dispatch', async () => {
    const worker = new NativeImportWorker(entry); const binding = { sessionId: 'session', capability: 'capability', generation: '1' };
    try {
      await worker.initialize(modelInput()); await worker.consume({ sequence: '0', facts: [versionFact()], next: null }); await worker.finish();
      const request: GraphRequest = { protocol: PROTOCOL, kind: 'request', requestId: 'late', binding, operation: 'graph.neighbours', payload: { identity: { kind: 'version', projectId: 'project', ref }, direction: 'both', relations: DEFAULT_RELATIONS, causalOnly: false, limits: DEFAULT_QUERY_LIMITS } };
      // Interpose only event delivery: the real compiled worker has already staged and posted a successful result.
      const transport = (worker as unknown as { worker: import('node:worker_threads').Worker }).worker;
      for (let i = 0; i < 9; i++) {
        const abort = new AbortController(); transport.prependOnceListener('message', () => abort.abort());
        await expect(worker.queryStart({ ...request, requestId: `cancel-${i}` }, abort.signal)).rejects.toMatchObject({ code: 'cancelled' });
      }
      const page = await worker.queryStart({ ...request, requestId: 'retained-capacity' }); expect(page.projectionToken).toBeTruthy();
      for (let i = 0; i < 9; i++) {
        const abort = new AbortController(); transport.prependOnceListener('message', () => abort.abort());
        await expect(worker.filterProjection({ binding, requestId: `late-filter-${i}`, baseProjectionToken: page.projectionToken!, filter }, abort.signal)).rejects.toMatchObject({ code: 'cancelled' });
      }
      const filtered = await worker.filterProjection({ binding, requestId: 'filter-capacity', baseProjectionToken: page.projectionToken!, filter });
      await worker.queryDrop({ binding, requestId: 'filter-capacity', continuationToken: null, projectionToken: filtered.projectionToken });
      await worker.queryDrop({ binding, requestId: 'retained-capacity', continuationToken: null, projectionToken: page.projectionToken });
    } finally { await worker.terminate(); }
  });
  it('rejects a previously computed groups result delivered after a controlled refresh', async () => {
    const f = fixture(); let release!: () => void; let entered!: () => void;
    const waiting = new Promise<void>(resolve => { release = resolve; }); const started = new Promise<void>(resolve => { entered = resolve; });
    try {
      await f.initialize(); const binding = f.binding();
      const bridge = createBridge({ invoke: async (channel, value) => { const result = await f.invoke(channel, value); if (channel === CHANNELS.groups) { entered(); await waiting; } return result; } });
      const work = bridge.groups(binding, 'old-groups', filter, 'kind'); const rejected = expect(work).rejects.toThrow();
      await started; await f.bridge.refreshSnapshot(binding, 'advance-groups'); release(); await rejected;
    } finally { release?.(); await f.controller.dispose(); }
  });
  it('supports real concurrent native calls and cancellation without terminating the accepted worker', async () => {
    const worker = new NativeImportWorker(entry); const binding = { sessionId: 'session', capability: 'capability', generation: '1' };
    try {
      await worker.initialize(modelInput()); await worker.consume({ sequence: '0', facts: [versionFact()], next: null }); await worker.finish();
      const req: GraphRequest = { protocol: PROTOCOL, kind: 'request', requestId: 'native-counts', binding, operation: 'graph.counts', payload: { filter } };
      const cancel = new AbortController(); const work = worker.queryStart(req, cancel.signal); cancel.abort();
      await expect(work).rejects.toMatchObject({ code: 'cancelled' });
      const alive = { ...req, requestId: 'alive' };
      const [page, span] = await Promise.all([worker.queryStart(alive), worker.span('fabric', versionFact().origin.pointer, '1')]);
      expect(new QueryTransfer(alive, true).accept(page, binding)?.response).toMatchObject({ payload: { vertices: '1' } });
      expect(span).toEqual({ offset: '0', length: '100' });
    } finally { await worker.terminate(); }
  });
});
