/** Disposable regression checks for raw-observation privacy, including public sibling and symlink aliases. */
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, symlinkSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { admitOutput } from './output-path.mjs';

const root = mkdtempSync(join(tmpdir(), 'renderer-output-boundary-'));
const experiment = join(root, 'apps/fabric-explorer/experiments/renderers');
try {
  mkdirSync(experiment, { recursive: true });
  mkdirSync(join(root, 'docs'));
  for (const denied of [root, experiment, join(experiment, 'public-results'), join(root, 'apps/public-results'), join(root, 'docs/results')]) {
    assert.throws(() => admitOutput(denied, experiment));
  }
  assert.equal(admitOutput(join(root, 'build/results'), experiment), join(root, 'build/results'));
  assert.equal(admitOutput(join(experiment, 'out/results'), experiment), join(experiment, 'out/results'));
  assert.equal(admitOutput(join(tmpdir(), 'external-renderer-results'), experiment), join(tmpdir(), 'external-renderer-results'));
  const linkType = process.platform === 'win32' ? 'junction' : 'dir';
  symlinkSync(join(root, 'docs'), join(experiment, 'out'), linkType);
  symlinkSync(join(root, 'docs'), join(root, 'build'), linkType);
  assert.throws(() => admitOutput(join(experiment, 'out/results'), experiment));
  assert.throws(() => admitOutput(join(root, 'build/results'), experiment));
  console.log('PASS: public checkout/sibling paths and ignored-root aliases rejected; explicit scratch roots admitted.');
} finally {
  rmSync(root, { recursive: true, force: true });
}
