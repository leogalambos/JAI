<!-- JAI:OUTPUT-CONTRACTS:START -->
# Commercial Pricing / Deal Finance Specialist: output contracts

Develop defensible supplier selling-price and deal-finance recommendations that connect delivery cost, cash flow, commercial terms and uncertainty to authorised return and risk appetite over the full contract lifecycle.

[Full catalogue](index.md)

<a id="output-commercial-pricing-deal-finance-specialist-1"></a>

## Deal financial and cash-flow model

**At a glance**

- **Purpose:** Deal financial and cash-flow model
- **Mandatory examples:** Identify sponsor, financial owner, funding decision and appraisal horizon. Show dated currency, baseline, costs and non-overlapping benefits with assumptions. Assess uncertain benefit, cost and timing assumptions and assign realisation owners.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `commercial-pricing-deal-finance-specialist:1`.

**Required inputs:**

- Scoped cost and effort estimate with uncertainty and resource rates
- Margin, return, discount, contingency and credit policy
- Payment, acceptance, liability, indexation, SLA, currency and exit terms
- Billing milestones, delivery/service schedule and resource pyramid

**Specification:** `kind/role/commercial-pricing-deal-finance-specialist:1`; **content version:** `1.2.0`.

Deal financial and cash-flow model

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/business-case`](spec-type-business-case.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/commercial-pricing-deal-finance-specialist:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Deal financial and cash-flow model
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:1.receiving_acceptance`** — `array`

- For each receiving role (Bid / Proposal Manager; Supplier Commercial / Deal Manager; Delegated human commercial and finance authority), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: business outcome -> scope -> work package -> staffing -> effort -> cost -> price -> observed evidence; material inputs -> source/version/assumption; client commitments -> protected internal commitment baseline; decision -> human approver where required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:1.delivery_verification`** — `array`

- For the specific output 'Deal financial and cash-flow model', provide verifiable evidence satisfying: Inputs, units, formulas, dependencies and policy treatment reconcile; no unsupported precision. Required delivery form: Versioned, reproducible calculations with cost bridge, price options, margin, cash and sensitivities.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Price reconciles to attributable scope, effort, rates and cost; every material adjustment or reserve has rationale and owner.
- G2: Margin and markup, cash and revenue, cost rate and sell rate are unambiguously distinguished.
- G3: Downside cases cover delivery and run/exit obligations, including schedule, volume and payment uncertainty.
- G4: No recommendation is treated as a signed price, discount approval, credit decision or legal/accounting opinion.
- G5: Critical business-to-economics-to-evidence links and client/internal commitment consistency are complete; unresolved links remain visible and decision-limiting.
- G6: Lifecycle effort and cost, including recurring service and exit where relevant, are classified without double-counting; missing evidence is never silently zero.
- G7: Author, independent reviewer and human approval/risk-acceptance boundaries are explicit; superseded versions and review/reopen triggers are retained.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:1.contract_input_1`** — `object`

- Analyse the specific input "Scoped cost and effort estimate with uncertainty and resource rates" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:1.contract_input_2`** — `object`

- Analyse the specific input "Margin, return, discount, contingency and credit policy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:1.contract_input_3`** — `object`

- Analyse the specific input "Payment, acceptance, liability, indexation, SLA, currency and exit terms" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:1.contract_input_4`** — `object`

- Analyse the specific input "Billing milestones, delivery/service schedule and resource pyramid" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:1.deal_model_assumptions`** — `array`

- Identify the exact deal scenario, term, currency, price/escalation basis, volumes, staffing/productivity, rates, tax/working-capital assumptions where applicable, source and accountable assumption owner.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:1.deal_model_calculations`** — `array`

- Provide inspectable formulas linking assumptions to delivery costs, supplier/customer cash-flow timing, revenues, margin and funding exposure; identify units, period granularity and calculation dependencies rather than supplying unexplained totals.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:1.deal_model_controls`** — `object`

- Reconcile detailed schedules and totals, expose formula/input inconsistencies and run sensitivity scenarios for material volume, timing, cost and collection assumptions; separate a modelled outcome from an approved price or commitment.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/commercial-pricing-deal-finance-specialist:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/commercial-pricing-deal-finance-specialist:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/commercial-pricing-deal-finance-specialist:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/commercial-pricing-deal-finance-specialist:1.irrelevant_detail`** — `object`

- Remove material unrelated to the stated purpose, required input analysis or receiving-role action.

### Proportionate scope

Inherited size guidance is reproduced below. It is not evidence of substantive completeness; verbosity is not a quality measure.

```json
{
  "semantic_units": {
    "metric": "semantic_units",
    "calibration_basis": "Modality-specific information coverage; numerical envelopes require approved enterprise calibration.",
    "minimum_is_quality_gate": false,
    "calibration_status": "synthetic-only",
    "allowance_rules": [
      "Document complexity and audience need; excess requires review, not automatic rejection."
    ],
    "annex_rules": [
      "Reference canonical detail rather than repeat it."
    ]
  }
}
```

### Professional sources and their limits

- **[HM Treasury, The Green Book](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)** — Options, appraisal, costs, benefits, risk, uncertainty and evaluation; used as a practice reference outside its own jurisdiction. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **JAI authored enterprise-delivery practice** — Explicit scope, accountable recipients, evidence limits, usable handoffs and independent review. Basis: `jai-practice`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Commercial Pricing / Deal Finance Specialist:** GAO Cost Estimating and Assessment Guide, GAO-20-195G (2020): credible cost baselines, risk/sensitivity analysis and updates with actuals; adapted to supplier deals, not a claim of GAO certification; IFRS 15 Revenue from Contracts with Customers, where applicable: route identification of performance obligations and revenue recognition to authorised accounting specialists; Organisation treasury, tax, pricing, credit and accounting policies; IAS 21 for applicable currency accounting questions, with qualified finance review. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-commercial-pricing-deal-finance-specialist-2"></a>

## Pricing and commercial trade-off recommendation

**At a glance**

- **Purpose:** Pricing and commercial trade-off recommendation
- **Mandatory examples:** Identify the specific choice, accountable authority and decision deadline. Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation. Compare viable options including the do-nothing baseline against common criteria.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `commercial-pricing-deal-finance-specialist:2`.

**Required inputs:**

- Scoped cost and effort estimate with uncertainty and resource rates
- Margin, return, discount, contingency and credit policy
- Payment, acceptance, liability, indexation, SLA, currency and exit terms
- Billing milestones, delivery/service schedule and resource pyramid

**Specification:** `kind/role/commercial-pricing-deal-finance-specialist:2`; **content version:** `1.2.0`.

Pricing and commercial trade-off recommendation

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/decision-paper`](spec-type-decision-paper.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/commercial-pricing-deal-finance-specialist:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Pricing and commercial trade-off recommendation
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:2.receiving_acceptance`** — `array`

- For each receiving role (Bid / Proposal Manager; Supplier Commercial / Deal Manager; Delegated human commercial and finance authority), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: business outcome -> scope -> work package -> staffing -> effort -> cost -> price -> observed evidence; material inputs -> source/version/assumption; client commitments -> protected internal commitment baseline; decision -> human approver where required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:2.delivery_verification`** — `array`

- For the specific output 'Pricing and commercial trade-off recommendation', provide verifiable evidence satisfying: Human decision owner can see trade-offs, limits and residual risk for the complete lifecycle. Required delivery form: Option paper covering price, terms, discount, reserves, return and downside exposure.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Price reconciles to attributable scope, effort, rates and cost; every material adjustment or reserve has rationale and owner.
- G2: Margin and markup, cash and revenue, cost rate and sell rate are unambiguously distinguished.
- G3: Downside cases cover delivery and run/exit obligations, including schedule, volume and payment uncertainty.
- G4: No recommendation is treated as a signed price, discount approval, credit decision or legal/accounting opinion.
- G5: Critical business-to-economics-to-evidence links and client/internal commitment consistency are complete; unresolved links remain visible and decision-limiting.
- G6: Lifecycle effort and cost, including recurring service and exit where relevant, are classified without double-counting; missing evidence is never silently zero.
- G7: Author, independent reviewer and human approval/risk-acceptance boundaries are explicit; superseded versions and review/reopen triggers are retained.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:2.contract_input_1`** — `object`

- Analyse the specific input "Scoped cost and effort estimate with uncertainty and resource rates" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:2.contract_input_2`** — `object`

- Analyse the specific input "Margin, return, discount, contingency and credit policy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:2.contract_input_3`** — `object`

- Analyse the specific input "Payment, acceptance, liability, indexation, SLA, currency and exit terms" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:2.contract_input_4`** — `object`

- Analyse the specific input "Billing milestones, delivery/service schedule and resource pyramid" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/commercial-pricing-deal-finance-specialist:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/commercial-pricing-deal-finance-specialist:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/commercial-pricing-deal-finance-specialist:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/commercial-pricing-deal-finance-specialist:2.irrelevant_detail`** — `object`

- Remove material unrelated to the stated purpose, required input analysis or receiving-role action.

### Proportionate scope

Inherited size guidance is reproduced below. It is not evidence of substantive completeness; verbosity is not a quality measure.

```json
{
  "semantic_units": {
    "metric": "semantic_units",
    "calibration_basis": "Modality-specific information coverage; numerical envelopes require approved enterprise calibration.",
    "minimum_is_quality_gate": false,
    "calibration_status": "synthetic-only",
    "allowance_rules": [
      "Document complexity and audience need; excess requires review, not automatic rejection."
    ],
    "annex_rules": [
      "Reference canonical detail rather than repeat it."
    ]
  }
}
```

### Professional sources and their limits

- **[HM Treasury, The Green Book](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)** — Options, appraisal, costs, benefits, risk, uncertainty and evaluation; used as a practice reference outside its own jurisdiction. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Commercial Pricing / Deal Finance Specialist:** GAO Cost Estimating and Assessment Guide, GAO-20-195G (2020): credible cost baselines, risk/sensitivity analysis and updates with actuals; adapted to supplier deals, not a claim of GAO certification; IFRS 15 Revenue from Contracts with Customers, where applicable: route identification of performance obligations and revenue recognition to authorised accounting specialists; Organisation treasury, tax, pricing, credit and accounting policies; IAS 21 for applicable currency accounting questions, with qualified finance review. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-commercial-pricing-deal-finance-specialist-3"></a>

## Deal baseline and variance review

**At a glance**

- **Purpose:** Deal baseline and variance review
- **Mandatory examples:** Identify the specific choice, accountable authority and decision deadline. Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation. Compare viable options including the do-nothing baseline against common criteria.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `commercial-pricing-deal-finance-specialist:3`.

**Required inputs:**

- Scoped cost and effort estimate with uncertainty and resource rates
- Margin, return, discount, contingency and credit policy
- Payment, acceptance, liability, indexation, SLA, currency and exit terms
- Billing milestones, delivery/service schedule and resource pyramid

**Specification:** `kind/role/commercial-pricing-deal-finance-specialist:3`; **content version:** `1.2.0`.

Deal baseline and variance review

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/decision-paper`](spec-type-decision-paper.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/commercial-pricing-deal-finance-specialist:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Deal baseline and variance review
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:3.receiving_acceptance`** — `array`

- For each receiving role (Bid / Proposal Manager; Supplier Commercial / Deal Manager; Delegated human commercial and finance authority), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: business outcome -> scope -> work package -> staffing -> effort -> cost -> price -> observed evidence; material inputs -> source/version/assumption; client commitments -> protected internal commitment baseline; decision -> human approver where required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:3.delivery_verification`** — `array`

- For the specific output 'Deal baseline and variance review', provide verifiable evidence satisfying: Material adverse variance has an owner, threshold, corrective option and decision date. Required delivery form: Signed-scope financial baseline, actuals, forecast at completion and change effects.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Price reconciles to attributable scope, effort, rates and cost; every material adjustment or reserve has rationale and owner.
- G2: Margin and markup, cash and revenue, cost rate and sell rate are unambiguously distinguished.
- G3: Downside cases cover delivery and run/exit obligations, including schedule, volume and payment uncertainty.
- G4: No recommendation is treated as a signed price, discount approval, credit decision or legal/accounting opinion.
- G5: Critical business-to-economics-to-evidence links and client/internal commitment consistency are complete; unresolved links remain visible and decision-limiting.
- G6: Lifecycle effort and cost, including recurring service and exit where relevant, are classified without double-counting; missing evidence is never silently zero.
- G7: Author, independent reviewer and human approval/risk-acceptance boundaries are explicit; superseded versions and review/reopen triggers are retained.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:3.contract_input_1`** — `object`

- Analyse the specific input "Scoped cost and effort estimate with uncertainty and resource rates" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:3.contract_input_2`** — `object`

- Analyse the specific input "Margin, return, discount, contingency and credit policy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:3.contract_input_3`** — `object`

- Analyse the specific input "Payment, acceptance, liability, indexation, SLA, currency and exit terms" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:3.contract_input_4`** — `object`

- Analyse the specific input "Billing milestones, delivery/service schedule and resource pyramid" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/commercial-pricing-deal-finance-specialist:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/commercial-pricing-deal-finance-specialist:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/commercial-pricing-deal-finance-specialist:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/commercial-pricing-deal-finance-specialist:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/commercial-pricing-deal-finance-specialist:3.irrelevant_detail`** — `object`

- Remove material unrelated to the stated purpose, required input analysis or receiving-role action.

### Proportionate scope

Inherited size guidance is reproduced below. It is not evidence of substantive completeness; verbosity is not a quality measure.

```json
{
  "semantic_units": {
    "metric": "semantic_units",
    "calibration_basis": "Modality-specific information coverage; numerical envelopes require approved enterprise calibration.",
    "minimum_is_quality_gate": false,
    "calibration_status": "synthetic-only",
    "allowance_rules": [
      "Document complexity and audience need; excess requires review, not automatic rejection."
    ],
    "annex_rules": [
      "Reference canonical detail rather than repeat it."
    ]
  }
}
```

### Professional sources and their limits

- **[HM Treasury, The Green Book](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)** — Options, appraisal, costs, benefits, risk, uncertainty and evaluation; used as a practice reference outside its own jurisdiction. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Commercial Pricing / Deal Finance Specialist:** GAO Cost Estimating and Assessment Guide, GAO-20-195G (2020): credible cost baselines, risk/sensitivity analysis and updates with actuals; adapted to supplier deals, not a claim of GAO certification; IFRS 15 Revenue from Contracts with Customers, where applicable: route identification of performance obligations and revenue recognition to authorised accounting specialists; Organisation treasury, tax, pricing, credit and accounting policies; IAS 21 for applicable currency accounting questions, with qualified finance review. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
