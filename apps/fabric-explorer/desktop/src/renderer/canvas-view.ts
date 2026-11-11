// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** React-independent canvas publication owner; no semantic query or source mutation occurs here. */
import type { GraphProjection } from '@jai/fabric-explorer-contracts';
import type { LayoutResult } from '../layout/types.js';
import type { GraphCanvas } from './canvas/index.js';
import type { CanvasPalette } from './canvas/palette.js';
/** Trusted canvas construction callback; fallback reports renderer availability only. */
export interface CanvasFactory {
  (unavailable: (message: string) => void): GraphCanvas;
}
/** One owned canvas lifetime for a mounted application graph host. */
export class CanvasView {
  private canvas: GraphCanvas | null = null;
  private projection: GraphProjection | null = null;
  private layout: LayoutResult | null = null;
  private visible = new Set<string>();
  private failed = false;
  private palette: CanvasPalette | null = null;
  /**
   * Bind an owned canvas factory and fixed presentation diagnostic sink.
   * @param factory Creates an adapter only for this mounted host.
   * @param report Displays a safe fixed renderer failure message.
   */
  constructor(private readonly factory: CanvasFactory, private readonly report: (message: string) => void) {}
  /**
   * Publish trusted theme colours without replacing graph or camera ownership.
   * @param palette Resolved application palette, retained across lazy construction and remount.
   * @returns Nothing; an adapter failure preserves the semantic alternative.
   */
  setPalette(palette: CanvasPalette): void {
    this.palette = palette;
    if (!this.canvas || this.failed) return;
    try { this.canvas.setPalette(palette); }
    catch { this.failed = true; this.release(); this.report('Graph rendering is unavailable. Use search, findings and the visible elements list.'); }
  }
  /**
   * Publish a current bounded graph and selection to the display adapter.
   * @param projection Current projection or null after close/generation reset.
   * @param layout Current numeric layout, null while the worker is pending.
   * @param handles Exact current vertex-handle ordering.
   * @param selected Exact inspector selection, possibly outside this projection.
   * @returns Nothing; source records remain immutable.
   */
  sync(projection: GraphProjection | null, layout: LayoutResult | null, handles: readonly number[], selected: string | null): void {
    if (!projection) { this.dispose(); return; }
    if (!layout) { this.visible.clear(); return; }
    if (this.failed) return;
    try {
      if (!this.canvas) {
        let constructing = true;
        const created = this.factory(message => { this.failed = true; this.report(message); if (!constructing) this.release(); });
        constructing = false;
        if (this.failed) { created.dispose(); return; }
        this.canvas = created;
        if (this.palette) this.canvas.setPalette(this.palette);
      }
      if (this.projection !== projection || this.layout !== layout) {
        this.canvas.replace(projection, layout, handles);
        this.projection = projection; this.layout = layout;
        this.visible = new Set([...projection.vertices, ...projection.edges].map(item => item.id));
      }
      this.canvas.select(selected && this.visible.has(selected) ? selected : null);
    } catch { this.failed = true; this.release(); this.report('Graph rendering is unavailable. Use search, findings and the visible elements list.'); }
  }
  /** Whether a real graph/layout has committed successfully to this adapter. */
  get ready(): boolean { return !!this.canvas && !!this.projection && !!this.layout && !this.failed; }
  /**
   * Apply an explicit camera action without changing semantic selection.
   * @param action Fixed fit/zoom/focus command, never a source-controlled method.
   * @param value Finite zoom factor or exact focused ID, according to action.
   * @returns Whether a canvas action was applied.
   */
  action(action: 'fit' | 'zoom' | 'focus', value?: number | string): boolean {
    if (!this.canvas || this.failed || action === 'focus' && (typeof value !== 'string' || !this.visible.has(value))) return false;
    try { if (action === 'fit') this.canvas.fit(); else if (action === 'zoom') this.canvas.zoom(value as number); else this.canvas.focus(value as string); return true; }
    catch { this.failed = true; this.release(); this.report('Graph camera is unavailable. Use the visible elements list.'); return false; }
  }
  private release(): void { this.canvas?.dispose(); this.canvas = null; this.projection = null; this.layout = null; this.visible.clear(); }
  /** Release this host's adapter; repeated disposal is safe. */
  dispose(): void { this.release(); this.failed = false; }
}
