// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Development-only synthetic sources and fixed production composition for native accessibility checks. */
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { app, BrowserWindow } from 'electron';
import { startDesktop } from '../src/shell/electron-shell.js';
import { ReadBroker } from '../src/broker/read-broker.js';
import { ImportSession } from '../src/import/session.js';
import { NativeImportWorker } from '../src/import/worker-client.js';

/** Fixed fixture destinations; none is supplied by a renderer or an imported project. */
export interface AccessibilityFixture {
  readonly root: string;
  readonly fabric: string;
  readonly findings: string;
  readonly originalFabric: Buffer;
  readonly originalFindings: Buffer;
  readonly configuration: { executable: string; coreTools: string };
}
/**
 * Create isolated synthetic sources before starting the production shell.
 * @param directory Compiled development helper directory.
 * @param output Private observation destination chosen by the runner.
 * @returns Exact fixture paths and unchanged-byte references.
 */
export function accessibilityFixture(directory: string, output: string): AccessibilityFixture {
  const repository = resolve(directory, '../../../..');
  // This interpreter prepares synthetic inputs only; the viewer imports through Node.
  const configuration = { executable: join(repository, 'build/fabric-explorer/helper-venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python'), coreTools: join(repository, '.ai/runtime/tools') };
  const root = join(output, 'synthetic-source'); mkdirSync(root, { mode: 0o700 });
  const created = JSON.parse(execFileSync(configuration.executable, ['-I', '-B', join(repository, 'apps/fabric-explorer/reader/test/make_fabric_fixture.py'), root], { timeout: 20000, maxBuffer: 1024 * 1024, encoding: 'utf8' })) as { filename: string };
  const fabric = join(root, created.filename); const findings = join(root, 'review.jsonl');
  writeFileSync(findings, readFileSync(join(repository, 'apps/fabric-explorer/test/fixtures/findings-review.jsonl')), { mode: 0o600 });
  const application = join(output, 'application'); mkdirSync(application, { mode: 0o700 }); app.setPath('appData', application);
  return { root, fabric, findings, configuration, originalFabric: readFileSync(fabric), originalFindings: readFileSync(findings) };
}
/**
 * Start the fixed application with real dialogs or an explicitly synthetic automatic picker.
 * @param directory Fixed compiled application directory.
 * @param fixture Test-only source destinations.
 * @param realDialogs True only for the manual native-dialog and Orca observations.
 * @returns The actual production window, with sandbox and bridge policy unchanged.
 */
export async function accessibilityHost(directory: string, fixture: AccessibilityFixture, realDialogs: boolean): Promise<BrowserWindow> {
  await startDesktop({
    ...(realDialogs ? {} : { picker: { project: async () => fixture.root, files: async (family: string) => [family === 'findings' ? fixture.findings : fixture.fabric] } }),
    createBroker: (_paths, registry, writeRoots) => new ReadBroker({ registry, writeRoots }),
    createImport: (input, broker, paths) => {
      if (!(broker instanceof ReadBroker)) throw new Error('Expected the fixed native read broker');
      return new ImportSession({ ...input, broker, archiveDirectory: join(paths.temp, 'captures'), workerFactory: () => new NativeImportWorker(join(directory, 'import-worker.cjs')) });
    },
  }, directory);
  const window = BrowserWindow.getAllWindows()[0]; if (!window) throw new Error('Production window unavailable');
  window.setSize(1440, 1100); return window;
}
/**
 * Append one maintained canonical event to the synthetic findings fixture only.
 * @param fixture Trusted fixture constructed by this helper.
 * @returns Nothing; the viewer itself never writes sources.
 */
export function prepareValidRefresh(fixture: AccessibilityFixture): void {
  execFileSync(fixture.configuration.executable, ['-I', '-B', '-c', "import os,sys; os.environ['FINDINGS_HOME']=sys.argv[2]; sys.dont_write_bytecode=True; sys.path.insert(0,sys.argv[1]); import findings; events=findings.load('review'); findings.append('review',events,[{'op':'resolve','id':'F-0001','by':'synthetic-accessibility-author','note':'Synthetic accessibility refresh','ref':None}])", fixture.configuration.coreTools, fixture.root], { timeout: 10000 });
}
