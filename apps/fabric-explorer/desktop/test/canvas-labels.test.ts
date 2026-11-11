// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Unified screen-space label priority and retained selected-relation collision regression. */
import { expect, it } from 'vitest';
import { placeLabels } from '../src/renderer/canvas/labels.js';
import type { LabelCandidate } from '../src/renderer/canvas/labels.js';
import { curveAnchor, loopAnchor } from '../src/renderer/canvas/geometry.js';
const measure = (text: string) => Array.from(text).length * 7;
const overlap = (a: { x: number; y: number; width: number; height: number }, b: { x: number; y: number; width: number; height: number }) => a.x < b.x + b.width && a.x + a.width > b.x && a.y < b.y + b.height && a.y + a.height > b.y;
it('places selected edge before endpoint labels and avoids all occupied node/label rectangles', () => {
  const candidates: LabelCandidate[] = [{ id: 'v0', text: 'Vertex label', x: 80, y: 80, radius: 8, kind: 'node', priority: 2 }, { id: 'e1', text: 'Selected relation', x: 120, y: 80, radius: 0, kind: 'edge', priority: 0 }, { id: 'v1', text: 'Other vertex', x: 240, y: 80, radius: 8, kind: 'node', priority: 2 }];
  const obstacles = [{ x: 70, y: 70, width: 20, height: 20 }, { x: 230, y: 70, width: 20, height: 20 }];
  const labels = placeLabels(candidates, obstacles, { width: 500, height: 240 }, measure, 0.3); expect(labels[0]?.id).toBe('e1');
  expect(labels.every(label => obstacles.every(body => !overlap(label, body)))).toBe(true);
  expect(labels.every((label, index) => labels.slice(index + 1).every(other => !overlap(label, other)))).toBe(true);
  expect(placeLabels([...candidates].reverse(), obstacles, { width: 500, height: 240 }, measure, 0.3)).toEqual(labels);
});
it('applies semantic zoom budgets and finite long Unicode label truncation without mutating source text', () => {
  const source = 'é😀<script>'.repeat(5000); const candidates: LabelCandidate[] = Array.from({ length: 100 }, (_, i) => ({ id: `n-${i}`, text: i === 0 ? source : `Node ${i}`, x: 40 + i % 10 * 95, y: 40 + Math.floor(i / 10) * 60, radius: 7, kind: 'node', priority: i === 0 ? 0 : 2 }));
  const viewport = { width: 1100, height: 700 };
  expect(placeLabels(candidates, [], viewport, measure, 2)).toHaveLength(1);
  expect(placeLabels(candidates, [], viewport, measure, 1).length).toBeLessThanOrEqual(25);
  const detail = placeLabels(candidates, [], viewport, measure, 0.2); expect(detail.length).toBeLessThanOrEqual(81); expect(detail[0]?.text.endsWith('…')).toBe(true); expect(detail[0]?.width).toBeLessThanOrEqual(320); expect(candidates[0]?.text).toBe(source);
  expect(placeLabels(candidates, [], { width: 20, height: 20 }, measure, 1)).toEqual([]);
  expect(() => placeLabels([], [], viewport, measure, 0)).toThrow();
});
it('computes distinct forward/reverse curve anchors and increasing self-loop tips', () => {
  const a = { x: 0, y: 0 }; const b = { x: 100, y: 0 };
  expect(curveAnchor(a, b, 0.4)).toEqual({ x: 50, y: 20 }); expect(curveAnchor(b, a, -0.4)).toEqual({ x: 50, y: 20 });
  expect(curveAnchor(a, b, -0.4)).toEqual({ x: 50, y: -20 }); expect(loopAnchor({ x: 80, y: 100 }, 8, 4)).toEqual({ x: 80, y: 84 });
  expect(loopAnchor({ x: 80, y: 100 }, 8, 5).y).toBeLessThan(loopAnchor({ x: 80, y: 100 }, 8, 4).y);
  expect(() => curveAnchor(a, b, NaN)).toThrow(); expect(() => loopAnchor(a, -1, 4)).toThrow();
});
it('keeps hovered vertex labels at overview and selected/hovered labels clear at supported display scales', () => {
  for (const scale of [1, 1.5, 2]) {
    const viewport = { width: 736 / scale, height: 400 / scale };
    const candidates: LabelCandidate[] = [
      { id: 'selected-edge', text: 'Selected relation', x: viewport.width / 2, y: viewport.height / 2, radius: 0, kind: 'edge', priority: 0 },
      { id: 'hovered-node', text: 'Hovered endpoint', x: viewport.width * 0.16, y: viewport.height / 2, radius: 9, kind: 'node', priority: 1 },
      { id: 'ordinary-node', text: 'Ordinary endpoint', x: viewport.width * 0.84, y: viewport.height / 2, radius: 7, kind: 'node', priority: 2 },
    ];
    const obstacles = candidates.filter(item => item.kind === 'node').map(item => ({ x: item.x - item.radius - 2, y: item.y - item.radius - 2, width: item.radius * 2 + 4, height: item.radius * 2 + 4 }));
    const placed = placeLabels(candidates, obstacles, viewport, measure, 2);
    expect(placed.map(label => label.id)).toEqual(['selected-edge', 'hovered-node']);
    expect(placed.every(label => label.x >= 0 && label.y >= 0 && label.x + label.width <= viewport.width && label.y + label.height <= viewport.height)).toBe(true);
    expect(placed.every((label, index) => obstacles.every(body => !overlap(label, body)) && placed.slice(index + 1).every(other => !overlap(label, other)))).toBe(true);
  }
});
