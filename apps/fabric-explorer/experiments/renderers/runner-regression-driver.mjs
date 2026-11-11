/** Disposable integration double: runs the real runner without launching a browser. */
import { chromium } from '@playwright/test';
import { writeFile } from 'node:fs/promises';
import { PassThrough } from 'node:stream';
import { MessageChannel } from 'node:worker_threads';
import fs from 'node:fs';
import { syncBuiltinESMExports } from 'node:module';

const scenario = process.argv[2];
const output = process.argv[3];
// Browser doubles do not execute assets; isolate lifecycle regressions from a
// concurrent build replacing its output directory or a clean source checkout.
const readFile = fs.promises.readFile;
fs.promises.readFile = async (path, ...options) => {
  const name = String(path).replaceAll('\\', '/');
  if (name.endsWith('/dist/phase-bootstrap.js')) return '/* synthetic early observer asset */';
  if (name.endsWith('/dist/probe.js')) return '/* synthetic browser-double asset */';
  if (name.endsWith('/dist/probe.css')) return '/* synthetic browser-double style */';
  return readFile(path, ...options);
};
syncBuiltinESMExports();
let createdCases = 0;
let closed = false;
let closedContexts = 0;
let exposedStop;
const events = [];
if (scenario === 'diagnostic-labels') { const schedule = globalThis.setTimeout; globalThis.setTimeout = (callback, milliseconds, ...args) => schedule(callback, milliseconds <= 100 ? 0 : milliseconds, ...args); }
const transport = new MessageChannel();
transport.port1.on('message', () => {});
class FakePage {
  handlers = new Map();
  on(event, handler) { this.handlers.set(event, handler); }
  async exposeBinding(_name, handler) { exposedStop = handler; }
  async route() {}
  async setContent() { events.push('html'); }
  async addStyleTag() {}
  async addScriptTag(value) { events.push(value.content.includes('early observer') ? 'early-observer' : 'harness'); }
  async waitForFunction() {}
  async screenshot() {}
  setDefaultTimeout() {}
  locator() { return { boundingBox: async () => null }; }
  async evaluate(fn) {
    const source = String(fn);
    if (source.includes('rendererProbePhases?.snapshot')) return { observerAvailable: true, overallMaxTaskMs: 942, noObservedTaskOver200ms: false, tasks: [{ startTime: 1, duration: 942 }], beforeCoverage: 'unknown-even-when-buffered-entries-exist' };
    if (source.includes('.animate(') && !source.includes('.cancel(')) {
      if (scenario === 'abort') throw Object.assign(new Error('Cancelled by operator'), { name: 'AbortError' });
      if (scenario === 'button') {
        await exposedStop({}, 'browser-stop-button');
        return {};
      }
      if (scenario === 'signal') { queueMicrotask(() => process.kill(process.pid, 'SIGINT')); return new Promise(() => {}); }
      if (scenario === 'eof') { queueMicrotask(() => input.end()); return new Promise(() => {}); }
      if (scenario === 'window-close') { queueMicrotask(() => this.handlers.get('close')?.()); return new Promise(() => {}); }
      return { samplesMs: [16], p95Ms: 16, cancelled: false };
    }
    if (source.includes('.nodePoint(')) return { x: NaN, y: NaN };
    if (source.includes('.details(')) return 'synthetic details';
    if (source.includes('rendererProbe.error')) return null;
    if (source.includes('.expand(') && scenario === 'failure-after-measurement') throw new Error('Synthetic expansion failure');
    if (source.includes('.review(')) {
      if (scenario === 'manual-signal') { queueMicrotask(() => process.kill(process.pid, 'SIGINT')); return new Promise(() => {}); }
      if (scenario === 'manual-button') { queueMicrotask(() => exposedStop({}, 'browser-stop-button')); return new Promise(() => {}); }
      return { criteria: {}, method: 'synthetic-test' };
    }
    return {};
  }
}
const browser = {
  version: () => 'synthetic-browser-double',
  newBrowserCDPSession: async () => ({ send: async () => ({ processInfo: [] }) }),
  on() {},
  close: async () => { closed = true; transport.port1.close(); transport.port2.close(); },
  newContext: async () => {
    createdCases++;
    const page = new FakePage();
    const context = { newPage: async () => page, close: async () => { closedContexts++; page.handlers.get('close')?.(); } };
    if (scenario === 'context-stop') return new Promise(resolve => queueMicrotask(() => {
      process.emit('SIGINT'); queueMicrotask(() => resolve(context));
    }));
    return context;
  },
};
chromium.launch = async () => {
  if (scenario === 'launch-stop') return new Promise(resolve => queueMicrotask(() => {
    process.emit('SIGINT'); queueMicrotask(() => resolve(browser));
  }));
  return browser;
};
const input = new PassThrough();
input.isTTY = scenario !== 'non-tty';
if (scenario === 'non-tty') input.end();
Object.defineProperty(process, 'stdin', { value: input });
process.argv = [process.argv[0], new URL('./run-probe.mjs', import.meta.url).pathname,
  `--output=${output}`, `--manual=${scenario.startsWith('manual-')}`, '--size=S', '--scales=1,1.5,2', `--renderer=${['focused-sigma', 'diagnostic-labels'].includes(scenario) ? 'sigma' : 'both'}`, `--diagnostics=${scenario === 'diagnostic-labels' ? 'memory-phases' : 'none'}`, `--review=${scenario === 'diagnostic-labels' ? 'labels' : 'all'}`];
await import('./run-probe.mjs');
await writeFile(`${output}/driver.json`, JSON.stringify({ createdCases, closed, closedContexts, events, exitCode: process.exitCode ?? 0 }));
process.exitCode = 0;
