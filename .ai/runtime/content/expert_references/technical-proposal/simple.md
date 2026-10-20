---
reference_id: example:technical-proposal:simple
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: technical-proposal
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/technical-proposal
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: HFS-FAR-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Technical architecture and engineering proposal — Field Appointment Reliability

**Client:** Harborline Field Services · **Reference:** `HFS-FAR-TECHNICAL_PROPOSAL-01` · **Complexity:** simple · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Operations Director and Procurement Lead.

<a id="dcs-proposed-technical-proposal.architecture_context"></a>

## Architecture concern, scope and governing requirements

The solution changes shared scheduling spreadsheet and single legacy dispatch application; late confirmations and duplicated technician assignments to **managed scheduling SaaS with a one-way dispatch synchronisation, central identity and auditable exception reconciliation** for Harborline Field Services. The design is bounded by Booking SaaS, corporate SSO, dispatch connector, durable notification queue, daily reconciliation dashboard. Requirements and operating horizon: 240 technicians, approximately 2,100 appointments each week; target p95 booking response below 2 seconds; monthly availability target 99.5%; RTO 8 hours and RPO 24 hours.

Architectural fitness questions: Which component owns business state? What may be replayed? Which identity is authorized across each trust boundary? How does the customer prove that the final business outcome occurred rather than an HTTP acknowledgement? All answers must be linked to canonical architecture identities, not duplicated diagrams.

<a id="dcs-proposed-technical-proposal.solution_design"></a>

## Logical design and component ownership

| Boundary/component | Proposed responsibility | Decision authority | Verification |
| --- | --- | --- | --- |
| Browser and SSO | OIDC/SAML through corporate identity | Client IAM owner | Denied-role tests and expired-session tests |
| Booking SaaS | Authoritative booking record and calendar consistency | Vendor / Client product owner | Double-booking negative tests |
| Dispatch connector | One-way sync with stable appointment keys | Supplier integration lead | Replay 150 synthetic appointments with duplicates |
| Operations dashboard | Daily exception count, stale sync alert | Service Desk Lead | Pilot reconciliation sign-off |


**Illustrative logical flow:** `authenticated channel → policy / validation → durable business-state boundary → controlled integration → reconciliation → monitored operations`.

Technical rationale: The proposition deliberately leaves the authoritative booking write in the SaaS platform; notifications and dispatch updates cannot become competing systems of record. The preferred design limits uncontrolled shared writes and uses explicit error states, source timestamps, idempotency keys and per-boundary logging. Alternative synchronous fan-out may reduce one hop but creates correlated timeout exposure; a purely batch approach can fail the business timeliness objective. Final selection must be ratified in an ADR.

<a id="dcs-proposed-technical-proposal.interfaces_security"></a>

## Interface contract, trust boundaries and controls

For each in-scope API or event define request and response schema version; allowed actor, service account or tenant; payload classification; idempotency key; timeout/retry/backoff; deduplication retention; error codes and dead-letter strategy. A delivery acknowledgement is not evidence of correct final business state.

Security design: SSO, minimum necessary dispatcher roles, encrypted transport, limited appointment data, no shared operations credentials and human authorization for bulk changes. Data handled: technician name, appointment address, job reference and visit window. Legal/regulatory qualification: UK data-protection applicability must be confirmed by the client privacy function. Unknown residency, supplier access and privileged control requirements remain blocking questions for the relevant client owner.

Reject unknown schema versions and cross-boundary access that fails explicit policy. Where rollback crosses irreversible business state, use authorized compensation and reconciliation, never an undocumented database edit.

<a id="dcs-proposed-technical-proposal.nonfunctional_requirements"></a>

## Quality attributes and allocation

Target engineering qualities: **p95 booking response below 2 seconds; monthly availability target 99.5%; RTO 8 hours and RPO 24 hours**. These are proposed acceptance objectives, not results.

| Domain | Measure | Acceptance target (proposed) | Evidence expected |
| --- | --- | --- | --- |
| Business outcome | Appointment rework | Baseline 2.3%; target ≤0.5% | Weekly reconciled dispatch report |
| Response | p95 booking response | <2 seconds | Measured synthetic and pilot traces |
| Integrity | Unexplained duplicate appointments | 0 during accepted pilot | Booking vs dispatch reconciliation |
| Recovery | RTO / RPO | 8 hours / 24 hours | Observed restore rehearsal |


Workload proof must match 240 technicians, approximately 2,100 appointments each week. Availability denominator, excluded windows and p95 populations require owner approval; RTO/RPO cannot be inferred from an architecture diagram. Capacity tests must cover backlog, supplier throttling, burst peaks and at least one failure of a shared dependency.

<a id="dcs-proposed-technical-proposal.verification_strategy"></a>

## Testing, deployment and release gates

Proof plan follows trace `business requirement → interface contract → build/fixture → functional and negative test → resilience exercise → service owner acceptance`. Execute representative valid and invalid access, duplicate/reordered events, partial failures and recovery.

| Window | Work package | Evidence produced / output | Receiving authority |
| --- | --- | --- | --- |
| W1–2 | Discovery and baseline | Signed requirements, data inventory, measured baseline | Operations Sponsor |
| W3–6 | Configure and integrate | Configured SaaS tenant, SSO, tested dispatch connector | Solution Lead |
| W7–8 | Verify and rehearse | Acceptance tests, restore rehearsal, defect disposition | Test Lead |
| W9 | Limited operational pilot | Pilot reconciliation and adoption evidence | Service Owner |
| W10 | Handover and acceptance | Runbook, training, acceptance record | Service Owner |


Release gate: zero unexplained business-record inconsistencies, actual negative authorization evidence, documented data-routing legality where applicable, operational alert ownership and timed recovery evidence. Missing tests remain NOT EXECUTED; no reviewer may convert them to PASS.

<a id="dcs-proposed-technical-proposal.technical_assumptions"></a>

## Design decisions, exclusions and unresolved matters

Working assumptions:
- **A1:** Client supplies authorized SaaS tenancy, identity integration owner and test access by W2.
- **A2:** Client makes available 2 dispatch SMEs and a decision owner within 2 working days of a material question.
- **A3:** No unexpected data transfer or licensing restriction invalidates the proposed SaaS solution.

Out of scope:
- Beside-the-scenes SaaS supplier platform changes
- Historical data cleansing beyond agreed fields
- 24×7 support subscription unless separately contracted
- Production endpoint credentials in any proposal deliverable

Risks demanding further design decisions:
| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Duplicate webhook updates | Idempotency by booking key; reconciliation | Application Lead |
| R2 | SaaS outage and export limitations | Daily verified export and offline dispatch procedure | Service Owner |
| R3 | Incomplete frontline adoption | Supervisor-assisted pilot and training | Business Sponsor |


The delivered HLD, security assessment and deployment specification must share source IDs and architecture snapshot hash. A customer scope change requires impact review and an updated technical and commercial proposal.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `HFS-FAR-E-SCOPE` (signed requirements), `HFS-FAR-E-COST` (validated rate-card and cost owner), `HFS-FAR-E-SEC` (risk/legal applicability), and `HFS-FAR-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `HFS-FAR`; **document kind:** `technical-proposal`; **scenario:** `simple`.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `HFS-FAR-PROPOSAL-EXAMPLE` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Component and trust-zone boundary | Is this statement supported for `HFS-FAR-PROPOSAL-EXAMPLE` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Interface and NFR test oracle | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Feasible implementation alternative | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — customer commitment integrity

Trace the exact customer-requested outcome to a separately priced deliverable and explicit acceptance test; classify any unsupported requirement as an assumption or clarification. For **technical-proposal**, the reviewer should actively challenge **component and trust-zone boundary** and **interface and nfr test oracle**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — contractual acceptance boundary

Distinguish indicative estimate, binding price, third-party pass-through and client internal cost. Change in scope requires a defined change-order rather than implied free delivery. The accountable party for this illustrative acceptance is **Bid Manager / Commercial Owner**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** component and trust-zone boundary, interface and nfr test oracle, and feasible implementation alternative. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

