---
name: it-roles-service-management-and-support
description: "Service Management and Support role skills: 20 defined roles covering service desk analyst; desktop support engineer; application support analyst; incident manager; major incident manager; problem manager; change manager; request fulfilment manager; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within service management and support. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Service Management and Support — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-advisor`, `role-author`, `role-engineer`.

`category-index: 10`  ·  `roles: 20`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| Service Desk Analyst | [`references/service-desk-analyst.md`](references/service-desk-analyst.md) | operate | 1-3 | `execute` | `role-engineer` |
| Desktop Support Engineer | [`references/desktop-support-engineer.md`](references/desktop-support-engineer.md) | operate | 2-4 | `execute` | `role-engineer` |
| Application Support Analyst | [`references/application-support-analyst.md`](references/application-support-analyst.md) | operate | 2-5 | `execute` | `role-engineer` |
| Incident Manager | [`references/incident-manager.md`](references/incident-manager.md) | operate | 4-6 | `execute` | `role-engineer` |
| Major Incident Manager | [`references/major-incident-manager.md`](references/major-incident-manager.md) | operate | 5-6 | `execute` | `role-engineer` |
| Problem Manager | [`references/problem-manager.md`](references/problem-manager.md) | analyze | 4-6 | `author` | `role-author` |
| Change Manager | [`references/change-manager.md`](references/change-manager.md) | govern | 4-6 | `advise` | `role-advisor` |
| Request Fulfilment Manager | [`references/request-fulfilment-manager.md`](references/request-fulfilment-manager.md) | manage | 3-5 | `author` | `role-author` |
| Service Level Manager | [`references/service-level-manager.md`](references/service-level-manager.md) | manage | 4-6 | `author` | `role-author` |
| Service Catalogue Manager | [`references/service-catalogue-manager.md`](references/service-catalogue-manager.md) | manage | 3-5 | `author` | `role-author` |
| Continual Improvement Manager | [`references/continual-improvement-manager.md`](references/continual-improvement-manager.md) | manage | 4-6 | `author` | `role-author` |
| Knowledge Manager | [`references/knowledge-manager.md`](references/knowledge-manager.md) | manage | 3-5 | `author` | `role-author` |
| Configuration Manager | [`references/configuration-manager.md`](references/configuration-manager.md) | manage | 4-6 | `author` | `role-author` |
| IT Asset Manager | [`references/it-asset-manager.md`](references/it-asset-manager.md) | manage | 4-6 | `author` | `role-author` |
| Software Asset Manager | [`references/software-asset-manager.md`](references/software-asset-manager.md) | manage | 4-6 | `author` | `role-author` |
| End-User Computing Engineer | [`references/end-user-computing-engineer.md`](references/end-user-computing-engineer.md) | build | 3-5 | `execute` | `role-engineer` |
| Business Relationship Manager | [`references/business-relationship-manager.md`](references/business-relationship-manager.md) | enable | 4-6 | `author` | `role-author` |

| Service Transition and Operational Readiness Manager | [`references/service-transition-and-operational-readiness-manager.md`](references/service-transition-and-operational-readiness-manager.md) | manage | 4-6 | `author` | `role-author` |
| Technology Lifecycle and Decommission Manager | [`references/technology-lifecycle-and-decommission-manager.md`](references/technology-lifecycle-and-decommission-manager.md) | manage | 4-6 | `author` | `role-author` |
| SIAM Manager | [`references/siam-manager.md`](references/siam-manager.md) | manage | 5-6 | `author` | `role-author` |

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

1 of the 20 roles here is `advise` tier (`Read, Grep, Glob, WebSearch`) because their work is assurance, oversight, evidential or adversarial. Operate them with `role-advisor`: analyse and document, and hand anything that changes a system to the role named in its interfaces section.
