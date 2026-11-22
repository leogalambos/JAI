// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Literal, bounded recorded label behavior independently of broker I/O. */
import { expect, it, vi } from 'vitest';
import { recordedLabel } from '../src/import/recorded-label.js';

const versionId = 'a'.repeat(64);
const blobId = 'b'.repeat(64);
const input = { sourceId: 'source', versionId, family: 'product', attachments: [], locator: { rowOffset: 0, rowLength: 42, effectIndex: 0 },
  record: { owner: { layer: 1n, question: 'how' }, product_kind: 'answer', material: [blobId] } };

it('uses the exact recorded summary as literal normalized text and skips the broker', async () => {
  const read = vi.fn();
  expect(await recordedLabel({ ...input, record: { ...input.record, display_summary: ' <b>Ω</b>\n 🛠 ' } }, read))
    .toEqual({ text: 'L1 HOW · <b>Ω</b> 🛠', source: { kind: 'record-field', versionId, pointer: '/content/record/display_summary' } });
  expect(read).not.toHaveBeenCalled();
});

it('truncates by code points and retains exact companion provenance', async () => {
  const attachment = { blob_id: blobId, byte_length: 644n, media_type: 'text/plain',
    classification: 'internal', access_handle: 'admitted' };
  const read = vi.fn(async () => ({ kind: 'text' as const, text: '🛠'.repeat(161) }));
  const label = await recordedLabel({ ...input, attachments: [attachment] }, read);
  expect(label?.text).toBe('L1 HOW · ' + '🛠'.repeat(159) + '…');
  expect(label?.source).toEqual({ kind: 'companion-excerpt', versionId, pointer: '/content/record/material/0', blobId });
  expect(read).toHaveBeenCalledWith({ sourceId: 'source', versionId, blobId, byteLength: 644, media: 'text/plain', ...input.locator });
});

it('rejects an ambiguous attachment before requesting content', async () => {
  const attachment = { blob_id: blobId, byte_length: 5n, media_type: 'text/plain',
    classification: 'internal', access_handle: 'admitted' };
  const read = vi.fn();
  expect(await recordedLabel({ ...input, attachments: [attachment, attachment] }, read))
    .toEqual({ text: 'L1 HOW · answer summary unavailable', source: { kind: 'unavailable', versionId, reason: 'ambiguous-source' } });
  expect(read).not.toHaveBeenCalled();
});

it('retains exact pointers for an action and its recorded reason', async () => {
  const record = { message: { payload: { action: 'rework', reason: 'Restore the missing condition.' } } };
  expect(await recordedLabel({ ...input, family: 'decision', record })).toEqual({
    text: 'rework · Restore the missing condition.',
    source: { kind: 'record-field', versionId, pointer: '/content/record/message/payload/action' },
    additionalSources: [{ kind: 'record-field', versionId, pointer: '/content/record/message/payload/reason' }],
  });
});

it('uses the exact companion-derived subject without repeating its context', async () => {
  const companionSource = { kind: 'companion-excerpt' as const, versionId,
    pointer: '/content/record/material/0', blobId };
  const assessmentId = 'c'.repeat(64);
  expect(await recordedLabel({ ...input, versionId: assessmentId, family: 'assessment',
    record: { verdict: 'accepted' }, subject: { versionId, record: input.record,
      resolve: async () => ({ text: 'L1 HOW · Restore one file.', source: companionSource }) },
  })).toEqual({ text: 'L1 HOW · accepted · Restore one file.',
    source: { kind: 'record-field', versionId: assessmentId, pointer: '/content/record/verdict' },
    additionalSources: [companionSource] });
});
