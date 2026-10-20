---
reference_id: example:transformation-baseline-assessment:medium
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: transformation-baseline-assessment
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/transformation-baseline-assessment
dcs_status: proposed-not-mapped
approval_status: not-human-approved
case_id: MRG-OEI
methodology_context: "TOGAF-inspired baseline/target architecture and evidence-led capability assessment"
---

# Enterprise transformation baseline and capability assessment — Order Event Integration

> **SYNTHETIC EXPERT REFERENCE / NOT AN APPROVED PROJECT RECORD.** All organisations, measurements, contracts, test results, approvals and evidence IDs are invented. Narrative is illustrative, not proof of implementation or statutory compliance. Do not copy synthetic values into a real deliverable as verified facts.

**Entity of interest:** cross-channel order ingestion and ERP fulfilment synchronisation. **Context:** Meridian Retail Group. **Complexity:** medium. **Status:** proposed phased delivery; no live ERP, market or regulatory evidence. **Decision authority:** Digital Commerce Sponsor, subject to separate competent security, finance and operational authority.

**Evidence rule:** distinguish proposed design, expected test, observed result and human approval. In this document observed execution = none; every run-specific status remains `NOT_EXECUTED` or `OPEN`.

<a id="dcs-proposed-transformation-baseline-assessment.baseline_boundary"></a>
## 1. Baseline boundary

Baseline scope: **cross-channel order ingestion and ERP fulfilment synchronisation** serving **commerce product owners, ERP teams, market operations and 24×7 on-call**. The current state is **nightly ERP batch exports and brittle point-to-point integrations** under **180,000 orders per peak day across twelve markets**. The assessment answers what is actually known, what prevents business outcomes and which capabilities need change; it does not start by assuming the preferred technology is correct. Stakeholders: Digital Commerce Sponsor for outcomes, Integration Architect for architecture evidence, Service Operations Manager for service continuity and Head of Digital Risk for risk. Unknown vendor obligations, personal-data flows and jurisdiction applicability are explicitly open.

<a id="dcs-proposed-transformation-baseline-assessment.capability_evidence"></a>
## 2. Capability evidence

Use capability IDs for business demand, processes, people, information, applications and technology. For each, distinguish current owner, service users, observed outcomes, interfaces, operating evidence and maturity confidence. The example capabilities include order/appointment/settlement acceptance, identity and authorization, reconciliation, incident recovery and change authorization. Rate evidence sufficiency on observed records, interviews and modelled assumptions separately. A 'mature' self-assessment without process logs is a hypothesis, not a measured baseline.

<a id="dcs-proposed-transformation-baseline-assessment.pain_points"></a>
## 3. Pain points

Material pain points: **customer-data misrouting, delayed order promises and incomplete reconciliation** and **duplicate or out-of-order messages create an incorrect fulfilment state**. Establish baseline for **p95 broker-to-ERP lag, replay rejection and unmatched order IDs**, lead time from request to completed business outcome, manual reconciliation work, failed-change rate and support burden. Do not invent baseline measurements from the synthetic operating target. Each issue has a causal hypothesis, business owner, affected population, evidence gap and counterfactual challenge. Retain competing explanations such as poor identity policy rather than immediately blaming an integration platform.

### Worked assessment matrix (synthetic)

| Capability | Current observation | Evidence confidence | Next verification |
|---|---|---|---|
| Business outcome | nightly ERP batch exports and brittle point-to-point integrations | Hypothesis | Baseline measure |
| Data lineage | Multi-component state dependencies | Not observed | Source-to-target trace |
| Operational readiness | Alert & recovery ownership unclear | Not observed | Service review |
| Security governance | Entity and role policy unknown | Not verified | Control mapping |

The matrix is a proposed verification instrument for **cross-channel order ingestion and ERP fulfilment synchronisation**. Its displayed rows are not actual enterprise observations. Evidence must be source-bound and independently interpreted before a finding or green status can support a project decision.

<a id="dcs-proposed-transformation-baseline-assessment.dependency_map"></a>
## 4. Dependency map

Model dependencies across systems, suppliers, skills, data ownership, operational teams and external obligations. The critical chain is **commerce write → transactional outbox → broker → idempotent ERP adapter → reconciliation**. Distinguish a shared runtime failure domain from organizational coupling (e.g., the only approving specialist). Mark boundaries where independent assurance is required. For the planned transition, map candidate changes onto upstream/downstream consumers, data transformations, controls and sunset obligations. A capability cannot be considered isolated if its data or identity service remains shared.

<a id="dcs-proposed-transformation-baseline-assessment.gap_prioritisation"></a>
## 5. Gap prioritisation

Prioritize gaps using business impact, urgency, effort, evidence confidence and regulatory constraints. Use ordered bands rather than false precision: immediate safety/control correction; validated high-value intervention; deferred low-value convenience. A gap may be critical due to absent evidence even when no failure has yet been observed. Protect scope boundaries and no-regression conditions; avoid forcing all legacy components into replacement when a safer process fix suffices. Funding estimates are provisional until finance validates the baseline.

### Dependency and challenge analysis

For MRG-OEI, a release or transformation claim is invalid if **country data-handling decisions, broker retention, ERP freeze windows and vendor SLAs** remains unresolved. Check the counterfactual: what would break if the preferred technology were removed while user behavior and business service demand stayed constant? An independent reviewer should challenge the alleged root cause, hidden vendor commitments, failures spanning commerce cloud → broker → region-scoped ERP service, and who accepts an unsuccessful delivery when the sponsor and implementer disagree.

<a id="dcs-proposed-transformation-baseline-assessment.baseline_decision"></a>
## 6. Baseline decision

Recommendation: establish an evidenced baseline before committing to **a transactional outbox, retained event broker and idempotent country-aware ERP adapters**. Approve only bounded discovery, instrumentation and controlled proof activities first. Entry conditions for target-design approval: verified data authority, risk taxonomy, ownership of the critical interfaces, observed service metrics and residual unknowns. The report is suitable for transformation decision support, not a certificate of enterprise maturity.

## Example decision register

| Decision | Alternatives / objections | Evidence needed | Owner and status |
|---|---|---|---|
| DR-01 — approve scoped approach | transactional outbox plus managed broker with a quarantine stream and idempotent consumers vs controlled baseline | Business invariant and dependency mapping | Digital Commerce Sponsor — OPEN |
| DR-02 — permit protected integration | Deny or quarantine unknown actor/entity vs permissive routing | Independent negative authorization and reconciliation | Head of Digital Risk — OPEN |
| DR-03 — accept operations handover | Reversible pilot vs direct cutover | 2 hours/15 minutes timed recovery, staffed on-call | Service Operations Manager — OPEN |

All decision IDs above are local worked-example identifiers; they are not proof that any person approved or that underlying evidence exists.

## Evidence register, validation and handoff

| Example evidence ID | Required underlying record | Status |
|---|---|---|
| MRG-OEI-E-SCOPE | Verifiable operating baseline, applicable entity/data obligations | PROPOSED / NOT OBSERVED |
| MRG-OEI-E-DESIGN | Versioned architecture/contract and independent review | PROPOSED |
| MRG-OEI-E-TEST | Executed test inputs, output, toolchain and build digest | NOT EXECUTED |
| MRG-OEI-E-OPS | Receiving service acceptance and live owner | PENDING |

**Minimum acceptance conditions:** authoritative requirement `MRG-OEI-REQ-01` traced to business owner; exact build `MRG-OEI-BUILD-01` and change `MRG-OEI-CHG-01` evidenced by immutable identifiers; critical controls evaluated on the intended trust boundary; explicit mitigation and verification of **duplicate or out-of-order messages create an incorrect fulfilment state**; completed handoff acknowledged by Service Operations Manager. An unsupported assumption remains OPEN and may justify deferral.

**Handoff graph:** MRG-OEI-REQ → MRG-OEI-ARCH → MRG-OEI-SEC → MRG-OEI-BUILD → MRG-OEI-TEST → MRG-OEI-OPS. These IDs are illustrative and must not be mistaken for existing documents.

**Methodological reference:** TOGAF-inspired baseline/target architecture and evidence-led capability assessment. These frameworks inform professional coverage and challenge questions; this reference does not assert compliance or quote normative control clauses.

**Professional review disposition:** OPEN. No actual implementation, live provider validation, signed security assessment, executive approval or legal determination occurred.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `MRG-OEI` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Evidence-backed baseline metric | Is this statement supported for `MRG-OEI` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Dependency and pain-point classification | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Measurement owner and open gap | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — baseline-to-target value bridge

Capture an attributable as-is metric and source system, target metric and accountable benefit owner. A future target is not a measured present capability. For **transformation-baseline-assessment**, the reviewer should actively challenge **evidence-backed baseline metric** and **dependency and pain-point classification**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — transition states

Track current, interim and target states with entry/exit criteria, service continuity, legacy retirement and irreversible data conversion boundaries. The accountable party for this illustrative acceptance is **Transformation Sponsor / Receiving Operations Owner**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** evidence-backed baseline metric, dependency and pain-point classification, and measurement owner and open gap. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

