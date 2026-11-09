<!-- JAI:OUTPUT-CONTRACTS:START -->
# API Developer: output contracts

Build and maintain interfaces other teams depend on, with contracts that do not break them

[Full catalogue](index.md)

<a id="output-api-developer-1"></a>

## API implementation

**At a glance**

- **Purpose:** Produce and govern the role deliverable: API implementation.
- **Mandatory examples:** Trace implemented behaviour and changed interfaces to requirements, design constraints and the exact reviewed source revision. Define deployment compatibility, telemetry, failure detection and rollback or forward recovery constraints. Identify reproducible automated checks, observed results, untested risks and independent review findings without inventing execution.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `api-developer:1`.

**Required inputs:**

- Interface requirements and consumer list
- Integration patterns
- Security requirements
- Expected volumes

**Specification:** `kind/role/api-developer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: API implementation.

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

**`role/api-developer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: API implementation.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:1.receiving_acceptance`** — `array`

- For each receiving role (Integration Developer; consumer teams), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:1.delivery_verification`** — `array`

- For the specific output 'API implementation', provide verifiable evidence satisfying: Trace implemented behaviour and changed interfaces to requirements, design constraints and the exact reviewed source revision. Identify reproducible automated checks, observed results, untested risks and independent review findings without inventing execution. Define deployment compatibility, telemetry, failure detection and rollback or forward recovery constraints. Required delivery form: Actual version-controlled implementation or analysis code, separate from its explanatory report.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: The specification is the source of truth and is published before implementation
- G9: contract tests run against it in the pipeline
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:1.contract_input_1`** — `object`

- Analyse the specific input "Interface requirements and consumer list" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:1.contract_input_2`** — `object`

- Analyse the specific input "Integration patterns" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:1.contract_input_3`** — `object`

- Analyse the specific input "Security requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:1.contract_input_4`** — `object`

- Analyse the specific input "Expected volumes" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/api-developer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/api-developer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/api-developer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/api-developer:1.irrelevant_detail`** — `object`

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

- **API Developer:** OpenAPI; AsyncAPI; OWASP API Security Top 10; semantic versioning. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace required behaviour and security constraints to exact source changes, reproducible checks and independently reviewed results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-api-developer-2"></a>

## OpenAPI or AsyncAPI specification

**At a glance**

- **Purpose:** Produce and govern the role deliverable: OpenAPI or AsyncAPI specification.
- **Mandatory examples:** Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `api-developer:2`.

**Required inputs:**

- Interface requirements and consumer list
- Integration patterns
- Security requirements
- Expected volumes

**Specification:** `kind/role/api-developer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: OpenAPI or AsyncAPI specification.

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

**`role/api-developer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: OpenAPI or AsyncAPI specification.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:2.receiving_acceptance`** — `array`

- For each receiving role (Integration Developer; consumer teams), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:2.delivery_verification`** — `array`

- For the specific output 'OpenAPI or AsyncAPI specification', provide verifiable evidence satisfying: Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. Existing source requirement: Every requirement is atomic, testable and traced to a source and a priority. Required delivery form: Uniquely identified verifiable requirements with rationale, priority, sources and acceptance conditions.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: The specification is the source of truth and is published before implementation
- G9: contract tests run against it in the pipeline
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:2.contract_input_1`** — `object`

- Analyse the specific input "Interface requirements and consumer list" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:2.contract_input_2`** — `object`

- Analyse the specific input "Integration patterns" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:2.contract_input_3`** — `object`

- Analyse the specific input "Security requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:2.contract_input_4`** — `object`

- Analyse the specific input "Expected volumes" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/api-developer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/api-developer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/api-developer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/api-developer:2.irrelevant_detail`** — `object`

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
- **[NIST SP 800-218, Secure Software Development Framework Version 1.1](https://doi.org/10.6028/NIST.SP.800-218)** — Secure development practices, protected source/build inputs, verification and vulnerability response. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **API Developer:** OpenAPI; AsyncAPI; OWASP API Security Top 10; semantic versioning. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace required behaviour and security constraints to exact source changes, reproducible checks and independently reviewed results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-api-developer-3"></a>

## consumer-facing documentation and examples

**At a glance**

- **Purpose:** Produce and govern the role deliverable: consumer-facing documentation and examples.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `api-developer:3`.

**Required inputs:**

- Interface requirements and consumer list
- Integration patterns
- Security requirements
- Expected volumes

**Specification:** `kind/role/api-developer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: consumer-facing documentation and examples.

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

**`role/api-developer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: consumer-facing documentation and examples.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:3.receiving_acceptance`** — `array`

- For each receiving role (Integration Developer; consumer teams), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:3.delivery_verification`** — `array`

- For the specific output 'consumer-facing documentation and examples', provide verifiable evidence satisfying: State the exact subject, intended recipient/use, boundary, source versions and the concrete question the document answers. Provide subject-specific findings or instructions with supporting facts, assumptions, reasoning, limitations and traceable references; generic background alone is insufficient. State conclusions, decisions requested or actionable instructions, accountable recipients and completion/acceptance conditions; identify open issues explicitly. Required delivery form: Purpose-specific professional document with source analysis, reasoning, conclusions and recipient actions.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: The specification is the source of truth and is published before implementation
- G9: contract tests run against it in the pipeline
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:3.contract_input_1`** — `object`

- Analyse the specific input "Interface requirements and consumer list" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:3.contract_input_2`** — `object`

- Analyse the specific input "Integration patterns" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:3.contract_input_3`** — `object`

- Analyse the specific input "Security requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:3.contract_input_4`** — `object`

- Analyse the specific input "Expected volumes" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/api-developer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/api-developer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/api-developer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/api-developer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/api-developer:3.irrelevant_detail`** — `object`

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

- **API Developer:** OpenAPI; AsyncAPI; OWASP API Security Top 10; semantic versioning. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace required behaviour and security constraints to exact source changes, reproducible checks and independently reviewed results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-api-developer-4"></a>

## contract tests

**At a glance**

- **Purpose:** Produce and govern the role deliverable: contract tests.
- **Mandatory examples:** Give reproducible invocation, assertions, expected outcomes and failure diagnostics; distinguish test definitions from evidence of executed runs. Define isolation, dependency handling, flakiness investigation, coverage limitations and maintenance ownership. Trace executable cases and reusable test abstractions to requirements, risk coverage, deterministic data and environment assumptions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `api-developer:4`.

**Required inputs:**

- Interface requirements and consumer list
- Integration patterns
- Security requirements
- Expected volumes

**Specification:** `kind/role/api-developer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: contract tests.

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

**`role/api-developer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: contract tests.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/api-developer:4.receiving_acceptance`** — `array`

- For each receiving role (Integration Developer; consumer teams), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/api-developer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/api-developer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/api-developer:4.delivery_verification`** — `array`

- For the specific output 'contract tests', provide verifiable evidence satisfying: Trace executable cases and reusable test abstractions to requirements, risk coverage, deterministic data and environment assumptions. Give reproducible invocation, assertions, expected outcomes and failure diagnostics; distinguish test definitions from evidence of executed runs. Define isolation, dependency handling, flakiness investigation, coverage limitations and maintenance ownership. Existing source requirement: States what is covered, what is not, and what the suite cannot detect. Required delivery form: Executable automated checks with deterministic setup, expected assertions and reproducible invocation.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/api-developer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: The specification is the source of truth and is published before implementation
- G9: contract tests run against it in the pipeline
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/api-developer:4.contract_input_1`** — `object`

- Analyse the specific input "Interface requirements and consumer list" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/api-developer:4.contract_input_2`** — `object`

- Analyse the specific input "Integration patterns" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/api-developer:4.contract_input_3`** — `object`

- Analyse the specific input "Security requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/api-developer:4.contract_input_4`** — `object`

- Analyse the specific input "Expected volumes" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/api-developer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/api-developer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/api-developer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/api-developer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/api-developer:4.irrelevant_detail`** — `object`

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

- **API Developer:** OpenAPI; AsyncAPI; OWASP API Security Top 10; semantic versioning. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace required behaviour and security constraints to exact source changes, reproducible checks and independently reviewed results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
