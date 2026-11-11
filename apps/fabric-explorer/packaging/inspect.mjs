/** Fixed binary-package selection and measured filesystem inventory; no runtime is executed. */
import { createHash } from 'node:crypto';
import { createReadStream } from 'node:fs';
import { lstat, readdir, readlink, realpath } from 'node:fs/promises';
import { resolve, relative, sep, isAbsolute } from 'node:path';
import { applicationPrefix, runtimeExecutable, validateRelativePath, validateLink } from './manifest.ts';

/** The complete compiled viewer input, independent of additional development outputs. */
export const APPLICATION_FILES = Object.freeze(['main.cjs', 'preload.cjs', 'import-worker.cjs', 'renderer/index.html', 'renderer/renderer.js', 'renderer/renderer.css']);

/**
 * Hash one regular file without allocating an entire runtime binary in memory.
 * @param {string} path Existing regular file selected by the caller.
 * @returns {Promise<string>} Exact lowercase SHA-256 bytes digest.
 * @throws {Error} If the file cannot be read.
 */
export async function hashFile(path) {
  const hash = createHash('sha256');
  for await (const bytes of createReadStream(path)) hash.update(bytes);
  return hash.digest('hex');
}

/**
 * Observe regular files, directories and confined relative links once.
 * @param {string} root Private payload or verified runtime tree.
 * @returns {Promise<import('./manifest.ts').InventoryEntry[]>} Sorted root-relative entries, excluding inventory.json.
 * @throws {Error} For inaccessible, special, linked-root or escaping/broken-link inputs.
 */
export async function collectEntries(root) {
  const absolute = resolve(root);
  if (!(await lstat(absolute)).isDirectory() || (await lstat(absolute)).isSymbolicLink()) throw new Error('Package root must be a real directory');
  const physicalRoot = await realpath(absolute);
  const entries = [];
  async function walk(directory, prefix) {
    for (const name of (await readdir(directory)).sort()) {
      const path = prefix ? `${prefix}/${name}` : name;
      if (path === 'inventory.json') continue;
      validateRelativePath(path);
      const native = resolve(directory, name); const info = await lstat(native);
      if (info.isSymbolicLink()) {
        const target = await readlink(native); validateLink(path, target);
        const resolved = await realpath(native); const subpath = relative(physicalRoot, resolved);
        if (isAbsolute(subpath) || subpath === '..' || subpath.startsWith(`..${sep}`)) throw new Error('Package link escapes its root');
        entries.push({ path, kind: 'symlink', target });
      } else if (info.isDirectory()) {
        entries.push({ path, kind: 'directory', mode: info.mode & 0o777 }); await walk(native, path);
      } else if (info.isFile()) entries.push({ path, kind: 'file', size: info.size, sha256: await hashFile(native), mode: info.mode & 0o777 });
      else throw new Error('Package contains a special filesystem entry');
    }
  }
  await walk(absolute, '');
  return entries.sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0);
}

function parents(path, into) {
  const parts = path.split('/');
  while (parts.length > 1) { parts.pop(); into.add(parts.join('/')); }
}

/**
 * Measure and inspect a staged payload against independently selected runtime/app names.
 * @param {string} root Existing private staged payload.
 * @param {{target: import('./manifest.ts').Target, version:string, runtimeEntries:import('./manifest.ts').InventoryEntry[], noticePaths:string[]}} options Verified runtime inventory and enumerated legal outputs.
 * @returns {Promise<import('./manifest.ts').Inventory>} Exact sorted inventory; no side effects or execution.
 * @throws {Error} For missing/extra files, modified runtime bytes, wrong executable or source leakage.
 */
export async function inspectPackage(root, { target, version, runtimeEntries, noticePaths }) {
  const prefix = applicationPrefix(target);
  const allowed = new Set(['runtime', 'installer.cjs']);
  const runtime = new Map(runtimeEntries.map(entry => [`runtime/${entry.path}`, entry]));
  for (const name of runtime.keys()) allowed.add(name);
  for (const name of [...APPLICATION_FILES, 'package.json']) allowed.add(`${prefix}/${name}`);
  for (const name of noticePaths) { validateRelativePath(name); if (!name.startsWith('notices/')) throw new Error('Notice outside legal output tree'); allowed.add(name); }
  for (const name of [...allowed]) parents(name, allowed);
  const entries = await collectEntries(root); const actual = new Set(entries.map(entry => entry.path));
  for (const entry of entries) {
    if (!allowed.has(entry.path)) throw new Error(`Unselected package entry: ${entry.path}`);
    const original = runtime.get(entry.path);
    if (original) {
      const { path: _path, ...expected } = original; const { path: _actual, ...observed } = entry;
      if (JSON.stringify(expected) !== JSON.stringify(observed)) throw new Error(`Runtime entry differs from its verified archive: ${entry.path}`);
    }
  }
  for (const name of allowed) if (!actual.has(name)) throw new Error(`Missing selected package entry: ${name}`);
  const executable = entries.find(entry => entry.path === runtimeExecutable(target));
  if (!executable || executable.kind !== 'file' || (!target.startsWith('win32') && !(executable.mode & 0o111))) throw new Error('Target runtime executable is missing or non-executable');
  return { format: 'jai.fabric-explorer.inventory/1', productVersion: version, target, entries };
}
