<!-- JAI:OUTPUT-CONTRACTS:START -->
# Codebase Reviewer: output contracts

Audit an existing codebase end to end and report, in priority order, what will actually hurt — without changing a line

[Full catalogue](index.md)

<a id="output-codebase-reviewer-1"></a>

## Codebase review report with prioritised findings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Codebase review report with prioritised findings.
- **Mandatory examples:** Identify the specific choice, accountable authority and decision deadline. Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation. Compare viable options including the do-nothing baseline against common criteria.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `codebase-reviewer:1`.

**Required inputs:**

- Repository access at a named commit
- Review criteria and target quality attributes
- Change and defect history
- Runtime and incident evidence

**Specification:** `kind/role/codebase-reviewer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Codebase review report with prioritised findings.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/decision-paper`](spec-type-decision-paper.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/codebase-reviewer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Codebase review report with prioritised findings.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:1.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Technical Lead; Application Security Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:1.delivery_verification`** — `array`

- For the specific output 'Codebase review report with prioritised findings', provide verifiable evidence satisfying: Conclusions are traceable to dated evidence; opinion is visibly separated from fact. Required delivery form: Structured document with executive summary and evidence annex.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Assessment criteria are fixed and documented before evidence collection begins.
- G2: Every finding is supported by retained, dated, attributable evidence.
- G3: The assessor is independent of the activity being assessed; any conflict is declared and documented.
- G4: Management responses record an owner, a date and an accepted residual risk for every finding.
- G5: Every finding cites a file, a line range and either a reproduction or a measurement — a finding that cannot be located in the code is an opinion and is labelled as one
- G6: Review criteria, scope and sampling approach are fixed and recorded before any code is read, so the conclusions cannot be reverse-engineered from whatever was noticed first
- G7: Findings are rated by the cost of leaving them, not by how easy they were to spot
- G8: The reviewer does not remediate what they found
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:1.contract_input_1`** — `object`

- Analyse the specific input "Repository access at a named commit" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:1.contract_input_2`** — `object`

- Analyse the specific input "Review criteria and target quality attributes" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:1.contract_input_3`** — `object`

- Analyse the specific input "Change and defect history" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:1.contract_input_4`** — `object`

- Analyse the specific input "Runtime and incident evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/codebase-reviewer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/codebase-reviewer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/codebase-reviewer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/codebase-reviewer:1.irrelevant_detail`** — `object`

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
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Codebase Reviewer:** ISO/IEC 25010 product quality; ISO/IEC 5055 code quality measures; OWASP ASVS; SWEBOK v4. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-codebase-reviewer-2"></a>

## architecture conformance and coupling analysis

**At a glance**

- **Purpose:** Produce and govern the role deliverable: architecture conformance and coupling analysis.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `codebase-reviewer:2`.

**Required inputs:**

- Repository access at a named commit
- Review criteria and target quality attributes
- Change and defect history
- Runtime and incident evidence

**Specification:** `kind/role/codebase-reviewer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: architecture conformance and coupling analysis.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/model`](spec-type-model.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/codebase-reviewer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: architecture conformance and coupling analysis.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:2.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Technical Lead; Application Security Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:2.delivery_verification`** — `array`

- For the specific output 'architecture conformance and coupling analysis', provide verifiable evidence satisfying: Every element traces to a driver or a quality-attribute target; no orphan elements. Required delivery form: Model in the EA tool plus a published view set.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Assessment criteria are fixed and documented before evidence collection begins.
- G2: Every finding is supported by retained, dated, attributable evidence.
- G3: The assessor is independent of the activity being assessed; any conflict is declared and documented.
- G4: Management responses record an owner, a date and an accepted residual risk for every finding.
- G5: Every finding cites a file, a line range and either a reproduction or a measurement — a finding that cannot be located in the code is an opinion and is labelled as one
- G6: Review criteria, scope and sampling approach are fixed and recorded before any code is read, so the conclusions cannot be reverse-engineered from whatever was noticed first
- G7: Findings are rated by the cost of leaving them, not by how easy they were to spot
- G8: The reviewer does not remediate what they found
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:2.contract_input_1`** — `object`

- Analyse the specific input "Repository access at a named commit" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:2.contract_input_2`** — `object`

- Analyse the specific input "Review criteria and target quality attributes" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:2.contract_input_3`** — `object`

- Analyse the specific input "Change and defect history" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:2.contract_input_4`** — `object`

- Analyse the specific input "Runtime and incident evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/codebase-reviewer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/codebase-reviewer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/codebase-reviewer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/codebase-reviewer:2.irrelevant_detail`** — `object`

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

- **Codebase Reviewer:** ISO/IEC 25010 product quality; ISO/IEC 5055 code quality measures; OWASP ASVS; SWEBOK v4. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-codebase-reviewer-3"></a>

## test coverage and risk gap assessment

**At a glance**

- **Purpose:** Produce and govern the role deliverable: test coverage and risk gap assessment.
- **Mandatory examples:** Identify the specific choice, accountable authority and decision deadline. Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation. Compare viable options including the do-nothing baseline against common criteria.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `codebase-reviewer:3`.

**Required inputs:**

- Repository access at a named commit
- Review criteria and target quality attributes
- Change and defect history
- Runtime and incident evidence

**Specification:** `kind/role/codebase-reviewer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: test coverage and risk gap assessment.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/decision-paper`](spec-type-decision-paper.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/codebase-reviewer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: test coverage and risk gap assessment.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:3.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Technical Lead; Application Security Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:3.delivery_verification`** — `array`

- For the specific output 'test coverage and risk gap assessment', provide verifiable evidence satisfying: Criteria were fixed before evidence collection and the method is reproducible. Required delivery form: Structured assessment document with scoring method stated.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Assessment criteria are fixed and documented before evidence collection begins.
- G2: Every finding is supported by retained, dated, attributable evidence.
- G3: The assessor is independent of the activity being assessed; any conflict is declared and documented.
- G4: Management responses record an owner, a date and an accepted residual risk for every finding.
- G5: Every finding cites a file, a line range and either a reproduction or a measurement — a finding that cannot be located in the code is an opinion and is labelled as one
- G6: Review criteria, scope and sampling approach are fixed and recorded before any code is read, so the conclusions cannot be reverse-engineered from whatever was noticed first
- G7: Findings are rated by the cost of leaving them, not by how easy they were to spot
- G8: The reviewer does not remediate what they found
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:3.contract_input_1`** — `object`

- Analyse the specific input "Repository access at a named commit" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:3.contract_input_2`** — `object`

- Analyse the specific input "Review criteria and target quality attributes" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:3.contract_input_3`** — `object`

- Analyse the specific input "Change and defect history" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:3.contract_input_4`** — `object`

- Analyse the specific input "Runtime and incident evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/codebase-reviewer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/codebase-reviewer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/codebase-reviewer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/codebase-reviewer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/codebase-reviewer:3.irrelevant_detail`** — `object`

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
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Codebase Reviewer:** ISO/IEC 25010 product quality; ISO/IEC 5055 code quality measures; OWASP ASVS; SWEBOK v4. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-codebase-reviewer-4"></a>

## dependency and supply chain exposure register

**At a glance**

- **Purpose:** Produce and govern the role deliverable: dependency and supply chain exposure register.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `codebase-reviewer:4`.

**Required inputs:**

- Repository access at a named commit
- Review criteria and target quality attributes
- Change and defect history
- Runtime and incident evidence

**Specification:** `kind/role/codebase-reviewer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: dependency and supply chain exposure register.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/codebase-reviewer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: dependency and supply chain exposure register.

**`role/codebase-reviewer:4.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Technical Lead; Application Security Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/codebase-reviewer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/codebase-reviewer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/codebase-reviewer:4.delivery_verification`** — `array`

- For the specific output 'dependency and supply chain exposure register', provide verifiable evidence satisfying: Every row has an owner, a date, a status and a next action. Required delivery form: Structured table in the system of record (CSV/tool export).

**`role/codebase-reviewer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Assessment criteria are fixed and documented before evidence collection begins.
- G2: Every finding is supported by retained, dated, attributable evidence.
- G3: The assessor is independent of the activity being assessed; any conflict is declared and documented.
- G4: Management responses record an owner, a date and an accepted residual risk for every finding.
- G5: Every finding cites a file, a line range and either a reproduction or a measurement — a finding that cannot be located in the code is an opinion and is labelled as one
- G6: Review criteria, scope and sampling approach are fixed and recorded before any code is read, so the conclusions cannot be reverse-engineered from whatever was noticed first
- G7: Findings are rated by the cost of leaving them, not by how easy they were to spot
- G8: The reviewer does not remediate what they found

**`role/codebase-reviewer:4.contract_input_1`** — `object`

- Analyse the specific input "Repository access at a named commit" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/codebase-reviewer:4.contract_input_2`** — `object`

- Analyse the specific input "Review criteria and target quality attributes" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/codebase-reviewer:4.contract_input_3`** — `object`

- Analyse the specific input "Change and defect history" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/codebase-reviewer:4.contract_input_4`** — `object`

- Analyse the specific input "Runtime and incident evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/codebase-reviewer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/codebase-reviewer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/codebase-reviewer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/codebase-reviewer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/codebase-reviewer:4.irrelevant_detail`** — `object`

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

### Role framework context

- **Codebase Reviewer:** ISO/IEC 25010 product quality; ISO/IEC 5055 code quality measures; OWASP ASVS; SWEBOK v4. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
