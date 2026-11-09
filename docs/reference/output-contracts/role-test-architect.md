<!-- JAI:OUTPUT-CONTRACTS:START -->
# Test Architect: output contracts

Design the overall approach to quality across systems, environments, data and tooling

[Full catalogue](index.md)

<a id="output-test-architect-1"></a>

## Enterprise test architecture

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Enterprise test architecture.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `test-architect:1`.

**Required inputs:**

- System landscape
- Delivery model and cadence
- Data protection constraints
- Current tooling estate

**Specification:** `kind/role/test-architect:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Enterprise test architecture.

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

**`role/test-architect:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Enterprise test architecture.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:1.receiving_acceptance`** — `array`

- For each receiving role (Test Manager; Test Automation Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:1.delivery_verification`** — `array`

- For the specific output 'Enterprise test architecture', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Existing source requirement: Every element traces to a driver or a quality-attribute target; no orphan elements. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: The strategy defines how production-like data is obtained lawfully
- G6: any approach relying on unmasked production personal data is rejected
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:1.contract_input_1`** — `object`

- Analyse the specific input "System landscape" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:1.contract_input_2`** — `object`

- Analyse the specific input "Delivery model and cadence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:1.contract_input_3`** — `object`

- Analyse the specific input "Data protection constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:1.contract_input_4`** — `object`

- Analyse the specific input "Current tooling estate" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/test-architect:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/test-architect:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/test-architect:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/test-architect:1.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Test Architect:** ISO/IEC/IEEE 29119; test pyramid and contract testing practice; data masking standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Use risk-based test or assessment methods with expected/actual results, coverage, sampling and bounded conclusions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-test-architect-2"></a>

## environment and test data strategy

**At a glance**

- **Purpose:** Produce and govern the role deliverable: environment and test data strategy.
- **Mandatory examples:** Define test levels, techniques, environments, representative data and responsibilities. Define traceable entry/exit criteria, coverage measurement and defect disposition rules. Define risk-based test objectives, quality targets, scope and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `test-architect:2`.

**Required inputs:**

- System landscape
- Delivery model and cadence
- Data protection constraints
- Current tooling estate

**Specification:** `kind/role/test-architect:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: environment and test data strategy.

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

**`role/test-architect:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: environment and test data strategy.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:2.receiving_acceptance`** — `array`

- For each receiving role (Test Manager; Test Automation Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:2.delivery_verification`** — `array`

- For the specific output 'environment and test data strategy', provide verifiable evidence satisfying: Identify product/build scope, critical requirements, quality risks, excluded risks and the confidence the selected tests can and cannot provide. Map risks to levels, techniques and responsibilities; specify environment, representative data, dependencies and expected evidence. Define measurable entry/exit criteria, coverage interpretation, triage/retest rules and treatment of blocked or unexecuted cases. Existing source requirement: Defines representative environments/data, lawful use, provisioning, isolation, dependencies and capability gaps. Required delivery form: Risk-based test specification with cases/techniques, expected outcomes, environments and entry/exit criteria.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: The strategy defines how production-like data is obtained lawfully
- G6: any approach relying on unmasked production personal data is rejected
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:2.contract_input_1`** — `object`

- Analyse the specific input "System landscape" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:2.contract_input_2`** — `object`

- Analyse the specific input "Delivery model and cadence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:2.contract_input_3`** — `object`

- Analyse the specific input "Data protection constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:2.contract_input_4`** — `object`

- Analyse the specific input "Current tooling estate" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/test-architect:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/test-architect:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/test-architect:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/test-architect:2.irrelevant_detail`** — `object`

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

- **Test Architect:** ISO/IEC/IEEE 29119; test pyramid and contract testing practice; data masking standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Use risk-based test or assessment methods with expected/actual results, coverage, sampling and bounded conclusions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-test-architect-3"></a>

## tooling standards and integration design

**At a glance**

- **Purpose:** Produce and govern the role deliverable: tooling standards and integration design.
- **Mandatory examples:** Describe bounded component responsibilities and deployment topology. Map measurable quality requirements to design verification and acceptance. Define versioned interface inputs, outputs, trust boundaries and failure handling.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `test-architect:3`.

**Required inputs:**

- System landscape
- Delivery model and cadence
- Data protection constraints
- Current tooling estate

**Specification:** `kind/role/test-architect:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: tooling standards and integration design.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/solution-design`](spec-type-solution-design.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `solution-design`.

Versioned solution design with component responsibilities, interfaces and measurable quality responses.

**Evidence accompanying the work product:**

- requirements-to-design traceability
- independent design review

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/test-architect:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: tooling standards and integration design.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:3.receiving_acceptance`** — `array`

- For each receiving role (Test Manager; Test Automation Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:3.delivery_verification`** — `array`

- For the specific output 'tooling standards and integration design', provide verifiable evidence satisfying: Define the proposed implementation boundary, use cases and external dependencies. State measurable availability, performance, security and operational acceptance targets. Describe component responsibilities, deployment topology and design rationale. Existing source requirement: Requirements are specific, measurable and technology-explicit. Required delivery form: Versioned solution design with component responsibilities, interfaces and measurable quality responses.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: The strategy defines how production-like data is obtained lawfully
- G6: any approach relying on unmasked production personal data is rejected
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:3.contract_input_1`** — `object`

- Analyse the specific input "System landscape" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:3.contract_input_2`** — `object`

- Analyse the specific input "Delivery model and cadence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:3.contract_input_3`** — `object`

- Analyse the specific input "Data protection constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:3.contract_input_4`** — `object`

- Analyse the specific input "Current tooling estate" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/test-architect:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/test-architect:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/test-architect:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/test-architect:3.irrelevant_detail`** — `object`

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

- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Test Architect:** ISO/IEC/IEEE 29119; test pyramid and contract testing practice; data masking standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Use risk-based test or assessment methods with expected/actual results, coverage, sampling and bounded conclusions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-test-architect-4"></a>

## quality metric framework

**At a glance**

- **Purpose:** Produce and govern the role deliverable: quality metric framework.
- **Mandatory examples:** Explain thresholds, uncertainty, missing data and actions supported by the view. Define metrics, units, denominators, targets, refresh cadence and accountable owners. Provide dated observations linked to versioned source queries and population scope.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `test-architect:4`.

**Required inputs:**

- System landscape
- Delivery model and cadence
- Data protection constraints
- Current tooling estate

**Specification:** `kind/role/test-architect:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: quality metric framework.

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

**`role/test-architect:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: quality metric framework.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:4.receiving_acceptance`** — `array`

- For each receiving role (Test Manager; Test Automation Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:4.delivery_verification`** — `array`

- For the specific output 'quality metric framework', provide verifiable evidence satisfying: For each metric, define question, formula, unit, population/denominator, time window, target/threshold and accountable owner. Show observation timestamp, source/query version, aggregation, missing-data handling and measurement limitations. Explain threshold crossings and trends, uncertainty and the action or decision supported; distinguish operational signals from causal explanations. Required delivery form: Dashboard or scorecard with metric definitions, observations, source queries and interpretation.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: The strategy defines how production-like data is obtained lawfully
- G6: any approach relying on unmasked production personal data is rejected
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:4.contract_input_1`** — `object`

- Analyse the specific input "System landscape" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:4.contract_input_2`** — `object`

- Analyse the specific input "Delivery model and cadence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:4.contract_input_3`** — `object`

- Analyse the specific input "Data protection constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:4.contract_input_4`** — `object`

- Analyse the specific input "Current tooling estate" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/test-architect:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

**`role/test-architect:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/test-architect:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.iso.org/standard/79429.html); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.w3.org/TR/WCAG22/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/test-architect:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/test-architect:4.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Test Architect:** ISO/IEC/IEEE 29119; test pyramid and contract testing practice; data masking standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Use risk-based test or assessment methods with expected/actual results, coverage, sampling and bounded conclusions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
