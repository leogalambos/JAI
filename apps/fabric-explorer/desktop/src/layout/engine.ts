// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Deterministic bounded visible layouts over generation-local numeric handles. */
import { DEFAULT_LAYOUT_OPTIONS, LAYOUT_LIMITS, LayoutError } from './types.js';
import type { LayoutBinding, LayoutControl, LayoutGroup, LayoutInput, LayoutOptions, LayoutResult } from './types.js';
import type { HandleEdge } from '../graph/types.js';

class Work {
  count = 0; private next: number = LAYOUT_LIMITS.yieldWork;
  constructor(private readonly maximum: number, private readonly control: LayoutControl) { this.check(); }
  check(): void { if (this.control.signal?.aborted || this.control.cancelled?.()) throw new LayoutError('cancelled', 'Layout cancelled.'); }
  add(): boolean { if (++this.count > this.maximum) throw new LayoutError('resource-limit', 'Layout work limit exceeded.'); return this.count >= this.next; }
  async yield(): Promise<void> {
    this.check();
    if (this.control.yieldControl) await this.control.yieldControl();
    else await new Promise<void>(resolve => { if (typeof setImmediate === 'function') setImmediate(resolve); else setTimeout(resolve, 0); });
    this.next = this.count + LAYOUT_LIMITS.yieldWork; this.check();
  }
}
function plain(value: unknown, names: readonly string[], optional: readonly string[] = []): asserts value is Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value) || ![Object.prototype, null].includes(Object.getPrototypeOf(value))) throw new LayoutError('invalid-message', 'Invalid layout record.');
  for (const key of Reflect.ownKeys(value)) {
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (typeof key !== 'string' || (!names.includes(key) && !optional.includes(key)) || !descriptor || !('value' in descriptor) || !descriptor.enumerable) throw new LayoutError('invalid-message', 'Unknown or executable layout field.');
  }
  if (names.some(name => !Object.hasOwn(value, name))) throw new LayoutError('invalid-message', 'Missing layout field.');
}
function array(value: unknown, maximum: number): asserts value is unknown[] {
  if (!Array.isArray(value) || value.length > maximum) throw new LayoutError('resource-limit', 'Visible layout count limit exceeded.');
  if (Object.getPrototypeOf(value) !== Array.prototype || Reflect.ownKeys(value).length !== value.length + 1) throw new LayoutError('invalid-message', 'Invalid layout list.');
  for (let index = 0; index < value.length; index++) { const field = Object.getOwnPropertyDescriptor(value, String(index)); if (!field || !('value' in field) || !field.enumerable) throw new LayoutError('invalid-message', 'Executable or sparse layout list.'); }
}
function handle(value: unknown): asserts value is number { if (!Number.isInteger(value) || (value as number) < 0 || (value as number) > 0xffffffff) throw new LayoutError('invalid-message', 'Layout handle is not uint32.'); }
function boundedBytes(value: unknown): void { if (new TextEncoder().encode(JSON.stringify(value)).length > LAYOUT_LIMITS.encodedBytes) throw new LayoutError('resource-limit', 'Compact layout byte limit exceeded.'); }
function options(value: unknown): LayoutOptions {
  if (value === undefined) return DEFAULT_LAYOUT_OPTIONS;
  plain(value, [], ['algorithm', 'seed', 'iterations', 'nodeSpacing', 'layerSpacing', 'maxWork']);
  const selected = { ...DEFAULT_LAYOUT_OPTIONS, ...value } as LayoutOptions;
  if (!['layered', 'force'].includes(selected.algorithm) || !Number.isInteger(selected.seed) || selected.seed < 0 || selected.seed > 0xffffffff || !Number.isInteger(selected.iterations) || selected.iterations < 1 || selected.iterations > LAYOUT_LIMITS.iterations || !Number.isInteger(selected.maxWork) || selected.maxWork < 1 || selected.maxWork > LAYOUT_LIMITS.maxWork || !Number.isFinite(selected.nodeSpacing) || selected.nodeSpacing < 8 || selected.nodeSpacing > 256 || !Number.isFinite(selected.layerSpacing) || selected.layerSpacing < 8 || selected.layerSpacing > 1024) throw new LayoutError('invalid-message', 'Invalid finite layout configuration.');
  return selected;
}
async function sort<T>(values: readonly T[], compare: (left: T, right: T) => number, work: Work): Promise<T[]> {
  let source = [...values]; let target = new Array<T>(source.length);
  for (let width = 1; width < source.length; width *= 2) {
    for (let start = 0; start < source.length; start += width * 2) {
      const middle = Math.min(start + width, source.length); const end = Math.min(start + width * 2, source.length); let left = start; let right = middle;
      for (let destination = start; destination < end; destination++) {
        target[destination] = right >= end || (left < middle && compare(source[left]!, source[right]!) <= 0) ? source[left++]! : source[right++]!;
        if (work.add()) await work.yield();
      }
    }
    [source, target] = [target, source];
  }
  return source;
}
function random(seed: number): () => number {
  let state = seed ^ 0x9e3779b9;
  return () => { state = (state + 0x6d2b79f5) | 0; let value = Math.imul(state ^ state >>> 15, 1 | state); value ^= value + Math.imul(value ^ value >>> 7, 61 | value); return ((value ^ value >>> 14) >>> 0) / 4294967296; };
}
interface Indexed { vertices: number[]; edges: HandleEdge[]; out: number[][]; incoming: number[][]; from: number[]; to: number[] }
async function prepare(input: LayoutInput, work: Work): Promise<Indexed> {
  plain(input, ['binding', 'graph'], ['options']); plain(input.binding, ['sessionId', 'capability', 'generation', 'requestId', 'projectionId']);
  for (const value of Object.values(input.binding)) {
    if (typeof value !== 'string' || !value.length || value.length > 128) throw new LayoutError('invalid-message', 'Invalid layout binding.');
    for (let index = 0; index < value.length; index++) { const unit = value.charCodeAt(index); if (unit >= 0xd800 && unit <= 0xdbff) { const next = value.charCodeAt(++index); if (!(next >= 0xdc00 && next <= 0xdfff)) throw new LayoutError('invalid-message', 'Invalid binding Unicode.'); } else if (unit >= 0xdc00 && unit <= 0xdfff) throw new LayoutError('invalid-message', 'Invalid binding Unicode.'); }
  }
  if (!/^(?:0|[1-9][0-9]*)$/.test(input.binding.generation)) throw new LayoutError('invalid-message', 'Invalid layout generation.');
  plain(input.graph, ['vertices', 'edges']); array(input.graph.vertices, LAYOUT_LIMITS.vertices); array(input.graph.edges, LAYOUT_LIMITS.edges);
  const vertices: number[] = []; const edges: HandleEdge[] = []; const seenVertices = new Set<number>(); const seenEdges = new Set<number>();
  for (const value of input.graph.vertices) { handle(value); if (seenVertices.has(value)) throw new LayoutError('invalid-message', 'Duplicate layout vertex.'); seenVertices.add(value); vertices.push(value); if (work.add()) await work.yield(); }
  for (const value of input.graph.edges) {
    plain(value, ['handle', 'from', 'to']); handle(value.handle); handle(value.from); handle(value.to);
    if (seenEdges.has(value.handle) || !seenVertices.has(value.from) || !seenVertices.has(value.to)) throw new LayoutError('invalid-message', 'Duplicate edge or absent layout endpoint.');
    seenEdges.add(value.handle); edges.push({ handle: value.handle, from: value.from, to: value.to }); if (work.add()) await work.yield();
  }
  boundedBytes(input);
  const orderedVertices = await sort(vertices, (a, b) => a - b, work); const orderedEdges = await sort(edges, (a, b) => a.handle - b.handle, work);
  const ordinal = new Map(orderedVertices.map((value, index) => [value, index])); const out = orderedVertices.map(() => [] as number[]); const incoming = orderedVertices.map(() => [] as number[]); const from: number[] = []; const to: number[] = [];
  for (const edge of orderedEdges) { const a = ordinal.get(edge.from)!; const b = ordinal.get(edge.to)!; out[a]!.push(b); incoming[b]!.push(a); from.push(a); to.push(b); if (work.add()) await work.yield(); }
  return { vertices: orderedVertices, edges: orderedEdges, out, incoming, from, to };
}
async function components(graph: Indexed, work: Work): Promise<{ groups: LayoutGroup[]; component: Int32Array }> {
  const visited = new Uint8Array(graph.vertices.length); const finish: number[] = [];
  for (let start = 0; start < graph.vertices.length; start++) {
    if (visited[start]) continue; visited[start] = 1;
    const stack = [{ vertex: start, next: 0 }];
    while (stack.length) {
      const frame = stack[stack.length - 1]!; const neighbors = graph.out[frame.vertex]!;
      if (frame.next < neighbors.length) { const next = neighbors[frame.next++]!; if (!visited[next]) { visited[next] = 1; stack.push({ vertex: next, next: 0 }); } }
      else { finish.push(frame.vertex); stack.pop(); }
      if (work.add()) await work.yield();
    }
  }
  visited.fill(0); const members: number[][] = [];
  for (let index = finish.length - 1; index >= 0; index--) {
    const start = finish[index]!; if (visited[start]) continue; visited[start] = 1; const stack = [start]; const group: number[] = [];
    while (stack.length) { const vertex = stack.pop()!; group.push(vertex); for (const next of graph.incoming[vertex]!) { if (!visited[next]) { visited[next] = 1; stack.push(next); } if (work.add()) await work.yield(); } if (work.add()) await work.yield(); }
    members.push(await sort(group, (a, b) => a - b, work));
  }
  const ordered = await sort(members, (a, b) => a[0]! - b[0]!, work); const component = new Int32Array(graph.vertices.length);
  const groups = ordered.map((values, id): LayoutGroup => { for (const value of values) component[value] = id; return { id, members: values.map(value => graph.vertices[value]!), cyclic: values.length > 1, internalEdges: 0, incomingEdges: 0, outgoingEdges: 0, derived: true }; });
  const counts = groups.map(() => ({ internal: 0, incoming: 0, outgoing: 0, loop: false }));
  for (let index = 0; index < graph.edges.length; index++) { const from = graph.from[index]!; const to = graph.to[index]!; const a = component[from]!; const b = component[to]!; if (a === b) { counts[a]!.internal++; counts[a]!.loop ||= from === to; } else { counts[a]!.outgoing++; counts[b]!.incoming++; } if (work.add()) await work.yield(); }
  return { groups: groups.map((group, index) => ({ ...group, cyclic: group.cyclic || counts[index]!.loop, internalEdges: counts[index]!.internal, incomingEdges: counts[index]!.incoming, outgoingEdges: counts[index]!.outgoing })), component };
}
async function layered(graph: Indexed, groups: readonly LayoutGroup[], component: Int32Array, config: LayoutOptions, work: Work): Promise<{ x: Float64Array; y: Float64Array }> {
  const forward = groups.map(() => new Set<number>()); const backward = groups.map(() => new Set<number>()); const indegree = new Int32Array(groups.length); const ranks = new Int32Array(groups.length);
  for (let index = 0; index < graph.edges.length; index++) { const from = component[graph.from[index]!]!; const to = component[graph.to[index]!]!; if (from !== to && !forward[from]!.has(to)) { forward[from]!.add(to); backward[to]!.add(from); indegree[to] = indegree[to]! + 1; } if (work.add()) await work.yield(); }
  const queue: number[] = []; for (let index = 0; index < groups.length; index++) if (!indegree[index]) queue.push(index);
  for (let head = 0; head < queue.length; head++) { const from = queue[head]!; for (const to of forward[from]!) { ranks[to] = Math.max(ranks[to]!, ranks[from]! + 1); indegree[to] = indegree[to]! - 1; if (indegree[to] === 0) queue.push(to); if (work.add()) await work.yield(); } }
  if (queue.length !== groups.length) throw new LayoutError('invalid-message', 'Condensation did not produce a DAG.');
  const layers: number[][] = []; for (let index = 0; index < groups.length; index++) (layers[ranks[index]!] ??= []).push(index);
  const seeded = random(config.seed); const tie = groups.map(() => seeded()); const order = new Float64Array(groups.length);
  for (let sweep = 0; sweep < 4; sweep++) {
    for (const layer of layers) layer.forEach((group, index) => { order[group] = index; });
    const indices = Array.from({ length: layers.length }, (_, index) => sweep % 2 === 0 ? index : layers.length - index - 1);
    for (const index of indices) {
      const scores = new Map<number, number>();
      for (const group of layers[index]!) { let total = 0; let count = 0; for (const neighbor of (sweep % 2 === 0 ? backward[group]! : forward[group]!)) { total += order[neighbor]!; count++; if (work.add()) await work.yield(); } scores.set(group, count ? total / count : order[group]!); }
      layers[index] = await sort(layers[index]!, (a, b) => scores.get(a)! - scores.get(b)! || tie[a]! - tie[b]! || a - b, work);
      layers[index]!.forEach((group, at) => { order[group] = at; });
    }
  }
  const radius = groups.map(group => group.members.length > 1 ? config.nodeSpacing / (2 * Math.sin(Math.PI / group.members.length)) : 0);
  const x = new Float64Array(graph.vertices.length); const y = new Float64Array(graph.vertices.length); const ordinal = new Map(graph.vertices.map((value, index) => [value, index]));
  let bandLeft = 0;
  for (const layer of layers) {
    // Pack full SCC footprints, not individual members, so cycles keep their circular geometry.
    const side = (group: number) => 2 * radius[group]! + 2 * config.nodeSpacing;
    const target = Math.max(...layer.map(side), Math.sqrt(layer.reduce((area, group) => area + side(group) ** 2, 0)));
    const tiles: { group: number; x: number; y: number }[] = []; let cursorX = 0; let cursorY = 0; let rowHeight = 0; let width = 0;
    for (const group of layer) {
      const extent = side(group);
      if (cursorX > 0 && cursorX + extent > target) { cursorX = 0; cursorY += rowHeight; rowHeight = 0; }
      tiles.push({ group, x: cursorX + radius[group]!, y: cursorY + radius[group]! });
      cursorX += extent; rowHeight = Math.max(rowHeight, extent); width = Math.max(width, cursorX);
      if (work.add()) await work.yield();
    }
    const height = cursorY + rowHeight;
    for (const tile of tiles) {
      const values = groups[tile.group]!.members; const phase = seeded() * 2 * Math.PI;
      for (let index = 0; index < values.length; index++) {
        const at = ordinal.get(values[index]!)!; const angle = phase + index * 2 * Math.PI / values.length;
        x[at] = bandLeft + tile.x + Math.cos(angle) * radius[tile.group]!;
        y[at] = tile.y - (height - 2 * config.nodeSpacing) / 2 + Math.sin(angle) * radius[tile.group]!;
        if (work.add()) await work.yield();
      }
    }
    bandLeft += width + config.layerSpacing;
  }
  return { x, y };
}
async function packDisconnected(graph: Indexed, positions: { x: Float64Array; y: Float64Array }, spacing: number, work: Work): Promise<void> {
  const seen = new Uint8Array(graph.vertices.length); const parts: { members: number[]; minX: number; minY: number; width: number; height: number }[] = [];
  for (let start = 0; start < graph.vertices.length; start++) {
    if (seen[start]) continue; seen[start] = 1; const stack = [start]; const members: number[] = []; let minX = Infinity; let maxX = -Infinity; let minY = Infinity; let maxY = -Infinity;
    while (stack.length) {
      const vertex = stack.pop()!; members.push(vertex); minX = Math.min(minX, positions.x[vertex]!); maxX = Math.max(maxX, positions.x[vertex]!); minY = Math.min(minY, positions.y[vertex]!); maxY = Math.max(maxY, positions.y[vertex]!);
      for (const neighbors of [graph.out[vertex]!, graph.incoming[vertex]!]) for (const next of neighbors) { if (!seen[next]) { seen[next] = 1; stack.push(next); } if (work.add()) await work.yield(); }
      if (work.add()) await work.yield();
    }
    parts.push({ members, minX, minY, width: maxX - minX + spacing * 2, height: maxY - minY + spacing * 2 });
  }
  if (parts.length < 2) return;
  const target = Math.sqrt(parts.reduce((area, part) => area + part.width * part.height, 0)); let cursorX = 0; let cursorY = 0; let rowHeight = 0;
  for (const part of parts) {
    if (cursorX > 0 && cursorX + part.width > target) { cursorX = 0; cursorY += rowHeight; rowHeight = 0; }
    for (const vertex of part.members) { positions.x[vertex] = positions.x[vertex]! - part.minX + cursorX + spacing; positions.y[vertex] = positions.y[vertex]! - part.minY + cursorY + spacing; if (work.add()) await work.yield(); }
    cursorX += part.width; rowHeight = Math.max(rowHeight, part.height);
  }
}
async function force(graph: Indexed, config: LayoutOptions, work: Work): Promise<{ x: Float64Array; y: Float64Array }> {
  const count = graph.vertices.length; const x = new Float64Array(count); const y = new Float64Array(count); const seeded = random(config.seed); const columns = Math.max(1, Math.ceil(Math.sqrt(count))); const cell = config.nodeSpacing * 2;
  const permutation = graph.vertices.map((_, index) => index);
  for (let index = permutation.length - 1; index > 0; index--) { const other = Math.floor(seeded() * (index + 1)); [permutation[index], permutation[other]] = [permutation[other]!, permutation[index]!]; if (work.add()) await work.yield(); }
  for (let index = 0; index < count; index++) { const at = permutation[index]!; x[at] = (index % columns) * cell + (seeded() - 0.5) * config.nodeSpacing; y[at] = Math.floor(index / columns) * cell + (seeded() - 0.5) * config.nodeSpacing; if (work.add()) await work.yield(); }
  for (let iteration = 0; iteration < config.iterations; iteration++) {
    const buckets = new Map<string, number[]>(); const dx = new Float64Array(count); const dy = new Float64Array(count);
    for (let index = 0; index < count; index++) { const key = `${Math.floor(x[index]! / cell)},${Math.floor(y[index]! / cell)}`; const bucket = buckets.get(key); if (bucket) bucket.push(index); else buckets.set(key, [index]); if (work.add()) await work.yield(); }
    for (let index = 0; index < count; index++) {
      const gridX = Math.floor(x[index]! / cell); const gridY = Math.floor(y[index]! / cell); let sampled = 0;
      for (let a = -1; a <= 1 && sampled < LAYOUT_LIMITS.neighborSamples; a++) for (let b = -1; b <= 1 && sampled < LAYOUT_LIMITS.neighborSamples; b++) {
        for (const other of buckets.get(`${gridX + a},${gridY + b}`) ?? []) { if (other === index) continue; const vx = x[index]! - x[other]!; const vy = y[index]! - y[other]!; const squared = Math.max(1, vx * vx + vy * vy); const weight = config.nodeSpacing * config.nodeSpacing / squared; dx[index] = dx[index]! + vx * weight; dy[index] = dy[index]! + vy * weight; sampled++; if (work.add()) await work.yield(); if (sampled >= LAYOUT_LIMITS.neighborSamples) break; }
        if (work.add()) await work.yield();
      }
    }
    for (let index = 0; index < graph.edges.length; index++) {
      const from = graph.from[index]!; const to = graph.to[index]!;
      if (from !== to) { const vx = x[to]! - x[from]!; const vy = y[to]! - y[from]!; const distance = Math.max(1, Math.hypot(vx, vy)); const weight = 0.025 * (distance - config.nodeSpacing) / distance; dx[from] = dx[from]! + vx * weight; dy[from] = dy[from]! + vy * weight; dx[to] = dx[to]! - vx * weight; dy[to] = dy[to]! - vy * weight; }
      if (work.add()) await work.yield();
    }
    const cooling = config.nodeSpacing * 0.25 * (1 - iteration / config.iterations);
    for (let index = 0; index < count; index++) { const length = Math.max(1, Math.hypot(dx[index]!, dy[index]!)); const scale = Math.min(cooling, length) / length; x[index] = x[index]! + dx[index]! * scale; y[index] = y[index]! + dy[index]! * scale; if (work.add()) await work.yield(); }
  }
  return { x, y };
}
/**
 * Lay out only a bounded visible handle projection in an isolated owning worker.
 * @param input Exact projection/request binding, numeric graph and finite configuration.
 * @param control Optional AbortSignal, atomic cancellation predicate and cooperative scheduler.
 * @returns Complete finite positions/SCC summaries bound to the unchanged input projection.
 * @throws {LayoutError} For malformed input, visible/byte/work limits or cancellation; no partial result is returned.
 */
export async function layoutProjection(input: LayoutInput, control: LayoutControl = {}): Promise<LayoutResult> {
  plain(input, ['binding', 'graph'], ['options']); plain(input.binding, ['sessionId', 'capability', 'generation', 'requestId', 'projectionId']);
  const binding = { ...input.binding };
  const config = options(input.options); const work = new Work(config.maxWork, control); const graph = await prepare(input, work); const { groups, component } = await components(graph, work);
  const positions = config.algorithm === 'force' ? await force(graph, config, work) : await layered(graph, groups, component, config, work);
  if (config.algorithm === 'layered') await packDisconnected(graph, positions, config.nodeSpacing, work);
  const result: LayoutResult = { binding: binding as LayoutBinding, algorithm: config.algorithm, positions: graph.vertices.map((handle, index) => ({ handle, x: positions.x[index]!, y: positions.y[index]! })), groups, work: work.count, iterations: graph.vertices.length ? config.algorithm === 'force' ? config.iterations : 4 : 0, complete: true };
  for (const position of result.positions) if (!Number.isFinite(position.x) || !Number.isFinite(position.y) || Math.abs(position.x) > 1e9 || Math.abs(position.y) > 1e9) throw new LayoutError('resource-limit', 'Layout coordinate bound exceeded.');
  boundedBytes(result); work.check(); return result;
}
