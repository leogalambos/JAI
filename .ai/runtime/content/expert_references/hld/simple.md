---
reference_id: example:hld:simple
schema_version: '1.0.0'
document_kind: hld
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/hld
approval_status: not-human-approved
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Harborline Field Services · Field Appointment Reliability · `HFS-FAR` · SIMPLE complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Field Operations Manager. **Scope:** single-business-unit, low-coupling rollout.

# High-level solution design — Field Appointment Reliability

<a id="dcs-hld.solution_scope"></a>
## Scope, assumptions and interfaces of responsibility

HLD `HFS-FAR-HLD-01` proposes the target implementation of technician appointment scheduling. Included: one internal scheduling service, managed identity provider, dispatch integration and managed booking SaaS. Excluded: internal code and infrastructure of unmanaged external counterparties, unapproved jurisdiction obligations and personal-device support.

Delivery owner: Delivery Lead; solution designer: Application Lead; operations receiver: Service Desk Lead. Assumption: contract and identity owners accept the proposed integration design. Every assumption is a condition for detailed design rather than an implicit confirmed fact.

<a id="dcs-hld.quality_requirements"></a>
## Quality attributes and measurable targets

Availability target **99.5% per calendar month**; recovery **RTO 8 hours / RPO 24 hours**; performance **p95 booking response below 2 seconds**. Identity: least-privilege workload and human accounts with centrally verifiable grants. Data controls: encrypt in transit and at rest, classify **technician names, customer addresses and appointment times**, limit retention to organisation-approved schedules and preserve traceable deletion decisions.

Verification must measure business success, not merely HTTP 200 responses. The solution must produce a named readiness report with observable failures for latency, error budgets, backups and unauthorised access attempts.

<a id="dcs-hld.solution_components"></a>
## Components, topology and rationale

| Component | Responsibility | Deployment / boundary |
|---|---|---|
| Scheduling UI | Authenticated technician/dispatcher operations | HTTPS via corporate SSO |
| Booking adapter | Validates request and adds idempotency token | SaaS API, outbound queue |
| Reconciliation job | Finds unmatched appointments | Read-only SaaS export |

Scope is limited to one business team; separation between booking and notification flows prevents an outage of messaging from corrupting appointments.

Isolation principle: business writes use a single authoritative path; asynchronous replication cannot become a second uncontrolled writer. Shared runtime dependencies and availability assumptions must be included in the dependency graph. Prefer a bounded failure path over indefinite retries during degraded operation.

<a id="dcs-hld.solution_interfaces"></a>
## Integration contracts, trust and failure behaviour

Logical data flow: `dispatch-ui → booking-api → appointment-store → notification-worker`. Each message or request includes stable business ID, correlation ID, schema version, source timestamp and data-classification tag. Consumers implement deduplication with an idempotency key and publish either accepted, rejected or quarantined state; error codes must be actionable.

Security: ingress authentication, per-service authorisation, field-level minimisation and segregated operational privileges. On timeout or broker backlog, propagate a known pending state and alert support; never report settlement/order/booking as final until authoritative reconciliation confirms it. Latency, queue depth, duplicate counts and reconciliation gaps are observable with owner-defined thresholds.

<a id="dcs-hld.delivery_strategy"></a>
## Delivery, rollout, rollback and verification

Deployment path: versioned infrastructure and application builds → pre-production contract tests → synthetic load/replay → canary/limited wave → reconciled monitoring → formal operations acceptance. Suggested change window: Sunday 06:00–08:00 local.

Rollback returns traffic to the last accepted contract or holds writes in a controlled queue. Pause outbound notifications; switch to read-only bookings and export pending appointments. Reversal of already-committed business state requires an independently authorised compensating transaction, not arbitrary data edits.

Exit checks: all critical requirements traced to tests; no high-severity open defects without authorised disposition; recovery rehearsal meeting 8 hours; independent security review; runbook handover and acceptance of open risks.

## Evidence register, assumptions and limitations

- **HFS-FAR-E-IF — Interface contract:** versioned API/event schemas and error matrix **Status:** proposed.
- **HFS-FAR-E-NFR — Non-functional verification:** measurements in isolated environment **Status:** not executed.
- **HFS-FAR-E-DEP — Deployment and rollback:** signed change plan and exercise evidence **Status:** pending.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `HFS-FAR-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** HFS-FAR-ADR-01, HFS-FAR-TEST-01, HFS-FAR-OPS-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.
