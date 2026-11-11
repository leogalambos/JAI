// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Numeric topology evidence over the admitted model; this helper does not authenticate input journals. */
import type { SealedGraphStore } from '../src/import/compact-store.js';

/** A bounded source-backed cycle witness, with incomplete long witnesses explicitly distinguished. */
export interface CycleWitness {
  readonly edgeCount: number;
  readonly complete: boolean;
  readonly classification: 'causal-only' | 'noncausal-only' | 'mixed';
  readonly associationEdges: number;
  readonly edges: readonly { readonly id: string; readonly from: string; readonly to: string; readonly relation: string; readonly basis: string; readonly causal: boolean; readonly source: ReturnType<SealedGraphStore['edge']>['source'] }[];
}

/**
 * Find a directed closed walk with at least two vertices, separately checking causal-only cycles.
 * @param graph Actual sealed store; the caller separately establishes canonical admission.
 * @returns A source-backed witness or explicit absence, plus independent causal-cycle and loop observations.
 * @remarks Numeric DFS uses O(V) scratch; each witness reconstructs at most 64 complete edge metadata records.
 */
export function observedTopology(graph: SealedGraphStore) {
  const find = (causalOnly: boolean): number[] | null => {
    const color = new Uint8Array(graph.vertexCount); const predecessor = new Int32Array(graph.vertexCount).fill(-1); const predecessorEdge = new Int32Array(graph.vertexCount).fill(-1);
    for (let start = 0; start < graph.vertexCount; start++) {
      if (color[start]) continue;
      const vertices = [start]; const positions = [graph.outBegin(start)]; color[start] = 1;
      while (vertices.length) {
        const position = vertices.length - 1; const vertex = vertices[position]!;
        if (positions[position]! >= graph.outEnd(vertex)) { color[vertex] = 2; vertices.pop(); positions.pop(); continue; }
        const edge = graph.outEdge(positions[position]!++); if (causalOnly && !graph.edgeCausal(edge)) continue;
        const to = graph.edgeTo(edge); if (!causalOnly && to === vertex) continue;
        if (!color[to]) { predecessor[to] = vertex; predecessorEdge[to] = edge; color[to] = 1; vertices.push(to); positions.push(graph.outBegin(to)); }
        else if (color[to] === 1) {
          const cycle = [edge]; for (let from = vertex; from !== to; from = predecessor[from]!) cycle.push(predecessorEdge[from]!);
          return cycle.reverse();
        }
      }
    }
    return null;
  };
  const witness = (handles: readonly number[] | null): CycleWitness | null => {
    if (!handles) return null;
    const causal = handles.filter(handle => graph.edgeCausal(handle)).length;
    const edges = handles.slice(0, 64).map(handle => { const edge = graph.edge(handle); return { id: edge.id, from: edge.from, to: edge.to, relation: edge.relation, basis: edge.basis, causal: edge.causal, source: edge.source }; });
    return { edgeCount: handles.length, complete: handles.length <= 64, classification: causal === handles.length ? 'causal-only' : causal === 0 ? 'noncausal-only' : 'mixed',
      associationEdges: edges.filter(edge => !edge.causal && (edge.basis === 'exact-reference' || edge.basis === 'textual-location')).length, edges };
  };
  let selfLoops = 0; for (let edge = 0; edge < graph.edgeCount; edge++) if (graph.edgeFrom(edge) === graph.edgeTo(edge)) selfLoops++;
  const cycle = witness(find(false)); const causalCycle = witness(find(true));
  return { selfLoops, directedCycle: cycle, causalOnlyCycle: causalCycle,
    permittedAssociationCycleEstablished: !!cycle?.complete && cycle.associationEdges > 0 && causalCycle === null,
    scope: 'Observed graph directions and source locators; no inferred causal classification or source authority.' };
}
