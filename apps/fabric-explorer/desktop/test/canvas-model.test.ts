// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Compact display staging checks; authoritative source validation remains the upstream contract boundary. */
import { describe, expect, it } from 'vitest';
import type { GraphProjection } from '@jai/fabric-explorer-contracts';
import golden from '../../packages/contracts/test/fixtures/projection.json' with { type: 'json' };
import type { LayoutResult } from '../src/layout/types.js';
import { canvasProjection, CanvasGraph } from '../src/renderer/canvas/model.js';
function fixture() {
  const projection = structuredClone(golden) as GraphProjection;
  const handles = projection.vertices.map((_, i) => i + 42);
  const layout: LayoutResult = { binding: { sessionId: projection.snapshot.sessionId, capability: 'capability', generation: projection.snapshot.generation, requestId: 'layout', projectionId: 'projection' }, algorithm: 'layered', positions: handles.map((handle, i) => ({ handle, x: i * 48, y: i % 3 * 80 })), groups: [], work: 1, iterations: 1, complete: true };
  return { projection, handles, layout };
}
describe('compact canvas projection', () => {
  it('maps numeric handles exactly and retains independent parallel keys without source attributes', () => {
    const f = fixture(); const original = JSON.stringify(f.projection); const view = canvasProjection(f.projection, { ...f.layout, positions: [...f.layout.positions].reverse() }, f.handles);
    expect(view.nodes[0]?.label).toBe(view.nodes[1]?.label); expect(view.nodes[0]?.id).not.toBe(view.nodes[1]?.id);
    expect(view.nodes[1]).toMatchObject({ x: 48, y: 80 }); expect(view.nodes.every(node => !('attributes' in node) && !('source' in node))).toBe(true);
    expect(view.edges.slice(0, 2).map(edge => [edge.from, edge.to])).toEqual(f.projection.edges.slice(0, 2).map(edge => [edge.from, edge.to]));
    expect(view.edges[0]?.id).not.toBe(view.edges[1]?.id); expect(JSON.stringify(f.projection)).toBe(original);
    expect(view.nodes.find(node => node.kind === 'finding')?.shape).toBe('diamond'); expect(view.nodes.find(node => node.kind === 'unresolved')?.shape).toBe('triangle');
  });
  it('accepts empty and exact visible ceilings, rejecting excess before graph mutation', () => {
    const f = fixture(); const empty = { ...f.projection, vertices: [], edges: [] }; expect(canvasProjection(empty, { ...f.layout, positions: [] }, [])).toEqual({ nodes: [], edges: [] });
    const vertices = Array.from({ length: 5000 }, (_, i) => ({ ...f.projection.vertices[0]!, id: `node-${i}` }));
    const edges = Array.from({ length: 20000 }, (_, i) => ({ ...f.projection.edges[0]!, id: `edge-${i}`, from: vertices[0]!.id, to: vertices[i % vertices.length]!.id }));
    const handles = vertices.map((_, i) => i); const layout = { ...f.layout, positions: handles.map(handle => ({ handle, x: handle, y: 0 })) };
    expect(canvasProjection({ ...f.projection, vertices, edges }, layout, handles).edges).toHaveLength(20000);
    expect(() => canvasProjection({ ...f.projection, vertices, edges: [...edges, edges[0]!] }, layout, handles)).toThrow();
  });
  it('rejects stale layout, duplicates, missing positions and dangling endpoints', () => {
    const f = fixture();
    expect(() => canvasProjection(f.projection, { ...f.layout, binding: { ...f.layout.binding, generation: '2' } }, f.handles)).toThrow();
    expect(() => canvasProjection(f.projection, f.layout, f.handles.map(() => 1))).toThrow();
    expect(() => canvasProjection(f.projection, { ...f.layout, positions: f.layout.positions.slice(1) }, f.handles)).toThrow();
    expect(() => canvasProjection(f.projection, { ...f.layout, positions: f.layout.positions.map(position => ({ ...position, x: NaN })) }, f.handles)).toThrow();
    expect(() => canvasProjection({ ...f.projection, edges: [{ ...f.projection.edges[0]!, from: 'missing' }] }, f.layout, f.handles)).toThrow();
    expect(() => canvasProjection({ ...f.projection, edges: [f.projection.edges[0]!, f.projection.edges[0]!] }, f.layout, f.handles)).toThrow();
  });
});

it('retains the actual Graphology multigraph across replacements and clears owned state on disposal', () => {
  const f = fixture(); const model = new CanvasGraph(); const original = model.graph;
  model.replace(f.projection, f.layout, f.handles);
  expect(model.graph).toBe(original); expect(model.graph.type).toBe('directed'); expect(model.graph.multi).toBe(true);
  const first = f.projection.edges[0]!; const second = f.projection.edges[1]!;
  expect(model.graph.hasEdge(first.id)).toBe(true); expect(model.graph.hasEdge(second.id)).toBe(true);
  expect(model.graph.extremities(first.id)).toEqual([first.from, first.to]);
  expect(model.graph.getNodeAttributes(f.projection.vertices[0]!.id)).not.toHaveProperty('attributes');
  const before = model.graph.export();
  expect(() => model.replace(f.projection, { ...f.layout, positions: [] }, f.handles)).toThrow(); expect(model.graph.export()).toEqual(before);
  model.replace({ ...f.projection, edges: [{ ...first, id: 'loop', from: first.from, to: first.from }, { ...second, id: 'reverse', from: first.to, to: first.from }] }, f.layout, f.handles);
  expect(model.graph).toBe(original); expect(model.graph.extremities('loop')).toEqual([first.from, first.from]); expect(model.graph.extremities('reverse')).toEqual([first.to, first.from]);
  model.dispose(); model.dispose(); expect(model.graph.order).toBe(0); expect(model.graph.size).toBe(0); expect(() => model.replace(f.projection, f.layout, f.handles)).toThrow('closed');
});
