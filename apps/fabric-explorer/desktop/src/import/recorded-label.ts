// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Bounded, source-backed labels derived from admitted recorded fields. */
import type { MaterialExcerpt, ExcerptFailure } from '../broker/direct-types.js';

type Data = Record<string, any>;
type Locator = { rowOffset: number; rowLength: number; effectIndex: number };
export type RecordedLabelSource = { kind: 'record-field'; versionId: string; pointer: string } |
  { kind: 'companion-excerpt'; versionId: string; pointer: string; blobId: string } |
  { kind: 'unavailable'; versionId: string; reason: ExcerptFailure | 'no-text-source' | 'ambiguous-source' | 'binary' | 'empty-text' };
/** Presentation value for one exact admitted version. */
export interface RecordedLabel { readonly text: string; readonly source: RecordedLabelSource; readonly additionalSources?: readonly RecordedLabelSource[] }

/** Collapse the contract's Unicode whitespace for recorded labels and their queries.
 * @param value Literal input text.
 * @returns Text with single internal ASCII spaces.
 */
export function normalizeLabelWhitespace(value: string): string {
  return value.replace(/\p{White_Space}+/gu, ' ').replace(/^ | $/g, '');
}

function normalized(value: unknown, limit: number): string {
  if (typeof value !== 'string') return '';
  const clean = normalizeLabelWhitespace(value);
  let count = 0; let end = 0;
  for (const char of clean) {
    if (count === limit) return clean.slice(0, end) + '…';
    if (count < limit - 1) end += char.length;
    count++;
  }
  return clean;
}

function structured(record: Data): { text: string; pointer: string } | undefined {
  for (const [value, pointer] of [
    [record.display_summary, '/content/record/display_summary'],
    [record.message?.payload?.specification?.question, '/content/record/message/payload/specification/question'],
    [record.criteria?.[0]?.statement, '/content/record/criteria/0/statement'],
    [record.observation, '/content/record/observation'],
    [record.message?.payload?.reason, '/content/record/message/payload/reason'],
  ] as const) {
    const text = normalized(value, 160);
    if (text) return { text, pointer };
  }
  return undefined;
}

function contextOf(owner: Data | undefined): string {
  const layer = owner?.layer;
  const question = owner?.question;
  return (typeof layer === 'bigint' && layer >= 0n && layer <= 6n || typeof layer === 'number' && Number.isInteger(layer) && layer >= 0 && layer <= 6)
    ? 'L' + String(layer) + (typeof question === 'string' && /^(what|why|how|who|where|when)$/.test(question) ? ' ' + question.toUpperCase() : '') : '';
}

/**
 * Derive an exact version label from its admitted record and attached text declaration.
 * @param input Version, admitted source ID, record body and its registration attachments.
 * @param read Fixed-purpose companion read within the candidate import.
 * @returns Bounded presentation and exact provenance, or undefined for structural records.
 */
export async function recordedLabel(input: {
  sourceId: string; versionId: string; family: string; record: Data; attachments: readonly Data[];
  locator: Locator; subject?: { versionId: string; record: Data; resolve?: () => Promise<RecordedLabel | undefined> };
}, read?: MaterialExcerpt): Promise<RecordedLabel | undefined> {
  const { sourceId, versionId, family, record, attachments, subject } = input;
  const kind = family === 'product' ? record.product_kind : family === 'source' ? record.source_role : family;
  const supported = ['answer', 'bundle', 'finding', 'escalation', 'criteria', 'assessment', 'decision'];
  if (!supported.includes(kind)) return undefined;
  const context = contextOf(record.owner) || contextOf(subject?.record.owner);
  const label = (...parts: string[]) => normalized([context, ...parts].filter(Boolean).join(' · '), 192);
  const fallback = (reason: Extract<RecordedLabelSource, { kind: 'unavailable' }>['reason']): RecordedLabel =>
    ({ text: label(kind + ' summary unavailable'), source: { kind: 'unavailable', versionId, reason } });
  const field = structured(record);
  const action = record.message?.payload?.action;
  const verdict = normalized(record.verdict ?? (action === 'configure_procedure'
    && field?.pointer === '/content/record/message/payload/specification/question' ? undefined : action), 160);
  const verdictSource: RecordedLabelSource = { kind: 'record-field', versionId,
    pointer: record.verdict === undefined ? '/content/record/message/payload/action' : '/content/record/verdict' };
  const subjectField = subject && structured(subject.record);
  if (field) {
    const fieldSource: RecordedLabelSource = { kind: 'record-field', versionId, pointer: field.pointer };
    return verdict
      ? { text: label(verdict, field.text), source: verdictSource, additionalSources: [fieldSource] }
      : { text: label(field.text), source: fieldSource };
  }
  if (verdict) {
    if (subject && subjectField) return { text: label(verdict, subjectField.text), source: verdictSource,
      additionalSources: [{ kind: 'record-field', versionId: subject.versionId, pointer: subjectField.pointer }] };
    const resolved = await subject?.resolve?.();
    if (subject && resolved?.source.kind === 'companion-excerpt') {
      const prefix = contextOf(subject.record.owner);
      const body = prefix ? resolved.text.slice(prefix.length + 3) : resolved.text;
      return { text: label(verdict, body), source: verdictSource, additionalSources: [resolved.source] };
    }
    return { text: label(verdict), source: verdictSource };
  }
  const material = Array.isArray(record.material) ? record.material : [];
  const designated = attachments.flatMap(item => {
    const index = material.indexOf(item?.blob_id);
    return index >= 0 && typeof item.blob_id === 'string' && /^[0-9a-f]{64}$/.test(item.blob_id)
      ? [{ item, index }] : [];
  });
  const eligible = designated.filter(({ item }) => item.media_type === 'text/plain' || item.media_type === 'text/markdown');
  if (!eligible.length) return fallback(designated.length ? 'binary' : 'no-text-source');
  if (eligible.length !== 1 || designated.filter(({ index }) => index === eligible[0]!.index).length !== 1) return fallback('ambiguous-source');
  const { item, index } = eligible[0]!;
  if (material.lastIndexOf(item.blob_id) !== index) return fallback('ambiguous-source');
  const byteLength = Number(item.byte_length);
  if ((typeof item.byte_length !== 'bigint' && typeof item.byte_length !== 'number') || !Number.isSafeInteger(byteLength) || byteLength < 0
      || !['public', 'internal', 'confidential', 'restricted'].includes(item.classification) || typeof item.access_handle !== 'string' || !item.access_handle) return fallback('no-text-source');
  if (!read) return fallback('read-denied');
  const result = await read({ sourceId, versionId, blobId: item.blob_id, byteLength, media: item.media_type, ...input.locator });
  if (result.kind !== 'text') return fallback(result.kind);
  const lines = result.text.split(/\r\n?|\n/);
  const line = lines.find(value => normalized(value, 1) && !(item.media_type === 'text/markdown' && /^\s{0,3}#{1,6}(?:\s|$)/.test(value)));
  if (line === undefined) return fallback('empty-text');
  return { text: label(normalized(line, 160)), source: { kind: 'companion-excerpt', versionId,
    pointer: '/content/record/material/' + index, blobId: item.blob_id } };
}
