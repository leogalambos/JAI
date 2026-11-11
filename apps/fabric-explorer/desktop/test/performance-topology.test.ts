// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Projection fixtures test witness logic only; canonical admission evidence comes from the corpus oracle. */
import { describe, expect, it } from 'vitest';
import type { Edge, Vertex } from '@jai/fabric-explorer-contracts';
import { edgeKey, elementKey } from '@jai/fabric-explorer-contracts';
import { CompactGraphStore } from '../src/import/compact-store.js';
import { modelInput, ref, revision } from './import-fixtures.js';
import { observedTopology } from './performance-topology.js';
function graph(links: readonly [number, number, boolean][], size = 3) {
  const { projectId, rootId, sourceId, family, relativePath, revisionId, adapterVersion } = revision();
  const source = { projectId, rootId, sourceId, family, relativePath, revisionId, adapterVersion, pointer: '/record', sequence: '1' };
  const vertices: Vertex[] = Array.from({ length: size }, (_, i) => { const identity = { kind: 'version' as const, projectId: source.projectId, ref: { ...ref, logical_id: `vertex-${i}` } }; return { kind: 'version', identity, id: elementKey(identity), label: String(i), family: 'source', source, attributes: { kind: 'inline', value: { type: 'null' } } }; });
  const edges: Edge[] = links.map(([from, to, causal], occurrence) => { const a = vertices[from]!; const b = vertices[to]!; const identity = { kind: 'occurrence' as const, projectId: source.projectId, origin: a.identity, from: a.identity, to: b.identity, pointer: '/related', occurrence }; return { id: edgeKey(identity), identity, from: a.id, to: b.id, source, label: 'Relation', relation: causal ? 'causal-dependency' : 'other-reference', basis: causal ? 'canonical-dependency' : 'exact-reference', causal, attributes: { kind: 'inline', value: { type: 'null' } } }; });
  const input = modelInput();
  return CompactGraphStore.fromRecords({ format: 'jai.fabric-explorer.snapshot/1', sessionId: input.binding.sessionId, generation: '1', sources: input.sources, counts: { vertices: String(size), edges: String(edges.length), findings: '0' }, authorityGranted: false, freshAssessment: false }, [...vertices, ...edges]);
}
describe('source-backed numeric topology witnesses', () => {
  it('distinguishes permitted mixed cycles, pure associations and no cycle', () => {
    const mixed = observedTopology(graph([[0, 1, true], [1, 0, false], [1, 2, true]]));
    expect(mixed.permittedAssociationCycleEstablished).toBe(true); expect(mixed.directedCycle?.classification).toBe('mixed'); expect(mixed.causalOnlyCycle).toBeNull();
    const edges = mixed.directedCycle!.edges; expect(edges[0]!.to).toBe(edges[1]!.from); expect(edges[1]!.to).toBe(edges[0]!.from);
    expect(observedTopology(graph([[0, 1, false], [1, 0, false]])).directedCycle).toMatchObject({ classification: 'noncausal-only', associationEdges: 2 });
    expect(observedTopology(graph([[0, 1, true], [1, 2, false]])).directedCycle).toBeNull();
  });
  it('reports causal cycles and self loops independently without misclassifying them as coverage', () => {
    const causal = observedTopology(graph([[0, 1, true], [1, 0, true]]));
    expect(causal.causalOnlyCycle?.classification).toBe('causal-only'); expect(causal.permittedAssociationCycleEstablished).toBe(false);
    const loop = observedTopology(graph([[0, 0, false]])); expect(loop.selfLoops).toBe(1); expect(loop.directedCycle).toBeNull();
    const large = observedTopology(graph(Array.from({ length: 65 }, (_, i) => [i, (i + 1) % 65, false]), 65));
    expect(large.directedCycle).toMatchObject({ edgeCount: 65, complete: false }); expect(large.permittedAssociationCycleEstablished).toBe(false);
  });
});
