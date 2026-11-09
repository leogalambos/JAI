<!-- JAI:OUTPUT-CONTRACTS:START -->
# Usability Tester: output contracts

Run structured usability sessions that show whether people can complete real tasks

[Full catalogue](index.md)

<a id="output-usability-tester-1"></a>

## Usability test plans and task scenarios

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Usability test plans and task scenarios.
- **Mandatory examples:** Define test levels, techniques, environments, representative data and responsibilities. Define traceable entry/exit criteria, coverage measurement and defect disposition rules. Define risk-based test objectives, quality targets, scope and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `usability-tester:1`.

**Required inputs:**

- Prototype or build under test
- Task scenarios
- Participant recruitment
- Accessibility requirements

**Specification:** `kind/role/usability-tester:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Usability test plans and task scenarios.

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

**`role/usability-tester:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Usability test plans and task scenarios.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:1.receiving_acceptance`** — `array`

- For each receiving role (UX Designer; Frontend Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:1.delivery_verification`** — `array`

- For the specific output 'Usability test plans and task scenarios', provide verifiable evidence satisfying: Identify product/build scope, critical requirements, quality risks, excluded risks and the confidence the selected tests can and cannot provide. Map risks to levels, techniques and responsibilities; specify environment, representative data, dependencies and expected evidence. Define measurable entry/exit criteria, coverage interpretation, triage/retest rules and treatment of blocked or unexecuted cases. Existing source requirement: Every milestone has an acceptance test and a named accountable owner. Required delivery form: Risk-based test specification with cases/techniques, expected outcomes, environments and entry/exit criteria.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Usability test plans and task scenarios") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Sessions test real tasks with representative participants including users of assistive technology
- G8: testing with colleagues is reported as a walkthrough, not usability testing
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:1.contract_input_1`** — `object`

- Analyse the specific input "Prototype or build under test" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:1.contract_input_2`** — `object`

- Analyse the specific input "Task scenarios" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:1.contract_input_3`** — `object`

- Analyse the specific input "Participant recruitment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:1.contract_input_4`** — `object`

- Analyse the specific input "Accessibility requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/usability-tester:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/usability-tester:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/usability-tester:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/usability-tester:1.irrelevant_detail`** — `object`

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
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Usability Tester:** ISO 9241-11 usability definition; common industry format for usability reporting; WCAG 2.2 AA. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-usability-tester-2"></a>

## session recordings and observation notes

**At a glance**

- **Purpose:** Produce and govern the role deliverable: session recordings and observation notes.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `usability-tester:2`.

**Required inputs:**

- Prototype or build under test
- Task scenarios
- Participant recruitment
- Accessibility requirements

**Specification:** `kind/role/usability-tester:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: session recordings and observation notes.

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

**`role/usability-tester:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: session recordings and observation notes.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:2.receiving_acceptance`** — `array`

- For each receiving role (UX Designer; Frontend Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:2.delivery_verification`** — `array`

- For the specific output 'session recordings and observation notes', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Usability test plans and task scenarios") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Sessions test real tasks with representative participants including users of assistive technology
- G8: testing with colleagues is reported as a walkthrough, not usability testing
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:2.contract_input_1`** — `object`

- Analyse the specific input "Prototype or build under test" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:2.contract_input_2`** — `object`

- Analyse the specific input "Task scenarios" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:2.contract_input_3`** — `object`

- Analyse the specific input "Participant recruitment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:2.contract_input_4`** — `object`

- Analyse the specific input "Accessibility requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/usability-tester:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/usability-tester:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/usability-tester:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/usability-tester:2.irrelevant_detail`** — `object`

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
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Usability Tester:** ISO 9241-11 usability definition; common industry format for usability reporting; WCAG 2.2 AA. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-usability-tester-3"></a>

## severity-rated usability findings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: severity-rated usability findings.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `usability-tester:3`.

**Required inputs:**

- Prototype or build under test
- Task scenarios
- Participant recruitment
- Accessibility requirements

**Specification:** `kind/role/usability-tester:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: severity-rated usability findings.

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

**`role/usability-tester:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: severity-rated usability findings.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:3.receiving_acceptance`** — `array`

- For each receiving role (UX Designer; Frontend Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:3.delivery_verification`** — `array`

- For the specific output 'severity-rated usability findings', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Existing source requirement: Reproduction steps are complete enough for an independent party to confirm. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Usability test plans and task scenarios") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Sessions test real tasks with representative participants including users of assistive technology
- G8: testing with colleagues is reported as a walkthrough, not usability testing
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:3.contract_input_1`** — `object`

- Analyse the specific input "Prototype or build under test" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:3.contract_input_2`** — `object`

- Analyse the specific input "Task scenarios" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:3.contract_input_3`** — `object`

- Analyse the specific input "Participant recruitment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:3.contract_input_4`** — `object`

- Analyse the specific input "Accessibility requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/usability-tester:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/usability-tester:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/usability-tester:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/usability-tester:3.irrelevant_detail`** — `object`

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
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Usability Tester:** ISO 9241-11 usability definition; common industry format for usability reporting; WCAG 2.2 AA. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-usability-tester-4"></a>

## retest results after changes

**At a glance**

- **Purpose:** Produce and govern the role deliverable: retest results after changes.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `usability-tester:4`.

**Required inputs:**

- Prototype or build under test
- Task scenarios
- Participant recruitment
- Accessibility requirements

**Specification:** `kind/role/usability-tester:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: retest results after changes.

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

**`role/usability-tester:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: retest results after changes.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:4.receiving_acceptance`** — `array`

- For each receiving role (UX Designer; Frontend Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:4.delivery_verification`** — `array`

- For the specific output 'retest results after changes', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Existing source requirement: Identifies assessed scope, method, environment or population, expected and observed outcomes, located findings, untested conditions and residual limitations. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Usability test plans and task scenarios") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Sessions test real tasks with representative participants including users of assistive technology
- G8: testing with colleagues is reported as a walkthrough, not usability testing
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:4.contract_input_1`** — `object`

- Analyse the specific input "Prototype or build under test" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:4.contract_input_2`** — `object`

- Analyse the specific input "Task scenarios" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:4.contract_input_3`** — `object`

- Analyse the specific input "Participant recruitment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:4.contract_input_4`** — `object`

- Analyse the specific input "Accessibility requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/usability-tester:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/usability-tester:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/usability-tester:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/usability-tester:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/usability-tester:4.irrelevant_detail`** — `object`

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
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Usability Tester:** ISO 9241-11 usability definition; common industry format for usability reporting; WCAG 2.2 AA. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
