# Command reference

Owner: JAI maintainers · Last reviewed: 2026-10-20

## Operator syntax versus implementation API

The slash commands below are **Claude Code conversation commands**. In **Codex CLI** invoke the corresponding skill (`/layered` → `$workflow-layered`, `/fabric-report` → `$workflow-fabric-report`, `/sabsa` → `$workflow-sabsa`) and provide the arguments in the Codex conversation. These are neither Bash programs nor aliases for `fabric.py`. The provider agent performs the allowed internal tool calls; if a step is blocked it must report the failure. Use the [interaction guide](../using/interaction-model.md) and the [layered walk-through](../using/layered-engagement.md) to distinguish operator actions from implementation.

**Exception:** human L0 authority cannot be delegated. In Codex the agent prepares an exact command and the human executes that authority operation in a trusted terminal; see [Human authority](../operations/human-authority.md).

## Choosing the workflow boundary

First-time readers should follow [How to use JAI](../examples/how-to-use-JAI/index.md), which places the method before its complete worked cases. This reference is for syntax and lookup after choosing the arrangement.

`/sabsa` supplies security-architecture methods; `/commercial` supplies the supplier commercial-delivery profile. `/layered` supplies the six-layer assurance process and can contain either domain workflow. You may use a domain command directly, govern its creation through `/layered`, or use `/layered` later for a **new decision** against the domain's exact snapshot. The later decision does not retroactively prove the earlier creation process. See [the methodical workflow guide](../using/methodical-workflows.md) for the choice table, complete examples and acceptance checkpoints.

In Codex, `/commercial` maps to `$workflow-commercial` in an installation generated from the commercial command source. Continuation instructions such as “Continue engagement <ID>” are natural-language requests, not implemented `resume` subcommands. Preserve and inspect existing engagement state before proceeding.

## High-level workflow commands

=== "Claude Code"

    ```text
    /demo setup|list|reset|check
    /guide [command|topic]
    /hint <natural-language project question>
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

=== "Codex CLI"

    ```text
    $workflow-demo setup|list|reset|check
    $workflow-guide [command|topic]
    $workflow-hint <natural-language project question>
    $workflow-analyse <path or description>
    $workflow-criteria <path>
    $workflow-review <path> [against <criteria>]
    $workflow-rework [ledger]
    $workflow-diagnose <symptom, failing test or issue>
    $workflow-develop <what to build or change>
    $workflow-govern <target>
    $workflow-research <question>
    $workflow-sabsa <prepare|create|update|review|suggest|questions|approve|approval|document|template> ...
    $workflow-publish <semantic model> [archetype] [formats]
    $workflow-repository <init|validate|import|export|views|portfolio|impact|decommission> ...
    $workflow-commercial <opportunity, bid or delivery scope>
    $workflow-layered <consequential intent>
    $workflow-fabric-report [engagement]
    ```

Codex provides the corresponding `$workflow-<command>` surfaces. For command-by-command prerequisites, demos and expected verification, consult the [full installed CLI guide](installed-cli-guide.md) or the [extended example walkthroughs](command-walkthroughs.md). The installed `GUIDE.md` is generated from that single Markdown source.

## Experimental advisory hint

`/hint <project question>` (`$workflow-hint` in Codex) recommends an adapted
procedure from maintained examples. It interprets the request in English,
uses deterministic local candidate ranking and reads selected scenario steps.
Every answer carries the experimental advisory label, sources, assumptions,
paired commands and evidence/authority limits. It does not execute the proposed
work, create a demo, schedule monitoring or import project histories. Selection
scores are lexical points, not confidence. See the [installed hint reference](installed-cli-guide.md#hint).

### Explicit local knowledge capture

Ask `/hint` or `$workflow-hint` to remember the useful part of your current
conversation. The active provider prepares the English record; you do not
need to describe each technical step or supply JSON. It asks for missing
essential metadata and the authorised destination in ordinary language,
then continues the original save request after your answers. A request only
for a draft does not authorise saving. There is no new slash subcommand.

Capture uses only selected context actually available to the provider, not
an automatic full-history archive. Use a caller-owned library outside the
distributed tree and installed runtime. Saving supplies no human approval,
and records participate in hint selection only with explicit library and
read/disclosure permission. They do not automatically become demo projects.
See [Build and reuse local know-how](../using/reusing-knowledge.md) for
selection, revisions, export and recoverable deletion.
See [Remember useful knowledge](../using/remembering-knowledge.md) for worked
conversations and [capture boundaries](installed-cli-guide.md#explicit-local-knowledge-capture)
for the command contract.

## Commercial delivery

=== "Claude Code"

    ```text
    /commercial <opportunity, bid or delivery scope>
    ```

=== "Codex CLI"

    ```text
    $workflow-commercial <opportunity, bid or delivery scope>
    ```

Use this opt-in command to add supplier-side qualification, discovery, estimation, staffing, costing/pricing, terms, dual publication and delivery/service monitoring to an existing JAI engagement, or to establish that scope for a new one. Supply the source material, commercial owner, intended outputs and disclosure/commitment boundaries. The argument is a scoped request; there are no documented `/commercial prepare`, `review` or `approve` subcommands.

Expected outputs depend on the requested stage: a discovery/assumption record, linked work packages and estimates, resource and economic models, review evidence, distinct client/internal projections, and unresolved human decisions. The command does not approve a bid or authorise a contract. Strict provider dispatch requires qualified execution controls; shipped capability records remain `not_run`. See [Commercial delivery](../capabilities/commercial-delivery.md) and [the worked proposal sequences](../using/methodical-workflows.md#4-example-prepare-an-enterprise-proposal).

## DCS foundation inspection

The shared `content_spec.py` tool provides `list`, `resolve --artifact-id ID`,
`compile --spec-ref ID`, `lint-registry` and `coverage`, each with `--root PATH`.
Resolution and compilation accept `--context FILE`. These inspect proposed
content obligations; they do not approve standards or run 26.10.7 content QA.
See [Document Content Specifications](../capabilities/document-content-specifications.md)
for scope, compatibility and the human acceptance boundary.

## Current operator boundary

For 26.10.14 {{ JAI_SCOPE }} use the [exact operator walkthrough](../operations/operator-walkthrough.md).
Native provider approval is not Fabric L0; external Ed25519 receipts require
protected trust and matching state. Actual Office QA is OPERATOR_ASSISTED;
WeasyPrint HTML/PDF does not inspect Office bytes. Privileged worker/API
mutation is NOT_SUPPORTED; optional host confinement is NOT_VERIFIED.
