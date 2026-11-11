/** Build fixed local application assets; sandboxed preload may depend externally only on Electron. */
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { builtinModules } from 'node:module';
import { readdir, mkdir, copyFile, readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { build } from 'vite';

const directory = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const native = process.argv.slice(2);
if (native.some(value => !['--with-native-smoke', '--with-accessibility-manual', '--with-security-check', '--with-performance-check'].includes(value)) || native.length > 1) throw new Error('Choose one fixed development helper profile');
// A fresh script-disabled directory-link install has no generated SDK assets.
const { buildSigma } = await import('./build-sigma.mjs');
await buildSigma({ offline: native.length > 0 });
const project = native[0] === '--with-accessibility-manual' ? 'tsconfig.accessibility-manual.json' : 'tsconfig.json';
const checked = spawnSync(process.execPath, [resolve(directory, 'node_modules/typescript/bin/tsc'), '--project', resolve(directory, project), '--noEmit'], { stdio: 'inherit' });
if (checked.status !== 0) throw new Error('Desktop typecheck failed');
const builtins = new Set(builtinModules.flatMap(name => [name, `node:${name}`]));

async function bundle(entry, filename, preload = false, clean = false, format = 'cjs', globalName = 'CanvasNative') {
  return build({
    configFile: false, envDir: false, publicDir: false, root: directory, logLevel: 'warn',
    build: {
      target: 'es2023', outDir: resolve(directory, 'dist'), emptyOutDir: clean,
      sourcemap: false, minify: false,
      lib: { entry: resolve(directory, entry), formats: [format], ...(format === 'iife' ? { name: globalName } : {}), fileName: () => filename },
      rolldownOptions: { ...(filename === 'performance-native.cjs' ? { output: { banner: `/* JAI_PERF_ENTRY_BEGIN */
console.log('JAI_PERF_EVENT ' + JSON.stringify({ name: 'native-entry', monotonicNs: String(process.hrtime.bigint()), value: null }));
/* JAI_PERF_ENTRY_END */` } } : {}), external(id) {
        if (id === 'electron') return true;
        if (builtins.has(id)) {
          if (preload) throw new Error(`Sandboxed preload cannot depend on ${id}`);
          return format !== 'iife';
        }
        return false;
      } },
    },
  });
}

await bundle('src/main.ts', 'main.cjs', false, true);
await bundle('src/import/worker.ts', 'import-worker.cjs');
const preload = await bundle('src/preload.ts', 'preload.cjs', true);
const outputs = Array.isArray(preload) ? preload : [preload];
for (const output of outputs) for (const item of output.output) if (item.type === 'chunk') {
  assert(item.imports.every(id => id === 'electron'), 'Preload must not contain other external dependencies');
  assert.equal(item.dynamicImports.length, 0, 'Preload must be one static bundle');
}
await build({
  configFile: false, envDir: false, publicDir: false,
  root: resolve(directory, 'src/renderer'), base: './', logLevel: 'warn',
  build: {
    target: 'es2023', outDir: resolve(directory, 'dist/renderer'), emptyOutDir: true,
    sourcemap: false, minify: false, modulePreload: false, cssCodeSplit: false,
    rolldownOptions: {
      input: resolve(directory, 'src/renderer/index.html'),
      output: { entryFileNames: 'renderer.js', assetFileNames: 'renderer.css' },
    },
  },
});
assert.deepEqual((await readdir(resolve(directory, 'dist/renderer'))).sort(), ['index.html', 'renderer.css', 'renderer.js']);
await mkdir(resolve(directory, 'dist/licenses'), { recursive: true });
await copyFile(resolve(directory, 'vendor/sigma/LICENSE.txt'), resolve(directory, 'dist/licenses/sigma-MIT.txt'));
if (native[0] === '--with-accessibility-manual') await bundle('test/accessibility-manual.ts', 'accessibility-manual.cjs');
if (native[0] === '--with-performance-check') {
  await bundle('test/performance-corpus-oracle.ts', 'performance-corpus-oracle.cjs');
  await bundle('test/performance-native.ts', 'performance-native.cjs');
  await bundle('test/performance-host.ts', 'performance-host.cjs');
  await bundle('test/performance-plan.ts', 'performance-plan.cjs');
}
if (native[0] === '--with-security-check') {
  await bundle('test/security-native.ts', 'security-native.cjs');
  await bundle('test/native-preload.ts', 'security-assets/preload.cjs', true);
  const target = resolve(directory, 'dist/security-assets/renderer');
  await mkdir(target, { recursive: true });
  for (const name of ['index.html', 'renderer.js', 'renderer.css']) {
    const source = resolve(directory, 'dist/renderer', name); const destination = resolve(target, name);
    await copyFile(source, destination);
    assert.deepEqual(await readFile(destination), await readFile(source), 'Security qualification renderer must exactly match production');
  }
}
if (native[0] === '--with-native-smoke') {
  await bundle('test/native-shell.ts', 'native-shell.cjs');
  await bundle('test/viewer-native.ts', 'viewer-native.cjs');
  await bundle('test/accessibility-native.ts', 'accessibility-native.cjs');
  await bundle('test/visual-details-native.ts', 'visual-details-native.cjs');
  await bundle('test/accessibility-manual.ts', 'accessibility-manual.cjs');
  await bundle('test/canvas-accessibility.ts', 'canvas-accessibility.js', false, false, 'iife', 'CanvasAccessibility');
  await bundle('test/canvas-native.ts', 'canvas-native.js', false, false, 'iife');
  await bundle('test/graph-smoke.mjs', 'graph-smoke.cjs');
  await bundle('test/native-preload.ts', 'native-smoke-assets/preload.cjs', true);
  const target = resolve(directory, 'dist/native-smoke-assets/renderer');
  await mkdir(target, { recursive: true });
  for (const name of ['index.html', 'renderer.js', 'renderer.css']) {
    const source = resolve(directory, 'dist/renderer', name); const destination = resolve(target, name);
    await copyFile(source, destination);
    assert.deepEqual(await readFile(destination), await readFile(source), 'Native smoke renderer must exactly match production');
  }
}
console.log(`Built fixed main/preload/renderer assets${native.length ? ' and development-only qualification helpers' : ''}.`);
