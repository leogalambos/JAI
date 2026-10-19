---
reference_id: example:adr:complex
schema_version: '1.0.0'
document_kind: adr
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/adr
approval_status: not-human-approved
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Orion Payments Group · Regulated Settlement Modernisation · `OPG-RSM` · COMPLEX complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Group Payments Executive. **Scope:** multi-jurisdiction mission-critical transformation with regulatory obligations determined per entity.

# Architecture decision record — Regulated Settlement Modernisation integration boundary

<a id="dcs-adr.decision_context"></a>
## Context, concern, constraints and status

`OPG-RSM-ADR-01`, **proposed**, authored by Chief Payments Architect for independent ARB review. The architectural concern is how to preserve correctness when cross-border settlement instruction processing spans unreliable interfaces. Existing state: regional legacy settlement engines with separate ledgers and manual end-of-day reconciliation. The design boundary is channel gateways, policy service, event ledger, settlement orchestration, regional connectors, immutable evidence store and resilience sites.

Drivers: **p95 instruction acknowledgement under 450 ms excluding external networks**, availability **99.95% monthly for critical processing**, audit traceability and reversible deployment. Data requiring protection: payer/payee identifiers, transaction metadata and restricted operational records. Assumed target cutover proposed phased waves during 2027–2028 subject to local approvals; not an approved go-live date.

<a id="dcs-adr.architecture_options"></a>
## Options and selection criteria

A: big-bang shared global ledger (simpler final shape, unacceptable cutover blast radius); B: regional phased ledger with parallel reconciliation (selected); C: unchanged ledgers linked by a global query façade (no assured finality).

Decision drivers are ranked: (1) correctness and recoverability; (2) containment of faults; (3) observable evidence lineage; (4) operational cost and maintainability. Performance gains are not accepted where they compromise exactly-once *business outcome* semantics; transport can be at-least-once if consumers are idempotent.

Trade-off: eventual consistency requires a clearly defined stale-data tolerance and transparent reconciliation; direct synchronous calls reduce lag but can trigger cascading failures.

<a id="dcs-adr.architecture_choice"></a>
## Proposed architecture decision and rationale

**Decision:** Adopt append-only instruction lineage and jurisdiction-aware settlement orchestration with independently reconciled parallel ledger checkpoints; prohibit automated cross-jurisdiction ledger substitution.

The programme has three explicit failure domains, jurisdiction-specific residency rules, intraday settlement cut-offs and an independently reconciled dual-run ledger; unsafe cross-region failover must not be assumed legal.

Stable identifiers: `OPG-RSM-EVENT-01` carries correlation ID, event schema version, business key, jurisdiction tag if relevant, originating system and source timestamp. An immutable processing record links request → accepted event → consumer result → reconciliation exception. Reject invalid/unknown schema versions to a quarantine stream; never silently drop events. Owner: Chief Payments Architect; decision date remains pending actual L0 approval.

<a id="dcs-adr.consequences"></a>
## Consequences, reversibility and risk

Benefits: replayable history, recoverable side effects and a measurable difference between successful technical delivery and accepted business state. Costs: new broker operations, duplicate suppression, retention governance, backpressure capacity and troubleshooting expertise.

The main residual hazard is settlement finality mismatch, cross-border data movement and correlated regional failure. Guardrails: separate read/write privileges, scoped service identities, retention that fits applicable data policy, anomaly alarms and a tested checkpoint rollback. Rollback is limited to stopping new processing and restoring adapters to known signed configurations; **already-finalised business transactions are not undone**.

Evaluation target: demonstrate p95 instruction acknowledgement under 450 ms excluding external networks, loss-free reconciliation over 1.2 million generated instructions across failure domains and cut-off conditions, and recovery within 30 minutes without falsifying success metrics.

<a id="dcs-adr.supersession"></a>
## Supersession and follow-up

No earlier signed decision is superseded by this synthetic record. Before adoption, query the architecture repository for overlapping integration and data-residency decisions, record explicit supersedes/superseded-by links and obtain acceptance from the system owners. Follow-ups: schema governance `OPG-RSM-SCHEMA-01`, resilience test `OPG-RSM-TEST-01`, operations handover `OPG-RSM-OPS-01`; reopen upon new legal restrictions, changed service SLO, or a serious replay incident.

## Evidence register, assumptions and limitations

- **OPG-RSM-E-REQ — Requirements:** versioned quality attributes and authoritative service owner **Status:** assumed.
- **OPG-RSM-E-INT — Interface prototype:** synthetic event traces, duplicate/reordering tests and consumer design **Status:** not executed.
- **OPG-RSM-E-RISK — Risk decision:** owner-reviewed residual risk acceptance **Status:** pending.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `OPG-RSM-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** OPG-RSM-HLD-01, OPG-RSM-TEST-01, OPG-RSM-OPS-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.
