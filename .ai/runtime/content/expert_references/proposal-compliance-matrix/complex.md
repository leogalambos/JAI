---
reference_id: example:proposal-compliance-matrix:complex
schema_version: '1.0.0'
content_revision: 2.1.0
document_kind: proposal-compliance-matrix
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/proposal-compliance-matrix
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: OPG-RSM-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# RFP requirement and response traceability matrix — Regulated Settlement Modernisation

**Client:** Orion Payments Group · **Reference:** `OPG-RSM-PROPOSAL_COMPLIANCE_MATRIX-01` · **Complexity:** complex · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Group Investment Committee, Payments Architecture Board, Risk and Legal Authorities.

<a id="dcs-proposed-proposal-compliance-matrix.requirement_source"></a>

## Controlled source basis and classification vocabulary

The source catalogue `OPG-RSM-RFP-2027-01` is **invented for this worked example**. In a live tender, ingest the exact customer requirement document with an immutable revision and clause location, then preserve customer wording separately from the supplier interpretation. Scope: Multi-Jurisdiction Settlement Control and Resilience for Orion Payments Group.

Allowed statuses: COMPLY—EVIDENCED, COMPLY—PROPOSED, CONDITIONAL, DEVIATION, NON-COMPLIANT, NOT APPLICABLE WITH RATIONALE, and NOT ASSESSED. **A design proposal without a test does not become COMPLY—EVIDENCED.**

<a id="dcs-proposed-proposal-compliance-matrix.response_classification"></a>

## Response classification, objective test and ownership

Each row is independently decidable. The matrix must express the supplier claim and its evidence limitation, not merely repeat 'we comply'.

| ID | Customer request | Response status | Proposed answer |
| --- | --- | --- | --- |
| REQ-01 | Describe target business outcome and baseline | Comply—subject to baseline validation | maintain traceable settlement instruction lineage and timely cut-off processing with zero unexplained ledger imbalance; baseline requires client source records |
| REQ-02 | Supply technical architecture and integration contracts | Comply—proposed | regional phased settlement replacement, jurisdiction policy gateway, append-only instruction journal, separately reconciled parallel ledger and strictly controlled recovery; exact interface schema pending discovery |
| REQ-03 | Provide data privacy and security assurance | Conditional—client authority required | Applicable payment, resilience, outsourcing, data-residency, privacy and reporting obligations must be determined for each legal entity and jurisdiction by competent client authority before binding commitments |
| REQ-04 | Prove application or transaction integrity | Conditional—test not executed | Design for Critical monthly availability but verification is pending |
| REQ-05 | Describe recovery and continuity | Conditional—exercise required | 99.95% monthly availability for critical processing; p95 acknowledgement under 450 ms excluding third-party network; RTO 30 minutes / RPO 5 minutes |
| REQ-06 | Provide schedule and acceptance milestones | Comply—planning | 18 months subject to dependencies |
| REQ-07 | Provide consistent commercial breakdown | Comply—illustrative model | Supplier €4,500,000; total envelope €6,800,000 |
| REQ-08 | State exclusions, dependencies and supplier responsibilities | Comply—proposed | RACI, SoW and exclusion schedule; signature pending |
| REQ-09 | Demonstrate named production support and skills transfer | Conditional—client staffing pending | Proposed handover and receiving owner; roster not validated |
| REQ-10 | Provide independent evidence of regulatory/certification claims | Not claimed / not evidenced | No certification, external audit or legal opinion is asserted |


The proposed supplier response is conditional on client baseline validation; a change to the underlying RFP version invalidates the corresponding matrix rows until re-review.

<a id="dcs-proposed-proposal-compliance-matrix.evidence_mapping"></a>

## Evidence register and receiving review authority

| Requirement | Evidence needed | Current status | Reviewer |
| --- | --- | --- | --- |
| REQ-01 | Verified requirement baseline | PROPOSED | Procurement / accountable owner |
| REQ-02 | Approved architecture diagram and interface contract | PROPOSED / NOT EXECUTED | Architecture and engineering |
| REQ-03 | Executed control test / legal evidence | PROPOSED / NOT EXECUTED | Privacy/Security/Risk |
| REQ-04 | Executed control test / legal evidence | PROPOSED / NOT EXECUTED | Privacy/Security/Risk |
| REQ-05 | Executed control test / legal evidence | PROPOSED / NOT EXECUTED | Privacy/Security/Risk |
| REQ-06 | Signed owner-accepted schedule / response | PROPOSED | Procurement / accountable owner |
| REQ-07 | Signed owner-accepted schedule / response | PROPOSED | Procurement / accountable owner |
| REQ-08 | Signed owner-accepted schedule / response | PROPOSED | Procurement / accountable owner |
| REQ-09 | Signed owner-accepted schedule / response | PROPOSED | Procurement / accountable owner |
| REQ-10 | Signed owner-accepted schedule / response | PROPOSED | Procurement / accountable owner |


An evidence link must include source artifact identity, version/hash and reviewing authority; an invented or inaccessible evidence ID cannot close a customer requirement.

<a id="dcs-proposed-proposal-compliance-matrix.exceptions_dependencies"></a>

## Gaps, non-negotiable controls and corrective actions

| ID | Exposure and reason it matters | Treatment and evidence gate | Owner |
| --- | --- | --- | --- |
| R1 | Settlement-finality mismatch or irreversibility | Parallel ledger and dual-control compensating workflow | Treasury Control Owner |
| R2 | Cross-border processing outside authorized legal scope | Per-entity jurisdiction rules and independent privacy/legal approval | Group Compliance |
| R3 | Correlated regional or identity-plane outage | Failure-domain separation, cut-off-safe contingency | Resilience Architect |
| R4 | Unrecoverable reconciliation evidence | Append-only signed checkpoints and independently tested evidence chain | Assurance Lead |


Mandatory controls with missing legal or recovery evidence remain CONDITIONALLY MET or NOT ASSESSED. If the client RFP prohibits conditional responses, the owner must select NON-COMPLIANT rather than suppressing the limitation. Each exception has: materiality, client clarification reference, accountable owner, planned evidence, target date and decision gate.

Data obligations: Applicable payment, resilience, outsourcing, data-residency, privacy and reporting obligations must be determined for each legal entity and jurisdiction by competent client authority before binding commitments. Proposed commercial total: €6,800,000, of which supplier fee €4,500,000. If an added compliance requirement changes effort, update the pricing schedule through explicit change control.

<a id="dcs-proposed-proposal-compliance-matrix.closure_governance"></a>

## Completeness, amendment handling and final sign-off

The release test for a completed response matrix is: every customer requirement in the selected revision has exactly one substantive response, a truthful classification, a documented evidence state and an authorized reviewer. No orphan requirements; no duplicate contradictory statuses; no implicit green for missing documents.

**Requested decision:** conditional clarification / rework, not a final compliance sign-off. Future approval must be recorded through existing JAI L0 and customer procurement processes. An amendatory RFP question changes the evidence and scope matrix and may invalidate proposal and SoW assumptions.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `OPG-RSM-E-SCOPE` (signed requirements), `OPG-RSM-E-COST` (validated rate-card and cost owner), `OPG-RSM-E-SEC` (risk/legal applicability), and `OPG-RSM-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `OPG-RSM`; **document kind:** `proposal-compliance-matrix`; **scenario:** `complex`.
