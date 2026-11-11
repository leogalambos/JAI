// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Development-only finite canvas gestures; no production settings or SDK internals are changed. */
import { resolveSettings } from 'sigma/settings';
const settings = resolveSettings({});
/** CSS-pixel input position relative to the actual SDK stage. */
export interface CanvasInputPoint { readonly x: number; readonly y: number }
/** Owned input boundary implemented by actual browser events or controlled SDK contract tests. */
export interface CanvasInputPort {
  /** Dispatch one actual input event at a stage-relative position, preserving document propagation. */
  dispatch(type: string, point: CanvasInputPoint, buttons: number): void;
  /** Wait the declared input-classification boundary, then paint; controlled clocks implement this in unit tests. */
  settle(milliseconds: number): Promise<void>;
  /** Cancel only camera animation after a completed native drag through the public camera API. */
  stopCameraAnimation(): void;
}
/**
 * Send one independent single-click gesture through the owned browser input boundary.
 * @param port Actual browser dispatch or controlled actual-SDK test boundary.
 * @param point Stage-relative CSS pixels.
 * @returns Completion after input dispatch and its explicit finite classification fence.
 */
export async function canvasSingleClick(port: CanvasInputPort, point: CanvasInputPoint): Promise<void> {
  port.dispatch('pointermove', point, 0); port.dispatch('pointerdown', point, 1); port.dispatch('pointerup', point, 0);
  // Consecutive checks are independent single clicks, not the SDK's double-click zoom gesture.
  await port.settle(settings.doubleClickTimeout);
}
/**
 * Send one stage pan gesture without changing source graph positions.
 * @param port Actual browser dispatch or controlled actual-SDK test boundary.
 * @param from Stage-relative start position in CSS pixels.
 * @param to Stage-relative final position in CSS pixels.
 * @returns Completion after pointer release, public camera cancellation and a finite input fence.
 */
export async function canvasDrag(port: CanvasInputPort, from: CanvasInputPoint, to: CanvasInputPoint): Promise<void> {
  port.dispatch('pointermove', from, 0); port.dispatch('pointerdown', from, 1);
  const moves = settings.draggedEventsTolerance + 1;
  for (let index = 1; index <= moves; index++) port.dispatch('pointermove', { x: from.x + (to.x - from.x) * index / moves, y: from.y + (to.y - from.y) * index / moves }, 1);
  port.dispatch('pointerup', to, 0); port.stopCameraAnimation(); await port.settle(settings.doubleClickTimeout);
}
