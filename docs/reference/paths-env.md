# Paths and environment variables

## Installation and runtime

| Variable | Default | Purpose |
| --- | --- | --- |
| `AI_IT_HOME` | `~/.ai` | Installer base AI IT data home |
| `AI_IT_HOUSE` | `<AI_IT_HOME>/it-role-house` (normally `~/.ai/it-role-house`) | Common runtime destination; an explicit value overrides the derived path |
| `CLAUDE_HOME` | `~/.claude` | Claude-facing provider surface |
| `CODEX_HOME` | `~/.codex` | Codex-facing provider surface |
| `AI_HOUSE_MODEL_CONFIG` | `~/.config/ai-it-house/models.json` | Model-routing override |

No path-variable exports are needed for the standard installation. These installer destination overrides do not migrate existing files or establish complete runtime relocation; generated instructions still reference the standard runtime path. See [installation path overrides](../configuration/runtime.md#installation-path-overrides) before using nonstandard destinations.

## Justifiable Fabric

| Variable | Default | Purpose |
| --- | --- | --- |
| `FABRIC_HOME` | `./.fabric` | Fabric record location |
| `FABRIC_AUTHORITY_KEY` | `~/.config/justifiable-fabric/authority.key` | HMAC authority key |
| `FABRIC_MAX_REWORK` | `3` | Rework bound |
| `FABRIC_MAX_REFORMULATE` | `2` | Reformulation bound |
| `FABRIC_MAX_CONTRACTS` | `40` | Contract bound |
| `FABRIC_MAX_ROUNDS` | `5` | Revision-round bound |
| `FABRIC_MAX_STEPS` | `120` | Shared episode budget |
