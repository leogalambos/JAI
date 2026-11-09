<!-- JAI:OUTPUT-CONTRACTS:START -->
# Innovation Lead: output contracts

Run the pipeline from idea to validated capability without wasting the organisation's attention

[Full catalogue](index.md)

<a id="output-innovation-lead-1"></a>

## Innovation portfolio and stage gates

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Innovation portfolio and stage gates.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `innovation-lead:1`.

**Required inputs:**

- Strategic themes
- Idea pipeline
- Market and technology scanning
- Prior experiment results

**Specification:** `kind/role/innovation-lead:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Innovation portfolio and stage gates.

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

**`role/innovation-lead:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Innovation portfolio and stage gates.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:1.receiving_acceptance`** — `array`

- For each receiving role (Research Engineer; Technology Scout), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:1.delivery_verification`** — `array`

- For the specific output 'Innovation portfolio and stage gates', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Innovation portfolio and stage gates") is published on the agreed cadence, including adverse results.
- G5: Every initiative has a stated kill criterion evaluated at each gate
- G6: initiatives that pass a gate with no evidence are terminated rather than renewed on enthusiasm
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:1.contract_input_1`** — `object`

- Analyse the specific input "Strategic themes" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:1.contract_input_2`** — `object`

- Analyse the specific input "Idea pipeline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:1.contract_input_3`** — `object`

- Analyse the specific input "Market and technology scanning" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:1.contract_input_4`** — `object`

- Analyse the specific input "Prior experiment results" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/innovation-lead:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/innovation-lead:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/innovation-lead:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/innovation-lead:1.irrelevant_detail`** — `object`

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

- **Innovation Lead:** lean startup validation; stage-gate innovation management; ISO 56002 innovation management. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-innovation-lead-2"></a>

## validated learning reports

**At a glance**

- **Purpose:** Produce and govern the role deliverable: validated learning reports.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `innovation-lead:2`.

**Required inputs:**

- Strategic themes
- Idea pipeline
- Market and technology scanning
- Prior experiment results

**Specification:** `kind/role/innovation-lead:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: validated learning reports.

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

**`role/innovation-lead:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: validated learning reports.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:2.receiving_acceptance`** — `array`

- For each receiving role (Research Engineer; Technology Scout), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:2.delivery_verification`** — `array`

- For the specific output 'validated learning reports', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Existing source requirement: Conclusions are traceable to dated evidence; opinion is visibly separated from fact. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Innovation portfolio and stage gates") is published on the agreed cadence, including adverse results.
- G5: Every initiative has a stated kill criterion evaluated at each gate
- G6: initiatives that pass a gate with no evidence are terminated rather than renewed on enthusiasm
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:2.contract_input_1`** — `object`

- Analyse the specific input "Strategic themes" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:2.contract_input_2`** — `object`

- Analyse the specific input "Idea pipeline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:2.contract_input_3`** — `object`

- Analyse the specific input "Market and technology scanning" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:2.contract_input_4`** — `object`

- Analyse the specific input "Prior experiment results" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/innovation-lead:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/innovation-lead:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/innovation-lead:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/innovation-lead:2.irrelevant_detail`** — `object`

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

- **Innovation Lead:** lean startup validation; stage-gate innovation management; ISO 56002 innovation management. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-innovation-lead-3"></a>

## adoption or termination decisions

**At a glance**

- **Purpose:** Produce and govern the role deliverable: adoption or termination decisions.
- **Mandatory examples:** Identify the specific choice, accountable authority and decision deadline. Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation. Compare viable options including the do-nothing baseline against common criteria.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `innovation-lead:3`.

**Required inputs:**

- Strategic themes
- Idea pipeline
- Market and technology scanning
- Prior experiment results

**Specification:** `kind/role/innovation-lead:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: adoption or termination decisions.

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

**`role/innovation-lead:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: adoption or termination decisions.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:3.receiving_acceptance`** — `array`

- For each receiving role (Research Engineer; Technology Scout), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:3.delivery_verification`** — `array`

- For the specific output 'adoption or termination decisions', provide verifiable evidence satisfying: Separate the requested decision from information for noting; state decision scope, eligible authority, deadline and consequences of deferral. List feasible options with consistent evaluation criteria, evidence, costs, benefits and constraints; justify any unavailable baseline. State recommendation, implementation dependencies, uncertainty and residual exposure; show which assumptions would change the preferred option. Required delivery form: Bounded decision paper with consistent option comparison and a clear authority/decision request.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Innovation portfolio and stage gates") is published on the agreed cadence, including adverse results.
- G5: Every initiative has a stated kill criterion evaluated at each gate
- G6: initiatives that pass a gate with no evidence are terminated rather than renewed on enthusiasm
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:3.contract_input_1`** — `object`

- Analyse the specific input "Strategic themes" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:3.contract_input_2`** — `object`

- Analyse the specific input "Idea pipeline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:3.contract_input_3`** — `object`

- Analyse the specific input "Market and technology scanning" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:3.contract_input_4`** — `object`

- Analyse the specific input "Prior experiment results" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/innovation-lead:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/innovation-lead:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/innovation-lead:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/innovation-lead:3.irrelevant_detail`** — `object`

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

- **Innovation Lead:** lean startup validation; stage-gate innovation management; ISO 56002 innovation management. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-innovation-lead-4"></a>

## innovation process and funding model

**At a glance**

- **Purpose:** Produce and govern the role deliverable: innovation process and funding model.
- **Mandatory examples:** List stable source-model element IDs, typed relations and labels represented in the view. Evidence endpoint validity, semantic compatibility, coverage and visual readability. Define the concern, viewpoint, system boundary, legend and notation.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `innovation-lead:4`.

**Required inputs:**

- Strategic themes
- Idea pipeline
- Market and technology scanning
- Prior experiment results

**Specification:** `kind/role/innovation-lead:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: innovation process and funding model.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/diagram`](spec-type-diagram.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `model-derived-view`.

Concern-specific diagram with declared notation, legend, typed relationships and source-element links.

**Evidence accompanying the work product:**

- endpoint/meaning/coverage checks
- legibility and explicit projection limitations

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/innovation-lead:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: innovation process and funding model.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:4.receiving_acceptance`** — `array`

- For each receiving role (Research Engineer; Technology Scout), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:4.delivery_verification`** — `array`

- For the specific output 'innovation process and funding model', provide verifiable evidence satisfying: Identify diagram purpose, scope, audience, version and notation/legend, including the meaning of every relationship type. Use stable element identifiers and meaningful labels; show relevant boundaries, directions, interfaces and external dependencies without invented facts. Check consistency with source models and related views; distinguish intentional abstraction from omitted or unresolved relationships. Existing source requirement: The model is validated against real observed behaviour or data, not only interviews. Required delivery form: Concern-specific diagram with declared notation, legend, typed relationships and source-element links.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Innovation portfolio and stage gates") is published on the agreed cadence, including adverse results.
- G5: Every initiative has a stated kill criterion evaluated at each gate
- G6: initiatives that pass a gate with no evidence are terminated rather than renewed on enthusiasm
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:4.contract_input_1`** — `object`

- Analyse the specific input "Strategic themes" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:4.contract_input_2`** — `object`

- Analyse the specific input "Idea pipeline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:4.contract_input_3`** — `object`

- Analyse the specific input "Market and technology scanning" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:4.contract_input_4`** — `object`

- Analyse the specific input "Prior experiment results" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/innovation-lead:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`role/innovation-lead:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/innovation-lead:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://www.acm.org/publications/policies/artifact-review-and-badging-current); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/innovation-lead:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/innovation-lead:4.irrelevant_detail`** — `object`

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
- **[ACM Artifact Review and Badging policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current)** — Artifact availability, evaluation and reproducibility terminology; informative evidence-pack practice, not proof that an experiment is scientifically sufficient. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Innovation Lead:** lean startup validation; stage-gate innovation management; ISO 56002 innovation management. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
