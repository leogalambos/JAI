<!-- JAI:OUTPUT-CONTRACTS:START -->
# AI Safety and Model Red Team Specialist: output contracts

Probe models and AI systems for harmful, unsafe or manipulable behaviour before users find it

[Full catalogue](index.md)

<a id="output-ai-safety-and-model-red-team-specialist-1"></a>

## Adversarial evaluation suite and results

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Adversarial evaluation suite and results.
- **Mandatory examples:** Give reproducible invocation, assertions, expected outcomes and failure diagnostics; distinguish test definitions from evidence of executed runs. Define isolation, dependency handling, flakiness investigation, coverage limitations and maintenance ownership. Trace executable cases and reusable test abstractions to requirements, risk coverage, deterministic data and environment assumptions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `ai-safety-and-model-red-team-specialist:1`.

**Required inputs:**

- Model and system under evaluation
- Use case and deployment context
- Policy and harm definitions
- Prior incident and abuse reports

**Specification:** `kind/role/ai-safety-and-model-red-team-specialist:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Adversarial evaluation suite and results.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/automated-tests`](spec-family-automated-tests.md)
- [`domain/testing`](spec-domain-testing.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `executable-test-suite`.

Executable automated checks with deterministic setup, expected assertions and reproducible invocation.

**Evidence accompanying the work product:**

- exact suite and tested revision
- risk/requirement coverage and actual run results

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/ai-safety-and-model-red-team-specialist:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Adversarial evaluation suite and results.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:1.receiving_acceptance`** — `array`

- For each receiving role (Machine Learning Engineer; AI Solutions Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:1.delivery_verification`** — `array`

- For the specific output 'Adversarial evaluation suite and results', provide verifiable evidence satisfying: Trace executable cases and reusable test abstractions to requirements, risk coverage, deterministic data and environment assumptions. Give reproducible invocation, assertions, expected outcomes and failure diagnostics; distinguish test definitions from evidence of executed runs. Define isolation, dependency handling, flakiness investigation, coverage limitations and maintenance ownership. Required delivery form: Executable automated checks with deterministic setup, expected assertions and reproducible invocation.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Adversarial evaluation suite and results") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Testing runs against the deployment configuration users will actually get, and findings are reported with severity, reproducibility and a mitigation owner
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:1.contract_input_1`** — `object`

- Analyse the specific input "Model and system under evaluation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:1.contract_input_2`** — `object`

- Analyse the specific input "Use case and deployment context" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:1.contract_input_3`** — `object`

- Analyse the specific input "Policy and harm definitions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:1.contract_input_4`** — `object`

- Analyse the specific input "Prior incident and abuse reports" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/ai-safety-and-model-red-team-specialist:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/ai-safety-and-model-red-team-specialist:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/ai-safety-and-model-red-team-specialist:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/ai-safety-and-model-red-team-specialist:1.irrelevant_detail`** — `object`

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
- **[NIST SP 800-218, Secure Software Development Framework Version 1.1](https://doi.org/10.6028/NIST.SP.800-218)** — Secure development practices, protected source/build inputs, verification and vulnerability response. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **AI Safety and Model Red Team Specialist:** NIST AI RMF 1.0; AI red-teaming practice; OWASP Top 10 for LLM applications. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-ai-safety-and-model-red-team-specialist-2"></a>

## harm taxonomy and severity ratings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: harm taxonomy and severity ratings.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `ai-safety-and-model-red-team-specialist:2`.

**Required inputs:**

- Model and system under evaluation
- Use case and deployment context
- Policy and harm definitions
- Prior incident and abuse reports

**Specification:** `kind/role/ai-safety-and-model-red-team-specialist:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: harm taxonomy and severity ratings.

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

**`role/ai-safety-and-model-red-team-specialist:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: harm taxonomy and severity ratings.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:2.receiving_acceptance`** — `array`

- For each receiving role (Machine Learning Engineer; AI Solutions Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:2.delivery_verification`** — `array`

- For the specific output 'harm taxonomy and severity ratings', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Adversarial evaluation suite and results") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Testing runs against the deployment configuration users will actually get, and findings are reported with severity, reproducibility and a mitigation owner
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:2.contract_input_1`** — `object`

- Analyse the specific input "Model and system under evaluation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:2.contract_input_2`** — `object`

- Analyse the specific input "Use case and deployment context" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:2.contract_input_3`** — `object`

- Analyse the specific input "Policy and harm definitions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:2.contract_input_4`** — `object`

- Analyse the specific input "Prior incident and abuse reports" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/ai-safety-and-model-red-team-specialist:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/ai-safety-and-model-red-team-specialist:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/ai-safety-and-model-red-team-specialist:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/ai-safety-and-model-red-team-specialist:2.irrelevant_detail`** — `object`

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
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **AI Safety and Model Red Team Specialist:** NIST AI RMF 1.0; AI red-teaming practice; OWASP Top 10 for LLM applications. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-ai-safety-and-model-red-team-specialist-3"></a>

## jailbreak and misuse findings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: jailbreak and misuse findings.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `ai-safety-and-model-red-team-specialist:3`.

**Required inputs:**

- Model and system under evaluation
- Use case and deployment context
- Policy and harm definitions
- Prior incident and abuse reports

**Specification:** `kind/role/ai-safety-and-model-red-team-specialist:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: jailbreak and misuse findings.

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

**`role/ai-safety-and-model-red-team-specialist:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: jailbreak and misuse findings.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:3.receiving_acceptance`** — `array`

- For each receiving role (Machine Learning Engineer; AI Solutions Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:3.delivery_verification`** — `array`

- For the specific output 'jailbreak and misuse findings', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Existing source requirement: Reproduction steps are complete enough for an independent party to confirm. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Adversarial evaluation suite and results") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Testing runs against the deployment configuration users will actually get, and findings are reported with severity, reproducibility and a mitigation owner
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:3.contract_input_1`** — `object`

- Analyse the specific input "Model and system under evaluation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:3.contract_input_2`** — `object`

- Analyse the specific input "Use case and deployment context" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:3.contract_input_3`** — `object`

- Analyse the specific input "Policy and harm definitions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:3.contract_input_4`** — `object`

- Analyse the specific input "Prior incident and abuse reports" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/ai-safety-and-model-red-team-specialist:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/ai-safety-and-model-red-team-specialist:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/ai-safety-and-model-red-team-specialist:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/ai-safety-and-model-red-team-specialist:3.irrelevant_detail`** — `object`

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
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **AI Safety and Model Red Team Specialist:** NIST AI RMF 1.0; AI red-teaming practice; OWASP Top 10 for LLM applications. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-ai-safety-and-model-red-team-specialist-4"></a>

## mitigation recommendations and retest results

**At a glance**

- **Purpose:** Produce and govern the role deliverable: mitigation recommendations and retest results.
- **Mandatory examples:** Define tested obligations, assurance period, sample and exclusions. Link procedures and observed results to immutable evidence and located deviations. Limit the independent conclusion to tested scope, evidence strength and unresolved findings.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `ai-safety-and-model-red-team-specialist:4`.

**Required inputs:**

- Model and system under evaluation
- Use case and deployment context
- Policy and harm definitions
- Prior incident and abuse reports

**Specification:** `kind/role/ai-safety-and-model-red-team-specialist:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: mitigation recommendations and retest results.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/assurance-report`](spec-type-assurance-report.md)
- [`domain/security`](spec-domain-security.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `assurance-assessment`.

Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.

**Evidence accompanying the work product:**

- criterion-to-test-to-observation traceability
- independent reviewer and limitations

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/ai-safety-and-model-red-team-specialist:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: mitigation recommendations and retest results.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:4.receiving_acceptance`** — `array`

- For each receiving role (Machine Learning Engineer; AI Solutions Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:4.delivery_verification`** — `array`

- For the specific output 'mitigation recommendations and retest results', provide verifiable evidence satisfying: State assessment objectives, criteria versions, scope, period, population, sample rationale and exclusions before drawing conclusions. For each criterion, identify procedure, sample, observed result, supporting material and located deviations; distinguish absent evidence from demonstrated failure. Bound the conclusion by coverage and limitations; list findings, severity rationale, management response, remediation owner and verification needed for closure. Existing source requirement: Identifies assessed scope, method, environment or population, expected and observed outcomes, located findings, untested conditions and residual limitations. Required delivery form: Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Adversarial evaluation suite and results") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Testing runs against the deployment configuration users will actually get, and findings are reported with severity, reproducibility and a mitigation owner
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:4.contract_input_1`** — `object`

- Analyse the specific input "Model and system under evaluation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:4.contract_input_2`** — `object`

- Analyse the specific input "Use case and deployment context" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:4.contract_input_3`** — `object`

- Analyse the specific input "Policy and harm definitions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:4.contract_input_4`** — `object`

- Analyse the specific input "Prior incident and abuse reports" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/ai-safety-and-model-red-team-specialist:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/ai-safety-and-model-red-team-specialist:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/ai-safety-and-model-red-team-specialist:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/ai-safety-and-model-red-team-specialist:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/ai-safety-and-model-red-team-specialist:4.irrelevant_detail`** — `object`

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

- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **AI Safety and Model Red Team Specialist:** NIST AI RMF 1.0; AI red-teaming practice; OWASP Top 10 for LLM applications. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
