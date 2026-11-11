/** Rebuild the maintained exact SDK source using the desktop's pinned compiler and bundler. */
import { rmSync, readdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { resolve, dirname } from 'node:path';
import { build } from 'vite';
import { prepareSigma } from './prepare-sigma.mjs';
const desktop = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const sdk = resolve(desktop, 'vendor/sigma');
/**
 * Compile the fixed maintained SDK from prepared ignored sources.
 * @param options Native/offline builds must use an already prepared source cache.
 * @throws {Error} For missing cache, type errors or bundling failures.
 */
export async function buildSigma(options = {}) {
  const sourceRoot = await prepareSigma(options);
  // Upstream extends a monorepo-only config; the ignored package uses our same standalone flags.
  const sourcePackagePath = resolve(sourceRoot, 'package.json');
  const sourcePackage = JSON.parse(readFileSync(sourcePackagePath, 'utf8'));
  const packageType = JSON.parse(readFileSync(resolve(sdk, 'package.json'), 'utf8')).type;
  if (sourcePackage.type !== packageType || sourcePackage.name !== 'jai-sigma-prepared-source') { sourcePackage.type = packageType; sourcePackage.name = 'jai-sigma-prepared-source'; writeFileSync(sourcePackagePath, JSON.stringify(sourcePackage, null, 2) + '\n'); }
  const sourceConfig = JSON.parse(readFileSync(resolve(sdk, 'tsconfig.json'), 'utf8'));
  sourceConfig.compilerOptions.rootDir = 'src'; sourceConfig.compilerOptions.outDir = '../dist/types';
  sourceConfig.compilerOptions.paths = { sigma: ['./src/index.ts'], 'sigma/*': ['./src/*'] };
  sourceConfig.include = ['src/**/*.ts']; sourceConfig.exclude = ['src/**/*.test.ts', 'src/**/*.test-d.ts'];
  const configText = JSON.stringify(sourceConfig, null, 2) + '\n';
  if (readFileSync(resolve(sourceRoot, 'tsconfig.json'), 'utf8') !== configText) writeFileSync(resolve(sourceRoot, 'tsconfig.json'), configText);

rmSync(resolve(sdk, '.cache/dist'), { recursive: true, force: true });
const result = spawnSync(process.execPath, [resolve(desktop, 'node_modules/typescript/bin/tsc'), '-p', resolve(sdk, 'tsconfig.json')], { stdio: 'inherit' });
if (result.status !== 0) throw new Error('Maintained Sigma declaration/type build failed');
// Normalize only generated declarations for NodeNext consumers; upstream source remains unchanged.
function declarations(directory) {
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    const path = resolve(directory, entry.name);
    if (entry.isDirectory()) declarations(path);
    else if (entry.name.endsWith('.d.ts')) {
      const text = readFileSync(path, 'utf8').replace(/((?:from\s*|import\s*\()(["']))(\.[^"']+)(["'])/g, (whole, prefix, quote, specifier, suffix) => {
        if (specifier.endsWith('.js')) return whole;
        const target = resolve(directory, specifier);
        const ending = existsSync(`${target}.d.ts`) ? '.js' : existsSync(resolve(target, 'index.d.ts')) ? '/index.js' : null;
        if (!ending) throw new Error(`Unresolved declaration import ${specifier} in ${path}`);
        return prefix + specifier + ending + suffix;
      });
      writeFileSync(path, text);
    }
  }
}
declarations(resolve(sdk, '.cache/dist/types'));
for (const format of ['es', 'cjs']) await build({ configFile: false, envDir: false, publicDir: false, root: sourceRoot, logLevel: 'warn', build: {
  target: 'es2023', outDir: resolve(sdk, '.cache/dist'), emptyOutDir: false, minify: false, sourcemap: false,
  lib: { entry: Object.fromEntries(Object.entries({ index: 'index', types: 'types', settings: 'settings', rendering: 'rendering/index', primitives: 'primitives/index', utils: 'utils/index' }).map(([name, source]) => [name, resolve(sourceRoot, `src/${source}.ts`)])), formats: [format], fileName: (format, name) => `${name}.${format === 'es' ? 'js' : 'cjs'}` },
  rolldownOptions: { external: ['events', 'graphology-utils', 'graphology-types'], output: { exports: 'named', chunkFileNames: `[name]-[hash].${format === 'es' ? 'js' : 'cjs'}` } },
} });
console.log('Maintained Sigma source, declarations and both public module formats built.');

}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const arguments_ = process.argv.slice(2); if (arguments_.some(value => value !== '--offline') || arguments_.length > 1) throw new Error('Usage: build-sigma.mjs [--offline]');
  await buildSigma({ offline: arguments_.includes('--offline') });
}
