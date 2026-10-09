---
name: it-roles-executive-and-leadership
description: "Executive and Leadership role skills: 11 defined roles covering chief information officer; chief technology officer; chief information security officer; chief data officer; chief digital officer; chief product officer; chief ai officer; it chief of staff; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within executive and leadership. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Executive and Leadership — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-advisor`, `role-author`.

`category-index: 01`  ·  `roles: 11`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| Chief Information Officer | [`references/chief-information-officer.md`](references/chief-information-officer.md) | exec | 6-7 | `advise` | `role-advisor` |
| Chief Technology Officer | [`references/chief-technology-officer.md`](references/chief-technology-officer.md) | exec | 6-7 | `advise` | `role-advisor` |
| Chief Information Security Officer | [`references/chief-information-security-officer.md`](references/chief-information-security-officer.md) | govern | 6-7 | `advise` | `role-advisor` |
| Chief Data Officer | [`references/chief-data-officer.md`](references/chief-data-officer.md) | exec | 6-7 | `advise` | `role-advisor` |
| Chief Digital Officer | [`references/chief-digital-officer.md`](references/chief-digital-officer.md) | exec | 6-7 | `advise` | `role-advisor` |
| Chief Product Officer | [`references/chief-product-officer.md`](references/chief-product-officer.md) | exec | 6-7 | `advise` | `role-advisor` |
| Chief AI Officer | [`references/chief-ai-officer.md`](references/chief-ai-officer.md) | govern | 6-7 | `advise` | `role-advisor` |
| IT Chief of Staff | [`references/it-chief-of-staff.md`](references/it-chief-of-staff.md) | manage | 5-6 | `author` | `role-author` |
| VP of Engineering | [`references/vp-of-engineering.md`](references/vp-of-engineering.md) | exec | 6-7 | `advise` | `role-advisor` |
| Head of Platform | [`references/head-of-platform.md`](references/head-of-platform.md) | manage | 5-6 | `author` | `role-author` |
| IT Service Owner | [`references/it-service-owner.md`](references/it-service-owner.md) | manage | 4-6 | `author` | `role-author` |

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

8 of the 11 roles here are `advise` tier (`Read, Grep, Glob, WebSearch`) because their work is assurance, oversight, evidential or adversarial. Operate them with `role-advisor`: analyse and document, and hand anything that changes a system to the role named in its interfaces section.
