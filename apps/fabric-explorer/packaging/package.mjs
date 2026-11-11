/** Deterministic developer-side packages from pinned runtimes and explicit compiled inputs. */
import { createHash, randomUUID } from 'node:crypto';
import { readFile, writeFile, mkdir, lstat, chmod, cp, rm, rename, mkdtemp, readdir, utimes, lutimes, open } from 'node:fs/promises';
import { createReadStream, createWriteStream, readFileSync, lstatSync, readlinkSync } from 'node:fs';
import { spawn, execFileSync } from 'node:child_process';
import { pipeline } from 'node:stream/promises';
import { createGzip, inflateRawSync } from 'node:zlib';
import { dirname, resolve, join, posix } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { applicationPrefix, runtimeExecutable, encodeManifest, parseInventory, sha256, validateRelativePath, validateLink } from './manifest.ts';
import { APPLICATION_FILES, collectEntries, hashFile, inspectPackage } from './inspect.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const application = resolve(here, '..');
const desktop = resolve(application, 'desktop');
const repository = resolve(application, '../..');
const pins = JSON.parse(await readFile(join(here, 'runtime-pins.json'), 'utf8'));
const releaseBase = `https://github.com/electron/electron/releases/download/v${pins.version}/`;
const defaultEpoch = 315532800;

/**
 * Select a frozen official archive; no caller can nominate a mirror or latest version.
 * @param {import('./manifest.ts').Target} target Exact supported OS/architecture identifier.
 * @returns {{fileName:string,sha256:string,url:string}} Fixed public build input.
 * @throws {Error} For unsupported targets or malformed maintained pins.
 */
export function runtimePin(target) {
  const pin = Object.hasOwn(pins.targets, target) ? pins.targets[target] : null;
  if (!pin || !/^[a-f0-9]{64}$/.test(pin.sha256) || pin.fileName !== `electron-v${pins.version}-${target}.zip`) throw new Error('Unsupported or unpinned runtime target');
  return { ...pin, url: releaseBase + pin.fileName };
}

/**
 * Inspect ordinary non-ZIP64 official runtime archives before extraction.
 * @param {Uint8Array} input Exact archive bytes already authenticated by the runtime pin.
 * @returns {{path:string,kind:'file'|'directory'|'symlink',mode:number,target?:string}[]} Unique confined members.
 * @throws {Error} For malformed, encrypted, unsupported, escaping or conflicting entries.
 */
export function inspectZip(input) {
  const bytes = Buffer.from(input); let end = -1;
  for (let at = bytes.length - 22; at >= Math.max(0, bytes.length - 65557); at--) if (bytes.readUInt32LE(at) === 0x06054b50 && at + 22 + bytes.readUInt16LE(at + 20) === bytes.length) { end = at; break; }
  if (end < 0 || bytes.readUInt16LE(end + 4) || bytes.readUInt16LE(end + 6)) throw new Error('Unsupported ZIP directory');
  const count = bytes.readUInt16LE(end + 10); const offset = bytes.readUInt32LE(end + 16); const length = bytes.readUInt32LE(end + 12);
  if (count === 65535 || count !== bytes.readUInt16LE(end + 8) || offset + length !== end) throw new Error('Unsupported ZIP64 or directory extent');
  const entries = []; const names = new Map(); let at = offset;
  for (let ordinal = 0; ordinal < count; ordinal++) {
    if (at + 46 > end || bytes.readUInt32LE(at) !== 0x02014b50) throw new Error('Invalid ZIP directory entry');
    const flags = bytes.readUInt16LE(at + 8); const method = bytes.readUInt16LE(at + 10); const packed = bytes.readUInt32LE(at + 20); const size = bytes.readUInt32LE(at + 24);
    const nameLength = bytes.readUInt16LE(at + 28); const extra = bytes.readUInt16LE(at + 30); const comment = bytes.readUInt16LE(at + 32); const local = bytes.readUInt32LE(at + 42);
    const mode = bytes.readUInt32LE(at + 38) >>> 16; const type = mode & 0o170000;
    if ((flags & 1) || ![0, 8].includes(method) || at + 46 + nameLength + extra + comment > end || local + 30 > offset || bytes.readUInt32LE(local) !== 0x04034b50) throw new Error('Unsupported ZIP encoding');
    const encoded = bytes.subarray(at + 46, at + 46 + nameLength); const name = new TextDecoder('utf8', { fatal: true }).decode(encoded);
    const path = name.endsWith('/') ? name.slice(0, -1) : name; validateRelativePath(path);
    if (names.has(path)) throw new Error('Duplicate ZIP member');
    const localLength = bytes.readUInt16LE(local + 26); const localExtra = bytes.readUInt16LE(local + 28); const data = local + 30 + localLength + localExtra;
    if (!bytes.subarray(local + 30, local + 30 + localLength).equals(encoded) || data + packed > offset) throw new Error('ZIP local header mismatch');
    const kind = type === 0o120000 ? 'symlink' : name.endsWith('/') || type === 0o040000 ? 'directory' : 'file';
    if (type && ![0o120000, 0o040000, 0o100000].includes(type)) throw new Error('ZIP special file is unsupported');
    const entry = { path, kind, mode: mode & 0o777 };
    if (kind === 'symlink') {
      if (size > 4096 || packed > 65536) throw new Error('Oversized ZIP link');
      const compressed = bytes.subarray(data, data + packed); const target = method === 0 ? compressed : inflateRawSync(compressed, { maxOutputLength: 4096 });
      if (target.length !== size) throw new Error('ZIP link length mismatch');
      entry.target = new TextDecoder('utf8', { fatal: true }).decode(target); validateLink(path, entry.target);
    }
    names.set(path, entry); entries.push(entry); at += 46 + nameLength + extra + comment;
  }
  if (at !== end) throw new Error('ZIP directory count mismatch');
  for (const entry of entries) {
    const parts = entry.path.split('/');
    while (parts.length > 1) { parts.pop(); const parent = names.get(parts.join('/')); if (parent && parent.kind !== 'directory') throw new Error('ZIP member traverses another member'); }
  }
  return entries;
}

async function command(program, args, options = {}) {
  const child = spawn(program, args, { stdio: ['ignore', 'pipe', 'pipe'], ...options });
  child.stdout?.resume();
  let stderr = ''; child.stderr?.on('data', bytes => { if (stderr.length < 8192) stderr += bytes.toString(); });
  const result = await new Promise((accept, reject) => { child.once('error', reject); child.once('close', code => accept(code)); });
  if (result !== 0) throw new Error(`${program} failed (${result}): ${stderr.trim()}`);
}

async function normalizeModes(root, archiveEntries) {
  for (const entry of archiveEntries) {
    if (entry.kind === 'symlink') continue;
    try { await chmod(join(root, entry.path), entry.mode || (entry.kind === 'directory' ? 0o755 : 0o644)); }
    catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
}

async function assertRuntimeTarget(root, target) {
  const path = join(root, runtimeExecutable(target).slice('runtime/'.length)); const handle = await open(path, 'r');
  const bytes = Buffer.alloc(65536); let read;
  try { read = (await handle.read(bytes, 0, bytes.length, 0)).bytesRead; } finally { await handle.close(); }
  const expected = target.endsWith('arm64') ? 'arm64' : 'x64'; let observed = null;
  if (target.startsWith('linux') && read >= 20 && bytes.subarray(0, 4).equals(Buffer.from([127, 69, 76, 70])) && bytes[4] === 2 && bytes[5] === 1) observed = ({ 62: 'x64', 183: 'arm64' })[bytes.readUInt16LE(18)];
  if (target.startsWith('win32') && read >= 64 && bytes.subarray(0, 2).toString() === 'MZ') { const pe = bytes.readUInt32LE(60); if (pe + 6 <= read && bytes.readUInt32LE(pe) === 0x4550 && bytes.readUInt16LE(pe + 4) === 0x8664) observed = 'x64'; }
  if (target.startsWith('darwin') && read >= 8) {
    if (bytes.readUInt32LE(0) === 0xfeedfacf) observed = ({ 0x1000007: 'x64', 0x100000c: 'arm64' })[bytes.readUInt32LE(4)];
    else if ([0xcafebabe, 0xcafebabf].includes(bytes.readUInt32BE(0))) {
      const count = bytes.readUInt32BE(4); const stride = bytes.readUInt32BE(0) === 0xcafebabf ? 32 : 20;
      if (count <= 16 && 8 + count * stride <= read) for (let i = 0; i < count; i++) if (({ 0x1000007: 'x64', 0x100000c: 'arm64' })[bytes.readUInt32BE(8 + i * stride)] === expected) observed = expected;
    }
  }
  if (observed !== expected) throw new Error(`Runtime executable does not match ${target}`);
}

/**
 * Prepare a fixed runtime once; later builds hash their staged copies against its recorded inventory.
 * @param {object} options Exact target, developer-owned cacheRoot, and optional offline flag rejecting absent cache without network.
 * @returns {Promise<{root:string,entries:import('./manifest.ts').InventoryEntry[],pin:ReturnType<typeof runtimePin>}>} Authenticated source tree and observed inventory.
 * @throws {Error} For offline misses, invalid pins/archives, architecture mismatch or incomplete cache.
 */
export async function prepareRuntime(options) {
  const { target, cacheRoot, offline = false } = options;
  const pin = runtimePin(target); const destination = resolve(cacheRoot, `electron-${pins.version}-${target}`); const metadata = join(destination, 'prepared.json');
  try {
    const cached = JSON.parse(await readFile(metadata, 'utf8'));
    if (cached.archiveSha256 !== pin.sha256 || cached.target !== target) throw new Error('Runtime cache pin mismatch');
    const inventory = parseInventory(Buffer.from(JSON.stringify(cached.inventory)));
    if (inventory.target !== target || inventory.productVersion !== pins.version || !inventory.entries.some(entry => entry.path === runtimeExecutable(target).slice('runtime/'.length) && entry.kind === 'file')) throw new Error('Runtime cache inventory mismatch');
    if (!(await lstat(join(destination, 'tree'))).isDirectory()) throw new Error('Runtime cache tree missing');
    return { root: join(destination, 'tree'), entries: inventory.entries, pin };
  } catch (error) { if (error.code !== 'ENOENT') throw error; }
  try { await lstat(destination); throw new Error('Incomplete runtime cache; remove the owned cache entry before rebuilding'); } catch (error) { if (error.code !== 'ENOENT') throw error; }
  if (offline) throw new Error(`Pinned runtime cache missing for ${target}`);
  await mkdir(cacheRoot, { recursive: true }); const stage = await mkdtemp(join(resolve(cacheRoot), `.electron-${target}-`));
  try {
    const response = await fetch(pin.url, { signal: AbortSignal.timeout(180000) });
    if (!response.ok || !response.body) throw new Error(`Official runtime download failed (${response.status})`);
    const archive = join(stage, pin.fileName); const hash = createHash('sha256'); let length = 0;
    const stream = createWriteStream(archive, { flags: 'wx', mode: 0o600 });
    await pipeline(response.body, async function* (source) { for await (const chunk of source) { length += chunk.length; if (length > 512 * 1024 * 1024) throw new Error('Official runtime exceeds build download bound'); hash.update(chunk); yield chunk; } }, stream);
    if (hash.digest('hex') !== pin.sha256) throw new Error('Official runtime SHA-256 differs from the frozen pin');
    const archiveEntries = inspectZip(await readFile(archive)); const tree = join(stage, 'tree'); await mkdir(tree);
    await command('unzip', ['-q', archive, '-d', tree]);
    for (const name of ['resources/default_app.asar', 'Electron.app/Contents/Resources/default_app.asar']) await rm(join(tree, name), { force: true });
    await normalizeModes(tree, archiveEntries); await assertRuntimeTarget(tree, target);
    const entries = await collectEntries(tree); const inventory = { format: 'jai.fabric-explorer.inventory/1', productVersion: pins.version, target, entries };
    await writeFile(join(stage, 'prepared.json'), JSON.stringify({ target, archiveSha256: pin.sha256, inventory }, null, 2) + '\n');
    await rename(stage, destination);
    return { root: join(destination, 'tree'), entries, pin };
  } catch (error) { await rm(stage, { recursive: true, force: true }); throw error; }
}

/**
 * Derive source identity from maintained public application inputs only.
 * @param {string} worktree Public project worktree; defaults to this build's repository.
 * @returns {{commit:string,dirty:boolean,closureSha256:string}} Git revision and exact source-closure digest.
 * @throws {Error} When public source inputs or Git metadata cannot be read.
 */
export function publicSourceRevision(worktree = repository) {
  const args = ['-C', worktree];
  const commit = execFileSync('git', [...args, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
  const names = new Set([...execFileSync('git', [...args, 'ls-files', '-z', '--', 'apps/fabric-explorer']).toString().split('\0'), ...execFileSync('git', [...args, 'ls-files', '--others', '--exclude-standard', '-z', '--', 'apps/fabric-explorer']).toString().split('\0')].filter(Boolean));
  const hash = createHash('sha256');
  for (const name of [...names].sort()) {
    if (/(?:^|\/)(?:\.env(?:\..*)?|\.npmrc|\.pypirc|id_rsa|id_ed25519|settings-security\.xml)$/.test(name)) throw new Error('Private configuration cannot enter public source identity');
    const path = join(worktree, name); const info = lstatSync(path);
    const bytes = info.isSymbolicLink() ? Buffer.from(readlinkSync(path)) : readFileSync(path);
    hash.update(name + '\0'); hash.update(bytes);
  }
  const dirty = execFileSync('git', [...args, 'status', '--porcelain', '--', 'apps/fabric-explorer'], { encoding: 'utf8' }).length > 0;
  return { commit, dirty, closureSha256: hash.digest('hex') };
}

async function notices(root, runtimeRoot, target, version, epoch) {
  const output = join(root, 'notices'); await mkdir(output, { mode: 0o755 }); await chmod(output, 0o755);
  const components = []; const licenseFiles = [];
  const names = ['react', 'react-dom', 'scheduler', 'graphology', 'graphology-utils', 'events', 'sigma'];
  for (const name of names) {
    const path = join(desktop, 'node_modules', name); const manifest = JSON.parse(await readFile(join(path, 'package.json'), 'utf8'));
    const licenseName = (await readdir(path)).find(value => /^(?:LICENSE|LICENCE)(?:\.(?:txt|md))?$/i.test(value));
    if (!licenseName) throw new Error(`Missing bundled dependency license: ${name}`);
    const bytes = await readFile(join(path, licenseName)); const outputName = `${name.replaceAll('/', '-')}-LICENSE.txt`;
    await writeFile(join(output, outputName), bytes, { mode: 0o644 }); licenseFiles.push(outputName);
    components.push({ name, version: manifest.version, licenseConcluded: manifest.license ?? 'NOASSERTION', licenseFile: `notices/${outputName}`, licenseSha256: sha256(bytes), role: 'bundled-application-library' });
  }
  for (const [source, name] of [['LICENSE', 'electron-LICENSE.txt'], ['LICENSES.chromium.html', 'chromium-NOTICES.html']]) {
    const candidates = [join(runtimeRoot, source), join(runtimeRoot, 'Electron.app/Contents/Resources', source), join(runtimeRoot, 'Electron.app/Contents/Frameworks/Electron Framework.framework/Resources', source)];
    let bytes; for (const path of candidates) { try { bytes = await readFile(path); break; } catch (error) { if (error.code !== 'ENOENT') throw error; } }
    if (!bytes) throw new Error(`Missing official runtime license: ${source}`);
    await writeFile(join(output, name), bytes, { mode: 0o644 }); licenseFiles.push(name);
  }
  const projectLicense = await readFile(join(repository, 'LICENSE')); await writeFile(join(output, 'JAI-LICENSE.txt'), projectLicense, { mode: 0o644 }); licenseFiles.push('JAI-LICENSE.txt');
  const body = ['JAI Fabric Explorer: BSD-4-Clause; see JAI-LICENSE.txt.', `Electron ${pins.version}: see electron-LICENSE.txt and chromium-NOTICES.html.`, ...components.map(value => `${value.name} ${value.version}: ${value.licenseConcluded}; see ${value.licenseFile.slice(8)}.`)].join('\n') + '\n';
  await writeFile(join(output, 'third-party.txt'), body, { mode: 0o644 });
  const sbom = { spdxVersion: 'SPDX-2.3', dataLicense: 'CC0-1.0', SPDXID: 'SPDXRef-DOCUMENT', name: 'JAI Fabric Explorer bundled runtime inventory', documentNamespace: 'https://jai.invalid/sbom/' + sha256(Buffer.from(body)), creationInfo: { creators: ['Tool: JAI Fabric Explorer packager'], created: new Date(epoch * 1000).toISOString().replace('.000Z', 'Z') }, packages: [{ name: 'jai-fabric-explorer', versionInfo: version, SPDXID: 'SPDXRef-application', downloadLocation: 'NOASSERTION', filesAnalyzed: false, licenseConcluded: 'BSD-4-Clause', licenseDeclared: 'BSD-4-Clause', copyrightText: 'See bundled JAI license' }, { name: 'electron', versionInfo: pins.version, SPDXID: 'SPDXRef-electron', downloadLocation: runtimePin(target).url, checksums: [{ algorithm: 'SHA256', checksumValue: runtimePin(target).sha256 }], filesAnalyzed: false, licenseConcluded: 'NOASSERTION', licenseDeclared: 'MIT', copyrightText: 'See bundled notices' }, ...components.map(value => ({ name: value.name, versionInfo: value.version, SPDXID: `SPDXRef-${value.name}`, downloadLocation: value.name === 'sigma' ? 'https://github.com/jacomyal/sigma.js' : `https://registry.npmjs.org/${value.name}`, filesAnalyzed: false, licenseConcluded: value.licenseConcluded, licenseDeclared: value.licenseConcluded, copyrightText: 'See bundled notices', externalRefs: [{ referenceCategory: 'PACKAGE-MANAGER', referenceType: 'purl', referenceLocator: `pkg:npm/${value.name}@${value.version}` }] }))], relationships: [{ spdxElementId: 'SPDXRef-DOCUMENT', relationshipType: 'DESCRIBES', relatedSpdxElement: 'SPDXRef-application' }, ...['electron', ...components.map(value => value.name)].map(name => ({ spdxElementId: 'SPDXRef-application', relationshipType: 'DEPENDS_ON', relatedSpdxElement: `SPDXRef-${name}` }))], annotations: [{ annotationType: 'OTHER', annotator: 'Tool: JAI Fabric Explorer packager', annotationDate: new Date(epoch * 1000).toISOString().replace('.000Z', 'Z'), comment: 'Dates use the explicit reproducible build epoch, not observed wall-clock creation time. Chromium transitive notices are retained verbatim; this component inventory does not claim an enumerated Chromium source dependency graph. Patched Sigma provenance is retained separately.' }] };
  const sigmaProvenance = await readFile(join(desktop, 'vendor/sigma/provenance.json')); await writeFile(join(output, 'sigma-provenance.json'), sigmaProvenance, { mode: 0o644 });
  await writeFile(join(output, 'sbom.json'), JSON.stringify(sbom, null, 2) + '\n', { mode: 0o644 });
  return [...licenseFiles.map(name => `notices/${name}`), 'notices/third-party.txt', 'notices/sbom.json', 'notices/sigma-provenance.json'];
}

async function normalizeTimes(root, epoch, entries) {
  const time = new Date(epoch * 1000);
  for (const entry of entries) {
    const path = join(root, entry.path);
    if (entry.kind === 'symlink') await lutimes(path, time, time); else await utimes(path, time, time);
  }
  await utimes(join(root, 'inventory.json'), time, time);
  await utimes(root, time, time);
}

async function archivePayload(root, destination, target, epoch, inventoryEntries) {
  await normalizeTimes(root, epoch, inventoryEntries);
  if (target.startsWith('win32')) {
    const entries = inventoryEntries.map(value => value.path); entries.push('inventory.json'); entries.sort();
    const child = spawn('zip', ['-X', '-y', '-q', destination, '-@'], { cwd: root, env: { ...process.env, TZ: 'UTC' }, stdio: ['pipe', 'pipe', 'pipe'] });
    let errorText = ''; child.stderr.on('data', bytes => { errorText += bytes.toString(); }); child.stdin.end(entries.join('\n') + '\n');
    await new Promise((accept, reject) => { child.on('error', reject); child.on('close', code => code === 0 ? accept() : reject(new Error(`zip failed: ${errorText}`))); });
  } else {
    const child = spawn('tar', ['--sort=name', `--mtime=@${epoch}`, '--owner=0', '--group=0', '--numeric-owner', '--format=posix', '--pax-option=delete=atime,delete=ctime', '-cf', '-', '-C', root, '.'], { env: { ...process.env, TZ: 'UTC' }, stdio: ['ignore', 'pipe', 'pipe'] });
    let text = ''; child.stderr.on('data', bytes => { text += bytes.toString(); });
    const closed = new Promise((accept, reject) => { child.on('error', reject); child.on('close', code => code === 0 ? accept() : reject(new Error(`tar failed: ${text}`))); });
    await Promise.all([closed, pipeline(child.stdout, createGzip({ level: 9 }), createWriteStream(destination, { flags: 'wx', mode: 0o600 }))]);
  }
}

/**
 * Assemble one unsigned development candidate without modifying or rebuilding app executables.
 * @param {object} options Explicit build inputs: target, version, outputRoot, cacheRoot, appRoot, installerFile and development:true. Optional offline rejects absent cached runtimes; epoch fixes archive time; sourceRevision and preparedRuntime are trusted already authenticated authoring handoffs.
 * @returns {Promise<{assetPath:string,manifestPath:string,inventoryPath:string}>} Archive and exact detached metadata paths.
 * @throws {Error} For invalid versions, missing assets, altered runtime, source leakage or archiver failure.
 */
export async function packageTarget(options) {
  const { target, version, outputRoot, cacheRoot, appRoot, installerFile } = options; runtimePin(target);
  if (options.development !== true || !/^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$/.test(version)) throw new Error('This builder emits explicitly development-only candidates');
  const epoch = options.epoch ?? defaultEpoch;
  if (!Number.isSafeInteger(epoch) || epoch < defaultEpoch) throw new Error('Invalid archive epoch');
  const runtime = options.preparedRuntime ?? await prepareRuntime({ target, cacheRoot, offline: options.offline });
  if (runtime.pin.sha256 !== runtimePin(target).sha256) throw new Error('Prepared runtime target pin mismatch');
  await mkdir(outputRoot, { recursive: true }); const stage = await mkdtemp(join(resolve(outputRoot), `.package-${target}-`));
  const payload = join(stage, 'payload'); await mkdir(payload); await chmod(payload, 0o755);
  try {
    await cp(runtime.root, join(payload, 'runtime'), { recursive: true, dereference: false, verbatimSymlinks: true });
    const prefix = applicationPrefix(target);
    for (const name of APPLICATION_FILES) { const source = join(appRoot, name); const info = await lstat(source); if (!info.isFile() || info.isSymbolicLink()) throw new Error('Compiled app input must be a regular file'); await mkdir(dirname(join(payload, prefix, name)), { recursive: true }); await cp(source, join(payload, prefix, name)); await chmod(join(payload, prefix, name), 0o644); }
    for (let path = join(payload, prefix); path !== payload; path = dirname(path)) await chmod(path, 0o755);
    await chmod(join(payload, prefix, 'renderer'), 0o755);
    await writeFile(join(payload, prefix, 'package.json'), JSON.stringify({ name: 'jai-fabric-explorer', productName: 'JAI Fabric Explorer', version, private: true, main: 'main.cjs', license: 'BSD-4-Clause' }, null, 2) + '\n', { mode: 0o644 });
    if (!(await lstat(installerFile)).isFile()) throw new Error('Missing compiled installer helper'); await cp(installerFile, join(payload, 'installer.cjs')); await chmod(join(payload, 'installer.cjs'), 0o644);
    const noticePaths = await notices(payload, runtime.root, target, version, epoch);
    const inventory = await inspectPackage(payload, { target, version, runtimeEntries: runtime.entries, noticePaths });
    const inventoryBytes = Buffer.from(JSON.stringify(inventory, null, 2) + '\n'); parseInventory(inventoryBytes); await writeFile(join(payload, 'inventory.json'), inventoryBytes, { mode: 0o644 });
    const extension = target.startsWith('win32') ? 'zip' : 'tar.gz'; const name = `jai-fabric-explorer-${version}-${target}.${extension}`; const asset = join(stage, name);
    await archivePayload(payload, asset, target, epoch, inventory.entries); const assetInfo = await lstat(asset);
    const manifest = { format: 'jai.fabric-explorer.asset/1', status: 'development', product: 'jai-fabric-explorer', productVersion: version, target, sourceRevision: options.sourceRevision ?? publicSourceRevision(), signatureKeyId: null, runtime: { name: 'electron', version: pins.version, archiveSha256: runtime.pin.sha256 }, asset: { fileName: name, byteLength: assetInfo.size, sha256: await hashFile(asset) }, inventory: { fileName: 'inventory.json', byteLength: inventoryBytes.length, sha256: sha256(inventoryBytes) }, sbom: { fileName: 'notices/sbom.json', sha256: await hashFile(join(payload, 'notices/sbom.json')) }, notices: { fileName: 'notices/third-party.txt', sha256: await hashFile(join(payload, 'notices/third-party.txt')) } };
    const manifestBytes = encodeManifest(manifest); const manifestName = name + '.manifest.json';
    await writeFile(join(stage, manifestName), manifestBytes, { mode: 0o644 });
    const assetPath = join(resolve(outputRoot), name); const manifestPath = assetPath + '.manifest.json'; const inventoryPath = assetPath + '.inventory.json';
    for (const path of [assetPath, manifestPath, inventoryPath]) { try { await lstat(path); throw new Error('Package output already exists'); } catch (error) { if (error.code !== 'ENOENT') throw error; } }
    await rename(asset, assetPath); await rename(join(stage, manifestName), manifestPath); await writeFile(inventoryPath, inventoryBytes, { flag: 'wx', mode: 0o644 });
    return { assetPath, manifestPath, inventoryPath };
  } finally { await rm(stage, { recursive: true, force: true }); }
}

if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  const [target, outputRoot = resolve(repository, 'build/fabric-explorer/packages'), mode] = process.argv.slice(2);
  if (!target) throw new Error('Usage: node package.mjs <target|all> [output-directory] [--offline]');
  const targets = target === 'all' ? Object.keys(pins.targets) : [target];
  const version = JSON.parse(await readFile(join(desktop, 'package.json'), 'utf8')).version;
  for (let i = 0; i < targets.length; i++) { console.log(`Package ${i + 1}/${targets.length}: ${targets[i]}`); console.log(JSON.stringify(await packageTarget({ target: targets[i], version, outputRoot, cacheRoot: resolve(repository, 'build/fabric-explorer/runtime-cache'), appRoot: join(desktop, 'dist'), installerFile: join(desktop, 'dist/installer.cjs'), development: true, offline: mode === '--offline' }))); }
}
