/** Explicit upstream CPU-only scope; instance-registry and remaining browser/GPU suites need native qualification. */
import { defineConfig } from 'vitest/config';
export default defineConfig({ test: { environment: 'node', setupFiles: ['test/sigma-sdk-constants.ts'], include: [
  'vendor/sigma/.cache/upstream/src/core/label-events.test.ts', 'vendor/sigma/.cache/upstream/src/core/label-renderer.test.ts',
  'vendor/sigma/.cache/upstream/src/core/edge-groups.test.ts', 'vendor/sigma/.cache/upstream/src/core/fit-extent.test.ts',
  'vendor/sigma/.cache/upstream/src/core/styles-dependency.test.ts', 'vendor/sigma/.cache/upstream/src/core/styles-resolver.test.ts',
  'vendor/sigma/.cache/upstream/src/utils/colors.test.ts', 'vendor/sigma/.cache/upstream/src/utils/data.test.ts',
  'vendor/sigma/.cache/upstream/src/utils/easings.test.ts', 'vendor/sigma/.cache/upstream/src/utils/fragments.test.ts',
  'vendor/sigma/.cache/upstream/src/utils/parseFontString.test.ts',
] } });
