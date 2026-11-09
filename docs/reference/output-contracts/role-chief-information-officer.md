<!-- JAI:OUTPUT-CONTRACTS:START -->
# Chief Information Officer: output contracts

Own the enterprise IT capability, its budget, its risk posture and its ability to serve the business

[Full catalogue](index.md)

<a id="output-chief-information-officer-1"></a>

## IT strategy

**At a glance**

- **Purpose:** Produce and govern the role deliverable: IT strategy.
- **Mandatory examples:** Compare investment and operating choices, dependencies, resource assumptions and rejected alternatives. Trace target outcomes and measurable success to business direction and baseline constraints. Assign sequenced initiatives, accountable owners, outcome measures and review triggers.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `chief-information-officer:1`.

**Required inputs:**

- Board and business strategy
- Risk appetite statement
- Demand pipeline
- Current cost and run position

**Specification:** `kind/role/chief-information-officer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: IT strategy.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/strategy`](spec-family-strategy.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `strategy`.

Evidenced strategic choices with target outcomes, alternatives, investment assumptions and execution accountability.

**Evidence accompanying the work product:**

- baseline and rejected options
- outcome measures, dependencies and review triggers

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/chief-information-officer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: IT strategy.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:1.receiving_acceptance`** — `array`

- For each receiving role (VP of Engineering; Head of Platform; IT Service Owner; IT Governance Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:1.delivery_verification`** — `array`

- For the specific output 'IT strategy', provide verifiable evidence satisfying: Trace target outcomes and measurable success to business direction and baseline constraints. Compare investment and operating choices, dependencies, resource assumptions and rejected alternatives. Assign sequenced initiatives, accountable owners, outcome measures and review triggers. Required delivery form: Evidenced strategic choices with target outcomes, alternatives, investment assumptions and execution accountability.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No option set is presented without a costed do-nothing baseline.
- G2: Every approved investment has a named accountable business owner (a person, not a committee) and one primary benefit measure.
- G3: Residual risk is explicitly accepted in writing by the person carrying the risk, at the correct level of authority.
- G4: The decision record states what would make this decision wrong, and when it will be re-tested.
- G5: Every portfolio item has a named business owner accountable for the benefit, not an IT sponsor standing in for one
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:1.contract_input_1`** — `object`

- Analyse the specific input "Board and business strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:1.contract_input_2`** — `object`

- Analyse the specific input "Risk appetite statement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:1.contract_input_3`** — `object`

- Analyse the specific input "Demand pipeline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:1.contract_input_4`** — `object`

- Analyse the specific input "Current cost and run position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/chief-information-officer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/chief-information-officer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/chief-information-officer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/chief-information-officer:1.irrelevant_detail`** — `object`

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

- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[HM Treasury, The Green Book](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)** — Options, appraisal, costs, benefits, risk, uncertainty and evaluation; used as a practice reference outside its own jurisdiction. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Chief Information Officer:** COBIT 2019 (EDM domain); ISO/IEC 38500; ITIL 4. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Connect strategic choices, investment options, measurable outcomes, risk appetite and accountable decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-chief-information-officer-2"></a>

## IT investment portfolio

**At a glance**

- **Purpose:** Produce and govern the role deliverable: IT investment portfolio.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `chief-information-officer:2`.

**Required inputs:**

- Board and business strategy
- Risk appetite statement
- Demand pipeline
- Current cost and run position

**Specification:** `kind/role/chief-information-officer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: IT investment portfolio.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `governed-register`.

Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.

**Evidence accompanying the work product:**

- actual source-attributed records
- uniqueness, completeness and relationship reconciliation

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/chief-information-officer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: IT investment portfolio.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:2.receiving_acceptance`** — `array`

- For each receiving role (VP of Engineering; Head of Platform; IT Service Owner; IT Governance Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:2.delivery_verification`** — `array`

- For the specific output 'IT investment portfolio', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No option set is presented without a costed do-nothing baseline.
- G2: Every approved investment has a named accountable business owner (a person, not a committee) and one primary benefit measure.
- G3: Residual risk is explicitly accepted in writing by the person carrying the risk, at the correct level of authority.
- G4: The decision record states what would make this decision wrong, and when it will be re-tested.
- G5: Every portfolio item has a named business owner accountable for the benefit, not an IT sponsor standing in for one
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:2.contract_input_1`** — `object`

- Analyse the specific input "Board and business strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:2.contract_input_2`** — `object`

- Analyse the specific input "Risk appetite statement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:2.contract_input_3`** — `object`

- Analyse the specific input "Demand pipeline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:2.contract_input_4`** — `object`

- Analyse the specific input "Current cost and run position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/chief-information-officer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/chief-information-officer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/chief-information-officer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/chief-information-officer:2.irrelevant_detail`** — `object`

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
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[HM Treasury, The Green Book](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)** — Options, appraisal, costs, benefits, risk, uncertainty and evaluation; used as a practice reference outside its own jurisdiction. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Chief Information Officer:** COBIT 2019 (EDM domain); ISO/IEC 38500; ITIL 4. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Connect strategic choices, investment options, measurable outcomes, risk appetite and accountable decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-chief-information-officer-3"></a>

## IT operating model

**At a glance**

- **Purpose:** Produce and govern the role deliverable: IT operating model.
- **Mandatory examples:** List stable source-model element IDs, typed relations and labels represented in the view. Evidence endpoint validity, semantic compatibility, coverage and visual readability. Define the concern, viewpoint, system boundary, legend and notation.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `chief-information-officer:3`.

**Required inputs:**

- Board and business strategy
- Risk appetite statement
- Demand pipeline
- Current cost and run position

**Specification:** `kind/role/chief-information-officer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: IT operating model.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/diagram`](spec-type-diagram.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `model-derived-view`.

Concern-specific diagram with declared notation, legend, typed relationships and source-element links.

**Evidence accompanying the work product:**

- endpoint/meaning/coverage checks
- legibility and explicit projection limitations

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/chief-information-officer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: IT operating model.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:3.receiving_acceptance`** — `array`

- For each receiving role (VP of Engineering; Head of Platform; IT Service Owner; IT Governance Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:3.delivery_verification`** — `array`

- For the specific output 'IT operating model', provide verifiable evidence satisfying: Identify diagram purpose, scope, audience, version and notation/legend, including the meaning of every relationship type. Use stable element identifiers and meaningful labels; show relevant boundaries, directions, interfaces and external dependencies without invented facts. Check consistency with source models and related views; distinguish intentional abstraction from omitted or unresolved relationships. Existing source requirement: The model is validated against real observed behaviour or data, not only interviews. Required delivery form: Concern-specific diagram with declared notation, legend, typed relationships and source-element links.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No option set is presented without a costed do-nothing baseline.
- G2: Every approved investment has a named accountable business owner (a person, not a committee) and one primary benefit measure.
- G3: Residual risk is explicitly accepted in writing by the person carrying the risk, at the correct level of authority.
- G4: The decision record states what would make this decision wrong, and when it will be re-tested.
- G5: Every portfolio item has a named business owner accountable for the benefit, not an IT sponsor standing in for one
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:3.contract_input_1`** — `object`

- Analyse the specific input "Board and business strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:3.contract_input_2`** — `object`

- Analyse the specific input "Risk appetite statement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:3.contract_input_3`** — `object`

- Analyse the specific input "Demand pipeline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:3.contract_input_4`** — `object`

- Analyse the specific input "Current cost and run position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/chief-information-officer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/chief-information-officer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/chief-information-officer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/chief-information-officer:3.irrelevant_detail`** — `object`

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
  "elements": {
    "metric": "elements",
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

- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[HM Treasury, The Green Book](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)** — Options, appraisal, costs, benefits, risk, uncertainty and evaluation; used as a practice reference outside its own jurisdiction. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Chief Information Officer:** COBIT 2019 (EDM domain); ISO/IEC 38500; ITIL 4. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Connect strategic choices, investment options, measurable outcomes, risk appetite and accountable decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-chief-information-officer-4"></a>

## annual IT plan and budget

**At a glance**

- **Purpose:** Produce and govern the role deliverable: annual IT plan and budget.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `chief-information-officer:4`.

**Required inputs:**

- Board and business strategy
- Risk appetite statement
- Demand pipeline
- Current cost and run position

**Specification:** `kind/role/chief-information-officer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: annual IT plan and budget.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/roadmap`](spec-type-roadmap.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `outcome-roadmap`.

Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.

**Evidence accompanying the work product:**

- current/target baseline and planning assumptions
- resource/funding constraints and decision triggers

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/chief-information-officer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: annual IT plan and budget.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:4.receiving_acceptance`** — `array`

- For each receiving role (VP of Engineering; Head of Platform; IT Service Owner; IT Governance Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:4.delivery_verification`** — `array`

- For the specific output 'annual IT plan and budget', provide verifiable evidence satisfying: State business outcomes, current/target baseline, planning horizons, sponsors and material planning assumptions. For each increment, identify deliverables, owner, indicative resource/funding requirement, milestone and measurable completion outcome. Identify dependencies and critical sequence, decision dates, constraints and alternative paths; distinguish committed work from tentative options. Existing source requirement: Every milestone has an acceptance test and a named accountable owner. Required delivery form: Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No option set is presented without a costed do-nothing baseline.
- G2: Every approved investment has a named accountable business owner (a person, not a committee) and one primary benefit measure.
- G3: Residual risk is explicitly accepted in writing by the person carrying the risk, at the correct level of authority.
- G4: The decision record states what would make this decision wrong, and when it will be re-tested.
- G5: Every portfolio item has a named business owner accountable for the benefit, not an IT sponsor standing in for one
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:4.contract_input_1`** — `object`

- Analyse the specific input "Board and business strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:4.contract_input_2`** — `object`

- Analyse the specific input "Risk appetite statement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:4.contract_input_3`** — `object`

- Analyse the specific input "Demand pipeline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:4.contract_input_4`** — `object`

- Analyse the specific input "Current cost and run position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:4.budget_baseline`** — `object`

- State financial year, currency, price/assumption basis, planning scope, accountable budget owner and reconciliation to the current approved baseline.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:4.budget_allocation`** — `array`

- Identify expenditure lines by service/initiative and accountable owner, distinguishing capital/operating and one-off/recurring cost where relevant; state amount, timing, funding source and material dependencies.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:4.budget_reconciliation`** — `object`

- Reconcile allocation totals to the requested envelope and financial periods; show forecast/commitment assumptions, material variances, contingency and the decisions needed for an unfunded or over-budget plan.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/chief-information-officer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chief-information-officer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/chief-information-officer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/chief-information-officer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/chief-information-officer:4.irrelevant_detail`** — `object`

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

- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[HM Treasury, The Green Book](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)** — Options, appraisal, costs, benefits, risk, uncertainty and evaluation; used as a practice reference outside its own jurisdiction. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Chief Information Officer:** COBIT 2019 (EDM domain); ISO/IEC 38500; ITIL 4. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Connect strategic choices, investment options, measurable outcomes, risk appetite and accountable decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
