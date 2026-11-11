/** Factory control-flow proof only: collaborator counters are not GPU performance evidence. */
import { expect, it, vi } from 'vitest';
const counts = vi.hoisted(() => ({ label: 0, backdrop: 0, background: 0, frame: 0, node: 0 }));
vi.hoisted(() => Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }));
vi.mock('../vendor/sigma/.cache/upstream/src/rendering/nodes/labels/index.ts', () => ({
  createLabelProgram: () => { counts.label++; return {}; },
  createLabelBackgroundProgram: () => { counts.background++; return {}; },
  NodeLabelFramePass: class { constructor() { counts.frame++; } },
}));
vi.mock('../vendor/sigma/.cache/upstream/src/rendering/nodes/backdrops/index.ts', () => ({ createBackdropProgram: () => { counts.backdrop++; return {}; } }));
vi.mock('../vendor/sigma/.cache/upstream/src/rendering/program.ts', () => ({ Program: class { constructor() { counts.node++; } } }));
vi.mock('../vendor/sigma/.cache/upstream/src/rendering/data-texture.ts', async importOriginal => ({ ...await importOriginal<object>(), ItemAttributeTexture: class {} }));
const source = '../vendor/sigma/.cache/upstream/src/rendering/nodes/factory.ts';
const primitiveSource = '../vendor/sigma/.cache/upstream/src/primitives/types.ts';
const { createNodeProgram } = await import(source);
const { DEFAULT_NODE_PRIMITIVES } = await import(primitiveSource);
it('omits exactly three companion factories while retaining node geometry and frame pass', () => {
  const options = { ...DEFAULT_NODE_PRIMITIVES };
  delete options.labelPrograms;
  const original = createNodeProgram({}, null, {}, options, true);
  expect(counts).toEqual({ label: 1, backdrop: 1, background: 1, frame: 1, node: 1 });
  expect(original.labelProgram).not.toBeNull(); expect(original.backdropProgram).not.toBeNull();
  const reduced = createNodeProgram({}, null, {}, { ...options, labelPrograms: false }, true);
  expect(counts).toEqual({ label: 1, backdrop: 1, background: 1, frame: 2, node: 2 });
  expect(reduced.labelProgram).toBeNull(); expect(reduced.backdropProgram).toBeNull(); expect(reduced.labelBackgroundProgram).toBeNull();
  expect(reduced.framePass).toBeDefined(); expect(reduced.nodeProgram).toBeDefined();
  createNodeProgram({}, null, {}, { ...options, labelPrograms: true }, true);
  expect(counts).toEqual({ label: 2, backdrop: 2, background: 2, frame: 3, node: 3 });
});

it('rejects attachments before any factory allocation in disabled mode', () => {
  const before = { ...counts };
  expect(() => createNodeProgram({}, null, {}, { ...DEFAULT_NODE_PRIMITIVES, labelPrograms: false, labelAttachments: { badge: () => null } }, true)).toThrow('labelPrograms');
  expect(counts).toEqual(before);
});
