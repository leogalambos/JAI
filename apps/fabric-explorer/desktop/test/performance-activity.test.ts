// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Controlled activity ordering; no native window or wall-clock sleeps. */
import { expect, it, vi } from 'vitest';
import { fitCommittedOverview, prepareNativeFocus, performObservedDrag } from './performance-activity.js';

it('withholds camera input while an inspector has completed but graph publication is pending', async () => {
  let publish: () => void = () => {}; let committed = false;
  const ready = new Promise<void>(resolve => { publish = () => { committed = true; resolve(); }; });
  const click = vi.fn(async () => { if (!committed) throw new Error('Required enabled control unavailable: #fit-graph'); });
  const operation = fitCommittedOverview({ waitForOverview: () => ready, clickFit: click });
  await Promise.resolve(); expect(click).not.toHaveBeenCalled();
  publish(); await operation; expect(click).toHaveBeenCalledOnce();
});

it('does not click when the existing overview diagnostic deadline expires', async () => {
  const click = vi.fn();
  await expect(fitCommittedOverview({ waitForOverview: async () => { throw new Error('Overview deadline'); }, clickFit: click })).rejects.toThrow('Overview deadline');
  expect(click).not.toHaveBeenCalled();
});

it('requests native focus once before awaiting independently observed focus', async () => {
  let focused = false; let observed: () => void = () => {};
  const ready = new Promise<void>(resolve => { observed = () => { focused = true; resolve(); }; });
  const focus = vi.fn();
  const operation = prepareNativeFocus({ requestFocus: focus, waitForFocus: () => ready, isFocused: () => focused });
  expect(focus).toHaveBeenCalledOnce(); await Promise.resolve(); observed(); await operation;
  expect(focus).toHaveBeenCalledOnce();
});

it('rejects refused or stale focus without retrying or manufacturing foreground evidence', async () => {
  const focus = vi.fn();
  await expect(prepareNativeFocus({ requestFocus: focus, waitForFocus: async () => {}, isFocused: () => false })).rejects.toThrow('foreground');
  expect(focus).toHaveBeenCalledOnce();
  const timeoutFocus = vi.fn();
  await expect(prepareNativeFocus({ requestFocus: timeoutFocus, waitForFocus: async () => { throw new Error('Focus deadline'); }, isFocused: () => false })).rejects.toThrow('Focus deadline');
  expect(timeoutFocus).toHaveBeenCalledOnce();
});

it('sends each held move only after the prior trusted receipt and always releases the pointer', async () => {
  let acknowledge: (value: boolean) => void = () => {}; const sent: number[] = []; const release = vi.fn();
  const operation = performObservedDrag({ move: index => { sent.push(index); return new Promise(resolve => { acknowledge = resolve; }); }, release });
  expect(sent).toEqual([1]); expect(release).not.toHaveBeenCalled();
  for (let index = 1; index <= 8; index++) {
    acknowledge(true); await Promise.resolve(); expect(sent).toEqual(Array.from({ length: Math.min(8, index + 1) }, (_, i) => i + 1));
  }
  await expect(operation).resolves.toBe(true); expect(release).toHaveBeenCalledOnce();
});

it('keeps an unacknowledged or expired gesture incomplete without resending input', async () => {
  const sent: number[] = []; const release = vi.fn();
  await expect(performObservedDrag({ move: async index => { sent.push(index); return index < 3; }, release })).resolves.toBe(false);
  expect(sent).toEqual([1, 2, 3]); expect(release).toHaveBeenCalledOnce();
});

it('releases held input even if the native sender or observer throws', async () => {
  const release = vi.fn();
  await expect(performObservedDrag({ move: async () => { throw new Error('Native input refused'); }, release })).rejects.toThrow('Native input refused');
  expect(release).toHaveBeenCalledOnce();
});
