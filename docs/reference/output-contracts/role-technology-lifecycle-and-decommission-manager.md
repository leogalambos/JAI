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

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/technology-lifecycle-and-decommission-manager:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Technology lifecycle and decommission assessment.

**`role/technology-lifecycle-and-decommission-manager:1.receiving_acceptance`** — `array`

- For each receiving role (IT Asset Manager; Benefits Realisation Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/technology-lifecycle-and-decommission-manager:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/technology-lifecycle-and-decommission-manager:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/technology-lifecycle-and-decommission-manager:1.delivery_verification`** — `array`

- For the specific output 'Technology lifecycle and decommission assessment', provide verifiable evidence satisfying: Scope, owner, lifecycle state, dependencies, obligations and authority are explicit and current. Required delivery form: Evidence-backed assessment with repository IDs and systems-of-record references.

**`role/technology-lifecycle-and-decommission-manager:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No retirement proceeds while an active material dependency has no migration, removal or named waiver.
- G2: Data retention/archive/destruction disposition is approved by the correct data/privacy/legal authority where required.
- G3: Identities, privileged access, secrets, certificates and integration credentials are revoked or transferred with evidence.
- G4: CMDB, asset/licence, supplier/contract, monitoring, backup and service-catalogue records reconcile to the retired state.
- G5: Architecture repository lifecycle is retired, with valid-to date and any residual cross-project obligations explicitly owned.
- G6: Expected retirement benefit/cost avoidance/risk reduction is measured or variance is owned by the benefit/business owner.

**`role/technology-lifecycle-and-decommission-manager:1.contract_input_1`** — `object`

- Analyse the specific input "Architecture dependency/impact view and lifecycle state" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/technology-lifecycle-and-decommission-manager:1.contract_input_2`** — `object`

- Analyse the specific input "Service, configuration and asset inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/technology-lifecycle-and-decommission-manager:1.contract_input_3`** — `object`

- Analyse the specific input "Data retention, archive and disposal obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/technology-lifecycle-and-decommission-manager:1.contract_input_4`** — `object`

- Analyse the specific input "Contracts, licences and supplier exit obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/technology-lifecycle-and-decommission-manager:1.contract_input_5`** — `object`

- Analyse the specific input "Access, secrets, certificates and integrations inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/technology-lifecycle-and-decommission-manager:1.contract_input_6`** — `object`

- Analyse the specific input "Benefits/cost baseline that justified retirement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/technology-lifecycle-and-decommission-manager:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/technology-lifecycle-and-decommission-manager:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/technology-lifecycle-and-decommission-manager:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

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

### Role framework context

- **Technology Lifecycle and Decommission Manager:** ITIL 4 service configuration, IT asset and change enablement practices; ISO/IEC 20000-1; COBIT governance and management objectives; ArchiMate 3.2 implementation/migration and technology concepts. Canonical role context; not proof that every listed framework applies to this output.


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

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/technology-lifecycle-and-decommission-manager:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Dependency impact and retirement plan.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.receiving_acceptance`** — `array`

- For each receiving role (IT Asset Manager; Benefits Realisation Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.delivery_verification`** — `array`

- For the specific output 'Dependency impact and retirement plan', provide verifiable evidence satisfying: Every material inbound/outbound dependency has an owned disposition and sequencing decision. Required delivery form: Versioned plan plus architecture dependency/view set and migration/disposition actions.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No retirement proceeds while an active material dependency has no migration, removal or named waiver.
- G2: Data retention/archive/destruction disposition is approved by the correct data/privacy/legal authority where required.
- G3: Identities, privileged access, secrets, certificates and integration credentials are revoked or transferred with evidence.
- G4: CMDB, asset/licence, supplier/contract, monitoring, backup and service-catalogue records reconcile to the retired state.
- G5: Architecture repository lifecycle is retired, with valid-to date and any residual cross-project obligations explicitly owned.
- G6: Expected retirement benefit/cost avoidance/risk reduction is measured or variance is owned by the benefit/business owner.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_input_1`** — `object`

- Analyse the specific input "Architecture dependency/impact view and lifecycle state" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_input_2`** — `object`

- Analyse the specific input "Service, configuration and asset inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_input_3`** — `object`

- Analyse the specific input "Data retention, archive and disposal obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_input_4`** — `object`

- Analyse the specific input "Contracts, licences and supplier exit obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_input_5`** — `object`

- Analyse the specific input "Access, secrets, certificates and integrations inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.contract_input_6`** — `object`

- Analyse the specific input "Benefits/cost baseline that justified retirement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technology-lifecycle-and-decommission-manager:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technology-lifecycle-and-decommission-manager:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

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

### Role framework context

- **Technology Lifecycle and Decommission Manager:** ITIL 4 service configuration, IT asset and change enablement practices; ISO/IEC 20000-1; COBIT governance and management objectives; ArchiMate 3.2 implementation/migration and technology concepts. Canonical role context; not proof that every listed framework applies to this output.


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

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/technology-lifecycle-and-decommission-manager:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Decommission acceptance and evidence record.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.receiving_acceptance`** — `array`

- For each receiving role (IT Asset Manager; Benefits Realisation Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.delivery_verification`** — `array`

- For the specific output 'Decommission acceptance and evidence record', provide verifiable evidence satisfying: Shutdown, data disposition, access/secrets, CMDB/assets/licences/contracts and monitoring changes are evidenced by the responsible roles. Required delivery form: Traceable evidence pack/register.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No retirement proceeds while an active material dependency has no migration, removal or named waiver.
- G2: Data retention/archive/destruction disposition is approved by the correct data/privacy/legal authority where required.
- G3: Identities, privileged access, secrets, certificates and integration credentials are revoked or transferred with evidence.
- G4: CMDB, asset/licence, supplier/contract, monitoring, backup and service-catalogue records reconcile to the retired state.
- G5: Architecture repository lifecycle is retired, with valid-to date and any residual cross-project obligations explicitly owned.
- G6: Expected retirement benefit/cost avoidance/risk reduction is measured or variance is owned by the benefit/business owner.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_input_1`** — `object`

- Analyse the specific input "Architecture dependency/impact view and lifecycle state" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_input_2`** — `object`

- Analyse the specific input "Service, configuration and asset inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_input_3`** — `object`

- Analyse the specific input "Data retention, archive and disposal obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_input_4`** — `object`

- Analyse the specific input "Contracts, licences and supplier exit obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_input_5`** — `object`

- Analyse the specific input "Access, secrets, certificates and integrations inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.contract_input_6`** — `object`

- Analyse the specific input "Benefits/cost baseline that justified retirement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technology-lifecycle-and-decommission-manager:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technology-lifecycle-and-decommission-manager:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

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

### Role framework context

- **Technology Lifecycle and Decommission Manager:** ITIL 4 service configuration, IT asset and change enablement practices; ISO/IEC 20000-1; COBIT governance and management objectives; ArchiMate 3.2 implementation/migration and technology concepts. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-technology-lifecycle-and-decommission-manager-4"></a>

## Residual obligations and benefits closure report

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Residual obligations and benefits closure report.
- **Mandatory examples:** Identify the specific choice, accountable authority and decision deadline. Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation. Compare viable options including the do-nothing baseline against common criteria.
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
- [`type/decision-paper`](spec-type-decision-paper.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/technology-lifecycle-and-decommission-manager:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Residual obligations and benefits closure report.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.receiving_acceptance`** — `array`

- For each receiving role (IT Asset Manager; Benefits Realisation Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.delivery_verification`** — `array`

- For the specific output 'Residual obligations and benefits closure report', provide verifiable evidence satisfying: Remaining obligations are owned and dated; expected cost/risk/complexity benefit is measured or variance is explained. Required delivery form: Decision-ready closure report.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No retirement proceeds while an active material dependency has no migration, removal or named waiver.
- G2: Data retention/archive/destruction disposition is approved by the correct data/privacy/legal authority where required.
- G3: Identities, privileged access, secrets, certificates and integration credentials are revoked or transferred with evidence.
- G4: CMDB, asset/licence, supplier/contract, monitoring, backup and service-catalogue records reconcile to the retired state.
- G5: Architecture repository lifecycle is retired, with valid-to date and any residual cross-project obligations explicitly owned.
- G6: Expected retirement benefit/cost avoidance/risk reduction is measured or variance is owned by the benefit/business owner.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_input_1`** — `object`

- Analyse the specific input "Architecture dependency/impact view and lifecycle state" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_input_2`** — `object`

- Analyse the specific input "Service, configuration and asset inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_input_3`** — `object`

- Analyse the specific input "Data retention, archive and disposal obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_input_4`** — `object`

- Analyse the specific input "Contracts, licences and supplier exit obligations" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_input_5`** — `object`

- Analyse the specific input "Access, secrets, certificates and integrations inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.contract_input_6`** — `object`

- Analyse the specific input "Benefits/cost baseline that justified retirement" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/technology-lifecycle-and-decommission-manager:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/technology-lifecycle-and-decommission-manager:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/technology-lifecycle-and-decommission-manager:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

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

- **[HM Treasury, The Green Book](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)** — Options, appraisal, costs, benefits, risk, uncertainty and evaluation; used as a practice reference outside its own jurisdiction. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Technology Lifecycle and Decommission Manager:** ITIL 4 service configuration, IT asset and change enablement practices; ISO/IEC 20000-1; COBIT governance and management objectives; ArchiMate 3.2 implementation/migration and technology concepts. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
