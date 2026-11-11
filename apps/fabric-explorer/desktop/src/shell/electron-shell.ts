/** Actual Electron wrapper around owned controller, path and document policy boundaries. */
import { app, BrowserWindow, dialog, ipcMain, session } from 'electron';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import type { BrokerPort, NamespaceRegistry } from '../broker/types.js';
import { initializeApplicationPaths, applicationWriteLocations } from './paths.js';
import type { DesktopPaths } from './paths.js';
import { PersistentNamespaceRegistry, PreferenceStore } from './preferences.js';
import { ShellController } from './controller.js';
import type { ImportSessionFactory, PickerPort } from './controller.js';
import type { ImportSessionPort } from '../import/session.js';
import type { QueryContinuation, QueryDrop, LayoutSelection, GroupSelection, ProjectionFilterSelection } from '../explore/types.js';
import { CHANNELS } from './bridge.js';
import { assertSafeArguments, authenticateSender, CONTENT_SECURITY_POLICY, installSessionPolicy } from './security.js';
import { createSourcePicker } from './source-picker.js';
/** Trusted construction dependencies; native tests may provide dialogs without exposing test methods to the renderer. */
export interface DesktopDependencies {
  /** Construct the main-only broker after application write roots have been fixed. */
  createBroker(paths: DesktopPaths, registry: NamespaceRegistry, excludedWrites: readonly string[]): BrokerPort;
  /**
   * Construct the app-owned importer only after native source admission.
   * @param input Admitted session, capability and source catalog.
   * @param broker Main-owned native source authority, never a renderer object.
   * @param paths Fixed private application destinations.
   * @returns Owned import lifetime without eagerly reading source data.
   * @throws {Error} When trusted composition resources are unavailable.
   */
  createImport?(input: Parameters<ImportSessionFactory>[0], broker: BrokerPort, paths: DesktopPaths): ImportSessionPort;
  readonly picker?: PickerPort;
}
/**
 * Configure app destinations before ready, then create one hardened local document.
 * @param dependencies Main-only factory and optional native-dialog adapter.
 * @param distributionDirectory Fixed compiled application directory, supplied by packaged entry.
 * @returns Completion after the initial window has loaded.
 * @throws {Error} For unsupported launch configuration, unsafe storage or initialization failure.
 */
export async function startDesktop(dependencies: DesktopDependencies, distributionDirectory: string): Promise<void> {
  assertSafeArguments(process.argv);
  const paths = initializeApplicationPaths({ appData: () => app.getPath('appData'), setPath: (name, value) => app.setPath(name, value), setLogsPath: value => app.setAppLogsPath(value), setCachePath: value => app.commandLine.appendSwitch('disk-cache-dir', value), setTemporaryEnvironment: value => { process.env.TMPDIR = value; process.env.TEMP = value; process.env.TMP = value; } });
  await app.whenReady();
  const localSession = session.fromPartition('fabric-explorer-local', { cache: false });
  // Clear queued Hunspell dictionary loads synchronously; the enable flag alone only affects renderers.
  localSession.setSpellCheckerLanguages([]);
  localSession.setSpellCheckerEnabled(false);
  const rendererDirectory = join(distributionDirectory, 'renderer');
  const documentUrl = pathToFileURL(join(rendererDirectory, 'index.html')).href;
  const assets = new Set(['index.html', 'renderer.js', 'renderer.css'].map(name => pathToFileURL(join(rendererDirectory, name)).href));
  installSessionPolicy({
    resource: handler => localSession.webRequest.onBeforeRequest((details, callback) => callback({ cancel: !handler(details.url) })),
    permissions: handler => { localSession.setPermissionCheckHandler(handler); localSession.setPermissionRequestHandler((_contents, _permission, callback) => callback(handler())); },
    downloads: handler => localSession.on('will-download', event => { if (!handler()) event.preventDefault(); }),
  }, assets);
  localSession.webRequest.onHeadersReceived((details, callback) => callback({ responseHeaders: { ...details.responseHeaders, 'Content-Security-Policy': [CONTENT_SECURITY_POLICY] } }));
  const broker = dependencies.createBroker(paths, new PersistentNamespaceRegistry(paths), applicationWriteLocations(paths));
  let window: BrowserWindow | null = null;
  let controller: ShellController | null = null;
  const cleanupTasks = new WeakMap<ShellController, Promise<void>>();
  const pendingCleanup = new Set<Promise<void>>();
  let quitting = false; let quitReady = false; let quitTask: Promise<void> | null = null;
  const cleanup = (owner: ShellController): Promise<void> => {
    const existing = cleanupTasks.get(owner); if (existing) return existing;
    const task = Promise.resolve().then(() => owner.dispose()).catch(() => { console.error('Fabric Explorer cleanup failed.'); });
    cleanupTasks.set(owner, task); pendingCleanup.add(task);
    void task.finally(() => pendingCleanup.delete(task)); return task;
  };
  const create = async () => {
    if (quitting) return;
    const current = new BrowserWindow({ width: 1100, height: 760, show: false, autoHideMenuBar: true, webPreferences: { preload: join(distributionDirectory, 'preload.cjs'), session: localSession, sandbox: true, contextIsolation: true, nodeIntegration: false, nodeIntegrationInWorker: false, webSecurity: true, allowRunningInsecureContent: false, webviewTag: false, devTools: false, spellcheck: false } });
    current.removeMenu();
    window = current;
    const picker: PickerPort = dependencies.picker ?? createSourcePicker({
      project: async () => { const result = await dialog.showOpenDialog(current, { title: 'Choose project association', properties: ['openDirectory'] }); return result.canceled ? null : result.filePaths[0] ?? null; },
      files: async (family, defaultPath) => { const result = await dialog.showOpenDialog(current, { title: family === 'fabric' ? 'Choose Fabric journals (referenced companion material is read-only)' : `Choose ${family} source files`, defaultPath, properties: ['openFile', 'multiSelections', 'dontAddToRecent'], filters: [{ name: 'JSON and JSON Lines sources', extensions: ['json', 'jsonl', 'ndjson'] }] }); return result.canceled ? null : result.filePaths; },
    });
    const owner = new ShellController(broker, picker, new PreferenceStore(paths), dependencies.createImport ? input => dependencies.createImport!(input, broker, paths) : undefined); controller = owner;
    current.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));
    current.webContents.on('will-navigate', event => event.preventDefault());
    current.webContents.on('will-redirect', event => event.preventDefault());
    current.webContents.on('will-attach-webview', event => event.preventDefault());
    current.webContents.on('render-process-gone', () => { void cleanup(owner); current.destroy(); });
    current.on('closed', () => { if (window === current) { window = null; controller = null; } void cleanup(owner); });
    await current.loadURL(documentUrl); if (!current.isDestroyed() && !quitting) current.show();
  };
  const authenticate = (event: Electron.IpcMainInvokeEvent): ShellController => {
    const current = window;
    if (!current || !controller) throw new Error('Session unavailable');
    authenticateSender(event, { sender: current.webContents, frame: current.webContents.mainFrame, session: localSession, url: documentUrl }, { session: event.sender.session, url: event.senderFrame?.url ?? '', destroyed: current.isDestroyed() || event.sender.isDestroyed() });
    return controller;
  };
  ipcMain.handle(CHANNELS.state, (event, value) => { const owner = authenticate(event); if (value !== undefined) throw new Error('Invalid state request'); return owner.state(); });
  ipcMain.handle(CHANNELS.request, (event, value) => authenticate(event).request(value));
  ipcMain.handle(CHANNELS.queryStart, (event, value) => authenticate(event).queryStart(value));
  ipcMain.handle(CHANNELS.searchFindings, (event, value) => authenticate(event).searchFindings(value));
  ipcMain.handle(CHANNELS.filterProjection, (event, value) => authenticate(event).filterProjection(value as ProjectionFilterSelection));
  ipcMain.handle(CHANNELS.queryNext, (event, value) => authenticate(event).queryNext(value as QueryContinuation));
  ipcMain.handle(CHANNELS.queryDrop, (event, value) => authenticate(event).queryDrop(value as QueryDrop));
  ipcMain.handle(CHANNELS.layout, (event, value) => authenticate(event).layout(value as LayoutSelection));
  ipcMain.handle(CHANNELS.groups, (event, value) => authenticate(event).groups(value as GroupSelection));
  ipcMain.handle(CHANNELS.cancelSelection, (event, value) => authenticate(event).cancelSelection(value));
  ipcMain.handle(CHANNELS.preferences, (event, value) => authenticate(event).savePreferences(value));
  app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
  app.on('activate', () => { if (!window && !quitting) void create().catch(() => app.quit()); });
  app.on('before-quit', event => {
    if (quitReady) return;
    event.preventDefault(); quitting = true;
    if (controller) void cleanup(controller);
    if (!quitTask) quitTask = Promise.allSettled([...pendingCleanup]).then(() => { quitReady = true; app.quit(); });
  });
  await create();
}
