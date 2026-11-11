// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** One explicit source-opening action owns selection, fresh admission state and automatic loading. */
import type { Binding, SourceFamily } from '@jai/fabric-explorer-contracts';
import type { DesktopBridge } from '../shell/bridge.js';
import type { ShellState } from '../shell/controller.js';

/** Current main-owned request context; cancellation never reuses an earlier renderer binding. */
export interface SourceWork { readonly id: string; readonly kind: 'selection' | 'import'; readonly binding: Binding }
/** User-visible completion category; main-owned state remains the authority for retained snapshots. */
export type OpenSourcesResult = 'ready' | 'selection-incomplete' | 'selection-failed' | 'no-sources' | 'cancelled' | 'import-rejected' | 'import-failed';
/** Narrow operation dependencies and renderer lifetime, with no native paths. */
export interface OpenSourcesOptions {
  readonly api: Pick<DesktopBridge, 'pickRoots' | 'importSnapshot'>;
  readonly initial: ShellState;
  readonly families: readonly SourceFamily[];
  readonly selectionId: string;
  readonly importId: string;
  readonly signal: AbortSignal;
  /** Publish fresh main state at admission and after import; failures propagate into the result. */
  readonly refresh: () => Promise<ShellState>;
  /** Publish the actual import context before the request starts, for progress and cancellation. */
  readonly onImport: (work: SourceWork) => void;
  /** Mark the current main request settled before state/presentation refresh; this callback must not throw. */
  readonly onRequestSettled?: () => void;
}

/**
 * Open the selected families and immediately load the freshly admitted sources exactly once.
 * @param options Existing bridge, initial selection session, request IDs and publication callbacks.
 * @returns A completion category; cancelled, failed or empty selection never starts an import.
 * @throws No expected bridge or state-read failure escapes; the result reports its owning phase.
 */
export async function openAndLoadSources(options: OpenSourcesOptions): Promise<OpenSourcesResult> {
  const { api, initial, families, selectionId, refresh, signal } = options;
  if (signal.aborted) return 'cancelled';
  let stateRead = false; let importing = false; let result: OpenSourcesResult = 'selection-failed';
  try {
    let selected: { status: string };
    try { selected = await api.pickRoots({ sessionId: initial.sessionId, capability: null, generation: null }, selectionId, families) as { status: string }; }
    finally { options.onRequestSettled?.(); }
    stateRead = true; const admitted = await refresh();
    if (signal.aborted) return 'cancelled';
    if (selected.status !== 'ok') return 'selection-incomplete';
    if (!admitted.capability || !admitted.sources.length) return 'no-sources';
    const work: SourceWork = { id: options.importId, kind: 'import', binding: { sessionId: admitted.sessionId, capability: admitted.capability, generation: admitted.snapshot?.generation ?? null } };
    options.onImport(work);
    if (signal.aborted) return 'cancelled';
    importing = true;
    let loaded: { status: string };
    try { loaded = await api.importSnapshot(work.binding, work.id, admitted.sources.map(source => source.sourceId)) as { status: string }; }
    finally { options.onRequestSettled?.(); }
    result = loaded.status === 'ok' ? 'ready' : signal.aborted ? 'cancelled' : 'import-rejected';
  } catch { result = signal.aborted ? 'cancelled' : importing ? 'import-failed' : 'selection-failed'; }
  finally {
    if (importing || !stateRead) {
      try { await refresh(); } catch { result = importing ? 'import-failed' : 'selection-failed'; }
    }
  }
  return result;
}
