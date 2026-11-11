// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Opt-in smoke-only renderer CPU diagnostics over a main-owned, closed debugger port. */

/** Only fixed profiler commands are available to this development helper. */
export type RendererProfilerCommand = 'Profiler.enable' | 'Profiler.setSamplingInterval' | 'Profiler.start' | 'Profiler.stop' | 'Profiler.disable';
/** Owned adapter over one actual renderer target; never exposed through preload or source data. */
export interface RendererProfilerPort {
  /** Attach this observer to its fixed renderer target. */
  attach(): void;
  /** Send one fixed profiler operation; parameters are maintainer-owned. */
  command(method: RendererProfilerCommand, parameters?: Readonly<Record<string, number>>): Promise<unknown>;
  /** Detach only this observer's owned session. */
  detach(): void;
}
/** Private profile output ceiling; profiling observations never qualify production timing or RSS. */
export const MAX_RENDERER_CPU_PROFILE_BYTES = 16 * 1024 * 1024;
/** Small profile metadata accompanies the separately saved private CPU profile image. */
export interface RendererCpuProfileResult { readonly json: string; readonly bytes: number; readonly nodes: number; readonly samples: number; readonly startTimeUs: number; readonly endTimeUs: number; readonly samplingIntervalUs: 1000 }

/**
 * Admit profiling only through the explicit trusted smoke input flag.
 * @param mode Trusted run mode; old native inputs may omit it while profiling is absent.
 * @param requested Optional flag, which must be exactly true when present.
 * @returns Whether the single smoke renderer should be profiled.
 * @throws {Error} For an enabled/non-boolean flag outside explicit smoke mode.
 */
export function rendererCpuProfileEnabled(mode: unknown, requested: unknown): boolean {
  if (requested === undefined) return false;
  if (mode !== 'smoke' || requested !== true) throw new Error('Renderer CPU profiling requires the explicit smoke-only diagnostic flag.');
  return true;
}

/** One non-reusable profiler lifetime; command failures still attempt owned-session detachment. */
export class RendererCpuProfiler {
  private state: 'idle' | 'starting' | 'recording' | 'closed' = 'idle';
  private attached = false;
  private cleaned = false;
  private readonly failures: string[] = [];
  /**
   * Bind a fixed main-owned debugger adapter and a bounded private image size.
   * @param port Adapter to the actual production renderer selected by the native helper.
   * @param maximumBytes Inclusive positive UTF-8 image ceiling, no greater than 16 MiB.
   * @throws {Error} For an invalid or excessive diagnostic bound.
   */
  constructor(private readonly port: RendererProfilerPort, private readonly maximumBytes = MAX_RENDERER_CPU_PROFILE_BYTES) {
    if (!Number.isSafeInteger(maximumBytes) || maximumBytes < 1 || maximumBytes > MAX_RENDERER_CPU_PROFILE_BYTES) throw new Error('Invalid private CPU profile bound.');
  }
  /**
   * Attach, enable, select 1000-microsecond sampling and start once before the actual Import click.
   * @returns Completion after the actual renderer profiler acknowledges start.
   * @throws {Error} For repeated use or any debugger operation failure; detachment is attempted.
   */
  async start(): Promise<void> {
    if (this.state !== 'idle') throw new Error('Renderer CPU profiler is not idle.');
    this.state = 'starting';
    try {
      this.port.attach(); this.attached = true;
      await this.port.command('Profiler.enable');
      await this.port.command('Profiler.setSamplingInterval', { interval: 1000 });
      await this.port.command('Profiler.start');
      if (!this.attached || this.state !== 'starting') throw new Error('Renderer CPU profiler start was aborted.');
      this.state = 'recording';
    } catch (error) { this.state = 'closed'; await this.cleanup(); throw error; }
  }
  /**
   * Stop after usable layout, validate the private image bound, disable and detach.
   * @returns Exact profile JSON plus small metadata; the class retains no profile image.
   * @throws {Error} For absent recording, malformed/oversized output or command/cleanup failure.
   */
  async stop(): Promise<RendererCpuProfileResult> {
    if (this.state !== 'recording') throw new Error('Renderer CPU profiler is not recording.');
    this.state = 'closed'; let result: RendererCpuProfileResult | null = null; let failure: unknown = null;
    try {
      const reply = await this.port.command('Profiler.stop') as { profile?: unknown } | null;
      const profile = reply?.profile as { nodes?: unknown; samples?: unknown; startTime?: unknown; endTime?: unknown } | undefined;
      if (!profile || !Array.isArray(profile.nodes) || typeof profile.startTime !== 'number' || !Number.isFinite(profile.startTime) || profile.startTime < 0 || typeof profile.endTime !== 'number' || !Number.isFinite(profile.endTime) || profile.endTime < profile.startTime || profile.samples !== undefined && !Array.isArray(profile.samples)) throw new Error('Malformed renderer CPU profile.');
      const json = JSON.stringify(profile) + '\n'; const bytes = Buffer.byteLength(json);
      if (bytes > this.maximumBytes) throw new Error('Private renderer CPU profile exceeds its byte bound.');
      result = { json, bytes, nodes: profile.nodes.length, samples: Array.isArray(profile.samples) ? profile.samples.length : 0, startTimeUs: profile.startTime, endTimeUs: profile.endTime, samplingIntervalUs: 1000 };
    } catch (error) { failure = error; }
    finally { await this.cleanup(); }
    if (failure) throw failure;
    if (this.failures.length) throw new Error('Renderer CPU profiler cleanup failed.');
    return result!;
  }
  /**
   * Release an incomplete profiler lifetime without retrying an observation.
   * @returns Completion after best-effort disable and owned-session detach.
   * @remarks Cleanup errors remain available through cleanupErrors(); no profile success is inferred.
   */
  async dispose(): Promise<void> { this.state = 'closed'; await this.cleanup(); }
  /**
   * Synchronously detach an owned profiler during window close, signal or emergency exit.
   * @returns Nothing; no command waits can delay the existing stop path.
   */
  abort(): void {
    this.state = 'closed'; this.cleaned = true;
    if (this.attached) { try { this.port.detach(); } catch (error) { this.failures.push(error instanceof Error ? error.message : 'Detach failed.'); } finally { this.attached = false; } }
  }
  /**
   * Obtain bounded-lifetime cleanup diagnostics without exposing the live adapter.
   * @returns Detached error messages from attempted disable/detach operations.
   */
  cleanupErrors(): readonly string[] { return [...this.failures]; }
  private async cleanup(): Promise<void> {
    if (this.cleaned) return; this.cleaned = true;
    if (!this.attached) return;
    try { await this.port.command('Profiler.disable'); } catch (error) { this.failures.push(error instanceof Error ? error.message : 'Disable failed.'); }
    finally { if (this.attached) { try { this.port.detach(); } catch (error) { this.failures.push(error instanceof Error ? error.message : 'Detach failed.'); } finally { this.attached = false; } } }
  }
}
