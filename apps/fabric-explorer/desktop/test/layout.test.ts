// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Visible-layout reference/property tests; numeric handles retain generation-local source identity. */
import { describe, expect, it } from 'vitest';
import { layoutProjection } from '../src/layout/engine.js';
import { DEFAULT_LAYOUT_OPTIONS, LAYOUT_LIMITS, LayoutError } from '../src/layout/types.js';
import type { LayoutInput } from '../src/layout/types.js';
function input(vertices: number[], endpoints: readonly (readonly [number, number])[] = []): LayoutInput { return { binding: { sessionId: 'session', capability: 'capability', generation: '1', requestId: 'request', projectionId: 'projection' }, graph: { vertices, edges: endpoints.map(([from, to], handle) => ({ handle, from, to })) } }; }
const immediate = { yieldControl: async () => undefined };
describe('visible layouts', () => {
  it('handles empty/singleton/self-loop and preserves exact binding and immutable input', async () => {
    const empty = await layoutProjection(input([])); expect(empty.positions).toEqual([]); expect(empty.groups).toEqual([]); expect(empty.iterations).toBe(0);
    const source = input([7], [[7, 7], [7, 7]]); const before = structuredClone(source); const result = await layoutProjection(source);
    expect(source).toEqual(before); expect(result.binding).toEqual(source.binding); expect(result.groups).toEqual([{ id: 0, members: [7], cyclic: true, internalEdges: 2, incomingEdges: 0, outgoingEdges: 0, derived: true }]); expect(result.positions).toEqual([{ handle: 7, x: 0, y: 0 }]);
    expect(DEFAULT_LAYOUT_OPTIONS.algorithm).toBe('layered'); expect(new LayoutError('cancelled', 'Cancelled.').code).toBe('cancelled');
  });
  it('condenses cycles before ranking, keeps parallel directed edge counts and places dependencies before consumers', async () => {
    const source = input([0, 1, 2, 3, 4], [[0, 1], [1, 0], [1, 2], [1, 2], [2, 3], [4, 4]]); const result = await layoutProjection(source);
    expect(result.groups.map(group => group.members)).toEqual([[0, 1], [2], [3], [4]]);
    expect(result.groups[0]).toMatchObject({ cyclic: true, internalEdges: 2, outgoingEdges: 2 }); expect(result.groups[1]).toMatchObject({ incomingEdges: 2, outgoingEdges: 1 });
    const positions = new Map(result.positions.map(position => [position.handle, position])); expect(positions.get(1)!.x).toBeLessThan(positions.get(2)!.x); expect(positions.get(2)!.x).toBeLessThan(positions.get(3)!.x);
    expect(source.graph.edges.map(edge => [edge.handle, edge.from, edge.to])).toEqual([[0, 0, 1], [1, 1, 0], [2, 1, 2], [3, 1, 2], [4, 2, 3], [5, 4, 4]]);
  });
  it.each(['layered', 'force'] as const)('is input-order/scheduler independent for %s with a fixed seed', async algorithm => {
    const source = { ...input([0, 1, 2, 3, 4, 5], [[0, 1], [1, 2], [2, 0], [2, 3], [0, 3], [4, 5]]), options: { algorithm, seed: 123, iterations: 5 } };
    const first = await layoutProjection(source, immediate); const reordered = { ...source, graph: { vertices: [...source.graph.vertices].reverse(), edges: [...source.graph.edges].reverse() } };
    const second = await layoutProjection(reordered); expect(second).toEqual(first);
    const other = await layoutProjection({ ...source, options: { ...source.options, seed: 124 } }, immediate); expect(other.positions).not.toEqual(first.positions); expect(other.groups).toEqual(first.groups);
    expect(first.positions.every(point => Number.isFinite(point.x) && Number.isFinite(point.y))).toBe(true); expect(first.iterations).toBe(algorithm === 'force' ? 5 : 4);
  });
  it('accepts exact maximum visible cardinalities without recursive stack exhaustion', async () => {
    const vertices = Array.from({ length: LAYOUT_LIMITS.vertices }, (_, index) => index); const pairs = Array.from({ length: LAYOUT_LIMITS.edges }, (_, index) => [index % vertices.length, (index + 1) % vertices.length] as const);
    const result = await layoutProjection(input(vertices, pairs), immediate); expect(result.positions).toHaveLength(5000); expect(result.groups).toHaveLength(1); expect(result.groups[0]?.internalEdges).toBe(20000); expect(result.work).toBeLessThan(DEFAULT_LAYOUT_OPTIONS.maxWork);
  });
  it('rejects count/configuration/handle/endpoint errors and finite work exhaustion without partial output', async () => {
    await expect(layoutProjection(input(Array.from({ length: 5001 }, (_, index) => index)))).rejects.toMatchObject({ code: 'resource-limit' });
    await expect(layoutProjection(input([0], Array.from({ length: 20001 }, () => [0, 0] as const)))).rejects.toMatchObject({ code: 'resource-limit' });
    for (const source of [input([0, 0]), input([-1]), input([0x100000000]), input([0], [[0, 1]]), { ...input([0]), graph: { vertices: [0], edges: [{ handle: 1, from: 0, to: 0 }, { handle: 1, from: 0, to: 0 }] } }]) await expect(layoutProjection(source)).rejects.toMatchObject({ code: 'invalid-message' });
    for (const options of [{ seed: -1 }, { seed: Infinity }, { iterations: 0 }, { iterations: 201 }, { nodeSpacing: NaN }, { layerSpacing: 0 }, { maxWork: 50000001 }]) await expect(layoutProjection({ ...input([0]), options })).rejects.toMatchObject({ code: 'invalid-message' });
    await expect(layoutProjection({ ...input([0, 1], [[0, 1]]), options: { maxWork: 1 } })).rejects.toMatchObject({ code: 'resource-limit' });
  });
  it('rejects executable shape and malformed context without invoking getters', async () => {
    let calls = 0; const source = input([0]); Object.defineProperty(source, 'options', { enumerable: true, get: () => { calls++; return {}; } });
    await expect(layoutProjection(source)).rejects.toMatchObject({ code: 'invalid-message' }); expect(calls).toBe(0);
    await expect(layoutProjection({ ...input([0]), binding: { ...source.binding, generation: '01' } })).rejects.toMatchObject({ code: 'invalid-message' });
    await expect(layoutProjection({ ...input([0]), binding: { ...source.binding, requestId: '\ud800' } })).rejects.toMatchObject({ code: 'invalid-message' });
  });
  it('cancels before work and at deterministic yielded checkpoints for AbortSignal and atomic predicate', async () => {
    const early = new AbortController(); early.abort(); await expect(layoutProjection(input([0]), { signal: early.signal })).rejects.toMatchObject({ code: 'cancelled' });
    const source = input(Array.from({ length: 5000 }, (_, index) => index)); let cancelled = false; let yields = 0;
    await expect(layoutProjection(source, { cancelled: () => cancelled, yieldControl: async () => { yields++; cancelled = true; } })).rejects.toMatchObject({ code: 'cancelled' }); expect(yields).toBe(1);
    const signal = new AbortController(); await expect(layoutProjection(source, { signal: signal.signal, yieldControl: async () => signal.abort() })).rejects.toMatchObject({ code: 'cancelled' });
  });
  it('matches SCC membership against an independent small-graph reachability oracle', async () => {
    let state = 97; const random = () => { state = Math.imul(state, 1664525) + 1013904223 | 0; return state >>> 0; };
    for (let example = 0; example < 24; example++) {
      const vertices = Array.from({ length: 9 }, (_, index) => index); const pairs = Array.from({ length: 22 }, () => [random() % 9, random() % 9] as const); const source = input(vertices, pairs);
      const reachable = (from: number, to: number) => { const seen = new Set([from]); const queue = [from]; for (let head = 0; head < queue.length; head++) for (const [left, right] of pairs) if (left === queue[head] && !seen.has(right)) { seen.add(right); queue.push(right); } return seen.has(to); };
      const result = await layoutProjection(source, immediate); for (const a of vertices) for (const b of vertices) expect(result.groups.find(group => group.members.includes(a))!.members.includes(b)).toBe(reachable(a, b) && reachable(b, a));
    }
  });
});

it('packs disconnected layered components into a useful finite area rather than one long column', async () => {
  const result = await layoutProjection(input(Array.from({ length: 100 }, (_, index) => index)), immediate);
  expect(new Set(result.positions.map(point => point.x)).size).toBeGreaterThan(1); expect(new Set(result.positions.map(point => `${point.x},${point.y}`)).size).toBe(100);
  const width = Math.max(...result.positions.map(point => point.x)) - Math.min(...result.positions.map(point => point.x)); const height = Math.max(...result.positions.map(point => point.y)) - Math.min(...result.positions.map(point => point.y)); expect(Math.max(width, height) / Math.min(width, height)).toBeLessThan(2);
});

it('bounds force iterations/work and notices cancellation inside yielded refinement', async () => {
  const source = { ...input(Array.from({ length: 32 }, (_, index) => index)), options: { algorithm: 'force' as const, iterations: 200, seed: 0 } };
  const result = await layoutProjection({ ...input([0, 1], [[0, 1], [1, 0]]), options: { algorithm: 'force', iterations: 200, seed: 0, nodeSpacing: 8, layerSpacing: 1024 } }, immediate); expect(result.iterations).toBe(200); expect(result.positions.every(point => Number.isFinite(point.x) && Number.isFinite(point.y))).toBe(true);
  await expect(layoutProjection({ ...source, options: { ...source.options, maxWork: 5000 } }, immediate)).rejects.toMatchObject({ code: 'resource-limit' });
  const abort = new AbortController(); let yielded = false;
  await expect(layoutProjection(source, { signal: abort.signal, yieldControl: async () => { yielded = true; abort.abort(); } })).rejects.toMatchObject({ code: 'cancelled' }); expect(yielded).toBe(true);
});

it('keeps the captured request binding when caller context changes across an asynchronous yield', async () => {
  const source = input(Array.from({ length: 5000 }, (_, index) => index)); const original = structuredClone(source.binding); let changed = false;
  const result = await layoutProjection(source, { yieldControl: async () => { if (!changed) { changed = true; Object.assign(source.binding, { requestId: 'later-request', projectionId: 'later-projection' }); } } });
  expect(changed).toBe(true); expect(result.binding).toEqual(original);
});
