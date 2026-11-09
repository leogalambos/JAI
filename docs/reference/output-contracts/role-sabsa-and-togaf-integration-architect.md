<!-- JAI:OUTPUT-CONTRACTS:START -->
# SABSA and TOGAF Integration Architect: output contracts

Make security architecture and enterprise architecture one coherent practice rather than two competing ones

[Full catalogue](index.md)

<a id="output-sabsa-and-togaf-integration-architect-1"></a>

## Integrated architecture method and governance

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Integrated architecture method and governance.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `sabsa-and-togaf-integration-architect:1`.

**Required inputs:**

- Enterprise architecture method
- Security architecture method
- Existing artefact and repository estate
- Governance forum structure

**Specification:** `kind/role/sabsa-and-togaf-integration-architect:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Integrated architecture method and governance.

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

**`role/sabsa-and-togaf-integration-architect:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Integrated architecture method and governance.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:1.receiving_acceptance`** — `array`

- For each receiving role (Solution Architect; Security Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:1.delivery_verification`** — `array`

- For the specific output 'Integrated architecture method and governance', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Existing source requirement: Every element traces to a driver or a quality-attribute target; no orphan elements. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Security requirements enter at the same ADM phase as other requirements, not as a review at the end
- G6: a method where security reviews designs after they are approved is reported as structurally broken
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:1.contract_input_1`** — `object`

- Analyse the specific input "Enterprise architecture method" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:1.contract_input_2`** — `object`

- Analyse the specific input "Security architecture method" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:1.contract_input_3`** — `object`

- Analyse the specific input "Existing artefact and repository estate" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:1.contract_input_4`** — `object`

- Analyse the specific input "Governance forum structure" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/sabsa-and-togaf-integration-architect:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/sabsa-and-togaf-integration-architect:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/sabsa-and-togaf-integration-architect:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/sabsa-and-togaf-integration-architect:1.irrelevant_detail`** — `object`

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

- **SABSA and TOGAF Integration Architect:** SABSA; TOGAF 10 ADM; ArchiMate 3.2; ISO/IEC 42010. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace business drivers and measurable attributes through risks, control objectives, services, mechanisms and operational measures.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-sabsa-and-togaf-integration-architect-2"></a>

## mapping between SABSA layers and TOGAF ADM phases

**At a glance**

- **Purpose:** Produce and govern the role deliverable: mapping between SABSA layers and TOGAF ADM phases.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `sabsa-and-togaf-integration-architect:2`.

**Required inputs:**

- Enterprise architecture method
- Security architecture method
- Existing artefact and repository estate
- Governance forum structure

**Specification:** `kind/role/sabsa-and-togaf-integration-architect:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: mapping between SABSA layers and TOGAF ADM phases.

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

**`role/sabsa-and-togaf-integration-architect:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: mapping between SABSA layers and TOGAF ADM phases.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:2.receiving_acceptance`** — `array`

- For each receiving role (Solution Architect; Security Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:2.delivery_verification`** — `array`

- For the specific output 'mapping between SABSA layers and TOGAF ADM phases', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Security requirements enter at the same ADM phase as other requirements, not as a review at the end
- G6: a method where security reviews designs after they are approved is reported as structurally broken
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:2.contract_input_1`** — `object`

- Analyse the specific input "Enterprise architecture method" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:2.contract_input_2`** — `object`

- Analyse the specific input "Security architecture method" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:2.contract_input_3`** — `object`

- Analyse the specific input "Existing artefact and repository estate" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:2.contract_input_4`** — `object`

- Analyse the specific input "Governance forum structure" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/sabsa-and-togaf-integration-architect:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/sabsa-and-togaf-integration-architect:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://sabsa.org/sabsa-executive-summary/); [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/sabsa-and-togaf-integration-architect:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/sabsa-and-togaf-integration-architect:2.irrelevant_detail`** — `object`

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
- **[SABSA Institute, SABSA Executive Summary](https://sabsa.org/sabsa-executive-summary/)** — Business-driven security architecture and traceability overview; actual SABSA deliveries must select the accessible authoritative method/version and their detailed obligations. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **SABSA and TOGAF Integration Architect:** SABSA; TOGAF 10 ADM; ArchiMate 3.2; ISO/IEC 42010. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace business drivers and measurable attributes through risks, control objectives, services, mechanisms and operational measures.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-sabsa-and-togaf-integration-architect-3"></a>

## shared repository and artefact model

**At a glance**

- **Purpose:** Produce and govern the role deliverable: shared repository and artefact model.
- **Mandatory examples:** List stable source-model element IDs, typed relations and labels represented in the view. Evidence endpoint validity, semantic compatibility, coverage and visual readability. Define the concern, viewpoint, system boundary, legend and notation.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `sabsa-and-togaf-integration-architect:3`.

**Required inputs:**

- Enterprise architecture method
- Security architecture method
- Existing artefact and repository estate
- Governance forum structure

**Specification:** `kind/role/sabsa-and-togaf-integration-architect:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: shared repository and artefact model.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/diagram`](spec-type-diagram.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `model-derived-view`.

Concern-specific diagram with declared notation, legend, typed relationships and source-element links.

**Evidence accompanying the work product:**

- endpoint/meaning/coverage checks
- legibility and explicit projection limitations

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/sabsa-and-togaf-integration-architect:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: shared repository and artefact model.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:3.receiving_acceptance`** — `array`

- For each receiving role (Solution Architect; Security Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:3.delivery_verification`** — `array`

- For the specific output 'shared repository and artefact model', provide verifiable evidence satisfying: Identify diagram purpose, scope, audience, version and notation/legend, including the meaning of every relationship type. Use stable element identifiers and meaningful labels; show relevant boundaries, directions, interfaces and external dependencies without invented facts. Check consistency with source models and related views; distinguish intentional abstraction from omitted or unresolved relationships. Existing source requirement: The model is validated against real observed behaviour or data, not only interviews. Required delivery form: Concern-specific diagram with declared notation, legend, typed relationships and source-element links.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Security requirements enter at the same ADM phase as other requirements, not as a review at the end
- G6: a method where security reviews designs after they are approved is reported as structurally broken
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:3.contract_input_1`** — `object`

- Analyse the specific input "Enterprise architecture method" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:3.contract_input_2`** — `object`

- Analyse the specific input "Security architecture method" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:3.contract_input_3`** — `object`

- Analyse the specific input "Existing artefact and repository estate" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:3.contract_input_4`** — `object`

- Analyse the specific input "Governance forum structure" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/sabsa-and-togaf-integration-architect:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/sabsa-and-togaf-integration-architect:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://sabsa.org/sabsa-executive-summary/); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/sabsa-and-togaf-integration-architect:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/sabsa-and-togaf-integration-architect:3.irrelevant_detail`** — `object`

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

- **SABSA and TOGAF Integration Architect:** SABSA; TOGAF 10 ADM; ArchiMate 3.2; ISO/IEC 42010. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace business drivers and measurable attributes through risks, control objectives, services, mechanisms and operational measures.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-sabsa-and-togaf-integration-architect-4"></a>

## joint review and gate design

**At a glance**

- **Purpose:** Produce and govern the role deliverable: joint review and gate design.
- **Mandatory examples:** Describe bounded component responsibilities and deployment topology. Map measurable quality requirements to design verification and acceptance. Define versioned interface inputs, outputs, trust boundaries and failure handling.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `sabsa-and-togaf-integration-architect:4`.

**Required inputs:**

- Enterprise architecture method
- Security architecture method
- Existing artefact and repository estate
- Governance forum structure

**Specification:** `kind/role/sabsa-and-togaf-integration-architect:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: joint review and gate design.

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

**`role/sabsa-and-togaf-integration-architect:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: joint review and gate design.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://sabsa.org/sabsa-executive-summary/) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:4.receiving_acceptance`** — `array`

- For each receiving role (Solution Architect; Security Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://sabsa.org/sabsa-executive-summary/) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://sabsa.org/sabsa-executive-summary/) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://sabsa.org/sabsa-executive-summary/) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:4.delivery_verification`** — `array`

- For the specific output 'joint review and gate design', provide verifiable evidence satisfying: Define the proposed implementation boundary, use cases and external dependencies. State measurable availability, performance, security and operational acceptance targets. Describe component responsibilities, deployment topology and design rationale. Existing source requirement: Every gate has an accountable authority, required SABSA/TOGAF inputs, evidence, entry/exit criteria and escalation path. Required delivery form: Versioned solution design with component responsibilities, interfaces and measurable quality responses.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://sabsa.org/sabsa-executive-summary/) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Security requirements enter at the same ADM phase as other requirements, not as a review at the end
- G6: a method where security reviews designs after they are approved is reported as structurally broken
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://sabsa.org/sabsa-executive-summary/) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:4.contract_input_1`** — `object`

- Analyse the specific input "Enterprise architecture method" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://sabsa.org/sabsa-executive-summary/) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:4.contract_input_2`** — `object`

- Analyse the specific input "Security architecture method" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://sabsa.org/sabsa-executive-summary/) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:4.contract_input_3`** — `object`

- Analyse the specific input "Existing artefact and repository estate" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://sabsa.org/sabsa-executive-summary/) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:4.contract_input_4`** — `object`

- Analyse the specific input "Governance forum structure" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://sabsa.org/sabsa-executive-summary/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/sabsa-and-togaf-integration-architect:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://sabsa.org/sabsa-executive-summary/) (informed-by; not a verbatim standard requirement).

**`role/sabsa-and-togaf-integration-architect:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://sabsa.org/sabsa-executive-summary/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/sabsa-and-togaf-integration-architect:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://sabsa.org/sabsa-executive-summary/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/sabsa-and-togaf-integration-architect:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/sabsa-and-togaf-integration-architect:4.irrelevant_detail`** — `object`

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
- **[SABSA Institute, SABSA Executive Summary](https://sabsa.org/sabsa-executive-summary/)** — Business-driven security architecture and traceability overview; actual SABSA deliveries must select the accessible authoritative method/version and their detailed obligations. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **SABSA and TOGAF Integration Architect:** SABSA; TOGAF 10 ADM; ArchiMate 3.2; ISO/IEC 42010. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace business drivers and measurable attributes through risks, control objectives, services, mechanisms and operational measures.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
