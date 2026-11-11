/** Disposable failed-first SDK geometry regression: spread is dimensionless, not pixel spacing. */
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { createCorpus } from './src/corpus.ts';
// Pure path factory construction needs the WebGL numeric enumeration only; no
// context is created, and this does not provide native paint or picking evidence.
const previous = globalThis.WebGL2RenderingContext;
globalThis.WebGL2RenderingContext = { FLOAT: 0x1406 };
try {
  const { pathCurved } = await import('sigma/rendering');
  const { sigmaOptions } = await import('./src/sigma-options.ts');
  const actual = sigmaOptions().styles.edges.parallelSpread;
  const sdkDirectory = new URL('./node_modules/sigma/dist/', import.meta.url);
  const defaults = readdirSync(sdkDirectory).filter(name => /^types-.+\.esm\.js$/.test(name)).flatMap(name => {
    const found = readFileSync(new URL(name, sdkDirectory), 'utf8').match(/parallelSpread:\s*([\d.]+)/);
    return found ? [Number(found[1])] : [];
  });
  assert.ok(defaults.length, 'Pinned SDK must expose its actual numeric default');
  assert.equal(new Set(defaults).size, 1);
  const standard = defaults[0];
  assert.equal(actual, standard, 'Adapter must use the SDK dimensionless spread default');
  const curve = pathCurved();
  assert.ok(curve.glsl.includes('perp * curvature * len'));
  for (const count of [2, 3, 4]) for (let index = 0; index < count; index++) {
    const curvature = curve.spread.compute(index, count, actual);
    assert.ok(Number.isFinite(curvature));
    assert.equal(curvature, curve.spread.compute(index, count, standard));
    assert.ok(Math.abs(curvature) * 0.5 <= 0.25, 'Parallel midpoint remains within the SDK default proportion of endpoint distance');
  }
  assert.deepEqual(createCorpus('S').edges.slice(0, 4).map(edge => edge.id), ['e0', 'e1', 'e2', 'e3']);
  console.log('PASS: actual pinned SDK default/factory preserves compact dimensionless parallel curvature and edge identity.');
} finally { globalThis.WebGL2RenderingContext = previous; }
