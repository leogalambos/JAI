// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Keyboard-native, paged semantic alternative to precise graph picking. */
import { useId, useState } from 'react';
import type { Edge, GraphProjection, Vertex } from '@jai/fabric-explorer-contracts';
import { elementTableWindow } from './element-table-model.js';
import type { ElementTableKind, ElementTableWindow } from './element-table-model.js';
import { displayNodeLabel } from './node-label.js';

/** Parent-owned exact selection and optional display aliases; records and source labels remain immutable. */
export interface ElementTableProps {
  readonly projection: GraphProjection | null;
  readonly selectedId: string | null;
  readonly onSelect: (id: string) => void;
  readonly labels?: ReadonlyMap<string, string>;
}
/** Stateless render boundary for the same production table and guarded native callbacks. */
export interface ElementTableViewProps {
  readonly window: ElementTableWindow;
  readonly selectedId: string | null;
  readonly idPrefix: string;
  readonly onSelect: (id: string) => void;
  readonly onKindChange: (kind: ElementTableKind) => void;
  readonly onPageChange: (page: number) => void;
  readonly labels?: ReadonlyMap<string, string>;
}
function context(item: Vertex | Edge): string {
  if (!('kind' in item)) return `Source ${item.source.sourceId} · ${item.source.pointer}`;
  const identity = item.identity;
  if (identity.kind === 'version' || identity.kind === 'use') return `${identity.ref.logical_id} · origin scope ${identity.ref.scope}${identity.kind === 'use' ? ` · use scope ${identity.useScope}` : ''}`;
  if (identity.kind === 'finding') return `${identity.findingId} · ledger ${identity.ledgerId}`;
  return `${item.kind === 'blob' ? 'Material' : item.kind} · ${item.source.relativePath}`;
}
function state(item: Vertex | Edge): string {
  if (!('kind' in item)) return 'Not applicable';
  if (item.kind === 'finding') return item.state;
  if (item.kind === 'unresolved') return item.reason;
  if (item.kind === 'blob') return item.availability;
  return 'Not applicable';
}

/**
 * Render the bounded native table and its keyboard-operable controls without custom grid behavior.
 * @param props Current finite window, exact selection and parent-owned callbacks; idPrefix is unique.
 * @returns Captioned table with global row indices, explicit selected text and finite paging controls.
 */
export function ElementTableView(props: ElementTableViewProps) {
  const window = props.window; const category = window.kind === 'vertices' ? 'vertex' : 'relation'; const plural = window.kind === 'vertices' ? 'vertices' : 'relations';
  const tableId = `${props.idPrefix}-table`; const statusId = `${props.idPrefix}-status`; const headingId = `${props.idPrefix}-heading`;
  const previous = window.page > 0; const next = window.page + 1 < window.pageCount;
  const range = window.total ? `Showing ${window.start + 1}–${window.end} of ${window.total} visible ${plural}. Page ${window.page + 1} of ${window.pageCount}.` : window.loaded ? `No visible ${plural} in this projection.` : 'No captured graph is loaded.';
  return <section className="semantic-panel element-table" aria-labelledby={headingId}>
    <div className="row"><h2 id={headingId}>Visible elements</h2><label>List <select id="element-kind" value={window.kind} onChange={event => { const kind = event.target.value; if (kind === 'vertices' || kind === 'edges') props.onKindChange(kind); }}><option value="vertices">Vertices</option><option value="edges">Relations</option></select></label></div>
    <nav className="row element-table-pager" aria-label="Visible element pages">
      <button type="button" aria-controls={tableId} aria-disabled={!previous} onClick={() => { if (previous) props.onPageChange(window.page - 1); }}>Previous elements</button>
      <button type="button" aria-controls={tableId} aria-disabled={!next} onClick={() => { if (next) props.onPageChange(window.page + 1); }}>Next elements</button>
    </nav>
    <p id={statusId} className="muted element-table-status" role="status" aria-live="polite" aria-atomic="true">{range}</p>
    <table id={tableId} aria-describedby={statusId} aria-rowcount={window.total + 1}>
      <caption>Visible {plural} in the current bounded graph projection</caption>
      <thead><tr aria-rowindex={1}><th scope="col">Label</th><th scope="col">Type</th><th scope="col">State</th><th scope="col">Exact identity</th><th scope="col">Selection</th></tr></thead>
      <tbody>{window.rows.map((item, index) => {
        const ordinal = window.start + index + 1; const selected = item.id === props.selectedId;
        const label = 'kind' in item ? displayNodeLabel(item, props.labels) : item.label;
        return <tr key={item.id} aria-rowindex={ordinal + 1} className={selected ? 'selected-row' : undefined}>
          <td><button type="button" title={item.id} data-element-id={item.id} aria-label={`Inspect ${category} ${ordinal}: ${label}`} aria-current={selected ? 'true' : undefined} onClick={() => props.onSelect(item.id)}>{label}</button><span className="element-table-context">{context(item)}</span></td>
          <td>{'kind' in item ? item.kind === 'version' ? `version · ${item.family}` : item.kind : item.relation}</td>
          <td>{state(item)}</td>
          <td><details><summary>Identity for {category} {ordinal}</summary><dl><dt>Canonical key</dt><dd><code>{item.id}</code></dd><dt>Original source label</dt><dd>{item.label}</dd>{!('kind' in item) && <><dt>From</dt><dd><code>{item.from}</code></dd><dt>To</dt><dd><code>{item.to}</code></dd></>}</dl></details></td>
          <td className="element-table-selection">{selected ? 'Selected' : 'Not selected'}</td>
        </tr>;
      })}</tbody>
    </table>
  </section>;
}

/**
 * Keep a 25-row native render window while preserving exact canonical selection identities.
 * @param props Trusted bounded projection and selected ID; onSelect delegates focus to the parent.
 * @returns Semantic table; projection or kind changes reset the page synchronously without effects.
 */
export function ElementTable(props: ElementTableProps) {
  const id = useId();
  const [position, setPosition] = useState<{ projection: GraphProjection | null; kind: ElementTableKind; page: number }>({ projection: props.projection, kind: 'vertices', page: 0 });
  if (position.projection !== props.projection) setPosition({ projection: props.projection, kind: position.kind, page: 0 });
  const window = elementTableWindow(props.projection, position.kind, position.projection === props.projection ? position.page : 0);
  return <ElementTableView window={window} selectedId={props.selectedId} idPrefix={`elements-${id}`} onSelect={props.onSelect} {...(props.labels ? { labels: props.labels } : {})}
    onKindChange={kind => setPosition({ projection: props.projection, kind, page: 0 })}
    onPageChange={page => setPosition({ projection: props.projection, kind: position.kind, page })}/>;
}
