/** Sandboxed context-isolated preload exposes only the immutable application bridge. */
import { contextBridge, ipcRenderer } from 'electron';
import { createBridge } from './shell/bridge.js';
contextBridge.exposeInMainWorld('fabricExplorer', createBridge({ invoke: (channel, value) => ipcRenderer.invoke(channel, value) }));
