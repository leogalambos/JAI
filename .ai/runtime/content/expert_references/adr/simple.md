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
content_revision: 2.3.0
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

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `HFS-FAR` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Architectural decision invariant | Is this statement supported for `HFS-FAR` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Alternatives and counterfactual | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Reversal/impact on downstream work | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — implementable contract

Specify the business invariant, interface/state schema, trust boundary, failure mode and explicit test oracle before claiming build readiness. For **adr**, the reviewer should actively challenge **architectural decision invariant** and **alternatives and counterfactual**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — trace to executable evidence

Link requirement → design choice → acceptance scenario → expected business output; HTTP status alone does not demonstrate correct business processing. The accountable party for this illustrative acceptance is **Technical Lead / Independent QA**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** architectural decision invariant, alternatives and counterfactual, and reversal/impact on downstream work. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

## Evidence register, assumptions and limitations

- **HFS-FAR-E-REQ — Requirements:** versioned quality attributes and authoritative service owner **Status:** assumed.
- **HFS-FAR-E-INT — Interface prototype:** synthetic event traces, duplicate/reordering tests and consumer design **Status:** not executed.
- **HFS-FAR-E-RISK — Risk decision:** owner-reviewed residual risk acceptance **Status:** pending.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `HFS-FAR-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** HFS-FAR-HLD-01, HFS-FAR-TEST-01, HFS-FAR-OPS-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.




## Professional deepening: decision rationale and practical checks

### Decision invariants and boundary

Describe the invariant the design must preserve, the architecture element being changed and what falls outside the ADR. For event and ledger designs, at-least-once delivery implies deduplication and replay design; exactly-once business effects are not a transport guarantee. For simpler components, identify consistency guarantees, failure-domain boundaries and ownership. State which downstream designs consume the ADR and which earlier decisions constrain it.

### Option mechanics and fitness functions

Do not compare products by name alone. Compare failure behaviour under unavailability, schema evolution, operational load and permissions. Express testable fitness functions such as idempotent replay preserving one business state transition, tenant segregation surviving incorrect routing metadata, and recovery under the agreed RTO/RPO. Record baseline measurements as unknown until actually collected.

