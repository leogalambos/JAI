// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Development-runner exit ownership; a window close must not replace a previously selected result. */
export class NativeExit {
  /** Whether a deliberate success, failure, timeout or interruption is already being handled. */
  finished = false;
  /**
   * Bind the host's immediate process-exit operation.
   * @param exit Trusted Electron application exit function.
   */
  constructor(private readonly exit: (code: number) => void) {}
  /**
   * Select one terminal result before host shutdown can synchronously close a window.
   * @param code Zero for success, one for failure, two for timeout, or 130 for interruption.
   * @returns Nothing; the host controls process termination.
   */
  finish(code: 0 | 1 | 2 | 130): void { if (this.finished) return; this.finished = true; this.exit(code); }
}
