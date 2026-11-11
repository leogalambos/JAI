// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Real admitted-descriptor equivalents exercise byte framing, one-pass parsing, tee and failures. */
import { createHash } from 'node:crypto';
import { mkdtemp, open, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { expect, it } from 'vitest';
import { importRecordedSources } from '../src/import/recorded-import.js';
import type { RecordedInput, RecordedReadHandle, RecordedWriteHandle } from '../src/import/recorded-import.js';
import type { CanonicalFact } from '../src/broker/semantic-types.js';
const add = { seq: 1, ts: '2026-11-11', hash: 'a'.repeat(64), prev: '0'.repeat(64), data: { op: 'add', reviewer: 'synthetic', target: 'recorded', findings: [{ id: 'F-1', title: 'Ω😀', severity: 'low', kind: 'gap', location: 'x', criterion: 'c', evidence: [], recommendation: 'r' }] } };
async function files(raw: Buffer, run: (input: RecordedInput, archive: string) => Promise<void>): Promise<void> {
  const dir = await mkdtemp(join(tmpdir(), 'jai-recorded-')); const source = join(dir, 'source'); const archive = join(dir, 'archive');
  await writeFile(source, raw); const read = await open(source, 'r'); const write = await open(archive, 'wx+');
  try { await run({ sourceId: 'synthetic', family: 'findings', byteLength: raw.length, sourceHandle: read, archiveHandle: write }, archive); }
  finally { await Promise.all([read.close(), write.close()]); await rm(dir, { recursive: true }); }
}
for (const terminator of ['\n', '\r\n', '\r', '']) it('retains exact row bytes and span for terminator' + JSON.stringify(terminator), async () => {
  const raw = Buffer.from(JSON.stringify(add) + terminator); const facts: CanonicalFact[] = [];
  await files(raw, async (input, archive) => {
    const observed = await importRecordedSources([input], fact => facts.push(fact), { cancelled: () => false });
    expect(observed[0]!.digest).toBe(createHash('sha256').update(raw).digest('hex'));
    expect(observed[0]!.verification.mode).toBe('recorded'); expect(observed[0]!.sequence).toBe('1');
    expect(facts).toHaveLength(1); expect(facts[0]!.origin.byteOffset).toBe('0'); expect(facts[0]!.origin.byteLength).toBe(String(raw.length));
    expect(await readFile(archive)).toEqual(raw);
  });
});
it('retains split CRLF and a multi-byte UTF8 scalar across read boundaries', async () => {
  const body = Buffer.from(JSON.stringify(add)); const second = Buffer.from(JSON.stringify({ ...add, seq: 2, data: { op: 'resolve', id: 'F-1', by: 'author', note: 'recorded' } }));
  const raw = Buffer.concat([Buffer.alloc(256 * 1024 - 1 - body.length, 32), body, Buffer.from('\r\n'), second, Buffer.from('\n')]);
  await files(raw, async (input, archive) => {
    const facts: CanonicalFact[] = []; await importRecordedSources([input], fact => facts.push(fact), { cancelled: () => false });
    expect(facts[0]!.origin.byteLength).toBe(String(256 * 1024 + 1)); expect((facts[0] as Extract<CanonicalFact, { kind: 'finding' }>).state).toBe('resolved'); expect(await readFile(archive)).toEqual(raw);
  });
  const padding = 256 * 1024 - 1 - body.indexOf(Buffer.from('Ω')); const split = Buffer.concat([Buffer.alloc(padding, 32), body]);
  await files(split, async input => { const facts: CanonicalFact[] = []; await importRecordedSources([input], fact => facts.push(fact), { cancelled: () => false }); expect((facts[0] as Extract<CanonicalFact, { kind: 'finding' }>).label).toBe('Ω😀'); });
});
it('writes all partial archive writes and never closes caller-owned handles', async () => {
  const raw = Buffer.from(JSON.stringify(add));
  await files(raw, async (input, archive) => {
    let writes = 0; const output: RecordedWriteHandle = { write: async (buffer, offset, length, position) => { writes++; return input.archiveHandle.write(buffer, offset, Math.min(length, 7), position); } };
    await importRecordedSources([{ ...input, archiveHandle: output }], () => {}, { cancelled: () => false });
    expect(writes).toBeGreaterThan(1); expect(await readFile(archive)).toEqual(raw);
    const probe = Buffer.alloc(1); expect((await input.sourceHandle.read(probe, 0, 1, 0)).bytesRead).toBe(1);
  });
});
it.each(['duplicate', 'truncated', 'invalid-utf8', 'blank-row'])('rejects %s source syntax without a partial successful observation', async mutation => {
  const raw = mutation === 'duplicate' ? Buffer.from('{"seq":1,"seq":2}\n') : mutation === 'truncated' ? Buffer.from('{"data":') : mutation === 'invalid-utf8' ? Buffer.from([0xc0, 0xaf]) : Buffer.from('\n');
  await files(raw, async input => { await expect(importRecordedSources([input], () => {}, { cancelled: () => false })).rejects.toMatchObject({ code: 'read-failed' }); });
});
it('rejects archive zero progress, read EOF and cancellation through owned boundaries', async () => {
  const raw = Buffer.from(JSON.stringify(add));
  await files(raw, async input => {
    const zero: RecordedWriteHandle = { write: async () => ({ bytesWritten: 0 }) };
    await expect(importRecordedSources([{ ...input, archiveHandle: zero }], () => {}, { cancelled: () => false })).rejects.toMatchObject({ code: 'read-failed' });
    const eof: RecordedReadHandle = { read: async () => ({ bytesRead: 0 }) };
    await expect(importRecordedSources([{ ...input, sourceHandle: eof }], () => {}, { cancelled: () => false })).rejects.toMatchObject({ code: 'read-failed' });
    await expect(importRecordedSources([input], () => {}, { cancelled: () => true })).rejects.toMatchObject({ code: 'cancelled' });
  });
});
it('checks cumulative input bytes before reading and includes the exact1GiB bound', async () => {
  await files(Buffer.alloc(0), async input => {
    let reads = 0; const eof: RecordedReadHandle = { read: async () => { reads++; return { bytesRead: 0 }; } };
    await expect(importRecordedSources([{ ...input, byteLength: 1024 ** 3 + 1, sourceHandle: eof }], () => {}, { cancelled: () => false })).rejects.toMatchObject({ code: 'resource-limit' }); expect(reads).toBe(0);
    await expect(importRecordedSources([{ ...input, byteLength: 1024 ** 3, sourceHandle: eof }], () => {}, { cancelled: () => false })).rejects.toMatchObject({ code: 'read-failed' }); expect(reads).toBe(1);
    await expect(importRecordedSources([{ ...input, byteLength: 600 * 1024 ** 2 }, { ...input, sourceId: 'second', byteLength: 600 * 1024 ** 2 }], () => {}, { cancelled: () => false })).rejects.toMatchObject({ code: 'resource-limit' });
  });
});
it('accepts empty sources without inventing format declarations and rejects optional audit explicitly', async () => {
  await files(Buffer.alloc(0), async input => {
    const seen = await importRecordedSources([{ ...input, family: 'fabric' }], () => { throw new Error('No facts expected'); }, { cancelled: () => false });
    expect(seen[0]!.head).toBe('0'.repeat(64)); expect(seen[0]!.sequence).toBe('0'); expect(seen[0]!.compatibility.declaredFormat).toBeNull();
    await expect(importRecordedSources([{ ...input, family: 'audit' }], () => {}, { cancelled: () => false })).rejects.toMatchObject({ code: 'incompatible-source' });
  });
});

it('preserves the supported UTF8 BOM dialect and exact source/archive bytes', async () => {
  const raw = Buffer.concat([Buffer.from([0xef, 0xbb, 0xbf]), Buffer.from(JSON.stringify(add) + '\n')]);
  await files(raw, async (input, archive) => { const facts: CanonicalFact[] = []; const seen = await importRecordedSources([input], fact => facts.push(fact), { cancelled: () => false }); expect(facts).toHaveLength(1); expect(facts[0]!.origin.byteLength).toBe(String(raw.length)); expect(seen[0]!.digest).toBe(createHash('sha256').update(raw).digest('hex')); expect(await readFile(archive)).toEqual(raw); });
});
it('cancels during acquisition before writing or emitting after the flag changes', async () => {
  const raw = Buffer.from(JSON.stringify(add));
  await files(raw, async (input, archive) => {
    let cancelled = false; let facts = 0;
    const source: RecordedReadHandle = { read: async (...args) => { const result = await input.sourceHandle.read(...args); cancelled = true; return result; } };
    await expect(importRecordedSources([{ ...input, sourceHandle: source }], () => facts++, { cancelled: () => cancelled })).rejects.toMatchObject({ code: 'cancelled' });
    expect(facts).toBe(0); expect(await readFile(archive)).toHaveLength(0);
  });
});
it('redacts controlled read and disk-full archive errors without a successful observation', async () => {
  const raw = Buffer.from(JSON.stringify(add));
  await files(raw, async input => {
    const source: RecordedReadHandle = { read: async () => { throw new Error('/private/source native failure'); } };
    await expect(importRecordedSources([{ ...input, sourceHandle: source }], () => {}, { cancelled: () => false })).rejects.toMatchObject({ code: 'read-failed', message: 'The selected source or private archive could not be read.' });
    if (process.platform === 'linux') {
      const full = await open('/dev/full', 'w');
      try { await expect(importRecordedSources([{ ...input, archiveHandle: full }], () => {}, { cancelled: () => false })).rejects.toMatchObject({ code: 'read-failed' }); }
      finally { await full.close(); }
    }
  });
});
it('uses one bounded source read for each owned chunk and no fact transport round trip', async () => {
  const raw = Buffer.from(JSON.stringify(add));
  await files(raw, async input => {
    let reads = 0; const source: RecordedReadHandle = { read: async (...args) => { reads++; return input.sourceHandle.read(...args); } };
    let sameWorkerValue: CanonicalFact | null = null;
    await importRecordedSources([{ ...input, sourceHandle: source }], fact => { sameWorkerValue = fact; }, { cancelled: () => false });
    expect(reads).toBe(1); expect(sameWorkerValue).toMatchObject({ kind: 'finding', label: 'Ω😀' });
  });
});

it('retains the prior explicit unsupported product boundary for a well-formed saved audit', async () => {
  const document = { format: 'jai.gen2-audit/1', head: 'a'.repeat(64), read_only: true, authority_granted: false };
  const raw = Buffer.from(JSON.stringify(document, null, 2) + '\n');
  await files(raw, async (input, archive) => {
    let facts = 0;
    await expect(importRecordedSources([{ ...input, family: 'audit' }], () => facts++, { cancelled: () => false })).rejects.toMatchObject({ code: 'incompatible-source' });
    expect(facts).toBe(0); expect(await readFile(archive)).toHaveLength(0);
  });
});

import { RecordedRowFramer } from '../src/import/recorded-import.js';
it('enforces inclusive body limits independently of0/1/2terminator bytes at the actual framer boundary', () => {
  for (const terminal of ['', '\n', '\r', '\r\n']) {
    const output: [string, number, number][] = [];
    const framer = new RecordedRowFramer((body, offset, span) => output.push([body.toString(), offset, span]), 8);
    for (const byte of Buffer.from('12345678' + terminal)) framer.push(Buffer.from([byte]));
    framer.finish(); expect(output).toEqual([['12345678', 0, 8 + terminal.length]]);
    const large = new RecordedRowFramer(() => { throw new Error('Oversized body must not emit'); }, 8);
    expect(() => { large.push(Buffer.from('123456789' + terminal)); large.finish(); }).toThrow(/limit/);
  }
  expect(() => new RecordedRowFramer(() => {}, 100 * 1024 * 1024 + 1)).toThrow(/limit/);
  expect(() => new RecordedRowFramer(() => {}, 0)).toThrow(/limit/);
});
it('retains bounded observed format and source sequence in a failure without rereading', async () => {
  const raw = Buffer.from('{"format":8,"protocol":"recorded-unsupported","sequence":42}\n');
  await files(raw, async input => {
    await expect(importRecordedSources([{ ...input, family: 'fabric' }], () => {}, { cancelled: () => false })).rejects.toMatchObject({ code: 'incompatible-source', diagnostic: { sourceId: 'synthetic', sequence: '1', pointer: '', code: 'incompatible-source' }, compatibility: [{ sourceId: 'synthetic', family: 'fabric', declaredFormat: '8', declaredProtocol: 'recorded-unsupported', supported: false }] });
  });
});

it('keeps duplicate and descending recorded claims while physical locators stay distinct', async () => {
  const rows = [
    { ...add, seq: 99 },
    { ...add, seq: 99, data: { ...add.data, findings: [{ ...add.data.findings[0], id: 'F-2' }] } },
    { ...add, seq: 1, data: { op: 'resolve', id: 'F-1', by: 'author', note: 'descending claim is recorded content' } },
  ];
  const lines = rows.map(row => Buffer.from(JSON.stringify(row) + '\n')); const raw = Buffer.concat(lines);
  await files(raw, async (input, archive) => {
    const facts: CanonicalFact[] = []; const seen = await importRecordedSources([input], fact => facts.push(fact), { cancelled: () => false });
    expect(seen[0]!.sequence).toBe('3'); expect(seen[0]!.adapterVersion).toBe('jai.fabric-explorer.findings/2');
    expect(facts.map(fact => [fact.origin.sequence, fact.origin.byteOffset, fact.origin.byteLength])).toEqual([['1', '0', String(lines[0]!.length)], ['2', String(lines[0]!.length), String(lines[1]!.length)]]);
    expect(JSON.stringify(facts[0]!.kind === 'finding' && facts[0]!.attributes)).toContain('"value":"99"');
    expect(JSON.stringify(facts[0]!.kind === 'finding' && facts[0]!.attributes)).toContain('"value":"1"');
    expect(await readFile(archive)).toEqual(raw);
  });
});
