/** Native-test-only preload imports the unmodified production bridge before reporting runtime isolation. */
import '../src/preload.js';
import { ipcRenderer } from 'electron';
ipcRenderer.send('jai:native-smoke:isolation', { sandboxed: process.sandboxed, contextIsolated: process.contextIsolated });
