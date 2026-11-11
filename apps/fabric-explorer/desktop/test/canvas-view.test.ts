// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Owned adapter collaborator checks; no DOM/GPU or third-party implementation is mocked. */
import { describe, expect, it } from 'vitest';
import type { GraphProjection } from '@jai/fabric-explorer-contracts';
import type { LayoutResult } from '../src/layout/types.js';
import type { GraphCanvas } from '../src/renderer/canvas/index.js';
import { DEFAULT_CANVAS_PALETTE } from '../src/renderer/canvas/palette.js';
import type { CanvasPalette } from '../src/renderer/canvas/palette.js';
import { CanvasView } from '../src/renderer/canvas-view.js';
const projection = { snapshot: { sessionId: 'session', generation: '1' }, vertices: [{ id: 'visible' }], edges: [] } as unknown as GraphProjection;
const layout = { binding: { sessionId: 'session', generation: '1' } } as LayoutResult;
function fixture(unavailable = false) {
  const selected: (string | null)[] = []; let disposals = 0; let replacements = 0; let creations = 0; const palettes: CanvasPalette[] = []; const order: string[] = [];
  const adapter: GraphCanvas = { setPalette: palette => { palettes.push(palette); order.push('palette'); }, replace: () => { replacements++; order.push('replace'); }, select: id => { if (unavailable || id !== null && id !== 'visible') throw new Error('Canvas precondition rejected'); selected.push(id); }, fit: () => {}, zoom: () => {}, focus: id => { if (id !== 'visible') throw new Error('Outside projection'); }, dispose: () => { disposals++; } };
  const messages: string[] = [];
  const view = new CanvasView(report => { creations++; if (unavailable) report('Graph unavailable'); return adapter; }, message => messages.push(message));
  return { view, selected, messages, palettes, order, counts: () => ({ disposals, replacements, creations }) };
}
describe('canvas view publication boundary', () => {
  it('applies a cached palette before graph publication and retains it across disposal', () => {
    const f = fixture(); f.view.setPalette(DEFAULT_CANVAS_PALETTE);
    expect(f.counts().creations).toBe(0);
    f.view.sync(projection, layout, [0], null);
    expect(f.order).toEqual(['palette', 'replace']);
    f.view.dispose(); f.view.sync(projection, layout, [0], null);
    expect(f.palettes).toEqual([DEFAULT_CANVAS_PALETTE, DEFAULT_CANVAS_PALETTE]);
  });
  it('forwards a live theme change without rebuilding geometry or owned resources', () => {
    const f = fixture(); f.view.sync(projection, layout, [0], 'visible');
    const next = { ...DEFAULT_CANVAS_PALETTE, background: '#152536' };
    f.view.setPalette(next);
    expect(f.palettes).toEqual([next]);
    expect(f.counts()).toEqual({ creations: 1, replacements: 1, disposals: 0 });
    expect(f.selected).toEqual(['visible']);
  });
  it('releases an adapter that rejects a live palette and retains semantic fallback', () => {
    let disposals = 0; const messages: string[] = [];
    const adapter: GraphCanvas = { setPalette: () => { throw new Error('Display rejected'); }, replace: () => {}, select: () => {}, fit: () => {}, zoom: () => {}, focus: () => {}, dispose: () => { disposals++; } };
    const view = new CanvasView(() => adapter, message => messages.push(message));
    view.sync(projection, layout, [0], null); view.setPalette(DEFAULT_CANVAS_PALETTE);
    expect(disposals).toBe(1); expect(view.action('fit')).toBe(false);
    expect(messages).toEqual(['Graph rendering is unavailable. Use search, findings and the visible elements list.']);
  });
  it('keeps an off-projection inspector selection without throwing or inventing a canvas node', () => {
    const f = fixture(); expect(() => f.view.sync(projection, layout, [0], 'outside')).not.toThrow(); expect(f.selected).toEqual([null]); expect(f.view.action('focus', 'outside')).toBe(false);
  });
  it('retains semantic fallback when initialization reports unavailable', () => {
    const f = fixture(true); expect(() => f.view.sync(projection, layout, [0], null)).not.toThrow(); expect(f.messages).toEqual(['Graph unavailable']); expect(f.view.action('fit')).toBe(false); expect(f.counts().disposals).toBe(1);
  });
  it('does not construct a GPU canvas before a projection is ready and disposes after close', () => {
    const f = fixture(); f.view.sync(null, null, [], null); expect(f.counts().creations).toBe(0);
    f.view.sync(projection, layout, [0], 'visible'); f.view.sync(null, null, [], null); expect(f.counts().disposals).toBe(1); f.view.dispose(); expect(f.counts().disposals).toBe(1);
  });
  it('reuses the current canvas and geometry when only inspector selection changes', () => {
    const f = fixture(); f.view.sync(projection, layout, [0], 'visible'); f.view.sync(projection, layout, [0], null); expect(f.counts()).toEqual({ creations: 1, replacements: 1, disposals: 0 }); expect(f.view.action('focus', 'visible')).toBe(true);
  });
});
