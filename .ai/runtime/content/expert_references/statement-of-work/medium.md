---
reference_id: example:statement-of-work:medium
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: statement-of-work
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/statement-of-work
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: MRG-OEI-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Illustrative statement of work — negotiation draft — Order Event Integration

**Client:** Meridian Retail Group · **Reference:** `MRG-OEI-STATEMENT_OF_WORK-01` · **Complexity:** medium · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Architecture Review Board, Finance Partner and Procurement.

<a id="dcs-proposed-statement-of-work.parties_scope"></a>

## Statement of work status, parties and service boundary

**Negotiation draft; not a signed contract.** Client: Meridian Retail Group; proposed supplier: fictional **Northstar Enterprise Delivery Ltd.** Effective date, company registration identifiers, governing law, jurisdiction and signatories are **TO BE AGREED** by authorized Legal and Procurement representatives. Neither this example nor the proposal is an offer acceptance.

**Services:** design, build/integrate, verify and hand over **transactional outbox, managed event broker, independently versioned ERP consumers, dead-letter quarantine and business reconciliation** in accordance with a baseline requirements schedule approved after discovery. In-scope service boundary: commerce outbox, event broker, ERP adapter, market routing policy, reconciliation store, observability; programme objective: make accepted orders visible to ERP within five minutes at p95, with zero unexplained order loss.

**Exclusions:**
- Replacement of the ERP core
- Transformation of downstream logistics vendor platforms
- Country-specific statutory legal opinions
- Perpetual guarantees of processing exactly once at transport level

Order of precedence to be agreed by Legal: executed master services agreement, executed SoW, agreed schedules, signed changes, and technical proposal attachments; no silent elevation of this reference above executed client terms.

<a id="dcs-proposed-statement-of-work.deliverables"></a>

## Deliverables, materials and acceptance criteria

| ID | Deliverable | Evidence-oriented output | Recipient/acceptance |
| --- | --- | --- | --- |
| D-01 | Discovery and requirement baseline | Signed scope, traceable stakeholder decisions | Design acceptance |
| D-02 | Architecture and interfaces | Approved HLD, interface contract, security boundary | Architecture authority review |
| D-03 | Solution implementation | Versioned configuration/code and deployment evidence | Technical verification |
| D-04 | Quality and recovery | Test cases, exceptions, rehearsal records | Independent test review |
| D-05 | Service acceptance | Runbook, monitoring, ownership, training | Receiving service owner sign-off |
| D-06 | Country rollout readiness | Two-market pilot baseline and controlled extension | Country lead acceptance |


For each deliverable, the supplier provides editable source, versioned evidence, document control and an identified recipient. The client reviews within a proposed five business days after formally complete submission; **silence must not constitute acceptance** in this exemplar. Missing evidence, unmatched scope or critical test failure gives the client a reasoned rejection. Re-submission follows documented remediation and retest.

Technical conditions include p95 order-to-ERP availability under 5 minutes; availability target 99.9% monthly; RTO 2 hours / RPO 15 minutes, but whether these become legally binding SLAs must be agreed explicitly; illustrative targets are not contractual warranties.

<a id="dcs-proposed-statement-of-work.responsibilities"></a>

## Client–supplier responsibilities, constraints and access

**Supplier:** delivery management; architectural design; implementation; agreed tests; design and operator documents; defect correction inside accepted scope; proposed risk controls. **Client:** access approvals, data classification, required third-party licences, SMEs, policy/legal interpretation, acceptance decisions and operational staffing. **Joint:** interface definitions, dependency management, incident/change coordination and design sign-off.

- **A1:** Client supplies sample outbox events, ERP non-production interfaces and named market owners by W4.
- **A2:** Each market approves data routing and customer field minimisation before its release.
- **A3:** No fundamental vendor contract restriction prevents the agreed event delivery architecture.

The supplier does not assume authority to approve business risk, override regulatory restrictions, process live customer data without authorization, or change production systems outside signed change controls. Dependencies not met by the client are escalated, with documented time/cost impacts but no unilateral change.

<a id="dcs-proposed-statement-of-work.milestones_acceptance"></a>

## Schedule, checkpoints, acceptance and exit

Illustrative expected duration: **32 weeks** from agreed start following prerequisite completion.

| Window | Work package | Evidence produced / output | Receiving authority |
| --- | --- | --- | --- |
| W1–4 | Baseline, discovery and contracts | Source-to-target maps, market classification and interface contract | Business/ERP Owners |
| W5–10 | Architecture and foundation | Broker, identity boundary, outbox and ADRs | Architecture Authority |
| W11–21 | Delivery wave 1 | Two-market adapter and reconciliation capability | Delivery Director |
| W22–27 | Verification and controlled market extension | Negative routing tests, resilience and performance evidence | QA Lead |
| W28–32 | Rollout and handover | Market adoption, 24×7 rota confirmation, exit checklist | Service Operations Manager |


| Domain | Measure | Acceptance target (proposed) | Evidence expected |
| --- | --- | --- | --- |
| Business outcome | Accepted order visibility | ≤5 minutes p95 | Correlated commerce/broker/ERP timestamps |
| Data integrity | Unexplained missing / duplicated orders | 0 within signed reconciliation window | Idempotency and ledger sample |
| Availability | Monthly service availability | 99.9% target | SLI agreed with service owner |
| Recovery | RTO / RPO | 2 hours / 15 minutes | Replayed checkpoint validation |


Acceptance is evidenced by independently reviewed test observations, specified recovery exercises, documented outstanding exceptions and acceptance by the receiving service owner. **Critical unexecuted or failed tests remain open**. The parties must explicitly agree a stabilization period, support start, final acceptance conditions and any permitted risk waiver mechanism in the executed contract.

<a id="dcs-proposed-statement-of-work.commercial_change"></a>

## Fees, change control and suspension

**Illustrative supplier professional services:** €780,000 from a model of **780 supplier person-days**; other costs (separate third-party €270,000, client internal €200,000) are not payable to the supplier under this proposed SoW. All taxes, expenses, payment timing, acceptance-linked invoicing and indexation require legal/commercial agreement.

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


**Change request:** must identify original baseline, requested change, deliverable deltas, additional/removed days, licensing, dates, privacy/security consequences, new acceptance measures and approvers. No oral or AI-authored change modifies scope or price.

Termination/suspension, intellectual property, liability, data protection, subcontracting, warranties, confidentiality and dispute resolution require review under a negotiated master agreement; this Markdown is **not** legal advice and contains no enforceable limitation of liability.

<a id="dcs-proposed-statement-of-work.legal_reservations"></a>

## Legal, data protection and signature reservations

Data classes: order ID, fulfilment events, pseudonymous customer reference and delivery address. Applicability reservation: GDPR applicability, market-level data routing and cross-border transfers require a documented client privacy decision. Before any real engagement, the client and supplier must identify controller/processor roles, permitted data locations, access permissions, applicable sector commitments, retention and exit arrangements.

Risk register:
| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Duplicate/out-of-order events | Outbox, stable idempotency keys, replay and exception reconciliation | Integration Architect |
| R2 | Incorrect country routing of personal data | Region tagging and negative policy tests | Privacy Lead |
| R3 | Market cutover and shared broker saturation | Two-market canary, back-pressure and capacity stress tests | Operations Manager |


**Execution block:** draft status, no customer procurement approval, no confirmed pricing authority, no actual data-processing authorization and no signature. Signatures must be created only through existing authorized human workflows; an AI-written name or hash is not a signature.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `MRG-OEI-E-SCOPE` (signed requirements), `MRG-OEI-E-COST` (validated rate-card and cost owner), `MRG-OEI-E-SEC` (risk/legal applicability), and `MRG-OEI-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `MRG-OEI`; **document kind:** `statement-of-work`; **scenario:** `medium`.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `MRG-OEI-PROPOSAL-EXAMPLE` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Deliverable acceptance and rejection window | Is this statement supported for `MRG-OEI-PROPOSAL-EXAMPLE` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Client/supplier responsibility split | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Change request and exclusion handling | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — customer commitment integrity

Trace the exact customer-requested outcome to a separately priced deliverable and explicit acceptance test; classify any unsupported requirement as an assumption or clarification. For **statement-of-work**, the reviewer should actively challenge **deliverable acceptance and rejection window** and **client/supplier responsibility split**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — contractual acceptance boundary

Distinguish indicative estimate, binding price, third-party pass-through and client internal cost. Change in scope requires a defined change-order rather than implied free delivery. The accountable party for this illustrative acceptance is **Bid Manager / Commercial Owner**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** deliverable acceptance and rejection window, client/supplier responsibility split, and change request and exclusion handling. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

