<!-- JAI:OUTPUT-CONTRACTS:START -->
# Performance Test Engineer: output contracts

Prove how the system behaves under realistic and unrealistic load, before production does it for you

[Full catalogue](index.md)

<a id="output-performance-test-engineer-1"></a>

## Performance test strategy and workload model

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Performance test strategy and workload model.
- **Mandatory examples:** Define test levels, techniques, environments, representative data and responsibilities. Define traceable entry/exit criteria, coverage measurement and defect disposition rules. Define risk-based test objectives, quality targets, scope and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `performance-test-engineer:1`.

**Required inputs:**

- Non-functional requirements
- Production traffic profiles
- Environment specification
- Business peak forecasts

**Specification:** `kind/role/performance-test-engineer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Performance test strategy and workload model.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/test-strategy`](spec-type-test-strategy.md)
- [`domain/testing`](spec-domain-testing.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `test-specification`.

Risk-based test specification with cases/techniques, expected outcomes, environments and entry/exit criteria.

**Evidence accompanying the work product:**

- requirement/risk-to-case coverage
- data/sample rationale and untested risks

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/performance-test-engineer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Performance test strategy and workload model.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:1.receiving_acceptance`** — `array`

- For each receiving role (Site Reliability Engineer; Capacity Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:1.delivery_verification`** — `array`

- For the specific output 'Performance test strategy and workload model', provide verifiable evidence satisfying: Identify product/build scope, critical requirements, quality risks, excluded risks and the confidence the selected tests can and cannot provide. Map risks to levels, techniques and responsibilities; specify environment, representative data, dependencies and expected evidence. Define measurable entry/exit criteria, coverage interpretation, triage/retest rules and treatment of blocked or unexecuted cases. Existing source requirement: The model is validated against real observed behaviour or data, not only interviews. Required delivery form: Risk-based test specification with cases/techniques, expected outcomes, environments and entry/exit criteria.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Performance test strategy and workload model") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Results state the environment's ratio to production
- G8: extrapolating from a scaled-down environment without stating the factor is reported as unusable
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:1.contract_input_1`** — `object`

- Analyse the specific input "Non-functional requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:1.contract_input_2`** — `object`

- Analyse the specific input "Production traffic profiles" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:1.contract_input_3`** — `object`

- Analyse the specific input "Environment specification" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:1.contract_input_4`** — `object`

- Analyse the specific input "Business peak forecasts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/performance-test-engineer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/performance-test-engineer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/performance-test-engineer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/performance-test-engineer:1.irrelevant_detail`** — `object`

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
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Performance Test Engineer:** ISO/IEC 25010 performance efficiency; load modelling practice; USE and RED methods. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Use risk-based test or assessment methods with expected/actual results, coverage, sampling and bounded conclusions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-performance-test-engineer-2"></a>

## load and stress test results with bottleneck analysis

**At a glance**

- **Purpose:** Produce and govern the role deliverable: load and stress test results with bottleneck analysis.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `performance-test-engineer:2`.

**Required inputs:**

- Non-functional requirements
- Production traffic profiles
- Environment specification
- Business peak forecasts

**Specification:** `kind/role/performance-test-engineer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: load and stress test results with bottleneck analysis.

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

**`role/performance-test-engineer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: load and stress test results with bottleneck analysis.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:2.receiving_acceptance`** — `array`

- For each receiving role (Site Reliability Engineer; Capacity Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:2.delivery_verification`** — `array`

- For the specific output 'load and stress test results with bottleneck analysis', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Existing source requirement: Identifies assessed scope, method, environment or population, expected and observed outcomes, located findings, untested conditions and residual limitations. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Performance test strategy and workload model") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Results state the environment's ratio to production
- G8: extrapolating from a scaled-down environment without stating the factor is reported as unusable
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:2.contract_input_1`** — `object`

- Analyse the specific input "Non-functional requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:2.contract_input_2`** — `object`

- Analyse the specific input "Production traffic profiles" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:2.contract_input_3`** — `object`

- Analyse the specific input "Environment specification" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:2.contract_input_4`** — `object`

- Analyse the specific input "Business peak forecasts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/performance-test-engineer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/performance-test-engineer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/performance-test-engineer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/performance-test-engineer:2.irrelevant_detail`** — `object`

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
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Performance Test Engineer:** ISO/IEC 25010 performance efficiency; load modelling practice; USE and RED methods. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Use risk-based test or assessment methods with expected/actual results, coverage, sampling and bounded conclusions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-performance-test-engineer-3"></a>

## capacity recommendations

**At a glance**

- **Purpose:** Produce and govern the role deliverable: capacity recommendations.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `performance-test-engineer:3`.

**Required inputs:**

- Non-functional requirements
- Production traffic profiles
- Environment specification
- Business peak forecasts

**Specification:** `kind/role/performance-test-engineer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: capacity recommendations.

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

**`role/performance-test-engineer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: capacity recommendations.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:3.receiving_acceptance`** — `array`

- For each receiving role (Site Reliability Engineer; Capacity Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:3.delivery_verification`** — `array`

- For the specific output 'capacity recommendations', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Performance test strategy and workload model") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Results state the environment's ratio to production
- G8: extrapolating from a scaled-down environment without stating the factor is reported as unusable
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:3.contract_input_1`** — `object`

- Analyse the specific input "Non-functional requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:3.contract_input_2`** — `object`

- Analyse the specific input "Production traffic profiles" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:3.contract_input_3`** — `object`

- Analyse the specific input "Environment specification" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:3.contract_input_4`** — `object`

- Analyse the specific input "Business peak forecasts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/performance-test-engineer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/performance-test-engineer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/performance-test-engineer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/performance-test-engineer:3.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Performance Test Engineer:** ISO/IEC 25010 performance efficiency; load modelling practice; USE and RED methods. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Use risk-based test or assessment methods with expected/actual results, coverage, sampling and bounded conclusions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-performance-test-engineer-4"></a>

## performance regression baselines

**At a glance**

- **Purpose:** Produce and govern the role deliverable: performance regression baselines.
- **Mandatory examples:** Record source versions, extraction time, transformations, lawful access and retention. Evidence completeness, uniqueness, consistency, drift and permitted-use limitations. Define fields, datatypes, units, keys, null handling and allowed values.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `performance-test-engineer:4`.

**Required inputs:**

- Non-functional requirements
- Production traffic profiles
- Environment specification
- Business peak forecasts

**Specification:** `kind/role/performance-test-engineer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: performance regression baselines.

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

**`role/performance-test-engineer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: performance regression baselines.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:4.receiving_acceptance`** — `array`

- For each receiving role (Site Reliability Engineer; Capacity Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:4.delivery_verification`** — `array`

- For the specific output 'performance regression baselines', provide verifiable evidence satisfying: Specify field names, meaning, type, units, code lists, keys, relationships, null semantics and permitted values. Identify source systems/extract versions, transformations, time coverage, access/licensing conditions and accountable custodian. Report completeness, validity, consistency and other relevant quality measures with method, population, results and known limitations. Required delivery form: Typed data or calculation model with units, keys/formulas, lineage and quality constraints.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Performance test strategy and workload model") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Results state the environment's ratio to production
- G8: extrapolating from a scaled-down environment without stating the factor is reported as unusable
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:4.contract_input_1`** — `object`

- Analyse the specific input "Non-functional requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:4.contract_input_2`** — `object`

- Analyse the specific input "Production traffic profiles" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:4.contract_input_3`** — `object`

- Analyse the specific input "Environment specification" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:4.contract_input_4`** — `object`

- Analyse the specific input "Business peak forecasts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/performance-test-engineer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/performance-test-engineer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/performance-test-engineer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/performance-test-engineer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/performance-test-engineer:4.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Performance Test Engineer:** ISO/IEC 25010 performance efficiency; load modelling practice; USE and RED methods. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Use risk-based test or assessment methods with expected/actual results, coverage, sampling and bounded conclusions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
