# Tool hooks, runtime controls and release checks

JAI combines provider hooks, runtime contracts and checks on particular outputs.
These controls have different purposes. Installing a hook does not demonstrate
that a provider has loaded it; inspect the active host configuration and events
when relying on its behavior.

## Separate the control boundaries

| Mechanism | Activation | What it establishes |
| --- | --- | --- |
| Role or workflow routing | A selected skill or command and actual agent actions | A specialist or process choice; no universal message interceptor. |
| Reference and content-specification resolution | Explicit runtime operations | Applicable content obligations and illustrative references. |
| Provider hook | A configured provider tool or lifecycle event | A local allow/deny decision or recorded observation within that event's coverage. |
| Domain validation | A semantic model and its checker | Findings about that artifact and its particular inputs. |
| Product release workflow | A matching release tag on reviewed source | Source, test, documentation and archive checks before package publication; no acceptance of a customer output. |

An interactive code hook does not replace runtime authorization or the product
release workflow. None of these mechanisms supplies human authority by itself.

## Packaged hooks and provider events

Canonical hooks live in `.ai/runtime/hooks/`. The installer merges registrations
from `.ai/adapters/claude/settings.snippet.json` or
`.ai/adapters/codex/hooks.snippet.json` into the selected provider configuration.
Codex requests review of changed hooks after installation or update. Start a new
provider session after installation so its instructions can be loaded.

| Hook | Claude registration | Codex registration |
| --- | --- | --- |
| `guard_library_write.py` | `PreToolUse`: `Write`, `Edit`, `MultiEdit`, `NotebookEdit` | `PreToolUse`: `Write`, `Edit`, `apply_patch` |
| `guard_authority.py` | `PreToolUse`: `Bash`, `PowerShell`, `Read`, `Write`, `Edit`, `MultiEdit`, `NotebookEdit` | `PreToolUse`: `Bash`, `Read`, `Write`, `Edit`, `apply_patch` |
| `code_gate.py` | `PostToolUse`: `Write`, `Edit`, `MultiEdit`, `Bash`, `PowerShell`; `PostToolUseFailure`: `Bash`, `PowerShell`; `Stop`, `SubagentStop` | `PostToolUse`: `Write`, `Edit`, `apply_patch`, `Bash`; `Stop`, `SubagentStop` |

The table describes shipped registrations. A handler's support for a tool name
does not mean a provider emits the corresponding event. Provider versions,
aliases, configuration and effective sandbox permissions determine actual coverage.

### Library changes

`guard_library_write.py` checks recognized target paths against protected library
resources and the applicable approval record. Proposed library changes use a
separate staging path. The hook recognizes named write targets and Codex patch
target lines; it is not a filesystem sandbox or a complete shell mutation monitor.
Host permissions remain the boundary for operations that hooks cannot observe.

### Human authority and records

`guard_authority.py` recognizes authority-sensitive commands, protected records
and signing-key locations. Claude can receive an interactive `ask` decision for
supported authority actions; noninteractive modes deny them. Codex cannot turn a
hook response into that approval prompt, so the human must run the exact reserved
command in the host terminal. The agent does not manufacture this approval.

This string/path guard supplements the host sandbox. It does not establish
identity, protect an unrestricted private key or make local records immutable.
For key creation, exact signing requests and public enrollment, see
[human authority](../operations/human-authority.md).

### Interactive code and documentation checks

`code_gate.py` records issues detected after observed edits, recognizes supported
test commands and checks outstanding issues when a session stops. Tests must run
after the tracked production change. A successful recognized command does not
prove exhaustive coverage, and post-tool checks do not undo an edit.

These are bounded session checks, not universal completion enforcement. Project
opt-out markers and repeated-stop behavior can change reporting. Inspect the
reported issues and the actual commands rather than treating a clean stop as a
professional review or acceptance.

## Product release checks

A pushed `release@YY.MM.VV` tag starts the release workflow. The tagged commit
must be on `main` and its version must match committed `VERSION`. The workflow
performs bounded source, policy, registry and documentation checks, builds the
public site, then constructs a deterministic source archive, SHA-256 checksum
and SPDX source/dependency inventory. It does not run the full regression suite
or install Office renderers. Before publication the operator runs the complete
maintained suite locally with `python3 scripts/prepublish.py --root .`.

A separate job publishes the checked assets only after validation succeeds and
refuses to overwrite an existing release. The workflow does not use historical
development results to qualify changed source. Local documentation builds do not
execute a remote release or demonstrate live provider behavior. See
[version and release tags](../reference/versioning.md) for the preparation and
publication boundary, and [release controls](../operations/validation.md) for
operator responsibilities.

## Domain and publication controls remain separate

Content checks assess required semantic fields, applicability and evidence.
Publication projection preserves an approved semantic snapshot and its lineage;
rendering and visual inspection assess the actual produced files. Missing
required evidence or an unavailable renderer does not become a passing result.

These controls do not make fictional examples true, substitute for independent
review or grant L0 acceptance. See
[document content specifications](../capabilities/document-content-specifications.md),
[reference and context delivery](../reference/reference-selection-context.md) and
[publication](../capabilities/artifacts-publication.md).
