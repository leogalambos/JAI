// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Owned profiler-port tests; Electron objects and timing/RSS qualification are not mocked. */
import { describe, expect, it } from 'vitest';
import { rendererCpuProfileEnabled, RendererCpuProfiler } from './renderer-cpu-profile.js';
import type { RendererProfilerCommand, RendererProfilerPort } from './renderer-cpu-profile.js';
const profile = { nodes: [{ id: 1, callFrame: { functionName: 'syntheticFunction', scriptId: '1', url: 'synthetic-renderer.js', lineNumber: 1, columnNumber: 0 } }], startTime: 1000, endTime: 2000, samples: [1], timeDeltas: [1000] };
function fixture(failedCommand: RendererProfilerCommand | null = null, reply: unknown = { profile }) {
  const calls: unknown[] = [];
  const port: RendererProfilerPort = { attach: () => { calls.push('attach'); }, command: async (method, parameters) => { calls.push(parameters ? [method, parameters] : method); if (method === failedCommand) throw new Error('Expected command failure'); return method === 'Profiler.stop' ? reply : {}; }, detach: () => { calls.push('detach'); } };
  return { calls, port };
}
describe('smoke-only renderer CPU diagnostic', () => {
  it('keeps default modes inactive and rejects profiling outside explicit smoke', () => {
    for (const mode of ['smoke', 'qualification', 'endurance', 'all', undefined]) expect(rendererCpuProfileEnabled(mode, undefined)).toBe(false);
    expect(rendererCpuProfileEnabled('smoke', true)).toBe(true);
    for (const mode of ['qualification', 'endurance', 'all', undefined]) expect(() => rendererCpuProfileEnabled(mode, true)).toThrow('smoke-only');
    for (const flag of [false, 1, 'true', null]) expect(() => rendererCpuProfileEnabled('smoke', flag)).toThrow();
  });
  it('records the fixed command sequence and exactly bounded private JSON image', async () => {
    const f = fixture(); const json = JSON.stringify(profile) + '\n'; const instance = new RendererCpuProfiler(f.port, Buffer.byteLength(json));
    await instance.start(); const result = await instance.stop(); await instance.dispose();
    expect(result).toMatchObject({ json, bytes: Buffer.byteLength(json), nodes: 1, samples: 1, samplingIntervalUs: 1000, startTimeUs: 1000, endTimeUs: 2000 });
    expect(f.calls).toEqual(['attach', 'Profiler.enable', ['Profiler.setSamplingInterval', { interval: 1000 }], 'Profiler.start', 'Profiler.stop', 'Profiler.disable', 'detach']);
    await expect(instance.start()).rejects.toThrow('idle'); await expect(instance.stop()).rejects.toThrow('recording');
  });
  it('attempts disable and detach after enable, start or stop failure without retry', async () => {
    for (const method of ['Profiler.enable', 'Profiler.setSamplingInterval', 'Profiler.start', 'Profiler.stop'] as const) {
      const f = fixture(method); const instance = new RendererCpuProfiler(f.port);
      if (method === 'Profiler.stop') { await instance.start(); await expect(instance.stop()).rejects.toThrow('Expected command failure'); }
      else await expect(instance.start()).rejects.toThrow('Expected command failure');
      await instance.dispose(); expect(f.calls.at(-1)).toBe('detach'); expect(f.calls.filter(item => item === 'detach')).toHaveLength(1);
    }
  });
  it('rejects a one-byte-over or malformed profile and still detaches', async () => {
    const f = fixture(); const instance = new RendererCpuProfiler(f.port, Buffer.byteLength(JSON.stringify(profile) + '\n') - 1); await instance.start(); await expect(instance.stop()).rejects.toThrow('byte bound'); expect(f.calls.at(-1)).toBe('detach');
    for (const reply of [{}, { profile: { nodes: [], startTime: 2, endTime: 1 } }, { profile: { nodes: [], startTime: NaN, endTime: 1 } }]) { const bad = fixture(null, reply); const observer = new RendererCpuProfiler(bad.port); await observer.start(); await expect(observer.stop()).rejects.toThrow('Malformed'); expect(bad.calls.at(-1)).toBe('detach'); }
  });
  it('detaches synchronously on emergency abort and does not duplicate cleanup', async () => {
    const f = fixture(); const instance = new RendererCpuProfiler(f.port); await instance.start(); instance.abort(); await instance.dispose();
    expect(f.calls.at(-1)).toBe('detach'); expect(f.calls.filter(item => item === 'detach')).toHaveLength(1); expect(f.calls).not.toContain('Profiler.stop');
  });
  it('still attempts detach when disabling fails and reports the cleanup failure', async () => {
    const f = fixture('Profiler.disable'); const instance = new RendererCpuProfiler(f.port); await instance.start();
    await expect(instance.stop()).rejects.toThrow('cleanup failed'); expect(f.calls.at(-1)).toBe('detach'); expect(instance.cleanupErrors()).toEqual(['Expected command failure']);
  });
  it('does not detach twice when emergency abort happens during pending cleanup', async () => {
    const f = fixture(); let release: () => void = () => {}; let entered: () => void = () => {};
    const cleanupEntered = new Promise<void>(resolve => { entered = resolve; });
    const pending = new Promise<void>(resolve => { release = resolve; });
    const command = f.port.command;
    f.port.command = async (method, parameters) => { if (method === 'Profiler.disable') { entered(); await pending; } return command(method, parameters); };
    const instance = new RendererCpuProfiler(f.port); await instance.start(); const stopped = instance.stop(); await cleanupEntered; instance.abort(); release(); await stopped;
    expect(f.calls.filter(item => item === 'detach')).toHaveLength(1);
  });
  it('does not resume recording after emergency abort during a pending start', async () => {
    const f = fixture(); let release: () => void = () => {}; let entered: () => void = () => {};
    const startEntered = new Promise<void>(resolve => { entered = resolve; }); const pending = new Promise<void>(resolve => { release = resolve; });
    const command = f.port.command;
    f.port.command = async (method, parameters) => { if (method === 'Profiler.start') { entered(); await pending; } return command(method, parameters); };
    const instance = new RendererCpuProfiler(f.port); const started = instance.start(); await startEntered; instance.abort(); release();
    await expect(started).rejects.toThrow('aborted'); await expect(instance.stop()).rejects.toThrow('recording'); expect(f.calls.filter(item => item === 'detach')).toHaveLength(1);
  });
});
