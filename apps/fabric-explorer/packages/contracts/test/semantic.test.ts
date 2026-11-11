import { describe, expect, it } from 'vitest';
import { assertSemantic, decodeSemantic, encodeSemantic } from '../src/semantic.js';
import { ContractError } from '../src/errors.js';

describe('lossless semantic transport', () => {
  it('preserves arbitrary integers and objects that resemble transport tags', () => {
    const input = { integer: 90071992547409931234567890n, negative: -8n, tag: { type: 'integer', value: '7' }, list: [null, true, 'café'] };
    const value = encodeSemantic(input);
    assertSemantic(value);
    const decoded = decodeSemantic(value) as Record<string, unknown>;
    expect(decoded.integer).toBe(input.integer);
    expect(decoded.tag).toEqual({ type: 'integer', value: '7' });
    expect(Object.getPrototypeOf(decoded)).toBe(null);
  });

  it('preserves findings normalization distinctions and prototype-like keys', () => {
    const input = Object.create(null) as Record<string, unknown>;
    input['é'] = 'é'; input['e\u0301'] = 'e\u0301'; input.__proto__ = 11n;
    const decoded = decodeSemantic(encodeSemantic(input)) as Record<string, unknown>;
    expect(Object.keys(decoded)).toEqual(['é', 'e\u0301', '__proto__']);
    expect(decoded['é']).not.toBe(decoded['e\u0301']);
    expect(decoded.__proto__).toBe(11n);
    expect(Object.getPrototypeOf(decoded)).toBe(null);
  });

  it('accepts exactly 64 source container levels and rejects the next', () => {
    let value: unknown = 1n;
    for (let i = 0; i < 64; i++) value = [value];
    expect(() => assertSemantic(encodeSemantic(value))).not.toThrow();
    expect(() => encodeSemantic([value])).toThrow(ContractError);
  });

  it.each([1.5, Number.NaN, Number.POSITIVE_INFINITY, 9007199254740992, undefined, new Date(0)])('rejects unsupported or lossy input %s', input => {
    expect(() => encodeSemantic(input)).toThrow(ContractError);
  });

  it('rejects cycles and duplicate exact semantic keys while retaining ordinary shared values', () => {
    const cyclic: unknown[] = []; cyclic.push(cyclic);
    expect(() => encodeSemantic(cyclic)).toThrow(ContractError);
    expect(() => assertSemantic({ type: 'object', entries: [{ key: 'a', value: { type: 'null' } }, { key: 'a', value: { type: 'null' } }] })).toThrow(ContractError);
    const shared = { a: 1n };
    expect(() => encodeSemantic([shared, shared])).not.toThrow();
  });

  it.each(['-0', '01', '+1', '1e3', '1.0', ''])('rejects ambiguous integer tag %s', value => {
    expect(() => decodeSemantic({ type: 'integer', value })).toThrow(ContractError);
  });

  it('rejects unknown semantic tag fields and does not execute object accessors', () => {
    expect(() => assertSemantic({ type: 'null', permission: true })).toThrow(ContractError);
    const input = Object.defineProperty({}, 'secret', { enumerable: true, get() { throw new Error('Accessor must not execute'); } });
    expect(() => encodeSemantic(input)).toThrow(ContractError);
  });

  it.each([1.5, 1.0, -0, Number.NaN, Number.POSITIVE_INFINITY, Number.NEGATIVE_INFINITY])('preserves findings float64 %s separately from source integers', value => {
    const tagged = encodeSemantic(value, 'findings');
    expect(tagged.type).toBe('float64');
    expect(Object.is(decodeSemantic(tagged, 'findings'), value)).toBe(true);
    expect(() => assertSemantic(tagged)).toThrow(ContractError);
    expect(encodeSemantic(1n, 'findings')).toEqual({ type: 'integer', value: '1' });
  });

  it('rejects accessor or symbol-bearing arrays without invoking an accessor', () => {
    const accessor = Object.defineProperty([1], '0', { enumerable: true, get() { throw new Error('Accessor must not execute'); } });
    expect(() => encodeSemantic(accessor)).toThrow(ContractError);
    const symbols = [1]; Object.defineProperty(symbols, Symbol('hidden'), { value: true });
    expect(() => encodeSemantic(symbols)).toThrow(ContractError);
  });

  it('does not execute accessors or custom iterators while validating unknown tagged data', () => {
    const tag = Object.defineProperty({}, 'type', { enumerable: true, get() { throw new Error('Do not execute'); } });
    expect(() => assertSemantic(tag)).toThrow(ContractError);
    const items: unknown[] = [];
    Object.defineProperty(items, Symbol.iterator, { value() { throw new Error('Do not execute'); } });
    expect(() => assertSemantic({ type: 'array', items })).toThrow(ContractError);
  });
});
