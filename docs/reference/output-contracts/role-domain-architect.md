<!-- JAI:OUTPUT-CONTRACTS:START -->
# Domain Architect: output contracts

Own the architecture of one business domain so that its systems, data and integrations stay coherent

[Full catalogue](index.md)

<a id="output-domain-architect-1"></a>

## Domain reference architecture

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Domain reference architecture.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `domain-architect:1`.

**Required inputs:**

- Domain business strategy
- Enterprise principles
- Domain system inventory
- Regulatory constraints for the domain

**Specification:** `kind/role/domain-architect:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Domain reference architecture.

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

**`role/domain-architect:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Domain reference architecture.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:1.receiving_acceptance`** — `array`

- For each receiving role (Solution Architect; Data Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:1.delivery_verification`** — `array`

- For the specific output 'Domain reference architecture', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Existing source requirement: Every element traces to a driver or a quality-attribute target; no orphan elements. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Domain boundaries and the ownership of shared entities are agreed with adjacent domains in writing before designs depend on them
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:1.contract_input_1`** — `object`

- Analyse the specific input "Domain business strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:1.contract_input_2`** — `object`

- Analyse the specific input "Enterprise principles" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:1.contract_input_3`** — `object`

- Analyse the specific input "Domain system inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:1.contract_input_4`** — `object`

- Analyse the specific input "Regulatory constraints for the domain" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/domain-architect:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/domain-architect:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/domain-architect:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/domain-architect:1.irrelevant_detail`** — `object`

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

- **Domain Architect:** TOGAF 10; domain-driven design; relevant sector reference models (e.g. TM Forum, BIAN, FHIR). Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-domain-architect-2"></a>

## domain data and service model

**At a glance**

- **Purpose:** Produce and govern the role deliverable: domain data and service model.
- **Mandatory examples:** Define measurable availability, support, capacity and recovery targets. Describe support responsibilities, suppliers, monitoring, continuity and lifecycle costs. Identify customers, service owner, outcomes, boundaries and demand assumptions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `domain-architect:2`.

**Required inputs:**

- Domain business strategy
- Enterprise principles
- Domain system inventory
- Regulatory constraints for the domain

**Specification:** `kind/role/domain-architect:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: domain data and service model.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/service-design`](spec-type-service-design.md)
- [`domain/operations`](spec-domain-operations.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `service-definition`.

Service definition with consumers, outcomes, responsibilities and measurable service commitments.

**Evidence accompanying the work product:**

- indicator/target/window definitions
- support, dependency and recovery arrangements

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/domain-architect:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: domain data and service model.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:2.receiving_acceptance`** — `array`

- For each receiving role (Solution Architect; Data Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:2.delivery_verification`** — `array`

- For the specific output 'domain data and service model', provide verifiable evidence satisfying: State service consumers, business outcomes, eligibility, service boundary, exclusions, accountable owner and demand assumptions. For every service level, define indicator, unit, measurement source/window, target, exclusions and breach response; label unagreed targets as proposals. Define support tiers, ownership, supplier/interface dependencies, change/incident escalation, recovery objectives and cost assumptions. Existing source requirement: The model is validated against real observed behaviour or data, not only interviews. Required delivery form: Service definition with consumers, outcomes, responsibilities and measurable service commitments.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Domain boundaries and the ownership of shared entities are agreed with adjacent domains in writing before designs depend on them
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:2.contract_input_1`** — `object`

- Analyse the specific input "Domain business strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:2.contract_input_2`** — `object`

- Analyse the specific input "Enterprise principles" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:2.contract_input_3`** — `object`

- Analyse the specific input "Domain system inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:2.contract_input_4`** — `object`

- Analyse the specific input "Regulatory constraints for the domain" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/domain-architect:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/domain-architect:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/domain-architect:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/domain-architect:2.irrelevant_detail`** — `object`

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

- **[ISO/IEC 20000-1:2018, Service management system requirements](https://www.iso.org/standard/70636.html)** — Service requirements, agreements, transition, operation and measurement concepts. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Domain Architect:** TOGAF 10; domain-driven design; relevant sector reference models (e.g. TM Forum, BIAN, FHIR). Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-domain-architect-3"></a>

## domain roadmap and lifecycle plan

**At a glance**

- **Purpose:** Produce and govern the role deliverable: domain roadmap and lifecycle plan.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `domain-architect:3`.

**Required inputs:**

- Domain business strategy
- Enterprise principles
- Domain system inventory
- Regulatory constraints for the domain

**Specification:** `kind/role/domain-architect:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: domain roadmap and lifecycle plan.

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

**`role/domain-architect:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: domain roadmap and lifecycle plan.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:3.receiving_acceptance`** — `array`

- For each receiving role (Solution Architect; Data Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:3.delivery_verification`** — `array`

- For the specific output 'domain roadmap and lifecycle plan', provide verifiable evidence satisfying: State business outcomes, current/target baseline, planning horizons, sponsors and material planning assumptions. For each increment, identify deliverables, owner, indicative resource/funding requirement, milestone and measurable completion outcome. Identify dependencies and critical sequence, decision dates, constraints and alternative paths; distinguish committed work from tentative options. Existing source requirement: Each item carries a dependency set, a cost band and a decision date. Required delivery form: Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Domain boundaries and the ownership of shared entities are agreed with adjacent domains in writing before designs depend on them
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:3.contract_input_1`** — `object`

- Analyse the specific input "Domain business strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:3.contract_input_2`** — `object`

- Analyse the specific input "Enterprise principles" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:3.contract_input_3`** — `object`

- Analyse the specific input "Domain system inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:3.contract_input_4`** — `object`

- Analyse the specific input "Regulatory constraints for the domain" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/domain-architect:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/domain-architect:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/domain-architect:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/domain-architect:3.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Domain Architect:** TOGAF 10; domain-driven design; relevant sector reference models (e.g. TM Forum, BIAN, FHIR). Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-domain-architect-4"></a>

## domain-specific standards

**At a glance**

- **Purpose:** Produce and govern the role deliverable: domain-specific standards.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `domain-architect:4`.

**Required inputs:**

- Domain business strategy
- Enterprise principles
- Domain system inventory
- Regulatory constraints for the domain

**Specification:** `kind/role/domain-architect:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: domain-specific standards.

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

**`role/domain-architect:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: domain-specific standards.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:4.receiving_acceptance`** — `array`

- For each receiving role (Solution Architect; Data Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:4.delivery_verification`** — `array`

- For the specific output 'domain-specific standards', provide verifiable evidence satisfying: State the exact subject, intended recipient/use, boundary, source versions and the concrete question the document answers. Provide subject-specific findings or instructions with supporting facts, assumptions, reasoning, limitations and traceable references; generic background alone is insufficient. State conclusions, decisions requested or actionable instructions, accountable recipients and completion/acceptance conditions; identify open issues explicitly. Existing source requirement: Requirements are specific, measurable and technology-explicit. Required delivery form: Purpose-specific professional document with source analysis, reasoning, conclusions and recipient actions.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Domain boundaries and the ownership of shared entities are agreed with adjacent domains in writing before designs depend on them
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:4.contract_input_1`** — `object`

- Analyse the specific input "Domain business strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:4.contract_input_2`** — `object`

- Analyse the specific input "Enterprise principles" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:4.contract_input_3`** — `object`

- Analyse the specific input "Domain system inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:4.contract_input_4`** — `object`

- Analyse the specific input "Regulatory constraints for the domain" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/domain-architect:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/domain-architect:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/domain-architect:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/domain-architect:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/domain-architect:4.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Domain Architect:** TOGAF 10; domain-driven design; relevant sector reference models (e.g. TM Forum, BIAN, FHIR). Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
