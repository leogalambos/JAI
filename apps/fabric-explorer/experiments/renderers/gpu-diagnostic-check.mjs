/** Actual app GPU-metadata source counters with public SDK accessor; no native GPU/time/memory claim. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { MultiDirectedGraph } from 'graphology';
const adapterSource = stripTypeScriptTypes(readFileSync(new URL('./src/sigma-adapter.ts', import.meta.url), 'utf8')).replace(/^import .*;\s*$/gm, '').replace('export function createSigmaAdapter', 'function createSigmaAdapter');
const main = readFileSync(new URL('./src/main.ts', import.meta.url), 'utf8');
const extract = (source, head) => { const start = source.indexOf(head); assert.ok(start >= 0); let index = source.indexOf('{', start), depth = 1, end = index + 1; for (; depth; end++) { if (source[end] === '{') depth++; if (source[end] === '}') depth--; } return source.slice(start, end); };
const sdk = readFileSync(new URL('./node_modules/sigma/dist/sigma.esm.js', import.meta.url), 'utf8');
const stageAccessor = new Function(`return ${extract(sdk, 'function getStageCanvas()')}`)();
for (let run = 0; run < 30; run++) {
  let allocations = 0, losses = 0, queries = 0;
  const document = { createElement() { allocations++; throw new Error('No diagnostic canvas creation permitted'); } };
  const gl = { getExtension: name => name === 'WEBGL_debug_renderer_info' ? { UNMASKED_RENDERER_WEBGL: 0x9246 } : name === 'WEBGL_lose_context' ? { loseContext() { losses++; } } : null, getParameter: () => 'ControlledGPU' };
  class Renderer {
    constructor() { this.stageCanvas = { getContext(name) { assert.equal(name, 'webgl2'); queries++; return gl; } }; }
    getStageCanvas() { return stageAccessor.call(this); }
    getCamera() { return { getState: () => ({ x: .5, y: .5, ratio: 1, angle: 0 }) }; }
    on() {}
  }
  const create = new Function('Sigma', 'MultiDirectedGraph', 'sigmaOptions', 'document', adapterSource + ';return createSigmaAdapter;')(Renderer, MultiDirectedGraph, () => ({}), document);
  const adapter = create({ nodes: [], edges: [] }, {}, () => {});
  const metadata = new Function('adapter', 'document', extract(main, 'function gpuInfo()') + ';return gpuInfo;')(adapter, document);
  const first = metadata(); assert.equal(first.renderer, 'ControlledGPU'); assert.equal(first.webgl2, true); assert.equal(first.softwareLikely, false);
  for (let index = 0; index < 10; index++) assert.equal(metadata(), first);
  const nonWebgl = new Function('adapter', 'document', extract(main, 'function gpuInfo()') + ';return gpuInfo;')({}, document)();
  assert.equal(nonWebgl.webgl2, false); assert.equal(nonWebgl.softwareLikely, null); assert.match(nonWebgl.renderer, /not-applicable/);
  assert.equal(queries, 1); assert.equal(allocations, 0); assert.equal(losses, 0);
}
console.log('PASS:30 actual adapter/main metadata trials with SDK public stage accessor, one borrowed lookup, cached metadata, zero canvas allocations/losses, non-WebGL unknown.');
