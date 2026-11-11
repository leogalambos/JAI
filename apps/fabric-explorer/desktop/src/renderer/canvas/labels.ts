// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Bounded deterministic screen-space labels shared by vertices and relations. */
/** Label anchor in CSS pixels; priority zero is the selected exact element. */
export interface LabelCandidate { readonly id: string; readonly text: string; readonly x: number; readonly y: number; readonly priority: number; readonly kind: 'node' | 'edge'; readonly radius: number }
/** Screen-space occupied rectangle, in CSS pixels. */
export interface LabelBox { readonly x: number; readonly y: number; readonly width: number; readonly height: number }
/** Display-only label; full semantic text remains in the inspector. */
export interface PlacedLabel extends LabelBox { readonly id: string; readonly text: string; readonly anchorX: number; readonly anchorY: number; readonly selected: boolean }
/**
 * Lay out one finite label budget, reserving node bodies and earlier higher-priority labels.
 * @param candidates Visible label anchors; selection first then deterministic exact-ID order.
 * @param obstacles Visible node-body bounds, never arbitrary full graph source records.
 * @param viewport Positive CSS-pixel stage dimensions.
 * @param measure Trusted canvas text width measurement in the active font.
 * @param ratio Positive camera ratio used for explicit semantic zoom budgets.
 * @returns At most82 inert text labels with nonoverlapping boxes or an empty narrow viewport.
 * @throws {Error} For invalid viewport, camera ratio or excessive bounded projection input.
 */
export function placeLabels(candidates: readonly LabelCandidate[], obstacles: readonly LabelBox[], viewport: { width: number; height: number }, measure: (text: string) => number, ratio: number): readonly PlacedLabel[] {
  if (![viewport.width, viewport.height, ratio].every(value => Number.isFinite(value) && value > 0) || candidates.length > 25000 || obstacles.length > 5000) throw new Error('Invalid canvas label bounds');
  if (viewport.width < 24 || viewport.height < 24) return [];
  const cells = new Map<string, LabelBox[]>();
  const visit = (box: LabelBox, callback: (key: string) => void) => { for (let x = Math.floor(box.x / 64); x <= Math.floor((box.x + box.width) / 64); x++) for (let y = Math.floor(box.y / 64); y <= Math.floor((box.y + box.height) / 64); y++) callback(`${x}:${y}`); };
  const insert = (box: LabelBox) => visit(box, key => { const list = cells.get(key) ?? []; list.push(box); cells.set(key, list); });
  const overlaps = (box: LabelBox) => { let found = false; visit(box, key => { for (const other of cells.get(key) ?? []) if (box.x < other.x + other.width + 3 && box.x + box.width + 3 > other.x && box.y < other.y + other.height + 3 && box.y + box.height + 3 > other.y) { found = true; break; } }); return found; };
  for (const obstacle of obstacles) insert(obstacle);
  const result: PlacedLabel[] = []; const budget = ratio > 1.4 ? 0 : ratio > 0.45 ? 24 : 80; let ordinary = 0;
  const ordered = [...candidates].sort((a, b) => a.priority - b.priority || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  for (const candidate of ordered) {
    if (result.length >= 82 || !candidate.text || (candidate.priority > 1 && (candidate.kind === 'edge' || ordinary >= budget))) continue;
    if (![candidate.x, candidate.y, candidate.radius].every(Number.isFinite)) continue;
    const maxWidth = Math.min(320, viewport.width - 16); let prefix = candidate.text.slice(0, 256); if (/[\uD800-\uDBFF]$/.test(prefix)) prefix = prefix.slice(0, -1); let text = Array.from(prefix).slice(0, 128).join('');
    if (maxWidth < measure('…') + 12) continue;
    const truncated = text.length < candidate.text.length;
    if (truncated) text += '…';
    while (text.length > 1 && measure(text) + 12 > maxWidth) { const points = Array.from(text.replace(/…$/, '')); points.pop(); text = points.join('') + '…'; }
    const width = Math.min(maxWidth, Math.max(12, measure(text) + 12)); const height = 22;
    const offsets = candidate.kind === 'node' ? [[candidate.radius + 8, -11], [-width - candidate.radius - 8, -11], [-width / 2, -height - candidate.radius - 8], [-width / 2, candidate.radius + 8]] : [[-width / 2, -height - 7], [-width / 2, 7], [12, -height / 2], [-width - 12, -height / 2], [-width / 2, -height - 32], [-width / 2, 32], [28, -height - 20], [-width - 28, -height - 20]];
    for (const [dx, dy] of offsets) {
      const box = { x: Math.max(4, Math.min(viewport.width - width - 4, candidate.x + dx!)), y: Math.max(4, Math.min(viewport.height - height - 4, candidate.y + dy!)), width, height };
      if (overlaps(box)) continue;
      const placed = { ...box, id: candidate.id, text, anchorX: candidate.x, anchorY: candidate.y, selected: candidate.priority === 0 }; result.push(placed); insert(box); if (candidate.priority > 1) ordinary++; break;
    }
  }
  return result;
}
