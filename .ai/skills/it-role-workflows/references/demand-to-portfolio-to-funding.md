# Demand to portfolio to funding

**Trigger.** A new business/technology demand needs to be qualified, compared with alternatives and either rejected, redirected or committed into a funded portfolio.

**Outcome.** Demand is traceable from intake through capability/architecture/risk/value assessment, sizing/capacity and prioritisation to an explicit funding/portfolio commitment decision.

## Mandatory artefacts

- Demand record
- Qualification assessment
- Capability-fit assessment
- Application portfolio impact assessment
- Architecture impact assessment
- Risk/value assessment
- Estimate and capacity view
- Prioritisation decision
- Funding decision
- Portfolio commitment

## Chain

| Step | Accountable role | Does | Hands over | Mandatory artefact | Gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | **Demand & Intake Manager** | captures demand with owner, problem/outcome, urgency and evidence status | demand record | Demand record | No anonymous or outcome-free demand enters prioritisation |
| 2 | **Demand & Intake Manager** | qualifies completeness, duplicates, mandatory obligations and routing | qualification assessment | Qualification assessment | Disposition is explicit: reject, redirect, discover or assess |
| 3 | **Enterprise Architect** | checks business capability fit, reuse and enterprise target-state alignment | capability-fit assessment | Capability-fit assessment | Existing capability/service reuse and strategic conflicts are explicit |
| 4 | **Application Portfolio Manager** | assesses affected application portfolio, lifecycle posture, duplication and invest/tolerate/migrate/retire consequences | application portfolio impact assessment | Application portfolio impact assessment | Impacted applications have an explicit lifecycle posture, duplication/dependency view and accountable owner |
| 5 | **Solution Architect** | assesses architecture/integration/data/security/operational impact at decision-appropriate depth | architecture impact assessment | Architecture impact assessment | Material cross-domain dependencies and constraints are identified |
| 6 | **IT Risk Manager** | frames risk/opportunity, compliance urgency and value-at-risk alongside benefit evidence | risk/value assessment | Risk/value assessment | Regulatory/risk urgency is evidence-based and not double-counted as value |
| 7 | **Resource Manager** | coordinates indicative sizing and scarce-capability/capacity demand | estimate and capacity view | Estimate and capacity view | Uncertainty ranges and constrained skills/capacity are explicit |
| 8 | **Portfolio Manager** | applies transparent prioritisation criteria across value, risk, strategy, capacity and dependencies | prioritisation decision | Prioritisation decision | Prioritisation can be reconstructed from declared criteria and exceptions |
| 9 | **IT Financial Management / TBM Manager** | validates TCO/funding profile and financial comparability | funding economics and cost profile | Funding decision | Cost boundaries, CAPEX/OPEX and transition costs reconcile to the cost model |
| 10 | **Portfolio Manager** | makes or routes the delegated funding/portfolio commitment decision | portfolio commitment | Portfolio commitment | Commitment has authority, funding/capacity basis and review condition |

## Control semantics

- A gate is blocking unless a named authority with the required decision right records an explicit waiver, rationale, expiry/review date and residual risk.
- A handoff is not complete because a document exists; the receiving role must be able to verify the acceptance condition from attributable evidence.
- Producer, approver and independent assurance responsibilities remain separated where the decision is consequential.
- Workflow order may branch or loop, but skipped steps and their unmet gates remain visible.
- Material claims/decisions use stable IDs and trace to evidence so Behavioral Quality evaluation can measure coverage and unsupported claims.
