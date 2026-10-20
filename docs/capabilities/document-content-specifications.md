# Document Content Specifications

Owner: JAI maintainers · Last reviewed: 2026-10-20

The 26.10.11 content implementation describes what an output must contain,
why each obligation exists and which existing role contract it supports. It
extends JAI through `jai/profiles/content-profile.json`; it does not introduce a
second semantic model, approval service or publication renderer.

## Scope and acceptance status

The catalogue preserves the 28 existing artifact types and registers explicit
`document_kinds` beneath them. Stable sidecar bindings connect the existing
1,139 role contracts to content specifications without rewriting their IDs,
source fingerprints, historical decisions or immutable Artifact Contract v3
schemas. Publication archetypes and SABSA mappings reference the same catalogue.
Production classification must use an explicit registered binding, never a guess
from the deliverable name.

All 1,139 role bindings now resolve authored **proposed** content contracts.
The 28 type foundations, six domain specialisations, 13 publication archetypes
and 19 SABSA views contribute typed obligations. Each remaining role-specific
kind retains its own purpose, required input duties, receiving acceptance and
contract relations. This preserves distinct specialist outputs instead of
replacing them with one generic document template.

Ten priority families retain detailed simple, medium and complex scenarios:
decision paper, ADR, business case, risk assessment, assurance report,
architecture definition, HLD, operational handover, runbook and test report.
Architecture definition describes architectural context and viewpoints; HLD
specifies a particular implementation. SABSA risk treatment strengthens the
risk-assessment contract with business-attribute and residual-acceptance links.

The additional catalogue probes exercise registered types and overlays through
the real deterministic validator. Coverage requires observed positive, negative
and borderline evaluations; a generated policy file alone is insufficient.
These probes establish development coverage, rather than professional semantic
adequacy. Review-based predicates remain pending without attributable review.
Calibration remains **synthetic-only**. Competent human approval of proposed
standards, real enterprise calibration and human-approved gold remain pending.
The 26.10.8 GA label in the plan is an acceptance target, not an approval granted
by implementing the version or passing synthetic tests.

## Resolve and inspect a specification

Run these commands from the repository root:

```sh
python3 .ai/runtime/tools/content_spec.py list --root .
python3 .ai/runtime/tools/content_spec.py lint-registry --root .
python3 .ai/runtime/tools/content_spec.py coverage --root .
python3 .ai/runtime/tools/content_spec.py resolve --artifact-id solution-architect:1 --root .
```

Choose an actual registered ID from the catalogue; a missing or ambiguous ID is
an error. Use `--context context.json` for explicit contextual applicability.
The `compile --spec-ref ID` command compiles a registered specification directly.
Resolution records the selected specification/version, selection reason and
compiled hash, so a later consumer can identify the exact obligations used.
Installed tools accept the installed library root through `--root` as well.

A compiled specification supplies a blueprint of semantic information units,
evidence duties, conditional applicability and size guidance. A heading alone
cannot prove that a substantive unit has been fulfilled. Unknown inputs remain
explicit unknowns; the author must not invent evidence to satisfy a template.

## Precedence and governance

Applicable law and binding organisational/customer requirements take precedence;
global security invariants, type policies, domain specialisations, presentation
overlays, role duties and engagement context follow. Lower levels may strengthen
obligations but cannot silently remove or weaken them. Unresolvable inheritance
or policy conflicts are `SPEC_CONFLICT` errors. Every derived obligation records
its basis; professional proposals are not represented as verbatim ISO requirements.

Both Claude and Codex adapters reference the same content profile, catalogue and
resolver. Provider permissions and human authority boundaries remain unchanged.
New content policies are advisory during the pilot. Existing security,
authorization, evidence and governance gates keep their current mandatory
behaviour. Editorial irrelevance and verbosity are distinct from security
prohibitions; initial size envelopes are calibration proposals, not a universal
mechanical word-count block.

Specific standards require independent competent human domain approval through
existing [JAI L0 authority](../operations/human-authority.md). An agent cannot
approve its own policy or upgrade synthetic examples to human-gold. Structural
CI acceptance and a product version change do not grant that approval.

## Compatibility and rollout

Older unprofiled installations remain readable. When the DCS sidecar profile is
present, `artifacts.py check` also validates its catalogue references and policy
conflicts. Source validation and release qualification run the same structural
lint while retaining all existing checks.

The shared implementation provides content outlines, deterministic semantic validation, immutable
content QA reports and projection/publication integration. Existing publication
and visual QA remain separate controls; a successful render never constitutes
content approval. All pilot results retain the synthetic-only qualification.
Independent semantic review predicates remain pending until attributable review
evidence is available. A structurally complete document is not automatically
CONTENT_PASS or RELEASED.

Rollback consists of reverting the foundation's new files and integration hunks
in an ordinary reviewed change. No historical contract, signed record or evidence
migration is required. Remove profile references together with the sidecar;
a partially removed packaged profile intentionally fails structural lint.

## Authoring and content QA pilot

Resolve the explicit role binding and create an authoring outline:

```sh
python3 .ai/runtime/tools/content_spec.py resolve --root . \
  --artifact-id enterprise-architect:4 > compiled.json
python3 .ai/runtime/tools/content_spec.py outline --root . \
  --artifact-id enterprise-architect:4 --output outline.json
python3 .ai/runtime/tools/content_lint.py check semantic.json \
  --spec compiled.json --output content-qa.json --provider codex
python3 .ai/runtime/tools/content_metrics.py analyze semantic.json
python3 .ai/runtime/tools/content_eval.py run --root . \
  --output build/dcs-26.10.8-pilot.json
```

The semantic source records its instance `artifact_id`, explicit role
`contract_id`, registered `document_kind`, `compiled_spec_hash` and typed
context. Required information belongs in `semantic_units`. Claims distinguish
known facts, assumptions and pending knowledge. Known material claims require
versioned evidence with a verified payload hash and explicit freshness dates.

The evaluator retains the original 30 priority references and 270 mutations,
and adds 1,225 enterprise probes with nine mutations each. The complete run
therefore evaluates 1,255 references and 11,295 seeded mutations. Every mutation
runs the production validator; expected identifiers are compared with actual
located findings. The report records source/specification/report hashes,
critical false negatives, reference false positives and evidenced catalogue
coverage for bindings, kinds, types, domains, archetypes and SABSA views.

The initial development thresholds remain 95 percent critical seeded-defect
recall and at most 10 percent reference false positives. A failing or incomplete
catalogue dimension fails the full pilot. These are synthetic development
thresholds, not enterprise calibration or professional acceptance. The report
never upgrades a synthetic example to human-gold.

Both provider paths use the same registry and deterministic validator.
Behavioral parity tests execute the CLI for Claude and Codex against identical
inputs and compare reports. This establishes engine parity, not equivalence
of unconstrained model-generated prose or human review judgments.

New content checks remain advisory or warning during this release. Blocking
activation requires qualified scope and existing human authority evidence;
a CLI mode or model-declared approval cannot grant it. Existing security,
evidence and governance failures remain blocking. A review must come from an
independent attributable execution, reference exact source/specification hashes
and contain located findings. Self-declared reviewer names are insufficient.

## Embedding the existing trusted host

The Python embedding API accepts the existing runtime verifier rather than
trust data supplied by a document. Reuse the host-owned
`commercial_runtime.TrustedDispatcher` instance that issued the producer
and reviewer attestations. Its authenticated principals must differ; the
review must bind the exact semantic snapshot, compiled specification and
context, with substantive per-unit observations. A renamed author is still
the same principal. An unmatched verifier or stale snapshot leaves the
review unverifiable and cannot establish content acceptance.

The host supplies these objects directly; this example assumes the host
has already loaded its canonical model, resolved specification, independent
review and existing fabric. It neither creates attestations nor approves
an artifact:

```python
from content_lint import ExistingFabricAuthority, evaluate
from projection import build
from publication import render_verified

authority = ExistingFabricAuthority(existing_fabric, accepted_fragment_id)
report = evaluate(
    model, compiled_spec, reviewer=independent_review,
    trusted_executions=existing_dispatcher, authority=authority,
)
problems, publication_model, manifest = build(
    semantic_path, profile_path, projection_directory,
    reviewer=independent_review,
    trusted_executions=existing_dispatcher, authority=authority,
)
if problems:
    raise ValueError(problems)
render_verified(
    publication_model, manifest, projection_directory,
    "docx", output_path, theme,
    trusted_executions=existing_dispatcher, authority=authority,
)
```

`ExistingFabricAuthority(fabric, fragment_id)` reads an existing signed
L0 acceptance of an L1 fragment. The fragment's persisted `text` contains
strict JSON with `profile: "content-enforcement"` and the scoped
`dcs_activation` payload. The adapter checks the existing fabric, strict
justification, accepted L0 review and pinned fragment hash. It does not
read an ad hoc node attribute, create a second approval command or provide
a new key service. The fragment and its acceptance follow existing JAI
answer/ingest and human authority procedures. Normal advisory evaluation
does not activate blocking enforcement merely because this adapter exists.

The command-line tools never accept a JSON file as a trusted verifier.
Host authentication and key custody remain runtime configuration, outside
the semantic model. Reusing a saved report requires the matching trusted
host and immutable source/specification sidecars so that its findings can
be recomputed and compared. A report hash alone proves neither reviewer
identity nor professional correctness.

New projection writes use the DCS-bound v4 manifest. Historical v3
manifests remain readable for compatibility; a new render requires a v4
projection rebuilt from an explicit contract binding. The current render
path marks output `DRAFT_INCOMPLETE`. Deterministic completeness or an
independently authenticated review does not approve a proposed domain
standard, upgrade synthetic calibration to human-gold or release the
publication. Those remain separate existing human authority conditions.

## Workflow receiving acceptance

The shared registry maps all 207 handoffs across 24 workflows to existing
contract IDs, producing roles, receiving roles and specific acceptance criteria.
It does not create 207 new document types. Inspect the explicit bindings:

```sh
python3 .ai/runtime/tools/content_workflow.py --root . list
python3 tools/generate_content_workflows.py --check
```

An embedding host calls `content_workflow.check` with the selected handoff ID,
canonical semantic source, exact content QA report and receiving evidence.
The checker replays QA, verifies the registered contract and requires a receiver
whose authenticated principal differs from the producer. Receiving roles come
from host-owned assignments, rather than role names asserted in a document.
The attested subject binds the handoff, catalogue, source and report hashes and
the specific acceptance criterion. A final human authority step requires the
existing signed JAI L0 acceptance; an agent receiver cannot substitute for it.
`ACCEPTANCE_VERIFIED` is a handoff result and does not authorise product release.

The CLI can inspect a draft but cannot authenticate receiver JSON. A `check`
result therefore remains pending until the trusted host supplies attributable
acceptance evidence. Advisory content warnings do not establish receiving
acceptance, and existing security or evidence failures cannot be waived here.

## Trends and proposed size calibration

```sh
python3 .ai/runtime/tools/content_metrics.py trends snapshots.json --root .
python3 .ai/runtime/tools/content_metrics.py calibrate samples.json \
  --metric words --root .
python3 tools/generate_content_calibration.py --check
```

Each trend snapshot contains `observed_at`, `semantic_model` and `content_qa`.
Reports must replay against the current registered specification. A comparable
series retains the same contract, kind, specification and context; incompatible
policy versions or contexts require a separate series. The result records
observed word counts, duplicate groups, critical findings and deltas, with exact
source/report hashes. Caller timestamps describe observations and do not prove
trusted execution time or release qualification.

Each calibration sample contains `project_id`, `complexity`, `synthetic`,
`semantic_model` and `content_qa`. At least three distinct projects must cover
simple, medium and complex scenarios for the same kind and policy inheritance.
Context strata remain explicit in the evidence. A range across strata is
descriptive and does not become a quality threshold for each individual stratum.
Only measured modalities may be calibrated; prose cannot establish page counts.

The generated `content/calibration/synthetic-development.json` contains ten
priority-family candidate word envelopes and ten missing-core-to-reference
trend examples derived from the 30 scenarios. Candidates remain proposed and
synthetic-only; they are not automatically applied to policy. Existing page
ranges remain informational pending measured enterprise examples and competent
human acceptance. A short document with all required information must not fail
solely because it falls below an indicative length range.

## Explicit historical migration

```sh
python3 .ai/runtime/tools/content_migrate.py historical.json --root . \
  --contract-id enterprise-architect:4 --artifact-id migrated/adr-1 \
  --source-release 26.10.5 --field-map field-map.json
```

Migration accepts explicit registered contract and instance identifiers and an
optional source-field map. It preserves the historical snapshot and source hash,
records field provenance, resolves the current specification and produces a
review-pending draft. It never guesses a kind from a title, transfers historical
approvals, fabricates missing information or overwrites the historical input.
Unmapped obligations remain unfilled. Existing v3 records remain readable;
new publication writes continue to require the v4 QA bundle described above.

## Expert references and offline readiness

The [default expert library](../using/expert-reference-documents.md) contains
30 supplied English AI-authored proposed examples. Their stable DCS anchors
support structural identification while evidence quality and professional
acceptance remain distinct. [Override precedence](../configuration/expert-document-overrides.md)
is engagement, organisation, user, bundled; invalid selected overrides fail
without fallback and cannot modify normative DCS obligations.

[Offline qualification](../validation/offline-content-qualification.md)
distinguishes the self-contained core profile from full-source evaluation
with digest-pinned optional synthetic data. Missing required data or renderer
dependencies are never PASS. [Optional provider evaluation](../validation/optional-provider-evaluation.md)
is an explicit operator action, tested offline with fake CLIs. It is not a
mandatory dependency and does not establish live provider qualification.


### Semantic families and historical artifact types

Stable role-contract IDs, document-kind IDs and historical artifact types remain
compatible. Authored semantic refinements select shared information obligations
for the actual deliverable. For example, deployment automation requires controlled
targets, verification and recovery, while a feasibility prototype retains its
explicit non-production boundary.

Registered policies use `semantic_foundation_ref` to select the shared family
policy instead of automatically inheriting a historically broad artifact type.
The reference must identify a registered semantic family; an unknown selection
fails explicitly. Policies without this field retain historical inheritance.
This catalog metadata is not a user reference override or an approval mechanism.
Global security, evidence and authority controls, existing domain obligations and
source role gates remain required. All authored corrections remain proposed and
subject to independent review and existing JAI L0 authority.
