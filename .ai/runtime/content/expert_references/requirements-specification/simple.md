---
reference_id: example:requirements-specification:simple
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: requirements-specification
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/requirements-specification
dcs_status: proposed-unmapped
approval_status: not-human-approved
---

> **ILLUSTRATIVE AI-AUTHORED EXPERT REFERENCE — NOT APPROVED OR EXECUTED.** The organisation, systems, costs, results, identifiers and roles are fictional. This is an engineering teaching example, not operational evidence, legal advice or an assurance opinion. Any proposed DCS anchors below require mapping and approval before becoming normative.

**Synthetic case:** Northbridge Library Trust · Access lifecycle for 1300 staff and contractors (`NLT-ID`). **Complexity:** simple. **Business authority:** Head of Digital Services.

# Requirements Specification — Access lifecycle for 1300 staff and contractors

## Scope and case assumptions

This example concerns **access lifecycle for 1300 staff and contractors**, with a boundary covering **cloud identity provider, HR feed and helpdesk**. The intended business outcome is to **remove stale privileged access without disrupting public services**. The governing constraints are **shift work, volunteer identities, constrained identity team**. The selected working direction is **phased identity recertification with accountable sponsors**, subject to independent verification and the authority that would actually own the decision.

The principal unacceptable failure scenario is **orphaned contractor access**. A working indicator is **100% privileged exits reviewed within 24 hours**; its definition, collection method and baseline would need to be validated before treating it as a contractual or delivery target. All mentioned events and outcomes are hypothetical, not observed.

<a id="dcs-proposed-requirements-specification.business_problem"></a>
## Problem, actors and operating scenarios

Define the business problem and intended capability in user-observable terms. Identify actors, process initiation and completion, normal and exceptional flows, jurisdiction and data ownership. Record the baseline and success criteria before decomposing into solution requirements. A requirements specification must distinguish stakeholder wishes, constraints and binding obligations from possible implementation patterns; premature commitment to a vendor or protocol is a design decision requiring separate justification.

**Case application:** The accountable Head of Digital Services must confirm whether the objective and boundary are materially complete for `NLT-ID`. The fact that a sample shows a proposed owner does not delegate any actual organizational authority.

<a id="dcs-proposed-requirements-specification.functional_requirements"></a>
## Functional behavior and acceptance

Specify each functional requirement with stable ID, trigger, precondition, input, processing rule, output, exception response and acceptance oracle. Test duplicates, retries, partial failure, cancellation, race conditions and out-of-order events where the business process warrants them. Avoid requirements such as “the system will be intuitive”: express a task, user cohort and observable outcome. Keep a trace from business objective through requirement to design, test and operational runbook.

**Case application:** For **cloud identity provider, HR feed and helpdesk**, the specification must document how orphaned contractor access could arise and what evidence would disprove or confirm that exposure. This remains an explicit open question, not a completed design validation.

<a id="dcs-proposed-requirements-specification.quality_constraints"></a>
## Quality attributes and regulatory constraints

Quantify service objectives as SLI/SLO with measurement windows, load profile and allowed exclusions. Address data integrity, confidentiality, availability, recoverability, accessibility and auditability proportional to risk. A privacy obligation must be accompanied by a documented applicability decision, not a generic claim that GDPR applies to every field. State the source and owner of constraints, and record when a requirement is still provisional.

<a id="dcs-proposed-requirements-specification.traceability_priorities"></a>
## Prioritization and change control

Rank requirements by business criticality, dependency, risk and feasibility, not by analyst preference. Use must/should/could only with rationale and release trade-off. Maintain a conflict register for mutually incompatible quality attributes, such as single-digit latency and synchronous global financial confirmation. Track versioned acceptance baselines and require authorization when a material requirement changes after design or test approval.

**Case-specific constraint:** Shift work, volunteer identities, constrained identity team. Document the decision that narrows this constraint, the owner of any exception and the consequences of a failed assumption. The safe default is to defer irreversible commitments until a competent owner has reviewed the evidence.

<a id="dcs-proposed-requirements-specification.acceptance_model"></a>
## Acceptance specification and open issues

Provide examples in a Given/When/Then style where unambiguous and add negative cases for authorization, resilience and invalid data. The receiving business owner must be able to determine if the requirement has been met by inspecting reproducible observations. Do not equate a passing unit test with demonstrated business acceptance. Maintain a list of unverified assumptions, owner and due date; release work cannot quietly reclassify missing requirements as not applicable.

## Worked decision/control matrix

| ID | Observable requirement | Verification |
|---|---|---|
| BR-01 | Business result measurable by service owner | Agreed operating sample |
| FR-01 | Every accepted update reaches one authoritative business state | Replay / duplicate-state checks |
| NFR-01 | Response timing within stated percentile and workload | Timestamped performance results |
| SEC-01 | Unentitled actor cannot modify another boundary | Negative authorization tests |

This matrix is an illustrative analytical artifact, not a list of completed implementation tasks or observed test outcomes. Each row must be connected to the actual project source and accountable receiving role before operational use.

## Complexity-specific engineering considerations

Risk appetite is intentionally narrow: a small service team cannot support a control requiring continuous manual monitoring. Prefer a reversible small cohort, a one-page acceptance record and direct operational proof. The limited environment should reduce obligations, not erase them: access controls, state integrity and recovery still need testable outcomes.

## Evidence status, exception handling and downstream traceability

All references below are **hypothetical placeholders**, not assertions that work has been performed. Proposed record `NLT-ID-REQ-01` defines the validated business objective; `NLT-ID-RISK-01` describes orphaned contractor access; `NLT-ID-DEC-01` captures the selected option and authority; `NLT-ID-TEST-01` must eventually contain independently observable test evidence; `NLT-ID-OPS-01` records acceptance into operation.

A production author must replace assumptions with trustworthy evidence, explicitly preserve missing information and seek the authorized decision when risk, finance, privacy or statutory interpretation exceeds the writer’s authority. A synthetic document must never be promoted to human-approved status by automatic checks or by using an LLM reviewer.

**Disposition:** illustrative draft only; no L0 authorization exists. Reassess when requirements, jurisdiction, supplier contracts, business volume or material security assumptions change. The recommended next step is independent verification of the most decision-sensitive uncertainty, not unconditional implementation.


## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `HFS-FAR` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Source-authorized business requirement | Is this statement supported for `HFS-FAR` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Testable acceptance oracle | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Conflict and change rule | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — implementable contract

Specify the business invariant, interface/state schema, trust boundary, failure mode and explicit test oracle before claiming build readiness. For **requirements-specification**, the reviewer should actively challenge **source-authorized business requirement** and **testable acceptance oracle**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — trace to executable evidence

Link requirement → design choice → acceptance scenario → expected business output; HTTP status alone does not demonstrate correct business processing. The accountable party for this illustrative acceptance is **Technical Lead / Independent QA**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** source-authorized business requirement, testable acceptance oracle, and conflict and change rule. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

