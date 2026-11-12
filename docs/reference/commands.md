# Command reference


## Operator syntax versus implementation API

The slash commands below are **Claude Code conversation commands**. In **Codex CLI** invoke the corresponding skill (`/layered` → `$workflow-layered`, `/fabric-report` → `$workflow-fabric-report`, `/sabsa` → `$workflow-sabsa`) and provide the arguments in the Codex conversation. These are neither Bash programs nor aliases for `fabric.py`. The provider agent performs the allowed internal tool calls; if a step is blocked it must report the failure. Use the [interaction guide](../using/interaction-model.md) and the [layered walk-through](../using/layered-engagement.md) to distinguish operator actions from implementation.

**Exception:** human L0 authority cannot be delegated. In Codex the agent prepares an exact command and the human executes that authority operation in a trusted terminal; see [Human authority](../operations/human-authority.md).

## Choosing the workflow boundary

First-time readers should follow [How to use JAI](../examples/how-to-use-JAI/index.md), which places the method before its complete worked cases. This reference is for syntax and lookup after choosing the arrangement.

`/sabsa` supplies security-architecture methods; `/commercial` supplies the supplier commercial-delivery profile. `/layered` supplies the six-layer assurance process and can contain either domain workflow. You may use a domain command directly, govern its creation through `/layered`, or use `/layered` later for a **new decision** against the domain's exact snapshot. The later decision does not retroactively prove the earlier creation process. See [the methodical workflow guide](../using/methodical-workflows.md) for the choice table, complete examples and acceptance checkpoints.

In Codex, `/commercial` maps to `$workflow-commercial` in an installation generated from the commercial command source. Continuation instructions such as “Continue engagement <ID>” are natural-language requests, not implemented `resume` subcommands. Preserve and inspect existing engagement state before proceeding.

## High-level workflow commands

`/layered` uses the Gen2 native bridge and the current SABSA layer model. Each
question has a local setter, author and independent reviewer; the layer then
integrates reviewed results before an adjacent handoff. Professions and models
are chosen locally from the retained catalogue. See the
[layered delivery](../using/layered-engagement.md) for the
implemented source boundary and actual activation evidence. Completion does not
grant human acceptance or release permission.

`/fabric-report` (`$workflow-fabric-report` in Codex) independently explains the
recorded current basis of exact Gen2 output versions. It distinguishes historical
integrity, relevant supporting material, qualification, human acceptance and
release. Missing or ambiguous outputs are reported explicitly; the audit does
not select replacements or grant permission. See the
[review and release readiness](../operations/validation.md) for scope and
activation limits.

Retained library, research and domain commands preserve their ordinary native
workflows. Their consequential branches use the shared Gen2 native handoff;
commercial and publication callbacks bind actual recorded work to exact scoped
outputs. Draft preparation grants no acceptance or release. See the
[review and release readiness](../operations/validation.md)
for the seventeen-command wiring scope and qualification limits.

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

Expected outputs depend on the requested stage: a discovery/assumption record, linked work packages and estimates, resource and economic models, review evidence, distinct client/internal projections, and unresolved human decisions. For a complete bid, commission the [full audience-specific work-product set](../capabilities/commercial-delivery.md#complete-bid-documents-and-readers), including actual internal calculation models and same-version capacity/feasibility dispositions; the eight linked client drafts alone are insufficient. The command reuses existing phase checks and projection facilities through authorised operators; the coordinator remains read-only. The command does not approve a bid or authorise a contract. Strict provider dispatch requires qualified execution controls; shipped capability records remain `not_run`. See [Commercial delivery](../capabilities/commercial-delivery.md) and [the worked proposal sequences](../using/methodical-workflows.md#4-example-prepare-an-enterprise-proposal).

## DCS foundation inspection

The shared `content_spec.py` tool provides `list`, `resolve --artifact-id ID`,
`compile --spec-ref ID`, `lint-registry` and `coverage`, each with `--root PATH`.
Resolution and compilation accept `--context FILE`. These inspect proposed
content obligations; they do not approve standards or run 26.10.7 content QA.
See [Document Content Specifications](../capabilities/document-content-specifications.md)
for scope, compatibility and the human acceptance boundary.

## Current operator boundary

For {{ JAI_VERSION }} {{ JAI_SCOPE }} use the [exact operator walkthrough](../operations/operator-walkthrough.md).
Native provider approval is not Fabric L0; external Ed25519 receipts require
protected trust and matching state. Actual Office QA uses route A when a working native Office renderer is available
within the permitted environment, or route C through the operator when required;
WeasyPrint HTML/PDF does not inspect Office bytes. Privileged worker/API
mutation is NOT_SUPPORTED; optional host confinement is NOT_VERIFIED.

## Execution preferences and efficiency

`/jai-profile` maps to `$workflow-profile`, and `/jai-stats` maps to
`$workflow-stats`. Both run inside the native conversation. The operator does not
need an external console. With no arguments, the first lists selectable profiles
and active configuration; the second shows compact recorded project history.

Use `/jai-profile stronger-reviewer` to select a project default, `show NAME` to
inspect a profile, `effective` for resolved settings, or `NAME --session` for
subsequent new runs in this conversation only. Existing runs retain their snapshot.
Use `/jai-stats last`, `profile NAME` or `compare A B` for recorded metrics.
The default task footer is a compact one-row table after the result. Unknown usage
or unrecorded workflows are explicit; no profile switches automatically.
See [execution profiles](../configuration/execution-profiles.md).


`/jai-profile workload` / `$workflow-profile workload` explicitly restore
class-based routing for future runs without deleting project settings. Add
`--local` when a project-local selection shadows the shared choice, or `--session`
for this conversation. Effective diagnostics distinguish routing mode from the
configured flag and show session context separately from persisted defaults.
