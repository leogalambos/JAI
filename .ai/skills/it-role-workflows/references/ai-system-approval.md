# AI system from idea to approved production use

`workflow: ai-system-approval`  ·  `steps: 8`  ·  `tool-tier: route`

**Trigger.** A business area wants to deploy a model or an AI-assisted workflow.

**Outcome.** An AI system classified, assessed, monitored, and accountable to a named human.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [AI Governance Officer](../../it-roles-data-analytics-and-ai/references/ai-governance-officer.md) | registers the use case and classifies its risk | risk classification and inventory entry | No production AI without a classification and an accountable human |
| 2 | [Data Protection Officer](../../it-roles-governance-risk-compliance-audit-and-privacy/references/data-protection-officer.md) | assesses lawfulness of the data and the decisioning | privacy and fairness position | Impact assessment before processing, not retrospectively |
| 3 | [Data Scientist](../../it-roles-data-analytics-and-ai/references/data-scientist.md) | builds and honestly characterises the model | model with held-out performance and stated limits | Failure modes and the population it must not be applied to are stated |
| 4 | [AI and ML Architect](../../it-roles-architecture/references/ai-and-ml-architect.md) | designs serving, monitoring and the human override path | serving and monitoring architecture | Drift, degradation and harmful-output monitoring designed in |
| 5 | [AI Safety and Model Red Team Specialist](../../it-roles-data-analytics-and-ai/references/ai-safety-and-model-red-team-specialist.md) | probes the deployment configuration for harm and misuse | adversarial findings with severity and owners | Tested against the configuration users will actually get |
| 6 | [Machine Learning Engineer](../../it-roles-data-analytics-and-ai/references/machine-learning-engineer.md) | productionises with full lineage | reproducible training and traceable deployed version | Every deployed version traceable to its training run |
| 7 | [MLOps Engineer](../../it-roles-data-analytics-and-ai/references/mlops-engineer.md) | operates the lifecycle with rollback | monitored model with defined thresholds and rollback | Automatic or documented rollback route exists |
| 8 | [AI Governance Officer](../../it-roles-data-analytics-and-ai/references/ai-governance-officer.md) | approves, and re-tests at the review date | approval record and review date | Route to challenge the system's decisions is published |

## Operating this chain

Each step is a role skill, operated by the agent matching its tool tier. Tiers used here: `advise`, `author`, `execute`.

Read the linked reference file before acting as a step. Do not collapse two adjacent steps into one actor without checking section 13 of both: several of these adjacencies are deliberate separations, and `sod-reviewer` will tell you which.

A hand-off is complete only when the receiving step states the acceptance criteria it applied and confirms they are met. Unconfirmed hand-offs are where this chain actually breaks.
