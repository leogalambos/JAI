# Enterprise release orchestration

**Trigger.** Multiple products/platforms/suppliers must release into a shared business/technology environment and need one dependency, readiness and go/no-go process.

**Outcome.** The integrated release is sequenced, independently readiness-checked, authorised, executed by technical owners, validated and closed with measurable release performance.

## Mandatory artefacts

- Integrated release calendar
- Dependency register
- Business readiness
- Cutover readiness
- Supplier readiness
- Rollback readiness
- Secure delivery readiness evidence
- Go/no-go decision
- Post-release validation

## Chain

| Step | Accountable role | Does | Hands over | Mandatory artefact | Gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | **Enterprise Release Manager** | builds integrated release scope/calendar and identifies cross-system dependencies/blackouts | integrated release calendar | Integrated release calendar | All material releases and blackout/business constraints are represented |
| 2 | **Architecture Repository and Modelling Lead** | validates technical/service dependency graph and critical sequencing constraints | release dependency register | Dependency register | No critical dependency is missing an owner or sequence |
| 3 | **Organisational Change and Adoption Manager** | validates communications/training/adoption/business readiness for affected cohorts | business readiness | Business readiness | Affected business cohorts have executable readiness actions/evidence |
| 4 | **Data Migration and Cutover Lead** | validates cutover sequence, data reconciliation, checkpoints and abort criteria | cutover readiness | Cutover readiness | Cutover and data reconciliation are rehearsed/evidenced for critical transitions |
| 5 | **SIAM Manager** | validates supplier staffing, dependencies, handoffs and escalation readiness | supplier readiness | Supplier readiness | No critical supplier dependency is relying on informal availability |
| 6 | **Release Engineer** | validates technical release artefacts, provenance and executable rollback | technical/rollback readiness | Rollback readiness | Release artefacts are traceable and rollback is exercised/feasible |
| 7 | **Secure Delivery / DevSecOps Architect** | checks that release provenance, pipeline controls, policy-as-code and software supply-chain evidence conform to the approved secure-delivery architecture | secure delivery readiness evidence | Secure delivery readiness evidence | Critical secure-delivery controls and provenance are evidenced; deviations are owned, time-bound and visible to independent release assurance |
| 8 | **Release Quality Gatekeeper** | independently checks mandatory release criteria and evidence | release gate assurance | Go/no-go decision | Producer cannot waive its own failed critical gate |
| 9 | **Enterprise Release Manager** | issues delegated integrated go/no-go or routes decision to higher authority | go/no-go decision | Go/no-go decision | Decision cites evidence, waivers, residual risk and abort triggers |
| 10 | **Release Engineer** | executes the authorised technical release through controlled pipelines | release execution evidence | Post-release validation | Executed artefacts/plan match what was approved |
| 11 | **Site Reliability Engineer** | monitors agreed technical/service signals and triggers reversal if thresholds breach | technical post-release validation | Post-release validation | Rollback/reversal triggers are acted on, not debated after breach |
| 12 | **IT Service Owner** | confirms business/service outcome and closes or escalates residual issues | release acceptance | Post-release validation | Closure states outcome, impact, residual issues and owners |

## Control semantics

- A gate is blocking unless a named authority with the required decision right records an explicit waiver, rationale, expiry/review date and residual risk.
- A handoff is not complete because a document exists; the receiving role must be able to verify the acceptance condition from attributable evidence.
- Producer, approver and independent assurance responsibilities remain separated where the decision is consequential.
- Workflow order may branch or loop, but skipped steps and their unmet gates remain visible.
- Material claims/decisions use stable IDs and trace to evidence so Behavioral Quality evaluation can measure coverage and unsupported claims.
