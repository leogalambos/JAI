/** One outstanding existing-state poll; late completion cannot update a replaced UI operation. */
import type { ImportProgress } from '../import/progress.js';
/**
 * Poll only while an import is displayed, without reloading presentation data.
 * @param read Existing bounded shell-state progress read.
 * @param accept Current operation's progress observer.
 * @returns Cleanup that stops the timer and discards in-flight results.
 */
export function pollImportProgress(read: () => Promise<ImportProgress | undefined>, accept: (value: ImportProgress) => void): () => void {
  let active = true; let pending = false;
  const poll = async () => { if (!active || pending) return; pending = true; try { const value = await read(); if (active && value) accept(value); } catch { /* The owning import request reports failures; progress is observational. */ } finally { pending = false; } };
  const timer = setInterval(() => { void poll(); }, 1000); void poll();
  return () => { active = false; clearInterval(timer); };
}
