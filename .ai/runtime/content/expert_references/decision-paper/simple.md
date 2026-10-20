---
reference_id: example:decision-paper:simple
schema_version: '1.0.0'
document_kind: decision-paper
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/decision-paper
approval_status: not-human-approved
content_revision: 2.3.0
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Harborline Field Services · Field Appointment Reliability · `HFS-FAR` · SIMPLE complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Field Operations Manager. **Scope:** single-business-unit, low-coupling rollout.

# Decision paper — Field Appointment Reliability

<a id="dcs-decision-paper.decision_request"></a>
## Decision request and authority

**Requested:** approve an architecture direction and conditional mobilisation for technician appointment scheduling. Operations Director is the receiving forum; Field Operations Manager is the sponsoring authority and must obtain any separate finance, risk and privacy approvals. Requested by **2027-02-01** (illustrative scheduling assumption). Outcomes are approve with conditions, defer for evidence, or reject. Approval cannot be inferred from this example.

The proposal boundary is one internal scheduling service, managed identity provider, dispatch integration and managed booking SaaS. The working performance objective is **reduce appointment rework from an illustrative 2.3% to at most 0.5% within two quarters** and the service target is 99.5% per calendar month. A different business outcome or change in data classification requires renewed review.

<a id="dcs-decision-paper.baseline"></a>
## Baseline and case for change

The current position is a shared spreadsheet and a single legacy dispatch application. This has created repeated double-bookings and delayed customer confirmations. Scope is 240 technicians and about 2,100 appointments each week. The baseline observation is **unverified synthetic input** (`HFS-FAR-E-BASE`); it must be replaced by a measured dataset from the actual system before commitment.

Do nothing is a legitimate alternative, not a cost-free default: it entails `£80,000` in illustrative continued-operation/remediation costs over 2027–2029 and carries the business outcome risk of failing the target. There is no claim that any regulator requires the proposed platform.

<a id="dcs-decision-paper.options"></a>
## Options assessed on a comparable basis

The alternatives are compared on a three-year undiscounted planning basis. All numbers below are **fabricated modelling assumptions**; scope boundaries and cost exclusions must be reconciled with Finance.

| Option | Three-year cost | Modelled benefits | Undiscounted net | Principal trade-off |
|---|---:|---:|---:|---|
| No change / manual remediation | £80,000 | £0 | -£80,000 | Continues 2.3% rework; low delivery risk |
| Managed scheduling SaaS | £140,000 | £240,000 | +£100,000 | Managed dependency; reversible exports |
| Custom scheduling platform | £310,000 | £270,000 | -£40,000 | Greater control but longer lead time |

Criteria: delivery continuity (30%), control/evidence integrity (25%), total cost/value (25%), operability and exit flexibility (20%). The options are assessed on the same scope; apparent value must not substitute for a risk acceptance decision.

<a id="dcs-decision-paper.tradeoffs"></a>
## Trade-offs, dependencies and residual risk

**Preferred path:** managed scheduling SaaS with a one-way dispatch sync. The main trade-off is faster delivery and clearer ownership in exchange for vendor availability and duplicated appointment updates. Detailed boundary: Scope is limited to one business team; separation between booking and notification flows prevents an outage of messaging from corrupting appointments.

Principal dependencies are identity integration, verified retention and recovery arrangements, availability of the receiving operations team, and evidence that the design meets **8 hours RTO** and **24 hours RPO**. Key residual risk `HFS-FAR-RISK-01` is retained with Head of Operations pending a tested restoration procedure. The indicative benefit model is sensitive to adoption: at 20% fewer realised benefits, model net value becomes £52,000.

Stop conditions: unresolved unauthorised data transfer, missing operational ownership, absent fallback procedure or reconciliation imbalance. Mitigations must be verified, not merely asserted.

<a id="dcs-decision-paper.recommendation"></a>
## Recommendation, conditions and implementation gate

Recommend **conditional selection of managed scheduling SaaS with a one-way dispatch sync**, not production approval. Rationale: it offers the best illustrative outcome when evaluated against traceability, delivery continuity and cost; the high-risk alternative increases blast radius without proportionate value.

Conditions before authorisation: (1) validate baseline and cost assumptions with source records; (2) approve the solution ADR/HLD; (3) obtain risk-owner treatment decision; (4) rehearse recovery and acceptance tests; (5) document vendor exit and portability arrangements. The authority should record approve/defer/reject, conditions, date and source hash in `HFS-FAR-DR-01`.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `HFS-FAR` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Exact decision authority and ask | Is this statement supported for `HFS-FAR` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Comparable option cost/risk | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Conditions and evidence deadline | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — customer commitment integrity

Trace the exact customer-requested outcome to a separately priced deliverable and explicit acceptance test; classify any unsupported requirement as an assumption or clarification. For **decision-paper**, the reviewer should actively challenge **exact decision authority and ask** and **comparable option cost/risk**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — contractual acceptance boundary

Distinguish indicative estimate, binding price, third-party pass-through and client internal cost. Change in scope requires a defined change-order rather than implied free delivery. The accountable party for this illustrative acceptance is **Bid Manager / Commercial Owner**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** exact decision authority and ask, comparable option cost/risk, and conditions and evidence deadline. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

## Evidence register, assumptions and limitations

- **HFS-FAR-E-BASE — Baseline:** measured incidents/service levels to be sourced from operating systems **Status:** hypothetical.
- **HFS-FAR-E-COST — Finance model:** cost and benefit workbook with owners and sensitivity inputs **Status:** hypothetical.
- **HFS-FAR-E-RISK — Risk assessment:** risk register and treatment evidence **Status:** pending.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `HFS-FAR-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** HFS-FAR-ADR-01, HFS-FAR-HLD-01, HFS-FAR-RA-01, HFS-FAR-BC-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.




## Professional deepening: decision rationale and practical checks

### Decision-quality and authority boundary

The decision statement must distinguish authorisation to explore, commitment of funds, authority to process sensitive data and permission to deploy. These are different decisions with different approvers. Record the decision's reversibility, expiry and triggers for renewal. Identify which alternative is selected when a prerequisite fails rather than treating every open condition as a generic action item. In the illustrative decision, an architecture preference can be agreed while release approval remains blocked on verified reconciliation, recovery and named risk acceptance.

### Comparable alternative evaluation

Normalise options against the same three-year service boundary and show separate operating costs, transition costs, control exposure and exit liabilities. The do-nothing baseline includes its own remediation and risk cost; it is not assumed to be zero. Score security and control performance as gates rather than allowing a cheap unsafe option to win on a weighted average. Record the criterion owner and sensitivity to changes in weights. A weighted result is explanatory evidence, never a substitute for an accountable choice.

