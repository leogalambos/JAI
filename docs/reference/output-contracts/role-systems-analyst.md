<!-- JAI:OUTPUT-CONTRACTS:START -->
# Systems Analyst: output contracts

Bridge requirements and existing systems: what the systems do now, what they must do, and what has to change

[Full catalogue](index.md)

<a id="output-systems-analyst-1"></a>

## System behaviour specification

**At a glance**

- **Purpose:** Produce and govern the role deliverable: System behaviour specification.
- **Mandatory examples:** Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `systems-analyst:1`.

**Required inputs:**

- Requirements baseline
- System documentation and source
- Data structures and dictionaries
- Interface contracts

**Specification:** `kind/role/systems-analyst:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: System behaviour specification.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/requirements-specification`](spec-family-requirements-specification.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `requirements-specification`.

Uniquely identified verifiable requirements with rationale, priority, sources and acceptance conditions.

**Evidence accompanying the work product:**

- forward/backward traceability
- conflict, interface and change-impact checks

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/systems-analyst:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: System behaviour specification.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:1.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Test Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:1.delivery_verification`** — `array`

- For the specific output 'System behaviour specification', provide verifiable evidence satisfying: Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. Existing source requirement: Every requirement is atomic, testable and traced to a source and a priority. Required delivery form: Uniquely identified verifiable requirements with rationale, priority, sources and acceptance conditions.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("System behaviour specification") has been walked through with the people who will build, test and operate the result.
- G5: Every field-level mapping is validated against real production data samples, not against documentation alone
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:1.contract_input_1`** — `object`

- Analyse the specific input "Requirements baseline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:1.contract_input_2`** — `object`

- Analyse the specific input "System documentation and source" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:1.contract_input_3`** — `object`

- Analyse the specific input "Data structures and dictionaries" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:1.contract_input_4`** — `object`

- Analyse the specific input "Interface contracts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/systems-analyst:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/systems-analyst:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/systems-analyst:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/systems-analyst:1.irrelevant_detail`** — `object`

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

- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Systems Analyst:** UML; IEEE 29148 requirements; data mapping practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace source needs, stakeholders and conflicting constraints into verifiable requirements, models and acceptance criteria.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-systems-analyst-2"></a>

## interface and data mapping

**At a glance**

- **Purpose:** Produce and govern the role deliverable: interface and data mapping.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `systems-analyst:2`.

**Required inputs:**

- Requirements baseline
- System documentation and source
- Data structures and dictionaries
- Interface contracts

**Specification:** `kind/role/systems-analyst:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: interface and data mapping.

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

**`role/systems-analyst:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: interface and data mapping.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:2.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Test Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:2.delivery_verification`** — `array`

- For the specific output 'interface and data mapping', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("System behaviour specification") has been walked through with the people who will build, test and operate the result.
- G5: Every field-level mapping is validated against real production data samples, not against documentation alone
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:2.contract_input_1`** — `object`

- Analyse the specific input "Requirements baseline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:2.contract_input_2`** — `object`

- Analyse the specific input "System documentation and source" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:2.contract_input_3`** — `object`

- Analyse the specific input "Data structures and dictionaries" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:2.contract_input_4`** — `object`

- Analyse the specific input "Interface contracts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/systems-analyst:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/systems-analyst:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/systems-analyst:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/systems-analyst:2.irrelevant_detail`** — `object`

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

- **Systems Analyst:** UML; IEEE 29148 requirements; data mapping practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace source needs, stakeholders and conflicting constraints into verifiable requirements, models and acceptance criteria.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-systems-analyst-3"></a>

## impact analysis across systems

**At a glance**

- **Purpose:** Produce and govern the role deliverable: impact analysis across systems.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `systems-analyst:3`.

**Required inputs:**

- Requirements baseline
- System documentation and source
- Data structures and dictionaries
- Interface contracts

**Specification:** `kind/role/systems-analyst:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: impact analysis across systems.

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

**`role/systems-analyst:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: impact analysis across systems.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:3.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Test Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:3.delivery_verification`** — `array`

- For the specific output 'impact analysis across systems', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("System behaviour specification") has been walked through with the people who will build, test and operate the result.
- G5: Every field-level mapping is validated against real production data samples, not against documentation alone
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:3.contract_input_1`** — `object`

- Analyse the specific input "Requirements baseline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:3.contract_input_2`** — `object`

- Analyse the specific input "System documentation and source" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:3.contract_input_3`** — `object`

- Analyse the specific input "Data structures and dictionaries" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:3.contract_input_4`** — `object`

- Analyse the specific input "Interface contracts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/systems-analyst:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/systems-analyst:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/systems-analyst:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/systems-analyst:3.irrelevant_detail`** — `object`

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

- **Systems Analyst:** UML; IEEE 29148 requirements; data mapping practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace source needs, stakeholders and conflicting constraints into verifiable requirements, models and acceptance criteria.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-systems-analyst-4"></a>

## transition and migration rules

**At a glance**

- **Purpose:** Produce and govern the role deliverable: transition and migration rules.
- **Mandatory examples:** Specify deployment, verification, rollback and reproducible acceptance tests. Specify schemas, error states, concurrency and compatibility requirements. Define typed configuration values, units, versions and permitted ranges without secrets.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `systems-analyst:4`.

**Required inputs:**

- Requirements baseline
- System documentation and source
- Data structures and dictionaries
- Interface contracts

**Specification:** `kind/role/systems-analyst:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: transition and migration rules.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/implementation-specification`](spec-type-implementation-specification.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `implementation-specification`.

Typed implementation specification with exact target versions, interfaces and verification/recovery conditions.

**Evidence accompanying the work product:**

- parameter/schema constraints
- reproducible acceptance and recovery procedure

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/systems-analyst:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: transition and migration rules.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:4.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Test Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:4.delivery_verification`** — `array`

- For the specific output 'transition and migration rules', provide verifiable evidence satisfying: Identify exact component/environment versions and each required parameter with type, unit, permitted range, default and secret-reference handling. State interface schemas, input/output semantics, error responses, concurrency/idempotency expectations and external dependency constraints. Give reproducible build/deploy/verification steps, expected results, stop conditions and recovery path; identify evidence still required before execution. Required delivery form: Typed implementation specification with exact target versions, interfaces and verification/recovery conditions.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("System behaviour specification") has been walked through with the people who will build, test and operate the result.
- G5: Every field-level mapping is validated against real production data samples, not against documentation alone
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:4.contract_input_1`** — `object`

- Analyse the specific input "Requirements baseline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:4.contract_input_2`** — `object`

- Analyse the specific input "System documentation and source" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:4.contract_input_3`** — `object`

- Analyse the specific input "Data structures and dictionaries" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:4.contract_input_4`** — `object`

- Analyse the specific input "Interface contracts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/systems-analyst:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/systems-analyst:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/systems-analyst:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/systems-analyst:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/systems-analyst:4.irrelevant_detail`** — `object`

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
  "typed": {
    "metric": "typed",
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

- **[NIST SP 800-218, Secure Software Development Framework Version 1.1](https://doi.org/10.6028/NIST.SP.800-218)** — Secure development practices, protected source/build inputs, verification and vulnerability response. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Systems Analyst:** UML; IEEE 29148 requirements; data mapping practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace source needs, stakeholders and conflicting constraints into verifiable requirements, models and acceptance criteria.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
