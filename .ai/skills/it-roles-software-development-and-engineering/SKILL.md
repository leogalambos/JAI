---
name: it-roles-software-development-and-engineering
description: "Software Development and Engineering role skills: 27 defined roles covering software engineer; senior software engineer; staff engineer; backend engineer; frontend engineer; full-stack engineer; mobile engineer; embedded firmware engineer; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within software development and engineering. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Software Development and Engineering — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-author`, `role-engineer`.

`category-index: 05`  ·  `roles: 27`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| Software Engineer | [`references/software-engineer.md`](references/software-engineer.md) | build | 2-6 | `execute` | `role-engineer` |
| Senior Software Engineer | [`references/senior-software-engineer.md`](references/senior-software-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Staff Engineer | [`references/staff-engineer.md`](references/staff-engineer.md) | architect | 5-6 | `author` | `role-author` |
| Backend Engineer | [`references/backend-engineer.md`](references/backend-engineer.md) | build | 3-6 | `execute` | `role-engineer` |
| Frontend Engineer | [`references/frontend-engineer.md`](references/frontend-engineer.md) | build | 3-6 | `execute` | `role-engineer` |
| Full-stack Engineer | [`references/full-stack-engineer.md`](references/full-stack-engineer.md) | build | 3-6 | `execute` | `role-engineer` |
| Mobile Engineer | [`references/mobile-engineer.md`](references/mobile-engineer.md) | build | 3-6 | `execute` | `role-engineer` |
| Embedded Firmware Engineer | [`references/embedded-firmware-engineer.md`](references/embedded-firmware-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Real-time Systems Engineer | [`references/real-time-systems-engineer.md`](references/real-time-systems-engineer.md) | build | 5-6 | `execute` | `role-engineer` |
| Systems Programmer | [`references/systems-programmer.md`](references/systems-programmer.md) | build | 4-6 | `execute` | `role-engineer` |
| Mainframe Developer | [`references/mainframe-developer.md`](references/mainframe-developer.md) | build | 3-6 | `execute` | `role-engineer` |
| API Developer | [`references/api-developer.md`](references/api-developer.md) | build | 3-5 | `execute` | `role-engineer` |
| Integration Developer | [`references/integration-developer.md`](references/integration-developer.md) | build | 3-5 | `execute` | `role-engineer` |
| ERP and CRM Consultant Developer | [`references/erp-and-crm-consultant-developer.md`](references/erp-and-crm-consultant-developer.md) | build | 3-6 | `execute` | `role-engineer` |
| Low-code and RPA Developer | [`references/low-code-and-rpa-developer.md`](references/low-code-and-rpa-developer.md) | build | 3-5 | `execute` | `role-engineer` |
| Game Developer | [`references/game-developer.md`](references/game-developer.md) | build | 3-6 | `execute` | `role-engineer` |
| Graphics and Engine Engineer | [`references/graphics-and-engine-engineer.md`](references/graphics-and-engine-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Blockchain and Smart Contract Developer | [`references/blockchain-and-smart-contract-developer.md`](references/blockchain-and-smart-contract-developer.md) | build | 4-6 | `execute` | `role-engineer` |
| Quantitative Developer | [`references/quantitative-developer.md`](references/quantitative-developer.md) | build | 4-6 | `execute` | `role-engineer` |
| Compiler and Toolchain Engineer | [`references/compiler-and-toolchain-engineer.md`](references/compiler-and-toolchain-engineer.md) | build | 5-6 | `execute` | `role-engineer` |
| Build Engineer | [`references/build-engineer.md`](references/build-engineer.md) | build | 3-5 | `execute` | `role-engineer` |
| Release Engineer | [`references/release-engineer.md`](references/release-engineer.md) | build | 3-5 | `execute` | `role-engineer` |
| CI/CD Platform Engineer | [`references/ci-cd-platform-engineer.md`](references/ci-cd-platform-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| GitOps and Continuous Delivery Engineer | [`references/gitops-and-continuous-delivery-engineer.md`](references/gitops-and-continuous-delivery-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Developer Experience Engineer | [`references/developer-experience-engineer.md`](references/developer-experience-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Open Source Program Office Engineer | [`references/open-source-program-office-engineer.md`](references/open-source-program-office-engineer.md) | manage | 4-6 | `author` | `role-author` |
| Software Modernisation Engineer | [`references/software-modernisation-engineer.md`](references/software-modernisation-engineer.md) | build | 4-6 | `execute` | `role-engineer` |

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
