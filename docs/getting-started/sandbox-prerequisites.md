# Sandbox and environment prerequisites

Owner: JAI maintainers · Last reviewed: 2026-10-16 · Review by: 2027-01-16

Use this reference when JAI works in a system terminal but a Claude or Codex session cannot read its runtime, resolve a host or render a document. Installation, executable availability, filesystem permissions and network authorisation are separate requirements. A program can be installed and on `PATH` while its libraries, fonts or configuration remain unreadable inside the sandbox.

The provider selects authorised tools from your natural-language request. Markdown remains the default SABSA documentation format. Request LaTeX source, a compiled PDF or DOCX explicitly when you need that output; you do not need to install every publication dependency for ordinary Markdown work. See [installation](install.md), [publication stack](../configuration/publication-stack.md) and [troubleshooting](../operations/troubleshooting.md).

## Dependencies by task

| Task | Required local components | Additional access to consider |
| --- | --- | --- |
| Use installed JAI workflows and Markdown documentation | Python 3.10+, installed provider surface and JAI runtime | Installed skills, runtime Python files, schemas and the working project |
| Generate SABSA `.tex` source or DOCX | Pandoc | Pandoc executable and its installed resources; writable output and temporary files |
| Compile SABSA LaTeX to PDF | Pandoc, XeLaTeX, required TeX packages and DejaVu Serif | TeX trees, configuration, compiled formats and fonts |
| Inspect PDF pages as images or text | Poppler tools such as `pdftoppm` and `pdftotext` | Readable PDF and writable inspection output |
| Inspect rendered Office output | LibreOffice or a suitable Office application | Office libraries/resources, fonts, writable application profile and output |
| Run full release/development qualification | Dependencies required by the selected release gates | The complete controlled build environment, described in [deployment notes](deployment-notes.md) |

Pandoc generates DOCX without LibreOffice. LibreOffice is optional for Office rendering and applicable HTML visual QA; it is not a prerequisite for every JAI workflow. Installing dependencies is an administrator task. Local rendering with installed TeX packages and fonts does not require unrestricted internet access or downloading remote TeX content.

## Codex: choose one permissions system

The [official OpenAI permissions documentation](https://learn.chatgpt.com/docs/permissions) describes permission profiles as **beta**. The configuration guidance below was checked against that documentation on 2026-10-16. The workstation involved in this deployment reported `codex-cli 0.162.1`; that is a user-reported version, not an automatic compatibility check for other installations.

Use either `default_permissions` with `[permissions]`, or the older `sandbox_mode` with `[sandbox_workspace_write]`. Do not combine them and assume both take effect. The official documentation explains precedence, including loaded configuration layers, `--sandbox` and managed requirements. An administrator must check which system is effective in the actual session and follow the schema supported by the installed client.

This is an **illustrative offline profile**, not a complete policy to paste over an existing configuration:

```toml
default_permissions = "jai-local"

[permissions.jai-local]
extends = ":workspace"

[permissions.jai-local.filesystem]
":root" = "deny"
":minimal" = "read"
"~/.ai/it-role-house" = "read"
"~/.codex/skills" = "read"

[permissions.jai-local.network]
enabled = false
```

The inherited `:workspace` profile supplies workspace write access and protects paths such as `.git`, `.agents`, `.codex` and `.aws` within workspace roots. It also supplies write access to `:tmpdir` and `:slash_tmp`. If an administrator needs to exclude those temporary locations, the **profile's filesystem table** must explicitly deny them:

```toml
# Optional entries inside [permissions.jai-local.filesystem]:
":tmpdir" = "deny"
":slash_tmp" = "deny"
```

Those entries replace the profile's inherited temporary-directory access. The legacy options `sandbox_workspace_write.exclude_slash_tmp` and `exclude_tmpdir_env_var` belong to the older permissions system; adding them to this example is not an equivalent configuration.

The example's runtime read permissions cover loading installed code and schemas. They do not authorise installation, upgrades, migrations or every workflow that persists state under `~/.ai`. Identify the exact state/configuration/cache directory used by the requested workflow before an administrator grants scoped write access. Keep working artefacts and evidence in the authorised project where the workflow supports that destination.

## Add only the paths your installation uses

The following are Linux deployment examples, not universal installation paths. Package managers, distributions, provider packaging and macOS/Windows layouts differ. Grant read access to the actual dependency path when diagnostics show it is needed; do not grant write access to system trees for rendering.

| Dependency | Example readable paths | When relevant |
| --- | --- | --- |
| Codex installed through npm | `~/.local/npm/lib/node_modules/@openai/codex` | The selected executable/helper lives in that npm prefix |
| Codex app runtime | `~/.codex/packages/app-server-daemon/releases` | The active app uses a runtime beneath that installation tree |
| TeX Live | `/usr/share/texlive`, `/etc/texmf`, `/var/lib/texmf` | XeLaTeX needs packages, configuration or compiled formats there |
| Font configuration and fonts | `/etc/fonts`, `/usr/share/fonts` | The renderer must discover installed fonts |
| LibreOffice | `/usr/lib64/libreoffice` | A Fedora-style installation needs its libraries/resources for Office rendering |
| systemd-resolved | `/run/systemd/resolve` | A resolver configuration symlink on this host points there and DNS fails because it is unreadable |

For example, an administrator could add `"/usr/share/texlive" = "read"` to the selected filesystem table after confirming that location. Existing denials and managed requirements still apply. Do not copy another person's username, plugin configuration, installation prefix or provider release number into your own policy.

For a Linux workstation using the TeX paths above, the following is a **replacement for the illustrative profile's filesystem section**, not a second table to append verbatim. The sensitive-file entries are examples of exact workspace-relative paths: replace them with the real protected files, including files outside this example's list. Omit the TeX/font entries when that output is not needed.

```toml
[permissions.jai-local.filesystem]
":root" = "deny"
":minimal" = "read"
"~/.ai/it-role-house" = "read"
"~/.codex/skills" = "read"
"/usr/share/texlive" = "read"
"/etc/texmf" = "read"
"/var/lib/texmf" = "read"
"/etc/fonts" = "read"
"/usr/share/fonts" = "read"

[permissions.jai-local.filesystem.":workspace_roots"]
".env" = "deny"
"config/production.env" = "deny"
"keys/deployment-private.pem" = "deny"
```

Retain the original profile selection, `extends = ":workspace"` and offline network section. This supplementary section does not authorise access to Codex helpers, Office resources or resolver state unless those required paths are separately included. A file moved or added outside the exact protected paths needs a corresponding policy review.

### Temporary files

Python, Pandoc, TeX and Office applications can need temporary files even when the final output is a project file. If `/tmp` and the inherited temporary directory are denied, provide a writable temporary directory under the authorised workspace and set `TMPDIR` for the relevant process to that location. Keep it in a subtree that is not separately denied. On platforms supporting additional temporary-directory variables, follow the application's documented selection rules.

Check the effective location: Python can fall back to another candidate when the requested temporary directory is unusable. Do not assume setting `TMPDIR` alone proves that the selected directory is writable or used. Office applications can also need a separate writable user profile; keep a visual-QA profile separate from the user's interactive Office profile.

An authorised engineer can check a project-local temporary directory from the project root:

```sh
mkdir -p build/tmp
TMPDIR="$PWD/build/tmp" python3 -c 'import tempfile; print(tempfile.gettempdir())'
```

The printed path should be this project's `build/tmp`. This only checks Python's selection for that process; pass the chosen environment to the actual renderer as well. The directory must remain authorised by the effective filesystem policy. The snippet does not modify the provider's configuration.

### Network and DNS

Reading `/run/systemd/resolve` permits reading resolver state; it does **not** authorise a network connection. Conversely, allowing network access cannot repair an unreadable resolver configuration. The systemd path is relevant only on hosts that use it.

Offline authoring/rendering can keep `network.enabled = false`. When a task needs official documentation or another external source, the administrator can authorise the required hosts separately. In the current Codex profile system, domain rules are enforced only with an active network proxy, such as `features.network_proxy = true` or an administrator-managed proxy. **Network enabled with the proxy disabled gives direct unrestricted command network access; domain entries alone do not filter it.** Include required redirect hosts when reviewing a documentation allowlist: OpenAI documentation URLs may redirect to `learn.chatgpt.com`. See [official network permissions](https://learn.chatgpt.com/docs/permissions#network-permissions).

### Sensitive files, environment variables and protected Git metadata

Retain protection for actual sensitive files such as project `.env` files, private keys and credential stores. Broad filename patterns such as `*secret*`, `*token*` or `*credential*` can also match legitimate role documentation, schema names or runtime modules. If that happens, report the exact denied path to the policy owner. The administrator decides whether a more precise rule preserves the intended protection. The agent must not rename/copy files to evade a denial or silently weaken the policy.

Environment inheritance is a separate control. Review `shell_environment_policy` against the current [configuration reference](https://developers.openai.com/codex/config-reference). `inherit = "core"` can provide a narrower baseline than inheriting the entire parent environment, but an API workflow may still need explicitly authorised credentials. Allow only the variables needed for that workflow, without printing their values. Name-based exclusions involving `KEY`, `SECRET` or `TOKEN` can also remove noncredential variables needed by a tool; diagnose the missing variable name before changing policy. Do not copy provider API keys into a documentation example.

The workspace profile's protected `.git` directory can prevent creating branches or updating Git metadata even while ordinary project edits succeed. Treat that as an intentional protection, not a reason to relocate metadata or bypass the sandbox. Report the blocked operation and use the administrator-approved human action or supported approval path.

## Claude Code has a different configuration and boundary

Do not translate Codex TOML keys into Claude settings. Follow the current [Claude Code sandbox documentation](https://code.claude.com/docs/en/sandboxing) and its JSON settings schema. Depending on the installation, `sandbox.enabled`, filesystem read/write rules and network domain rules may be configured in user, project or managed settings. Relative paths depend on the location of the settings file; confirm that resolution before using `.` as an allow rule.

Claude's documented Bash sandbox covers shell commands and their child processes. Built-in file/web tools, hooks and MCP servers are outside that sandbox boundary. A sandbox `denyRead` does not itself deny the built-in Read tool, and `allowedDomains` does not constrain WebFetch. Configure the corresponding tool permission rules and managed controls as well; consult the official [permissions documentation](https://code.claude.com/docs/en/permissions). Do not solve an extra read-path requirement by excluding the whole renderer from the sandbox.

## Diagnose the failing boundary before changing policy

Ask the provider to identify the failing operation and preserve its exact error. The administrator or authorised engineer checks the following in order:

1. The executable is installed and discoverable in the environment used by the workflow.
2. Its required libraries, resources, fonts and configuration are readable in that same sandbox.
3. Output, temporary and application-profile locations are writable.
4. A network-dependent task has both authorised connectivity and functioning resolver access.
5. The active provider configuration, inherited rules and managed restrictions match the intended policy.

`Permission denied`, a missing font, an unavailable compiled TeX format and an absent executable have different remedies. A failed format lookup does not establish that XeLaTeX is uninstalled; compare the error with the actual package/configuration access. Stop and report an unexpected program/dependency failure instead of installing replacements, enabling broad network access or using another renderer without agreement. Provider configuration changes belong to the user or administrator; this guide does not change them automatically.

## Sources and validation status

- [OpenAI: permission profiles](https://learn.chatgpt.com/docs/permissions), including profile inheritance, legacy precedence, protected paths and network proxy behaviour.
- [OpenAI: configuration reference](https://developers.openai.com/codex/config-reference), including environment inheritance and legacy temporary-directory settings.
- [Claude Code: sandboxing](https://code.claude.com/docs/en/sandboxing) and [permissions](https://code.claude.com/docs/en/permissions).

The policy snippets are documentation examples reviewed against those sources, not a verified production policy for every client/version. JAI publication checks on the development workstation established that filesystem access to installed TeX/font assets and Office resources matters independently of executable availability. An administrator must validate the effective policy on the target host before rollout; keep any unexecuted host-specific procedure marked unverified.

## Implementation details

[Tool hooks, runtime controls and release gates](../configuration/hooks-gates-verification.md) describes the inspected implementation.
Hooks depend on host event delivery and do not replace sandbox or filesystem controls.
