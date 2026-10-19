# Document Content Specifications

Owner: JAI maintainers · Last reviewed: 2026-10-19

The 26.10.6 semantic content foundation describes what an output must contain,
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

26.10.7 introduces authoring/content QA enforcement, semantic result reports and
projection/publication integration. These are not implemented or claimed by the
26.10.6 foundation. Existing publication and visual QA remain separate controls;
a successful render never constitutes content approval.

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
