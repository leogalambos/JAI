---
reference_id: example:decision-paper:complex
schema_version: '1.0.0'
document_kind: decision-paper
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/decision-paper
approval_status: not-human-approved
content_revision: 2.0.0
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Orion Payments Group · Regulated Settlement Modernisation · `OPG-RSM` · COMPLEX complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Group Payments Executive. **Scope:** multi-jurisdiction mission-critical transformation with regulatory obligations determined per entity.

# Decision paper — Regulated Settlement Modernisation

<a id="dcs-decision-paper.decision_request"></a>
## Decision request and authority

**Requested:** approve an architecture direction and conditional mobilisation for cross-border settlement instruction processing. Investment Committee and Architecture Authority is the receiving forum; Group Payments Executive is the sponsoring authority and must obtain any separate finance, risk and privacy approvals. Requested by **2027-02-01** (illustrative scheduling assumption). Outcomes are approve with conditions, defer for evidence, or reject. Approval cannot be inferred from this example.

The proposal boundary is channel gateways, policy service, event ledger, settlement orchestration, regional connectors, immutable evidence store and resilience sites. The working performance objective is **achieve complete instruction lineage and timely settlement at defined cut-offs with zero unexplained financial imbalance** and the service target is 99.95% monthly for critical processing. A different business outcome or change in data classification requires renewed review.

<a id="dcs-decision-paper.baseline"></a>
## Baseline and case for change

The current position is regional legacy settlement engines with separate ledgers and manual end-of-day reconciliation. This has created legacy component concentration, missed settlement deadlines and fragmented reconciliation evidence. Scope is 14 jurisdictions, synthetic 2.4 million instructions daily and multiple settlement cut-offs. The baseline observation is **unverified synthetic input** (`OPG-RSM-E-BASE`); it must be replaced by a measured dataset from the actual system before commitment.

Do nothing is a legitimate alternative, not a cost-free default: it entails `€4,400,000` in illustrative continued-operation/remediation costs over 2027–2029 and carries the business outcome risk of failing the target. There is no claim that any regulator requires the proposed platform.

<a id="dcs-decision-paper.options"></a>
## Options assessed on a comparable basis

The alternatives are compared on a three-year undiscounted planning basis. All numbers below are **fabricated modelling assumptions**; scope boundaries and cost exclusions must be reconciled with Finance.

| Option | Three-year cost | Modelled benefits | Undiscounted net | Principal trade-off |
|---|---:|---:|---:|---|
| Reinforce legacy estates | €4,400,000 | €0 | -€4,400,000 | Retains fragmented reconciliation |
| Phased regional migration | €6,800,000 | €9,900,000 | +€3,100,000 | Long dual-run period, controlled exposure |
| Single multi-region cutover | €8,100,000 | €10,400,000 | +€2,300,000 | High settlement-continuity risk |

Criteria: delivery continuity (30%), control/evidence integrity (25%), total cost/value (25%), operability and exit flexibility (20%). The options are assessed on the same scope; apparent value must not substitute for a risk acceptance decision.

<a id="dcs-decision-paper.tradeoffs"></a>
## Trade-offs, dependencies and residual risk

**Preferred path:** phased regional replacement with parallel ledger and controlled reconciliation. The main trade-off is faster delivery and clearer ownership in exchange for settlement finality mismatch, cross-border data movement and correlated regional failure. Detailed boundary: The programme has three explicit failure domains, jurisdiction-specific residency rules, intraday settlement cut-offs and an independently reconciled dual-run ledger; unsafe cross-region failover must not be assumed legal.

Principal dependencies are identity integration, verified retention and recovery arrangements, availability of the receiving operations team, and evidence that the design meets **30 minutes RTO** and **5 minutes RPO**. Key residual risk `OPG-RSM-RISK-01` is retained with Enterprise Financial Risk Officer pending a tested restoration procedure. The indicative benefit model is sensitive to adoption: at 20% fewer realised benefits, model net value becomes €1,120,000.

Stop conditions: unresolved unauthorised data transfer, missing operational ownership, absent fallback procedure or reconciliation imbalance. Mitigations must be verified, not merely asserted.

<a id="dcs-decision-paper.recommendation"></a>
## Recommendation, conditions and implementation gate

Recommend **conditional selection of phased regional replacement with parallel ledger and controlled reconciliation**, not production approval. Rationale: it offers the best illustrative outcome when evaluated against traceability, delivery continuity and cost; the high-risk alternative increases blast radius without proportionate value.

Conditions before authorisation: (1) validate baseline and cost assumptions with source records; (2) approve the solution ADR/HLD; (3) obtain risk-owner treatment decision; (4) rehearse recovery and acceptance tests; (5) document vendor exit and portability arrangements. The authority should record approve/defer/reject, conditions, date and source hash in `OPG-RSM-DR-01`.

## Evidence register, assumptions and limitations

- **OPG-RSM-E-BASE — Baseline:** measured incidents/service levels to be sourced from operating systems **Status:** hypothetical.
- **OPG-RSM-E-COST — Finance model:** cost and benefit workbook with owners and sensitivity inputs **Status:** hypothetical.
- **OPG-RSM-E-RISK — Risk assessment:** risk register and treatment evidence **Status:** pending.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `OPG-RSM-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** OPG-RSM-ADR-01, OPG-RSM-HLD-01, OPG-RSM-RA-01, OPG-RSM-BC-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.




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

### Residual uncertainty and evidence provenance

Rank open assumptions by decision sensitivity rather than listing every unknown. Distinguish model assumptions from independent operational measurements, and map each material claim to an evidence ID plus verification status. Report a counterfactual: what new fact would make the preferred option cease to be preferred? Preserve the rejected options and the basis for rejection so a future reviewer can reconstruct the decision without reconstructing an AI conversation.

### Enterprise review challenge and operational hand-off

The reviewer should challenge the weakest evidence source before accepting the proposed conclusion, including dependency coupling, supplier exit conditions and whether ownership survives organizational change. If a required artifact is missing, record an unresolved gap rather than generating plausible-looking completion text. Translate each material concern into a downstream receiving artifact with stable ID, explicit owner and verification condition.

The following review disposition is intentionally **OPEN**: professional approval absent; operating evidence not provided; example cannot be repurposed as a production release, financial authorization or safety assurance.

