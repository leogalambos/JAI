---
reference_id: example:service-design-sla:simple
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: service-design-sla
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/service-design-sla
dcs_status: proposed-unmapped
approval_status: not-human-approved
---

> **ILLUSTRATIVE AI-AUTHORED EXPERT REFERENCE — NOT APPROVED OR EXECUTED.** The organisation, systems, costs, results, identifiers and roles are fictional. This is an engineering teaching example, not operational evidence, legal advice or an assurance opinion. Any proposed DCS anchors below require mapping and approval before becoming normative.

**Synthetic case:** Clearwater Municipal IT · Change-controlled update of shared workplace services (`CMI-PATCH`). **Complexity:** simple. **Business authority:** IT Service Owner.

# Service Design & SLA — Change-controlled update of shared workplace services

## Scope and case assumptions

This example concerns **change-controlled update of shared workplace services**, with a boundary covering **endpoint platform, directory and monitoring suite**. The intended business outcome is to **reduce exposure and support disruption through repeatable maintenance**. The governing constraints are **mixed legacy clients, municipal change windows and public access**. The selected working direction is **canary rollout with preflight and restore proof**, subject to independent verification and the authority that would actually own the decision.

The principal unacceptable failure scenario is **failed rollback after configuration drift**. A working indicator is **critical patch conformance above 98%**; its definition, collection method and baseline would need to be validated before treating it as a contractual or delivery target. All mentioned events and outcomes are hypothetical, not observed.

<a id="dcs-proposed-service-design-sla.service_value"></a>
## Service definition and customer outcomes

Define service consumers, business capability enabled, catalog boundary, eligibility and explicit exclusions. Separate internal technology components from the outcome experienced by the consumer. Establish supported locations, hours, priority classes, cost model and retained responsibilities across suppliers. The service design must not imply a contract commitment until the authorized parties have agreed to it.

**Case application:** The accountable IT Service Owner must confirm whether the objective and boundary are materially complete for `CMI-PATCH`. The fact that a sample shows a proposed owner does not delegate any actual organizational authority.

<a id="dcs-proposed-service-design-sla.sli_slo"></a>
## Service levels and measurement contract

Define SLI numerators and denominators, collection sources, observation windows, exclusions and breach-handling policy. A 99.95% target is meaningless without specifying service minutes and allowable unavailability. Map customer-facing SLAs to internal SLOs and OLAs with sufficient margin. For latency, specify percentile, transaction class and threshold rather than using an unexplained “fast response” objective.

**Case application:** For **endpoint platform, directory and monitoring suite**, the specification must document how failed rollback after configuration drift could arise and what evidence would disprove or confirm that exposure. This remains an explicit open question, not a completed design validation.

<a id="dcs-proposed-service-design-sla.support_operating_model"></a>
## Support, ownership and observability

Define L1/L2/L3 service support, incident and problem process, supplier escalation, on-call coverage, monitoring dashboards and change ownership. Ensure that a single incident can be routed to an accountable service owner despite multiple technical teams. Include capacity and lifecycle management for infrastructure dependencies; a service design is not complete when the diagram ends at the provider boundary.

<a id="dcs-proposed-service-design-sla.continuity_security"></a>
## Continuity, security and information obligations

State critical service dependencies, RTO/RPO, recovery strategy and actual verification obligations. Define data classification and jurisdiction handling; map controls and retention to authoritative policy. Avoid assuming that vendor marketing availability implies end-to-end service resilience. Describe exit, portability, data destruction and continuing evidence retention at contract end.

**Case-specific constraint:** Mixed legacy clients, municipal change windows and public access. Document the decision that narrows this constraint, the owner of any exception and the consequences of a failed assumption. The safe default is to defer irreversible commitments until a competent owner has reviewed the evidence.

<a id="dcs-proposed-service-design-sla.service_acceptance"></a>
## Service acceptance and change governance

Define requirements for service acceptance, knowledge handover and SLA commencement. Contractual SLA breach processes must align with actual monitoring and agreed measurement dispute resolution. Establish periodic service review, improvement backlog, exception management and the authority to revise service levels. Record conditions still subject to supplier negotiation rather than silently treating them as accepted.

## Worked decision/control matrix

| Dimension | Service commitment definition | Operating owner |
|---|---|---|
| Availability | User-observable transaction success / time window | Service Owner |
| Latency | p95 completion time by transaction class | Product Owner |
| Security | Reviewed identity and data boundary | Security Owner |
| Continuity | Measured RTO/RPO for business state | Resilience Owner |

This matrix is an illustrative analytical artifact, not a list of completed implementation tasks or observed test outcomes. Each row must be connected to the actual project source and accountable receiving role before operational use.

## Complexity-specific engineering considerations

Risk appetite is intentionally narrow: a small service team cannot support a control requiring continuous manual monitoring. Prefer a reversible small cohort, a one-page acceptance record and direct operational proof. The limited environment should reduce obligations, not erase them: access controls, state integrity and recovery still need testable outcomes.

## Evidence status, exception handling and downstream traceability

All references below are **hypothetical placeholders**, not assertions that work has been performed. Proposed record `CMI-PATCH-REQ-01` defines the validated business objective; `CMI-PATCH-RISK-01` describes failed rollback after configuration drift; `CMI-PATCH-DEC-01` captures the selected option and authority; `CMI-PATCH-TEST-01` must eventually contain independently observable test evidence; `CMI-PATCH-OPS-01` records acceptance into operation.

A production author must replace assumptions with trustworthy evidence, explicitly preserve missing information and seek the authorized decision when risk, finance, privacy or statutory interpretation exceeds the writer’s authority. A synthetic document must never be promoted to human-approved status by automatic checks or by using an LLM reviewer.

**Disposition:** illustrative draft only; no L0 authorization exists. Reassess when requirements, jurisdiction, supplier contracts, business volume or material security assumptions change. The recommended next step is independent verification of the most decision-sensitive uncertainty, not unconditional implementation.


## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `HFS-FAR` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Service boundary and customer population | Is this statement supported for `HFS-FAR` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Measurable SLI/SLO denominator | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| OLA and response owner | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — service boundary

State service, covered tenant/region, in-scope components, excluded suppliers, accountable service owner and observability boundary. For **service-design-sla**, the reviewer should actively challenge **service boundary and customer population** and **measurable sli/slo denominator**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — failure-safe control

Name precise abort or escalation triggers, untested rollback edges and data integrity invariants. Do not treat a green process health probe as business recovery. The accountable party for this illustrative acceptance is **Service Owner / Incident Authority**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** service boundary and customer population, measurable sli/slo denominator, and ola and response owner. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

