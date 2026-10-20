---
reference_id: example:delivery-proposal:complex
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: delivery-proposal
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/delivery-proposal
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: OPG-RSM-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Programme delivery and governance proposal — Regulated Settlement Modernisation

**Client:** Orion Payments Group · **Reference:** `OPG-RSM-DELIVERY_PROPOSAL-01` · **Complexity:** complex · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Group Investment Committee, Payments Architecture Board, Risk and Legal Authorities.

<a id="dcs-proposed-delivery-proposal.delivery_scope"></a>

## Delivery objective, contractual boundaries and approach

A staged engagement will produce **regional phased settlement replacement, jurisdiction policy gateway, append-only instruction journal, separately reconciled parallel ledger and strictly controlled recovery** for the objective **maintain traceable settlement instruction lineage and timely cut-off processing with zero unexplained ledger imbalance**. Scope is restricted to channel gateway, jurisdiction policy decision, durable instruction journal, settlement orchestrator, regional connector, parallel ledger, evidence store, three independent failure domains; delivery does not imply operational acceptance until proof against agreed business outcomes is submitted.

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
| D-06 | Jurisdiction control evidence | Entity applicability and legal exception decisions | Legal/Risk acceptance |
| D-07 | Dual-run ledger exit | Per-cutoff reconciliations and signed finality | Treasury acceptance |


**Out of scope:**
- Guarantees about requirements in jurisdictions not validated by counsel
- Automated reversal of already-final settlements
- Unrestricted cross-border failover or replication
- External financial system modifications without signed interfaces
- Customer regulatory approvals or legal opinions

Each work package has traceable input requirements, a responsible supplier role, client decision rights, an objectively checkable acceptance condition and a named receiving team. The sponsor cannot waive data-protection or financial-finality obligations merely to recover a missed delivery date.

<a id="dcs-proposed-delivery-proposal.resources_governance"></a>

## Accountability, resource model and governance cadence

Illustrative supplier effort: **3000 person-days**, broken down below. The effort calculation is independent of elapsed calendar duration and assumes parallel resources.

| Workstream | Supplier days | Blended rate | Total |
| --- | --- | --- | --- |
| Regulatory and business discovery | 300 | €1,500 | €450,000 |
| Architecture, controls and assurance | 550 | €1,500 | €825,000 |
| Settlement platform and journal integration | 900 | €1,500 | €1,350,000 |
| Regional connectors and wave migration | 500 | €1,500 | €750,000 |
| Resilience, security and acceptance testing | 450 | €1,500 | €675,000 |
| Transition and operational transfer | 300 | €1,500 | €450,000 |


Client responsibilities: supply SMEs and system access, designate business and risk owners, conduct user acceptance and issue authorized decisions. Supplier responsibilities: project management, design, build, test evidence, defect remediation and handover. Weekly RAID and dependency meeting; monthly/phase steering and independent quality gates. Unapproved change requests cannot be reported as delivered scope.

<a id="dcs-proposed-delivery-proposal.schedule_dependencies"></a>

## Integrated schedule, critical path and milestones

Planning duration **18 months**, excluding unapproved dependency slippage.

| Window | Work package | Evidence produced / output | Receiving authority |
| --- | --- | --- | --- |
| M1–3 | Jurisdiction discovery and programme controls | Entity-by-entity applicability, service architecture baseline, dependency register | Executive/Legal/Risk |
| M4–6 | Target architecture and control design | Decision papers, typed flow model, dual-ledger design, approved ADR/HLD | Architecture Board |
| M7–10 | Core build and evidence instrumentation | Policy gateway, journal, reconciliation, resilience test plans | Delivery Director |
| M11–13 | First jurisdiction-controlled wave | Regulator-ready evidence package, parallel-run and cut-off rehearsals | Payments Operations |
| M14–17 | Remaining phased waves | Dual-control migration decisions, jurisdiction-specific acceptance | Local Legal Entity Owners |
| M18 | Operational takeover and governance close | Service owner acceptance, tested recovery, retention and decommission controls | Group Operations/Risk |


Critical path: confirmed requirements and interface rights → design and legal boundary decisions → technical integration → negative/resilience test evidence → operational acceptance. Customer delays require a visible decision: replan scope/cost, pause, or terminate the work package. There is no automatic acceptance or implied acceleration.

<a id="dcs-proposed-delivery-proposal.quality_acceptance"></a>

## Definition of ready, done and receiving acceptance

Acceptance is by objective evidence, not by activity completion.

| Domain | Measure | Acceptance target (proposed) | Evidence expected |
| --- | --- | --- | --- |
| Business outcome | Unexplained ledger imbalance | 0 at authorised settlement finality checkpoints | Independently reconciled dual ledger |
| Processing | Acknowledgement latency | <450ms p95 excluding external networks | Measured agreed test population |
| Service | Critical monthly availability | 99.95% target | Per-region/cutoff business SLI |
| Recovery | RTO / RPO | 30 minutes / 5 minutes | Observed multi-site rehearsal |
| Jurisdiction | Forbidden routes | 0 accepted | Negative-case policy proof |


A deliverable is **Ready for Review** when its DCS units and references are complete; it is **Accepted** only following recorded client authority, verified inputs, passed relevant tests and properly disposed exceptions. Maintain a defect register including severity, correction owner and retest. Do not mark blocked tests PASS.

<a id="dcs-proposed-delivery-proposal.transition_controls"></a>

## Change, risk, recovery and transfer

| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Settlement-finality mismatch or irreversibility | Parallel ledger and dual-control compensating workflow | Treasury Control Owner |
| R2 | Cross-border processing outside authorized legal scope | Per-entity jurisdiction rules and independent privacy/legal approval | Group Compliance |
| R3 | Correlated regional or identity-plane outage | Failure-domain separation, cut-off-safe contingency | Resilience Architect |
| R4 | Unrecoverable reconciliation evidence | Append-only signed checkpoints and independently tested evidence chain | Assurance Lead |


After each tranche, issue evidence-linked checkpoint and next-stage permission. Transition includes configuration, editable designs, source repository, runbooks, alert ownership, supplier terms, backup/restore evidence and knowledge transfer. At formal handover, the receiving service owner must accept or reject outstanding conditions.

- **A1:** Legal entity owners determine applicable financial, data and outsourcing obligations before target design is frozen.
- **A2:** The client provides settlement message specifications, test ledgers, HSM/PKI policies and independent treasury sign-off authority.
- **A3:** Regional rollout is conditioned on dual-run evidence; unresolved cut-off reconciliation prevents release.
- **A4:** External clearing-house simulation and settlement counterparty test rights are obtained before resilience rehearsal.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `OPG-RSM-E-SCOPE` (signed requirements), `OPG-RSM-E-COST` (validated rate-card and cost owner), `OPG-RSM-E-SEC` (risk/legal applicability), and `OPG-RSM-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `OPG-RSM`; **document kind:** `delivery-proposal`; **scenario:** `complex`.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `OPG-RSM-PROPOSAL-EXAMPLE` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Work package / staffing assumptions | Is this statement supported for `OPG-RSM-PROPOSAL-EXAMPLE` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Milestone predecessor and client duty | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Exit/acceptance evidence | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — customer commitment integrity

Trace the exact customer-requested outcome to a separately priced deliverable and explicit acceptance test; classify any unsupported requirement as an assumption or clarification. For **delivery-proposal**, the reviewer should actively challenge **work package / staffing assumptions** and **milestone predecessor and client duty**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — contractual acceptance boundary

Distinguish indicative estimate, binding price, third-party pass-through and client internal cost. Change in scope requires a defined change-order rather than implied free delivery. The accountable party for this illustrative acceptance is **Bid Manager / Commercial Owner**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** work package / staffing assumptions, milestone predecessor and client duty, and exit/acceptance evidence. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

