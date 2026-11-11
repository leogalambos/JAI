// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Application-only import lifecycle metadata and trusted resource budgets. */
import type { Diagnostic, SnapshotDescriptor } from '@jai/fabric-explorer-contracts';

/** Trusted application limits; renderer requests cannot enlarge them. */
export interface ImportLimits { readonly encodedGraphBytes: number; readonly vertices: number; readonly edges: number; readonly diagnostics: number }
/** Candidate bounds, counting all provenance and unresolved elements rather than only visible records. */
export const DEFAULT_IMPORT_LIMITS: ImportLimits = Object.freeze({ encodedGraphBytes: 512 * 1024 * 1024, vertices: 100_000, edges: 500_000, diagnostics: 1000 });
/** An observed source-format outcome; findings deliberately have no invented envelope version. */
export interface SupportedVersion { readonly sourceId: string; readonly family: string; readonly declaredFormat: string | null; readonly declaredProtocol: string | null; readonly supported: boolean; readonly adapterVersion: string }
/** Known failed-source scope without a fabricated verified revision or native pathname. */
export interface DiagnosticContext { readonly sourceId: string | null; readonly pointer: string; readonly sequence: string | null }
/** Finite import outcome distinct from authority, fresh assessment and global transaction consistency. */
export interface ImportReport {
  readonly status: 'ready' | 'failed' | 'cancelled';
  readonly selectedSources: string; readonly acceptedSources: string; readonly rejectedSources: string;
  readonly vertices: string; readonly edges: string; readonly unresolvedVertices: string; readonly skippedItems: string;
  readonly diagnosticTotal: string; readonly diagnostics: readonly Diagnostic[];
  readonly diagnosticContexts?: readonly DiagnosticContext[]; readonly supportedVersions: readonly SupportedVersion[];
  readonly observation: 'observed-revision-set'; readonly limitation: string | null;
}
/** Main-side public import state; graph arrays never leave their owning worker. */
export interface ImportState { readonly snapshot: SnapshotDescriptor | null; readonly report: ImportReport | null; readonly stale: boolean; readonly progress?: import('./progress.js').ImportProgress }
/** Bounded typed candidate failure; native paths and arbitrary exception messages are never exposed. */
export class ImportError extends Error {
  /**
   * Construct a typed application-owned failure.
   * @param code Consumer-compatible diagnostic category.
   * @param message Fixed application-authored explanation.
   * @param report Optional failed helper/import report, never an accepted partial model.
   */
  constructor(readonly code: Diagnostic['code'], message: string, readonly report: ImportReport | null = null) { super(message); this.name = 'ImportError'; }
}
/**
 * Validate deliberate app-only limits without allowing unbounded allocations.
 * @param value Trusted application configuration, never unchecked renderer input.
 * @returns Frozen detached positive limits no larger than maintained hard ceilings.
 * @throws {ImportError} For invalid or excessive resource bounds.
 */
export function importLimits(value: ImportLimits = DEFAULT_IMPORT_LIMITS): ImportLimits {
  for (const key of ['encodedGraphBytes', 'vertices', 'edges', 'diagnostics'] as const) if (!Number.isSafeInteger(value[key]) || value[key] < 1 || value[key] > DEFAULT_IMPORT_LIMITS[key]) throw new ImportError('resource-limit', 'Invalid import resource limits.');
  return Object.freeze({ encodedGraphBytes: value.encodedGraphBytes, vertices: value.vertices, edges: value.edges, diagnostics: value.diagnostics });
}
