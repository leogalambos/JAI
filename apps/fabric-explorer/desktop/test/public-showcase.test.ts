/** Real canonical public-workflow generation through the fixed broker and actual compiled TypeScript worker. */
import { expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { mkdtemp, mkdir, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { ReadBroker } from '../src/broker/read-broker.js';
import { ImportSession } from '../src/import/session.js';
import { NativeImportWorker } from '../src/import/worker-client.js';
import { PROTOCOL, decodeChunkFrame } from '@jai/fabric-explorer-contracts';
import type { Edge, SourceReference, Vertex } from '@jai/fabric-explorer-contracts';
import { DEFAULT_QUERY_LIMITS } from '../src/graph/query-index.js';
it('imports the source-only public reference, readable roles and available canonical materials without findings', async () => {
  const root = resolve(import.meta.dirname, '../../../..'); const base = await mkdtemp(join(tmpdir(), 'jai-public-showcase-')); const project = join(base, 'public-project'); const application = join(base, 'application'); await mkdir(application);
  let session: ImportSession | null = null; let broker: ReadBroker | null = null;
  try {
    const metadata = JSON.parse(execFileSync(join(root, 'build/fabric-explorer/helper-venv/bin/python'), ['-I', '-B', join(root, 'apps/fabric-explorer/examples/public_workflows.py'), project], { encoding: 'utf8' })) as { journal: string; source_records: number; roles: { role: string; ref: SourceReference }[] };
    const path = join(project, metadata.journal); const before = await readFile(path); expect(before.toString()).toContain('Software Engineer');
    const registry = new Map<string, string>(); broker = new ReadBroker({ cwd: application, writeRoots: [application], registry: { getOrCreate: async (kind, key) => { const id = `${kind}:${key}`; if (!registry.has(id)) registry.set(id, `${kind}-${registry.size}`); return registry.get(id)!; } } });
    const opened = await broker.open('public-showcase', [{ projectPath: project, path, family: 'fabric' }]);
    session = new ImportSession({ sessionId: 'public-showcase', capability: opened.capability, sources: opened.sources, broker, archiveDirectory: join(application, 'captures'), workerFactory: () => new NativeImportWorker(join(root, 'apps/fabric-explorer/desktop/dist/import-worker.cjs')) });
    const descriptor = await session.import(opened.sources.map(source => source.sourceId), null);
    expect(descriptor.counts.findings).toBe('0'); expect(Number(descriptor.counts.vertices)).toBeGreaterThan(90); expect(Number(descriptor.counts.edges)).toBeGreaterThan(60); expect(descriptor.sources[0]?.sequence).toBe('1');
    const binding = { sessionId: 'public-showcase', capability: opened.capability, generation: descriptor.generation };
    const ref = metadata.roles.find(item => item.role === 'Software Engineer')!.ref;
    let page = await session.queryStart({ protocol: PROTOCOL, kind: 'request', requestId: 'branching-reference', binding, operation: 'graph.neighbours', payload: { identity: { kind: 'use', projectId: opened.sources[0]!.projectId, ref, useScope: 'documentation' }, direction: 'both', relations: ['inheritance'], causalOnly: true, limits: { ...DEFAULT_QUERY_LIMITS, maxHops: 4 } } });
    const vertices: Vertex[] = []; const edges: Edge[] = [];
    for (;;) { const frame = decodeChunkFrame(page.frame); vertices.push(...frame.vertices); edges.push(...frame.edges); if (!page.continuationToken) break; page = await session.queryNext({ binding, requestId: 'branching-reference', continuationToken: page.continuationToken }); }
    const degree = new Map(vertices.map(vertex => [vertex.id, new Set<string>()]));
    for (const edge of edges) { degree.get(edge.from)!.add(edge.to); degree.get(edge.to)!.add(edge.from); }
    expect(vertices).toHaveLength(22); expect(edges).toHaveLength(22);
    expect([...degree.values()].filter(neighbours => neighbours.size >= 3)).toHaveLength(9);
    expect(vertices.some(vertex => vertex.label.startsWith('Delivery '))).toBe(true); expect(vertices.some(vertex => vertex.label.startsWith('Remediation '))).toBe(true);
    expect(vertices.every(vertex => vertex.kind === 'use')).toBe(true);
    await session.queryDrop({ binding, requestId: 'branching-reference', continuationToken: null, projectionToken: page.projectionToken });
    expect(await readFile(path)).toEqual(before);
  } finally { await session?.dispose(); await broker?.disposeSession('public-showcase'); await rm(base, { recursive: true, force: true }); }
});
