// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Actual filesystem bounds and link rejection for private helper diagnostics. */
import { expect, it } from 'vitest';
import { mkdtemp, rm, writeFile, symlink, chmod } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { readCapEvidence } from './performance-cap-evidence.js';

it('reads the inclusive private bound, preserves absence and rejects excess or links', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'jai-cap-evidence-')); const file = join(directory, 'semantic-cap-diagnostic.json');
  try {
    expect(await readCapEvidence(directory)).toBeNull();
    const bytes = Buffer.alloc(16385, 32); await writeFile(file, bytes, { mode: 0o600 });
    expect(await readCapEvidence(directory)).toEqual(bytes);
    await writeFile(file, Buffer.alloc(16386)); await expect(readCapEvidence(directory)).rejects.toThrow('Invalid private');
    await rm(file); const other = join(directory, 'other'); await writeFile(other, '{}', { mode: 0o600 }); await symlink(other, file);
    await expect(readCapEvidence(directory)).rejects.toThrow();
  } finally { await rm(directory, { recursive: true, force: true }); }
});
it('rejects publicly readable records on Unix', async () => {
  if (process.platform === 'win32') return;
  const directory = await mkdtemp(join(tmpdir(), 'jai-cap-mode-')); const file = join(directory, 'semantic-cap-diagnostic.json');
  try { await writeFile(file, '{}', { mode: 0o600 }); await chmod(file, 0o644); await expect(readCapEvidence(directory)).rejects.toThrow('Invalid private'); }
  finally { await rm(directory, { recursive: true, force: true }); }
});
