---
reference_id: example:adr:simple
schema_version: '1.0.0'
document_kind: adr
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/adr
approval_status: not-human-approved
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Harborline Field Services · Field Appointment Reliability · `HFS-FAR` · SIMPLE complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Field Operations Manager. **Scope:** single-business-unit, low-coupling rollout.

# Architecture decision record — Field Appointment Reliability integration boundary

<a id="dcs-adr.decision_context"></a>
## Context, concern, constraints and status

`HFS-FAR-ADR-01`, **proposed**, authored by Application Lead for independent ARB review. The architectural concern is how to preserve correctness when technician appointment scheduling spans unreliable interfaces. Existing state: a shared spreadsheet and a single legacy dispatch application. The design boundary is one internal scheduling service, managed identity provider, dispatch integration and managed booking SaaS.

Drivers: **p95 booking response below 2 seconds**, availability **99.5% per calendar month**, audit traceability and reversible deployment. Data requiring protection: technician names, customer addresses and appointment times. Assumed target cutover proposed 2027-03-15; not an approved go-live date.

<a id="dcs-adr.architecture_options"></a>
## Options and selection criteria

Option A: direct calendar API writes (low setup cost but duplicate updates on retry). Option B: queue + idempotency + reconciliation (selected). Option C: nightly CSV exchange (insufficient appointment freshness).

Decision drivers are ranked: (1) correctness and recoverability; (2) containment of faults; (3) observable evidence lineage; (4) operational cost and maintainability. Performance gains are not accepted where they compromise exactly-once *business outcome* semantics; transport can be at-least-once if consumers are idempotent.

Trade-off: eventual consistency requires a clearly defined stale-data tolerance and transparent reconciliation; direct synchronous calls reduce lag but can trigger cascading failures.

<a id="dcs-adr.architecture_choice"></a>
## Proposed architecture decision and rationale

**Decision:** Use managed webhook events with a durable inbound queue and idempotent appointment keys, plus scheduled reconciliation; do not perform unguarded direct database writes.

Scope is limited to one business team; separation between booking and notification flows prevents an outage of messaging from corrupting appointments.

Stable identifiers: `HFS-FAR-EVENT-01` carries correlation ID, event schema version, business key, jurisdiction tag if relevant, originating system and source timestamp. An immutable processing record links request → accepted event → consumer result → reconciliation exception. Reject invalid/unknown schema versions to a quarantine stream; never silently drop events. Owner: Application Lead; decision date remains pending actual L0 approval.

<a id="dcs-adr.consequences"></a>
## Consequences, reversibility and risk

Benefits: replayable history, recoverable side effects and a measurable difference between successful technical delivery and accepted business state. Costs: new broker operations, duplicate suppression, retention governance, backpressure capacity and troubleshooting expertise.

The main residual hazard is vendor availability and duplicated appointment updates. Guardrails: separate read/write privileges, scoped service identities, retention that fits applicable data policy, anomaly alarms and a tested checkpoint rollback. Rollback is limited to stopping new processing and restoring adapters to known signed configurations; **already-finalised business transactions are not undone**.

Evaluation target: demonstrate p95 booking response below 2 seconds, loss-free reconciliation over 150 synthetic appointments, and recovery within 8 hours without falsifying success metrics.

<a id="dcs-adr.supersession"></a>
## Supersession and follow-up

No earlier signed decision is superseded by this synthetic record. Before adoption, query the architecture repository for overlapping integration and data-residency decisions, record explicit supersedes/superseded-by links and obtain acceptance from the system owners. Follow-ups: schema governance `HFS-FAR-SCHEMA-01`, resilience test `HFS-FAR-TEST-01`, operations handover `HFS-FAR-OPS-01`; reopen upon new legal restrictions, changed service SLO, or a serious replay incident.

## Evidence register, assumptions and limitations

- **HFS-FAR-E-REQ — Requirements:** versioned quality attributes and authoritative service owner **Status:** assumed.
- **HFS-FAR-E-INT — Interface prototype:** synthetic event traces, duplicate/reordering tests and consumer design **Status:** not executed.
- **HFS-FAR-E-RISK — Risk decision:** owner-reviewed residual risk acceptance **Status:** pending.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `HFS-FAR-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** HFS-FAR-HLD-01, HFS-FAR-TEST-01, HFS-FAR-OPS-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.
