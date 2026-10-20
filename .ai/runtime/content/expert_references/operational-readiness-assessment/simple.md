---
reference_id: example:operational-readiness-assessment:simple
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: operational-readiness-assessment
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/operational-readiness-assessment
dcs_status: proposed-unmapped
approval_status: not-human-approved
---

> **ILLUSTRATIVE AI-AUTHORED EXPERT REFERENCE — NOT APPROVED OR EXECUTED.** The organisation, systems, costs, results, identifiers and roles are fictional. This is an engineering teaching example, not operational evidence, legal advice or an assurance opinion. Any proposed DCS anchors below require mapping and approval before becoming normative.

**Synthetic case:** Ridgeway Food Logistics · Warehouse slotting and replenishment for 14 depots (`RFL-WMS`). **Complexity:** simple. **Business authority:** Warehouse Operations Head.

# Operational Readiness Assessment — Warehouse slotting and replenishment for 14 depots

## Scope and case assumptions

This example concerns **warehouse slotting and replenishment for 14 depots**, with a boundary covering **warehouse platform, scanners and purchase-order adapter**. The intended business outcome is to **reduce missed pick windows without sacrificing inventory accuracy**. The governing constraints are **legacy handheld devices, nightly supplier files, short maintenance windows**. The selected working direction is **limited-wave replacement with reconciliation checks**, subject to independent verification and the authority that would actually own the decision.

The principal unacceptable failure scenario is **inventory drift during scanner outage**. A working indicator is **inventory mismatch below 0.05% per batch**; its definition, collection method and baseline would need to be validated before treating it as a contractual or delivery target. All mentioned events and outcomes are hypothetical, not observed.

<a id="dcs-proposed-operational-readiness-assessment.operating_scope"></a>
## Service scope and live-support boundary

Define operational scope, interfaces, legal entities, users, business hours, supplier involvement and criticality. Identify who will own the service on day one and who has emergency authority outside normal hours. A launch forecast is not readiness evidence; account for staffing and realistic incident volumes, not only product completion.

**Case application:** The accountable Warehouse Operations Head must confirm whether the objective and boundary are materially complete for `RFL-WMS`. The fact that a sample shows a proposed owner does not delegate any actual organizational authority.

<a id="dcs-proposed-operational-readiness-assessment.technical_readiness"></a>
## Monitoring, security and recovery readiness

Verify service-level indicators, alert ownership, runbooks, identity reviews, backups and demonstrated restore consistency. Check on-call coverage against support hours and technical knowledge transfer. Record evidence status for each item as tested, pending, blocked or not applicable with rationale. Distinguish a documented recovery target from an observed recovery test.

**Case application:** For **warehouse platform, scanners and purchase-order adapter**, the specification must document how inventory drift during scanner outage could arise and what evidence would disprove or confirm that exposure. This remains an explicit open question, not a completed design validation.

<a id="dcs-proposed-operational-readiness-assessment.service_dependencies"></a>
## Supplier and cross-service dependencies

Map incident and change ownership across infrastructure, vendor and application teams. Ensure contract SLAs and OLAs cover the same service and clock windows. Validate capacity, access to support tooling, CMDB mapping, vendor escalation and software entitlements. Missing contractual escalation in a critical chain cannot be assumed solved by an internal contact list.

<a id="dcs-proposed-operational-readiness-assessment.readiness_findings"></a>
## Readiness findings and risk treatment

| Domain | Proof expected | Typical gap | Gate decision |
|---|---|---|---|
| On-call | Staffed escalation schedule | Weekend unstaffed | Defer |
| Recovery | Observed timed restore | No integrity check | Defer |
| Security | Reviewed least-privilege access | Unowned admin identity | Block until resolved |
| Monitoring | Alerts and ownership test | No actionable SLI | Conditional only if noncritical |

Each finding needs an owner, closure evidence and acceptance date.

**Case-specific constraint:** Legacy handheld devices, nightly supplier files, short maintenance windows. Document the decision that narrows this constraint, the owner of any exception and the consequences of a failed assumption. The safe default is to defer irreversible commitments until a competent owner has reviewed the evidence.

<a id="dcs-proposed-operational-readiness-assessment.go_live"></a>
## Go-live recommendation and early-life support

Separate readiness opinion from deployment permission. Recommend go, conditional go or no-go against published gates and name the authority for each exception. Define stabilization measures, heightened monitoring and reversal authority for early-life support. Acceptance into operations is a separate recorded act by the receiving Service Owner.

## Worked decision/control matrix

| Readiness check | Expected evidence | Receiver |
|---|---|---|
| On-call | 24/7 or declared-hours actual staffing | Service Owner |
| Monitoring | Alert routing dry run and SLI definition | Operations |
| Recovery | Restored business state, not just infrastructure | Resilience Owner |
| Vendors | Current support contract and escalation tree | Supplier Manager |

This matrix is an illustrative analytical artifact, not a list of completed implementation tasks or observed test outcomes. Each row must be connected to the actual project source and accountable receiving role before operational use.

## Complexity-specific engineering considerations

Risk appetite is intentionally narrow: a small service team cannot support a control requiring continuous manual monitoring. Prefer a reversible small cohort, a one-page acceptance record and direct operational proof. The limited environment should reduce obligations, not erase them: access controls, state integrity and recovery still need testable outcomes.

## Evidence status, exception handling and downstream traceability

All references below are **hypothetical placeholders**, not assertions that work has been performed. Proposed record `RFL-WMS-REQ-01` defines the validated business objective; `RFL-WMS-RISK-01` describes inventory drift during scanner outage; `RFL-WMS-DEC-01` captures the selected option and authority; `RFL-WMS-TEST-01` must eventually contain independently observable test evidence; `RFL-WMS-OPS-01` records acceptance into operation.

A production author must replace assumptions with trustworthy evidence, explicitly preserve missing information and seek the authorized decision when risk, finance, privacy or statutory interpretation exceeds the writer’s authority. A synthetic document must never be promoted to human-approved status by automatic checks or by using an LLM reviewer.

**Disposition:** illustrative draft only; no L0 authorization exists. Reassess when requirements, jurisdiction, supplier contracts, business volume or material security assumptions change. The recommended next step is independent verification of the most decision-sensitive uncertainty, not unconditional implementation.


## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `HFS-FAR` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Service ownership and runbooks | Is this statement supported for `HFS-FAR` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| RTO/RPO acceptance evidence | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Explicit accept/defer decision | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — service boundary

State service, covered tenant/region, in-scope components, excluded suppliers, accountable service owner and observability boundary. For **operational-readiness-assessment**, the reviewer should actively challenge **service ownership and runbooks** and **rto/rpo acceptance evidence**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — failure-safe control

Name precise abort or escalation triggers, untested rollback edges and data integrity invariants. Do not treat a green process health probe as business recovery. The accountable party for this illustrative acceptance is **Service Owner / Incident Authority**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** service ownership and runbooks, rto/rpo acceptance evidence, and explicit accept/defer decision. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

