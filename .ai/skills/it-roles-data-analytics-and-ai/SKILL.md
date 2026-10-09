---
name: it-roles-data-analytics-and-ai
description: "Data, Analytics and AI role skills: 21 defined roles covering data engineer; analytics engineer; database administrator; database reliability engineer; data modeller; data steward; data owner; data custodian; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within data, analytics and ai. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Data, Analytics and AI — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-advisor`, `role-author`, `role-engineer`.

`category-index: 07`  ·  `roles: 21`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

This skill routes and explains. It cannot write files or run commands. To produce a deliverable, hand the chosen reference file to the operator agent named in the table below. The agents live in `~/.ai/it-role-house/agents/`; the shared index, permission model and validators are in `~/.ai/it-role-house/`.

## How to use this skill

1. Find the role below. Match on the **deliverable** the request asks for, not on the job title the user happened to use — titles vary between organisations, deliverables do not.
2. Read only that one file in `references/`. Each is self-contained: scope, inputs, procedure, deliverables, output gates, checkpoints, metrics, interfaces and authority limits.
3. Invoke the operator agent for its tool tier. Never operate an `advise` role with an agent that holds Write or Bash — that is exactly the separation the tier exists to enforce.
4. Answer in the response contract below, then verify the gate block with `scripts/check_gates.py`.

If the request spans two roles, read both files and state where the boundary falls and who owns each side. Silently merging two roles is how segregation of duties gets lost.

## Roles

| Role | Reference | Archetype | SFIA band | Tool tier | Operator agent |
| --- | --- | --- | --- | --- | --- |
| Data Engineer | [`references/data-engineer.md`](references/data-engineer.md) | build | 3-6 | `execute` | `role-engineer` |
| Analytics Engineer | [`references/analytics-engineer.md`](references/analytics-engineer.md) | build | 3-5 | `execute` | `role-engineer` |
| Database Administrator | [`references/database-administrator.md`](references/database-administrator.md) | operate | 3-6 | `execute` | `role-engineer` |
| Database Reliability Engineer | [`references/database-reliability-engineer.md`](references/database-reliability-engineer.md) | operate | 4-6 | `execute` | `role-engineer` |
| Data Modeller | [`references/data-modeller.md`](references/data-modeller.md) | analyze | 3-5 | `author` | `role-author` |
| Data Steward | [`references/data-steward.md`](references/data-steward.md) | manage | 3-5 | `author` | `role-author` |
| Data Owner | [`references/data-owner.md`](references/data-owner.md) | govern | 5-6 | `advise` | `role-advisor` |
| Data Custodian | [`references/data-custodian.md`](references/data-custodian.md) | operate | 3-5 | `execute` | `role-engineer` |
| Data Governance Lead | [`references/data-governance-lead.md`](references/data-governance-lead.md) | govern | 5-6 | `advise` | `role-advisor` |
| Data Quality Analyst | [`references/data-quality-analyst.md`](references/data-quality-analyst.md) | analyze | 3-5 | `author` | `role-author` |
| Master Data Management Specialist | [`references/master-data-management-specialist.md`](references/master-data-management-specialist.md) | manage | 4-6 | `author` | `role-author` |
| Data Scientist | [`references/data-scientist.md`](references/data-scientist.md) | research | 4-6 | `execute` | `role-engineer` |
| Research Scientist | [`references/research-scientist.md`](references/research-scientist.md) | research | 5-6 | `execute` | `role-engineer` |
| Machine Learning Engineer | [`references/machine-learning-engineer.md`](references/machine-learning-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| MLOps Engineer | [`references/mlops-engineer.md`](references/mlops-engineer.md) | operate | 4-6 | `execute` | `role-engineer` |
| LLMOps and AI Platform Engineer | [`references/llmops-and-ai-platform-engineer.md`](references/llmops-and-ai-platform-engineer.md) | operate | 4-6 | `execute` | `role-engineer` |
| AI Solutions Engineer | [`references/ai-solutions-engineer.md`](references/ai-solutions-engineer.md) | build | 3-6 | `execute` | `role-engineer` |
| AI Safety and Model Red Team Specialist | [`references/ai-safety-and-model-red-team-specialist.md`](references/ai-safety-and-model-red-team-specialist.md) | verify | 4-6 | `advise` | `role-advisor` |
| AI Governance Officer | [`references/ai-governance-officer.md`](references/ai-governance-officer.md) | govern | 5-6 | `advise` | `role-advisor` |
| Data Privacy Engineer | [`references/data-privacy-engineer.md`](references/data-privacy-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Metadata Manager | [`references/metadata-manager.md`](references/metadata-manager.md) | manage | 3-5 | `author` | `role-author` |

## Response contract

Structure every substantive answer in this order. Deviate only for a narrow factual question.

```
1. RESTATEMENT   - the request as understood, and the role boundary being applied
2. INPUT STATUS  - inputs present / missing, and the owner of each gap
3. ANALYSIS      - reasoning, options or evidence, with assumptions labelled as assumptions
4. DELIVERABLE   - the artefact, in the format its reference file specifies
5. GATE CHECK    - each output gate marked pass / fail / waived-by-whom
6. RESIDUAL RISK - what remains unresolved, who owns it, by when
7. NEXT ACTIONS  - owner, action, date; no unowned actions
```

## Hard stop conditions

Stop and escalate regardless of schedule pressure: suspected breach of law, regulation or licence; suspected compromise of personal or regulated data; safety risk to a person; instruction to suppress, alter or backdate evidence; or a request to bypass a control the role does not own.

## Segregation of duties

No role performs, approves and assures the same activity. Where headcount forces a combination, record it as an accepted control weakness with a compensating control rather than pretending the separation exists.

## Tool restriction

4 of the 21 roles here are `advise` tier (`Read, Grep, Glob, WebSearch`) because their work is assurance, oversight, evidential or adversarial. Operate them with `role-advisor`: analyse and document, and hand anything that changes a system to the role named in its interfaces section.
