// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Projection mapping keeps canonical use scopes, exact identities and historical/governing facts distinct. */
import { describe, expect, it } from 'vitest';
import type { Edge, Vertex } from '@jai/fabric-explorer-contracts';
import type { CanonicalFact } from '../src/broker/semantic-types.js';
import { ImportModel } from '../src/import/model.js';
import { factChunk, recordedFact, unsigned } from '../src/import/facts.js';
import { importLimits } from '../src/import/types.js';
import { modelInput, ref, revision, versionFact } from './import-fixtures.js';
const complete = (facts: readonly CanonicalFact[]) => ({ sequence: '0', facts, next: null });
describe('canonical fact model', () => {
  it('maps exact large semantic integers and resolves a reference without label rebinding', () => {
    const model = new ImportModel(modelInput()); const fact = versionFact(); const target = { ...ref, logical_id: 'same-label', version_id: 'd'.repeat(64) };
    model.consume(complete([fact, { kind: 'reference', sourceId: 'fabric', origin: fact.origin, originRef: ref, originUseScope: 'selected', fieldPointer: '/inputs/0/refs/0', occurrence: 0, targetRef: target, targetUseScope: 'different', historicalCausal: true, governing: false, dependencyBasis: 'historical' }, { kind: 'governing-dependency', sourceId: 'fabric', origin: fact.origin, originPoint: { ref, use_scope: 'selected' }, prerequisitePoint: { ref: target, use_scope: 'different' }, occurrence: 0, dependencyBasis: 'governing' }]));
    const ready = model.finish(); expect(ready.descriptor.counts).toEqual({ vertices: '3', edges: '2', findings: '0' }); expect(ready.report.unresolvedVertices).toBe('2');
    const records = [...model.records()]; const vertex = records.find(item => 'kind' in item && item.kind === 'version') as Vertex;
    expect(vertex.attributes).toEqual({ kind: 'inline', value: { type: 'integer', value: '9007199254740993' } });
    const edges = records.filter(item => 'relation' in item) as Edge[]; expect(edges.map(item => item.identity.kind === 'occurrence' ? item.identity.pointer : null)).toEqual(['/inputs/0/refs/0', '/@canonical/governing-dependencies']);
    expect(edges[0]?.identity.from).toMatchObject({ kind: 'use', useScope: 'different', ref: target }); expect(edges[0]?.extensions?.['jai.governing']).toEqual({ type: 'boolean', value: false }); expect(edges[1]?.extensions?.['jai.derived']).toEqual({ type: 'boolean', value: true });
    expect(model.span('fabric', fact.origin.pointer, '1')).toEqual({ offset: '0', length: '100' }); expect(model.span('fabric', '/invented', '1')).toBeNull();
  });
  it('replaces exact unresolved placeholders when their matching primary facts arrive', () => {
    const model = new ImportModel(modelInput()); const fact = versionFact();
    model.consume(complete([{ kind: 'reference', sourceId: 'fabric', origin: fact.origin, originRef: ref, originUseScope: null, fieldPointer: '/related/0/refs/0', occurrence: 0, targetRef: ref, targetUseScope: null, historicalCausal: false, governing: false, dependencyBasis: 'association' }, fact]));
    expect(model.finish().report.unresolvedVertices).toBe('0'); expect([...model.records()].filter(item => 'relation' in item)[0]).toMatchObject({ causal: false, relation: 'other-reference' });
  });
  it('maps finding text to unresolved locations and retains reducer uncertainty', () => {
    const input = modelInput(); const model = new ImportModel({ ...input, sources: [revision('findings')] }); const origin = versionFact().origin;
    model.consume(complete([{ kind: 'finding', sourceId: 'findings', origin, findingId: 'F-0001', state: 'accepted', severity: 'high', findingKind: 'defect', rounds: '2', recordedExpiry: '2026-12-01', label: 'Finding', target: 'record', location: 'record', attributes: { kind: 'inline', value: { type: 'float64', bits: '8000000000000000' } }, effectiveMaxRounds: 3, historicalMaxRoundsKnown: false }]));
    expect(model.finish().descriptor.counts).toEqual({ vertices: '2', edges: '2', findings: '1' });
    const vertices = [...model.records()].filter(item => 'kind' in item) as Vertex[]; expect(vertices.find(item => item.kind === 'finding')).toMatchObject({ state: 'accepted', rounds: '2', extensions: { 'jai.historical-max-rounds-known': { type: 'boolean', value: false } } }); expect(vertices.find(item => item.kind === 'unresolved')).toMatchObject({ reason: 'textual-location', identity: { kind: 'location', text: 'record' } });
  });
  it('rejects duplicate primary identities, wrong sequence, invalid spans and missing terminal', () => {
    const model = new ImportModel(modelInput()); expect(() => model.finish()).toThrow(); expect(() => [...model.records()]).toThrow();
    expect(() => model.consume(complete([versionFact()]))).toThrow('unavailable');
    expect(() => new ImportModel(modelInput()).consume(complete([versionFact(), versionFact()]))).toThrow('Duplicate');
    expect(() => new ImportModel(modelInput()).consume({ sequence: '1', facts: [], next: null })).toThrow('order');
    const bad = { ...versionFact(), origin: { ...versionFact().origin, byteLength: '1001' } }; expect(() => new ImportModel(modelInput()).consume(complete([bad]))).toThrow('span');
    expect(() => factChunk({ sequence: '0', facts: [{ ...versionFact(), extra: true }], next: null }, new Map([['fabric', revision()]]), 0n)).toThrow('field');
  });
  it('counts provenance/unresolved elements and encoded bytes against finite hard limits', () => {
    const input = modelInput(); const fact = versionFact();
    const nodes = new ImportModel({ ...input, limits: { ...input.limits, vertices: 1 } });
    expect(() => nodes.consume(complete([fact, { kind: 'reference', sourceId: 'fabric', origin: fact.origin, originRef: ref, originUseScope: null, fieldPointer: '/related/0/refs/0', occurrence: 0, targetRef: { ...ref, version_id: 'e'.repeat(64) }, targetUseScope: null, historicalCausal: false, governing: false, dependencyBasis: 'association' }]))).toThrow('vertex limit');
    expect(() => new ImportModel({ ...input, limits: { ...input.limits, encodedGraphBytes: 10 } }).consume(complete([fact]))).toThrow('byte limit');
    expect(() => importLimits({ ...input.limits, edges: 500001 })).toThrow(); expect(() => unsigned('01')).toThrow(); expect(unsigned('9007199254740993')).toBe(9007199254740993n);
  });
});

it('maps every provenance variant, explicit decision targets and distinct parallel edges', () => {
  const model = new ImportModel(modelInput()); const first = versionFact(); const origin = first.origin;
  const facts: CanonicalFact[] = [first,
    { kind: 'participant', sourceId: 'fabric', origin, originRef: ref, participant: { kind: 'controller', id: 'owner' }, fieldPointer: '/origin' },
    { kind: 'ownership', sourceId: 'fabric', origin, originRef: ref, owner: { layer: 1, work_kind: 'question', question: 'what', work_item: 'fixture' } },
    { kind: 'material', sourceId: 'fabric', origin, originRef: ref, blobId: 'e'.repeat(64), availability: 'missing', fieldPointer: '/material/0' },
    { kind: 'decision-effect', sourceId: 'fabric', origin, decisionRef: ref, effectKind: 'recorded-change', targetPoint: { ref, use_scope: 'selected' }, effect: { type: 'string', value: 'complete recorded effect' }, occurrence: 0 },
    { kind: 'decision-effect', sourceId: 'fabric', origin, decisionRef: ref, effectKind: 'metadata-only', targetPoint: null, effect: { type: 'null' }, occurrence: 1 },
    ...[0, 1].map((occurrence): CanonicalFact => ({ kind: 'reference', sourceId: 'fabric', origin, originRef: ref, originUseScope: null, fieldPointer: '/related/0/refs/0', occurrence, targetRef: ref, targetUseScope: null, historicalCausal: false, governing: false, dependencyBasis: 'association' })),
  ];
  model.consume({ sequence: '0', facts, next: null }); const ready = model.finish(); expect(ready.descriptor.counts).toEqual({ vertices: '5', edges: '6', findings: '0' });
  const records = [...model.records()]; expect(records.find(item => 'kind' in item && item.kind === 'blob')).toMatchObject({ availability: 'missing' });
  const decisions = records.filter(item => 'relation' in item && item.relation === 'decision-effect') as Edge[]; expect(decisions).toHaveLength(1); expect(decisions[0]).toMatchObject({ causal: false, basis: 'recorded-effect', attributes: { kind: 'inline', value: { type: 'string', value: 'complete recorded effect' } } });
  expect(new Set(records.filter(item => 'relation' in item).map(item => item.id)).size).toBe(6);
});

it('rejects unbounded/no-progress streams, unsupported audit, bad metadata and late terminal data', () => {
  const model = new ImportModel(modelInput()); expect(() => model.consume({ sequence: '0', facts: [], next: 'continue' })).toThrow('progress');
  const sealed = new ImportModel(modelInput()); sealed.consume({ sequence: '0', facts: [], next: null }); sealed.finish(); expect(() => sealed.consume({ sequence: '1', facts: [], next: null })).toThrow('terminal'); expect(() => sealed.finish()).toThrow('terminal');
  const source = revision(); const sources = new Map([['fabric', source]]);
  for (const fact of [{ ...versionFact(), kind: 'unknown' }, { ...versionFact(), sourceId: 'foreign' }, { ...versionFact(), origin: { ...versionFact().origin, sequence: '2' } }]) expect(() => factChunk({ sequence: '0', facts: [fact], next: null }, sources, 0n)).toThrow();
  expect(() => new ImportModel({ ...modelInput(), generation: '2' })).toThrow('generation');
  const audit = { ...source, family: 'audit' as const, verification: { ...source.verification, replay: 'unknown' as const } };
  expect(() => factChunk({ sequence: '0', facts: [{ kind: 'audit', sourceId: 'fabric', origin: versionFact().origin, attributes: { kind: 'inline', value: { type: 'null' } } }], next: null }, new Map([['fabric', audit]]), 0n)).toThrow('audit');
});

it('rejects facts from canonically empty sources regardless of source byte length', () => {
  const input = modelInput(); const empty = { ...revision(), sequence: '0', head: '0'.repeat(64) };
  expect(() => new ImportModel({ ...input, sources: [empty] }).consume({ sequence: '0', facts: [{ ...versionFact(), origin: { ...versionFact().origin, sequence: null } }], next: null })).toThrow('empty source');
  const model = new ImportModel({ ...input, sources: [empty] }); model.consume({ sequence: '0', facts: [], next: null }); expect(model.finish().descriptor.counts).toEqual({ vertices: '0', edges: '0', findings: '0' });
});

it('rejects governing membership that contradicts supplied historical causal facts', () => {
  const fact = versionFact(); const contradictory = { kind: 'reference', sourceId: 'fabric', origin: fact.origin, originRef: ref, originUseScope: null, fieldPointer: '/related/0/refs/0', occurrence: 0, targetRef: ref, targetUseScope: null, historicalCausal: false, governing: true, dependencyBasis: 'association' };
  expect(() => factChunk({ sequence: '0', facts: [contradictory], next: null }, new Map([['fabric', revision()]]), 0n)).toThrow('dependency facts');
});

it.each([false, true])('aggregates shared blob observations independently of source order (reverse=%s)', reverse => {
  const first = { ...revision(), sourceId: 'source-a', revisionId: 'revision-a', relativePath: 'a.jsonl' };
  const second = { ...revision(), sourceId: 'source-b', revisionId: 'revision-b', relativePath: 'b.jsonl' };
  const origin = versionFact().origin; const blobId = 'f'.repeat(64);
  const observe = (sourceId: string, availability: 'available' | 'missing' | 'unknown', suffix: string): CanonicalFact => ({ kind: 'material', sourceId, origin, originRef: { ...ref, logical_id: suffix, version_id: suffix === 'a' ? 'a'.repeat(64) : 'b'.repeat(64) }, blobId, availability, fieldPointer: '/material/0' });
  const order = [observe('source-a', 'missing', 'a'), observe('source-b', 'available', 'b')]; if (reverse) order.reverse();
  {
    const model = new ImportModel({ ...modelInput(), sources: [first, second] }); model.consume({ sequence: '0', facts: order, next: null }); model.finish();
    const records = [...model.records()]; const blob = records.find(item => 'kind' in item && item.kind === 'blob'); expect(blob).toMatchObject({ availability: 'available', source: { sourceId: 'source-b' } });
    const edges = records.filter(item => 'relation' in item) as Edge[]; expect(edges).toHaveLength(2);
    expect(edges.find(item => item.source.sourceId === 'source-a')?.extensions?.['jai.material-availability']).toEqual({ type: 'string', value: 'missing' }); expect(edges.find(item => item.source.sourceId === 'source-b')?.extensions?.['jai.material-availability']).toEqual({ type: 'string', value: 'available' });
  }
});

it.each(['unknown', 'available'] as const)('uses stable contributor provenance for equal blob rank and keeps project/root namespaces (%s)', availability => {
  const original = revision(); const a = { ...original, sourceId: 'a', revisionId: 'revision-a' }; const b = { ...original, sourceId: 'b', revisionId: 'revision-b' };
  const c = { ...original, projectId: 'other-project', sourceId: 'c', revisionId: 'revision-c' }; const d = { ...original, rootId: 'other-root', sourceId: 'd', revisionId: 'revision-d' };
  const make = (sourceId: string, state: 'missing' | 'unknown' | 'available'): CanonicalFact => ({ kind: 'material', sourceId, origin: versionFact().origin, originRef: { ...ref, logical_id: sourceId, version_id: sourceId.repeat(64) }, blobId: 'e'.repeat(64), availability: state, fieldPointer: '/material/0' });
  const model = new ImportModel({ ...modelInput(), sources: [a, b, c, d] }); model.consume({ sequence: '0', facts: [make('b', availability), make('a', availability), make('c', 'missing'), make('d', 'missing')], next: null }); model.finish();
  const blobs = [...model.records()].filter(item => 'kind' in item && item.kind === 'blob'); expect(blobs).toHaveLength(3); expect(blobs.find(item => item.identity.projectId === 'project' && item.identity.kind === 'blob' && item.identity.rootId === original.rootId)).toMatchObject({ availability, source: { sourceId: 'a' } });
});

it('aggregates unknown above missing and chooses stable provenance when all observations are missing', () => {
  const a = { ...revision(), sourceId: 'a', revisionId: 'revision-a' }; const b = { ...revision(), sourceId: 'b', revisionId: 'revision-b' };
  const make = (sourceId: string, availability: 'missing' | 'unknown'): CanonicalFact => ({ kind: 'material', sourceId, origin: versionFact().origin, originRef: { ...ref, logical_id: sourceId, version_id: sourceId.repeat(64) }, blobId: 'e'.repeat(64), availability, fieldPointer: '/material/0' });
  for (const observed of ['unknown', 'missing'] as const) {
    const model = new ImportModel({ ...modelInput(), sources: [a, b] }); model.consume({ sequence: '0', facts: [make('b', observed), make('a', 'missing')], next: null }); model.finish();
    expect([...model.records()].find(item => 'kind' in item && item.kind === 'blob')).toMatchObject({ availability: observed, source: { sourceId: observed === 'unknown' ? 'b' : 'a' } });
  }
});


it('admits repeated exact relations under the compact budget without relaxing the fact stream cap', () => {
  const input = modelInput(); const first = versionFact();
  const facts: CanonicalFact[] = [first, ...Array.from({ length: 700 }, (_, occurrence): CanonicalFact => ({ kind: 'reference', sourceId: 'fabric', origin: first.origin, originRef: ref, originUseScope: null, fieldPointer: '/related/0', occurrence, targetRef: ref, targetUseScope: null, historicalCausal: false, governing: false, dependencyBasis: 'association' }))];
  const model = new ImportModel({ ...input, limits: { ...input.limits, encodedGraphBytes: 1024 * 1024 } });
  model.consume({ sequence: '0', facts, next: null });
  expect(model.finish().descriptor.counts).toEqual({ vertices: '1', edges: '700', findings: '0' });
});


it('keeps an accepted graph usable while a separate malformed candidate is poisoned', () => {
  const accepted = new ImportModel(modelInput()); accepted.consume(complete([versionFact()])); accepted.finish();
  const candidate = new ImportModel(modelInput());
  expect(() => candidate.consume(complete([versionFact(), versionFact()]))).toThrow('Duplicate');
  expect(() => candidate.finish()).toThrow(); expect(() => candidate.graph()).toThrow();
  expect(() => [...candidate.records()]).toThrow(); expect(() => candidate.span('fabric', '', null)).toThrow();
  expect(accepted.graph().vertexCount).toBe(1); expect(accepted.graph().vertex(0).label).toBe('Record');
});

it('bounds direct physical source spans with only LF/CRLF allowance beyond the unchanged body limit', () => {
  const maximum = 100 * 1024 * 1024;
  for (const ending of [0, 1, 2]) {
    const input = modelInput(); const revision = { ...input.sources[0]!, byteLength: String(maximum + 3), sequence: null };
    const model = new ImportModel({ ...input, sources: [revision] }); const fact = { ...versionFact(), origin: { ...versionFact().origin, byteLength: String(maximum + ending) } };
    expect(() => model.consumeDirect(fact)).not.toThrow();
  }
  const input = modelInput(); const model = new ImportModel({ ...input, sources: [{ ...input.sources[0]!, byteLength: String(maximum + 3), sequence: null }] });
  expect(() => model.consumeDirect({ ...versionFact(), origin: { ...versionFact().origin, byteLength: String(maximum + 3) } })).toThrow('100 MiB');
});

 it('checks direct typed fact source binding without transport serialization', () => {
  const fact = versionFact(); const sources = new Map([['fabric', revision()]]);
  expect(recordedFact(fact, sources)).toBe(fact);
  expect(recordedFact({ ...fact, origin: { ...fact.origin, byteOffset: '0', byteLength: '0' } }, sources).origin.byteLength).toBe('0');
  expect(() => recordedFact({ ...fact, sourceId: 'foreign' }, sources)).toThrow();
 });
