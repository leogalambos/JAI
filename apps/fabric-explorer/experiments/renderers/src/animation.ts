/** Disposable shared animation measurement; injected clocks make ordering regressions deterministic. */
export type AnimationEnvironment = {
  now(): number;
  requestFrame(callback: (frameTimestamp: number) => void): void;
  generation(): number;
  panZoom(seconds: number): void;
};
/** Raw active frame intervals and separate wall-clock completion observations. */
export type AnimationResult = { samplesMs: number[]; p95Ms: number | null; durationMs: number; cancelled: boolean; frameBudgetMet: boolean };

/**
 * Measure the registered active projection interval with an injected scheduler.
 * @param environment Monotonic wall clock, animation scheduler and current generation.
 * @param durationMs Registered duration; only 20000 milliseconds is allowed.
 * @returns Recorded samples and completion/cancellation observations.
 * @throws {Error} Rejects an unregistered duration or invalid clock/frame ordering.
 */
export function animateProjection(environment: AnimationEnvironment, durationMs = 20000): Promise<AnimationResult> {
  return new Promise((resolve, reject) => {
    if (durationMs !== 20000) throw new Error('Registered active pan/zoom duration is 20000ms');
    const samples: number[] = [];
    const activeGeneration = environment.generation();
    const start = environment.now();
    if (!Number.isFinite(start)) throw new Error('Finite monotonic invocation clock required');
    let previousWall = start;
    let previousFrame: number | undefined;
    const tick = (frameTimestamp: number) => {
      try {
        const wallNow = environment.now();
        if (!Number.isFinite(wallNow) || wallNow < previousWall) throw new Error('Monotonic callback clock required');
        previousWall = wallNow;
        const elapsedMs = wallNow - start;
        const cancelled = environment.generation() !== activeGeneration;
        if (!cancelled) {
          if (!Number.isFinite(frameTimestamp) || (previousFrame !== undefined && frameTimestamp < previousFrame)) throw new Error('Nondecreasing frame timestamps required');
          // A frame starts before its callbacks. Only successive frame timestamps
          // are comparable; invocation time is a separate wall-time observation.
          if (previousFrame !== undefined) samples.push(frameTimestamp - previousFrame);
          previousFrame = frameTimestamp;
        }
        if (cancelled || elapsedMs >= durationMs) {
          const sorted = [...samples].sort((a, b) => a - b);
          const p95 = sorted.length ? sorted[Math.ceil(0.95 * sorted.length) - 1] : null;
          resolve({ samplesMs: samples, p95Ms: p95, durationMs: elapsedMs, cancelled, frameBudgetMet: p95 !== null && p95 <= 33 });
          return;
        }
        environment.panZoom(elapsedMs / 1000);
        environment.requestFrame(tick);
      } catch (error) { reject(error); }
    };
    environment.requestFrame(tick);
  });
}
