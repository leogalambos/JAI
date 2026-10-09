---
name: it-roles-governance-risk-compliance-audit-and-privacy
description: "Governance, Risk, Compliance, Audit and Privacy role skills: 17 defined roles covering it governance manager; grc analyst; it risk manager; information security officer (local); compliance officer (technology); internal it auditor; external auditor and assessor; control owner; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within governance, risk, compliance, audit and privacy. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Governance, Risk, Compliance, Audit and Privacy — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-advisor`, `role-author`, `role-engineer`.

`category-index: 13`  ·  `roles: 18`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| IT Governance Manager | [`references/it-governance-manager.md`](references/it-governance-manager.md) | govern | 5-6 | `advise` | `role-advisor` |
| GRC Analyst | [`references/grc-analyst.md`](references/grc-analyst.md) | assure | 3-5 | `advise` | `role-advisor` |
| IT Risk Manager | [`references/it-risk-manager.md`](references/it-risk-manager.md) | assure | 4-6 | `advise` | `role-advisor` |
| Information Security Officer (Local) | [`references/information-security-officer-local.md`](references/information-security-officer-local.md) | govern | 4-5 | `advise` | `role-advisor` |
| Compliance Officer (Technology) | [`references/compliance-officer-technology.md`](references/compliance-officer-technology.md) | assure | 4-6 | `advise` | `role-advisor` |
| Internal IT Auditor | [`references/internal-it-auditor.md`](references/internal-it-auditor.md) | assure | 4-6 | `advise` | `role-advisor` |
| External Auditor and Assessor | [`references/external-auditor-and-assessor.md`](references/external-auditor-and-assessor.md) | assure | 4-6 | `advise` | `role-advisor` |
| Control Owner | [`references/control-owner.md`](references/control-owner.md) | manage | 4-6 | `author` | `role-author` |
| Control Tester | [`references/control-tester.md`](references/control-tester.md) | assure | 3-5 | `advise` | `role-advisor` |
| Data Protection Officer | [`references/data-protection-officer.md`](references/data-protection-officer.md) | govern | 5-6 | `advise` | `role-advisor` |
| Privacy Analyst | [`references/privacy-analyst.md`](references/privacy-analyst.md) | analyze | 3-5 | `advise` | `role-advisor` |
| Records Manager | [`references/records-manager.md`](references/records-manager.md) | govern | 4-5 | `advise` | `role-advisor` |
| Business Continuity Manager | [`references/business-continuity-manager.md`](references/business-continuity-manager.md) | govern | 4-6 | `advise` | `role-advisor` |
| Disaster Recovery Coordinator | [`references/disaster-recovery-coordinator.md`](references/disaster-recovery-coordinator.md) | operate | 3-5 | `execute` | `role-engineer` |
| Third-Party Risk Manager | [`references/third-party-risk-manager.md`](references/third-party-risk-manager.md) | assure | 4-6 | `advise` | `role-advisor` |
| Policy Author | [`references/policy-author.md`](references/policy-author.md) | govern | 4-5 | `advise` | `role-advisor` |
| Crisis Manager | [`references/crisis-manager.md`](references/crisis-manager.md) | operate | 5-6 | `execute` | `role-engineer` |

| Privacy Architect | [`references/privacy-architect.md`](references/privacy-architect.md) | architect | 5-6 | `author` | `role-author` |

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

14 of the 17 roles here are `advise` tier (`Read, Grep, Glob, WebSearch`) because their work is assurance, oversight, evidential or adversarial. Operate them with `role-advisor`: analyse and document, and hand anything that changes a system to the role named in its interfaces section.
