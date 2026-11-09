<!-- JAI:OUTPUT-CONTRACTS:START -->
# Database Reliability Engineer: output contracts

Apply engineering practice to data stores: automation, service objectives and safe schema evolution

[Full catalogue](index.md)

<a id="output-database-reliability-engineer-1"></a>

## Database automation and infrastructure-as-code

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Database automation and infrastructure-as-code.
- **Mandatory examples:** Define ordered automated stages, verification checkpoints, error handling, stop conditions and rollback or forward recovery paths. Identify exact deployment targets, versioned build inputs, configuration contracts and authorised execution boundaries without secrets. Link reproducible automation checks and observed outcomes to controlled environments; do not claim production execution or authorisation without evidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `database-reliability-engineer:1`.

**Required inputs:**

- Service level requirements
- Schema change pipeline
- Performance telemetry
- Platform capabilities

**Specification:** `kind/role/database-reliability-engineer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Database automation and infrastructure-as-code.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/deployment-automation`](spec-family-deployment-automation.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `executable-deployment-automation`.

Versioned executable build/provision/deploy automation with controlled targets and failure/recovery gates.

**Evidence accompanying the work product:**

- reproducible invocation and target versions
- observed idempotency, health and rollback checks

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/database-reliability-engineer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Database automation and infrastructure-as-code.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:1.receiving_acceptance`** — `array`

- For each receiving role (Backend Engineer; Database Administrator), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:1.delivery_verification`** — `array`

- For the specific output 'Database automation and infrastructure-as-code', provide verifiable evidence satisfying: Identify exact deployment targets, versioned build inputs, configuration contracts and authorised execution boundaries without secrets. Define ordered automated stages, verification checkpoints, error handling, stop conditions and rollback or forward recovery paths. Link reproducible automation checks and observed outcomes to controlled environments; do not claim production execution or authorisation without evidence. Existing source requirement: Passes automated checks, carries tests and telemetry, and has a rollback path. Required delivery form: Versioned executable build/provision/deploy automation with controlled targets and failure/recovery gates.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: A recurring incident gets a root-cause analysis that compares against the last known good state, a working analogue and timing factors — duration, ordering, schedules, expiry — before a permanent fix is chosen (it-role-library/standards/defect-analysis.md).
- G2: No change reaches production outside the agreed change path, including 'emergency' changes, which are logged retrospectively within the agreed window.
- G3: Evidence needed for root-cause analysis is preserved before destructive recovery actions.
- G4: Communication cadence is met for every major incident, with a named communications owner.
- G5: Every recurring incident has an open problem record; recurrence without a problem record is a process failure.
- G6: Every schema migration is backward compatible or ships with a tested, timed rollback
- G7: blocking migrations on live tables are refused
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:1.contract_input_1`** — `object`

- Analyse the specific input "Service level requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:1.contract_input_2`** — `object`

- Analyse the specific input "Schema change pipeline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:1.contract_input_3`** — `object`

- Analyse the specific input "Performance telemetry" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:1.contract_input_4`** — `object`

- Analyse the specific input "Platform capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/database-reliability-engineer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/database-reliability-engineer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/database-reliability-engineer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/database-reliability-engineer:1.irrelevant_detail`** — `object`

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

- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-218, Secure Software Development Framework Version 1.1](https://doi.org/10.6028/NIST.SP.800-218)** — Secure development practices, protected source/build inputs, verification and vulnerability response. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Database Reliability Engineer:** Google SRE practice; online schema change patterns; vendor high-availability guidance. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-database-reliability-engineer-2"></a>

## service level objectives for data stores

**At a glance**

- **Purpose:** Produce and govern the role deliverable: service level objectives for data stores.
- **Mandatory examples:** Define measurable availability, support, capacity and recovery targets. Describe support responsibilities, suppliers, monitoring, continuity and lifecycle costs. Identify customers, service owner, outcomes, boundaries and demand assumptions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `database-reliability-engineer:2`.

**Required inputs:**

- Service level requirements
- Schema change pipeline
- Performance telemetry
- Platform capabilities

**Specification:** `kind/role/database-reliability-engineer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: service level objectives for data stores.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/service-design`](spec-type-service-design.md)
- [`domain/operations`](spec-domain-operations.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `service-definition`.

Service definition with consumers, outcomes, responsibilities and measurable service commitments.

**Evidence accompanying the work product:**

- indicator/target/window definitions
- support, dependency and recovery arrangements

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/database-reliability-engineer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: service level objectives for data stores.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:2.receiving_acceptance`** — `array`

- For each receiving role (Backend Engineer; Database Administrator), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:2.delivery_verification`** — `array`

- For the specific output 'service level objectives for data stores', provide verifiable evidence satisfying: State service consumers, business outcomes, eligibility, service boundary, exclusions, accountable owner and demand assumptions. For every service level, define indicator, unit, measurement source/window, target, exclusions and breach response; label unagreed targets as proposals. Define support tiers, ownership, supplier/interface dependencies, change/incident escalation, recovery objectives and cost assumptions. Required delivery form: Service definition with consumers, outcomes, responsibilities and measurable service commitments.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: A recurring incident gets a root-cause analysis that compares against the last known good state, a working analogue and timing factors — duration, ordering, schedules, expiry — before a permanent fix is chosen (it-role-library/standards/defect-analysis.md).
- G2: No change reaches production outside the agreed change path, including 'emergency' changes, which are logged retrospectively within the agreed window.
- G3: Evidence needed for root-cause analysis is preserved before destructive recovery actions.
- G4: Communication cadence is met for every major incident, with a named communications owner.
- G5: Every recurring incident has an open problem record; recurrence without a problem record is a process failure.
- G6: Every schema migration is backward compatible or ships with a tested, timed rollback
- G7: blocking migrations on live tables are refused
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:2.contract_input_1`** — `object`

- Analyse the specific input "Service level requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:2.contract_input_2`** — `object`

- Analyse the specific input "Schema change pipeline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:2.contract_input_3`** — `object`

- Analyse the specific input "Performance telemetry" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:2.contract_input_4`** — `object`

- Analyse the specific input "Platform capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/database-reliability-engineer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/database-reliability-engineer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/database-reliability-engineer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/database-reliability-engineer:2.irrelevant_detail`** — `object`

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

- **[ISO/IEC 20000-1:2018, Service management system requirements](https://www.iso.org/standard/70636.html)** — Service requirements, agreements, transition, operation and measurement concepts. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Database Reliability Engineer:** Google SRE practice; online schema change patterns; vendor high-availability guidance. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-database-reliability-engineer-3"></a>

## schema migration tooling and policy

**At a glance**

- **Purpose:** Produce and govern the role deliverable: schema migration tooling and policy.
- **Mandatory examples:** Trace implemented behaviour and changed interfaces to requirements, design constraints and the exact reviewed source revision. Define deployment compatibility, telemetry, failure detection and rollback or forward recovery constraints. Identify reproducible automated checks, observed results, untested risks and independent review findings without inventing execution.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `database-reliability-engineer:3`.

**Required inputs:**

- Service level requirements
- Schema change pipeline
- Performance telemetry
- Platform capabilities

**Specification:** `kind/role/database-reliability-engineer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: schema migration tooling and policy.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/software-change`](spec-family-software-change.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `versioned-source-change`.

Actual version-controlled implementation or analysis code, separate from its explanatory report.

**Evidence accompanying the work product:**

- exact source and dependency revision
- observed checks and independent review

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/database-reliability-engineer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: schema migration tooling and policy.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:3.receiving_acceptance`** — `array`

- For each receiving role (Backend Engineer; Database Administrator), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:3.delivery_verification`** — `array`

- For the specific output 'schema migration tooling and policy', provide verifiable evidence satisfying: Trace implemented behaviour and changed interfaces to requirements, design constraints and the exact reviewed source revision. Identify reproducible automated checks, observed results, untested risks and independent review findings without inventing execution. Define deployment compatibility, telemetry, failure detection and rollback or forward recovery constraints. Existing source requirement: Supplies actual tool source/configuration, dependencies, reproducible checks, compatibility, authorised migration controls and recovery evidence; planned tooling is not delivered tooling. Required delivery form: Actual version-controlled implementation or analysis code, separate from its explanatory report.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: A recurring incident gets a root-cause analysis that compares against the last known good state, a working analogue and timing factors — duration, ordering, schedules, expiry — before a permanent fix is chosen (it-role-library/standards/defect-analysis.md).
- G2: No change reaches production outside the agreed change path, including 'emergency' changes, which are logged retrospectively within the agreed window.
- G3: Evidence needed for root-cause analysis is preserved before destructive recovery actions.
- G4: Communication cadence is met for every major incident, with a named communications owner.
- G5: Every recurring incident has an open problem record; recurrence without a problem record is a process failure.
- G6: Every schema migration is backward compatible or ships with a tested, timed rollback
- G7: blocking migrations on live tables are refused
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:3.contract_input_1`** — `object`

- Analyse the specific input "Service level requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:3.contract_input_2`** — `object`

- Analyse the specific input "Schema change pipeline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:3.contract_input_3`** — `object`

- Analyse the specific input "Performance telemetry" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:3.contract_input_4`** — `object`

- Analyse the specific input "Platform capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/database-reliability-engineer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/database-reliability-engineer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/database-reliability-engineer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/database-reliability-engineer:3.irrelevant_detail`** — `object`

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

- **[NIST SP 800-218, Secure Software Development Framework Version 1.1](https://doi.org/10.6028/NIST.SP.800-218)** — Secure development practices, protected source/build inputs, verification and vulnerability response. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Database Reliability Engineer:** Google SRE practice; online schema change patterns; vendor high-availability guidance. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-database-reliability-engineer-4"></a>

## reliability and toil reduction plan

**At a glance**

- **Purpose:** Produce and govern the role deliverable: reliability and toil reduction plan.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `database-reliability-engineer:4`.

**Required inputs:**

- Service level requirements
- Schema change pipeline
- Performance telemetry
- Platform capabilities

**Specification:** `kind/role/database-reliability-engineer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: reliability and toil reduction plan.

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

**`role/database-reliability-engineer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: reliability and toil reduction plan.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:4.receiving_acceptance`** — `array`

- For each receiving role (Backend Engineer; Database Administrator), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:4.delivery_verification`** — `array`

- For the specific output 'reliability and toil reduction plan', provide verifiable evidence satisfying: State business outcomes, current/target baseline, planning horizons, sponsors and material planning assumptions. For each increment, identify deliverables, owner, indicative resource/funding requirement, milestone and measurable completion outcome. Identify dependencies and critical sequence, decision dates, constraints and alternative paths; distinguish committed work from tentative options. Existing source requirement: Every milestone has an acceptance test and a named accountable owner. Required delivery form: Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: A recurring incident gets a root-cause analysis that compares against the last known good state, a working analogue and timing factors — duration, ordering, schedules, expiry — before a permanent fix is chosen (it-role-library/standards/defect-analysis.md).
- G2: No change reaches production outside the agreed change path, including 'emergency' changes, which are logged retrospectively within the agreed window.
- G3: Evidence needed for root-cause analysis is preserved before destructive recovery actions.
- G4: Communication cadence is met for every major incident, with a named communications owner.
- G5: Every recurring incident has an open problem record; recurrence without a problem record is a process failure.
- G6: Every schema migration is backward compatible or ships with a tested, timed rollback
- G7: blocking migrations on live tables are refused
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:4.contract_input_1`** — `object`

- Analyse the specific input "Service level requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:4.contract_input_2`** — `object`

- Analyse the specific input "Schema change pipeline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:4.contract_input_3`** — `object`

- Analyse the specific input "Performance telemetry" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:4.contract_input_4`** — `object`

- Analyse the specific input "Platform capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/database-reliability-engineer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/database-reliability-engineer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/database-reliability-engineer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/database-reliability-engineer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/database-reliability-engineer:4.irrelevant_detail`** — `object`

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
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Database Reliability Engineer:** Google SRE practice; online schema change patterns; vendor high-availability guidance. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
