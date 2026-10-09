---
name: it-roles-offensive-security-and-adversarial-testing
description: "Offensive Security and Adversarial Testing role skills: 21 defined roles covering penetration tester (network and infrastructure); penetration tester (web application); penetration tester (mobile); penetration tester (api); penetration tester (cloud); penetration tester (wireless); penetration tester (thick client); red team operator; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within offensive security and adversarial testing. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Offensive Security and Adversarial Testing — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-advisor`.

`category-index: 12`  ·  `roles: 21`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| Penetration Tester (Network and Infrastructure) | [`references/penetration-tester-network-and-infrastructure.md`](references/penetration-tester-network-and-infrastructure.md) | offend | 3-6 | `advise` | `role-advisor` |
| Penetration Tester (Web Application) | [`references/penetration-tester-web-application.md`](references/penetration-tester-web-application.md) | offend | 3-6 | `advise` | `role-advisor` |
| Penetration Tester (Mobile) | [`references/penetration-tester-mobile.md`](references/penetration-tester-mobile.md) | offend | 4-6 | `advise` | `role-advisor` |
| Penetration Tester (API) | [`references/penetration-tester-api.md`](references/penetration-tester-api.md) | offend | 4-6 | `advise` | `role-advisor` |
| Penetration Tester (Cloud) | [`references/penetration-tester-cloud.md`](references/penetration-tester-cloud.md) | offend | 4-6 | `advise` | `role-advisor` |
| Penetration Tester (Wireless) | [`references/penetration-tester-wireless.md`](references/penetration-tester-wireless.md) | offend | 3-5 | `advise` | `role-advisor` |
| Penetration Tester (Thick Client) | [`references/penetration-tester-thick-client.md`](references/penetration-tester-thick-client.md) | offend | 4-6 | `advise` | `role-advisor` |
| Red Team Operator | [`references/red-team-operator.md`](references/red-team-operator.md) | offend | 4-6 | `advise` | `role-advisor` |
| Red Team Lead | [`references/red-team-lead.md`](references/red-team-lead.md) | manage | 5-6 | `advise` | `role-advisor` |
| Exploit Developer | [`references/exploit-developer.md`](references/exploit-developer.md) | research | 5-6 | `advise` | `role-advisor` |
| Vulnerability Researcher | [`references/vulnerability-researcher.md`](references/vulnerability-researcher.md) | research | 5-6 | `advise` | `role-advisor` |
| Binary Reverse Engineer | [`references/binary-reverse-engineer.md`](references/binary-reverse-engineer.md) | research | 5-6 | `advise` | `role-advisor` |
| Social Engineering Specialist | [`references/social-engineering-specialist.md`](references/social-engineering-specialist.md) | offend | 4-6 | `advise` | `role-advisor` |
| Physical Intrusion Specialist | [`references/physical-intrusion-specialist.md`](references/physical-intrusion-specialist.md) | offend | 4-6 | `advise` | `role-advisor` |
| Open Source Intelligence Investigator | [`references/open-source-intelligence-investigator.md`](references/open-source-intelligence-investigator.md) | analyze | 3-5 | `advise` | `role-advisor` |
| Adversary Emulation Engineer | [`references/adversary-emulation-engineer.md`](references/adversary-emulation-engineer.md) | verify | 4-6 | `advise` | `role-advisor` |
| Breach and Attack Simulation Engineer | [`references/breach-and-attack-simulation-engineer.md`](references/breach-and-attack-simulation-engineer.md) | verify | 3-5 | `advise` | `role-advisor` |
| Bug Bounty Programme Manager | [`references/bug-bounty-programme-manager.md`](references/bug-bounty-programme-manager.md) | manage | 4-6 | `advise` | `role-advisor` |
| Bug Bounty Triage Analyst | [`references/bug-bounty-triage-analyst.md`](references/bug-bounty-triage-analyst.md) | verify | 3-5 | `advise` | `role-advisor` |
| Vulnerability Disclosure Coordinator | [`references/vulnerability-disclosure-coordinator.md`](references/vulnerability-disclosure-coordinator.md) | manage | 4-6 | `advise` | `role-advisor` |
| Hardware and IoT Security Researcher | [`references/hardware-and-iot-security-researcher.md`](references/hardware-and-iot-security-researcher.md) | research | 5-6 | `advise` | `role-advisor` |

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

21 of the 21 roles here are `advise` tier (`Read, Grep, Glob, WebSearch`) because their work is assurance, oversight, evidential or adversarial. Operate them with `role-advisor`: analyse and document, and hand anything that changes a system to the role named in its interfaces section.
