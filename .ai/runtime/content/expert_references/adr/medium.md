---
reference_id: example:adr:medium
schema_version: '1.0.0'
document_kind: adr
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/adr
approval_status: not-human-approved
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Meridian Retail Group · Order Event Integration · `MRG-OEI` · MEDIUM complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Digital Commerce Sponsor. **Scope:** multi-system integration with phased market rollout.

# Architecture decision record — Order Event Integration integration boundary

<a id="dcs-adr.decision_context"></a>
## Context, concern, constraints and status

`MRG-OEI-ADR-01`, **proposed**, authored by Integration Architect for independent ARB review. The architectural concern is how to preserve correctness when cross-channel order ingestion and fulfilment synchronisation spans unreliable interfaces. Existing state: nightly ERP batch exports with fragile point-to-point integrations. The design boundary is commerce platform, API gateway, event broker, integration workers, ERP and observability stack.

Drivers: **p95 event-to-ERP availability under 5 minutes**, availability **99.9% measured monthly**, audit traceability and reversible deployment. Data requiring protection: order identifiers, delivery addresses and limited customer identifiers. Assumed target cutover proposed first market 2027-06-01; not an approved go-live date.

<a id="dcs-adr.architecture_options"></a>
## Options and selection criteria

A: point-to-point synchronous API fan-out (simple observability, systemic timeout coupling); B: managed broker + outbox (selected); C: nightly batch (low complexity but violates time-to-ERP objective).

Decision drivers are ranked: (1) correctness and recoverability; (2) containment of faults; (3) observable evidence lineage; (4) operational cost and maintainability. Performance gains are not accepted where they compromise exactly-once *business outcome* semantics; transport can be at-least-once if consumers are idempotent.

Trade-off: eventual consistency requires a clearly defined stale-data tolerance and transparent reconciliation; direct synchronous calls reduce lag but can trigger cascading failures.

<a id="dcs-adr.architecture_choice"></a>
## Proposed architecture decision and rationale

**Decision:** Use a transactional outbox, managed event broker and separately versioned idempotent ERP consumers; reject direct synchronous fan-out from checkout.

Wave 1 covers two markets and the ERP adapter, then four groups of countries; country routing and customer-data minimisation must be verified separately before each promotion.

Stable identifiers: `MRG-OEI-EVENT-01` carries correlation ID, event schema version, business key, jurisdiction tag if relevant, originating system and source timestamp. An immutable processing record links request → accepted event → consumer result → reconciliation exception. Reject invalid/unknown schema versions to a quarantine stream; never silently drop events. Owner: Integration Architect; decision date remains pending actual L0 approval.

<a id="dcs-adr.consequences"></a>
## Consequences, reversibility and risk

Benefits: replayable history, recoverable side effects and a measurable difference between successful technical delivery and accepted business state. Costs: new broker operations, duplicate suppression, retention governance, backpressure capacity and troubleshooting expertise.

The main residual hazard is lost or duplicated events, country-specific data routing and supplier dependency. Guardrails: separate read/write privileges, scoped service identities, retention that fits applicable data policy, anomaly alarms and a tested checkpoint rollback. Rollback is limited to stopping new processing and restoring adapters to known signed configurations; **already-finalised business transactions are not undone**.

Evaluation target: demonstrate p95 event-to-ERP availability under 5 minutes, loss-free reconciliation over 50,000 synthetic events including duplicates and reordering, and recovery within 2 hours without falsifying success metrics.

<a id="dcs-adr.supersession"></a>
## Supersession and follow-up

No earlier signed decision is superseded by this synthetic record. Before adoption, query the architecture repository for overlapping integration and data-residency decisions, record explicit supersedes/superseded-by links and obtain acceptance from the system owners. Follow-ups: schema governance `MRG-OEI-SCHEMA-01`, resilience test `MRG-OEI-TEST-01`, operations handover `MRG-OEI-OPS-01`; reopen upon new legal restrictions, changed service SLO, or a serious replay incident.

## Evidence register, assumptions and limitations

- **MRG-OEI-E-REQ — Requirements:** versioned quality attributes and authoritative service owner **Status:** assumed.
- **MRG-OEI-E-INT — Interface prototype:** synthetic event traces, duplicate/reordering tests and consumer design **Status:** not executed.
- **MRG-OEI-E-RISK — Risk decision:** owner-reviewed residual risk acceptance **Status:** pending.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `MRG-OEI-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** MRG-OEI-HLD-01, MRG-OEI-TEST-01, MRG-OEI-OPS-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.
