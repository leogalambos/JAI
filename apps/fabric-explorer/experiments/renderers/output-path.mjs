/** Disposable result-path boundary: raw host observations never enter a public checkout tree. */
import { realpathSync, existsSync } from 'node:fs';
import { resolve, relative, isAbsolute, sep, dirname, basename } from 'node:path';

function canonicalDestination(candidate) {
  let current = resolve(candidate);
  const remaining = [];
  while (!existsSync(current)) {
    const parent = dirname(current);
    if (parent === current) throw new Error('Output destination has no existing ancestor');
    remaining.unshift(basename(current)); current = parent;
  }
  return resolve(realpathSync(current), ...remaining);
}
function within(parent, child) {
  const value = relative(parent, child);
  return value === '' || (!isAbsolute(value) && value !== '..' && !value.startsWith('..' + sep));
}
/**
 * Admit raw observations only outside public checkout paths or in ignored scratch.
 * @param {string} candidate Explicit operator-selected output directory.
 * @param {string} experimentDirectory Existing disposable experiment directory.
 * @returns {string} Canonical destination with existing symlink aliases resolved.
 * @throws {Error} If the destination would expose results in a public tree.
 */
export function admitOutput(candidate, experimentDirectory) {
  const experiment = realpathSync(experimentDirectory);
  const repository = realpathSync(resolve(experiment, '../../../..'));
  const output = canonicalDestination(candidate);
  const allowedBuild = resolve(repository, 'build');
  const allowedOut = resolve(experiment, 'out');
  if (within(output, repository) || (within(repository, output) && !within(allowedBuild, output) && !within(allowedOut, output))) {
    throw new Error('Raw results require storage outside the checkout, root build/, or ignored experiment out/');
  }
  return output;
}
