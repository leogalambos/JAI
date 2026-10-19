# Command reference

Owner: JAI maintainers · Last reviewed: 2026-10-16

## Operator syntax versus implementation API

The slash commands below are **Claude Code conversation commands**. In **Codex CLI** invoke the corresponding skill (`/layered` → `$workflow-layered`, `/fabric-report` → `$workflow-fabric-report`, `/sabsa` → `$workflow-sabsa`) and provide the arguments in the Codex conversation. These are neither Bash programs nor aliases for `fabric.py`. The provider agent performs the allowed internal tool calls; if a step is blocked it must report the failure. Use the [interaction guide](../using/interaction-model.md) and the [layered walk-through](../using/layered-engagement.md) to distinguish operator actions from implementation.

**Exception:** human L0 authority cannot be delegated. In Codex the agent prepares an exact command and the human executes that authority operation in a trusted terminal; see [Human authority](../operations/human-authority.md).

## Choosing the workflow boundary

First-time readers should follow [How to use JAI](../examples/how-to-use-JAI/index.md), which places the method before its complete worked cases. This reference is for syntax and lookup after choosing the arrangement.

`/sabsa` supplies security-architecture methods; `/commercial` supplies the supplier commercial-delivery profile. `/layered` supplies the six-layer assurance process and can contain either domain workflow. You may use a domain command directly, govern its creation through `/layered`, or use `/layered` later for a **new decision** against the domain's exact snapshot. The later decision does not retroactively prove the earlier creation process. See [the methodical workflow guide](../using/methodical-workflows.md) for the choice table, complete examples and acceptance checkpoints.

In Codex, `/commercial` maps to `$workflow-commercial` in an installation generated from the commercial command source. Continuation instructions such as “Continue engagement <ID>” are natural-language requests, not implemented `resume` subcommands. Preserve and inspect existing engagement state before proceeding.

## High-level workflow commands

```text
/demo setup|list|reset|check
/guide [command|topic]
/analyse <path or description>
/criteria <path>
/review <path> [against <criteria>]
/rework [ledger]
/diagnose <symptom, failing test or issue>
/develop <what to build or change>
/govern <target>
/research <question>
/sabsa <prepare|create|update|review|suggest|questions|approve|approval|document|template> ...
/publish <semantic model> [archetype] [formats]
/repository <init|validate|import|export|views|portfolio|impact|decommission> ...
/commercial <opportunity, bid or delivery scope>
/layered <consequential intent>
/fabric-report [engagement]
```

Codex provides the corresponding `$workflow-<command>` surfaces. For command-by-command prerequisites, demos and expected verification, consult the [full installed CLI guide](installed-cli-guide.md) or the [extended example walkthroughs](command-walkthroughs.md). The installed `GUIDE.md` is generated from that single Markdown source.

## Commercial delivery

**Claude Code:** `/commercial <opportunity, bid or delivery scope>`

**Codex:** `$workflow-commercial <opportunity, bid or delivery scope>`

Use this opt-in command to add supplier-side qualification, discovery, estimation, staffing, costing/pricing, terms, dual publication and delivery/service monitoring to an existing JAI engagement, or to establish that scope for a new one. Supply the source material, commercial owner, intended outputs and disclosure/commitment boundaries. The argument is a scoped request; there are no documented `/commercial prepare`, `review` or `approve` subcommands.

Expected outputs depend on the requested stage: a discovery/assumption record, linked work packages and estimates, resource and economic models, review evidence, distinct client/internal projections, and unresolved human decisions. The command does not approve a bid or authorise a contract. Strict provider dispatch requires qualified execution controls; shipped capability records remain `not_run`. See [Commercial delivery](../capabilities/commercial-delivery.md) and [the worked proposal sequences](../using/methodical-workflows.md#4-example-prepare-an-enterprise-proposal).

## DCS foundation inspection

The shared `content_spec.py` tool provides `list`, `resolve --artifact-id ID`,
`compile --spec-ref ID`, `lint-registry` and `coverage`, each with `--root PATH`.
Resolution and compilation accept `--context FILE`. These inspect proposed
content obligations; they do not approve standards or run 26.10.7 content QA.
See [Document Content Specifications](../capabilities/document-content-specifications.md)
for scope, compatibility and the human acceptance boundary.
