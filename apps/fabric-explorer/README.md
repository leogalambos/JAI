# JAI Fabric Explorer

Local, offline, read-only exploration of JAI Fabric, findings and recorded relationships.

The complete user guide and technical reference are maintained in the
[main JAI documentation](../../docs/fabric-explorer/index.md), including
installation, source formats, architecture, model and query contracts,
rendering, packaging, security and support.

## Source layout

- `desktop/`: Electron shell, read-only broker, TypeScript import/query/layout worker and React interface.
- `packages/contracts/`: renderer-independent semantic and transport contracts.
- `packaging/`: target archive creation and per-user installation.
- `examples/`: reproducible public workflow reference data.
- `benchmarks/`: bounded data preparation and measurement tools.
- `config/`: pinned dependency and platform baselines.
- `test/fixtures/`: maintained source compatibility fixtures.

## Install from a clone

From the repository root, use `./install-viewer.sh --build --allow-development`
(`install-viewer.cmd` on Windows) to explicitly build and install the current
platform's unsigned development package. Source building requires the pinned
development toolchain. Installing an existing local package with
`--package-dir DIRECTORY` requires no Node.js, npm or Python and never falls
back to a build. The main JAI installer remains separate.

## Development

The desktop package declares the exact Node.js and npm versions. Install locked
dependencies with lifecycle scripts disabled, then use the maintained explicit
build commands. Third-party renderer sources are acquired during that build;
downloaded archives, runtime binaries, generated outputs and dependencies do
not belong in Git.

Select checks by the changed invariants and boundaries. Native graphical,
accessibility and performance checks have distinct scopes; test definitions or
cross-target archive assembly do not establish native platform qualification.
Installed application packages contain only compiled runtime assets and their
required resources and notices, without source trees, tests or private evidence.
