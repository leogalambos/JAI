# SIAM / multi-supplier service integration

**Trigger.** A service depends on multiple suppliers/teams and end-to-end accountability, OLAs, incidents, problems, changes or acceptance are fragmented across boundaries.

**Outcome.** One governed service-integration model joins supplier responsibilities into end-to-end service outcomes with measurable SLAs/OLAs, clear process ownership and cross-supplier escalation.

## Mandatory artefacts

- SIAM operating model
- SLA/OLA matrix
- Dependency register
- Cross-supplier incident model
- Cross-supplier problem model
- Integrated change calendar
- Escalation matrix
- Shared service acceptance

## Chain

| Step | Accountable role | Does | Hands over | Mandatory artefact | Gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | **SIAM Manager** | defines end-to-end service scope, integrator authority and supplier responsibility model | SIAM operating model | SIAM operating model | No customer outcome or integration process is ownerless |
| 2 | **Service Level Manager** | decomposes customer SLA into measurable OLAs/underpinning supplier obligations | SLA/OLA matrix | SLA/OLA matrix | Every SLA has sufficient underpinning measures/owners |
| 3 | **Architecture Repository and Modelling Lead** | maintains cross-supplier service/technology/dependency model | shared dependency register/view set | Dependency register | Material supplier/service dependencies have stable IDs and owners |
| 4 | **Incident Manager** | defines cross-supplier incident ownership, bridge, evidence and handoff rules | cross-supplier incident model | Cross-supplier incident model | Severity and service restoration ownership cannot bounce between suppliers |
| 5 | **Problem Manager** | owns systemic problem process across supplier boundaries | cross-supplier problem model | Cross-supplier problem model | Root causes crossing contracts still receive one end-to-end owner |
| 6 | **Enterprise Release Manager** | integrates supplier change/release windows, collisions and readiness | integrated change/release calendar | Integrated change calendar | Cross-supplier change collisions and blackout constraints are governed |
| 7 | **SIAM Manager** | defines dispute/escalation clocks, evidence standard and decision authority | supplier escalation matrix | Escalation matrix | Escalation cannot be blocked by contractual ownership ambiguity |
| 8 | **IT Service Owner** | accepts the integrated service and residual multi-supplier risks | shared service acceptance | Shared service acceptance | Service acceptance is end-to-end, not a collection of supplier self-attestations |

## Control semantics

- A gate is blocking unless a named authority with the required decision right records an explicit waiver, rationale, expiry/review date and residual risk.
- A handoff is not complete because a document exists; the receiving role must be able to verify the acceptance condition from attributable evidence.
- Producer, approver and independent assurance responsibilities remain separated where the decision is consequential.
- Workflow order may branch or loop, but skipped steps and their unmet gates remain visible.
- Material claims/decisions use stable IDs and trace to evidence so Behavioral Quality evaluation can measure coverage and unsupported claims.
