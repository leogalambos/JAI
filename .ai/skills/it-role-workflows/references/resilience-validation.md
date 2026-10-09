# Resilience validation

**Trigger.** A critical service or architecture needs evidence that resilience, RTO/RPO and dependency assumptions work under realistic failure.

**Outcome.** Business criticality, dependencies and recovery objectives are validated through exercised failure scenarios, findings are remediated and retested, and residual resilience risk is accepted by the correct authority.

## Mandatory artefacts

- Business criticality baseline
- Dependency/failure-domain model
- Validated RTO/RPO register
- Resilience design
- Exercise plan
- Exercise evidence
- Findings register
- Remediation plan
- Retest result
- Resilience acceptance

## Chain

| Step | Accountable role | Does | Hands over | Mandatory artefact | Gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | **Business Continuity Manager** | confirms business criticality, impact tolerances and priority services/processes | business criticality baseline | Business criticality baseline | Criticality and tolerances have business ownership |
| 2 | **Operational and Technology Resilience Architect** | maps technical/supplier/data dependencies and correlated failure domains | dependency/failure-domain model | Dependency/failure-domain model | No critical path has an unknown/unowned dependency |
| 3 | **Disaster Recovery Coordinator** | validates RTO/RPO and recovery sequencing against dependency reality | validated recovery objectives | Validated RTO/RPO register | Objectives are feasible end to end, not only per component |
| 4 | **Operational and Technology Resilience Architect** | defines resilience/recovery architecture and degradation patterns | resilience design with failure assumptions | Resilience design | Design addresses single/shared failure modes and measurable outcomes |
| 5 | **Test Manager** | builds the exercise plan, entry/exit criteria, injects and evidence capture method | approved exercise plan | Exercise plan | Test design can falsify the resilience claims and protects production safety |
| 6 | **Chaos and Resilience Engineer** | executes authorised failure experiments/exercises and captures telemetry | exercise evidence | Exercise evidence | Execution matches approved scope and evidence is attributable |
| 7 | **Control Tester** | independently evaluates evidence and records control/resilience findings | findings register | Findings register | Findings distinguish observation, criterion, impact and evidence |
| 8 | **Operational and Technology Resilience Architect** | coordinates owned remediation across architecture, operations and suppliers | remediation plan | Remediation plan | Every material finding has owner/date/design response |
| 9 | **Test Manager** | retests failed claims after remediation using comparable criteria | retest result | Retest result | Critical findings are demonstrated fixed, not administratively closed |
| 10 | **IT Service Owner** | accepts demonstrated resilience or explicitly accepts residual risk within authority | resilience acceptance | Resilience acceptance | Acceptance states evidence, residual risk and next validation date |

## Control semantics

- A gate is blocking unless a named authority with the required decision right records an explicit waiver, rationale, expiry/review date and residual risk.
- A handoff is not complete because a document exists; the receiving role must be able to verify the acceptance condition from attributable evidence.
- Producer, approver and independent assurance responsibilities remain separated where the decision is consequential.
- Workflow order may branch or loop, but skipped steps and their unmet gates remain visible.
- Material claims/decisions use stable IDs and trace to evidence so Behavioral Quality evaluation can measure coverage and unsupported claims.
