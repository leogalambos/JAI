---
name: it-roles-infrastructure-cloud-and-operations
description: "Infrastructure, Cloud and Operations role skills: 21 defined roles covering linux systems administrator; windows systems administrator; cloud engineer; cloud operations engineer; platform engineer; devops engineer; site reliability engineer; kubernetes platform engineer; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within infrastructure, cloud and operations. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Infrastructure, Cloud and Operations — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-author`, `role-engineer`.

`category-index: 08`  ·  `roles: 21`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| Linux Systems Administrator | [`references/linux-systems-administrator.md`](references/linux-systems-administrator.md) | operate | 2-5 | `execute` | `role-engineer` |
| Windows Systems Administrator | [`references/windows-systems-administrator.md`](references/windows-systems-administrator.md) | operate | 2-5 | `execute` | `role-engineer` |
| Cloud Engineer | [`references/cloud-engineer.md`](references/cloud-engineer.md) | build | 3-5 | `execute` | `role-engineer` |
| Cloud Operations Engineer | [`references/cloud-operations-engineer.md`](references/cloud-operations-engineer.md) | operate | 3-5 | `execute` | `role-engineer` |
| Platform Engineer | [`references/platform-engineer.md`](references/platform-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| DevOps Engineer | [`references/devops-engineer.md`](references/devops-engineer.md) | build | 3-5 | `execute` | `role-engineer` |
| Site Reliability Engineer | [`references/site-reliability-engineer.md`](references/site-reliability-engineer.md) | operate | 4-6 | `execute` | `role-engineer` |
| Kubernetes Platform Engineer | [`references/kubernetes-platform-engineer.md`](references/kubernetes-platform-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Infrastructure as Code Engineer | [`references/infrastructure-as-code-engineer.md`](references/infrastructure-as-code-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Container Platform Engineer | [`references/container-platform-engineer.md`](references/container-platform-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Environment Manager | [`references/environment-manager.md`](references/environment-manager.md) | manage | 3-5 | `author` | `role-author` |
| Virtualisation Engineer | [`references/virtualisation-engineer.md`](references/virtualisation-engineer.md) | operate | 3-5 | `execute` | `role-engineer` |
| Storage Engineer | [`references/storage-engineer.md`](references/storage-engineer.md) | operate | 3-5 | `execute` | `role-engineer` |
| Backup and Recovery Engineer | [`references/backup-and-recovery-engineer.md`](references/backup-and-recovery-engineer.md) | operate | 3-5 | `execute` | `role-engineer` |
| Datacentre Technician | [`references/datacentre-technician.md`](references/datacentre-technician.md) | operate | 2-4 | `execute` | `role-engineer` |
| Capacity Manager | [`references/capacity-manager.md`](references/capacity-manager.md) | analyze | 4-6 | `author` | `role-author` |
| Availability Manager | [`references/availability-manager.md`](references/availability-manager.md) | manage | 4-6 | `author` | `role-author` |
| Observability Engineer | [`references/observability-engineer.md`](references/observability-engineer.md) | build | 3-6 | `execute` | `role-engineer` |
| Middleware Administrator | [`references/middleware-administrator.md`](references/middleware-administrator.md) | operate | 3-5 | `execute` | `role-engineer` |
| FinOps Engineer | [`references/finops-engineer.md`](references/finops-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Sustainable IT Engineer | [`references/sustainable-it-engineer.md`](references/sustainable-it-engineer.md) | analyze | 4-6 | `author` | `role-author` |

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
