<!-- JAI:OUTPUT-CONTRACTS:START -->
# Information Architect: output contracts

Organise content and functionality so people can find things and understand where they are

[Full catalogue](index.md)

<a id="output-information-architect-1"></a>

## Site and content structure

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Site and content structure.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `information-architect:1`.

**Required inputs:**

- Content inventory and audit
- User mental models research
- Search and navigation analytics
- Governance and ownership model

**Specification:** `kind/role/information-architect:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Site and content structure.

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

**`role/information-architect:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Site and content structure.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:1.receiving_acceptance`** — `array`

- For each receiving role (Content Designer; Frontend Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:1.delivery_verification`** — `array`

- For the specific output 'Site and content structure', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: Structure is validated with tree testing or card sorting against real user tasks, not agreed in a workshop with stakeholders alone
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:1.contract_input_1`** — `object`

- Analyse the specific input "Content inventory and audit" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:1.contract_input_2`** — `object`

- Analyse the specific input "User mental models research" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:1.contract_input_3`** — `object`

- Analyse the specific input "Search and navigation analytics" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:1.contract_input_4`** — `object`

- Analyse the specific input "Governance and ownership model" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/information-architect:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/information-architect:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/information-architect:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/information-architect:1.irrelevant_detail`** — `object`

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
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Information Architect:** information architecture practice; ISO/IEC 11179 for metadata; WCAG 2.2 AA navigation criteria. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-information-architect-2"></a>

## navigation and taxonomy design

**At a glance**

- **Purpose:** Produce and govern the role deliverable: navigation and taxonomy design.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `information-architect:2`.

**Required inputs:**

- Content inventory and audit
- User mental models research
- Search and navigation analytics
- Governance and ownership model

**Specification:** `kind/role/information-architect:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: navigation and taxonomy design.

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

**`role/information-architect:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: navigation and taxonomy design.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:2.receiving_acceptance`** — `array`

- For each receiving role (Content Designer; Frontend Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:2.delivery_verification`** — `array`

- For the specific output 'navigation and taxonomy design', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Existing source requirement: Defines labels, hierarchy, relationships, user tasks and findability validation with evidence gaps. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: Structure is validated with tree testing or card sorting against real user tasks, not agreed in a workshop with stakeholders alone
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:2.contract_input_1`** — `object`

- Analyse the specific input "Content inventory and audit" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:2.contract_input_2`** — `object`

- Analyse the specific input "User mental models research" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:2.contract_input_3`** — `object`

- Analyse the specific input "Search and navigation analytics" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:2.contract_input_4`** — `object`

- Analyse the specific input "Governance and ownership model" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/information-architect:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/information-architect:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/information-architect:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/information-architect:2.irrelevant_detail`** — `object`

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
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Information Architect:** information architecture practice; ISO/IEC 11179 for metadata; WCAG 2.2 AA navigation criteria. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-information-architect-3"></a>

## labelling and metadata schemes

**At a glance**

- **Purpose:** Produce and govern the role deliverable: labelling and metadata schemes.
- **Mandatory examples:** Identify actual governed entities with owners, source, status and lifecycle dates. Evidence duplicate detection, relationship integrity and reconciliation against sources. Define entity classes, stable identifiers, required attributes and relations.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `information-architect:3`.

**Required inputs:**

- Content inventory and audit
- User mental models research
- Search and navigation analytics
- Governance and ownership model

**Specification:** `kind/role/information-architect:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: labelling and metadata schemes.

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

**`role/information-architect:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: labelling and metadata schemes.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:3.receiving_acceptance`** — `array`

- For each receiving role (Content Designer; Frontend Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:3.delivery_verification`** — `array`

- For the specific output 'labelling and metadata schemes', provide verifiable evidence satisfying: Define the catalogued entity type, unique identifier, classification, required descriptive fields and inclusion/exclusion rules. Provide usable entries with owner, state, source/version, discovery/access reference and relevant service or dependency relationships. Check identifiers, required metadata, broken references, duplicates and lifecycle status; name unresolved gaps and responsible maintainers. Required delivery form: Structured entity definitions/entries with stable identifiers, metadata, ownership and relationships.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: Structure is validated with tree testing or card sorting against real user tasks, not agreed in a workshop with stakeholders alone
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:3.contract_input_1`** — `object`

- Analyse the specific input "Content inventory and audit" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:3.contract_input_2`** — `object`

- Analyse the specific input "User mental models research" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:3.contract_input_3`** — `object`

- Analyse the specific input "Search and navigation analytics" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:3.contract_input_4`** — `object`

- Analyse the specific input "Governance and ownership model" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/information-architect:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/information-architect:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/information-architect:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/information-architect:3.irrelevant_detail`** — `object`

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
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Information Architect:** information architecture practice; ISO/IEC 11179 for metadata; WCAG 2.2 AA navigation criteria. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-information-architect-4"></a>

## findability test results

**At a glance**

- **Purpose:** Produce and govern the role deliverable: findability test results.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `information-architect:4`.

**Required inputs:**

- Content inventory and audit
- User mental models research
- Search and navigation analytics
- Governance and ownership model

**Specification:** `kind/role/information-architect:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: findability test results.

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

**`role/information-architect:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: findability test results.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:4.receiving_acceptance`** — `array`

- For each receiving role (Content Designer; Frontend Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:4.delivery_verification`** — `array`

- For the specific output 'findability test results', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Existing source requirement: Identifies assessed scope, method, environment or population, expected and observed outcomes, located findings, untested conditions and residual limitations. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: Structure is validated with tree testing or card sorting against real user tasks, not agreed in a workshop with stakeholders alone
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:4.contract_input_1`** — `object`

- Analyse the specific input "Content inventory and audit" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:4.contract_input_2`** — `object`

- Analyse the specific input "User mental models research" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:4.contract_input_3`** — `object`

- Analyse the specific input "Search and navigation analytics" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:4.contract_input_4`** — `object`

- Analyse the specific input "Governance and ownership model" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/information-architect:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/information-architect:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/information-architect:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/information-architect:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/information-architect:4.irrelevant_detail`** — `object`

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

- **Information Architect:** information architecture practice; ISO/IEC 11179 for metadata; WCAG 2.2 AA navigation criteria. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
