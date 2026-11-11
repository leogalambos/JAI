# Fabric Explorer source contracts

Owner: JAI runtime maintainers. Reviewed source date: 2026-11-11.
See [Support and compatibility](support.md) for validated compatibility and
platform scope.

This reference records the maintained input formats and the obligations of a
read-only graph consumer. Source facts below describe the current implementation;
graph mapping rules specify the consumer contract. A valid message example is
not an admitted journal or proof that a runtime transition occurred.

## Authoritative sources and compatibility

| Input | Maintained contract and reader | Consumer treatment |
| --- | --- | --- |
| Governed fabric journal | [lifecycle.py](https://github.com/leogalambos/JAI/blob/main/.ai/runtime/tools/lifecycle.py): format `9`, protocol `jai.governed-delivery/1`; `Store.read`, `replay`, `_transaction_shape`, `_verify_transaction` | Required input family. Preserve recorded sequence/head claims and project recorded manifests/effects directly. Canonical APIs describe the producer, not the viewer runtime. |
| Record schemas | [record.schema.json](https://github.com/leogalambos/JAI/blob/main/.ai/runtime/protocol/governed-delivery/v1/record.schema.json), [common.schema.json](https://github.com/leogalambos/JAI/blob/main/.ai/runtime/protocol/governed-delivery/v1/common.schema.json), [message.schema.json](https://github.com/leogalambos/JAI/blob/main/.ai/runtime/protocol/governed-delivery/v1/message.schema.json) | Six closed record families; proposals and messages are wrappers, not admitted versions. |
| Immutable manifests | `lifecycle.manifest`, `record_manifest`, `version_id` | Schema `jai.lifecycle.manifest/2`; kinds `delivery.source`, `delivery.profile`, `delivery.assignment`, `delivery.context`, `delivery.product`, `delivery.assessment`, plus derived `delivery.decision`. |
| Fabric material | `Store._blob`, `lifecycle.blob` | Companion directory `<engagement>.jsonl.blobs`; each blob is addressed by its domain-separated digest. The viewer reports bounded admitted-path readability without verifying this content digest. |
| Findings journal | [findings.py](https://github.com/leogalambos/JAI/blob/main/.ai/runtime/tools/findings.py): `_parse_events`, `state` | Required input family. Parse the unversioned envelope and reduce recorded events without chain verification; do not invent a schema version or treat it as format-9 fabric. |
| Audit projection | [governed_audit.py](https://github.com/leogalambos/JAI/blob/main/.ai/runtime/tools/governed_audit.py): `report` | Optional explicit input, format `jai.gen2-audit/1`. It covers selected products and their assessed closures; it is not a complete graph export. |

[fabric.py](https://github.com/leogalambos/JAI/blob/main/.ai/runtime/fabric/fabric.py) uses `FABRIC_HOME`, defaulting to
`~/.ai/fabric`, and `<engagement>.jsonl`. Findings use `FINDINGS_HOME`, defaulting to
`cwd/.findings`, and `<ledger>.jsonl`. A project `.fabric/` directory is an explicit
convenience location, not the only canonical location. Selecting a project and
source families permits bounded lookup of immediate regular `.jsonl` files in
its `.fabric/` and `.findings/` directories. Unavailable or over-limit lookup
falls back to a native file dialog rooted in that project or its available
family directory. Audit and other locations require explicit file selection.
The viewer does not inspect environment-selected homes, scan recursively or
execute configuration found in the selected project.

Canonical producer verification rejects unsupported formats and semantic encoder
versions. The viewer rejects unsupported outer formats; an opaque recorded message
codec does not trigger adjudication of otherwise readable recorded effects. Archived
Gen1 mutation/evaluation logic is not a fallback for Gen2. The older professional
catalogue and workflows remain outside this viewer adapter boundary; this
restriction does not remove them from JAI. The viewer requires a supported envelope and safe structure, without claiming
that successful parsing establishes canonical validity.

## Identities, scope and source locators

A governed reference has exactly `engagement`, `scope`, `logical_id`, `version_id`.
`scope` is the version's origin scope. A use point adds `use_scope`; applicability
can differ for two uses of the same immutable version. `State._point`, `_key`,
`_assignment_use`, `_subject_use` and `_dependency_point` define these distinctions.
Do not equate origin scope with applicability scope.

Use a project namespace and exact reference for a version vertex, and preserve
use points separately or as explicitly typed use vertices. A short label or
`logical_id` alone is not a persistent key. Findings keys must include the
project and ledger as well as `F-0001`, which is only ledger-local. Blob keys must
include their source namespace. Missing referenced records remain unresolved
objects with their original reference, never silently rebound by matching labels.

Each projected element needs a source family, selected-root identity, relative
file locator, record pointer or sequence, exact source revision and adapter
version. An explicit source edge ID takes precedence. Otherwise address an edge
by source record/version, reference-field pointer and occurrence, including both
use points where applicable. Endpoint pairs do not distinguish parallel edges.
Reordering an occurrence-based relation can change its address; retain that
limitation for future annotation reconciliation.

Lifecycle semantic JSON normalises strings and keys to NFC, rejects duplicate
normalised keys, floats and nonfinite values, and preserves integer precision.
`version_id` uses `jai.lifecycle.version.v2\0`; blobs use
`jai.lifecycle.blob.v2\0`; transactions use `jai.lifecycle.transaction.v9\0`.
Python's sorted-key encoding must not be replaced by ordinary JavaScript
stringification. A TypeScript boundary must encode large integers losslessly and
keep raw proof bytes separate from semantic JSON. No IEEE-754 coercion, newline
normalisation or display truncation may change identifiers or captured bytes.

## Record-to-graph mapping

The paths below are relative to `manifest.content.record` unless stated
otherwise. Preserve all remaining closed-schema properties in the inspector;
the table identifies graph semantics, not a field-dropping transformation.

| Family | Vertex and inspected fields | Typed relationships and exceptions |
| --- | --- | --- |
| `source` | `source_role`, `owner`, `origin`, `criteria`; roles input/criteria/policy/assumption remain distinct | `inherited[]` references; `origin.ref` when the origin is an assignment; `material[]` blob references; each criterion's `requirement` reference. Authority/controller origin values are provenance, not fabricated version references. |
| `profile` | `profile_id`, `protocol`, `owner`, obligations, clock/request limits, authority/routing policy IDs, scheduling, content profile and local budget | `source_profiles[]`; nested exact references remain inspectable. Scalar policy IDs are attributes unless a maintained reference field provides a target. |
| `assignment` | `responsibility`, `assigned_actor`, `owner`, limits, deadline, use scope and routing | `profile`, `inherited[]`, `inputs[].refs[]`, `criteria`, nullable `issued_under`, `routing.policy`; retain `inputs[].slot_id`, `input_uses[].at/use_scope` and nested effect policy/target references. `handling.episode/package` are handling associations excluded from causal dependency extraction. |
| `context` | `purpose`, `run_id`, `issued_to`, `owner`, expiry, effects, execution phase, speculation and ready-basis metadata | `assignment`, `profile`, `inputs[].refs[]`, `execution.selection` when present; `attachments[].blob_id` denotes material with byte length, media type, classification and access handle. Opaque access handles are not file paths. |
| `product` | `product_kind`, `owner`, limitations and optional episode/outcome | `assignment`, `profile`, `inputs[].refs[]`, `material[]`, `evidence[]`, `related[].refs[]`, and exact optional episode/outcome references. Escalation `episode` and `related` associations are excluded from canonical causal dependencies. Keep all product kinds, including finding, answer, observation, handoff, bundle, escalation and final_result. |
| `assessment` | `assessment_kind`, `verdict`, `assessed_hash`, `findings`, conditions and owner | `assignment`, `subject`, `criteria`, `profile`, `assessed_closure[].ref` with its own `use_scope`. Professional, integration and receiving assessments retain their own kind and verdict vocabulary. An assessment is not a standalone findings ledger. |
| `decision` | Derived by `State._decision_manifest`; identity `decision:<request_id>`, owner and complete `message` | `message.payload` exact targets, bases and decisions remain typed associations. The viewer projects recorded effects and use transitions without evaluating their authorization. Never infer acceptance or release from the presence of a decision-shaped JSON object. |

[governed_records.py](https://github.com/leogalambos/JAI/blob/main/.ai/runtime/tools/governed_records.py)
`build_proposal` builds source/assignment/product/assessment proposals for an
existing work packet. It does not write or admit them. `record.schema.json` also
defines profile/context; the consumer must not accidentally restrict its record
catalogue to the proposal builder's subset.

## Relationship direction registry

Every edge carries a relation type, semantic direction, originating field,
derivation basis and exact endpoints. Layout orientation does not redefine it.
The graph can contain association cycles and parallel edges even though a
canonical scoped causal closure rejects a causal dependency cycle.

| Relation class | Display direction | Basis and traversal policy |
| --- | --- | --- |
| Causal dependency | Dependency use point → consuming use point | Recorded references, use selectors and dependencies; separate structural projections support traversal without asserting validity. Not every nested reference belongs here. |
| Input binding | Referenced input → binding consumer | Preserve slot ID, occurrence and selected use scope; retain the format's structural reference classification. |
| Profile/criteria/inheritance/assignment | Referenced prerequisite → containing record | Keep field-specific labels rather than collapsing them into one generic edge. Use recorded structural scope selectors. |
| Assessed subject | Subject use point → assessment | Identifies what was inspected; an assessment verdict does not make every connected record valid. |
| Material attachment | Containing record → blob | Provenance/attachment relation, not the same direction convention as causal information flow. Missing blob remains visible. |
| Actor/ownership | Record → declared participant or ownership descriptor | Provenance only. Participant kind/ID or ownership tuple is not a grant or an enterprise identity assertion. |
| Decision effect | Decision → affected use point | Establishment, cancellation, withdrawal, permission cancellation or other source event retains its exact kind and scope; no causal-flow inference from the arrow alone. |
| Finding subject | Finding → exact resolved subject | Only when a source-supported exact reference exists. Textual locations and target strings remain unresolved/location associations unless exact resolution is established. |
| Other exact reference | Referencing record → referenced record | Field-labelled association excluded from causal traversal unless its recorded structural classification includes it. |

`_causal_reference_paths` excludes handling links and escalation episode/related
links. For an assignment it also excludes read-grant target references; tool
policies and non-read effect targets still participate. The dependency engine
also applies scope-specific rules, including the global routing-policy anchor
and `issued_under` ownership scope. A regex over all digest strings cannot
reconstruct this graph. No string similarity becomes an asserted edge.

## Journal and refresh semantics

A format-9 row has the closed fields `format`, `protocol`, `engagement`,
`sequence`, `previous`, `transaction_id`, `timestamp`, `operations`,
`authority_proof`, `return_artifact`, `validation_artifacts`, `hash`. It contains
one `governed` operation with `data.message` and `data.effects`. Producer validation checks
the sequence, predecessor, unique canonical transaction UUID and hash, then
replays the message and compares the exact derived effects and validation assets.
Hash-chain validity alone is not canonical semantic verification.

The producer's `Store` verifies canonical history and maintains its own checkpoints. The viewer does not construct it or load producer modules. Viewer-local TypeScript projection indexes recorded manifests, provenance, use effects and structural selectors. Unchanged Refresh reuses the accepted worker and generation after file-observation checks. Changed-source candidates and the automatic initial load after source selection parse a new selection once into a separate worker. The lower application bridge retains its explicit import operation for orchestration and qualification; it is not a separate normal user action. They do not perform canonical history verification or claim incremental suffix projection.

Direct adapter `/2` source sequence and locator sequence identify physical JSONL row counts and ordinals. Recorded sequence claims remain exact in provenance, attributes and captured bytes; duplicate or descending recorded claims are not continuity judgments. Replacement rejects refresh under the admitted source identity contract. Malformed data and concurrent changes reject the candidate without replacing the accepted view.

Read-only consumers must not expose `Store.submit`, `put_blob`, writer locking,
findings commands or repair paths. Opening a missing path cannot initialise an
engagement. A failed refresh retains the previously displayed generation with a
stale/error indication. Watch notifications are hints; publish a new view only
after its selected inputs, parsing and indexes agree. Concurrent append/in-place
change can invalidate a read; do not hide it with unbounded retries.

Incomplete or unreadable JSON tails fail import rather than silently becoming
admitted records. Complete readable recorded effects are displayed without
re-adjudicating their chain, authority or transition legality. Ledger sequence is local to that ledger. No shared global
transaction or reliable total ordering follows from fabric/findings timestamps.
A combined view records each source head/revision and its observation time;
absent a maintained common boundary, describe it as an observed revision set.

## Findings mapping and transition semantics

The findings envelope is `seq`, `ts`, `data`, `prev`, `hash`; sequence begins at 1
and `prev` begins at 64 zeroes. Hashing is SHA256 of UTF-8
`prev + canonical(data) + str(seq)`. Findings `canonical` is sorted-key compact
JSON with `ensure_ascii=False`; it does not apply lifecycle NFC or domain prefixes.
These are producer serialization rules. The viewer directly parses events and
reduces recorded operations without `_parse_events` or chain recomputation.

`add` records review `reviewer`, `target`, `criteria` and each finding's `id`,
title, severity, kind, location, criterion, evidence and recommendation. Preserve
all values and raw provenance. Severities are critical/high/medium/low; kinds
are defect/gap/risk/inconsistency/suggestion. `target`, `location` and resolve
`ref` are textual, not guaranteed governed references. Findings emitted as
`product_kind=finding` belong to the governed product family and are distinct
from these ledger-local findings.

| Event | State/reducer result | Important distinction |
| --- | --- | --- |
| `add` | `open`, rounds 0, resolver null | IDs are scoped to one ledger. |
| `resolve` | `resolved`, remembers resolver | Rework awaits independent verification. |
| `verify`, `ok=true` | `verified` | Different from a merely resolved finding. |
| `verify`, `ok=false` | Increments rounds, then `open` or `stuck` | The producer threshold is configurable and not recorded per event. The viewer reports its display threshold (3) and historical uncertainty. |
| `withdraw` | `withdrawn` | Not equivalent to verified. |
| `accept-risk` | `accepted`, records `expires` | Time-bound human decision metadata, not proof the defect was repaired. |

Preserve each history event's actor/note/timestamp and the event envelope. The
canonical producer reader checks the chain; command preconditions enforce who
can resolve or verify and when. The viewer performs neither check. A chain-valid arbitrary event stream is not proof those command
preconditions were observed. `state` does not automatically expire acceptance;
display its recorded expiry separately. When historical round configuration is
unknown, expose the round count/configuration uncertainty rather than asserting
a universal stuck threshold. Non-suggestion open/resolved/stuck findings block
the canonical summary; open suggestions do not.

## Verification levels and diagnostic display

The viewer reports `mode: recorded`, `decoded: decoded`, `chain: unknown`,
`replay: recorded` and `publicTrust: unknown`. It does not authenticate journals,
verify historical signatures, consult enrolled trust or grant authority. Private
signing keys, OpenSSL and public trust enrollment are not viewing requirements.
Captured SHA256 identifies displayed bytes; it is not a chain or authenticity
verdict. Recorded head/sequence claims, use states, Findings verification events
and acceptance/release claims remain source content, not fresh conclusions.

`governed_audit.report` captures one `Store.read` snapshot and reports
`history_verified`, `head`, `assessed_at_ms`, `recorded_applicability`, `read_only`
and `authority_granted=false`. Inventory state is not a fresh assessment of every
product. `_output` assesses only selected/requested products and distinguishes
missing material in their governing closure from irrelevant historical material.
The GUI must not rerun those assessments on every redraw or present a saved
report as a fresh current decision.

Canonical producer verification may reject a history that the viewer can safely
display. Recorded broken chains, invalid signatures and opaque message codecs do
not trigger duplicate adjudication here. Malformed or unsupported structure gets
a bounded diagnostic and retains the previous snapshot. Missing exact references
remain unresolved; structural projections do not assert an authoritative current
governing closure. No source execution, dynamic project imports, remote fetches
or mutation are permitted.

## Filesystem and installation baseline

The production native broker opens project-discovered or explicitly picker-selected files read-only, pins their lossless native file identities and transfers handles to the fixed Node import worker. It rejects detected links, nonregular files, hard links, overlapping application-write destinations and changed identities. The worker streams each source once into its private archive while parsing; accepted inspector pages read the immutable archive. Producer `operator_actions.journal_snapshot` and the historical Python filesystem adapters are not runtime dependencies.

Portable Node admission observes parent paths but does not promise atomic confinement against hostile parent-directory replacement during initial acquisition. Later reads bind the admitted file identity and validate finite capture metadata. Windows and macOS source reading remains available; their native qualification is deferred rather than inferred from Linux. No Python runtime, cryptographic verifier or project-loaded code is required by the production viewer.

[install.sh](https://github.com/leogalambos/JAI/blob/main/install.sh) invokes Python
[installer.py](https://github.com/leogalambos/JAI/blob/main/.ai/setup/installer.py). Its `desired_outputs` prepares
runtime/skills/agents/commands and a managed manifest without writing the
destination; `main` applies those outputs or reports a dry run. Neither includes
this application.
The separate [viewer installer](installation.md) installs a prebuilt portable
archive or explicitly builds the current host target with `--build`. The
[package contract](building-packages.md) includes the runtime and application
assets; it does not install the development tree or alter the CLI installation.
Packaging a target does not establish native Windows/macOS qualification;
see [Support and compatibility](support.md).

## Optional sources and synthetic fixture coverage

Optional inputs require explicit adapter/version selection; never import every
JSON file under a project. Audit `jai.gen2-audit/1` is the identified read-only
projection above. [Execution statistics](https://github.com/leogalambos/JAI/blob/main/.ai/runtime/tools/execution_stats.py)
use version-one aggregate summaries in `.jai/stats`; aggregates are not journal
authority or per-element evidence and are deferred from the initial graph
mapping. [SABSA/EA schemas](https://github.com/leogalambos/JAI/blob/main/.ai/runtime/sabsa/schema/elements.json)
describe a separate repository projection; these need their own explicit adapter
and identities and are deferred. Neither deferral changes their availability in
JAI. Arbitrary attachments are inert material, not plugins or executable inputs.

The [fixture manifest](https://github.com/leogalambos/JAI/blob/main/apps/fabric-explorer/test/fixtures/manifest.json) references maintained public
protocol examples without copying their definitions. It covers source roles,
profile, assignment, context, product kinds, assessment kinds and decision
messages. These are structural examples, not admitted format-9 journals.
`findings-review.jsonl` and `expected-findings.json` in the same directory contain
fixed synthetic findings history and reducer expectations, including all six
states under explicit round configuration. Their identifiers are fictional.

[test_fabric_explorer_sources.py](https://github.com/leogalambos/JAI/blob/main/tests/test_fabric_explorer_sources.py) checks the synthetic
baseline against canonical schemas/readers. Full journal semantics and scoped
audit cases remain in [governed_fixtures.py](https://github.com/leogalambos/JAI/blob/main/tests/governed_fixtures.py),
[test_governed_audit.py](https://github.com/leogalambos/JAI/blob/main/tests/test_governed_audit.py),
[test_lifecycle.py](https://github.com/leogalambos/JAI/blob/main/tests/test_lifecycle.py),
[test_findings.py](https://github.com/leogalambos/JAI/blob/main/tests/test_findings.py) and
[test_operator_journal_snapshot.py](https://github.com/leogalambos/JAI/blob/main/tests/test_operator_journal_snapshot.py).
Fixture validity does not establish UI, performance or platform qualification.
