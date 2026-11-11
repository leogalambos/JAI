/** Main-only project source lookup; file admission remains owned by the read broker. */
import type { SourceFamily } from '@jai/fabric-explorer-contracts';
import { lstat, opendir } from 'node:fs/promises';
import { join } from 'node:path';
import type { PickerPort } from './controller.js';

/** Trusted native dialog adapter; paths remain in the main process. */
export interface SourceDialogs {
  /** Select a project association directory; null means cancellation. */
  project(): Promise<string | null>;
  /**
   * Select explicit files, initially browsing the selected project or its family directory.
   * @param family Requested source family.
   * @param defaultPath Initial native dialog directory, never inferred from cwd.
   * @returns Selected paths or null on cancellation.
   * @throws {Error} If the native dialog cannot be opened.
   */
  files(family: SourceFamily, defaultPath: string): Promise<readonly string[] | null>;
}

/**
 * Compose project selection and source selection without exposing native paths to the renderer.
 * @param dialogs Trusted native directory and file dialogs.
 * @returns Main-owned picker using complete sorted direct regular `.jsonl` lists in
 * project `.fabric`/`.findings`, or manual selection when lookup is unavailable.
 * Lookup reads directory metadata only, stops beyond 4096 entries or the remaining
 * source capacity, and never follows candidate links or returns a partial list.
 * @throws {Error} Invalid capacity or native dialog failures propagate to the shell boundary.
 */
export function createSourcePicker(dialogs: SourceDialogs): PickerPort {
  return {
    project: () => dialogs.project(),
    files: async (family, projectPath, maximumFiles, signal) => {
      if (!Number.isInteger(maximumFiles) || maximumFiles < 0 || maximumFiles > 128) throw new Error('Invalid source selection capacity');
      if (signal.aborted) return null;
      let defaultPath = projectPath;
      if (family === 'fabric' || family === 'findings') {
        const directory = join(projectPath, family === 'fabric' ? '.fabric' : '.findings');
        try {
          const info = await lstat(directory);
          if (info.isDirectory() && !info.isSymbolicLink()) {
            defaultPath = directory;
            if (maximumFiles > 0 && !signal.aborted) {
              const candidates: string[] = []; let entries = 0; let complete = true;
              for await (const entry of await opendir(directory)) {
                if (signal.aborted) return null;
                if (++entries > 4096) { complete = false; break; }
                if (entry.isFile() && entry.name.endsWith('.jsonl')) candidates.push(join(directory, entry.name));
                if (candidates.length > maximumFiles) { complete = false; break; }
              }
              if (complete && candidates.length && !signal.aborted) return candidates.sort();
            }
          }
        } catch {
          // A lookup is only a convenience; existing broker admission owns file validation.
          defaultPath = projectPath;
        }
      }
      return signal.aborted ? null : dialogs.files(family, defaultPath);
    },
  };
}
