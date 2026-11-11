// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Pure bitmap predicate contracts; synthetic bytes test encoding, not GPU rendering success. */
import { expect, it } from 'vitest';
import { LIGHT_THEME, DARK_THEME } from '../src/renderer/theme.js';
import { graphNodePixels } from './visual-pixels.js';
it.each([LIGHT_THEME, DARK_THEME])('matches actual resolved $name node RGB in BGRA order within the clipped CSS region', theme => {
  const bitmap = new Uint8Array(8 * 8 * 4); for (let i = 0; i < bitmap.length; i += 4) { bitmap[i] = 20; bitmap[i + 1] = 30; bitmap[i + 2] = 40; bitmap[i + 3] = 255; }
  const rgb = [1, 3, 5].map(index => parseInt(theme.canvas.node.slice(index, index + 2), 16));
  const set = (x: number, y: number) => { const at = (y * 8 + x) * 4; bitmap.set([rgb[2]!, rgb[1]!, rgb[0]!, 255], at); };
  for (let y = 4; y < 7; y++) for (let x = 4; x < 7; x++) set(x, y); set(0, 0);
  const result = graphNodePixels(bitmap, { width: 8, height: 8 }, { width: 4, height: 4 }, { left: 2, top: 2, right: 4, bottom: 4 }, theme.canvas.node); expect(result.matches).toBe(9); expect(result.sampled).toBe(16); expect(result.region).toEqual({ left: 4, top: 4, right: 8, bottom: 8 });
  for (let i = 0; i < bitmap.length; i += 4) bitmap.set([0, 0, 0, 255], i); set(0, 0); expect(graphNodePixels(bitmap, result.image, { width: 4, height: 4 }, { left: 2, top: 2, right: 4, bottom: 4 }, theme.canvas.node).matches).toBe(0);
});
it('rejects mismatched NativeImage dimensions and invalid colors instead of interpreting another buffer format', () => { expect(() => graphNodePixels(new Uint8Array(3), { width: 1, height: 1 }, { width: 1, height: 1 }, { left: 0, top: 0, right: 1, bottom: 1 }, '#123456')).toThrow(); expect(() => graphNodePixels(new Uint8Array(4), { width: 1, height: 1 }, { width: 1, height: 1 }, { left: 0, top: 0, right: 1, bottom: 1 }, 'blue')).toThrow(); });

it('accepts observed color-managed light node pixels but rejects actual label text/background colors', () => {
  const bitmap = new Uint8Array([144, 94, 41, 255, 67, 43, 22, 255, 255, 255, 255, 255]);
  expect(graphNodePixels(bitmap, { width: 3, height: 1 }, { width: 3, height: 1 }, { left: 0, top: 0, right: 3, bottom: 1 }, LIGHT_THEME.canvas.node).matches).toBe(1);
});
it.each([LIGHT_THEME, DARK_THEME])('does not mistake actual $name label/background/leader colors for node glyphs', theme => {
  const colors = [theme.canvas.labelText, theme.canvas.labelBackground, theme.canvas.selected, theme.canvas.edge]; const bitmap = new Uint8Array(colors.length * 4);
  colors.forEach((color, index) => { const rgb = [1, 3, 5].map(start => parseInt(color.slice(start, start + 2), 16)); bitmap.set([rgb[2]!, rgb[1]!, rgb[0]!, 255], index * 4); });
  expect(graphNodePixels(bitmap, { width: colors.length, height: 1 }, { width: colors.length, height: 1 }, { left: 0, top: 0, right: colors.length, bottom: 1 }, theme.canvas.node).matches).toBe(0);
});
