<!-- JAI:OUTPUT-CONTRACTS:START -->
# Business Security Architect (SABSA Contextual Layer): output contracts

Establish what the business needs security to achieve, in the business's own language, before any technology is considered

[Full catalogue](index.md)

<a id="output-business-security-architect-sabsa-contextual-layer-1"></a>

## Contextual security architecture (business view)

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Contextual security architecture (business view).
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `business-security-architect-sabsa-contextual-layer:1`.

**Required inputs:**

- Business strategy and objectives
- Business process and value streams
- Legal and regulatory obligations
- Business risk appetite

**Specification:** `kind/role/business-security-architect-sabsa-contextual-layer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Contextual security architecture (business view).

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

**`role/business-security-architect-sabsa-contextual-layer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Contextual security architecture (business view).
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:1.receiving_acceptance`** — `array`

- For each receiving role (Business Attribute Profiler; Conceptual Security Architect (SABSA Architect's View)), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:1.delivery_verification`** — `array`

- For the specific output 'Contextual security architecture (business view)', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Existing source requirement: Every element traces to a driver or a quality-attribute target; no orphan elements. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Requirements are expressed in business outcomes and constraints, never as product names or technical controls
- G6: a contextual layer containing technology choices has skipped the layer it exists to capture
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:1.contract_input_1`** — `object`

- Analyse the specific input "Business strategy and objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:1.contract_input_2`** — `object`

- Analyse the specific input "Business process and value streams" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:1.contract_input_3`** — `object`

- Analyse the specific input "Legal and regulatory obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:1.contract_input_4`** — `object`

- Analyse the specific input "Business risk appetite" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/business-security-architect-sabsa-contextual-layer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/business-security-architect-sabsa-contextual-layer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/business-security-architect-sabsa-contextual-layer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/business-security-architect-sabsa-contextual-layer:1.irrelevant_detail`** — `object`

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

- **Business Security Architect (SABSA Contextual Layer):** SABSA contextual layer and the What-Why-How-Who-Where-When matrix; ISO/IEC 27001 context of the organisation; BIZBOK. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace business drivers and measurable attributes through risks, control objectives, services, mechanisms and operational measures.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-business-security-architect-sabsa-contextual-layer-2"></a>

## business driver and requirement catalogue

**At a glance**

- **Purpose:** Produce and govern the role deliverable: business driver and requirement catalogue.
- **Mandatory examples:** Identify actual governed entities with owners, source, status and lifecycle dates. Evidence duplicate detection, relationship integrity and reconciliation against sources. Define entity classes, stable identifiers, required attributes and relations.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `business-security-architect-sabsa-contextual-layer:2`.

**Required inputs:**

- Business strategy and objectives
- Business process and value streams
- Legal and regulatory obligations
- Business risk appetite

**Specification:** `kind/role/business-security-architect-sabsa-contextual-layer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: business driver and requirement catalogue.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/catalogue`](spec-type-catalogue.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `governed-catalogue`.

Structured entity definitions/entries with stable identifiers, metadata, ownership and relationships.

**Evidence accompanying the work product:**

- source reconciliation and lifecycle state
- duplicate/reference integrity checks

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/business-security-architect-sabsa-contextual-layer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: business driver and requirement catalogue.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:2.receiving_acceptance`** — `array`

- For each receiving role (Business Attribute Profiler; Conceptual Security Architect (SABSA Architect's View)), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:2.delivery_verification`** — `array`

- For the specific output 'business driver and requirement catalogue', provide verifiable evidence satisfying: Define the catalogued entity type, unique identifier, classification, required descriptive fields and inclusion/exclusion rules. Provide usable entries with owner, state, source/version, discovery/access reference and relevant service or dependency relationships. Check identifiers, required metadata, broken references, duplicates and lifecycle status; name unresolved gaps and responsible maintainers. Existing source requirement: Each entry has an owner, a lifecycle status and a last-verified date. Required delivery form: Structured entity definitions/entries with stable identifiers, metadata, ownership and relationships.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Requirements are expressed in business outcomes and constraints, never as product names or technical controls
- G6: a contextual layer containing technology choices has skipped the layer it exists to capture
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:2.contract_input_1`** — `object`

- Analyse the specific input "Business strategy and objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:2.contract_input_2`** — `object`

- Analyse the specific input "Business process and value streams" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:2.contract_input_3`** — `object`

- Analyse the specific input "Legal and regulatory obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:2.contract_input_4`** — `object`

- Analyse the specific input "Business risk appetite" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/business-security-architect-sabsa-contextual-layer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/business-security-architect-sabsa-contextual-layer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/business-security-architect-sabsa-contextual-layer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/business-security-architect-sabsa-contextual-layer:2.irrelevant_detail`** — `object`

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
- **[SABSA Institute, SABSA Executive Summary](https://sabsa.org/sabsa-executive-summary/)** — Business-driven security architecture and traceability overview; actual SABSA deliveries must select the accessible authoritative method/version and their detailed obligations. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Business Security Architect (SABSA Contextual Layer):** SABSA contextual layer and the What-Why-How-Who-Where-When matrix; ISO/IEC 27001 context of the organisation; BIZBOK. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace business drivers and measurable attributes through risks, control objectives, services, mechanisms and operational measures.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-business-security-architect-sabsa-contextual-layer-3"></a>

## business risk and opportunity context

**At a glance**

- **Purpose:** Produce and govern the role deliverable: business risk and opportunity context.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `business-security-architect-sabsa-contextual-layer:3`.

**Required inputs:**

- Business strategy and objectives
- Business process and value streams
- Legal and regulatory obligations
- Business risk appetite

**Specification:** `kind/role/business-security-architect-sabsa-contextual-layer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: business risk and opportunity context.

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

**`role/business-security-architect-sabsa-contextual-layer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: business risk and opportunity context.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:3.receiving_acceptance`** — `array`

- For each receiving role (Business Attribute Profiler; Conceptual Security Architect (SABSA Architect's View)), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:3.delivery_verification`** — `array`

- For the specific output 'business risk and opportunity context', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Requirements are expressed in business outcomes and constraints, never as product names or technical controls
- G6: a contextual layer containing technology choices has skipped the layer it exists to capture
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:3.contract_input_1`** — `object`

- Analyse the specific input "Business strategy and objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:3.contract_input_2`** — `object`

- Analyse the specific input "Business process and value streams" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:3.contract_input_3`** — `object`

- Analyse the specific input "Legal and regulatory obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:3.contract_input_4`** — `object`

- Analyse the specific input "Business risk appetite" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/business-security-architect-sabsa-contextual-layer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/business-security-architect-sabsa-contextual-layer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/business-security-architect-sabsa-contextual-layer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/business-security-architect-sabsa-contextual-layer:3.irrelevant_detail`** — `object`

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
- **[SABSA Institute, SABSA Executive Summary](https://sabsa.org/sabsa-executive-summary/)** — Business-driven security architecture and traceability overview; actual SABSA deliveries must select the accessible authoritative method/version and their detailed obligations. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Business Security Architect (SABSA Contextual Layer):** SABSA contextual layer and the What-Why-How-Who-Where-When matrix; ISO/IEC 27001 context of the organisation; BIZBOK. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace business drivers and measurable attributes through risks, control objectives, services, mechanisms and operational measures.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-business-security-architect-sabsa-contextual-layer-4"></a>

## security business case inputs

**At a glance**

- **Purpose:** Produce and govern the role deliverable: security business case inputs.
- **Mandatory examples:** Identify sponsor, financial owner, funding decision and appraisal horizon. Show dated currency, baseline, costs and non-overlapping benefits with assumptions. Assess uncertain benefit, cost and timing assumptions and assign realisation owners.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `business-security-architect-sabsa-contextual-layer:4`.

**Required inputs:**

- Business strategy and objectives
- Business process and value streams
- Legal and regulatory obligations
- Business risk appetite

**Specification:** `kind/role/business-security-architect-sabsa-contextual-layer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: security business case inputs.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/business-case`](spec-type-business-case.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `investment-appraisal`.

Reconciled investment appraisal with dated financial model and accountable benefits.

**Evidence accompanying the work product:**

- source cash flows and calculations
- scenario sensitivity and benefit ownership

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/business-security-architect-sabsa-contextual-layer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: security business case inputs.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:4.receiving_acceptance`** — `array`

- For each receiving role (Business Attribute Profiler; Conceptual Security Architect (SABSA Architect's View)), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:4.delivery_verification`** — `array`

- For the specific output 'security business case inputs', provide verifiable evidence satisfying: State sponsor, financial owner, investment boundary, appraisal period and the precise funding or continuation decision requested. Show source and date of costs/benefits, currency, price basis, cash-flow periods, baseline and incremental treatment; avoid double-counted benefits. Identify key uncertain variables, sensitivity/scenario results, benefit measures, baseline, accountable realisation owner and review trigger. Required delivery form: Reconciled investment appraisal with dated financial model and accountable benefits.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Requirements are expressed in business outcomes and constraints, never as product names or technical controls
- G6: a contextual layer containing technology choices has skipped the layer it exists to capture
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:4.contract_input_1`** — `object`

- Analyse the specific input "Business strategy and objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:4.contract_input_2`** — `object`

- Analyse the specific input "Business process and value streams" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:4.contract_input_3`** — `object`

- Analyse the specific input "Legal and regulatory obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:4.contract_input_4`** — `object`

- Analyse the specific input "Business risk appetite" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/business-security-architect-sabsa-contextual-layer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/business-security-architect-sabsa-contextual-layer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/business-security-architect-sabsa-contextual-layer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/business-security-architect-sabsa-contextual-layer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/business-security-architect-sabsa-contextual-layer:4.irrelevant_detail`** — `object`

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

- **[HM Treasury, The Green Book](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)** — Options, appraisal, costs, benefits, risk, uncertainty and evaluation; used as a practice reference outside its own jurisdiction. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[SABSA Institute, SABSA Executive Summary](https://sabsa.org/sabsa-executive-summary/)** — Business-driven security architecture and traceability overview; actual SABSA deliveries must select the accessible authoritative method/version and their detailed obligations. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Business Security Architect (SABSA Contextual Layer):** SABSA contextual layer and the What-Why-How-Who-Where-When matrix; ISO/IEC 27001 context of the organisation; BIZBOK. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace business drivers and measurable attributes through risks, control objectives, services, mechanisms and operational measures.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
