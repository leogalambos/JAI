<!-- JAI:OUTPUT-CONTRACTS:START -->
# Technology Scout: output contracts

Watch what is emerging and tell the organisation what deserves attention, when

[Full catalogue](index.md)

<a id="output-technology-scout-1"></a>

## Technology radar with adopt/trial/assess/hold positions

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Technology radar with adopt/trial/assess/hold positions.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `technology-scout:1`.

**Required inputs:**

- Strategic priorities
- Market and vendor landscape
- Internal capability gaps
- Peer and sector practice

**Specification:** `kind/role/technology-scout:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Technology radar with adopt/trial/assess/hold positions.

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

**`role/technology-scout:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Technology radar with adopt/trial/assess/hold positions.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:1.receiving_acceptance`** — `array`

- For each receiving role (Enterprise Architect; Innovation Lead), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:1.delivery_verification`** — `array`

- For the specific output 'Technology radar with adopt/trial/assess/hold positions', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Success and failure criteria are written before the experiment runs.
- G2: Negative results are reported, not quietly abandoned.
- G3: Prototype code is labelled non-production and is never deployed to a production path without a rewrite decision.
- G4: Licensing, export-control, data-protection and ethical constraints are checked before using external data or models.
- G5: Every radar position states the evidence and the trigger that would move it
- G6: positions based only on vendor marketing are marked as unevidenced
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:1.contract_input_1`** — `object`

- Analyse the specific input "Strategic priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:1.contract_input_2`** — `object`

- Analyse the specific input "Market and vendor landscape" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:1.contract_input_3`** — `object`

- Analyse the specific input "Internal capability gaps" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:1.contract_input_4`** — `object`

- Analyse the specific input "Peer and sector practice" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technology-scout:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technology-scout:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/technology-scout:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/technology-scout:1.irrelevant_detail`** — `object`

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

- **Technology Scout:** technology radar practice; Gartner-style hype cycle positioning used critically; structured vendor evaluation. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-technology-scout-2"></a>

## vendor and ecosystem assessments

**At a glance**

- **Purpose:** Produce and govern the role deliverable: vendor and ecosystem assessments.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `technology-scout:2`.

**Required inputs:**

- Strategic priorities
- Market and vendor landscape
- Internal capability gaps
- Peer and sector practice

**Specification:** `kind/role/technology-scout:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: vendor and ecosystem assessments.

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

**`role/technology-scout:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: vendor and ecosystem assessments.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:2.receiving_acceptance`** — `array`

- For each receiving role (Enterprise Architect; Innovation Lead), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:2.delivery_verification`** — `array`

- For the specific output 'vendor and ecosystem assessments', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Existing source requirement: Criteria were fixed before evidence collection and the method is reproducible. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Success and failure criteria are written before the experiment runs.
- G2: Negative results are reported, not quietly abandoned.
- G3: Prototype code is labelled non-production and is never deployed to a production path without a rewrite decision.
- G4: Licensing, export-control, data-protection and ethical constraints are checked before using external data or models.
- G5: Every radar position states the evidence and the trigger that would move it
- G6: positions based only on vendor marketing are marked as unevidenced
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:2.contract_input_1`** — `object`

- Analyse the specific input "Strategic priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:2.contract_input_2`** — `object`

- Analyse the specific input "Market and vendor landscape" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:2.contract_input_3`** — `object`

- Analyse the specific input "Internal capability gaps" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:2.contract_input_4`** — `object`

- Analyse the specific input "Peer and sector practice" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technology-scout:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technology-scout:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/technology-scout:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/technology-scout:2.irrelevant_detail`** — `object`

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

- **Technology Scout:** technology radar practice; Gartner-style hype cycle positioning used critically; structured vendor evaluation. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-technology-scout-3"></a>

## emerging technology briefings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: emerging technology briefings.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `technology-scout:3`.

**Required inputs:**

- Strategic priorities
- Market and vendor landscape
- Internal capability gaps
- Peer and sector practice

**Specification:** `kind/role/technology-scout:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: emerging technology briefings.

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

**`role/technology-scout:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: emerging technology briefings.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:3.receiving_acceptance`** — `array`

- For each receiving role (Enterprise Architect; Innovation Lead), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:3.delivery_verification`** — `array`

- For the specific output 'emerging technology briefings', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Success and failure criteria are written before the experiment runs.
- G2: Negative results are reported, not quietly abandoned.
- G3: Prototype code is labelled non-production and is never deployed to a production path without a rewrite decision.
- G4: Licensing, export-control, data-protection and ethical constraints are checked before using external data or models.
- G5: Every radar position states the evidence and the trigger that would move it
- G6: positions based only on vendor marketing are marked as unevidenced
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:3.contract_input_1`** — `object`

- Analyse the specific input "Strategic priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:3.contract_input_2`** — `object`

- Analyse the specific input "Market and vendor landscape" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:3.contract_input_3`** — `object`

- Analyse the specific input "Internal capability gaps" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:3.contract_input_4`** — `object`

- Analyse the specific input "Peer and sector practice" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technology-scout:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technology-scout:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/technology-scout:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/technology-scout:3.irrelevant_detail`** — `object`

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

- **Technology Scout:** technology radar practice; Gartner-style hype cycle positioning used critically; structured vendor evaluation. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-technology-scout-4"></a>

## watch list with review triggers

**At a glance**

- **Purpose:** Produce and govern the role deliverable: watch list with review triggers.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `technology-scout:4`.

**Required inputs:**

- Strategic priorities
- Market and vendor landscape
- Internal capability gaps
- Peer and sector practice

**Specification:** `kind/role/technology-scout:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: watch list with review triggers.

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

**`role/technology-scout:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: watch list with review triggers.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:4.receiving_acceptance`** — `array`

- For each receiving role (Enterprise Architect; Innovation Lead), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:4.delivery_verification`** — `array`

- For the specific output 'watch list with review triggers', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Success and failure criteria are written before the experiment runs.
- G2: Negative results are reported, not quietly abandoned.
- G3: Prototype code is labelled non-production and is never deployed to a production path without a rewrite decision.
- G4: Licensing, export-control, data-protection and ethical constraints are checked before using external data or models.
- G5: Every radar position states the evidence and the trigger that would move it
- G6: positions based only on vendor marketing are marked as unevidenced
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:4.contract_input_1`** — `object`

- Analyse the specific input "Strategic priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:4.contract_input_2`** — `object`

- Analyse the specific input "Market and vendor landscape" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:4.contract_input_3`** — `object`

- Analyse the specific input "Internal capability gaps" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:4.contract_input_4`** — `object`

- Analyse the specific input "Peer and sector practice" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technology-scout:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/technology-scout:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technology-scout:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/technology-scout:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/technology-scout:4.irrelevant_detail`** — `object`

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

- **Technology Scout:** technology radar practice; Gartner-style hype cycle positioning used critically; structured vendor evaluation. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
