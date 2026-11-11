// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Read-only relation-label anchors against the owned renderer facade. */
import { curveAnchor, loopAnchor } from './geometry.js';
import type { CanvasEdge, CanvasNode } from './model.js';
import type { CanvasRenderer } from './sdk.js';
/**
 * Resolve a relation label anchor from the current renderer's public display values.
 * @param renderer Current owned public SDK facade; no semantic graph writes occur.
 * @param edge Exact compact relation.
 * @param source Exact compact source layout record.
 * @param target Exact compact target layout record.
 * @returns Current CSS-pixel label anchor, or null while active SDK display data is unavailable.
 */
export function edgeLabelAnchor(renderer: Pick<CanvasRenderer, 'project' | 'normalize' | 'scaleSize' | 'edgeData' | 'nodeData'>, edge: CanvasEdge, source: CanvasNode, target: CanvasNode): { x: number; y: number } | null {
  const data = renderer.edgeData(edge.id); if (!data) return null;
  if (edge.from === edge.to) { const size = activeNodeSize(renderer, source.id); if (size === null) return null; return loopDisplayAnchor(renderer, source, size, typeof data.loopRadius === 'number' ? data.loopRadius : 4); }
  return renderer.project(curveAnchor(source, target, typeof data?.curvature === 'number' ? data.curvature : 0));
}

/**
 * Read the actual active SDK size rather than reconstructing selection styling from compact source attributes.
 * @param renderer Owned public display-read facade.
 * @param id Exact current visible node ID.
 * @returns Finite positive active size, or null before its renderer display data is available.
 */
export function activeNodeSize(renderer: Pick<CanvasRenderer, 'nodeData'>, id: string): number | null {
  const data = renderer.nodeData(id); return data && Number.isFinite(data.size) && data.size > 0 ? data.size : null;
}

/**
 * Calibrate the SDK loop tip, including its minimum framed-world radius at deep zoom.
 * @param renderer Current public projection/normalization and size facade.
 * @param source Source graph-space position.
 * @param activeSize Actual post-reducer node size.
 * @param multiplier Actual resolved loop-radius multiplier.
 * @returns Fixed-up CSS loop tip matching the configured unrotated public loop primitive.
 */
export function loopDisplayAnchor(renderer: Pick<CanvasRenderer, 'project' | 'normalize' | 'scaleSize'>, source: { x: number; y: number }, activeSize: number, multiplier: number): { x: number; y: number } {
  const center = renderer.project(source); const nominal = loopAnchor(center, renderer.scaleSize(activeSize), multiplier);
  const sample = { x: source.x + 1, y: source.y }; const projected = renderer.project(sample); const origin = renderer.normalize(source); const framed = renderer.normalize(sample);
  const framedDistance = Math.hypot(framed.x - origin.x, framed.y - origin.y);
  const floor = framedDistance > 0 ? 0.001 * Math.hypot(projected.x - center.x, projected.y - center.y) / framedDistance : 0;
  return { x: center.x, y: center.y - Math.max(center.y - nominal.y, floor) };
}
