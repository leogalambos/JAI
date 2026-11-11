// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Palette shape, immutable handoff and active public SDK style contrast, without a GPU claim. */
import { expect, it, vi } from 'vitest';
vi.hoisted(() => { Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }); });
import { MultiDirectedGraph } from 'graphology';
import { evaluateNodeStyle, evaluateEdgeStyle } from 'sigma/types';
import { canvasPalette, DEFAULT_CANVAS_PALETTE } from '../src/renderer/canvas/palette.js';
import { canvasReducers } from '../src/renderer/canvas/styles.js';
import { LIGHT_THEME, DARK_THEME } from '../src/renderer/theme.js';
import { canvasOptions } from '../src/renderer/canvas/sdk.js';
function contrast(left: string, right: string): number {
  const luminance = (color: string) => { const values = [1, 3, 5].map(index => Number.parseInt(color.slice(index, index + 2), 16) / 255).map(value => value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4); return values[0]! * 0.2126 + values[1]! * 0.7152 + values[2]! * 0.0722; };
  const a = luminance(left); const b = luminance(right); return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
}
it('takes an immutable nine-field palette snapshot and rejects invalid unresolved or extra input', () => {
  const input = { ...DEFAULT_CANVAS_PALETTE }; const result = canvasPalette(input); expect(Object.isFrozen(result)).toBe(true); expect(Object.keys(result)).toHaveLength(9);
  input.labelText = '#ffffff'; expect(result.labelText).toBe(DEFAULT_CANVAS_PALETTE.labelText);
  expect(() => canvasPalette({ ...input, sourcePath: '/untrusted' })).toThrow(); expect(() => canvasPalette({ ...input, node: 'var(--node)' })).toThrow();
  expect(() => canvasPalette({ ...input, node: 'url(https://example.invalid)' })).toThrow(); expect(() => canvasPalette({ ...input, edge: '#abc' })).toThrow();
  const { finding: _finding, ...missing } = input; expect(() => canvasPalette(missing)).toThrow(); expect(() => canvasPalette(null)).toThrow();
});
it.each([LIGHT_THEME, DARK_THEME].map(theme => [theme.name, theme.canvas] as const))('applies actual %s SDK reducer colors with qualifying text/nontext contrast and non-colour cues', (_name, colors) => {
  const palette = canvasPalette(colors); const options = canvasOptions(); const graph = new MultiDirectedGraph(); const source = { size: 7, color: '#000000', label: 'Node', x: 0, y: 0, kind: 'version', shape: 'circle' }; graph.addNode('node', source);
  const state = { isHovered: false, isLabelHovered: false, isHidden: false, isHighlighted: false, isDragged: false }; const gs = { isIdle: true, isPanning: false, isZooming: false, isDragging: false, hasHovered: false, hasHighlighted: false };
  let selected: string | null = null; const reducers = canvasReducers(() => selected, () => palette);
  for (const kind of ['version', 'finding', 'unresolved']) {
    const attrs = { ...source, kind, shape: kind === 'finding' ? 'diamond' : kind === 'unresolved' ? 'triangle' : 'circle' };
    const active = evaluateNodeStyle(options.styles?.nodes, attrs, state, gs, graph); Object.assign(active, reducers.nodeReducer!('node', active, attrs, state, gs, graph));
    expect(contrast(active.color, palette.background)).toBeGreaterThanOrEqual(3); expect(active.shape).toBe(attrs.shape);
  }
  selected = 'node'; const active = evaluateNodeStyle(options.styles?.nodes, source, state, gs, graph); Object.assign(active, reducers.nodeReducer!('node', active, source, state, gs, graph)); expect(active.color).toBe(palette.selected); expect(active.size).toBe(9);
  const es = { isHovered: false, isLabelHovered: false, isHidden: false, isHighlighted: false, parallelIndex: 0, parallelCount: 1 };
  const edge = evaluateEdgeStyle(options.styles?.edges, { color: '#000000', size: 1.5, label: 'Relation' }, es, gs, graph); Object.assign(edge, reducers.edgeReducer!('edge', edge, {}, es, gs, graph)); expect(edge.color).toBe(palette.edge); expect(edge.head).toBe('arrow');
  selected = 'edge'; Object.assign(edge, reducers.edgeReducer!('edge', edge, {}, es, gs, graph)); expect(edge.color).toBe(palette.selected); expect(edge.size).toBe(3); expect(edge.head).toBe('arrow');
  expect(contrast(edge.color, palette.background)).toBeGreaterThanOrEqual(3); expect(contrast(active.color, palette.background)).toBeGreaterThanOrEqual(3);
  expect(contrast(palette.labelText, palette.labelBackground)).toBeGreaterThanOrEqual(4.5); expect(contrast(palette.labelBorder, palette.labelBackground)).toBeGreaterThanOrEqual(3); expect(contrast(palette.selected, palette.labelBackground)).toBeGreaterThanOrEqual(3);
});
