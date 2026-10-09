# Idea to production

`workflow: idea-to-production`  ·  `steps: 13`  ·  `tool-tier: route`

**Trigger.** A business need, opportunity or customer problem arrives with no agreed solution.

**Outcome.** A change running in production with a measured benefit and a named owner.

The most common enterprise value stream, and the one where handoffs are usually implicit. Each arrow below is a place where work is accepted or refused; an unconfirmed handoff reappears later as someone else's incident.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Business Relationship Manager](../../it-roles-service-management-and-support/references/business-relationship-manager.md) | captures the demand with a business outcome and an owner | demand record with outcome and owner | Demand with no named business outcome does not enter the pipeline |
| 2 | [Product Manager](../../it-roles-product-delivery-and-agile/references/product-manager.md) | decides whether and why to pursue it, against evidence | roadmap item with problem statement and success measure | The customer problem and its evidence are stated |
| 3 | [Business Analyst](../../it-roles-analysis/references/business-analyst.md) | elicits and specifies the need with testable acceptance criteria | requirements baseline with traceability | Every requirement is atomic, testable and traced to a source |
| 4 | [Solution Architect](../../it-roles-architecture/references/solution-architect.md) | designs the solution end to end and records the decisions | solution architecture and ADRs | Reviewed by someone who will operate it; failure modes documented |
| 5 | [Security Architect](../../it-roles-architecture/references/security-architect.md) | designs the controls the solution needs | security requirements and threat model | Every control traces to a threat and a business risk |
| 6 | [Technical Lead](../../it-roles-product-delivery-and-agile/references/technical-lead.md) | breaks the work down and sets the technical approach | technical breakdown and readiness-checked items | Acceptance criteria and dependencies exist before start |
| 7 | [Software Engineer](../../it-roles-software-development-and-engineering/references/software-engineer.md) | implements with tests and telemetry | reviewed, merged change with rollback path | Peer reviewed; no secrets in source; telemetry present |
| 8 | [Test Analyst](../../it-roles-quality-and-testing/references/test-analyst.md) | verifies against the claims and reports residual risk | test evidence and residual risk statement | Exit criteria agreed before execution and met or waived |
| 9 | [Release Engineer](../../it-roles-software-development-and-engineering/references/release-engineer.md) | assembles the release and proves the rollback | release manifest and tested rollback | Manifest states exactly which artefact versions ship where |
| 10 | [Change Manager](../../it-roles-service-management-and-support/references/change-manager.md) | authorises the production change proportionate to its risk | change authorisation | Risk class matched to approval path; emergency changes logged within the window |
| 11 | [GitOps and Continuous Delivery Engineer](../../it-roles-software-development-and-engineering/references/gitops-and-continuous-delivery-engineer.md) | promotes the artefact and runs the progressive rollout | deployed change with health gate | Health gate and automatic rollback defined and exercised |
| 12 | [Site Reliability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/site-reliability-engineer.md) | observes against the service objective and owns the run | service operating within SLO, or an error-budget decision | Error budget policy actually enforced |
| 13 | [Product Analyst](../../it-roles-analysis/references/product-analyst.md) | measures whether the stated benefit arrived | benefit measurement against the success measure | Result reported with effect size, not just direction |

## Operating this chain

Each step is a role skill, operated by the agent matching its tool tier. Tiers used here: `advise`, `author`, `execute`.

Read the linked reference file before acting as a step. Do not collapse two adjacent steps into one actor without checking section 13 of both: several of these adjacencies are deliberate separations, and `sod-reviewer` will tell you which.

A hand-off is complete only when the receiving step states the acceptance criteria it applied and confirms they are met. Unconfirmed hand-offs are where this chain actually breaks.
