<!-- JAI:OUTPUT-CONTRACTS:START -->
# Cloud Engineer: output contracts

Build and maintain cloud infrastructure as code, within the agreed guardrails

[Full catalogue](index.md)

<a id="output-cloud-engineer-1"></a>

## Infrastructure-as-code modules

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Infrastructure-as-code modules.
- **Mandatory examples:** Define ordered automated stages, verification checkpoints, error handling, stop conditions and rollback or forward recovery paths. Identify exact deployment targets, versioned build inputs, configuration contracts and authorised execution boundaries without secrets. Link reproducible automation checks and observed outcomes to controlled environments; do not claim production execution or authorisation without evidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `cloud-engineer:1`.

**Required inputs:**

- Landing zone and architecture standards
- Workload requirements
- Security baseline
- Cost envelope

**Specification:** `kind/role/cloud-engineer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Infrastructure-as-code modules.

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

**`role/cloud-engineer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Infrastructure-as-code modules.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:1.receiving_acceptance`** — `array`

- For each receiving role (Site Reliability Engineer; Cloud Operations Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:1.delivery_verification`** — `array`

- For the specific output 'Infrastructure-as-code modules', provide verifiable evidence satisfying: Identify exact deployment targets, versioned build inputs, configuration contracts and authorised execution boundaries without secrets. Define ordered automated stages, verification checkpoints, error handling, stop conditions and rollback or forward recovery paths. Link reproducible automation checks and observed outcomes to controlled environments; do not claim production execution or authorisation without evidence. Existing source requirement: Passes automated checks, carries tests and telemetry, and has a rollback path. Required delivery form: Versioned executable build/provision/deploy automation with controlled targets and failure/recovery gates.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: No production resource is created outside infrastructure-as-code
- G9: console changes are treated as incidents and reconciled or reverted
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:1.contract_input_1`** — `object`

- Analyse the specific input "Landing zone and architecture standards" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:1.contract_input_2`** — `object`

- Analyse the specific input "Workload requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:1.contract_input_3`** — `object`

- Analyse the specific input "Security baseline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:1.contract_input_4`** — `object`

- Analyse the specific input "Cost envelope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/cloud-engineer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/cloud-engineer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/cloud-engineer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/cloud-engineer:1.irrelevant_detail`** — `object`

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
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Cloud Engineer:** provider well-architected frameworks; CIS Benchmarks; infrastructure-as-code practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Define measurable service objectives, capacity and dependency assumptions, failure behaviour, recovery and observed operational evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-cloud-engineer-2"></a>

## environment provisioning automation

**At a glance**

- **Purpose:** Produce and govern the role deliverable: environment provisioning automation.
- **Mandatory examples:** Define ordered automated stages, verification checkpoints, error handling, stop conditions and rollback or forward recovery paths. Identify exact deployment targets, versioned build inputs, configuration contracts and authorised execution boundaries without secrets. Link reproducible automation checks and observed outcomes to controlled environments; do not claim production execution or authorisation without evidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `cloud-engineer:2`.

**Required inputs:**

- Landing zone and architecture standards
- Workload requirements
- Security baseline
- Cost envelope

**Specification:** `kind/role/cloud-engineer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: environment provisioning automation.

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

**`role/cloud-engineer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: environment provisioning automation.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:2.receiving_acceptance`** — `array`

- For each receiving role (Site Reliability Engineer; Cloud Operations Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:2.delivery_verification`** — `array`

- For the specific output 'environment provisioning automation', provide verifiable evidence satisfying: Identify exact deployment targets, versioned build inputs, configuration contracts and authorised execution boundaries without secrets. Define ordered automated stages, verification checkpoints, error handling, stop conditions and rollback or forward recovery paths. Link reproducible automation checks and observed outcomes to controlled environments; do not claim production execution or authorisation without evidence. Required delivery form: Versioned executable build/provision/deploy automation with controlled targets and failure/recovery gates.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: No production resource is created outside infrastructure-as-code
- G9: console changes are treated as incidents and reconciled or reverted
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:2.contract_input_1`** — `object`

- Analyse the specific input "Landing zone and architecture standards" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:2.contract_input_2`** — `object`

- Analyse the specific input "Workload requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:2.contract_input_3`** — `object`

- Analyse the specific input "Security baseline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:2.contract_input_4`** — `object`

- Analyse the specific input "Cost envelope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/cloud-engineer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/cloud-engineer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/cloud-engineer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/cloud-engineer:2.irrelevant_detail`** — `object`

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
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Cloud Engineer:** provider well-architected frameworks; CIS Benchmarks; infrastructure-as-code practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Define measurable service objectives, capacity and dependency assumptions, failure behaviour, recovery and observed operational evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-cloud-engineer-3"></a>

## cloud configuration baselines

**At a glance**

- **Purpose:** Produce and govern the role deliverable: cloud configuration baselines.
- **Mandatory examples:** Identify managed assets, tool/schema versions and authorised configuration scope. Provide typed desired settings, permitted ranges and secret-manager references. Evidence reproducibility, drift checks, deployment validation and rollback to a known baseline.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `cloud-engineer:3`.

**Required inputs:**

- Landing zone and architecture standards
- Workload requirements
- Security baseline
- Cost envelope

**Specification:** `kind/role/cloud-engineer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: cloud configuration baselines.

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

**`role/cloud-engineer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: cloud configuration baselines.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:3.receiving_acceptance`** — `array`

- For each receiving role (Site Reliability Engineer; Cloud Operations Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:3.delivery_verification`** — `array`

- For the specific output 'cloud configuration baselines', provide verifiable evidence satisfying: Identify managed components, exact versions, environments, approved parameter values, exceptions and configuration owner without exposing secrets. Describe how the baseline is created/applied, validated and changed, including dependencies and recovery from an unsuccessful change. Compare observed configuration with the declared baseline, classify drift, identify material impact and record authorised remediation or unresolved exceptions. Required delivery form: Typed desired-state configuration with exact targets, versioned values and controlled secret references.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: No production resource is created outside infrastructure-as-code
- G9: console changes are treated as incidents and reconciled or reverted
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:3.contract_input_1`** — `object`

- Analyse the specific input "Landing zone and architecture standards" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:3.contract_input_2`** — `object`

- Analyse the specific input "Workload requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:3.contract_input_3`** — `object`

- Analyse the specific input "Security baseline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:3.contract_input_4`** — `object`

- Analyse the specific input "Cost envelope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/cloud-engineer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/cloud-engineer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/cloud-engineer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/cloud-engineer:3.irrelevant_detail`** — `object`

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
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Cloud Engineer:** provider well-architected frameworks; CIS Benchmarks; infrastructure-as-code practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Define measurable service objectives, capacity and dependency assumptions, failure behaviour, recovery and observed operational evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-cloud-engineer-4"></a>

## cost and tagging compliance

**At a glance**

- **Purpose:** Produce and govern the role deliverable: cost and tagging compliance.
- **Mandatory examples:** Define tested obligations, assurance period, sample and exclusions. Link procedures and observed results to immutable evidence and located deviations. Limit the independent conclusion to tested scope, evidence strength and unresolved findings.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `cloud-engineer:4`.

**Required inputs:**

- Landing zone and architecture standards
- Workload requirements
- Security baseline
- Cost envelope

**Specification:** `kind/role/cloud-engineer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: cost and tagging compliance.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/assurance-report`](spec-type-assurance-report.md)
- [`domain/security`](spec-domain-security.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `assurance-assessment`.

Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.

**Evidence accompanying the work product:**

- criterion-to-test-to-observation traceability
- independent reviewer and limitations

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/cloud-engineer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: cost and tagging compliance.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:4.receiving_acceptance`** — `array`

- For each receiving role (Site Reliability Engineer; Cloud Operations Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:4.delivery_verification`** — `array`

- For the specific output 'cost and tagging compliance', provide verifiable evidence satisfying: State assessment objectives, criteria versions, scope, period, population, sample rationale and exclusions before drawing conclusions. For each criterion, identify procedure, sample, observed result, supporting material and located deviations; distinguish absent evidence from demonstrated failure. Bound the conclusion by coverage and limitations; list findings, severity rationale, management response, remediation owner and verification needed for closure. Required delivery form: Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: No production resource is created outside infrastructure-as-code
- G9: console changes are treated as incidents and reconciled or reverted
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:4.contract_input_1`** — `object`

- Analyse the specific input "Landing zone and architecture standards" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:4.contract_input_2`** — `object`

- Analyse the specific input "Workload requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:4.contract_input_3`** — `object`

- Analyse the specific input "Security baseline" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:4.contract_input_4`** — `object`

- Analyse the specific input "Cost envelope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/cloud-engineer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cloud-engineer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/cloud-engineer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://sre.google/sre-book/service-level-objectives/); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/cloud-engineer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/cloud-engineer:4.irrelevant_detail`** — `object`

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

- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Cloud Engineer:** provider well-architected frameworks; CIS Benchmarks; infrastructure-as-code practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Define measurable service objectives, capacity and dependency assumptions, failure behaviour, recovery and observed operational evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
