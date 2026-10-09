---
name: it-roles-network-and-telecommunications
description: "Network and Telecommunications role skills: 9 defined roles covering network engineer; network administrator; network operations centre analyst; wireless and rf engineer; unified communications engineer; sd-wan and edge engineer; firewall and perimeter engineer; dns dhcp and ipam specialist; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within network and telecommunications. Read the matching file in references/ before answering."
allowed-tools: Read, Grep, Glob
---

# Network and Telecommunications — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-engineer`.

`category-index: 09`  ·  `roles: 9`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`  ·  `licence: BSD-4-Clause`

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
| Network Engineer | [`references/network-engineer.md`](references/network-engineer.md) | operate | 3-5 | `execute` | `role-engineer` |
| Network Administrator | [`references/network-administrator.md`](references/network-administrator.md) | operate | 2-4 | `execute` | `role-engineer` |
| Network Operations Centre Analyst | [`references/network-operations-centre-analyst.md`](references/network-operations-centre-analyst.md) | operate | 2-4 | `execute` | `role-engineer` |
| Wireless and RF Engineer | [`references/wireless-and-rf-engineer.md`](references/wireless-and-rf-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Unified Communications Engineer | [`references/unified-communications-engineer.md`](references/unified-communications-engineer.md) | operate | 3-5 | `execute` | `role-engineer` |
| SD-WAN and Edge Engineer | [`references/sd-wan-and-edge-engineer.md`](references/sd-wan-and-edge-engineer.md) | build | 4-6 | `execute` | `role-engineer` |
| Firewall and Perimeter Engineer | [`references/firewall-and-perimeter-engineer.md`](references/firewall-and-perimeter-engineer.md) | operate | 3-5 | `execute` | `role-engineer` |
| DNS DHCP and IPAM Specialist | [`references/dns-dhcp-and-ipam-specialist.md`](references/dns-dhcp-and-ipam-specialist.md) | operate | 3-5 | `execute` | `role-engineer` |
| Network Field Technician | [`references/network-field-technician.md`](references/network-field-technician.md) | operate | 1-3 | `execute` | `role-engineer` |

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
