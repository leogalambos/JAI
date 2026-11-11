/** Failed-first view lifecycle regression; no native resource or latency claim. */
import assert from 'node:assert/strict';
import { createViewController } from './src/view-controller.ts';
let created = 0; let killed = 0; let replaced = 0; let view;
const controller = createViewController(next => { created++; view = next; return { destroy: () => killed++, replace: value => { replaced++; view = value; } }; });
for (const name of ['default', 'expanded', 'grouped', 'reset', 'feature']) controller.set(name);
assert.equal(created, 1, 'Graph-only transitions must retain the same replace-capable renderer');
assert.equal(replaced, 4); assert.equal(killed, 0); assert.equal(view, 'feature');
controller.dispose(); controller.dispose(); assert.equal(killed, 1);
console.log('PASS: one renderer, four graph switches, final-only idempotent disposal.');
