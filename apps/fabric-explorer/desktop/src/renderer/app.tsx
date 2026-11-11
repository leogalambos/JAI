// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Read-only application composition over generation-owned presentation state and the isolated bridge. */
import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react';
import { importProgressText, type ImportProgress } from '../import/progress.js';
import { pollImportProgress } from './import-progress.js';
import { RELATION_DIRECTIONS, elementKey } from '@jai/fabric-explorer-contracts';
import type { ElementIdentity, Filter, FindingState, RecordFamily, RelationClass, SourceFamily, Vertex } from '@jai/fabric-explorer-contracts';
import type { DesktopBridge } from '../shell/bridge.js';
import { ExploreController } from './presentation/controller.js';
import type { ExplorePage, ExploreState } from './presentation/types.js';
import { prepareCanvas } from './canvas/index.js';
import { PhasedCanvasView } from './canvas-phases.js';
import type { CanvasCommit } from './canvas-phases.js';
import { ApplicationMenu, type MenuGroup } from './application-menu.js';
import { IconButton } from './commands.js';
import { PaneSplitter, workspaceGeometry } from './workspace-layout.js';
import { PreferencesDialog } from './preferences-dialog.js';
import { Inspector } from './inspector.js';
import { SourceHealth } from './source-health.js';
import { ResultPager } from './result-pager.js';
import { ElementTable } from './element-table.js';
import { keyboardAction } from './keyboard.js';
import { InspectorFocusIntent, shouldRecoverFocus } from './focus.js';
import { LIGHT_THEME, observeTheme } from './theme.js';
import type { ResolvedTheme } from './theme.js';
import type { CanvasPalette } from './canvas/palette.js';
import { displayNodeLabel, projectionLabelMap } from './node-label.js';
import { openAndLoadSources } from './source-flow.js';
import type { OpenSourcesResult, SourceWork } from './source-flow.js';

/** Trusted fixed preload bridge; source records never choose callbacks or runtime modules. */
export interface ExplorerAppProps { readonly api: DesktopBridge; readonly presentation?: ExploreController }
/**
 * Compose local source admission and complete bounded read-only exploration journeys.
 * @param props Trusted application bridge supplied by the fixed local entry.
 * @returns English application controls, graph, semantic alternatives and evidence inspector.
 */
export function ExplorerApp({ api, presentation }: ExplorerAppProps) {
  const controller = useMemo(() => presentation ?? new ExploreController(api), [api, presentation]);
  const view = useSyncExternalStore(controller.subscribe, controller.getSnapshot, controller.getSnapshot);
  const [pending, setPending] = useState<SourceWork | null>(null);
  const pendingWork = useRef<SourceWork | null>(null); const selectionAbort = useRef<AbortController | null>(null);
  const requestActive = useRef(false);
  const [retryImport, setRetryImport] = useState(false);
  const setWork = (work: SourceWork | null) => { pendingWork.current = work; requestActive.current = !!work; setPending(work); };
  const [loadingProgress, setLoadingProgress] = useState<ImportProgress | null>(null);
  const [status, setStatus] = useState('Starting…');
  const [families, setFamilies] = useState<readonly SourceFamily[]>(['fabric', 'findings']);
  const [text, setText] = useState(''); const [findingText, setFindingText] = useState('');
  const [direction, setDirection] = useState<'forward' | 'reverse' | 'both'>('both'); const [hops, setHops] = useState(2);
  const [causal, setCausal] = useState(false); const [pathStart, setPathStart] = useState<{ identity: ElementIdentity; label: string } | null>(null);
  const [resolvedTheme, setResolvedTheme] = useState<ResolvedTheme>(LIGHT_THEME);
  const [focusTicket, setFocusTicket] = useState(0); const selectionFocus = useRef(new InspectorFocusIntent());
  const operationFocus = useRef<{ previous: Element | null; ids: readonly string[] } | null>(null); const lastFocused = useRef<HTMLElement | null>(null);
  const shell = view.shell; const busy = !!pending; const ready = !!shell?.snapshot;
  const bindingKey = JSON.stringify(view.binding);
  useEffect(() => {
    setLoadingProgress(null); if (pending?.kind !== 'import') return;
    const sessionId = pending.binding.sessionId; const capability = pending.binding.capability;
    return pollImportProgress(async () => { const current = await api.getState(); return current.sessionId === sessionId && current.capability === capability ? current.progress : undefined; }, setLoadingProgress);
  }, [api, pending]);
  const displayLabels = useMemo(() => view.projection ? projectionLabelMap(view.projection) : new Map<string, string>(), [view.projection]);
  const [navigationOpen, setNavigationOpen] = useState(true); const [inspectorOpen, setInspectorOpen] = useState(true);
  const [navTab, setNavTab] = useState('sources'); const [elementMode, setElementMode] = useState('table');
  const [preferencesOpen, setPreferencesOpen] = useState(false); const [helpOpen, setHelpOpen] = useState(false);
  const [searchFiltersOpen, setSearchFiltersOpen] = useState(false); const [findingsFiltersOpen, setFindingsFiltersOpen] = useState(false);
  const [viewportWidth, setViewportWidth] = useState(typeof window === 'undefined' ? 1240 : window.innerWidth);
  const [navigationWidth, setNavigationWidth] = useState(276); const [inspectorWidth, setInspectorWidth] = useState(340);
  const [drawer, setDrawer] = useState<'navigation' | 'inspector' | null>(null);
  const geometry = workspaceGeometry(viewportWidth, navigationOpen, inspectorOpen, navigationWidth, inspectorWidth);
  const navigationVisible = geometry.drawer ? drawer === 'navigation' : navigationOpen;
  const inspectorVisible = geometry.drawer ? drawer === 'inspector' : inspectorOpen;
  const [paneFocus, setPaneFocus] = useState<string | null>(null);
  const revealPane = (pane: string) => { if (pane === 'navigation' || pane === 'search' || pane === 'elements' || pane === 'findings') { setNavigationOpen(true); setDrawer('navigation'); if (pane !== 'navigation') setNavTab(pane); } else if (pane === 'inspector') { setInspectorOpen(true); setDrawer('inspector'); } else setDrawer(null); setPaneFocus(pane); };
  const collapsePane = (pane: 'navigation' | 'inspector') => { document.getElementById(`show-${pane}`)?.focus(); setDrawer(null); if (pane === 'navigation') setNavigationOpen(false); else setInspectorOpen(false); };
  useEffect(() => { const resize = () => setViewportWidth(window.innerWidth); window.addEventListener('resize', resize); return () => window.removeEventListener('resize', resize); }, []);
  useLayoutEffect(() => { if (!paneFocus) return; const id = paneFocus === 'search' ? 'search-text' : paneFocus === 'inspector' ? 'inspector-heading' : paneFocus === 'elements' ? 'elements-heading' : paneFocus === 'findings' ? 'finding-text' : `${paneFocus}-heading`; document.getElementById(id)?.focus(); setPaneFocus(null); }, [paneFocus, navigationVisible, inspectorVisible, navTab]);
  const [canvasState, setCanvasState] = useState({ ready: false, focusable: false });
  const canvasAvailability = useCallback((ready: boolean, focusable: boolean) => setCanvasState(previous => previous.ready === ready && previous.focusable === focusable ? previous : { ready, focusable }), []);
  const helpDialog = useRef<HTMLDialogElement>(null);
  useEffect(() => { if (!helpOpen || !helpDialog.current) return; const previous = document.activeElement as HTMLElement | null; helpDialog.current.showModal(); document.getElementById('help-close')?.focus(); return () => { helpDialog.current?.close(); if (previous?.isConnected) previous.focus(); }; }, [helpOpen]);
  const refreshShell = async () => { const next = await api.getState(); await controller.setShell(next); return next; };
  const binding = (pick = false) => ({ sessionId: shell!.sessionId, capability: pick ? null : shell!.capability, generation: pick ? null : shell!.snapshot?.generation ?? null });
  useEffect(() => { let active = true; void refreshShell().then(next => { if (active) setStatus(next.warning ?? 'Open local sources to begin.'); }).catch(() => { if (active) setStatus('Application initialization failed. Close and restart the application.'); }); return () => { active = false; selectionAbort.current?.abort(); void controller.dispose(); }; }, [controller]);
  useLayoutEffect(() => observeTheme(shell?.preferences.theme ?? 'system', window.matchMedia('(prefers-color-scheme: dark)'), theme => {
    document.documentElement.dataset.theme = theme.name; document.documentElement.style.colorScheme = theme.name;
    for (const [name, color] of Object.entries(theme.css)) document.documentElement.style.setProperty(name, color);
    setResolvedTheme(theme);
  }), [shell?.preferences.theme]);
  useEffect(() => { document.documentElement.dataset.reducedMotion = String(shell?.preferences.reducedMotion ?? false); }, [shell?.preferences.reducedMotion]);
  useLayoutEffect(() => { selectionFocus.current.reset(); }, [bindingKey]);
  useLayoutEffect(() => { if (selectionFocus.current.consume(focusTicket, view.selection?.element.id ?? null, bindingKey)) document.getElementById('inspector-heading')?.focus(); }, [focusTicket, view.selection, bindingKey]);
  useLayoutEffect(() => {
    const request = operationFocus.current; if (pending || !request) return;
    const target = request.ids.map(id => document.getElementById(id)).find(item => item instanceof HTMLElement && !item.matches(':disabled'));
    if (target && shouldRecoverFocus(request.previous, document.activeElement, document.body)) target.focus();
    operationFocus.current = null;
  }, [pending, shell?.capability, shell?.snapshot?.generation]);
  useEffect(() => { const listener = (event: FocusEvent) => { if (event.target instanceof HTMLElement) lastFocused.current = event.target; }; document.addEventListener('focusin', listener); return () => { document.removeEventListener('focusin', listener); selectionFocus.current.reset(); }; }, []);
  useLayoutEffect(() => { if (!pending && !operationFocus.current && lastFocused.current && !lastFocused.current.isConnected && document.activeElement === document.body) document.getElementById('main-workspace')?.focus(); }, [view.projection, view.selection, pending, bindingKey]);
  useEffect(() => { setPathStart(null); }, [view.binding?.sessionId, view.binding?.generation]);
  const cancel = async () => {
    selectionAbort.current?.abort();
    const work = pendingWork.current; if (!work || !requestActive.current) { await controller.cancel(); return; }
    try { if (work.kind === 'selection') await api.cancelSelection(work.id); else await api.cancelRequest(work.binding, crypto.randomUUID(), work.id); setStatus(work.kind === 'selection' ? 'Cancellation requested. Close any native dialog to continue.' : 'Cancellation requested. The accepted snapshot remains available.'); }
    catch { setStatus('The operation may already have completed.'); }
  };
  const open = async () => {
    if (!shell || busy || pendingWork.current || !families.length) return;
    operationFocus.current = { previous: document.activeElement, ids: ['open'] };
    const id = crypto.randomUUID(); const abort = new AbortController(); selectionAbort.current = abort;
    setRetryImport(false); setWork({ id, kind: 'selection', binding: binding(true) }); setStatus('Choose a project folder. Its selected sources will load automatically.');
    try {
      const result = await openAndLoadSources({ api, initial: shell, families, selectionId: id, importId: crypto.randomUUID(), signal: abort.signal, refresh: refreshShell,
        onImport: work => { setWork(work); setStatus('Importing read-only sources; the accepted snapshot remains available.'); }, onRequestSettled: () => { requestActive.current = false; } });
      const messages: Record<OpenSourcesResult, string> = { ready: 'Snapshot ready. Sources were not modified.', 'selection-incomplete': 'Source selection was not completed.', 'selection-failed': 'Source selection failed. No source data was changed.', 'no-sources': 'No source files were selected.', cancelled: 'Loading cancelled. Any previous snapshot is retained.', 'import-rejected': 'Import rejected. Any previous snapshot is retained.', 'import-failed': 'Import failed. Any previous snapshot is retained.' };
      setStatus(messages[result]);
      const current = controller.getSnapshot().shell; const retry = result !== 'ready' && !!current?.capability && !!current.sources.length && !current.snapshot;
      setRetryImport(retry); operationFocus.current = { previous: operationFocus.current?.previous ?? null, ids: result === 'ready' ? ['show-graph', 'open'] : retry ? ['retry-import', 'close', 'open'] : ['open'] };
    } finally { selectionAbort.current = null; setWork(null); }
  };
  const importSources = async (update: boolean) => {
    const current = controller.getSnapshot().shell; if (!current?.capability || busy || pendingWork.current) return;
    operationFocus.current = { previous: document.activeElement, ids: update ? ['refresh'] : ['retry-import', 'show-graph', 'open'] };
    const id = crypto.randomUUID(); const context = { sessionId: current.sessionId, capability: current.capability, generation: current.snapshot?.generation ?? null };
    setRetryImport(false); setWork({ id, kind: 'import', binding: context }); setStatus('Importing read-only sources; the accepted snapshot remains available.');
    try { const response = await (update ? api.refreshSnapshot(context, id) : api.importSnapshot(context, id, current.sources.map(item => item.sourceId))) as { status: string }; setStatus(response.status === 'ok' ? 'Snapshot ready. Sources were not modified.' : 'Import rejected. Any previous snapshot is retained.'); }
    catch { setStatus('Import failed. Any previous snapshot is retained.'); }
    finally { requestActive.current = false; try { await refreshShell(); } catch { setStatus('The latest source state could not be loaded. Close sources and try again.'); } finally { const latest = controller.getSnapshot().shell; setRetryImport(!update && !!latest?.capability && !!latest.sources.length && !latest.snapshot); setWork(null); } }
  };
  const close = async () => { if (!shell || busy || pendingWork.current) return; operationFocus.current = { previous: document.activeElement, ids: ['open'] }; try { await controller.cancel(); await api.closeRoots(binding(), crypto.randomUUID()); await refreshShell(); setRetryImport(false); setStatus('Sources closed.'); } catch { setStatus('Could not close sources.'); } };
  const inspect = (id: string, action: () => Promise<void>) => {
    setInspectorOpen(true); setDrawer('inspector');
    const ticket = selectionFocus.current.request(id, JSON.stringify(controller.getSnapshot().binding));
    void action().then(() => { const current = controller.getSnapshot(); if (selectionFocus.current.complete(ticket, current.selection?.element.id ?? null, JSON.stringify(current.binding))) setFocusTicket(ticket); });
  };
  const select = (identity: ElementIdentity) => inspect(elementKey(identity), () => controller.select(identity));
  const selectedVertex = view.selection && 'kind' in view.selection.element ? view.selection.element : null;
  const relations = view.filter.relations.length ? view.filter.relations : Object.keys(RELATION_DIRECTIONS) as RelationClass[];
  const traversal = { direction, causalOnly: causal, relations, limits: { maxVertices: 2000, maxEdges: 8000, maxVisitedVertices: 10000, maxScannedEdges: 50000, maxHops: hops } };
  useEffect(() => {
    const listener = (event: KeyboardEvent) => {
      if (event.defaultPrevented || preferencesOpen || helpOpen) return;
      const target = event.target; const editing = target instanceof HTMLElement && (target.matches('input,textarea,select') || target.isContentEditable);
      if (!editing && !event.isComposing && !event.altKey && (event.ctrlKey || event.metaKey) && event.key === ',') { event.preventDefault(); document.getElementById('menu-file')?.focus(); setPreferencesOpen(true); return; }
      const search = document.getElementById('search-text') as HTMLInputElement | null; const fit = document.getElementById('fit-graph') as HTMLButtonElement | null;
      const action = keyboardAction(event, { editing, search: !!search && !search.disabled, fit: !!fit && !fit.disabled, back: view.history.canBack, forward: view.history.canForward, activeWork: !!pending || view.busy.length > 0 });
      if (!action) return; event.preventDefault();
      if (action === 'search') revealPane('search'); else if (action === 'fit') fit?.click(); else if (action === 'back') void controller.back(); else if (action === 'forward') void controller.forward(); else void cancel();
    }; window.addEventListener('keydown', listener); return () => window.removeEventListener('keydown', listener);
  }, [controller, pending, shell, view.busy, view.history, preferencesOpen, helpOpen]);
  const menus: readonly MenuGroup[] = [
    { id: 'menu-file', label: 'File', commands: [
      { id: 'menu-open', label: 'Open sources…', disabled: !shell || busy || !!shell.capability || !families.length, action: () => { void open(); } },
      { id: 'menu-refresh', label: 'Refresh snapshot', disabled: busy || !ready, action: () => { void importSources(true); } },
      { id: 'menu-close', label: 'Close sources', disabled: busy || !shell?.capability, action: () => { void close(); } },
      { id: 'menu-cancel', label: 'Cancel operation', shortcut: 'Escape', disabled: !busy && !view.busy.length, action: () => { void cancel(); } },
      { id: 'preferences-open', label: 'Preferences…', shortcut: 'Ctrl/Cmd+,', action: () => setPreferencesOpen(true) }] },
    { id: 'menu-view', label: 'View', commands: [
      ...['sources', 'search', 'findings', 'elements'].map(pane => ({ id: `menu-${pane}`, label: pane.charAt(0).toUpperCase() + pane.slice(1), action: () => { if (pane === 'sources') { setNavTab('sources'); revealPane('navigation'); } else revealPane(pane); } })),
      { id: 'menu-graph', label: 'Graph', action: () => revealPane('graph') },
      { id: 'menu-navigation-visible', label: 'Navigation pane', checked: navigationVisible, action: () => navigationVisible ? collapsePane('navigation') : revealPane('navigation') },
      { id: 'menu-inspector-visible', label: 'Inspector pane', checked: inspectorVisible, action: () => inspectorVisible ? collapsePane('inspector') : revealPane('inspector') },
      ...([['zoom-in','Zoom in'], ['zoom-out','Zoom out'], ['fit-graph','Fit graph'], ['focus-selected','Focus selected']] as const).map(([id,label]) => ({ id: `menu-${id}`, label, disabled: !canvasState.ready || (id === 'focus-selected' && !canvasState.focusable), reason: id === 'focus-selected' ? 'Select an element visible in the graph.' : 'Wait for the graph display to be ready.', action: () => { document.getElementById(id)?.click(); } })),
      { id: 'menu-reset-widths', label: 'Reset pane widths', action: () => { setNavigationWidth(276); setInspectorWidth(340); } }] },
    { id: 'menu-navigate', label: 'Navigate', commands: [
      { id: 'menu-back', label: 'Back', shortcut: 'Alt+←', disabled: !view.history.canBack, action: () => { void controller.back(); } },
      { id: 'menu-forward', label: 'Forward', shortcut: 'Alt+→', disabled: !view.history.canForward, action: () => { void controller.forward(); } },
      { id: 'menu-explore', label: 'Explore selected neighbourhood', disabled: !selectedVertex, action: () => { document.getElementById('expand')?.click(); } },
      { id: 'menu-path-start', label: 'Use selected as path start', disabled: !selectedVertex, action: () => setPathStart({ identity: selectedVertex!.identity, label: selectedVertex!.label }) },
      { id: 'menu-path', label: 'Find path to selected', disabled: !pathStart || !selectedVertex, action: () => { void controller.path(pathStart!.identity, selectedVertex!.identity, traversal); } }] },
    { id: 'menu-help', label: 'Help', commands: [{ id: 'help-open', label: 'Help and keyboard bindings', action: () => setHelpOpen(true) }] }
  ];
  const filters = (finding: boolean) => <div className="filter-anchor"><button id={finding ? 'findings-filters' : 'search-filters'} aria-expanded={finding ? findingsFiltersOpen : searchFiltersOpen} onClick={() => finding ? setFindingsFiltersOpen(!findingsFiltersOpen) : setSearchFiltersOpen(!searchFiltersOpen)}>Filters</button><div className="filter-popover" hidden={!(finding ? findingsFiltersOpen : searchFiltersOpen)} onKeyDown={event => { if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); finding ? setFindingsFiltersOpen(false) : setSearchFiltersOpen(false); document.getElementById(finding ? 'findings-filters' : 'search-filters')?.focus(); } }}><FilterControls idPrefix={finding ? 'findings-filter' : 'filter'} filter={view.filter} ready={ready} projectIds={shell?.snapshot?.sources.map(item => item.projectId) ?? []} change={filter => { void controller.setFilter(filter); }}/><button id={finding ? 'findings-reset-filters' : 'reset-filters'} disabled={!ready} onClick={() => void controller.setFilter({ projectIds: [], families: [], findingStates: [], relations: [] })}>Reset filters</button><p className="muted">Filters affect results and the visible graph.</p></div></div>;
  return <div className="app-shell ergonomic-shell">
    <nav className="skip-links" aria-label="Skip navigation"><a href="#main-workspace" onClick={event => { event.preventDefault(); revealPane('graph'); }}>Skip to workspace</a><a href="#inspector-heading" onClick={event => { event.preventDefault(); revealPane('inspector'); }}>Skip to inspector</a></nav>
    <header className="app-header"><div className="app-brand"><h1>Fabric Explorer</h1><span className="badge">Read-only</span></div><ApplicationMenu groups={menus}/></header>
    <nav className="toolbar command-bar" aria-label="Source and history actions"><div className="command-group"><IconButton id="open" icon="open" label="Open sources…" primary disabled={!shell || busy || !!shell.capability || !families.length} reason={!shell ? 'Application initialization is in progress.' : busy ? 'Wait for current work to finish or cancel it.' : shell.capability ? 'Close current sources before opening another project.' : 'Select at least one source family.'} onClick={open}/>{retryImport && !!shell?.capability && !ready && <button id="retry-import" disabled={busy} onClick={() => void importSources(false)}>Retry import</button>}<IconButton id="refresh" icon="refresh" label="Refresh snapshot" disabled={busy || !ready} reason="Load a snapshot first." onClick={() => importSources(true)}/><IconButton id="close" icon="close" label="Close sources" reason="Open sources first; finish or cancel active work before closing." disabled={busy || !shell?.capability} onClick={close}/></div><div className="command-group"><IconButton id="back" icon="back" label="Back" reason="No earlier view in history." disabled={!view.history.canBack} onClick={() => controller.back()}/><IconButton id="forward" icon="forward" label="Forward" reason="No later view in history." disabled={!view.history.canForward} onClick={() => controller.forward()}/></div><IconButton id="cancel" icon="cancel" label="Cancel operation" reason="No operation is running." disabled={!busy && !view.busy.length} onClick={cancel}/><span className="toolbar-spacer"/><IconButton id="show-navigation" icon="navigation" label="Navigation" pressed={navigationVisible} onClick={() => navigationVisible ? collapsePane('navigation') : revealPane('navigation')}/><IconButton id="show-graph" icon="elements" label="Graph" onClick={() => revealPane('graph')}/><IconButton id="show-inspector" icon="inspect" label="Inspector" pressed={inspectorVisible} onClick={() => inspectorVisible ? collapsePane('inspector') : revealPane('inspector')}/></nav>
    <main id="main-workspace" className={`workspace ergonomic-workspace${geometry.drawer ? ' drawer-mode' : ''}`} style={{ gridTemplateColumns: geometry.drawer ? 'minmax(0,1fr)' : `${geometry.navigation}px ${navigationOpen ? 12 : 0}px minmax(360px,1fr) ${inspectorOpen ? 12 : 0}px ${geometry.inspector}px` }} tabIndex={-1} aria-label="Fabric exploration workspace">
      <aside className="workspace-pane navigation-pane" hidden={!navigationVisible} style={geometry.drawer ? { width: geometry.navigation } : undefined} aria-label="Navigation and elements"><div className="pane-heading"><h2 id="navigation-heading" tabIndex={-1}>Navigation</h2><button onClick={() => collapsePane('navigation')} aria-label="Collapse Navigation">×</button></div><div id="navigation-content" className="navigation-body"><div role="tablist" aria-label="Navigation sections" className="navigation-tabs" onKeyDown={event => { if (event.altKey || event.ctrlKey || event.metaKey || event.nativeEvent.isComposing) return; const tabs = ['sources','search','findings','elements']; const current = tabs.indexOf(navTab); const next = event.key === 'ArrowRight' ? (current + 1) % 4 : event.key === 'ArrowLeft' ? (current + 3) % 4 : event.key === 'Home' ? 0 : event.key === 'End' ? 3 : -1; if (next >= 0) { event.preventDefault(); setNavTab(tabs[next]!); document.getElementById(next === 3 ? 'show-elements' : `tab-${tabs[next]}`)?.focus(); } }}>{['sources','search','findings','elements'].map(pane => <button key={pane} id={pane === 'elements' ? 'show-elements' : `tab-${pane}`} role="tab" aria-selected={navTab === pane} aria-controls={`${pane}-content`} tabIndex={navTab === pane ? 0 : -1} onClick={() => setNavTab(pane)}>{pane.charAt(0).toUpperCase() + pane.slice(1)}</button>)}</div>
      <div id="sources-content" role="tabpanel" aria-labelledby="tab-sources" hidden={navTab !== 'sources'} className="pane-scroll">      <p className="muted">Choose a project folder. Direct .jsonl files in its .fabric and .findings directories are selected automatically; other locations use native file dialogs. Fabric import reads referenced companion material read-only. No project code is executed.</p>
      <fieldset id="families"><legend>Source families</legend>{(['fabric', 'findings', 'audit'] as const).map(family => <label key={family}><input type="checkbox" value={family} checked={families.includes(family)} disabled={!!shell?.capability || busy} onChange={event => setFamilies(event.target.checked ? [...families, family] : families.filter(item => item !== family))}/>{family}</label>)}</fieldset>
      <ul id="sources" className="source-list">{shell?.sources.map(item => <li key={item.sourceId}>{item.family}: {item.relativePath}</li>)}</ul>
      <SourceHealth shell={shell}/>
    </div>
      <div id="search-content" role="tabpanel" aria-labelledby="tab-search" hidden={navTab !== 'search'} className="pane-scroll">{filters(false)}<section><h2>Search</h2><form className="search-form" onSubmit={event => { event.preventDefault(); void controller.search(text); }}><label className="sr-only" htmlFor="search-text">Label or exact identity</label><input id="search-text" type="text" placeholder="Label or exact identity" value={text} onChange={event => setText(event.target.value)} disabled={!ready}/><button disabled={!ready}>Search</button></form>
        <Results page={view.search} select={select} labels={displayLabels}/><ResultPager id="search-next" label="Next search page" page={view.search} busy={view.busy.includes('search')} next={(retainedText, order) => { void controller.search(retainedText, order, true); }}/></section>
</div>
      <div id="findings-content" role="tabpanel" aria-labelledby="tab-findings" hidden={navTab !== 'findings'} className="pane-scroll">{filters(true)}      <section><h2>Findings</h2><form className="search-form" onSubmit={event => { event.preventDefault(); void controller.findings(findingText); }}><label className="sr-only" htmlFor="finding-text">Findings search</label><input id="finding-text" type="text" placeholder="Finding label or ID" value={findingText} onChange={event => setFindingText(event.target.value)} disabled={!ready}/><button disabled={!ready}>Find</button></form><Results page={view.findings} select={select} labels={displayLabels}/><ResultPager id="findings-next" label="Next findings page" page={view.findings} busy={view.busy.includes('findings')} next={retainedText => { void controller.findings(retainedText, true); }}/></section>
</div>
      <div id="elements-content" role="tabpanel" aria-labelledby="show-elements" hidden={navTab !== 'elements'} className="pane-scroll"><h2 id="elements-heading" tabIndex={-1}>Elements</h2><div className="row"><button aria-pressed={elementMode === 'table'} onClick={() => setElementMode('table')}>Table</button><button aria-pressed={elementMode === 'groups'} onClick={() => setElementMode('groups')}>Groups</button></div><div hidden={elementMode !== 'table'}><ElementTable projection={view.projection} selectedId={view.selection?.element.id ?? null} labels={displayLabels} onSelect={id => inspect(id, () => controller.selectElement(id))}/></div><div hidden={elementMode !== 'groups'}>      <section><h2>Overview groups</h2><label>Group by <select disabled={!ready} value={view.groupAxis} onChange={event => void controller.setGroupAxis(event.target.value as ExploreState['groupAxis'])}><option value="kind">Kind</option><option value="project">Project</option><option value="family">Family</option><option value="finding-state">Finding state</option></select></label><ul className="results">{view.groups?.groups.slice(0, 30).map(group => <li key={group.id}>{group.value}: {group.vertices} vertices, {group.edges} internal relations</li>)}</ul>{view.groups && <p className="muted">Showing {Math.min(30, view.groups.groups.length)} of {view.groups.groups.length} groups. Derived summaries. Ungrouped: {view.groups.ungroupedVertices} vertices. Cross-group relations: {view.groups.crossGroupEdges}.</p>}</section>

</div></div></div></aside>
      <PaneSplitter side="navigation" width={geometry.navigation} maximum={geometry.navigationMax} hidden={geometry.drawer || !navigationOpen} onChange={setNavigationWidth}/>
      <section className="graph-panel" aria-label="Graph workspace">
        <div className="graph-header"><h2 id="graph-heading" tabIndex={-1}>Graph</h2>
          <p className="visible-graph-counts"><strong>Visible graph</strong>: {view.projection?.vertices.length ?? 0} vertices · {view.projection?.edges.length ?? 0} relations · {view.projection ? view.projection.complete ? 'Current query complete' : 'Partial query; do not infer absence' : 'No query loaded'}<span className="hidden-graph-counts"> · Hidden globally: {view.projection?.hiddenVertices ?? '—'} vertices / {view.projection?.hiddenEdges ?? '—'} relations</span></p>
          <div className="row"><IconButton id="expand" icon="explore" label="Explore selected neighbourhood" disabled={!selectedVertex} reason="Select a vertex first." onClick={() => controller.neighbours({ ...traversal, identity: selectedVertex!.identity })}/><details className="graph-query-details"><summary>Query details</summary><div className="graph-counts"><p><strong>Snapshot totals</strong>: {shell?.snapshot?.counts.vertices ?? '—'} vertices · {shell?.snapshot?.counts.edges ?? '—'} relations · {shell?.snapshot?.counts.findings ?? '—'} findings</p><p className="counts"><strong>Filter matches</strong>: <span data-testid="count-vertices">{view.counts?.vertices ?? '—'}</span> vertices · <span data-testid="count-edges">{view.counts?.edges ?? '—'}</span> relations · <span data-testid="count-findings">{view.counts?.findings ?? '—'}</span> findings</p></div><p className="graph-guidance">This is a bounded neighbourhood or path, not the entire snapshot. Select or search a starting point, then Explore selected neighbourhood.</p><p>Omissions: {view.projection?.omissions.join(', ') || 'none'}. Arrows preserve original direction. Completeness applies to the current query scope.</p></details></div>
        </div>
        <details className="exploration-controls"><summary>Traversal and path options</summary><div className="graph-toolbar stack"><div className="row"><label>Traverse <select id="direction" value={direction} onChange={event => setDirection(event.target.value as typeof direction)}><option value="both">Both directions</option><option value="forward">Forward · from → to</option><option value="reverse">Reverse · to → from</option></select></label><label>Hops <input id="hops" type="number" min="0" max="32" value={hops} onChange={event => setHops(Math.max(0, Math.min(32, Math.floor(Number(event.target.value) || 0))))}/></label><label><input type="checkbox" checked={causal} onChange={event => setCausal(event.target.checked)}/> Causal only</label></div>
        <div className="row"><button disabled={!selectedVertex} onClick={() => setPathStart({ identity: selectedVertex!.identity, label: selectedVertex!.label })}>Use selected as path start</button><button id="find-path" disabled={!pathStart || !selectedVertex} onClick={() => void controller.path(pathStart!.identity, selectedVertex!.identity, traversal)}>Find path to selected</button></div>{pathStart && <p className="muted">Path start: {pathStart.label}. Select a destination, then Find path.</p>}
      </div></details>
        <GraphSurface view={view} controller={controller} palette={resolvedTheme.canvas} onAvailability={canvasAvailability}/>
      </section>
      <PaneSplitter side="inspector" width={geometry.inspector} maximum={geometry.inspectorMax} hidden={geometry.drawer || !inspectorOpen} onChange={setInspectorWidth}/>
      <aside className="workspace-pane inspector" style={geometry.drawer ? { width: geometry.inspector } : undefined} hidden={!inspectorVisible} aria-label="Selected evidence"><div className="pane-heading"><h2>Evidence</h2><button aria-controls="evidence-content" aria-expanded={inspectorVisible} onClick={() => collapsePane('inspector')}>Collapse Inspector</button></div>
        <div id="evidence-content" className="pane-scroll" tabIndex={0} role="region" aria-label="Evidence panel"><Inspector labels={displayLabels} element={view.selection?.element ?? null} attributes={view.selection?.attributes ?? null} endpoints={view.selection?.endpoints ?? []} subjects={view.selection?.subjectCandidates ?? []} onSelect={select} subjectIncomplete={selectedVertex?.kind === 'finding' && !view.selection?.subjectComplete} evidencePage={view.sourcePage && <section className="source-page" aria-label="Captured source page"><h3>Captured source bytes</h3><p className="muted">Byte offset {view.sourcePage.page.offset}; {view.sourcePage.page.byteLength} bytes. UTF-8 display may show replacement characters at byte boundaries.</p><pre id="source-text" tabIndex={0} role="region" aria-label="Captured source bytes">{view.sourcePage.text}</pre><div className="row"><button disabled={view.sourcePage.page.offset === '0'} onClick={() => void controller.pageSource(String(BigInt(view.sourcePage!.page.offset) > 4096n ? BigInt(view.sourcePage!.page.offset) - 4096n : 0n))}>Previous bytes</button><button id="source-next" disabled={view.sourcePage.page.eof} onClick={() => void controller.pageSource(String(BigInt(view.sourcePage!.page.offset) + BigInt(view.sourcePage!.page.byteLength)))}>Next bytes</button></div></section>} onSource={() => { void controller.pageSource(); }}/>
    </div>
      </aside>
    </main>
    <footer className="status-strip" role="region" aria-label="Application status"><p id="snapshot-state">{shell?.snapshot ? `Snapshot ${shell.snapshot.generation} · ${shell.snapshot.sources.length} sources` : 'No snapshot imported.'}</p>{view.error && <p className="error" role="alert">{view.error}</p>}{shell?.stale && <p className="warning">Previous snapshot retained after unsuccessful refresh.</p>}<p id="status" role="status">{pending?.kind === 'import' ? loadingProgress ? importProgressText(loadingProgress) : status : view.message ?? status}{view.busy.length ? ` Working: ${view.busy.join(', ')}.` : ''}</p></footer>
    <PreferencesDialog open={preferencesOpen} api={api} preferences={shell?.preferences ?? { version: 1, theme: 'system', reducedMotion: false }} onSaved={async () => { await refreshShell(); }} onClose={() => setPreferencesOpen(false)} onStatus={setStatus}/>
    <dialog id="help-dialog" ref={helpDialog} aria-labelledby="help-title" onCancel={() => setHelpOpen(false)}><header><h2 id="help-title">Help and keyboard bindings</h2></header><section className="help"><p>Open sources to load a snapshot automatically. Choose Search, Findings or Elements, then select an item. The inspector shows Overview, Relations, Evidence and Raw details. The graph shows a bounded neighbourhood or path; incomplete results do not prove absence.</p><p>Ctrl/Cmd+K: Search. Ctrl/Cmd+Shift+F: Fit graph. Alt+Left / Alt+Right: history. Ctrl/Cmd+,: Preferences. Escape: close a menu or dialog, or cancel active work. Arrow keys navigate tabs and menus. Arrow keys resize focused separators; Shift makes a larger step; Enter resets. Wheel zooms the graph; drag its background to pan.</p><p>Source content is displayed as inert text. Sources are never edited.</p></section><footer><button id="help-close" onClick={() => setHelpOpen(false)}>Close help</button></footer></dialog>
  </div>;
}

function Results({ page, select, labels }: { page: ExplorePage | null; select: (identity: ElementIdentity) => void; labels: ReadonlyMap<string, string> }) {
  if (!page) return <p className="muted">No results loaded.</p>;
  return <><ul className="results">{page.items.map(item => <li key={item.id}><button onClick={() => select(item.identity)} title={item.id}>{displayNodeLabel(item, labels)}<small>{item.kind}{item.kind === 'finding' ? ` · ${item.state} · ${item.severity}` : ''}</small></button></li>)}</ul><p className="muted">{page.items.length} shown; {page.hidden} remaining. {page.complete ? 'Last page.' : 'More results available.'}</p></>;
}
function FilterControls({ filter, change, ready, projectIds, idPrefix = 'filter' }: { idPrefix?: string; filter: Filter; change: (filter: Filter) => void; ready: boolean; projectIds: readonly string[] }) {
  return <div className="stack"><label>Project<select id={`${idPrefix}-project`} disabled={!ready} value={filter.projectIds[0] ?? ''} onChange={event => change({ ...filter, projectIds: event.target.value ? [event.target.value] : [] })}><option value="">All projects</option>{[...new Set(projectIds)].map(id => <option key={id} value={id}>{id}</option>)}</select></label>
    <label>Family<select id={`${idPrefix}-family`} disabled={!ready} value={filter.families[0] ?? ''} onChange={event => change({ ...filter, families: event.target.value ? [event.target.value as RecordFamily] : [] })}><option value="">All families</option>{['source', 'profile', 'assignment', 'context', 'product', 'assessment', 'decision'].map(value => <option key={value}>{value}</option>)}</select></label>
    <label>Finding state<select id={`${idPrefix}-state`} disabled={!ready} value={filter.findingStates[0] ?? ''} onChange={event => change({ ...filter, findingStates: event.target.value ? [event.target.value as FindingState] : [] })}><option value="">All states</option>{['open', 'resolved', 'verified', 'stuck', 'withdrawn', 'accepted'].map(value => <option key={value}>{value}</option>)}</select></label>
    <label>Relation<select id={`${idPrefix}-relation`} disabled={!ready} value={filter.relations[0] ?? ''} onChange={event => change({ ...filter, relations: event.target.value ? [event.target.value as RelationClass] : [] })}><option value="">All relations</option>{Object.keys(RELATION_DIRECTIONS).map(value => <option key={value}>{value}</option>)}</select></label></div>;
}
function GraphSurface({ view, controller, palette, onAvailability }: { view: ExploreState; controller: ExploreController; palette: CanvasPalette; onAvailability: (ready: boolean, focusable: boolean) => void }) {
  const container = useRef<HTMLDivElement>(null); const display = useRef<PhasedCanvasView | null>(null); const [unavailable, setUnavailable] = useState<string | null>(null); const [commit, setCommit] = useState<CanvasCommit | null>(null);
  useEffect(() => { display.current = new PhasedCanvasView(report => prepareCanvas(container.current!, id => { if (id) void controller.selectElement(id); }, report), setUnavailable, undefined, setCommit); return () => { display.current?.dispose(); display.current = null; }; }, [controller]);
  useEffect(() => { display.current?.setPalette(palette); }, [controller, palette]);
  useEffect(() => { if (!view.projection) setUnavailable(null); display.current?.sync(view.projection, view.layout, view.handles, view.selection?.element.id ?? null); }, [view.projection, view.layout, view.handles, view.selection]);
  const ready = !!commit && commit.projection === view.projection && commit.layout === view.layout && !unavailable;
  const focusable = !!view.selection && !!view.projection && [...view.projection.vertices, ...view.projection.edges].some(item => item.id === view.selection!.element.id);
  useEffect(() => { onAvailability(ready, focusable); }, [ready, focusable, onAvailability]);
  return <><div className="graph-toolbar row"><IconButton id="zoom-in" icon="zoom-in" label="Zoom in" reason="Wait for the graph display to be ready." onClick={() => { display.current?.action('zoom', 1.4); }} disabled={!ready}/><IconButton id="zoom-out" icon="zoom-out" label="Zoom out" reason="Wait for the graph display to be ready." onClick={() => { display.current?.action('zoom', .7); }} disabled={!ready}/><IconButton id="fit-graph" icon="fit" label="Fit graph" reason="Wait for the graph display to be ready." onClick={() => { display.current?.action('fit'); }} disabled={!ready}/><IconButton id="focus-selected" icon="focus" label="Focus selected" reason="Select an element visible in the ready graph." onClick={() => { if (view.selection) display.current?.action('focus', view.selection.element.id); }} disabled={!focusable || !ready}/></div><div className="graph-stage" aria-busy={!!view.projection && !ready && !unavailable}><div ref={container} data-canvas-ready={ready ? 'true' : 'false'} aria-hidden={!ready} style={{ visibility: !view.projection || !view.layout || unavailable ? 'hidden' : 'visible', opacity: ready ? 1 : 0, pointerEvents: !ready ? 'none' : 'auto' }} className="graph-canvas" role="img" aria-label="Directed graph; use the visible elements list for keyboard selection"/>{!!view.projection?.vertices.length && !ready && !unavailable && <div className="graph-empty" role="status"><p>Preparing graph display...</p></div>}{(!view.projection || !view.projection.vertices.length || unavailable) && <div className="graph-empty"><h2>{unavailable ? 'Graph unavailable' : view.projection ? 'No vertices in this view' : 'Explore recorded relationships'}</h2><p>{unavailable ?? (view.projection ? 'Reset filters or select another starting point.' : 'Open local fabric and findings sources to load a read-only snapshot.')}</p></div>}</div></>;
}