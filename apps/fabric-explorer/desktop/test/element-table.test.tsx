// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Actual component SSR and native callback contracts; browser focus/assistive technology use native journeys. */
import { createElement, isValidElement, useState } from 'react';
import type { ReactElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { elementKey } from '@jai/fabric-explorer-contracts';
import type { Vertex } from '@jai/fabric-explorer-contracts';
import { describe, expect, it, vi } from 'vitest';
import { ElementTable, ElementTableView } from '../src/renderer/element-table.js';
import type { ElementTableProps, ElementTableViewProps } from '../src/renderer/element-table.js';
import { elementTableWindow } from '../src/renderer/element-table-model.js';
import { tableProjection } from './element-table-fixtures.js';

function elements(input: unknown, type: string): ReactElement<Record<string, unknown>>[] {
  if (Array.isArray(input)) return input.flatMap(child => elements(child, type));
  if (!isValidElement(input)) return [];
  const element = input as ReactElement<Record<string, unknown>>;
  return [...(element.type === type ? [element] : []), ...elements(element.props.children, type)];
}
function view(overrides: Partial<ElementTableViewProps> = {}) {
  const props: ElementTableViewProps = { window: elementTableWindow(tableProjection(26), 'vertices', 0), selectedId: null, idPrefix: 'test-elements', onSelect: vi.fn(), onKindChange: vi.fn(), onPageChange: vi.fn(), ...overrides };
  return { props, tree: ElementTableView(props) };
}
describe('keyboard-native semantic element table', () => {
  it.each(['different', 'null', 'shrunk'] as const)('resets retained page state through A → %s → the same immutable A using actual React hooks', transition => {
    const first = tableProjection(26); const middle = transition === 'null' ? null : tableProjection(transition === 'shrunk' ? 1 : 30);
    let phase = 0; const frames: { phase: number; page: number; start: number }[] = [];
    function Mounted() {
      const [, force] = useState(0); const projection = phase < 2 ? first : phase === 2 ? middle : first;
      const tree = ElementTable({ projection, selectedId: null, onSelect() {} });
      frames.push({ phase, page: tree.props.window.page, start: tree.props.window.start });
      if (phase === 0) { phase++; tree.props.onPageChange(1); }
      else if (phase === 1) { phase++; force(2); }
      else if (phase === 2) { phase++; force(3); }
      return tree;
    }
    renderToStaticMarkup(createElement(Mounted));
    expect(frames.find(frame => frame.phase === 1)?.page).toBe(1); expect(frames.filter(frame => frame.phase === 3).every(frame => frame.page === 0 && frame.start === 0)).toBe(true);
  });
  it('renders the real stateful entry with explicit unavailable and empty states', () => {
    function Mounted(props: ElementTableProps) { return ElementTable(props); }
    const unavailable = renderToStaticMarkup(createElement(Mounted, { projection: null, selectedId: null, onSelect() {} }));
    expect(unavailable).toContain('No captured graph is loaded.'); expect(unavailable).toContain('id="element-kind"'); expect(unavailable).not.toContain('data-element-id=');
    const empty = renderToStaticMarkup(createElement(Mounted, { projection: tableProjection(0), selectedId: null, onSelect() {} })); expect(empty).toContain('No visible vertices in this projection.'); expect(empty).toContain('aria-rowcount="1"');
  });
  it('uses a caption, scoped native headers and global counts/row indices for a bounded page', () => {
    const { tree } = view({ window: elementTableWindow(tableProjection(26), 'vertices', 1) }); const html = renderToStaticMarkup(tree);
    expect(elements(tree, 'tbody')[0]?.props.children).toHaveLength(1); expect(html).toContain('aria-rowcount="27"'); expect(html).toContain('aria-rowindex="27"'); expect(html).toContain('Showing 26–26 of 26 visible vertices. Page 2 of 2.');
    expect(html).toContain('<caption>Visible vertices in the current bounded graph projection</caption>'); expect(elements(tree, 'th')).toHaveLength(5); expect(elements(tree, 'th').every(header => header.props.scope === 'col')).toBe(true);
    expect(html.indexOf('<nav')).toBeLessThan(html.indexOf('<table')); expect(html).not.toContain('role="grid"');
  });
  it('keeps duplicate labels distinct through ordinal button names and exact identity details', () => {
    const projection = tableProjection(2); const { tree, props } = view({ window: elementTableWindow(projection, 'vertices', 0), selectedId: projection.vertices[1]!.id });
    const buttons = elements(tree, 'button').filter(button => button.props['data-element-id']); expect(buttons.map(button => button.props['aria-label'])).toEqual(['Inspect vertex 1: Same label', 'Inspect vertex 2: Same label']);
    buttons.forEach((button, index) => { expect(button.props.title).toBe(projection.vertices[index]!.id); expect(button.props['aria-describedby']).toBeUndefined(); (button.props.onClick as () => void)(); });
    expect(props.onSelect).toHaveBeenNthCalledWith(1, projection.vertices[0]!.id); expect(props.onSelect).toHaveBeenNthCalledWith(2, projection.vertices[1]!.id);
    expect(buttons[1]!.props['aria-current']).toBe('true'); expect(renderToStaticMarkup(tree)).toContain('>Selected</td>'); expect(elements(tree, 'details').every(details => details.props.open === undefined)).toBe(true);
    expect(elements(tree, 'code').map(code => code.props.children)).toEqual(projection.vertices.map(vertex => vertex.id));
  });
  it('preserves parallel relation identity, original endpoint direction and inert long text', () => {
    const projection = tableProjection(2, 2); const edge = projection.edges[0]!; const label = '<img src=x onerror=alert(1)> ' + 'long label '.repeat(100);
    const changed = { ...projection, edges: [{ ...edge, label }, projection.edges[1]!] }; const { tree } = view({ window: elementTableWindow(changed, 'edges', 0) }); const html = renderToStaticMarkup(tree);
    expect(elements(tree, 'code').map(code => code.props.children)).toEqual([edge.id, edge.from, edge.to, projection.edges[1]!.id, edge.from, edge.to]);
    expect(html).toContain('&lt;img'); expect(html).not.toContain('<img'); expect(elements(tree, 'button').find(button => button.props['data-element-id'] === edge.id)?.props['aria-label']).toBe(`Inspect relation 1: ${label}`); expect(html).toContain('other-reference');
  });
  it('keeps native page buttons focusable at bounds while guarding no-op actions', () => {
    const first = view(); const firstButtons = elements(first.tree, 'button'); expect(firstButtons[0]!.props['aria-disabled']).toBe(true); expect(firstButtons[0]!.props.disabled).toBeUndefined();
    (firstButtons[0]!.props.onClick as () => void)(); expect(first.props.onPageChange).not.toHaveBeenCalled(); (firstButtons[1]!.props.onClick as () => void)(); expect(first.props.onPageChange).toHaveBeenCalledWith(1);
    const last = view({ window: elementTableWindow(tableProjection(26), 'vertices', 1) }); const lastButtons = elements(last.tree, 'button'); expect(lastButtons[1]!.props['aria-disabled']).toBe(true);
    (lastButtons[1]!.props.onClick as () => void)(); expect(last.props.onPageChange).not.toHaveBeenCalled(); (lastButtons[0]!.props.onClick as () => void)(); expect(last.props.onPageChange).toHaveBeenCalledWith(0);
  });
  it('only forwards supported native table kinds and makes no selection for an off-page ID', () => {
    const { tree, props } = view({ selectedId: 'not-in-this-window' }); const select = elements(tree, 'select')[0]!;
    const change = select.props.onChange as (event: { target: { value: string } }) => void;
    change({ target: { value: 'edges' } }); change({ target: { value: 'unexpected' } }); expect(props.onKindChange).toHaveBeenCalledExactlyOnceWith('edges'); expect(elements(tree, 'button').every(button => button.props['aria-current'] === undefined)).toBe(true); expect(props.onSelect).not.toHaveBeenCalled();
  });
  it('mounts at most 25 semantic rows for the maximum bounded projection', () => {
    const { tree } = view({ window: elementTableWindow(tableProjection(5000, 20000), 'edges', 799) });
    expect(elements(tree, 'button').filter(button => button.props['data-element-id'])).toHaveLength(25); const html = renderToStaticMarkup(tree); expect(html).toContain('aria-rowcount="20001"'); expect(html).toContain('aria-rowindex="20001"'); expect(html).toContain('Page 800 of 800.');
  });
  it('displays applicable finding, unresolved and material states without inventing a universal status', () => {
    const projection = tableProjection(1); const base = projection.vertices[0]!; if (base.identity.kind !== 'version') throw new Error('Version fixture required.');
    const shared = { source: base.source, attributes: base.attributes };
    const findingIdentity = { kind: 'finding' as const, projectId: 'project', ledgerId: 'ledger', findingId: 'F-1' };
    const blobIdentity = { kind: 'blob' as const, projectId: 'project', rootId: 'root', blobId: 'a'.repeat(64) };
    const useIdentity = { kind: 'use' as const, projectId: 'project', ref: base.identity.ref, useScope: 'consumer-scope' };
    const rows: Vertex[] = [
      { ...shared, source: { ...base.source, family: 'findings' }, kind: 'finding', id: elementKey(findingIdentity), identity: findingIdentity, label: 'Finding', state: 'verified', severity: 'medium', findingKind: 'defect', rounds: '0', recordedExpiry: null },
      { ...shared, kind: 'unresolved', id: base.id, identity: base.identity, label: 'Missing exact version', reason: 'missing-reference' },
      { ...shared, kind: 'blob', id: elementKey(blobIdentity), identity: blobIdentity, label: 'Material', availability: 'missing' },
      { ...shared, kind: 'use', id: elementKey(useIdentity), identity: useIdentity, label: 'Use point' },
    ];
    const { tree } = view({ window: elementTableWindow({ ...projection, vertices: rows }, 'vertices', 0) }); const html = renderToStaticMarkup(tree);
    expect(html).toContain('>verified</td>'); expect(html).toContain('>missing-reference</td>'); expect(html).toContain('>missing</td>'); expect(html).toContain('>Not applicable</td>'); expect(html).toContain('F-1 · ledger ledger'); expect(html).toContain('use scope consumer-scope');
  });
  it('uses an exact-key display alias without changing selection or discarding the original source label', () => {
    const projection = tableProjection(1); const original = projection.vertices[0]!; const raw = 'a'.repeat(64); const changed = { ...projection, vertices: [{ ...original, label: raw }] };
    const { tree, props } = view({ window: elementTableWindow(changed, 'vertices', 0), labels: new Map([[original.id, 'Readable source title']]) });
    const button = elements(tree, 'button').find(item => item.props['data-element-id'] === original.id)!; expect(button.props.children).toBe('Readable source title'); (button.props.onClick as () => void)(); expect(props.onSelect).toHaveBeenCalledWith(original.id);
    expect(renderToStaticMarkup(tree)).toContain(raw); expect(changed.vertices[0]!.label).toBe(raw);
  });
});
