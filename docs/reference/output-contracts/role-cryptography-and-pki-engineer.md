<!-- JAI:OUTPUT-CONTRACTS:START -->
# Cryptography and PKI Engineer: output contracts

Run the organisation's keys, certificates and cryptographic controls so that trust holds and nothing expires unexpectedly

[Full catalogue](index.md)

<a id="output-cryptography-and-pki-engineer-1"></a>

## PKI architecture and certificate policy

**At a glance**

- **Purpose:** Produce and govern the role deliverable: PKI architecture and certificate policy.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `cryptography-and-pki-engineer:1`.

**Required inputs:**

- Trust requirements
- Regulatory and algorithm requirements
- Certificate inventory
- HSM and key store capabilities

**Specification:** `kind/role/cryptography-and-pki-engineer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: PKI architecture and certificate policy.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/model`](spec-type-model.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `typed-semantic-model`.

Versioned typed model with stable entities, relations, constraints, provenance and selected views.

**Evidence accompanying the work product:**

- metamodel/reference/cross-view checks
- source baseline and unresolved semantic gaps

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/cryptography-and-pki-engineer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: PKI architecture and certificate policy.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:1.receiving_acceptance`** — `array`

- For each receiving role (Security Engineer; Platform Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:1.delivery_verification`** — `array`

- For the specific output 'PKI architecture and certificate policy', provide verifiable evidence satisfying: Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions. Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question. Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity. Existing source requirement: Every element traces to a driver or a quality-attribute target; no orphan elements. Required delivery form: Versioned typed model with stable entities, relations, constraints, provenance and selected views.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Every private key's custody, protection level and recovery path is documented
- G9: keys whose location is unknown are treated as compromised
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:1.contract_input_1`** — `object`

- Analyse the specific input "Trust requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:1.contract_input_2`** — `object`

- Analyse the specific input "Regulatory and algorithm requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:1.contract_input_3`** — `object`

- Analyse the specific input "Certificate inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:1.contract_input_4`** — `object`

- Analyse the specific input "HSM and key store capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/cryptography-and-pki-engineer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/cryptography-and-pki-engineer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/cryptography-and-pki-engineer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/cryptography-and-pki-engineer:1.irrelevant_detail`** — `object`

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
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Cryptography and PKI Engineer:** NIST SP 800-57; RFC 5280 and CA/Browser Forum requirements; FIPS 140-3; post-quantum migration guidance (NIST). Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Separate observed events, detection coverage, analytic hypotheses, confidence and containment/recovery evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-cryptography-and-pki-engineer-2"></a>

## key lifecycle and ceremony records

**At a glance**

- **Purpose:** Produce and govern the role deliverable: key lifecycle and ceremony records.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `cryptography-and-pki-engineer:2`.

**Required inputs:**

- Trust requirements
- Regulatory and algorithm requirements
- Certificate inventory
- HSM and key store capabilities

**Specification:** `kind/role/cryptography-and-pki-engineer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: key lifecycle and ceremony records.

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

**`role/cryptography-and-pki-engineer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: key lifecycle and ceremony records.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:2.receiving_acceptance`** — `array`

- For each receiving role (Security Engineer; Platform Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:2.delivery_verification`** — `array`

- For the specific output 'key lifecycle and ceremony records', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Every private key's custody, protection level and recovery path is documented
- G9: keys whose location is unknown are treated as compromised
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:2.contract_input_1`** — `object`

- Analyse the specific input "Trust requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:2.contract_input_2`** — `object`

- Analyse the specific input "Regulatory and algorithm requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:2.contract_input_3`** — `object`

- Analyse the specific input "Certificate inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:2.contract_input_4`** — `object`

- Analyse the specific input "HSM and key store capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/cryptography-and-pki-engineer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/cryptography-and-pki-engineer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/cryptography-and-pki-engineer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/cryptography-and-pki-engineer:2.irrelevant_detail`** — `object`

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
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Cryptography and PKI Engineer:** NIST SP 800-57; RFC 5280 and CA/Browser Forum requirements; FIPS 140-3; post-quantum migration guidance (NIST). Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Separate observed events, detection coverage, analytic hypotheses, confidence and containment/recovery evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-cryptography-and-pki-engineer-3"></a>

## certificate inventory and expiry monitoring

**At a glance**

- **Purpose:** Produce and govern the role deliverable: certificate inventory and expiry monitoring.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `cryptography-and-pki-engineer:3`.

**Required inputs:**

- Trust requirements
- Regulatory and algorithm requirements
- Certificate inventory
- HSM and key store capabilities

**Specification:** `kind/role/cryptography-and-pki-engineer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: certificate inventory and expiry monitoring.

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

**`role/cryptography-and-pki-engineer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: certificate inventory and expiry monitoring.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:3.receiving_acceptance`** — `array`

- For each receiving role (Security Engineer; Platform Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:3.delivery_verification`** — `array`

- For the specific output 'certificate inventory and expiry monitoring', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Every private key's custody, protection level and recovery path is documented
- G9: keys whose location is unknown are treated as compromised
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:3.contract_input_1`** — `object`

- Analyse the specific input "Trust requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:3.contract_input_2`** — `object`

- Analyse the specific input "Regulatory and algorithm requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:3.contract_input_3`** — `object`

- Analyse the specific input "Certificate inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:3.contract_input_4`** — `object`

- Analyse the specific input "HSM and key store capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/cryptography-and-pki-engineer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/cryptography-and-pki-engineer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/cryptography-and-pki-engineer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/cryptography-and-pki-engineer:3.irrelevant_detail`** — `object`

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
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Cryptography and PKI Engineer:** NIST SP 800-57; RFC 5280 and CA/Browser Forum requirements; FIPS 140-3; post-quantum migration guidance (NIST). Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Separate observed events, detection coverage, analytic hypotheses, confidence and containment/recovery evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-cryptography-and-pki-engineer-4"></a>

## cryptographic standard for the organisation

**At a glance**

- **Purpose:** Produce and govern the role deliverable: cryptographic standard for the organisation.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `cryptography-and-pki-engineer:4`.

**Required inputs:**

- Trust requirements
- Regulatory and algorithm requirements
- Certificate inventory
- HSM and key store capabilities

**Specification:** `kind/role/cryptography-and-pki-engineer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: cryptographic standard for the organisation.

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

**`role/cryptography-and-pki-engineer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: cryptographic standard for the organisation.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:4.receiving_acceptance`** — `array`

- For each receiving role (Security Engineer; Platform Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:4.delivery_verification`** — `array`

- For the specific output 'cryptographic standard for the organisation', provide verifiable evidence satisfying: State the exact subject, intended recipient/use, boundary, source versions and the concrete question the document answers. Provide subject-specific findings or instructions with supporting facts, assumptions, reasoning, limitations and traceable references; generic background alone is insufficient. State conclusions, decisions requested or actionable instructions, accountable recipients and completion/acceptance conditions; identify open issues explicitly. Existing source requirement: Requirements are specific, measurable and technology-explicit. Required delivery form: Purpose-specific professional document with source analysis, reasoning, conclusions and recipient actions.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Every private key's custody, protection level and recovery path is documented
- G9: keys whose location is unknown are treated as compromised
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:4.contract_input_1`** — `object`

- Analyse the specific input "Trust requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:4.contract_input_2`** — `object`

- Analyse the specific input "Regulatory and algorithm requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:4.contract_input_3`** — `object`

- Analyse the specific input "Certificate inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:4.contract_input_4`** — `object`

- Analyse the specific input "HSM and key store capabilities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/cryptography-and-pki-engineer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

**`role/cryptography-and-pki-engineer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/cryptography-and-pki-engineer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-34r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/cryptography-and-pki-engineer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/cryptography-and-pki-engineer:4.irrelevant_detail`** — `object`

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
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Cryptography and PKI Engineer:** NIST SP 800-57; RFC 5280 and CA/Browser Forum requirements; FIPS 140-3; post-quantum migration guidance (NIST). Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Separate observed events, detection coverage, analytic hypotheses, confidence and containment/recovery evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
