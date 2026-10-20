---
reference_id: example:transformation-baseline-assessment:complex
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: transformation-baseline-assessment
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/transformation-baseline-assessment
dcs_status: proposed-not-mapped
approval_status: not-human-approved
case_id: OPG-RSM
methodology_context: "TOGAF-inspired baseline/target architecture and evidence-led capability assessment"
---

# Enterprise transformation baseline and capability assessment — Regulated Settlement Modernisation

> **SYNTHETIC EXPERT REFERENCE / NOT AN APPROVED PROJECT RECORD.** All organisations, measurements, contracts, test results, approvals and evidence IDs are invented. Narrative is illustrative, not proof of implementation or statutory compliance. Do not copy synthetic values into a real deliverable as verified facts.

**Entity of interest:** cross-border settlement instruction processing and finality reconciliation. **Context:** Orion Payments Group. **Complexity:** complex. **Status:** proposed transformation; no enacted jurisdictional approval or production evidence. **Decision authority:** Group Payments Executive, subject to separate competent security, finance and operational authority.

**Evidence rule:** distinguish proposed design, expected test, observed result and human approval. In this document observed execution = none; every run-specific status remains `NOT_EXECUTED` or `OPEN`.

<a id="dcs-proposed-transformation-baseline-assessment.baseline_boundary"></a>
## 1. Baseline boundary

Baseline scope: **cross-border settlement instruction processing and finality reconciliation** serving **treasury control, regional settlement teams, regulators where applicable, resilience and security operations**. The current state is **jurisdiction-specific legacy engines and manual end-of-day reconciliation** under **2.4 million synthetic instructions daily across fourteen jurisdictions**. The assessment answers what is actually known, what prevents business outcomes and which capabilities need change; it does not start by assuming the preferred technology is correct. Stakeholders: Group Payments Executive for outcomes, Chief Payments Architect for architecture evidence, Critical Service Operations Director for service continuity and Enterprise Financial Risk Officer for risk. Unknown vendor obligations, personal-data flows and jurisdiction applicability are explicitly open.

<a id="dcs-proposed-transformation-baseline-assessment.capability_evidence"></a>
## 2. Capability evidence

Use capability IDs for business demand, processes, people, information, applications and technology. For each, distinguish current owner, service users, observed outcomes, interfaces, operating evidence and maturity confidence. The example capabilities include order/appointment/settlement acceptance, identity and authorization, reconciliation, incident recovery and change authorization. Rate evidence sufficiency on observed records, interviews and modelled assumptions separately. A 'mature' self-assessment without process logs is a hypothesis, not a measured baseline.

<a id="dcs-proposed-transformation-baseline-assessment.pain_points"></a>
## 3. Pain points

Material pain points: **financial integrity, data-residency breach and loss of transaction finality** and **unexplained ledger imbalance or illegal cross-region failover invalidates settlement finality**. Establish baseline for **finality reconciliation exceptions, policy-denied jurisdiction routes and settlement cut-off lag**, lead time from request to completed business outcome, manual reconciliation work, failed-change rate and support burden. Do not invent baseline measurements from the synthetic operating target. Each issue has a causal hypothesis, business owner, affected population, evidence gap and counterfactual challenge. Retain competing explanations such as poor identity policy rather than immediately blaming an integration platform.

### Worked assessment matrix (synthetic)

| Capability | Current observation | Evidence confidence | Next verification |
|---|---|---|---|
| Business outcome | jurisdiction-specific legacy engines and manual end-of-day reconciliation | Hypothesis | Baseline measure |
| Data lineage | Multi-component state dependencies | Not observed | Source-to-target trace |
| Operational readiness | Alert & recovery ownership unclear | Not observed | Service review |
| Security governance | Entity and role policy unknown | Not verified | Control mapping |

The matrix is a proposed verification instrument for **cross-border settlement instruction processing and finality reconciliation**. Its displayed rows are not actual enterprise observations. Evidence must be source-bound and independently interpreted before a finding or green status can support a project decision.

<a id="dcs-proposed-transformation-baseline-assessment.dependency_map"></a>
## 4. Dependency map

Model dependencies across systems, suppliers, skills, data ownership, operational teams and external obligations. The critical chain is **channel → policy gateway → signed journal → settlement orchestration → ledger / regional connector → reconciliation**. Distinguish a shared runtime failure domain from organizational coupling (e.g., the only approving specialist). Mark boundaries where independent assurance is required. For the planned transition, map candidate changes onto upstream/downstream consumers, data transformations, controls and sunset obligations. A capability cannot be considered isolated if its data or identity service remains shared.

<a id="dcs-proposed-transformation-baseline-assessment.gap_prioritisation"></a>
## 5. Gap prioritisation

Prioritize gaps using business impact, urgency, effort, evidence confidence and regulatory constraints. Use ordered bands rather than false precision: immediate safety/control correction; validated high-value intervention; deferred low-value convenience. A gap may be critical due to absent evidence even when no failure has yet been observed. Protect scope boundaries and no-regression conditions; avoid forcing all legacy components into replacement when a safer process fix suffices. Funding estimates are provisional until finance validates the baseline.

### Dependency and challenge analysis

For OPG-RSM, a release or transformation claim is invalid if **legal applicability by entity, immutable evidence, HSM policy, finality and regional cut-off controls** remains unresolved. Check the counterfactual: what would break if the preferred technology were removed while user behavior and business service demand stayed constant? An independent reviewer should challenge the alleged root cause, hidden vendor commitments, failures spanning channel boundary → policy decision → immutable journal → regulated ledger and regional processors, and who accepts an unsuccessful delivery when the sponsor and implementer disagree.

<a id="dcs-proposed-transformation-baseline-assessment.baseline_decision"></a>
## 6. Baseline decision

Recommendation: establish an evidenced baseline before committing to **jurisdiction-aware orchestration, signed instruction lineage, parallel ledger and controlled migration**. Approve only bounded discovery, instrumentation and controlled proof activities first. Entry conditions for target-design approval: verified data authority, risk taxonomy, ownership of the critical interfaces, observed service metrics and residual unknowns. The report is suitable for transformation decision support, not a certificate of enterprise maturity.

## Enterprise-level adversarial review and exceptional paths

**Compound failure exercise:** independently simulate supplier unavailability, revocation of a privileged deployment identity and loss of trustworthy state observations. The safety response must be bounded: freeze new acceptance and perform authorised compensating reconciliation; never reverse finalised ledgers as a generic rollback. The test never permits bypassing jurisdictional or risk authority; every state-changing activity needs a decision owner, reversible boundary, observed invariant and auditable approval.

**Jurisdiction and third-party boundary:** do not assume an authorization in one market extends to another or that a supplier statement covers the entire fourteen jurisdictions, three failure domains, regional connectors, dual-run ledger, evidence store. A transition must preserve retention and finality duties, business data ownership, security of pipeline credentials and a record of exceptions with expiry.

**Contested decision:** compare the recommended approach **append-only instruction lineage and jurisdiction-aware orchestration with parallel ledger checkpoints** with maintaining the baseline and an aggressive fast-cutover alternative. Ask what evidence would invalidate the preference and estimate the operational consequence of an unplanned halt during **an eighteen-month phased programme with parallel-run cut-offs**. Neither an attractive ROI nor a technically green build overrides a critical missing control or competent stakeholder approval.

## Example decision register

| Decision | Alternatives / objections | Evidence needed | Owner and status |
|---|---|---|---|
| DR-01 — approve scoped approach | append-only instruction lineage and jurisdiction-aware orchestration with parallel ledger checkpoints vs controlled baseline | Business invariant and dependency mapping | Group Payments Executive — OPEN |
| DR-02 — permit protected integration | Deny or quarantine unknown actor/entity vs permissive routing | Independent negative authorization and reconciliation | Enterprise Financial Risk Officer — OPEN |
| DR-03 — accept operations handover | Reversible pilot vs direct cutover | 30 minutes/5 minutes timed recovery, staffed on-call | Critical Service Operations Director — OPEN |

All decision IDs above are local worked-example identifiers; they are not proof that any person approved or that underlying evidence exists.

## Evidence register, validation and handoff

| Example evidence ID | Required underlying record | Status |
|---|---|---|
| OPG-RSM-E-SCOPE | Verifiable operating baseline, applicable entity/data obligations | PROPOSED / NOT OBSERVED |
| OPG-RSM-E-DESIGN | Versioned architecture/contract and independent review | PROPOSED |
| OPG-RSM-E-TEST | Executed test inputs, output, toolchain and build digest | NOT EXECUTED |
| OPG-RSM-E-OPS | Receiving service acceptance and live owner | PENDING |

**Minimum acceptance conditions:** authoritative requirement `OPG-RSM-REQ-01` traced to business owner; exact build `OPG-RSM-BUILD-01` and change `OPG-RSM-CHG-01` evidenced by immutable identifiers; critical controls evaluated on the intended trust boundary; explicit mitigation and verification of **unexplained ledger imbalance or illegal cross-region failover invalidates settlement finality**; completed handoff acknowledged by Critical Service Operations Director. An unsupported assumption remains OPEN and may justify deferral.

**Handoff graph:** OPG-RSM-REQ → OPG-RSM-ARCH → OPG-RSM-SEC → OPG-RSM-BUILD → OPG-RSM-TEST → OPG-RSM-OPS. These IDs are illustrative and must not be mistaken for existing documents.

**Methodological reference:** TOGAF-inspired baseline/target architecture and evidence-led capability assessment. These frameworks inform professional coverage and challenge questions; this reference does not assert compliance or quote normative control clauses.

**Professional review disposition:** OPEN. No actual implementation, live provider validation, signed security assessment, executive approval or legal determination occurred.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `OPG-RSM` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Evidence-backed baseline metric | Is this statement supported for `OPG-RSM` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
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

