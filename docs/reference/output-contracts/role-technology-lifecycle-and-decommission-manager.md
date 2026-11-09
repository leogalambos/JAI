<!-- JAI:OUTPUT-CONTRACTS:START -->
# Technology Lifecycle and Decommission Manager: output contracts

Retire technology, services and platforms without leaving hidden dependencies, unmanaged data, active access, stale assets, avoidable cost or unowned residual obligations.

[Full catalogue](index.md)

<a id="output-technology-lifecycle-and-decommission-manager-1"></a>

## Technology lifecycle and decommission assessment

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Technology lifecycle and decommission assessment.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `technology-lifecycle-and-decommission-manager:1`.

**Required inputs:**

- Architecture dependency/impact view and lifecycle state
- Service, configuration and asset inventory
- Data retention, archive and disposal obligations
- Contracts, licences and supplier exit obligations
- Access, secrets, certificates and integrations inventory
- Benefits/cost baseline that justified retirement

**Specification:** `kind/role/technology-lifecycle-and-decommission-manager:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Technology lifecycle and decommission assessment.

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

**`role/technology-lifecycle-and-decommission-manager:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Technology lifecycle and decommission assessment.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:1.receiving_acceptance`** — `array`

- For each receiving role (IT Asset Manager; Benefits Realisation Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:1.delivery_verification`** — `array`

- For the specific output 'Technology lifecycle and decommission assessment', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Existing source requirement: Scope, owner, lifecycle state, dependencies, obligations and authority are explicit and current. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No retirement proceeds while an active material dependency has no migration, removal or named waiver.
- G2: Data retention/archive/destruction disposition is approved by the correct data/privacy/legal authority where required.
- G3: Identities, privileged access, secrets, certificates and integration credentials are revoked or transferred with evidence.
- G4: CMDB, asset/licence, supplier/contract, monitoring, backup and service-catalogue records reconcile to the retired state.
- G5: Architecture repository lifecycle is retired, with valid-to date and any residual cross-project obligations explicitly owned.
- G6: Expected retirement benefit/cost avoidance/risk reduction is measured or variance is owned by the benefit/business owner.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:1.contract_input_1`** — `object`

- Analyse the specific input "Architecture dependency/impact view and lifecycle state" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:1.contract_input_2`** — `object`

- Analyse the specific input "Service, configuration and asset inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:1.contract_input_3`** — `object`

- Analyse the specific input "Data retention, archive and disposal obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:1.contract_input_4`** — `object`

- Analyse the specific input "Contracts, licences and supplier exit obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:1.contract_input_5`** — `object`

- Analyse the specific input "Access, secrets, certificates and integrations inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:1.contract_input_6`** — `object`

- Analyse the specific input "Benefits/cost baseline that justified retirement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technology-lifecycle-and-decommission-manager:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technology-lifecycle-and-decommission-manager:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/technology-lifecycle-and-decommission-manager:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/technology-lifecycle-and-decommission-manager:1.irrelevant_detail`** — `object`

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
- **[ISO/IEC 20000-1:2018, Service management system requirements](https://www.iso.org/standard/70636.html)** — Service requirements, agreements, transition, operation and measurement concepts. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Technology Lifecycle and Decommission Manager:** ITIL 4 service configuration, IT asset and change enablement practices; ISO/IEC 20000-1; COBIT governance and management objectives; ArchiMate 3.2 implementation/migration and technology concepts. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Distinguish service restoration, problem resolution, authorised change and receiving service acceptance with measured outcomes.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-technology-lifecycle-and-decommission-manager-2"></a>

## Dependency impact and retirement plan

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Dependency impact and retirement plan.
- **Mandatory examples:** Identify source/target assets, data owners, versions and dependencies. Define integrity checks, fallback decision time, rollback and business continuity. Assign sequencing, capacity, reconciliation checks and acceptance criteria to each wave.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `technology-lifecycle-and-decommission-manager:2`.

**Required inputs:**

- Architecture dependency/impact view and lifecycle state
- Service, configuration and asset inventory
- Data retention, archive and disposal obligations
- Contracts, licences and supplier exit obligations
- Access, secrets, certificates and integrations inventory
- Benefits/cost baseline that justified retirement

**Specification:** `kind/role/technology-lifecycle-and-decommission-manager:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Dependency impact and retirement plan.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/migration-plan`](spec-type-migration-plan.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `migration-plan`.

Versioned migration inventory, mappings and sequenced waves with reconciliation and fallback criteria.

**Evidence accompanying the work product:**

- source/target and ownership inventory
- integrity/reconciliation and recovery checkpoints

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/technology-lifecycle-and-decommission-manager:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Dependency impact and retirement plan.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.receiving_acceptance`** — `array`

- For each receiving role (IT Asset Manager; Benefits Realisation Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.delivery_verification`** — `array`

- For the specific output 'Dependency impact and retirement plan', provide verifiable evidence satisfying: Inventory source/target versions, data classes, owners, interfaces, dependencies and mapping or transformation rules. For each wave, identify entry criteria, ordered activities, resource/window assumptions, reconciliation measures and receiving acceptance. State integrity checks, recovery points, fallback decision authority, latest safe reversal point and continuity arrangements for an unsuccessful wave. Existing source requirement: Every material inbound/outbound dependency has an owned disposition and sequencing decision. Required delivery form: Versioned migration inventory, mappings and sequenced waves with reconciliation and fallback criteria.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No retirement proceeds while an active material dependency has no migration, removal or named waiver.
- G2: Data retention/archive/destruction disposition is approved by the correct data/privacy/legal authority where required.
- G3: Identities, privileged access, secrets, certificates and integration credentials are revoked or transferred with evidence.
- G4: CMDB, asset/licence, supplier/contract, monitoring, backup and service-catalogue records reconcile to the retired state.
- G5: Architecture repository lifecycle is retired, with valid-to date and any residual cross-project obligations explicitly owned.
- G6: Expected retirement benefit/cost avoidance/risk reduction is measured or variance is owned by the benefit/business owner.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_input_1`** — `object`

- Analyse the specific input "Architecture dependency/impact view and lifecycle state" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_input_2`** — `object`

- Analyse the specific input "Service, configuration and asset inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_input_3`** — `object`

- Analyse the specific input "Data retention, archive and disposal obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_input_4`** — `object`

- Analyse the specific input "Contracts, licences and supplier exit obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_input_5`** — `object`

- Analyse the specific input "Access, secrets, certificates and integrations inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_input_6`** — `object`

- Analyse the specific input "Benefits/cost baseline that justified retirement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technology-lifecycle-and-decommission-manager:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technology-lifecycle-and-decommission-manager:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/technology-lifecycle-and-decommission-manager:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/technology-lifecycle-and-decommission-manager:2.irrelevant_detail`** — `object`

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
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC 20000-1:2018, Service management system requirements](https://www.iso.org/standard/70636.html)** — Service requirements, agreements, transition, operation and measurement concepts. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Technology Lifecycle and Decommission Manager:** ITIL 4 service configuration, IT asset and change enablement practices; ISO/IEC 20000-1; COBIT governance and management objectives; ArchiMate 3.2 implementation/migration and technology concepts. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Distinguish service restoration, problem resolution, authorised change and receiving service acceptance with measured outcomes.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-technology-lifecycle-and-decommission-manager-3"></a>

## Decommission acceptance and evidence record

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Decommission acceptance and evidence record.
- **Mandatory examples:** Define tested obligations, assurance period, sample and exclusions. Link procedures and observed results to immutable evidence and located deviations. Limit the independent conclusion to tested scope, evidence strength and unresolved findings.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `technology-lifecycle-and-decommission-manager:3`.

**Required inputs:**

- Architecture dependency/impact view and lifecycle state
- Service, configuration and asset inventory
- Data retention, archive and disposal obligations
- Contracts, licences and supplier exit obligations
- Access, secrets, certificates and integrations inventory
- Benefits/cost baseline that justified retirement

**Specification:** `kind/role/technology-lifecycle-and-decommission-manager:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Decommission acceptance and evidence record.

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

**`role/technology-lifecycle-and-decommission-manager:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Decommission acceptance and evidence record.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.receiving_acceptance`** — `array`

- For each receiving role (IT Asset Manager; Benefits Realisation Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.delivery_verification`** — `array`

- For the specific output 'Decommission acceptance and evidence record', provide verifiable evidence satisfying: State assessment objectives, criteria versions, scope, period, population, sample rationale and exclusions before drawing conclusions. For each criterion, identify procedure, sample, observed result, supporting material and located deviations; distinguish absent evidence from demonstrated failure. Bound the conclusion by coverage and limitations; list findings, severity rationale, management response, remediation owner and verification needed for closure. Existing source requirement: Shutdown, data disposition, access/secrets, CMDB/assets/licences/contracts and monitoring changes are evidenced by the responsible roles. Required delivery form: Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No retirement proceeds while an active material dependency has no migration, removal or named waiver.
- G2: Data retention/archive/destruction disposition is approved by the correct data/privacy/legal authority where required.
- G3: Identities, privileged access, secrets, certificates and integration credentials are revoked or transferred with evidence.
- G4: CMDB, asset/licence, supplier/contract, monitoring, backup and service-catalogue records reconcile to the retired state.
- G5: Architecture repository lifecycle is retired, with valid-to date and any residual cross-project obligations explicitly owned.
- G6: Expected retirement benefit/cost avoidance/risk reduction is measured or variance is owned by the benefit/business owner.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_input_1`** — `object`

- Analyse the specific input "Architecture dependency/impact view and lifecycle state" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_input_2`** — `object`

- Analyse the specific input "Service, configuration and asset inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_input_3`** — `object`

- Analyse the specific input "Data retention, archive and disposal obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_input_4`** — `object`

- Analyse the specific input "Contracts, licences and supplier exit obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_input_5`** — `object`

- Analyse the specific input "Access, secrets, certificates and integrations inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_input_6`** — `object`

- Analyse the specific input "Benefits/cost baseline that justified retirement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technology-lifecycle-and-decommission-manager:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technology-lifecycle-and-decommission-manager:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/technology-lifecycle-and-decommission-manager:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/technology-lifecycle-and-decommission-manager:3.irrelevant_detail`** — `object`

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
- **[ISO/IEC 20000-1:2018, Service management system requirements](https://www.iso.org/standard/70636.html)** — Service requirements, agreements, transition, operation and measurement concepts. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Technology Lifecycle and Decommission Manager:** ITIL 4 service configuration, IT asset and change enablement practices; ISO/IEC 20000-1; COBIT governance and management objectives; ArchiMate 3.2 implementation/migration and technology concepts. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Distinguish service restoration, problem resolution, authorised change and receiving service acceptance with measured outcomes.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-technology-lifecycle-and-decommission-manager-4"></a>

## Residual obligations and benefits closure report

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Residual obligations and benefits closure report.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `technology-lifecycle-and-decommission-manager:4`.

**Required inputs:**

- Architecture dependency/impact view and lifecycle state
- Service, configuration and asset inventory
- Data retention, archive and disposal obligations
- Contracts, licences and supplier exit obligations
- Access, secrets, certificates and integrations inventory
- Benefits/cost baseline that justified retirement

**Specification:** `kind/role/technology-lifecycle-and-decommission-manager:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Residual obligations and benefits closure report.

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

**`role/technology-lifecycle-and-decommission-manager:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Residual obligations and benefits closure report.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.receiving_acceptance`** — `array`

- For each receiving role (IT Asset Manager; Benefits Realisation Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.delivery_verification`** — `array`

- For the specific output 'Residual obligations and benefits closure report', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Existing source requirement: Remaining obligations are owned and dated; expected cost/risk/complexity benefit is measured or variance is explained. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No retirement proceeds while an active material dependency has no migration, removal or named waiver.
- G2: Data retention/archive/destruction disposition is approved by the correct data/privacy/legal authority where required.
- G3: Identities, privileged access, secrets, certificates and integration credentials are revoked or transferred with evidence.
- G4: CMDB, asset/licence, supplier/contract, monitoring, backup and service-catalogue records reconcile to the retired state.
- G5: Architecture repository lifecycle is retired, with valid-to date and any residual cross-project obligations explicitly owned.
- G6: Expected retirement benefit/cost avoidance/risk reduction is measured or variance is owned by the benefit/business owner.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_input_1`** — `object`

- Analyse the specific input "Architecture dependency/impact view and lifecycle state" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_input_2`** — `object`

- Analyse the specific input "Service, configuration and asset inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_input_3`** — `object`

- Analyse the specific input "Data retention, archive and disposal obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_input_4`** — `object`

- Analyse the specific input "Contracts, licences and supplier exit obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_input_5`** — `object`

- Analyse the specific input "Access, secrets, certificates and integrations inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_input_6`** — `object`

- Analyse the specific input "Benefits/cost baseline that justified retirement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technology-lifecycle-and-decommission-manager:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technology-lifecycle-and-decommission-manager:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/technology-lifecycle-and-decommission-manager:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/technology-lifecycle-and-decommission-manager:4.irrelevant_detail`** — `object`

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
- **[ISO/IEC 20000-1:2018, Service management system requirements](https://www.iso.org/standard/70636.html)** — Service requirements, agreements, transition, operation and measurement concepts. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Technology Lifecycle and Decommission Manager:** ITIL 4 service configuration, IT asset and change enablement practices; ISO/IEC 20000-1; COBIT governance and management objectives; ArchiMate 3.2 implementation/migration and technology concepts. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Distinguish service restoration, problem resolution, authorised change and receiving service acceptance with measured outcomes.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
