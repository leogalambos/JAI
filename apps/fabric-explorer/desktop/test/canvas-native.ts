// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Development-only finite actual-DOM/Sigma checks; never imported by production renderer or preload. */
import { assertProjection, edgeKey } from '@jai/fabric-explorer-contracts';
import type { Edge, GraphProjection } from '@jai/fabric-explorer-contracts';
import type { AbstractGraph } from 'graphology-types';
import golden from '../../packages/contracts/test/fixtures/projection.json' with { type: 'json' };
import type { LayoutResult } from '../src/layout/types.js';
import { createCanvas } from '../src/renderer/canvas/index.js';
import type { GraphCanvas } from '../src/renderer/canvas/index.js';
import { createSigmaRenderer } from '../src/renderer/canvas/sdk.js';
import type { CanvasRenderer, CanvasRendererFactory } from '../src/renderer/canvas/sdk.js';
import { curveAnchor, loopAnchor } from '../src/renderer/canvas/geometry.js';
import { canvasSingleClick, canvasDrag } from './canvas-input.js';
import type { CanvasInputPort } from './canvas-input.js';
import { placeLabels } from '../src/renderer/canvas/labels.js';
import type { LabelCandidate, LabelBox } from '../src/renderer/canvas/labels.js';
export { runSdkNativeComparison } from './sdk-native.js';
/** Bounded active SDK loop values retained only in development observations. */
export interface CanvasLoopDiagnostics { readonly edgeId: string; readonly active: { readonly loopRadius: number | null; readonly loopAngle: number | null; readonly loopFixedOrientation: number | null }; readonly scaledNodeSize: number | null; readonly target: { readonly x: number; readonly y: number } | null; readonly selectedId: string | null }
/** One existing numbered check; failures/skips remain failures for the owning native runner. */
export interface CanvasNativeStep { readonly step: number; readonly title: string; readonly status: 'pass' | 'fail' | 'unknown' | 'skipped'; readonly error?: string; readonly blockedBy?: readonly number[]; readonly diagnostics?: CanvasLoopDiagnostics }
/** Complete finite observations; this report never grants acceptance or masks failed checks. */
export interface CanvasNativeReport { readonly steps: readonly CanvasNativeStep[]; readonly contextLoss: 'observed' | 'unknown'; readonly source: 'actual-production-adapter' }
function check(condition: unknown, message: string): asserts condition { if (!condition) throw new Error(`Canvas native check: ${message}`); }
async function paint(): Promise<void> { await new Promise<void>(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve()))); }
/**
 * Run eleven finite display checks using the production canvas and actual pinned SDK in a real document.
 * @param container Trusted development-only host; the helper owns/removes only one child panel.
 * @returns All eleven numbered observations after initialization; dependent failures are skipped and unsupported context loss is unknown, never fabricated pass.
 * @throws {Error} For initialization failure or invalid fixed fixture; later failed invariants are returned explicitly for the owning runner to reject.
 */
export async function runCanvasNativeChecks(container: HTMLElement): Promise<CanvasNativeReport> {
  const panel = document.createElement('section'); Object.assign(panel.style, { position: 'fixed', left: '16px', top: '16px', width: '760px', background: 'white', color: '#172b43', zIndex: '100000', padding: '12px', border: '2px solid #172b43' });
  const progress = document.createElement('p'); progress.setAttribute('role', 'status'); const host = document.createElement('div'); Object.assign(host.style, { width: '736px', height: '400px', position: 'relative' }); panel.append(progress, host); container.append(panel);
  const steps: CanvasNativeStep[] = [];
  const start = (title: string) => { progress.textContent = `Canvas check ${steps.length + 1}/11: ${title}`; console.info(progress.textContent); };
  const done = (title: string, status: 'pass' | 'unknown' = 'pass') => { steps.push({ step: steps.length + 1, title, status }); };
  const captureStep = async (title: string, action: () => Promise<void | 'pass' | 'unknown'>, dependencies: readonly number[] = [], diagnostics?: () => CanvasLoopDiagnostics): Promise<void> => {
    const step = steps.length + 1; start(title);
    const blockedBy = dependencies.filter(number => steps[number - 1]?.status !== 'pass');
    if (blockedBy.length) { steps.push({ step, title, status: 'skipped', error: 'Prerequisite canvas check failed.', blockedBy }); return; }
    let status: CanvasNativeStep['status'] = 'pass'; let failure: string | undefined;
    try { status = await action() ?? 'pass'; } catch (error) { status = 'fail'; failure = error instanceof Error ? error.message.slice(0, 512) : 'Canvas check failed.'; }
    let detail: CanvasLoopDiagnostics | undefined;
    try { detail = diagnostics?.(); } catch { /* Diagnostic unavailability cannot hide the original result. */ }
    steps.push({ step, title, status, ...(failure ? { error: failure } : {}), ...(detail ? { diagnostics: detail } : {}) });
  };
  let adapter: GraphCanvas | null = null; let runtime: CanvasRenderer | null = null; let graph: AbstractGraph | null = null; let stage: HTMLElement | null = null; let selected: string | null = null; let unavailable = false; let contextLoss: 'observed' | 'unknown' = 'unknown';
  const factory: CanvasRendererFactory = (input, element, options) => { graph = input; stage = element; runtime = createSigmaRenderer(input, element, options); return runtime; };
  const canvas = () => { check(adapter, 'canvas adapter missing'); return adapter; };
  const renderer = () => { check(runtime, 'actual SDK is unavailable'); return runtime; };
  const ownedGraph = () => { check(graph, 'graph missing'); return graph; };
  const stageElement = () => { check(stage, 'stage missing'); return stage; };
  const source = structuredClone(golden) as GraphProjection;
  const vertices = source.vertices.slice(0, 2).map((vertex, index) => ({ ...vertex, label: index === 0 ? 'v0 — a long endpoint label competing with the selected relation' : 'v1' }));
  const original = source.edges[0]!; check(original.identity.kind === 'occurrence', 'fixture edge origin');
  const edge = (occurrence: number, from: number, to: number, label: string): Edge => {
    const identity = { ...original.identity, occurrence, from: vertices[from]!.identity, to: vertices[to]!.identity } as Edge['identity'];
    return { ...original, id: edgeKey(identity), identity, from: vertices[from]!.id, to: vertices[to]!.id, label };
  };
  const edges = [edge(0, 0, 1, 'e0 first relation'), edge(1, 0, 1, 'e1 selected relation'), edge(2, 1, 0, 'e3 reverse relation'), edge(3, 0, 0, 'e2 self loop')];
  const projection: GraphProjection = { ...source, snapshot: { ...source.snapshot, counts: { vertices: '2', edges: '4', findings: '0' } }, vertices, edges, hiddenVertices: '0', hiddenEdges: '0', complete: true, omissions: [] }; assertProjection(projection);
  const layout: LayoutResult = { binding: { sessionId: projection.snapshot.sessionId, capability: 'native-synthetic-capability', generation: projection.snapshot.generation, requestId: 'native-layout', projectionId: 'native-projection' }, algorithm: 'layered', positions: [{ handle: 101, x: -150, y: 0 }, { handle: 102, x: 150, y: 0 }], groups: [], work: 2, iterations: 1, complete: true };
  const positions = new Map(vertices.map((vertex, index) => [vertex.id, layout.positions[index]!]));
  const pointForEdge = (id: string) => {
    const current = renderer(); const item = edges.find(value => value.id === id)!; const from = positions.get(item.from)!; const to = positions.get(item.to)!; const data = current.edgeData(id);
    if (item.from === item.to) return loopAnchor(current.project(from), current.scaleSize(7), Number(data?.loopRadius ?? 4));
    return current.project(curveAnchor(from, to, Number(data?.curvature ?? 0)));
  };
  const inputPort: CanvasInputPort = {
    dispatch: (type, point, buttons) => {
      check(typeof PointerEvent === 'function', 'PointerEvent input is unavailable');
      const rect = stageElement().getBoundingClientRect(); const element = document.elementFromPoint(rect.left + point.x, rect.top + point.y); check(element && stageElement().contains(element), 'actual SDK input target missing');
      element.dispatchEvent(new PointerEvent(type, { bubbles: true, clientX: rect.left + point.x, clientY: rect.top + point.y, button: 0, buttons, pointerType: 'mouse', pointerId: 1, isPrimary: true, view: window }));
    },
    // This finite SDK-derived input fence establishes separate gestures; it is not a renderer timeout or retry.
    settle: async milliseconds => { if (milliseconds > 0) await new Promise<void>(resolve => window.setTimeout(resolve, milliseconds)); await paint(); },
    stopCameraAnimation: () => { const current = renderer(); current.move(current.camera()); },
  };
  const input = (point: { x: number; y: number }) => canvasSingleClick(inputPort, point);
  const loopDiagnostics = (): CanvasLoopDiagnostics => {
    const current = renderer(); const active = current.edgeData(edges[3]!.id); const finite = (value: unknown): number | null => typeof value === 'number' && Number.isFinite(value) ? value : null;
    const target = pointForEdge(edges[3]!.id);
    return { edgeId: edges[3]!.id, active: { loopRadius: finite(active?.loopRadius), loopAngle: finite(active?.loopAngle), loopFixedOrientation: finite(active?.loopFixedOrientation) }, scaledNodeSize: finite(current.scaleSize(7)), target: Number.isFinite(target.x) && Number.isFinite(target.y) ? target : null, selectedId: selected };
  };
  try {
    start('Initialize and replace production canvas'); adapter = createCanvas(host, id => { selected = id; }, () => { unavailable = true; }, factory); check(!unavailable, 'WebGL2 initialization failed'); canvas().replace(projection, layout, [101, 102]); await paint(); check(ownedGraph().order === 2 && ownedGraph().size === 4, 'bounded graph cardinality'); done('Initialize and replace production canvas');
    await captureStep('Select exact vertex through actual DOM input', async () => { await input(renderer().project(layout.positions[0]!)); check(selected === vertices[0]!.id, 'node picking identity');
    });
    await captureStep('Pick both parallel and reverse relations independently', async () => {
      for (const item of edges.slice(0, 3)) { await input(pointForEdge(item.id)); check(selected === item.id, 'parallel/reverse edge picking identity'); check(renderer().edgeData(item.id)?.head === 'arrow', 'directed arrow style'); }
    });
    await captureStep('Pick self loop independently', async () => { await input(pointForEdge(edges[3]!.id)); check(selected === edges[3]!.id, 'loop picking identity');
    }, [], loopDiagnostics);
    await captureStep('Observe selected edge label geometry and actual overlay pixels', async () => { await input(pointForEdge(edges[1]!.id));
      const current = renderer(); const viewport = current.dimensions(); const obstacles: LabelBox[] = []; const candidates: LabelCandidate[] = [];
      for (const vertex of vertices) { const point = current.project(positions.get(vertex.id)!); const radius = current.scaleSize(7); obstacles.push({ x: point.x - radius - 2, y: point.y - radius - 2, width: 2 * radius + 4, height: 2 * radius + 4 }); candidates.push({ id: vertex.id, text: vertex.label, ...point, radius, kind: 'node', priority: 2 }); }
      candidates.push({ id: edges[1]!.id, text: edges[1]!.label, ...pointForEdge(edges[1]!.id), radius: 0, kind: 'edge', priority: 0 });
      const overlay = host.querySelector('.fabric-graph-canvas > canvas') as HTMLCanvasElement | null; check(overlay, 'label overlay missing'); const context = overlay.getContext('2d'); check(context, '2D overlay missing'); context.font = '12px system-ui, sans-serif';
      const labels = placeLabels(candidates, obstacles, viewport, text => context.measureText(text).width, current.camera().ratio); check(labels[0]?.id === edges[1]!.id, 'selected relation label not prioritized');
      const overlaps = (a: LabelBox, b: LabelBox) => a.x < b.x + b.width && a.x + a.width > b.x && a.y < b.y + b.height && a.y + a.height > b.y;
      check(labels.every((label, index) => obstacles.every(body => !overlaps(label, body)) && labels.slice(index + 1).every(other => !overlaps(label, other))), 'selected/node label overlap');
      const selectedBox = labels[0]!; const dpr = overlay.width / viewport.width; const pixels = context.getImageData(Math.floor((selectedBox.x + 4) * dpr), Math.floor((selectedBox.y + 4) * dpr), Math.max(1, Math.floor((selectedBox.width - 8) * dpr)), Math.max(1, Math.floor((selectedBox.height - 8) * dpr))).data;
      check(pixels.some((value, index) => index % 4 === 3 && value > 0 && pixels[index - 1]! < 180), 'selected label pixels absent');
    }, [3]);
    await captureStep('Pan with actual DOM pointer input', async () => { const before = renderer().camera();
      await canvasDrag(inputPort, { x: 300, y: 330 }, { x: 355, y: 350 }); check(renderer().camera().x !== before.x || renderer().camera().y !== before.y, 'camera did not pan');
    });
    await captureStep('Zoom fit and focus through production camera methods', async () => { canvas().fit(); canvas().zoom(2); check(Math.abs(renderer().camera().ratio - 0.5) < 1e-9, 'zoom ratio'); canvas().focus(vertices[1]!.id); check(renderer().camera().ratio <= 0.4, 'focus zoom'); canvas().fit(); check(renderer().camera().ratio === 1 && renderer().camera().x === 0.5, 'fit state');
    });
    await captureStep('Resize stage and label overlay', async () => { host.style.width = '640px'; await paint(); check(Math.abs(renderer().dimensions().width - 640) < 2, 'SDK stage resize'); check(Math.abs(Number.parseFloat((host.querySelector('.fabric-graph-canvas > canvas') as HTMLCanvasElement).style.width) - 640) < 2, 'overlay resize');
    });
    await captureStep('Replace using original graph and reject stale layout', async () => { const same = ownedGraph(); canvas().replace(projection, layout, [101, 102]); check(ownedGraph() === same, 'Graphology instance changed'); let rejected = false; try { canvas().replace(projection, { ...layout, binding: { ...layout.binding, generation: '2' } }, [101, 102]); } catch { rejected = true; } check(rejected && ownedGraph().size === 4, 'invalid replacement destroyed view');
    });
    await captureStep('Observe context loss fallback when supported', async () => {  const glCanvas = stageElement().querySelector('canvas.sigma-stage') as HTMLCanvasElement | null; const gl = glCanvas?.getContext('webgl2'); const extension = gl?.getExtension('WEBGL_lose_context');
      if (extension) { extension.loseContext(); for (let i = 0; i < 8 && !unavailable; i++) await paint(); if (unavailable) contextLoss = 'observed'; }

        return contextLoss === 'observed' ? 'pass' : 'unknown';
    });
    await captureStep('Dispose and remount without owned resource accumulation', async () => { canvas().dispose(); canvas().dispose(); check(host.childElementCount === 0, 'owned DOM leaked'); unavailable = false;
      adapter = createCanvas(host, id => { selected = id; }, () => { unavailable = true; }, factory); check(!unavailable, 'remount failed'); canvas().replace(projection, layout, [101, 102]); await paint(); canvas().dispose(); check(host.childElementCount === 0, 'remounted DOM leaked');
    });
    return { steps, contextLoss, source: 'actual-production-adapter' };
  } finally { adapter?.dispose(); panel.remove(); }
}
