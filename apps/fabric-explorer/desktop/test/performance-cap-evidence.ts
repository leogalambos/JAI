// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Bounded development-only capture of the fixed helper failure record after process disposal. */
import { constants } from 'node:fs';
import { open } from 'node:fs/promises';
import { join } from 'node:path';

/**
 * Read only the fixed private diagnostic file, without following a linked final component.
 * @param directory Owned helper working directory after helper quiescence.
 * @returns Exact bounded bytes, or null when no failure record was written.
 * @throws {Error} For linked, nonregular, nonprivate, oversized or foreign-owned records.
 */
export async function readCapEvidence(directory: string): Promise<Buffer | null> {
  let handle;
  try { handle = await open(join(directory, 'semantic-cap-diagnostic.json'), constants.O_RDONLY | (constants.O_NOFOLLOW ?? 0) | (constants.O_NONBLOCK ?? 0)); }
  catch (error) { if ((error as NodeJS.ErrnoException).code === 'ENOENT') return null; throw error; }
  try {
    const info = await handle.stat();
    if (!info.isFile() || info.nlink !== 1 || info.size < 1 || info.size > 16385 || process.platform !== 'win32' && ((info.mode & 0o077) !== 0 || process.getuid && info.uid !== process.getuid())) throw new Error('Invalid private cap diagnostic record.');
    const bytes = Buffer.alloc(16385); const read = await handle.read(bytes, 0, bytes.length, 0);
    if (read.bytesRead !== info.size) throw new Error('Cap diagnostic record changed.');
    const extra = Buffer.alloc(1); if ((await handle.read(extra, 0, 1, read.bytesRead)).bytesRead) throw new Error('Cap diagnostic record exceeds its bound.');
    return bytes.subarray(0, read.bytesRead);
  } finally { await handle.close(); }
}
