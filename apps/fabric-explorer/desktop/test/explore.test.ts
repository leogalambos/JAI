// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Worker-local transport tests retain real semantic records and maintained consumer validators. */
import { describe, expect, it, vi } from 'vitest';
import { PROTOCOL, encodeFrame, decodeChunkFrame } from '@jai/fabric-explorer-contracts';
import type { Binding, Vertex } from '@jai/fabric-explorer-contracts';
import { ImportModel } from '../src/import/model.js';
import { CompactGraphStore } from '../src/import/compact-store.js';
import { QueryIndex, DEFAULT_QUERY_LIMITS, DEFAULT_RELATIONS } from '../src/graph/query-index.js';
import type { GraphRequest } from '../src/graph/types.js';
import { ExploreService } from '../src/explore/service.js';
import { QueryTransfer, queryPage, graphGroups, projectionFilterView } from '../src/explore/transport.js';
import { EXPLORE_LIMITS } from '../src/explore/types.js';
import { modelInput, versionFact } from './import-fixtures.js';
const binding: Binding = { sessionId: 'session', capability: 'capability', generation: '1' };
const filter = { projectIds: [], families: [], findingStates: [], relations: [] };
function setup(count = 1, attributeBytes = 0) {
  const model = new ImportModel(modelInput());
  for (let i = 0; i < count; i++) {
    const original = versionFact(); if (original.kind !== 'version') throw new Error('Invalid fixture');
    model.consume({ sequence: String(i), facts: [{ ...original, ref: { ...original.ref, logical_id: `record-${i}` }, origin: { ...original.origin, pointer: `/rows/${i}` }, attributes: { kind: 'inline', value: { type: 'string', value: 'x'.repeat(attributeBytes) } } }], next: i === count - 1 ? null : 'next' });
  }
  const ready = model.finish(); const records = [...model.records()];
  const store = model.graph(); const index = new QueryIndex({ snapshot: ready.descriptor, store }, binding);
  return { service: new ExploreService(index, binding), index, store, records: records as Vertex[], snapshot: ready.descriptor };
}
function request(operation: GraphRequest['operation'], payload: unknown, requestId = 'query'): GraphRequest { return { protocol: PROTOCOL, kind: 'request', operation, binding, requestId, payload } as GraphRequest; }
describe('bounded accepted-worker query transport', () => {
  it('rejects oversized lookup before decoding while allowing small details on a large-label vertex', () => {
    const f = setup(); const vertex = { ...f.records[0]!, label: 'x'.repeat(EXPLORE_LIMITS.frameBytes) };
    const store = CompactGraphStore.fromRecords(f.snapshot, [vertex]); const index = new QueryIndex({ snapshot: f.snapshot, store }, binding);
    const service = new ExploreService(index, binding); const decode = vi.spyOn(store, 'vertex');
    expect(() => service.start(request('element.lookup', { identity: vertex.identity }))).toThrow(/frame limit/);
    expect(decode).not.toHaveBeenCalled();
    const req = request('element.details', { identity: vertex.identity });
    const response = new QueryTransfer(req, true).accept(service.start(req), binding)?.response;
    expect(response).toMatchObject({ status: 'ok', payload: { attributes: vertex.attributes } });
    expect(decode).not.toHaveBeenCalled();
  });
  it('rejects oversized inspector attributes before decoding their payload', () => {
    const f = setup(); const vertex: Vertex = { ...f.records[0]!, attributes: { kind: 'inline', value: { type: 'string', value: 'x'.repeat(EXPLORE_LIMITS.frameBytes) } } };
    const store = CompactGraphStore.fromRecords(f.snapshot, [vertex]); const index = new QueryIndex({ snapshot: f.snapshot, store }, binding);
    const service = new ExploreService(index, binding); const decode = vi.spyOn(store, 'vertexAttributes');
    expect(() => service.start(request('element.details', { identity: vertex.identity }))).toThrow(/frame limit/);
    expect(decode).not.toHaveBeenCalled();
  });
  it('reconstructs only emitted-frame vertices and releases a numeric-only continuation', () => {
    const f = setup(8, 350_000); const decode = vi.spyOn(f.store, 'vertex');
    const req = request('search.page', { text: '', filter, order: 'identity', limit: 20, cursor: null });
    const first = f.service.start(req); const frame = decodeChunkFrame(first.frame);
    expect(first.continuationToken).not.toBeNull(); expect(frame.vertices.length).toBeLessThan(8);
    expect(decode).toHaveBeenCalledTimes(frame.vertices.length);
    f.service.drop({ binding, requestId: req.requestId, continuationToken: first.continuationToken, projectionToken: null });
    expect(() => f.service.next({ binding, requestId: req.requestId, continuationToken: first.continuationToken! })).toThrow();
    expect(decode).toHaveBeenCalledTimes(frame.vertices.length);
  });
  it('chunks large search records without loss and rejects replay or cross-request continuation', () => {
    const f = setup(8, 350_000); const req = request('search.page', { text: '', filter, order: 'identity', limit: 20, cursor: null });
    const first = f.service.start(req); expect(first.continuationToken).not.toBeNull();
    const transfer = new QueryTransfer(req, true); expect(transfer.accept(first, binding)).toBeNull();
    const selection = { binding, requestId: req.requestId, continuationToken: first.continuationToken! };
    expect(() => f.service.next({ ...selection, requestId: 'other' })).toThrow();
    const second = f.service.next(selection); expect(second.continuationToken).toBeNull();
    const result = transfer.accept(second, binding); expect(result?.response).toMatchObject({ operation: 'search.page', status: 'ok', payload: { items: f.records } });
    expect(() => f.service.next(selection)).toThrow(); expect(() => transfer.accept(second, binding)).toThrow();
    for (const page of [first, second]) expect(Buffer.byteLength(page.frame)).toBeLessThanOrEqual(EXPLORE_LIMITS.frameBytes);
  });
  it('keeps generation-local numeric projection handles and revokes only owned tokens', async () => {
    const f = setup(); const req = request('graph.neighbours', { identity: f.records[0]!.identity, direction: 'both', relations: DEFAULT_RELATIONS, causalOnly: false, limits: DEFAULT_QUERY_LIMITS });
    const page = f.service.start(req); const view = new QueryTransfer(req, true).accept(page, binding);
    expect(view?.handles).toEqual([0]); expect(view?.projectionToken).toBeTruthy();
    const layout = await f.service.layout({ binding, requestId: 'layout', projectionToken: page.projectionToken!, options: {} });
    expect(layout.positions.map(p => p.handle)).toEqual([0]); expect(layout.binding).toMatchObject({ generation: '1', projectionId: page.projectionToken });
    expect(() => f.service.drop({ binding, requestId: 'other', continuationToken: null, projectionToken: page.projectionToken })).toThrow();
    f.service.drop({ binding, requestId: req.requestId, continuationToken: null, projectionToken: page.projectionToken });
    await expect(f.service.layout({ binding, requestId: 'later', projectionToken: page.projectionToken!, options: {} })).rejects.toThrow();
    expect(() => f.service.start({ ...req, binding: { ...binding, generation: '0' } })).toThrow();
  });
  it('rejects cancelled work and unsendable individual records explicitly without truncating attributes', () => {
    const f = setup(); const req = request('graph.counts', { filter });
    expect(() => f.service.start(req, { cancelled: () => true })).toThrow();
    expect(new QueryTransfer(req, true).accept(f.service.start(req), binding)?.response).toMatchObject({ payload: { vertices: '1' } });
    const vertex = { ...f.records[0]!, attributes: { kind: 'inline', value: { type: 'string', value: 'x'.repeat(EXPLORE_LIMITS.frameBytes) } } } as Vertex;
    const service = new ExploreService(new QueryIndex({ snapshot: f.snapshot, records: [vertex] }, binding), binding);
    expect(() => service.start(request('element.lookup', { identity: vertex.identity }))).toThrow(/frame limit/);
    expect(vertex.attributes).toMatchObject({ kind: 'inline', value: { value: 'x'.repeat(EXPLORE_LIMITS.frameBytes) } });
  });
  it('rejects tampered frames, tokens, sequence, handles and stale publication', () => {
    const f = setup(); const req = request('search.page', { text: '', filter, order: 'identity', limit: 20, cursor: null }); const page = f.service.start(req);
    const chunk = decodeChunkFrame(page.frame);
    expect(() => new QueryTransfer(req, true).accept({ ...page, authority: true }, binding)).toThrow();
    expect(() => new QueryTransfer(req, true).accept(page, { ...binding, generation: '2' })).toThrow();
    expect(() => new QueryTransfer(req, true).accept({ ...page, continuationToken: 'extra' }, binding)).toThrow();
    expect(() => new QueryTransfer(req, true).accept({ ...page, frame: JSON.stringify({ ...chunk, sequence: '1' }) }, binding)).toThrow();
    expect(() => new QueryTransfer(req, true).accept({ ...page, projectionToken: 'token', handles: [] }, binding)).toThrow();
    expect(() => new QueryTransfer(req, true).accept({ ...page, frame: ' '.repeat(EXPLORE_LIMITS.frameBytes + 1) }, binding)).toThrow();
  });
  it('bounds retained jobs and projections and supports explicit release', () => {
    const f = setup(8, 350_000); const req = request('search.page', { text: '', filter, order: 'identity', limit: 20, cursor: null });
    const pages = Array.from({ length: 8 }, (_, i) => f.service.start({ ...req, requestId: `q-${i}` }));
    expect(() => f.service.start({ ...req, requestId: 'overflow' })).toThrow(/limit/);
    f.service.drop({ binding, requestId: 'q-0', continuationToken: pages[0]!.continuationToken, projectionToken: null });
    expect(f.service.start({ ...req, requestId: 'new' }).continuationToken).toBeTruthy(); f.service.dispose();
  });
});

it('validates exact logical frame boundary and rejects oversized or extra private fields', () => {
  const f = setup(); const page = f.service.start(request('graph.counts', { filter }));
  const exact = { ...page, frame: page.frame.padEnd(EXPLORE_LIMITS.frameBytes, ' ') };
  expect(queryPage(exact).frame.length).toBe(EXPLORE_LIMITS.frameBytes);
  expect(() => queryPage({ ...exact, frame: exact.frame + ' ' })).toThrow();
  expect(() => queryPage({ ...page, nativePath: '/synthetic' })).toThrow();
});
it('validates bounded group counts and rejects malformed or cross-axis metadata', () => {
  const empty = { by: 'kind' as const, groups: [], ungroupedVertices: '0', ungroupedEdges: '0', crossGroupEdges: '0' };
  expect(graphGroups(empty, 'kind')).toEqual(empty);
  const full = { ...empty, groups: [{ id: 'group', by: 'kind' as const, value: 'version', vertices: '100000', edges: '500000', findings: '0' }] };
  expect(graphGroups(full, 'kind').groups).toHaveLength(1);
  expect(() => graphGroups(full, 'project')).toThrow();
  expect(() => graphGroups({ ...full, groups: [{ ...full.groups[0]!, vertices: '100001' }] }, 'kind')).toThrow();
  expect(() => graphGroups({ ...empty, authority: true }, 'kind')).toThrow();
});

it('routes findings-only results through normal S04 chunks and rejects a different operation', () => {
  const f = setup(); const req = request('search.page', { text: '', filter, order: 'identity', limit: 20, cursor: null });
  expect(new QueryTransfer(req, true).accept(f.service.start(req, undefined, 'findings'), binding)?.response).toMatchObject({ operation: 'search.page', payload: { items: [] } });
  expect(() => f.service.start(request('graph.counts', { filter }), undefined, 'findings')).toThrow();
});
it('filters original numeric projection masks and enforces independent output ownership and capacity', async () => {
  const f = setup(); const req = request('graph.neighbours', { identity: f.records[0]!.identity, direction: 'both', relations: DEFAULT_RELATIONS, causalOnly: false, limits: DEFAULT_QUERY_LIMITS });
  const base = f.service.start(req);
  const selection = { binding, requestId: 'filtered', baseProjectionToken: base.projectionToken!, filter: { ...filter, projectIds: ['elsewhere'] } };
  const view = f.service.filterProjection(selection);
  expect(projectionFilterView(view, selection)).toMatchObject({ vertexMask: 'AA==', edgeMask: '', handles: [], hiddenVertices: '1', complete: true, omissions: ['filter'] });
  expect(() => f.service.drop({ binding, requestId: req.requestId, continuationToken: null, projectionToken: view.projectionToken })).toThrow();
  expect((await f.service.layout({ binding, requestId: 'empty-layout', projectionToken: view.projectionToken, options: {} })).positions).toEqual([]);
  f.service.drop({ binding, requestId: selection.requestId, continuationToken: null, projectionToken: view.projectionToken });
  expect((await f.service.layout({ binding, requestId: 'base-layout', projectionToken: base.projectionToken!, options: {} })).positions).toHaveLength(1);
  for (let i = 0; i < 7; i++) f.service.filterProjection({ ...selection, requestId: `capacity-${i}` });
  expect(() => f.service.filterProjection({ ...selection, requestId: 'overflow' })).toThrow(/limit/);
  expect(() => f.service.filterProjection({ ...selection, binding: { ...binding, generation: '2' } })).toThrow();
});
it('rejects closed filtered metadata with changed correlation, counts, masks or private fields', () => {
  const f = setup(); const base = f.service.start(request('graph.neighbours', { identity: f.records[0]!.identity, direction: 'both', relations: DEFAULT_RELATIONS, causalOnly: false, limits: DEFAULT_QUERY_LIMITS }));
  const selection = { binding, requestId: 'filter', baseProjectionToken: base.projectionToken!, filter };
  const view = f.service.filterProjection(selection);
  for (const changed of [{ authority: true }, { requestId: 'different' }, { baseProjectionToken: 'different' }, { binding: { ...binding, generation: '2' } }, { vertexMask: '!' }, { vertexMask: 'AB==' }, { vertexMask: 'AA==' }, { hiddenVertices: '-1' }, { handles: [0, 0] }, { omissions: ['work-limit'] }]) expect(() => projectionFilterView({ ...view, ...changed }, selection)).toThrow();
  expect(() => f.service.filterProjection(selection, { cancelled: () => true })).toThrow();
});
