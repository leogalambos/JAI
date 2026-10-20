---
reference_id: example:commercial-proposal:simple
schema_version: '1.0.0'
content_revision: 2.1.0
document_kind: commercial-proposal
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/commercial-proposal
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: HFS-FAR-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Commercial and pricing proposal — Field Appointment Reliability

**Client:** Harborline Field Services · **Reference:** `HFS-FAR-COMMERCIAL_PROPOSAL-01` · **Complexity:** simple · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Operations Director and Procurement Lead.

<a id="dcs-proposed-commercial-proposal.price_basis"></a>

## Price basis, scope and authorization

This is an **illustrative commercial estimate** for Managed Scheduling and Dispatch under the scope of the accompanying technical and delivery proposals. Currency: **GBP**; rates are synthetic planning assumptions and exclude VAT/sales taxes. The supplier-services price is not equal to the programme TCO: customer effort and third-party subscriptions are separately identified.

Supplier professional services are a fixed-fee illustrative quote of £84,000 excluding taxes; estimated SaaS licensing £42,000 over 36 months and £14,000 customer internal transition are non-supplier items. The three-year indicative programme cost is £140,000, not a supplier invoice. No party is bound by these terms until the existing authorized commercial/legal approvals and an executed contractual instrument.

<a id="dcs-proposed-commercial-proposal.cost_breakdown"></a>

## Itemized effort, third-party and total-cost reconciliation

| Workstream | Model basis | Illustrative cost |
| --- | --- | --- |
| Discovery and design | 15 days × £700/day | £10,500 |
| Configuration and workflow | 55 days × £700/day | £38,500 |
| Connector and assurance | 32 days × £700/day | £22,400 |
| Testing and handover | 18 days × £700/day | £12,600 |
| Supplier professional services total | Calculated from person-days | £84,000 |
| Indicative licences / platform (36 months) | Separate third-party estimate | £42,000 |
| Client internal effort / transition | Not part of supplier invoice | £14,000 |
| Indicative programme envelope | Services + third-party + internal | £140,000 |


**Arithmetic control:** the person-days multiplied by their rates must sum to £84,000; supplier services + platform assumptions + client internal effort must sum to **£140,000**. Every alternative scope must have its own table, not change totals invisibly.

Pricing excludes legal opinion fees, taxes, financing and change requests unless separately confirmed. Third-party estimates are not supplier-priced products, guarantees or order forms.

<a id="dcs-proposed-commercial-proposal.assumptions_exclusions"></a>

## Inclusions, pricing dependencies and exclusions

The supplier rate includes engineering and planned QA effort for the work packages described in the associated delivery proposal. Risks from client delays, incomplete data migration or altered regulatory requirements require impact assessment; these are not blanket grounds for arbitrary price increases.

- **A1:** Client supplies authorized SaaS tenancy, identity integration owner and test access by W2.
- **A2:** Client makes available 2 dispatch SMEs and a decision owner within 2 working days of a material question.
- **A3:** No unexpected data transfer or licensing restriction invalidates the proposed SaaS solution.

Exclusions:
- Beside-the-scenes SaaS supplier platform changes
- Historical data cleansing beyond agreed fields
- 24×7 support subscription unless separately contracted
- Production endpoint credentials in any proposal deliverable

Procurement must verify intellectual property rights, licence measurements, supplier exit costs, support windows, subcontractor access and personal data processing obligations.

<a id="dcs-proposed-commercial-proposal.payment_terms"></a>

## Illustrative milestone payments and invoicing protections

Milestone payments apply only to the **supplier-services subtotal**, not to third-party or internal amounts. Proposed schedule: 15% upon accepted discovery/design baseline; 35% upon accepted platform and integration build; 30% upon independent test and controlled pilot acceptance; 20% upon receiving service-owner handover.

| Invoice milestone | Percent of supplier fee | Illustrative amount | Condition |
| --- | --- | --- | --- |
| Discovery baseline | 15% | £12,600 | Written acceptance of scoped requirements |
| Build milestone | 35% | £29,400 | Versioned source/config and integration evidence |
| Test / pilot | 30% | £25,200 | Defect disposition and test evidence |
| Operational handover | 20% | £16,800 | Service owner receives artifacts and responsibilities |


All payment conditions remain subject to negotiation, credit terms and applicable law. A delivery claim without corresponding evidence must not automatically trigger invoice acceptance.

<a id="dcs-proposed-commercial-proposal.commercial_risks"></a>

## Variance, optional services and commercial risk treatment

| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Duplicate webhook updates | Idempotency by booking key; reconciliation | Application Lead |
| R2 | SaaS outage and export limitations | Daily verified export and offline dispatch procedure | Service Owner |
| R3 | Incomplete frontline adoption | Supervisor-assisted pilot and training | Business Sponsor |


**Explicit optional scope:** Optional identity/control uplift £18,000 fixed illustrative supplier fee, separate from the £84,000 core professional-services fee. Optional monitoring £2,400 per month plus £4,500 onboarding; initial 12-month service estimate £33,300, excluded from the base programme investment. These are separate offers. They are **not included** in the base supplier fee or base programme envelope and must not be added without a formal scope and cost decision.

Quote validity for this illustrative sample is 30 calendar days after a hypothetical date of issue; no actual price hold exists. Specify inflation/indexation only after client procurement agrees the indices, cap and effective date. Price a change against an approved baseline and record new dates, impacts and acceptance predicates.

<a id="dcs-proposed-commercial-proposal.approval_boundary"></a>

## Commercial approval, signature and validity

Commercial negotiation is authorized only by the designated delegated authority. Prior to offer execution, Finance verifies the cost model, Procurement confirms supplier/procurement constraints, Legal approves contract language, and relevant risk owners accept residual exposures within their authority.

Required sign-off record contains party identifiers, versioned proposal/SoW, agreed price schedule, exceptions, offer-validity date and formal signatures. Do not imply any customer reference, guaranteed savings or regulatory certification from this demonstration.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `HFS-FAR-E-SCOPE` (signed requirements), `HFS-FAR-E-COST` (validated rate-card and cost owner), `HFS-FAR-E-SEC` (risk/legal applicability), and `HFS-FAR-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `HFS-FAR`; **document kind:** `commercial-proposal`; **scenario:** `simple`.
