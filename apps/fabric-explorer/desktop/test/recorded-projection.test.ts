// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Exact recorded scalar/identity behavior and the retained genuine complete source oracle. */
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { expect, it } from 'vitest';
import { parseRecordedJSON } from '../src/import/recorded-json.js';
import { RecordedProjection, recordedSemantic, recordedVersionId, identityJSON, compareCodepoints } from '../src/import/recorded-projection.js';
const fixture = fileURLToPath(new URL('../../reader/test/fixtures/recorded-projection.json', import.meta.url));
const normalize = (value: any): any => {
  if (Array.isArray(value)) return value.map(normalize);
  if (value && typeof value === 'object') { const result = Object.fromEntries(Object.entries(value).map(([key, item]) => [key, normalize(item)])); if (result.type === 'object' && Array.isArray(result.entries)) result.entries.sort((a: any, b: any) => compareCodepoints(a.key, b.key)); return result; }
  return value;
};
const sortedJSON = (value: any): string => {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return '[' + value.map(sortedJSON).join(',') + ']';
  return '{' + Object.keys(value).sort(compareCodepoints).map(key => JSON.stringify(key) + ':' + sortedJSON(value[key])).join(',') + '}';
};
it('preserves the entire ordered693fact genuine valid oracle without Python runtime', async () => {
  const oracle = JSON.parse(await readFile(fixture, 'utf8')); const raw = Buffer.from(oracle.rawBase64, 'base64');
  const projection = new RecordedProjection('synthetic-fabric', 'fabric'); let offset = 0;
  for (const line of raw.toString('utf8').split(/(?<=\n)/)) { if (!line) continue; const length = Buffer.byteLength(line); projection.consume(parseRecordedJSON(line, 'fabric'), offset, length); offset += length; }
  const available = new Set(oracle.materialIds); const digest = createHash('sha256'); let count = 0;
  for await (const fact of projection.facts({ cancelled: () => false, materialAvailability: async (_source, id) => available.has(id) ? 'available' : 'missing' })) {
    const encoded = Buffer.from(sortedJSON(normalize(fact))); const prefix = Buffer.alloc(4); prefix.writeUInt32BE(encoded.length); digest.update(prefix); digest.update(encoded); count++;
  }
  expect(count).toBe(oracle.factCount); expect(digest.digest('hex')).toBe(oracle.factDigest);
});
it('counts exact finite/tagged and surrogate wire bytes inclusively', () => {
  for (const source of ['null', 'true', 'false', '"Ω東京"', '"\\ud800"', '0', '9007199254740993', '-0.0', 'NaN', '[1,2.0,"x"]', '{"1":1,"0":"\\udfff"}']) {
    const value = parseRecordedJSON(source, 'findings'); const tagged = recordedSemantic(value); const bytes = Buffer.byteLength(JSON.stringify(tagged.value));
    expect(tagged.size).toBe(bytes); expect(recordedSemantic(value, bytes).size).toBe(bytes); expect(() => recordedSemantic(value, bytes - 1)).toThrow();
  }
});
it('preserves floatbits and rejects float/surrogate identity values', () => {
  expect(recordedSemantic(parseRecordedJSON('-0.0', 'findings')).value).toEqual({ type: 'float64', bits: '8000000000000000' });
  expect(recordedSemantic(parseRecordedJSON('1.0', 'findings')).value).toEqual({ type: 'float64', bits: '3ff0000000000000' });
  expect(() => recordedVersionId(parseRecordedJSON('{"x":1.0}', 'fabric'))).toThrow();
  expect(() => recordedVersionId(parseRecordedJSON('{"x":"\\ud800"}', 'fabric'))).toThrow();
  expect(identityJSON(parseRecordedJSON('{"𐀀":1,"\ue000":2,"cafe\\u0301":3}', 'fabric'))).toBe('{"café":3,"\ue000":2,"𐀀":1}');
  expect(() => identityJSON(parseRecordedJSON('{"é":1,"e\\u0301":2}', 'fabric'))).toThrow();
});

it('rejects nonfinite lifecycle identity tokens while preserving findings float bit patterns', () => {
  for (const [source, bits] of [['NaN', '7ff8000000000000'], ['Infinity', '7ff0000000000000'], ['-Infinity', 'fff0000000000000'], ['1e400', '7ff0000000000000']] as const) {
    expect(recordedSemantic(parseRecordedJSON(source, 'findings')).value).toEqual({ type: 'float64', bits });
  }
  expect(() => recordedVersionId(parseRecordedJSON('{"x":1e400}', 'fabric'))).toThrow();
  expect(identityJSON(parseRecordedJSON('{"x":-0}', 'fabric'))).toBe('{"x":0}');
});
it('displays unverified chains, noncontiguous sequences and recorded effects without adjudication', async () => {
  const oracle = JSON.parse(await readFile(fixture, 'utf8')); const rows = Buffer.from(oracle.rawBase64, 'base64').toString('utf8').trimEnd().split('\n').map(line => JSON.parse(line));
  rows[0].sequence = 40; rows.at(-1).sequence = 77;
  const projection = new RecordedProjection('synthetic-fabric', 'fabric'); let offset = 0;
  for (const row of rows) { row.hash = 'e'.repeat(64); row.previous = 'd'.repeat(64); row.authority_proof = 'not-a-signed-proof'; const line = JSON.stringify(row) + '\n'; const length = Buffer.byteLength(line); projection.consume(parseRecordedJSON(line, 'fabric'), offset, length); offset += length; }
  const facts = []; for await (const fact of projection.facts({ cancelled: () => false })) facts.push(fact);
  expect(facts).toHaveLength(oracle.factCount); expect(facts[0]!.origin.sequence).toBe('1'); expect(projection.summary().head).toBe('e'.repeat(64)); expect(projection.summary().sequence).toBe(String(rows.length));
});

it('keeps explicit null recorded applicability instead of substituting a truth claim', async () => {
  const oracle = JSON.parse(await readFile(fixture, 'utf8')); const row = JSON.parse(Buffer.from(oracle.rawBase64, 'base64').toString('utf8').split('\n')[0]!);
  const parsed = parseRecordedJSON(JSON.stringify(row), 'fabric') as any; const effects = parsed.operations[0].data.effects;
  const id = recordedVersionId(effects[0].manifest); effects.push({ op: 'qualify', subject: id, applicable: null });
  const projection = new RecordedProjection('synthetic', 'fabric'); projection.consume(parsed, 0, Buffer.byteLength(JSON.stringify(row)));
  const facts = []; for await (const fact of projection.facts({ cancelled: () => false })) facts.push(fact);
  const use = facts.find(fact => fact.kind === 'use' && fact.point.ref.version_id === id);
  expect(use && use.kind === 'use' && use.state).toMatchObject({ type: 'object', entries: expect.arrayContaining([{ key: 'applicable', value: { type: 'null' } }]) });
});
it('keeps recorded empty rationale and NaN truthiness in the pure Findings reduction', async () => {
  const rows = [String.raw`{"seq":1,"ts":"t","hash":"a","data":{"op":"add","reviewer":"r","findings":[{"id":"F-1","title":"t","severity":"low","kind":"gap"}]}}`, String.raw`{"seq":2,"ts":"t","hash":"b","data":{"op":"verify","id":"F-1","ok":NaN,"rationale":""}}`];
  const projection = new RecordedProjection('synthetic', 'findings'); let offset = 0;
  for (const row of rows) { projection.consume(parseRecordedJSON(row, 'findings'), offset, Buffer.byteLength(row)); offset += Buffer.byteLength(row); }
  const facts = []; for await (const fact of projection.facts({ cancelled: () => false })) facts.push(fact);
  expect(facts[0]).toMatchObject({ kind: 'finding', state: 'verified' });
  expect(JSON.stringify(facts[0])).toContain('"key":"note","value":{"type":"string","value":""}');
});
