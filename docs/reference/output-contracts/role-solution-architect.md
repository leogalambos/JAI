<!-- JAI:OUTPUT-CONTRACTS:START -->
# Solution Architect: output contracts

Design one solution end to end so that it meets its requirements, fits the estate and can actually be built and run

[Full catalogue](index.md)

<a id="output-solution-architect-1"></a>

## Solution architecture document

**At a glance**

- **Purpose:** Accept the proposed solution design as the basis for detailed engineering.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include deeper calculations or technical detail only when linked to a reader need.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `solution-architect:1`.

**Required inputs:**

- Requirements baseline
- Enterprise standards and patterns
- Security requirements
- Operational constraints

**Specification:** `kind/hld`; **content version:** `1.2.0`.

Accept the proposed solution design as the basis for detailed engineering.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/model`](spec-type-model.md)

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

**`hld.solution_scope`** — `object`

- Define the proposed implementation boundary, use cases and external dependencies.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`hld.quality_requirements`** — `array`

- State measurable availability, performance, security and operational acceptance targets.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`hld.solution_components`** — `array`

- Describe component responsibilities, deployment topology and design rationale.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`hld.solution_interfaces`** — `array`

- Specify integration contracts, data flows, trust boundaries and failure behaviour.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`hld.delivery_strategy`** — `object`

- Describe deployment, migration, operability, rollback and design verification.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`hld.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify personal-data flows, lawful handling constraints, minimisation and review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`hld.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Trace each applicable regulatory obligation to scope, evidence and competent interpretation; exceptions cannot waive law.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`hld.technical_annex`** — `object`

- Include deeper calculations or technical detail only when linked to a reader need.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`hld.unsupported_material_claim`** — `object`

- Never state a material conclusion as established without evidence or explicit uncertainty.

### Content to omit unless justified

**`hld.irrelevant_detail`** — `object`

- Remove detail that does not support the stated purpose or a referenced annex.

**`hld.duplicate_claim`** — `object`

- Reference an existing claim instead of repeating it without new analytical value.

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
  },
  "pages": {
    "metric": "pages",
    "calibration_basis": "Modality-specific information coverage; numerical envelopes require approved enterprise calibration.",
    "minimum_is_quality_gate": false,
    "calibration_status": "synthetic-only",
    "allowance_rules": [
      "Document complexity and audience need; excess requires review, not automatic rejection."
    ],
    "annex_rules": [
      "Reference canonical detail rather than repeat it."
    ],
    "target": [
      10,
      30
    ],
    "soft_max": 40,
    "basis": "Indicative pilot intervals from approved implementation direction; assurance and handover use proposed evidence-pack intervals requiring calibration.",
    "exclude": [
      "controlled_annexes",
      "source_register"
    ],
    "target_is_informational": true
  }
}
```

### Professional sources and their limits

- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Solution Architect:** TOGAF 10; ISO/IEC 25010; ATAM scenario evaluation; C4 model. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-solution-architect-2"></a>

## interface and integration design

**At a glance**

- **Purpose:** Produce and govern the role deliverable: interface and integration design.
- **Mandatory examples:** Describe bounded component responsibilities and deployment topology. Map measurable quality requirements to design verification and acceptance. Define versioned interface inputs, outputs, trust boundaries and failure handling.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `solution-architect:2`.

**Required inputs:**

- Requirements baseline
- Enterprise standards and patterns
- Security requirements
- Operational constraints

**Specification:** `kind/role/solution-architect:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: interface and integration design.

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

**`role/solution-architect:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: interface and integration design.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:2.receiving_acceptance`** — `array`

- For each receiving role (Technical Lead; Software Engineer; Site Reliability Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:2.delivery_verification`** — `array`

- For the specific output 'interface and integration design', provide verifiable evidence satisfying: Define the proposed implementation boundary, use cases and external dependencies. State measurable availability, performance, security and operational acceptance targets. Describe component responsibilities, deployment topology and design rationale. Existing source requirement: Defines versioned schemas, producer/consumer obligations, trust boundaries, failure handling and compatibility checks. Required delivery form: Versioned solution design with component responsibilities, interfaces and measurable quality responses.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: The design has been reviewed by someone who will operate it, and its failure modes and blast radius are documented before build starts
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:2.contract_input_1`** — `object`

- Analyse the specific input "Requirements baseline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:2.contract_input_2`** — `object`

- Analyse the specific input "Enterprise standards and patterns" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:2.contract_input_3`** — `object`

- Analyse the specific input "Security requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:2.contract_input_4`** — `object`

- Analyse the specific input "Operational constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/solution-architect:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/solution-architect:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/solution-architect:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/solution-architect:2.irrelevant_detail`** — `object`

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

- **Solution Architect:** TOGAF 10; ISO/IEC 25010; ATAM scenario evaluation; C4 model. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-solution-architect-3"></a>

## non-functional requirement specification

**At a glance**

- **Purpose:** Produce and govern the role deliverable: non-functional requirement specification.
- **Mandatory examples:** Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `solution-architect:3`.

**Required inputs:**

- Requirements baseline
- Enterprise standards and patterns
- Security requirements
- Operational constraints

**Specification:** `kind/role/solution-architect:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: non-functional requirement specification.

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

**`role/solution-architect:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: non-functional requirement specification.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:3.receiving_acceptance`** — `array`

- For each receiving role (Technical Lead; Software Engineer; Site Reliability Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:3.delivery_verification`** — `array`

- For the specific output 'non-functional requirement specification', provide verifiable evidence satisfying: Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. Existing source requirement: Every requirement is atomic, testable and traced to a source and a priority. Required delivery form: Uniquely identified verifiable requirements with rationale, priority, sources and acceptance conditions.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: The design has been reviewed by someone who will operate it, and its failure modes and blast radius are documented before build starts
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:3.contract_input_1`** — `object`

- Analyse the specific input "Requirements baseline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:3.contract_input_2`** — `object`

- Analyse the specific input "Enterprise standards and patterns" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:3.contract_input_3`** — `object`

- Analyse the specific input "Security requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:3.contract_input_4`** — `object`

- Analyse the specific input "Operational constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/solution-architect:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/solution-architect:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/solution-architect:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/solution-architect:3.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Solution Architect:** TOGAF 10; ISO/IEC 25010; ATAM scenario evaluation; C4 model. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-solution-architect-4"></a>

## architecture decision records

**At a glance**

- **Purpose:** Produce and govern the role deliverable: architecture decision records.
- **Mandatory examples:** Describe rejected options, reversibility, debt and operational consequences. Record decision status, owner, date and architecture concern. Compare feasible alternatives against explicit drivers and constraints.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `solution-architect:4`.

**Required inputs:**

- Requirements baseline
- Enterprise standards and patterns
- Security requirements
- Operational constraints

**Specification:** `kind/role/solution-architect:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: architecture decision records.

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

**`role/solution-architect:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: architecture decision records.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:4.receiving_acceptance`** — `array`

- For each receiving role (Technical Lead; Software Engineer; Site Reliability Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:4.delivery_verification`** — `array`

- For the specific output 'architecture decision records', provide verifiable evidence satisfying: Identify the architecture concern, constraints, scope and decision status. Compare feasible design alternatives and the rejected baseline against drivers. Record the selected design, decision owner and dated rationale. Existing source requirement: Every element traces to a driver or a quality-attribute target; no orphan elements. Required delivery form: Versioned decision record with context, alternatives, consequences, status and supersession.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: The design has been reviewed by someone who will operate it, and its failure modes and blast radius are documented before build starts
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:4.contract_input_1`** — `object`

- Analyse the specific input "Requirements baseline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:4.contract_input_2`** — `object`

- Analyse the specific input "Enterprise standards and patterns" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:4.contract_input_3`** — `object`

- Analyse the specific input "Security requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:4.contract_input_4`** — `object`

- Analyse the specific input "Operational constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/solution-architect:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/solution-architect:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/solution-architect:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/solution-architect:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/solution-architect:4.irrelevant_detail`** — `object`

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

- **Solution Architect:** TOGAF 10; ISO/IEC 25010; ATAM scenario evaluation; C4 model. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
