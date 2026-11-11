// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Actual public Sigma captor contract with owned event targets and controlled timing; no GPU claim. */
import { afterEach, expect, it, vi } from 'vitest';
vi.hoisted(() => { Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }); Object.defineProperty(globalThis, 'PointerEvent', { configurable: true, value: class PointerEvent {} }); });
import { MouseCaptor } from 'sigma';
import { resolveSettings } from 'sigma/settings';
import { canvasSingleClick, canvasDrag } from './canvas-input.js';
import type { CanvasInputPort, CanvasInputPoint } from './canvas-input.js';
class InputTarget {
  readonly listeners = new Map<string, EventListener[]>();
  addEventListener(type: string, listener: EventListener) { const list = this.listeners.get(type) ?? []; list.push(listener); this.listeners.set(type, list); }
  removeEventListener(type: string, listener: EventListener) { this.listeners.set(type, (this.listeners.get(type) ?? []).filter(value => value !== listener)); }
  getBoundingClientRect() { return { left: 10, top: 20, width: 400, height: 300 }; }
  dispatch(type: string, point: CanvasInputPoint, buttons: number, document: InputTarget) {
    const event = { type, pointerType: 'mouse', pointerId: 1, isPrimary: true, button: 0, buttons, clientX: point.x + 10, clientY: point.y + 20, target: this, composedPath: () => [this, document], preventDefault() {}, stopPropagation() {} } as unknown as Event;
    for (const listener of this.listeners.get(type) ?? []) listener(event);
    for (const listener of document.listeners.get(type) ?? []) listener(event);
  }
}
const captors: MouseCaptor[] = [];
afterEach(() => { for (const captor of captors.splice(0)) captor.kill(); vi.useRealTimers(); vi.unstubAllGlobals(); });
function fixture() {
  vi.useFakeTimers({ now: 1000 });
  const document = new InputTarget(); vi.stubGlobal('document', document); const target = new InputTarget(); const settings = resolveSettings({});
  let animations = 0; let clicks = 0; let doubles = 0; let dragMoves = 0; let coordinate: readonly number[] = [];
  const state = { x: 0.5, y: 0.5, ratio: 1, angle: 0 };
  const renderer = { getCamera: () => ({ getState: () => state, getPreviousState: () => state, setState() {}, getBoundedRatio: (ratio: number) => ratio, animate: () => { animations++; } }), getSetting: () => false, getViewportZoomedState: (_point: unknown, ratio: number) => ({ ...state, ratio }) };
  const captor = new MouseCaptor(target as unknown as HTMLElement, renderer as never); captors.push(captor);
  captor.on('click', event => { clicks++; coordinate = [event.x, event.y]; }); captor.on('doubleClick', () => { doubles++; });
  // Classification is isolated from camera implementation through its public cancellation event.
  captor.on('mousemovebody', event => { if ('buttons' in event.original && event.original.buttons === 1) dragMoves++; event.preventSigmaDefault(); });
  const waits: number[] = []; let stopped = 0;
  const port: CanvasInputPort = { dispatch: (type, point, buttons) => target.dispatch(type, point, buttons, document), settle: async milliseconds => { waits.push(milliseconds); await vi.advanceTimersByTimeAsync(milliseconds); }, stopCameraAnimation: () => { stopped++; } };
  return { port, captor, target, document, settings, waits, counts: () => ({ clicks, doubles, animations, stopped, coordinate, dragMoves }) };
}
it('delivers independent ordinary clicks to the actual pinned pointer captor at exact local coordinates', async () => {
  const f = fixture(); await canvasSingleClick(f.port, { x: 17, y: 23 }); expect(f.counts()).toMatchObject({ clicks: 1, doubles: 0, animations: 0, coordinate: [17, 23] });
  await canvasSingleClick(f.port, { x: 34, y: 45 }); expect(f.counts()).toMatchObject({ clicks: 2, doubles: 0, animations: 0, coordinate: [34, 45] });
  expect(f.waits).toEqual([f.settings.doubleClickTimeout, f.settings.doubleClickTimeout]);
  f.captor.kill(); expect([...f.target.listeners.values(), ...f.document.listeners.values()].flat()).toHaveLength(0);
});
it('crosses the actual drag classification threshold and stops camera inertia without generating a click', async () => {
  const f = fixture(); await canvasDrag(f.port, { x: 100, y: 100 }, { x: 160, y: 140 });
  expect(f.counts()).toMatchObject({ clicks: 0, doubles: 0, stopped: 1 }); expect(f.counts().dragMoves).toBeGreaterThan(f.settings.draggedEventsTolerance);
});
it('demonstrates rapid gestures are doubles until the controlled public clock boundary expires', async () => {
  const f = fixture(); const point = { x: 17, y: 23 };
  for (let i = 0; i < 2; i++) { f.port.dispatch('pointerdown', point, 1); f.port.dispatch('pointerup', point, 0); }
  expect(f.counts()).toMatchObject({ clicks: 1, doubles: 1, animations: 1 });
  await vi.advanceTimersByTimeAsync(f.settings.doubleClickTimeout);
  f.port.dispatch('pointerdown', point, 1); f.port.dispatch('pointerup', point, 0); expect(f.counts()).toMatchObject({ clicks: 2, doubles: 1, animations: 1 });
});

it('retains the actual SDK one-move counterexample rather than treating it as a completed drag', () => {
  const f = fixture(); f.port.dispatch('pointerdown', { x: 100, y: 100 }, 1); f.port.dispatch('pointermove', { x: 160, y: 140 }, 1); f.port.dispatch('pointerup', { x: 160, y: 140 }, 0);
  expect(f.counts()).toMatchObject({ clicks: 1, dragMoves: 1 });
});
