// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Display-only path anchors following the pinned SDK's public curved/loop geometry. */
/** Finite layout-space or viewport-space point, depending on caller. */
export interface Point { readonly x: number; readonly y: number }
/**
 * Return the t=0.5 quadratic Bézier anchor used by Sigma's curved path.
 * @param source Exact directed source layout position.
 * @param target Exact directed target layout position.
 * @param curvature Active SDK display curvature after parallel/reverse-direction spread.
 * @returns Finite midpoint on the unchanged directed curve.
 * @throws {Error} For nonfinite geometry.
 */
export function curveAnchor(source: Point, target: Point, curvature: number): Point {
  if (![source.x, source.y, target.x, target.y, curvature].every(Number.isFinite)) throw new Error('Invalid edge geometry');
  return { x: (source.x + target.x) / 2 - (target.y - source.y) * curvature / 2, y: (source.y + target.y) / 2 + (target.x - source.x) * curvature / 2 };
}
/**
 * Return the loop tip in CSS pixels for fixed upward loops and a rotation-disabled camera.
 * @param center Node center in CSS pixels.
 * @param nodeSize Active SDK scaleSize output; shader/world-to-CSS conversion contributes a one-half factor.
 * @param loopRadius Active SDK loop-radius multiplier, including parallel loop spread.
 * @returns Upward tip matching the SDK loop's t=0.5 radius constraint.
 * @throws {Error} For invalid radius or nonfinite geometry.
 */
export function loopAnchor(center: Point, nodeSize: number, loopRadius: number): Point {
  if (![center.x, center.y, nodeSize, loopRadius].every(Number.isFinite) || nodeSize < 0 || loopRadius <= 0) throw new Error('Invalid loop geometry');
  return { x: center.x, y: center.y - nodeSize * loopRadius / 2 };
}
