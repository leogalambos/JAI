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

```bash
export AI_IT_HOME=/opt/company-ai
export AI_IT_HOUSE=/opt/company-ai/it-role-house
export CLAUDE_HOME=/home/user/.claude
export CODEX_HOME=/home/user/.codex
```

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
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../models/"><small>← Previous · Configuration</small><strong>Providers, models & reasoning effort</strong></a>
  <a class="ai-next" href="../policy/"><small>Next · Configuration →</small><strong>Governance, policy & approvals</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
