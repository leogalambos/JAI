---
reference_id: example:commercial-proposal:medium
schema_version: '1.0.0'
content_revision: 2.3.0
document_kind: commercial-proposal
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/commercial-proposal
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: MRG-OEI-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Commercial and pricing proposal — Order Event Integration

**Client:** Meridian Retail Group · **Reference:** `MRG-OEI-COMMERCIAL_PROPOSAL-01` · **Complexity:** medium · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Architecture Review Board, Finance Partner and Procurement.

<a id="dcs-proposed-commercial-proposal.price_basis"></a>

## Price basis, scope and authorization

This is an **illustrative commercial estimate** for European Commerce-to-ERP Event Backbone under the scope of the accompanying technical and delivery proposals. Currency: **EUR**; rates are synthetic planning assumptions and exclude VAT/sales taxes. The supplier-services price is not equal to the programme TCO: customer effort and third-party subscriptions are separately identified.

Supplier delivery services €780,000 (780 person-days at illustrative blended €1,000/day). Separately estimated managed platform/subscriptions €270,000 over three years and client internal transition €200,000 yield an indicative three-year programme envelope of €1,250,000. No party is bound by these terms until the existing authorized commercial/legal approvals and an executed contractual instrument.

<a id="dcs-proposed-commercial-proposal.cost_breakdown"></a>

## Itemized effort, third-party and total-cost reconciliation

| Workstream | Model basis | Illustrative cost |
| --- | --- | --- |
| Discovery and source analysis | 90 days × €1,000/day | €90,000 |
| Architecture and platform | 120 days × €1,000/day | €120,000 |
| Integration implementation | 360 days × €1,000/day | €360,000 |
| Testing and migration | 130 days × €1,000/day | €130,000 |
| Readiness and transfer | 80 days × €1,000/day | €80,000 |
| Supplier professional services total | Calculated from person-days | €780,000 |
| Indicative licences / platform (36 months) | Separate third-party estimate | €270,000 |
| Client internal effort / transition | Not part of supplier invoice | €200,000 |
| Indicative programme envelope | Services + third-party + internal | €1,250,000 |


**Arithmetic control:** the person-days multiplied by their rates must sum to €780,000; supplier services + platform assumptions + client internal effort must sum to **€1,250,000**. Every alternative scope must have its own table, not change totals invisibly.

Pricing excludes legal opinion fees, taxes, financing and change requests unless separately confirmed. Third-party estimates are not supplier-priced products, guarantees or order forms.

<a id="dcs-proposed-commercial-proposal.assumptions_exclusions"></a>

## Inclusions, pricing dependencies and exclusions

The supplier rate includes engineering and planned QA effort for the work packages described in the associated delivery proposal. Risks from client delays, incomplete data migration or altered regulatory requirements require impact assessment; these are not blanket grounds for arbitrary price increases.

- **A1:** Client supplies sample outbox events, ERP non-production interfaces and named market owners by W4.
- **A2:** Each market approves data routing and customer field minimisation before its release.
- **A3:** No fundamental vendor contract restriction prevents the agreed event delivery architecture.

Exclusions:
- Replacement of the ERP core
- Transformation of downstream logistics vendor platforms
- Country-specific statutory legal opinions
- Perpetual guarantees of processing exactly once at transport level

Procurement must verify intellectual property rights, licence measurements, supplier exit costs, support windows, subcontractor access and personal data processing obligations.

<a id="dcs-proposed-commercial-proposal.payment_terms"></a>

## Illustrative milestone payments and invoicing protections

Milestone payments apply only to the **supplier-services subtotal**, not to third-party or internal amounts. Proposed schedule: 15% upon accepted discovery/design baseline; 35% upon accepted platform and integration build; 30% upon independent test and controlled pilot acceptance; 20% upon receiving service-owner handover.

| Invoice milestone | Percent of supplier fee | Illustrative amount | Condition |
| --- | --- | --- | --- |
| Discovery baseline | 15% | €117,000 | Written acceptance of scoped requirements |
| Build milestone | 35% | €273,000 | Versioned source/config and integration evidence |
| Test / pilot | 30% | €234,000 | Defect disposition and test evidence |
| Operational handover | 20% | €156,000 | Service owner receives artifacts and responsibilities |


All payment conditions remain subject to negotiation, credit terms and applicable law. A delivery claim without corresponding evidence must not automatically trigger invoice acceptance.

<a id="dcs-proposed-commercial-proposal.commercial_risks"></a>

## Variance, optional services and commercial risk treatment

| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Duplicate/out-of-order events | Outbox, stable idempotency keys, replay and exception reconciliation | Integration Architect |
| R2 | Incorrect country routing of personal data | Region tagging and negative policy tests | Privacy Lead |
| R3 | Market cutover and shared broker saturation | Two-market canary, back-pressure and capacity stress tests | Operations Manager |


**Explicit optional scope:** Optional zero-trust design and control-verification work package €135,000 (90 days at €1,500), not included in the €780,000 base estimate. Optional managed integration-security monitoring: €15,000/month plus €45,000 onboarding; 12-month illustrative estimate €225,000, separate from core delivery and platform costs. These are separate offers. They are **not included** in the base supplier fee or base programme envelope and must not be added without a formal scope and cost decision.

Quote validity for this illustrative sample is 30 calendar days after a hypothetical date of issue; no actual price hold exists. Specify inflation/indexation only after client procurement agrees the indices, cap and effective date. Price a change against an approved baseline and record new dates, impacts and acceptance predicates.

<a id="dcs-proposed-commercial-proposal.approval_boundary"></a>

## Commercial approval, signature and validity

Commercial negotiation is authorized only by the designated delegated authority. Prior to offer execution, Finance verifies the cost model, Procurement confirms supplier/procurement constraints, Legal approves contract language, and relevant risk owners accept residual exposures within their authority.

Required sign-off record contains party identifiers, versioned proposal/SoW, agreed price schedule, exceptions, offer-validity date and formal signatures. Do not imply any customer reference, guaranteed savings or regulatory certification from this demonstration.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `MRG-OEI-E-SCOPE` (signed requirements), `MRG-OEI-E-COST` (validated rate-card and cost owner), `MRG-OEI-E-SEC` (risk/legal applicability), and `MRG-OEI-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `MRG-OEI`; **document kind:** `commercial-proposal`; **scenario:** `medium`.

## Evidence-led expert review supplement (v2.3.0)

> **Editorial status:** reviewer-designed example content for the fictional `MRG-OEI-PROPOSAL-EXAMPLE` context. No underlying customer system, security test, supplier quote or sign-off was inspected. This section is an illustrative professional decision aid, not completed assurance.

### Context-specific decision and evidence matrix

| Evaluation object | Explicit verification question | Evidence to request | Required disposition |
|---|---|---|---|
| Supplier vs third-party vs client costs | Is this statement supported for `MRG-OEI-PROPOSAL-EXAMPLE` by a source-controlled input with an identified owner? | Source record, scope identifier, timestamp and version | OPEN until attributable evidence exists |
| Volume × rate reconciled to total | Is the claim testable against a falsifiable success or failure criterion? | Expected/observed values and independent review result | NOT_EXECUTED if no actual test or review |
| Contractual assumptions and validity | Does the proposed conclusion change a decision, cost, permission or release condition? | Approval or refusal recorded in the existing JAI authority mechanism | PENDING, never inferred approval |

### Technical expert challenge — customer commitment integrity

Trace the exact customer-requested outcome to a separately priced deliverable and explicit acceptance test; classify any unsupported requirement as an assumption or clarification. For **commercial-proposal**, the reviewer should actively challenge **supplier vs third-party vs client costs** and **volume × rate reconciled to total**. A plausible narrative without attributable source material remains a proposed hypothesis.

### Management challenge — contractual acceptance boundary

Distinguish indicative estimate, binding price, third-party pass-through and client internal cost. Change in scope requires a defined change-order rather than implied free delivery. The accountable party for this illustrative acceptance is **Bid Manager / Commercial Owner**, not an unspecified project team. Required management decision: **DEFER external commitment or release when a material evidence gap remains**. Create a tracked action with named owner, due date, acceptance predicate and escalation path; none is asserted as completed here.

### Presentation and reader decision check

**Decision headline:** evidence is insufficient for an unconditional approval; the current proposal is fit for discussion and refinement only. **What matters now:** supplier vs third-party vs client costs, volume × rate reconciled to total, and contractual assumptions and validity. **Next step:** obtain original evidence, reconcile contradictory figures and issue an updated, independently reviewed version. Use descriptive heading hierarchy, non-colour-only statuses, concise table labels, explicit units and a separate annex for technical detail. Do not bury exceptions below a visually positive summary.

### Decision-oriented quality acceptance

| Test | Expected finding for this fictional example | Decision implication |
|---|---|---|
| Source fidelity | Unverified example facts are marked synthetic or assumed | No production factual claim |
| Cross-artifact consistency | IDs, scope, prices, controls and status must reconcile with linked artifacts | Any substantive mismatch requires correction |
| Independent review | No real reviewer evidence is provided | Human-approved status remains **false** |
| Publication quality | Headings, tables, links and any figures must render without truncation; validate when a renderer is present | Missing renderer = NOT_EXECUTED, not PASS |

