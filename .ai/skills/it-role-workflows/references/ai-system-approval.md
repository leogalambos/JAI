# AI system from idea to approved production use

`workflow: ai-system-approval`  ·  `steps: 9`  ·  `tool-tier: route`

**Trigger.** A business area wants to deploy a model or an AI-assisted workflow.

**Outcome.** An AI system classified, assessed, monitored, and accountable to a named human.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [AI Governance Officer](../../it-roles-data-analytics-and-ai/references/ai-governance-officer.md) | registers the use case and classifies its risk | risk classification and inventory entry | No production AI without a classification and an accountable human |
| 2 | [Data Protection Officer](../../it-roles-governance-risk-compliance-audit-and-privacy/references/data-protection-officer.md) | assesses lawfulness of the data and the decisioning | privacy and fairness position | Impact assessment before processing, not retrospectively |
| 3 | [Data Scientist](../../it-roles-data-analytics-and-ai/references/data-scientist.md) | builds and characterises a candidate model within the explicitly permitted pre-production scope | candidate model with held-out performance and stated limits | Permitted data and test scope are explicit; no production or pilot use before named human approval; failure modes and excluded populations are stated |
| 4 | [AI and ML Architect](../../it-roles-architecture/references/ai-and-ml-architect.md) | designs serving, monitoring and the human override path | serving and monitoring architecture | Drift, degradation and harmful-output monitoring designed in |
| 5 | [AI Safety and Model Red Team Specialist](../../it-roles-data-analytics-and-ai/references/ai-safety-and-model-red-team-specialist.md) | assesses the candidate deployment configuration for harm and misuse within the authorised test scope | adversarial findings with severity and owners | Candidate tests use the intended configuration without production or pilot effects; any offensive testing requires prior written authorisation |
| 6 | Named authority | records the human deployment and operating decision on the reviewed candidate | exact scoped human approval or rejection | Candidate evidence, privacy, safety, lineage, monitoring and rollback readiness are reviewed before any production or pilot effect; an agent cannot approve |
| 7 | [Machine Learning Engineer](../../it-roles-data-analytics-and-ai/references/machine-learning-engineer.md) | deploys the exact approved model and configuration with full lineage | authorised deployed version and reproducible training lineage | Prior named human approval covers the exact version, data, users, environment and production or pilot scope; every deployed version is traceable to its training run |
| 8 | [MLOps Engineer](../../it-roles-data-analytics-and-ai/references/mlops-engineer.md) | operates the approved lifecycle with monitoring and rollback | monitored model with defined thresholds and rollback | Prior named human approval covers operation and rollback scope; thresholds and an authorised rollback route exist |
| 9 | [AI Governance Officer](../../it-roles-data-analytics-and-ai/references/ai-governance-officer.md) | coordinates periodic reassessment and routes material changes for renewed human approval | periodic assessment, challenge route and next review trigger | The challenge route is published; expired or materially changed scope is not operated without renewed prior human approval |

## Operating this chain

Each step is a role skill, operated by the agent matching its tool tier. Tiers used here: `advise`, `author`, `execute`.

Read the linked reference file before acting as a step. Do not collapse two adjacent steps into one actor without checking section 13 of both: several of these adjacencies are deliberate separations, and `sod-reviewer` will tell you which.

A hand-off is complete only when the receiving step states the acceptance criteria it applied and confirms they are met. Unconfirmed hand-offs are where this chain actually breaks.

Preparatory work is limited to its explicitly permitted scope. Named human approval must precede every effect it authorises; neither a role title nor a later review supplies authority retrospectively. All policy-required pre-approval evidence remains mandatory. Collect candidate evidence only within explicitly permitted pre-production scope. If policy requires operational proof, obtain a separate prior named human approval for the bounded pilot needed to collect it, then seek the wider approval; no pilot permission is implied. If no governing route permits the required evidence collection, stop and consult the accountable authority before proceeding. Any policy-permitted waiver must already be issued by the competent named human authority for the exact gate, scope and validity period before the gated action; non-waivable controls remain blocking.
