// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** S08 positive refresh boundary: actual canonical append, retained native source and accepted worker generation. */
import { expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { mkdtemp, mkdir, readFile, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { PROTOCOL, decodeChunkFrame } from '@jai/fabric-explorer-contracts';
import { ReadBroker } from '../src/broker/read-broker.js';
import { ImportSession } from '../src/import/session.js';
import { NativeImportWorker } from '../src/import/worker-client.js';
it('publishes one coherent new generation after a valid in-place canonical finding append without source writes', async () => {
  const repository = resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');
  const python = join(repository, 'build/fabric-explorer/helper-venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
  const root = await mkdtemp(join(tmpdir(), 'jai-viewer-refresh-')); const project = join(root, 'project'); const application = join(root, 'application'); await mkdir(project); await mkdir(application);
  const filename = join(project, 'review.jsonl'); await writeFile(filename, await readFile(join(repository, 'apps/fabric-explorer/test/fixtures/findings-review.jsonl')));
  const namespaces = new Map<string, string>();
  const broker = new ReadBroker({ executable: python, script: join(repository, 'apps/fabric-explorer/reader/raw_reader.py'), coreTools: join(repository, '.ai/runtime/tools'), cwd: application, writeRoots: [application], registry: { getOrCreate: async (kind, key) => { const address = `${kind}:${key}`; if (!namespaces.has(address)) namespaces.set(address, `${kind}-${namespaces.size}`); return namespaces.get(address)!; } } });
  let session: ImportSession | null = null;
  try {
    const opened = await broker.open('refresh-integration', [{ projectPath: project, path: filename, family: 'findings' }]);
    session = new ImportSession({ sessionId: 'refresh-integration', capability: opened.capability, sources: opened.sources, broker, archiveDirectory: join(application, 'captures'), workerFactory: () => new NativeImportWorker(join(repository, 'apps/fabric-explorer/desktop/dist/import-worker.cjs')) });
    const first = await session.import(opened.sources.map(source => source.sourceId), null);
    execFileSync(python, ['-I', '-B', '-c', "import os,sys; os.environ['FINDINGS_HOME']=sys.argv[2]; sys.dont_write_bytecode=True; sys.path.insert(0,sys.argv[1]); import findings; events=findings.load('review'); findings.append('review',events,[{'op':'resolve','id':'F-0001','by':'synthetic-viewer-author','note':'Synthetic successful refresh','ref':None}])", join(repository, '.ai/runtime/tools'), project], { timeout: 10000 });
    const expected = await readFile(filename); const refreshed = await session.refresh('1');
    expect(refreshed.generation).toBe('2'); expect(refreshed.counts.findings).toBe('6'); expect(refreshed.sources[0]!.head).not.toBe(first.sources[0]!.head);
    const binding = { sessionId: 'refresh-integration', capability: opened.capability, generation: '2' };
    const result = await session.searchFindings({ protocol: PROTOCOL, kind: 'request', binding, requestId: 'finding-refresh', operation: 'search.page', payload: { text: 'Synthetic example 1', filter: { projectIds: [], families: [], findingStates: [], relations: [] }, order: 'identity', limit: 50, cursor: null } });
    const frame = decodeChunkFrame(result.frame); expect(frame.vertices).toHaveLength(1); expect(frame.vertices[0]).toMatchObject({ kind: 'finding', state: 'resolved' }); expect(frame.terminal).not.toBeNull();
    expect(await readFile(filename)).toEqual(expected); expect(session.state().stale).toBe(false);
  } finally { await session?.dispose(); await broker.disposeSession('refresh-integration'); await rm(root, { recursive: true, force: true }); }
});
