<!-- JAI:OUTPUT-CONTRACTS:START -->
# Business Attribute Profiler: output contracts

Translate business drivers into measurable business attributes that security architecture can actually be designed and tested against

[Full catalogue](index.md)

<a id="output-business-attribute-profiler-1"></a>

## Business attribute profile

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Business attribute profile.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `business-attribute-profiler:1`.

**Required inputs:**

- Business drivers and objectives
- Stakeholder expectations
- Regulatory constraints
- Existing performance data

**Specification:** `kind/role/business-attribute-profiler:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Business attribute profile.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/business-attribute-profiler:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Business attribute profile.

**`role/business-attribute-profiler:1.receiving_acceptance`** — `array`

- For each receiving role (Conceptual Security Architect (SABSA Architect's View); Security Assurance and Measurement Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/business-attribute-profiler:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/business-attribute-profiler:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/business-attribute-profiler:1.delivery_verification`** — `array`

- For the specific output 'Business attribute profile', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/business-attribute-profiler:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("Business attribute profile") has been walked through with the people who will build, test and operate the result.
- G5: Every attribute has a definition, a metric, a measurement method and a target threshold agreed with the business
- G6: attributes without measures cannot drive design or prove assurance and are rejected

**`role/business-attribute-profiler:1.contract_input_1`** — `object`

- Analyse the specific input "Business drivers and objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/business-attribute-profiler:1.contract_input_2`** — `object`

- Analyse the specific input "Stakeholder expectations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/business-attribute-profiler:1.contract_input_3`** — `object`

- Analyse the specific input "Regulatory constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/business-attribute-profiler:1.contract_input_4`** — `object`

- Analyse the specific input "Existing performance data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/business-attribute-profiler:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/business-attribute-profiler:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/business-attribute-profiler:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/business-attribute-profiler:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/business-attribute-profiler:1.irrelevant_detail`** — `object`

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

### Role framework context

- **Business Attribute Profiler:** SABSA business attribute profiling; SABSA attributes taxonomy; measurement and metrics design practice. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-business-attribute-profiler-2"></a>

## attribute definitions with measurement approach

**At a glance**

- **Purpose:** Produce and govern the role deliverable: attribute definitions with measurement approach.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `business-attribute-profiler:2`.

**Required inputs:**

- Business drivers and objectives
- Stakeholder expectations
- Regulatory constraints
- Existing performance data

**Specification:** `kind/role/business-attribute-profiler:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: attribute definitions with measurement approach.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/business-attribute-profiler:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: attribute definitions with measurement approach.

**`role/business-attribute-profiler:2.receiving_acceptance`** — `array`

- For each receiving role (Conceptual Security Architect (SABSA Architect's View); Security Assurance and Measurement Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/business-attribute-profiler:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/business-attribute-profiler:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/business-attribute-profiler:2.delivery_verification`** — `array`

- For the specific output 'attribute definitions with measurement approach', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/business-attribute-profiler:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("Business attribute profile") has been walked through with the people who will build, test and operate the result.
- G5: Every attribute has a definition, a metric, a measurement method and a target threshold agreed with the business
- G6: attributes without measures cannot drive design or prove assurance and are rejected

**`role/business-attribute-profiler:2.contract_input_1`** — `object`

- Analyse the specific input "Business drivers and objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/business-attribute-profiler:2.contract_input_2`** — `object`

- Analyse the specific input "Stakeholder expectations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/business-attribute-profiler:2.contract_input_3`** — `object`

- Analyse the specific input "Regulatory constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/business-attribute-profiler:2.contract_input_4`** — `object`

- Analyse the specific input "Existing performance data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/business-attribute-profiler:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/business-attribute-profiler:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/business-attribute-profiler:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/business-attribute-profiler:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/business-attribute-profiler:2.irrelevant_detail`** — `object`

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

### Role framework context

- **Business Attribute Profiler:** SABSA business attribute profiling; SABSA attributes taxonomy; measurement and metrics design practice. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-business-attribute-profiler-3"></a>

## performance targets and thresholds per attribute

**At a glance**

- **Purpose:** Produce and govern the role deliverable: performance targets and thresholds per attribute.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `business-attribute-profiler:3`.

**Required inputs:**

- Business drivers and objectives
- Stakeholder expectations
- Regulatory constraints
- Existing performance data

**Specification:** `kind/role/business-attribute-profiler:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: performance targets and thresholds per attribute.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/business-attribute-profiler:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: performance targets and thresholds per attribute.

**`role/business-attribute-profiler:3.receiving_acceptance`** — `array`

- For each receiving role (Conceptual Security Architect (SABSA Architect's View); Security Assurance and Measurement Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/business-attribute-profiler:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/business-attribute-profiler:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/business-attribute-profiler:3.delivery_verification`** — `array`

- For the specific output 'performance targets and thresholds per attribute', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/business-attribute-profiler:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("Business attribute profile") has been walked through with the people who will build, test and operate the result.
- G5: Every attribute has a definition, a metric, a measurement method and a target threshold agreed with the business
- G6: attributes without measures cannot drive design or prove assurance and are rejected

**`role/business-attribute-profiler:3.contract_input_1`** — `object`

- Analyse the specific input "Business drivers and objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/business-attribute-profiler:3.contract_input_2`** — `object`

- Analyse the specific input "Stakeholder expectations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/business-attribute-profiler:3.contract_input_3`** — `object`

- Analyse the specific input "Regulatory constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/business-attribute-profiler:3.contract_input_4`** — `object`

- Analyse the specific input "Existing performance data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/business-attribute-profiler:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/business-attribute-profiler:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/business-attribute-profiler:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/business-attribute-profiler:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/business-attribute-profiler:3.irrelevant_detail`** — `object`

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

### Role framework context

- **Business Attribute Profiler:** SABSA business attribute profiling; SABSA attributes taxonomy; measurement and metrics design practice. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-business-attribute-profiler-4"></a>

## traceability from drivers to attributes

**At a glance**

- **Purpose:** Produce and govern the role deliverable: traceability from drivers to attributes.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `business-attribute-profiler:4`.

**Required inputs:**

- Business drivers and objectives
- Stakeholder expectations
- Regulatory constraints
- Existing performance data

**Specification:** `kind/role/business-attribute-profiler:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: traceability from drivers to attributes.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/business-attribute-profiler:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: traceability from drivers to attributes.

**`role/business-attribute-profiler:4.receiving_acceptance`** — `array`

- For each receiving role (Conceptual Security Architect (SABSA Architect's View); Security Assurance and Measurement Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/business-attribute-profiler:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/business-attribute-profiler:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/business-attribute-profiler:4.delivery_verification`** — `array`

- For the specific output 'traceability from drivers to attributes', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/business-attribute-profiler:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("Business attribute profile") has been walked through with the people who will build, test and operate the result.
- G5: Every attribute has a definition, a metric, a measurement method and a target threshold agreed with the business
- G6: attributes without measures cannot drive design or prove assurance and are rejected

**`role/business-attribute-profiler:4.contract_input_1`** — `object`

- Analyse the specific input "Business drivers and objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/business-attribute-profiler:4.contract_input_2`** — `object`

- Analyse the specific input "Stakeholder expectations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/business-attribute-profiler:4.contract_input_3`** — `object`

- Analyse the specific input "Regulatory constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/business-attribute-profiler:4.contract_input_4`** — `object`

- Analyse the specific input "Existing performance data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/business-attribute-profiler:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/business-attribute-profiler:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/business-attribute-profiler:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/business-attribute-profiler:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/business-attribute-profiler:4.irrelevant_detail`** — `object`

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

### Role framework context

- **Business Attribute Profiler:** SABSA business attribute profiling; SABSA attributes taxonomy; measurement and metrics design practice. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
