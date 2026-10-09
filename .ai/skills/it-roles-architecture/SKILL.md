---
name: it-roles-architecture
description: "Architecture role skills: 18 defined roles covering enterprise architect; business architect; solution architect; application architect; domain architect; data architect; integration architect; cloud architect; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within architecture. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Architecture — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-author`.

`category-index: 04`  ·  `roles: 18`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| Enterprise Architect | [`references/enterprise-architect.md`](references/enterprise-architect.md) | architect | 5-7 | `author` | `role-author` |
| Business Architect | [`references/business-architect.md`](references/business-architect.md) | architect | 5-6 | `author` | `role-author` |
| Solution Architect | [`references/solution-architect.md`](references/solution-architect.md) | architect | 4-6 | `author` | `role-author` |
| Application Architect | [`references/application-architect.md`](references/application-architect.md) | architect | 4-6 | `author` | `role-author` |
| Domain Architect | [`references/domain-architect.md`](references/domain-architect.md) | architect | 5-6 | `author` | `role-author` |
| Data Architect | [`references/data-architect.md`](references/data-architect.md) | architect | 5-6 | `author` | `role-author` |
| Integration Architect | [`references/integration-architect.md`](references/integration-architect.md) | architect | 5-6 | `author` | `role-author` |
| Cloud Architect | [`references/cloud-architect.md`](references/cloud-architect.md) | architect | 4-6 | `author` | `role-author` |
| Network Architect | [`references/network-architect.md`](references/network-architect.md) | architect | 5-6 | `author` | `role-author` |
| Security Architect | [`references/security-architect.md`](references/security-architect.md) | architect | 5-6 | `author` | `role-author` |
| AI and ML Architect | [`references/ai-and-ml-architect.md`](references/ai-and-ml-architect.md) | architect | 5-6 | `author` | `role-author` |
| Technical Design Authority Member | [`references/technical-design-authority-member.md`](references/technical-design-authority-member.md) | architect | 5-6 | `author` | `role-author` |

| Architecture Repository and Modelling Lead | [`references/architecture-repository-and-modelling-lead.md`](references/architecture-repository-and-modelling-lead.md) | architect | 5-6 | `author` | `role-author` |
| Identity and Access Management Architect | [`references/identity-and-access-management-architect.md`](references/identity-and-access-management-architect.md) | architect | 5-6 | `author` | `role-author` |
| Operational and Technology Resilience Architect | [`references/operational-and-technology-resilience-architect.md`](references/operational-and-technology-resilience-architect.md) | architect | 5-6 | `author` | `role-author` |
| Enterprise Applications Architect | [`references/enterprise-applications-architect.md`](references/enterprise-applications-architect.md) | architect | 5-7 | `author` | `role-author` |
| Secure Delivery / DevSecOps Architect | [`references/secure-delivery-devsecops-architect.md`](references/secure-delivery-devsecops-architect.md) | architect | 5-6 | `author` | `role-author` |
| Application Portfolio Manager | [`references/application-portfolio-manager.md`](references/application-portfolio-manager.md) | manage | 5-6 | `author` | `role-author` |

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
