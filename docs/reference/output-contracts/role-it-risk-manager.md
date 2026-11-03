<!-- JAI:OUTPUT-CONTRACTS:START -->
# IT Risk Manager: output contracts

Make technology risk visible, comparable and owned, so the organisation can decide rather than hope

[Full catalogue](index.md)

<a id="output-it-risk-manager-1"></a>

## Technology risk register with quantified exposure

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Technology risk register with quantified exposure.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `it-risk-manager:1`.

**Required inputs:**

- Threat and vulnerability data
- Control effectiveness
- Business impact analysis
- Appetite statement

**Specification:** `kind/role/it-risk-manager:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Technology risk register with quantified exposure.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/it-risk-manager:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Technology risk register with quantified exposure.

**`role/it-risk-manager:1.receiving_acceptance`** — `array`

- For each receiving role (Control Owner; GRC Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/it-risk-manager:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/it-risk-manager:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/it-risk-manager:1.delivery_verification`** — `array`

- For the specific output 'Technology risk register with quantified exposure', provide verifiable evidence satisfying: Every row has an owner, a date, a status and a next action. Required delivery form: Structured table in the system of record (CSV/tool export).

**`role/it-risk-manager:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Assessment criteria are fixed and documented before evidence collection begins.
- G2: Every finding is supported by retained, dated, attributable evidence.
- G3: The assessor is independent of the activity being assessed; any conflict is declared and documented.
- G4: Management responses record an owner, a date and an accepted residual risk for every finding.
- G5: Every risk has a named owner with authority over the resources needed to treat it
- G6: risks owned by a role that cannot act are escalated rather than recorded

**`role/it-risk-manager:1.contract_input_1`** — `object`

- Analyse the specific input "Threat and vulnerability data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/it-risk-manager:1.contract_input_2`** — `object`

- Analyse the specific input "Control effectiveness" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/it-risk-manager:1.contract_input_3`** — `object`

- Analyse the specific input "Business impact analysis" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/it-risk-manager:1.contract_input_4`** — `object`

- Analyse the specific input "Appetite statement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/it-risk-manager:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/it-risk-manager:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/it-risk-manager:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/it-risk-manager:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/it-risk-manager:1.irrelevant_detail`** — `object`

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

- **IT Risk Manager:** ISO 31000; NIST SP 800-30 and 800-37; COBIT 2019 APO12; FAIR for quantification. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-it-risk-manager-2"></a>

## risk assessments for changes and initiatives

**At a glance**

- **Purpose:** Select treatments and decide whether residual change risks are acceptable.
- **Mandatory examples:** Link assets, causes, events, consequences and inherent/residual ratings to evidence. Define scope, likelihood, impact scales and applicable risk appetite. Assign treatments, deadlines, risk owners and residual acceptance authority.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include deeper calculations or technical detail only when linked to a reader need.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `it-risk-manager:2`.

**Required inputs:**

- Threat and vulnerability data
- Control effectiveness
- Business impact analysis
- Appetite statement

**Specification:** `kind/risk-assessment`; **content version:** `1.2.0`.

Select treatments and decide whether residual change risks are acceptable.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/risk-assessment`](spec-type-risk-assessment.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`risk-assessment.assessment_scope`** — `object`

- Identify assets, business outcomes, boundaries and accountable risk owners.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`risk-assessment.scoring_method`** — `object`

- Define likelihood, impact, evaluation scales and the applicable risk appetite.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`risk-assessment.risk_scenarios`** — `array`

- Describe causes, events, consequences and the evidence behind each scenario.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`risk-assessment.risk_evaluation`** — `array`

- Link inherent and residual scores to scenarios, control effectiveness and uncertainty.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`risk-assessment.risk_treatment`** — `array`

- Assign response actions, owners, deadlines and residual-risk acceptance authority.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`risk-assessment.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify personal-data flows, lawful handling constraints, minimisation and review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`risk-assessment.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Trace each applicable regulatory obligation to scope, evidence and competent interpretation; exceptions cannot waive law.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`risk-assessment.technical_annex`** — `object`

- Include deeper calculations or technical detail only when linked to a reader need.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`risk-assessment.unsupported_material_claim`** — `object`

- Never state a material conclusion as established without evidence or explicit uncertainty.

### Content to omit unless justified

**`risk-assessment.irrelevant_detail`** — `object`

- Remove detail that does not support the stated purpose or a referenced annex.

**`risk-assessment.duplicate_claim`** — `object`

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
      4,
      12
    ],
    "soft_max": 16,
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

- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **IT Risk Manager:** ISO 31000; NIST SP 800-30 and 800-37; COBIT 2019 APO12; FAIR for quantification. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-it-risk-manager-3"></a>

## risk appetite monitoring

**At a glance**

- **Purpose:** Produce and govern the role deliverable: risk appetite monitoring.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `it-risk-manager:3`.

**Required inputs:**

- Threat and vulnerability data
- Control effectiveness
- Business impact analysis
- Appetite statement

**Specification:** `kind/role/it-risk-manager:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: risk appetite monitoring.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/it-risk-manager:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: risk appetite monitoring.

**`role/it-risk-manager:3.receiving_acceptance`** — `array`

- For each receiving role (Control Owner; GRC Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/it-risk-manager:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/it-risk-manager:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/it-risk-manager:3.delivery_verification`** — `array`

- For the specific output 'risk appetite monitoring', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/it-risk-manager:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Assessment criteria are fixed and documented before evidence collection begins.
- G2: Every finding is supported by retained, dated, attributable evidence.
- G3: The assessor is independent of the activity being assessed; any conflict is declared and documented.
- G4: Management responses record an owner, a date and an accepted residual risk for every finding.
- G5: Every risk has a named owner with authority over the resources needed to treat it
- G6: risks owned by a role that cannot act are escalated rather than recorded

**`role/it-risk-manager:3.contract_input_1`** — `object`

- Analyse the specific input "Threat and vulnerability data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/it-risk-manager:3.contract_input_2`** — `object`

- Analyse the specific input "Control effectiveness" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/it-risk-manager:3.contract_input_3`** — `object`

- Analyse the specific input "Business impact analysis" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/it-risk-manager:3.contract_input_4`** — `object`

- Analyse the specific input "Appetite statement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/it-risk-manager:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/it-risk-manager:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/it-risk-manager:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/it-risk-manager:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/it-risk-manager:3.irrelevant_detail`** — `object`

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

- **IT Risk Manager:** ISO 31000; NIST SP 800-30 and 800-37; COBIT 2019 APO12; FAIR for quantification. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-it-risk-manager-4"></a>

## treatment plans and acceptance records

**At a glance**

- **Purpose:** Produce and govern the role deliverable: treatment plans and acceptance records.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `it-risk-manager:4`.

**Required inputs:**

- Threat and vulnerability data
- Control effectiveness
- Business impact analysis
- Appetite statement

**Specification:** `kind/role/it-risk-manager:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: treatment plans and acceptance records.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/it-risk-manager:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: treatment plans and acceptance records.

**`role/it-risk-manager:4.receiving_acceptance`** — `array`

- For each receiving role (Control Owner; GRC Analyst), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/it-risk-manager:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/it-risk-manager:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/it-risk-manager:4.delivery_verification`** — `array`

- For the specific output 'treatment plans and acceptance records', provide verifiable evidence satisfying: Every milestone has an acceptance test and a named accountable owner. Required delivery form: Document with milestones, owners, dependencies and assumptions.

**`role/it-risk-manager:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Assessment criteria are fixed and documented before evidence collection begins.
- G2: Every finding is supported by retained, dated, attributable evidence.
- G3: The assessor is independent of the activity being assessed; any conflict is declared and documented.
- G4: Management responses record an owner, a date and an accepted residual risk for every finding.
- G5: Every risk has a named owner with authority over the resources needed to treat it
- G6: risks owned by a role that cannot act are escalated rather than recorded

**`role/it-risk-manager:4.contract_input_1`** — `object`

- Analyse the specific input "Threat and vulnerability data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/it-risk-manager:4.contract_input_2`** — `object`

- Analyse the specific input "Control effectiveness" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/it-risk-manager:4.contract_input_3`** — `object`

- Analyse the specific input "Business impact analysis" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/it-risk-manager:4.contract_input_4`** — `object`

- Analyse the specific input "Appetite statement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/it-risk-manager:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/it-risk-manager:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/it-risk-manager:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/it-risk-manager:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/it-risk-manager:4.irrelevant_detail`** — `object`

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

- **IT Risk Manager:** ISO 31000; NIST SP 800-30 and 800-37; COBIT 2019 APO12; FAIR for quantification. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
