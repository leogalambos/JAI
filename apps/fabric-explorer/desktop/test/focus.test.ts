// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Controlled focus ownership tests; actual browser focus and spoken output are qualified separately. */
import { describe, expect, it } from 'vitest';
import { InspectorFocusIntent, shouldRecoverFocus } from '../src/renderer/focus.js';
describe('explicit presentation focus ownership', () => {
  it('consumes an exact successful inspector focus intent once after completion', () => {
    const intent = new InspectorFocusIntent(); const ticket = intent.request('exact-edge', 'generation1');
    expect(intent.consume(ticket, 'exact-edge', 'generation1')).toBe(false); expect(intent.complete(ticket, 'exact-edge', 'generation1')).toBe(true); expect(intent.consume(ticket, 'exact-edge', 'generation1')).toBe(true); expect(intent.consume(ticket, 'exact-edge', 'generation1')).toBe(false);
  });
  it('rejects stale selection, changed binding, superseded tickets and pointer-only selections', () => {
    const intent = new InspectorFocusIntent(); expect(intent.consume(0, 'pointer-only', 'g1')).toBe(false);
    const old = intent.request('old', 'g1'); const latest = intent.request('latest', 'g1'); expect(intent.complete(old, 'old', 'g1')).toBe(false); expect(intent.complete(latest, 'different', 'g1')).toBe(false);
    const changed = intent.request('exact', 'g1'); expect(intent.complete(changed, 'exact', 'g2')).toBe(false);
    const reset = intent.request('exact', 'g1'); intent.reset(); expect(intent.complete(reset, 'exact', 'g1')).toBe(false);
  });
  it('does not focus an inspector changed again between completion and DOM publication', () => {
    const intent = new InspectorFocusIntent(); const ticket = intent.request('exact', 'g1'); expect(intent.complete(ticket, 'exact', 'g1')).toBe(true); expect(intent.consume(ticket, 'another', 'g1')).toBe(false);
  });
  it('recovers lost focus while preserving deliberate focus on a different connected control', () => {
    const original = { isConnected: true }; const body = { isConnected: true }; const other = { isConnected: true };
    expect(shouldRecoverFocus(original, original, body)).toBe(true); expect(shouldRecoverFocus(original, body, body)).toBe(true); expect(shouldRecoverFocus(original, null, body)).toBe(true); expect(shouldRecoverFocus(original, { isConnected: false }, body)).toBe(true); expect(shouldRecoverFocus(original, other, body)).toBe(false);
  });
});
