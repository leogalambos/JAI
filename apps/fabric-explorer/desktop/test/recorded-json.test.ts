// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Direct native parsing must retain the recorded numeric token before projection. */
import { describe, expect, it } from 'vitest';
import { parseRecordedJSON } from '../src/import/recorded-json.js';

describe('recorded JSON direct parser', () => {
  it('preserves unsafe integer and integral float token types in one record', () => {
    const plain = JSON.parse('{"integer":9007199254740993,"float":1.0}') as { integer: number };
    expect(plain.integer).toBe(9007199254740992);
    const value = parseRecordedJSON('{"integer":9007199254740993,"float":1.0}', 'findings') as Record<string, unknown>;
    expect(value.integer).toBe(9007199254740993n);
    expect(typeof value.float).toBe('number');
  });
});

import { recordedEntries } from '../src/import/recorded-json.js';

it('keeps negative float zero, huge integer precision and all float extension bits', () => {
  const value = parseRecordedJSON('[-0,-0.0,1,1.0,1e0,900719925474099312345678901234567890,NaN,Infinity,-Infinity,1e400]', 'findings') as unknown[];
  expect(value.slice(0, 6)).toEqual([0n, -0, 1n, 1, 1, 900719925474099312345678901234567890n]);
  expect(Object.is(value[1], -0)).toBe(true); expect(Number.isNaN(value[6])).toBe(true);
  expect(value.slice(7)).toEqual([Infinity, -Infinity, Infinity]);
});

it('distinguishes marker-looking original raw and escaped strings from extensions', () => {
  const value = parseRecordedJSON('[' + String.raw`"\u0000JAI:0:NaN","\u0000JAI:1:Infinity","\u0000JAI:2:-Infinity","\u0000JAI:\u0033:NaN",NaN,Infinity,-Infinity,"NaN"` + ']', 'findings') as unknown[];
  expect(value.slice(0, 4)).toEqual(['\0JAI:0:NaN', '\0JAI:1:Infinity', '\0JAI:2:-Infinity', '\0JAI:3:NaN']);
  expect(Number.isNaN(value[4])).toBe(true); expect(value.slice(5)).toEqual([Infinity, -Infinity, 'NaN']);
});

it('retains source object member order even for integer keys and nested reordered objects', () => {
  const value = parseRecordedJSON('{"2":{"z":1,"a":2},"1":{"x":3,"y":4},"__proto__":5}', 'fabric') as Record<string, unknown>;
  expect(recordedEntries(value).map(([key]) => key)).toEqual(['2', '1', '__proto__']);
  expect(recordedEntries(value['2'] as object).map(([key]) => key)).toEqual(['z', 'a']);
  expect(recordedEntries(value['1'] as object).map(([key]) => key)).toEqual(['x', 'y']);
  expect(Object.getPrototypeOf(value)).toBe(Object.prototype);
  expect(Object.getOwnPropertyDescriptor(value, '__proto__')?.value).toBe(5n);
});

it.each(['{"x":1,"x":2}', String.raw`{"x":1,"\u0078":2}`, '[1,]', '{"a":}', '00', 'true false', '{"a":1,}', String.raw`"\q"`, 'NaN', 'Infinity', '-Infinity'])('rejects duplicate or malformed fabric JSON %s', text => {
  expect(() => parseRecordedJSON(text, 'fabric')).toThrow();
});

it('keeps surrogate code units and rejects only containers beyond depth64', () => {
  expect(parseRecordedJSON(String.raw`["\ud800","\udfff","\ud83d\ude00","\u0000\n\"\\"]`, 'findings')).toEqual(['\ud800', '\udfff', '😀', '\0\n"\\']);
  expect(() => parseRecordedJSON('['.repeat(64) + '0' + ']'.repeat(64), 'fabric')).not.toThrow();
  expect(() => parseRecordedJSON('['.repeat(65) + '0' + ']'.repeat(65), 'fabric')).toThrow(/nesting/);
});
