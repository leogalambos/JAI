---
reference_id: example:decision-paper:medium
schema_version: '1.0.0'
document_kind: decision-paper
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/decision-paper
approval_status: not-human-approved
content_revision: 2.0.0
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Meridian Retail Group · Order Event Integration · `MRG-OEI` · MEDIUM complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Digital Commerce Sponsor. **Scope:** multi-system integration with phased market rollout.

# Decision paper — Order Event Integration

<a id="dcs-decision-paper.decision_request"></a>
## Decision request and authority

**Requested:** approve an architecture direction and conditional mobilisation for cross-channel order ingestion and fulfilment synchronisation. Architecture Review Board is the receiving forum; Digital Commerce Sponsor is the sponsoring authority and must obtain any separate finance, risk and privacy approvals. Requested by **2027-02-01** (illustrative scheduling assumption). Outcomes are approve with conditions, defer for evidence, or reject. Approval cannot be inferred from this example.

The proposal boundary is commerce platform, API gateway, event broker, integration workers, ERP and observability stack. The working performance objective is **move accepted-order visibility from the next batch cycle to 5 minutes at p95, without losing order records** and the service target is 99.9% measured monthly. A different business outcome or change in data classification requires renewed review.

<a id="dcs-decision-paper.baseline"></a>
## Baseline and case for change

The current position is nightly ERP batch exports with fragile point-to-point integrations. This has created batch latency and failed reconciliation delaying order promises. Scope is 12 European markets and a synthetic peak of 180,000 orders per day. The baseline observation is **unverified synthetic input** (`MRG-OEI-E-BASE`); it must be replaced by a measured dataset from the actual system before commitment.

Do nothing is a legitimate alternative, not a cost-free default: it entails `€550,000` in illustrative continued-operation/remediation costs over 2027–2029 and carries the business outcome risk of failing the target. There is no claim that any regulator requires the proposed platform.

<a id="dcs-decision-paper.options"></a>
## Options assessed on a comparable basis

The alternatives are compared on a three-year undiscounted planning basis. All numbers below are **fabricated modelling assumptions**; scope boundaries and cost exclusions must be reconciled with Finance.

| Option | Three-year cost | Modelled benefits | Undiscounted net | Principal trade-off |
|---|---:|---:|---:|---|
| Retain batch and patch | €550,000 | €0 | -€550,000 | Does not meet five-minute target |
| Managed broker and adapters | €1,250,000 | €2,150,000 | +€900,000 | Versioned events; replays needed |
| Synchronous API fan-out | €1,900,000 | €2,350,000 | +€450,000 | Propagates peak-load coupling |

Criteria: delivery continuity (30%), control/evidence integrity (25%), total cost/value (25%), operability and exit flexibility (20%). The options are assessed on the same scope; apparent value must not substitute for a risk acceptance decision.

<a id="dcs-decision-paper.tradeoffs"></a>
## Trade-offs, dependencies and residual risk

**Preferred path:** managed event backbone and decoupled ERP adapters. The main trade-off is faster delivery and clearer ownership in exchange for lost or duplicated events, country-specific data routing and supplier dependency. Detailed boundary: Wave 1 covers two markets and the ERP adapter, then four groups of countries; country routing and customer-data minimisation must be verified separately before each promotion.

Principal dependencies are identity integration, verified retention and recovery arrangements, availability of the receiving operations team, and evidence that the design meets **2 hours RTO** and **15 minutes RPO**. Key residual risk `MRG-OEI-RISK-01` is retained with Head of Digital Risk pending a tested restoration procedure. The indicative benefit model is sensitive to adoption: at 20% fewer realised benefits, model net value becomes €470,000.

Stop conditions: unresolved unauthorised data transfer, missing operational ownership, absent fallback procedure or reconciliation imbalance. Mitigations must be verified, not merely asserted.

<a id="dcs-decision-paper.recommendation"></a>
## Recommendation, conditions and implementation gate

Recommend **conditional selection of managed event backbone and decoupled ERP adapters**, not production approval. Rationale: it offers the best illustrative outcome when evaluated against traceability, delivery continuity and cost; the high-risk alternative increases blast radius without proportionate value.

Conditions before authorisation: (1) validate baseline and cost assumptions with source records; (2) approve the solution ADR/HLD; (3) obtain risk-owner treatment decision; (4) rehearse recovery and acceptance tests; (5) document vendor exit and portability arrangements. The authority should record approve/defer/reject, conditions, date and source hash in `MRG-OEI-DR-01`.

## Evidence register, assumptions and limitations

- **MRG-OEI-E-BASE — Baseline:** measured incidents/service levels to be sourced from operating systems **Status:** hypothetical.
- **MRG-OEI-E-COST — Finance model:** cost and benefit workbook with owners and sensitivity inputs **Status:** hypothetical.
- **MRG-OEI-E-RISK — Risk assessment:** risk register and treatment evidence **Status:** pending.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `MRG-OEI-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** MRG-OEI-ADR-01, MRG-OEI-HLD-01, MRG-OEI-RA-01, MRG-OEI-BC-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.




## Professional deepening: decision rationale and practical checks

### Decision-quality and authority boundary

The decision statement must distinguish authorisation to explore, commitment of funds, authority to process sensitive data and permission to deploy. These are different decisions with different approvers. Record the decision's reversibility, expiry and triggers for renewal. Identify which alternative is selected when a prerequisite fails rather than treating every open condition as a generic action item. In the illustrative decision, an architecture preference can be agreed while release approval remains blocked on verified reconciliation, recovery and named risk acceptance.

### Comparable alternative evaluation

Normalise options against the same three-year service boundary and show separate operating costs, transition costs, control exposure and exit liabilities. The do-nothing baseline includes its own remediation and risk cost; it is not assumed to be zero. Score security and control performance as gates rather than allowing a cheap unsafe option to win on a weighted average. Record the criterion owner and sensitivity to changes in weights. A weighted result is explanatory evidence, never a substitute for an accountable choice.

### Decision matrix and challenge

| Review question | Evidence to inspect | Failure response |
|---|---|---|
| Are options genuinely comparable? | Scope and excluded costs for each candidate | Rework comparison before decision |
| Can the proposed outcome be measured? | Baseline, SLI definitions and target owner | Defer benefits claim |
| Have non-negotiable controls been met? | Control applicability and risk decisions | Do not authorise production |
| Is exit/reversibility credible? | Contract terms, rollback rehearsal and migration dependencies | Restrict commitment to reversible stage |

The analyst should record a reasoned dissent from Security, Operations or Finance alongside the sponsor recommendation, including why the dissent is or is not material.

### Conditional decision record

Provide an explicit disposition table: *approved in principle*, *deferred pending evidence* or *rejected*, each with scope, constraints, authority and timestamp. An illustrative acceptance condition should identify an owner, a deadline, a verifiable predicate and an escalation if missed; “address security risks” is not verifiable. A change of jurisdiction, design boundary, external processor or accepted risk invalidates the previous advice and prompts decision renewal.

