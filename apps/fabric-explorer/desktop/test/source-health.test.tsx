// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Exact recorded provenance and diagnostic-context presentation, independent of source replay. */
import { renderToStaticMarkup } from 'react-dom/server';
import { expect, it } from 'vitest';
import { SourceHealth } from '../src/renderer/source-health.js';
import type { ShellState } from '../src/shell/controller.js';
import { revision, report } from './import-fixtures.js';
const source = revision();
const shell: ShellState = { sessionId: 'session', capability: 'capability', snapshot: { format: 'jai.fabric-explorer.snapshot/1', sessionId: 'session', generation: '1', sources: [source], counts: { vertices: '1', edges: '0', findings: '0' }, authorityGranted: false, freshAssessment: false }, sources: [], report: report(), stale: false, warning: null, preferences: { version: 1, theme: 'light', reducedMotion: false } };
it('exposes accepted source revisions, observed time and recorded verification fields without promoting them to authority', () => {
  const html = renderToStaticMarkup(SourceHealth({ shell }));
  for (const value of ['canonical', 'Chain', 'Replay', 'Public trust', 'Material', 'Recorded applicability', source.observedAt, source.digest, source.head!]) expect(html).toContain(value);
  expect(html).toContain('No viewing action grants authority'); expect(html).toContain('jai.fabric-explorer.fabric/1');
});
it('renders diagnostic contexts when source is null and preserves safe literal labels', () => {
  const state = { ...shell, sources: [{ sourceId: 'fabric', relativePath: 'broken.jsonl', projectId: 'project', rootId: 'root', family: 'fabric', readHandle: 'opaque' }], report: { ...report(), diagnostics: [{ code: 'invalid-model', message: '<broken>', severity: 'error', source: null }], diagnosticContexts: [{ sourceId: 'fabric', pointer: '/entry', sequence: '7' }], diagnosticTotal: '1' } } as ShellState;
  const html = renderToStaticMarkup(SourceHealth({ shell: state }));
  expect(html).toContain('broken.jsonl'); expect(html).toContain('/entry'); expect(html).toContain('[7]'); expect(html).toContain('&lt;broken&gt;');
});
it('uses an explicit empty state before any import', () => { expect(renderToStaticMarkup(SourceHealth({ shell: null }))).toContain('No import report yet.'); });
