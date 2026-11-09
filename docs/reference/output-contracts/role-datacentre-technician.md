<!-- JAI:OUTPUT-CONTRACTS:START -->
# Datacentre Technician: output contracts

Keep the physical estate working: installation, replacement, cabling, power and physical access

[Full catalogue](index.md)

<a id="output-datacentre-technician-1"></a>

## Rack and asset installation records

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Rack and asset installation records.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `datacentre-technician:1`.

**Required inputs:**

- Work orders and change records
- Asset records
- Capacity and layout plan
- Vendor maintenance schedules

**Specification:** `kind/role/datacentre-technician:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Rack and asset installation records.

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

**`role/datacentre-technician:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Rack and asset installation records.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:1.receiving_acceptance`** — `array`

- For each receiving role (Systems Administrator; IT Asset Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:1.delivery_verification`** — `array`

- For the specific output 'Rack and asset installation records', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: A recurring incident gets a root-cause analysis that compares against the last known good state, a working analogue and timing factors — duration, ordering, schedules, expiry — before a permanent fix is chosen (it-role-library/standards/defect-analysis.md).
- G2: No change reaches production outside the agreed change path, including 'emergency' changes, which are logged retrospectively within the agreed window.
- G3: Evidence needed for root-cause analysis is preserved before destructive recovery actions.
- G4: Communication cadence is met for every major incident, with a named communications owner.
- G5: Every recurring incident has an open problem record; recurrence without a problem record is a process failure.
- G6: Every physical change is reflected in the asset and configuration records the same day
- G7: undocumented physical changes are treated as incidents
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:1.contract_input_1`** — `object`

- Analyse the specific input "Work orders and change records" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:1.contract_input_2`** — `object`

- Analyse the specific input "Asset records" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:1.contract_input_3`** — `object`

- Analyse the specific input "Capacity and layout plan" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:1.contract_input_4`** — `object`

- Analyse the specific input "Vendor maintenance schedules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/datacentre-technician:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/datacentre-technician:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/datacentre-technician:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/datacentre-technician:1.irrelevant_detail`** — `object`

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
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Datacentre Technician:** ANSI/TIA-942; vendor installation guidance; site physical security policy. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Define measurable service objectives, capacity and dependency assumptions, failure behaviour, recovery and observed operational evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-datacentre-technician-2"></a>

## hardware replacement and RMA evidence

**At a glance**

- **Purpose:** Produce and govern the role deliverable: hardware replacement and RMA evidence.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `datacentre-technician:2`.

**Required inputs:**

- Work orders and change records
- Asset records
- Capacity and layout plan
- Vendor maintenance schedules

**Specification:** `kind/role/datacentre-technician:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: hardware replacement and RMA evidence.

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

**`role/datacentre-technician:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: hardware replacement and RMA evidence.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:2.receiving_acceptance`** — `array`

- For each receiving role (Systems Administrator; IT Asset Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:2.delivery_verification`** — `array`

- For the specific output 'hardware replacement and RMA evidence', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Existing source requirement: Chain of custody is unbroken and the set is reproducible from the record. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: A recurring incident gets a root-cause analysis that compares against the last known good state, a working analogue and timing factors — duration, ordering, schedules, expiry — before a permanent fix is chosen (it-role-library/standards/defect-analysis.md).
- G2: No change reaches production outside the agreed change path, including 'emergency' changes, which are logged retrospectively within the agreed window.
- G3: Evidence needed for root-cause analysis is preserved before destructive recovery actions.
- G4: Communication cadence is met for every major incident, with a named communications owner.
- G5: Every recurring incident has an open problem record; recurrence without a problem record is a process failure.
- G6: Every physical change is reflected in the asset and configuration records the same day
- G7: undocumented physical changes are treated as incidents
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:2.contract_input_1`** — `object`

- Analyse the specific input "Work orders and change records" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:2.contract_input_2`** — `object`

- Analyse the specific input "Asset records" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:2.contract_input_3`** — `object`

- Analyse the specific input "Capacity and layout plan" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:2.contract_input_4`** — `object`

- Analyse the specific input "Vendor maintenance schedules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/datacentre-technician:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/datacentre-technician:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/datacentre-technician:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/datacentre-technician:2.irrelevant_detail`** — `object`

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
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Datacentre Technician:** ANSI/TIA-942; vendor installation guidance; site physical security policy. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Define measurable service objectives, capacity and dependency assumptions, failure behaviour, recovery and observed operational evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-datacentre-technician-3"></a>

## environmental and power readings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: environmental and power readings.
- **Mandatory examples:** Record source versions, extraction time, transformations, lawful access and retention. Evidence completeness, uniqueness, consistency, drift and permitted-use limitations. Define fields, datatypes, units, keys, null handling and allowed values.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `datacentre-technician:3`.

**Required inputs:**

- Work orders and change records
- Asset records
- Capacity and layout plan
- Vendor maintenance schedules

**Specification:** `kind/role/datacentre-technician:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: environmental and power readings.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/dataset`](spec-type-dataset.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `typed-dataset-or-calculation-model`.

Typed data or calculation model with units, keys/formulas, lineage and quality constraints.

**Evidence accompanying the work product:**

- versioned inputs and reproducible transformations
- reconciliation, quality measures and permitted use

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/datacentre-technician:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: environmental and power readings.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:3.receiving_acceptance`** — `array`

- For each receiving role (Systems Administrator; IT Asset Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:3.delivery_verification`** — `array`

- For the specific output 'environmental and power readings', provide verifiable evidence satisfying: Specify field names, meaning, type, units, code lists, keys, relationships, null semantics and permitted values. Identify source systems/extract versions, transformations, time coverage, access/licensing conditions and accountable custodian. Report completeness, validity, consistency and other relevant quality measures with method, population, results and known limitations. Required delivery form: Typed data or calculation model with units, keys/formulas, lineage and quality constraints.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: A recurring incident gets a root-cause analysis that compares against the last known good state, a working analogue and timing factors — duration, ordering, schedules, expiry — before a permanent fix is chosen (it-role-library/standards/defect-analysis.md).
- G2: No change reaches production outside the agreed change path, including 'emergency' changes, which are logged retrospectively within the agreed window.
- G3: Evidence needed for root-cause analysis is preserved before destructive recovery actions.
- G4: Communication cadence is met for every major incident, with a named communications owner.
- G5: Every recurring incident has an open problem record; recurrence without a problem record is a process failure.
- G6: Every physical change is reflected in the asset and configuration records the same day
- G7: undocumented physical changes are treated as incidents
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:3.contract_input_1`** — `object`

- Analyse the specific input "Work orders and change records" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:3.contract_input_2`** — `object`

- Analyse the specific input "Asset records" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:3.contract_input_3`** — `object`

- Analyse the specific input "Capacity and layout plan" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:3.contract_input_4`** — `object`

- Analyse the specific input "Vendor maintenance schedules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/datacentre-technician:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/datacentre-technician:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/datacentre-technician:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/datacentre-technician:3.irrelevant_detail`** — `object`

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

- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Datacentre Technician:** ANSI/TIA-942; vendor installation guidance; site physical security policy. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Define measurable service objectives, capacity and dependency assumptions, failure behaviour, recovery and observed operational evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-datacentre-technician-4"></a>

## physical access and escort logs

**At a glance**

- **Purpose:** Produce and govern the role deliverable: physical access and escort logs.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `datacentre-technician:4`.

**Required inputs:**

- Work orders and change records
- Asset records
- Capacity and layout plan
- Vendor maintenance schedules

**Specification:** `kind/role/datacentre-technician:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: physical access and escort logs.

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

**`role/datacentre-technician:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: physical access and escort logs.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:4.receiving_acceptance`** — `array`

- For each receiving role (Systems Administrator; IT Asset Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:4.delivery_verification`** — `array`

- For the specific output 'physical access and escort logs', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: A recurring incident gets a root-cause analysis that compares against the last known good state, a working analogue and timing factors — duration, ordering, schedules, expiry — before a permanent fix is chosen (it-role-library/standards/defect-analysis.md).
- G2: No change reaches production outside the agreed change path, including 'emergency' changes, which are logged retrospectively within the agreed window.
- G3: Evidence needed for root-cause analysis is preserved before destructive recovery actions.
- G4: Communication cadence is met for every major incident, with a named communications owner.
- G5: Every recurring incident has an open problem record; recurrence without a problem record is a process failure.
- G6: Every physical change is reflected in the asset and configuration records the same day
- G7: undocumented physical changes are treated as incidents
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:4.contract_input_1`** — `object`

- Analyse the specific input "Work orders and change records" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:4.contract_input_2`** — `object`

- Analyse the specific input "Asset records" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:4.contract_input_3`** — `object`

- Analyse the specific input "Capacity and layout plan" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:4.contract_input_4`** — `object`

- Analyse the specific input "Vendor maintenance schedules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/datacentre-technician:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/datacentre-technician:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/datacentre-technician:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/datacentre-technician:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/datacentre-technician:4.irrelevant_detail`** — `object`

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
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Datacentre Technician:** ANSI/TIA-942; vendor installation guidance; site physical security policy. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Define measurable service objectives, capacity and dependency assumptions, failure behaviour, recovery and observed operational evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
