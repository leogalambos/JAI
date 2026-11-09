<!-- JAI:OUTPUT-CONTRACTS:START -->
# Service Designer: output contracts

Design the whole service across channels, including the parts users never see

[Full catalogue](index.md)

<a id="output-service-designer-1"></a>

## Service blueprints across front and back stage

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Service blueprints across front and back stage.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `service-designer:1`.

**Required inputs:**

- User journeys and pain points
- Operational process reality
- Policy and regulatory constraints
- Channel capability

**Specification:** `kind/role/service-designer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Service blueprints across front and back stage.

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

**`role/service-designer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Service blueprints across front and back stage.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:1.receiving_acceptance`** — `array`

- For each receiving role (Product Designer; Process Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:1.delivery_verification`** — `array`

- For the specific output 'Service blueprints across front and back stage', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: The blueprint covers back-stage capability and staff experience
- G6: a service design that assumes staff will absorb the complexity is returned as incomplete
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:1.contract_input_1`** — `object`

- Analyse the specific input "User journeys and pain points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:1.contract_input_2`** — `object`

- Analyse the specific input "Operational process reality" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:1.contract_input_3`** — `object`

- Analyse the specific input "Policy and regulatory constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:1.contract_input_4`** — `object`

- Analyse the specific input "Channel capability" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/service-designer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/service-designer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/service-designer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/service-designer:1.irrelevant_detail`** — `object`

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

- **Service Designer:** ISO 9241-210; service design practice; UK GDS service standard as a reference model. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-service-designer-2"></a>

## channel and touchpoint design

**At a glance**

- **Purpose:** Produce and govern the role deliverable: channel and touchpoint design.
- **Mandatory examples:** Define measurable availability, support, capacity and recovery targets. Describe support responsibilities, suppliers, monitoring, continuity and lifecycle costs. Identify customers, service owner, outcomes, boundaries and demand assumptions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `service-designer:2`.

**Required inputs:**

- User journeys and pain points
- Operational process reality
- Policy and regulatory constraints
- Channel capability

**Specification:** `kind/role/service-designer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: channel and touchpoint design.

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

**`role/service-designer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: channel and touchpoint design.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:2.receiving_acceptance`** — `array`

- For each receiving role (Product Designer; Process Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:2.delivery_verification`** — `array`

- For the specific output 'channel and touchpoint design', provide verifiable evidence satisfying: State service consumers, business outcomes, eligibility, service boundary, exclusions, accountable owner and demand assumptions. For every service level, define indicator, unit, measurement source/window, target, exclusions and breach response; label unagreed targets as proposals. Define support tiers, ownership, supplier/interface dependencies, change/incident escalation, recovery objectives and cost assumptions. Existing source requirement: Defines user journeys, front/back-stage responsibilities, channel transitions, failure recovery and validation criteria. Required delivery form: Service definition with consumers, outcomes, responsibilities and measurable service commitments.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: The blueprint covers back-stage capability and staff experience
- G6: a service design that assumes staff will absorb the complexity is returned as incomplete
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:2.contract_input_1`** — `object`

- Analyse the specific input "User journeys and pain points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:2.contract_input_2`** — `object`

- Analyse the specific input "Operational process reality" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:2.contract_input_3`** — `object`

- Analyse the specific input "Policy and regulatory constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:2.contract_input_4`** — `object`

- Analyse the specific input "Channel capability" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/service-designer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/service-designer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/service-designer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/service-designer:2.irrelevant_detail`** — `object`

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
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Service Designer:** ISO 9241-210; service design practice; UK GDS service standard as a reference model. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-service-designer-3"></a>

## operational process implications

**At a glance**

- **Purpose:** Produce and govern the role deliverable: operational process implications.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `service-designer:3`.

**Required inputs:**

- User journeys and pain points
- Operational process reality
- Policy and regulatory constraints
- Channel capability

**Specification:** `kind/role/service-designer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: operational process implications.

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

**`role/service-designer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: operational process implications.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:3.receiving_acceptance`** — `array`

- For each receiving role (Product Designer; Process Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:3.delivery_verification`** — `array`

- For the specific output 'operational process implications', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: The blueprint covers back-stage capability and staff experience
- G6: a service design that assumes staff will absorb the complexity is returned as incomplete
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:3.contract_input_1`** — `object`

- Analyse the specific input "User journeys and pain points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:3.contract_input_2`** — `object`

- Analyse the specific input "Operational process reality" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:3.contract_input_3`** — `object`

- Analyse the specific input "Policy and regulatory constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:3.contract_input_4`** — `object`

- Analyse the specific input "Channel capability" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/service-designer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/service-designer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/service-designer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/service-designer:3.irrelevant_detail`** — `object`

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
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Service Designer:** ISO 9241-210; service design practice; UK GDS service standard as a reference model. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-service-designer-4"></a>

## service prototype and pilot results

**At a glance**

- **Purpose:** Produce and govern the role deliverable: service prototype and pilot results.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `service-designer:4`.

**Required inputs:**

- User journeys and pain points
- Operational process reality
- Policy and regulatory constraints
- Channel capability

**Specification:** `kind/role/service-designer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: service prototype and pilot results.

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

**`role/service-designer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: service prototype and pilot results.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:4.receiving_acceptance`** — `array`

- For each receiving role (Product Designer; Process Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:4.delivery_verification`** — `array`

- For the specific output 'service prototype and pilot results', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: The blueprint covers back-stage capability and staff experience
- G6: a service design that assumes staff will absorb the complexity is returned as incomplete
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:4.contract_input_1`** — `object`

- Analyse the specific input "User journeys and pain points" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:4.contract_input_2`** — `object`

- Analyse the specific input "Operational process reality" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:4.contract_input_3`** — `object`

- Analyse the specific input "Policy and regulatory constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:4.contract_input_4`** — `object`

- Analyse the specific input "Channel capability" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/service-designer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/service-designer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/service-designer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/service-designer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/service-designer:4.irrelevant_detail`** — `object`

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

- **Service Designer:** ISO 9241-210; service design practice; UK GDS service standard as a reference model. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
