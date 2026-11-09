<!-- JAI:OUTPUT-CONTRACTS:START -->
# Chief Security Architect (SABSA Practice Lead): output contracts

Own the enterprise security architecture practice and keep every security decision traceable to a business driver

[Full catalogue](index.md)

<a id="output-chief-security-architect-sabsa-practice-lead-1"></a>

## SABSA architecture practice and governance model

**At a glance**

- **Purpose:** Produce and govern the role deliverable: SABSA architecture practice and governance model.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `chief-security-architect-sabsa-practice-lead:1`.

**Required inputs:**

- Business strategy and drivers
- Risk appetite and tolerance
- Enterprise architecture direction
- Threat and regulatory landscape

**Specification:** `kind/role/chief-security-architect-sabsa-practice-lead:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: SABSA architecture practice and governance model.

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

**`role/chief-security-architect-sabsa-practice-lead:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: SABSA architecture practice and governance model.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:1.receiving_acceptance`** — `array`

- For each receiving role (Business Security Architect (SABSA Contextual Layer); Conceptual Security Architect (SABSA Architect's View); Security Domain Authority), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:1.delivery_verification`** — `array`

- For the specific output 'SABSA architecture practice and governance model', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Existing source requirement: Every element traces to a driver or a quality-attribute target; no orphan elements. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Every control in the enterprise architecture traces upward to a business attribute and a driver
- G6: controls with no traceable business justification are removed as unjustified cost
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:1.contract_input_1`** — `object`

- Analyse the specific input "Business strategy and drivers" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:1.contract_input_2`** — `object`

- Analyse the specific input "Risk appetite and tolerance" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:1.contract_input_3`** — `object`

- Analyse the specific input "Enterprise architecture direction" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:1.contract_input_4`** — `object`

- Analyse the specific input "Threat and regulatory landscape" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/chief-security-architect-sabsa-practice-lead:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/chief-security-architect-sabsa-practice-lead:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/chief-security-architect-sabsa-practice-lead:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/chief-security-architect-sabsa-practice-lead:1.irrelevant_detail`** — `object`

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
- **[SABSA Institute, SABSA Executive Summary](https://sabsa.org/sabsa-executive-summary/)** — Business-driven security architecture and traceability overview; actual SABSA deliveries must select the accessible authoritative method/version and their detailed obligations. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Chief Security Architect (SABSA Practice Lead):** SABSA (Sherwood Applied Business Security Architecture); ISO/IEC 27001; TOGAF 10 for integration; O-ESA. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace business drivers and measurable attributes through risks, control objectives, services, mechanisms and operational measures.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-chief-security-architect-sabsa-practice-lead-2"></a>

## enterprise security architecture matrix

**At a glance**

- **Purpose:** Produce and govern the role deliverable: enterprise security architecture matrix.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `chief-security-architect-sabsa-practice-lead:2`.

**Required inputs:**

- Business strategy and drivers
- Risk appetite and tolerance
- Enterprise architecture direction
- Threat and regulatory landscape

**Specification:** `kind/role/chief-security-architect-sabsa-practice-lead:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: enterprise security architecture matrix.

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

**`role/chief-security-architect-sabsa-practice-lead:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: enterprise security architecture matrix.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:2.receiving_acceptance`** — `array`

- For each receiving role (Business Security Architect (SABSA Contextual Layer); Conceptual Security Architect (SABSA Architect's View); Security Domain Authority), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:2.delivery_verification`** — `array`

- For the specific output 'enterprise security architecture matrix', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Existing source requirement: Every element traces to a driver or a quality-attribute target; no orphan elements. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Every control in the enterprise architecture traces upward to a business attribute and a driver
- G6: controls with no traceable business justification are removed as unjustified cost
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:2.contract_input_1`** — `object`

- Analyse the specific input "Business strategy and drivers" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:2.contract_input_2`** — `object`

- Analyse the specific input "Risk appetite and tolerance" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:2.contract_input_3`** — `object`

- Analyse the specific input "Enterprise architecture direction" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:2.contract_input_4`** — `object`

- Analyse the specific input "Threat and regulatory landscape" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/chief-security-architect-sabsa-practice-lead:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/chief-security-architect-sabsa-practice-lead:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/chief-security-architect-sabsa-practice-lead:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/chief-security-architect-sabsa-practice-lead:2.irrelevant_detail`** — `object`

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
- **[SABSA Institute, SABSA Executive Summary](https://sabsa.org/sabsa-executive-summary/)** — Business-driven security architecture and traceability overview; actual SABSA deliveries must select the accessible authoritative method/version and their detailed obligations. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Chief Security Architect (SABSA Practice Lead):** SABSA (Sherwood Applied Business Security Architecture); ISO/IEC 27001; TOGAF 10 for integration; O-ESA. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace business drivers and measurable attributes through risks, control objectives, services, mechanisms and operational measures.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-chief-security-architect-sabsa-practice-lead-3"></a>

## architecture principles and patterns

**At a glance**

- **Purpose:** Produce and govern the role deliverable: architecture principles and patterns.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `chief-security-architect-sabsa-practice-lead:3`.

**Required inputs:**

- Business strategy and drivers
- Risk appetite and tolerance
- Enterprise architecture direction
- Threat and regulatory landscape

**Specification:** `kind/role/chief-security-architect-sabsa-practice-lead:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: architecture principles and patterns.

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

**`role/chief-security-architect-sabsa-practice-lead:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: architecture principles and patterns.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:3.receiving_acceptance`** — `array`

- For each receiving role (Business Security Architect (SABSA Contextual Layer); Conceptual Security Architect (SABSA Architect's View); Security Domain Authority), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:3.delivery_verification`** — `array`

- For the specific output 'architecture principles and patterns', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Existing source requirement: Every element traces to a driver or a quality-attribute target; no orphan elements. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Every control in the enterprise architecture traces upward to a business attribute and a driver
- G6: controls with no traceable business justification are removed as unjustified cost
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:3.contract_input_1`** — `object`

- Analyse the specific input "Business strategy and drivers" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:3.contract_input_2`** — `object`

- Analyse the specific input "Risk appetite and tolerance" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:3.contract_input_3`** — `object`

- Analyse the specific input "Enterprise architecture direction" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:3.contract_input_4`** — `object`

- Analyse the specific input "Threat and regulatory landscape" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/chief-security-architect-sabsa-practice-lead:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/chief-security-architect-sabsa-practice-lead:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/chief-security-architect-sabsa-practice-lead:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/chief-security-architect-sabsa-practice-lead:3.irrelevant_detail`** — `object`

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
- **[SABSA Institute, SABSA Executive Summary](https://sabsa.org/sabsa-executive-summary/)** — Business-driven security architecture and traceability overview; actual SABSA deliveries must select the accessible authoritative method/version and their detailed obligations. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Chief Security Architect (SABSA Practice Lead):** SABSA (Sherwood Applied Business Security Architecture); ISO/IEC 27001; TOGAF 10 for integration; O-ESA. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace business drivers and measurable attributes through risks, control objectives, services, mechanisms and operational measures.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-chief-security-architect-sabsa-practice-lead-4"></a>

## security architecture roadmap

**At a glance**

- **Purpose:** Produce and govern the role deliverable: security architecture roadmap.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `chief-security-architect-sabsa-practice-lead:4`.

**Required inputs:**

- Business strategy and drivers
- Risk appetite and tolerance
- Enterprise architecture direction
- Threat and regulatory landscape

**Specification:** `kind/role/chief-security-architect-sabsa-practice-lead:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: security architecture roadmap.

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

**`role/chief-security-architect-sabsa-practice-lead:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: security architecture roadmap.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:4.receiving_acceptance`** — `array`

- For each receiving role (Business Security Architect (SABSA Contextual Layer); Conceptual Security Architect (SABSA Architect's View); Security Domain Authority), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:4.delivery_verification`** — `array`

- For the specific output 'security architecture roadmap', provide verifiable evidence satisfying: State business outcomes, current/target baseline, planning horizons, sponsors and material planning assumptions. For each increment, identify deliverables, owner, indicative resource/funding requirement, milestone and measurable completion outcome. Identify dependencies and critical sequence, decision dates, constraints and alternative paths; distinguish committed work from tentative options. Existing source requirement: Every element traces to a driver or a quality-attribute target; no orphan elements. Required delivery form: Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Every control in the enterprise architecture traces upward to a business attribute and a driver
- G6: controls with no traceable business justification are removed as unjustified cost
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:4.contract_input_1`** — `object`

- Analyse the specific input "Business strategy and drivers" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:4.contract_input_2`** — `object`

- Analyse the specific input "Risk appetite and tolerance" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:4.contract_input_3`** — `object`

- Analyse the specific input "Enterprise architecture direction" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:4.contract_input_4`** — `object`

- Analyse the specific input "Threat and regulatory landscape" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/chief-security-architect-sabsa-practice-lead:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/chief-security-architect-sabsa-practice-lead:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/chief-security-architect-sabsa-practice-lead:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/chief-security-architect-sabsa-practice-lead:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/chief-security-architect-sabsa-practice-lead:4.irrelevant_detail`** — `object`

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
- **[SABSA Institute, SABSA Executive Summary](https://sabsa.org/sabsa-executive-summary/)** — Business-driven security architecture and traceability overview; actual SABSA deliveries must select the accessible authoritative method/version and their detailed obligations. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Chief Security Architect (SABSA Practice Lead):** SABSA (Sherwood Applied Business Security Architecture); ISO/IEC 27001; TOGAF 10 for integration; O-ESA. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace business drivers and measurable attributes through risks, control objectives, services, mechanisms and operational measures.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
