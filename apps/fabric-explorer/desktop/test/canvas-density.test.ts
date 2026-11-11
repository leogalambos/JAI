// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Dense-rank and actual SDK screen-size regressions; no GPU qualification is implied. */
import { expect, it, vi } from 'vitest';
vi.hoisted(() => { Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }); });
import Sigma from 'sigma';
import { resolveSettings } from 'sigma/settings';
import { matrixFromCamera, multiplyVec2 } from 'sigma/utils';
import { canvasOptions } from '../src/renderer/canvas/sdk.js';
import { layoutProjection } from '../src/layout/engine.js';
it('packs a connected 298-leaf rank into a compact separated band without changing handles', async () => {
  const vertices = Array.from({ length: 299 }, (_, i) => i); const edges = vertices.slice(1).map(handle => ({ handle, from: 0, to: handle }));
  const result = await layoutProjection({ binding: { sessionId: 's', capability: 'c', generation: '1', requestId: 'q', projectionId: 'p' }, graph: { vertices, edges } });
  const leaves = result.positions.slice(1); const width = Math.max(...leaves.map(p => p.x)) - Math.min(...leaves.map(p => p.x)); const height = Math.max(...leaves.map(p => p.y)) - Math.min(...leaves.map(p => p.y));
  expect(width).toBeGreaterThan(0); expect(Math.max(width, height) / Math.min(width, height)).toBeLessThan(2);
  expect(leaves.every(p => p.x > result.positions[0]!.x)).toBe(true);
  for (let i = 0; i < leaves.length; i++) for (let j = i + 1; j < leaves.length; j++) expect(Math.hypot(leaves[i]!.x - leaves[j]!.x, leaves[i]!.y - leaves[j]!.y)).toBeGreaterThanOrEqual(47.999);
});
it('keeps actual SDK glyphs bounded while camera magnification separates a maximum-size SCC', () => {
  const settings = resolveSettings(canvasOptions().settings ?? {}); const count = 5000; const spacing = 48; const span = spacing / Math.sin(Math.PI / count); const radius = settings.minCameraRatio!;
  const viewport = { width: 400, height: 300 }; const camera = { x: 0.5, y: 0.5, angle: 0, ratio: radius }; const matrix = matrixFromCamera(camera, viewport, { width: span, height: span }, 48);
  const screen = (x: number) => { const clip = multiplyVec2(matrix, { x, y: 0.5 }); return (1 + clip.x) * viewport.width / 2; };
  const receiver = { camera, graphToViewportRatio: 1, internals: { settings }, getSetting: (key: keyof typeof settings) => settings[key] };
  const size = Sigma.prototype.scaleSize.call(receiver as unknown as Sigma, 11);
  expect(size).toBeLessThanOrEqual(11); expect(screen(0.5 + spacing / span) - screen(0.5)).toBeGreaterThan(size * 2 + 4);
});

import { CAMERA_LIMITS, cameraRatio, localFocusRatio } from '../src/renderer/canvas/camera.js';
it('shares SDK camera bounds and focuses using local normalized spacing instead of an overview ratio', () => {
  const settings = resolveSettings(canvasOptions().settings ?? {}); expect(settings.minCameraRatio).toBe(CAMERA_LIMITS.minimum); expect(settings.maxCameraRatio).toBe(CAMERA_LIMITS.maximum);
  expect(settings.itemSizesReference).toBe('screen');
  expect(localFocusRatio({ x: 0.5, y: 0.5 }, [{ x: 0.5, y: 0.5 }, { x: 0.5001, y: 0.5 }], { width: 400, height: 300 })).toBeLessThan(0.001);
  expect(cameraRatio(1e-12)).toBe(CAMERA_LIMITS.minimum); expect(cameraRatio(100)).toBe(CAMERA_LIMITS.maximum);
  for (const value of [0, -1, NaN, Infinity]) expect(() => cameraRatio(value)).toThrow();
});
