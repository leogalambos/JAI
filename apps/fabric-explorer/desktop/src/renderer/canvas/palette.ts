// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Resolved presentation-only colors; no CSS, source semantics or native bridge dependency. */
/** Closed resolved hex RGB palette supplied by the application's theme owner. */
export interface CanvasPalette {
  readonly background: string;
  readonly node: string;
  readonly finding: string;
  readonly unresolved: string;
  readonly edge: string;
  readonly selected: string;
  readonly labelBackground: string;
  readonly labelText: string;
  readonly labelBorder: string;
}
/** Default light appearance used until the root supplies its resolved theme. */
export const DEFAULT_CANVAS_PALETTE: CanvasPalette = Object.freeze({ background: '#f8fafc', node: '#235d91', finding: '#9b2c65', unresolved: '#8a5815', edge: '#65768a', selected: '#123a63', labelBackground: '#ffffff', labelText: '#162b43', labelBorder: '#66788a' });
/**
 * Validate and snapshot a closed resolved palette before applying any display change.
 * @param input Exactly the nine named hex RGB color fields, with no unresolved CSS values.
 * @returns Frozen detached palette; later caller mutations cannot change active rendering.
 * @throws {Error} For missing/extra fields or invalid RGB syntax; the old canvas palette is unaffected.
 */
export function canvasPalette(input: unknown): CanvasPalette {
  const names = Object.keys(DEFAULT_CANVAS_PALETTE).sort();
  if (!input || typeof input !== 'object' || Array.isArray(input) || Object.keys(input).sort().join() !== names.join()) throw new Error('Invalid canvas palette');
  const values = input as Record<string, unknown>;
  if (names.some(name => typeof values[name] !== 'string' || !/^#[0-9a-fA-F]{6}$/.test(values[name] as string))) throw new Error('Invalid canvas palette color');
  return Object.freeze(Object.fromEntries(names.map(name => [name, values[name]]))) as unknown as CanvasPalette;
}
