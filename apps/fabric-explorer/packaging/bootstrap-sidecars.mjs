/** Emit local development installation entry scripts beside existing package manifests. */
import { readFile, readdir, writeFile, chmod, lstat } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { parseManifest } from './manifest.ts';
import { posixBootstrap, powershellBootstrap } from './bootstrap/generate.ts';

/**
 * Generate exact-manifest-bound unsigned development sidecars without rebuilding archives.
 * @param {string} outputRoot Developer-owned directory containing completed detached manifests.
 * @returns {Promise<string[]>} Sorted generated or identical existing installation script paths.
 * @throws {Error} For absent manifests, release metadata, conflicting scripts or inaccessible output.
 */
export async function generateDevelopmentSidecars(outputRoot) {
  const root = resolve(outputRoot);
  const names = (await readdir(root)).filter(name => name.endsWith('.manifest.json')).sort();
  if (!names.length) throw new Error('No completed package manifests found');
  const planned = [];
  for (const name of names) {
    const manifestBytes = await readFile(join(root, name));
    const manifest = parseManifest(manifestBytes);
    if (manifest.status !== 'development' || manifest.signatureKeyId !== null) throw new Error('Development sidecar command requires unsigned development metadata');
    if (name !== manifest.asset.fileName + '.manifest.json') throw new Error('Detached manifest filename mismatch');
    const windows = manifest.target === 'win32-x64';
    const path = join(root, manifest.asset.fileName + (windows ? '.install.ps1' : '.install.sh'));
    const bytes = Buffer.from((windows ? powershellBootstrap : posixBootstrap)({ manifestBytes, publicKey: null }));
    planned.push({ path, bytes, mode: windows ? 0o644 : 0o755 });
  }
  // Preflight every existing output before writing any new script.
  for (const item of planned) {
    try { if (!(await lstat(item.path)).isFile()) throw new Error('Installation script output must be a regular file'); if (!(await readFile(item.path)).equals(item.bytes)) throw new Error('Installation script output already differs'); }
    catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  for (const item of planned) {
    try { await writeFile(item.path, item.bytes, { flag: 'wx', mode: item.mode }); }
    catch (error) { if (error.code !== 'EEXIST' || !(await readFile(item.path)).equals(item.bytes)) throw error; }
    await chmod(item.path, item.mode);
  }
  return planned.map(item => item.path);
}

if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  const [outputRoot, permission, ...extra] = process.argv.slice(2);
  if (!outputRoot || permission !== '--allow-development' || extra.length) throw new Error('Usage: node bootstrap-sidecars.mjs <package-directory> --allow-development');
  for (const path of await generateDevelopmentSidecars(outputRoot)) console.log(path);
}
