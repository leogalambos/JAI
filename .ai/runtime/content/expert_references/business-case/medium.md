---
reference_id: example:business-case:medium
schema_version: '1.0.0'
document_kind: business-case
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/business-case
approval_status: not-human-approved
content_revision: 2.3.0
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Meridian Retail Group · Order Event Integration · `MRG-OEI` · MEDIUM complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Digital Commerce Sponsor. **Scope:** multi-system integration with phased market rollout.

# Investment business case — Order Event Integration

<a id="dcs-business-case.investment_request"></a>
## Investment request and accountability

Request conditional authorisation to invest in **managed event backbone and decoupled ERP adapters** to address batch latency and failed reconciliation delaying order promises. Business sponsor: Digital Commerce Sponsor; delegated cost owner: Finance Business Partner (not yet named in the illustrative record). Funding envelope €1,250,000 over 2027–2029; no capital commitment is implied. Expected decision forum: Architecture Review Board.

Target outcome is move accepted-order visibility from the next batch cycle to 5 minutes at p95, without losing order records. Benefits ownership remains with the operating function rather than automatically transferring to the implementation team.

<a id="dcs-business-case.investment_options"></a>
## Investment choices and do-nothing baseline

Three options within the same illustrative three-year horizon: **no investment / baseline** incurs €550,000 of legacy operation or remediation cost; **preferred** managed event backbone and decoupled ERP adapters incurs €1,250,000 and could produce €2,150,000 of quantifiable benefits; **alternative** extend synchronous API fan-out and nightly reconciliation incurs €1,900,000 against €2,350,000 in modelled benefits.

The alternative may have different delivery risk, maintenance burden and portability. Baseline benefits are not double-counted in the preferred option. Finance must independently verify that benefits are genuinely incremental to the baseline and not already recognised elsewhere.

<a id="dcs-business-case.financial_model"></a>
## Financial model, scope and cash flow

Illustrative **nominal, undiscounted** cash flow; currency **EUR**, calendar years 2027–2029. Figures are invented model assumptions, not quotations, commitments, accounting forecasts or a regulatory ROI calculation.

| Year | Cash cost | Incremental realised benefit | Net cash flow | Cumulative net |
|---|---:|---:|---:|---:|
| 2027 | €650,000 | €250,000 | €-400,000 | €-400,000 |
| 2028 | €350,000 | €800,000 | €450,000 | €50,000 |
| 2029 | €250,000 | €1,100,000 | €850,000 | €900,000 |

Three-year total **TCO €1,250,000**, benefits **€2,150,000**, simple net **€900,000**. The model includes setup, implementation, subscriptions/support and operational change. It excludes tax effects, financing costs and time-value discounting pending corporate finance methodology. Physical assets, shadow labour and exit liabilities require an explicit reconciliation before board submission.

<a id="dcs-business-case.sensitivity"></a>
## Sensitivity, dependencies and decision limits

| Benefit realisation | Cost factor | Three-year net |
|---|---|---:|
| 80% | 100% | €470,000 |
| 100% | 100% | €900,000 |
| 100% | 125% | €587,500 |
| 80% | 125% | €157,500 |

The decision is most sensitive to actual adoption, interface complexity and supplier charges. Trigger a reforecast if forecast TCO rises by more than 15%, if annual benefit realisation is below 80% of plan for two reporting periods or if 2 hours cannot be demonstrated. The financial model does not justify relaxing a security or statutory control.

Dependency chain: validated baseline → target architecture → phased implementation → operational readiness → benefits measurement. Risks: lost or duplicated events, country-specific data routing and supplier dependency; accountable risk owner: Head of Digital Risk.

<a id="dcs-business-case.benefit_realisation"></a>
## Benefit-realisation plan and follow-up

Benefits owner: Digital Commerce Sponsor; financial tracking: Finance Business Partner; technical operating measures: p95 order latency, lost-event count, replay rate and order reconciliation gap. The baseline must be collected from source systems for at least one representative operating cycle before go-live. Review at 30, 90 and 180 days after launch, then quarterly; record realised net benefits separately from avoided costs, non-cash service quality and compliance risk reduction.

If milestones are missed, suspend discretionary rollout and request an updated business case, not retrospective rewriting of original assumptions. The committee must decide whether to approve stage 1, conditionally defer or reject, and maintain an immutable decision record.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `MRG-OEI` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Incremental finance baseline | Is this statement supported for `MRG-OEI` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| NPV/TCO sensitivity assumptions | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Accountable benefit owner | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — customer commitment integrity

Trace the exact customer-requested outcome to a separately priced deliverable and explicit acceptance test; classify any unsupported requirement as an assumption or clarification. For **business-case**, the reviewer should actively challenge **incremental finance baseline** and **npv/tco sensitivity assumptions**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — contractual acceptance boundary

Distinguish indicative estimate, binding price, third-party pass-through and client internal cost. Change in scope requires a defined change-order rather than implied free delivery. The accountable party for this illustrative acceptance is **Bid Manager / Commercial Owner**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** incremental finance baseline, npv/tco sensitivity assumptions, and accountable benefit owner. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

## Evidence register, assumptions and limitations

- **MRG-OEI-E-FIN — Cost model:** versioned detailed line items, date/currency assumptions and accountable cost sign-off **Status:** synthetic.
- **MRG-OEI-E-BEN — Benefit register:** measurement definitions, owner and duplication checks **Status:** synthetic.
- **MRG-OEI-E-DEP — Dependencies:** supplier price/exit obligations and delivery estimates **Status:** pending.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `MRG-OEI-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** MRG-OEI-DR-01, MRG-OEI-FIN-01, MRG-OEI-OPS-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.




## Professional deepening: decision rationale and practical checks

### Accounting and model integrity

Present incremental cash flows relative to a clearly declared baseline, with explicit horizon, currency, nominal/real basis, tax treatment and discount convention. Separate cost avoidance, cash-releasing savings, productivity capacity, revenue uplift and risk reduction; these categories must not be added together without checks for overlap. Assign each cost and benefit line to a named accountable function. A planning model is not an approved forecast.

### Discounted economics and scenario bounds

Illustrative evaluation can use an 8% year-end discount rate if Finance has not supplied an authoritative rate, clearly marked as an assumption. Apply NPV = sum(net cash flow in year t / (1+r)^t) and do not silently mix the capital approval envelope with benefit realisation. Show base, downside and upside scenarios with both benefits and supplier costs changing; identify the break-even adoption level. A sensitivity table only varying one driver at a time understates correlated downside.

### Benefits evidence and anti-double-counting controls

| Benefit category | Operational measure | Baseline evidence | Accountable owner | Double-count guard |
|---|---|---|---|---|
| Cycle-time reduction | p95 completion time | Timestamped process sample | Process owner | Exclude hours already included in capacity gain |
| Avoided incidents | Verified incident frequency | ITSM incident register | Service owner | Do not treat hypothetical loss as realised cash |
| Revenue protection | Completed valid transactions | Reconciled finance ledger | Finance owner | Separate gross turnover from contribution margin |
| Compliance improvement | Control failures and exposure | Assessment record | Risk owner | Report qualitatively unless model independently approved |

### Funding gates and exit economics

Allocate spend by reversible discovery, implementation and transition stages. Each tranche should have a named sponsor, acceptance evidence and stop condition. Include dual-running, training, supplier exit, data retention and decommissioning in TCO. Identify constraints that might force a more expensive but legally viable option. A positive NPV cannot authorise a risk outside appetite or override procurement policy.

