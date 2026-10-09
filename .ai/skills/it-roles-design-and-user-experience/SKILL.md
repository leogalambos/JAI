---
name: it-roles-design-and-user-experience
description: "Design and User Experience role skills: 11 defined roles covering ux designer; ui designer; product designer; ux researcher; usability tester; interaction designer; service designer; information architect; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within design and user experience. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Design and User Experience — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-advisor`, `role-author`, `role-engineer`.

`category-index: 14`  ·  `roles: 11`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| UX Designer | [`references/ux-designer.md`](references/ux-designer.md) | design | 3-5 | `author` | `role-author` |
| UI Designer | [`references/ui-designer.md`](references/ui-designer.md) | design | 3-5 | `author` | `role-author` |
| Product Designer | [`references/product-designer.md`](references/product-designer.md) | design | 4-6 | `author` | `role-author` |
| UX Researcher | [`references/ux-researcher.md`](references/ux-researcher.md) | analyze | 3-5 | `author` | `role-author` |
| Usability Tester | [`references/usability-tester.md`](references/usability-tester.md) | verify | 2-4 | `execute` | `role-engineer` |
| Interaction Designer | [`references/interaction-designer.md`](references/interaction-designer.md) | design | 3-5 | `author` | `role-author` |
| Service Designer | [`references/service-designer.md`](references/service-designer.md) | design | 4-6 | `author` | `role-author` |
| Information Architect | [`references/information-architect.md`](references/information-architect.md) | design | 4-5 | `author` | `role-author` |
| Design System Engineer | [`references/design-system-engineer.md`](references/design-system-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Accessibility Specialist | [`references/accessibility-specialist.md`](references/accessibility-specialist.md) | govern | 4-6 | `advise` | `role-advisor` |
| Content Designer | [`references/content-designer.md`](references/content-designer.md) | design | 3-5 | `author` | `role-author` |

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

1 of the 11 roles here are `advise` tier (`Read, Grep, Glob, WebSearch`) because their work is assurance, oversight, evidential or adversarial. Operate them with `role-advisor`: analyse and document, and hand anything that changes a system to the role named in its interfaces section.
