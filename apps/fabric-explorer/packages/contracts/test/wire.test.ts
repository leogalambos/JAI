/** Wire-boundary tests use real JSON/UTF-8 behavior, independently of operation schemas. */
import { describe, expect, it } from 'vitest';
import { LIMITS } from '../src/model.js';
import { ContractError } from '../src/errors.js';
import { assertWireValue, encodeWire, parseWire } from '../src/wire.js';

function expectCode(action: () => unknown, code: string): void {
  try { action(); throw new Error('Expected a contract rejection'); }
  catch (error) { expect(error).toBeInstanceOf(ContractError); expect((error as ContractError).code).toBe(code); }
}

describe('wire JSON boundary', () => {
  it('round-trips plain data, aliases and exact distinct Unicode keys', () => {
    const shared = { value: 'café ∑' };
    const value = { first: shared, second: shared, 'é': 1, 'e\u0301': 2 };
    expect(parseWire(encodeWire(value))).toEqual(value);
    expect(parseWire(' {"nested":[null,true,false,-7,"\\ud83d\\ude00"]} ')).toEqual({ nested: [null, true, false, -7, '😀'] });
  });

  it.each(['{"a":1,"a":2}', '{"a":1,"\\u0061":2}', '{"outer":{"x":0,"x":1}}'])('rejects exact duplicate keys: %s', text => {
    expectCode(() => parseWire(text), 'invalid-message');
  });

  it.each(['[1,]', '{"a" 1}', '{"a":', 'true false', '"unterminated', 'NaN', 'Infinity', '01'])('rejects malformed JSON: %s', text => {
    expectCode(() => parseWire(text), 'invalid-message');
  });

  it.each(['9007199254740992', '-9007199254740992', '1.5', '1.0', '1e0', '-0'])('rejects non-lossless administrative number syntax: %s', text => {
    expectCode(() => parseWire(text), 'invalid-message');
  });

  it('keeps safe integer boundaries and leaves tagged number strings untouched', () => {
    expect(parseWire('[9007199254740991,-9007199254740991]')).toEqual([Number.MAX_SAFE_INTEGER, -Number.MAX_SAFE_INTEGER]);
    expect(parseWire(encodeWire({ type: 'integer', value: '90071992547409931234567890' }))).toEqual({ type: 'integer', value: '90071992547409931234567890' });
  });

  it('enforces physical nesting at the exact boundary', () => {
    const allowed = '['.repeat(LIMITS.wireDepth) + '0' + ']'.repeat(LIMITS.wireDepth);
    expect(() => parseWire(allowed)).not.toThrow();
    expectCode(() => parseWire('[' + allowed + ']'), 'resource-limit');
    let nested: unknown = 0;
    for (let index = 0; index < LIMITS.wireDepth; index++) nested = [nested];
    expect(() => assertWireValue(nested)).not.toThrow();
    expectCode(() => assertWireValue([nested]), 'resource-limit');
  });

  it('accepts exactly 8 MiB UTF-8 and rejects an oversized frame before parsing', () => {
    const value = 'é'.repeat((LIMITS.frameBytes - 2) / 2);
    const frame = encodeWire(value);
    expect(new TextEncoder().encode(frame).byteLength).toBe(LIMITS.frameBytes);
    expect(parseWire(frame)).toBe(value);
    expectCode(() => parseWire(frame + ' '), 'resource-limit');
    expectCode(() => encodeWire(value + 'é'), 'resource-limit');
    expectCode(() => parseWire(' '.repeat(LIMITS.frameBytes + 1)), 'resource-limit');
  });

  it('counts escaping overhead rather than only input string length', () => {
    expect(encodeWire('\u0000\n"\\')).toBe(JSON.stringify('\u0000\n"\\'));
    expectCode(() => encodeWire('\u0000'.repeat(Math.floor((LIMITS.frameBytes - 2) / 6) + 1)), 'resource-limit');
  });

  it('accounts for four-byte Unicode scalars at the frame boundary', () => {
    const value = '😀'.repeat((LIMITS.frameBytes - 4) / 4) + 'é';
    const frame = encodeWire(value);
    expect(new TextEncoder().encode(frame).byteLength).toBe(LIMITS.frameBytes);
    expect(parseWire(frame)).toBe(value);
    expectCode(() => encodeWire(value + 'x'), 'resource-limit');
  });

  it.each(['"\\ud800"', '"\\udc00"', '{"\\ud800":1}'])('rejects escaped unpaired surrogates: %s', text => {
    expectCode(() => parseWire(text), 'invalid-message');
  });

  it('rejects invalid raw Unicode without normalizing valid source strings', () => {
    expect(() => parseWire('"\ud800"')).toThrowError(ContractError);
    expect(() => encodeWire('\ud800')).toThrowError(ContractError);
    expect(() => encodeWire({ '\udc00': 1 })).toThrowError(ContractError);
  });

  it('rejects accessors without invoking them and rejects lossy object kinds', () => {
    let invoked = false;
    const getter = Object.defineProperty({}, 'value', { enumerable: true, get() { invoked = true; return 1; } });
    expectCode(() => encodeWire(getter), 'invalid-message');
    expect(invoked).toBe(false);
    const hidden = Object.defineProperty({}, 'hidden', { value: 1 });
    for (const value of [undefined, 1n, NaN, Infinity, -0, new Date(0), new Map(), hidden, { value: undefined }, { [Symbol('key')]: 1 }]) {
      expectCode(() => assertWireValue(value), 'invalid-message');
    }
  });

  it('rejects cycles, sparse arrays, custom array properties and indexed accessors', () => {
    const cycle: unknown[] = []; cycle.push(cycle);
    const extra = Object.assign([1], { extra: 2 });
    const getter: unknown[] = [1]; Object.defineProperty(getter, '0', { enumerable: true, get() { throw new Error('Must not read getter'); } });
    for (const value of [cycle, new Array(2), extra, getter]) expect(() => encodeWire(value)).toThrowError(ContractError);
  });

  it('preserves prototype-looking JSON data without changing global prototypes', () => {
    const value = parseWire('{"__proto__":{"polluted":true},"constructor":"data"}');
    expect(Object.prototype.hasOwnProperty.call(value, '__proto__')).toBe(true);
    expect(Object.getPrototypeOf(value)).toBe(Object.prototype);
    expect(({} as Record<string, unknown>).polluted).toBeUndefined();
    expect(parseWire(encodeWire(value))).toEqual(value);
  });
});
