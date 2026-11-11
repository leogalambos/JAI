# Fabric Explorer architecture decisions

Maintained by the JAI architecture and runtime maintainers. These decisions
explain the implemented design, alternatives and review triggers.
[Support and compatibility](support.md) describes the validated product scope.

The [architecture](architecture.md), [source contracts](source-contract.md),
[qualification](qualification.md), [dependency baseline](https://github.com/leogalambos/JAI/blob/main/apps/fabric-explorer/config/dependency-baseline.json)
and [platform baseline](https://github.com/leogalambos/JAI/blob/main/apps/fabric-explorer/config/platform-baseline.json) supply the associated
interfaces, limits and exact component versions. Each decision is superseded by
a new dated record when its assumptions or consequences change.

## ADR-01 — TypeScript desktop application with Electron

**Context.** The viewer needs consistent graphical behaviour on Linux, Windows
and macOS, direct local file selection and rich vertex/edge navigation.

**Decision.** Use Electron with React and strict TypeScript. Freeze exact tool
versions in the dependency baseline. Deploy a native application package with
bundled JavaScript and necessary runtime resources; do not ship the development
tree or require end-user Node.js/Python installations. This interpretation allows
inspectable executable JavaScript and bytecode, not hidden native-only code.

**Alternatives.** Browser-only delivery has less uniform filesystem/watch
capability. Tauri reduces runtime size but adds Rust and system-WebView variance.
C++/Qt provides native UI with a different implementation/maintenance cost.

**Consequences.** Chromium behaviour is consistent and the frontend ecosystem
is reusable. Downloads and resident memory are larger; Electron security support
requires regular dependency refresh. Electron is not an OS-wide read-only
sandbox, and cross-compilation does not qualify an untested platform.

**Review trigger.** The solution architect revisits this decision for
a native-machine-code-only requirement or an unmet platform/security budget.

## ADR-02 — One renderer behind a narrow abstraction

**Context.** Efficient exploration needs labels, arrows, loops and separately
selectable parallel relations as well as throughput on dense graphs.

**Decision.** Select Sigma.js 4.0.5 with Graphology 0.26.0 for integration after
the synthetic comparison and native Linux interaction checks. Keep the semantic
model independent of the renderer and ship only the selected renderer.
See [Support and compatibility](support.md) for the validated functionality
and the remaining packaged-performance and platform qualification boundaries.

Retain the original Graphology object when replacing the visible contents.
The pinned Sigma version's `setGraph` leaves its parallel-edge grouping index
bound to the original graph. Use public graph mutation and renderer refresh APIs,
with explicit camera/selection reset; do not patch dependency internals. Read GPU
metadata from the existing stage context rather than creating another context.

**Alternatives.** Selecting Sigma solely for WebGL throughput risks label/picking
gaps. Selecting Cytoscape solely for styling risks the performance envelope.
Shipping both increases packaging, security and maintenance costs without
resolving which interaction contract is authoritative.

**Consequences.** The comparison can reject a fast renderer with inadequate
relation inspection. The abstraction adds integration work; integration selection
does not by itself qualify dependencies for production. Extensions
must be maintained and license-compatible; essential features cannot depend on
an unowned plugin.

**Review trigger.** The frontend/performance maintainer owns node/edge label
collision and priority behaviour in the UI and revisits the decision after
measured incompatibility or a dependency/API change.

## ADR-03 — Immutable semantic snapshot and bounded projection

**Context.** Complete source history can exceed the readable/renderable graph;
interactive exploration must preserve identities and exact relationships.

**Decision.** Retain one immutable accepted semantic generation and derive a
bounded visible projection. Use compact handles, independent edge identity,
forward/reverse adjacency, indexed search and cancellable seeded worker layouts.
Keep raw details paged and reject stale generation results.

**Alternatives.** A fully rendered authoritative graph couples source fidelity
to graphics limits. Rebuilding every view from all journals repeats accepted
work. Renderer-owned mutable state makes refresh and later notes ambiguous.

**Consequences.** Queries and future directional overlays reuse indexes; source
records remain stable. Additional indexes and worker transfer can duplicate
memory, so full process-tree measurements include renderer, workers and buffers.
Hidden elements and partial results must be counted explicitly.

**Review trigger.** The data/graph architect revisits this decision when identity, memory or
incremental-equivalence qualification fails.

## ADR-04 — Worker-native recorded-data import

**Context.** Fabric and Findings have structured identities and lossless values. A viewer must decode these records without repeating canonical authority, signature or lifecycle verification.

**Decision.** Use the fixed TypeScript import worker to stream selected JSONL directly into the compact recorded-data graph. Main admits read-only file objects and transfers native handles; the worker tees the same bytes to the source archive. No Python reader, fact spool, semantic JSON RPC, installed JAI core or OpenSSL verifier is a viewing dependency. Source records remain data, never import locations.

**Alternatives.** An ambient Python or canonical JAI runtime dependency breaks standalone installation. Loading project modules or arbitrary CLI commands expands execution rights. Repeating canonical verification adds unrelated work and misleading assurance to a visual preview.

**Consequences.** Recorded identities, states and dependency classifications remain visible with explicit unknown chain/trust metadata. Viewing does not authenticate recorded claims. Native packaging and platform qualification remain release obligations. Helper failure preserves the displayed generation; no signing keys or enrollment are required to view data.

**Review trigger.** The runtime maintainer revisits this decision for
unavailable secure adapters or failed standalone/semantic parity. See
[Support and compatibility](support.md) for native validation scope.

## ADR-05 — No writes to selected source roots

**Context.** The initial product is an offline viewer of confidential local data.
Read-only input must include indirect writes such as logs, locks and GPU caches.

**Decision.** Use a fixed-capability read broker, isolated preload and sandboxed
renderer. Confine preferences/cache/scratch to application-owned destinations,
reject overlap with selected roots, and deny network/update/source-mutation
operations. The application-requested external launch capability is restricted
to Electron's fixed packaged runtime. The application does not launch a reader executable. Electron's intrinsic renderer,
GPU, utility and platform helper/crash-handler children are separately allowed
only as fixed packaged runtime images in the artifact inventory. Neither class
permits project plugins or additional runtime binary discovery; selected source
configuration cannot affect execution.

**Alternatives.** A renderer filesystem API is simpler but expands authority.
Project-local caches/locks contaminate the source tree. An OS-specific sandbox
alone does not express the complete cross-platform product contract.

**Consequences.** Privacy and source integrity have a clear testable boundary.
Broad overlapping root selection is refused; users may need narrower roots.
Updates are manual, app-owned state needs its own retention controls, and
read-only claims require denied-write and process-boundary evidence per target.

**Review trigger.** The desktop/security architect revisits this decision for a new write,
network, subprocess or source-root capability.

## ADR-06 — Future notes and flow styling remain separate overlays

**Context.** A later version may annotate vertices/edges and colour directed
information flows without modifying authoritative JAI data.

**Decision.** Preserve stable, version-aware element references, parallel-edge
addresses and typed relation direction. Keep presentation styling pure and
separate from semantic records. Future notes belong to a separately governed
store; traversal overlays select relation classes and terminate safely on cycles.

**Alternatives.** Storing notes in source ledgers violates the viewer boundary.
Label-keyed notes can attach to the wrong version or edge. Renderer-specific
annotations make renderer replacement a data migration.

**Consequences.** The model can accommodate later overlays without a source
format change. Occurrence-derived edge IDs can become orphaned after rewrites
and need an explicit future reconciliation policy. No note persistence/editor,
saved flow colouring or dormant mutation command is implemented in this version.

**Review trigger.** The data architect revisits these extension constraints
when annotation identity or persistence is specified. Annotations are not a
shipped editing capability.
