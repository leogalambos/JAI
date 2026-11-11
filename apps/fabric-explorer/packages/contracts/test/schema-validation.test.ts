import { expect, it } from 'vitest';
import { assertShape } from '../src/schema-validation.js';

it('runs the generated closed schema without coercion or extra-field removal', () => {
  const identity = { kind: 'finding', projectId: 'p', ledgerId: 'ledger', findingId: 'F-0001' };
  expect(() => assertShape('elementIdentity', identity)).not.toThrow();
  expect(() => assertShape('elementIdentity', { ...identity, authorityGranted: true })).toThrow();
  expect(() => assertShape('elementIdentity', { ...identity, findingId: 1 })).toThrow();
  expect(identity).toEqual({ kind: 'finding', projectId: 'p', ledgerId: 'ledger', findingId: 'F-0001' });
});
