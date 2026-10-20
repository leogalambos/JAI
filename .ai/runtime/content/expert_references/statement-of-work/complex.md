---
reference_id: example:statement-of-work:complex
schema_version: '1.0.0'
content_revision: 2.1.0
document_kind: statement-of-work
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/statement-of-work
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: OPG-RSM-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Illustrative statement of work — negotiation draft — Regulated Settlement Modernisation

**Client:** Orion Payments Group · **Reference:** `OPG-RSM-STATEMENT_OF_WORK-01` · **Complexity:** complex · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Group Investment Committee, Payments Architecture Board, Risk and Legal Authorities.

<a id="dcs-proposed-statement-of-work.parties_scope"></a>

## Statement of work status, parties and service boundary

**Negotiation draft; not a signed contract.** Client: Orion Payments Group; proposed supplier: fictional **Northstar Enterprise Delivery Ltd.** Effective date, company registration identifiers, governing law, jurisdiction and signatories are **TO BE AGREED** by authorized Legal and Procurement representatives. Neither this example nor the proposal is an offer acceptance.

**Services:** design, build/integrate, verify and hand over **regional phased settlement replacement, jurisdiction policy gateway, append-only instruction journal, separately reconciled parallel ledger and strictly controlled recovery** in accordance with a baseline requirements schedule approved after discovery. In-scope service boundary: channel gateway, jurisdiction policy decision, durable instruction journal, settlement orchestrator, regional connector, parallel ledger, evidence store, three independent failure domains; programme objective: maintain traceable settlement instruction lineage and timely cut-off processing with zero unexplained ledger imbalance.

**Exclusions:**
- Guarantees about requirements in jurisdictions not validated by counsel
- Automated reversal of already-final settlements
- Unrestricted cross-border failover or replication
- External financial system modifications without signed interfaces
- Customer regulatory approvals or legal opinions

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
| D-06 | Jurisdiction control evidence | Entity applicability and legal exception decisions | Legal/Risk acceptance |
| D-07 | Dual-run ledger exit | Per-cutoff reconciliations and signed finality | Treasury acceptance |


For each deliverable, the supplier provides editable source, versioned evidence, document control and an identified recipient. The client reviews within a proposed five business days after formally complete submission; **silence must not constitute acceptance** in this exemplar. Missing evidence, unmatched scope or critical test failure gives the client a reasoned rejection. Re-submission follows documented remediation and retest.

Technical conditions include 99.95% monthly availability for critical processing; p95 acknowledgement under 450 ms excluding third-party network; RTO 30 minutes / RPO 5 minutes, but whether these become legally binding SLAs must be agreed explicitly; illustrative targets are not contractual warranties.

<a id="dcs-proposed-statement-of-work.responsibilities"></a>

## Client–supplier responsibilities, constraints and access

**Supplier:** delivery management; architectural design; implementation; agreed tests; design and operator documents; defect correction inside accepted scope; proposed risk controls. **Client:** access approvals, data classification, required third-party licences, SMEs, policy/legal interpretation, acceptance decisions and operational staffing. **Joint:** interface definitions, dependency management, incident/change coordination and design sign-off.

- **A1:** Legal entity owners determine applicable financial, data and outsourcing obligations before target design is frozen.
- **A2:** The client provides settlement message specifications, test ledgers, HSM/PKI policies and independent treasury sign-off authority.
- **A3:** Regional rollout is conditioned on dual-run evidence; unresolved cut-off reconciliation prevents release.
- **A4:** External clearing-house simulation and settlement counterparty test rights are obtained before resilience rehearsal.

The supplier does not assume authority to approve business risk, override regulatory restrictions, process live customer data without authorization, or change production systems outside signed change controls. Dependencies not met by the client are escalated, with documented time/cost impacts but no unilateral change.

<a id="dcs-proposed-statement-of-work.milestones_acceptance"></a>

## Schedule, checkpoints, acceptance and exit

Illustrative expected duration: **18 months** from agreed start following prerequisite completion.

| Window | Work package | Evidence produced / output | Receiving authority |
| --- | --- | --- | --- |
| M1–3 | Jurisdiction discovery and programme controls | Entity-by-entity applicability, service architecture baseline, dependency register | Executive/Legal/Risk |
| M4–6 | Target architecture and control design | Decision papers, typed flow model, dual-ledger design, approved ADR/HLD | Architecture Board |
| M7–10 | Core build and evidence instrumentation | Policy gateway, journal, reconciliation, resilience test plans | Delivery Director |
| M11–13 | First jurisdiction-controlled wave | Regulator-ready evidence package, parallel-run and cut-off rehearsals | Payments Operations |
| M14–17 | Remaining phased waves | Dual-control migration decisions, jurisdiction-specific acceptance | Local Legal Entity Owners |
| M18 | Operational takeover and governance close | Service owner acceptance, tested recovery, retention and decommission controls | Group Operations/Risk |


| Domain | Measure | Acceptance target (proposed) | Evidence expected |
| --- | --- | --- | --- |
| Business outcome | Unexplained ledger imbalance | 0 at authorised settlement finality checkpoints | Independently reconciled dual ledger |
| Processing | Acknowledgement latency | <450ms p95 excluding external networks | Measured agreed test population |
| Service | Critical monthly availability | 99.95% target | Per-region/cutoff business SLI |
| Recovery | RTO / RPO | 30 minutes / 5 minutes | Observed multi-site rehearsal |
| Jurisdiction | Forbidden routes | 0 accepted | Negative-case policy proof |


Acceptance is evidenced by independently reviewed test observations, specified recovery exercises, documented outstanding exceptions and acceptance by the receiving service owner. **Critical unexecuted or failed tests remain open**. The parties must explicitly agree a stabilization period, support start, final acceptance conditions and any permitted risk waiver mechanism in the executed contract.

<a id="dcs-proposed-statement-of-work.commercial_change"></a>

## Fees, change control and suspension

**Illustrative supplier professional services:** €4,500,000 from a model of **3000 supplier person-days**; other costs (separate third-party €1,500,000, client internal €800,000) are not payable to the supplier under this proposed SoW. All taxes, expenses, payment timing, acceptance-linked invoicing and indexation require legal/commercial agreement.

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


**Change request:** must identify original baseline, requested change, deliverable deltas, additional/removed days, licensing, dates, privacy/security consequences, new acceptance measures and approvers. No oral or AI-authored change modifies scope or price.

Termination/suspension, intellectual property, liability, data protection, subcontracting, warranties, confidentiality and dispute resolution require review under a negotiated master agreement; this Markdown is **not** legal advice and contains no enforceable limitation of liability.

<a id="dcs-proposed-statement-of-work.legal_reservations"></a>

## Legal, data protection and signature reservations

Data classes: payer/payee identifiers, settlement instructions, financial transaction metadata and restricted operational records. Applicability reservation: Applicable payment, resilience, outsourcing, data-residency, privacy and reporting obligations must be determined for each legal entity and jurisdiction by competent client authority before binding commitments. Before any real engagement, the client and supplier must identify controller/processor roles, permitted data locations, access permissions, applicable sector commitments, retention and exit arrangements.

Risk register:
| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Settlement-finality mismatch or irreversibility | Parallel ledger and dual-control compensating workflow | Treasury Control Owner |
| R2 | Cross-border processing outside authorized legal scope | Per-entity jurisdiction rules and independent privacy/legal approval | Group Compliance |
| R3 | Correlated regional or identity-plane outage | Failure-domain separation, cut-off-safe contingency | Resilience Architect |
| R4 | Unrecoverable reconciliation evidence | Append-only signed checkpoints and independently tested evidence chain | Assurance Lead |


**Execution block:** draft status, no customer procurement approval, no confirmed pricing authority, no actual data-processing authorization and no signature. Signatures must be created only through existing authorized human workflows; an AI-written name or hash is not a signature.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `OPG-RSM-E-SCOPE` (signed requirements), `OPG-RSM-E-COST` (validated rate-card and cost owner), `OPG-RSM-E-SEC` (risk/legal applicability), and `OPG-RSM-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `OPG-RSM`; **document kind:** `statement-of-work`; **scenario:** `complex`.
