/** Failed-first actual worker payload boundary; full corpus must remain in the worker. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { createCorpus } from './src/corpus.ts';
const source = readFileSync(new URL('./src/corpus.worker.ts', import.meta.url), 'utf8');
const compiled = stripTypeScriptTypes(source, { mode: 'strip' }).replace(/^import .*;\s*$/gm, '');
const replies = [];
const worker = { onmessage: null, postMessage: value => replies.push(value) };
let service;
try { service = (await import('./src/corpus-service.ts')).createCorpusService; } catch (error) { if (error.code !== 'ERR_MODULE_NOT_FOUND') throw error; }
new Function('self', 'createCorpus', 'createCorpusService', compiled)(worker, createCorpus, service);
worker.onmessage({ data: { type: 'initialize', size: 'M', requestId: 1 } });
assert.ok(replies.length);
assert.equal('corpus' in replies[0], false, 'Worker must not structured-clone its complete corpus into the UI');
assert.equal(replies[0].view.nodes.length, 2000);
assert.equal(replies[0].view.edges.length, 8000);
assert.equal(replies[0].metadata.vertices, 25000);
assert.equal(replies[0].metadata.edges, 100000);
worker.onmessage({ data: { type: 'initialize', size: 'S', vertexLimit: 2, edgeLimit: 4, requestId: 2 } });
assert.equal(replies[1].view.nodes.length, 2); assert.equal(replies[1].view.edges.length, 4);
assert.deepEqual(replies[1].view.nodes, createCorpus('M').nodes.slice(0, 2));
assert.deepEqual(replies[1].view.edges, createCorpus('M').edges.slice(0, 4));
console.log('PASS: actual corpus worker posts bounded projection plus dimensional metadata, not full corpus.');
