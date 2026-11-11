// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Synthetic exact-ID projection fixtures for semantic table rendering, not journal admission evidence. */
import { edgeKey, elementKey } from '@jai/fabric-explorer-contracts';
import type { Edge, GraphProjection, Vertex } from '@jai/fabric-explorer-contracts';
import { ImportModel } from '../src/import/model.js';
import { modelInput, versionFact } from './import-fixtures.js';

/**
 * Build a bounded fixture with duplicate labels and distinct canonical vertex/parallel edge keys.
 * @param vertexCount Number of original vertex rows.
 * @param edgeCount Number of parallel or self-loop relation rows; requires at least one vertex.
 * @returns Synthetic immutable-shape projection backed by actual S04 importer output metadata.
 */
export function tableProjection(vertexCount: number, edgeCount = 0): GraphProjection {
  const model = new ImportModel(modelInput()); model.consume({ sequence: '0', facts: [versionFact()], next: null }); const ready = model.finish();
  const original = [...model.records()][0] as Vertex; if (original.kind !== 'version') throw new Error('Version fixture required.');
  const vertices: Vertex[] = Array.from({ length: vertexCount }, (_, index) => {
    const identity = { ...original.identity, ref: { ...original.identity.ref, logical_id: `entity-${index}` } };
    return { ...original, id: elementKey(identity), identity, label: 'Same label' };
  });
  const edges: Edge[] = Array.from({ length: edgeCount }, (_, index) => {
    const from = vertices[0]!; const to = vertices[1] ?? from;
    const identity = { kind: 'occurrence' as const, projectId: 'project', origin: from.identity, pointer: '/references', occurrence: index, from: from.identity, to: to.identity };
    return { id: edgeKey(identity), identity, from: from.id, to: to.id, label: 'Same relation', relation: 'other-reference', basis: 'exact-reference', causal: false, source: from.source, attributes: from.attributes };
  });
  return { format: 'jai.fabric-explorer.projection/1', snapshot: { ...ready.descriptor, counts: { vertices: String(vertexCount), edges: String(edgeCount), findings: '0' } }, vertices, edges, hiddenVertices: '0', hiddenEdges: '0', complete: true, omissions: [] };
}
