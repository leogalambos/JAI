import { describe, expect, it } from 'vitest';
import fixture from './fixtures/projection.json' with { type: 'json' };
import { assertAdapterChunk, assertAdapterInput, assertEdge, assertOverlayTarget, assertProjection, assertSnapshot, assertVertex } from '../src/validation.js';
import { elementKey } from '../src/identity.js';
import { encodeSemantic } from '../src/semantic.js';

const copy = () => structuredClone(fixture);

describe('source-backed projection DTOs', () => {
  it('accepts the synthetic golden including six source families, derived decision, six finding states and parallel/unresolved edges', () => {
    const value = copy(); assertProjection(value);
    expect(value.vertices.filter(vertex => vertex.kind === 'version')).toHaveLength(7);
    expect(new Set(value.vertices.filter(vertex => vertex.kind === 'finding').map(vertex => vertex.state)).size).toBe(6);
    expect(value.edges[0]!.from).toBe(value.edges[1]!.from);
    expect(value.edges[0]!.to).toBe(value.edges[1]!.to);
    expect(value.edges[0]!.id).not.toBe(value.edges[1]!.id);
    expect(value.vertices[0]!.label).toBe(value.vertices[1]!.label);
    expect(value.vertices[0]!.id).not.toBe(value.vertices[1]!.id);
  });

  it('supports a 100 MiB record through paging rather than oversized inline attributes', () => {
    const vertex = copy().vertices[0]!;
    vertex.attributes = { kind: 'paged', source: vertex.source, byteLength: String(100 * 1024 * 1024), mediaType: 'application/json' } as never;
    expect(() => assertVertex(vertex)).not.toThrow();
    (vertex.attributes as unknown as { byteLength: string }).byteLength = String(100 * 1024 * 1024 + 3);
    expect(() => assertVertex(vertex)).toThrow();
  });

  it('rejects identity rewrites, unknown authority claims and wrong source families', () => {
    const vertex = copy().vertices[0]!;
    expect(() => assertVertex({ ...vertex, id: 'same label' })).toThrow();
    expect(() => assertVertex({ ...vertex, authorityGranted: true })).toThrow();
    expect(() => assertVertex({ ...vertex, source: { ...vertex.source, family: 'findings' } })).toThrow();
  });

  it('rejects cyclic semantic models before recursive schema code can overflow', () => {
    const vertex = copy().vertices[0]!;
    const cycle: { type: 'array'; items: unknown[] } = { type: 'array', items: [] };
    cycle.items.push(cycle);
    expect(() => assertVertex({ ...vertex, attributes: { kind: 'inline', value: cycle } })).toThrowError(/Contract|Cyclic|Invalid/);
  });

  it.each(['family', 'relativePath', 'adapterVersion', 'pointer', 'sequence'])('binds paged attributes to the complete source locator: %s', field => {
    const value = copy(); const vertex = value.vertices[0]!;
    const source = { ...vertex.source, [field]: field === 'family' ? 'findings' : field === 'sequence' ? '2' : 'different' };
    vertex.attributes = { kind: 'paged', source, byteLength: '1', mediaType: 'application/json' } as never;
    expect(() => assertProjection(value)).toThrow();
  });

  it('preserves findings float/nonfinite payloads without allowing them in lifecycle records', () => {
    const value = copy();
    const attributes = { kind: 'inline', value: encodeSemantic({ integer: 1n, float: 1.0, negativeZero: -0, nan: Number.NaN }, 'findings') };
    expect(() => assertVertex({ ...value.vertices[8], attributes })).not.toThrow();
    expect(() => assertVertex({ ...value.vertices[0], attributes })).toThrow();
  });

  it('rejects absent endpoints, duplicate IDs and wrong revision provenance', () => {
    const absent = copy(); absent.vertices = absent.vertices.slice(1);
    expect(() => assertProjection(absent)).toThrow();
    const duplicate = copy(); duplicate.vertices.push(duplicate.vertices[0]!);
    expect(() => assertProjection(duplicate)).toThrow();
    const changed = copy(); changed.vertices[0]!.source.revisionId = 'other';
    expect(() => assertProjection(changed)).toThrow();
  });

  it('resolves an exact missing target without changing its future overlay identity', () => {
    const pending = copy().vertices[7]!;
    expect(() => assertVertex(pending)).not.toThrow();
    const resolved = { ...pending, kind: 'version', family: 'source' } as Record<string, unknown>;
    delete resolved.reason;
    expect(() => assertVertex(resolved)).not.toThrow();
    expect(resolved.id).toBe(pending.id);
  });

  it('allows association cycles while refusing causal inference and textual finding-subject promotion', () => {
    const edge = copy().edges[0]!;
    expect(() => assertEdge(edge)).not.toThrow();
    expect(() => assertEdge({ ...edge, causal: true })).toThrow();
    expect(() => assertEdge({ ...edge, relation: 'material-attachment', basis: 'canonical-dependency', causal: true })).toThrow();
    expect(() => assertEdge({ ...edge, relation: 'finding-subject', basis: 'textual-location' })).toThrow();
  });

  it('cannot label a limited projection complete and checks maximum visible counts', () => {
    const value = copy();
    expect(() => assertProjection({ ...value, omissions: ['visible-limit'] })).toThrow();
    expect(() => assertProjection({ ...value, complete: false, omissions: [] })).toThrow();
    expect(() => assertProjection({ ...value, vertices: Array.from({ length: 5001 }, () => value.vertices[0]) })).toThrow();
  });

  it('separates diagnostic facts from verified replay, authority and resource claims', () => {
    const snapshot = copy().snapshot;
    expect(() => assertSnapshot(snapshot)).not.toThrow();
    const diagnostic = structuredClone(snapshot); diagnostic.sources[0]!.verification.mode = 'diagnostic';
    expect(() => assertSnapshot(diagnostic)).toThrow();
    const authority = { ...snapshot, authorityGranted: true };
    expect(() => assertSnapshot(authority)).toThrow();
    const large = structuredClone(snapshot); large.sources[0]!.byteLength = String(1024 ** 3 + 1);
    expect(() => assertSnapshot(large)).toThrow();
    expect(() => assertSnapshot({ ...snapshot, sources: [...snapshot.sources, snapshot.sources[0]] })).toThrow();
  });

  it('rejects ambiguous source IDs across roots/projects in one observed catalog', () => {
    const snapshot = copy().snapshot;
    const first = snapshot.sources[0]!;
    snapshot.sources.push({ ...first, revisionId: 'different-revision', projectId: 'different-project', rootId: 'different-root' });
    expect(() => assertSnapshot(snapshot)).toThrow();
  });

  it.each(['unknown', 'failed'])('cannot expose derived applicability when canonical replay is %s', replay => {
    const snapshot = copy().snapshot;
    snapshot.sources[0]!.verification.replay = replay;
    snapshot.sources[0]!.verification.recordedApplicability = { type: 'boolean', value: true } as never;
    expect(() => assertSnapshot(snapshot)).toThrow();
    snapshot.sources[0]!.verification.recordedApplicability = null;
    expect(() => assertSnapshot(snapshot)).not.toThrow();
    snapshot.sources[0]!.verification.replay = 'verified';
    snapshot.sources[0]!.verification.recordedApplicability = { type: 'boolean', value: true } as never;
    expect(() => assertSnapshot(snapshot)).not.toThrow();
  });

  it('defines stable overlay addresses without accepting note content', () => {
    const value = copy();
    const overlay = { format: 'jai.fabric-explorer.overlay-target/1', target: { kind: 'element', identity: value.vertices[0]!.identity } };
    expect(() => assertOverlayTarget(overlay)).not.toThrow();
    expect(() => assertOverlayTarget({ ...overlay, note: 'must not be persisted here' })).toThrow();
    expect(elementKey(value.vertices[0]!.identity as never)).toBe(value.vertices[0]!.id);
  });

  it('checks canonical adapter binding, bounded records and candidate generations', () => {
    const value = copy(); const binding = { sessionId: 'synthetic-session', capability: 'opaque-capability', generation: null };
    const input = { binding, sources: [{ projectId: 'synthetic-project-A', rootId: 'synthetic-root', sourceId: 'synthetic-fabric', family: 'fabric', relativePath: 'fabric.jsonl', readHandle: 'opaque-read' }], previous: null, checkpointToken: null };
    expect(() => assertAdapterInput(input)).not.toThrow();
    expect(() => assertAdapterInput({ ...input, binding: { ...binding, capability: null } })).toThrow();
    expect(() => assertAdapterChunk({ kind: 'records', binding, vertices: value.vertices, edges: value.edges })).not.toThrow();
    expect(() => assertAdapterChunk({ kind: 'complete', binding, snapshot: value.snapshot, checkpointToken: 'opaque-checkpoint' })).not.toThrow();
    expect(() => assertAdapterChunk({ kind: 'complete', binding: { ...binding, generation: '1' }, snapshot: value.snapshot, checkpointToken: null })).toThrow();
    expect(() => assertAdapterChunk({ kind: 'diagnostics', binding, diagnostics: [], total: '-1' })).toThrow();
  });
});

it('accepts recorded decoded sources without manufacturing chain or replay verification', () => {
  const snapshot = copy().snapshot;
  snapshot.sources[0]!.verification = { ...snapshot.sources[0]!.verification, mode: 'recorded', decoded: 'decoded', chain: 'unknown', replay: 'recorded', publicTrust: 'unknown', material: 'not-observed', recordedApplicability: null };
  expect(() => assertSnapshot(snapshot)).not.toThrow();
  for (const changes of [{ chain: 'verified' }, { replay: 'verified' }, { publicTrust: 'available' }, { decoded: 'unknown' }]) {
    const forged = structuredClone(snapshot); Object.assign(forged.sources[0]!.verification, changes);
    expect(() => assertSnapshot(forged)).toThrow();
  }
});

it('permits at most two physical record terminator bytes in bounded paged attributes', () => {
  const maximum = 100 * 1024 * 1024;
  for (const ending of [0, 1, 2]) {
    const vertex = copy().vertices[0]!;
    vertex.attributes = { kind: 'paged', source: structuredClone(vertex.source), byteLength: String(maximum + ending), mediaType: 'application/json' } as typeof vertex.attributes;
    expect(() => assertVertex(vertex)).not.toThrow();
  }
  const vertex = copy().vertices[0]!;
  vertex.attributes = { kind: 'paged', source: structuredClone(vertex.source), byteLength: String(maximum + 3), mediaType: 'application/json' } as typeof vertex.attributes;
  expect(() => assertVertex(vertex)).toThrow('limit');
});
