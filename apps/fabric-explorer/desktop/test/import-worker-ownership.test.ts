/** Actual transferred FileHandle ownership on rejected worker envelopes. */
import { expect, it } from 'vitest';
import { Worker } from 'node:worker_threads';
import { open, mkdtemp, rm } from 'node:fs/promises';
import { fstatSync } from 'node:fs';
import { once } from 'node:events';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

it('closes transferred source and archive handles when the direct envelope is rejected before parsing', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'jai-worker-ownership-'));
  const source = await open(join(directory, 'source'), 'w+'); const archive = await open(join(directory, 'archive'), 'w+');
  const descriptors = [source.fd, archive.fd]; const worker = new Worker(new URL('../dist/import-worker.cjs', import.meta.url));
  try {
    const reply = once(worker, 'message');
    worker.postMessage({ id: 1, operation: 'directImport', extra: true, value: { files: [{ sourceHandle: source, archiveHandle: archive }] } }, [source, archive]);
    expect((await reply)[0]).toMatchObject({ ok: false });
    for (const descriptor of descriptors) expect(() => fstatSync(descriptor)).toThrow(expect.objectContaining({ code: 'EBADF' }));
  } finally { await worker.terminate(); await Promise.allSettled([source.close(), archive.close()]); await rm(directory, { recursive: true, force: true }); }
});
