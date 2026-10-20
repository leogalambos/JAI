---
reference_id: example:hld:medium
schema_version: '1.0.0'
document_kind: hld
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/hld
approval_status: not-human-approved
content_revision: 2.3.0
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Meridian Retail Group · Order Event Integration · `MRG-OEI` · MEDIUM complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Digital Commerce Sponsor. **Scope:** multi-system integration with phased market rollout.

# High-level solution design — Order Event Integration

<a id="dcs-hld.solution_scope"></a>
## Scope, assumptions and interfaces of responsibility

HLD `MRG-OEI-HLD-01` proposes the target implementation of cross-channel order ingestion and fulfilment synchronisation. Included: commerce platform, API gateway, event broker, integration workers, ERP and observability stack. Excluded: internal code and infrastructure of unmanaged external counterparties, unapproved jurisdiction obligations and personal-device support.

Delivery owner: Programme Delivery Manager; solution designer: Integration Architect; operations receiver: Service Operations Manager. Assumption: contract and identity owners accept the proposed integration design. Every assumption is a condition for detailed design rather than an implicit confirmed fact.

<a id="dcs-hld.quality_requirements"></a>
## Quality attributes and measurable targets

Availability target **99.9% measured monthly**; recovery **RTO 2 hours / RPO 15 minutes**; performance **p95 event-to-ERP availability under 5 minutes**. Identity: least-privilege workload and human accounts with centrally verifiable grants. Data controls: encrypt in transit and at rest, classify **order identifiers, delivery addresses and limited customer identifiers**, limit retention to organisation-approved schedules and preserve traceable deletion decisions.

Verification must measure business success, not merely HTTP 200 responses. The solution must produce a named readiness report with observable failures for latency, error budgets, backups and unauthorised access attempts.

<a id="dcs-hld.solution_components"></a>
## Components, topology and rationale

| Component | Responsibility | Deployment / boundary |
|---|---|---|
| Commerce outbox | Atomic publication intent with order transaction | Local transactional store |
| Event broker | Retained versioned order events | TLS + producer/consumer ACL |
| ERP adapter | Idempotent consumer and schema translation | Bounded retry, dead-letter quarantine |
| Reconciliation service | End-to-end order state and discrepancies | Signed checkpoints + dashboard |

Wave 1 covers two markets and the ERP adapter, then four groups of countries; country routing and customer-data minimisation must be verified separately before each promotion.

Isolation principle: business writes use a single authoritative path; asynchronous replication cannot become a second uncontrolled writer. Shared runtime dependencies and availability assumptions must be included in the dependency graph. Prefer a bounded failure path over indefinite retries during degraded operation.

<a id="dcs-hld.solution_interfaces"></a>
## Integration contracts, trust and failure behaviour

Logical data flow: `commerce-api → transactional outbox → event-broker → idempotent ERP-adapter → reconciliation-store`. Each message or request includes stable business ID, correlation ID, schema version, source timestamp and data-classification tag. Consumers implement deduplication with an idempotency key and publish either accepted, rejected or quarantined state; error codes must be actionable.

Security: ingress authentication, per-service authorisation, field-level minimisation and segregated operational privileges. On timeout or broker backlog, propagate a known pending state and alert support; never report settlement/order/booking as final until authoritative reconciliation confirms it. Latency, queue depth, duplicate counts and reconciliation gaps are observable with owner-defined thresholds.

<a id="dcs-hld.delivery_strategy"></a>
## Delivery, rollout, rollback and verification

Deployment path: versioned infrastructure and application builds → pre-production contract tests → synthetic load/replay → canary/limited wave → reconciled monitoring → formal operations acceptance. Suggested change window: Saturday 22:00–Sunday 03:00 CET.

Rollback returns traffic to the last accepted contract or holds writes in a controlled queue. Stop consumer offsets, maintain durable broker retention, replay from signed checkpoints. Reversal of already-committed business state requires an independently authorised compensating transaction, not arbitrary data edits.

Exit checks: all critical requirements traced to tests; no high-severity open defects without authorised disposition; recovery rehearsal meeting 2 hours; independent security review; runbook handover and acceptance of open risks.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `MRG-OEI` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Runtime boundary and interface | Is this statement supported for `MRG-OEI` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Quantified NFR and test oracle | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Deployment/rollback trade-off | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — implementable contract

Specify the business invariant, interface/state schema, trust boundary, failure mode and explicit test oracle before claiming build readiness. For **hld**, the reviewer should actively challenge **runtime boundary and interface** and **quantified nfr and test oracle**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — trace to executable evidence

Link requirement → design choice → acceptance scenario → expected business output; HTTP status alone does not demonstrate correct business processing. The accountable party for this illustrative acceptance is **Technical Lead / Independent QA**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** runtime boundary and interface, quantified nfr and test oracle, and deployment/rollback trade-off. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

## Evidence register, assumptions and limitations

- **MRG-OEI-E-IF — Interface contract:** versioned API/event schemas and error matrix **Status:** proposed.
- **MRG-OEI-E-NFR — Non-functional verification:** measurements in isolated environment **Status:** not executed.
- **MRG-OEI-E-DEP — Deployment and rollback:** signed change plan and exercise evidence **Status:** pending.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `MRG-OEI-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** MRG-OEI-ADR-01, MRG-OEI-TEST-01, MRG-OEI-OPS-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.




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

