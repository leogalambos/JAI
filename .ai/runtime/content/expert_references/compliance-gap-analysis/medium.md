---
reference_id: example:compliance-gap-analysis:medium
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: compliance-gap-analysis
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/compliance-gap-analysis
dcs_status: proposed-unmapped
approval_status: not-human-approved
---

> **ILLUSTRATIVE AI-AUTHORED EXPERT REFERENCE — NOT APPROVED OR EXECUTED.** The organisation, systems, costs, results, identifiers and roles are fictional. This is an engineering teaching example, not operational evidence, legal advice or an assurance opinion. Any proposed DCS anchors below require mapping and approval before becoming normative.

**Synthetic case:** Crestline Insurance Services · Enterprise identity entitlement consolidation (`CIS-IAM`). **Complexity:** medium. **Business authority:** Security Architecture Authority.

# Compliance Gap Analysis — Enterprise identity entitlement consolidation

## Scope and case assumptions

This example concerns **enterprise identity entitlement consolidation**, with a boundary covering **HR, directory, SaaS apps, privileged access and ticketing**. The intended business outcome is to **simplify access approval while preserving separation of duties**. The governing constraints are **outsourced operations, multiple identity sources, sensitive claims records**. The selected working direction is **policy-governed entitlements and reconciliation**, subject to independent verification and the authority that would actually own the decision.

The principal unacceptable failure scenario is **wrong-entity claims entitlement on role change**. A working indicator is **critical access revocation < 60 minutes**; its definition, collection method and baseline would need to be validated before treating it as a contractual or delivery target. All mentioned events and outcomes are hypothetical, not observed.

<a id="dcs-proposed-compliance-gap-analysis.applicability"></a>
## Obligation applicability and control universe

Determine the legal entity, jurisdiction, service and effective date to which each obligation applies. Record the source, controlling version, accountable interpretation and relevant exclusions. A crosswalk is not a legal opinion; do not copy a standard checklist and declare every item binding. Identify overlapping obligations and the authoritative baseline for each.

**Case application:** The accountable Security Architecture Authority must confirm whether the objective and boundary are materially complete for `CIS-IAM`. The fact that a sample shows a proposed owner does not delegate any actual organizational authority.

<a id="dcs-proposed-compliance-gap-analysis.mapping"></a>
## Requirement-to-control-to-evidence mapping

Trace obligation → specific requirement → control objective → implemented control → observed evidence → accountable owner. Do not confuse a documented policy with proof that it operated. For each control assign coverage status as covered, partially covered, uncovered, not assessed or not applicable with rationale. Evidence freshness and independence are first-class properties, not footnotes.

**Case application:** For **HR, directory, SaaS apps, privileged access and ticketing**, the specification must document how wrong-entity claims entitlement on role change could arise and what evidence would disprove or confirm that exposure. This remains an explicit open question, not a completed design validation.

<a id="dcs-proposed-compliance-gap-analysis.gap_analysis"></a>
## Finding and severity evaluation

| Obligation area | Illustrative evidence state | Gap | Severity basis |
|---|---|---|---|
| Privileged access | Policy exists; sample unavailable | Effectiveness unproven | Sensitive access potential |
| Data retention | Legal mapping incomplete | Applicability unresolved | Jurisdiction-dependent impact |
| Restore capability | Recovery plan but no test | Operating assurance missing | Business continuity exposure |
| Vendor oversight | Contracts mapped partially | Supplier accountability gap | Service criticality |

Severity is a risk-driven judgment requiring authorized interpretation.

<a id="dcs-proposed-compliance-gap-analysis.remediation"></a>
## Remediation design and accountable priorities

Prioritize gaps by legal impact, business exposure, control dependency and remediation time. Assign accountable owners, interim compensating measures, deadlines and evidence to demonstrate closure. Separate immediate containment, durable design change and long-term governance improvement. A policy exception cannot neutralize an external legal obligation, and escalation to legal/compliance must be explicit where applicability is unresolved.

**Case-specific constraint:** Outsourced operations, multiple identity sources, sensitive claims records. Document the decision that narrows this constraint, the owner of any exception and the consequences of a failed assumption. The safe default is to defer irreversible commitments until a competent owner has reviewed the evidence.

<a id="dcs-proposed-compliance-gap-analysis.closure"></a>
## Independent assurance and residual uncertainty

Require independent verification of new control evidence before closing a material gap. Retain historical findings, evidence revisions and signed disposition for audit. State uncertainties as questions rather than inventing affirmative applicability conclusions. Update the gap register after regulatory changes or a system boundary change, and track accepted residual exposure under the existing governance authority.

## Worked decision/control matrix

| Mapping | Evidence state | Action |
|---|---|---|
| Obligation -> control | Mapped, not necessarily met | Confirm applicability |
| Control -> operation | Owner and implemented location | Inspect operation |
| Operation -> evidence | Observed/absent/expired | Acquire valid proof |
| Finding -> closure | Unresolved until independently verified | Retest |

This matrix is an illustrative analytical artifact, not a list of completed implementation tasks or observed test outcomes. Each row must be connected to the actual project source and accountable receiving role before operational use.

## Complexity-specific engineering considerations

The rollout spans independently owned systems and therefore requires consumer-driven contract tests, country or business-unit boundary checks, supplier escalation and a backlog reconciliation method. A green application health check is insufficient if integration state or business results are inconsistent. The chosen wave must have an operations recipient and measurable stabilization criteria.

### Interfaces, dependencies and operational boundaries

The proposed transformation connects **HR, directory, SaaS apps, privileged access and ticketing**. Establish an authoritative contract for data owner, schema version, retries, failure observability, identity scope and recovery responsibilities. Each integration crosses an operational boundary that requires a named recipient and current documentation; a vendor support promise does not replace an internal business decision.

Record how a planned change can fail halfway through. For data-bearing transitions, a successful service restart does not prove consistency, and restoring an older deployment cannot undo already accepted business events. Build a reconciliation step into the receiving acceptance and document the residual uncertainty left after testing.

### Structured dependency and handoff record

| Dependency | Responsible role | Before proceeding | If unavailable |
|---|---|---|---|
| Business state | Security Architecture Authority | Verified current state and signed scope | Defer irreversible step |
| Identity and policy | Security / IAM owner | Negative test of cross-boundary access | Block restricted operation |
| Operational evidence | Service Owner | Current SLI, support rota and recovery proof | Retain previous stable service |
| Supplier/contract | Vendor Manager | Confirmed escalation and exit provisions | Escalate procurement risk |


## Evidence status, exception handling and downstream traceability

All references below are **hypothetical placeholders**, not assertions that work has been performed. Proposed record `CIS-IAM-REQ-01` defines the validated business objective; `CIS-IAM-RISK-01` describes wrong-entity claims entitlement on role change; `CIS-IAM-DEC-01` captures the selected option and authority; `CIS-IAM-TEST-01` must eventually contain independently observable test evidence; `CIS-IAM-OPS-01` records acceptance into operation.

A production author must replace assumptions with trustworthy evidence, explicitly preserve missing information and seek the authorized decision when risk, finance, privacy or statutory interpretation exceeds the writer’s authority. A synthetic document must never be promoted to human-approved status by automatic checks or by using an LLM reviewer.

**Disposition:** illustrative draft only; no L0 authorization exists. Reassess when requirements, jurisdiction, supplier contracts, business volume or material security assumptions change. The recommended next step is independent verification of the most decision-sensitive uncertainty, not unconditional implementation.


## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `MRG-OEI` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Applicable clause/version and applicability owner | Is this statement supported for `MRG-OEI` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Control/evidence gap | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Remediation and independent closure | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — implementable contract

Specify the business invariant, interface/state schema, trust boundary, failure mode and explicit test oracle before claiming build readiness. For **compliance-gap-analysis**, the reviewer should actively challenge **applicable clause/version and applicability owner** and **control/evidence gap**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — trace to executable evidence

Link requirement → design choice → acceptance scenario → expected business output; HTTP status alone does not demonstrate correct business processing. The accountable party for this illustrative acceptance is **Technical Lead / Independent QA**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** applicable clause/version and applicability owner, control/evidence gap, and remediation and independent closure. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

