/** Actual development bundle entry timestamps preserve the host launch clock and event ordering. */
import { expect, it } from 'vitest';
import { readFile } from 'node:fs/promises';
import { runInNewContext } from 'node:vm';
import { performanceEvent } from './performance-host-support.js';
it('emits native-entry before bundle initialization using the unchanged monotonic event protocol', async () => {
  const bundle = await readFile(new URL('../dist/performance-native.cjs', import.meta.url), 'utf8');
  const prefix = bundle.match(/^\/\* JAI_PERF_ENTRY_BEGIN \*\/([\s\S]*?)\/\* JAI_PERF_ENTRY_END \*\//)?.[1];
  expect(prefix).toBeDefined();
  const output: string[] = []; let now = 123456789n;
  runInNewContext(prefix! + '\nconsole.log("body-start");', { console: { log: (value: string) => output.push(value) }, process: { hrtime: { bigint: () => now++ } } });
  expect(output).toHaveLength(2); expect(performanceEvent(output[0]!)).toEqual({ name: 'native-entry', monotonicNs: '123456789', value: null }); expect(output[1]).toBe('body-start');
  expect(bundle.indexOf('JAI_PERF_ENTRY_END')).toBeLessThan(bundle.indexOf('require('));
});
