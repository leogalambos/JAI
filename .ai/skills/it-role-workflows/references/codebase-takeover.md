# Inherited codebase takeover

`workflow: codebase-takeover`  ·  `steps: 8`  ·  `tool-tier: route`

**Trigger.** The organisation acquires, inherits or repatriates a system nobody present built.

**Outcome.** A reviewed, measured, supportable system with a sequenced improvement plan.

The temptation is to rewrite. The sequence below exists so that the rewrite decision is made with evidence rather than with the reaction of the first engineer to open the repository.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Codebase Reviewer](../../it-roles-quality-and-testing/references/codebase-reviewer.md) | audits against fixed criteria and reports prioritised findings | review report with located, measured findings | Criteria fixed before any code is read |
| 2 | [Application Architect](../../it-roles-architecture/references/application-architect.md) | assesses structure and defines module boundaries | boundary definition and refactoring roadmap | Boundaries enforced by automated checks, not prose |
| 3 | [Test Architect](../../it-roles-quality-and-testing/references/test-architect.md) | establishes how the system can be verified at all | test and environment strategy | Production-like data obtained lawfully |
| 4 | [Software Modernisation Engineer](../../it-roles-software-development-and-engineering/references/software-modernisation-engineer.md) | captures existing behaviour before changing it | characterisation test suite | Undocumented behaviour treated as a requirement until proven otherwise |
| 5 | [Infrastructure as Code Engineer](../../it-roles-infrastructure-cloud-and-operations/references/infrastructure-as-code-engineer.md) | codifies whatever it currently runs on | reproducible environment definition | Applies from clean; drift detectable |
| 6 | [Observability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/observability-engineer.md) | makes its behaviour visible before changing it | instrumentation and baseline signals | Baseline captured before the first change |
| 7 | [Technical Lead](../../it-roles-product-delivery-and-agile/references/technical-lead.md) | sequences the work so each slice ships independently | incremental delivery plan | No step requires a simultaneous big-bang cutover |
| 8 | [IT Service Owner](../../it-roles-executive-and-leadership/references/it-service-owner.md) | accepts ownership with a cost and risk position | service definition, SLA, risk profile | A service with no owner is reported as ungoverned |

## Operating this chain

Each step is a role skill, operated by the agent matching its tool tier. Tiers used here: `author`, `execute`, `inspect`.

Read the linked reference file before acting as a step. Do not collapse two adjacent steps into one actor without checking section 13 of both: several of these adjacencies are deliberate separations, and `sod-reviewer` will tell you which.

A hand-off is complete only when the receiving step states the acceptance criteria it applied and confirms they are met. Unconfirmed hand-offs are where this chain actually breaks.
