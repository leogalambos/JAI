---
reference_id: example:risk-assessment:medium
schema_version: '1.0.0'
document_kind: risk-assessment
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/risk-assessment
approval_status: not-human-approved
content_revision: 2.0.0
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Meridian Retail Group · Order Event Integration · `MRG-OEI` · MEDIUM complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Digital Commerce Sponsor. **Scope:** multi-system integration with phased market rollout.

# Information-security and service risk assessment — Order Event Integration

<a id="dcs-risk-assessment.assessment_scope"></a>
## Assessment scope and assets at risk

Risk assessment `MRG-OEI-RA-01` covers cross-channel order ingestion and fulfilment synchronisation and the supporting boundary commerce platform, API gateway, event broker, integration workers, ERP and observability stack. Business asset: reliable fulfilment of move accepted-order visibility from the next batch cycle to 5 minutes at p95, without losing order records; information asset: order identifiers, delivery addresses and limited customer identifiers; technology assets: integration interfaces, identity plane, state stores and telemetry. Exposure: multi-country commercial service involving customer personal data.

Assessment owner is Head of Digital Risk; independent reviewer remains unassigned. This document is an illustrative analysis only; real owners must establish the applicable legal/regulatory obligations for each operating location.

<a id="dcs-risk-assessment.scoring_method"></a>
## Scoring method and decision appetite

Working qualitative 5×5 method: likelihood 1 (rare) to 5 (frequent); impact 1 (negligible) to 5 (critical interruption, compromise or liability); product gives a **relative prioritisation score**, not a probabilistic annual-loss estimate. Bands: 1–5 low, 6–10 moderate, 11–15 high, 16–25 severe.

Risk appetite is assumed for this synthetic exercise: no severe untreated risk may move to production; high residual risk requires named executive acceptance and documented compensating controls. The actual organisation must substitute its approved appetite and scoring rubric; regulatory breaches cannot be made acceptable by selecting a low number.

<a id="dcs-risk-assessment.risk_scenarios"></a>
## Threat-event scenarios and supporting assumptions

The critical initiating events include lost or duplicated events, country-specific data routing and supplier dependency, operator error and malicious misuse of privileged interfaces. A failure may cause loss or duplication of business records, unavailable processing or unauthorised disclosure. Threat and control effectiveness are hypotheses; no production penetration test, audit or outage history was available for the fictional organisation.

Evidence obligations: service-dependency map `MRG-OEI-E-MAP`, access review `MRG-OEI-E-IAM`, recovery exercises `MRG-OEI-E-REC` and lineage/reconciliation sample `MRG-OEI-E-LOG`. The consequence is evaluated for each business process and recovery time window rather than assuming technical availability equals business continuity.

<a id="dcs-risk-assessment.risk_evaluation"></a>
## Inherent and residual risk evaluation

| ID | Scenario | Inherent L×I | Residual L×I | Treatment/control hypothesis | Risk owner |
|---|---|---:|---:|---|---|
| R-01 | Event loss during ERP consumer restart | 4 × 5 = 20 | 2 × 5 = 10 | Durable broker, replay + reconciliation | Integration Architect |
| R-02 | Cross-country routing leaks delivery address | 3 × 5 = 15 | 2 × 5 = 10 | Region tagging, scoped processing, audit trails | Privacy Lead |
| R-03 | Broker saturation delays customer promises | 4 × 4 = 16 | 2 × 4 = 8 | Backpressure and automated queue-depth alarm | Operations Manager |

All control-related residual scores are **projections contingent on test evidence**; they are not claims that mitigations have been implemented. There is no statistical confidence claim for the likelihood values. A measured control failure reopens the corresponding assessment and invalidates any contingent approval.

<a id="dcs-risk-assessment.risk_treatment"></a>
## Risk treatment, escalation and acceptance

For each risk owner, create actions with deadlines ahead of proposed first market 2027-06-01: implement idempotency and recoverability; verify least-privilege access and data-handling restrictions; conduct controlled failure/recovery rehearsal and preserve evidence; assign monitoring to the receiving team.

Decision rule: production promotion is blocked if any severe untreated item persists, if a risk owner is missing, or if required regulatory applicability is unknown. High residual risk requires a recorded L0 authority decision tied to the canonical risk snapshot. Proposed treatments do not themselves constitute acceptance. Reassess after architecture changes, new suppliers or critical incidents.

## Evidence register, assumptions and limitations

- **MRG-OEI-E-MAP — Dependency map:** versioned system and data-flow relationships **Status:** illustrative.
- **MRG-OEI-E-REC — Recovery exercise:** reproducible recovery drill measurements **Status:** not executed.
- **MRG-OEI-E-IAM — Access-control review:** owner-scoped privilege and segregation checks **Status:** not executed.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `MRG-OEI-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** MRG-OEI-HLD-01, MRG-OEI-TEST-01, MRG-OEI-OPS-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.




## Professional deepening: decision rationale and practical checks

### Risk taxonomy and scenario articulation

Express each material scenario as threat/event → vulnerable condition → business impact, against a concrete asset and an operational horizon. Use a stable risk ID, asset owner, impact owner and named treatment owner. Keep compliance obligations distinct from discretionary risk appetite: a likely regulatory violation cannot be accepted merely by assigning a low score.

### Scoring and inherent/residual distinction

Qualitative likelihood and impact scales must have unambiguous anchors. An inherent score describes exposure before evaluated controls; a residual score requires evidence of control design and effectiveness. Where controls have not been tested, residual scores are **conditional projections**, not measured facts. Separate uncertainty about likelihood from uncertainty about impact, and record the assessor's confidence alongside the score.

### Scenario and control assurance matrix

| Risk event | Preventive control | Detective control | Recovery control | Required evidence |
|---|---|---|---|---|
| Duplicate financial instruction | Idempotency key enforced at business boundary | Ledger reconciliation alert | Safe replay from checkpoint | Replay and balancing tests |
| Unauthorized entitlement | Approval and separation of duties | Privileged session review | Revoke and reconcile permissions | IAM policy and negative-case results |
| Regional dependency outage | Failure domain separation | Dependency health signals | Tested controlled switchover | Restoration timings and data-integrity check |
| Data location breach | Rule-based routing and encryption | Routing exception detection | Isolate and remediate affected records | Jurisdiction mapping and privacy review |

### Treatment plan and risk acceptance

For each high-impact item, record treatment option (reduce, avoid, transfer or accept), action, testable control objective, deadline and budget dependency. Transferring a commercial liability does not remove accountability for service continuity. Risk acceptance must identify the authorised business owner, acceptance expiry and monitored indicators; authoring this example does not exercise that authority.

