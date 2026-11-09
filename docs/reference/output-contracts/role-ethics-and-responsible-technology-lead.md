<!-- JAI:OUTPUT-CONTRACTS:START -->
# Ethics and Responsible Technology Lead: output contracts

Make sure the organisation considers the harm its technology can do, before it does it

[Full catalogue](index.md)

<a id="output-ethics-and-responsible-technology-lead-1"></a>

## Ethical review process and criteria

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Ethical review process and criteria.
- **Mandatory examples:** Define test levels, techniques, environments, representative data and responsibilities. Define traceable entry/exit criteria, coverage measurement and defect disposition rules. Define risk-based test objectives, quality targets, scope and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `ethics-and-responsible-technology-lead:1`.

**Required inputs:**

- Initiative and product proposals
- Stakeholder and affected group input
- Legal and regulatory position
- Incident and complaint patterns

**Specification:** `kind/role/ethics-and-responsible-technology-lead:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Ethical review process and criteria.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/test-strategy`](spec-type-test-strategy.md)
- [`domain/testing`](spec-domain-testing.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `test-specification`.

Risk-based test specification with cases/techniques, expected outcomes, environments and entry/exit criteria.

**Evidence accompanying the work product:**

- requirement/risk-to-case coverage
- data/sample rationale and untested risks

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/ethics-and-responsible-technology-lead:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Ethical review process and criteria.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:1.receiving_acceptance`** — `array`

- For each receiving role (Product Manager; AI Governance Officer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:1.delivery_verification`** — `array`

- For the specific output 'Ethical review process and criteria', provide verifiable evidence satisfying: Identify product/build scope, critical requirements, quality risks, excluded risks and the confidence the selected tests can and cannot provide. Map risks to levels, techniques and responsibilities; specify environment, representative data, dependencies and expected evidence. Define measurable entry/exit criteria, coverage interpretation, triage/retest rules and treatment of blocked or unexecuted cases. Required delivery form: Risk-based test specification with cases/techniques, expected outcomes, environments and entry/exit criteria.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every policy statement has a named owner, an effective date and a review date.
- G2: Exceptions are time-bound, risk-assessed, approved at the correct authority level and tracked to expiry.
- G3: Reported position is based on independent evidence, not self-assessment alone.
- G4: Any breach of tolerance triggers a defined action, not merely a note in the minutes.
- G5: The role has an escalation path to the board that cannot be blocked by the business owner of the initiative under review
- G6: an ethics function that can be overruled quietly is decorative
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:1.contract_input_1`** — `object`

- Analyse the specific input "Initiative and product proposals" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:1.contract_input_2`** — `object`

- Analyse the specific input "Stakeholder and affected group input" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:1.contract_input_3`** — `object`

- Analyse the specific input "Legal and regulatory position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:1.contract_input_4`** — `object`

- Analyse the specific input "Incident and complaint patterns" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/ethics-and-responsible-technology-lead:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/ethics-and-responsible-technology-lead:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/ethics-and-responsible-technology-lead:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/ethics-and-responsible-technology-lead:1.irrelevant_detail`** — `object`

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
- **[ACM Artifact Review and Badging policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current)** — Artifact availability, evaluation and reproducibility terminology; informative evidence-pack practice, not proof that an experiment is scientifically sufficient. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Ethics and Responsible Technology Lead:** IEEE 7000 series; ISO/IEC 42001 for AI; UNGP business and human rights; internal ethics policy. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-ethics-and-responsible-technology-lead-2"></a>

## impact assessments for high-risk initiatives

**At a glance**

- **Purpose:** Produce and govern the role deliverable: impact assessments for high-risk initiatives.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `ethics-and-responsible-technology-lead:2`.

**Required inputs:**

- Initiative and product proposals
- Stakeholder and affected group input
- Legal and regulatory position
- Incident and complaint patterns

**Specification:** `kind/role/ethics-and-responsible-technology-lead:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: impact assessments for high-risk initiatives.

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

**`role/ethics-and-responsible-technology-lead:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: impact assessments for high-risk initiatives.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:2.receiving_acceptance`** — `array`

- For each receiving role (Product Manager; AI Governance Officer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:2.delivery_verification`** — `array`

- For the specific output 'impact assessments for high-risk initiatives', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Existing source requirement: Criteria were fixed before evidence collection and the method is reproducible. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every policy statement has a named owner, an effective date and a review date.
- G2: Exceptions are time-bound, risk-assessed, approved at the correct authority level and tracked to expiry.
- G3: Reported position is based on independent evidence, not self-assessment alone.
- G4: Any breach of tolerance triggers a defined action, not merely a note in the minutes.
- G5: The role has an escalation path to the board that cannot be blocked by the business owner of the initiative under review
- G6: an ethics function that can be overruled quietly is decorative
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:2.contract_input_1`** — `object`

- Analyse the specific input "Initiative and product proposals" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:2.contract_input_2`** — `object`

- Analyse the specific input "Stakeholder and affected group input" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:2.contract_input_3`** — `object`

- Analyse the specific input "Legal and regulatory position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:2.contract_input_4`** — `object`

- Analyse the specific input "Incident and complaint patterns" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/ethics-and-responsible-technology-lead:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/ethics-and-responsible-technology-lead:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/ethics-and-responsible-technology-lead:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/ethics-and-responsible-technology-lead:2.irrelevant_detail`** — `object`

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
- **[ACM Artifact Review and Badging policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current)** — Artifact availability, evaluation and reproducibility terminology; informative evidence-pack practice, not proof that an experiment is scientifically sufficient. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Ethics and Responsible Technology Lead:** IEEE 7000 series; ISO/IEC 42001 for AI; UNGP business and human rights; internal ethics policy. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-ethics-and-responsible-technology-lead-3"></a>

## responsible technology principles

**At a glance**

- **Purpose:** Produce and govern the role deliverable: responsible technology principles.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `ethics-and-responsible-technology-lead:3`.

**Required inputs:**

- Initiative and product proposals
- Stakeholder and affected group input
- Legal and regulatory position
- Incident and complaint patterns

**Specification:** `kind/role/ethics-and-responsible-technology-lead:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: responsible technology principles.

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

**`role/ethics-and-responsible-technology-lead:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: responsible technology principles.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:3.receiving_acceptance`** — `array`

- For each receiving role (Product Manager; AI Governance Officer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:3.delivery_verification`** — `array`

- For the specific output 'responsible technology principles', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every policy statement has a named owner, an effective date and a review date.
- G2: Exceptions are time-bound, risk-assessed, approved at the correct authority level and tracked to expiry.
- G3: Reported position is based on independent evidence, not self-assessment alone.
- G4: Any breach of tolerance triggers a defined action, not merely a note in the minutes.
- G5: The role has an escalation path to the board that cannot be blocked by the business owner of the initiative under review
- G6: an ethics function that can be overruled quietly is decorative
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:3.contract_input_1`** — `object`

- Analyse the specific input "Initiative and product proposals" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:3.contract_input_2`** — `object`

- Analyse the specific input "Stakeholder and affected group input" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:3.contract_input_3`** — `object`

- Analyse the specific input "Legal and regulatory position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:3.contract_input_4`** — `object`

- Analyse the specific input "Incident and complaint patterns" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/ethics-and-responsible-technology-lead:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/ethics-and-responsible-technology-lead:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/ethics-and-responsible-technology-lead:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/ethics-and-responsible-technology-lead:3.irrelevant_detail`** — `object`

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
- **[ACM Artifact Review and Badging policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current)** — Artifact availability, evaluation and reproducibility terminology; informative evidence-pack practice, not proof that an experiment is scientifically sufficient. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Ethics and Responsible Technology Lead:** IEEE 7000 series; ISO/IEC 42001 for AI; UNGP business and human rights; internal ethics policy. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-ethics-and-responsible-technology-lead-4"></a>

## escalation and stop recommendations

**At a glance**

- **Purpose:** Produce and govern the role deliverable: escalation and stop recommendations.
- **Mandatory examples:** Identify the specific choice, accountable authority and decision deadline. Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation. Compare viable options including the do-nothing baseline against common criteria.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `ethics-and-responsible-technology-lead:4`.

**Required inputs:**

- Initiative and product proposals
- Stakeholder and affected group input
- Legal and regulatory position
- Incident and complaint patterns

**Specification:** `kind/role/ethics-and-responsible-technology-lead:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: escalation and stop recommendations.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/decision-paper`](spec-type-decision-paper.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `decision-paper`.

Bounded decision paper with consistent option comparison and a clear authority/decision request.

**Evidence accompanying the work product:**

- baseline and feasible alternatives
- cost/benefit/uncertainty and consequences

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/ethics-and-responsible-technology-lead:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: escalation and stop recommendations.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:4.receiving_acceptance`** — `array`

- For each receiving role (Product Manager; AI Governance Officer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:4.delivery_verification`** — `array`

- For the specific output 'escalation and stop recommendations', provide verifiable evidence satisfying: Separate the requested decision from information for noting; state decision scope, eligible authority, deadline and consequences of deferral. List feasible options with consistent evaluation criteria, evidence, costs, benefits and constraints; justify any unavailable baseline. State recommendation, implementation dependencies, uncertainty and residual exposure; show which assumptions would change the preferred option. Required delivery form: Bounded decision paper with consistent option comparison and a clear authority/decision request.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every policy statement has a named owner, an effective date and a review date.
- G2: Exceptions are time-bound, risk-assessed, approved at the correct authority level and tracked to expiry.
- G3: Reported position is based on independent evidence, not self-assessment alone.
- G4: Any breach of tolerance triggers a defined action, not merely a note in the minutes.
- G5: The role has an escalation path to the board that cannot be blocked by the business owner of the initiative under review
- G6: an ethics function that can be overruled quietly is decorative
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:4.contract_input_1`** — `object`

- Analyse the specific input "Initiative and product proposals" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:4.contract_input_2`** — `object`

- Analyse the specific input "Stakeholder and affected group input" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:4.contract_input_3`** — `object`

- Analyse the specific input "Legal and regulatory position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:4.contract_input_4`** — `object`

- Analyse the specific input "Incident and complaint patterns" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/ethics-and-responsible-technology-lead:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/ethics-and-responsible-technology-lead:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/ethics-and-responsible-technology-lead:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/ethics-and-responsible-technology-lead:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/ethics-and-responsible-technology-lead:4.irrelevant_detail`** — `object`

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
- **[ACM Artifact Review and Badging policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current)** — Artifact availability, evaluation and reproducibility terminology; informative evidence-pack practice, not proof that an experiment is scientifically sufficient. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Ethics and Responsible Technology Lead:** IEEE 7000 series; ISO/IEC 42001 for AI; UNGP business and human rights; internal ethics policy. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
