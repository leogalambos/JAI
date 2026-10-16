---
name: it-roles-commercial-sourcing-and-enablement
description: "Commercial, Sourcing and Enablement role skills: 20 defined roles covering supplier bid/proposal management, estimation and cost engineering, commercial pricing and deal finance, supplier commercial lifecycle management, independent commercial assurance, procurement, contracts, pre-sales and enablement. Use for these specialist deliverables or role design, RACI and segregation of duties. Read the matching reference before operating; technical pre-sales, TBM and FinOps do not substitute for supplier commercial specialists."
allowed-tools: Read, Grep, Glob
---

# Commercial, Sourcing and Enablement — role skills

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-advisor`, `role-author`.

`category-index: 15`  ·  `roles: 20`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.1.0`  ·  `licence: BSD-4-Clause`

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
| IT Procurement Specialist | [`references/it-procurement-specialist.md`](references/it-procurement-specialist.md) | manage | 3-5 | `author` | `role-author` |
| Vendor Manager | [`references/vendor-manager.md`](references/vendor-manager.md) | manage | 4-6 | `author` | `role-author` |
| Contract Manager | [`references/contract-manager.md`](references/contract-manager.md) | manage | 4-6 | `author` | `role-author` |
| Software Licence Compliance Specialist | [`references/software-licence-compliance-specialist.md`](references/software-licence-compliance-specialist.md) | assure | 3-5 | `advise` | `role-advisor` |
| Pre-Sales Solution Consultant | [`references/pre-sales-solution-consultant.md`](references/pre-sales-solution-consultant.md) | enable | 4-6 | `author` | `role-author` |
| Sales Engineer | [`references/sales-engineer.md`](references/sales-engineer.md) | enable | 3-5 | `author` | `role-author` |
| Customer Success Engineer | [`references/customer-success-engineer.md`](references/customer-success-engineer.md) | enable | 3-5 | `author` | `role-author` |
| Implementation Consultant | [`references/implementation-consultant.md`](references/implementation-consultant.md) | enable | 3-5 | `author` | `role-author` |
| Technical Account Manager | [`references/technical-account-manager.md`](references/technical-account-manager.md) | enable | 4-6 | `author` | `role-author` |
| Technical Writer | [`references/technical-writer.md`](references/technical-writer.md) | enable | 3-5 | `author` | `role-author` |
| Developer Advocate | [`references/developer-advocate.md`](references/developer-advocate.md) | enable | 4-6 | `author` | `role-author` |
| IT Trainer | [`references/it-trainer.md`](references/it-trainer.md) | enable | 3-5 | `author` | `role-author` |
| Technical Recruiter | [`references/technical-recruiter.md`](references/technical-recruiter.md) | enable | 3-5 | `author` | `role-author` |
| Resource Manager | [`references/resource-manager.md`](references/resource-manager.md) | manage | 3-5 | `author` | `role-author` |
| IT Financial Management / TBM Manager | [`references/it-financial-management-tbm-manager.md`](references/it-financial-management-tbm-manager.md) | manage | 5-6 | `author` | `role-author` |
| Bid / Proposal Manager | [`references/bid-proposal-manager.md`](references/bid-proposal-manager.md) | manage | 4-6 | `author` | `role-author` |
| Commercial Pricing / Deal Finance Specialist | [`references/commercial-pricing-deal-finance-specialist.md`](references/commercial-pricing-deal-finance-specialist.md) | manage | 5-6 | `author` | `role-author` |
| Estimation / Cost Engineering Specialist | [`references/estimation-cost-engineering-specialist.md`](references/estimation-cost-engineering-specialist.md) | manage | 4-6 | `author` | `role-author` |
| Independent Commercial Assurance Reviewer | [`references/independent-commercial-assurance-reviewer.md`](references/independent-commercial-assurance-reviewer.md) | assure | 5-6 | `advise` | `role-advisor` |
| Supplier Commercial / Deal Manager | [`references/supplier-commercial-deal-manager.md`](references/supplier-commercial-deal-manager.md) | manage | 5-6 | `author` | `role-author` |

## Supplier commercial specialisation

For supplier proposals, route response coordination to Bid / Proposal Manager, work and cost uncertainty to Estimation / Cost Engineering Specialist, selling price and cash economics to Commercial Pricing / Deal Finance Specialist, and negotiation plus post-award commercial exposure to Supplier Commercial / Deal Manager. Route independent challenge to Independent Commercial Assurance Reviewer using a separate operator. Read only the references needed for the current handoff.

Pre-sales owns technical solution evidence; TBM owns enterprise cost/allocation methodology; buyer procurement owns buying activities. They supply specialist inputs without replacing the five supplier commercial responsibilities. Human bid/no-bid, price approval, signature and risk acceptance remain reserved under delegated authority.

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

2 of the 20 roles here are `advise` tier (`Read, Grep, Glob, WebSearch`) because their work is assurance or oversight. Operate them with `role-advisor`: return analysis and findings, and hand file changes to an authorised writer. The independent reviewer does not repair or author the evidence it judges.
