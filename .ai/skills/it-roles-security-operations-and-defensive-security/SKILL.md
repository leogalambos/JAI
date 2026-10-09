---
name: it-roles-security-operations-and-defensive-security
description: "Security Operations and Defensive Security role skills: 24 defined roles covering security analyst tier 1; security analyst tier 2; security analyst tier 3; soc manager; threat hunter; incident responder; digital forensics examiner; malware analyst; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within security operations and defensive security. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Security Operations and Defensive Security — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `codebase-reviewer`, `role-advisor`, `role-author`, `role-engineer`.

`category-index: 11`  ·  `roles: 24`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| Security Analyst Tier 1 | [`references/security-analyst-tier-1.md`](references/security-analyst-tier-1.md) | defend | 2-3 | `author` | `role-author` |
| Security Analyst Tier 2 | [`references/security-analyst-tier-2.md`](references/security-analyst-tier-2.md) | defend | 3-5 | `author` | `role-author` |
| Security Analyst Tier 3 | [`references/security-analyst-tier-3.md`](references/security-analyst-tier-3.md) | defend | 4-6 | `author` | `role-author` |
| SOC Manager | [`references/soc-manager.md`](references/soc-manager.md) | manage | 5-6 | `author` | `role-author` |
| Threat Hunter | [`references/threat-hunter.md`](references/threat-hunter.md) | defend | 4-6 | `author` | `role-author` |
| Incident Responder | [`references/incident-responder.md`](references/incident-responder.md) | defend | 4-6 | `author` | `role-author` |
| Digital Forensics Examiner | [`references/digital-forensics-examiner.md`](references/digital-forensics-examiner.md) | defend | 4-6 | `inspect` | `codebase-reviewer` |
| Malware Analyst | [`references/malware-analyst.md`](references/malware-analyst.md) | defend | 4-6 | `inspect` | `codebase-reviewer` |
| Threat Intelligence Analyst | [`references/threat-intelligence-analyst.md`](references/threat-intelligence-analyst.md) | analyze | 4-6 | `author` | `role-author` |
| Detection Engineer | [`references/detection-engineer.md`](references/detection-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Security Engineer | [`references/security-engineer.md`](references/security-engineer.md) | build | 3-6 | `execute` | `role-engineer` |
| Vulnerability Management Analyst | [`references/vulnerability-management-analyst.md`](references/vulnerability-management-analyst.md) | manage | 3-5 | `author` | `role-author` |
| Cryptography and PKI Engineer | [`references/cryptography-and-pki-engineer.md`](references/cryptography-and-pki-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Secrets and Configuration Management Engineer | [`references/secrets-and-configuration-management-engineer.md`](references/secrets-and-configuration-management-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Identity and Access Management Engineer | [`references/identity-and-access-management-engineer.md`](references/identity-and-access-management-engineer.md) | build | 3-6 | `execute` | `role-engineer` |
| Identity Governance Specialist | [`references/identity-governance-specialist.md`](references/identity-governance-specialist.md) | assure | 3-5 | `advise` | `role-advisor` |
| Privileged Access Management Administrator | [`references/privileged-access-management-administrator.md`](references/privileged-access-management-administrator.md) | operate | 3-5 | `execute` | `role-engineer` |
| Cloud Security Engineer | [`references/cloud-security-engineer.md`](references/cloud-security-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Application Security Engineer | [`references/application-security-engineer.md`](references/application-security-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Security Champion | [`references/security-champion.md`](references/security-champion.md) | enable | 3-5 | `author` | `role-author` |
| Operational Technology Security Engineer | [`references/operational-technology-security-engineer.md`](references/operational-technology-security-engineer.md) | defend | 4-6 | `author` | `role-author` |
| Security Awareness and Training Manager | [`references/security-awareness-and-training-manager.md`](references/security-awareness-and-training-manager.md) | enable | 4-5 | `author` | `role-author` |
| Insider Threat Analyst | [`references/insider-threat-analyst.md`](references/insider-threat-analyst.md) | defend | 4-6 | `advise` | `role-advisor` |
| Purple Team Lead | [`references/purple-team-lead.md`](references/purple-team-lead.md) | verify | 5-6 | `advise` | `role-advisor` |

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

3 of the 24 roles here are `advise` tier (`Read, Grep, Glob, WebSearch`) because their work is assurance, oversight, evidential or adversarial. Operate them with `role-advisor`: analyse and document, and hand anything that changes a system to the role named in its interfaces section.
