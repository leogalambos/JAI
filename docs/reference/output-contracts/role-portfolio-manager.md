<!-- JAI:OUTPUT-CONTRACTS:START -->
# Portfolio Manager: output contracts

Decide which investments the organisation starts, continues and stops, against capacity and strategy

[Full catalogue](index.md)

<a id="output-portfolio-manager-1"></a>

## Investment portfolio and prioritisation model

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Investment portfolio and prioritisation model.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `portfolio-manager:1`.

**Required inputs:**

- Strategic objectives
- Business cases
- Capacity and run-rate
- Benefit performance

**Specification:** `kind/role/portfolio-manager:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Investment portfolio and prioritisation model.

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

**`role/portfolio-manager:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Investment portfolio and prioritisation model.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:1.receiving_acceptance`** — `array`

- For each receiving role (Programme Manager; Epic Owner; PMO Lead), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:1.delivery_verification`** — `array`

- For the specific output 'Investment portfolio and prioritisation model', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Existing source requirement: The model is validated against real observed behaviour or data, not only interviews. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No option set is presented without a costed do-nothing baseline.
- G2: Every approved investment has a named accountable business owner (a person, not a committee) and one primary benefit measure.
- G3: Residual risk is explicitly accepted in writing by the person carrying the risk, at the correct level of authority.
- G4: The decision record states what would make this decision wrong, and when it will be re-tested.
- G5: New work is only started when capacity is freed by stopping or completing something else
- G6: the portfolio never commits beyond measured throughput
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:1.contract_input_1`** — `object`

- Analyse the specific input "Strategic objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:1.contract_input_2`** — `object`

- Analyse the specific input "Business cases" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:1.contract_input_3`** — `object`

- Analyse the specific input "Capacity and run-rate" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:1.contract_input_4`** — `object`

- Analyse the specific input "Benefit performance" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/portfolio-manager:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/portfolio-manager:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/portfolio-manager:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/portfolio-manager:1.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Portfolio Manager:** MoP (Management of Portfolios); lean portfolio management; COBIT 2019 APO05. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-portfolio-manager-2"></a>

## capacity and funding allocation

**At a glance**

- **Purpose:** Produce and govern the role deliverable: capacity and funding allocation.
- **Mandatory examples:** Record source versions, extraction time, transformations, lawful access and retention. Evidence completeness, uniqueness, consistency, drift and permitted-use limitations. Define fields, datatypes, units, keys, null handling and allowed values.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `portfolio-manager:2`.

**Required inputs:**

- Strategic objectives
- Business cases
- Capacity and run-rate
- Benefit performance

**Specification:** `kind/role/portfolio-manager:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: capacity and funding allocation.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/dataset`](spec-type-dataset.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `typed-dataset-or-calculation-model`.

Typed data or calculation model with units, keys/formulas, lineage and quality constraints.

**Evidence accompanying the work product:**

- versioned inputs and reproducible transformations
- reconciliation, quality measures and permitted use

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/portfolio-manager:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: capacity and funding allocation.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:2.receiving_acceptance`** — `array`

- For each receiving role (Programme Manager; Epic Owner; PMO Lead), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:2.delivery_verification`** — `array`

- For the specific output 'capacity and funding allocation', provide verifiable evidence satisfying: Specify field names, meaning, type, units, code lists, keys, relationships, null semantics and permitted values. Identify source systems/extract versions, transformations, time coverage, access/licensing conditions and accountable custodian. Report completeness, validity, consistency and other relevant quality measures with method, population, results and known limitations. Required delivery form: Typed data or calculation model with units, keys/formulas, lineage and quality constraints.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No option set is presented without a costed do-nothing baseline.
- G2: Every approved investment has a named accountable business owner (a person, not a committee) and one primary benefit measure.
- G3: Residual risk is explicitly accepted in writing by the person carrying the risk, at the correct level of authority.
- G4: The decision record states what would make this decision wrong, and when it will be re-tested.
- G5: New work is only started when capacity is freed by stopping or completing something else
- G6: the portfolio never commits beyond measured throughput
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:2.contract_input_1`** — `object`

- Analyse the specific input "Strategic objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:2.contract_input_2`** — `object`

- Analyse the specific input "Business cases" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:2.contract_input_3`** — `object`

- Analyse the specific input "Capacity and run-rate" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:2.contract_input_4`** — `object`

- Analyse the specific input "Benefit performance" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/portfolio-manager:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/portfolio-manager:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/portfolio-manager:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/portfolio-manager:2.irrelevant_detail`** — `object`

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

- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Portfolio Manager:** MoP (Management of Portfolios); lean portfolio management; COBIT 2019 APO05. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-portfolio-manager-3"></a>

## portfolio performance report

**At a glance**

- **Purpose:** Produce and govern the role deliverable: portfolio performance report.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `portfolio-manager:3`.

**Required inputs:**

- Strategic objectives
- Business cases
- Capacity and run-rate
- Benefit performance

**Specification:** `kind/role/portfolio-manager:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: portfolio performance report.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/analysis-report`](spec-family-analysis-report.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `evidence-based-analysis-report`.

Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.

**Evidence accompanying the work product:**

- versioned source/period/population and reproducible method
- observations, uncertainty, counterevidence and accountable follow-up

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/portfolio-manager:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: portfolio performance report.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:3.receiving_acceptance`** — `array`

- For each receiving role (Programme Manager; Epic Owner; PMO Lead), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:3.delivery_verification`** — `array`

- For the specific output 'portfolio performance report', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Existing source requirement: Conclusions are traceable to dated evidence; opinion is visibly separated from fact. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No option set is presented without a costed do-nothing baseline.
- G2: Every approved investment has a named accountable business owner (a person, not a committee) and one primary benefit measure.
- G3: Residual risk is explicitly accepted in writing by the person carrying the risk, at the correct level of authority.
- G4: The decision record states what would make this decision wrong, and when it will be re-tested.
- G5: New work is only started when capacity is freed by stopping or completing something else
- G6: the portfolio never commits beyond measured throughput
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:3.contract_input_1`** — `object`

- Analyse the specific input "Strategic objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:3.contract_input_2`** — `object`

- Analyse the specific input "Business cases" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:3.contract_input_3`** — `object`

- Analyse the specific input "Capacity and run-rate" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:3.contract_input_4`** — `object`

- Analyse the specific input "Benefit performance" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/portfolio-manager:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/portfolio-manager:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/portfolio-manager:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/portfolio-manager:3.irrelevant_detail`** — `object`

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

- **JAI authored enterprise-delivery practice** — Explicit scope, accountable recipients, evidence limits, usable handoffs and independent review. Basis: `jai-practice`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Portfolio Manager:** MoP (Management of Portfolios); lean portfolio management; COBIT 2019 APO05. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-portfolio-manager-4"></a>

## stop/continue decisions

**At a glance**

- **Purpose:** Produce and govern the role deliverable: stop/continue decisions.
- **Mandatory examples:** Identify the specific choice, accountable authority and decision deadline. Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation. Compare viable options including the do-nothing baseline against common criteria.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `portfolio-manager:4`.

**Required inputs:**

- Strategic objectives
- Business cases
- Capacity and run-rate
- Benefit performance

**Specification:** `kind/role/portfolio-manager:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: stop/continue decisions.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/decision-paper`](spec-type-decision-paper.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `decision-paper`.

Bounded decision paper with consistent option comparison and a clear authority/decision request.

**Evidence accompanying the work product:**

- baseline and feasible alternatives
- cost/benefit/uncertainty and consequences

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/portfolio-manager:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: stop/continue decisions.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:4.receiving_acceptance`** — `array`

- For each receiving role (Programme Manager; Epic Owner; PMO Lead), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:4.delivery_verification`** — `array`

- For the specific output 'stop/continue decisions', provide verifiable evidence satisfying: Separate the requested decision from information for noting; state decision scope, eligible authority, deadline and consequences of deferral. List feasible options with consistent evaluation criteria, evidence, costs, benefits and constraints; justify any unavailable baseline. State recommendation, implementation dependencies, uncertainty and residual exposure; show which assumptions would change the preferred option. Required delivery form: Bounded decision paper with consistent option comparison and a clear authority/decision request.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No option set is presented without a costed do-nothing baseline.
- G2: Every approved investment has a named accountable business owner (a person, not a committee) and one primary benefit measure.
- G3: Residual risk is explicitly accepted in writing by the person carrying the risk, at the correct level of authority.
- G4: The decision record states what would make this decision wrong, and when it will be re-tested.
- G5: New work is only started when capacity is freed by stopping or completing something else
- G6: the portfolio never commits beyond measured throughput
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:4.contract_input_1`** — `object`

- Analyse the specific input "Strategic objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:4.contract_input_2`** — `object`

- Analyse the specific input "Business cases" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:4.contract_input_3`** — `object`

- Analyse the specific input "Capacity and run-rate" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:4.contract_input_4`** — `object`

- Analyse the specific input "Benefit performance" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/portfolio-manager:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/portfolio-manager:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/portfolio-manager:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/portfolio-manager:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/portfolio-manager:4.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Portfolio Manager:** MoP (Management of Portfolios); lean portfolio management; COBIT 2019 APO05. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
