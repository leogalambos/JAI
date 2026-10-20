---
reference_id: example:delivery-proposal:medium
schema_version: '1.0.0'
content_revision: 2.1.0
document_kind: delivery-proposal
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/delivery-proposal
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: MRG-OEI-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Programme delivery and governance proposal — Order Event Integration

**Client:** Meridian Retail Group · **Reference:** `MRG-OEI-DELIVERY_PROPOSAL-01` · **Complexity:** medium · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Architecture Review Board, Finance Partner and Procurement.

<a id="dcs-proposed-delivery-proposal.delivery_scope"></a>

## Delivery objective, contractual boundaries and approach

A staged engagement will produce **transactional outbox, managed event broker, independently versioned ERP consumers, dead-letter quarantine and business reconciliation** for the objective **make accepted orders visible to ERP within five minutes at p95, with zero unexplained order loss**. Scope is restricted to commerce outbox, event broker, ERP adapter, market routing policy, reconciliation store, observability; delivery does not imply operational acceptance until proof against agreed business outcomes is submitted.

Delivery style: discovery-led baseline, risk-driven solution increments, gated verification and formal service transfer. Iterative technical demonstrations may occur throughout, but contractual deliverables and acceptance remain explicitly controlled.

<a id="dcs-proposed-delivery-proposal.work_packages"></a>

## Work breakdown and acceptance-ready work products

| ID | Deliverable | Evidence-oriented output | Recipient/acceptance |
| --- | --- | --- | --- |
| D-01 | Discovery and requirement baseline | Signed scope, traceable stakeholder decisions | Design acceptance |
| D-02 | Architecture and interfaces | Approved HLD, interface contract, security boundary | Architecture authority review |
| D-03 | Solution implementation | Versioned configuration/code and deployment evidence | Technical verification |
| D-04 | Quality and recovery | Test cases, exceptions, rehearsal records | Independent test review |
| D-05 | Service acceptance | Runbook, monitoring, ownership, training | Receiving service owner sign-off |
| D-06 | Country rollout readiness | Two-market pilot baseline and controlled extension | Country lead acceptance |


**Out of scope:**
- Replacement of the ERP core
- Transformation of downstream logistics vendor platforms
- Country-specific statutory legal opinions
- Perpetual guarantees of processing exactly once at transport level

Each work package has traceable input requirements, a responsible supplier role, client decision rights, an objectively checkable acceptance condition and a named receiving team. The sponsor cannot waive data-protection or financial-finality obligations merely to recover a missed delivery date.

<a id="dcs-proposed-delivery-proposal.resources_governance"></a>

## Accountability, resource model and governance cadence

Illustrative supplier effort: **780 person-days**, broken down below. The effort calculation is independent of elapsed calendar duration and assumes parallel resources.

| Workstream | Supplier days | Blended rate | Total |
| --- | --- | --- | --- |
| Discovery and source analysis | 90 | €1,000 | €90,000 |
| Architecture and platform | 120 | €1,000 | €120,000 |
| Integration implementation | 360 | €1,000 | €360,000 |
| Testing and migration | 130 | €1,000 | €130,000 |
| Readiness and transfer | 80 | €1,000 | €80,000 |


Client responsibilities: supply SMEs and system access, designate business and risk owners, conduct user acceptance and issue authorized decisions. Supplier responsibilities: project management, design, build, test evidence, defect remediation and handover. Weekly RAID and dependency meeting; monthly/phase steering and independent quality gates. Unapproved change requests cannot be reported as delivered scope.

<a id="dcs-proposed-delivery-proposal.schedule_dependencies"></a>

## Integrated schedule, critical path and milestones

Planning duration **32 weeks**, excluding unapproved dependency slippage.

| Window | Work package | Evidence produced / output | Receiving authority |
| --- | --- | --- | --- |
| W1–4 | Baseline, discovery and contracts | Source-to-target maps, market classification and interface contract | Business/ERP Owners |
| W5–10 | Architecture and foundation | Broker, identity boundary, outbox and ADRs | Architecture Authority |
| W11–21 | Delivery wave 1 | Two-market adapter and reconciliation capability | Delivery Director |
| W22–27 | Verification and controlled market extension | Negative routing tests, resilience and performance evidence | QA Lead |
| W28–32 | Rollout and handover | Market adoption, 24×7 rota confirmation, exit checklist | Service Operations Manager |


Critical path: confirmed requirements and interface rights → design and legal boundary decisions → technical integration → negative/resilience test evidence → operational acceptance. Customer delays require a visible decision: replan scope/cost, pause, or terminate the work package. There is no automatic acceptance or implied acceleration.

<a id="dcs-proposed-delivery-proposal.quality_acceptance"></a>

## Definition of ready, done and receiving acceptance

Acceptance is by objective evidence, not by activity completion.

| Domain | Measure | Acceptance target (proposed) | Evidence expected |
| --- | --- | --- | --- |
| Business outcome | Accepted order visibility | ≤5 minutes p95 | Correlated commerce/broker/ERP timestamps |
| Data integrity | Unexplained missing / duplicated orders | 0 within signed reconciliation window | Idempotency and ledger sample |
| Availability | Monthly service availability | 99.9% target | SLI agreed with service owner |
| Recovery | RTO / RPO | 2 hours / 15 minutes | Replayed checkpoint validation |


A deliverable is **Ready for Review** when its DCS units and references are complete; it is **Accepted** only following recorded client authority, verified inputs, passed relevant tests and properly disposed exceptions. Maintain a defect register including severity, correction owner and retest. Do not mark blocked tests PASS.

<a id="dcs-proposed-delivery-proposal.transition_controls"></a>

## Change, risk, recovery and transfer

| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Duplicate/out-of-order events | Outbox, stable idempotency keys, replay and exception reconciliation | Integration Architect |
| R2 | Incorrect country routing of personal data | Region tagging and negative policy tests | Privacy Lead |
| R3 | Market cutover and shared broker saturation | Two-market canary, back-pressure and capacity stress tests | Operations Manager |


After each tranche, issue evidence-linked checkpoint and next-stage permission. Transition includes configuration, editable designs, source repository, runbooks, alert ownership, supplier terms, backup/restore evidence and knowledge transfer. At formal handover, the receiving service owner must accept or reject outstanding conditions.

- **A1:** Client supplies sample outbox events, ERP non-production interfaces and named market owners by W4.
- **A2:** Each market approves data routing and customer field minimisation before its release.
- **A3:** No fundamental vendor contract restriction prevents the agreed event delivery architecture.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `MRG-OEI-E-SCOPE` (signed requirements), `MRG-OEI-E-COST` (validated rate-card and cost owner), `MRG-OEI-E-SEC` (risk/legal applicability), and `MRG-OEI-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `MRG-OEI`; **document kind:** `delivery-proposal`; **scenario:** `medium`.
