---
reference_id: example:business-case:complex
schema_version: '1.0.0'
document_kind: business-case
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/business-case
approval_status: not-human-approved
content_revision: 2.0.0
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Orion Payments Group · Regulated Settlement Modernisation · `OPG-RSM` · COMPLEX complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Group Payments Executive. **Scope:** multi-jurisdiction mission-critical transformation with regulatory obligations determined per entity.

# Investment business case — Regulated Settlement Modernisation

<a id="dcs-business-case.investment_request"></a>
## Investment request and accountability

Request conditional authorisation to invest in **phased regional replacement with parallel ledger and controlled reconciliation** to address legacy component concentration, missed settlement deadlines and fragmented reconciliation evidence. Business sponsor: Group Payments Executive; delegated cost owner: Finance Business Partner (not yet named in the illustrative record). Funding envelope €6,800,000 over 2027–2029; no capital commitment is implied. Expected decision forum: Investment Committee and Architecture Authority.

Target outcome is achieve complete instruction lineage and timely settlement at defined cut-offs with zero unexplained financial imbalance. Benefits ownership remains with the operating function rather than automatically transferring to the implementation team.

<a id="dcs-business-case.investment_options"></a>
## Investment choices and do-nothing baseline

Three options within the same illustrative three-year horizon: **no investment / baseline** incurs €4,400,000 of legacy operation or remediation cost; **preferred** phased regional replacement with parallel ledger and controlled reconciliation incurs €6,800,000 and could produce €9,900,000 of quantifiable benefits; **alternative** single-cutover replacement across all jurisdictions incurs €8,100,000 against €10,400,000 in modelled benefits.

The alternative may have different delivery risk, maintenance burden and portability. Baseline benefits are not double-counted in the preferred option. Finance must independently verify that benefits are genuinely incremental to the baseline and not already recognised elsewhere.

<a id="dcs-business-case.financial_model"></a>
## Financial model, scope and cash flow

Illustrative **nominal, undiscounted** cash flow; currency **EUR**, calendar years 2027–2029. Figures are invented model assumptions, not quotations, commitments, accounting forecasts or a regulatory ROI calculation.

| Year | Cash cost | Incremental realised benefit | Net cash flow | Cumulative net |
|---|---:|---:|---:|---:|
| 2027 | €3,400,000 | €1,000,000 | €-2,400,000 | €-2,400,000 |
| 2028 | €2,000,000 | €3,400,000 | €1,400,000 | €-1,000,000 |
| 2029 | €1,400,000 | €5,500,000 | €4,100,000 | €3,100,000 |

Three-year total **TCO €6,800,000**, benefits **€9,900,000**, simple net **€3,100,000**. The model includes setup, implementation, subscriptions/support and operational change. It excludes tax effects, financing costs and time-value discounting pending corporate finance methodology. Physical assets, shadow labour and exit liabilities require an explicit reconciliation before board submission.

<a id="dcs-business-case.sensitivity"></a>
## Sensitivity, dependencies and decision limits

| Benefit realisation | Cost factor | Three-year net |
|---|---|---:|
| 80% | 100% | €1,120,000 |
| 100% | 100% | €3,100,000 |
| 100% | 125% | €1,400,000 |
| 80% | 125% | €-580,000 |

The decision is most sensitive to actual adoption, interface complexity and supplier charges. Trigger a reforecast if forecast TCO rises by more than 15%, if annual benefit realisation is below 80% of plan for two reporting periods or if 30 minutes cannot be demonstrated. The financial model does not justify relaxing a security or statutory control.

Dependency chain: validated baseline → target architecture → phased implementation → operational readiness → benefits measurement. Risks: settlement finality mismatch, cross-border data movement and correlated regional failure; accountable risk owner: Enterprise Financial Risk Officer.

<a id="dcs-business-case.benefit_realisation"></a>
## Benefit-realisation plan and follow-up

Benefits owner: Group Payments Executive; financial tracking: Finance Business Partner; technical operating measures: unmatched ledger entries, finality latency, jurisdiction cut-off breaches, recovery drill results. The baseline must be collected from source systems for at least one representative operating cycle before go-live. Review at 30, 90 and 180 days after launch, then quarterly; record realised net benefits separately from avoided costs, non-cash service quality and compliance risk reduction.

If milestones are missed, suspend discretionary rollout and request an updated business case, not retrospective rewriting of original assumptions. The committee must decide whether to approve stage 1, conditionally defer or reject, and maintain an immutable decision record.

## Evidence register, assumptions and limitations

- **OPG-RSM-E-FIN — Cost model:** versioned detailed line items, date/currency assumptions and accountable cost sign-off **Status:** synthetic.
- **OPG-RSM-E-BEN — Benefit register:** measurement definitions, owner and duplication checks **Status:** synthetic.
- **OPG-RSM-E-DEP — Dependencies:** supplier price/exit obligations and delivery estimates **Status:** pending.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `OPG-RSM-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** OPG-RSM-DR-01, OPG-RSM-FIN-01, OPG-RSM-OPS-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.




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

### Post-go-live value assurance

Track forecast, actual and explanation by reporting period; do not retrospectively overwrite the approved assumptions. Define who can validate a claimed cash saving versus non-cash service improvement. Capture negative outcomes, such as increased support burden, so the benefit report does not selectively count successes. At post-implementation review, distinguish opportunity remaining from value already booked in financial accounts.

### Enterprise review challenge and operational hand-off

The reviewer should challenge the weakest evidence source before accepting the proposed conclusion, including dependency coupling, supplier exit conditions and whether ownership survives organizational change. If a required artifact is missing, record an unresolved gap rather than generating plausible-looking completion text. Translate each material concern into a downstream receiving artifact with stable ID, explicit owner and verification condition.

The following review disposition is intentionally **OPEN**: professional approval absent; operating evidence not provided; example cannot be repurposed as a production release, financial authorization or safety assurance.

