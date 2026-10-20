---
reference_id: example:target-operating-model:complex
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: target-operating-model
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/target-operating-model
dcs_status: proposed-not-mapped
approval_status: not-human-approved
case_id: OPG-RSM
methodology_context: "ITIL service value thinking and accountable enterprise operating-model design"
---

# Target operating model and service accountability — Regulated Settlement Modernisation

> **SYNTHETIC EXPERT REFERENCE / NOT AN APPROVED PROJECT RECORD.** All organisations, measurements, contracts, test results, approvals and evidence IDs are invented. Narrative is illustrative, not proof of implementation or statutory compliance. Do not copy synthetic values into a real deliverable as verified facts.

**Entity of interest:** cross-border settlement instruction processing and finality reconciliation. **Context:** Orion Payments Group. **Complexity:** complex. **Status:** proposed transformation; no enacted jurisdictional approval or production evidence. **Decision authority:** Group Payments Executive, subject to separate competent security, finance and operational authority.

**Evidence rule:** distinguish proposed design, expected test, observed result and human approval. In this document observed execution = none; every run-specific status remains `NOT_EXECUTED` or `OPEN`.

<a id="dcs-proposed-target-operating-model.target_value"></a>
## 1. Target value

The proposed operating model exists to achieve **zero unexplained finality imbalance at the mandated cut-off** for **cross-border settlement instruction processing and finality reconciliation**, not to reproduce a generic ITIL org chart. Specify customers, demand channels, accountable service/product owners, regulated decision rights, support hours and supplier boundaries. Current model depends on **jurisdiction-specific legacy engines and manual end-of-day reconciliation**; future model supports **jurisdiction-aware orchestration, signed instruction lineage, parallel ledger and controlled migration**. The design boundary is **fourteen jurisdictions, three failure domains, regional connectors, dual-run ledger, evidence store** and its purpose is verifiable business-state integrity.

<a id="dcs-proposed-target-operating-model.capability_ownership"></a>
## 2. Capability ownership

Operating capabilities: service ownership, product/change decision, supplier management, IAM, incident/problem, configuration, observability, release assurance, information governance and continuity. State who owns each capability and which budget or rota sustains it. Capability evolution must include human skills, not only target applications. Where Critical Service Operations Director is receiving authority, receipt must be evidenced; a delivery team cannot appoint operations acceptance by generating a RACI table.

<a id="dcs-proposed-target-operating-model.process_and_decisions"></a>
## 3. Process and decisions

Design handoffs from customer request through solution approval, implementation, change, service incident and financial/operational reporting. Work cannot cross a handoff without a stable artifact ID, evidence, recipient, acceptance state and escalation. Define decision rights for production promotion, policy exception, major incident command, supplier termination and residual risk. Separation of duties is maintained: implementer, independent reviewer, risk owner and recipient remain distinct where required.

### Worked design matrix (synthetic)

| Decision area | Accountable target role | Evidence / review | Acceptance risk |
|---|---|---|---|
| Service outcomes | Group Payments Executive | Outcome scorecard | Unverified baseline |
| Technical service | Critical Service Operations Director | Operational rehearsal | No staffed response |
| Security exception | Enterprise Financial Risk Officer | Signed risk disposition | Author conflict |
| Change approval | Separate release authority | Change record + build digest | Unreviewed release |

The matrix is a proposed verification instrument for **cross-border settlement instruction processing and finality reconciliation**. Its displayed rows are not actual enterprise observations. Evidence must be source-bound and independently interpreted before a finding or green status can support a project decision.

<a id="dcs-proposed-target-operating-model.organization_skills"></a>
## 4. Organization skills

People/organization dimension includes named role profiles, skills gap assessment, on-call coverage, support and training. For **treasury control, regional settlement teams, regulators where applicable, resilience and security operations**, assign adoption leaders and accountable local process owners, and avoid implying training attendance proves proficiency. Vendor transition must include runbooks, access recovery, knowledge-transfer rehearsal and contract exit triggers. Complexity level complex: multiple authorities, jurisdictional decisions and non-reversible business boundaries. A single unstaffed control role can invalidate an otherwise plausible TOM.

<a id="dcs-proposed-target-operating-model.controls_and_measurement"></a>
## 5. Controls and measurement

Measure outcomes, not activities: **finality reconciliation exceptions, policy-denied jurisdiction routes and settlement cut-off lag**, change failure rate, recovery to **30 minutes/5 minutes**, access-review completion with actual evidence, financial variance and adoption expressed as correct use. Attach metric definitions, denominators, observation windows, owner and response thresholds. Use a service scorecard distinguishing implemented, observed, accepted and retired capabilities. An SLO target is not a service-level agreement absent a validated service scope and competent approval.

### Dependency and challenge analysis

For OPG-RSM, a release or transformation claim is invalid if **legal applicability by entity, immutable evidence, HSM policy, finality and regional cut-off controls** remains unresolved. Check the counterfactual: what would break if the preferred technology were removed while user behavior and business service demand stayed constant? An independent reviewer should challenge the alleged root cause, hidden vendor commitments, failures spanning channel boundary → policy decision → immutable journal → regulated ledger and regional processors, and who accepts an unsuccessful delivery when the sponsor and implementer disagree.

<a id="dcs-proposed-target-operating-model.transition_acceptance"></a>
## 6. Transition acceptance

Transition from current RACI to target authority through supervised coexistence, staged service acceptance, incident drill and supplier switchovers. A TOM becomes operational only when the receiving team can operate the exact deployed service independently and all material risks have authorized dispositions. Example decision is **CONDITIONAL PROPOSAL**; no staffing commitment, L0 approval or real operating metrics exist in this reference.

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

**Methodological reference:** ITIL service value thinking and accountable enterprise operating-model design. These frameworks inform professional coverage and challenge questions; this reference does not assert compliance or quote normative control clauses.

**Professional review disposition:** OPEN. No actual implementation, live provider validation, signed security assessment, executive approval or legal determination occurred.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `OPG-RSM` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Accountable operating role and decision right | Is this statement supported for `OPG-RSM` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Capability/process interface | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Operational acceptance measure | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — baseline-to-target value bridge

Capture an attributable as-is metric and source system, target metric and accountable benefit owner. A future target is not a measured present capability. For **target-operating-model**, the reviewer should actively challenge **accountable operating role and decision right** and **capability/process interface**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — transition states

Track current, interim and target states with entry/exit criteria, service continuity, legacy retirement and irreversible data conversion boundaries. The accountable party for this illustrative acceptance is **Transformation Sponsor / Receiving Operations Owner**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** accountable operating role and decision right, capability/process interface, and operational acceptance measure. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

