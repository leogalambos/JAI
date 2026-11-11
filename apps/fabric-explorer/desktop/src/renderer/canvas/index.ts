// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Maintained bounded graph canvas; semantic source ownership stays outside this adapter. */
import { cameraRatio, localFocusRatio } from './camera.js';
import type { GraphProjection } from '@jai/fabric-explorer-contracts';
import type { LayoutResult } from '../../layout/types.js';
import { CanvasGraph } from './model.js';
import type { CanvasProjection } from './model.js';
import { canvasOptions, createSigmaRenderer } from './sdk.js';
import type { CanvasEvent, CanvasRenderer, CanvasRendererFactory } from './sdk.js';
import { placeLabels } from './labels.js';
import type { LabelCandidate, LabelBox } from './labels.js';
import { canvasPalette, DEFAULT_CANVAS_PALETTE } from './palette.js';
import type { CanvasPalette } from './palette.js';
import { canvasReducers } from './styles.js';
import { edgeLabelAnchor, activeNodeSize } from './display.js';
import { curveAnchor } from './geometry.js';
/** Narrow presentation-only renderer lifetime; no source writer or query operation exists here. */
export interface GraphCanvas {
  /** Replace only a current bounded projection and its matching numeric layout; invalid data preserves the old view. */
  replace(projection: GraphProjection, layout: LayoutResult, handles: readonly number[]): void;
  /** Select one exact visible vertex/edge ID or clear selection; source data is unchanged. */
  select(id: string | null): void;
  /**
   * Apply resolved presentation colors without replacing the graph, selection or camera.
   * @param palette Closed resolved hex RGB theme colors supplied by the root.
   * @throws {Error} For invalid colors or an unavailable canvas; the old palette is retained.
   */
  setPalette(palette: CanvasPalette): void;
  /** Fit the current bounded projection by resetting the normalized camera. */
  fit(): void;
  /** Zoom by a positive finite factor; values greater than one zoom in, with explicit ratio limits. */
  zoom(factor: number): void;
  /** Focus one exact visible node or relation anchor; unknown IDs reject. */
  focus(id: string): void;
  /** Release owned DOM, observers, listeners and GPU resources idempotently. */
  dispose(): void;
}
/** DOM-only preparation; initialization remains explicitly owned and cancellable. */
export interface CanvasPreparation {
  /** Observe browser-provided geometry without reading layout getters; returns an idempotent disconnect. */
  observe(changed: () => void): () => void;
  /** Whether the most recent observed presentation area is positive and finite. */
  measurable(): boolean;
  /** Construct the SDK once after layout, optionally installing the initial palette before any empty refresh. */
  initialize(palette?: CanvasPalette): GraphCanvas;
  /** Live-size gate for a scheduled constructor task; null retains observation until the next positive size. */
  initializeWhenMeasurable(palette?: CanvasPalette): GraphCanvas | null;
  /** Release pending DOM/observer or initialized adapter idempotently. */
  dispose(): void;
}
/**
 * Prepare owned canvas DOM without reading geometry or constructing GPU resources.
 * @param container Root-owned stage host; this adapter adds/removes only its owned child wrapper.
 * @param onSelect Receives exact canonical node/edge IDs, or null after a stage click.
 * @param onUnavailable Optional fixed English status after unavailable WebGL2 or context loss; semantic controls remain root-owned.
 * @param factory Trusted application/test composition factory; defaults to the actual selected Sigma public API.
 * @returns Pending DOM/size owner; initialize constructs the SDK and returns the narrow display adapter.
 * @throws {Error} For invalid host or preparation lifecycle use; SDK initialization failure is reported through onUnavailable.
 */
export function prepareCanvas(container: HTMLElement, onSelect: (id: string | null) => void, onUnavailable?: (message: string) => void, factory: CanvasRendererFactory = createSigmaRenderer): CanvasPreparation {
  if (!container || !container.ownerDocument || typeof container.append !== 'function') throw new Error('Invalid graph canvas container');
  const owner = container.ownerDocument; const wrapper = owner.createElement('div'); wrapper.className = 'fabric-graph-canvas'; Object.assign(wrapper.style, { position: 'relative', width: '100%', height: '100%', overflow: 'hidden' });
  const stage = owner.createElement('div'); Object.assign(stage.style, { position: 'absolute', inset: '0' }); stage.setAttribute('aria-hidden', 'true');
  const overlay = owner.createElement('canvas'); Object.assign(overlay.style, { position: 'absolute', inset: '0', pointerEvents: 'none' }); overlay.setAttribute('aria-hidden', 'true');
  wrapper.append(stage, overlay); container.append(wrapper);
  let palette = DEFAULT_CANVAS_PALETTE; wrapper.style.backgroundColor = palette.background;
  const model = new CanvasGraph(); const graph = model.graph;
  let renderer: CanvasRenderer | null = null; let disposed = false; let failed = false; let selected: string | null = null; let hovered: string | null = null;
  let visible: CanvasProjection = { nodes: [], edges: [] };
  const nodes = new Map<string, CanvasProjection['nodes'][number]>(); const edges = new Map<string, CanvasProjection['edges'][number]>();
  const listeners: { event: CanvasEvent; callback: (payload?: unknown) => void }[] = [];
  let resize: ResizeObserver | null = null; let pendingRefresh = false;
  const measurable = () => Number.isFinite(stage.clientWidth) && Number.isFinite(stage.clientHeight) && stage.clientWidth > 0 && stage.clientHeight > 0;
  const refresh = () => { if (!renderer || disposed || failed) return; if (!measurable()) { pendingRefresh = true; return; } renderer.refresh(); pendingRefresh = false; };
  const requireReady = () => { if (disposed || failed || !renderer) throw new Error('Graph canvas is unavailable'); return renderer; };
  const shutdownRenderer = () => { const current = renderer; renderer = null; if (current) { for (const { event, callback } of listeners) current.off(event, callback); current.kill(); } listeners.length = 0; resize?.disconnect(); resize = null; };
  const unavailable = () => { if (failed || disposed) return; failed = true; shutdownRenderer(); overlay.getContext('2d')?.clearRect(0, 0, overlay.width, overlay.height); onUnavailable?.('Graph canvas is unavailable. Use the element lists and inspector; reopen this view to retry.'); };
  const edgePoint = (id: string) => {
    const current = requireReady(); const edge = edges.get(id)!; const source = nodes.get(edge.from)!; const target = nodes.get(edge.to)!;
    return edgeLabelAnchor(current, edge, source, target);
  };
  const draw = () => {
    if (disposed || failed || !renderer || !measurable()) return;
    const viewport = renderer.dimensions(); if (viewport.width <= 0 || viewport.height <= 0) return;
    const pixelRatio = Math.min(4, Math.max(1, owner.defaultView?.devicePixelRatio ?? 1)); const width = Math.round(viewport.width * pixelRatio); const height = Math.round(viewport.height * pixelRatio);
    if (overlay.width !== width || overlay.height !== height) { overlay.width = width; overlay.height = height; overlay.style.width = `${viewport.width}px`; overlay.style.height = `${viewport.height}px`; }
    const context = overlay.getContext('2d'); if (!context) return;
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0); context.clearRect(0, 0, viewport.width, viewport.height); context.font = '12px system-ui, sans-serif';
    const candidates: LabelCandidate[] = []; const obstacles: LabelBox[] = [];
    for (const node of visible.nodes) {
      const point = renderer.project(node); const active = activeNodeSize(renderer, node.id); if (active === null) continue; const radius = renderer.scaleSize(active);
      if (point.x + radius < 0 || point.y + radius < 0 || point.x - radius > viewport.width || point.y - radius > viewport.height) continue;
      obstacles.push({ x: point.x - radius - 2, y: point.y - radius - 2, width: radius * 2 + 4, height: radius * 2 + 4 });
      candidates.push({ id: node.id, text: node.label, ...point, radius, priority: node.id === selected ? 0 : node.id === hovered ? 1 : 2, kind: 'node' });
    }
    for (const id of new Set([selected, hovered])) if (id && edges.has(id)) { const edge = edges.get(id)!; const point = edgePoint(id); if (!point) continue; candidates.push({ id, text: edge.label, ...point, radius: 0, priority: id === selected ? 0 : 1, kind: 'edge' }); }
    const placed = placeLabels(candidates, obstacles, viewport, text => context.measureText(text).width, renderer.camera().ratio);
    for (const label of placed) {
      context.strokeStyle = label.selected ? palette.selected : palette.labelBorder; context.lineWidth = 1;
      if (label.selected) { context.beginPath(); context.moveTo(label.anchorX, label.anchorY); context.lineTo(Math.max(label.x, Math.min(label.x + label.width, label.anchorX)), Math.max(label.y, Math.min(label.y + label.height, label.anchorY))); context.stroke(); }
      context.fillStyle = palette.labelBackground; context.fillRect(label.x, label.y, label.width, label.height); context.strokeRect(label.x, label.y, label.width, label.height); context.fillStyle = palette.labelText; context.fillText(label.text, label.x + 6, label.y + 15);
    }
  };

  let preparationObserver: ResizeObserver | null = null; let observedPositive = false; let initialized = false;
  const disconnectPreparation = () => { preparationObserver?.disconnect(); preparationObserver = null; };
  const adapter: GraphCanvas = {
    replace: (projection, layout, handles) => {
      const current = requireReady(); const staged = model.replace(projection, layout, handles);
      selected = null; hovered = null; visible = staged; nodes.clear(); edges.clear();
      for (const node of staged.nodes) nodes.set(node.id, node);
      for (const edge of staged.edges) edges.set(edge.id, edge);
      refresh(); current.move({ x: 0.5, y: 0.5, ratio: 1, angle: 0 }); draw();
    },
    select: id => { requireReady(); if (id !== null && !nodes.has(id) && !edges.has(id)) throw new Error('Selected element is not visible'); selected = id; refresh(); draw(); },
    setPalette: value => { requireReady(); const next = canvasPalette(value); palette = next; wrapper.style.backgroundColor = palette.background; refresh(); draw(); },
    fit: () => { requireReady().move({ x: 0.5, y: 0.5, ratio: 1, angle: 0 }); draw(); },
    zoom: factor => { const current = requireReady(); if (!Number.isFinite(factor) || factor <= 0) throw new Error('Invalid zoom factor'); current.move({ ratio: cameraRatio(current.camera().ratio / factor) }); draw(); },
    focus: id => { const current = requireReady(); const node = nodes.get(id); const edge = edges.get(id); if (!node && !edge) throw new Error('Focused element is not visible'); const center = node ?? curveAnchor(nodes.get(edge!.from)!, nodes.get(edge!.to)!, typeof current.edgeData(id)?.curvature === 'number' ? current.edgeData(id)!.curvature as number : 0); current.move({ ...current.normalize(center), ratio: localFocusRatio(current.normalize(center), [...nodes.values()].map(point => current.normalize(point)), current.dimensions()), angle: 0 }); draw(); },
    dispose: () => { if (disposed) return; disposed = true; disconnectPreparation(); shutdownRenderer(); model.dispose(); nodes.clear(); edges.clear(); visible = { nodes: [], edges: [] }; wrapper.remove(); },
  };
  const preparation: CanvasPreparation = {
    observe: changed => {
      if (disposed || initialized || preparationObserver) throw new Error('Canvas preparation is unavailable');
      if (typeof ResizeObserver === 'undefined') throw new Error('Canvas size observation is unavailable');
      preparationObserver = new ResizeObserver(entries => {
        if (disposed || initialized) return;
        const area = entries.find(entry => entry.target === stage)?.contentRect;
        observedPositive = !!area && Number.isFinite(area.width) && Number.isFinite(area.height) && area.width > 0 && area.height > 0;
        changed();
      });
      preparationObserver.observe(stage); return disconnectPreparation;
    },
    measurable: () => !disposed && observedPositive,
    initialize: initialPalette => {
      if (disposed || initialized) throw new Error('Canvas preparation is unavailable');
      initialized = true; disconnectPreparation();
      if (initialPalette) { palette = canvasPalette(initialPalette); wrapper.style.backgroundColor = palette.background; }
  try {
    const options = canvasOptions();
    Object.assign(options, canvasReducers(() => selected, () => palette));
    if (!measurable()) throw new Error('Graph canvas has no measurable presentation area');
    renderer = factory(graph, stage, options);
    const listen = (event: CanvasEvent, callback: (payload?: unknown) => void) => { const guarded = (payload?: unknown) => { if (disposed || failed) return; try { callback(payload); } catch { unavailable(); } }; listeners.push({ event, callback: guarded }); renderer!.on(event, guarded); };
    const choose = (id: string | null) => { selected = id; refresh(); onSelect(id); };
    listen('clickNode', payload => { const id = (payload as { node?: unknown })?.node; if (typeof id === 'string' && nodes.has(id)) choose(id); });
    listen('clickEdge', payload => { const id = (payload as { edge?: unknown })?.edge; if (typeof id === 'string' && edges.has(id)) choose(id); });
    listen('clickStage', () => { hovered = null; choose(null); });
    listen('enterNode', payload => { const id = (payload as { node?: unknown })?.node; hovered = typeof id === 'string' && nodes.has(id) ? id : null; draw(); });
    listen('leaveNode', payload => { const id = (payload as { node?: unknown })?.node; if (hovered === id) hovered = null; draw(); });
    listen('enterEdge', payload => { const id = (payload as { edge?: unknown })?.edge; hovered = typeof id === 'string' && edges.has(id) ? id : null; draw(); });
    listen('leaveEdge', payload => { const id = (payload as { edge?: unknown })?.edge; if (hovered === id) hovered = null; draw(); }); listen('afterRender', draw); listen('resize', draw); listen('webglContextLost', unavailable);
    if (typeof ResizeObserver !== 'undefined') {
      resize = new ResizeObserver(() => {
        if (disposed || failed || !renderer) return;
        if (!measurable()) { pendingRefresh = true; return; }
        try {
          const previous = renderer.dimensions(); const changed = previous.width !== stage.clientWidth || previous.height !== stage.clientHeight;
          renderer.resize();
          // Public SDK resize invalidates backing pixels but does not render graph primitives.
          if (changed || pendingRefresh) refresh();
          draw();
        } catch { unavailable(); }
      });
      resize.observe(wrapper);
    }
  } catch { unavailable(); }
      return adapter;
    },
    initializeWhenMeasurable: initialPalette => {
      if (disposed || initialized) throw new Error('Canvas preparation is unavailable');
      if (!measurable()) { observedPositive = false; return null; }
      return preparation.initialize(initialPalette);
    },
    dispose: () => adapter.dispose(),
  };
  return preparation;
}
/**
 * Construct synchronously for existing explicit canvas consumers and native checks.
 * @param container Host retaining the owned wrapper for this adapter lifetime.
 * @param onSelect Exact visible identity callback; no source mutation occurs.
 * @param onUnavailable Fixed diagnostic sink for unavailable rendering.
 * @param factory Trusted public SDK collaborator, never source-controlled input.
 * @returns Disposable narrow canvas adapter with existing synchronous semantics.
 * @throws {Error} For an invalid host or preparation lifecycle.
 */
export function createCanvas(container: HTMLElement, onSelect: (id: string | null) => void, onUnavailable?: (message: string) => void, factory: CanvasRendererFactory = createSigmaRenderer): GraphCanvas {
  return prepareCanvas(container, onSelect, onUnavailable, factory).initialize();
}
