/** Bounded JSON transport only; canonical source parsing and proof hashing belong to the maintained readers. */
import { ContractError } from './errors.js';
import { LIMITS } from './model.js';

function invalid(message: string): never { throw new ContractError('invalid-message', message); }

class ByteBudget {
  private used = 0;

  add(bytes: number): void {
    this.used += bytes;
    if (this.used > LIMITS.frameBytes) throw new ContractError('resource-limit', 'Wire frame exceeds its UTF-8 byte limit');
  }

  string(value: string, escaped: boolean): void {
    if (escaped) this.add(2);
    for (let index = 0; index < value.length; index++) {
      const code = value.charCodeAt(index);
      if (escaped && (code === 34 || code === 92)) this.add(2);
      else if (escaped && code < 32) this.add([8, 9, 10, 12, 13].includes(code) ? 2 : 6);
      else if (code < 0x80) this.add(1);
      else if (code < 0x800) this.add(2);
      else if (code >= 0xd800 && code <= 0xdbff) {
        const next = value.charCodeAt(++index);
        if (!(next >= 0xdc00 && next <= 0xdfff)) invalid('Unpaired Unicode surrogate in wire data');
        this.add(4);
      } else if (code >= 0xdc00 && code <= 0xdfff) invalid('Unpaired Unicode surrogate in wire data');
      else this.add(3);
    }
  }
}

function unicode(value: string): void {
  for (let index = 0; index < value.length; index++) {
    const code = value.charCodeAt(index);
    if (code >= 0xd800 && code <= 0xdbff) {
      const next = value.charCodeAt(++index);
      if (!(next >= 0xdc00 && next <= 0xdfff)) invalid('Unpaired escaped Unicode surrogate');
    } else if (code >= 0xdc00 && code <= 0xdfff) invalid('Unpaired escaped Unicode surrogate');
  }
}

function safeNumber(value: number): void {
  if (!Number.isSafeInteger(value) || Object.is(value, -0)) invalid('Wire numbers must be safe integers; source numbers require semantic tags');
}

function containerDepth(depth: number): void {
  if (depth >= LIMITS.wireDepth) throw new ContractError('resource-limit', 'Wire frame exceeds its physical nesting limit');
}

/**
 * Check JSON-compatible values and their encoded size without invoking getters or coercing source data.
 * @param value A candidate frame; plain/null-prototype objects and dense ordinary arrays are supported.
 * @returns Nothing when safe scalar values, physical depth and UTF-8 frame bounds hold.
 * @throws {ContractError} With invalid-message for lossy/unsafe values, or resource-limit for byte/depth exhaustion.
 */
export function assertWireValue(value: unknown): void {
  const budget = new ByteBudget();
  const active = new Set<object>();
  const visit = (item: unknown, depth: number): void => {
    if (item === null) { budget.add(4); return; }
    if (typeof item === 'string') { budget.string(item, true); return; }
    if (typeof item === 'boolean') { budget.add(item ? 4 : 5); return; }
    if (typeof item === 'number') { safeNumber(item); budget.add(String(item).length); return; }
    if (typeof item !== 'object') invalid('Wire data contains a value JSON cannot preserve');
    containerDepth(depth);
    if (active.has(item)) invalid('Cyclic wire data is unsupported');
    active.add(item);
    try {
      const array = Array.isArray(item);
      const prototype: unknown = Object.getPrototypeOf(item);
      if (prototype !== null && prototype !== (array ? Array.prototype : Object.prototype)) invalid('Only plain wire objects and ordinary arrays are supported');
      if (array && item.length * 2 + 1 > LIMITS.frameBytes) throw new ContractError('resource-limit', 'Array cannot fit the wire frame');
      const keys = Reflect.ownKeys(item);
      budget.add(2);
      if (array) {
        if (keys.length !== item.length + 1 || keys.some(key => typeof key !== 'string')) invalid('Sparse arrays and extra array properties are unsupported');
        budget.add(Math.max(0, item.length - 1));
        for (let index = 0; index < item.length; index++) {
          const descriptor = Object.getOwnPropertyDescriptor(item, String(index));
          if (!descriptor || !('value' in descriptor) || !descriptor.enumerable) invalid('Array elements must be enumerable data properties');
          visit(descriptor.value, depth + 1);
        }
      } else {
        let index = 0;
        for (const key of keys) {
          if (typeof key !== 'string') invalid('Symbol keys are unsupported in wire objects');
          const descriptor = Object.getOwnPropertyDescriptor(item, key);
          if (!descriptor || !('value' in descriptor) || !descriptor.enumerable) invalid('Wire objects cannot contain accessors or hidden properties');
          if (index++) budget.add(1);
          budget.string(key, true); budget.add(1); visit(descriptor.value, depth + 1);
        }
      }
    } finally { active.delete(item); }
  };
  try { visit(value, 0); }
  catch (error) {
    if (error instanceof ContractError) throw error;
    throw new ContractError('invalid-message', 'Wire data cannot be inspected safely');
  }
}

/**
 * Serialize an already constructed transport value without normalization or number coercion.
 * @param value A JSON-compatible frame; large/floating source numbers must be explicitly tagged.
 * @returns JSON text whose UTF-8 length is at most the frame limit.
 * @throws {ContractError} For unsupported values or exhausted byte/depth limits.
 */
export function encodeWire(value: unknown): string {
  assertWireValue(value);
  const text = JSON.stringify(value);
  if (typeof text !== 'string') invalid('Wire data has no JSON representation');
  return text;
}

/**
 * Parse a bounded wire frame, rejecting duplicates before native JSON parsing can discard them.
 * @param text Raw JSON text; exact keys remain distinct without NFC normalization.
 * @returns Plain JSON data, not an authenticated request or a canonically verified source record.
 * @throws {ContractError} For malformed/unsafe JSON, duplicate keys, invalid Unicode, or byte/depth exhaustion.
 */
export function parseWire(text: string): unknown {
  if (typeof text !== 'string') invalid('Wire frame must be JSON text');
  if (text.length > LIMITS.frameBytes) throw new ContractError('resource-limit', 'Wire frame exceeds its byte limit');
  new ByteBudget().string(text, false);
  let cursor = 0;
  const whitespace = () => {
    while (cursor < text.length) {
      const code = text.charCodeAt(cursor);
      if (code !== 32 && code !== 9 && code !== 13 && code !== 10) return;
      cursor++;
    }
  };
  const string = (): string => {
    if (text.charAt(cursor) !== '"') invalid('Expected a JSON string');
    const start = cursor++;
    while (cursor < text.length) {
      const code = text.charCodeAt(cursor++);
      if (code === 34) {
        const decoded: unknown = JSON.parse(text.slice(start, cursor));
        if (typeof decoded !== 'string') invalid('Expected a JSON string');
        unicode(decoded); return decoded;
      }
      if (code < 32) invalid('Unescaped control character in JSON string');
      if (code === 92) cursor++;
    }
    return invalid('Unterminated JSON string');
  };
  const number = /-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/y;
  const value = (depth: number): void => {
    whitespace();
    const character = text.charAt(cursor);
    if (character === '{') {
      containerDepth(depth); cursor++; whitespace();
      const names = new Set<string>();
      if (text.charAt(cursor) === '}') { cursor++; return; }
      while (true) {
        const key = string();
        if (names.has(key)) invalid('Duplicate JSON object key');
        names.add(key); whitespace();
        if (text.charAt(cursor++) !== ':') invalid('Expected object key separator');
        value(depth + 1); whitespace();
        if (text.charAt(cursor) === '}') { cursor++; return; }
        if (text.charAt(cursor++) !== ',') invalid('Expected object separator');
        whitespace();
      }
    }
    if (character === '[') {
      containerDepth(depth); cursor++; whitespace();
      if (text.charAt(cursor) === ']') { cursor++; return; }
      while (true) {
        value(depth + 1); whitespace();
        if (text.charAt(cursor) === ']') { cursor++; return; }
        if (text.charAt(cursor++) !== ',') invalid('Expected array separator');
      }
    }
    if (character === '"') { string(); return; }
    for (const literal of ['true', 'false', 'null']) if (text.startsWith(literal, cursor)) { cursor += literal.length; return; }
    number.lastIndex = cursor;
    const match = number.exec(text);
    if (!match) invalid('Invalid JSON value');
    const token = match[0];
    if (/[.eE]/.test(token)) invalid('Wire number syntax must be an integer; use semantic tags');
    safeNumber(Number(token)); cursor += token.length;
  };
  try {
    value(0); whitespace();
    if (cursor !== text.length) invalid('Trailing data after JSON value');
    return JSON.parse(text) as unknown;
  } catch (error) {
    if (error instanceof ContractError) throw error;
    throw new ContractError('invalid-message', 'Malformed JSON wire frame');
  }
}
