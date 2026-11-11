// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Finite native-table render windows over an already bounded, immutable graph projection. */
import type { Edge, GraphProjection, Vertex } from '@jai/fabric-explorer-contracts';

/** Select the original vertex or relation ordering without conflating labels with identities. */
export type ElementTableKind = 'vertices' | 'edges';
/** Maximum mounted data rows; pagination reaches every row of the bounded projection. */
export const ELEMENT_TABLE_PAGE_SIZE = 25;
/** Existing immutable record references and zero-based window boundaries; end is exclusive. */
export interface ElementTableWindow {
  readonly kind: ElementTableKind;
  readonly loaded: boolean;
  readonly rows: readonly (Vertex | Edge)[];
  readonly total: number;
  readonly start: number;
  readonly end: number;
  readonly page: number;
  readonly pageCount: number;
}

/**
 * Select at most 25 rows without cloning semantic records or inspecting the whole snapshot.
 * @param projection Trusted current bounded projection, or null before a graph is available.
 * @param kind Vertex or relation table; original projection ordering is retained.
 * @param page Requested nonnegative integer page index, clamped after projection shrinkage.
 * @returns Frozen finite window; an empty table has page zero and pageCount zero.
 * @throws {RangeError} For unsupported kinds or negative, fractional or nonfinite page indices.
 */
export function elementTableWindow(projection: GraphProjection | null, kind: ElementTableKind, page: number): ElementTableWindow {
  if (kind !== 'vertices' && kind !== 'edges' || !Number.isSafeInteger(page) || page < 0) throw new RangeError('Invalid element table window.');
  const rows = projection?.[kind] ?? []; const total = rows.length; const pageCount = Math.ceil(total / ELEMENT_TABLE_PAGE_SIZE);
  const current = Math.min(page, Math.max(0, pageCount - 1)); const start = current * ELEMENT_TABLE_PAGE_SIZE; const end = Math.min(total, start + ELEMENT_TABLE_PAGE_SIZE);
  return Object.freeze({ kind, loaded: projection !== null, rows: Object.freeze(rows.slice(start, end)), total, start, end, page: current, pageCount });
}
