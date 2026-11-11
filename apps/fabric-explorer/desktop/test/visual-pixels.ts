// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Read-only BGRA pixel evidence inside the actual clipped production graph region. */
/** Exact RGB count and sampled bitmap region; this does not establish edge completeness or visual quality. */
export interface GraphPixelObservation { readonly matches: number; readonly sampled: number; readonly color: string; readonly tolerance: number; readonly image: { width: number; height: number }; readonly region: { left: number; top: number; right: number; bottom: number } }
/**
 * Count resolved unselected-node color in a NativeImage scale-one BGRA bitmap.
 * @param bitmap Actual tightly packed NativeImage.toBitmap data, not DOM or overlay metadata.
 * @param image Matching NativeImage.getSize(1) dimensions.
 * @param viewport Actual current CSS viewport used to map the clipped graph rectangle.
 * @param region Ancestor-clipped CSS graph rectangle.
 * @param color Resolved application canvas.node hex RGB color.
 * @returns Actual matching opaque pixels and exact sampled bitmap region.
 * @throws {Error} For malformed size, color or bitmap correspondence.
 */
export function graphNodePixels(bitmap: Uint8Array, image: { width: number; height: number }, viewport: { width: number; height: number }, region: { left: number; top: number; right: number; bottom: number }, color: string): GraphPixelObservation {
  if (![image.width, image.height].every(value => Number.isInteger(value) && value > 0) || ![viewport.width, viewport.height].every(value => Number.isFinite(value) && value > 0) || !Object.values(region).every(Number.isFinite) || bitmap.length !== image.width * image.height * 4 || !/^#[a-f0-9]{6}$/i.test(color)) throw new Error('Invalid native bitmap correspondence');
  const target = [1, 3, 5].map(index => Number.parseInt(color.slice(index, index + 2), 16)); const tolerance = 10;
  const left = Math.max(0, Math.min(image.width, Math.ceil(region.left * image.width / viewport.width))); const right = Math.max(left, Math.min(image.width, Math.floor(region.right * image.width / viewport.width)));
  const top = Math.max(0, Math.min(image.height, Math.ceil(region.top * image.height / viewport.height))); const bottom = Math.max(top, Math.min(image.height, Math.floor(region.bottom * image.height / viewport.height)));
  let matches = 0;
  for (let y = top; y < bottom; y++) for (let x = left; x < right; x++) { const at = (y * image.width + x) * 4; if (bitmap[at + 3]! >= 240 && Math.abs(bitmap[at + 2]! - target[0]!) <= tolerance && Math.abs(bitmap[at + 1]! - target[1]!) <= tolerance && Math.abs(bitmap[at]! - target[2]!) <= tolerance) matches++; }
  return { matches, sampled: (right - left) * (bottom - top), color, tolerance, image: { ...image }, region: { left, top, right, bottom } };
}
