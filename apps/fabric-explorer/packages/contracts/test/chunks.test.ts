import { describe, expect, it } from 'vitest';
import fixture from './fixtures/projection.json' with { type: 'json' };
import { advanceChunks, assertResponseChunk, decodeChunkFrame, encodeChunkFrame, startChunks } from '../src/chunks.js';
import type { Request, ResponseChunk } from '../src/protocol.js';
import { PROTOCOL } from '../src/protocol.js';

const binding = { sessionId: 'synthetic-session', capability: 'opaque-capability', generation: '1' };
const request: Request = { protocol: PROTOCOL, kind: 'request', requestId: 'stream-one', binding, operation: 'graph.neighbours', payload: { identity: fixture.vertices[0]!.identity as never, direction: 'both', relations: ['other-reference'], causalOnly: false, limits: { maxVertices: 5000, maxEdges: 20000, maxVisitedVertices: 10000, maxScannedEdges: 50000, maxHops: 32 } } };
const chunk = (sequence = '0', terminal: unknown = null): ResponseChunk => ({ protocol: PROTOCOL, kind: 'response-chunk', requestId: request.requestId, binding, operation: request.operation, sequence, vertices: fixture.vertices, edges: [], terminal }) as ResponseChunk;
const terminal = () => ({ snapshot: fixture.snapshot, hiddenVertices: '0', hiddenEdges: '0', complete: true, omissions: [] });

describe('finite bounded query streams', () => {
  it('accepts records then terminal metadata without publishing an incomplete graph', () => {
    const first = chunk(); assertResponseChunk(first);
    expect(decodeChunkFrame(encodeChunkFrame(first))).toEqual(first);
    const start = startChunks(request); const next = advanceChunks(start, first, request, binding);
    const last = { ...chunk('1', terminal()), vertices: [], edges: fixture.edges };
    const ended = advanceChunks(next, last, request, binding);
    expect(ended.ended).toBe(true); expect(ended.vertices).toBe(fixture.vertices.length);
    expect(Object.isFrozen(ended)).toBe(true); expect(Object.isFrozen(start.binding)).toBe(true);
    expect(start.nextSequence).toBe('0');
  });

  it('rejects empty nonterminal, duplicate, out-of-order and postterminal delivery', () => {
    expect(() => assertResponseChunk({ ...chunk(), vertices: [], edges: [] })).toThrow();
    const start = startChunks(request);
    expect(() => advanceChunks(start, chunk('1'), request, binding)).toThrow();
    const next = advanceChunks(start, chunk(), request, binding);
    expect(() => advanceChunks(next, chunk(), request, binding)).toThrow();
    const ended = advanceChunks(start, chunk('0', terminal()), request, binding);
    expect(() => advanceChunks(ended, chunk('1', terminal()), request, binding)).toThrow();
  });

  it('rejects changed sessions, generations, request IDs and cumulative limit overflow', () => {
    const start = startChunks(request);
    expect(() => advanceChunks(start, chunk(), request, { ...binding, generation: '2' })).toThrow();
    expect(() => advanceChunks(start, { ...chunk(), requestId: 'other' }, request, binding)).toThrow();
    const tiny = { ...request, payload: { ...request.payload, limits: { ...request.payload.limits, maxVertices: 1 } } };
    expect(() => advanceChunks(startChunks(tiny), chunk(), tiny, binding)).toThrow();
    expect(() => startChunks({ ...request, operation: 'roots.close', payload: {} } as Request)).toThrow();
  });

  it('does not allow incomplete path streams to assert absence', () => {
    const path = { ...chunk('0', { ...terminal(), complete: false, omissions: ['work-limit'], found: false }), operation: 'graph.path' };
    expect(() => assertResponseChunk(path)).toThrow();
    expect(() => assertResponseChunk({ ...path, terminal: { ...path.terminal, found: null } })).not.toThrow();
  });

  it('keeps full in-memory projection limits separate from per-frame byte limits', () => {
    const huge = { ...chunk(), vertices: [{ ...fixture.vertices[0], label: 'x'.repeat(8 * 1024 * 1024) }] };
    expect(() => assertResponseChunk(huge)).not.toThrow();
    expect(() => encodeChunkFrame(huge as ResponseChunk)).toThrow();
  });
});
