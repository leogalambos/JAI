// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** One native JSON value parse with lexical duplicate/depth guards and exact numeric tokens. */
import { ImportError } from './types.js';

/** Recorded integer tokens are bigint; number denotes a float token, including Findings extensions. */
export type RecordedValue = null | boolean | string | bigint | number | RecordedValue[] | RecordedObject;
/** Plain JSON object; original member order is retained separately without injected fields. */
export interface RecordedObject { [key: string]: RecordedValue }
const orders = new WeakMap<object, readonly string[]>();
const fail = (): never => { throw new ImportError('read-failed', 'The selected record has unreadable JSON structure.'); };
interface Container { readonly parent: number | null; readonly key: string | number | null; readonly keys: string[] | null }
interface Extension { readonly start: number; readonly end: number; readonly token: string }
const numberToken = /-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/y;

/**
 * Return source-order members, including integer-looking keys, without changing the object.
 * @param value A parsed or application-owned plain record.
 * @returns Every own enumerable member in source order, or ordinary insertion order for constructed records.
 */
export function recordedEntries(value: object): [string, RecordedValue][] {
  const record = value as RecordedObject;
  return (orders.get(value) ?? Object.keys(value)).map(key => [key, record[key]!] as [string, RecordedValue]);
}

/**
 * Parse a physical record once using the pinned native reviver's exact token context.
 * @param text Exact decoded record body; offsets are owned by the byte framer.
 * @param family Findings alone admits bare NaN/Infinity extensions.
 * @returns Lossless plain data; integer and float lexical types remain distinct.
 * @throws {ImportError} For duplicate members, unsupported JSON, depth overflow or missing native token context.
 */
export function parseRecordedJSON(text: string, family: 'fabric' | 'findings' | 'audit'): RecordedValue {
  const leading = text.trimStart(); const body = leading.trimEnd();
  if (!/^[ \t\r\n]*$/.test(text.slice(0, text.length - leading.length)) || !/^[ \t\r\n]*$/.test(leading.slice(body.length))) return fail();
  text = body;
  let at = 0;
  const containers: Container[] = []; const extensions: Extension[] = []; const markerIds = new Set<string>();
  const whitespace = (): void => { while (at < text.length && /[ \t\r\n]/.test(text[at]!)) at++; };
  const string = (decode: boolean): string => {
    if (text[at++] !== '"') return fail();
    const start = at - 1; let segment = at; let result = '';
    if (!decode) {
      let quote = text.indexOf('"', at);
      while (quote >= 0) {
        let slashes = 0; for (let before = quote - 1; before >= at && text.charCodeAt(before) === 92; before--) slashes++;
        if (slashes % 2 === 0) break;
        quote = text.indexOf('"', quote + 1);
      }
      if (quote < 0) return fail();
      at = quote + 1;
      if (text.startsWith('"\\u0000JAI:', start)) {
        const marker = /^"\\u0000JAI:([0-9]+):(NaN|Infinity|-Infinity)"$/.exec(text.slice(start, at));
        if (marker) markerIds.add(marker[1]!);
      }
      return '';
    }
    while (at < text.length) {
      const code = text.charCodeAt(at++);
      if (code === 34) {
        if (decode) result += text.slice(segment, at - 1);
        if (text.startsWith('"\\u0000JAI:', start)) {
          const marker = /^"\\u0000JAI:([0-9]+):(NaN|Infinity|-Infinity)"$/.exec(text.slice(start, at));
          if (marker) markerIds.add(marker[1]!);
        }
        return result;
      }
      if (code < 32) return fail();
      if (code !== 92) continue;
      if (decode) result += text.slice(segment, at - 1);
      const escaped = text[at++];
      if (escaped === 'u') {
        const hex = text.slice(at, at + 4);
        if (!/^[0-9a-fA-F]{4}$/.test(hex)) return fail();
        if (decode) result += String.fromCharCode(parseInt(hex, 16));
        at += 4;
      } else {
        const escapes: Record<string, string> = { '"': '"', '\\': '\\', '/': '/', b: '\b', f: '\f', n: '\n', r: '\r', t: '\t' };
        if (escaped === undefined || !Object.hasOwn(escapes, escaped)) return fail();
        if (decode) result += escapes[escaped];
      }
      segment = at;
    }
    return fail();
  };
  const value = (depth: number, parent: number | null, key: string | number | null): void => {
    whitespace(); const char = text[at];
    if (char === '{' || char === '[') {
      if (depth >= 64) throw new ImportError('resource-limit', 'Selected record nesting exceeds its limit.');
      const object = char === '{'; const keys = object ? [] as string[] : null; const seen = object ? new Set<string>() : null;
      const id = containers.length; containers.push({ parent, key, keys }); at++; whitespace();
      const closing = object ? '}' : ']';
      if (text[at] === closing) { at++; return; }
      let index = 0;
      while (at < text.length) {
        let child: string | number = index++;
        if (object) {
          child = string(true);
          if (seen!.has(child)) return fail();
          seen!.add(child); keys!.push(child); whitespace();
          if (text[at++] !== ':') return fail();
        }
        value(depth + 1, id, child); whitespace();
        if (text[at] === closing) { at++; return; }
        if (text[at++] !== ',') return fail();
        whitespace();
      }
      return fail();
    }
    if (char === '"') { string(false); return; }
    for (const token of ['true', 'false', 'null']) if (text.startsWith(token, at)) { at += token.length; return; }
    if (family === 'findings') for (const token of ['-Infinity', 'Infinity', 'NaN']) if (text.startsWith(token, at)) {
      extensions.push({ start: at, end: at + token.length, token }); at += token.length; return;
    }
    numberToken.lastIndex = at; const number = numberToken.exec(text);
    if (!number) return fail();
    at = numberToken.lastIndex;
  };
  try {
    value(0, null, null); whitespace(); if (at !== text.length) return fail();
    let marker = 0; while (markerIds.has(String(marker))) marker++;
    const replacements = new Map<string, number>();
    let input = text;
    if (extensions.length) {
      const pieces: string[] = []; let offset = 0;
      for (const extension of extensions) {
        const replacement = `"\\u0000JAI:${marker}:${extension.token}"`;
        replacements.set(replacement, extension.token === 'NaN' ? NaN : extension.token === 'Infinity' ? Infinity : -Infinity);
        pieces.push(text.slice(offset, extension.start), replacement); offset = extension.end;
      }
      pieces.push(text.slice(offset)); input = pieces.join('');
    }
    const nativeParse = JSON.parse as (source: string, revive: (this: object, key: string, value: unknown, context: { source?: string }) => unknown) => unknown;
    const result = nativeParse(input, (_key, parsed, context) => {
      if (context.source !== undefined && replacements.has(context.source)) return replacements.get(context.source)!;
      if (typeof parsed !== 'number') return parsed;
      if (context.source === undefined) return fail();
      return /^-?(?:0|[1-9][0-9]*)$/.test(context.source) ? BigInt(context.source) : parsed;
    }) as RecordedValue;
    const resolved: object[] = [];
    for (const container of containers) {
      const current = container.parent === null ? result : Object.getOwnPropertyDescriptor(resolved[container.parent]!, container.key!)?.value;
      if (!current || typeof current !== 'object') return fail();
      resolved.push(current);
      if (container.keys !== null) orders.set(current, container.keys);
    }
    return result;
  } catch (error) { if (error instanceof ImportError) throw error; return fail(); }
}
