/** DOM preparation must not force layout or construct a renderer before a later owned phase. */
import { expect, it, vi } from 'vitest';
vi.hoisted(() => Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }));
import { prepareCanvas } from '../src/renderer/canvas/index.js';
import type { CanvasRenderer } from '../src/renderer/canvas/sdk.js';
it('prepares and observes without a geometry read; initializes only on explicit later request', () => {
  let readsAllowed = false; let reads = 0; let removals = 0;
  const observers: { callback: ResizeObserverCallback; target?: Element; disconnect: () => void }[] = [];
  const owner = { defaultView: { devicePixelRatio: 1 }, createElement: () => new Element() };
  class Element {
    ownerDocument = owner; style = {}; children: Element[] = [];
    append(...children: Element[]) { this.children.push(...children); } setAttribute() {} remove() { removals++; } getContext() { return null; }
    get clientWidth() { reads++; if (!readsAllowed) throw new Error('forced layout in preparation'); return 320; }
    get clientHeight() { reads++; if (!readsAllowed) throw new Error('forced layout in preparation'); return 200; }
  }
  vi.stubGlobal('ResizeObserver', class {
    private entry: typeof observers[number];
    constructor(callback: ResizeObserverCallback) { this.entry = { callback, disconnect: vi.fn() }; observers.push(this.entry); }
    observe(target: Element) { this.entry.target = target; } disconnect() { this.entry.disconnect(); }
  });
  const renderer = { on: vi.fn(), off: vi.fn(), kill: vi.fn() } as unknown as CanvasRenderer;
  const factory = vi.fn(() => renderer); const changed = vi.fn();
  try {
    const pending = prepareCanvas(new Element() as unknown as HTMLElement, () => {}, undefined, factory);
    expect(reads).toBe(0); expect(factory).not.toHaveBeenCalled(); pending.observe(changed);
    const observation = observers[0]!;
    observation.callback([{ target: observation.target, contentRect: { width: 320, height: 200 } }] as unknown as ResizeObserverEntry[], {} as ResizeObserver);
    expect(reads).toBe(0); expect(pending.measurable()).toBe(true); expect(changed).toHaveBeenCalledOnce(); expect(factory).not.toHaveBeenCalled();
    readsAllowed = true; const canvas = pending.initialize(); expect(factory).toHaveBeenCalledOnce(); expect(reads).toBeGreaterThan(0);
    expect(observation.disconnect).toHaveBeenCalledOnce(); expect(() => pending.initialize()).toThrow('preparation');
    canvas.dispose(); pending.dispose(); expect(renderer.kill).toHaveBeenCalledOnce(); expect(removals).toBe(1);
  } finally { vi.unstubAllGlobals(); }
});
