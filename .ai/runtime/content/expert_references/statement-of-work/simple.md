---
reference_id: example:statement-of-work:simple
schema_version: '1.0.0'
content_revision: 2.1.0
document_kind: statement-of-work
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/statement-of-work
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: HFS-FAR-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Illustrative statement of work — negotiation draft — Field Appointment Reliability

**Client:** Harborline Field Services · **Reference:** `HFS-FAR-STATEMENT_OF_WORK-01` · **Complexity:** simple · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Operations Director and Procurement Lead.

<a id="dcs-proposed-statement-of-work.parties_scope"></a>

## Statement of work status, parties and service boundary

**Negotiation draft; not a signed contract.** Client: Harborline Field Services; proposed supplier: fictional **Northstar Enterprise Delivery Ltd.** Effective date, company registration identifiers, governing law, jurisdiction and signatories are **TO BE AGREED** by authorized Legal and Procurement representatives. Neither this example nor the proposal is an offer acceptance.

**Services:** design, build/integrate, verify and hand over **managed scheduling SaaS with a one-way dispatch synchronisation, central identity and auditable exception reconciliation** in accordance with a baseline requirements schedule approved after discovery. In-scope service boundary: Booking SaaS, corporate SSO, dispatch connector, durable notification queue, daily reconciliation dashboard; programme objective: reduce appointment rework from an illustrative 2.3% to 0.5% within two quarters.

**Exclusions:**
- Beside-the-scenes SaaS supplier platform changes
- Historical data cleansing beyond agreed fields
- 24×7 support subscription unless separately contracted
- Production endpoint credentials in any proposal deliverable

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


For each deliverable, the supplier provides editable source, versioned evidence, document control and an identified recipient. The client reviews within a proposed five business days after formally complete submission; **silence must not constitute acceptance** in this exemplar. Missing evidence, unmatched scope or critical test failure gives the client a reasoned rejection. Re-submission follows documented remediation and retest.

Technical conditions include p95 booking response below 2 seconds; monthly availability target 99.5%; RTO 8 hours and RPO 24 hours, but whether these become legally binding SLAs must be agreed explicitly; illustrative targets are not contractual warranties.

<a id="dcs-proposed-statement-of-work.responsibilities"></a>

## Client–supplier responsibilities, constraints and access

**Supplier:** delivery management; architectural design; implementation; agreed tests; design and operator documents; defect correction inside accepted scope; proposed risk controls. **Client:** access approvals, data classification, required third-party licences, SMEs, policy/legal interpretation, acceptance decisions and operational staffing. **Joint:** interface definitions, dependency management, incident/change coordination and design sign-off.

- **A1:** Client supplies authorized SaaS tenancy, identity integration owner and test access by W2.
- **A2:** Client makes available 2 dispatch SMEs and a decision owner within 2 working days of a material question.
- **A3:** No unexpected data transfer or licensing restriction invalidates the proposed SaaS solution.

The supplier does not assume authority to approve business risk, override regulatory restrictions, process live customer data without authorization, or change production systems outside signed change controls. Dependencies not met by the client are escalated, with documented time/cost impacts but no unilateral change.

<a id="dcs-proposed-statement-of-work.milestones_acceptance"></a>

## Schedule, checkpoints, acceptance and exit

Illustrative expected duration: **10 weeks** from agreed start following prerequisite completion.

| Window | Work package | Evidence produced / output | Receiving authority |
| --- | --- | --- | --- |
| W1–2 | Discovery and baseline | Signed requirements, data inventory, measured baseline | Operations Sponsor |
| W3–6 | Configure and integrate | Configured SaaS tenant, SSO, tested dispatch connector | Solution Lead |
| W7–8 | Verify and rehearse | Acceptance tests, restore rehearsal, defect disposition | Test Lead |
| W9 | Limited operational pilot | Pilot reconciliation and adoption evidence | Service Owner |
| W10 | Handover and acceptance | Runbook, training, acceptance record | Service Owner |


| Domain | Measure | Acceptance target (proposed) | Evidence expected |
| --- | --- | --- | --- |
| Business outcome | Appointment rework | Baseline 2.3%; target ≤0.5% | Weekly reconciled dispatch report |
| Response | p95 booking response | <2 seconds | Measured synthetic and pilot traces |
| Integrity | Unexplained duplicate appointments | 0 during accepted pilot | Booking vs dispatch reconciliation |
| Recovery | RTO / RPO | 8 hours / 24 hours | Observed restore rehearsal |


Acceptance is evidenced by independently reviewed test observations, specified recovery exercises, documented outstanding exceptions and acceptance by the receiving service owner. **Critical unexecuted or failed tests remain open**. The parties must explicitly agree a stabilization period, support start, final acceptance conditions and any permitted risk waiver mechanism in the executed contract.

<a id="dcs-proposed-statement-of-work.commercial_change"></a>

## Fees, change control and suspension

**Illustrative supplier professional services:** £84,000 from a model of **120 supplier person-days**; other costs (separate third-party £42,000, client internal £14,000) are not payable to the supplier under this proposed SoW. All taxes, expenses, payment timing, acceptance-linked invoicing and indexation require legal/commercial agreement.

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


**Change request:** must identify original baseline, requested change, deliverable deltas, additional/removed days, licensing, dates, privacy/security consequences, new acceptance measures and approvers. No oral or AI-authored change modifies scope or price.

Termination/suspension, intellectual property, liability, data protection, subcontracting, warranties, confidentiality and dispute resolution require review under a negotiated master agreement; this Markdown is **not** legal advice and contains no enforceable limitation of liability.

<a id="dcs-proposed-statement-of-work.legal_reservations"></a>

## Legal, data protection and signature reservations

Data classes: technician name, appointment address, job reference and visit window. Applicability reservation: UK data-protection applicability must be confirmed by the client privacy function. Before any real engagement, the client and supplier must identify controller/processor roles, permitted data locations, access permissions, applicable sector commitments, retention and exit arrangements.

Risk register:
| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Duplicate webhook updates | Idempotency by booking key; reconciliation | Application Lead |
| R2 | SaaS outage and export limitations | Daily verified export and offline dispatch procedure | Service Owner |
| R3 | Incomplete frontline adoption | Supervisor-assisted pilot and training | Business Sponsor |


**Execution block:** draft status, no customer procurement approval, no confirmed pricing authority, no actual data-processing authorization and no signature. Signatures must be created only through existing authorized human workflows; an AI-written name or hash is not a signature.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `HFS-FAR-E-SCOPE` (signed requirements), `HFS-FAR-E-COST` (validated rate-card and cost owner), `HFS-FAR-E-SEC` (risk/legal applicability), and `HFS-FAR-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `HFS-FAR`; **document kind:** `statement-of-work`; **scenario:** `simple`.
