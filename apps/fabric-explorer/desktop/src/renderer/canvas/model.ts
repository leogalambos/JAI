// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Compact display projection staging; source attributes and verification never become renderer-owned state. */
import { projectionLabelMap, displayNodeLabel } from '../node-label.js';
import { MultiDirectedGraph } from 'graphology';
import type { GraphProjection } from '@jai/fabric-explorer-contracts';
import type { LayoutResult } from '../../layout/types.js';
/** Minimal node attributes copied to the rendering graph. */
export interface CanvasNode { readonly id: string; readonly label: string; readonly x: number; readonly y: number; readonly kind: string; readonly color: string; readonly size: number; readonly shape: string }
/** Minimal independently addressable directed relation. */
export interface CanvasEdge { readonly id: string; readonly from: string; readonly to: string; readonly label: string; readonly color: string; readonly size: number }
/** Fully staged bounded display records; no full semantic records are cloned. */
export interface CanvasProjection { readonly nodes: readonly CanvasNode[]; readonly edges: readonly CanvasEdge[] }
/**
 * Stage a validated semantic projection and matching numeric layout before mutating the visible graph.
 * @param projection Current immutable bounded consumer projection, already semantically validated upstream.
 * @param layout Finite current-session/generation numeric positions from the accepted worker.
 * @param handles Numeric vertex handles aligned exactly with projection.vertices.
 * @returns Compact display-only nodes/edges preserving exact IDs and source direction.
 * @throws {Error} For stale context, exceeded budgets, duplicate/missing handles or malformed endpoints/positions.
 */
export function canvasProjection(projection: GraphProjection, layout: LayoutResult, handles: readonly number[]): CanvasProjection {
  if (!projection || !layout || projection.vertices.length > 5000 || projection.edges.length > 20000 || handles.length !== projection.vertices.length || layout.positions.length !== handles.length || layout.complete !== true || layout.binding.sessionId !== projection.snapshot.sessionId || layout.binding.generation !== projection.snapshot.generation) throw new Error('Canvas projection context rejected');
  const positions = new Map(layout.positions.map(position => [position.handle, position]));
  if (positions.size !== handles.length || new Set(handles).size !== handles.length || handles.some(handle => !Number.isInteger(handle) || handle < 0 || handle > 0xffffffff)) throw new Error('Canvas handles rejected');
  const labels = projectionLabelMap(projection);
  const ids = new Set<string>();
  const nodes = projection.vertices.map((vertex, index): CanvasNode => {
    const position = positions.get(handles[index]!);
    if (!position || ![position.x, position.y].every(value => Number.isFinite(value) && Math.abs(value) <= 1e9) || ids.has(vertex.id) || typeof vertex.id !== 'string' || !vertex.id || typeof vertex.label !== 'string') throw new Error('Canvas node rejected'); ids.add(vertex.id);
    return { id: vertex.id, label: displayNodeLabel(vertex, labels), x: position.x, y: position.y, kind: vertex.kind, color: vertex.kind === 'finding' ? '#9b2c65' : vertex.kind === 'unresolved' ? '#8a5815' : '#235d91', size: vertex.kind === 'finding' ? 9 : 7, shape: vertex.kind === 'finding' ? 'diamond' : vertex.kind === 'unresolved' ? 'triangle' : 'circle' };
  });
  const edgeIds = new Set<string>();
  const edges = projection.edges.map((edge): CanvasEdge => { if (typeof edge.id !== 'string' || !edge.id || !ids.has(edge.from) || !ids.has(edge.to) || edgeIds.has(edge.id) || ids.has(edge.id) || typeof edge.label !== 'string') throw new Error('Canvas edge rejected'); edgeIds.add(edge.id); return { id: edge.id, from: edge.from, to: edge.to, label: edge.label, color: '#65768a', size: 1.5 }; });
  return { nodes, edges };
}

/** One compact Graphology object retained across every visible replacement; the SDK never receives source attributes. */
export class CanvasGraph {
  /** Trusted SDK graph; callers must retain this exact instance rather than calling setGraph. */
  readonly graph = new MultiDirectedGraph({ allowSelfLoops: true });
  private closed = false;
  /**
   * Validate/stage a bounded projection, then replace contents of the same graph instance.
   * @param projection Current immutable semantic projection.
   * @param layout Matching finite current-generation numeric layout.
   * @param handles Exact positional mapping into projection.vertices.
   * @returns Compact display records after successful public Graphology mutation.
   * @throws {Error} For disposed state or invalid display input; rejected staging leaves the previous graph unchanged.
   */
  replace(projection: GraphProjection, layout: LayoutResult, handles: readonly number[]): CanvasProjection {
    if (this.closed) throw new Error('Canvas graph is closed');
    const staged = canvasProjection(projection, layout, handles);
    this.graph.clear();
    for (const node of staged.nodes) this.graph.addNode(node.id, { label: node.label, x: node.x, y: node.y, kind: node.kind, color: node.color, size: node.size, shape: node.shape });
    for (const edge of staged.edges) this.graph.addDirectedEdgeWithKey(edge.id, edge.from, edge.to, { label: edge.label, color: edge.color, size: edge.size, loopAngle: Math.PI / 2, loopFixedOrientation: 1 });
    return staged;
  }
  /** Revoke this display lifetime and clear compact records idempotently; source records are unaffected. */
  dispose(): void { if (this.closed) return; this.closed = true; this.graph.clear(); }
}
