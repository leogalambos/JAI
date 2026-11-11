// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Private storage tests use S04 DTO fixtures; canonical helper admission is tested separately. */
import { createHash } from 'node:crypto';
import { describe, expect, it } from 'vitest';
import { assertEdge, assertVertex, edgeKey, elementKey, stableLocator } from '@jai/fabric-explorer-contracts';
import type { Edge, ElementIdentity, SnapshotDescriptor, SourceLocator, Vertex } from '@jai/fabric-explorer-contracts';
import { CompactGraphStore } from '../src/import/compact-store.js';
import { ref, revision } from './import-fixtures.js';
const empty = { kind: 'inline' as const, value: { type: 'null' as const } };
const source = (family: 'fabric' | 'findings' = 'fabric'): SourceLocator => { const r = revision(family); return { projectId: r.projectId, rootId: r.rootId, sourceId: r.sourceId, family, relativePath: r.relativePath, pointer: '/rows/0', sequence: '1', revisionId: r.revisionId, adapterVersion: r.adapterVersion }; };
function node(name: string): Vertex { const identity = { kind: 'version' as const, projectId: 'project', ref: { ...ref, logical_id: name, version_id: createHash('sha256').update(name).digest('hex') } }; return { kind: 'version', identity, id: elementKey(identity), label: name, family: 'product', source: source(), attributes: empty }; }
function descriptor(vertices: Vertex[], edges: Edge[]): SnapshotDescriptor { return { format: 'jai.fabric-explorer.snapshot/1', sessionId: 'session', generation: '1', sources: [revision(), revision('findings')], counts: { vertices: String(vertices.length), edges: String(edges.length), findings: String(vertices.filter(vertex => vertex.kind === 'finding').length) }, authorityGranted: false, freshAssessment: false }; }
function link(from: Vertex, to: Vertex, occurrence = 0, origin: ElementIdentity = from.identity, pointer = '/related/0', explicit = false): Edge { const fields = { projectId: 'project', origin, from: from.identity, to: to.identity }; const identity: Edge['identity'] = explicit ? { kind: 'explicit', ...fields, sourceEdgeId: pointer } : { kind: 'occurrence', ...fields, pointer, occurrence }; return { id: edgeKey(identity), identity, from: from.id, to: to.id, relation: 'other-reference', label: pointer, source: source(), attributes: empty, basis: 'exact-reference', causal: false }; }
function sealed(vertices: Vertex[], edges: Edge[], limit?: number) { return CompactGraphStore.fromRecords(descriptor(vertices, edges), [...edges, ...vertices], limit) as CompactGraphStore; }

describe('compact graph storage', () => {
  it('round-trips every identity family and tagged values without normalization', () => {
    const first = node('A'); const ids: ElementIdentity[] = [first.identity,
      { kind: 'use', projectId: 'project', ref, useScope: 'selected' },
      { kind: 'blob', projectId: 'project', rootId: 'root-fabric', blobId: 'e'.repeat(64) },
      ...(['authority', 'controller'] as const).map(kind => ({ kind: 'participant' as const, projectId: 'project', participant: { kind, id: 'same-label' } })),
      { kind: 'participant', projectId: 'project', participant: { kind: 'assignment', ref } },
      { kind: 'ownership', projectId: 'project', owner: { layer: 1, work_kind: 'question', question: 'what', work_item: 'synthetic' } },
      { kind: 'ownership', projectId: 'project', owner: { layer: 6, work_kind: 'integration', question: null, work_item: 'synthetic' } },
      { kind: 'finding', projectId: 'project', ledgerId: 'findings', findingId: 'F-1' },
      { kind: 'location', projectId: 'project', origin: stableLocator(source()), text: 'Ω e\u0301 é "\\\n😀' },
    ];
    const vertices = ids.map((identity): Vertex => {
      const base = { id: elementKey(identity), identity, label: 'Complete Ω label', source: source(), attributes: empty };
      if (identity.kind === 'version') return { ...base, kind: 'version', family: 'product' } as Vertex;
      if (identity.kind === 'use') return { ...base, kind: 'use' } as Vertex;
      if (identity.kind === 'blob') return { ...base, kind: 'blob', availability: 'unknown' } as Vertex;
      if (identity.kind === 'finding') return { ...base, kind: 'finding', state: 'accepted', severity: 'high', findingKind: 'risk', rounds: '9007199254740993', recordedExpiry: '2040-01-01', source: source('findings') } as Vertex;
      if (identity.kind === 'location') return { ...base, kind: 'unresolved', reason: 'textual-location' } as Vertex;
      return { ...base, kind: identity.kind } as Vertex;
    });
    vertices[0] = { ...vertices[0]!, attributes: { kind: 'inline', value: { type: 'integer', value: '9007199254740993' } }, extensions: {} } as Vertex;
    const finding = vertices.findIndex(vertex => vertex.kind === 'finding');
    vertices[finding] = { ...vertices[finding]!, attributes: { kind: 'inline', value: { type: 'object', entries: [{ key: 'integer', value: { type: 'integer', value: '9007199254740993' } }, { key: 'NaN', value: { type: 'float64', bits: '7ff8000000000001' } }, { key: '-zero', value: { type: 'float64', bits: '8000000000000000' } }] } } } as Vertex;
    vertices.forEach(assertVertex); const store = sealed(vertices, []);
    expect([...store.records()]).toEqual(vertices);
    for (let n = 0; n < store.vertexCount; n++) { assertVertex(store.vertex(n)); expect(store.vertexWireBytes(n)).toBe(Buffer.byteLength(JSON.stringify(store.vertex(n)))); }
  });
  it('preserves paged locators, null sequences, spans and whole-source requests', () => {
    const v = { ...node('paged'), source: { ...source(), sequence: null }, attributes: { kind: 'paged', source: { ...source(), sequence: null }, byteLength: '100', mediaType: 'application/json' } } as Vertex;
    const store = new CompactGraphStore(descriptor([v], [])); store.putVertex(v, true); store.putSpan('fabric', '/rows/0', null, '123', '100'); store.putSpan('fabric', '/rows/0', null, '123', '100'); store.seal();
    expect(store.vertex(0)).toEqual(v); expect(store.vertexAttributes(0)).toEqual(v.attributes); expect(store.vertexAttributesWireBytes(0)).toBe(Buffer.byteLength(JSON.stringify(v.attributes))); expect(store.span('fabric', '/rows/0', null)).toEqual({ offset: '123', length: '100' });
    expect(store.span('fabric', '', null)).toEqual({ offset: '0', length: '1000' }); expect(store.span('unknown', '', null)).toBeNull();
  });
  it('orders exact escaped keys and occurrences lexically with independent third origins', () => {
    const vertices = ['prefix', 'prefix-more', '"', '\\', '\n', '😀'].map(node); const third = node('origin-not-a-vertex');
    const edges = vertices.flatMap((v, n) => [2, 10, Number.MAX_SAFE_INTEGER].map(occurrence => link(v, vertices[(n + 1) % vertices.length]!, occurrence, third.identity, '/field/"\\\n' + n)));
    edges.push(link(vertices[0]!, vertices[0]!, 0, third.identity, 'explicit-source-ID', true)); const store = sealed(vertices, edges);
    expect(store.vertexCount).toBe(vertices.length); expect(Array.from({ length: store.edgeCount }, (_, handle) => store.edge(handle).id)).toEqual(edges.map(edge => edge.id).sort());
    expect([...store.records()].filter(value => 'relation' in value)).toEqual(edges);
    for (let handle = 0; handle < store.edgeCount; handle++) { const edge = store.edge(handle); assertEdge(edge); expect(store.vertexId(store.edgeFrom(handle))).toBe(edge.from); expect(store.vertexId(store.edgeTo(handle))).toBe(edge.to); expect(store.edgeWireBytes(handle)).toBe(Buffer.byteLength(JSON.stringify(edge))); }
  });
  it('emits an exact codec image and admits exactly-at-budget while rejecting one byte under', () => {
    const a = node('A'); const b = node('B'); const edges = Array.from({ length: 1100 }, (_, n) => link(a, b, n)); const original = sealed([a, b], edges);
    const bytes = original.compactBytes(); const image = [...original.encodedChunks()].reduce((sum, value) => sum + value.length, 0);
    expect(image).toBe(bytes); const usage = original.usage(); expect(bytes).toBe(usage.headerBytes + usage.dictionaryBytes + usage.rowBytes + usage.indexBytes);
    expect(sealed([a, b], edges, bytes).compactBytes()).toBe(bytes); expect(() => sealed([a, b], edges, bytes - 1)).toThrow('byte limit');
  });
  it('keeps all DTOs, snapshots and emitted codec buffers detached from storage', () => {
    const a = node('A'); const store = sealed([a], [link(a, a)]); const value = store.vertex(0) as any; value.label = 'changed'; value.identity.ref.logical_id = 'changed'; value.attributes.value.type = 'string';
    const snapshot = store.snapshot as any; snapshot.sources[0].sourceId = 'changed'; for (const bytes of store.encodedChunks()) bytes.fill(0);
    expect(store.vertex(0)).toEqual(a); expect(store.edge(0)).toEqual(link(a, a)); expect(store.span('fabric', '', null)).toEqual({ offset: '0', length: '1000' });
  });
  it('retains ascending parallel/self edge ordinals in both CSR directions', () => {
    const a = node('A'); const b = node('B'); const edges = [link(a, b, 2), link(a, b, 10), link(a, a, 0)]; const store = sealed([a, b], edges);
    for (let vertex = 0; vertex < store.vertexCount; vertex++) {
      const out = Array.from({ length: store.outEnd(vertex) - store.outBegin(vertex) }, (_, n) => store.outEdge(store.outBegin(vertex) + n));
      const input = Array.from({ length: store.inEnd(vertex) - store.inBegin(vertex) }, (_, n) => store.inEdge(store.inBegin(vertex) + n));
      expect(out).toEqual(out.toSorted((x, y) => x - y)); expect(input).toEqual(input.toSorted((x, y) => x - y)); expect(out.every(edge => store.edgeFrom(edge) === vertex)).toBe(true); expect(input.every(edge => store.edgeTo(edge) === vertex)).toBe(true);
    }
  });
  it('rejects missing endpoints, duplicate primaries and conflicting spans by poisoning candidates', () => {
    const a = node('A'); const b = node('B'); expect(() => sealed([a], [link(a, b)])).toThrow('endpoint');
    const store = new CompactGraphStore(descriptor([a], [])); store.putVertex(a, true); expect(() => store.putVertex(a, true)).toThrow('Duplicate'); expect(() => store.seal()).toThrow('unavailable'); expect(() => [...store.records()]).toThrow('unavailable');
    const span = new CompactGraphStore(descriptor([], [])); span.putSpan('fabric', '/row', '1', '0', '10'); expect(() => span.putSpan('fabric', '/row', '1', '0', '11')).toThrow('Conflicting'); expect(() => span.usage()).toThrow();
  });
  it('supports empty stores and exact count fields independent of object key order', () => {
    const emptyStore = sealed([], []); expect(emptyStore.vertexCount).toBe(0); expect(emptyStore.edgeCount).toBe(0); expect([...emptyStore.encodedChunks()].reduce((sum, bytes) => sum + bytes.length, 0)).toBe(emptyStore.compactBytes());
    const a = node('A'); const snapshot = { ...descriptor([a], []), counts: { edges: '0', findings: '0', vertices: '1' } };
    expect(CompactGraphStore.fromRecords(snapshot, [a]).vertexCount).toBe(1);
    expect(() => emptyStore.vertex(-1)).toThrow(); expect(() => emptyStore.edge(0)).toThrow(); expect(() => emptyStore.outEdge(0)).toThrow();
  });
  it('preflights quote scratch and rejects later writes without mutating a sealed store', () => {
    const a = node('x'.repeat(200_000)); expect(() => sealed([a], [], 1024 * 1024)).toThrow('scratch');
    const normal = sealed([node('A')], []); expect(() => normal.putVertex(node('B'))).toThrow('sealed'); expect(() => normal.setFactBytes(0)).toThrow('sealed'); expect(normal.vertexCount).toBe(1);
  });
});

it('decodes exact attributes independently of a large vertex label', () => {
  const value = { ...node('attribute-only'), label: 'x'.repeat(2 * 1024 * 1024) } as Vertex;
  const store = sealed([value], []);
  expect(store.vertexAttributes(0)).toEqual(value.attributes);
  expect(store.vertexAttributesWireBytes(0)).toBe(Buffer.byteLength(JSON.stringify(value.attributes)));
  expect(store.vertexWireBytes(0)).toBeGreaterThan(2 * 1024 * 1024);
});

it('keeps generated writer duplicate/resource poisoning and public invalid-record admission separate', () => {
  const a = node('A'); const b = node('B'); const edge = link(a, b);
  const candidate = CompactGraphStore.candidate(descriptor([a, b], [edge]), 512 * 1024 * 1024);
  candidate.writer.vertex(a, true); candidate.writer.vertex(b, true); candidate.writer.edge(edge);
  expect(() => candidate.writer.edge(edge)).toThrow(); expect(() => candidate.store.seal(descriptor([a, b], [edge]))).toThrow();
  const limited = CompactGraphStore.candidate(descriptor([], []), 2048);
  expect(() => limited.writer.vertex({ ...a, label: 'x'.repeat(4096) }, true)).toThrow(); expect(() => limited.writer.vertex(a, true)).toThrow();
  const external = new CompactGraphStore(descriptor([], []));
  expect(() => external.putVertex({ ...a, id: 'forged' })).toThrow(); expect(() => external.putVertex(a)).toThrow();
});
