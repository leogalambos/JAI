// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Actual pinned SDK option/factory contracts; static GL constants do not simulate a GPU or native render. */
import { expect, it, vi } from 'vitest';
vi.hoisted(() => { Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }); });
import { createCanvas } from '../src/renderer/canvas/index.js';
import { MultiDirectedGraph } from 'graphology';
import { canvasOptions, createSigmaRenderer } from '../src/renderer/canvas/sdk.js';
import { pathCurved, pathLoop } from 'sigma/rendering';
import { resolveSettings } from 'sigma/settings';
import { curveAnchor } from '../src/renderer/canvas/geometry.js';
it('uses real public SDK paths/arrows and settings for independently pickable directed parallel/self edges', () => {
  const options = canvasOptions(); const settings = resolveSettings(options.settings ?? {});
  expect(settings.enableEdgeEvents).toBe(true); expect(settings.enableNodeDrag).toBe(false); expect(settings.enableCameraRotation).toBe(false);
  expect(options.primitives?.nodes?.labelPrograms).toBe(false); expect(settings.nodeLabelEvents).toBe(false); expect(settings.renderLabels).toBe(false); expect(settings.renderEdgeLabels).toBe(false);
  expect(options.primitives?.edges?.paths?.map(path => path.name)).toEqual(['straight', 'curved', 'loop']); expect(options.primitives?.edges?.defaultHead).toBe('arrow');
  expect(options.styles?.edges).toMatchObject({ path: 'straight', parallelPath: 'curved', selfLoopPath: 'loop', head: 'arrow', parallelSpread: 0.35 });
});
it('matches pinned SDK parallel spread and loop-radius computations through the maintained public SDK API', () => {
  const path = pathCurved(); const curvatures = [0, 1, 2].map(index => path.spread!.compute(index, 3, 0.35)); expect(curvatures).toEqual([-0.35, 0, 0.35]);
  const anchors = curvatures.map(curvature => curveAnchor({ x: 0, y: 0 }, { x: 100, y: 0 }, curvature)); expect(new Set(anchors.map(point => point.y)).size).toBe(3);
  expect(pathLoop().spread!.compute(0, 2, 0.35)).toBe(4); expect(pathLoop().spread!.compute(1, 2, 0.35)).toBe(5);
});

it('rejects an invalid DOM host before attaching owned resources or attempting renderer construction', () => {
  expect(() => createCanvas(null as unknown as HTMLElement, () => {})).toThrow('Invalid graph canvas container');
  expect(() => createSigmaRenderer(new MultiDirectedGraph(), null as unknown as HTMLElement, canvasOptions())).toThrow();
});
