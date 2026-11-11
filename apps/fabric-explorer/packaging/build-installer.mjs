/** Compile only the installation helper; qualified application assets are not rebuilt. */
import { builtinModules, createRequire } from 'node:module';
import { spawnSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const directory = dirname(fileURLToPath(import.meta.url));
const desktop = resolve(directory, '../desktop');
const checked = spawnSync(process.execPath, [resolve(desktop, 'node_modules/typescript/bin/tsc'), '--project', resolve(directory, 'tsconfig.json'), '--noEmit'], { stdio: 'inherit' });
if (checked.status !== 0) throw new Error('Installer typecheck failed');
const require = createRequire(resolve(desktop, 'package.json'));
const { build } = await import(pathToFileURL(require.resolve('vite')).href);
const external = new Set(builtinModules.flatMap(name => [name, `node:${name}`]));
await build({
  configFile: false, envDir: false, publicDir: false, root: directory, logLevel: 'warn',
  build: {
    target: 'es2023', outDir: resolve(desktop, 'dist'), emptyOutDir: false, sourcemap: false, minify: false,
    lib: { entry: resolve(directory, 'installer-cli.ts'), formats: ['cjs'], fileName: () => 'installer.cjs' },
    rolldownOptions: { external: id => external.has(id) },
  },
});
console.log('Built installation-only helper; application executables were not rebuilt.');
