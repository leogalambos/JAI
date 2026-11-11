// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Exact finite coordinate codec is separate from source semantic numeric domains. */
import { expect, it } from 'vitest';
import { encodeLayout, decodeLayout } from '../src/explore/layout-wire.js';
import type { LayoutResult } from '../src/layout/types.js';
const result: LayoutResult = { binding: { sessionId: 'session', capability: 'capability', generation: '1', requestId: 'layout', projectionId: 'projection' }, algorithm: 'force', positions: [{ handle: 0, x: -0, y: Math.PI }], groups: [{ id: 0, members: [0], cyclic: false, internalEdges: 0, incomingEdges: 0, outgoingEdges: 0, derived: true }], work: 12, iterations: 1, complete: true };
it('preserves finite fractional coordinate bits and signed zero through strict administrative JSON', () => {
  const wire = encodeLayout(result); expect(wire.positions[0]).toEqual({ handle: 0, x: '8000000000000000', y: '400921fb54442d18' });
  const decoded = decodeLayout(JSON.parse(JSON.stringify(wire))); expect(Object.is(decoded.positions[0]!.x, -0)).toBe(true); expect(decoded.positions[0]!.y).toBe(Math.PI);
});
it('rejects nonfinite coordinates, extra fields, malformed hex and duplicate handles', () => {
  expect(() => encodeLayout({ ...result, positions: [{ handle: 0, x: Infinity, y: 0 }] })).toThrow();
  const wire = encodeLayout(result);
  expect(() => decodeLayout({ ...wire, groups: [] })).toThrow();
  expect(() => decodeLayout({ ...wire, binding: { ...wire.binding, authority: true } } as never)).toThrow();
  expect(() => decodeLayout({ ...wire, groups: [{ ...wire.groups[0]!, members: [99] }] })).toThrow();
  expect(() => decodeLayout({ ...wire, authority: true } as never)).toThrow();
  expect(() => decodeLayout({ ...wire, positions: [{ handle: 0, x: '7ff0000000000000', y: '0000000000000000' }] })).toThrow();
  expect(() => decodeLayout({ ...wire, positions: [{ handle: 0, x: 'bad', y: '0000000000000000' }] })).toThrow();
  expect(() => decodeLayout({ ...wire, positions: [wire.positions[0]!, wire.positions[0]!] })).toThrow();
});
