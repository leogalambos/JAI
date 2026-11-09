<!-- JAI:OUTPUT-CONTRACTS:START -->
# Breach and Attack Simulation Engineer: output contracts

Run continuous, safe simulation of attack paths to validate that controls still work today

[Full catalogue](index.md)

<a id="output-breach-and-attack-simulation-engineer-1"></a>

## Simulation schedule and scenario configuration

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Simulation schedule and scenario configuration.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `breach-and-attack-simulation-engineer:1`.

**Required inputs:**

- Control inventory and expected behaviour
- Authorisation and safe scope
- Threat priorities
- Platform integration points

**Specification:** `kind/role/breach-and-attack-simulation-engineer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Simulation schedule and scenario configuration.

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

**`role/breach-and-attack-simulation-engineer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Simulation schedule and scenario configuration.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:1.receiving_acceptance`** — `array`

- For each receiving role (Security Engineer; Detection Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:1.delivery_verification`** — `array`

- For the specific output 'Simulation schedule and scenario configuration', provide verifiable evidence satisfying: State business outcomes, current/target baseline, planning horizons, sponsors and material planning assumptions. For each increment, identify deliverables, owner, indicative resource/funding requirement, milestone and measurable completion outcome. Identify dependencies and critical sequence, decision dates, constraints and alternative paths; distinguish committed work from tentative options. Required delivery form: Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Simulation schedule and scenario configuration") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Simulations are safe by construction and clearly attributable
- G8: any simulation capable of causing real impact requires the same authorisation as live testing
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:1.contract_input_1`** — `object`

- Analyse the specific input "Control inventory and expected behaviour" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:1.contract_input_2`** — `object`

- Analyse the specific input "Authorisation and safe scope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:1.contract_input_3`** — `object`

- Analyse the specific input "Threat priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:1.contract_input_4`** — `object`

- Analyse the specific input "Platform integration points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/breach-and-attack-simulation-engineer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/breach-and-attack-simulation-engineer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/breach-and-attack-simulation-engineer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/breach-and-attack-simulation-engineer:1.irrelevant_detail`** — `object`

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
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Breach and Attack Simulation Engineer:** MITRE ATT&CK; control validation practice; NIST CSF 2.0 Protect and Detect. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Bind authorised scope and methodology to reproducible observations, impact, evidence limitations and retest results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-breach-and-attack-simulation-engineer-2"></a>

## control efficacy results and trends

**At a glance**

- **Purpose:** Produce and govern the role deliverable: control efficacy results and trends.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `breach-and-attack-simulation-engineer:2`.

**Required inputs:**

- Control inventory and expected behaviour
- Authorisation and safe scope
- Threat priorities
- Platform integration points

**Specification:** `kind/role/breach-and-attack-simulation-engineer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: control efficacy results and trends.

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

**`role/breach-and-attack-simulation-engineer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: control efficacy results and trends.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:2.receiving_acceptance`** — `array`

- For each receiving role (Security Engineer; Detection Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:2.delivery_verification`** — `array`

- For the specific output 'control efficacy results and trends', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Simulation schedule and scenario configuration") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Simulations are safe by construction and clearly attributable
- G8: any simulation capable of causing real impact requires the same authorisation as live testing
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:2.contract_input_1`** — `object`

- Analyse the specific input "Control inventory and expected behaviour" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:2.contract_input_2`** — `object`

- Analyse the specific input "Authorisation and safe scope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:2.contract_input_3`** — `object`

- Analyse the specific input "Threat priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:2.contract_input_4`** — `object`

- Analyse the specific input "Platform integration points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/breach-and-attack-simulation-engineer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/breach-and-attack-simulation-engineer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/breach-and-attack-simulation-engineer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/breach-and-attack-simulation-engineer:2.irrelevant_detail`** — `object`

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
- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Breach and Attack Simulation Engineer:** MITRE ATT&CK; control validation practice; NIST CSF 2.0 Protect and Detect. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Bind authorised scope and methodology to reproducible observations, impact, evidence limitations and retest results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-breach-and-attack-simulation-engineer-3"></a>

## prioritised control gap findings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: prioritised control gap findings.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `breach-and-attack-simulation-engineer:3`.

**Required inputs:**

- Control inventory and expected behaviour
- Authorisation and safe scope
- Threat priorities
- Platform integration points

**Specification:** `kind/role/breach-and-attack-simulation-engineer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: prioritised control gap findings.

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

**`role/breach-and-attack-simulation-engineer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: prioritised control gap findings.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:3.receiving_acceptance`** — `array`

- For each receiving role (Security Engineer; Detection Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:3.delivery_verification`** — `array`

- For the specific output 'prioritised control gap findings', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Existing source requirement: Reproduction steps are complete enough for an independent party to confirm. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Simulation schedule and scenario configuration") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Simulations are safe by construction and clearly attributable
- G8: any simulation capable of causing real impact requires the same authorisation as live testing
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:3.contract_input_1`** — `object`

- Analyse the specific input "Control inventory and expected behaviour" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:3.contract_input_2`** — `object`

- Analyse the specific input "Authorisation and safe scope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:3.contract_input_3`** — `object`

- Analyse the specific input "Threat priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:3.contract_input_4`** — `object`

- Analyse the specific input "Platform integration points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/breach-and-attack-simulation-engineer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/breach-and-attack-simulation-engineer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/breach-and-attack-simulation-engineer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/breach-and-attack-simulation-engineer:3.irrelevant_detail`** — `object`

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
- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Breach and Attack Simulation Engineer:** MITRE ATT&CK; control validation practice; NIST CSF 2.0 Protect and Detect. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Bind authorised scope and methodology to reproducible observations, impact, evidence limitations and retest results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-breach-and-attack-simulation-engineer-4"></a>

## evidence pack for assurance

**At a glance**

- **Purpose:** Produce and govern the role deliverable: evidence pack for assurance.
- **Mandatory examples:** Define tested obligations, assurance period, sample and exclusions. Link procedures and observed results to immutable evidence and located deviations. Limit the independent conclusion to tested scope, evidence strength and unresolved findings.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `breach-and-attack-simulation-engineer:4`.

**Required inputs:**

- Control inventory and expected behaviour
- Authorisation and safe scope
- Threat priorities
- Platform integration points

**Specification:** `kind/role/breach-and-attack-simulation-engineer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: evidence pack for assurance.

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

**`role/breach-and-attack-simulation-engineer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: evidence pack for assurance.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:4.receiving_acceptance`** — `array`

- For each receiving role (Security Engineer; Detection Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:4.delivery_verification`** — `array`

- For the specific output 'evidence pack for assurance', provide verifiable evidence satisfying: State assessment objectives, criteria versions, scope, period, population, sample rationale and exclusions before drawing conclusions. For each criterion, identify procedure, sample, observed result, supporting material and located deviations; distinguish absent evidence from demonstrated failure. Bound the conclusion by coverage and limitations; list findings, severity rationale, management response, remediation owner and verification needed for closure. Existing source requirement: Chain of custody is unbroken and the set is reproducible from the record. Required delivery form: Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Simulation schedule and scenario configuration") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Simulations are safe by construction and clearly attributable
- G8: any simulation capable of causing real impact requires the same authorisation as live testing
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:4.contract_input_1`** — `object`

- Analyse the specific input "Control inventory and expected behaviour" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:4.contract_input_2`** — `object`

- Analyse the specific input "Authorisation and safe scope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:4.contract_input_3`** — `object`

- Analyse the specific input "Threat priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:4.contract_input_4`** — `object`

- Analyse the specific input "Platform integration points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/breach-and-attack-simulation-engineer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/breach-and-attack-simulation-engineer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/breach-and-attack-simulation-engineer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/breach-and-attack-simulation-engineer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/breach-and-attack-simulation-engineer:4.irrelevant_detail`** — `object`

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
- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Breach and Attack Simulation Engineer:** MITRE ATT&CK; control validation practice; NIST CSF 2.0 Protect and Detect. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Bind authorised scope and methodology to reproducible observations, impact, evidence limitations and retest results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
