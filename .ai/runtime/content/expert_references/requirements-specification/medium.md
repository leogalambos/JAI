---
reference_id: example:requirements-specification:medium
schema_version: '1.0.0'
content_revision: 2.0.0
document_kind: requirements-specification
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/requirements-specification
dcs_status: proposed-unmapped
approval_status: not-human-approved
---

> **ILLUSTRATIVE AI-AUTHORED EXPERT REFERENCE — NOT APPROVED OR EXECUTED.** The organisation, systems, costs, results, identifiers and roles are fictional. This is an engineering teaching example, not operational evidence, legal advice or an assurance opinion. Any proposed DCS anchors below require mapping and approval before becoming normative.

**Synthetic case:** Crestline Insurance Services · Enterprise identity entitlement consolidation (`CIS-IAM`). **Complexity:** medium. **Business authority:** Security Architecture Authority.

# Requirements Specification — Enterprise identity entitlement consolidation

## Scope and case assumptions

This example concerns **enterprise identity entitlement consolidation**, with a boundary covering **HR, directory, SaaS apps, privileged access and ticketing**. The intended business outcome is to **simplify access approval while preserving separation of duties**. The governing constraints are **outsourced operations, multiple identity sources, sensitive claims records**. The selected working direction is **policy-governed entitlements and reconciliation**, subject to independent verification and the authority that would actually own the decision.

The principal unacceptable failure scenario is **wrong-entity claims entitlement on role change**. A working indicator is **critical access revocation < 60 minutes**; its definition, collection method and baseline would need to be validated before treating it as a contractual or delivery target. All mentioned events and outcomes are hypothetical, not observed.

<a id="dcs-proposed-requirements-specification.business_problem"></a>
## Problem, actors and operating scenarios

Define the business problem and intended capability in user-observable terms. Identify actors, process initiation and completion, normal and exceptional flows, jurisdiction and data ownership. Record the baseline and success criteria before decomposing into solution requirements. A requirements specification must distinguish stakeholder wishes, constraints and binding obligations from possible implementation patterns; premature commitment to a vendor or protocol is a design decision requiring separate justification.

**Case application:** The accountable Security Architecture Authority must confirm whether the objective and boundary are materially complete for `CIS-IAM`. The fact that a sample shows a proposed owner does not delegate any actual organizational authority.

<a id="dcs-proposed-requirements-specification.functional_requirements"></a>
## Functional behavior and acceptance

Specify each functional requirement with stable ID, trigger, precondition, input, processing rule, output, exception response and acceptance oracle. Test duplicates, retries, partial failure, cancellation, race conditions and out-of-order events where the business process warrants them. Avoid requirements such as “the system will be intuitive”: express a task, user cohort and observable outcome. Keep a trace from business objective through requirement to design, test and operational runbook.

**Case application:** For **HR, directory, SaaS apps, privileged access and ticketing**, the specification must document how wrong-entity claims entitlement on role change could arise and what evidence would disprove or confirm that exposure. This remains an explicit open question, not a completed design validation.

<a id="dcs-proposed-requirements-specification.quality_constraints"></a>
## Quality attributes and regulatory constraints

Quantify service objectives as SLI/SLO with measurement windows, load profile and allowed exclusions. Address data integrity, confidentiality, availability, recoverability, accessibility and auditability proportional to risk. A privacy obligation must be accompanied by a documented applicability decision, not a generic claim that GDPR applies to every field. State the source and owner of constraints, and record when a requirement is still provisional.

<a id="dcs-proposed-requirements-specification.traceability_priorities"></a>
## Prioritization and change control

Rank requirements by business criticality, dependency, risk and feasibility, not by analyst preference. Use must/should/could only with rationale and release trade-off. Maintain a conflict register for mutually incompatible quality attributes, such as single-digit latency and synchronous global financial confirmation. Track versioned acceptance baselines and require authorization when a material requirement changes after design or test approval.

**Case-specific constraint:** Outsourced operations, multiple identity sources, sensitive claims records. Document the decision that narrows this constraint, the owner of any exception and the consequences of a failed assumption. The safe default is to defer irreversible commitments until a competent owner has reviewed the evidence.

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

