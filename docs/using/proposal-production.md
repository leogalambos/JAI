# Proposal production

Owner: JAI maintainers · Last reviewed: 2026-10-20

The `commercial-delivery/1` profile prepares a coherent proposal package for
independent professional review. It reuses the shared expert-reference
resolver, DCS registry, specialist roles and enterprise publication controls.
Preparing a draft does not authorize an offer, contractual commitment or
production deployment.

## Choose the components

The core package has eight related document kinds:

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
with the [colleague pilot rubric](../validation/proposal-pilot.md). A pilot
opinion does not authorize issue, signing or production activation.
