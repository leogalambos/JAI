<!-- JAI:OUTPUT-CONTRACTS:START -->
# SAFe System Architect: output contracts

Maintain the architectural runway so that teams can deliver upcoming features without stalling

[Full catalogue](index.md)

<a id="output-safe-system-architect-1"></a>

## Architectural runway plan

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Architectural runway plan.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `safe-system-architect:1`.

**Required inputs:**

- Programme backlog
- Current system constraints
- Non-functional targets
- Technical debt position

**Specification:** `kind/role/safe-system-architect:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Architectural runway plan.

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

**`role/safe-system-architect:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Architectural runway plan.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:1.receiving_acceptance`** — `array`

- For each receiving role (Technical Lead; Platform Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:1.delivery_verification`** — `array`

- For the specific output 'Architectural runway plan', provide verifiable evidence satisfying: State business outcomes, current/target baseline, planning horizons, sponsors and material planning assumptions. For each increment, identify deliverables, owner, indicative resource/funding requirement, milestone and measurable completion outcome. Identify dependencies and critical sequence, decision dates, constraints and alternative paths; distinguish committed work from tentative options. Existing source requirement: Every milestone has an acceptance test and a named accountable owner. Required delivery form: Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Every enabler in the backlog names the feature it unblocks and the date it must be ready
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:1.contract_input_1`** — `object`

- Analyse the specific input "Programme backlog" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:1.contract_input_2`** — `object`

- Analyse the specific input "Current system constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:1.contract_input_3`** — `object`

- Analyse the specific input "Non-functional targets" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:1.contract_input_4`** — `object`

- Analyse the specific input "Technical debt position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/safe-system-architect:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/safe-system-architect:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/safe-system-architect:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/safe-system-architect:1.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **SAFe System Architect:** SAFe architecture guidance; ISO/IEC 25010; ATAM scenario evaluation. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-safe-system-architect-2"></a>

## enabler backlog

**At a glance**

- **Purpose:** Produce and govern the role deliverable: enabler backlog.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `safe-system-architect:2`.

**Required inputs:**

- Programme backlog
- Current system constraints
- Non-functional targets
- Technical debt position

**Specification:** `kind/role/safe-system-architect:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: enabler backlog.

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

**`role/safe-system-architect:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: enabler backlog.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:2.receiving_acceptance`** — `array`

- For each receiving role (Technical Lead; Platform Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:2.delivery_verification`** — `array`

- For the specific output 'enabler backlog', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Existing source requirement: Every item has acceptance criteria, a priority rationale and an estimate or an explicit 'unsized'. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Every enabler in the backlog names the feature it unblocks and the date it must be ready
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:2.contract_input_1`** — `object`

- Analyse the specific input "Programme backlog" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:2.contract_input_2`** — `object`

- Analyse the specific input "Current system constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:2.contract_input_3`** — `object`

- Analyse the specific input "Non-functional targets" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:2.contract_input_4`** — `object`

- Analyse the specific input "Technical debt position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/safe-system-architect:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/safe-system-architect:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/safe-system-architect:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/safe-system-architect:2.irrelevant_detail`** — `object`

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
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **SAFe System Architect:** SAFe architecture guidance; ISO/IEC 25010; ATAM scenario evaluation. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-safe-system-architect-3"></a>

## non-functional requirement set

**At a glance**

- **Purpose:** Produce and govern the role deliverable: non-functional requirement set.
- **Mandatory examples:** Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `safe-system-architect:3`.

**Required inputs:**

- Programme backlog
- Current system constraints
- Non-functional targets
- Technical debt position

**Specification:** `kind/role/safe-system-architect:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: non-functional requirement set.

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

**`role/safe-system-architect:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: non-functional requirement set.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:3.receiving_acceptance`** — `array`

- For each receiving role (Technical Lead; Platform Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:3.delivery_verification`** — `array`

- For the specific output 'non-functional requirement set', provide verifiable evidence satisfying: Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. Required delivery form: Uniquely identified verifiable requirements with rationale, priority, sources and acceptance conditions.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Every enabler in the backlog names the feature it unblocks and the date it must be ready
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:3.contract_input_1`** — `object`

- Analyse the specific input "Programme backlog" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:3.contract_input_2`** — `object`

- Analyse the specific input "Current system constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:3.contract_input_3`** — `object`

- Analyse the specific input "Non-functional targets" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:3.contract_input_4`** — `object`

- Analyse the specific input "Technical debt position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/safe-system-architect:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/safe-system-architect:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/safe-system-architect:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/safe-system-architect:3.irrelevant_detail`** — `object`

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
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **SAFe System Architect:** SAFe architecture guidance; ISO/IEC 25010; ATAM scenario evaluation. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-safe-system-architect-4"></a>

## system-level interface definitions

**At a glance**

- **Purpose:** Produce and govern the role deliverable: system-level interface definitions.
- **Mandatory examples:** Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `safe-system-architect:4`.

**Required inputs:**

- Programme backlog
- Current system constraints
- Non-functional targets
- Technical debt position

**Specification:** `kind/role/safe-system-architect:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: system-level interface definitions.

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

**`role/safe-system-architect:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: system-level interface definitions.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:4.receiving_acceptance`** — `array`

- For each receiving role (Technical Lead; Platform Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:4.delivery_verification`** — `array`

- For the specific output 'system-level interface definitions', provide verifiable evidence satisfying: Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. Required delivery form: Uniquely identified verifiable requirements with rationale, priority, sources and acceptance conditions.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Every enabler in the backlog names the feature it unblocks and the date it must be ready
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:4.contract_input_1`** — `object`

- Analyse the specific input "Programme backlog" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:4.contract_input_2`** — `object`

- Analyse the specific input "Current system constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:4.contract_input_3`** — `object`

- Analyse the specific input "Non-functional targets" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:4.contract_input_4`** — `object`

- Analyse the specific input "Technical debt position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/safe-system-architect:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/safe-system-architect:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/safe-system-architect:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/safe-system-architect:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/safe-system-architect:4.irrelevant_detail`** — `object`

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
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **SAFe System Architect:** SAFe architecture guidance; ISO/IEC 25010; ATAM scenario evaluation. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
