---
reference_id: example:incident-postmortem:simple
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: incident-postmortem
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/incident-postmortem
dcs_status: proposed-unmapped
approval_status: not-human-approved
---

> **ILLUSTRATIVE AI-AUTHORED EXPERT REFERENCE — NOT APPROVED OR EXECUTED.** The organisation, systems, costs, results, identifiers and roles are fictional. This is an engineering teaching example, not operational evidence, legal advice or an assurance opinion. Any proposed DCS anchors below require mapping and approval before becoming normative.

**Synthetic case:** Lakeside Service Cooperative · Field service appointments for 220 mobile technicians (`LSC-FSM`). **Complexity:** simple. **Business authority:** Service Operations Director.

# Incident & Postmortem Report — Field service appointments for 220 mobile technicians

## Scope and case assumptions

This example concerns **field service appointments for 220 mobile technicians**, with a boundary covering **dispatch portal, technician mobile app and directory**. The intended business outcome is to **lower missed visits without creating unstaffed support obligations**. The governing constraints are **seasonal demand, unreliable mobile connectivity, small operations team**. The selected working direction is **bounded pilot with auditable offline-resync controls**, subject to independent verification and the authority that would actually own the decision.

The principal unacceptable failure scenario is **double booking after offline resync**. A working indicator is **p95 appointment confirmation < 3 minutes**; its definition, collection method and baseline would need to be validated before treating it as a contractual or delivery target. All mentioned events and outcomes are hypothetical, not observed.

<a id="dcs-proposed-incident-postmortem.incident_boundary"></a>
## Incident identity, impact and chronology

State the incident identifier, affected services, customer/business impact, timeline source and reporting clock. Distinguish what is known, inferred and unknown at each point in time. Preserve original raw telemetry references and avoid rewriting early uncertainty after root cause is found. The incident review is a learning and accountability mechanism, not an invitation to fabricate an uninterrupted sequence of perfect decisions.

**Case application:** The accountable Service Operations Director must confirm whether the objective and boundary are materially complete for `LSC-FSM`. The fact that a sample shows a proposed owner does not delegate any actual organizational authority.

<a id="dcs-proposed-incident-postmortem.contain_recovery"></a>
## Containment, restoration and evidence handling

Record actions taken or proposed, authorization, observed effect and reversibility. In a synthetic example, label actions as simulated rather than executed. Cyber incidents require evidence preservation before destructive remediation where lawful and feasible; operational restoration and forensic investigation can have conflicting timing needs. Separate system up-time restoration from validation that transactions and data are correct.

**Case application:** For **dispatch portal, technician mobile app and directory**, the specification must document how double booking after offline resync could arise and what evidence would disprove or confirm that exposure. This remains an explicit open question, not a completed design validation.

<a id="dcs-proposed-incident-postmortem.causal_analysis"></a>
## Causal factors and counterfactuals

Use a causal chain with contributing technical, process and organizational conditions. Avoid reducing a multi-layer outage to one operator action without examining why the system permitted it. Identify which controls should have detected or contained the failure, when they first signaled and why escalation was delayed. Distinguish root-cause evidence from hypotheses requiring a follow-up experiment.

<a id="dcs-proposed-incident-postmortem.action_plan"></a>
## Corrective and preventive action commitments

| Finding | Remedial control | Verification | Owner class |
|---|---|---|---|
| Unbounded retry storm | Backpressure and circuit-breaker guard | Load/failure test | Platform owner |
| Blind support escalation | Tested alert routing and on-call rota | Drill record | Service owner |
| Insufficient audit lineage | Correlated trace IDs and protected retention | Evidence review | Security owner |
| Unsafe rollback | Stateful cutover and reconciliation rehearsal | Recovery drill | Release owner |

**Case-specific constraint:** Seasonal demand, unreliable mobile connectivity, small operations team. Document the decision that narrows this constraint, the owner of any exception and the consequences of a failed assumption. The safe default is to defer irreversible commitments until a competent owner has reviewed the evidence.

<a id="dcs-proposed-incident-postmortem.lessons_followup"></a>
## Learning, recurrence controls and closure

List customer communications, regulatory assessment decisions and service-review follow-ups within authorized policy. Set due dates and evidence required to close actions, plus a periodic check for recurrence. Incident commander and accountable service owner sign off actions separately from approval of underlying risk exceptions. Avoid unqualified guarantees such as “this can never happen again”.

## Worked decision/control matrix

| Moment | Control expected | What investigator must establish |
|---|---|---|
| Detection | Signal and accountable on-call | First actual observation and clock |
| Containment | Reduce customer harm | Side effects and authorisation |
| Recovery | Validate business records | Observed state after restoration |
| Learning | Track durable fixes | Independent verification |

This matrix is an illustrative analytical artifact, not a list of completed implementation tasks or observed test outcomes. Each row must be connected to the actual project source and accountable receiving role before operational use.

## Complexity-specific engineering considerations

Risk appetite is intentionally narrow: a small service team cannot support a control requiring continuous manual monitoring. Prefer a reversible small cohort, a one-page acceptance record and direct operational proof. The limited environment should reduce obligations, not erase them: access controls, state integrity and recovery still need testable outcomes.

## Evidence status, exception handling and downstream traceability

All references below are **hypothetical placeholders**, not assertions that work has been performed. Proposed record `LSC-FSM-REQ-01` defines the validated business objective; `LSC-FSM-RISK-01` describes double booking after offline resync; `LSC-FSM-DEC-01` captures the selected option and authority; `LSC-FSM-TEST-01` must eventually contain independently observable test evidence; `LSC-FSM-OPS-01` records acceptance into operation.

A production author must replace assumptions with trustworthy evidence, explicitly preserve missing information and seek the authorized decision when risk, finance, privacy or statutory interpretation exceeds the writer’s authority. A synthetic document must never be promoted to human-approved status by automatic checks or by using an LLM reviewer.

**Disposition:** illustrative draft only; no L0 authorization exists. Reassess when requirements, jurisdiction, supplier contracts, business volume or material security assumptions change. The recommended next step is independent verification of the most decision-sensitive uncertainty, not unconditional implementation.


## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `HFS-FAR` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Timeline with observed evidence | Is this statement supported for `HFS-FAR` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Contributing causes and counterfactual | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Action owner/retest due date | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — service boundary

State service, covered tenant/region, in-scope components, excluded suppliers, accountable service owner and observability boundary. For **incident-postmortem**, the reviewer should actively challenge **timeline with observed evidence** and **contributing causes and counterfactual**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — failure-safe control

Name precise abort or escalation triggers, untested rollback edges and data integrity invariants. Do not treat a green process health probe as business recovery. The accountable party for this illustrative acceptance is **Service Owner / Incident Authority**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** timeline with observed evidence, contributing causes and counterfactual, and action owner/retest due date. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

