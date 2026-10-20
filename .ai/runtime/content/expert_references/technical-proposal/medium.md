---
reference_id: example:technical-proposal:medium
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: technical-proposal
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/technical-proposal
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: MRG-OEI-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Technical architecture and engineering proposal — Order Event Integration

**Client:** Meridian Retail Group · **Reference:** `MRG-OEI-TECHNICAL_PROPOSAL-01` · **Complexity:** medium · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Architecture Review Board, Finance Partner and Procurement.

<a id="dcs-proposed-technical-proposal.architecture_context"></a>

## Architecture concern, scope and governing requirements

The solution changes nightly ERP batch exports and fragile point-to-point integration with delayed order promise updates to **transactional outbox, managed event broker, independently versioned ERP consumers, dead-letter quarantine and business reconciliation** for Meridian Retail Group. The design is bounded by commerce outbox, event broker, ERP adapter, market routing policy, reconciliation store, observability. Requirements and operating horizon: 12 European markets, peak 180,000 orders/day; first rollout covers two markets; target p95 order-to-ERP availability under 5 minutes; availability target 99.9% monthly; RTO 2 hours / RPO 15 minutes.

Architectural fitness questions: Which component owns business state? What may be replayed? Which identity is authorized across each trust boundary? How does the customer prove that the final business outcome occurred rather than an HTTP acknowledgement? All answers must be linked to canonical architecture identities, not duplicated diagrams.

<a id="dcs-proposed-technical-proposal.solution_design"></a>

## Logical design and component ownership

| Boundary/component | Proposed responsibility | Decision authority | Verification |
| --- | --- | --- | --- |
| Commerce outbox | Atomic publication intent linked to checkout | Commerce Platform Lead | Crash/duplicate/restart test |
| Event broker | Durable retained topics with scoped ACLs | Platform Team | Quota, backlog and failover exercise |
| ERP consumer | Versioned idempotent order update | Integration Supplier | Reordered/duplicated 50,000-event suite |
| Market policy | Country routing, field minimization | Privacy/IAM | Wrong-country negative tests |
| Reconciliation | Compare accepted to final ERP orders | ERP Service Owner | No unexplained order-ID gap |


**Illustrative logical flow:** `authenticated channel → policy / validation → durable business-state boundary → controlled integration → reconciliation → monitored operations`.

Technical rationale: The managed broker is not the system of record; order state remains authoritative in commerce/ERP with reconciliation establishing business processing success. The preferred design limits uncontrolled shared writes and uses explicit error states, source timestamps, idempotency keys and per-boundary logging. Alternative synchronous fan-out may reduce one hop but creates correlated timeout exposure; a purely batch approach can fail the business timeliness objective. Final selection must be ratified in an ADR.

<a id="dcs-proposed-technical-proposal.interfaces_security"></a>

## Interface contract, trust boundaries and controls

For each in-scope API or event define request and response schema version; allowed actor, service account or tenant; payload classification; idempotency key; timeout/retry/backoff; deduplication retention; error codes and dead-letter strategy. A delivery acknowledgement is not evidence of correct final business state.

Security design: Scoped producer and consumer identities, tenant/market segregation, encryption, immutable correlation tracing and client-owned data retention rules. Data handled: order ID, fulfilment events, pseudonymous customer reference and delivery address. Legal/regulatory qualification: GDPR applicability, market-level data routing and cross-border transfers require a documented client privacy decision. Unknown residency, supplier access and privileged control requirements remain blocking questions for the relevant client owner.

Reject unknown schema versions and cross-boundary access that fails explicit policy. Where rollback crosses irreversible business state, use authorized compensation and reconciliation, never an undocumented database edit.

<a id="dcs-proposed-technical-proposal.nonfunctional_requirements"></a>

## Quality attributes and allocation

Target engineering qualities: **p95 order-to-ERP availability under 5 minutes; availability target 99.9% monthly; RTO 2 hours / RPO 15 minutes**. These are proposed acceptance objectives, not results.

| Domain | Measure | Acceptance target (proposed) | Evidence expected |
| --- | --- | --- | --- |
| Business outcome | Accepted order visibility | ≤5 minutes p95 | Correlated commerce/broker/ERP timestamps |
| Data integrity | Unexplained missing / duplicated orders | 0 within signed reconciliation window | Idempotency and ledger sample |
| Availability | Monthly service availability | 99.9% target | SLI agreed with service owner |
| Recovery | RTO / RPO | 2 hours / 15 minutes | Replayed checkpoint validation |


Workload proof must match 12 European markets, peak 180,000 orders/day; first rollout covers two markets. Availability denominator, excluded windows and p95 populations require owner approval; RTO/RPO cannot be inferred from an architecture diagram. Capacity tests must cover backlog, supplier throttling, burst peaks and at least one failure of a shared dependency.

<a id="dcs-proposed-technical-proposal.verification_strategy"></a>

## Testing, deployment and release gates

Proof plan follows trace `business requirement → interface contract → build/fixture → functional and negative test → resilience exercise → service owner acceptance`. Execute representative valid and invalid access, duplicate/reordered events, partial failures and recovery.

| Window | Work package | Evidence produced / output | Receiving authority |
| --- | --- | --- | --- |
| W1–4 | Baseline, discovery and contracts | Source-to-target maps, market classification and interface contract | Business/ERP Owners |
| W5–10 | Architecture and foundation | Broker, identity boundary, outbox and ADRs | Architecture Authority |
| W11–21 | Delivery wave 1 | Two-market adapter and reconciliation capability | Delivery Director |
| W22–27 | Verification and controlled market extension | Negative routing tests, resilience and performance evidence | QA Lead |
| W28–32 | Rollout and handover | Market adoption, 24×7 rota confirmation, exit checklist | Service Operations Manager |


Release gate: zero unexplained business-record inconsistencies, actual negative authorization evidence, documented data-routing legality where applicable, operational alert ownership and timed recovery evidence. Missing tests remain NOT EXECUTED; no reviewer may convert them to PASS.

<a id="dcs-proposed-technical-proposal.technical_assumptions"></a>

## Design decisions, exclusions and unresolved matters

Working assumptions:
- **A1:** Client supplies sample outbox events, ERP non-production interfaces and named market owners by W4.
- **A2:** Each market approves data routing and customer field minimisation before its release.
- **A3:** No fundamental vendor contract restriction prevents the agreed event delivery architecture.

Out of scope:
- Replacement of the ERP core
- Transformation of downstream logistics vendor platforms
- Country-specific statutory legal opinions
- Perpetual guarantees of processing exactly once at transport level

Risks demanding further design decisions:
| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Duplicate/out-of-order events | Outbox, stable idempotency keys, replay and exception reconciliation | Integration Architect |
| R2 | Incorrect country routing of personal data | Region tagging and negative policy tests | Privacy Lead |
| R3 | Market cutover and shared broker saturation | Two-market canary, back-pressure and capacity stress tests | Operations Manager |


The delivered HLD, security assessment and deployment specification must share source IDs and architecture snapshot hash. A customer scope change requires impact review and an updated technical and commercial proposal.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `MRG-OEI-E-SCOPE` (signed requirements), `MRG-OEI-E-COST` (validated rate-card and cost owner), `MRG-OEI-E-SEC` (risk/legal applicability), and `MRG-OEI-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `MRG-OEI`; **document kind:** `technical-proposal`; **scenario:** `medium`.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `MRG-OEI-PROPOSAL-EXAMPLE` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Component and trust-zone boundary | Is this statement supported for `MRG-OEI-PROPOSAL-EXAMPLE` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
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

