import { ContractError } from './errors.js';
import { LIMITS } from './model.js';
import type { SemanticValue } from './model.js';

const decimal = /^(?:0|-?[1-9][0-9]*)$/;

/** Source numeric domain; findings preserve IEEE-754 floats, lifecycle semantic JSON forbids them. */
export type SemanticDomain = 'lifecycle' | 'findings';

function floatBits(value: number): string {
  const buffer = new ArrayBuffer(8); new DataView(buffer).setFloat64(0, value, false);
  return Array.from(new Uint8Array(buffer), byte => byte.toString(16).padStart(2, '0')).join('');
}

function plainRecord(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value) || (Object.getPrototypeOf(value) !== Object.prototype && Object.getPrototypeOf(value) !== null)) throw new ContractError('invalid-model', 'Invalid tagged semantic object');
  if (Object.getOwnPropertySymbols(value).length || Object.values(Object.getOwnPropertyDescriptors(value)).some(descriptor => !('value' in descriptor) || !descriptor.enumerable)) throw new ContractError('invalid-model', 'Semantic accessors/hidden properties are unsupported');
  return value as Record<string, unknown>;
}

function plainItems(value: unknown): unknown[] {
  if (!Array.isArray(value) || Object.getPrototypeOf(value) !== Array.prototype || Reflect.ownKeys(value).length !== value.length + 1) throw new ContractError('invalid-model', 'Invalid semantic array');
  const result: unknown[] = [];
  for (let index = 0; index < value.length; index++) {
    const descriptor = Object.getOwnPropertyDescriptor(value, String(index));
    if (!descriptor || !('value' in descriptor) || !descriptor.enumerable) throw new ContractError('invalid-model', 'Semantic array accessors/holes are unsupported');
    result.push(descriptor.value);
  }
  return result;
}

/**
 * Encode a plain source value using unambiguous tags and exact integer strings.
 * @param input Plain data with exact bigint integers; no accessors/cycles. Findings numbers denote float64.
 * @param domain Source numeric rules; lifecycle is the default and never accepts float64.
 * @returns A detached tagged semantic value, preserving exact strings and object entry order.
 * @throws {ContractError} For unsupported objects, floats, unsafe numbers, cycles or depth exhaustion.
 */
export function encodeSemantic(input: unknown, domain: SemanticDomain = 'lifecycle'): SemanticValue {
  const active = new Set<object>();
  const visit = (value: unknown, depth: number): SemanticValue => {
    if (value === null) return { type: 'null' };
    if (typeof value === 'boolean') return { type: 'boolean', value };
    if (typeof value === 'string') return { type: 'string', value };
    if (typeof value === 'bigint') return { type: 'integer', value: value.toString() };
    if (typeof value === 'number') {
      if (domain === 'findings') return { type: 'float64', bits: floatBits(value) };
      if (!Number.isSafeInteger(value)) throw new ContractError('invalid-model', 'Semantic numbers must be exact safe integers or bigint');
      return { type: 'integer', value: String(value) };
    }
    if (typeof value !== 'object' || value === undefined) throw new ContractError('invalid-model', 'Unsupported semantic value');
    if (depth >= LIMITS.semanticDepth) throw new ContractError('resource-limit', 'Semantic nesting limit exceeded');
    if (active.has(value)) throw new ContractError('invalid-model', 'Cyclic semantic values are unsupported');
    if (!Array.isArray(value) && Object.getPrototypeOf(value) !== Object.prototype && Object.getPrototypeOf(value) !== null) throw new ContractError('invalid-model', 'Semantic objects must be plain data');
    active.add(value);
    try {
      if (Array.isArray(value)) {
        if (Object.getPrototypeOf(value) !== Array.prototype || Reflect.ownKeys(value).length !== value.length + 1) throw new ContractError('invalid-model', 'Sparse or extended semantic arrays are unsupported');
        const items: SemanticValue[] = [];
        for (let index = 0; index < value.length; index++) {
          const descriptor = Object.getOwnPropertyDescriptor(value, String(index));
          if (!descriptor || !('value' in descriptor) || !descriptor.enumerable) throw new ContractError('invalid-model', 'Semantic arrays cannot contain accessors or missing entries');
          items.push(visit(descriptor.value, depth + 1));
        }
        return { type: 'array', items };
      }
      const entries = Object.entries(Object.getOwnPropertyDescriptors(value)).map(([key, descriptor]) => {
        if (!('value' in descriptor) || !descriptor.enumerable) throw new ContractError('invalid-model', 'Semantic objects cannot contain accessors or hidden properties');
        return { key, value: visit(descriptor.value, depth + 1) };
      });
      if (Object.getOwnPropertySymbols(value).length) throw new ContractError('invalid-model', 'Semantic symbol keys are unsupported');
      return { type: 'object', entries };
    } finally { active.delete(value); }
  };
  return visit(input, 0);
}

/**
 * Validate logical semantic depth and tag invariants without source normalization.
 * @param input Potential tagged semantic value; wrappers do not count as source levels.
 * @param domain Source numeric rules; float64 tags are admitted only for findings.
 * @returns Nothing when the value satisfies the lossless semantic contract.
 * @throws {ContractError} For malformed/extra fields, duplicate keys, invalid integers or excess depth.
 */
export function assertSemantic(input: unknown, domain: SemanticDomain = 'lifecycle'): asserts input is SemanticValue {
  const active = new Set<object>();
  const fail = (): never => { throw new ContractError('invalid-model', 'Invalid tagged semantic value'); };
  const visit = (value: unknown, depth: number): void => {
    const record = plainRecord(value);
    if (active.has(record)) fail();
    active.add(record);
    try {
      const keys = Object.keys(record).sort().join(',');
      switch (record.type) {
        case 'null': if (keys !== 'type') fail(); break;
        case 'boolean': if (keys !== 'type,value' || typeof record.value !== 'boolean') fail(); break;
        case 'string': if (keys !== 'type,value' || typeof record.value !== 'string') fail(); break;
        case 'integer': if (keys !== 'type,value' || typeof record.value !== 'string' || !decimal.test(record.value)) fail(); break;
        case 'float64': if (domain !== 'findings' || keys !== 'bits,type' || typeof record.bits !== 'string' || !/^[0-9a-f]{16}$/.test(record.bits)) fail(); break;
        case 'array':
          if (keys !== 'items,type' || !Array.isArray(record.items)) fail();
          if (depth >= LIMITS.semanticDepth) throw new ContractError('resource-limit', 'Semantic nesting limit exceeded');
          for (const item of plainItems(record.items)) visit(item, depth + 1);
          break;
        case 'object': {
          if (keys !== 'entries,type' || !Array.isArray(record.entries)) fail();
          if (depth >= LIMITS.semanticDepth) throw new ContractError('resource-limit', 'Semantic nesting limit exceeded');
          const names = new Set<string>();
          for (const entry of plainItems(record.entries)) {
            const pair = plainRecord(entry);
            if (Object.keys(pair).sort().join(',') !== 'key,value' || typeof pair.key !== 'string' || names.has(pair.key)) fail();
            names.add(pair.key as string); visit(pair.value, depth + 1);
          }
          break;
        }
        default: fail();
      }
    } finally { active.delete(record); }
  };
  visit(input, 0);
}

/**
 * Decode tagged data without losing integer precision or invoking object prototypes.
 * @param input Tagged semantic value; validated before decoding.
 * @param domain Source numeric rules; findings float64 tags decode to number without integer coercion.
 * @returns Detached data with bigint integers and null-prototype objects.
 * @throws {ContractError} When tags, integer representation, duplicate keys or depth are invalid.
 */
export function decodeSemantic(input: SemanticValue, domain: SemanticDomain = 'lifecycle'): unknown {
  assertSemantic(input, domain);
  const visit = (value: SemanticValue): unknown => {
    switch (value.type) {
      case 'null': return null;
      case 'boolean': case 'string': return value.value;
      case 'integer': return BigInt(value.value);
      case 'float64': {
        const bytes = Uint8Array.from(value.bits.match(/../g)!, byte => Number.parseInt(byte, 16));
        return new DataView(bytes.buffer).getFloat64(0, false);
      }
      case 'array': return value.items.map(visit);
      case 'object': {
        const result = Object.create(null) as Record<string, unknown>;
        for (const entry of value.entries) result[entry.key] = visit(entry.value);
        return result;
      }
    }
  };
  return visit(input);
}
