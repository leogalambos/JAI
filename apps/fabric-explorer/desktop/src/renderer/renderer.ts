// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Fixed local React entry; only the isolated named preload bridge reaches native operations. */
import { createElement } from 'react';
import { createRoot } from 'react-dom/client';
import type { DesktopBridge } from '../shell/bridge.js';
import { ExplorerApp } from './app.js';
declare global { interface Window { readonly fabricExplorer: DesktopBridge } }
const container = document.getElementById('root');
if (!container) throw new Error('Application root unavailable');
createRoot(container).render(createElement(ExplorerApp, { api: window.fabricExplorer }));
