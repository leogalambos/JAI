<!-- JAI:OUTPUT-CONTRACTS:START -->
# Systems Engineer (INCOSE): output contracts

Engineer the whole system across hardware, software, people and process so that it meets its purpose

[Full catalogue](index.md)

<a id="output-systems-engineer-incose-1"></a>

## System requirements specification

**At a glance**

- **Purpose:** Produce and govern the role deliverable: System requirements specification.
- **Mandatory examples:** Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `systems-engineer-incose:1`.

**Required inputs:**

- Stakeholder needs and operational concept
- Constraints including safety and certification
- Subsystem capabilities
- Risk analysis

**Specification:** `kind/role/systems-engineer-incose:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: System requirements specification.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/requirements-specification`](spec-family-requirements-specification.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/systems-engineer-incose:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: System requirements specification.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:1.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Embedded Firmware Engineer; Test Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:1.delivery_verification`** — `array`

- For the specific output 'System requirements specification', provide verifiable evidence satisfying: Every requirement is atomic, testable and traced to a source and a priority. Required delivery form: Versioned specification with numbered, traceable requirements.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Every requirement has a verification method assigned (test, analysis, inspection, demonstration) at the time it is written, not at the end of the programme
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:1.contract_input_1`** — `object`

- Analyse the specific input "Stakeholder needs and operational concept" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:1.contract_input_2`** — `object`

- Analyse the specific input "Constraints including safety and certification" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:1.contract_input_3`** — `object`

- Analyse the specific input "Subsystem capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:1.contract_input_4`** — `object`

- Analyse the specific input "Risk analysis" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/systems-engineer-incose:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/systems-engineer-incose:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/systems-engineer-incose:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/systems-engineer-incose:1.irrelevant_detail`** — `object`

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

### Role framework context

- **Systems Engineer (INCOSE):** INCOSE Systems Engineering Handbook; ISO/IEC/IEEE 15288; ISO/IEC/IEEE 29148. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-systems-engineer-incose-2"></a>

## system architecture and interface definitions

**At a glance**

- **Purpose:** Produce and govern the role deliverable: system architecture and interface definitions.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `systems-engineer-incose:2`.

**Required inputs:**

- Stakeholder needs and operational concept
- Constraints including safety and certification
- Subsystem capabilities
- Risk analysis

**Specification:** `kind/role/systems-engineer-incose:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: system architecture and interface definitions.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/model`](spec-type-model.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/systems-engineer-incose:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: system architecture and interface definitions.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:2.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Embedded Firmware Engineer; Test Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:2.delivery_verification`** — `array`

- For the specific output 'system architecture and interface definitions', provide verifiable evidence satisfying: Every element traces to a driver or a quality-attribute target; no orphan elements. Required delivery form: Model in the EA tool plus a published view set.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Every requirement has a verification method assigned (test, analysis, inspection, demonstration) at the time it is written, not at the end of the programme
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:2.contract_input_1`** — `object`

- Analyse the specific input "Stakeholder needs and operational concept" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:2.contract_input_2`** — `object`

- Analyse the specific input "Constraints including safety and certification" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:2.contract_input_3`** — `object`

- Analyse the specific input "Subsystem capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:2.contract_input_4`** — `object`

- Analyse the specific input "Risk analysis" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/systems-engineer-incose:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/systems-engineer-incose:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/systems-engineer-incose:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/systems-engineer-incose:2.irrelevant_detail`** — `object`

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

### Role framework context

- **Systems Engineer (INCOSE):** INCOSE Systems Engineering Handbook; ISO/IEC/IEEE 15288; ISO/IEC/IEEE 29148. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-systems-engineer-incose-3"></a>

## verification and validation plan

**At a glance**

- **Purpose:** Produce and govern the role deliverable: verification and validation plan.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `systems-engineer-incose:3`.

**Required inputs:**

- Stakeholder needs and operational concept
- Constraints including safety and certification
- Subsystem capabilities
- Risk analysis

**Specification:** `kind/role/systems-engineer-incose:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: verification and validation plan.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/roadmap`](spec-type-roadmap.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/systems-engineer-incose:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: verification and validation plan.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:3.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Embedded Firmware Engineer; Test Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:3.delivery_verification`** — `array`

- For the specific output 'verification and validation plan', provide verifiable evidence satisfying: Every milestone has an acceptance test and a named accountable owner. Required delivery form: Document with milestones, owners, dependencies and assumptions.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Every requirement has a verification method assigned (test, analysis, inspection, demonstration) at the time it is written, not at the end of the programme
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:3.contract_input_1`** — `object`

- Analyse the specific input "Stakeholder needs and operational concept" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:3.contract_input_2`** — `object`

- Analyse the specific input "Constraints including safety and certification" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:3.contract_input_3`** — `object`

- Analyse the specific input "Subsystem capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:3.contract_input_4`** — `object`

- Analyse the specific input "Risk analysis" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/systems-engineer-incose:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/systems-engineer-incose:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/systems-engineer-incose:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/systems-engineer-incose:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/systems-engineer-incose:3.irrelevant_detail`** — `object`

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

### Role framework context

- **Systems Engineer (INCOSE):** INCOSE Systems Engineering Handbook; ISO/IEC/IEEE 15288; ISO/IEC/IEEE 29148. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-systems-engineer-incose-4"></a>

## trade study and decision records

**At a glance**

- **Purpose:** Produce and govern the role deliverable: trade study and decision records.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `systems-engineer-incose:4`.

**Required inputs:**

- Stakeholder needs and operational concept
- Constraints including safety and certification
- Subsystem capabilities
- Risk analysis

**Specification:** `kind/role/systems-engineer-incose:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: trade study and decision records.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/systems-engineer-incose:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: trade study and decision records.

**`role/systems-engineer-incose:4.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Embedded Firmware Engineer; Test Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/systems-engineer-incose:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/systems-engineer-incose:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/systems-engineer-incose:4.delivery_verification`** — `array`

- For the specific output 'trade study and decision records', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/systems-engineer-incose:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every quality attribute has a target number and a way of measuring it before design starts.
- G2: Every significant decision has an ADR with an explicit consequences section, including the negative ones.
- G3: The design names its failure modes and its blast radius, not just its happy path.
- G4: Deviations accepted at build time are recorded as debt with an owner and a repayment trigger.
- G5: Every requirement has a verification method assigned (test, analysis, inspection, demonstration) at the time it is written, not at the end of the programme

**`role/systems-engineer-incose:4.contract_input_1`** — `object`

- Analyse the specific input "Stakeholder needs and operational concept" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/systems-engineer-incose:4.contract_input_2`** — `object`

- Analyse the specific input "Constraints including safety and certification" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/systems-engineer-incose:4.contract_input_3`** — `object`

- Analyse the specific input "Subsystem capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/systems-engineer-incose:4.contract_input_4`** — `object`

- Analyse the specific input "Risk analysis" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/systems-engineer-incose:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/systems-engineer-incose:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/systems-engineer-incose:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/systems-engineer-incose:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/systems-engineer-incose:4.irrelevant_detail`** — `object`

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

### Role framework context

- **Systems Engineer (INCOSE):** INCOSE Systems Engineering Handbook; ISO/IEC/IEEE 15288; ISO/IEC/IEEE 29148. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
