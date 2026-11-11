// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Loop anchor calibration against the actual pinned SDK shader and public viewport transforms; no GPU claim. */
import { expect, it, vi } from 'vitest';
vi.hoisted(() => { Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }); });
import Sigma from 'sigma';
import { pathLoop } from 'sigma/rendering';
import { resolveSettings } from 'sigma/settings';
import { getMatrixImpact, matrixFromCamera, multiplyVec2 } from 'sigma/utils';
import { loopAnchor } from '../src/renderer/canvas/geometry.js';
it('matches active loop shader radius after the actual SDK world-to-CSS transform', () => {
  const path = pathLoop(); expect(path.glsl).toContain('v_sourceNodeSize * u_correctionRatio / u_sizeRatio');
  const settings = resolveSettings({}); const graph = { width: 300, height: 1 };
  for (const [width, height] of [[736, 400], [640, 400], [1920, 1080]]) for (const ratio of [0.5, 1, 2]) for (const size of [7, 9]) {
    const viewport = { width: width!, height: height! }; const camera = { x: 0.5, y: 0.5, ratio, angle: 0 }; const matrix = matrixFromCamera(camera, viewport, graph, 48);
    const receiver = { camera, graphToViewportRatio: 1, internals: { settings }, getSetting: (key: keyof typeof settings) => settings[key] };
    const scaled = Sigma.prototype.scaleSize.call(receiver as unknown as Sigma, size);
    const correction = getMatrixImpact(matrix, camera, viewport);
    const css = (point: { x: number; y: number }) => { const clip = multiplyVec2(matrix, point); return { x: (1 + clip.x) * viewport.width / 2, y: (1 - clip.y) * viewport.height / 2 }; };
    const source = { x: 0.25, y: 0.5 }; const center = css(source);
    for (const index of [0, 1]) {
      const multiplier = path.spread!.compute(index, 2, 0.35);
      const shaderRadius = Math.max(size * correction / (size / scaled) * multiplier, 0.001);
      const tip = css({ x: source.x, y: source.y + shaderRadius });
      expect(loopAnchor(center, scaled, multiplier).y).toBeCloseTo(tip.y, 5);
    }
  }
});

import { canvasOptions } from '../src/renderer/canvas/sdk.js';
import { edgeLabelAnchor } from '../src/renderer/canvas/display.js';
import { createNormalizationFunction } from 'sigma/utils';
import type { CanvasNode, CanvasEdge } from '../src/renderer/canvas/model.js';
it('tracks the actual SDK loop world-radius floor at deep screen-sized zoom and multiple viewports', () => {
  const settings = resolveSettings(canvasOptions().settings ?? {}); const dimensions = { width: 300, height: 1 }; const normalize = createNormalizationFunction({ x: [-150, 150], y: [0, 1] });
  const source = { id: 'source', x: -75, y: 0.5 } as CanvasNode; const edge = { id: 'loop', from: 'source', to: 'source' } as CanvasEdge;
  for (const viewport of [{ width: 736, height: 400 }, { width: 1200, height: 800 }, { width: 400, height: 736 }]) for (const ratio of [settings.minCameraRatio!, 0.001, 0.02, 0.5, 1, settings.maxCameraRatio!]) for (const size of [7, 9, 11]) {
    const camera = { x: 0.5, y: 0.5, ratio, angle: 0 }; const matrix = matrixFromCamera(camera, viewport, dimensions, 48);
    const css = (point: { x: number; y: number }) => { const clip = multiplyVec2(matrix, point); return { x: (1 + clip.x) * viewport.width / 2, y: (1 - clip.y) * viewport.height / 2 }; };
    const receiver = { camera, graphToViewportRatio: 1, internals: { settings }, getSetting: (key: keyof typeof settings) => settings[key] };
    const scaleSize = (value: number) => Sigma.prototype.scaleSize.call(receiver as unknown as Sigma, value);
    const radius = Math.max(size * getMatrixImpact(matrix, camera, viewport) / (size / scaleSize(size)) * 4, 0.001); const origin = normalize(source);
    const expected = css({ x: origin.x, y: origin.y + radius });
    const actual = edgeLabelAnchor({ project: point => css(normalize(point)), normalize, scaleSize, edgeData: () => ({ loopRadius: 4 }), nodeData: () => ({ size, color: '#123456' }) }, edge, source, source)!;
    expect(actual.x).toBeCloseTo(expected.x, 3);
    // Public matrices use Float32 storage; at the deepest magnification compare within 0.05 CSS pixels.
    expect(Math.abs(actual.y - expected.y)).toBeLessThan(0.05);
  }
});
