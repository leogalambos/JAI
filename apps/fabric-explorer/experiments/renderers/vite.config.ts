/** Disposable offline IIFE build; inline corpus worker avoids HTTP and file-fetch dependencies. */
import { defineConfig } from 'vite';
export default defineConfig({
  build: {
    lib: { entry: 'src/main.ts', name: 'RendererProbeExperiment', formats: ['iife'], fileName: () => 'probe.js', cssFileName: 'probe' },
    sourcemap: false,
    reportCompressedSize: true,
  },
});
