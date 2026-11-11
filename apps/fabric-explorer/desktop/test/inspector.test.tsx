// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Literal inspector markup checks; interactive navigation is covered by native DOM journeys. */
import { createElement, isValidElement, useState } from 'react';
import type { ReactElement } from 'react';
import { describe, expect, it, vi } from 'vitest';
import { renderToStaticMarkup } from 'react-dom/server';
import { edgeKey, elementKey } from '@jai/fabric-explorer-contracts';
import type { Edge, Vertex } from '@jai/fabric-explorer-contracts';
import type { InspectorProps } from '../src/renderer/inspector.js';
import { Inspector } from '../src/renderer/inspector.js';
import { revision } from './import-fixtures.js';
const metadata = revision();
const source = { projectId: metadata.projectId, rootId: metadata.rootId, sourceId: metadata.sourceId, family: metadata.family, relativePath: metadata.relativePath, pointer: '/record', sequence: '1', revisionId: metadata.revisionId, adapterVersion: metadata.adapterVersion };
const identity = { kind: 'participant' as const, projectId: 'project', participant: { kind: 'controller' as const, id: 'controller' } };
const vertex: Vertex = { id: elementKey(identity), identity, kind: 'participant', label: '<script>hostile()</script>', source, attributes: { kind: 'inline', value: { type: 'integer', value: '9007199254740993' } } };
const edgeIdentity = { kind: 'explicit' as const, projectId: 'project', origin: identity, sourceEdgeId: 'parallel-1', from: identity, to: identity };
const edge: Edge = { id: edgeKey(edgeIdentity), identity: edgeIdentity, from: vertex.id, to: vertex.id, relation: 'other-reference', label: 'Observed relation', basis: 'exact-reference', causal: false, source, attributes: vertex.attributes };
const props = { attributes: null, endpoints: [], subjects: [], onSelect: () => {}, onSource: () => {} };
function renderInspector(input: InspectorProps) { return renderToStaticMarkup(createElement(Inspector, input)); }
describe('literal source-backed inspector', () => {
  it('shows an empty selection without invented record or authority', () => {
    const html = renderInspector({ ...props, element: null });
    expect(html).toContain('Select a vertex or relation'); expect(html).not.toContain('read-source');
  });
  it('escapes hostile labels and preserves exact tagged integers and source provenance', () => {
    const html = renderInspector({ ...props, element: vertex });
    expect(html).toContain('&lt;script&gt;hostile()&lt;/script&gt;'); expect(html).not.toContain('<script>');
    expect(html).toContain('9007199254740993'); expect(html).toContain(metadata.revisionId); expect(html).toContain('/record');
  });
  it('explains original direction, endpoints and association basis for an addressable self-relation', () => {
    const html = renderInspector({ ...props, element: edge, endpoints: [vertex] });
    expect(html).toContain('From → To, as recorded'); expect(html).toContain('exact-reference'); expect(html).toContain('Association; no causal claim'); expect(html).toContain('parallel-1');
  });
  it('states missing endpoint evidence instead of inventing a label', () => {
    const html = renderInspector({ ...props, element: edge });
    expect(html.match(/Endpoint outside this visible projection/g)).toHaveLength(2);
  });
  it('places useful relation labels and endpoint controls before collapsed exact identity and named raw regions', () => {
    const html = renderInspector({ ...props, element: edge, endpoints: [vertex] });
    expect(html.indexOf('Observed relation')).toBeLessThan(html.indexOf('data-testid="selected-id"')); expect(html.indexOf('From → To, as recorded')).toBeLessThan(html.indexOf('Exact identity and original fields'));
    expect(html).toContain('id="inspector-heading" tabindex="-1"'); expect(html).toContain('<details><summary>Exact identity and original fields'); expect(html).not.toContain('<details open'); expect(html).toContain('role="region" aria-label="Original identity fields"'); expect(html).toContain('role="region" aria-label="Selected attributes"');
  });
  it('presents readable exact-key aliases while retaining full raw source labels in identity evidence', () => {
    const raw = 'b'.repeat(64); const record = { ...vertex, label: raw };
    const html = renderInspector({ ...props, element: record, labels: new Map([[record.id, 'Readable recorded name']]) });
    expect(html).toContain('data-testid="selected-label">Readable recorded name'); expect(html).toContain('Original source label'); expect(html).toContain(raw); expect(record.id).toBe(vertex.id); expect(record.label).toBe(raw);
  });
});

it('describes historical dependency classification without implying fresh verification', () => {
  const html = renderInspector({ ...props, element: { ...edge, basis: 'canonical-dependency', causal: true } });
  expect(html).toContain('Recorded dependency classification'); expect(html).toContain('Original relation basis'); expect(html).toContain('canonical-dependency');
});

it('exposes discoverable semantic tabs and keeps captured bytes inside Evidence with incomplete-subject context', () => {
  const html = renderInspector({ ...props, element: vertex, evidencePage: <pre id="source-text">{'<img inert>'}</pre>, subjectIncomplete: true });
  for (const label of ['Overview', 'Relations', 'Evidence', 'Raw']) expect(html).toContain(`>${label}</button>`);
  expect(html).toContain('role="tablist"'); expect(html).toContain('aria-controls="inspector-evidence"'); expect(html).toContain('id="inspector-evidence"'); expect(html).toContain('&lt;img inert&gt;'); expect(html).not.toContain('<img'); expect(html).toContain('Subject resolution is incomplete');
});

it('actual tab callbacks select Evidence before requesting exact source and preserve relation selection callbacks', () => {
  const onSource = vi.fn(); const onSelect = vi.fn(); let tree!: ReactElement; let phase = 0; const frames: string[] = [];
  function find(input: unknown, match: (item: ReactElement<Record<string, unknown>>) => boolean): ReactElement<Record<string, unknown>> | undefined {
    if (Array.isArray(input)) return input.map(item => find(item, match)).find(Boolean);
    if (!isValidElement(input)) return undefined; const item = input as ReactElement<Record<string, unknown>>;
    return match(item) ? item : find(item.props.children, match);
  }
  function Mounted() {
    tree = Inspector({ ...props, element: edge, endpoints: [vertex], onSource, onSelect });
    frames.push(String(find(tree, item => item.props.id === 'inspector-tab-evidence')?.props['aria-selected']));
    if (phase++ === 0) {
      (find(tree, item => item.props.id === 'read-source')!.props.onClick as () => void)();
      (find(tree, item => item.type === 'button' && item.props.id === 'inspector-tab-relations')!.props.onKeyDown as Function)({ key: 'End', preventDefault() {}, currentTarget: { parentElement: { querySelector: () => ({ focus() {} }) } } });
    }
    return tree;
  }
  renderToStaticMarkup(createElement(Mounted)); expect(onSource).toHaveBeenCalledExactlyOnceWith(source);
  expect(frames).toHaveLength(2); expect(renderToStaticMarkup(tree)).toContain('id="inspector-tab-raw" role="tab" aria-selected="true"');
});

it('retains the chosen Raw section when the selected record changes', () => {
  let phase = 0; const selected: boolean[] = [];
  function Mounted() {
    const [, force] = useState(0); const tree = Inspector({ ...props, element: phase < 2 ? vertex : edge });
    const children = tree.props.children as unknown[];
    const tablist = children.find(item => isValidElement(item) && (item.props as Record<string, unknown>).role === 'tablist') as ReactElement<{ children: ReactElement<Record<string, unknown>>[] }>;
    const raw = tablist.props.children.find(item => item.props.id === 'inspector-tab-raw')!; selected.push(raw.props['aria-selected'] as boolean);
    if (phase === 0) { phase++; (raw.props.onClick as () => void)(); }
    else if (phase === 1) { phase++; force(2); }
    return tree;
  }
  renderToStaticMarkup(createElement(Mounted)); expect(selected).toEqual([false, true, true]);
});

it('serializes immutable identity and attributes once across tab-state rerenders', () => {
  const stringify = vi.spyOn(JSON, 'stringify'); let phase = 0;
  try {
    function Mounted() {
      const tree = Inspector({ ...props, element: vertex });
      if (phase++ === 0) {
        const list = (tree.props.children as ReactElement<Record<string, unknown>>[]).find(item => isValidElement(item) && item.props.role === 'tablist')!;
        const tabs = list.props.children as ReactElement<Record<string, unknown>>[]; (tabs[3]!.props.onClick as () => void)();
      }
      return tree;
    }
    renderToStaticMarkup(createElement(Mounted));
    expect(stringify.mock.calls.filter(args => args[0] === vertex.identity)).toHaveLength(1);
    expect(stringify.mock.calls.filter(args => args[0] === vertex.attributes)).toHaveLength(1);
  } finally { stringify.mockRestore(); }
});

it.each(['altKey', 'ctrlKey', 'metaKey', 'defaultPrevented', 'composition'])('preserves %s arrow gestures without changing the selected inspector section', flag => {
  let tree!: ReactElement;
  function Mounted() { tree = Inspector({ ...props, element: vertex }); return tree; }
  renderToStaticMarkup(createElement(Mounted));
  const tabs = (tree.props as { children: ReactElement<Record<string, unknown>>[] }).children.find(item => isValidElement(item) && item.props.role === 'tablist')!.props.children as ReactElement<Record<string, unknown>>[];
  const preventDefault = vi.fn(); const focus = vi.fn();
  (tabs[0]!.props.onKeyDown as Function)({ key: 'ArrowRight', [flag]: true, nativeEvent: { isComposing: flag === 'composition' }, preventDefault, currentTarget: { parentElement: { querySelector: () => ({ focus }) } } });
  expect(preventDefault).not.toHaveBeenCalled(); expect(focus).not.toHaveBeenCalled();
});
