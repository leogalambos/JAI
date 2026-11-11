# Sigma integration recipe

This directory contains Fabric Explorer's build recipe, reviewed text patch,
pinned provenance and MIT license attribution. It contains no maintained upstream
SDK source or generated package archive. The upstream source is Sigma 4.0.5 at
commit `617afb0508fc0fd8b60b208a04a83c49edf05a9f`.

The approved patch adds the default-on immutable `primitives.nodes.labelPrograms`
capability. Disabling it requires disabled labels/events and no label attachments;
geometry, frame passes, arrows and ordinary picking remain unchanged. See the
reviewable patch and provenance for the exact maintained variant.

## Build preparation

Install the pinned desktop dependencies with `npm ci --ignore-scripts`. The local
`file:vendor/sigma` dependency links this recipe; it needs no generated source or
output during installation and runs no lifecycle hook.

Run `npm run prepare:sdk` once with network access. This downloads only the pinned
upstream commit archive, checks its SHA256 before extraction, applies the fixed
patch and verifies the resulting source hashes. Developer preparation requires
Node, git and tar. Sources are cached under ignored `.cache/upstream/`; generated JS and
declarations are written to ignored `.cache/dist/`. A matching prepared cache is reused
without reconstructing or rehashing the entire source tree on every command.

Normal builds compile the SDK before typechecking. `npm run build:sdk` builds it
alone. Native operator builds use the prepared cache without network downloads;
CI explicitly prepares it before offline checks. `node tools/build-sigma.mjs
--offline` fails clearly if the cache is missing. A mismatched cache fails rather
than falling back to an unpatched installed package; remove only the generated
`.cache/upstream/` directory before deliberate preparation of a changed recipe.

All six public entrypoints retain ESM, CommonJS and declaration outputs. Source
updates require patch review, affected CPU/public API tests and separate native
GPU qualification. CPU tests do not establish the complete upstream browser suite.

The installed viewer performs no SDK download and ships compiled application
assets with the Sigma MIT notice under `licenses/sigma-MIT.txt`; SDK sources are
not installed with it. The retained LICENSE.txt supplies the required upstream
copyright and permission notice.

Build-tool API/negative tests run with `npm run test:build`; the separate
`npm run test:build:integration` command tests the real first-use download and
requires network. Ordinary prepared-cache tests remain offline.
