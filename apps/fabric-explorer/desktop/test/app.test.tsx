// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Server-rendered entry states; actual browser effects and journeys have separate native coverage. */
import { createElement, isValidElement } from 'react';
import type { ReactElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { afterEach, describe, expect, it, vi } from 'vitest';
// Sigma imports static GL enum descriptors; this enables SSR, not GPU/render qualification.
vi.hoisted(() => { Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }); });
import type { DesktopBridge } from '../src/shell/bridge.js';
import { ExploreController } from '../src/renderer/presentation/controller.js';
import { ExplorerApp } from '../src/renderer/app.js';
import type { ShellState } from '../src/shell/controller.js';
import { DEFAULT_PREFERENCES } from '../src/shell/preferences.js';
const api = {} as DesktopBridge;
afterEach(() => vi.unstubAllGlobals());
function render(presentation: ExploreController) {
  function Mounted() { return ExplorerApp({ api, presentation }); }
  return renderToStaticMarkup(createElement(Mounted));
}
describe('read-only React application entry', () => {
  it.each(['none', 'during-import', 'after-import'] as const)('the actual Open handler automatically loads fresh admission once and routes cancellation to active work: %s', async cancel => {
    vi.stubGlobal('document', { activeElement: null });
    const initial: ShellState = { sessionId: 'old-session', capability: null, sources: [], preferences: DEFAULT_PREFERENCES, warning: null, snapshot: null, report: null, stale: false };
    const admitted: ShellState = { ...initial, sessionId: 'new-session', capability: 'new-capability', sources: [{ projectId: 'p', rootId: 'r', sourceId: 'new-source', family: 'fabric', relativePath: 'source.jsonl', readHandle: 'handle' }] };
    let selected!: () => void; let imported!: () => void; let finishImport!: (value: { status: string }) => void;
    const selection = new Promise<void>(resolve => { selected = resolve; });
    const importStarted = new Promise<void>(resolve => { imported = resolve; });
    const importReply = new Promise<{ status: string }>(resolve => { finishImport = resolve; });
    let finalReadStarted!: () => void; let finishFinalRead!: (state: ShellState) => void; let reads = 0;
    const finalRead = new Promise<ShellState>(resolve => { finishFinalRead = resolve; }); const finalStarted = new Promise<void>(resolve => { finalReadStarted = resolve; });
    const bridge = { pickRoots: vi.fn(async (..._args: Parameters<DesktopBridge['pickRoots']>) => { await selection; return { status: 'ok' }; }), getState: vi.fn(async () => { if (++reads === 2 && cancel === 'after-import') { finalReadStarted(); return finalRead; } return admitted; }), importSnapshot: vi.fn(async (..._args: Parameters<DesktopBridge['importSnapshot']>) => { imported(); return importReply; }), cancelRequest: vi.fn(async (..._args: Parameters<DesktopBridge['cancelRequest']>) => ({ status: 'ok' })), cancelSelection: vi.fn(async () => true) };
    const presentation = new ExploreController(bridge as unknown as DesktopBridge); await presentation.setShell(initial);
    let tree!: ReactElement;
    function Mounted() { tree = ExplorerApp({ api: bridge as unknown as DesktopBridge, presentation }); return tree; }
    renderToStaticMarkup(createElement(Mounted));
    const button = (input: unknown, id: string): ReactElement<Record<string, unknown>> | undefined => {
      if (Array.isArray(input)) return input.map(item => button(item, id)).find(Boolean);
      if (!isValidElement(input)) return undefined;
      const element = input as ReactElement<Record<string, unknown>>;
      return element.props.id === id && typeof element.props.onClick === 'function' ? element : button(element.props.children, id);
    };
    const open = button(tree, 'open')!.props.onClick as () => Promise<void>;
    const work = open(); await open(); expect(bridge.pickRoots).toHaveBeenCalledOnce(); selected(); await importStarted;
    expect(bridge.importSnapshot).toHaveBeenCalledExactlyOnceWith({ sessionId: 'new-session', capability: 'new-capability', generation: null }, expect.any(String), ['new-source']);
    if (cancel === 'during-import') {
      await (button(tree, 'cancel')!.props.onClick as () => Promise<void>)();
      expect(bridge.cancelRequest).toHaveBeenCalledExactlyOnceWith({ sessionId: 'new-session', capability: 'new-capability', generation: null }, expect.any(String), bridge.importSnapshot.mock.calls[0]?.[1]);
      expect(bridge.cancelSelection).not.toHaveBeenCalled();
    }
    finishImport({ status: cancel === 'during-import' ? 'error' : 'ok' });
    if (cancel === 'after-import') {
      await finalStarted; await (button(tree, 'cancel')!.props.onClick as () => Promise<void>)();
      expect(bridge.cancelRequest).not.toHaveBeenCalled(); expect(bridge.cancelSelection).not.toHaveBeenCalled(); finishFinalRead(admitted);
    }
    await work;
    expect(bridge.importSnapshot).toHaveBeenCalledOnce(); expect(bridge.getState).toHaveBeenCalledTimes(2);
  });
  it('provides named source, search, graph and evidence controls while awaiting initialization', () => {
    const html = render(new ExploreController(api));
    expect(html).toContain('Open sources…'); expect(html).toContain('Read-only'); expect(html).toContain('No snapshot imported.');
    expect(html).toContain('id="search-text"'); expect(html).toContain('Visible vertices in the current bounded graph projection'); expect(html).toContain('Select a vertex or relation');
    expect(html).not.toContain('id="import"'); expect(html).not.toContain('Import sources</button>'); expect(html).not.toContain('contenteditable');
  });
  it('provides skip targets, named workspace and modifier-only shortcut help', () => {
    const html = render(new ExploreController(api));
    expect(html).toContain('href="#main-workspace"'); expect(html).toContain('href="#inspector-heading"'); expect(html).toContain('id="main-workspace" class="workspace ergonomic-workspace"'); expect(html).toContain('tabindex="-1" aria-label="Fabric exploration workspace"'); expect(html).toContain('id="inspector-heading" tabindex="-1"');
    expect(html).toContain('Ctrl/Cmd+K'); expect(html).toContain('Ctrl/Cmd+Shift+F'); expect(html).not.toContain('<kbd>/</kbd>'); expect(html).not.toContain('<kbd>F</kbd>');
  });
  it('gives captured byte text a named focusable scroll region and preserves literal source content', () => {
    // This owned controller port supplies a fixed presentation publication; browser effects remain native coverage.
    const snapshot = { ...new ExploreController(api).getSnapshot(), sourcePage: { page: { sourceId: 'synthetic', pointer: '/row', sequence: '1', offset: '0', byteLength: 3, bytesBase64: 'PGI+', eof: true }, text: '<b>' } };
    const controller = { getSnapshot: () => snapshot, subscribe: () => () => {} } as unknown as ExploreController;
    const html = render(controller); expect(html).toContain('id="source-text" tabindex="0" role="region" aria-label="Captured source bytes"'); expect(html).toContain('&lt;b&gt;'); expect(html).not.toContain('<b>');
  });
  it('admits source selection without enabling import before a capability exists', async () => {
    const state = new ExploreController(api);
    await state.setShell({ sessionId: 'session', capability: null, snapshot: null, report: null, stale: false, sources: [], preferences: { version: 1, theme: 'light', reducedMotion: false }, warning: null });
    const html = render(state); expect(html).toMatch(/id="open"[^>]*aria-label="Open sources…"/); expect(html).not.toMatch(/id="open"[^>]*disabled/); expect(html).toMatch(/id="refresh"[^>]*disabled/);
  });
  it('renders malformed-input diagnostics as literal text and keeps recovery controls', async () => {
    const state = new ExploreController(api);
    await state.setShell({ sessionId: 'session', capability: null, snapshot: null, report: { status: 'failed', selectedSources: '1', acceptedSources: '0', rejectedSources: '1', vertices: '0', edges: '0', unresolvedVertices: '0', skippedItems: '0', diagnosticTotal: '1', diagnostics: [{ code: 'invalid-model', message: '<img src=https://example.invalid/>', severity: 'error', source: null }], supportedVersions: [], observation: 'observed-revision-set', limitation: null }, stale: false, sources: [], preferences: { version: 1, theme: 'light', reducedMotion: false }, warning: null });
    const html = render(state); expect(html).toContain('&lt;img src=https://example.invalid/&gt;'); expect(html).not.toContain('<img'); expect(html).toContain('0/1 sources accepted'); expect(html).toContain('Open sources');
  });
});
