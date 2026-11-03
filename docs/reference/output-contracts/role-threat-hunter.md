<!-- JAI:OUTPUT-CONTRACTS:START -->
# Threat Hunter: output contracts

Look for adversaries that existing detection missed, using hypotheses rather than alerts

[Full catalogue](index.md)

<a id="output-threat-hunter-1"></a>

## Hunt hypotheses and methodology

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Hunt hypotheses and methodology.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `threat-hunter:1`.

**Required inputs:**

- Threat intelligence and adversary tradecraft
- Full telemetry access
- Environment and crown-jewel map
- Previous hunt results

**Specification:** `kind/role/threat-hunter:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Hunt hypotheses and methodology.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/threat-hunter:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Hunt hypotheses and methodology.

**`role/threat-hunter:1.receiving_acceptance`** — `array`

- For each receiving role (Detection Engineer; Security Analyst Tier 2), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/threat-hunter:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/threat-hunter:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/threat-hunter:1.delivery_verification`** — `array`

- For the specific output 'Hunt hypotheses and methodology', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/threat-hunter:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Nothing is declared a false positive without a recorded reason; unexplained closures hide real intrusions.
- G2: Evidence handling preserves integrity and chain of custody wherever legal or disciplinary action is conceivable.
- G3: Containment actions with business impact are authorised at the agreed level before execution.
- G4: Regulatory notification clocks (e.g. GDPR 72 hours, NIS2/DORA timelines) are assessed explicitly and the assessment is recorded.
- G5: Every hunt records its hypothesis, data sources, time range and result including negatives
- G6: a hunt with no finding still produces a documented coverage statement

**`role/threat-hunter:1.contract_input_1`** — `object`

- Analyse the specific input "Threat intelligence and adversary tradecraft" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/threat-hunter:1.contract_input_2`** — `object`

- Analyse the specific input "Full telemetry access" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/threat-hunter:1.contract_input_3`** — `object`

- Analyse the specific input "Environment and crown-jewel map" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/threat-hunter:1.contract_input_4`** — `object`

- Analyse the specific input "Previous hunt results" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/threat-hunter:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/threat-hunter:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/threat-hunter:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/threat-hunter:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/threat-hunter:1.irrelevant_detail`** — `object`

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

- **Threat Hunter:** MITRE ATT&CK; TaHiTI or PEAK hunting methodologies; pyramid of pain. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-threat-hunter-2"></a>

## hunt findings and negative results

**At a glance**

- **Purpose:** Produce and govern the role deliverable: hunt findings and negative results.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `threat-hunter:2`.

**Required inputs:**

- Threat intelligence and adversary tradecraft
- Full telemetry access
- Environment and crown-jewel map
- Previous hunt results

**Specification:** `kind/role/threat-hunter:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: hunt findings and negative results.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/threat-hunter:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: hunt findings and negative results.

**`role/threat-hunter:2.receiving_acceptance`** — `array`

- For each receiving role (Detection Engineer; Security Analyst Tier 2), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/threat-hunter:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/threat-hunter:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/threat-hunter:2.delivery_verification`** — `array`

- For the specific output 'hunt findings and negative results', provide verifiable evidence satisfying: Reproduction steps are complete enough for an independent party to confirm. Required delivery form: Finding record with reproducible evidence and risk rating.

**`role/threat-hunter:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Nothing is declared a false positive without a recorded reason; unexplained closures hide real intrusions.
- G2: Evidence handling preserves integrity and chain of custody wherever legal or disciplinary action is conceivable.
- G3: Containment actions with business impact are authorised at the agreed level before execution.
- G4: Regulatory notification clocks (e.g. GDPR 72 hours, NIS2/DORA timelines) are assessed explicitly and the assessment is recorded.
- G5: Every hunt records its hypothesis, data sources, time range and result including negatives
- G6: a hunt with no finding still produces a documented coverage statement

**`role/threat-hunter:2.contract_input_1`** — `object`

- Analyse the specific input "Threat intelligence and adversary tradecraft" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/threat-hunter:2.contract_input_2`** — `object`

- Analyse the specific input "Full telemetry access" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/threat-hunter:2.contract_input_3`** — `object`

- Analyse the specific input "Environment and crown-jewel map" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/threat-hunter:2.contract_input_4`** — `object`

- Analyse the specific input "Previous hunt results" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/threat-hunter:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/threat-hunter:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/threat-hunter:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/threat-hunter:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/threat-hunter:2.irrelevant_detail`** — `object`

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

### Role framework context

- **Threat Hunter:** MITRE ATT&CK; TaHiTI or PEAK hunting methodologies; pyramid of pain. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-threat-hunter-3"></a>

## new detection candidates

**At a glance**

- **Purpose:** Produce and govern the role deliverable: new detection candidates.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `threat-hunter:3`.

**Required inputs:**

- Threat intelligence and adversary tradecraft
- Full telemetry access
- Environment and crown-jewel map
- Previous hunt results

**Specification:** `kind/role/threat-hunter:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: new detection candidates.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/threat-hunter:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: new detection candidates.

**`role/threat-hunter:3.receiving_acceptance`** — `array`

- For each receiving role (Detection Engineer; Security Analyst Tier 2), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/threat-hunter:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/threat-hunter:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/threat-hunter:3.delivery_verification`** — `array`

- For the specific output 'new detection candidates', provide verifiable evidence satisfying: Mapped to an ATT&CK technique, with documented true- and false-positive behaviour. Required delivery form: Detection rule in version control with test cases.

**`role/threat-hunter:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Nothing is declared a false positive without a recorded reason; unexplained closures hide real intrusions.
- G2: Evidence handling preserves integrity and chain of custody wherever legal or disciplinary action is conceivable.
- G3: Containment actions with business impact are authorised at the agreed level before execution.
- G4: Regulatory notification clocks (e.g. GDPR 72 hours, NIS2/DORA timelines) are assessed explicitly and the assessment is recorded.
- G5: Every hunt records its hypothesis, data sources, time range and result including negatives
- G6: a hunt with no finding still produces a documented coverage statement

**`role/threat-hunter:3.contract_input_1`** — `object`

- Analyse the specific input "Threat intelligence and adversary tradecraft" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/threat-hunter:3.contract_input_2`** — `object`

- Analyse the specific input "Full telemetry access" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/threat-hunter:3.contract_input_3`** — `object`

- Analyse the specific input "Environment and crown-jewel map" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/threat-hunter:3.contract_input_4`** — `object`

- Analyse the specific input "Previous hunt results" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/threat-hunter:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/threat-hunter:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/threat-hunter:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/threat-hunter:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/threat-hunter:3.irrelevant_detail`** — `object`

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

### Role framework context

- **Threat Hunter:** MITRE ATT&CK; TaHiTI or PEAK hunting methodologies; pyramid of pain. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-threat-hunter-4"></a>

## visibility gap findings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: visibility gap findings.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `threat-hunter:4`.

**Required inputs:**

- Threat intelligence and adversary tradecraft
- Full telemetry access
- Environment and crown-jewel map
- Previous hunt results

**Specification:** `kind/role/threat-hunter:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: visibility gap findings.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/threat-hunter:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: visibility gap findings.

**`role/threat-hunter:4.receiving_acceptance`** — `array`

- For each receiving role (Detection Engineer; Security Analyst Tier 2), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/threat-hunter:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/threat-hunter:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/threat-hunter:4.delivery_verification`** — `array`

- For the specific output 'visibility gap findings', provide verifiable evidence satisfying: Reproduction steps are complete enough for an independent party to confirm. Required delivery form: Finding record with reproducible evidence and risk rating.

**`role/threat-hunter:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Nothing is declared a false positive without a recorded reason; unexplained closures hide real intrusions.
- G2: Evidence handling preserves integrity and chain of custody wherever legal or disciplinary action is conceivable.
- G3: Containment actions with business impact are authorised at the agreed level before execution.
- G4: Regulatory notification clocks (e.g. GDPR 72 hours, NIS2/DORA timelines) are assessed explicitly and the assessment is recorded.
- G5: Every hunt records its hypothesis, data sources, time range and result including negatives
- G6: a hunt with no finding still produces a documented coverage statement

**`role/threat-hunter:4.contract_input_1`** — `object`

- Analyse the specific input "Threat intelligence and adversary tradecraft" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/threat-hunter:4.contract_input_2`** — `object`

- Analyse the specific input "Full telemetry access" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/threat-hunter:4.contract_input_3`** — `object`

- Analyse the specific input "Environment and crown-jewel map" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/threat-hunter:4.contract_input_4`** — `object`

- Analyse the specific input "Previous hunt results" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/threat-hunter:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/threat-hunter:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/threat-hunter:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/threat-hunter:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/threat-hunter:4.irrelevant_detail`** — `object`

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

### Role framework context

- **Threat Hunter:** MITRE ATT&CK; TaHiTI or PEAK hunting methodologies; pyramid of pain. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
