<!-- JAI:OUTPUT-CONTRACTS:START -->
# Technical Lead: output contracts

Set and hold the technical direction inside one team, and keep its code and design healthy enough to change

[Full catalogue](index.md)

<a id="output-technical-lead-1"></a>

## Team technical design and ADRs

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Team technical design and ADRs.
- **Mandatory examples:** Describe rejected options, reversibility, debt and operational consequences. Record decision status, owner, date and architecture concern. Compare feasible alternatives against explicit drivers and constraints.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `technical-lead:1`.

**Required inputs:**

- Upcoming backlog
- Architecture constraints
- Production behaviour and incidents
- Team skill profile

**Specification:** `kind/role/technical-lead:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Team technical design and ADRs.

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

**`role/technical-lead:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Team technical design and ADRs.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:1.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Test Automation Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:1.delivery_verification`** — `array`

- For the specific output 'Team technical design and ADRs', provide verifiable evidence satisfying: Identify the architecture concern, constraints, scope and decision status. Compare feasible design alternatives and the rejected baseline against drivers. Record the selected design, decision owner and dated rationale. Existing source requirement: Context, options, decision, status and consequences (including negative) are all populated. Required delivery form: Versioned decision record with context, alternatives, consequences, status and supersession.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Technical debt taken deliberately is recorded with the trigger that will force its repayment, otherwise it is not a decision but an accident
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:1.contract_input_1`** — `object`

- Analyse the specific input "Upcoming backlog" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:1.contract_input_2`** — `object`

- Analyse the specific input "Architecture constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:1.contract_input_3`** — `object`

- Analyse the specific input "Production behaviour and incidents" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:1.contract_input_4`** — `object`

- Analyse the specific input "Team skill profile" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technical-lead:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technical-lead:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/technical-lead:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/technical-lead:1.irrelevant_detail`** — `object`

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
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Technical Lead:** SWEBOK v4; architecture decision records; team coding standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-technical-lead-2"></a>

## technical debt register

**At a glance**

- **Purpose:** Produce and govern the role deliverable: technical debt register.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `technical-lead:2`.

**Required inputs:**

- Upcoming backlog
- Architecture constraints
- Production behaviour and incidents
- Team skill profile

**Specification:** `kind/role/technical-lead:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: technical debt register.

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

**`role/technical-lead:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: technical debt register.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:2.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Test Automation Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:2.delivery_verification`** — `array`

- For the specific output 'technical debt register', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Existing source requirement: Every row has an owner, a date, a status and a next action. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Technical debt taken deliberately is recorded with the trigger that will force its repayment, otherwise it is not a decision but an accident
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:2.contract_input_1`** — `object`

- Analyse the specific input "Upcoming backlog" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:2.contract_input_2`** — `object`

- Analyse the specific input "Architecture constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:2.contract_input_3`** — `object`

- Analyse the specific input "Production behaviour and incidents" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:2.contract_input_4`** — `object`

- Analyse the specific input "Team skill profile" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technical-lead:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technical-lead:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/technical-lead:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/technical-lead:2.irrelevant_detail`** — `object`

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

- **Technical Lead:** SWEBOK v4; architecture decision records; team coding standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-technical-lead-3"></a>

## code and review standards

**At a glance**

- **Purpose:** Produce and govern the role deliverable: code and review standards.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `technical-lead:3`.

**Required inputs:**

- Upcoming backlog
- Architecture constraints
- Production behaviour and incidents
- Team skill profile

**Specification:** `kind/role/technical-lead:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: code and review standards.

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

**`role/technical-lead:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: code and review standards.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:3.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Test Automation Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:3.delivery_verification`** — `array`

- For the specific output 'code and review standards', provide verifiable evidence satisfying: State the exact subject, intended recipient/use, boundary, source versions and the concrete question the document answers. Provide subject-specific findings or instructions with supporting facts, assumptions, reasoning, limitations and traceable references; generic background alone is insufficient. State conclusions, decisions requested or actionable instructions, accountable recipients and completion/acceptance conditions; identify open issues explicitly. Existing source requirement: Requirements are specific, measurable and technology-explicit. Required delivery form: Purpose-specific professional document with source analysis, reasoning, conclusions and recipient actions.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Technical debt taken deliberately is recorded with the trigger that will force its repayment, otherwise it is not a decision but an accident
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:3.contract_input_1`** — `object`

- Analyse the specific input "Upcoming backlog" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:3.contract_input_2`** — `object`

- Analyse the specific input "Architecture constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:3.contract_input_3`** — `object`

- Analyse the specific input "Production behaviour and incidents" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:3.contract_input_4`** — `object`

- Analyse the specific input "Team skill profile" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technical-lead:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technical-lead:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/technical-lead:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/technical-lead:3.irrelevant_detail`** — `object`

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
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Technical Lead:** SWEBOK v4; architecture decision records; team coding standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-technical-lead-4"></a>

## technical breakdown of upcoming work

**At a glance**

- **Purpose:** Produce and govern the role deliverable: technical breakdown of upcoming work.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `technical-lead:4`.

**Required inputs:**

- Upcoming backlog
- Architecture constraints
- Production behaviour and incidents
- Team skill profile

**Specification:** `kind/role/technical-lead:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: technical breakdown of upcoming work.

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

**`role/technical-lead:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: technical breakdown of upcoming work.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:4.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Test Automation Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:4.delivery_verification`** — `array`

- For the specific output 'technical breakdown of upcoming work', provide verifiable evidence satisfying: State business outcomes, current/target baseline, planning horizons, sponsors and material planning assumptions. For each increment, identify deliverables, owner, indicative resource/funding requirement, milestone and measurable completion outcome. Identify dependencies and critical sequence, decision dates, constraints and alternative paths; distinguish committed work from tentative options. Required delivery form: Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Technical debt taken deliberately is recorded with the trigger that will force its repayment, otherwise it is not a decision but an accident
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:4.contract_input_1`** — `object`

- Analyse the specific input "Upcoming backlog" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:4.contract_input_2`** — `object`

- Analyse the specific input "Architecture constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:4.contract_input_3`** — `object`

- Analyse the specific input "Production behaviour and incidents" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:4.contract_input_4`** — `object`

- Analyse the specific input "Team skill profile" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technical-lead:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/technical-lead:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technical-lead:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/technical-lead:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/technical-lead:4.irrelevant_detail`** — `object`

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

- **Technical Lead:** SWEBOK v4; architecture decision records; team coding standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
