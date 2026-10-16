---
owner: JAI documentation maintainers
review_due: 2027-01-16
---

# Concepts, demonstrations and review controls

Use this page to look up the concepts shared by JAI workflows. For a first engagement, follow [How to use JAI](../examples/how-to-use-JAI/index.md): method, interaction, then a complete case. For a short installation exercise use the [20-minute quick start](../getting-started/quick-start.md).

This page replaces a duplicated handbook tour. The detailed command exercises remain in [Command walkthroughs](../reference/command-walkthroughs.md); the generated installed handbook has its maintained source in [Installed CLI guide](../reference/installed-cli-guide.md). Those references support lookup rather than establish a second beginner reading order.

## Provider use and the implementation explained

Enter slash commands in Claude Code and `$workflow-<name>` skills in Codex conversations. The provider orchestrates agents and runtime tools; users supply scope and evidence, inspect results and make reserved decisions. Runtime Python commands are maintainer interfaces, except for exact human authority commands handed to the operator where required. See [Interaction patterns](interaction-model.md).

## Getting started and demonstration tour

Install the package, check task-specific [environment prerequisites](../getting-started/sandbox-prerequisites.md), start a fresh provider session and follow the [quick start](../getting-started/quick-start.md). The [demo estate](demo-estate.md) supplies seeded code, document and client-material workspaces. Its exercises are separate learning activities, not evidence that a single engagement completed the full lifecycle.

## Core concepts

### Review criteria

Criteria state what the reviewer will judge before inspecting the target. Resolve them from the request, project criteria, personal defaults or the package's target-specific defaults. The review records the selected criteria and their fingerprint; findings identify the applicable criterion. See `/criteria` and `/review` in the [command walkthroughs](../reference/command-walkthroughs.md).

### The findings ledger

The append-only ledger records open, resolved, verified, stuck, accepted and withdrawn findings. The reviewer never fixes the target; the author never verifies its own repair. Repeated non-convergence reaches a bounded stop and the decision owner. Do not edit `.findings/` directly. See `/rework` in the [command reference](../reference/installed-cli-guide.md).

### Approvals

Review, snapshot approval, risk acceptance and release authorisation are different states. The relevant human must perform reserved authority acts. In Codex, an agent cannot run the protected L0 operation; it supplies the exact command for the human's trusted terminal. See [Human authority and escalation](../operations/human-authority.md).

### SABSA library layout

A canonical library contains source material, typed architecture entries, answers to the 36 matrix cells, authored narrative and snapshot approval state. Generated documents and CSV catalogues are projections of that model. They do not create a second semantic authority. See [SABSA and EA capabilities](../capabilities/sabsa-ea.md) and the [security-assessment case](../examples/how-to-use-JAI/security-assessment.md).

### Defect analysis

Diagnosis precedes a fix. Compare the failing state with the last known good state, a working analogue and timing/order behaviour. Record evidence for competing hypotheses, distinguish root cause from trigger, and require a regression that exposes the defect. See [Research and defect analysis](../capabilities/research-defect.md).

### Source code documentation and tests

Engineering changes follow the installed code-documentation and testing standards. Documentation describes public contracts and design reasons; meaningful tests cover affected normal, boundary and failure behaviour. Report actual post-change execution results and unavailable prerequisites. See `/develop` in the [installed CLI guide](../reference/installed-cli-guide.md) and [Validation and release controls](../operations/validation.md).

### Decision records (`/layered`)

The Fabric records intent, requirements, contracts, fragments, evidence, reviews, unsuccessful attempts, reformulation and escalation. A new layered decision can use existing domain material; it does not recreate the history of that material. See [Methodical workflows](methodical-workflows.md) for mode selection and [Running a layered engagement](layered-engagement.md) for the complete cycle.

## Command overview

Use [Commands and direct tools](commands.md) to select an entry point, [Command reference](../reference/commands.md) for syntax and [Command walkthroughs](../reference/command-walkthroughs.md) for individual demonstrations. The [workflow library](workflows.md) specifies enterprise stages and handoffs. A domain workflow, a role, a model selector and a runtime tool serve different purposes.

## Troubleshooting

If a command is unavailable, check the installed version and start a fresh provider session. If tools fail, identify the environment or permission boundary rather than treating a fluent response as successful execution. Use [Troubleshooting](../operations/troubleshooting.md), [Sandbox prerequisites](../getting-started/sandbox-prerequisites.md) and [Current runtime help](../runtime-reference/current-help.md). Report unperformed checks as unverified.
