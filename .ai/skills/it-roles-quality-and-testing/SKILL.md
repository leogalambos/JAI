---
name: it-roles-quality-and-testing
description: "Quality and Testing role skills: 11 defined roles covering test analyst; test automation engineer; performance test engineer; test manager; test architect; user acceptance test coordinator; accessibility tester; localisation qa analyst; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within quality and testing. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Quality and Testing — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `codebase-reviewer`, `role-advisor`, `role-author`, `role-engineer`.

`category-index: 06`  ·  `roles: 11`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| Test Analyst | [`references/test-analyst.md`](references/test-analyst.md) | verify | 2-5 | `execute` | `role-engineer` |
| Test Automation Engineer | [`references/test-automation-engineer.md`](references/test-automation-engineer.md) | verify | 3-6 | `execute` | `role-engineer` |
| Performance Test Engineer | [`references/performance-test-engineer.md`](references/performance-test-engineer.md) | verify | 4-6 | `execute` | `role-engineer` |
| Test Manager | [`references/test-manager.md`](references/test-manager.md) | manage | 4-6 | `author` | `role-author` |
| Test Architect | [`references/test-architect.md`](references/test-architect.md) | architect | 5-6 | `author` | `role-author` |
| User Acceptance Test Coordinator | [`references/user-acceptance-test-coordinator.md`](references/user-acceptance-test-coordinator.md) | manage | 3-5 | `author` | `role-author` |
| Accessibility Tester | [`references/accessibility-tester.md`](references/accessibility-tester.md) | verify | 3-5 | `execute` | `role-engineer` |
| Localisation QA Analyst | [`references/localisation-qa-analyst.md`](references/localisation-qa-analyst.md) | verify | 2-4 | `execute` | `role-engineer` |
| Chaos and Resilience Engineer | [`references/chaos-and-resilience-engineer.md`](references/chaos-and-resilience-engineer.md) | verify | 4-6 | `execute` | `role-engineer` |
| Codebase Reviewer | [`references/codebase-reviewer.md`](references/codebase-reviewer.md) | assure | 4-6 | `inspect` | `codebase-reviewer` |
| Release Quality Gatekeeper | [`references/release-quality-gatekeeper.md`](references/release-quality-gatekeeper.md) | verify | 4-6 | `advise` | `role-advisor` |

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
