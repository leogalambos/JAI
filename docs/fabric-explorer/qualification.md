# Qualification envelope

Owner: Fabric Explorer maintainers. Baseline date: 2026-11-09.
Status: maintained acceptance specification. Current observed development scope
and remaining qualification limits are described in
[Support and compatibility](support.md); this specification is not a release
qualification claim.

This reference specifies how an implementation is judged. Version availability,
successful schema checks and a frozen target list do not demonstrate a runnable
application. See [architecture](architecture.md), [decisions](decisions.md),
[dependencies](https://github.com/leogalambos/JAI/blob/main/apps/fabric-explorer/config/dependency-baseline.json) and
[platform targets](https://github.com/leogalambos/JAI/blob/main/apps/fabric-explorer/config/platform-baseline.json).

## Toolchain and dependency admission

Use Node.js 24.22.2 and npm 11.21.2 for application builds. Electron 45.2.3
supplies the packaged Node/Chromium runtime; the viewer does not require an
end-user Node, npm, Python or JAI installation. The import implementation is
bundled TypeScript running in a fixed Node worker, with no external reader or
cryptographic verifier. CPython 3.14.10 remains a development-only synthetic
fixture tool. Historical PyInstaller reader probes are not release components.
Nothing is resolved through the selected project's PATH or configuration.

Exact direct package versions, registry provenance, initial license evidence,
engine constraints, renderer selection and comparator are in the dependency baseline.
That file is not an npm or Python transitive lockfile. Before any executable
candidate is qualified, produce exact platform-specific resolutions with hashes,
license notices and a transitive SBOM. Optional build peers may be omitted only
when unused and identified as optional by the package's own metadata. No package
installation or dependency graph compatibility is claimed by this baseline.

React/React DOM and their types must resolve together; Vitest and coverage
versions must match; the Vite/plugin pair must satisfy declared peers. Validate
the selected renderer's actual API and any custom edge program dependencies
before adding them to a release runtime. A graph benchmark may use both frozen
renderer candidates; the application ships the selected renderer only.

Preserve runtime licenses and bundled third-party notices, including Chromium,
Node and any packaged runtime dependencies. Development-only fixture tools
are excluded from the runtime inventory.
Registry license metadata is preliminary evidence. Inspect actual distribution
files and hooks' exceptions and notices before accepting a release SBOM.

Review upstream security advisories at each dependency change and release;
triage applicable critical/high exposure within one working day and block
release until repaired or explicitly dispositioned by the human risk owner.
Stay within Electron's upstream supported three-major window. An EOL dependency
or a new applicable advisory triggers an owned dependency update and affected
verification, not runtime downloads or silent version floating. Revalidate
future-dated upstream support information before release.

## Platform and artifact contract

The five design targets are Ubuntu 24.04 LTS x64/arm64, Windows 11 24H2 x64,
and macOS 15 arm64/x64. These application floors are intentionally stricter than
some upstream minimums. Every architecture has a separate artifact; no universal
macOS binary or emulated run is assumed. Windows ARM64, musl Linux and older OSs
are outside the advertised target matrix, without changing JAI's role catalogue.

The platform baseline names native build/functional runner labels and desktop
clean-machine targets. Runner labels are documented infrastructure candidates,
not proof that repository runner access or signing identities exist. The release
engineer owns provisioning. Assert the actual OS/architecture/image before
qualification. Windows Server CI is useful for packaging but does not replace
Windows 11 Desktop evidence. Hosted virtual graphics do not qualify hardware GPU
performance or native assistive-technology usability.

Each target has an explicitly named performance-reference profile with a frozen
hardware admission contract. Capture an actual matching host and its exact
CPU/GPU/driver/OS/display/power metadata before measurements. No host has been
enrolled or measured by this document; unavailable hosts block that target's
performance verdict. Do not substitute a faster machine, software rendering or
an emulated architecture and retain the same verdict. Owner: performance engineer.

Linux and macOS use target-specific tar.gz archives; Windows uses a
target-specific ZIP archive. A separate per-user installer verifies and manages
the local package without compiling or downloading dependencies. See
[installation](installation.md) for installation, upgrade, rollback and removal.
Required desktop libraries remain explicit system prerequisites. Distributor
signing and operating-system signing/notarization remain separate release
conditions. Qualify Linux X11 and Wayland independently. No `--no-sandbox`
launch option is permitted to make a packaged acceptance run pass.

An application asset manifest uses the versioned fields in the platform
baseline, an exact asset length and SHA-256, and an external distributor's
Ed25519 signature over its exact bytes. Bootstrap the public distributor key
through the reviewed distribution channel. Never accept a trust key offered by
an input project or an unverified download. This distributor signature is
separate from governed fabric human-decision enrollment and from OS signing.

The operator holds signing credentials outside agent access. No credential has
been inspected, created or claimed provisioned here. Unsigned development
artifacts can support local functional investigation, but cannot qualify release
signing or pass the release installer. macOS nested helper binaries need
proper signing before app notarization; Windows application/helper/installer
signatures and timestamps must verify. Offline runtime operation is required;
online notarization/signature services belong to the external release process.

Install only the compiled app, required Electron/native/runtime resources and
notices. Authored `.ts/.tsx/.py`, source maps, tests, fixtures, developer dependency
trees and build scripts are excluded. Bundled executable JavaScript is an
allowed runtime representation, not a promise of source secrecy. Inspect
Electron's ASAR and its native resources. No Python helper or Python bytecode
belongs to the direct-import runtime allowlist.

The application is an optional JAI installation component. Resolve a local
reviewed asset by exact product version/OS/architecture; never compile or install
packages at the destination. Dry-run does not download or write. A missing or
invalid asset preserves the CLI-only installation and any previous app. Upgrade
is atomic, supports rollback and preserves preferences. Uninstall removes
binaries/launchers; preference purging is a separate deliberate operation.

## Corpora and measurement protocol

All public corpora are synthetic. Give each generated corpus a version, seed,
counts, byte length and digest. Use seed `20261109` for the baseline topology and
fixed test clocks; alternative seeds must be reported separately. Valid fabric
corpora are generated by maintained test builders outside the measured viewer.
Their recorded counts and exact source revisions are the import oracle; the
viewer does not rerun canonical verification. Bare projection DTOs cannot
substitute for actual JSONL source admission.
Any corpus that exercises rendering alone is labelled a projection benchmark.

| Corpus | Vertices | Edges | Findings | Encoded selected input size |
| --- | ---: | ---: | ---: | ---: |
| S | 1,000 | 3,000 | 100 | 10 MiB |
| M | 25,000 | 100,000 | 5,000 | 250 MiB |
| L | 100,000 | 500,000 | 20,000 | 1 GiB |

Padding and raw material contribute to byte-size targets but are reported
separately from indexed metadata. Keep graph counts, encoded input bytes and
canonical transaction count distinct. Include high-degree hubs, disconnected
components, cycles in permitted associations, parallel edges, long Unicode
labels, multiple versions and unresolved subjects. Use field-aware graph
generation so a causal cycle rejected by the runtime is a negative case, not a
pretend valid journal. Representative topology distributions may be derived from
permitted private observation; public fixtures contain no identifying values or
provenance. Evidence from private inputs stays private.

Use a 1920x1080 logical viewport at 100% scale for performance. Default visible
budget is 2,000 vertices/8,000 edges; explicit bounded expansion allows at most
5,000/20,000. Counts omitted by filters, aggregation or limits remain visible.
The maximum expansion is a bound, not a claim that its frame-time equals the
default projection. A failed essential label/direction/picking interaction
disqualifies a renderer regardless of throughput. Accessibility qualification
also covers 150%/200% scale and the actual shipped theme(s).

| Metric | Frozen threshold | Measurement |
| --- | --- | --- |
| Shell readiness | <=3.5 s (owner-adopted ceiling) | Ten fresh packaged process launches: OS spawn to ready controls; report median and maximum, require each run to pass |
| Cold import | M <=10 s; L <=45 s | Ten fresh application/import sessions: accepted root selection to usable indexed overview; include parsing, source capture and query/index publication; each run must pass |
| Exact-ID query | p95 <=100 ms on M | Five warmups, 30 timed mixed ID queries, including absent/versioned IDs; request to response |
| Indexed text query | p95 <=300 ms on M | Same sampling; fixed mix of frequent, sparse and absent terms, paginated result correctness checked |
| Cached inspector | p95 <=100 ms on M | Selection to visible metadata; vertex/edge cases, 30 after five warmups |
| Raw record page | p95 <=500 ms on M | Selection/page request to escaped visible page, including disk read if not cached |
| Pan/zoom | p95 frame time <=33 ms | Fixed 20-second active pan/zoom script on default visible graph; measure presented active frames; do not discard slow frames |
| UI responsiveness | No renderer UI task >250 ms; optimization target 200 ms | Renderer long-task durations during import/layout; main-process event-loop delay and cancellation are supporting evidence, without an exhaustive individual-task claim |
| Peak resident memory | M <=2 GiB; L <=4 GiB | Sum RSS/working sets across app and workers, sampled <=100 ms; include old/new refresh overlap and import peak |
| Cancellation | Ack <=250 ms; quiescence <=2 s | Request to accepted cancellation and termination/quiescence; old usable snapshot retained |
| Endurance | 30 min on M | Repeated selection/filter/focus/open/close/refresh; no crash, unbounded queue or monotonic retained-session growth; peak memory remains within budget |
| Usability | Owner acceptance of the functional and ergonomic workflows | Record the owner's explicit assessment of entity/relationship/finding exploration and the current interface; no five-user study or task-time threshold is required |

Calculate p95 using nearest rank `ceil(0.95*n)` on sorted recorded samples;
report all samples and failures, not just aggregates. Search is an indexed query
metric; separately capture end-to-end input/result visibility during usability
qualification. RSS summation can double-count shared pages; use that conservative
definition consistently and record OS-specific measurement APIs. Functional
deadline/expiry tests use controlled clocks. Real-time performance tests do not
change production deadlines, add retries or hide failed samples.

Freeze dataset generation and measuring scripts with each measured revision.
Record both raw input and graph-projection dimensions. Cache state is explicit:
fresh process means no retained import model; report OS cache conditions without
requiring privileged global cache flushing. An unchanged refresh reuses the
accepted generation; measure changed-source refresh separately from cold import. GPU context loss,
worker death, malformed input and failed refresh must preserve a safe usable
prior generation or a bounded error screen without source modification.

## Resource and security acceptance

Bound acquisition before allocating or decoding: selected input aggregate at
most 1 GiB, structured non-journal file/decoded record at most 100 MiB,
material objects at most the canonical 32 MiB, JSON nesting depth 64, raw display
page 256 KiB and at most 1,000 visible diagnostics with complete counts.
Each IPC frame is at most 8 MiB; larger permitted records are transferred as
bounded pages/chunks. Source FileHandles transfer only through main-owned
worker messages, never the renderer bridge. At most eight exploration tasks may
be outstanding per session; backpressure rejects or queues bounded work explicitly.
Interactive traversal is capped at 10,000 visited vertices/50,000 scanned edges
and 32 hops, with result limits bounded by the visible projection. Exhaustion
reports an incomplete result; it cannot assert that no path exists.
Journal aggregate size is not confused with a single-record limit. Canonical
reader memory can exceed raw input size substantially; qualify peak process-tree
memory and retain the failing limit as a diagnostic. A resource guard never
labels a silently truncated graph complete.

Before allocation, reserve for current and candidate generations, indexes and
IPC copies. If the envelope cannot fit safely, reject the requested operation
with the named limit and retain the old view. Threshold changes require an
explicit versioned baseline update and rerun of affected acceptance scenarios.

Required negative cases include input mutation attempts, traversal, symlink and
reparse-point races, hard links, nonregular files, denied ACLs, in-place journal
changes, partial tails, unsupported versions, duplicate/normalized JSON keys,
lossy integers, hostile Markdown/HTML labels, IPC capability forgery and stale
generations. Exercise real OS filesystem boundaries. Source snapshots and
directory entries remain unchanged; no lock files or bytecode caches appear in
input roots. Recorded applicability never implies fresh qualification or human
release authority. Source chain, signature and lifecycle verification are not
performed by this viewer; no public enrollment or private key is required.

No default network, telemetry, remote fonts, content navigation, external-open,
project-controlled subprocess or auto-update path is allowed. Application-requested
external reader launches are absent from direct import. Intrinsic Electron
renderer/GPU/utility/crash-handler children (including packaged macOS Helper
binaries) are allowed only as fixed packaged runtime components; they retain
their sandbox/capability restrictions and cannot resolve extra project binaries.
Include these runtime children in process-tree network/write/memory checks.
Test both denied capabilities and actual
behavior; a declared Electron setting alone is insufficient. Persist preferences
only outside selected roots; reject overlap, including an app-data/root collision.
Crash recovery must not automatically reopen projects. Corrupt preferences reset
safely; local clear-data actions never delete selected source material.

## Evidence and acceptance boundaries

Each result identifies source/artifact revision, relevant input/dependency
digests, OS/architecture/image, host metadata, corpus/seed, command, samples,
result, duration and rerun trigger. Private results and operational records stay
private; public claims use sanitized maintained specifications and qualified
artifact facts. A screenshot proves neither semantic fidelity nor source safety.

Run direct invariant tests after meaningful edits and affected boundary checks
at a coherent increment. Once a broad product change is stable, run the complete
maintained suite for the affected product once. A whole-JAI run is warranted
when shared core behavior is affected or the impact is unknown, rather than for
every viewer increment. An interrupted run is not a passing result. Preserve
valid evidence for unchanged inputs; do not repeatedly replay unrelated
historical prefixes. Reviewers report findings and verify repairs independently
of authors. Human release decisions, signing and actual publication remain
separate from design and test acceptance.

## Primary dependency and platform sources

- [Electron supported release policy](https://www.electronjs.org/docs/latest/tutorial/electron-timelines)
- [Electron security recommendations](https://www.electronjs.org/docs/latest/tutorial/security)
- [Electron 45 release](https://www.electronjs.org/blog/electron-45-0)
- [Node 24.22.2 release](https://nodejs.org/en/blog/release/v24.22.2)
- [Native GitHub runner specifications](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)

Upstream pages change. Exact package metadata is frozen in the dependency
baseline; updates require a reviewed new baseline rather than reinterpreting
historical qualification against today's `latest` page.

## Focused import comparison

The development runner accepts `--imports` for exactly one fresh-process import at each S, M and L tier. Each case has six numbered stages. Existing diagnostic envelopes remain 180/180/240 seconds; the outer bound is 1,006 seconds including the existing drain and integrity reserves. This mode repeats no boot, query, retention, fault or endurance population. It provides a finite before/after observation, not the ten-run cold-import qualification or a waiver of unchanged timing and memory requirements. Missing or failed cases remain incomplete.
