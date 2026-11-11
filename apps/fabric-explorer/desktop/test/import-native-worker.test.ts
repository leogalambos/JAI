// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Real worker boundary integration; no mock stands in for native thread lifecycle or graph memory ownership. */
import { describe, expect, it } from 'vitest';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { NativeImportWorker } from '../src/import/worker-client.js';
import { modelInput, versionFact } from './import-fixtures.js';
const directory = resolve(dirname(fileURLToPath(import.meta.url)), '../dist/import-worker.cjs');
describe('fixed native import worker', () => {
  it('initializes, seals and pages span metadata while keeping full arrays inside the thread', async () => {
    const worker = new NativeImportWorker(directory);
    try {
      await worker.initialize(modelInput()); await worker.consume({ sequence: '0', facts: [versionFact()], next: null });
      const ready = await worker.finish(); expect(ready.descriptor.counts.vertices).toBe('1'); expect(ready).not.toHaveProperty('vertices');
      expect(await worker.span('fabric', versionFact().origin.pointer, '1')).toEqual({ offset: '0', length: '100' });
      await expect(worker.consume({ sequence: '1', facts: [], next: null })).rejects.toMatchObject({ code: 'invalid-model' });
    } finally { await worker.terminate(); }
  });
  it('rejects relative worker resources and premature/in-flight/terminated work', async () => {
    expect(() => new NativeImportWorker('relative.cjs')).toThrow('fixed');
    const worker = new NativeImportWorker(directory);
    try {
      const initialized = worker.initialize(modelInput()); await expect(worker.finish()).rejects.toMatchObject({ code: 'resource-limit' }); await initialized;
      await expect(worker.finish()).rejects.toMatchObject({ code: 'invalid-model' }); await worker.terminate(); await expect(worker.finish()).rejects.toMatchObject({ code: 'worker-failed' });
    } finally { await worker.terminate(); }
  });
});
