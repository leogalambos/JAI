# Deployment and recovery


This procedure targets journal format **9**, semantic wire format
`jai.semantic-return/1` and host encoder `jai.semantic-encoder/2`. Use the actual
reviewed revision and file manifest; a release label alone does not identify
verified runtime bytes.

## Prerequisites and preparation

Installation uses Python 3.10+ and its standard library. Contract processing also
requires `jsonschema>=4.18,<5` in the selected runtime interpreter. An existing
compatible environment need not be replaced. See [installation](../getting-started/install.md).
Bubblewrap/libseccomp are requirements of the retained process backend, not
universal prerequisites for native Claude/Codex delegation.

Before replacing managed files, stop engagement writers and preserve outstanding
invocation identities. Back up software, managed provider configuration and public
trust. Retain each engagement's **newest journal, CAS directory, locator and pinned
enrollment** together. Installer backups do not replace operational data backups.
The installer offers operator-confirmed creation of a default signing key, as
described in [human authority](human-authority.md). Existing keys are preserved;
`--force-genkey` requires confirmation and keeps a private backup. Dry runs and
noninteractive installations never create keys. Generation does not enroll
public trust or grant signing authority; private keys remain outside agent access.

Freeze the exact source hashes, desired installation hashes/modes and selected
model registry. Record reviewed uncommitted delivery changes explicitly instead
of presenting a modified checkout as a clean commit. Preserve an operator's
valid existing model-registry override rather than silently selecting new models.

## Existing installer and verification

From the reviewed checkout, select an existing compatible interpreter:

```sh
JAI_RUNTIME_PYTHON=/absolute/path/to/python3
git rev-parse HEAD
"$JAI_RUNTIME_PYTHON" -c 'import sys; sys.path.insert(0,".ai/runtime/tools"); from runtime_dependencies import jsonschema_status; s=jsonschema_status(); print(s); raise SystemExit(s["status"]!="ready")'
JAI_PYTHON="$JAI_RUNTIME_PYTHON" bash ./install.sh --dry-run
```

Review the dry-run before applying the same plan:

```sh
JAI_PYTHON="$JAI_RUNTIME_PYTHON" bash ./install.sh
```

Use the same explicit `--model-config` selection on both commands when needed.
Exit status 2 means a managed-file conflict. Inspect actual local changes before
explicitly choosing the installer's existing `--force`; do not automatically retry
with force. Its backups cannot override evidence, applicability or permissions.

Equal content with different installed permissions is a mode-only delta. Normal
installation backs up the previous file and corrects its mode without rewriting
its content; dry-run reports the delta without changing it.

Verify every desired installed hash/mode against the reviewed plan, the complete
286-role population, 17 commands and selected provider routes, compatible Python
and unchanged unrelated settings/public trust. A successful copy or help response
does not establish that a model executed work. The checkout GUIDE is a symlink;
installation materializes its canonical bytes without depending on checkout paths.

`JAI_PYTHON` selects the installer interpreter only. Start a new provider session
with the chosen runtime Python's directory first on `PATH`, so hooks and the
foreground runtime use that environment. A shell-profile edit is unnecessary.
Installing both projections requires no client launch or account credentials.
Projections do not prove separate operating-system confinement for each child.

## Select a SABSA row algorithm

For a new governed SABSA engagement, tell `/sabsa` in Claude Code or
`$workflow-sabsa` in Codex which row mode to use. The workflow selects
`deterministic` by default. The foreground runtime and the Codex carrier
accept these options on `start`:

| Option | Input |
| --- | --- |
| `--sabsa-row-mode MODE` | Default for all rows. Choose `deterministic`, `llm-assisted` or `left-to-right`. |
| `--sabsa-row-modes FILE` | JSON object with layer numbers as string keys and mode names as values, for example `{"3":"llm-assisted"}`. |
| `--question-dependencies FILE` | JSON object keyed by layer number, then by dependent question. For example, `{"1":{"who":["what"]}}` makes L1 Who wait for What. |

Use keys `"1"` through `"6"` and exact lowercase question names. Additional
prerequisites are merged with the maintained rules. Invalid names, self
dependencies and cycles are rejected. The runtime captures the policy at launch,
and resume reuses it. The [SABSA delivery profile](../reference/sabsa-delivery-profile.md#row-scheduling)
explains how each algorithm evaluates dependencies.

The same row policy is available through both clients. The orchestrating
parent uses the start command for its transport and supplies the local task
file and engagement identifiers.

=== "Claude Code"

    ```sh
    "$JAI_RUNTIME_PYTHON" "$HOME/.ai/it-role-house/tools/governed_layered.py" \
      start --provider claude --engagement "$ENGAGEMENT_ID" \
      --work-item "$WORK_ITEM_ID" --task "$TASK_FILE" --sabsa-row-mode deterministic
    ```

    The Claude parent keeps the foreground runtime open and handles native
    collaboration and admission through that session.

=== "Codex CLI"

    ```sh
    "$JAI_RUNTIME_PYTHON" "$HOME/.ai/it-role-house/tools/governed_codex_carrier.py" \
      --codex "$CODEX_EXECUTABLE" start --engagement "$ENGAGEMENT_ID" \
      --work-item "$WORK_ITEM_ID" --task "$TASK_FILE" --sabsa-row-mode deterministic
    ```

    JAI starts the Codex App Server child process and handles dispatch and admission.

### Recover a blocked row

When the runtime reports `question_order_conflict`, retain the exact
`procedure` reference from the response as JSON. Pause the foreground carrier,
save the operator's instruction to switch that row to dependency order in a
local text file, and run:

```sh
"$JAI_RUNTIME_PYTHON" "$HOME/.ai/it-role-house/tools/governed_layered.py" \
  change-blocked-row-order --session "$SESSION_LOCATOR" \
  --procedure "$PROCEDURE_REF_FILE" --operator-instruction "$INSTRUCTION_FILE"
```

Use the complete reference object, including the engagement, scope, logical ID
and version ID. The runtime accepts the switch only for the reported blocked
layer procedure in the current scope. It records the instruction and switches
that procedure to deterministic dependency order with its mandatory
prerequisites intact. Resume the same engagement using its original carrier.

## Restart and recovery

The parent resumes current-format work using its original carrier and the
existing session locator.

=== "Claude Code"

    ```sh
    "$JAI_RUNTIME_PYTHON" "$HOME/.ai/it-role-house/tools/governed_layered.py" \
      resume --session "$SESSION_LOCATOR"
    ```

=== "Codex CLI"

    ```sh
    "$JAI_RUNTIME_PYTHON" "$HOME/.ai/it-role-house/tools/governed_codex_carrier.py" \
      --codex "$CODEX_EXECUTABLE" resume --session "$SESSION_LOCATOR"
    ```

    Use the absolute path of the Codex executable used at launch. The optional
    `--parallel N` goes before `start` or `resume` and accepts 1 through 6.

Reconcile the exact prepared intent or bound handle before continuing. Do not
repeat completed/uncertain work, reset local budgets, or replay the whole prefix
at every step. Initialization establishes the Store once; ordinary processing
keeps it warm. Continuation is separate from output acceptance and release.

For changed derived inputs, their owner records a new criterion and explicit
replacement effects. Obtain fresh affected verification; do not inherit an old
PASS. The installed independent audit explains the exact current basis.

For software recovery, stop writers and preserve the current data tail first.
Restore reviewed software/configuration or use the existing installer from the
known reviewed package. **Never restore an old journal over current decisions.**
If the restored reader does not support the data format or pinned enrollment,
retain the complete immutable archive and start a distinct engagement from
actual authorized inputs. No migration or acceptance continuity is assumed.
Missing/corrupt required CAS files fail explicitly; working paths are not substitutes.
