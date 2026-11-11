import * as validators from '../generated/validators.js';
import { ContractError } from './errors.js';
import { LIMITS } from './model.js';

function guardModelTree(value: unknown): void {
  const active = new Set<object>();
  const pending: { value: unknown; depth: number; exit?: boolean }[] = [{ value, depth: 0 }];
  while (pending.length) {
    const item = pending.pop()!; const data = item.value;
    if (item.exit) { active.delete(data as object); continue; }
    if (data === null || typeof data === 'boolean') continue;
    if (typeof data === 'string') {
      for (let i = 0; i < data.length; i++) {
        const unit = data.charCodeAt(i);
        if (unit >= 0xd800 && unit <= 0xdbff) { const next = data.charCodeAt(++i); if (!(next >= 0xdc00 && next <= 0xdfff)) throw new ContractError('invalid-model', 'Invalid Unicode in model data'); }
        else if (unit >= 0xdc00 && unit <= 0xdfff) throw new ContractError('invalid-model', 'Invalid Unicode in model data');
      }
      continue;
    }
    if (typeof data === 'number') { if (!Number.isSafeInteger(data)) throw new ContractError('invalid-model', 'Model administrative numbers must be safe integers'); continue; }
    if (typeof data !== 'object') throw new ContractError('invalid-model', 'Unsupported model data value');
    if (item.depth >= LIMITS.wireDepth) throw new ContractError('resource-limit', 'Model wrapper nesting limit exceeded');
    if (active.has(data)) throw new ContractError('invalid-model', 'Cyclic model data is unsupported');
    const array = Array.isArray(data); const prototype = Object.getPrototypeOf(data);
    if (array ? prototype !== Array.prototype : prototype !== Object.prototype && prototype !== null) throw new ContractError('invalid-model', 'Model data must use plain objects/arrays');
    const descriptors = Object.getOwnPropertyDescriptors(data);
    if (Object.getOwnPropertySymbols(data).length) throw new ContractError('invalid-model', 'Model symbol properties are unsupported');
    if (array && Object.keys(descriptors).length !== data.length + 1) throw new ContractError('invalid-model', 'Sparse or extended model arrays are unsupported');
    active.add(data); pending.push({ value: data, depth: item.depth, exit: true });
    for (const [key, descriptor] of Object.entries(descriptors)) {
      if (array && key === 'length') continue;
      if (!('value' in descriptor) || !descriptor.enumerable || (array && !/^(?:0|[1-9][0-9]*)$/.test(key))) throw new ContractError('invalid-model', 'Model accessors/hidden properties are unsupported');
      pending.push({ value: descriptor.value, depth: item.depth + 1 });
    }
  }
}

/** Named definitions emitted from the one published schema; arbitrary remote references are unsupported. */
export type SchemaDefinition = keyof typeof validators;

/**
 * Enforce a precompiled structural schema without runtime compilation or source mutation.
 * @param definition One fixed package definition, never an untrusted schema or URL.
 * @param value Candidate data; callers own it and validation does not coerce/default/drop fields.
 * @returns Nothing on structural success; semantic/source truth is not established. In-memory models are not capped to one IPC frame.
 * @throws {ContractError} For a missing definition or invalid closed structure.
 */
export function assertShape(definition: SchemaDefinition, value: unknown): void {
  // Recursive generated schemas require acyclic bounded data even for direct
  // structured-clone callers; this guard deliberately has no wire-byte budget.
  guardModelTree(value);
  const validate = validators[definition];
  if (typeof validate !== 'function' || !validate(value)) throw new ContractError('invalid-model', `Invalid ${definition} structure`);
}
