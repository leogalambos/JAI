/** Finding names retain ledger-local identifiers across real shared display consumers. */
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { expect, it, vi } from 'vitest';
import { elementKey } from '@jai/fabric-explorer-contracts';
import type { GraphProjection, Vertex } from '@jai/fabric-explorer-contracts';
import golden from '../../packages/contracts/test/fixtures/projection.json' with { type: 'json' };
import { displayNodeLabel, projectionLabelMap } from '../src/renderer/node-label.js';
import { Inspector } from '../src/renderer/inspector.js';
import { canvasProjection } from '../src/renderer/canvas/model.js';
import { ElementTableView } from '../src/renderer/element-table.js';
import { elementTableWindow } from '../src/renderer/element-table-model.js';
import type { DesktopBridge } from '../src/shell/bridge.js';
import { ExploreController } from '../src/renderer/presentation/controller.js';
// This enables static React markup, not native WebGL qualification.
vi.hoisted(() => { Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }); });
import { ExplorerApp } from '../src/renderer/app.js';

function finding(title: string, ledgerId = 'review', findingId = 'F-0001'): Extract<Vertex, { kind: 'finding' }> {
  const base = (structuredClone(golden) as GraphProjection).vertices[0]!;
  const identity = { kind: 'finding' as const, projectId: base.source.projectId, ledgerId, findingId };
  return { identity, id: elementKey(identity), kind: 'finding', label: title, source: { ...base.source, family: 'findings', relativePath: ledgerId + '.jsonl' }, attributes: { kind: 'inline', value: { type: 'object', entries: [{ key: 'title', value: { type: 'string', value: title } }] } }, state: 'open', severity: 'medium', findingKind: 'defect', rounds: '0', recordedExpiry: null };
}
const inspectorProps = { attributes: null, endpoints: [], subjects: [], onSelect: () => {}, onSource: () => {} };

it('keeps the complete canonical finding ID visible alongside the authored title without mutating its record', () => {
  const record = finding('Missing source evidence'); const before = JSON.stringify(record);
  expect(displayNodeLabel(record)).toBe('F-0001 · Missing source evidence');
  expect(JSON.stringify(record)).toBe(before);
});
it('retains canonical finding IDs through projection aliases and custom names without duplicate prefixes', () => {
  const record = finding('Source title'); const projection = { ...(structuredClone(golden) as GraphProjection), vertices: [record], edges: [] };
  const labels = projectionLabelMap(projection);
  expect(labels.get(record.id)).toBe('F-0001 · Source title'); expect(displayNodeLabel(record, labels)).toBe('F-0001 · Source title');
  expect(displayNodeLabel(record, new Map([[record.id, 'Custom view name']]))).toBe('F-0001 · Custom view name');
  expect(displayNodeLabel(record, new Map([[record.id, 'F-0001 · Existing view name']]))).toBe('F-0001 · Existing view name');
  expect(Array.from(displayNodeLabel(record, new Map([[record.id, 'F-0001 · ' + 'x'.repeat(10000)]])).slice('F-0001 · '.length)).length).toBeLessThanOrEqual(96);
});
it('preserves an ID-only or already prefixed name while bounding a long title independently of the ID', () => {
  expect(displayNodeLabel(finding('F-0001'))).toBe('F-0001');
  expect(displayNodeLabel(finding('F-0001 · Already named'))).toBe('F-0001 · Already named');
  const record = finding('Résumé '.repeat(1000), 'review', 'F-00000000000000000001');
  const name = displayNodeLabel(record); expect(name.startsWith('F-00000000000000000001 · ')).toBe(true);
  expect(Array.from(name.slice('F-00000000000000000001 · '.length)).length).toBeLessThanOrEqual(96);
  const fullId = 'F-' + '0'.repeat(100) + '1'; expect(displayNodeLabel(finding(fullId, 'review', fullId))).toBe(fullId);
  expect(displayNodeLabel(finding(fullId + ' · Already named', 'review', fullId))).toBe(fullId + ' · Already named');
});
it('renders the ordinary finding ID and ledger before technical details while leaving HTML literal', () => {
  const record = finding('<img src=x onerror=alert(1)>'); const html = renderToStaticMarkup(createElement(Inspector, { ...inspectorProps, element: record }));
  expect(html).toContain('data-testid="selected-label">F-0001 · &lt;img'); expect(html).not.toContain('<img');
  const semantic = html.replace(/<svg\b[^>]*aria-hidden="true"[^>]*>[\s\S]*?<\/svg>/g, ''); expect(html).toContain('aria-hidden="true"');
  expect(semantic).toContain('<dt>Finding ID</dt><dd>F-0001</dd>'); expect(semantic).toContain('<dt>Ledger</dt><dd>review</dd>');
  expect(semantic.indexOf('<dt>Finding ID')).toBeGreaterThanOrEqual(0); expect(semantic.indexOf('<dt>Finding ID')).toBeLessThan(semantic.indexOf('Exact identity and original fields'));
  expect(html).toContain('Finding IDs are local to their ledger.'); expect(record.label).toBe('<img src=x onerror=alert(1)>');
});
it('keeps equal ledger-local finding IDs separately addressable and exposes the exact ledger', () => {
  const first = finding('Same title', 'first-ledger'); const second = finding('Same title', 'second-ledger');
  expect(first.id).not.toBe(second.id); expect(first.identity.findingId).toBe(second.identity.findingId);
  const projection = { ...(structuredClone(golden) as GraphProjection), vertices: [first, second], edges: [] }; const labels = projectionLabelMap(projection);
  expect(labels.size).toBe(2); expect(displayNodeLabel(first, labels)).toBe('F-0001 · Same title');
  for (const record of [first, second]) {
    const html = renderToStaticMarkup(createElement(Inspector, { ...inspectorProps, element: record, labels }));
    expect(html.replace(/<svg\b[^>]*aria-hidden="true"[^>]*>[\s\S]*?<\/svg>/g, '')).toContain(`<dt>Ledger</dt><dd>${record.identity.ledgerId}</dd>`); expect(html).toContain('Finding IDs are local to their ledger.');
  }
});
it('uses the same finding name in canvas and semantic table without changing selection keys', () => {
  const record = finding('Visible finding'); const projection = { ...(structuredClone(golden) as GraphProjection), vertices: [record], edges: [] };
  const layout = { binding: { sessionId: projection.snapshot.sessionId, capability: 'c', generation: projection.snapshot.generation, requestId: 'q', projectionId: 'p' }, algorithm: 'layered' as const, positions: [{ handle: 1, x: 0, y: 0 }], groups: [], work: 0, iterations: 1, complete: true as const };
  const canvas = canvasProjection(projection, layout, [1]); expect(canvas.nodes[0]?.label).toBe('F-0001 · Visible finding'); expect(canvas.nodes[0]?.id).toBe(record.id);
  const html = renderToStaticMarkup(ElementTableView({ window: elementTableWindow(projection, 'vertices', 0), selectedId: record.id, idPrefix: 'finding-table', onSelect: () => {}, onKindChange: () => {}, onPageChange: () => {}, labels: projectionLabelMap(projection) }));
  expect(html).toContain('F-0001 · Visible finding'); expect(html).toContain('>Selected</td>');
});
it('shows the finding ID as part of the visible sidebar button name rather than only its technical title', () => {
  const api = {} as DesktopBridge; const record = finding('<img src=x>'); const base = new ExploreController(api).getSnapshot();
  const snapshot = { ...base, findings: { items: [record], text: '', order: 'identity' as const, hidden: '0', nextCursor: null, complete: true } };
  const controller = { getSnapshot: () => snapshot, subscribe: () => () => {} } as unknown as ExploreController;
  function Mounted() { return ExplorerApp({ api, presentation: controller }); }
  const html = renderToStaticMarkup(createElement(Mounted)); expect(html).toContain('>F-0001 · &lt;img src=x&gt;<small>finding'); expect(html).not.toContain('<img');
});
