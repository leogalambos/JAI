// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Shared finite camera policy with screen-sized glyphs, independent of semantic graph content. */
export const CAMERA_LIMITS = Object.freeze({ minimum: 0.000001, maximum: 8 });
/**
 * Clamp a finite positive presentation ratio to the same bounds used by the SDK.
 * @param ratio Requested normalized camera ratio.
 * @returns A finite allowed ratio; smaller values magnify the graph.
 * @throws {Error} When the requested ratio is not finite and positive.
 */
export function cameraRatio(ratio: number): number { if (!Number.isFinite(ratio) || ratio <= 0) throw new Error('Invalid camera ratio'); return Math.max(CAMERA_LIMITS.minimum, Math.min(CAMERA_LIMITS.maximum, ratio)); }
/**
 * Choose a local focus scale from actual normalized neighbour distances and viewport space.
 * @param center Normalized focus point.
 * @param points Visible normalized vertices, excluding coincident positions for scale estimation.
 * @param viewport Current CSS viewport dimensions.
 * @returns A bounded ratio that aims for at least 64 CSS pixels between nearby centres.
 */
export function localFocusRatio(center: { x: number; y: number }, points: readonly { x: number; y: number }[], viewport: { width: number; height: number }): number {
  let nearest = Infinity; for (const point of points) { const distance = Math.hypot(point.x - center.x, point.y - center.y); if (distance > 1e-12) nearest = Math.min(nearest, distance); }
  const usable = Math.max(1, Math.min(viewport.width, viewport.height) - 96);
  return cameraRatio(Math.min(0.4, Number.isFinite(nearest) ? nearest * usable / 64 : 0.4));
}
