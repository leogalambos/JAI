// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Controlled synchronous close events preserve actual runner exit ownership. */
import { expect, it } from 'vitest';
import { NativeExit } from './native-exit.js';
it.each([0, 1, 2] as const)('preserves deliberate exit %s when shutdown re-enters through window close', code => {
  const codes: number[] = []; let native: NativeExit;
  native = new NativeExit(value => { codes.push(value); if (codes.length === 1) native.finish(130); });
  native.finish(code); expect(codes).toEqual([code]); expect(native.finished).toBe(true);
});
it('uses interruption only when the operator closes before a terminal result exists', () => {
  const codes: number[] = []; const native = new NativeExit(code => codes.push(code)); expect(native.finished).toBe(false); native.finish(130); expect(codes).toEqual([130]);
});
