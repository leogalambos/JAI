/** Explicit clone-local source build/install orchestration; prebuilt entry scripts need no Node.js. */
import { existsSync, readFileSync, realpathSync } from 'node:fs';
import { dirname, delimiter, isAbsolute, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawnSync } from 'node:child_process';
const repository = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
const MIN_NODE_VERSION = '24.0.0'; const MIN_NPM_VERSION = '11.0.0';
// Qualification pins describe reproducibility; host admission uses stable minimum versions.
function meetsMinimum(version, minimum) {
  if (!/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/.test(version)) return false;
  const actual = version.split('.').map(Number); const required = minimum.split('.').map(Number);
  for (let index = 0; index < required.length; index++) {
    if (actual[index] !== required[index]) return actual[index] > required[index];
  }
  return true;
}
/**
 * Select the current supported package target before any mutation or dependency operation.
 * @param {string} platform Node platform identifier.
 * @param {string} architecture Node architecture identifier.
 * @returns {string} Exact maintained target.
 * @throws {Error} For an unsupported combination; no fallback architecture is used.
 */
export function currentTarget(platform, architecture) {
  const target = `${platform}-${architecture}`;
  if (!['linux-x64', 'linux-arm64', 'darwin-x64', 'darwin-arm64', 'win32-x64'].includes(target)) throw new Error(`Unsupported viewer platform: ${target}`);
  return target;
}
/**
 * Validate the explicitly requested source-build flags.
 * @param {string[]} args User argument vector, without shell reconstruction.
 * @returns {{dryRun:boolean}} Validated source-build mode.
 * @throws {Error} For missing development consent, conflicting or unknown flags.
 */
export function sourceOptions(args) {
  if (args.some(value => !['--build', '--allow-development', '--dry-run'].includes(value)) || new Set(args).size !== args.length) throw new Error('Source build accepts only --build --allow-development [--dry-run]; use --package-dir for existing packages.');
  if (!args.includes('--build') || !args.includes('--allow-development')) throw new Error('Source compilation and unsigned installation require explicit --build --allow-development.');
  return { dryRun: args.includes('--dry-run') };
}
/**
 * Locate the host npm JavaScript CLI without invoking a shell or downloading a toolchain.
 * @param {object} options Host environment and Node executable.
 * @param {object} env Environment member used for explicit npm selection and PATH lookup.
 * @param {string} node Node executable member used to locate a sibling npm installation.
 * @returns {string} Existing npm-cli.js absolute path.
 * @throws {Error} If no npm CLI is available; JAI_VIEWER_NPM_CLI can select an explicit installation.
 */
export function npmCli({ env = process.env, node = process.execPath } = {}) {
  const candidates = env.JAI_VIEWER_NPM_CLI ? [env.JAI_VIEWER_NPM_CLI] : [join(dirname(node), 'node_modules/npm/bin/npm-cli.js'), join(dirname(node), '../lib/node_modules/npm/bin/npm-cli.js'), ...String(env.PATH ?? '').split(delimiter).flatMap(directory => [join(directory, 'node_modules/npm/bin/npm-cli.js'), join(directory, 'npm')])];
  for (const candidate of candidates) {
    try { const path = realpathSync(candidate); if (path.endsWith('/npm-cli.js') || path.endsWith('\\npm-cli.js')) return path; } catch { /* Try only other existing host candidates; never fetch a replacement. */ }
  }
  throw new Error(`npm >=${MIN_NPM_VERSION} CLI missing. Install the documented host toolchain or set JAI_VIEWER_NPM_CLI to its absolute npm-cli.js.`);
}
/**
 * Describe only the current target's bounded build and verified bootstrap commands.
 * @param {object} options Repository, target, Node/npm paths and a fresh output name.
 * @returns {{program:string,args:string[],cwd:string}[]} Ordered commands; creating this plan has no effects.
 */
export function sourcePlan({ root, target, node, npm, output }) {
  const app = join(root, 'apps/fabric-explorer'); const desktop = join(app, 'desktop'); const contracts = join(app, 'packages/contracts'); const packaging = join(app, 'packaging');
  const version = JSON.parse(readFileSync(join(desktop, 'package.json'), 'utf8')).version;
  const command = (args, cwd = root) => ({ program: node, args, cwd });
  const plan = [command([npm, 'ci', '--ignore-scripts', '--include=dev', '--no-audit', '--no-fund'], contracts), command([join(contracts, 'tools/generate-validators.mjs')], contracts), command([join(contracts, 'node_modules/typescript/bin/tsc'), '-p', join(contracts, 'tsconfig.json')], contracts), command([join(contracts, 'tools/check-built-contracts.mjs')], contracts), command([npm, 'ci', '--ignore-scripts', '--include=dev', '--no-audit', '--no-fund'], desktop), command([join(desktop, 'tools/build.mjs')], desktop), command([join(packaging, 'build-installer.mjs')]), command([join(packaging, 'package.mjs'), target, output]), command([join(packaging, 'bootstrap-sidecars.mjs'), output, '--allow-development'])];
  const archive = `jai-fabric-explorer-${version}-${target}.${target.startsWith('win32') ? 'zip' : 'tar.gz'}`;
  plan.push(target.startsWith('win32') ? { program: 'powershell.exe', args: ['-NoProfile', '-File', join(output, archive + '.install.ps1'), '-AllowDevelopment'], cwd: root } : { program: 'sh', args: [join(output, archive + '.install.sh'), '--allow-development'], cwd: root });
  return plan;
}
/**
 * Execute an explicit source build with stable Node >=24.0.0 and npm >=11.0.0, checking external tools before writes.
 * Package dependencies retain their own engine constraints when npm installs the locked build inputs.
 * @param {string[]} args Exact source-build command arguments.
 * @param {object} ports Injectable host facts/runner/output for deterministic plan and failure tests.
 * @returns {object} Planned commands and dry-run status.
 * @throws {Error} For unsupported hosts, prerequisites, an existing output or the first failed command; no automatic retries.
 */
export function installFromSource(args, ports = {}) {
  const target = currentTarget(ports.platform ?? process.platform, ports.architecture ?? process.arch); const options = sourceOptions(args);
  const root = ports.root ?? repository; const node = ports.node ?? process.execPath; const env = ports.env ?? process.env;
  const nodeVersion = ports.nodeVersion ?? process.versions.node; if (!meetsMinimum(nodeVersion, MIN_NODE_VERSION)) throw new Error(`Source build requires stable Node.js >=${MIN_NODE_VERSION}; found ${nodeVersion}. Set JAI_VIEWER_NODE in the entry script to a supported executable if needed.`);
  const npm = ports.npm ?? npmCli({ env, node }); const npmVersion = ports.npmVersion ?? JSON.parse(readFileSync(resolve(dirname(npm), '../package.json'), 'utf8')).version;
  if (!meetsMinimum(npmVersion, MIN_NPM_VERSION)) throw new Error(`Source build requires stable npm >=${MIN_NPM_VERSION}; found ${npmVersion}. Set JAI_VIEWER_NPM_CLI to a supported npm-cli.js if needed.`);
  const output = ports.output ?? join(root, 'build/fabric-explorer/source-installer', `${target}-${Date.now()}`);
  if (existsSync(output)) throw new Error('Source package output already exists; choose a fresh run instead of overwriting it.');
  const commands = sourcePlan({ root, target, node, npm, output }); const result = { target, development: true, output, dryRun: options.dryRun, requiredTools: target.startsWith('win32') ? ['git', 'tar', 'unzip', 'zip', 'powershell.exe'] : ['git', 'GNU tar', 'unzip'], commands };
  const log = ports.log ?? (value => console.log(value)); log(JSON.stringify(result, null, 2)); if (options.dryRun) return result;
  const run = ports.run ?? ((program, values, cwd) => { const child = spawnSync(program, values, { cwd, stdio: 'inherit', env: { ...env, PATH: dirname(node) + delimiter + String(env.PATH ?? ''), npm_config_ignore_scripts: 'true', ELECTRON_SKIP_BINARY_DOWNLOAD: '1' } }); if (child.error || child.status !== 0) throw new Error(`${program} failed: ${child.error?.message ?? child.status}`); });
  const probe = ports.probe ?? ((program, values) => { const child = spawnSync(program, values, { encoding: 'utf8', env }); if (child.error || child.status !== 0) throw new Error(`Required source-build tool unavailable: ${program}`); return child.stdout + child.stderr; });
  probe('git', ['--version']); const tar = probe('tar', ['--version']); if (!target.startsWith('win32') && !tar.includes('GNU tar')) throw new Error('Source packaging requires GNU tar on PATH (macOS: install GNU tar and prepend its gnubin directory).'); probe('unzip', ['-v']); if (target.startsWith('win32')) { probe('zip', ['-v']); probe('powershell.exe', ['-NoProfile', '-Command', '$PSVersionTable.PSVersion.ToString()']); }
  for (const command of commands) run(command.program, command.args, command.cwd);
  return result;
}
if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  try { installFromSource(process.argv.slice(2)); } catch (error) { console.error(error instanceof Error ? error.message : String(error)); process.exitCode = 1; }
}
