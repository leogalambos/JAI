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

## Restart and recovery

The parent resumes current-format work through the actual installed CLI:

```sh
"$JAI_RUNTIME_PYTHON" "$HOME/.ai/it-role-house/tools/governed_layered.py" resume --session /private/engagement/example.session.json
```

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
