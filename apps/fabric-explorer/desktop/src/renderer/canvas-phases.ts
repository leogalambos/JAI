// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Cancellable DOM/layout, SDK construction and graph-publication task ownership. */
import type { GraphProjection } from '@jai/fabric-explorer-contracts';
import type { LayoutResult } from '../layout/types.js';
import type { CanvasPreparation, GraphCanvas } from './canvas/index.js';
import type { CanvasPalette } from './canvas/palette.js';
import { CanvasView } from './canvas-view.js';
/** Schedule one later browser task and return its idempotent cancellation. */
export type CanvasTaskScheduler = (run: () => void) => () => void;
/** Exact publication token; numeric layout readiness alone is insufficient. */
export interface CanvasCommit { readonly projection: GraphProjection; readonly layout: LayoutResult }
interface Desired extends CanvasCommit { readonly handles: readonly number[]; readonly selected: string | null }
/** A MessageChannel delivers real tasks without a deadline, animation callback or retry loop. */
export const scheduleCanvasTask: CanvasTaskScheduler = run => {
  const channel = new MessageChannel(); let active = true;
  const cancel = () => { if (!active) return; active = false; channel.port1.close(); channel.port2.close(); };
  channel.port1.onmessage = () => { if (!active) return; cancel(); run(); }; channel.port2.postMessage(null); return cancel;
};
/** Production owner composing the synchronous publication adapter after observed browser layout. */
export class PhasedCanvasView {
  private preparation: CanvasPreparation | null = null;
  private adapter: GraphCanvas | null = null;
  private current: CanvasView | null = null;
  private desired: Desired | null = null;
  private palette: CanvasPalette | null = null;
  private stopSize: (() => void) | null = null;
  private cancelInitialization: (() => void) | null = null;
  private cancelPublication: (() => void) | null = null;
  private epoch = 0;
  private initializationSequence = 0;
  private publicationSequence = 0;
  private binding: { readonly sessionId: string; readonly generation: string } | null = null;
  private appliedPalette: CanvasPalette | null = null;
  private failed = false;
  private disposed = false;
  /** Bind trusted preparation, diagnostic, scheduler and exact-commit observers for this host only. */
  constructor(private readonly prepare: (unavailable: (message: string) => void) => CanvasPreparation,
    private readonly report: (message: string) => void, private readonly schedule: CanvasTaskScheduler = scheduleCanvasTask,
    private readonly committed: (commit: CanvasCommit | null) => void = () => {}) {}
  /** Retain the latest theme during preparation; apply live updates without replacing geometry. */
  setPalette(palette: CanvasPalette): void {
    this.palette = palette;
    if (this.current && !this.failed && !this.disposed) { this.current.setPalette(palette); this.appliedPalette = palette; }
  }
  /** Coalesce exact desired publication; null closes the lifetime and invalidates queued work. */
  sync(projection: GraphProjection | null, layout: LayoutResult | null, handles: readonly number[], selected: string | null): void {
    if (this.disposed) return;
    if (!projection) { this.release(); this.failed = false; return; }
    const previous = this.binding;
    if (previous && (previous.sessionId !== projection.snapshot.sessionId || previous.generation !== projection.snapshot.generation)) { this.release(); this.failed = false; }
    this.binding = projection.snapshot; this.committed(null);
    if (!layout || layout.binding.sessionId !== projection.snapshot.sessionId || layout.binding.generation !== projection.snapshot.generation) {
      this.desired = null; this.cancelInitialization?.(); this.cancelInitialization = null; this.cancelPublication?.(); this.cancelPublication = null; return;
    }
    this.desired = { projection, layout, handles, selected };
    if (this.failed) return;
    if (this.adapter) { this.queuePublication(); return; }
    if (this.preparation) { this.queueInitialization(); return; }
    const epoch = this.epoch;
    try {
      const prepared = this.prepare(message => this.fail(epoch, message));
      if (epoch !== this.epoch || this.failed || this.disposed) { prepared.dispose(); return; }
      this.preparation = prepared;
      this.stopSize = prepared.observe(() => this.queueInitialization());
      this.queueInitialization();
    } catch { this.fail(epoch); }
  }
  /** Forward camera input only after the exact latest graph/layout has committed. */
  action(action: 'fit' | 'zoom' | 'focus', value?: number | string): boolean {
    return !this.cancelPublication && !!this.desired && !this.failed && !this.disposed && !!this.current?.ready && this.current.action(action, value);
  }
  private queueInitialization(): void {
    if (!this.desired || !this.preparation?.measurable() || this.adapter || this.cancelInitialization || this.failed || this.disposed) return;
    const epoch = this.epoch; const sequence = ++this.initializationSequence;
    this.cancelInitialization = this.schedule(() => {
      if (epoch !== this.epoch || sequence !== this.initializationSequence) return;
      this.cancelInitialization = null;
      if (epoch !== this.epoch || !this.desired || !this.preparation?.measurable() || this.failed || this.disposed) return;
      try {
        const initialPalette = this.palette;
        const adapter = this.preparation.initializeWhenMeasurable(initialPalette ?? undefined);
        if (!adapter) return;
        if (epoch !== this.epoch || this.failed || this.disposed) return;
        this.adapter = adapter; this.appliedPalette = initialPalette; this.stopSize?.(); this.stopSize = null; this.queuePublication();
      } catch { this.fail(epoch); }
    });
  }
  private queuePublication(): void {
    if (!this.desired || !this.adapter || this.cancelPublication || this.failed || this.disposed) return;
    const epoch = this.epoch; const sequence = ++this.publicationSequence;
    this.cancelPublication = this.schedule(() => {
      if (epoch !== this.epoch || sequence !== this.publicationSequence) return;
      this.cancelPublication = null;
      if (epoch !== this.epoch || !this.desired || !this.adapter || this.failed || this.disposed) return;
      const desired = this.desired;
      try {
        if (this.palette && this.palette !== this.appliedPalette) { this.adapter.setPalette(this.palette); this.appliedPalette = this.palette; }
      } catch { this.fail(epoch); return; }
      this.current ??= new CanvasView(() => this.adapter!, message => this.fail(epoch, message));
      this.current.sync(desired.projection, desired.layout, desired.handles, desired.selected);
      if (epoch === this.epoch && this.current?.ready && this.desired === desired) this.committed({ projection: desired.projection, layout: desired.layout });
    });
  }
  private fail(epoch: number, message = 'Graph rendering is unavailable. Use search, findings and the visible elements list.'): void {
    if (epoch !== this.epoch || this.failed || this.disposed) return;
    this.failed = true; this.release(); this.report(message);
  }
  private release(): void {
    this.epoch++; this.cancelInitialization?.(); this.cancelInitialization = null; this.cancelPublication?.(); this.cancelPublication = null;
    this.stopSize?.(); this.stopSize = null;
    const current = this.current, adapter = this.adapter, preparation = this.preparation;
    this.current = null; this.adapter = null; this.preparation = null; this.desired = null; this.binding = null; this.appliedPalette = null; this.committed(null);
    if (current) current.dispose(); else adapter?.dispose(); preparation?.dispose();
  }
  /** Permanently release this mounted owner; a remount receives a new owner and epoch. */
  dispose(): void { if (this.disposed) return; this.disposed = true; this.release(); }
}
