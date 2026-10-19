# Document Content Specifications

Owner: JAI maintainers · Last reviewed: 2026-10-19

The 26.10.6 semantic content foundation and 26.10.7 content QA pilot describe what an output must contain,
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

Ten families have detailed **proposed** specifications: decision paper, ADR,
business case, risk assessment, assurance report, architecture definition, HLD,
operational handover, runbook and test report. Architecture definition describes
architectural context and viewpoints; HLD describes a specific solution design.
Other kinds and mappings provide a traceable foundation, rather than a claim
that every specialist document standard has already been professionally accepted.
SABSA risk treatment remains a subsequent risk-assessment specialisation.

Synthetic reference scenarios cover simple, medium and complex contexts, with
seeded defects and expected observations. Their calibration status is
**synthetic-only**. Passing a structural check establishes catalogue integrity;
it does not establish professional content acceptance. Human approval of the ten
priority standards, real enterprise calibration and a human-approved gold corpus
remain pending. The phase's manual-approval exit condition is therefore open.

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

## Compatibility and subsequent phases

Older unprofiled installations remain readable. When the DCS sidecar profile is
present, `artifacts.py check` also validates its catalogue references and policy
conflicts. Source validation and release qualification run the same structural
lint while retaining all existing checks.

26.10.7 adds content outlines, deterministic semantic validation, immutable
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

## Implementation baseline

This foundation follows the approved plan and binding answers in the source
repository. SHA-256 identifies the exact inputs used; subsequent edits require
a new implementation assessment.

| Input | SHA-256 |
| --- | --- |
| `INBOX/JAI_DCS_implementation_plan.md` | `9a7a7bdefebc60fd9574e3416da24a5a59440ace409711e684b28370fc6fc1ec` |
| `INBOX/JAI_DCS_implementation_plan-answers.md` | `d0c879ca30e920e1ce2b6037a66535e1bec66d24c0bc4cd49272c0220227e7dc` |

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
  --output build/dcs-26.10.7-pilot.json
```

The semantic source records its instance `artifact_id`, explicit role
`contract_id`, registered `document_kind`, `compiled_spec_hash` and typed
context. Required information belongs in `semantic_units`. Claims distinguish
known facts, assumptions and pending knowledge. Known material claims require
versioned evidence with a verified payload hash and explicit freshness dates.

The evaluator applies all 270 mutation recipes to the 30 canonical references
and runs the production validator. Expected rule identifiers are compared with
actual located findings. Reports retain per-case source, specification and
report hashes, seeded critical false negatives and reference false positives.
The initial thresholds are 95 percent critical seeded-defect recall and at
most 10 percent reference false positives. These are synthetic development
thresholds, not enterprise calibration or human professional acceptance.

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
