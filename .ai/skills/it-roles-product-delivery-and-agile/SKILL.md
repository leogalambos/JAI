---
name: it-roles-product-delivery-and-agile
description: "Product, Delivery and Agile role skills: 22 defined roles covering product manager; product owner; technical product manager; scrum master; agile coach; delivery manager; release train engineer; epic owner; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within product, delivery and agile. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Product, Delivery and Agile — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-advisor`, `role-author`.

`category-index: 02`  ·  `roles: 22`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| Product Manager | [`references/product-manager.md`](references/product-manager.md) | manage | 4-6 | `author` | `role-author` |
| Product Owner | [`references/product-owner.md`](references/product-owner.md) | manage | 3-5 | `author` | `role-author` |
| Technical Product Manager | [`references/technical-product-manager.md`](references/technical-product-manager.md) | manage | 4-6 | `author` | `role-author` |
| Scrum Master | [`references/scrum-master.md`](references/scrum-master.md) | manage | 3-5 | `author` | `role-author` |
| Agile Coach | [`references/agile-coach.md`](references/agile-coach.md) | enable | 5-6 | `author` | `role-author` |
| Delivery Manager | [`references/delivery-manager.md`](references/delivery-manager.md) | manage | 4-6 | `author` | `role-author` |
| Release Train Engineer | [`references/release-train-engineer.md`](references/release-train-engineer.md) | manage | 5-6 | `author` | `role-author` |
| Epic Owner | [`references/epic-owner.md`](references/epic-owner.md) | manage | 4-6 | `author` | `role-author` |
| SAFe System Architect | [`references/safe-system-architect.md`](references/safe-system-architect.md) | architect | 5-6 | `author` | `role-author` |
| Project Manager | [`references/project-manager.md`](references/project-manager.md) | manage | 4-6 | `author` | `role-author` |
| Programme Manager | [`references/programme-manager.md`](references/programme-manager.md) | manage | 5-6 | `author` | `role-author` |
| Portfolio Manager | [`references/portfolio-manager.md`](references/portfolio-manager.md) | exec | 5-7 | `advise` | `role-advisor` |
| PMO Analyst | [`references/pmo-analyst.md`](references/pmo-analyst.md) | analyze | 3-5 | `author` | `role-author` |
| PMO Lead | [`references/pmo-lead.md`](references/pmo-lead.md) | manage | 5-6 | `author` | `role-author` |
| Engineering Manager | [`references/engineering-manager.md`](references/engineering-manager.md) | manage | 4-6 | `author` | `role-author` |
| Technical Lead | [`references/technical-lead.md`](references/technical-lead.md) | architect | 4-6 | `author` | `role-author` |
| Transformation Manager | [`references/transformation-manager.md`](references/transformation-manager.md) | manage | 5-6 | `author` | `role-author` |

| Organisational Change and Adoption Manager | [`references/organisational-change-and-adoption-manager.md`](references/organisational-change-and-adoption-manager.md) | manage | 4-6 | `author` | `role-author` |
| Benefits Realisation Manager | [`references/benefits-realisation-manager.md`](references/benefits-realisation-manager.md) | manage | 4-6 | `author` | `role-author` |
| Data Migration and Cutover Lead | [`references/data-migration-and-cutover-lead.md`](references/data-migration-and-cutover-lead.md) | manage | 4-6 | `author` | `role-author` |
| Enterprise Release Manager | [`references/enterprise-release-manager.md`](references/enterprise-release-manager.md) | manage | 5-6 | `author` | `role-author` |
| Demand & Intake Manager | [`references/demand-and-intake-manager.md`](references/demand-and-intake-manager.md) | manage | 4-6 | `author` | `role-author` |

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

1 of the 22 roles here are `advise` tier (`Read, Grep, Glob, WebSearch`) because their work is assurance, oversight, evidential or adversarial. Operate them with `role-advisor`: analyse and document, and hand anything that changes a system to the role named in its interfaces section.
