# Fabric Explorer architecture

Maintained by the JAI architecture and runtime maintainers.
See [Support and compatibility](support.md) for the validated platform scope.

This document constrains the read-only desktop consumer of the maintained
[source contracts](source-contract.md). [Architecture decisions](decisions.md),
[qualification requirements](qualification.md), the
[dependency baseline](https://github.com/leogalambos/JAI/blob/main/apps/fabric-explorer/config/dependency-baseline.json) and
[platform baseline](https://github.com/leogalambos/JAI/blob/main/apps/fabric-explorer/config/platform-baseline.json) define its accompanying
contracts. A design target is not a measured result or release permission.

## Product boundary

The application opens explicitly selected local fabric and findings roots and
projects their records into a navigable graph. It provides search, filters,
bounded neighbourhood/path exploration, vertex/edge inspectors, findings
navigation and a keyboard-accessible tabular alternative. Graph layout and
connectivity do not establish professional correctness or authority.

Input roots are read-only. The application neither initialises missing ledgers
nor repairs, migrates, locks, annotates, signs or appends to them. Local view
preferences are separate application data. There are no workflow/authority
commands, editing controls, automatic updates, telemetry or external services.
Optional source families require an explicit adapter; no recursive generic JSON
importer or executable project configuration is permitted.

## Deployment and process responsibilities

```text
Native package
  Electron main / read-only file broker
       |                     |
       | narrow preload      | admitted source and archive FileHandles
  sandboxed renderer         +-- TypeScript import/query/layout worker
       |                              |
       +-- bounded graph and tables --+-- compact graph and indexes

Application-owned state: platform app-data and private captured-source archive
Source-owned state: explicitly selected ledgers and associated material files
```

| Component | Responsibility | Forbidden capability |
| --- | --- | --- |
| Main process | Native picker, file admission, app-owned preferences, archive adoption, IPC validation and cancellation | Renderer-supplied paths, source writes or dynamic project modules |
| Read broker | Bind selected file objects to opaque capabilities, retain read-only handles, enforce identity and byte limits | Generic renderer filesystem API or write/open-for-update source handles |
| Import/query/layout worker | Stream selected JSONL into recorded projections, compact graph/indexes and bounded query/layout results | Canonical verification, source writes or execution of source content |
| Preload | Expose the versioned allowlist of typed consumer operations | Node exports, native handles, unrestricted IPC or a generic RPC method |
| Semantic snapshot | Retain immutable identities, use points, relations, findings, revisions and source locators | Presentation coordinates or colour as authoritative source state |
| Renderer and inspector | Draw/pick a bounded graph and expose full labels, attributes, source pages and accessible tables | Disk/process access, external resources or executable attachments |

The application does not launch an external reader process. Electron may create
its intrinsic renderer, GPU, utility and platform helper processes; their images
must belong to the packaged runtime and appear in the artifact inventory.
Worker threads use the fixed bundled TypeScript implementation. No Python,
canonical JAI runtime, source-signature verifier or selected-project module is a
viewing dependency. Python may prepare synthetic development fixtures before a
qualification run; it is not part of the application's import path.

One worker streams each selected source exactly once and writes those same
bytes to its app-owned archive while producing graph facts directly into the
compact model. No fact spool or JSON message transfer between a Python reader
and the graph model exists. Main adopts the completed archive without rereading
or copying the source bytes a second time.

## Trust boundaries and read-only enforcement

The selected data and every label, path, Markdown fragment and attachment are
untrusted. Application binaries and fixed resources are trusted only through the
release verification boundary. The renderer has `nodeIntegration: false`,
`contextIsolation: true`, sandboxing enabled and no remote module. Packaged
pages use a restrictive Content Security Policy with no remote script, font,
image, frame or connection source; executable inline content is forbidden.
Development tooling is not a production capability.

Reject window creation, external navigation, permission requests, downloads,
arbitrary protocols and automatic external-link handling. No production remote
debugging endpoint or development server is exposed. Network-denial tests cover
the Electron process tree and resource requests; disabling a
JavaScript `fetch` call alone does not establish this boundary.

Before Electron creates a window, worker, log or cache, configure its app-owned
`userData`, session data, logs and temporary locations. Preferences, crash data,
GPU/shader caches and import scratch must not land in the selected project.
Do not start upload-enabled crash reporting. Source contents, raw labels and
selected paths are not routine persistent diagnostics. Local diagnostics expose
bounded error categories; deliberate debug collection requires a separate
operator action and is not enabled by opening a project.

Reject a source root if it equals or contains any application write destination,
or is contained within the app-owned runtime/cache/scratch tree. Resolve the
relevant filesystem identities, not only textual path prefixes. A broad root
such as the user's home may therefore require selecting narrower source roots.
Revalidate mutable root/handle conditions before the affected operation. The
application does not attempt to manufacture an OS-wide sandbox guarantee.

Selected sources open read-only. The broker authenticates the actual file
handle's identity before reading and checks regular-file, link, size and change
markers. Each candidate reads a fixed byte length and rejects observed changes;
accepted pages come from the retained immutable archive. Portable Node pathname
observations do not prove atomic protection against a hostile ancestor swap
during initial admission. This limitation must not be described as native
parent-relative confinement. Windows/macOS reading remains implemented with
portable handles; native qualification is recorded separately. Read-only
mounts/ACLs and process/file observation qualify zero source writes per target.

## Acquisition, snapshots and verification

The picker starts from a deliberately selected project and source families.
It may list immediate regular `.jsonl` files in that project’s `.fabric/` and
`.findings/` directories; unavailable or over-limit lookup uses a project-rooted
native file dialog. Audit stays explicit. The broker admits the resulting files
read-only; lookup itself does not grant a source capability. A root capability
cannot be expanded by a renderer-supplied absolute path. Source locators remain
inspectable metadata, not a grant to open arbitrary files. Material readability observations are bound to exact associated blob names;
they do not verify material digests. Public/private signing keys are not needed
or searched for by the viewer.

A snapshot generation identifies adapter versions and the observed revisions of
every included source. It preserves origin scope separately from `use_scope`,
all immutable version references and ledger-local finding identities. No global
atomic commit or total ordering is inferred across independent ledgers.

The importer projects recorded manifests, effects, references and findings.
It does not verify chains, signatures, permissions, transition legality or
professional correctness. Snapshot metadata explicitly identifies recorded
projection and unknown chain/trust state. Recorded applicability and decisions
remain source claims; no viewer operation grants authority or performs a fresh
assessment. Malformed JSON, unreadable structures, unknown format versions and
resource violations receive bounded diagnostics without repairing inputs.

Refresh builds the next generation away from the displayed one, validates its
source revisions and indexes, then publishes it atomically. Filesystem watch
events are hints. Preserve the last successful generation after partial writes,
source replacement, cancellation, worker failure or invalid refresh. Mark it
stale and explain the rejected acquisition. A partial tail is never an admitted
transaction. A cold open can fail without creating source files.

An unchanged whole selection retains its accepted worker, graph and generation.
An explicit import creates a candidate; a changed-source refresh streams the
candidate's sources again. This implementation does not claim cross-worker
parsed-prefix reuse or suffix-only disk I/O. It never repeats canonical history
verification, because that operation is absent from the viewer.

## Consumer protocol and resource ownership

Every allowed operation binds protocol version, request ID, session capability
and snapshot generation. The receiver validates message shape, bounds and
operation-specific arguments. Results identify their generation; stale worker
responses cannot update a later view. Pagination cursors also bind filter/query
identity. Unknown operations and versions return a typed rejection, not dynamic
dispatch.

The operation families are root admission/close, import/refresh/cancel, exact
lookup, paginated search, filtered counts, bounded neighbours/path query,
element details and source-record paging. The exact versioned shapes are defined
in the [consumer contracts](contracts.md). No operation accepts a shell command, module name,
arbitrary method, attachment execution request or source mutation.

Preserve arbitrary-precision semantic integers through an unambiguous tagged
transport; retain exact proof/material bytes separately. Display strings must
not be reparsed as identities. Lifecycle NFC canonicalisation and findings
canonicalisation remain distinct. Canonical sorting, domain-separated hashes
and source bytes are never recomputed from shortened UI text.

The qualification baseline bounds acquisition, decoded nesting, individual
records, transport frames, raw paging, diagnostics, visible elements and query
work. Large results are paged/chunked with generation and completion markers;
they cannot bypass budgets through one oversized IPC object. Backpressure and
cancellation reach the import/query worker. Main/renderer event loops do not run
full journal parsing or graph layout synchronously.

## Graph model and presentation

Keep the complete accepted semantic snapshot separate from its visible graph.
Compact integer handles, independently addressable edges and forward/reverse
adjacency avoid treating labels or endpoint pairs as identity. Graphology, if
retained, is a derived working index whose memory duplication is measured.
Raw payloads and inspector attributes use handles/paging rather than full copies
in every render object.

Causal information-flow edges run dependency use point to consumer use point.
Ownership, attachment, finding-subject and decision-effect relations retain
their own typed direction. Traversal selects relation classes deliberately;
not every reference is a causal dependency. Cycles, self-loops, disconnected
components and parallel edges remain inspectable. Cycle-safe BFS supports
bounded neighbourhoods and unweighted paths. SCC condensation is a derived
layout aid, never replacement of the original graph.

Source-provided grouping takes precedence over inferred communities. Every
aggregation reports hidden counts and can expand within the visible budget.
Semantic zoom uses deterministic label/collision budgets; the selected element
always has its complete label and attributes available in the inspector.
Arrowheads, shapes, patterns and text supplement colour. Virtualised tables and
keyboard navigation expose the same semantic information without canvas picking.

The renderer is behind a narrow draw/select/layout interface. Sigma.js with
Graphology implements the renderer following comparison with Cytoscape.js.
Only the selected renderer ships; the validated platform and measurement scope
is described in [Support and compatibility](support.md). Benchmark
label readability, directed parallel-edge picking, loops, high DPI, WebGL loss,
memory and interaction latency, not just maximum vertex count.

## Distribution, future compatibility and review triggers

An application package contains bundled executable JavaScript, the Electron
runtime, selected renderer, required schemas/resources and legal notices. This is executable distribution, not a promise of native-code secrecy.
Exclude authored TypeScript/Python source, source maps, tests, fixtures, build
scripts, development dependency trees and the repository checkout. Preserve
required third-party runtime components and notices through an explicit artifact
allowlist and inspection of nested archives.

Native artifacts are selected by exact product version, OS and architecture,
verified before installation and replace the prior app atomically. No package
manager or compiler runs on the end-user machine. App installation is optional
and independent of JAI's existing CLI source/resource installation. Unsupported
or unavailable assets preserve the existing installation; uninstall leaves
preferences unless a distinct deliberate purge is requested.

Future node/edge notes use a separate store keyed by stable element identity and
applicable source version. Source rewrites may orphan a note, never reassign it
by label. A pure style reducer can later combine base state, selection and
cycle-safe upstream/downstream traversal overlays. No note editor, note storage,
saved flow-colouring feature or dormant source-write API belongs to this version.

Reopen the architecture baseline when canonical source meaning, IPC exposure,
worker composition, identity rules, platform floor or qualification
budgets change. Record deviations with owner, rationale and repayment/review
trigger. Independent implementer and operator review precedes build acceptance;
this document neither records their approval nor waives a failed requirement.
