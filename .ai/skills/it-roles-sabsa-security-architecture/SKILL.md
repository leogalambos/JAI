---
name: it-roles-sabsa-security-architecture
description: "SABSA Security Architecture role skills: 12 defined roles covering chief security architect (sabsa practice lead); business security architect (sabsa contextual layer); business attribute profiler; conceptual security architect (sabsa architect's view); logical security designer (sabsa designer's view); physical security solution builder (sabsa builder's view); security component specialist (sabsa tradesman's view); security service manager (sabsa service management view); and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within sabsa security architecture. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# SABSA Security Architecture — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-advisor`, `role-author`, `role-engineer`.

`category-index: 17`  ·  `roles: 12`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| Chief Security Architect (SABSA Practice Lead) | [`references/chief-security-architect-sabsa-practice-lead.md`](references/chief-security-architect-sabsa-practice-lead.md) | architect | 6-7 | `author` | `role-author` |
| Business Security Architect (SABSA Contextual Layer) | [`references/business-security-architect-sabsa-contextual-layer.md`](references/business-security-architect-sabsa-contextual-layer.md) | architect | 5-6 | `author` | `role-author` |
| Business Attribute Profiler | [`references/business-attribute-profiler.md`](references/business-attribute-profiler.md) | analyze | 4-6 | `author` | `role-author` |
| Conceptual Security Architect (SABSA Architect's View) | [`references/conceptual-security-architect-sabsa-architect-s-view.md`](references/conceptual-security-architect-sabsa-architect-s-view.md) | architect | 5-6 | `author` | `role-author` |
| Logical Security Designer (SABSA Designer's View) | [`references/logical-security-designer-sabsa-designer-s-view.md`](references/logical-security-designer-sabsa-designer-s-view.md) | architect | 4-6 | `author` | `role-author` |
| Physical Security Solution Builder (SABSA Builder's View) | [`references/physical-security-solution-builder-sabsa-builder-s-view.md`](references/physical-security-solution-builder-sabsa-builder-s-view.md) | build | 4-6 | `execute` | `role-engineer` |
| Security Component Specialist (SABSA Tradesman's View) | [`references/security-component-specialist-sabsa-tradesman-s-view.md`](references/security-component-specialist-sabsa-tradesman-s-view.md) | build | 3-5 | `execute` | `role-engineer` |
| Security Service Manager (SABSA Service Management View) | [`references/security-service-manager-sabsa-service-management-view.md`](references/security-service-manager-sabsa-service-management-view.md) | manage | 4-6 | `author` | `role-author` |
| Security Domain Authority | [`references/security-domain-authority.md`](references/security-domain-authority.md) | govern | 5-6 | `advise` | `role-advisor` |
| Security Risk and Opportunity Architect | [`references/security-risk-and-opportunity-architect.md`](references/security-risk-and-opportunity-architect.md) | assure | 5-6 | `advise` | `role-advisor` |
| Security Assurance and Measurement Architect | [`references/security-assurance-and-measurement-architect.md`](references/security-assurance-and-measurement-architect.md) | assure | 5-6 | `advise` | `role-advisor` |
| SABSA and TOGAF Integration Architect | [`references/sabsa-and-togaf-integration-architect.md`](references/sabsa-and-togaf-integration-architect.md) | architect | 5-6 | `author` | `role-author` |

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

3 of the 12 roles here are `advise` tier (`Read, Grep, Glob, WebSearch`) because their work is assurance, oversight, evidential or adversarial. Operate them with `role-advisor`: analyse and document, and hand anything that changes a system to the role named in its interfaces section.
