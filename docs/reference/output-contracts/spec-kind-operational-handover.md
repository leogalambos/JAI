<!-- JAI:OUTPUT-CONTRACTS:START -->
# kind/operational-handover

**Specification:** `kind/operational-handover`; **content version:** `1.2.0`.

Accept service responsibility or require remediation before operational transfer.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `service-handover`.

Versioned service boundary, operational inventory and receiving responsibilities with readiness disposition.

**Evidence accompanying the work product:**

- actual monitoring/recovery/security/support readiness
- recipient acceptance and unresolved obligations

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`operational-handover.service_boundary`** — `object`

- Define the service, service owner, support teams, assets and responsibility boundaries.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`operational-handover.readiness_evidence`** — `array`

- Link monitoring, backup, recovery, capacity and security readiness criteria to observed evidence.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`operational-handover.support_arrangements`** — `object`

- Specify support hours, contacts, escalation paths, service levels and access prerequisites.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`operational-handover.handover_inventory`** — `array`

- Identify versioned runbooks, configuration, known errors, training and dependency records.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`operational-handover.acceptance_decision`** — `object`

- Record receiving operations acceptance, unresolved risks, action owners and authority status.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`operational-handover.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify personal-data flows, lawful handling constraints, minimisation and review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`operational-handover.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Trace each applicable regulatory obligation to scope, evidence and competent interpretation; exceptions cannot waive law.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`operational-handover.technical_annex`** — `object`

- Include deeper calculations or technical detail only when linked to a reader need.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`operational-handover.unsupported_material_claim`** — `object`

- Never state a material conclusion as established without evidence or explicit uncertainty.

### Content to omit unless justified

**`operational-handover.irrelevant_detail`** — `object`

- Remove detail that does not support the stated purpose or a referenced annex.

**`operational-handover.duplicate_claim`** — `object`

- Reference an existing claim instead of repeating it without new analytical value.

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
  "pages": {
    "metric": "pages",
    "calibration_basis": "Modality-specific information coverage; numerical envelopes require approved enterprise calibration.",
    "minimum_is_quality_gate": false,
    "calibration_status": "synthetic-only",
    "allowance_rules": [
      "Document complexity and audience need; excess requires review, not automatic rejection."
    ],
    "annex_rules": [
      "Reference canonical detail rather than repeat it."
    ],
    "target": [
      4,
      12
    ],
    "soft_max": 16,
    "basis": "Indicative pilot intervals from approved implementation direction; assurance and handover use proposed evidence-pack intervals requiring calibration.",
    "exclude": [
      "controlled_annexes",
      "source_register"
    ],
    "target_is_informational": true
  }
}
```

### Professional sources and their limits

- **[ISO/IEC 20000-1:2018, Service management system requirements](https://www.iso.org/standard/70636.html)** — Service requirements, agreements, transition, operation and measurement concepts. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[HM Treasury, The Green Book](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)** — Options, appraisal, costs, benefits, risk, uncertainty and evaluation; used as a practice reference outside its own jurisdiction. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Implementation Consultant:** vendor implementation methodology; PRINCE2 or equivalent for the engagement; data migration practice. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Expose sourcing/pricing assumptions, obligations, economic sensitivities, acceptance responsibilities and exit conditions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
