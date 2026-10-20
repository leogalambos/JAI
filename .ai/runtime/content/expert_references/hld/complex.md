---
reference_id: example:hld:complex
schema_version: '1.0.0'
document_kind: hld
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/hld
approval_status: not-human-approved
content_revision: 2.0.0
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Orion Payments Group · Regulated Settlement Modernisation · `OPG-RSM` · COMPLEX complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Group Payments Executive. **Scope:** multi-jurisdiction mission-critical transformation with regulatory obligations determined per entity.

# High-level solution design — Regulated Settlement Modernisation

<a id="dcs-hld.solution_scope"></a>
## Scope, assumptions and interfaces of responsibility

HLD `OPG-RSM-HLD-01` proposes the target implementation of cross-border settlement instruction processing. Included: channel gateways, policy service, event ledger, settlement orchestration, regional connectors, immutable evidence store and resilience sites. Excluded: internal code and infrastructure of unmanaged external counterparties, unapproved jurisdiction obligations and personal-device support.

Delivery owner: Transformation Director; solution designer: Chief Payments Architect; operations receiver: Critical Service Operations Director. Assumption: contract and identity owners accept the proposed integration design. Every assumption is a condition for detailed design rather than an implicit confirmed fact.

<a id="dcs-hld.quality_requirements"></a>
## Quality attributes and measurable targets

Availability target **99.95% monthly for critical processing**; recovery **RTO 30 minutes / RPO 5 minutes**; performance **p95 instruction acknowledgement under 450 ms excluding external networks**. Identity: least-privilege workload and human accounts with centrally verifiable grants. Data controls: encrypt in transit and at rest, classify **payer/payee identifiers, transaction metadata and restricted operational records**, limit retention to organisation-approved schedules and preserve traceable deletion decisions.

Verification must measure business success, not merely HTTP 200 responses. The solution must produce a named readiness report with observable failures for latency, error budgets, backups and unauthorised access attempts.

<a id="dcs-hld.solution_components"></a>
## Components, topology and rationale

| Component | Responsibility | Deployment / boundary |
|---|---|---|
| Policy gateway | Jurisdiction eligibility and risk rules | Dual-admin policy deployment |
| Durable ingress | Immutable instruction sequence | Signed journal with replay limits |
| Settlement orchestrator | Maintains finality state machine | Idempotent regional connectors |
| Parallel ledger | Independently reconciled balances | Append-only checkpoints |
| Evidence store | Immutable audited lineage | Scoped read access and retention |

The programme has three explicit failure domains, jurisdiction-specific residency rules, intraday settlement cut-offs and an independently reconciled dual-run ledger; unsafe cross-region failover must not be assumed legal.

Isolation principle: business writes use a single authoritative path; asynchronous replication cannot become a second uncontrolled writer. Shared runtime dependencies and availability assumptions must be included in the dependency graph. Prefer a bounded failure path over indefinite retries during degraded operation.

<a id="dcs-hld.solution_interfaces"></a>
## Integration contracts, trust and failure behaviour

Logical data flow: `channel → policy-gateway → durable ingress → settlement-orchestrator → ledger + jurisdiction-connector → reconciliation/evidence`. Each message or request includes stable business ID, correlation ID, schema version, source timestamp and data-classification tag. Consumers implement deduplication with an idempotency key and publish either accepted, rejected or quarantined state; error codes must be actionable.

Security: ingress authentication, per-service authorisation, field-level minimisation and segregated operational privileges. On timeout or broker backlog, propagate a known pending state and alert support; never report settlement/order/booking as final until authoritative reconciliation confirms it. Latency, queue depth, duplicate counts and reconciliation gaps are observable with owner-defined thresholds.

<a id="dcs-hld.delivery_strategy"></a>
## Delivery, rollout, rollback and verification

Deployment path: versioned infrastructure and application builds → pre-production contract tests → synthetic load/replay → canary/limited wave → reconciled monitoring → formal operations acceptance. Suggested change window: jurisdiction-specific non-settlement cut-off windows with dual human authorisation.

Rollback returns traffic to the last accepted contract or holds writes in a controlled queue. Halt new instruction acceptance, preserve durable sequence checkpoints, invoke independently authorised compensating workflow. Reversal of already-committed business state requires an independently authorised compensating transaction, not arbitrary data edits.

Exit checks: all critical requirements traced to tests; no high-severity open defects without authorised disposition; recovery rehearsal meeting 30 minutes; independent security review; runbook handover and acceptance of open risks.

## Evidence register, assumptions and limitations

- **OPG-RSM-E-IF — Interface contract:** versioned API/event schemas and error matrix **Status:** proposed.
- **OPG-RSM-E-NFR — Non-functional verification:** measurements in isolated environment **Status:** not executed.
- **OPG-RSM-E-DEP — Deployment and rollback:** signed change plan and exercise evidence **Status:** pending.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `OPG-RSM-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** OPG-RSM-ADR-01, OPG-RSM-TEST-01, OPG-RSM-OPS-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.




## Professional deepening: decision rationale and practical checks

### Service boundary and responsibility model

For each runtime component, declare responsibilities, data authority, upstream/downstream interfaces, scaling unit and failure response. Security responsibilities must be explicit at trust boundaries: which service authenticates the caller, enforces the business authorization and issues an audit event. A high-level design should not substitute vague terms such as “secure API” for enforceable controls.

### Interfaces, consistency and error semantics

Specify request IDs, idempotency keys, schema compatibility, ordering needs, timeouts, retries, dead-letter handling and retention boundaries. Define whether a response means acceptance, persistence or final business processing. If an asynchronous consumer fails after acknowledging a message, demonstrate how the source of truth and replay mechanism prevent permanent loss and duplicate business effects.

### NFR and observability allocation

| Requirement | Design allocation | Observable signal | Verification |
|---|---|---|---|
| Availability | Isolated failure domains | Dependency SLI and synthetic health | Fault injection |
| Data integrity | Durable state + reconciliation | Unmatched records and checksum variance | Replay, corruption and balance tests |
| Access control | Service identity + least privilege | Denied action rate and policy audit | Negative entitlement tests |
| Recoverability | Restorable checkpoints | Restore time and consistency proof | Timed recovery rehearsal |

### Deployment and cutover strategy

Describe environment separation, infrastructure ownership, configuration provenance, secret injection, progressive traffic shifting and rollback boundary. A rollback must explain what happens to data created in the new path. Provide an order of operations consistent with migration dependencies, and name the release authority who decides whether to resume or abort after a partial failure.

### Security and operability review

Document service-level threat assumptions, trust-zone crossings, encryption and key ownership, monitoring responsibilities, capacity bounds and incident escalation. Challenge single shared identity, policy or telemetry services as possible correlated failure sources. HLD approval permits detailed implementation planning only; it does not substitute for penetration testing or production acceptance.

### Enterprise review challenge and operational hand-off

The reviewer should challenge the weakest evidence source before accepting the proposed conclusion, including dependency coupling, supplier exit conditions and whether ownership survives organizational change. If a required artifact is missing, record an unresolved gap rather than generating plausible-looking completion text. Translate each material concern into a downstream receiving artifact with stable ID, explicit owner and verification condition.

The following review disposition is intentionally **OPEN**: professional approval absent; operating evidence not provided; example cannot be repurposed as a production release, financial authorization or safety assurance.

