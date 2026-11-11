# Building portable packages

For building and installing only the current host target from a clone, use
`./install-viewer.sh --build --allow-development` at the repository root
(`install-viewer.cmd` on Windows). This explicit source-build mode requires the
pinned development tools and may download dependencies. The
[main viewer installation guide](installation.md)
lists prerequisites, dry-run, tool overrides and prebuilt-package installation.
The lower-level commands below are for maintainers assembling package artifacts.

This maintainer workflow assembles unsigned development candidates for Linux x64 and arm64, Windows x64, and macOS x64 and arm64. Users receive a compiled application and bundled Electron runtime; installation requires no Node.js, Python, npm, compiler, or dependency download. See [installation](installation.md) for the user workflow.

Build the desktop assets using the maintained desktop build recipe, then compile the separate installer helper:

```sh
node apps/fabric-explorer/packaging/build-installer.mjs
node apps/fabric-explorer/packaging/package.mjs all
node apps/fabric-explorer/packaging/bootstrap-sidecars.mjs build/fabric-explorer/packages --allow-development
```

The helper build type-checks the packaging TypeScript and writes only `desktop/dist/installer.cjs`. Packaging copies the existing six compiled application outputs without recompiling them. It downloads the five fixed Electron 45.2.3 archives from the official release, verifies the SHA-256 pins in `packaging/runtime-pins.json`, inspects archive paths and links, and caches their prepared runtime trees under the ignored build directory. Subsequent builds reuse those inputs. Use `--offline` as the third argument after the target and output directory to reject a cache miss without network access:

```sh
node apps/fabric-explorer/packaging/package.mjs linux-x64 build/fabric-explorer/packages --offline
```

The selected runtime executable's binary header must match its target architecture. macOS framework links remain relative and confined to the package. The unused Electron default application is removed. The application resides in Electron's native resources directory; macOS retains a self-contained `Electron.app`. Normal launch requires no development application path argument.

The separate sidecar command reads the completed detached manifests and emits their fixed-digest `.install.sh` or `.install.ps1` siblings. It requires explicit development permission and rejects release manifests. It does not rebuild or modify archives, manifests or inventories. Identical existing scripts are reused; differing scripts fail before any output is written. To regenerate after an installer-script update, preserve any needed previous scripts and remove only those generated sidecars before rerunning the command. Release script generation and trusted distributor keys belong to the separately authorized release process.

Each target produces a Linux/macOS tar.gz or Windows ZIP, an exact detached asset manifest, and a copy of its internal inventory. The allowlist admits only runtime files, the six compiled application outputs, minimal application metadata, the compiled installer, and declared notices. Source files, source maps, tests, fixtures, private inputs and development dependencies are excluded. An unexpected payload member fails packaging.

The detached manifest hashes the archive, internal inventory, SBOM and consolidated notices. The internal inventory hashes each regular file and records modes and confined symbolic links; it excludes only itself. This avoids a digest cycle. The source identity covers maintained public application inputs, including dirty changes. It does not grant release authority. The SBOM records bundled application libraries and the pinned Electron input; Chromium's upstream transitive notices are retained verbatim rather than represented as an independently enumerated dependency graph.

Archive member order, ownership and timestamps are normalized. The default reproducibility epoch is 1980-01-01 UTC; SBOM dates describe that explicit build epoch, not observed creation time. Reproducibility requires identical compiled assets, helper, runtime pins, dependency notices, source identity, version and archive tooling. Build a second candidate in a separate output directory to compare archive and manifest digests. Existing outputs are never overwritten.

These candidates have manifest status `development`, no signature key identifier and no release signature. They are not signed, notarized or release-qualified artifacts. Release signing and trusted key distribution require an independently authorized release process. Assembly and static inspection of another target do not establish native execution compatibility; Windows/macOS native qualification is separate.

Direct checks for the packager and inspector use Node's test runner:

```sh
node --test apps/fabric-explorer/packaging/test/package.test.mjs apps/fabric-explorer/packaging/test/package-inspect.test.mjs apps/fabric-explorer/packaging/test/package-sidecars.test.mjs
node --test apps/fabric-explorer/packaging/test/integration/package-runtime.test.mjs
```

The second command deliberately fetches the fixed official Linux runtime on a cache miss and checks subsequent offline reuse. It does not execute Electron. All runtime caches and generated packages belong in ignored build output, never in Git.
