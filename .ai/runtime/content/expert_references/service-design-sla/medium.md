---
reference_id: example:service-design-sla:medium
schema_version: '1.0.0'
content_revision: 2.0.0
document_kind: service-design-sla
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/service-design-sla
dcs_status: proposed-unmapped
approval_status: not-human-approved
---

> **ILLUSTRATIVE AI-AUTHORED EXPERT REFERENCE — NOT APPROVED OR EXECUTED.** The organisation, systems, costs, results, identifiers and roles are fictional. This is an engineering teaching example, not operational evidence, legal advice or an assurance opinion. Any proposed DCS anchors below require mapping and approval before becoming normative.

**Synthetic case:** Bluehaven Healthcare Network · Patient contact-center and CRM modernization (`BHN-CRM`). **Complexity:** medium. **Business authority:** Clinical Digital Owner.

# Service Design & SLA — Patient contact-center and CRM modernization

## Scope and case assumptions

This example concerns **patient contact-center and crm modernization**, with a boundary covering **service CRM, EHR gateway, identity and analytics**. The intended business outcome is to **reduce referral handling time with privacy-preserving workflows**. The governing constraints are **three hospitals, high staff turnover, clinical safety review**. The selected working direction is **segmented rollout with safe data-access controls**, subject to independent verification and the authority that would actually own the decision.

The principal unacceptable failure scenario is **misrouted patient reference in support ticket**. A working indicator is **90% of referrals acknowledged within one business day**; its definition, collection method and baseline would need to be validated before treating it as a contractual or delivery target. All mentioned events and outcomes are hypothetical, not observed.

<a id="dcs-proposed-service-design-sla.service_value"></a>
## Service definition and customer outcomes

Define service consumers, business capability enabled, catalog boundary, eligibility and explicit exclusions. Separate internal technology components from the outcome experienced by the consumer. Establish supported locations, hours, priority classes, cost model and retained responsibilities across suppliers. The service design must not imply a contract commitment until the authorized parties have agreed to it.

**Case application:** The accountable Clinical Digital Owner must confirm whether the objective and boundary are materially complete for `BHN-CRM`. The fact that a sample shows a proposed owner does not delegate any actual organizational authority.

<a id="dcs-proposed-service-design-sla.sli_slo"></a>
## Service levels and measurement contract

Define SLI numerators and denominators, collection sources, observation windows, exclusions and breach-handling policy. A 99.95% target is meaningless without specifying service minutes and allowable unavailability. Map customer-facing SLAs to internal SLOs and OLAs with sufficient margin. For latency, specify percentile, transaction class and threshold rather than using an unexplained “fast response” objective.

**Case application:** For **service CRM, EHR gateway, identity and analytics**, the specification must document how misrouted patient reference in support ticket could arise and what evidence would disprove or confirm that exposure. This remains an explicit open question, not a completed design validation.

<a id="dcs-proposed-service-design-sla.support_operating_model"></a>
## Support, ownership and observability

Define L1/L2/L3 service support, incident and problem process, supplier escalation, on-call coverage, monitoring dashboards and change ownership. Ensure that a single incident can be routed to an accountable service owner despite multiple technical teams. Include capacity and lifecycle management for infrastructure dependencies; a service design is not complete when the diagram ends at the provider boundary.

<a id="dcs-proposed-service-design-sla.continuity_security"></a>
## Continuity, security and information obligations

State critical service dependencies, RTO/RPO, recovery strategy and actual verification obligations. Define data classification and jurisdiction handling; map controls and retention to authoritative policy. Avoid assuming that vendor marketing availability implies end-to-end service resilience. Describe exit, portability, data destruction and continuing evidence retention at contract end.

**Case-specific constraint:** Three hospitals, high staff turnover, clinical safety review. Document the decision that narrows this constraint, the owner of any exception and the consequences of a failed assumption. The safe default is to defer irreversible commitments until a competent owner has reviewed the evidence.

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

The rollout spans independently owned systems and therefore requires consumer-driven contract tests, country or business-unit boundary checks, supplier escalation and a backlog reconciliation method. A green application health check is insufficient if integration state or business results are inconsistent. The chosen wave must have an operations recipient and measurable stabilization criteria.

### Interfaces, dependencies and operational boundaries

The proposed transformation connects **service CRM, EHR gateway, identity and analytics**. Establish an authoritative contract for data owner, schema version, retries, failure observability, identity scope and recovery responsibilities. Each integration crosses an operational boundary that requires a named recipient and current documentation; a vendor support promise does not replace an internal business decision.

Record how a planned change can fail halfway through. For data-bearing transitions, a successful service restart does not prove consistency, and restoring an older deployment cannot undo already accepted business events. Build a reconciliation step into the receiving acceptance and document the residual uncertainty left after testing.

### Structured dependency and handoff record

| Dependency | Responsible role | Before proceeding | If unavailable |
|---|---|---|---|
| Business state | Clinical Digital Owner | Verified current state and signed scope | Defer irreversible step |
| Identity and policy | Security / IAM owner | Negative test of cross-boundary access | Block restricted operation |
| Operational evidence | Service Owner | Current SLI, support rota and recovery proof | Retain previous stable service |
| Supplier/contract | Vendor Manager | Confirmed escalation and exit provisions | Escalate procurement risk |


## Evidence status, exception handling and downstream traceability

All references below are **hypothetical placeholders**, not assertions that work has been performed. Proposed record `BHN-CRM-REQ-01` defines the validated business objective; `BHN-CRM-RISK-01` describes misrouted patient reference in support ticket; `BHN-CRM-DEC-01` captures the selected option and authority; `BHN-CRM-TEST-01` must eventually contain independently observable test evidence; `BHN-CRM-OPS-01` records acceptance into operation.

A production author must replace assumptions with trustworthy evidence, explicitly preserve missing information and seek the authorized decision when risk, finance, privacy or statutory interpretation exceeds the writer’s authority. A synthetic document must never be promoted to human-approved status by automatic checks or by using an LLM reviewer.

**Disposition:** illustrative draft only; no L0 authorization exists. Reassess when requirements, jurisdiction, supplier contracts, business volume or material security assumptions change. The recommended next step is independent verification of the most decision-sensitive uncertainty, not unconditional implementation.

