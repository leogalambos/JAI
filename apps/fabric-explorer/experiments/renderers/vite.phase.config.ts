/** Disposable early-observer asset, built separately so startup attribution precedes harness evaluation. */
import { defineConfig } from 'vite';
export default defineConfig({ build: { emptyOutDir: false, lib: { entry: 'src/phase-bootstrap.ts', name: 'RendererProbePhases', formats: ['iife'], fileName: () => 'phase-bootstrap.js' }, sourcemap: false } });
