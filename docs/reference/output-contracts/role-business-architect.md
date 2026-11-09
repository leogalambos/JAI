<!-- JAI:OUTPUT-CONTRACTS:START -->
# Business Architect: output contracts

Model what the business does and needs to be able to do, independent of how systems currently support it

[Full catalogue](index.md)

<a id="output-business-architect-1"></a>

## Business capability model

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Business capability model.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `business-architect:1`.

**Required inputs:**

- Corporate strategy
- Operating model and org structure
- Process models
- Performance pain points

**Specification:** `kind/role/business-architect:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Business capability model.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/model`](spec-type-model.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `typed-semantic-model`.

Versioned typed model with stable entities, relations, constraints, provenance and selected views.

**Evidence accompanying the work product:**

- metamodel/reference/cross-view checks
- source baseline and unresolved semantic gaps

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/business-architect:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Business capability model.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:1.receiving_acceptance`** — `array`

- For each receiving role (Enterprise Architect; Enterprise Business Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:1.delivery_verification`** — `array`

- For the specific output 'Business capability model', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Existing source requirement: The model is validated against real observed behaviour or data, not only interviews. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Capabilities are expressed as what the business does, never as system or department names, so the model survives reorganisation
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:1.contract_input_1`** — `object`

- Analyse the specific input "Corporate strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:1.contract_input_2`** — `object`

- Analyse the specific input "Operating model and org structure" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:1.contract_input_3`** — `object`

- Analyse the specific input "Process models" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:1.contract_input_4`** — `object`

- Analyse the specific input "Performance pain points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/business-architect:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/business-architect:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/business-architect:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/business-architect:1.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Business Architect:** BIZBOK; TOGAF 10 business architecture; value stream mapping. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-business-architect-2"></a>

## value stream maps

**At a glance**

- **Purpose:** Produce and govern the role deliverable: value stream maps.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `business-architect:2`.

**Required inputs:**

- Corporate strategy
- Operating model and org structure
- Process models
- Performance pain points

**Specification:** `kind/role/business-architect:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: value stream maps.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/model`](spec-type-model.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `typed-semantic-model`.

Versioned typed model with stable entities, relations, constraints, provenance and selected views.

**Evidence accompanying the work product:**

- metamodel/reference/cross-view checks
- source baseline and unresolved semantic gaps

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/business-architect:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: value stream maps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:2.receiving_acceptance`** — `array`

- For each receiving role (Enterprise Architect; Enterprise Business Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:2.delivery_verification`** — `array`

- For the specific output 'value stream maps', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Capabilities are expressed as what the business does, never as system or department names, so the model survives reorganisation
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:2.contract_input_1`** — `object`

- Analyse the specific input "Corporate strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:2.contract_input_2`** — `object`

- Analyse the specific input "Operating model and org structure" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:2.contract_input_3`** — `object`

- Analyse the specific input "Process models" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:2.contract_input_4`** — `object`

- Analyse the specific input "Performance pain points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/business-architect:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/business-architect:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/business-architect:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/business-architect:2.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Business Architect:** BIZBOK; TOGAF 10 business architecture; value stream mapping. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-business-architect-3"></a>

## capability heat map against strategy

**At a glance**

- **Purpose:** Produce and govern the role deliverable: capability heat map against strategy.
- **Mandatory examples:** Explain thresholds, uncertainty, missing data and actions supported by the view. Define metrics, units, denominators, targets, refresh cadence and accountable owners. Provide dated observations linked to versioned source queries and population scope.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `business-architect:3`.

**Required inputs:**

- Corporate strategy
- Operating model and org structure
- Process models
- Performance pain points

**Specification:** `kind/role/business-architect:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: capability heat map against strategy.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/dashboard`](spec-type-dashboard.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `measured-dashboard`.

Dashboard or scorecard with metric definitions, observations, source queries and interpretation.

**Evidence accompanying the work product:**

- units, denominators and measurement windows
- dated values, thresholds and actionable exceptions

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/business-architect:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: capability heat map against strategy.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:3.receiving_acceptance`** — `array`

- For each receiving role (Enterprise Architect; Enterprise Business Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:3.delivery_verification`** — `array`

- For the specific output 'capability heat map against strategy', provide verifiable evidence satisfying: For each metric, define question, formula, unit, population/denominator, time window, target/threshold and accountable owner. Show observation timestamp, source/query version, aggregation, missing-data handling and measurement limitations. Explain threshold crossings and trends, uncertainty and the action or decision supported; distinguish operational signals from causal explanations. Required delivery form: Dashboard or scorecard with metric definitions, observations, source queries and interpretation.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Capabilities are expressed as what the business does, never as system or department names, so the model survives reorganisation
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:3.contract_input_1`** — `object`

- Analyse the specific input "Corporate strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:3.contract_input_2`** — `object`

- Analyse the specific input "Operating model and org structure" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:3.contract_input_3`** — `object`

- Analyse the specific input "Process models" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:3.contract_input_4`** — `object`

- Analyse the specific input "Performance pain points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/business-architect:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/business-architect:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/business-architect:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/business-architect:3.irrelevant_detail`** — `object`

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

- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Business Architect:** BIZBOK; TOGAF 10 business architecture; value stream mapping. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-business-architect-4"></a>

## business architecture roadmap

**At a glance**

- **Purpose:** Produce and govern the role deliverable: business architecture roadmap.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `business-architect:4`.

**Required inputs:**

- Corporate strategy
- Operating model and org structure
- Process models
- Performance pain points

**Specification:** `kind/role/business-architect:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: business architecture roadmap.

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

**`role/business-architect:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: business architecture roadmap.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:4.receiving_acceptance`** — `array`

- For each receiving role (Enterprise Architect; Enterprise Business Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:4.delivery_verification`** — `array`

- For the specific output 'business architecture roadmap', provide verifiable evidence satisfying: State business outcomes, current/target baseline, planning horizons, sponsors and material planning assumptions. For each increment, identify deliverables, owner, indicative resource/funding requirement, milestone and measurable completion outcome. Identify dependencies and critical sequence, decision dates, constraints and alternative paths; distinguish committed work from tentative options. Existing source requirement: Every element traces to a driver or a quality-attribute target; no orphan elements. Required delivery form: Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Capabilities are expressed as what the business does, never as system or department names, so the model survives reorganisation
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:4.contract_input_1`** — `object`

- Analyse the specific input "Corporate strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:4.contract_input_2`** — `object`

- Analyse the specific input "Operating model and org structure" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:4.contract_input_3`** — `object`

- Analyse the specific input "Process models" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:4.contract_input_4`** — `object`

- Analyse the specific input "Performance pain points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/business-architect:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/business-architect:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/business-architect:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/business-architect:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/business-architect:4.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Business Architect:** BIZBOK; TOGAF 10 business architecture; value stream mapping. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
