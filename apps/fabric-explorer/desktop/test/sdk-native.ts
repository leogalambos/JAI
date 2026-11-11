// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Development-only actual WebGL program counts; no timing qualification or dependency-internal overrides. */
import { MultiDirectedGraph } from 'graphology';
import { canvasOptions, createSigmaRenderer } from '../src/renderer/canvas/sdk.js';

const operations = ['createShader', 'createProgram', 'compileShader', 'linkProgram', 'getShaderParameter', 'getProgramParameter'] as const;
/** Actual native method invocations within one synchronous renderer lifetime. */
export type ShaderCounts = Record<typeof operations[number], number>;

/**
 * Compare default-on and opt-out constructors on fresh actual contexts with the same primitive configuration.
 * @param container Trusted native test document; only the created child panel is removed.
 * @returns Actual per-constructor counts and explicit pass/fail, retaining partial counts on failure.
 * @throws {Error} For unavailable WebGL2 or a document that cannot create the owned test panel.
 * @remarks Wrapping native methods adds overhead; this result never establishes a duration or RSS pass.
 */
export function runSdkNativeComparison(container: HTMLElement) {
  if (typeof WebGL2RenderingContext === 'undefined') throw new Error('Actual WebGL2 is required for SDK program counts.');
  const panel = document.createElement('div'); Object.assign(panel.style, { position: 'fixed', left: '0', top: '0', width: '512px', height: '256px', background: 'white', zIndex: '100001' }); container.append(panel);
  const cases: { labelPrograms: boolean; counts: ShaderCounts; completed: boolean }[] = [];
  const run = (labelPrograms: boolean): ShaderCounts => {
    console.info(`SDK program check ${labelPrograms ? 1 : 2}/2: ${labelPrograms ? 'default companion programs' : 'reduced companion programs'}`);
    const host = document.createElement('div'); Object.assign(host.style, { width: '512px', height: '256px' }); panel.append(host);
    const counts = Object.fromEntries(operations.map(name => [name, 0])) as ShaderCounts;
    const prototype = WebGL2RenderingContext.prototype; const originals = new Map<string, PropertyDescriptor>();
    let completed = false;
    try {
      for (const name of operations) {
        const descriptor = Object.getOwnPropertyDescriptor(prototype, name);
        if (!descriptor || typeof descriptor.value !== 'function' || !descriptor.configurable) throw new Error('Native GL counter boundary is unavailable.');
        originals.set(name, descriptor); const original = descriptor.value as (...args: unknown[]) => unknown;
        Object.defineProperty(prototype, name, { ...descriptor, value: function(this: WebGL2RenderingContext, ...args: unknown[]) { counts[name]++; return Reflect.apply(original, this, args); } });
      }
      const options = canvasOptions();
      options.primitives = { ...options.primitives, nodes: { ...options.primitives?.nodes, labelPrograms } };
      const renderer = createSigmaRenderer(new MultiDirectedGraph(), host, options);
      try { renderer.refresh(); } finally { renderer.kill(); }
      completed = true;
    } finally {
      for (const [name, descriptor] of originals) Object.defineProperty(prototype, name, descriptor);
      cases.push({ labelPrograms, counts, completed });
      host.remove();
    }
    return counts;
  };
  let status: 'pass' | 'fail' = 'fail'; let failure: string | null = null;
  try {
    const defaultPrograms = run(true); const reducedPrograms = run(false);
    for (const name of operations) if (reducedPrograms[name] < 1 || reducedPrograms[name] > defaultPrograms[name]) throw new Error(`Invalid actual SDK program count: ${name}`);
    if (reducedPrograms.createProgram >= defaultPrograms.createProgram || reducedPrograms.compileShader >= defaultPrograms.compileShader || reducedPrograms.linkProgram >= defaultPrograms.linkProgram) throw new Error('No actual SDK companion-program reduction observed.');
    status = 'pass';
  } catch { failure = 'Actual constructor, counter boundary or program reduction failed; inspect retained cases.'; }
  finally { panel.remove(); }
  return { status, failure, source: 'actual-native-WebGL2-calls', cases, scope: 'Empty graph constructor comparison only; geometry/picking checks and cold performance observations are separate.' };
}
