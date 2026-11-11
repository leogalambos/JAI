// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Presentation names preserve exact identities while avoiding raw digest primary labels. */
import { expect, it } from 'vitest';
import type { GraphProjection, Vertex } from '@jai/fabric-explorer-contracts';
import golden from '../../packages/contracts/test/fixtures/projection.json' with { type: 'json' };
import { canvasProjection } from '../src/renderer/canvas/model.js';
it('uses a recorded material association and field pointer while preserving the full digest and graph identity', () => {
  const source = structuredClone(golden) as GraphProjection; const owner = { ...source.vertices[0]!, id: 'owner', label: 'Role routing' }; const digest = 'a'.repeat(64);
  const blob: Vertex = { ...source.vertices[0]!, id: 'material', kind: 'blob', identity: { kind: 'blob', projectId: 'project', rootId: 'root', blobId: digest }, label: digest, availability: 'available' };
  const projection = { ...source, vertices: [owner, blob], edges: [{ ...source.edges[0]!, from: owner.id, to: blob.id, relation: 'material-attachment' as const, label: '/materials/0', identity: { ...source.edges[0]!.identity, kind: 'occurrence' as const, pointer: '/materials/0', occurrence: 0 } }] };
  const before = JSON.stringify(projection); const layout = { binding: { sessionId: source.snapshot.sessionId, capability: 'c', generation: source.snapshot.generation, requestId: 'q', projectionId: 'p' }, algorithm: 'layered' as const, positions: [{ handle: 1, x: 0, y: 0 }, { handle: 2, x: 48, y: 0 }], groups: [], work: 0, iterations: 1, complete: true as const };
  const displayed = canvasProjection(projection, layout, [1, 2]);
  expect(displayed.nodes[1]!.label).toContain('Role routing'); expect(displayed.nodes[1]!.label).toContain('/materials/0'); expect(displayed.nodes[1]!.label).not.toBe(digest);
  expect(displayed.nodes[1]!.id).toBe('material'); expect(JSON.stringify(projection)).toBe(before);
});

import { displayNodeLabel, projectionLabelMap } from '../src/renderer/node-label.js';
it('prefers actual authored shallow names, bounds Unicode labels and never guesses a paged title', () => {
  const source = structuredClone(golden) as GraphProjection; const vertex = source.vertices[0]!;
  const named: Vertex = { ...vertex, label: 'b'.repeat(64), attributes: { kind: 'inline', value: { type: 'object', entries: [{ key: 'title', value: { type: 'string', value: 'Résumé review' } }] } } };
  expect(displayNodeLabel(named)).toBe('Résumé review'); expect(displayNodeLabel({ ...named, attributes: { kind: 'paged', source: named.source, byteLength: '10000000', mediaType: 'application/json' } })).not.toBe('Résumé review');
  expect(displayNodeLabel({ ...vertex, label: 'x'.repeat(10000) }).length).toBeLessThanOrEqual(96);
  expect(displayNodeLabel({ ...vertex, label: 'Meaningful identifier' })).toBe('Meaningful identifier');
});
it('resolves material associations deterministically, distinguishes short-digest collisions and limits visible inputs', () => {
  const source = structuredClone(golden) as GraphProjection; const raw = source.vertices[0]!; const prefix = '1'.repeat(10); const suffix = '2'.repeat(8);
  const make = (id: string, middle: string): Vertex => ({ ...raw, id, kind: 'blob', identity: { kind: 'blob', projectId: 'p', rootId: 'r', blobId: prefix + middle.repeat(46) + suffix }, label: prefix + middle.repeat(46) + suffix, availability: 'available' });
  const a = make('a', 'a'); const b = make('b', 'b'); const owner = { ...raw, id: 'owner', label: 'Authored context' }; const other = { ...raw, id: 'other', label: 'Another context' };
  const edges = [owner, other].map((vertex, i) => ({ ...source.edges[0]!, id: `e${i}`, from: vertex.id, to: a.id, relation: 'material-attachment' as const }));
  const projection = { ...source, vertices: [a, b, owner, other], edges }; const first = projectionLabelMap(projection); const reverse = projectionLabelMap({ ...projection, vertices: [...projection.vertices].reverse(), edges: [...edges].reverse() });
  expect([...first].sort()).toEqual([...reverse].sort()); expect(first.get('a')).toContain('(+1 related nodes)');
  expect(projectionLabelMap({ ...projection, vertices: [{ ...a, label: 'Provided material name' }, b, owner, other] }).get('a')).toBe('Provided material name');
  const fallback = projectionLabelMap({ ...projection, edges: [] }); expect(fallback.get('a')).not.toBe(fallback.get('b')); expect(fallback.get('a')).toContain('Material');
  expect(() => projectionLabelMap({ ...projection, vertices: Array.from({ length: 5001 }, () => raw) })).toThrow('limit');
});
