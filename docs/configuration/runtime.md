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
| Fabric CLI records | `~/.ai/fabric/` |
| Purpose-specific public trust | `<runtime>/trust/jai-<purpose>-trust.json` |
| L0 private signing key | Host-only default or explicit alternate path; see [key creation and signing](../operations/human-authority.md#default-signing-key-and-host-script) |

## User versus deployment configuration

The explicit host [workflow interface](../operations/normal-layered-workflow.md) operates
against an already bootstrapped Store. Ordinary native users invoke `/layered`
in Claude or `$workflow-layered` in Codex; the native parent handles bootstrap
and transport. Explicit process-host integration supplies its configuration;
ordinary dispatch and recording require no private key. Only L0 signs explicit
decisions outside the agent sandbox. Known public trust files are fixed
runtime-relative inputs. Unix identity and an environment variable do not grant
decision authority. The human remains responsible for explicit L0 axioms and
resource risk; larger runtime limits do not make a result accepted.

## Installation path overrides

The standard installation needs no path-variable exports. The installer defaults to `AI_IT_HOME=~/.ai`, derives `AI_IT_HOUSE` as `<AI_IT_HOME>/it-role-house`, and uses `~/.claude` and `~/.codex` for the provider surfaces.

Administrators can override these installer destinations with `AI_IT_HOME`, `AI_IT_HOUSE`, `CLAUDE_HOME` and `CODEX_HOME`. If `AI_IT_HOUSE` is explicitly set, it takes precedence over the path derived from `AI_IT_HOME`. See the [environment reference](../reference/paths-env.md) for the defaults.

Destination overrides do not establish support for complete runtime relocation: generated instructions still contain references to `~/.ai/it-role-house`. A deployment using other destinations needs separate validation of its generated provider instructions and runtime paths. Exporting variables alone does not move or migrate an existing installation.

## Current Store location and recorded limits

| Variable | Default | Meaning |
| --- | ---: | --- |
| `FABRIC_HOME` | `~/.ai/fabric` | Fabric CLI engagement JSONL location |

`governed_workflow.py --store` and `governed_dispatch.py --store` name that exact
Store explicitly. An explicit L0 signed request must bind the same target path;
ordinary work requires no signed request.
Old `FABRIC_AUTHORITY_KEY` and `FABRIC_MAX_*` settings do not authorize current
effects. Current rework/reformulation limits belong to the recorded profile;
assignment/global allowances and deadlines are explicit immutable inputs, not
ambient defaults that a worker can increase.

## Operational reading

Selection and work use their applicable recorded local allowances. The runtime has a
finite readiness-driven coordinator, signed speculative grants and episode
handling under the recorded profile's `scheduling` bounds. It does not implement
an unbounded solver or a caller-controlled budget reset. Speculative permission
and current result qualification remain separate. The active native meter is
elapsed milliseconds; unsupported token/currency metering is not inferred.

## Implementation details

[Tool hooks, runtime controls and release gates](hooks-gates-verification.md) describes the inspected implementation.
Inspect the shipped provider event registrations and their enforcement limits.

Current Ed25519 public enrollment uses the purpose-specific governed keyring,
with explicit signer, capabilities, engagement/scope grants and validity windows.
Unsupported historical ledgers are archive-only, with no executable fallback.
See [operator workflows](../security/product-operations.md). In a host terminal,
the installer offers confirmed creation of the default operator key and preserves
an existing key. Key creation does not enrol trust or grant decision authority.
See [key creation and signing](../operations/human-authority.md#default-signing-key-and-host-script).

## Local QA and human intervention

Use A / AUTO for role-authorized local work inside the actual sandbox. B is
an observed native permission request; C is an exact operator host task. Neither
is Fabric L0. D is a separately signed consequential decision; it may precede C.
Every B/C/D request must include the complete action and reason inline before
linking details. See [execution routes and boundaries](../security/product-operations.md)
and the [full operator guide](../operations/operator-walkthrough.md).


## Supported release capabilities: one source

The version-controlled root `RELEASE-SCOPE.json` is the sole supported-release
capability declaration. It is not generated from Python. The installer copies
that exact manifest into the common runtime. `schema_resolver.release_scope`
validates the selected package/runtime against
`schema/release-scope.schema.json`; `agent_runtime.release_scope` is its runtime
API wrapper. Missing/invalid resources or a missing validator fail closed.
There is no current-working-directory, environment or CLI profile fallback.

The schema enumerates implemented feature vocabulary, not which features a
release supports. Edit only the manifest for a different supported subset or
compatible profile revision, then regenerate projections/docs and requalify.
A new implemented feature also requires actual implementation and schema work;
adding an arbitrary capability string is rejected. Privileged deployment and
agent-required Git remain prohibited by schema and independent runtime guards.
The manifest is product metadata, not permission, policy, L0 or an activation
switch. Editing it cannot create an executor or authorize a privileged effect.

Runtime projections, installer, release reports, compatibility/provenance and
generated documentation share this validation path. Website `JAI_SCOPE` tokens
and generated inventories derive from it; generated copies are not authorities.
Historical qualification records, release labels and schema identities remain
historical and are not rewritten to match the current declaration.
