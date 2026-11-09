<!-- JAI:OUTPUT-CONTRACTS:START -->
# Compiler and Toolchain Engineer: output contracts

Build the language tooling other engineers depend on: compilers, analysers, build systems and runtimes

[Full catalogue](index.md)

<a id="output-compiler-and-toolchain-engineer-1"></a>

## Compiler or tool implementation

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Compiler or tool implementation.
- **Mandatory examples:** Trace implemented behaviour and changed interfaces to requirements, design constraints and the exact reviewed source revision. Define deployment compatibility, telemetry, failure detection and rollback or forward recovery constraints. Identify reproducible automated checks, observed results, untested risks and independent review findings without inventing execution.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `compiler-and-toolchain-engineer:1`.

**Required inputs:**

- Language or tool specification
- User pain points
- Benchmark corpus
- Platform targets

**Specification:** `kind/role/compiler-and-toolchain-engineer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Compiler or tool implementation.

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

**`role/compiler-and-toolchain-engineer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Compiler or tool implementation.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:1.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Build Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:1.delivery_verification`** — `array`

- For the specific output 'Compiler or tool implementation', provide verifiable evidence satisfying: Trace implemented behaviour and changed interfaces to requirements, design constraints and the exact reviewed source revision. Identify reproducible automated checks, observed results, untested risks and independent review findings without inventing execution. Define deployment compatibility, telemetry, failure detection and rollback or forward recovery constraints. Required delivery form: Actual version-controlled implementation or analysis code, separate from its explanatory report.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: No change ships without running the full conformance and regression corpus
- G9: miscompilation defects are treated as severity one regardless of rarity
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:1.contract_input_1`** — `object`

- Analyse the specific input "Language or tool specification" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:1.contract_input_2`** — `object`

- Analyse the specific input "User pain points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:1.contract_input_3`** — `object`

- Analyse the specific input "Benchmark corpus" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:1.contract_input_4`** — `object`

- Analyse the specific input "Platform targets" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/compiler-and-toolchain-engineer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/compiler-and-toolchain-engineer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/compiler-and-toolchain-engineer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/compiler-and-toolchain-engineer:1.irrelevant_detail`** — `object`

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

- **Compiler and Toolchain Engineer:** language standards; compiler testing practice; semantic versioning. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace required behaviour and security constraints to exact source changes, reproducible checks and independently reviewed results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-compiler-and-toolchain-engineer-2"></a>

## correctness test suite and conformance evidence

**At a glance**

- **Purpose:** Produce and govern the role deliverable: correctness test suite and conformance evidence.
- **Mandatory examples:** Give reproducible invocation, assertions, expected outcomes and failure diagnostics; distinguish test definitions from evidence of executed runs. Define isolation, dependency handling, flakiness investigation, coverage limitations and maintenance ownership. Trace executable cases and reusable test abstractions to requirements, risk coverage, deterministic data and environment assumptions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `compiler-and-toolchain-engineer:2`.

**Required inputs:**

- Language or tool specification
- User pain points
- Benchmark corpus
- Platform targets

**Specification:** `kind/role/compiler-and-toolchain-engineer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: correctness test suite and conformance evidence.

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

**`role/compiler-and-toolchain-engineer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: correctness test suite and conformance evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:2.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Build Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:2.delivery_verification`** — `array`

- For the specific output 'correctness test suite and conformance evidence', provide verifiable evidence satisfying: Trace executable cases and reusable test abstractions to requirements, risk coverage, deterministic data and environment assumptions. Give reproducible invocation, assertions, expected outcomes and failure diagnostics; distinguish test definitions from evidence of executed runs. Define isolation, dependency handling, flakiness investigation, coverage limitations and maintenance ownership. Existing source requirement: States what is covered, what is not, and what the suite cannot detect. Required delivery form: Executable automated checks with deterministic setup, expected assertions and reproducible invocation.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: No change ships without running the full conformance and regression corpus
- G9: miscompilation defects are treated as severity one regardless of rarity
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:2.contract_input_1`** — `object`

- Analyse the specific input "Language or tool specification" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:2.contract_input_2`** — `object`

- Analyse the specific input "User pain points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:2.contract_input_3`** — `object`

- Analyse the specific input "Benchmark corpus" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:2.contract_input_4`** — `object`

- Analyse the specific input "Platform targets" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/compiler-and-toolchain-engineer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/compiler-and-toolchain-engineer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/compiler-and-toolchain-engineer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/compiler-and-toolchain-engineer:2.irrelevant_detail`** — `object`

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

### Role framework context

- **Compiler and Toolchain Engineer:** language standards; compiler testing practice; semantic versioning. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace required behaviour and security constraints to exact source changes, reproducible checks and independently reviewed results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-compiler-and-toolchain-engineer-3"></a>

## performance benchmarks

**At a glance**

- **Purpose:** Produce and govern the role deliverable: performance benchmarks.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `compiler-and-toolchain-engineer:3`.

**Required inputs:**

- Language or tool specification
- User pain points
- Benchmark corpus
- Platform targets

**Specification:** `kind/role/compiler-and-toolchain-engineer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: performance benchmarks.

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

**`role/compiler-and-toolchain-engineer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: performance benchmarks.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:3.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Build Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:3.delivery_verification`** — `array`

- For the specific output 'performance benchmarks', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: No change ships without running the full conformance and regression corpus
- G9: miscompilation defects are treated as severity one regardless of rarity
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:3.contract_input_1`** — `object`

- Analyse the specific input "Language or tool specification" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:3.contract_input_2`** — `object`

- Analyse the specific input "User pain points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:3.contract_input_3`** — `object`

- Analyse the specific input "Benchmark corpus" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:3.contract_input_4`** — `object`

- Analyse the specific input "Platform targets" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/compiler-and-toolchain-engineer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/compiler-and-toolchain-engineer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/compiler-and-toolchain-engineer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/compiler-and-toolchain-engineer:3.irrelevant_detail`** — `object`

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

### Role framework context

- **Compiler and Toolchain Engineer:** language standards; compiler testing practice; semantic versioning. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace required behaviour and security constraints to exact source changes, reproducible checks and independently reviewed results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-compiler-and-toolchain-engineer-4"></a>

## migration guidance for users

**At a glance**

- **Purpose:** Produce and govern the role deliverable: migration guidance for users.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `compiler-and-toolchain-engineer:4`.

**Required inputs:**

- Language or tool specification
- User pain points
- Benchmark corpus
- Platform targets

**Specification:** `kind/role/compiler-and-toolchain-engineer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: migration guidance for users.

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

**`role/compiler-and-toolchain-engineer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: migration guidance for users.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:4.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Build Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:4.delivery_verification`** — `array`

- For the specific output 'migration guidance for users', provide verifiable evidence satisfying: State the exact subject, intended recipient/use, boundary, source versions and the concrete question the document answers. Provide subject-specific findings or instructions with supporting facts, assumptions, reasoning, limitations and traceable references; generic background alone is insufficient. State conclusions, decisions requested or actionable instructions, accountable recipients and completion/acceptance conditions; identify open issues explicitly. Required delivery form: Purpose-specific professional document with source analysis, reasoning, conclusions and recipient actions.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: No change ships without running the full conformance and regression corpus
- G9: miscompilation defects are treated as severity one regardless of rarity
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:4.contract_input_1`** — `object`

- Analyse the specific input "Language or tool specification" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:4.contract_input_2`** — `object`

- Analyse the specific input "User pain points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:4.contract_input_3`** — `object`

- Analyse the specific input "Benchmark corpus" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:4.contract_input_4`** — `object`

- Analyse the specific input "Platform targets" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/compiler-and-toolchain-engineer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/compiler-and-toolchain-engineer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/compiler-and-toolchain-engineer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/compiler-and-toolchain-engineer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/compiler-and-toolchain-engineer:4.irrelevant_detail`** — `object`

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

- **Compiler and Toolchain Engineer:** language standards; compiler testing practice; semantic versioning. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace required behaviour and security constraints to exact source changes, reproducible checks and independently reviewed results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
