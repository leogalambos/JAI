/** Deterministic phase tests: no timer sleeps, GPU, or source access. */
import { expect, it, vi } from 'vitest';
import { PhasedCanvasView, scheduleCanvasTask } from '../src/renderer/canvas-phases.js';
import type { GraphProjection } from '@jai/fabric-explorer-contracts';
import type { LayoutResult } from '../src/layout/types.js';
import type { GraphCanvas } from '../src/renderer/canvas/index.js';
import type { CanvasPalette } from '../src/renderer/canvas/palette.js';
import { DEFAULT_CANVAS_PALETTE } from '../src/renderer/canvas/palette.js';
const projection = { snapshot: { sessionId: 's', generation: '1' }, vertices: [{ id: 'v' }], edges: [] } as unknown as GraphProjection;
const layout = { binding: projection.snapshot } as unknown as LayoutResult;
function fixture() {
  const tasks: { run: () => void; cancelled: boolean }[] = [];
  const schedule = (run: () => void) => { const task = { run, cancelled: false }; tasks.push(task); return () => { task.cancelled = true; }; };
  let size: (() => void) | null = null; let positive = false; let fail: (message: string) => void = () => {};
  const adapter: GraphCanvas = { replace: vi.fn(), select: vi.fn(), setPalette: vi.fn(), fit: vi.fn(), zoom: vi.fn(), focus: vi.fn(), dispose: vi.fn() };
  const initialize = vi.fn((_palette?: CanvasPalette) => adapter);
  const prepared = { observe: vi.fn((listener: () => void) => { size = listener; return vi.fn(); }), measurable: () => positive, initialize, initializeWhenMeasurable: initialize, dispose: vi.fn() };
  const factory = vi.fn((report: (message: string) => void) => { fail = report; return prepared; });
  const committed = vi.fn(); const report = vi.fn(); const view = new PhasedCanvasView(factory, report, schedule, committed);
  return { view, tasks, adapter, prepared, committed, report, factory, fail: (message = 'unavailable') => fail(message), size: (value: boolean) => { positive = value; size?.(); }, next: () => { const task = tasks.shift(); if (task && !task.cancelled) task.run(); } };
}
it('waits for positive observed size, then separates construction from latest graph publication', () => {
  const f = fixture(); f.view.sync(projection, layout, [1], null);
  expect(f.prepared.initialize).not.toHaveBeenCalled(); expect(f.adapter.replace).not.toHaveBeenCalled();
  f.size(false); expect(f.tasks).toHaveLength(0); f.size(true); expect(f.tasks).toHaveLength(1);
  f.next(); expect(f.prepared.initialize).toHaveBeenCalledOnce(); expect(f.adapter.replace).not.toHaveBeenCalled(); expect(f.tasks).toHaveLength(1);
  f.view.sync(projection, layout, [1], 'v'); f.next(); expect(f.adapter.replace).toHaveBeenCalledOnce(); expect(f.adapter.select).toHaveBeenLastCalledWith('v');
  expect(f.committed).toHaveBeenLastCalledWith({ projection, layout });
});
it('does not prewarm before valid projection/layout and cancels pending construction on close', () => {
  const f = fixture(); f.view.sync(null, null, [], null); f.view.sync(projection, null, [1], null); expect(f.factory).not.toHaveBeenCalled();
  f.view.sync(projection, layout, [1], null); f.size(true); f.view.sync(null, null, [], null); f.next();
  expect(f.prepared.initialize).not.toHaveBeenCalled(); expect(f.prepared.dispose).toHaveBeenCalledOnce();
});
it('invalidates queued publication and exact ownership on disposal', () => {
  const f = fixture(); f.view.sync(projection, layout, [1], null); f.size(true); f.next(); f.view.dispose(); f.next(); f.view.dispose();
  expect(f.adapter.replace).not.toHaveBeenCalled(); expect(f.adapter.dispose).toHaveBeenCalledOnce(); expect(f.prepared.dispose).toHaveBeenCalledOnce();
});
it('coalesces latest projection, layout, selection and palette before publication', () => {
  const f = fixture(); f.view.setPalette(DEFAULT_CANVAS_PALETTE); f.view.sync(projection, layout, [1], null); f.size(true);
  const next = { ...projection, vertices: [{ id: 'new' }] } as unknown as GraphProjection; const nextLayout = { ...layout };
  const palette = { ...DEFAULT_CANVAS_PALETTE, background: '#123456' }; f.view.setPalette(palette); f.view.sync(next, nextLayout, [2], 'new');
  f.next(); expect(f.prepared.initialize).toHaveBeenCalledWith(palette); f.next(); expect(f.adapter.replace).toHaveBeenCalledWith(next, nextLayout, [2]); expect(f.adapter.select).toHaveBeenLastCalledWith('new');
});
it('does not initialize after a positive observation becomes zero before its task; resumes without polling', () => {
  const f = fixture(); f.view.sync(projection, layout, [1], null); f.size(true); f.size(false); f.next(); expect(f.prepared.initialize).not.toHaveBeenCalled();
  f.size(true); f.next(); expect(f.prepared.initialize).toHaveBeenCalledOnce(); f.next(); expect(f.adapter.replace).toHaveBeenCalledOnce();
});
it('ignores a stale cancelled callback after a new generation has its own scheduled work', () => {
  const f = fixture(); f.view.sync(projection, layout, [1], null); f.size(true); const stale = f.tasks[0]!;
  const next = { ...projection, snapshot: { ...projection.snapshot, generation: '2' } } as GraphProjection;
  f.view.sync(next, { ...layout, binding: { ...layout.binding, generation: '2' } }, [1], null);
  stale.run(); expect(f.prepared.initialize).not.toHaveBeenCalled(); f.next(); f.next(); expect(f.prepared.initialize).toHaveBeenCalledOnce();
});
it('applies a theme change between construction and publication and disables camera commands until commit', () => {
  const f = fixture(); f.view.sync(projection, layout, [1], null); f.size(true); expect(f.view.action('fit')).toBe(false); f.next(); expect(f.view.action('fit')).toBe(false);
  const palette = { ...DEFAULT_CANVAS_PALETTE, background: '#123456' }; f.view.setPalette(palette); f.next();
  expect(f.adapter.setPalette).toHaveBeenCalledWith(palette); expect(f.view.action('fit')).toBe(true);
});
it('contains construction throws and late availability failure with exactly one owned release', () => {
  const f = fixture(); f.prepared.initialize.mockImplementation(() => { throw new Error('SDK failed'); });
  f.view.sync(projection, layout, [1], null); f.size(true); f.next(); expect(f.report).toHaveBeenCalledOnce(); expect(f.prepared.dispose).toHaveBeenCalledOnce(); expect(f.adapter.replace).not.toHaveBeenCalled();
  const late = fixture(); late.view.sync(projection, layout, [1], null); late.size(true); late.next(); late.next(); late.fail(); late.view.dispose();
  expect(late.report).toHaveBeenCalledOnce(); expect(late.adapter.dispose).toHaveBeenCalledOnce(); expect(late.prepared.dispose).toHaveBeenCalledOnce(); expect(late.view.action('fit')).toBe(false);
});
it('contains synchronous failure during preparation and initialization without leaking returned ownership', () => {
  const preparing = fixture(); preparing.factory.mockImplementation(report => { report('unavailable'); return preparing.prepared; });
  preparing.view.sync(projection, layout, [1], null); expect(preparing.prepared.dispose).toHaveBeenCalledOnce(); expect(preparing.tasks).toHaveLength(0);
  const initializing = fixture(); initializing.prepared.initialize.mockImplementation(() => {
    initializing.prepared.dispose.mockImplementation(() => initializing.adapter.dispose()); initializing.fail(); return initializing.adapter;
  });
  initializing.view.sync(projection, layout, [1], null); initializing.size(true); initializing.next();
  expect(initializing.prepared.dispose).toHaveBeenCalledOnce(); expect(initializing.adapter.dispose).toHaveBeenCalledOnce(); expect(initializing.adapter.replace).not.toHaveBeenCalled();
});
it('reopens after close with fresh preparation and ignores old availability callbacks', () => {
  const f = fixture(); f.view.sync(projection, layout, [1], null); const oldFailure = f.factory.mock.calls[0]![0];
  f.view.sync(null, null, [], null); f.view.sync(projection, layout, [1], 'v'); oldFailure('old failure');
  expect(f.report).not.toHaveBeenCalled(); expect(f.factory).toHaveBeenCalledTimes(2); f.size(true); f.next(); f.next(); expect(f.adapter.select).toHaveBeenLastCalledWith('v');
});
it('withholds commit for a pending or stale layout and cancels an already queued publication', () => {
  const f = fixture(); f.view.sync(projection, layout, [1], null); f.size(true); f.next();
  f.view.sync(projection, null, [1], null); f.next(); expect(f.adapter.replace).not.toHaveBeenCalled(); expect(f.view.action('fit')).toBe(false);
  f.view.sync(projection, { ...layout, binding: { ...layout.binding, generation: 'stale' } }, [1], null); expect(f.tasks).toHaveLength(0);
  f.view.sync(projection, layout, [1], 'v'); f.next(); expect(f.adapter.replace).toHaveBeenCalledOnce(); expect(f.committed).toHaveBeenLastCalledWith({ projection, layout });
});
it('ignores a cancelled same-generation publication after a newer publication is queued', () => {
  const f = fixture(); f.view.sync(projection, layout, [1], null); f.size(true); f.next(); const stale = f.tasks[0]!;
  f.view.sync(projection, null, [1], null); f.view.sync(projection, layout, [1], 'v'); stale.run();
  expect(f.adapter.replace).not.toHaveBeenCalled(); f.next(); f.next(); expect(f.adapter.replace).toHaveBeenCalledOnce(); expect(f.adapter.select).toHaveBeenLastCalledWith('v');
});
it('uses a new mounted owner after permanent disposal', () => {
  const f = fixture(); f.view.dispose(); f.view.sync(projection, layout, [1], null); expect(f.factory).not.toHaveBeenCalled();
  const remount = fixture(); remount.view.sync(projection, layout, [1], null); remount.size(true); remount.next(); remount.next(); expect(remount.adapter.replace).toHaveBeenCalledOnce();
});

it('owns and closes both message ports for deferred execution and cancellation', () => {
  const channels: { port1: { onmessage: (() => void) | null; close: ReturnType<typeof vi.fn> }; port2: { postMessage: ReturnType<typeof vi.fn>; close: ReturnType<typeof vi.fn> } }[] = [];
  vi.stubGlobal('MessageChannel', class {
    port1 = { onmessage: null as (() => void) | null, close: vi.fn() };
    port2 = { postMessage: vi.fn(), close: vi.fn() };
    constructor() { channels.push(this); }
  });
  try {
    const run = vi.fn(); scheduleCanvasTask(run); expect(run).not.toHaveBeenCalled();
    channels[0]!.port1.onmessage!(); expect(run).toHaveBeenCalledOnce();
    for (const port of [channels[0]!.port1, channels[0]!.port2]) expect(port.close).toHaveBeenCalledOnce();
    const cancel = scheduleCanvasTask(run); cancel(); cancel(); channels[1]!.port1.onmessage!(); expect(run).toHaveBeenCalledOnce();
    for (const port of [channels[1]!.port1, channels[1]!.port2]) expect(port.close).toHaveBeenCalledOnce();
  } finally { vi.unstubAllGlobals(); }
});
