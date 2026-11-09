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
| 1 | [Security Analyst Tier 1](../../it-roles-security-operations-and-defensive-security/references/security-analyst-tier-1.md) | detects and records the alert/incident with initial facts and provenance | incident record with source/time/scope | A real event or explicit false-positive rationale is recorded |
| 2 | [Incident Responder](../../it-roles-security-operations-and-defensive-security/references/incident-responder.md) | triages severity, scope, likely attack path and immediate priorities | triage decision and containment objectives | Severity/scope have evidence and an accountable incident lead |
| 3 | [Incident Responder](../../it-roles-security-operations-and-defensive-security/references/incident-responder.md) | contains affected assets/accounts while preserving reversibility and evidence | containment actions and status | Containment does not destroy material evidence without authority |
| 4 | [Digital Forensics Examiner](../../it-roles-security-operations-and-defensive-security/references/digital-forensics-examiner.md) | preserves and validates forensic evidence, chain of custody and timeline facts | evidence register and forensic timeline | Evidence integrity, time source and custody are documented |
| 5 | [IT Risk Manager](../../it-roles-governance-risk-compliance-audit-and-privacy/references/it-risk-manager.md) | assesses business, service, security and regulatory impact using verified facts | impact assessment with uncertainty and affected obligations | Critical impact claims distinguish confirmed fact from inference |
| 6 | [Data Protection Officer](../../it-roles-governance-risk-compliance-audit-and-privacy/references/data-protection-officer.md) | performs privacy/breach assessment and coordinates legal/regulatory decision inputs | breach/notification decision basis | Notification/non-notification has correct authority, clock and evidence |
| 7 | [Incident Responder](../../it-roles-security-operations-and-defensive-security/references/incident-responder.md) | eradicates malicious persistence/root causes and verifies the environment | eradication evidence and residual technical risks | Known persistence and exploited control gaps are addressed or explicitly owned |
| 8 | [Disaster Recovery Coordinator](../../it-roles-governance-risk-compliance-audit-and-privacy/references/disaster-recovery-coordinator.md) | coordinates recovery sequencing, integrity validation and rollback/fallback readiness | recovery evidence and service restoration status | Recovery uses trusted state/data and respects RTO/RPO/business priorities |
| 9 | [IT Service Owner](../../it-roles-executive-and-leadership/references/it-service-owner.md) | validates business/service recovery and accepts restored operating state | business recovery acceptance | Service owner confirms agreed validation signals and residual limitations |
| 10 | [Crisis Manager](../../it-roles-governance-risk-compliance-audit-and-privacy/references/crisis-manager.md) | coordinates customer/regulator/executive communications decision and timing where required | communication/regulatory action record | Communications are authorised, consistent and evidence-based |
| 11 | [Problem Manager](../../it-roles-service-management-and-support/references/problem-manager.md) | runs lessons learned/root-cause analysis across people/process/technology | lessons learned and systemic findings | Findings address causes and failed controls, not only symptoms |
| 12 | [Control Owner](../../it-roles-governance-risk-compliance-audit-and-privacy/references/control-owner.md) | owns control remediation, target dates and evidence of completion | control remediation plan | Every material finding has a control owner, due date and verification method |
| 13 | [Internal IT Auditor](../../it-roles-governance-risk-compliance-audit-and-privacy/references/internal-it-auditor.md) | independently verifies closure evidence for material incidents where governance requires | closure assurance result | No open critical finding is silently closed or self-assured |

## Control semantics

- A gate is blocking unless a named authority with the required decision right records an explicit waiver, rationale, expiry/review date and residual risk.
- A handoff is not complete because a document exists; the receiving role must be able to verify the acceptance condition from attributable evidence.
- Producer, approver and independent assurance responsibilities remain separated where the decision is consequential.
- Workflow order may branch or loop, but skipped steps and their unmet gates remain visible.
- Material claims/decisions use stable IDs and trace to evidence so Behavioral Quality evaluation can measure coverage and unsupported claims.

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- The incident is contained and eradicated, evidence is preserved, recovery is accepted by the business, notification decisions are traceable, and control remediation is closed or owned.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| suspected | Triage hypotheses and preserve evidence before drawing conclusions | Observed event, reliability, scope confidence and lead |
| confirmed-breach | Coordinate containment, notification and trusted recovery under exact authority | Custody/timeline, impact, clock assessment and actual decisions |

Return disproved hypotheses, incomplete impact evidence or failed recovery to the responsible response/forensic/service owner. Stop unauthorised destructive handling, unsupported notification claims or recovery from untrusted state. Close on independent assurance of actual recovery and owned control remediation; retain justified false-positive disposition separately. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Observed event, time and affected scope
- Current response authority and evidence handling
- Business priorities and notification obligations

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return disproved hypotheses, incomplete impact evidence or failed recovery to the responsible response/forensic/service owner.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop unauthorised destructive handling, unsupported notification claims or recovery from untrusted state.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Close on independent assurance of actual recovery and owned control remediation; retain justified false-positive disposition separately.

**Bounded paths and scope:**

Suspected and confirmed events retain evidence confidence and authority; unobserved breach/notification actions cannot be inferred from suspicion.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| suspected | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 | 13 |
| confirmed-breach | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 | 13 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
