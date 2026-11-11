/** Actual SDK lifecycle methods over owned factory collaborators; no real GPU is simulated. */
import { expect, it, vi } from 'vitest';
const observed = vi.hoisted(() => ({ nodeOptions: [] as unknown[], killed: 0 }));
vi.hoisted(() => Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }));
vi.mock('../vendor/sigma/.cache/upstream/src/primitives/parser.ts', async original => ({
  ...await original<object>(),
  generateNodeProgram: (_gl: unknown, _pick: unknown, _owner: unknown, options: unknown) => {
    observed.nodeOptions.push(options);
    return { nodeProgram: { kill: () => { observed.killed++; } }, framePass: { kill: () => { observed.killed++; } }, labelProgram: null, backdropProgram: null, labelBackgroundProgram: null, attachmentProgram: null, variables: {} };
  },
  generateEdgeProgram: () => ({ edgeProgram: { kill: () => {} }, framePass: { kill: () => {} }, variables: {}, paths: [], createLabelPrograms: () => { throw new Error('unused edge labels'); } }),
}));
const source = '../vendor/sigma/.cache/upstream/src/sigma.ts';
const { default: Sigma } = await import(source);
it('preserves immutable opt-out across context restoration even if caller mutates primitive input', () => {
  const primitives = { nodes: { labelPrograms: true } };
  const receiver = {
    nodeLabelProgramsEnabled: false, webGLContext: {}, pickingFrameBuffer: {},
    internals: { primitives, settings: { renderLabels: false, nodeLabelEvents: false }, hoverResolver: { reset: vi.fn() } },
    customLayerPrograms: new Map(), initPickingFramebuffer: vi.fn(),
    initPrograms: Sigma.prototype.initPrograms, emit: vi.fn(), refresh: vi.fn(), contextLost: true,
  };
  Sigma.prototype.restoreWebGLContext.call(receiver);
  expect(observed.nodeOptions).toEqual([{ labelPrograms: false }]);
  expect(receiver.internals).toMatchObject({ labelProgram: null, backdropProgram: null, labelBackgroundProgram: null });
  expect(receiver.contextLost).toBe(false); expect(receiver.emit).toHaveBeenCalledWith('webglContextRestored');
  expect(receiver.refresh).toHaveBeenCalledOnce();
});
it('rejects newly attached label dependencies before restoring program resources', () => {
  const before = observed.nodeOptions.length;
  expect(() => Sigma.prototype.initPrograms.call({ nodeLabelProgramsEnabled: false }, { nodes: { labelAttachments: { badge: () => null } } }, { renderLabels: false, nodeLabelEvents: false })).toThrow('labelPrograms');
  expect(observed.nodeOptions).toHaveLength(before);
});
it.each([false, true])('disposes geometry/frame passes and nullable companions exactly once (companions=%s)', companions => {
  const kill = vi.fn(); const program = () => ({ kill: vi.fn() });
  const node = program(), edge = program(), nodeFrame = program(), edgeFrame = program();
  const label = companions ? program() : null, backdrop = companions ? program() : null, background = companions ? program() : null;
  vi.stubGlobal('window', { removeEventListener: vi.fn() });
  const receiver = {
    emit: vi.fn(), removeAllListeners: vi.fn(), camera: { cancelAnimation: vi.fn() }, unbindCameraHandlers: vi.fn(),
    activeListeners: {}, mouseCaptor: { kill }, touchCaptor: { kill }, unbindGraphHandlers: vi.fn(), clearIndices: vi.fn(), clearState: vi.fn(),
    container: { firstChild: null }, nodeProgram: node, edgeProgram: edge, nodeFramePass: nodeFrame, edgeFramePass: edgeFrame,
    internals: { hoverResolver: { kill }, labelProgram: label, backdropProgram: backdrop, labelBackgroundProgram: background },
    customLayerPrograms: new Map(), sdfAtlas: null, webGLContext: { getExtension: () => null },
    mouseLayer: { remove: vi.fn() }, extraElements: {},
  };
  try {
    expect(() => Sigma.prototype.kill.call(receiver)).not.toThrow();
    for (const item of [node, edge, nodeFrame, edgeFrame, label, backdrop, background].filter(Boolean)) expect(item!.kill).toHaveBeenCalledOnce();
    expect(receiver.webGLContext).toBeNull();
  } finally { vi.unstubAllGlobals(); }
});
