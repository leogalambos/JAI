<!-- JAI:OUTPUT-CONTRACTS:START -->
# Operational and Technology Resilience Architect: output contracts

Design end-to-end technology resilience across services, dependencies, failure domains and recovery capabilities so that business impact tolerances are technically credible.

[Full catalogue](index.md)

<a id="output-operational-and-technology-resilience-architect-1"></a>

## Technology resilience architecture

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Technology resilience architecture.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `operational-and-technology-resilience-architect:1`.

**Required inputs:**

- Business impact tolerances and process priorities
- Service/application/dependency architecture
- Observed reliability and incident evidence
- Supplier continuity constraints

**Specification:** `kind/role/operational-and-technology-resilience-architect:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Technology resilience architecture.

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

**`role/operational-and-technology-resilience-architect:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Technology resilience architecture.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:1.receiving_acceptance`** — `array`

- For each receiving role (Site Reliability Engineer; Disaster Recovery Coordinator), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:1.delivery_verification`** — `array`

- For the specific output 'Technology resilience architecture', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Existing source requirement: Critical service paths, resilience requirements and mechanisms trace to business impact tolerances. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Resilience requirements trace to business impact tolerance or explicit business risk.
- G2: Shared dependencies and failure domains are modelled; duplicated components in one failure domain are not called resilient.
- G3: Recovery claims distinguish failover, restore, rebuild and manual workaround.
- G4: RTO/RPO and degradation claims have validation evidence or a dated validation roadmap.
- G5: Supplier/concentration dependencies have exit, contingency or explicit risk acceptance where material.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:1.contract_input_1`** — `object`

- Analyse the specific input "Business impact tolerances and process priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:1.contract_input_2`** — `object`

- Analyse the specific input "Service/application/dependency architecture" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:1.contract_input_3`** — `object`

- Analyse the specific input "Observed reliability and incident evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:1.contract_input_4`** — `object`

- Analyse the specific input "Supplier continuity constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/operational-and-technology-resilience-architect:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/operational-and-technology-resilience-architect:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/operational-and-technology-resilience-architect:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/operational-and-technology-resilience-architect:1.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Operational and Technology Resilience Architect:** ISO 22301; ISO/IEC 27031; NIST SP 800-34 and relevant operational resilience regulation. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-operational-and-technology-resilience-architect-2"></a>

## Dependency and failure-domain model

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Dependency and failure-domain model.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `operational-and-technology-resilience-architect:2`.

**Required inputs:**

- Business impact tolerances and process priorities
- Service/application/dependency architecture
- Observed reliability and incident evidence
- Supplier continuity constraints

**Specification:** `kind/role/operational-and-technology-resilience-architect:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Dependency and failure-domain model.

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

**`role/operational-and-technology-resilience-architect:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Dependency and failure-domain model.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:2.receiving_acceptance`** — `array`

- For each receiving role (Site Reliability Engineer; Disaster Recovery Coordinator), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:2.delivery_verification`** — `array`

- For the specific output 'Dependency and failure-domain model', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Existing source requirement: Critical dependencies and correlated/shared failure domains are explicit and owned. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Resilience requirements trace to business impact tolerance or explicit business risk.
- G2: Shared dependencies and failure domains are modelled; duplicated components in one failure domain are not called resilient.
- G3: Recovery claims distinguish failover, restore, rebuild and manual workaround.
- G4: RTO/RPO and degradation claims have validation evidence or a dated validation roadmap.
- G5: Supplier/concentration dependencies have exit, contingency or explicit risk acceptance where material.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:2.contract_input_1`** — `object`

- Analyse the specific input "Business impact tolerances and process priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:2.contract_input_2`** — `object`

- Analyse the specific input "Service/application/dependency architecture" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:2.contract_input_3`** — `object`

- Analyse the specific input "Observed reliability and incident evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:2.contract_input_4`** — `object`

- Analyse the specific input "Supplier continuity constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/operational-and-technology-resilience-architect:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/operational-and-technology-resilience-architect:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/operational-and-technology-resilience-architect:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/operational-and-technology-resilience-architect:2.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Operational and Technology Resilience Architect:** ISO 22301; ISO/IEC 27031; NIST SP 800-34 and relevant operational resilience regulation. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-operational-and-technology-resilience-architect-3"></a>

## Recovery architecture and resilience patterns

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Recovery architecture and resilience patterns.
- **Mandatory examples:** Identify stakeholders, system boundary, concerns and architecture baseline. Identify target gaps, accountable owners and decisions required to close them. Link business, data, application and technology viewpoints using stable source-model IDs.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `operational-and-technology-resilience-architect:3`.

**Required inputs:**

- Business impact tolerances and process priorities
- Service/application/dependency architecture
- Observed reliability and incident evidence
- Supplier continuity constraints

**Specification:** `kind/role/operational-and-technology-resilience-architect:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Recovery architecture and resilience patterns.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/architecture-definition`](spec-type-architecture-definition.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `architecture-description`.

Concern-driven description with a versioned model and views selected for stakeholder questions.

**Evidence accompanying the work product:**

- stakeholder/concern coverage
- cross-view consistency and known gaps

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/operational-and-technology-resilience-architect:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Recovery architecture and resilience patterns.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:3.receiving_acceptance`** — `array`

- For each receiving role (Site Reliability Engineer; Disaster Recovery Coordinator), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:3.delivery_verification`** — `array`

- For the specific output 'Recovery architecture and resilience patterns', provide verifiable evidence satisfying: Name the system of interest, boundary exclusions, stakeholder groups, each concern and the versioned current/target baseline. Identify each viewpoint and its conventions; trace each view to the concerns it addresses and identify cross-view correspondences and unresolved inconsistencies. For each material gap, identify current and target elements, business impact, owner, proposed response and the decision or evidence needed to close it. Existing source requirement: Patterns state failure assumptions, degradation mode, RTO/RPO contribution and validation method. Required delivery form: Concern-driven description with a versioned model and views selected for stakeholder questions.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Resilience requirements trace to business impact tolerance or explicit business risk.
- G2: Shared dependencies and failure domains are modelled; duplicated components in one failure domain are not called resilient.
- G3: Recovery claims distinguish failover, restore, rebuild and manual workaround.
- G4: RTO/RPO and degradation claims have validation evidence or a dated validation roadmap.
- G5: Supplier/concentration dependencies have exit, contingency or explicit risk acceptance where material.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:3.contract_input_1`** — `object`

- Analyse the specific input "Business impact tolerances and process priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:3.contract_input_2`** — `object`

- Analyse the specific input "Service/application/dependency architecture" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:3.contract_input_3`** — `object`

- Analyse the specific input "Observed reliability and incident evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:3.contract_input_4`** — `object`

- Analyse the specific input "Supplier continuity constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/operational-and-technology-resilience-architect:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/operational-and-technology-resilience-architect:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/operational-and-technology-resilience-architect:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/operational-and-technology-resilience-architect:3.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Operational and Technology Resilience Architect:** ISO 22301; ISO/IEC 27031; NIST SP 800-34 and relevant operational resilience regulation. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-operational-and-technology-resilience-architect-4"></a>

## Resilience validation roadmap and decision record

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Resilience validation roadmap and decision record.
- **Mandatory examples:** Describe rejected options, reversibility, debt and operational consequences. Record decision status, owner, date and architecture concern. Compare feasible alternatives against explicit drivers and constraints.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `operational-and-technology-resilience-architect:4`.

**Required inputs:**

- Business impact tolerances and process priorities
- Service/application/dependency architecture
- Observed reliability and incident evidence
- Supplier continuity constraints

**Specification:** `kind/role/operational-and-technology-resilience-architect:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Resilience validation roadmap and decision record.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/architecture-decision`](spec-type-architecture-decision.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `architecture-decision-record`.

Versioned decision record with context, alternatives, consequences, status and supersession.

**Evidence accompanying the work product:**

- comparable option evaluation
- actual decision status and owner

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/operational-and-technology-resilience-architect:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Resilience validation roadmap and decision record.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:4.receiving_acceptance`** — `array`

- For each receiving role (Site Reliability Engineer; Disaster Recovery Coordinator), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:4.delivery_verification`** — `array`

- For the specific output 'Resilience validation roadmap and decision record', provide verifiable evidence satisfying: Identify the architecture concern, constraints, scope and decision status. Compare feasible design alternatives and the rejected baseline against drivers. Record the selected design, decision owner and dated rationale. Existing source requirement: Untested claims and residual resilience gaps have owners, dates and acceptance authority. Required delivery form: Versioned decision record with context, alternatives, consequences, status and supersession.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Resilience requirements trace to business impact tolerance or explicit business risk.
- G2: Shared dependencies and failure domains are modelled; duplicated components in one failure domain are not called resilient.
- G3: Recovery claims distinguish failover, restore, rebuild and manual workaround.
- G4: RTO/RPO and degradation claims have validation evidence or a dated validation roadmap.
- G5: Supplier/concentration dependencies have exit, contingency or explicit risk acceptance where material.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:4.contract_input_1`** — `object`

- Analyse the specific input "Business impact tolerances and process priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:4.contract_input_2`** — `object`

- Analyse the specific input "Service/application/dependency architecture" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:4.contract_input_3`** — `object`

- Analyse the specific input "Observed reliability and incident evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:4.contract_input_4`** — `object`

- Analyse the specific input "Supplier continuity constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/operational-and-technology-resilience-architect:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/operational-and-technology-resilience-architect:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/operational-and-technology-resilience-architect:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/operational-and-technology-resilience-architect:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/operational-and-technology-resilience-architect:4.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Operational and Technology Resilience Architect:** ISO 22301; ISO/IEC 27031; NIST SP 800-34 and relevant operational resilience regulation. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
