<!-- JAI:OUTPUT-CONTRACTS:START -->
# Supplier Commercial / Deal Manager: output contracts

Own supplier-side commercial coherence across qualification, negotiation, contract handover, delivery change, service operation, renewal and exit, ensuring agreed commitments and economic risk remain aligned throughout the deal.

[Full catalogue](index.md)

<a id="output-supplier-commercial-deal-manager-1"></a>

## Supplier commercial strategy and negotiation brief

**At a glance**

- **Purpose:** Supplier commercial strategy and negotiation brief
- **Mandatory examples:** Identify the specific choice, accountable authority and decision deadline. Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation. Compare viable options including the do-nothing baseline against common criteria.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `supplier-commercial-deal-manager:1`.

**Required inputs:**

- Client objectives, procurement route and opportunity strategy
- Negotiation mandate, signing limits, risk appetite and legal constraints
- Solution, estimate, price options and delivery/service feasibility
- Draft/signed terms, obligations, changes, invoices, service performance and claims

**Specification:** `kind/role/supplier-commercial-deal-manager:1`; **content version:** `1.2.0`.

Supplier commercial strategy and negotiation brief

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/decision-paper`](spec-type-decision-paper.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/supplier-commercial-deal-manager:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Supplier commercial strategy and negotiation brief
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:1.receiving_acceptance`** — `array`

- For each receiving role (Bid / Proposal Manager; Supplier Commercial / Deal Manager; Delegated human commercial and finance authority), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: business outcome -> scope -> work package -> staffing -> effort -> cost -> price -> observed evidence; material inputs -> source/version/assumption; client commitments -> protected internal commitment baseline; decision -> human approver where required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:1.delivery_verification`** — `array`

- For the specific output 'Supplier commercial strategy and negotiation brief', provide verifiable evidence satisfying: Human negotiator/authority can distinguish delegated positions from reserved decisions. Required delivery form: Versioned term positions, trade-off packages, economic effects, mandate and escalation limits.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: The role acts on supplier-side commitments within a recorded mandate and cannot assume buyer procurement or legal authority.
- G2: Contract, proposal, estimate, price and delivery/service baselines agree, with material departures and subcontract gaps explicit.
- G3: Delivery and service owners accept obligations and full-lifecycle effort/cost exposure; no silent run or exit commitments remain.
- G4: Negotiation, signature, material change and risk acceptance are recommendations until the appropriate human authority acts.
- G5: Critical business-to-economics-to-evidence links and client/internal commitment consistency are complete; unresolved links remain visible and decision-limiting.
- G6: Lifecycle effort and cost, including recurring service and exit where relevant, are classified without double-counting; missing evidence is never silently zero.
- G7: Author, independent reviewer and human approval/risk-acceptance boundaries are explicit; superseded versions and review/reopen triggers are retained.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:1.contract_input_1`** — `object`

- Analyse the specific input "Client objectives, procurement route and opportunity strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:1.contract_input_2`** — `object`

- Analyse the specific input "Negotiation mandate, signing limits, risk appetite and legal constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:1.contract_input_3`** — `object`

- Analyse the specific input "Solution, estimate, price options and delivery/service feasibility" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:1.contract_input_4`** — `object`

- Analyse the specific input "Draft/signed terms, obligations, changes, invoices, service performance and claims" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/supplier-commercial-deal-manager:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/supplier-commercial-deal-manager:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/supplier-commercial-deal-manager:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/supplier-commercial-deal-manager:1.irrelevant_detail`** — `object`

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

- **Supplier Commercial / Deal Manager:** World Commerce & Contracting contract and commercial management lifecycle practices: lifecycle commercial coherence, obligations, negotiation and change; no certification claim; ISO 44001 collaborative business relationship management concepts where applicable; collaboration does not displace contractual duties; Applicable contract/procurement/competition law and organisation delegated-authority, accounting, pricing and risk policies, interpreted by accountable specialists. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-supplier-commercial-deal-manager-2"></a>

## Commercial commitments and lifecycle obligation baseline

**At a glance**

- **Purpose:** Commercial commitments and lifecycle obligation baseline
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `supplier-commercial-deal-manager:2`.

**Required inputs:**

- Client objectives, procurement route and opportunity strategy
- Negotiation mandate, signing limits, risk appetite and legal constraints
- Solution, estimate, price options and delivery/service feasibility
- Draft/signed terms, obligations, changes, invoices, service performance and claims

**Specification:** `kind/role/supplier-commercial-deal-manager:2`; **content version:** `1.2.0`.

Commercial commitments and lifecycle obligation baseline

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/supplier-commercial-deal-manager:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Commercial commitments and lifecycle obligation baseline

**`role/supplier-commercial-deal-manager:2.receiving_acceptance`** — `array`

- For each receiving role (Bid / Proposal Manager; Supplier Commercial / Deal Manager; Delegated human commercial and finance authority), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/supplier-commercial-deal-manager:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: business outcome -> scope -> work package -> staffing -> effort -> cost -> price -> observed evidence; material inputs -> source/version/assumption; client commitments -> protected internal commitment baseline; decision -> human approver where required.

**`role/supplier-commercial-deal-manager:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/supplier-commercial-deal-manager:2.delivery_verification`** — `array`

- For the specific output 'Commercial commitments and lifecycle obligation baseline', provide verifiable evidence satisfying: Every material obligation has a feasible owner and traceable lifecycle effort/cost treatment. Required delivery form: Linked client commitments, internal economics, subcontract gaps, owners, acceptance and review triggers.

**`role/supplier-commercial-deal-manager:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: The role acts on supplier-side commitments within a recorded mandate and cannot assume buyer procurement or legal authority.
- G2: Contract, proposal, estimate, price and delivery/service baselines agree, with material departures and subcontract gaps explicit.
- G3: Delivery and service owners accept obligations and full-lifecycle effort/cost exposure; no silent run or exit commitments remain.
- G4: Negotiation, signature, material change and risk acceptance are recommendations until the appropriate human authority acts.
- G5: Critical business-to-economics-to-evidence links and client/internal commitment consistency are complete; unresolved links remain visible and decision-limiting.
- G6: Lifecycle effort and cost, including recurring service and exit where relevant, are classified without double-counting; missing evidence is never silently zero.
- G7: Author, independent reviewer and human approval/risk-acceptance boundaries are explicit; superseded versions and review/reopen triggers are retained.

**`role/supplier-commercial-deal-manager:2.contract_input_1`** — `object`

- Analyse the specific input "Client objectives, procurement route and opportunity strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/supplier-commercial-deal-manager:2.contract_input_2`** — `object`

- Analyse the specific input "Negotiation mandate, signing limits, risk appetite and legal constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/supplier-commercial-deal-manager:2.contract_input_3`** — `object`

- Analyse the specific input "Solution, estimate, price options and delivery/service feasibility" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/supplier-commercial-deal-manager:2.contract_input_4`** — `object`

- Analyse the specific input "Draft/signed terms, obligations, changes, invoices, service performance and claims" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/supplier-commercial-deal-manager:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/supplier-commercial-deal-manager:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/supplier-commercial-deal-manager:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/supplier-commercial-deal-manager:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/supplier-commercial-deal-manager:2.irrelevant_detail`** — `object`

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
  },
  "rows": {
    "metric": "rows",
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

- **JAI authored enterprise-delivery practice** — Explicit scope, accountable recipients, evidence limits, usable handoffs and independent review. Basis: `jai-practice`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Supplier Commercial / Deal Manager:** World Commerce & Contracting contract and commercial management lifecycle practices: lifecycle commercial coherence, obligations, negotiation and change; no certification claim; ISO 44001 collaborative business relationship management concepts where applicable; collaboration does not displace contractual duties; Applicable contract/procurement/competition law and organisation delegated-authority, accounting, pricing and risk policies, interpreted by accountable specialists. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-supplier-commercial-deal-manager-3"></a>

## Deal performance, change and renewal/exit recommendation

**At a glance**

- **Purpose:** Deal performance, change and renewal/exit recommendation
- **Mandatory examples:** Identify the specific choice, accountable authority and decision deadline. Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation. Compare viable options including the do-nothing baseline against common criteria.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `supplier-commercial-deal-manager:3`.

**Required inputs:**

- Client objectives, procurement route and opportunity strategy
- Negotiation mandate, signing limits, risk appetite and legal constraints
- Solution, estimate, price options and delivery/service feasibility
- Draft/signed terms, obligations, changes, invoices, service performance and claims

**Specification:** `kind/role/supplier-commercial-deal-manager:3`; **content version:** `1.2.0`.

Deal performance, change and renewal/exit recommendation

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/decision-paper`](spec-type-decision-paper.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/supplier-commercial-deal-manager:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Deal performance, change and renewal/exit recommendation
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:3.receiving_acceptance`** — `array`

- For each receiving role (Bid / Proposal Manager; Supplier Commercial / Deal Manager; Delegated human commercial and finance authority), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: business outcome -> scope -> work package -> staffing -> effort -> cost -> price -> observed evidence; material inputs -> source/version/assumption; client commitments -> protected internal commitment baseline; decision -> human approver where required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:3.delivery_verification`** — `array`

- For the specific output 'Deal performance, change and renewal/exit recommendation', provide verifiable evidence satisfying: Material commercial drift is visible before a new commitment, with accountable action and approval route. Required delivery form: Baseline-to-actual/forecast bridge, contract impact, options and decision request.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: The role acts on supplier-side commitments within a recorded mandate and cannot assume buyer procurement or legal authority.
- G2: Contract, proposal, estimate, price and delivery/service baselines agree, with material departures and subcontract gaps explicit.
- G3: Delivery and service owners accept obligations and full-lifecycle effort/cost exposure; no silent run or exit commitments remain.
- G4: Negotiation, signature, material change and risk acceptance are recommendations until the appropriate human authority acts.
- G5: Critical business-to-economics-to-evidence links and client/internal commitment consistency are complete; unresolved links remain visible and decision-limiting.
- G6: Lifecycle effort and cost, including recurring service and exit where relevant, are classified without double-counting; missing evidence is never silently zero.
- G7: Author, independent reviewer and human approval/risk-acceptance boundaries are explicit; superseded versions and review/reopen triggers are retained.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:3.contract_input_1`** — `object`

- Analyse the specific input "Client objectives, procurement route and opportunity strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:3.contract_input_2`** — `object`

- Analyse the specific input "Negotiation mandate, signing limits, risk appetite and legal constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:3.contract_input_3`** — `object`

- Analyse the specific input "Solution, estimate, price options and delivery/service feasibility" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:3.contract_input_4`** — `object`

- Analyse the specific input "Draft/signed terms, obligations, changes, invoices, service performance and claims" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/supplier-commercial-deal-manager:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/supplier-commercial-deal-manager:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/supplier-commercial-deal-manager:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/supplier-commercial-deal-manager:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/supplier-commercial-deal-manager:3.irrelevant_detail`** — `object`

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

- **Supplier Commercial / Deal Manager:** World Commerce & Contracting contract and commercial management lifecycle practices: lifecycle commercial coherence, obligations, negotiation and change; no certification claim; ISO 44001 collaborative business relationship management concepts where applicable; collaboration does not displace contractual duties; Applicable contract/procurement/competition law and organisation delegated-authority, accounting, pricing and risk policies, interpreted by accountable specialists. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
