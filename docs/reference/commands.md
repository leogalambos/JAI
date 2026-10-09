# Command reference

## Operator syntax versus implementation API

The slash commands below are **Claude Code conversation commands**. In **Codex CLI** invoke the corresponding skill (`/layered` → `$workflow-layered`, `/fabric-report` → `$workflow-fabric-report`, `/sabsa` → `$workflow-sabsa`) and provide the arguments in the Codex conversation. These are neither Bash programs nor aliases for `fabric.py`. The provider agent performs the allowed internal tool calls; if a step is blocked it must report the failure. Use the [interaction guide](../using/interaction-model.md) and the [layered walk-through](../using/layered-engagement.md) to distinguish operator actions from implementation.

**Exception:** human L0 authority cannot be delegated. In Codex the agent prepares an exact command and the human executes that authority operation in a trusted terminal; see [Human authority](../operations/human-authority.md).

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
/layered <consequential intent>
/fabric-report [engagement]
```

Codex provides the corresponding `$workflow-<command>` surfaces. For command-by-command prerequisites, demos and expected verification, consult the [full installed CLI guide](installed-cli-guide.md) or the [extended example walkthroughs](command-walkthroughs.md). The installed `GUIDE.md` is generated from that single Markdown source.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../roles/"><small>← Previous · Reference</small><strong>Full role catalogue</strong></a>
  <a class="ai-next" href="../paths-env/"><small>Next · Reference →</small><strong>Paths and environment variables</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
