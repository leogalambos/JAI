---
reference_id: example:runbook:simple
schema_version: '1.0.0'
document_kind: runbook
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/runbook
approval_status: not-human-approved
content_revision: 2.0.0
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Harborline Field Services · Field Appointment Reliability · `HFS-FAR` · SIMPLE complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Field Operations Manager. **Scope:** single-business-unit, low-coupling rollout.

# Operator recovery runbook — Field Appointment Reliability (simple)

<a id="dcs-runbook.operational_trigger"></a>
## Trigger, authority and safety stop conditions

Runbook `HFS-FAR-RB-01` supports technician appointment scheduling only. Activate for **booking API 5xx over 5% for ten minutes or duplicate appointment count above 5 per hour**; on-call operator may gather evidence and perform preapproved containment, but production-impacting steps require an authorised change/incident authority. Never run this example as a production procedure without service-specific verification.

**STOP immediately** on inconsistent system identity, unverified privileged access, missing backups/checkpoints, an unknown jurisdiction restriction, risk of irreversible business action, or evidence of active compromise. Escalate to Service Desk Lead and Head of Operations.

<a id="dcs-runbook.prerequisites"></a>
## Prerequisites, access and safe operating boundary

Require the live incident identifier, relevant asset and deployment version, network/tenant scope, read-only telemetry role, tested rollback package and authorised operational approver. Verify that the environment is the intended isolated tenant/region before any action. No credentials, private endpoints or production customer data are embedded here.

Prerequisite evidence: alert `HFS-FAR-E-ALERT`, configuration snapshot `HFS-FAR-E-CFG`, recovery checkpoint `HFS-FAR-E-CKPT` and acceptance limits **8 hours/24 hours**. If a prerequisite is absent, remain at safe observation-only mode and escalate.

<a id="dcs-runbook.procedure_steps"></a>
## Ordered recovery procedure and expected outcomes

Execution must log operator, timestamp, authority, target and observed output for each step. The actions below are **illustrative**, not verified CLI commands; translate them to the platform-specific, least-privileged scripts only after service-owner approval.

| # | Stage | Operator action | Expected evidence / checkpoint |
|---:|---|---|---|
| 1 | Establish identity | Open the incident record and confirm authorised on-call identity | Incident ID and service/build identity recorded |
| 2 | Collect evidence | Query synthetic dashboard and inspect booking mismatch dashboard | Error timeline, tenant ID and pending appointment count preserved |
| 3 | Contain | Pause **notification workers only**, leaving authoritative bookings unchanged | Queue depth stops growing; bookings retained |
| 4 | Recover | Restart approved adapter through preauthorised deployment runbook; replay quarantined ID ranges once | Each business key reconciles exactly once |
| 5 | Validate | Compare appointment and dispatch totals; test customer notification in synthetic tenant | Zero unexplained duplicates or mismatched IDs |

Use only versioned, tested commands from the local operations repository. Each action must be idempotent or contain a defined one-time execution token to prevent duplicate recovery effects.

<a id="dcs-runbook.failure_recovery"></a>
## Failure branches, rollback and escalation

If any step cannot produce the expected checkpoint, **stop further state-changing actions** and preserve the observed error. If the latest accepted snapshot is intact, revert only the responsible integration configuration; do not delete business records or attempt to reverse finalised transactions by hand.

Expected safe state: pause outbound notifications; switch to read-only bookings and export pending appointments. Escalate to incident commander if recovery threatens 8 hours, to security if secrets or anomalous privilege use are suspected, and to risk/treasury where financial or jurisdictional obligations may be affected. Document compensating actions and their independent approvals.

<a id="dcs-runbook.operational_validation"></a>
## Validation, rehearsal and review trigger

Measure business-level reconciliation, not just process health: weekly duplicate-booking rate and reconciliation exception count. Check that all acknowledged work is either correctly applied, explicitly pending or independently rejected; no unknown status. Follow up with a controlled limited-service test before declaring restored.

**Last rehearsal:** not executed for this synthetic example. **Required rehearsal:** isolated environment with 150 synthetic appointments and adverse conditions, evidence reviewed by Test Lead and service owner. Reassess following dependency change, runbook failure, provider upgrade or a material control issue; normal review cycle no longer than six months for this example.

## Evidence register, assumptions and limitations

- **HFS-FAR-E-ALERT — Trigger proof:** time series and incident correlation **Status:** illustrative.
- **HFS-FAR-E-CKPT — Checkpoint:** signed state/offset/reference before attempted recovery **Status:** not executed.
- **HFS-FAR-E-REC — Drill record:** operator log, expected vs actual outcomes and review **Status:** not executed.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `HFS-FAR-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** HFS-FAR-OPS-01, HFS-FAR-RA-01, HFS-FAR-INC-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.




## Professional deepening: decision rationale and practical checks

### Preflight and safe operating envelope

Distinguish read-only diagnosis from a potentially destructive corrective action. Specify required privileges, working hours, customer impact, change authorization, required backups and expected system state before touching production. Privilege or environment verification failure terminates the procedure and triggers escalation; do not recommend bypassing enterprise controls to “unblock” recovery.

### Executable sequence and checkpoints

| Step | Action class | Observable success criterion | Abort condition |
|---|---|---|---|
| 1 | Read-only identify | Correct environment, service and incident ID | Scope mismatch |
| 2 | Read-only baseline | Fresh telemetry and consistent state | Missing/contradictory signals |
| 3 | Authorized change | Named change approval and controlled execution | Approval missing |
| 4 | Verification | Business transaction and integrity tests pass | Any critical mismatch |
| 5 | Closure | Evidence captured and on-call handoff accepted | Open severe issue |

