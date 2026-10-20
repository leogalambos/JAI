# Runtime paths and environment variables

## Standard paths

| Purpose | Default |
| --- | --- |
| AI IT House home | `~/.ai/it-role-house/` |
| Claude home | `~/.claude/` |
| Codex home | `~/.codex/` |
| Model override | `~/.config/ai-it-house/models.json` |
| Demo estate | `~/it-role-demo/` |
| Findings ledger | `<project>/.findings/` |
| Fabric records | `<project>/.fabric/` |
| Fabric authority key | `~/.config/justifiable-fabric/authority.key` |

## User versus deployment configuration

Ordinary users need not set any of these variables to start `/layered` or `$workflow-layered`; the orchestrator uses the installed defaults in the current workspace. The shell commands and Fabric budget settings below are **administrator/developer configuration**, applied only under the organisation's change and security policy. The human alone is responsible for accepted exceptions and revised risk tolerances; increasing runtime limits is not a substitute for those decisions.

## Installation path overrides

The standard installation needs no path-variable exports. The installer defaults to `AI_IT_HOME=~/.ai`, derives `AI_IT_HOUSE` as `<AI_IT_HOME>/it-role-house`, and uses `~/.claude` and `~/.codex` for the provider surfaces.

Administrators can override these installer destinations with `AI_IT_HOME`, `AI_IT_HOUSE`, `CLAUDE_HOME` and `CODEX_HOME`. If `AI_IT_HOUSE` is explicitly set, it takes precedence over the path derived from `AI_IT_HOME`. See the [environment reference](../reference/paths-env.md) for the defaults.

Destination overrides do not establish support for complete runtime relocation: generated instructions still contain references to `~/.ai/it-role-house`. A deployment using other destinations needs separate validation of its generated provider instructions and runtime paths. Exporting variables alone does not move or migrate an existing installation.

## Fabric-specific environment controls

| Variable | Default | Meaning |
| --- | ---: | --- |
| `FABRIC_HOME` | `./.fabric` | Engagement JSONL location |
| `FABRIC_AUTHORITY_KEY` | `~/.config/justifiable-fabric/authority.key` | HMAC authority key |
| `FABRIC_MAX_REWORK` | `3` | Rework attempts per contract lineage |
| `FABRIC_MAX_REFORMULATE` | `2` | Reformulations per layer/round |
| `FABRIC_MAX_CONTRACTS` | `40` | Contracts per round |
| `FABRIC_MAX_ROUNDS` | `5` | Human revision rounds |
| `FABRIC_MAX_STEPS` | `120` | Shared episode budget |

## Operational reading

Treat these environment variables as governance controls, not as mere performance knobs. Changing them alters what autonomous rework and escalation behaviour is permitted.

## Implementation details

[Tool hooks, runtime controls and release gates](hooks-gates-verification.md) describes the inspected implementation.
Inspect the shipped provider event registrations and their enforcement limits.
