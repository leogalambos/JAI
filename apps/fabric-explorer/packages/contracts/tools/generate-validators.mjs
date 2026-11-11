/** Build-only schema compiler: emit static ESM validators so renderer imports never require unsafe-eval. */
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, dirname } from 'node:path';
import { Ajv2020 } from 'ajv/dist/2020.js';
import standalone from 'ajv/dist/standalone/index.js';

const directory = dirname(fileURLToPath(import.meta.url));
const argument = process.argv[2];
if (process.argv.length > 3 || (argument !== undefined && !argument.startsWith('--output='))) throw new Error('Only --output=<directory> is supported');
const output = argument ? resolve(argument.slice('--output='.length)) : resolve(directory, '../generated');
const schema = JSON.parse(await readFile(resolve(directory, '../schema/contracts.schema.json'), 'utf8'));
const names = ['elementIdentity', 'edgeIdentity', 'stableLocator', 'sourceLocator', 'vertex', 'edge', 'verification', 'sourceRevision', 'snapshot', 'projection', 'overlayTarget', 'request', 'response', 'rejection', 'binding', 'cursor', 'adapterInput', 'adapterChunk', 'attributes', 'bytePage', 'responseChunk'];
const ajv = new Ajv2020({ strict: true, allErrors: false, code: { source: true, esm: true, lines: true } });
ajv.addSchema(schema);
const exports = Object.fromEntries(names.map(name => [name, `${schema.$id}#/$defs/${name}`]));
let source = standalone.default ? standalone.default(ajv, exports) : standalone(ajv, exports);
// Ajv's pinned standalone emitter uses CJS snippets for these pure runtime
// helpers even in ESM output. Replace only known literal dependencies at build
// time; importing generated code must need neither require nor a Node shim.
const helpers = new Map();
source = source.replace(/require\("ajv\/dist\/runtime\/([a-z0-9_-]+)"\)(\.default)?/gi, (_match, name) => {
  const allowed = new Set(['ucs2length', 'equal']);
  if (!allowed.has(name)) throw new Error(`Unreviewed standalone helper: ${name}`);
  const identifier = `runtime_${name}`; helpers.set(name, identifier);
  return identifier;
});
if (/\brequire\s*\(/.test(source) || /\bnew Function\b|\beval\s*\(/.test(source)) throw new Error('Standalone output is not CSP-safe static ESM');
const imports = [...helpers].map(([name, identifier]) => `import ${identifier}_module from 'ajv/dist/runtime/${name}.js';\nconst ${identifier} = typeof ${identifier}_module === 'function' ? ${identifier}_module : ${identifier}_module.default;`).join('\n');
await mkdir(output, { recursive: true });
await writeFile(resolve(output, 'validators.js'), `// Generated from the published contracts schema; do not edit.\n${imports}\n${source}\n`);
await writeFile(resolve(output, 'validators.d.ts'), names.map(name => `export declare function ${name}(value: unknown): boolean;`).join('\n') + '\n');
console.log(`Generated ${names.length} static contract validators.`);
