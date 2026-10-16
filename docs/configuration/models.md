# Providers, models and reasoning effort

AI IT House does not hard-code provider model names into the role knowledge. Instead, agents use workload classes that are resolved by the provider adapter.

## Workload classes

| Class | Intended workload | Typical use |
| --- | --- | --- |
| `light` | low-cost, fast bounded work | routing, inventory, simple structured tasks |
| `standard` | mainstream professional work | most authoring, normal analysis, standard reviews |
| `heavy` | high-complexity work | architecture, policy, diagnosis, consequential synthesis |
| `research` | highest-complexity exploratory work | deep investigation, novel methods, high uncertainty |

## Default mapping in 26.10.4

| Workload | Claude | Codex/OpenAI | Codex reasoning effort |
| --- | --- | --- | --- |
| `light` | `haiku` | `gpt-6-luna` | `low` |
| `standard` | `sonnet` | `gpt-6.1-sol` | `medium` |
| `heavy` | `opus` | `gpt-6-astra` | `high` |
| `research` | `opus` | `gpt-6-astra` | `xhigh` |

## Why reasoning effort matters

In the Codex mapping, reasoning effort is part of the routing policy. This lets the organisation align cost, latency and quality expectations by workload class rather than by editing every role definition.

## Effective routing files

Package default:

```text
~/.ai/it-role-house/models/model-registry.json
```

Effective merged copy used by the installation:

```text
~/.ai/it-role-house/models/effective-model-registry.json
```

## Responsibility boundary

A normal Claude/Codex user selects the business task and, where relevant, requests a stronger or cheaper quality/cost profile in the conversation. A **deployment administrator** owns these provider mappings and installs/validates model-routing overrides; changing environment variables or JSON files is a system-configuration action, not a per-engagement user step. Codex/Claude adapters resolve the effective workload class when dispatching agents. Do not infer successful isolation or a particular live model version from the mere presence of a mapping string; verify against the actual provider invocation and policy.

## Organisation-specific override patterns

Default override path:

```text
~/.config/ai-it-house/models.json
```

Environment variable:

```bash
export AI_HOUSE_MODEL_CONFIG=/secure/config/ai-it-house-models.json
```

Installation argument:

```bash
./install.sh --model-config /secure/config/ai-it-house-models.json
```

## Example override

```json
{
  "providers": {
    "codex": {
      "classes": {
        "standard": {
          "model_selector": "gpt-5.6-sol",
          "reasoning_effort": "medium"
        }
      }
    }
  }
}
```

## Validation commands — administrator or CI

```bash
python3 ~/.ai/it-role-house/tools/model_router.py self-test
python3 ~/.ai/it-role-house/tools/provider_parity.py
```

These should be part of any controlled enterprise upgrade.
