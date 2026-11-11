/** Prepare one pinned upstream SDK plus the maintained patch; never invoked by the installed viewer. */
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync, renameSync, rmSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
const desktop = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const recipe = resolve(desktop, 'vendor/sigma');
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
/**
 * Materialize a verified fixed source archive only on a missing prepared cache.
 * @param offline Require an already prepared matching source cache without network access.
 * @returns The ignored prepared upstream source root.
 * @throws {Error} For cache/pin mismatch, unavailable network/tools, or failed source preparation.
 */
export async function prepareSigma({ offline = false } = {}) {
  const provenance = JSON.parse(readFileSync(resolve(recipe, 'provenance.json'), 'utf8'));
  const patch = resolve(recipe, 'label-programs.patch');
  if (sha256(readFileSync(patch)) !== provenance.patchSha256) throw new Error('Sigma patch differs from its recorded pin.');
  const pin = sha256(JSON.stringify([provenance.upstream.commit, provenance.upstream.sourceArchiveSha256, provenance.patchSha256, provenance.maintainedVersion]));
  const source = resolve(recipe, '.cache/upstream'); const marker = resolve(source, '.jai-prepared.json');
  if (existsSync(source)) {
    const prepared = existsSync(marker) ? JSON.parse(readFileSync(marker, 'utf8')) : null;
    if (prepared?.format !== 'jai.sigma-prepared/1' || prepared.pin !== pin) throw new Error('Prepared Sigma cache differs from the recipe; remove only the generated .cache/upstream cache before explicit preparation.');
    console.log('Sigma SDK: reusing prepared source cache; no download or source reconstruction.'); return source;
  }
  if (offline) throw new Error('Sigma source cache is missing; run npm run prepare:sdk before an offline build.');
  const url = `https://codeload.github.com/jacomyal/sigma.js/tar.gz/${provenance.upstream.commit}`;
  console.log(`Sigma SDK: downloading pinned upstream source ${provenance.upstream.commit}; no install hooks.`);
  mkdirSync(resolve(recipe, '.cache'), { recursive: true });
  const stage = mkdtempSync(resolve(recipe, '.cache/stage-'));
  try {
    const response = await fetch(url, { signal: AbortSignal.timeout(60000) });
    if (!response.ok || !response.body) throw new Error('Pinned Sigma source download failed.');
    const chunks = []; let length = 0;
    for await (const chunk of response.body) { length += chunk.length; if (length > 64 * 1024 * 1024) throw new Error('Sigma source archive exceeds the build download bound.'); chunks.push(chunk); }
    const bytes = Buffer.concat(chunks);
    if (sha256(bytes) !== provenance.upstream.sourceArchiveSha256) throw new Error('Sigma source archive differs from its recorded SHA256.');
    const archive = resolve(stage, 'source.tar.gz'); writeFileSync(archive, bytes, { mode: 0o600 });
    const extracted = resolve(stage, 'source'); mkdirSync(extracted);
    const unpacked = spawnSync('tar', ['-xzf', archive, '--strip-components=3', '-C', extracted, `sigma.js-${provenance.upstream.commit}/packages/sigma`], { stdio: 'inherit' });
    if (unpacked.status !== 0) throw new Error('Sigma extraction failed; developer builds require tar.');
    const patched = spawnSync('git', ['apply', '--no-index', patch], { cwd: extracted, stdio: 'inherit' });
    if (patched.status !== 0) throw new Error('Sigma patch failed; developer builds require git.');
    for (const [name, expected] of Object.entries(provenance.sourceSha256)) {
      if (sha256(readFileSync(resolve(extracted, name))) !== expected) throw new Error(`Prepared Sigma source differs from its recorded pin: ${name}`);
    }
    writeFileSync(resolve(extracted, '.jai-prepared.json'), JSON.stringify({ format: 'jai.sigma-prepared/1', pin }) + '\n', { flag: 'wx', mode: 0o600 });
    renameSync(extracted, source);
    console.log('Sigma SDK: fixed archive, patch and prepared source hashes verified.'); return source;
  } finally { rmSync(stage, { recursive: true, force: true }); }
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const arguments_ = process.argv.slice(2); if (arguments_.some(value => value !== '--offline') || arguments_.length > 1) throw new Error('Usage: prepare-sigma.mjs [--offline]');
  await prepareSigma({ offline: arguments_.includes('--offline') });
}
