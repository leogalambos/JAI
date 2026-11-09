<!-- JAI:OUTPUT-CONTRACTS:START -->
# Product Analyst: output contracts

Measure how the product is actually used and whether changes to it worked

[Full catalogue](index.md)

<a id="output-product-analyst-1"></a>

## Product metric framework

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Product metric framework.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `product-analyst:1`.

**Required inputs:**

- Product telemetry
- Experiment hypotheses
- User research findings
- Commercial data

**Specification:** `kind/role/product-analyst:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Product metric framework.

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

**`role/product-analyst:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Product metric framework.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:1.receiving_acceptance`** — `array`

- For each receiving role (Product Manager; Product Designer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:1.delivery_verification`** — `array`

- For the specific output 'Product metric framework', provide verifiable evidence satisfying: State the exact subject, intended recipient/use, boundary, source versions and the concrete question the document answers. Provide subject-specific findings or instructions with supporting facts, assumptions, reasoning, limitations and traceable references; generic background alone is insufficient. State conclusions, decisions requested or actionable instructions, accountable recipients and completion/acceptance conditions; identify open issues explicitly. Required delivery form: Purpose-specific professional document with source analysis, reasoning, conclusions and recipient actions.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("Product metric framework") has been walked through with the people who will build, test and operate the result.
- G5: Experiment results are reported with effect size, confidence interval and the pre-registered hypothesis
- G6: post-hoc segment hunting is labelled as exploratory
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:1.contract_input_1`** — `object`

- Analyse the specific input "Product telemetry" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:1.contract_input_2`** — `object`

- Analyse the specific input "Experiment hypotheses" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:1.contract_input_3`** — `object`

- Analyse the specific input "User research findings" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:1.contract_input_4`** — `object`

- Analyse the specific input "Commercial data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/product-analyst:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/product-analyst:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/product-analyst:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/product-analyst:1.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Product Analyst:** experiment design practice; statistical significance testing; product analytics instrumentation standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace source needs, stakeholders and conflicting constraints into verifiable requirements, models and acceptance criteria.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-product-analyst-2"></a>

## experiment design and results

**At a glance**

- **Purpose:** Produce and govern the role deliverable: experiment design and results.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `product-analyst:2`.

**Required inputs:**

- Product telemetry
- Experiment hypotheses
- User research findings
- Commercial data

**Specification:** `kind/role/product-analyst:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: experiment design and results.

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

**`role/product-analyst:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: experiment design and results.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:2.receiving_acceptance`** — `array`

- For each receiving role (Product Manager; Product Designer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:2.delivery_verification`** — `array`

- For the specific output 'experiment design and results', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Existing source requirement: States hypothesis, sample/population, allocation, measures, stopping criteria, observed effects and uncertainty. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("Product metric framework") has been walked through with the people who will build, test and operate the result.
- G5: Experiment results are reported with effect size, confidence interval and the pre-registered hypothesis
- G6: post-hoc segment hunting is labelled as exploratory
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:2.contract_input_1`** — `object`

- Analyse the specific input "Product telemetry" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:2.contract_input_2`** — `object`

- Analyse the specific input "Experiment hypotheses" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:2.contract_input_3`** — `object`

- Analyse the specific input "User research findings" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:2.contract_input_4`** — `object`

- Analyse the specific input "Commercial data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/product-analyst:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/product-analyst:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/product-analyst:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/product-analyst:2.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Product Analyst:** experiment design practice; statistical significance testing; product analytics instrumentation standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace source needs, stakeholders and conflicting constraints into verifiable requirements, models and acceptance criteria.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-product-analyst-3"></a>

## funnel and retention analysis

**At a glance**

- **Purpose:** Produce and govern the role deliverable: funnel and retention analysis.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `product-analyst:3`.

**Required inputs:**

- Product telemetry
- Experiment hypotheses
- User research findings
- Commercial data

**Specification:** `kind/role/product-analyst:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: funnel and retention analysis.

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

**`role/product-analyst:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: funnel and retention analysis.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:3.receiving_acceptance`** — `array`

- For each receiving role (Product Manager; Product Designer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:3.delivery_verification`** — `array`

- For the specific output 'funnel and retention analysis', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("Product metric framework") has been walked through with the people who will build, test and operate the result.
- G5: Experiment results are reported with effect size, confidence interval and the pre-registered hypothesis
- G6: post-hoc segment hunting is labelled as exploratory
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:3.contract_input_1`** — `object`

- Analyse the specific input "Product telemetry" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:3.contract_input_2`** — `object`

- Analyse the specific input "Experiment hypotheses" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:3.contract_input_3`** — `object`

- Analyse the specific input "User research findings" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:3.contract_input_4`** — `object`

- Analyse the specific input "Commercial data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/product-analyst:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/product-analyst:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/product-analyst:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/product-analyst:3.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Product Analyst:** experiment design practice; statistical significance testing; product analytics instrumentation standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace source needs, stakeholders and conflicting constraints into verifiable requirements, models and acceptance criteria.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-product-analyst-4"></a>

## feature adoption assessment

**At a glance**

- **Purpose:** Produce and govern the role deliverable: feature adoption assessment.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `product-analyst:4`.

**Required inputs:**

- Product telemetry
- Experiment hypotheses
- User research findings
- Commercial data

**Specification:** `kind/role/product-analyst:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: feature adoption assessment.

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

**`role/product-analyst:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: feature adoption assessment.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:4.receiving_acceptance`** — `array`

- For each receiving role (Product Manager; Product Designer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:4.delivery_verification`** — `array`

- For the specific output 'feature adoption assessment', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Existing source requirement: Criteria were fixed before evidence collection and the method is reproducible. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("Product metric framework") has been walked through with the people who will build, test and operate the result.
- G5: Experiment results are reported with effect size, confidence interval and the pre-registered hypothesis
- G6: post-hoc segment hunting is labelled as exploratory
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:4.contract_input_1`** — `object`

- Analyse the specific input "Product telemetry" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:4.contract_input_2`** — `object`

- Analyse the specific input "Experiment hypotheses" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:4.contract_input_3`** — `object`

- Analyse the specific input "User research findings" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:4.contract_input_4`** — `object`

- Analyse the specific input "Commercial data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/product-analyst:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`role/product-analyst:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/product-analyst:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/product-analyst:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/product-analyst:4.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Product Analyst:** experiment design practice; statistical significance testing; product analytics instrumentation standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace source needs, stakeholders and conflicting constraints into verifiable requirements, models and acceptance criteria.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
