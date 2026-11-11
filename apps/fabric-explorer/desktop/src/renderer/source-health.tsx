// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Source-health presentation maps recorded outcomes literally; it never evaluates trust or authority. */
import type { ShellState } from '../shell/controller.js';
/**
 * Display accepted snapshot provenance and bounded import diagnostics.
 * @param props Current immutable shell state, null before initialization.
 * @returns Literal source observations and fixed import-health labels.
 */
export function SourceHealth({ shell }: { shell: ShellState | null }) {
  const report = shell?.report;
  return <>
    <p id="import-counts" className="muted">{report ? `${report.status}: ${report.acceptedSources}/${report.selectedSources} sources accepted; ${report.skippedItems} skipped. ${report.diagnosticTotal} diagnostics.${report.limitation ? ` ${report.limitation}` : ''}` : 'No import report yet.'}</p>
    <ul id="diagnostics" className="diagnostic-list">{report?.diagnostics.slice(0, 20).map((item, index) => {
      const context = report.diagnosticContexts?.[index];
      const file = item.source?.relativePath ?? shell?.sources.find(source => source.sourceId === context?.sourceId)?.relativePath;
      return <li key={index}>{file ? `${file}${context?.sequence ? ` [${context.sequence}]` : ''}${context?.pointer ? ` ${context.pointer}` : ''}: ` : ''}{item.code}: {item.message}</li>;
    })}</ul>
    {Number(report?.diagnosticTotal ?? 0) > 20 && <p className="muted">Only the first 20 diagnostics are displayed.</p>}
    {!!report?.supportedVersions.length && <details><summary>Source compatibility</summary><ul className="source-list">{report.supportedVersions.map((version, index) => <li key={`${version.sourceId}-${index}`}>{version.family} · {version.supported ? 'supported' : 'unsupported'} · format {version.declaredFormat ?? 'unknown'} · protocol {version.declaredProtocol ?? 'unknown'} · adapter {version.adapterVersion}</li>)}</ul></details>}
    {shell?.snapshot && <details id="snapshot-provenance"><summary>Snapshot provenance · observed revision set</summary><p className="muted">No viewing action grants authority or performs a fresh assessment. These fields are recorded observations, not a combined transaction or current permission.</p>
      {shell.snapshot.sources.map(source => <details key={source.revisionId}><summary>{source.family}: {source.relativePath} · {source.verification.mode}</summary><dl className="provenance-fields">
        <dt>Revision</dt><dd><code>{source.revisionId}</code></dd><dt>Observed at</dt><dd>{source.observedAt}</dd><dt>Digest</dt><dd><code>{source.digest}</code></dd>
        <dt>Head</dt><dd><code>{source.head ?? 'Not recorded'}</code></dd><dt>Sequence</dt><dd>{source.sequence ?? 'Not recorded'}</dd><dt>Bytes</dt><dd>{source.byteLength}</dd>
        <dt>Adapter</dt><dd>{source.adapterVersion}</dd><dt>Mode</dt><dd>{source.verification.mode}</dd><dt>Decoded</dt><dd>{source.verification.decoded}</dd>
        <dt>Chain</dt><dd>{source.verification.chain}</dd><dt>Replay</dt><dd>{source.verification.replay}</dd><dt>Public trust</dt><dd>{source.verification.publicTrust}</dd><dt>Material</dt><dd>{source.verification.material}</dd>
        <dt>Recorded applicability</dt><dd><pre>{source.verification.recordedApplicability === null ? 'Not recorded' : JSON.stringify(source.verification.recordedApplicability, null, 2)}</pre></dd>
      </dl></details>)}
    </details>}
  </>;
}
