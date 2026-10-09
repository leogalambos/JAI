---
name: it-roles-research-innovation-and-specialist-engineering
description: "Research, Innovation and Specialist Engineering role skills: 9 defined roles covering research engineer; innovation lead; technology scout; standards body representative; ethics and responsible technology lead; systems engineer (incose); simulation engineer; high performance computing engineer; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within research, innovation and specialist engineering. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Research, Innovation and Specialist Engineering — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-advisor`, `role-author`, `role-engineer`.

`category-index: 16`  ·  `roles: 9`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| Research Engineer | [`references/research-engineer.md`](references/research-engineer.md) | research | 4-6 | `execute` | `role-engineer` |
| Innovation Lead | [`references/innovation-lead.md`](references/innovation-lead.md) | manage | 5-6 | `author` | `role-author` |
| Technology Scout | [`references/technology-scout.md`](references/technology-scout.md) | research | 4-6 | `author` | `role-author` |
| Standards Body Representative | [`references/standards-body-representative.md`](references/standards-body-representative.md) | enable | 5-6 | `author` | `role-author` |
| Ethics and Responsible Technology Lead | [`references/ethics-and-responsible-technology-lead.md`](references/ethics-and-responsible-technology-lead.md) | govern | 5-6 | `advise` | `role-advisor` |
| Systems Engineer (INCOSE) | [`references/systems-engineer-incose.md`](references/systems-engineer-incose.md) | architect | 5-7 | `author` | `role-author` |
| Simulation Engineer | [`references/simulation-engineer.md`](references/simulation-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| High Performance Computing Engineer | [`references/high-performance-computing-engineer.md`](references/high-performance-computing-engineer.md) | operate | 4-6 | `execute` | `role-engineer` |
| Quantum Computing Engineer | [`references/quantum-computing-engineer.md`](references/quantum-computing-engineer.md) | research | 5-6 | `execute` | `role-engineer` |

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

1 of the 9 roles here are `advise` tier (`Read, Grep, Glob, WebSearch`) because their work is assurance, oversight, evidential or adversarial. Operate them with `role-advisor`: analyse and document, and hand anything that changes a system to the role named in its interfaces section.
