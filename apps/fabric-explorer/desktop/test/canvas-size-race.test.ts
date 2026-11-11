/** Actual preparation/phase-owner regression with independently controlled live and observed geometry. */
import { expect, it, vi } from 'vitest';
vi.hoisted(() => Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }));
import { prepareCanvas } from '../src/renderer/canvas/index.js';
import { PhasedCanvasView } from '../src/renderer/canvas-phases.js';
import type { CanvasRenderer } from '../src/renderer/canvas/sdk.js';
import type { GraphProjection } from '@jai/fabric-explorer-contracts';
import type { LayoutResult } from '../src/layout/types.js';
import golden from '../../packages/contracts/test/fixtures/projection.json' with { type: 'json' };
it.each(['resume', 'close', 'generation'] as const)('retains or cancels a live-zero deferral without stale work (%s)', mode => {
  let width = 320; const tasks: (() => void)[] = [];
  const observations: { callback: ResizeObserverCallback; target?: Element; disconnect: () => void }[] = [];
  const document = { defaultView: { devicePixelRatio: 1 }, createElement: () => new Element() };
  class Element {
    ownerDocument = document; style = {}; children: Element[] = [];
    append(...children: Element[]) { this.children.push(...children); } setAttribute() {} remove() {} getContext() { return null; }
    get clientWidth() { return width; } get clientHeight() { return 200; }
  }
  vi.stubGlobal('ResizeObserver', class {
    private entry: typeof observations[number];
    constructor(callback: ResizeObserverCallback) { this.entry = { callback, disconnect: vi.fn() }; observations.push(this.entry); }
    observe(target: Element) { this.entry.target = target; } disconnect() { this.entry.disconnect(); }
  });
  const renderer: CanvasRenderer = { on: vi.fn(), off: vi.fn(), refresh: vi.fn(), resize: vi.fn(), dimensions: () => ({ width, height: 200 }), project: point => point, normalize: point => point, camera: () => ({ x: .5, y: .5, ratio: 1, angle: 0 }), move: vi.fn(), nodeData: () => undefined, edgeData: () => undefined, scaleSize: size => size, kill: vi.fn() };
  const factory = vi.fn(() => renderer); const report = vi.fn(); const commit = vi.fn();
  const view = new PhasedCanvasView(unavailable => prepareCanvas(new Element() as unknown as HTMLElement, () => {}, unavailable, factory), report,
    run => { let active = true; tasks.push(() => { if (active) run(); }); return () => { active = false; }; }, commit);
  const projection = golden as GraphProjection; const handles = projection.vertices.map((_, index) => index);
  const layout: LayoutResult = { binding: { sessionId: projection.snapshot.sessionId, generation: projection.snapshot.generation, capability: 'c', requestId: 'r', projectionId: 'p' }, algorithm: 'layered', positions: handles.map(handle => ({ handle, x: handle * 48, y: 0 })), groups: [], work: 1, iterations: 1, complete: true };
  const notify = (index = 0) => { const observation = observations[index]!; observation.callback([{ target: observation.target, contentRect: { width, height: 200 } }] as unknown as ResizeObserverEntry[], {} as ResizeObserver); };
  try {
    view.sync(projection, layout, handles, null); notify(); expect(tasks).toHaveLength(1);
    width = 0; tasks.shift()!();
    expect(factory).not.toHaveBeenCalled(); expect(report).not.toHaveBeenCalled(); expect(observations[0]!.disconnect).not.toHaveBeenCalled();
    expect(view.action('fit')).toBe(false); expect(tasks).toHaveLength(0);
    if (mode === 'close') {
      view.sync(null, null, [], null); width = 320; notify();
      expect(tasks).toHaveLength(0); expect(factory).not.toHaveBeenCalled(); expect(report).not.toHaveBeenCalled();
      expect(observations[0]!.disconnect).toHaveBeenCalledOnce(); return;
    }
    if (mode === 'generation') {
      const next = { ...projection, snapshot: { ...projection.snapshot, generation: '2' } };
      const nextLayout = { ...layout, binding: { ...layout.binding, generation: '2' } };
      view.sync(next, nextLayout, handles, null); width = 320; notify(); expect(tasks).toHaveLength(0);
      notify(1); expect(tasks).toHaveLength(1); tasks.shift()!(); expect(factory).toHaveBeenCalledOnce();
      tasks.shift()!(); expect(commit).toHaveBeenLastCalledWith({ projection: next, layout: nextLayout });
      view.dispose(); expect(renderer.kill).toHaveBeenCalledOnce(); expect(report).not.toHaveBeenCalled();
      expect(observations[0]!.disconnect).toHaveBeenCalledOnce(); expect(observations[1]!.disconnect).toHaveBeenCalledOnce(); return;
    }
    width = 320; notify(); expect(tasks).toHaveLength(1); tasks.shift()!(); expect(factory).toHaveBeenCalledOnce();
    expect(tasks).toHaveLength(1); tasks.shift()!(); expect(commit).toHaveBeenLastCalledWith({ projection, layout }); expect(view.action('fit')).toBe(true);
    view.dispose(); expect(renderer.kill).toHaveBeenCalledOnce(); expect(observations[0]!.disconnect).toHaveBeenCalledOnce();
  } finally { view.dispose(); vi.unstubAllGlobals(); }
});
