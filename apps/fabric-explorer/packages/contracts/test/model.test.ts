import { expect, it } from 'vitest';
import { LIMITS, RELATION_DIRECTIONS } from '../src/model.js';

it('exposes the frozen resource baseline and immutable direction policy', () => {
  expect(LIMITS.frameBytes).toBe(8 * 1024 * 1024);
  expect(LIMITS.visibleVertices).toBe(5000);
  expect(LIMITS.visibleEdges).toBe(20000);
  expect(LIMITS.hops).toBe(32);
  expect(Object.isFrozen(LIMITS)).toBe(true);
  expect(Object.isFrozen(RELATION_DIRECTIONS)).toBe(true);
  expect(Object.isFrozen(RELATION_DIRECTIONS['material-attachment'])).toBe(true);
});
