---
reference_id: example:compliance-gap-analysis:simple
schema_version: '1.0.0'
content_revision: 2.0.0
document_kind: compliance-gap-analysis
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/compliance-gap-analysis
dcs_status: proposed-unmapped
approval_status: not-human-approved
---

> **ILLUSTRATIVE AI-AUTHORED EXPERT REFERENCE — NOT APPROVED OR EXECUTED.** The organisation, systems, costs, results, identifiers and roles are fictional. This is an engineering teaching example, not operational evidence, legal advice or an assurance opinion. Any proposed DCS anchors below require mapping and approval before becoming normative.

**Synthetic case:** Northbridge Library Trust · Access lifecycle for 1300 staff and contractors (`NLT-ID`). **Complexity:** simple. **Business authority:** Head of Digital Services.

# Compliance Gap Analysis — Access lifecycle for 1300 staff and contractors

## Scope and case assumptions

This example concerns **access lifecycle for 1300 staff and contractors**, with a boundary covering **cloud identity provider, HR feed and helpdesk**. The intended business outcome is to **remove stale privileged access without disrupting public services**. The governing constraints are **shift work, volunteer identities, constrained identity team**. The selected working direction is **phased identity recertification with accountable sponsors**, subject to independent verification and the authority that would actually own the decision.

The principal unacceptable failure scenario is **orphaned contractor access**. A working indicator is **100% privileged exits reviewed within 24 hours**; its definition, collection method and baseline would need to be validated before treating it as a contractual or delivery target. All mentioned events and outcomes are hypothetical, not observed.

<a id="dcs-proposed-compliance-gap-analysis.applicability"></a>
## Obligation applicability and control universe

Determine the legal entity, jurisdiction, service and effective date to which each obligation applies. Record the source, controlling version, accountable interpretation and relevant exclusions. A crosswalk is not a legal opinion; do not copy a standard checklist and declare every item binding. Identify overlapping obligations and the authoritative baseline for each.

**Case application:** The accountable Head of Digital Services must confirm whether the objective and boundary are materially complete for `NLT-ID`. The fact that a sample shows a proposed owner does not delegate any actual organizational authority.

<a id="dcs-proposed-compliance-gap-analysis.mapping"></a>
## Requirement-to-control-to-evidence mapping

Trace obligation → specific requirement → control objective → implemented control → observed evidence → accountable owner. Do not confuse a documented policy with proof that it operated. For each control assign coverage status as covered, partially covered, uncovered, not assessed or not applicable with rationale. Evidence freshness and independence are first-class properties, not footnotes.

**Case application:** For **cloud identity provider, HR feed and helpdesk**, the specification must document how orphaned contractor access could arise and what evidence would disprove or confirm that exposure. This remains an explicit open question, not a completed design validation.

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

**Case-specific constraint:** Shift work, volunteer identities, constrained identity team. Document the decision that narrows this constraint, the owner of any exception and the consequences of a failed assumption. The safe default is to defer irreversible commitments until a competent owner has reviewed the evidence.

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

Risk appetite is intentionally narrow: a small service team cannot support a control requiring continuous manual monitoring. Prefer a reversible small cohort, a one-page acceptance record and direct operational proof. The limited environment should reduce obligations, not erase them: access controls, state integrity and recovery still need testable outcomes.

## Evidence status, exception handling and downstream traceability

All references below are **hypothetical placeholders**, not assertions that work has been performed. Proposed record `NLT-ID-REQ-01` defines the validated business objective; `NLT-ID-RISK-01` describes orphaned contractor access; `NLT-ID-DEC-01` captures the selected option and authority; `NLT-ID-TEST-01` must eventually contain independently observable test evidence; `NLT-ID-OPS-01` records acceptance into operation.

A production author must replace assumptions with trustworthy evidence, explicitly preserve missing information and seek the authorized decision when risk, finance, privacy or statutory interpretation exceeds the writer’s authority. A synthetic document must never be promoted to human-approved status by automatic checks or by using an LLM reviewer.

**Disposition:** illustrative draft only; no L0 authorization exists. Reassess when requirements, jurisdiction, supplier contracts, business volume or material security assumptions change. The recommended next step is independent verification of the most decision-sensitive uncertainty, not unconditional implementation.

