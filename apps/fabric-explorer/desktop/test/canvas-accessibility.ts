// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Development-only actual SDK readability fixture; distinct from production application state and Orca evidence. */
import { assertProjection, edgeKey } from '@jai/fabric-explorer-contracts';
import type { Edge, GraphProjection } from '@jai/fabric-explorer-contracts';
import golden from '../../packages/contracts/test/fixtures/projection.json' with { type: 'json' };
import { createCanvas } from '../src/renderer/canvas/index.js';
import type { GraphCanvas } from '../src/renderer/canvas/index.js';
import { createSigmaRenderer } from '../src/renderer/canvas/sdk.js';
import type { CanvasRenderer, CanvasRendererFactory } from '../src/renderer/canvas/sdk.js';
import { canvasPalette } from '../src/renderer/canvas/palette.js';
import type { CanvasPalette } from '../src/renderer/canvas/palette.js';
import { curveAnchor } from '../src/renderer/canvas/geometry.js';
import { loopDisplayAnchor } from '../src/renderer/canvas/display.js';
import { placeLabels } from '../src/renderer/canvas/labels.js';
import type { LabelCandidate, LabelBox } from '../src/renderer/canvas/labels.js';
import type { LayoutResult } from '../src/layout/types.js';
/** One actual renderer observation; booleans are persisted before the main runner decides pass/fail. */
export interface CanvasAccessibilityObservation { readonly scope: 'synthetic-sdk-fixture'; readonly scenario: 'selected-relation' | 'selected-source-hovered-loop'; readonly checks: Readonly<Record<string, boolean>>; readonly activeSourceSize: number; readonly selectedId: string; readonly hoveredId: string | null; readonly labels: readonly { readonly id: string; readonly text: string; readonly x: number; readonly y: number; readonly width: number; readonly height: number }[]; readonly colors: readonly { readonly role: string; readonly foreground: string; readonly background: string; readonly ratio: number }[]; readonly viewport: { readonly width: number; readonly height: number; readonly pixelRatio: number }; readonly loopTip: { readonly x: number; readonly y: number } }
/** Owned development session retained only until both screenshots and observations are captured. */
export interface CanvasAccessibilitySession { readonly relation: CanvasAccessibilityObservation; hoverLoop(): Promise<CanvasAccessibilityObservation>; dispose(): void }
const source = structuredClone(golden) as GraphProjection;
const vertices = source.vertices.slice(0, 2).map((vertex, index) => ({ ...vertex, label: index === 0 ? 'v0 — selected source and a long competing endpoint label' : 'v1 — other endpoint' }));
const original = source.edges[0]!;
if (original.identity.kind !== 'occurrence') throw new Error('Unexpected fixed canvas fixture');
function relation(occurrence: number, from: number, to: number, label: string): Edge {
  const identity = { ...original.identity, occurrence, from: vertices[from]!.identity, to: vertices[to]!.identity } as Edge['identity'];
  return { ...original, id: edgeKey(identity), identity, from: vertices[from]!.id, to: vertices[to]!.id, label };
}
const edges = [relation(0, 0, 1, 'e0 parallel relation'), relation(1, 0, 1, 'e1 selected relation'), relation(2, 1, 0, 'e3 reverse relation'), relation(3, 0, 0, 'e2 hovered self loop')];
const projection: GraphProjection = { ...source, snapshot: { ...source.snapshot, counts: { vertices: '2', edges: '4', findings: '0' } }, vertices, edges, hiddenVertices: '0', hiddenEdges: '0', complete: true, omissions: [] };
assertProjection(projection);
const layout: LayoutResult = { binding: { sessionId: projection.snapshot.sessionId, capability: 'accessibility-fixture', generation: projection.snapshot.generation, requestId: 'layout', projectionId: 'projection' }, algorithm: 'layered', positions: [{ handle: 101, x: -150, y: 0 }, { handle: 102, x: 150, y: 0 }], groups: [], work: 2, iterations: 1, complete: true };
async function paint(): Promise<void> { await new Promise<void>(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve()))); }
function contrast(a: string, b: string): number { const luminance = (color: string) => { const values = [1, 3, 5].map(index => Number.parseInt(color.slice(index, index + 2), 16) / 255).map(value => value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4); return values[0]! * 0.2126 + values[1]! * 0.7152 + values[2]! * 0.0722; }; const x = luminance(a); const y = luminance(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
/**
 * Prepare a bounded actual Sigma fixture, selected relation first and selected-source loop hover on demand.
 * @param container Trusted development host; only the helper-owned panel is removed.
 * @param input Actual resolved application palette for the current theme/scale context.
 * @returns Actual style/label observations and disposal; caller captures both scenarios before disposing.
 * @throws {Error} For unavailable graphics or malformed fixed setup. Failed observation booleans remain in the returned report.
 */
export async function runCanvasAccessibilityChecks(container: HTMLElement, input: CanvasPalette): Promise<CanvasAccessibilitySession> {
  const palette = canvasPalette(input); const panel = document.createElement('section'); const host = document.createElement('div'); const caption = document.createElement('p');
  const width = Math.max(240, Math.min(736, window.innerWidth - 64)); const height = Math.max(180, Math.min(300, window.innerHeight - 150));
  Object.assign(panel.style, { position: 'fixed', left: '12px', top: '12px', width: `${width + 24}px`, padding: '12px', zIndex: '100000', backgroundColor: palette.background, color: palette.labelText, border: `2px solid ${palette.labelBorder}`, font: '12px system-ui' });
  Object.assign(host.style, { width: `${width}px`, height: `${height}px`, position: 'relative' }); caption.textContent = 'Synthetic SDK fixture — actual renderer, separate from the production graph and inspector.'; panel.append(caption, host); container.append(panel);
  let adapter: GraphCanvas | null = null; let runtime: CanvasRenderer | null = null; let stage: HTMLElement | null = null; let unavailable = false; let selected = edges[1]!.id; let hovered: string | null = null;
  const factory: CanvasRendererFactory = (graph, element, options) => { stage = element; runtime = createSigmaRenderer(graph, element, options); runtime.on('enterEdge', payload => { const id = (payload as { edge?: unknown })?.edge; hovered = typeof id === 'string' ? id : null; }); return runtime; };
  const current = () => { if (!runtime || unavailable) throw new Error('Accessibility canvas is unavailable'); return runtime; };
  const positions = new Map(vertices.map((vertex, index) => [vertex.id, layout.positions[index]!]));
  const point = (edge: Edge) => { const renderer = current(); const from = positions.get(edge.from)!; const to = positions.get(edge.to)!; const data = renderer.edgeData(edge.id); return edge.from === edge.to ? loopDisplayAnchor(renderer, from, renderer.nodeData(edge.from)!.size, Number(data?.loopRadius ?? 4)) : renderer.project(curveAnchor(from, to, Number(data?.curvature ?? 0))); };
  const observe = (scenario: CanvasAccessibilityObservation['scenario']): CanvasAccessibilityObservation => {
    const renderer = current(); const viewport = renderer.dimensions(); const overlay = host.querySelector('.fabric-graph-canvas > canvas') as HTMLCanvasElement | null; const context = overlay?.getContext('2d'); if (!overlay || !context) throw new Error('Accessibility label overlay is unavailable');
    context.font = '12px system-ui, sans-serif'; const candidates: LabelCandidate[] = []; const bodies: LabelBox[] = [];
    for (const vertex of vertices) { const active = renderer.nodeData(vertex.id)!; const center = renderer.project(positions.get(vertex.id)!); const radius = renderer.scaleSize(active.size); bodies.push({ x: center.x - radius - 2, y: center.y - radius - 2, width: radius * 2 + 4, height: radius * 2 + 4 }); candidates.push({ id: vertex.id, text: vertex.label, ...center, radius, kind: 'node', priority: vertex.id === selected ? 0 : 2 }); }
    const highlighted = scenario === 'selected-relation' ? edges[1]! : edges[3]!; candidates.push({ id: highlighted.id, text: highlighted.label, ...point(highlighted), radius: 0, kind: 'edge', priority: scenario === 'selected-relation' ? 0 : 1 });
    const labels = placeLabels(candidates, bodies, viewport, text => context.measureText(text).width, renderer.camera().ratio);
    const overlaps = (a: LabelBox, b: LabelBox) => a.x < b.x + b.width && a.x + a.width > b.x && a.y < b.y + b.height && a.y + a.height > b.y;
    const label = labels.find(item => item.id === highlighted.id);
    let labelBackground = palette.labelBackground;
    if (label) { const dpr = overlay.width / viewport.width; const pixel = context.getImageData(Math.floor((label.x + 2) * dpr), Math.floor((label.y + 2) * dpr), 1, 1).data; labelBackground = '#' + [...pixel.slice(0, 3)].map(value => value.toString(16).padStart(2, '0')).join(''); }
    const colors = [{ role: 'active-source', foreground: renderer.nodeData(vertices[0]!.id)!.color, background: palette.background }, { role: 'active-relation', foreground: String(renderer.edgeData(highlighted.id)?.color), background: palette.background }, { role: 'label-text', foreground: String(context.fillStyle), background: labelBackground }, { role: 'label-border', foreground: label?.selected ? palette.selected : palette.labelBorder, background: labelBackground }].map(item => ({ ...item, ratio: contrast(item.foreground, item.background) }));
    let ink = false;
    if (label) { const dpr = overlay.width / viewport.width; const pixels = context.getImageData(Math.floor((label.x + 4) * dpr), Math.floor((label.y + 4) * dpr), Math.max(1, Math.floor((label.width - 8) * dpr)), Math.max(1, Math.floor((label.height - 8) * dpr))).data; ink = pixels.some((value, index) => index % 4 === 3 && value > 0 && (pixels[index - 3] !== Number.parseInt(palette.labelBackground.slice(1, 3), 16) || pixels[index - 2] !== Number.parseInt(palette.labelBackground.slice(3, 5), 16) || pixels[index - 1] !== Number.parseInt(palette.labelBackground.slice(5, 7), 16))); }
    return { scope: 'synthetic-sdk-fixture', scenario, selectedId: selected, hoveredId: hovered, activeSourceSize: renderer.nodeData(vertices[0]!.id)!.size, loopTip: point(edges[3]!), viewport: { ...viewport, pixelRatio: overlay.width / viewport.width }, labels, colors, checks: { labelPresent: !!label, labelInk: ink, noLabelOrBodyOverlap: labels.every((item, index) => bodies.every(body => !overlaps(item, body)) && labels.slice(index + 1).every(other => !overlaps(item, other))), inViewport: labels.every(item => item.x >= 0 && item.y >= 0 && item.x + item.width <= viewport.width && item.y + item.height <= viewport.height), textContrast: colors.find(item => item.role === 'label-text')!.ratio >= 4.5, objectContrast: colors.filter(item => item.role !== 'label-text').every(item => item.ratio >= 3), activeSelectedSource: scenario !== 'selected-source-hovered-loop' || renderer.nodeData(vertices[0]!.id)!.size === 9, actualLoopHover: scenario !== 'selected-source-hovered-loop' || hovered === edges[3]!.id } };
  };
  try {
    adapter = createCanvas(host, () => {}, () => { unavailable = true; }, factory); if (unavailable) throw new Error('Accessibility canvas initialization failed'); adapter.setPalette(palette); adapter.replace(projection, layout, [101, 102]); adapter.select(selected); await paint();
    const relationObservation = observe('selected-relation');
    return { relation: relationObservation, hoverLoop: async () => { selected = vertices[0]!.id; adapter!.select(selected); await paint(); const location = point(edges[3]!); const rect = stage!.getBoundingClientRect(); const target = document.elementFromPoint(rect.left + location.x, rect.top + location.y); if (!target || !stage!.contains(target)) throw new Error('Accessibility pointer target is unavailable'); target.dispatchEvent(new PointerEvent('pointermove', { bubbles: true, pointerId: 1, pointerType: 'mouse', isPrimary: true, clientX: rect.left + location.x, clientY: rect.top + location.y, buttons: 0, view: window })); await paint(); caption.textContent = 'Synthetic SDK fixture — selected source v0 (active size 9) and actual hovered loop e2.'; return observe('selected-source-hovered-loop'); }, dispose: () => { adapter?.dispose(); panel.remove(); } };
  } catch (error) { adapter?.dispose(); panel.remove(); throw error; }
}
