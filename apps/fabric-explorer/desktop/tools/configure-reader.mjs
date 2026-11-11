/** Compatibility command: validate the fixed direct-import worker without a Python runtime configuration. */
import { access } from 'node:fs/promises';
import { constants } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

if (process.argv.length > 2) throw new Error('Development worker paths are fixed by this application checkout');
const directory = resolve(dirname(fileURLToPath(import.meta.url)), '..');
await access(resolve(directory, 'dist/import-worker.cjs'), constants.R_OK);
console.log('Validated the fixed direct TypeScript import worker; no Python runtime configuration.');
