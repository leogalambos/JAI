# Expert reference editorial review

Owner: JAI maintainers · Last reviewed: 2026-10-20

Expert Reference Library v2.3.0 is a complete library of 135 English Markdown
examples across 45 families and three complexity levels. All bodies have
been revised. Reference IDs, family/complexity slots and stable DCS anchors
remain the same; current integrity hashes identify the new bytes. The
library version is independent of JAI's calendar release numbering.

## Review status and scope

Technical, management and presentation lenses were applied by the **same AI
system**. They are distinct editorial protocols, not three independent
reviewers, separate models or human expert approvals. The supplied editorial
assessment reports a corpus-wide structural scan and selected close reading;
it does not establish substantive professional review of every statement.

All 135 documents contain editorial supplements. The bundled manifest marks
them `tri-lens-ai-review-applied-not-human-approved` with review version
`2.3.0`. This means editorial changes were applied, not that security tests,
financial assurance, a customer pilot, usability testing or human acceptance
were executed. Professional acceptance remains `NOT_APPROVED`.

## What the three lenses address

The following summarizes editorial findings and intended remedies. A remedy
in reference prose is not evidence that the corresponding project control
works or that an independent reviewer accepted it.

| Lens | Editorial issues | Reference changes and remaining duties |
| --- | --- | --- |
| Technical | Generic review instructions, ambiguous simulated results, disconnected scope/cost/trust checks and unclear source/build identity | Contextual verification questions, requested evidence, explicit execution states and cross-artifact acceptance checks. Validate actual systems and claims separately. |
| Management | Conflated direction/spending/release authorities, absent evidence owners, fictional forecasts and incomplete receiving acceptance | Separate decision authority, named ownership duties, stop conditions, financial reconciliation and operational handoff criteria. Obtain actual competent approval. |
| Presentation | Buried exceptions, generic narrative, untested layouts and colour-only status communication | Decision headline, decisive checks, next action, readable hierarchy and text statuses. Exercise renderers and accessibility checks before making visual-quality claims. |

Methodological references inform the questions, not a conformance claim:
architecture-description concepts, secure development, scoped AppSec
verification, build provenance, control assessment, service ownership and
accessible communication. No ISO, NIST, ASVS, SLSA or WCAG attainment follows
from importing or selecting a reference.

## Supplement structure

The existing front matter and stable DCS sections remain authoritative for
structural reference identification. Supplements add:

1. A context-specific decision/evidence matrix: verification object,
   falsifiable question, requested source and required disposition.
2. Technical and management challenges: relevant boundaries, accountable
   roles, material assumptions and conditions for deferral.
3. A reader decision check: headline, decisive issues and next action.
4. Acceptance questions covering source fidelity, cross-artifact consistency,
   independent review and publication quality.

The supplement headings are readable editorial structure, not additional
normative DCS anchors. Selecting a reference or installing an override does
not modify MUST/MUST NOT obligations, signed JAI L0 acts, independent review,
segregation of duties, publication authorization or A–H release gates.

Use the matrix to ask for evidence; do not copy its fictional context,
prices, control conclusions, test results or approval wording as verified
facts. Keep absent execution `NOT_EXECUTED`, unresolved matters `OPEN` or
`PENDING`, and professional approval separate. A recommendation to defer is
not a recorded authority decision.

## Select and inspect a reference

The shared resolver continues to select by family, complexity, explicit
context and intended audience:

```bash
python3 .ai/runtime/tools/expert_references.py inspect --root . \
  --kind decision-paper --complexity medium --audience decision-owner
python3 .ai/runtime/tools/expert_references.py resolve --root . \
  --kind security-control-assessment --complexity complex \
  --audience control-assessor
python3 .ai/runtime/tools/expert_references.py validate --root . --all
```

Use existing registered role contracts or explicit advisory `kind/` selectors
as described in the [authoring guide](../using/expert-reference-documents.md).
Source `dcs-proposed-*` namespaces retain explicit
[registered mappings](../reference/expert-reference-format.md#registered-family-mappings)
and proposed status. The same mappings serve both provider adapters.

Precedence remains `engagement > organisation > user > bundled`. Missing
higher levels continue normally; a selected invalid override fails explicitly
without falling back or merging. See [override paths and restoration](../configuration/expert-document-overrides.md).
An override is authoring data, not a policy amendment or approval.

## Verification and acceptance

Offline validation checks all current document hashes, metadata, unique IDs,
mandatory stable anchors and mapped units. Regression fixtures exercise
override failures, proposal arithmetic and optional-service boundaries,
security/evidence states and compatibility with existing publication.
Structural success does not prove arbitrary prose, financial forecasts,
control effectiveness or expert correctness.

Use the [proposal pilot](proposal-pilot.md) or
[engineering/security rubric](engineering-security-review.md) for optional
competent human evaluation. Record the actual output revision, evidence,
reviewer independence, findings and disposition through existing JAI records.
Never substitute the bundled editorial status for that review.

Reference-specific visual evaluation is distinct from baseline release
renderer gates. Missing optional reference rendering is `NOT_EXECUTED`;
an unavailable mandatory renderer remains a release blocker. No live LLM or
paid provider is required for mandatory
[offline qualification](offline-content-qualification.md).

Public outputs must omit private source paths, confidential review details,
customer identifiers and identifying source-package fingerprints. Preserve
private lineage and source integrity records only in the authorized private
environment; use the current public-synthetic document hashes for bundled
integrity verification.
