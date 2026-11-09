<!-- JAI:OUTPUT-CONTRACTS:START -->
# Process Analyst: output contracts

Model, measure and improve how work actually flows through the organisation

[Full catalogue](index.md)

<a id="output-process-analyst-1"></a>

## As-is and to-be process models

**At a glance**

- **Purpose:** Produce and govern the role deliverable: As-is and to-be process models.
- **Mandatory examples:** List stable source-model element IDs, typed relations and labels represented in the view. Evidence endpoint validity, semantic compatibility, coverage and visual readability. Define the concern, viewpoint, system boundary, legend and notation.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `process-analyst:1`.

**Required inputs:**

- Observed process execution
- Event log data
- Control requirements
- Volume and cost data

**Specification:** `kind/role/process-analyst:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: As-is and to-be process models.

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

**`role/process-analyst:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: As-is and to-be process models.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:1.receiving_acceptance`** — `array`

- For each receiving role (Solution Architect; Software Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:1.delivery_verification`** — `array`

- For the specific output 'As-is and to-be process models', provide verifiable evidence satisfying: Identify diagram purpose, scope, audience, version and notation/legend, including the meaning of every relationship type. Use stable element identifiers and meaningful labels; show relevant boundaries, directions, interfaces and external dependencies without invented facts. Check consistency with source models and related views; distinguish intentional abstraction from omitted or unresolved relationships. Existing source requirement: The model is validated against real observed behaviour or data, not only interviews. Required delivery form: Concern-specific diagram with declared notation, legend, typed relationships and source-element links.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("As-is and to-be process models") has been walked through with the people who will build, test and operate the result.
- G5: The as-is model is validated against event data or direct observation, never against what management believes the process to be
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:1.contract_input_1`** — `object`

- Analyse the specific input "Observed process execution" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:1.contract_input_2`** — `object`

- Analyse the specific input "Event log data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:1.contract_input_3`** — `object`

- Analyse the specific input "Control requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:1.contract_input_4`** — `object`

- Analyse the specific input "Volume and cost data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/process-analyst:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/process-analyst:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/process-analyst:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/process-analyst:1.irrelevant_detail`** — `object`

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
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Process Analyst:** BPMN 2.0; DMN; Lean and value stream mapping; process mining practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace source needs, stakeholders and conflicting constraints into verifiable requirements, models and acceptance criteria.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-process-analyst-2"></a>

## process performance analysis

**At a glance**

- **Purpose:** Produce and govern the role deliverable: process performance analysis.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `process-analyst:2`.

**Required inputs:**

- Observed process execution
- Event log data
- Control requirements
- Volume and cost data

**Specification:** `kind/role/process-analyst:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: process performance analysis.

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

**`role/process-analyst:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: process performance analysis.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:2.receiving_acceptance`** — `array`

- For each receiving role (Solution Architect; Software Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:2.delivery_verification`** — `array`

- For the specific output 'process performance analysis', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("As-is and to-be process models") has been walked through with the people who will build, test and operate the result.
- G5: The as-is model is validated against event data or direct observation, never against what management believes the process to be
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:2.contract_input_1`** — `object`

- Analyse the specific input "Observed process execution" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:2.contract_input_2`** — `object`

- Analyse the specific input "Event log data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:2.contract_input_3`** — `object`

- Analyse the specific input "Control requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:2.contract_input_4`** — `object`

- Analyse the specific input "Volume and cost data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/process-analyst:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/process-analyst:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/process-analyst:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/process-analyst:2.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Process Analyst:** BPMN 2.0; DMN; Lean and value stream mapping; process mining practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace source needs, stakeholders and conflicting constraints into verifiable requirements, models and acceptance criteria.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-process-analyst-3"></a>

## control point map

**At a glance**

- **Purpose:** Produce and govern the role deliverable: control point map.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `process-analyst:3`.

**Required inputs:**

- Observed process execution
- Event log data
- Control requirements
- Volume and cost data

**Specification:** `kind/role/process-analyst:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: control point map.

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

**`role/process-analyst:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: control point map.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:3.receiving_acceptance`** — `array`

- For each receiving role (Solution Architect; Software Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:3.delivery_verification`** — `array`

- For the specific output 'control point map', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("As-is and to-be process models") has been walked through with the people who will build, test and operate the result.
- G5: The as-is model is validated against event data or direct observation, never against what management believes the process to be
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:3.contract_input_1`** — `object`

- Analyse the specific input "Observed process execution" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:3.contract_input_2`** — `object`

- Analyse the specific input "Event log data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:3.contract_input_3`** — `object`

- Analyse the specific input "Control requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:3.contract_input_4`** — `object`

- Analyse the specific input "Volume and cost data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/process-analyst:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/process-analyst:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/process-analyst:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/process-analyst:3.irrelevant_detail`** — `object`

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
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Process Analyst:** BPMN 2.0; DMN; Lean and value stream mapping; process mining practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace source needs, stakeholders and conflicting constraints into verifiable requirements, models and acceptance criteria.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-process-analyst-4"></a>

## improvement case

**At a glance**

- **Purpose:** Produce and govern the role deliverable: improvement case.
- **Mandatory examples:** Identify sponsor, financial owner, funding decision and appraisal horizon. Show dated currency, baseline, costs and non-overlapping benefits with assumptions. Assess uncertain benefit, cost and timing assumptions and assign realisation owners.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `process-analyst:4`.

**Required inputs:**

- Observed process execution
- Event log data
- Control requirements
- Volume and cost data

**Specification:** `kind/role/process-analyst:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: improvement case.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/business-case`](spec-type-business-case.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `investment-appraisal`.

Reconciled investment appraisal with dated financial model and accountable benefits.

**Evidence accompanying the work product:**

- source cash flows and calculations
- scenario sensitivity and benefit ownership

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/process-analyst:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: improvement case.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:4.receiving_acceptance`** — `array`

- For each receiving role (Solution Architect; Software Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:4.delivery_verification`** — `array`

- For the specific output 'improvement case', provide verifiable evidence satisfying: State sponsor, financial owner, investment boundary, appraisal period and the precise funding or continuation decision requested. Show source and date of costs/benefits, currency, price basis, cash-flow periods, baseline and incremental treatment; avoid double-counted benefits. Identify key uncertain variables, sensitivity/scenario results, benefit measures, baseline, accountable realisation owner and review trigger. Required delivery form: Reconciled investment appraisal with dated financial model and accountable benefits.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("As-is and to-be process models") has been walked through with the people who will build, test and operate the result.
- G5: The as-is model is validated against event data or direct observation, never against what management believes the process to be
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:4.contract_input_1`** — `object`

- Analyse the specific input "Observed process execution" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:4.contract_input_2`** — `object`

- Analyse the specific input "Event log data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:4.contract_input_3`** — `object`

- Analyse the specific input "Control requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:4.contract_input_4`** — `object`

- Analyse the specific input "Volume and cost data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/process-analyst:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/process-analyst:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/process-analyst:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/process-analyst:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/process-analyst:4.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Process Analyst:** BPMN 2.0; DMN; Lean and value stream mapping; process mining practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace source needs, stakeholders and conflicting constraints into verifiable requirements, models and acceptance criteria.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
