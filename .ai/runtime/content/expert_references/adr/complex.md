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
content_revision: 2.3.0
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

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `OPG-RSM` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Architectural decision invariant | Is this statement supported for `OPG-RSM` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
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

- **OPG-RSM-E-REQ — Requirements:** versioned quality attributes and authoritative service owner **Status:** assumed.
- **OPG-RSM-E-INT — Interface prototype:** synthetic event traces, duplicate/reordering tests and consumer design **Status:** not executed.
- **OPG-RSM-E-RISK — Risk decision:** owner-reviewed residual risk acceptance **Status:** pending.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `OPG-RSM-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** OPG-RSM-HLD-01, OPG-RSM-TEST-01, OPG-RSM-OPS-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.




## Professional deepening: decision rationale and practical checks

### Decision invariants and boundary

Describe the invariant the design must preserve, the architecture element being changed and what falls outside the ADR. For event and ledger designs, at-least-once delivery implies deduplication and replay design; exactly-once business effects are not a transport guarantee. For simpler components, identify consistency guarantees, failure-domain boundaries and ownership. State which downstream designs consume the ADR and which earlier decisions constrain it.

### Option mechanics and fitness functions

Do not compare products by name alone. Compare failure behaviour under unavailability, schema evolution, operational load and permissions. Express testable fitness functions such as idempotent replay preserving one business state transition, tenant segregation surviving incorrect routing metadata, and recovery under the agreed RTO/RPO. Record baseline measurements as unknown until actually collected.

### Structured consequence ledger

| Consequence | Benefit | New cost or exposure | Evidence to close |
|---|---|---|
| Decoupling | Consumer independence | Eventual-consistency windows | Reconciliation and replay test |
| Resilience | Isolation of a failed component | Recovery complexity | Failure exercise report |
| Governance | Stable interface contract | Versioning discipline | Contract compatibility tests |
| Security | Centralised policy enforcement | Shared-policy failure domain | Privilege review and negative tests |

Each consequence must have an accountable owner; “technology team” alone is insufficient.

### Supersession and review triggers

An ADR is immutable as a historical decision but may be superseded. Define superseded-by links, affected capabilities, dependent contracts and a review trigger for materially changed requirements. Security approvals and financial decisions do not inherit automatically into the new ADR. Changes to message ordering, transaction semantics or data residency should create a new decision or formally amend the accepted architecture.

### Rejection and rollback proof

For each rejected option, state why its strongest advantage did not compensate for disadvantages in this context. Describe what evidence could reverse the decision. Where migration is involved, record a reversible step, safe rollback boundary, irreversible data transformation and the checkpoint after which old services cannot simply be restarted. A viable rollback plan includes the state reconciliation needed after the cutover boundary.

### Enterprise review challenge and operational hand-off

The reviewer should challenge the weakest evidence source before accepting the proposed conclusion, including dependency coupling, supplier exit conditions and whether ownership survives organizational change. If a required artifact is missing, record an unresolved gap rather than generating plausible-looking completion text. Translate each material concern into a downstream receiving artifact with stable ID, explicit owner and verification condition.

The following review disposition is intentionally **OPEN**: professional approval absent; operating evidence not provided; example cannot be repurposed as a production release, financial authorization or safety assurance.

