---
reference_id: example:risk-assessment:complex
schema_version: '1.0.0'
document_kind: risk-assessment
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/risk-assessment
approval_status: not-human-approved
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Orion Payments Group · Regulated Settlement Modernisation · `OPG-RSM` · COMPLEX complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Group Payments Executive. **Scope:** multi-jurisdiction mission-critical transformation with regulatory obligations determined per entity.

# Information-security and service risk assessment — Regulated Settlement Modernisation

<a id="dcs-risk-assessment.assessment_scope"></a>
## Assessment scope and assets at risk

Risk assessment `OPG-RSM-RA-01` covers cross-border settlement instruction processing and the supporting boundary channel gateways, policy service, event ledger, settlement orchestration, regional connectors, immutable evidence store and resilience sites. Business asset: reliable fulfilment of achieve complete instruction lineage and timely settlement at defined cut-offs with zero unexplained financial imbalance; information asset: payer/payee identifiers, transaction metadata and restricted operational records; technology assets: integration interfaces, identity plane, state stores and telemetry. Exposure: regulated critical payment processing with material third-party dependencies.

Assessment owner is Enterprise Financial Risk Officer; independent reviewer remains unassigned. This document is an illustrative analysis only; real owners must establish the applicable legal/regulatory obligations for each operating location.

<a id="dcs-risk-assessment.scoring_method"></a>
## Scoring method and decision appetite

Working qualitative 5×5 method: likelihood 1 (rare) to 5 (frequent); impact 1 (negligible) to 5 (critical interruption, compromise or liability); product gives a **relative prioritisation score**, not a probabilistic annual-loss estimate. Bands: 1–5 low, 6–10 moderate, 11–15 high, 16–25 severe.

Risk appetite is assumed for this synthetic exercise: no severe untreated risk may move to production; high residual risk requires named executive acceptance and documented compensating controls. The actual organisation must substitute its approved appetite and scoring rubric; regulatory breaches cannot be made acceptable by selecting a low number.

<a id="dcs-risk-assessment.risk_scenarios"></a>
## Threat-event scenarios and supporting assumptions

The critical initiating events include settlement finality mismatch, cross-border data movement and correlated regional failure, operator error and malicious misuse of privileged interfaces. A failure may cause loss or duplication of business records, unavailable processing or unauthorised disclosure. Threat and control effectiveness are hypotheses; no production penetration test, audit or outage history was available for the fictional organisation.

Evidence obligations: service-dependency map `OPG-RSM-E-MAP`, access review `OPG-RSM-E-IAM`, recovery exercises `OPG-RSM-E-REC` and lineage/reconciliation sample `OPG-RSM-E-LOG`. The consequence is evaluated for each business process and recovery time window rather than assuming technical availability equals business continuity.

<a id="dcs-risk-assessment.risk_evaluation"></a>
## Inherent and residual risk evaluation

| ID | Scenario | Inherent L×I | Residual L×I | Treatment/control hypothesis | Risk owner |
|---|---|---:|---:|---|---|
| R-01 | Ledger divergence alters settlement finality | 4 × 5 = 20 | 2 × 5 = 10 | Signed checkpoints, daily dual-ledger balancing | Treasury Controls Owner |
| R-02 | Incorrect jurisdiction routing / residency breach | 3 × 5 = 15 | 2 × 5 = 10 | Legal entity tagging, policy enforcement | Data Protection Authority |
| R-03 | Shared dependency causes correlated regional outage | 4 × 5 = 20 | 3 × 5 = 15 | Failure-domain isolation, tested cut-off fallback | Resilience Owner |
| R-04 | Privilege abuse alters approval instructions | 3 × 5 = 15 | 2 × 5 = 10 | Dual authorisation, privileged session audit | IAM Authority |

All control-related residual scores are **projections contingent on test evidence**; they are not claims that mitigations have been implemented. There is no statistical confidence claim for the likelihood values. A measured control failure reopens the corresponding assessment and invalidates any contingent approval.

<a id="dcs-risk-assessment.risk_treatment"></a>
## Risk treatment, escalation and acceptance

For each risk owner, create actions with deadlines ahead of proposed phased waves during 2027–2028 subject to local approvals: implement idempotency and recoverability; verify least-privilege access and data-handling restrictions; conduct controlled failure/recovery rehearsal and preserve evidence; assign monitoring to the receiving team.

Decision rule: production promotion is blocked if any severe untreated item persists, if a risk owner is missing, or if required regulatory applicability is unknown. High residual risk requires a recorded L0 authority decision tied to the canonical risk snapshot. Proposed treatments do not themselves constitute acceptance. Reassess after architecture changes, new suppliers or critical incidents.

## Evidence register, assumptions and limitations

- **OPG-RSM-E-MAP — Dependency map:** versioned system and data-flow relationships **Status:** illustrative.
- **OPG-RSM-E-REC — Recovery exercise:** reproducible recovery drill measurements **Status:** not executed.
- **OPG-RSM-E-IAM — Access-control review:** owner-scoped privilege and segregation checks **Status:** not executed.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `OPG-RSM-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** OPG-RSM-HLD-01, OPG-RSM-TEST-01, OPG-RSM-OPS-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.
