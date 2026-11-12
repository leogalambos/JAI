# Proposal production


The `commercial-delivery/1` profile prepares a coherent proposal package for
independent professional review. It reuses the shared expert-reference
resolver, DCS registry, specialist roles and enterprise publication controls.
Preparing a draft does not authorize an offer, contractual commitment or
production deployment.

## Choose the scope and readers

First distinguish a complete supplier bid, a bounded clarification/calculation
and a linked client-draft package. A complete bid follows the
[commercial work-product and review process](../capabilities/commercial-delivery.md#complete-bid-documents-and-readers),
including its protected internal dossier and reproducible estimate, resource and
financial models. The proposal helper prepares eight related client-draft
document kinds; those views alone do not constitute that complete bid:

| Kind | Main audience and purpose |
| --- | --- |
| `client-proposal` | Sponsor and procurement: the integrated commissioning decision. |
| `executive-proposal` | Executive authority: outcomes, alternatives, cost and risk. |
| `technical-proposal` | Architects and engineering: solution boundaries and assurance. |
| `delivery-proposal` | Delivery authority: resources, sequencing and dependencies. |
| `commercial-proposal` | Procurement and finance: fees, assumptions and total cost. |
| `statement-of-work` | Delivery and legal reviewers: scope, acceptance and responsibilities. |
| `rfp-response` | Evaluators: explicit, qualified answers to customer requirements. |
| `proposal-compliance-matrix` | Bid reviewers: coverage, exceptions and evidence status. |

Identify the actual readers and their decision or operational task for every
selected document. The helper's shared audience input does not establish that
each component suits its own readers. Use the dedicated role contracts to
provide the necessary recipient-specific detail and keep all views on the same
baseline. A decision summary links to its detailed evidence; it does not replace
source calculations, an executable delivery plan or required contractual detail.

Two optional offerings have their own boundaries and pricing:
`cybersecurity-transformation-proposal` and
`managed-security-services-proposal`. Selecting one never silently adds its
charges or commitments to the baseline programme.

Select `simple`, `medium` or `complex` from the actual dependencies, risks and
decision structure. Record business context and the intended audience.
Reference selection guides structure and reasoning; customer requirements
and authorized supplier sources establish facts. Missing project facts stay
open. Neither a reference's fictional customer name nor its numbers, test
results, certifications or approvals become evidence for a real proposal.

## Prepare a reviewable draft

The existing commercial CLI accepts a structured proposal authoring input.
The bundled fixtures are synthetic demonstrations, not customer offers:

```bash
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 \
  proposal-plan .ai/runtime/commercial/fixtures/proposal-simple.json
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 \
  proposal-validate .ai/runtime/commercial/fixtures/proposal-simple.json
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 \
  proposal-prepare .ai/runtime/commercial/fixtures/proposal-simple.json \
  --output build/proposal-pilot-draft
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 \
  proposal-validate build/proposal-pilot-draft/proposal-package.json
```

Use a new output directory for each revision. Inspect the generated Markdown,
semantic models and findings together. For real work, supply an authorized
input matching `commercial/schema/proposal-authoring.schema.json`; preserve
source and assumption status rather than copying the synthetic fixture.
Keep confidential inputs and outputs in an authorized private workspace.

The input identifies `package_kind: proposal-authoring-input/1`, source
records, source-linked narrative and assumptions, deliverables, acceptance,
milestones, commercial lines, component claims, RFP responses and separately
priced optional offerings. `selection_context` contains business qualifiers;
`dcs_context` contains registered typed applicability fields. They have
different purposes. Validate a prepared `proposal-package.json` to check the
exact Markdown and semantic-model bytes. After editing a draft, prepare and
review a new revision; free-text edits are not automatically semantically
reconciled or approved.

For a standalone proposal outline, select its registered DCS identity:

```bash
python3 .ai/runtime/tools/content_spec.py outline --root . \
  --artifact-id kind/client-proposal --reference-complexity medium \
  --reference-audience sponsor
```

This explicit DCS selection is not a historical role-contract identity or
permission to act for that role. Existing role bindings retain their IDs.

The [reference resolver](expert-reference-documents.md) supports the existing
`engagement > organisation > user > bundled` precedence. An invalid selected
override fails explicitly. Overrides change examples, never normative DCS,
security rules, commercial authority or human approval.

## Reconcile the package

Check the entire package, not just each document separately:

- Scope, deliverable identifiers, technical commitments and SoW boundaries.
- Person-days multiplied by declared rates, supplier fees, third-party
  estimates, customer internal cost, currency and time horizon.
- Milestones, prerequisite dependencies, responsibilities and acceptance.
- Assumptions, exclusions, risks and unresolved evidence.
- Every applicable RFP requirement, qualified response and evidence status.
- Optional service charges kept separate from baseline programme totals.

Deterministic agreement cannot establish feasibility or professional quality.
Use dedicated bid/proposal, estimation, commercial pricing and supplier deal
specialists. The independent commercial assurance reviewer challenges exact
versions and never edits or approves its own assessed proposal. Keep executive,
technical, commercial, legal/scope and presentation review results distinct.

For a complete bid, reconcile the actual internal models and client documents
against the same version set. The existing `options` and `bid-review` phase
checks use supplied estimate, price and capacity inputs; an authorised
execute-tier operator runs them against the current commercial snapshot.
Resource Manager supplies the period-specific capacity disposition, and
delivery/service owners assess feasibility and accept receiving obligations.
These accountable owners may have authored their plans; independent commercial
assurance remains separate from the assessed authors. Reopen affected evidence,
acceptances and decisions when material inputs change, retaining valid
unaffected work.

`CONSISTENT_DRAFT` and `consistency_pass` describe only the helper's checked
consistency. Prepared content remains `DRAFT_NOT_FOR_SUBMISSION` with
`release_ready: false`. Likewise, governed readiness `ready` does not inspect
every model formula or establish a complete dossier. Actual work products,
professional assessment and reserved human decisions remain necessary.

## Publication and colleague pilot

Drafts remain visibly provisional. Publication handoff uses the existing
canonical commercial snapshot, disclosure policy, JAI lineage and enterprise
projection gates. Missing authority or evidence blocks an authorized client
publication; an authoring JSON cannot manufacture either.

```bash
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 \
  proposal-handoff ./private-proposal-draft/proposal-package.json \
  --kind client-proposal \
  --output ./private-publication-handoff
```

This example requires actual project inputs and the existing publication
prerequisites; it is not an approval command. Follow
[commercial delivery](../capabilities/commercial-delivery.md) for engagement,
specialist and disclosure controls. Evaluate a clearly marked pilot draft
with the [review and release readiness](../operations/validation.md). A pilot
opinion does not authorize issue, signing or production activation.
