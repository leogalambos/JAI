---
reference_id: example:client-proposal:medium
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: client-proposal
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/client-proposal
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: MRG-OEI-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Integrated client solution proposal — Order Event Integration

**Client:** Meridian Retail Group · **Reference:** `MRG-OEI-CLIENT_PROPOSAL-01` · **Complexity:** medium · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Architecture Review Board, Finance Partner and Procurement.

<a id="dcs-proposed-client-proposal.customer_need"></a>

## Business need, constraints and agreed discovery boundary

Meridian Retail Group is presented in this fictional engagement as a multi-market European retailer integrating commerce and ERP platforms. The business challenge is nightly ERP batch exports and fragile point-to-point integration with delayed order promise updates. The intended outcome is to **make accepted orders visible to ERP within five minutes at p95, with zero unexplained order loss**. Size and variability: 12 European markets, peak 180,000 orders/day; first rollout covers two markets. The first step is a validated baseline workshop, not a commitment that these figures are true.

The decision requested is to proceed to a scoped, gated implementation of **European Commerce-to-ERP Event Backbone**. The project must explicitly demonstrate how the result changes the business outcome and identify accountable owners for requirements, information protection, and acceptance.

**Success is not a visually persuasive proposal alone:** the recommendation must be rejected if its evidence cannot support feasibility, a non-negotiable legal requirement, or the stated cost envelope.

<a id="dcs-proposed-client-proposal.proposed_solution"></a>

## Proposed solution and reasons for this direction

We propose **transactional outbox, managed event broker, independently versioned ERP consumers, dead-letter quarantine and business reconciliation**. The primary boundaries are commerce outbox, event broker, ERP adapter, market routing policy, reconciliation store, observability. Design rationale: The managed broker is not the system of record; order state remains authoritative in commerce/ERP with reconciliation establishing business processing success.

Alternatives evaluated are (A) retain and remediate the baseline, (B) adopt the proposed gated architecture, and (C) procure or build a less staged alternative. A is fastest to maintain temporarily but leaves the documented structural failure; C may shorten a feature delivery path yet increases cutover, operational or control uncertainty. The preferred B is contingent on measured requirements and a rehearsed operational pathway.

**Technical commitments are conditional.** Target characteristics: p95 order-to-ERP availability under 5 minutes; availability target 99.9% monthly; RTO 2 hours / RPO 15 minutes. Controls: Scoped producer and consumer identities, tenant/market segregation, encryption, immutable correlation tracing and client-owned data retention rules. Approval of the architecture direction must not be interpreted as acceptance of production readiness.

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
| D-06 | Country rollout readiness | Two-market pilot baseline and controlled extension | Country lead acceptance |


**Explicit exclusions:**
- Replacement of the ERP core
- Transformation of downstream logistics vendor platforms
- Country-specific statutory legal opinions
- Perpetual guarantees of processing exactly once at transport level

In-scope deliverables are accepted only against their named criteria with an actual receiving role and submitted evidence; missing evidence is **open**, not implicitly accepted. Specifications, commercial schedules and the statement of work must have the same scope boundary.

<a id="dcs-proposed-client-proposal.delivery_plan"></a>

## Implementation sequence, responsibilities and key dependencies

The illustrative delivery window is **32 weeks**, conditional on timely client prerequisites.

| Window | Work package | Evidence produced / output | Receiving authority |
| --- | --- | --- | --- |
| W1–4 | Baseline, discovery and contracts | Source-to-target maps, market classification and interface contract | Business/ERP Owners |
| W5–10 | Architecture and foundation | Broker, identity boundary, outbox and ADRs | Architecture Authority |
| W11–21 | Delivery wave 1 | Two-market adapter and reconciliation capability | Delivery Director |
| W22–27 | Verification and controlled market extension | Negative routing tests, resilience and performance evidence | QA Lead |
| W28–32 | Rollout and handover | Market adoption, 24×7 rota confirmation, exit checklist | Service Operations Manager |


Client prerequisites:
- **A1:** Client supplies sample outbox events, ERP non-production interfaces and named market owners by W4.
- **A2:** Each market approves data routing and customer field minimisation before its release.
- **A3:** No fundamental vendor contract restriction prevents the agreed event delivery architecture.

The project manager maintains an integrated RAID log and change control. A dependency failure triggers a recorded impact assessment; a revised timeline or scope requires explicit approval rather than optimistic redrafting.

<a id="dcs-proposed-client-proposal.commercial_overview"></a>

## Commercial structure, estimate and material risks

Supplier delivery services €780,000 (780 person-days at illustrative blended €1,000/day). Separately estimated managed platform/subscriptions €270,000 over three years and client internal transition €200,000 yield an indicative three-year programme envelope of €1,250,000. This is an indicative, non-binding price basis, excluding applicable taxes and subject to procurement and legal approval.

| Workstream | Model basis | Illustrative cost |
| --- | --- | --- |
| Discovery and source analysis | 90 days × €1,000/day | €90,000 |
| Architecture and platform | 120 days × €1,000/day | €120,000 |
| Integration implementation | 360 days × €1,000/day | €360,000 |
| Testing and migration | 130 days × €1,000/day | €130,000 |
| Readiness and transfer | 80 days × €1,000/day | €80,000 |
| Supplier professional services total | Calculated from person-days | €780,000 |
| Indicative licences / platform (36 months) | Separate third-party estimate | €270,000 |
| Client internal effort / transition | Not part of supplier invoice | €200,000 |
| Indicative programme envelope | Services + third-party + internal | €1,250,000 |


Material exposures:
| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Duplicate/out-of-order events | Outbox, stable idempotency keys, replay and exception reconciliation | Integration Architect |
| R2 | Incorrect country routing of personal data | Region tagging and negative policy tests | Privacy Lead |
| R3 | Market cutover and shared broker saturation | Two-market canary, back-pressure and capacity stress tests | Operations Manager |


Any additional work, supplier subscriptions or optional managed services must be distinctly marked, priced, and excluded from the base total unless a signed change order says otherwise.

<a id="dcs-proposed-client-proposal.decision_request"></a>

## Recommendation, conditions to proceed and next steps

**Recommendation:** approve a limited mobilisation or negotiation mandate for the selected approach, subject to verified requirements, commercial confirmation, security applicability and named receiving owners. Do not authorize broad production rollout from this proposal alone.

| Domain | Measure | Acceptance target (proposed) | Evidence expected |
| --- | --- | --- | --- |
| Business outcome | Accepted order visibility | ≤5 minutes p95 | Correlated commerce/broker/ERP timestamps |
| Data integrity | Unexplained missing / duplicated orders | 0 within signed reconciliation window | Idempotency and ledger sample |
| Availability | Monthly service availability | 99.9% target | SLI agreed with service owner |
| Recovery | RTO / RPO | 2 hours / 15 minutes | Replayed checkpoint validation |


Before signing: validate the baseline; reconcile service scope to the SoW; confirm estimates against a supplier rate card; agree legal and data responsibilities; rehearse material recovery; and obtain independent commercial and security review. The decision record should state APPROVE WITH CONDITIONS / DEFER / REJECT, authority, evidence snapshot and expiry. A failed non-negotiable requirement results in DEFER or redesign, not a weighted-score waiver.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `MRG-OEI-E-SCOPE` (signed requirements), `MRG-OEI-E-COST` (validated rate-card and cost owner), `MRG-OEI-E-SEC` (risk/legal applicability), and `MRG-OEI-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `MRG-OEI`; **document kind:** `client-proposal`; **scenario:** `medium`.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `MRG-OEI-PROPOSAL-EXAMPLE` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Client-requested service outcome | Is this statement supported for `MRG-OEI-PROPOSAL-EXAMPLE` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
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

