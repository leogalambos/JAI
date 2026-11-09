<!-- JAI:OUTPUT-CONTRACTS:START -->
# Master Data Management Specialist: output contracts

Establish and maintain single, trusted versions of core business entities across systems

[Full catalogue](index.md)

<a id="output-master-data-management-specialist-1"></a>

## Match, merge and survivorship rules

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Match, merge and survivorship rules.
- **Mandatory examples:** Specify deployment, verification, rollback and reproducible acceptance tests. Specify schemas, error states, concurrency and compatibility requirements. Define typed configuration values, units, versions and permitted ranges without secrets.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `master-data-management-specialist:1`.

**Required inputs:**

- Entity definitions
- Source system records and quality
- Business matching rules
- Downstream consumption requirements

**Specification:** `kind/role/master-data-management-specialist:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Match, merge and survivorship rules.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/implementation-specification`](spec-type-implementation-specification.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `implementation-specification`.

Typed implementation specification with exact target versions, interfaces and verification/recovery conditions.

**Evidence accompanying the work product:**

- parameter/schema constraints
- reproducible acceptance and recovery procedure

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/master-data-management-specialist:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Match, merge and survivorship rules.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:1.receiving_acceptance`** — `array`

- For each receiving role (Data Engineer; Data Steward), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:1.delivery_verification`** — `array`

- For the specific output 'Match, merge and survivorship rules', provide verifiable evidence satisfying: Identify exact component/environment versions and each required parameter with type, unit, permitted range, default and secret-reference handling. State interface schemas, input/output semantics, error responses, concurrency/idempotency expectations and external dependency constraints. Give reproducible build/deploy/verification steps, expected results, stop conditions and recovery path; identify evidence still required before execution. Required delivery form: Typed implementation specification with exact target versions, interfaces and verification/recovery conditions.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Match, merge and survivorship rules") is published on the agreed cadence, including adverse results.
- G5: Automated merge thresholds are tuned with a measured false-merge rate
- G6: merging two real customers is treated as a severity-one data incident
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:1.contract_input_1`** — `object`

- Analyse the specific input "Entity definitions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:1.contract_input_2`** — `object`

- Analyse the specific input "Source system records and quality" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:1.contract_input_3`** — `object`

- Analyse the specific input "Business matching rules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:1.contract_input_4`** — `object`

- Analyse the specific input "Downstream consumption requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/master-data-management-specialist:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/master-data-management-specialist:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/master-data-management-specialist:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/master-data-management-specialist:1.irrelevant_detail`** — `object`

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
  "typed": {
    "metric": "typed",
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

- **[NIST SP 800-218, Secure Software Development Framework Version 1.1](https://doi.org/10.6028/NIST.SP.800-218)** — Secure development practices, protected source/build inputs, verification and vulnerability response. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Master Data Management Specialist:** DAMA-DMBOK 2 master data management; entity resolution practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-master-data-management-specialist-2"></a>

## golden record definitions and stewardship workflow

**At a glance**

- **Purpose:** Produce and govern the role deliverable: golden record definitions and stewardship workflow.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `master-data-management-specialist:2`.

**Required inputs:**

- Entity definitions
- Source system records and quality
- Business matching rules
- Downstream consumption requirements

**Specification:** `kind/role/master-data-management-specialist:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: golden record definitions and stewardship workflow.

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

**`role/master-data-management-specialist:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: golden record definitions and stewardship workflow.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:2.receiving_acceptance`** — `array`

- For each receiving role (Data Engineer; Data Steward), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:2.delivery_verification`** — `array`

- For the specific output 'golden record definitions and stewardship workflow', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Match, merge and survivorship rules") is published on the agreed cadence, including adverse results.
- G5: Automated merge thresholds are tuned with a measured false-merge rate
- G6: merging two real customers is treated as a severity-one data incident
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:2.contract_input_1`** — `object`

- Analyse the specific input "Entity definitions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:2.contract_input_2`** — `object`

- Analyse the specific input "Source system records and quality" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:2.contract_input_3`** — `object`

- Analyse the specific input "Business matching rules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:2.contract_input_4`** — `object`

- Analyse the specific input "Downstream consumption requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/master-data-management-specialist:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/master-data-management-specialist:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/master-data-management-specialist:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/master-data-management-specialist:2.irrelevant_detail`** — `object`

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
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Master Data Management Specialist:** DAMA-DMBOK 2 master data management; entity resolution practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-master-data-management-specialist-3"></a>

## MDM hub configuration

**At a glance**

- **Purpose:** Produce and govern the role deliverable: MDM hub configuration.
- **Mandatory examples:** Identify managed assets, tool/schema versions and authorised configuration scope. Provide typed desired settings, permitted ranges and secret-manager references. Evidence reproducibility, drift checks, deployment validation and rollback to a known baseline.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `master-data-management-specialist:3`.

**Required inputs:**

- Entity definitions
- Source system records and quality
- Business matching rules
- Downstream consumption requirements

**Specification:** `kind/role/master-data-management-specialist:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: MDM hub configuration.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/configuration-baseline`](spec-type-configuration-baseline.md)
- [`domain/operations`](spec-domain-operations.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `versioned-configuration`.

Typed desired-state configuration with exact targets, versioned values and controlled secret references.

**Evidence accompanying the work product:**

- reproduction/drift observations
- verification and recovery to a known baseline

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/master-data-management-specialist:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: MDM hub configuration.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:3.receiving_acceptance`** — `array`

- For each receiving role (Data Engineer; Data Steward), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:3.delivery_verification`** — `array`

- For the specific output 'MDM hub configuration', provide verifiable evidence satisfying: Identify managed components, exact versions, environments, approved parameter values, exceptions and configuration owner without exposing secrets. Describe how the baseline is created/applied, validated and changed, including dependencies and recovery from an unsuccessful change. Compare observed configuration with the declared baseline, classify drift, identify material impact and record authorised remediation or unresolved exceptions. Required delivery form: Typed desired-state configuration with exact targets, versioned values and controlled secret references.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Match, merge and survivorship rules") is published on the agreed cadence, including adverse results.
- G5: Automated merge thresholds are tuned with a measured false-merge rate
- G6: merging two real customers is treated as a severity-one data incident
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:3.contract_input_1`** — `object`

- Analyse the specific input "Entity definitions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:3.contract_input_2`** — `object`

- Analyse the specific input "Source system records and quality" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:3.contract_input_3`** — `object`

- Analyse the specific input "Business matching rules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:3.contract_input_4`** — `object`

- Analyse the specific input "Downstream consumption requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/master-data-management-specialist:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/master-data-management-specialist:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/master-data-management-specialist:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/master-data-management-specialist:3.irrelevant_detail`** — `object`

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
  "typed": {
    "metric": "typed",
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

- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Master Data Management Specialist:** DAMA-DMBOK 2 master data management; entity resolution practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-master-data-management-specialist-4"></a>

## data quality and duplication metrics

**At a glance**

- **Purpose:** Produce and govern the role deliverable: data quality and duplication metrics.
- **Mandatory examples:** Explain thresholds, uncertainty, missing data and actions supported by the view. Define metrics, units, denominators, targets, refresh cadence and accountable owners. Provide dated observations linked to versioned source queries and population scope.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `master-data-management-specialist:4`.

**Required inputs:**

- Entity definitions
- Source system records and quality
- Business matching rules
- Downstream consumption requirements

**Specification:** `kind/role/master-data-management-specialist:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: data quality and duplication metrics.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/dashboard`](spec-type-dashboard.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `measured-dashboard`.

Dashboard or scorecard with metric definitions, observations, source queries and interpretation.

**Evidence accompanying the work product:**

- units, denominators and measurement windows
- dated values, thresholds and actionable exceptions

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/master-data-management-specialist:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: data quality and duplication metrics.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:4.receiving_acceptance`** — `array`

- For each receiving role (Data Engineer; Data Steward), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:4.delivery_verification`** — `array`

- For the specific output 'data quality and duplication metrics', provide verifiable evidence satisfying: For each metric, define question, formula, unit, population/denominator, time window, target/threshold and accountable owner. Show observation timestamp, source/query version, aggregation, missing-data handling and measurement limitations. Explain threshold crossings and trends, uncertainty and the action or decision supported; distinguish operational signals from causal explanations. Required delivery form: Dashboard or scorecard with metric definitions, observations, source queries and interpretation.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Match, merge and survivorship rules") is published on the agreed cadence, including adverse results.
- G5: Automated merge thresholds are tuned with a measured false-merge rate
- G6: merging two real customers is treated as a severity-one data incident
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:4.contract_input_1`** — `object`

- Analyse the specific input "Entity definitions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:4.contract_input_2`** — `object`

- Analyse the specific input "Source system records and quality" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:4.contract_input_3`** — `object`

- Analyse the specific input "Business matching rules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:4.contract_input_4`** — `object`

- Analyse the specific input "Downstream consumption requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/master-data-management-specialist:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/master-data-management-specialist:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/master-data-management-specialist:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/master-data-management-specialist:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/master-data-management-specialist:4.irrelevant_detail`** — `object`

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

- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Master Data Management Specialist:** DAMA-DMBOK 2 master data management; entity resolution practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
