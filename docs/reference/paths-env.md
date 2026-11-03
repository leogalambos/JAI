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
| `FABRIC_HOME` | `~/.ai/fabric` | Fabric CLI engagement-journal location |

Process-host commands may instead supply an explicit Store path. The host,
queries, continuation and any reserved signed decision must refer to the same
actual engagement. See [runtime paths](../configuration/runtime.md).

Current local iteration and rework allowances belong to the recorded profile;
assignment allowances and any explicitly requested overall stop are governed
inputs. Retired `FABRIC_MAX_*` and `FABRIC_AUTHORITY_KEY` settings neither reset
those limits nor grant authority. Ordinary recording needs no signing key.
Only reserved human decisions use the external operator signing procedure.
