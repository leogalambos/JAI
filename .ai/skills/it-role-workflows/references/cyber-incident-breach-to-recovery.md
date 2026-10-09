# Cyber incident / breach to recovery

**Trigger.** A suspected or confirmed cyber incident may affect systems, data, customers, regulatory obligations or business operations.

**Outcome.** The incident is contained and eradicated, evidence is preserved, recovery is accepted by the business, notification decisions are traceable, and control remediation is closed or owned.

## Mandatory artefacts

- Incident record
- Evidence register
- Incident timeline
- Impact assessment
- Breach / notification decision
- Recovery acceptance
- Lessons learned
- Control remediation plan

## Chain

| Step | Accountable role | Does | Hands over | Mandatory artefact | Gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | **Security Analyst Tier 1** | detects and records the alert/incident with initial facts and provenance | incident record with source/time/scope | Incident record | A real event or explicit false-positive rationale is recorded |
| 2 | **Incident Responder** | triages severity, scope, likely attack path and immediate priorities | triage decision and containment objectives | Incident record | Severity/scope have evidence and an accountable incident lead |
| 3 | **Incident Responder** | contains affected assets/accounts while preserving reversibility and evidence | containment actions and status | Incident timeline | Containment does not destroy material evidence without authority |
| 4 | **Digital Forensics Examiner** | preserves and validates forensic evidence, chain of custody and timeline facts | evidence register and forensic timeline | Evidence register | Evidence integrity, time source and custody are documented |
| 5 | **IT Risk Manager** | assesses business, service, security and regulatory impact using verified facts | impact assessment with uncertainty and affected obligations | Impact assessment | Critical impact claims distinguish confirmed fact from inference |
| 6 | **Data Protection Officer** | performs privacy/breach assessment and coordinates legal/regulatory decision inputs | breach/notification decision basis | Breach / notification decision | Notification/non-notification has correct authority, clock and evidence |
| 7 | **Incident Responder** | eradicates malicious persistence/root causes and verifies the environment | eradication evidence and residual technical risks | Control remediation plan | Known persistence and exploited control gaps are addressed or explicitly owned |
| 8 | **Disaster Recovery Coordinator** | coordinates recovery sequencing, integrity validation and rollback/fallback readiness | recovery evidence and service restoration status | Recovery acceptance | Recovery uses trusted state/data and respects RTO/RPO/business priorities |
| 9 | **IT Service Owner** | validates business/service recovery and accepts restored operating state | business recovery acceptance | Recovery acceptance | Service owner confirms agreed validation signals and residual limitations |
| 10 | **Crisis Manager** | coordinates customer/regulator/executive communications decision and timing where required | communication/regulatory action record | Breach / notification decision | Communications are authorised, consistent and evidence-based |
| 11 | **Problem Manager** | runs lessons learned/root-cause analysis across people/process/technology | lessons learned and systemic findings | Lessons learned | Findings address causes and failed controls, not only symptoms |
| 12 | **Control Owner** | owns control remediation, target dates and evidence of completion | control remediation plan | Control remediation plan | Every material finding has a control owner, due date and verification method |
| 13 | **Internal IT Auditor** | independently verifies closure evidence for material incidents where governance requires | closure assurance result | Control remediation plan | No open critical finding is silently closed or self-assured |

## Control semantics

- A gate is blocking unless a named authority with the required decision right records an explicit waiver, rationale, expiry/review date and residual risk.
- A handoff is not complete because a document exists; the receiving role must be able to verify the acceptance condition from attributable evidence.
- Producer, approver and independent assurance responsibilities remain separated where the decision is consequential.
- Workflow order may branch or loop, but skipped steps and their unmet gates remain visible.
- Material claims/decisions use stable IDs and trace to evidence so Behavioral Quality evaluation can measure coverage and unsupported claims.
