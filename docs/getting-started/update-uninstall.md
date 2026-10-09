# Update and uninstall

## Updating to a new release

Updating is performed by the same installer used for a fresh deployment. Start with a dry run:

```bash
./install.sh --dry-run
```

The installer is state-aware and hash-aware. It distinguishes:

- new package files;
- changed package-owned files that were not locally modified;
- unchanged package-owned files;
- obsolete package-owned files;
- locally modified managed files;
- pre-existing unowned collisions.

If conflicts exist, the update stops unless you pass `--force`.

## Forced update and backups

```bash
./install.sh --force
```

Before replacing or removing conflicting managed paths, the installer backs them up under:

```text
~/.ai/backups/<timestamp>/
```

## Installation state

The runtime records managed ownership in:

```text
~/.ai/it-role-house/install-state.json
```

This state is what allows safe updates and safe uninstalls.

## Model override strategy

Do not edit the packaged registry directly. Keep local model policy in:

```text
~/.config/ai-it-house/models.json
```

or point `AI_HOUSE_MODEL_CONFIG` to an organisation-managed file.

## Uninstalling

!!! important
    The uninstaller is intended to run from the extracted release package. It is **not** copied into the protected common runtime.

=== "Linux / macOS"

    ```bash
    ./uninstall.sh --dry-run
    ./uninstall.sh
    ```

=== "Windows"

    ```bat
    uninstall.cmd --dry-run
    uninstall.cmd
    ```

### Uninstaller options

| Option | Effect |
| --- | --- |
| `--dry-run` | Show what would be removed without making changes. |
| `--force` | Remove locally modified managed files after backup. |
| `--remove-key` | Also remove the Fabric authority key created by installation. |

### Default uninstall behaviour

- unchanged package-owned files are removed;
- user-created or untracked files are preserved;
- locally modified managed files are preserved unless `--force` is explicit;
- only recorded managed settings and hooks are removed.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../install/"><small>← Previous · Getting started</small><strong>Installation</strong></a>
  <a class="ai-next" href="../quick-start/"><small>Next · Getting started →</small><strong>20-minute quick start</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
