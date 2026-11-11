/** Packaged-local desktop composition; no source-controlled project can choose a runtime executable. */
import { app } from 'electron';
import { join } from 'node:path';
import { startDesktop } from './shell/electron-shell.js';
import { ReadBroker } from './broker/read-broker.js';
import { ImportSession } from './import/session.js';
import { NativeImportWorker } from './import/worker-client.js';

// The main entry is compiled exclusively as a CommonJS bundle.
const directory = __dirname;
void startDesktop({ createBroker: (_paths, registry, writeRoots) => new ReadBroker({ writeRoots, registry }), createImport: (input, broker, paths) => {
  if (!(broker instanceof ReadBroker)) throw new Error('Trusted read broker unavailable.');
  return new ImportSession({ ...input, broker, archiveDirectory: join(paths.temp, 'captures'), workerFactory: () => new NativeImportWorker(join(directory, 'import-worker.cjs')) });
} }, directory).catch(() => { console.error('Fabric Explorer initialization failed.'); app.exit(1); });
