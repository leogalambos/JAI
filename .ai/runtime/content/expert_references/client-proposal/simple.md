---
reference_id: example:client-proposal:simple
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: client-proposal
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/client-proposal
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: HFS-FAR-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Integrated client solution proposal — Field Appointment Reliability

**Client:** Harborline Field Services · **Reference:** `HFS-FAR-CLIENT_PROPOSAL-01` · **Complexity:** simple · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Operations Director and Procurement Lead.

<a id="dcs-proposed-client-proposal.customer_need"></a>

## Business need, constraints and agreed discovery boundary

Harborline Field Services is presented in this fictional engagement as a regional field-service provider operating one UK business unit. The business challenge is shared scheduling spreadsheet and single legacy dispatch application; late confirmations and duplicated technician assignments. The intended outcome is to **reduce appointment rework from an illustrative 2.3% to 0.5% within two quarters**. Size and variability: 240 technicians, approximately 2,100 appointments each week. The first step is a validated baseline workshop, not a commitment that these figures are true.

The decision requested is to proceed to a scoped, gated implementation of **Managed Scheduling and Dispatch**. The project must explicitly demonstrate how the result changes the business outcome and identify accountable owners for requirements, information protection, and acceptance.

**Success is not a visually persuasive proposal alone:** the recommendation must be rejected if its evidence cannot support feasibility, a non-negotiable legal requirement, or the stated cost envelope.

<a id="dcs-proposed-client-proposal.proposed_solution"></a>

## Proposed solution and reasons for this direction

We propose **managed scheduling SaaS with a one-way dispatch synchronisation, central identity and auditable exception reconciliation**. The primary boundaries are Booking SaaS, corporate SSO, dispatch connector, durable notification queue, daily reconciliation dashboard. Design rationale: The proposition deliberately leaves the authoritative booking write in the SaaS platform; notifications and dispatch updates cannot become competing systems of record.

Alternatives evaluated are (A) retain and remediate the baseline, (B) adopt the proposed gated architecture, and (C) procure or build a less staged alternative. A is fastest to maintain temporarily but leaves the documented structural failure; C may shorten a feature delivery path yet increases cutover, operational or control uncertainty. The preferred B is contingent on measured requirements and a rehearsed operational pathway.

**Technical commitments are conditional.** Target characteristics: p95 booking response below 2 seconds; monthly availability target 99.5%; RTO 8 hours and RPO 24 hours. Controls: SSO, minimum necessary dispatcher roles, encrypted transport, limited appointment data, no shared operations credentials and human authorization for bulk changes. Approval of the architecture direction must not be interpreted as acceptance of production readiness.

<a id="dcs-proposed-client-proposal.scope_deliverables"></a>

## Scope of work, outputs and acceptance

The supplier proposes to design, configure, integrate, verify and hand over the in-scope capability; the client remains accountable for access, data classification and the business decision to accept it. The deliverables are as follows:

| ID | Deliverable | Evidence-oriented output | Recipient/acceptance |
| --- | --- | --- | --- |
| D-01 | Discovery and requirement baseline | Signed scope, traceable stakeholder decisions | Design acceptance |
| D-02 | Architecture and interfaces | Approved HLD, interface contract, security boundary | Architecture authority review |
| D-03 | Solution implementation | Versioned configuration/code and deployment evidence | Technical verification |
| D-04 | Quality and recovery | Test cases, exceptions, rehearsal records | Independent test review |
| D-05 | Service acceptance | Runbook, monitoring, ownership, training | Receiving service owner sign-off |


**Explicit exclusions:**
- Beside-the-scenes SaaS supplier platform changes
- Historical data cleansing beyond agreed fields
- 24×7 support subscription unless separately contracted
- Production endpoint credentials in any proposal deliverable

In-scope deliverables are accepted only against their named criteria with an actual receiving role and submitted evidence; missing evidence is **open**, not implicitly accepted. Specifications, commercial schedules and the statement of work must have the same scope boundary.

<a id="dcs-proposed-client-proposal.delivery_plan"></a>

## Implementation sequence, responsibilities and key dependencies

The illustrative delivery window is **10 weeks**, conditional on timely client prerequisites.

| Window | Work package | Evidence produced / output | Receiving authority |
| --- | --- | --- | --- |
| W1–2 | Discovery and baseline | Signed requirements, data inventory, measured baseline | Operations Sponsor |
| W3–6 | Configure and integrate | Configured SaaS tenant, SSO, tested dispatch connector | Solution Lead |
| W7–8 | Verify and rehearse | Acceptance tests, restore rehearsal, defect disposition | Test Lead |
| W9 | Limited operational pilot | Pilot reconciliation and adoption evidence | Service Owner |
| W10 | Handover and acceptance | Runbook, training, acceptance record | Service Owner |


Client prerequisites:
- **A1:** Client supplies authorized SaaS tenancy, identity integration owner and test access by W2.
- **A2:** Client makes available 2 dispatch SMEs and a decision owner within 2 working days of a material question.
- **A3:** No unexpected data transfer or licensing restriction invalidates the proposed SaaS solution.

The project manager maintains an integrated RAID log and change control. A dependency failure triggers a recorded impact assessment; a revised timeline or scope requires explicit approval rather than optimistic redrafting.

<a id="dcs-proposed-client-proposal.commercial_overview"></a>

## Commercial structure, estimate and material risks

Supplier professional services are a fixed-fee illustrative quote of £84,000 excluding taxes; estimated SaaS licensing £42,000 over 36 months and £14,000 customer internal transition are non-supplier items. The three-year indicative programme cost is £140,000, not a supplier invoice. This is an indicative, non-binding price basis, excluding applicable taxes and subject to procurement and legal approval.

| Workstream | Model basis | Illustrative cost |
| --- | --- | --- |
| Discovery and design | 15 days × £700/day | £10,500 |
| Configuration and workflow | 55 days × £700/day | £38,500 |
| Connector and assurance | 32 days × £700/day | £22,400 |
| Testing and handover | 18 days × £700/day | £12,600 |
| Supplier professional services total | Calculated from person-days | £84,000 |
| Indicative licences / platform (36 months) | Separate third-party estimate | £42,000 |
| Client internal effort / transition | Not part of supplier invoice | £14,000 |
| Indicative programme envelope | Services + third-party + internal | £140,000 |


Material exposures:
| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Duplicate webhook updates | Idempotency by booking key; reconciliation | Application Lead |
| R2 | SaaS outage and export limitations | Daily verified export and offline dispatch procedure | Service Owner |
| R3 | Incomplete frontline adoption | Supervisor-assisted pilot and training | Business Sponsor |


Any additional work, supplier subscriptions or optional managed services must be distinctly marked, priced, and excluded from the base total unless a signed change order says otherwise.

<a id="dcs-proposed-client-proposal.decision_request"></a>

## Recommendation, conditions to proceed and next steps

**Recommendation:** approve a limited mobilisation or negotiation mandate for the selected approach, subject to verified requirements, commercial confirmation, security applicability and named receiving owners. Do not authorize broad production rollout from this proposal alone.

| Domain | Measure | Acceptance target (proposed) | Evidence expected |
| --- | --- | --- | --- |
| Business outcome | Appointment rework | Baseline 2.3%; target ≤0.5% | Weekly reconciled dispatch report |
| Response | p95 booking response | <2 seconds | Measured synthetic and pilot traces |
| Integrity | Unexplained duplicate appointments | 0 during accepted pilot | Booking vs dispatch reconciliation |
| Recovery | RTO / RPO | 8 hours / 24 hours | Observed restore rehearsal |


Before signing: validate the baseline; reconcile service scope to the SoW; confirm estimates against a supplier rate card; agree legal and data responsibilities; rehearse material recovery; and obtain independent commercial and security review. The decision record should state APPROVE WITH CONDITIONS / DEFER / REJECT, authority, evidence snapshot and expiry. A failed non-negotiable requirement results in DEFER or redesign, not a weighted-score waiver.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `HFS-FAR-E-SCOPE` (signed requirements), `HFS-FAR-E-COST` (validated rate-card and cost owner), `HFS-FAR-E-SEC` (risk/legal applicability), and `HFS-FAR-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `HFS-FAR`; **document kind:** `client-proposal`; **scenario:** `simple`.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `HFS-FAR-PROPOSAL-EXAMPLE` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Client-requested service outcome | Is this statement supported for `HFS-FAR-PROPOSAL-EXAMPLE` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Deliverable and acceptance reference | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Commercial basis, validity and exclusions | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — customer commitment integrity

Trace the exact customer-requested outcome to a separately priced deliverable and explicit acceptance test; classify any unsupported requirement as an assumption or clarification. For **client-proposal**, the reviewer should actively challenge **client-requested service outcome** and **deliverable and acceptance reference**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — contractual acceptance boundary

Distinguish indicative estimate, binding price, third-party pass-through and client internal cost. Change in scope requires a defined change-order rather than implied free delivery. The accountable party for this illustrative acceptance is **Bid Manager / Commercial Owner**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** client-requested service outcome, deliverable and acceptance reference, and commercial basis, validity and exclusions. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

