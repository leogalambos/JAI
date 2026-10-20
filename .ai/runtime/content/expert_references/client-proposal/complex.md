---
reference_id: example:client-proposal:complex
schema_version: '1.0.0'
content_revision: 2.1.0
document_kind: client-proposal
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/client-proposal
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: OPG-RSM-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Integrated client solution proposal — Regulated Settlement Modernisation

**Client:** Orion Payments Group · **Reference:** `OPG-RSM-CLIENT_PROPOSAL-01` · **Complexity:** complex · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Group Investment Committee, Payments Architecture Board, Risk and Legal Authorities.

<a id="dcs-proposed-client-proposal.customer_need"></a>

## Business need, constraints and agreed discovery boundary

Orion Payments Group is presented in this fictional engagement as a regulated payment-services group operating settlement flows across multiple jurisdictions. The business challenge is regional legacy settlement engines, separate ledgers and manual end-of-day reconciliations with critical dependency concentration. The intended outcome is to **maintain traceable settlement instruction lineage and timely cut-off processing with zero unexplained ledger imbalance**. Size and variability: 14 jurisdictions; synthetic planning assumption 2.4 million instructions/day; multiple intraday cut-offs. The first step is a validated baseline workshop, not a commitment that these figures are true.

The decision requested is to proceed to a scoped, gated implementation of **Multi-Jurisdiction Settlement Control and Resilience**. The project must explicitly demonstrate how the result changes the business outcome and identify accountable owners for requirements, information protection, and acceptance.

**Success is not a visually persuasive proposal alone:** the recommendation must be rejected if its evidence cannot support feasibility, a non-negotiable legal requirement, or the stated cost envelope.

<a id="dcs-proposed-client-proposal.proposed_solution"></a>

## Proposed solution and reasons for this direction

We propose **regional phased settlement replacement, jurisdiction policy gateway, append-only instruction journal, separately reconciled parallel ledger and strictly controlled recovery**. The primary boundaries are channel gateway, jurisdiction policy decision, durable instruction journal, settlement orchestrator, regional connector, parallel ledger, evidence store, three independent failure domains. Design rationale: Settlement finality is a business/legal state rather than an API response; an apparently successful technical acknowledgement cannot replace independently reconciled evidence of finality.

Alternatives evaluated are (A) retain and remediate the baseline, (B) adopt the proposed gated architecture, and (C) procure or build a less staged alternative. A is fastest to maintain temporarily but leaves the documented structural failure; C may shorten a feature delivery path yet increases cutover, operational or control uncertainty. The preferred B is contingent on measured requirements and a rehearsed operational pathway.

**Technical commitments are conditional.** Target characteristics: 99.95% monthly availability for critical processing; p95 acknowledgement under 450 ms excluding third-party network; RTO 30 minutes / RPO 5 minutes. Controls: Jurisdiction-aware processing policy, dual authorization for settlement-affecting operations, segregated privileged identities, HSM/key ownership, control evidence at every irrevocable state boundary and restricted cross-border transfers. Approval of the architecture direction must not be interpreted as acceptance of production readiness.

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
| D-06 | Jurisdiction control evidence | Entity applicability and legal exception decisions | Legal/Risk acceptance |
| D-07 | Dual-run ledger exit | Per-cutoff reconciliations and signed finality | Treasury acceptance |


**Explicit exclusions:**
- Guarantees about requirements in jurisdictions not validated by counsel
- Automated reversal of already-final settlements
- Unrestricted cross-border failover or replication
- External financial system modifications without signed interfaces
- Customer regulatory approvals or legal opinions

In-scope deliverables are accepted only against their named criteria with an actual receiving role and submitted evidence; missing evidence is **open**, not implicitly accepted. Specifications, commercial schedules and the statement of work must have the same scope boundary.

<a id="dcs-proposed-client-proposal.delivery_plan"></a>

## Implementation sequence, responsibilities and key dependencies

The illustrative delivery window is **18 months**, conditional on timely client prerequisites.

| Window | Work package | Evidence produced / output | Receiving authority |
| --- | --- | --- | --- |
| M1–3 | Jurisdiction discovery and programme controls | Entity-by-entity applicability, service architecture baseline, dependency register | Executive/Legal/Risk |
| M4–6 | Target architecture and control design | Decision papers, typed flow model, dual-ledger design, approved ADR/HLD | Architecture Board |
| M7–10 | Core build and evidence instrumentation | Policy gateway, journal, reconciliation, resilience test plans | Delivery Director |
| M11–13 | First jurisdiction-controlled wave | Regulator-ready evidence package, parallel-run and cut-off rehearsals | Payments Operations |
| M14–17 | Remaining phased waves | Dual-control migration decisions, jurisdiction-specific acceptance | Local Legal Entity Owners |
| M18 | Operational takeover and governance close | Service owner acceptance, tested recovery, retention and decommission controls | Group Operations/Risk |


Client prerequisites:
- **A1:** Legal entity owners determine applicable financial, data and outsourcing obligations before target design is frozen.
- **A2:** The client provides settlement message specifications, test ledgers, HSM/PKI policies and independent treasury sign-off authority.
- **A3:** Regional rollout is conditioned on dual-run evidence; unresolved cut-off reconciliation prevents release.
- **A4:** External clearing-house simulation and settlement counterparty test rights are obtained before resilience rehearsal.

The project manager maintains an integrated RAID log and change control. A dependency failure triggers a recorded impact assessment; a revised timeline or scope requires explicit approval rather than optimistic redrafting.

<a id="dcs-proposed-client-proposal.commercial_overview"></a>

## Commercial structure, estimate and material risks

Indicative capped programme envelope €6,800,000 over three years: €4,500,000 supplier professional services (3,000 person-days at model blended €1,500/day), €1,500,000 assumed tooling/infrastructure and €800,000 client transition/operations effort. These are planning assumptions, not a firm fixed-price commitment. This is an indicative, non-binding price basis, excluding applicable taxes and subject to procurement and legal approval.

| Workstream | Model basis | Illustrative cost |
| --- | --- | --- |
| Regulatory and business discovery | 300 days × €1,500/day | €450,000 |
| Architecture, controls and assurance | 550 days × €1,500/day | €825,000 |
| Settlement platform and journal integration | 900 days × €1,500/day | €1,350,000 |
| Regional connectors and wave migration | 500 days × €1,500/day | €750,000 |
| Resilience, security and acceptance testing | 450 days × €1,500/day | €675,000 |
| Transition and operational transfer | 300 days × €1,500/day | €450,000 |
| Supplier professional services total | Calculated from person-days | €4,500,000 |
| Indicative licences / platform (36 months) | Separate third-party estimate | €1,500,000 |
| Client internal effort / transition | Not part of supplier invoice | €800,000 |
| Indicative programme envelope | Services + third-party + internal | €6,800,000 |


Material exposures:
| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Settlement-finality mismatch or irreversibility | Parallel ledger and dual-control compensating workflow | Treasury Control Owner |
| R2 | Cross-border processing outside authorized legal scope | Per-entity jurisdiction rules and independent privacy/legal approval | Group Compliance |
| R3 | Correlated regional or identity-plane outage | Failure-domain separation, cut-off-safe contingency | Resilience Architect |
| R4 | Unrecoverable reconciliation evidence | Append-only signed checkpoints and independently tested evidence chain | Assurance Lead |


Any additional work, supplier subscriptions or optional managed services must be distinctly marked, priced, and excluded from the base total unless a signed change order says otherwise.

<a id="dcs-proposed-client-proposal.decision_request"></a>

## Recommendation, conditions to proceed and next steps

**Recommendation:** approve a limited mobilisation or negotiation mandate for the selected approach, subject to verified requirements, commercial confirmation, security applicability and named receiving owners. Do not authorize broad production rollout from this proposal alone.

| Domain | Measure | Acceptance target (proposed) | Evidence expected |
| --- | --- | --- | --- |
| Business outcome | Unexplained ledger imbalance | 0 at authorised settlement finality checkpoints | Independently reconciled dual ledger |
| Processing | Acknowledgement latency | <450ms p95 excluding external networks | Measured agreed test population |
| Service | Critical monthly availability | 99.95% target | Per-region/cutoff business SLI |
| Recovery | RTO / RPO | 30 minutes / 5 minutes | Observed multi-site rehearsal |
| Jurisdiction | Forbidden routes | 0 accepted | Negative-case policy proof |


Before signing: validate the baseline; reconcile service scope to the SoW; confirm estimates against a supplier rate card; agree legal and data responsibilities; rehearse material recovery; and obtain independent commercial and security review. The decision record should state APPROVE WITH CONDITIONS / DEFER / REJECT, authority, evidence snapshot and expiry. A failed non-negotiable requirement results in DEFER or redesign, not a weighted-score waiver.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `OPG-RSM-E-SCOPE` (signed requirements), `OPG-RSM-E-COST` (validated rate-card and cost owner), `OPG-RSM-E-SEC` (risk/legal applicability), and `OPG-RSM-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `OPG-RSM`; **document kind:** `client-proposal`; **scenario:** `complex`.
