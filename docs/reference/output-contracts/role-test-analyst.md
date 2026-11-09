<!-- JAI:OUTPUT-CONTRACTS:START -->
# Test Analyst: output contracts

Design and run tests that find the defects that matter before customers do

[Full catalogue](index.md)

<a id="output-test-analyst-1"></a>

## Test conditions and cases

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Test conditions and cases.
- **Mandatory examples:** Define test levels, techniques, environments, representative data and responsibilities. Define traceable entry/exit criteria, coverage measurement and defect disposition rules. Define risk-based test objectives, quality targets, scope and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `test-analyst:1`.

**Required inputs:**

- Requirements and acceptance criteria
- Risk assessment
- Test environment and data
- Build under test

**Specification:** `kind/role/test-analyst:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Test conditions and cases.

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

**`role/test-analyst:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Test conditions and cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:1.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Release Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:1.delivery_verification`** — `array`

- For the specific output 'Test conditions and cases', provide verifiable evidence satisfying: Identify product/build scope, critical requirements, quality risks, excluded risks and the confidence the selected tests can and cannot provide. Map risks to levels, techniques and responsibilities; specify environment, representative data, dependencies and expected evidence. Define measurable entry/exit criteria, coverage interpretation, triage/retest rules and treatment of blocked or unexecuted cases. Existing source requirement: Each case identifies requirement or risk, preconditions, data, actions, expected observations and execution method; manual cases need not be automated. Required delivery form: Risk-based test specification with cases/techniques, expected outcomes, environments and entry/exit criteria.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Test conditions and cases") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Every defect report contains reproduction steps, environment, build version and observed-versus-expected behaviour
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:1.contract_input_1`** — `object`

- Analyse the specific input "Requirements and acceptance criteria" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:1.contract_input_2`** — `object`

- Analyse the specific input "Risk assessment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:1.contract_input_3`** — `object`

- Analyse the specific input "Test environment and data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:1.contract_input_4`** — `object`

- Analyse the specific input "Build under test" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/test-analyst:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/test-analyst:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/test-analyst:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/test-analyst:1.irrelevant_detail`** — `object`

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

- **Test Analyst:** ISTQB; ISO/IEC/IEEE 29119; risk-based testing practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Use risk-based test or assessment methods with expected/actual results, coverage, sampling and bounded conclusions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-test-analyst-2"></a>

## executed test evidence

**At a glance**

- **Purpose:** Determine whether tested requirements satisfy exit criteria and residual defects permit progression.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include deeper calculations or technical detail only when linked to a reader need.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `test-analyst:2`.

**Required inputs:**

- Requirements and acceptance criteria
- Risk assessment
- Test environment and data
- Build under test

**Specification:** `kind/test-report`; **content version:** `1.2.0`.

Determine whether tested requirements satisfy exit criteria and residual defects permit progression.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/test-report`](spec-type-test-report.md)

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

**`test-report.test_scope`** — `object`

- Identify tested requirements, exclusions, build versions and the reporting period.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`test-report.test_environment`** — `object`

- Record environment, data constraints, tools and reproducible execution configuration.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`test-report.execution_results`** — `array`

- Link test cases and requirement IDs to execution timestamps, actual outcomes and evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`test-report.defect_analysis`** — `array`

- Record unresolved defects, severity, retest state and their impact on acceptance.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`test-report.test_conclusion`** — `object`

- Compare achieved coverage with exit criteria and explain limitations and residual release risk.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`test-report.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify personal-data flows, lawful handling constraints, minimisation and review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`test-report.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Trace each applicable regulatory obligation to scope, evidence and competent interpretation; exceptions cannot waive law.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`test-report.technical_annex`** — `object`

- Include deeper calculations or technical detail only when linked to a reader need.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`test-report.unsupported_material_claim`** — `object`

- Never state a material conclusion as established without evidence or explicit uncertainty.

### Content to omit unless justified

**`test-report.irrelevant_detail`** — `object`

- Remove detail that does not support the stated purpose or a referenced annex.

**`test-report.duplicate_claim`** — `object`

- Reference an existing claim instead of repeating it without new analytical value.

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
  "pages": {
    "metric": "pages",
    "calibration_basis": "Modality-specific information coverage; numerical envelopes require approved enterprise calibration.",
    "minimum_is_quality_gate": false,
    "calibration_status": "synthetic-only",
    "allowance_rules": [
      "Document complexity and audience need; excess requires review, not automatic rejection."
    ],
    "annex_rules": [
      "Reference canonical detail rather than repeat it."
    ],
    "target": [
      3,
      10
    ],
    "soft_max": 14,
    "basis": "Indicative pilot intervals from approved implementation direction; assurance and handover use proposed evidence-pack intervals requiring calibration.",
    "exclude": [
      "controlled_annexes",
      "source_register"
    ],
    "target_is_informational": true
  }
}
```

### Professional sources and their limits

- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Test Analyst:** ISTQB; ISO/IEC/IEEE 29119; risk-based testing practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Use risk-based test or assessment methods with expected/actual results, coverage, sampling and bounded conclusions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-test-analyst-3"></a>

## defect reports with business impact

**At a glance**

- **Purpose:** Produce and govern the role deliverable: defect reports with business impact.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `test-analyst:3`.

**Required inputs:**

- Requirements and acceptance criteria
- Risk assessment
- Test environment and data
- Build under test

**Specification:** `kind/role/test-analyst:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: defect reports with business impact.

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

**`role/test-analyst:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: defect reports with business impact.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:3.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Release Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:3.delivery_verification`** — `array`

- For the specific output 'defect reports with business impact', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Existing source requirement: Conclusions are traceable to dated evidence; opinion is visibly separated from fact. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Test conditions and cases") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Every defect report contains reproduction steps, environment, build version and observed-versus-expected behaviour
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:3.contract_input_1`** — `object`

- Analyse the specific input "Requirements and acceptance criteria" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:3.contract_input_2`** — `object`

- Analyse the specific input "Risk assessment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:3.contract_input_3`** — `object`

- Analyse the specific input "Test environment and data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:3.contract_input_4`** — `object`

- Analyse the specific input "Build under test" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:3.reproducible_defect_records`** — `array`

- Record each defect ID, exact build/environment/locale, requirement or expected behaviour, reproduction inputs and steps, actual observation/evidence, business impact, severity rationale, accountable owner and fix/retest status. A defect report is not an investment or architecture option appraisal.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/test-analyst:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/test-analyst:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/test-analyst:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/test-analyst:3.irrelevant_detail`** — `object`

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

- **Test Analyst:** ISTQB; ISO/IEC/IEEE 29119; risk-based testing practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Use risk-based test or assessment methods with expected/actual results, coverage, sampling and bounded conclusions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-test-analyst-4"></a>

## test completion summary

**At a glance**

- **Purpose:** Produce and govern the role deliverable: test completion summary.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `test-analyst:4`.

**Required inputs:**

- Requirements and acceptance criteria
- Risk assessment
- Test environment and data
- Build under test

**Specification:** `kind/role/test-analyst:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: test completion summary.

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

**`role/test-analyst:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: test completion summary.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:4.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Release Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:4.delivery_verification`** — `array`

- For the specific output 'test completion summary', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Existing source requirement: Identifies assessed scope, method, environment or population, expected and observed outcomes, located findings, untested conditions and residual limitations. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Test conditions and cases") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Every defect report contains reproduction steps, environment, build version and observed-versus-expected behaviour
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:4.contract_input_1`** — `object`

- Analyse the specific input "Requirements and acceptance criteria" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:4.contract_input_2`** — `object`

- Analyse the specific input "Risk assessment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:4.contract_input_3`** — `object`

- Analyse the specific input "Test environment and data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:4.contract_input_4`** — `object`

- Analyse the specific input "Build under test" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/test-analyst:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-analyst:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/test-analyst:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/test-analyst:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/test-analyst:4.irrelevant_detail`** — `object`

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

- **Test Analyst:** ISTQB; ISO/IEC/IEEE 29119; risk-based testing practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Use risk-based test or assessment methods with expected/actual results, coverage, sampling and bounded conclusions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
