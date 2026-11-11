// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Native activity preparation over actual production readiness and OS observations. */
/** Existing bounded overview observer and real enabled-control click. */
export interface PerformanceCameraPort {
  /** Await the current visible graph commit within the existing diagnostic window. */
  waitForOverview(): Promise<void>;
  /** Click the actual enabled Fit control; reject absent or disabled controls. */
  clickFit(): Promise<void>;
}
/** Trusted native window adapter; focus requests are not evidence of focus. */
export interface PerformanceFocusPort {
  /** Make one native focus request before measurement. */
  requestFocus(): void;
  /** Await actual focus within the existing diagnostic window, rejecting expiry. */
  waitForFocus(): Promise<void>;
  /** Read the actual native window focus immediately before measurement. */
  isFocused(): boolean;
}
/**
 * Fit only after the current projection has visibly committed.
 * @param port Actual overview observation and camera control, with their existing deadlines.
 * @returns Completion of the enabled Fit action; propagates readiness or click failure.
 */
export async function fitCommittedOverview(port: PerformanceCameraPort): Promise<void> {
  await port.waitForOverview();
  await port.clickFit();
}
/**
 * Request foreground once and verify the independently observed native state.
 * @param port Actual native focus request and bounded OS/renderer observation.
 * @returns Successful foreground preparation; throws on refusal, expiry or lost focus.
 */
export async function prepareNativeFocus(port: PerformanceFocusPort): Promise<void> {
  port.requestFocus();
  await port.waitForFocus();
  if (!port.isFocused()) throw new Error('Native input requires the actual test window in foreground.');
}

/** Held native motion adapter; each move result describes an actual trusted receipt before the fixed measurement end. */
export interface PerformanceDragPort {
  /** Send the one-based move once, then await its actual trusted held receipt; false means the observation ended. */
  move(index: number): Promise<boolean>;
  /** Release the held pointer even on incomplete input or failed observation. */
  release(): void;
}
/**
 * Submit eight held moves without letting the native queue collapse the whole gesture into one burst.
 * @param port Native move/receipt boundary and mandatory pointer release.
 * @returns True only after eight received moves; false preserves incomplete input, and errors propagate after release.
 */
export async function performObservedDrag(port: PerformanceDragPort): Promise<boolean> {
  try {
    for (let index = 1; index <= 8; index++) if (!await port.move(index)) return false;
    return true;
  } finally { port.release(); }
}
