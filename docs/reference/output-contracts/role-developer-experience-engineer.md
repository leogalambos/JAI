<!-- JAI:OUTPUT-CONTRACTS:START -->
# Developer Experience Engineer: output contracts

Reduce the friction between an engineer having an idea and that idea running in production

[Full catalogue](index.md)

<a id="output-developer-experience-engineer-1"></a>

## Golden path tooling and templates

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Golden path tooling and templates.
- **Mandatory examples:** Trace implemented behaviour and changed interfaces to requirements, design constraints and the exact reviewed source revision. Define deployment compatibility, telemetry, failure detection and rollback or forward recovery constraints. Identify reproducible automated checks, observed results, untested risks and independent review findings without inventing execution.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `developer-experience-engineer:1`.

**Required inputs:**

- Cycle time and flow metrics
- Developer survey and interview findings
- Platform capabilities
- Security requirements

**Specification:** `kind/role/developer-experience-engineer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Golden path tooling and templates.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/software-change`](spec-family-software-change.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `versioned-source-change`.

Actual version-controlled implementation or analysis code, separate from its explanatory report.

**Evidence accompanying the work product:**

- exact source and dependency revision
- observed checks and independent review

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/developer-experience-engineer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Golden path tooling and templates.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:1.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Build Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:1.delivery_verification`** — `array`

- For the specific output 'Golden path tooling and templates', provide verifiable evidence satisfying: Trace implemented behaviour and changed interfaces to requirements, design constraints and the exact reviewed source revision. Identify reproducible automated checks, observed results, untested risks and independent review findings without inventing execution. Define deployment compatibility, telemetry, failure detection and rollback or forward recovery constraints. Required delivery form: Actual version-controlled implementation or analysis code, separate from its explanatory report.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Every improvement is validated against a measured baseline of developer time or error rate
- G9: tooling adoption is voluntary and measured
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:1.contract_input_1`** — `object`

- Analyse the specific input "Cycle time and flow metrics" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:1.contract_input_2`** — `object`

- Analyse the specific input "Developer survey and interview findings" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:1.contract_input_3`** — `object`

- Analyse the specific input "Platform capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:1.contract_input_4`** — `object`

- Analyse the specific input "Security requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/developer-experience-engineer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/developer-experience-engineer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/developer-experience-engineer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/developer-experience-engineer:1.irrelevant_detail`** — `object`

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

- **[NIST SP 800-218, Secure Software Development Framework Version 1.1](https://doi.org/10.6028/NIST.SP.800-218)** — Secure development practices, protected source/build inputs, verification and vulnerability response. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Developer Experience Engineer:** DORA and SPACE metrics; Team Topologies; internal developer platform practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace required behaviour and security constraints to exact source changes, reproducible checks and independently reviewed results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-developer-experience-engineer-2"></a>

## developer friction measurement

**At a glance**

- **Purpose:** Produce and govern the role deliverable: developer friction measurement.
- **Mandatory examples:** Explain thresholds, uncertainty, missing data and actions supported by the view. Define metrics, units, denominators, targets, refresh cadence and accountable owners. Provide dated observations linked to versioned source queries and population scope.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `developer-experience-engineer:2`.

**Required inputs:**

- Cycle time and flow metrics
- Developer survey and interview findings
- Platform capabilities
- Security requirements

**Specification:** `kind/role/developer-experience-engineer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: developer friction measurement.

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

**`role/developer-experience-engineer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: developer friction measurement.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:2.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Build Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:2.delivery_verification`** — `array`

- For the specific output 'developer friction measurement', provide verifiable evidence satisfying: For each metric, define question, formula, unit, population/denominator, time window, target/threshold and accountable owner. Show observation timestamp, source/query version, aggregation, missing-data handling and measurement limitations. Explain threshold crossings and trends, uncertainty and the action or decision supported; distinguish operational signals from causal explanations. Required delivery form: Dashboard or scorecard with metric definitions, observations, source queries and interpretation.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Every improvement is validated against a measured baseline of developer time or error rate
- G9: tooling adoption is voluntary and measured
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:2.contract_input_1`** — `object`

- Analyse the specific input "Cycle time and flow metrics" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:2.contract_input_2`** — `object`

- Analyse the specific input "Developer survey and interview findings" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:2.contract_input_3`** — `object`

- Analyse the specific input "Platform capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:2.contract_input_4`** — `object`

- Analyse the specific input "Security requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/developer-experience-engineer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/developer-experience-engineer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/developer-experience-engineer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/developer-experience-engineer:2.irrelevant_detail`** — `object`

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
- **[NIST SP 800-218, Secure Software Development Framework Version 1.1](https://doi.org/10.6028/NIST.SP.800-218)** — Secure development practices, protected source/build inputs, verification and vulnerability response. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Developer Experience Engineer:** DORA and SPACE metrics; Team Topologies; internal developer platform practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace required behaviour and security constraints to exact source changes, reproducible checks and independently reviewed results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-developer-experience-engineer-3"></a>

## local development environment

**At a glance**

- **Purpose:** Produce and govern the role deliverable: local development environment.
- **Mandatory examples:** Identify managed assets, tool/schema versions and authorised configuration scope. Provide typed desired settings, permitted ranges and secret-manager references. Evidence reproducibility, drift checks, deployment validation and rollback to a known baseline.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `developer-experience-engineer:3`.

**Required inputs:**

- Cycle time and flow metrics
- Developer survey and interview findings
- Platform capabilities
- Security requirements

**Specification:** `kind/role/developer-experience-engineer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: local development environment.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/configuration-baseline`](spec-type-configuration-baseline.md)
- [`domain/operations`](spec-domain-operations.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `versioned-configuration`.

Typed desired-state configuration with exact targets, versioned values and controlled secret references.

**Evidence accompanying the work product:**

- reproduction/drift observations
- verification and recovery to a known baseline

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/developer-experience-engineer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: local development environment.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:3.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Build Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:3.delivery_verification`** — `array`

- For the specific output 'local development environment', provide verifiable evidence satisfying: Identify managed components, exact versions, environments, approved parameter values, exceptions and configuration owner without exposing secrets. Describe how the baseline is created/applied, validated and changed, including dependencies and recovery from an unsuccessful change. Compare observed configuration with the declared baseline, classify drift, identify material impact and record authorised remediation or unresolved exceptions. Required delivery form: Typed desired-state configuration with exact targets, versioned values and controlled secret references.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Every improvement is validated against a measured baseline of developer time or error rate
- G9: tooling adoption is voluntary and measured
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:3.contract_input_1`** — `object`

- Analyse the specific input "Cycle time and flow metrics" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:3.contract_input_2`** — `object`

- Analyse the specific input "Developer survey and interview findings" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:3.contract_input_3`** — `object`

- Analyse the specific input "Platform capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:3.contract_input_4`** — `object`

- Analyse the specific input "Security requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/developer-experience-engineer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/developer-experience-engineer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/developer-experience-engineer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/developer-experience-engineer:3.irrelevant_detail`** — `object`

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

- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-218, Secure Software Development Framework Version 1.1](https://doi.org/10.6028/NIST.SP.800-218)** — Secure development practices, protected source/build inputs, verification and vulnerability response. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Developer Experience Engineer:** DORA and SPACE metrics; Team Topologies; internal developer platform practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace required behaviour and security constraints to exact source changes, reproducible checks and independently reviewed results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-developer-experience-engineer-4"></a>

## internal tooling documentation

**At a glance**

- **Purpose:** Produce and govern the role deliverable: internal tooling documentation.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `developer-experience-engineer:4`.

**Required inputs:**

- Cycle time and flow metrics
- Developer survey and interview findings
- Platform capabilities
- Security requirements

**Specification:** `kind/role/developer-experience-engineer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: internal tooling documentation.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `professional-document`.

Purpose-specific professional document with source analysis, reasoning, conclusions and recipient actions.

**Evidence accompanying the work product:**

- attributable subject-specific findings and limitations
- reviewable sources and verifiable follow-up actions

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/developer-experience-engineer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: internal tooling documentation.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:4.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Build Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:4.delivery_verification`** — `array`

- For the specific output 'internal tooling documentation', provide verifiable evidence satisfying: State the exact subject, intended recipient/use, boundary, source versions and the concrete question the document answers. Provide subject-specific findings or instructions with supporting facts, assumptions, reasoning, limitations and traceable references; generic background alone is insufficient. State conclusions, decisions requested or actionable instructions, accountable recipients and completion/acceptance conditions; identify open issues explicitly. Required delivery form: Purpose-specific professional document with source analysis, reasoning, conclusions and recipient actions.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Every improvement is validated against a measured baseline of developer time or error rate
- G9: tooling adoption is voluntary and measured
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:4.contract_input_1`** — `object`

- Analyse the specific input "Cycle time and flow metrics" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:4.contract_input_2`** — `object`

- Analyse the specific input "Developer survey and interview findings" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:4.contract_input_3`** — `object`

- Analyse the specific input "Platform capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:4.contract_input_4`** — `object`

- Analyse the specific input "Security requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/developer-experience-engineer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/developer-experience-engineer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/developer-experience-engineer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/developer-experience-engineer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/developer-experience-engineer:4.irrelevant_detail`** — `object`

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
- **[NIST SP 800-218, Secure Software Development Framework Version 1.1](https://doi.org/10.6028/NIST.SP.800-218)** — Secure development practices, protected source/build inputs, verification and vulnerability response. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Developer Experience Engineer:** DORA and SPACE metrics; Team Topologies; internal developer platform practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace required behaviour and security constraints to exact source changes, reproducible checks and independently reviewed results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
