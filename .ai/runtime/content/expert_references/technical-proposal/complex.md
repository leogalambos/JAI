---
reference_id: example:technical-proposal:complex
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: technical-proposal
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/technical-proposal
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: OPG-RSM-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Technical architecture and engineering proposal — Regulated Settlement Modernisation

**Client:** Orion Payments Group · **Reference:** `OPG-RSM-TECHNICAL_PROPOSAL-01` · **Complexity:** complex · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Group Investment Committee, Payments Architecture Board, Risk and Legal Authorities.

<a id="dcs-proposed-technical-proposal.architecture_context"></a>

## Architecture concern, scope and governing requirements

The solution changes regional legacy settlement engines, separate ledgers and manual end-of-day reconciliations with critical dependency concentration to **regional phased settlement replacement, jurisdiction policy gateway, append-only instruction journal, separately reconciled parallel ledger and strictly controlled recovery** for Orion Payments Group. The design is bounded by channel gateway, jurisdiction policy decision, durable instruction journal, settlement orchestrator, regional connector, parallel ledger, evidence store, three independent failure domains. Requirements and operating horizon: 14 jurisdictions; synthetic planning assumption 2.4 million instructions/day; multiple intraday cut-offs; target 99.95% monthly availability for critical processing; p95 acknowledgement under 450 ms excluding third-party network; RTO 30 minutes / RPO 5 minutes.

Architectural fitness questions: Which component owns business state? What may be replayed? Which identity is authorized across each trust boundary? How does the customer prove that the final business outcome occurred rather than an HTTP acknowledgement? All answers must be linked to canonical architecture identities, not duplicated diagrams.

<a id="dcs-proposed-technical-proposal.solution_design"></a>

## Logical design and component ownership

| Boundary/component | Proposed responsibility | Decision authority | Verification |
| --- | --- | --- | --- |
| Policy gateway | Jurisdiction and legal-entity permission before processing | Risk/Legal + Architecture | Forbidden-route negative cases |
| Durable journal | Ordered signed instruction lineage and recovery checkpoints | Technology Architecture | Replay and tamper-detection proof |
| Orchestration | State transitions respecting finality boundaries | Payments Engineering | State-machine and idempotency tests |
| Parallel ledger | Independent balancing and exception disposition | Treasury Control | Per-cutoff dual-run reconciliation |
| Resilience boundary | Three failure domains without unlawful transfer | Resilience/Privacy | Observed failover with business-state reconciliation |
| Evidence store | Immutable lineage linked to retention obligations | GRC Owner | Integrity, access and retention verification |


**Illustrative logical flow:** `authenticated channel → policy / validation → durable business-state boundary → controlled integration → reconciliation → monitored operations`.

Technical rationale: Settlement finality is a business/legal state rather than an API response; an apparently successful technical acknowledgement cannot replace independently reconciled evidence of finality. The preferred design limits uncontrolled shared writes and uses explicit error states, source timestamps, idempotency keys and per-boundary logging. Alternative synchronous fan-out may reduce one hop but creates correlated timeout exposure; a purely batch approach can fail the business timeliness objective. Final selection must be ratified in an ADR.

<a id="dcs-proposed-technical-proposal.interfaces_security"></a>

## Interface contract, trust boundaries and controls

For each in-scope API or event define request and response schema version; allowed actor, service account or tenant; payload classification; idempotency key; timeout/retry/backoff; deduplication retention; error codes and dead-letter strategy. A delivery acknowledgement is not evidence of correct final business state.

Security design: Jurisdiction-aware processing policy, dual authorization for settlement-affecting operations, segregated privileged identities, HSM/key ownership, control evidence at every irrevocable state boundary and restricted cross-border transfers. Data handled: payer/payee identifiers, settlement instructions, financial transaction metadata and restricted operational records. Legal/regulatory qualification: Applicable payment, resilience, outsourcing, data-residency, privacy and reporting obligations must be determined for each legal entity and jurisdiction by competent client authority before binding commitments. Unknown residency, supplier access and privileged control requirements remain blocking questions for the relevant client owner.

Reject unknown schema versions and cross-boundary access that fails explicit policy. Where rollback crosses irreversible business state, use authorized compensation and reconciliation, never an undocumented database edit.

<a id="dcs-proposed-technical-proposal.nonfunctional_requirements"></a>

## Quality attributes and allocation

Target engineering qualities: **99.95% monthly availability for critical processing; p95 acknowledgement under 450 ms excluding third-party network; RTO 30 minutes / RPO 5 minutes**. These are proposed acceptance objectives, not results.

| Domain | Measure | Acceptance target (proposed) | Evidence expected |
| --- | --- | --- | --- |
| Business outcome | Unexplained ledger imbalance | 0 at authorised settlement finality checkpoints | Independently reconciled dual ledger |
| Processing | Acknowledgement latency | <450ms p95 excluding external networks | Measured agreed test population |
| Service | Critical monthly availability | 99.95% target | Per-region/cutoff business SLI |
| Recovery | RTO / RPO | 30 minutes / 5 minutes | Observed multi-site rehearsal |
| Jurisdiction | Forbidden routes | 0 accepted | Negative-case policy proof |


Workload proof must match 14 jurisdictions; synthetic planning assumption 2.4 million instructions/day; multiple intraday cut-offs. Availability denominator, excluded windows and p95 populations require owner approval; RTO/RPO cannot be inferred from an architecture diagram. Capacity tests must cover backlog, supplier throttling, burst peaks and at least one failure of a shared dependency.

<a id="dcs-proposed-technical-proposal.verification_strategy"></a>

## Testing, deployment and release gates

Proof plan follows trace `business requirement → interface contract → build/fixture → functional and negative test → resilience exercise → service owner acceptance`. Execute representative valid and invalid access, duplicate/reordered events, partial failures and recovery.

| Window | Work package | Evidence produced / output | Receiving authority |
| --- | --- | --- | --- |
| M1–3 | Jurisdiction discovery and programme controls | Entity-by-entity applicability, service architecture baseline, dependency register | Executive/Legal/Risk |
| M4–6 | Target architecture and control design | Decision papers, typed flow model, dual-ledger design, approved ADR/HLD | Architecture Board |
| M7–10 | Core build and evidence instrumentation | Policy gateway, journal, reconciliation, resilience test plans | Delivery Director |
| M11–13 | First jurisdiction-controlled wave | Regulator-ready evidence package, parallel-run and cut-off rehearsals | Payments Operations |
| M14–17 | Remaining phased waves | Dual-control migration decisions, jurisdiction-specific acceptance | Local Legal Entity Owners |
| M18 | Operational takeover and governance close | Service owner acceptance, tested recovery, retention and decommission controls | Group Operations/Risk |


Release gate: zero unexplained business-record inconsistencies, actual negative authorization evidence, documented data-routing legality where applicable, operational alert ownership and timed recovery evidence. Missing tests remain NOT EXECUTED; no reviewer may convert them to PASS.

<a id="dcs-proposed-technical-proposal.technical_assumptions"></a>

## Design decisions, exclusions and unresolved matters

Working assumptions:
- **A1:** Legal entity owners determine applicable financial, data and outsourcing obligations before target design is frozen.
- **A2:** The client provides settlement message specifications, test ledgers, HSM/PKI policies and independent treasury sign-off authority.
- **A3:** Regional rollout is conditioned on dual-run evidence; unresolved cut-off reconciliation prevents release.
- **A4:** External clearing-house simulation and settlement counterparty test rights are obtained before resilience rehearsal.

Out of scope:
- Guarantees about requirements in jurisdictions not validated by counsel
- Automated reversal of already-final settlements
- Unrestricted cross-border failover or replication
- External financial system modifications without signed interfaces
- Customer regulatory approvals or legal opinions

Risks demanding further design decisions:
| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Settlement-finality mismatch or irreversibility | Parallel ledger and dual-control compensating workflow | Treasury Control Owner |
| R2 | Cross-border processing outside authorized legal scope | Per-entity jurisdiction rules and independent privacy/legal approval | Group Compliance |
| R3 | Correlated regional or identity-plane outage | Failure-domain separation, cut-off-safe contingency | Resilience Architect |
| R4 | Unrecoverable reconciliation evidence | Append-only signed checkpoints and independently tested evidence chain | Assurance Lead |


The delivered HLD, security assessment and deployment specification must share source IDs and architecture snapshot hash. A customer scope change requires impact review and an updated technical and commercial proposal.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `OPG-RSM-E-SCOPE` (signed requirements), `OPG-RSM-E-COST` (validated rate-card and cost owner), `OPG-RSM-E-SEC` (risk/legal applicability), and `OPG-RSM-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `OPG-RSM`; **document kind:** `technical-proposal`; **scenario:** `complex`.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `OPG-RSM-PROPOSAL-EXAMPLE` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Component and trust-zone boundary | Is this statement supported for `OPG-RSM-PROPOSAL-EXAMPLE` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
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

