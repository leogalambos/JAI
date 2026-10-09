---
name: it-roles-analysis
description: "Analysis role skills: 11 defined roles covering business analyst; systems analyst; requirements engineer; process analyst; enterprise business analyst; data analyst; business intelligence analyst; finops analyst; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within analysis. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Analysis — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-author`.

`category-index: 03`  ·  `roles: 11`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| Business Analyst | [`references/business-analyst.md`](references/business-analyst.md) | analyze | 3-6 | `author` | `role-author` |
| Systems Analyst | [`references/systems-analyst.md`](references/systems-analyst.md) | analyze | 3-5 | `author` | `role-author` |
| Requirements Engineer | [`references/requirements-engineer.md`](references/requirements-engineer.md) | analyze | 4-6 | `author` | `role-author` |
| Process Analyst | [`references/process-analyst.md`](references/process-analyst.md) | analyze | 3-5 | `author` | `role-author` |
| Enterprise Business Analyst | [`references/enterprise-business-analyst.md`](references/enterprise-business-analyst.md) | analyze | 5-6 | `author` | `role-author` |
| Data Analyst | [`references/data-analyst.md`](references/data-analyst.md) | analyze | 3-5 | `author` | `role-author` |
| Business Intelligence Analyst | [`references/business-intelligence-analyst.md`](references/business-intelligence-analyst.md) | analyze | 3-5 | `author` | `role-author` |
| FinOps Analyst | [`references/finops-analyst.md`](references/finops-analyst.md) | analyze | 3-5 | `author` | `role-author` |
| Product Analyst | [`references/product-analyst.md`](references/product-analyst.md) | analyze | 3-5 | `author` | `role-author` |
| Service Level Analyst | [`references/service-level-analyst.md`](references/service-level-analyst.md) | analyze | 3-4 | `author` | `role-author` |
| Configuration Analyst | [`references/configuration-analyst.md`](references/configuration-analyst.md) | analyze | 3-4 | `author` | `role-author` |

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
