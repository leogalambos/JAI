// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Literal source-backed inspection components; no source content becomes markup or navigation URLs. */
import { useEffect, useMemo, useState } from 'react';
import type { ReactNode } from 'react';
import type { Attributes, Edge, ElementIdentity, SourceLocator, Vertex } from '@jai/fabric-explorer-contracts';
import { CommandIcon } from './commands.js';
import type { IconName } from './commands.js';
import { displayNodeLabel } from './node-label.js';

/** Original records plus optional exact-key display aliases; callbacks are read-only navigation. */
export interface InspectorProps {
  readonly element: Vertex | Edge | null;
  readonly attributes: Attributes | null;
  readonly endpoints: readonly Vertex[];
  readonly subjects: readonly Vertex[];
  readonly onSelect: (identity: ElementIdentity) => void;
  readonly onSource: (source: SourceLocator) => void;
  /** Optional captured-source paging controls and literal bytes, rendered inside Evidence. */
  readonly evidencePage?: ReactNode;
  /** Warn when the observed finding links do not resolve all subjects. */
  readonly subjectIncomplete?: boolean;
  readonly labels?: ReadonlyMap<string, string>;
}

/**
 * Present readable selection evidence; original labels and keys remain available in identity details.
 * @param props Immutable records and named navigation callbacks.
 * @returns Accessible inspector; an empty state when nothing is selected.
 */
export function Inspector(props: InspectorProps) {
  const [tab, setTab] = useState('overview');
  const hasEvidence = !!props.evidencePage;
  useEffect(() => { if (hasEvidence) setTab('evidence'); }, [hasEvidence]);
  const record = props.element;
  const attributes = props.attributes ?? record?.attributes;
  const identityText = useMemo(() => JSON.stringify(record?.identity, null, 2), [record?.identity]);
  const attributesText = useMemo(() => JSON.stringify(attributes, null, 2), [attributes]);
  if (!record) return <section className="inspector-empty"><h2 id="inspector-heading" tabIndex={-1}>Inspector</h2><p>Select a vertex or relation to see its identity and evidence.</p>{props.evidencePage && <section aria-label="Captured source evidence">{props.evidencePage}</section>}</section>;
  const edge = 'relation' in record ? record : null;
  const vertex = 'kind' in record ? record : null;
  const endpoint = (id: string) => props.endpoints.find(item => item.id === id);
  return <section aria-labelledby="inspector-heading" className="inspector-content">
    <h2 id="inspector-heading" tabIndex={-1}>{edge ? 'Relation' : 'Vertex'} inspector</h2>
    <p className="selected-label" data-testid="selected-label">{vertex ? displayNodeLabel(vertex, props.labels) : record.label}</p>
    <div role="tablist" aria-label="Inspector sections" className="pane-tabs">{(['overview', 'relations', 'evidence', 'raw'] as const).map((name, index, names) => <button key={name} id={`inspector-tab-${name}`} role="tab" aria-selected={tab === name} aria-controls={`inspector-${name}`} tabIndex={tab === name ? 0 : -1} onClick={() => setTab(name)} onKeyDown={event => {
      if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || event.nativeEvent?.isComposing) return;
      const next = event.key === 'ArrowRight' ? (index + 1) % names.length : event.key === 'ArrowLeft' ? (index + names.length - 1) % names.length : event.key === 'Home' ? 0 : event.key === 'End' ? names.length - 1 : null;
      if (next !== null) { event.preventDefault(); const name = names[next]!; setTab(name); event.currentTarget.parentElement?.querySelector<HTMLButtonElement>(`#inspector-tab-${name}`)?.focus(); }
    }}>{name[0]!.toUpperCase() + name.slice(1)}</button>)}</div>
    <div id="inspector-overview" role="tabpanel" aria-labelledby="inspector-tab-overview" hidden={tab !== 'overview'}><dl>
      {vertex && <><Field label="Kind" icon="elements"/><dd>{vertex.kind}</dd></>}
      {vertex?.kind === 'version' && <><Field label="Family" icon="elements"/><dd>{vertex.family}</dd></>}
      {vertex?.kind === 'finding' && <><Field label="Finding ID" icon="findings"/><dd>{vertex.identity.findingId}</dd><Field label="Ledger" icon="source"/><dd>{vertex.identity.ledgerId}</dd><Field label="Finding state" icon="findings"/><dd>{vertex.state}</dd><Field label="Severity" icon="findings"/><dd>{vertex.severity}</dd><Field label="Finding kind" icon="findings"/><dd>{vertex.findingKind}</dd><Field label="Recorded rounds" icon="findings"/><dd>{vertex.rounds}</dd></>}
      {vertex?.kind === 'unresolved' && <><Field label="Unresolved reference" icon="relations"/><dd>{vertex.reason}. This placeholder does not establish that its target exists.</dd></>}

    </dl></div>
    <div id="inspector-relations" role="tabpanel" aria-labelledby="inspector-tab-relations" hidden={tab !== 'relations'}>
    <dl>
      {edge && <><Field label="Relation type" icon="relations"/><dd>{edge.relation}</dd><Field label="Direction" icon="relations"/><dd>From → To, as recorded. Reverse navigation does not reverse this arrow.</dd><Field label="Recorded relation basis" icon="relations"/><dd>{edge.basis === 'canonical-dependency' ? 'Recorded dependency classification' : edge.basis}</dd><Field label="Causal membership" icon="relations"/><dd>{edge.causal ? 'Recorded as causal' : 'Association; no causal claim'}</dd>
        <Field label="From" icon="relations"/><dd><Endpoint item={endpoint(edge.from)} id={edge.from} select={props.onSelect} labels={props.labels}/></dd>
        <Field label="To" icon="relations"/><dd><Endpoint item={endpoint(edge.to)} id={edge.to} select={props.onSelect} labels={props.labels}/></dd></>}
    </dl>
    {vertex?.kind === 'finding' && <section aria-label="Finding subjects"><h3>Finding subjects</h3>
      <p className="muted">Finding IDs are local to their ledger.</p>
      {props.subjects.length === 0 ? <p>No resolved subject is available in the observed finding links. Inspect its source evidence.</p> : <>
        <p>{props.subjects.length === 1 ? 'One observed subject.' : `${props.subjects.length} subject candidates; choose explicitly.`}</p>
        <ul>{props.subjects.map(item => <li key={item.id}><button title={item.id} onClick={() => props.onSelect(item.identity)}>{displayNodeLabel(item, props.labels)}{item.kind === 'unresolved' ? ' · unresolved' : ''}</button><details><summary>Exact subject identity</summary><code>{item.id}</code></details></li>)}</ul>
      </>}
    </section>}
    {props.subjectIncomplete && <p className="warning">Subject resolution is incomplete. Unresolved references do not establish that their targets exist.</p>}
    {!edge && vertex?.kind !== 'finding' && <p>No relation endpoints or finding subjects apply to this selection.</p>}</div>
    <div id="inspector-evidence" role="tabpanel" aria-labelledby="inspector-tab-evidence" hidden={tab !== 'evidence'}>
    <section aria-label="Source provenance"><h3>Source evidence</h3><dl>
      <Field label="Source family" icon="source"/><dd>{record.source.family}</dd><Field label="File" icon="source"/><dd>{record.source.relativePath}</dd>
      <Field label="Revision" icon="source"/><dd><code>{record.source.revisionId}</code></dd><Field label="Record pointer" icon="source"/><dd><code>{record.source.pointer || '(root)'}</code></dd>
      <Field label="Sequence" icon="source"/><dd>{record.source.sequence ?? 'Not recorded'}</dd><Field label="Adapter" icon="source"/><dd>{record.source.adapterVersion}</dd>
    </dl><button id="read-source" onClick={() => { setTab('evidence'); props.onSource(record.source); }}>Read captured source</button></section>{props.evidencePage}</div>
    <div id="inspector-raw" role="tabpanel" aria-labelledby="inspector-tab-raw" hidden={tab !== 'raw'}><details><summary>Exact identity and original fields</summary><dl><Field label="Stable identity" icon="raw"/><dd><code data-testid="selected-id">{record.id}</code></dd><Field label="Original source label" icon="raw"/><dd>{record.label}</dd>{edge && <><Field label="Original relation basis" icon="relations"/><dd>{edge.basis}</dd><Field label="Exact From key" icon="relations"/><dd><code>{edge.from}</code></dd><Field label="Exact To key" icon="relations"/><dd><code>{edge.to}</code></dd></>}</dl><pre tabIndex={0} role="region" aria-label="Original identity fields">{identityText}</pre></details>
    <details><summary>Attributes · {attributes!.kind}</summary><pre data-testid="attributes" tabIndex={0} role="region" aria-label="Selected attributes">{attributesText}</pre></details></div>
    <p className="muted">Recorded evidence is displayed read-only. Viewing it grants no approval or authority.</p>
  </section>;
}

function Endpoint({ item, id, select, labels }: { item: Vertex | undefined; id: string; select: (identity: ElementIdentity) => void; labels: ReadonlyMap<string, string> | undefined }) {
  return <>{item ? <button title={id} onClick={() => select(item.identity)}>{displayNodeLabel(item, labels)}{item.kind === 'unresolved' ? ' · unresolved' : ''}</button> : <span>Endpoint outside this visible projection</span>}</>;
}

/** Fixed semantic field decoration; source values never choose SVG data or replace the text label. */
function Field({ label, icon }: { label: string; icon: IconName }) { return <dt><CommandIcon name={icon}/>{label}</dt>; }
