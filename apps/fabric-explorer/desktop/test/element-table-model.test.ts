// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Deterministic finite-window arithmetic and immutable record-reference tests. */
import { describe, expect, it } from 'vitest';
import { ELEMENT_TABLE_PAGE_SIZE, elementTableWindow } from '../src/renderer/element-table-model.js';
import type { ElementTableKind } from '../src/renderer/element-table-model.js';
import { tableProjection } from './element-table-fixtures.js';

describe('bounded element table windows', () => {
  it('distinguishes an unavailable graph from an empty projected table without invented rows', () => {
    expect(elementTableWindow(null, 'vertices', 0)).toMatchObject({ loaded: false, rows: [], total: 0, start: 0, end: 0, page: 0, pageCount: 0 });
    expect(elementTableWindow(tableProjection(0), 'vertices', 99)).toMatchObject({ loaded: true, rows: [], total: 0, start: 0, end: 0, page: 0, pageCount: 0 });
  });
  it.each([1, 24, 25, 26, 50, 51])('keeps every row reachable and mounts at most 25 records for %i vertices', count => {
    const projection = tableProjection(count); const pages = Math.ceil(count / ELEMENT_TABLE_PAGE_SIZE); const ids: string[] = [];
    for (let page = 0; page < pages; page++) {
      const window = elementTableWindow(projection, 'vertices', page);
      expect(window.rows.length).toBeLessThanOrEqual(25); expect(window.pageCount).toBe(pages); expect(window.start).toBe(page * 25); expect(window.end).toBe(Math.min(count, (page + 1) * 25));
      ids.push(...window.rows.map(row => row.id));
    }
    expect(ids).toEqual(projection.vertices.map(vertex => vertex.id));
  });
  it('clamps a retained page after shrinkage and preserves original immutable record identities', () => {
    const projection = tableProjection(26); const window = elementTableWindow(projection, 'vertices', 999);
    expect(window).toMatchObject({ page: 1, start: 25, end: 26 }); expect(window.rows[0]).toBe(projection.vertices[25]); expect(Object.isFrozen(window)).toBe(true); expect(Object.isFrozen(window.rows)).toBe(true);
    expect(elementTableWindow({ ...projection, vertices: projection.vertices.slice(0, 1) }, 'vertices', 1)).toMatchObject({ page: 0, start: 0, end: 1 }); expect(projection.vertices).toHaveLength(26);
  });
  it('handles the maximum bounded projection without mounting the entire vertex or edge set', () => {
    const projection = tableProjection(5000, 20000);
    expect(elementTableWindow(projection, 'vertices', 199)).toMatchObject({ total: 5000, start: 4975, end: 5000, pageCount: 200 });
    const last = elementTableWindow(projection, 'edges', 799); expect(last).toMatchObject({ total: 20000, start: 19975, end: 20000, pageCount: 800 }); expect(last.rows).toHaveLength(25); expect(last.rows[24]).toBe(projection.edges[19999]);
  });
  it.each([-1, 0.5, NaN, Infinity, Number.MAX_SAFE_INTEGER + 1])('rejects malformed page index %s', page => {
    expect(() => elementTableWindow(null, 'vertices', page)).toThrow(RangeError);
  });
  it('rejects unsupported table kinds without admitting another object property', () => {
    expect(() => elementTableWindow(tableProjection(1), 'snapshot' as ElementTableKind, 0)).toThrow(RangeError);
  });
});
