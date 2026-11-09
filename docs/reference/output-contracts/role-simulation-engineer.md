<!-- JAI:OUTPUT-CONTRACTS:START -->
# Simulation Engineer: output contracts

Build models that predict real-world behaviour well enough to make decisions with

[Full catalogue](index.md)

<a id="output-simulation-engineer-1"></a>

## Simulation models and configurations

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Simulation models and configurations.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `simulation-engineer:1`.

**Required inputs:**

- System behaviour and parameters
- Real-world measurement data
- Decision questions to answer
- Compute resources

**Specification:** `kind/role/simulation-engineer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Simulation models and configurations.

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

**`role/simulation-engineer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Simulation models and configurations.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:1.receiving_acceptance`** — `array`

- For each receiving role (sponsor; Data Scientist), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:1.delivery_verification`** — `array`

- For the specific output 'Simulation models and configurations', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Existing source requirement: The model is validated against real observed behaviour or data, not only interviews. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Every model states its validation evidence and its domain of applicability
- G9: results used outside the validated domain are reported as extrapolation
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:1.contract_input_1`** — `object`

- Analyse the specific input "System behaviour and parameters" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:1.contract_input_2`** — `object`

- Analyse the specific input "Real-world measurement data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:1.contract_input_3`** — `object`

- Analyse the specific input "Decision questions to answer" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:1.contract_input_4`** — `object`

- Analyse the specific input "Compute resources" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/simulation-engineer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/simulation-engineer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/simulation-engineer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/simulation-engineer:1.irrelevant_detail`** — `object`

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
- **[ACM Artifact Review and Badging policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current)** — Artifact availability, evaluation and reproducibility terminology; informative evidence-pack practice, not proof that an experiment is scientifically sufficient. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Simulation Engineer:** simulation verification and validation practice; ASME V&V or domain equivalent; uncertainty quantification. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-simulation-engineer-2"></a>

## validation against real-world data

**At a glance**

- **Purpose:** Produce and govern the role deliverable: validation against real-world data.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `simulation-engineer:2`.

**Required inputs:**

- System behaviour and parameters
- Real-world measurement data
- Decision questions to answer
- Compute resources

**Specification:** `kind/role/simulation-engineer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: validation against real-world data.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/test-report`](spec-type-test-report.md)
- [`domain/testing`](spec-domain-testing.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `test-results`.

Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.

**Evidence accompanying the work product:**

- expected/actual observations and execution references
- coverage denominators and residual defects

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/simulation-engineer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: validation against real-world data.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:2.receiving_acceptance`** — `array`

- For each receiving role (sponsor; Data Scientist), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:2.delivery_verification`** — `array`

- For the specific output 'validation against real-world data', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Every model states its validation evidence and its domain of applicability
- G9: results used outside the validated domain are reported as extrapolation
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:2.contract_input_1`** — `object`

- Analyse the specific input "System behaviour and parameters" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:2.contract_input_2`** — `object`

- Analyse the specific input "Real-world measurement data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:2.contract_input_3`** — `object`

- Analyse the specific input "Decision questions to answer" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:2.contract_input_4`** — `object`

- Analyse the specific input "Compute resources" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/simulation-engineer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/simulation-engineer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/simulation-engineer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/simulation-engineer:2.irrelevant_detail`** — `object`

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

- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ACM Artifact Review and Badging policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current)** — Artifact availability, evaluation and reproducibility terminology; informative evidence-pack practice, not proof that an experiment is scientifically sufficient. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Simulation Engineer:** simulation verification and validation practice; ASME V&V or domain equivalent; uncertainty quantification. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-simulation-engineer-3"></a>

## scenario results and sensitivity analysis

**At a glance**

- **Purpose:** Produce and govern the role deliverable: scenario results and sensitivity analysis.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `simulation-engineer:3`.

**Required inputs:**

- System behaviour and parameters
- Real-world measurement data
- Decision questions to answer
- Compute resources

**Specification:** `kind/role/simulation-engineer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: scenario results and sensitivity analysis.

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

**`role/simulation-engineer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: scenario results and sensitivity analysis.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:3.receiving_acceptance`** — `array`

- For each receiving role (sponsor; Data Scientist), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:3.delivery_verification`** — `array`

- For the specific output 'scenario results and sensitivity analysis', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Every model states its validation evidence and its domain of applicability
- G9: results used outside the validated domain are reported as extrapolation
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:3.contract_input_1`** — `object`

- Analyse the specific input "System behaviour and parameters" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:3.contract_input_2`** — `object`

- Analyse the specific input "Real-world measurement data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:3.contract_input_3`** — `object`

- Analyse the specific input "Decision questions to answer" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:3.contract_input_4`** — `object`

- Analyse the specific input "Compute resources" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/simulation-engineer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/simulation-engineer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/simulation-engineer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/simulation-engineer:3.irrelevant_detail`** — `object`

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
- **[ACM Artifact Review and Badging policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current)** — Artifact availability, evaluation and reproducibility terminology; informative evidence-pack practice, not proof that an experiment is scientifically sufficient. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Simulation Engineer:** simulation verification and validation practice; ASME V&V or domain equivalent; uncertainty quantification. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-simulation-engineer-4"></a>

## model limitation documentation

**At a glance**

- **Purpose:** Produce and govern the role deliverable: model limitation documentation.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `simulation-engineer:4`.

**Required inputs:**

- System behaviour and parameters
- Real-world measurement data
- Decision questions to answer
- Compute resources

**Specification:** `kind/role/simulation-engineer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: model limitation documentation.

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

**`role/simulation-engineer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: model limitation documentation.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:4.receiving_acceptance`** — `array`

- For each receiving role (sponsor; Data Scientist), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:4.delivery_verification`** — `array`

- For the specific output 'model limitation documentation', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Existing source requirement: The model is validated against real observed behaviour or data, not only interviews. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Every model states its validation evidence and its domain of applicability
- G9: results used outside the validated domain are reported as extrapolation
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:4.contract_input_1`** — `object`

- Analyse the specific input "System behaviour and parameters" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:4.contract_input_2`** — `object`

- Analyse the specific input "Real-world measurement data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:4.contract_input_3`** — `object`

- Analyse the specific input "Decision questions to answer" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:4.contract_input_4`** — `object`

- Analyse the specific input "Compute resources" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/simulation-engineer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/simulation-engineer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/simulation-engineer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/simulation-engineer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/simulation-engineer:4.irrelevant_detail`** — `object`

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
- **[ACM Artifact Review and Badging policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current)** — Artifact availability, evaluation and reproducibility terminology; informative evidence-pack practice, not proof that an experiment is scientifically sufficient. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Simulation Engineer:** simulation verification and validation practice; ASME V&V or domain equivalent; uncertainty quantification. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
