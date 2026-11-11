// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Controlled owned-facade resize transitions; this does not simulate GPU or native layout. */
import { expect, it, vi } from 'vitest';
vi.hoisted(() => { Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }); });
import { createCanvas } from '../src/renderer/canvas/index.js';
import type { CanvasRenderer } from '../src/renderer/canvas/sdk.js';
function setup(initialWidth = 320, initialHeight = 200) {
  let width = initialWidth; let height = initialHeight; let callback: ResizeObserverCallback = () => {}; let disconnected = 0; let resizes = 0; let refreshes = 0; let kills = 0; let fail = false; let bufferVisible = true; let cachedWidth = initialWidth; let cachedHeight = initialHeight;
  const errors: string[] = []; const camera = { x: 0.2, y: 0.3, ratio: 0.4, angle: 0 };
  const owner = { defaultView: { devicePixelRatio: 1 }, createElement: () => new Element() };
  class Element { ownerDocument = owner; style = {}; width = 0; height = 0; children: unknown[] = []; append(...children: unknown[]) { this.children.push(...children); } setAttribute() {} remove() {} getContext() { return null; } getBoundingClientRect() { return { width, height }; } get clientWidth() { return width; } get clientHeight() { return height; } }
  vi.stubGlobal('ResizeObserver', class { constructor(fn: ResizeObserverCallback) { callback = fn; } observe() {} disconnect() { disconnected++; } });
  const renderer: CanvasRenderer = { on() {}, off() {}, refresh() { bufferVisible = true; refreshes++; if (width <= 0 || height <= 0 || fail) throw new Error('Renderer cannot render'); }, resize() { if (cachedWidth !== width || cachedHeight !== height) bufferVisible = false; cachedWidth = width; cachedHeight = height; resizes++; if (width <= 0 || height <= 0 || fail) throw new Error('Renderer cannot resize'); }, dimensions: () => ({ width: cachedWidth, height: cachedHeight }), project: point => point, normalize: point => point, camera: () => camera, move: () => { throw new Error('Resize must not move the camera'); }, nodeData: () => undefined, edgeData: () => undefined, scaleSize: size => size, kill: () => { kills++; } };
  const canvas = createCanvas(new Element() as unknown as HTMLElement, () => {}, message => errors.push(message), () => renderer);
  return { canvas, errors, notify: () => callback([], {} as ResizeObserver), size: (x: number, y: number) => { width = x; height = y; }, fail: () => { fail = true; }, state: () => ({ resizes, refreshes, kills, disconnected, camera, bufferVisible }) };
}
it('defers zero-width and zero-height observer work, then resumes the same camera exactly once', () => {
  const test = setup(); try { test.notify(); const live = test.state(); test.size(0, 200); expect(() => test.notify()).not.toThrow(); test.notify(); test.canvas.select(null); test.size(320, 0); expect(() => test.notify()).not.toThrow(); expect(test.state().resizes).toBe(live.resizes); test.size(320, 200); test.notify(); expect(test.state().resizes).toBe(live.resizes + 1); expect(test.state().refreshes).toBe(live.refreshes + 1); expect(test.state().kills).toBe(0); expect(test.errors).toEqual([]); } finally { test.canvas.dispose(); vi.unstubAllGlobals(); }
});
it('contains an actual positive-size renderer failure and releases the lifetime only once', () => {
  const test = setup(); try { test.fail(); expect(() => test.notify()).not.toThrow(); expect(test.errors).toHaveLength(1); expect(test.state().kills).toBe(1); expect(test.state().disconnected).toBe(1); test.notify(); test.canvas.dispose(); expect(test.state().kills).toBe(1); expect(test.errors).toHaveLength(1); } finally { test.canvas.dispose(); vi.unstubAllGlobals(); }
});
it('ignores queued observer callbacks after disposal', () => { const test = setup(); try { test.canvas.dispose(); test.size(0, 0); expect(() => test.notify()).not.toThrow(); expect(test.state().resizes).toBe(0); expect(test.state().kills).toBe(1); } finally { vi.unstubAllGlobals(); } });

it('does not construct the renderer against a zero-size initial host', () => { const test = setup(0, 200); try { expect(test.errors).toHaveLength(1); expect(test.state().resizes).toBe(0); expect(test.state().kills).toBe(0); } finally { test.canvas.dispose(); vi.unstubAllGlobals(); } });

it('repaints graph bodies after a positive-to-positive backing-buffer invalidation, then coalesces unchanged notifications', () => {
  const test = setup(); try { expect(test.state().bufferVisible).toBe(true); test.size(640, 400); test.notify(); expect(test.state().bufferVisible).toBe(true); expect(test.state().refreshes).toBe(1); test.notify(); expect(test.state().refreshes).toBe(1); expect(test.state().camera).toEqual({ x: 0.2, y: 0.3, ratio: 0.4, angle: 0 }); } finally { test.canvas.dispose(); vi.unstubAllGlobals(); }
});
