# Installation

## Reconfigure JAI after installing additional tools

Installation and updates automatically run bounded, offline optional-tool
discovery after the managed files have been installed. Missing optional tools
do not invalidate a successful core installation. `--dry-run` writes nothing
and does not run the post-install probes.

After installing, upgrading or removing a tool, run with the Python environment
you intend to use for JAI:

```sh
python3 ~/.ai/it-role-house/tools/operator_actions.py configure --refresh
python3 ~/.ai/it-role-house/tools/operator_actions.py configure --refresh --dry-run
```

Both commands produce JSON without writing preferences or readiness caches.
`configuration_changed: false` is expected: automatic defaults are resolved at
use time, so no configuration file is needed. Keep an earlier report yourself
if you need a before/after comparison: save output with `> capabilities.json`,
then use `configure --refresh --compare capabilities.json` on the next run.
The optional `changes` lists are observations only, never input to selection.
The `python` field identifies the actual
interpreter; packages installed into a different virtual environment are not
available to it. Run the same command with that environment's Python to switch.

For example, a compatible WeasyPrint environment can report
`html_pdf: READY: actual WeasyPrint PDF conversion verified`, while a discovered
browser reports `AVAILABLE` with functional/sandbox readiness `NOT_VERIFIED`.
Executable version discovery alone is never READY. An unsuccessful optional
probe reports UNAVAILABLE or an operator action, not an installation failure.

- **Add WeasyPrint:** install the optional renderer requirements in your chosen
  virtual environment, then use its Python for refresh and publication.
- **Add LibreOffice:** refresh discovers `libreoffice` or `soffice` on PATH.
  Actual Office conversion is checked when rendering the real document.
- **Add Chromium:** refresh discovers the browser version; a real screenshot
  still must succeed inside the role's native sandbox before it counts as A.
- **Sandbox denial:** a detected tool does not grant access. After an observed
  failure, request exact category C host execution, not formal L0 approval.
- **Remove/upgrade tools:** refresh reports current availability. HTML auto
  selection rechecks WeasyPrint compatibility and can select LibreOffice for
  HTML when WeasyPrint is missing or incompatible; it never substitutes HTML
  rendering for native Office QA. Explicit backend/executable arguments remain
  explicit; remove those arguments or select `auto` to restore automatic choice.

Discovery includes Poppler, Pandoc, supported LaTeX engines, OpenSSL, provider
CLIs, pytest and MkDocs. Tools are optional for their respective functions.
Each version probe has a ten-second budget. Installation prints the full
capability JSON, selected Python and PATH, probe commands, durations, return
codes, separate stdout/stderr (up to 8000 characters each) and timeout/error
reasons. Doctor includes the underlying HTML conversion exception. The outer
installer budget is 150 seconds so ten slow tool probes and the 35-second doctor budget fit.
Missing programs and programs whose version probe failed both remain
`UNAVAILABLE`; use `executable` and `reason` to distinguish them. Browser
lookup currently uses CLI names on PATH, not macOS application bundles.
Reports include local paths; review them before sharing. No full environment
dump is collected. Redirect installation output to a local file when preserving
an observation for later comparison.

No packages, keys, trust pins or provider settings are installed by refresh.
Release support remains defined solely by `RELEASE-SCOPE.json`. Discovery does
not authorize an agent, certify confinement or activate privileged mutations.

## Audience

This section is written for an engineer, architect or administrator who needs a predictable local installation of AI IT House {{ JAI_VERSION }}.

## Which interface is used at each stage?

| Stage | Person and location | Automatic/runtime responsibility |
| --- | --- | --- |
| Install or update | Administrator runs `install.sh` or `install.cmd` in a **system terminal**, once per relevant installation. | Installer copies shared runtime and renders Claude commands/Codex skills; it does not ask the user to hand-wire each Python tool. |
| Use the product | Operator opens a new Claude/Codex session and types `/demo` / `$workflow-demo`, a named skill, or a natural-language request. | Provider skill/agent selects and executes permitted internal tools; the user receives results and evidence. |
| Diagnose deployment | Developer/admin may run direct self-tests in a **system terminal**, or ask the provider to do so if permitted. | Self-tests verify their technical invariants; they do not approve domain decisions. |
| Authorise L0 | In either provider, the human reviews and signs the exact request outside the AI sandbox. Native tool approval is not Fabric L0. | Runtime verifies the Ed25519 receipt, protected public trust and matching state, or fails closed. |

See [the interaction guide](../using/interaction-model.md) for normal work and [human authority](../operations/human-authority.md) for the reserved exception.

## Prerequisites

### Installation: standard library only

The installer needs **Python 3.10 or newer and an extracted release package**.
No preinstalled Python packages, `pip`, virtual environment or activated shell
profile are required to run `install.sh`, `install.cmd` or the Python installer.
Installation never installs dependencies or changes the host Python environment.
This applies to macOS as well as Linux and Windows.

Before writing files, installation validates `RELEASE-SCOPE.json` against the
maintained release-scope schema using a narrow standard-library validator.
It supports exactly that schema's const/enum, closed-object, unique-array and
patterned-string vocabulary. Malformed schemas or unsupported schema keywords
fail closed; validation is never skipped when a package is unavailable.

### Runtime workflows: additional dependencies

A successful copy/install does **not** mean contract workflows are ready.
Before running installed Agent/Policy, DCS or Artifact Contract validation,
provide `jsonschema>=4.26,<5` in the Python interpreter used by those workflows.
These broader schemas still use the full JSON Schema validator and fail closed
if it is absent. Doctor/installer discovery reports the missing runtime package
explicitly while retaining successful installation status.

Use an existing suitable OS package or Python environment. If you choose `pip`,
install only the needed runtime package with that interpreter's
`python -m pip install 'jsonschema>=4.26,<5'`, following its package-management
policy. A user-owned venv is an option when system Python is externally managed;
it is not an installation prerequisite, and unrelated packages need not migrate.
`requirements.txt` additionally contains documentation/build dependencies and is
not necessary just to copy/install JAI. No package is installed automatically.

Normal workflow use also needs **Claude Code and/or a supported Codex CLI**.
Use the same intended workflow interpreter when running `configure --refresh`;
installer discovery preserves `-S` when installation was explicitly run with
site packages disabled, and identifies this mode in its diagnostics.

#### macOS: finish runtime setup when the validator is missing

Installation completion prints the following steps only when its selected
Python lacks a compatible runtime validator. They install the validator and its
dependencies, not your unrelated Python packages. From a terminal:

```sh
python3 -m venv "$HOME/.venvs/jai"
"$HOME/.venvs/jai/bin/python" -m pip install 'jsonschema>=4.26,<5'
"$HOME/.venvs/jai/bin/python" "$HOME/.ai/it-role-house/tools/operator_actions.py" configure --refresh
```

Then start a **new** session with the venv first on PATH; choose your provider:

```sh
PATH="$HOME/.venvs/jai/bin:$PATH" codex
PATH="$HOME/.venvs/jai/bin:$PATH" claude
```

The installed `python3` hooks and commands inherit that PATH. An already running
or GUI-launched provider may have a different environment; restart it with this
PATH before relying on those hooks. No `.bash_profile` edit is needed.
`JAI_PYTHON` selects the installer interpreter for that invocation only; it does
not persistently select the interpreter used by provider hooks. For a custom
installation destination, use the exact refresh path printed by the installer.
Linux and Windows need the same runtime dependency in their selected interpreter;
the installer gives a concise dependency notice rather than these macOS steps.

## Optional capabilities and additional setup

AI IT House is ready for normal use after installation of its core dependencies and a supported AI provider (Codex CLI or Claude Code).

**You do not need to generate security keys, configure an approval service, or install an Office renderer to start using JAI.**

Some advanced capabilities require additional tools or an action performed by a human operator.

### Additional tools

| Tool | When do you need it? | Installation requirement |
| --- | --- | --- |
| **WeasyPrint 70** | Generate PDF documents directly from JAI-produced HTML | Optional; recommended for HTML/PDF publication |
| **LibreOffice** | Render actual Word, PowerPoint and Excel files for visual quality review | Optional; can run outside the AI sandbox |
| **Chromium** | Browser screenshots of approved local pages | Optional; use a disposable profile and the effective sandbox |
| **Poppler** | Convert PDF pages to images for visual inspection | Optional; required for applicable page-image QA |
| **Pandoc** | Produce supported SABSA DOCX and LaTeX outputs | Optional |
| **XeLaTeX and fonts** | Compile LaTeX documents to PDF | Optional |
| **OpenSSL** | Sign and verify human approval decisions using the local L0 workflow | Required only when using signed local L0 approval |

Task-specific validation also uses lxml for EA XSD conformance and Pillow for image QA. Repository release CI is not required for local installation.

#### A clean optional renderer environment

Pyphen is a transitive WeasyPrint dependency for hyphenation, not a requirement
for installation or core workflows. A normal `pip install weasyprint` installs
Pyphen automatically as a dependency; no separate manual installation is normally
needed. An OS-provided package with working dependencies is acceptable. Doctor
reports the Pyphen version for diagnosis but does not reject a renderer merely
because that version differs from 0.17.x; actual HTML/PDF conversion determines
readiness. The current Python API backend requires WeasyPrint 70.
LibreOffice rendering does not need either Python package.

You may keep your existing Python for core work. A separate renderer interpreter
is an option when you need isolated packages, not an installation prerequisite.
On every platform, JAI first tries the WeasyPrint 70 CLI on PATH. This works
with the Fedora `weasyprint` CLI package (which depends on `python3-weasyprint`)
and macOS Homebrew `weasyprint`, even when the caller's Python cannot import
their packages. On Fedora, use `dnf install weasyprint` for the CLI; installing
only `python3-weasyprint` supplies the Python library and may not supply the CLI.
The CLI receives HTML through stdin, a fixed trusted stylesheet and deny-all
resource options (`--allowed-protocols ''`, `--no-http-redirects`,
`--fail-on-http-errors`). External CSS, custom font loading and entities are
also rejected before rendering. A fixed non-sensitive base URI ensures relative
resources resolve into URLs and are denied too, rather than silently skipped.
Its version probe has ten seconds and actual
conversion has twenty seconds.

If the CLI is absent, incompatible or cannot complete its version/startup probe,
JAI falls back to WeasyPrint 70 in the current Python interpreter. There is no
OS-specific interpreter discovery. Doctor uses the same selection and reports
the selected execution mode, CLI executable/version or Python version under
`renderer_dependencies.selected_renderer`. CLI-managed Python/Pyphen versions
are reported as unknown (`null`), rather than guessed from caller packages.
No venv or duplicate Python packages are needed for a working CLI.
Explicit LibreOffice bypasses WeasyPrint discovery. Automatic mode can use
LibreOffice if both WeasyPrint backends are unavailable. Resource denials,
conversion failures and conversion timeouts never trigger a weaker fallback.

The optional pip requirements select Pyphen 0.17.x to avoid an older Fedora
package's deprecated `pkg_resources` import. This clean-environment recipe is
an option, not a requirement to replace a working macOS package.

From the extracted package root, a human operator may create a disposable
virtual environment (normal user, no sudo):

```sh
python3 -m venv build/render-venv
build/render-venv/bin/python -m pip install -r requirements-rendering.txt "jsonschema>=4.26,<5"
build/render-venv/bin/python .ai/runtime/tools/operator_actions.py doctor
```

On Windows, use `build\render-venv\Scripts\python.exe` instead of
`build/render-venv/bin/python`. These commands install packages only into that
virtual environment, downloading from the configured Python package index.
The `build/` location is excluded from release packaging; do not place
custom virtual environments among maintained distribution resources.
The additional `jsonschema` package lets JAI validate runtime contracts in this
renderer environment. Installation and `configure --refresh` themselves do not
require it; doctor will report those runtime contracts as not ready without it. The documentation-building
packages in `requirements.txt` are not needed just to render HTML/PDF.
Review the requirements first. They do not modify system Python or JAI's
installed files. Use this interpreter for subsequent Python render commands;
creating a venv does not switch an already running provider's interpreter.

Doctor should report actual HTML/PDF conversion READY; Pyphen metadata is informational.
This package-local command checks the selected candidate, not an older public
installation. After installing that candidate, the same venv Python can invoke
`~/.ai/it-role-house/tools/operator_actions.py doctor` instead.
If native libraries or fonts are absent, consult the Fedora examples in
[the publication dependency matrix](../configuration/publication-stack.md#dependencies-by-task).
Fedora package versions vary; installing `python3-weasyprint` alone is not a
promise that its transitive Python dependencies match the supported environment.
Do not downgrade setuptools or edit system site-packages to hide a warning.

##### macOS and separate Python environments

If WeasyPrint is already installed through Homebrew and its CLI is on PATH,
JAI automatically uses it first, using the same selection as every other OS. No venv or
duplicate package installation is required. For a new optional HTML/PDF setup on
macOS, prefer the Homebrew package:

```sh
brew install weasyprint
python3 "$HOME/.ai/it-role-house/tools/operator_actions.py" configure --refresh
```

Homebrew supplies the formula's Python dependencies and native libraries.
If the CLI is unavailable but the current Python provides a working WeasyPrint
70 module, JAI uses that fallback and no additional setup is needed.

A separate pip environment is an **optional alternative if you do not choose
Homebrew**. Homebrew Python may refuse global `pip install` because it is
externally managed. In that case, create a user-owned renderer environment
from the extracted package root:

```sh
python3 -m venv "$HOME/.venvs/jai-render"
"$HOME/.venvs/jai-render/bin/python" -m pip install -r requirements-rendering.txt "jsonschema>=4.26,<5"
"$HOME/.venvs/jai-render/bin/python" "$HOME/.ai/it-role-house/tools/operator_actions.py" configure --refresh
```

WeasyPrint also requires native libraries such as Pango and usable fonts;
with Homebrew, install the host dependency using `brew install pango`. A venv
isolates Python packages; it does not supply native libraries or repair their
loader paths. Keep the reported conversion exception and doctor stderr if
conversion still fails.

A normal venv cannot see packages installed into the base Python. Install only
the packages required for the tasks you run inside it, including their transitive
dependencies. You do **not** need to copy all existing packages or move unrelated
tools into it. External programs such as LibreOffice, Pandoc and XeLaTeX remain
host programs discovered through the inherited PATH. `--system-site-packages`
can expose base Python packages, but weakens isolation and can reintroduce the
version conflicts this clean environment avoids.

No `activate` command or `.bash_profile` modification is required: explicit
interpreter paths work in any shell. If you choose to run installation with
this interpreter too, use `JAI_PYTHON="$HOME/.venvs/jai-render/bin/python" bash ./install.sh`.
This selects Python for that invocation only; it does not change the interpreter
used by an already running provider or by future bare `python3` commands.

WeasyPrint renders HTML/CSS, not DOCX/PPTX/XLSX. Actual Office visual QA
still needs an Office-compatible renderer and page images. It can use an
operator's separate host environment; see the
[complete rendering walkthrough](../operations/operator-walkthrough.md).

### Human approval (L0): When do I need security keys?

JAI supports a six-layer AI processing model (L1–L6). Some consequential decisions require an additional authority called **L0 — Human Authority**.

For example, an AI agent may prepare an architecture decision and recommend accepting a residual security risk. It may explain and document the recommendation, but it must not approve that decision on behalf of a human.

When formal L0 approval is required:

1. JAI prepares a request describing the exact decision and the state of the affected artefact.
2. The human operator reviews the request outside the AI sandbox.
3. The operator approves or declines the request using a separately protected signing key.
4. JAI verifies the returned signature and confirms that the approval applies to the current request and artefact state.
5. The workflow continues only if the required authorization has been verified.

#### What are the Ed25519 keys?

- **Private signing key:** used by the human operator to sign a decision. It must remain outside the AI agent's accessible files and must never be shared with the agent.
- **Public verification key:** allows JAI to verify the signature without accessing the private key. Its trusted configuration must also be protected against unauthorized changes.

These are **not API keys** for Codex, Claude, or an AI model provider.

The installer does not automatically generate these new L0 signing keys. You need to set them up only if you intend to use signed local human-approval workflows.

See [Human authority and escalation](../operations/human-authority.md) for key setup, approval, rejection, verification, troubleshooting and security limitations.

### Working with tools outside the AI sandbox

Codex and Claude may operate in restricted environments where some host operations are unavailable.

This is expected. JAI can request that a human perform a specific operation outside the AI sandbox without granting the AI broader permissions.

For example, when LibreOffice cannot execute inside the sandbox:

1. JAI prepares a rendering request identifying the exact source document.
2. The operator reviews and executes the requested conversion in a separate terminal.
3. The resulting document and execution evidence are provided to JAI.
4. JAI verifies the result and continues the publication workflow.

The same cooperation model can be used for approved software installation, Git maintenance and other host operations. These remain independent human actions, not an agent-operated privileged command service or automatic Fabric approval.

See [Operator workflows and security boundaries](../security/product-operations.md) for detailed procedures and limitations.

### Check which capabilities are available

On a supported Linux installation, run:

```bash
python3 ~/.ai/it-role-house/tools/operator_actions.py doctor
```

The diagnostic reports which supported capabilities are ready, which need an operator action, and which are unavailable or not verified.

A successful installation does not imply that all optional security or publication capabilities are configured. These can be enabled when needed.

### Security and deployment limitations

JAI relies on the effective sandbox and host permissions to restrict AI execution. Its role contracts and hooks provide additional controls but do not replace operating-system enforcement.

Autonomous privileged host and external-system mutations are not supported by this release. Optional host hardening may improve deployment security, but its effectiveness must be checked on the actual target environment.

For deployment details, see [Sandbox prerequisites](sandbox-prerequisites.md) and [Security boundaries](../security/product-operations.md).


## Before you install

Read the installation as a **rendering step** rather than a simple file copy. The package maintains provider-neutral canonical sources under the common runtime and then renders provider-facing surfaces for Claude and Codex.

## Step 1 — inspect the package safely

=== "Linux / macOS"

    ```bash
    ./install.sh --dry-run
    ```

=== "Windows"

    ```bat
    install.cmd --dry-run
    ```

A dry run validates the package, reads the effective model-routing source and reports what would change without writing any managed files.

## Step 2 — install

=== "Linux / macOS"

    ```bash
    ./install.sh
    ```

=== "Windows"

    ```bat
    install.cmd
    ```

By default, both provider surfaces are installed.

### Provider-specific installation

=== "Claude Code"

    ```bash
    ./install.sh --claude-only
    ```

=== "Codex CLI"

    ```bash
    ./install.sh --codex-only
    ```

## Installer options

| Option | Effect |
| --- | --- |
| `--dry-run` | Validate and show the file delta without writing. |
| `--force` | Back up and replace locally modified or colliding managed files. |
| `--claude-only` | Install/update only the Claude-facing surface plus common runtime. |
| `--codex-only` | Install/update only the Codex-facing surface plus common runtime. |
| `--no-claude-md` | Do not add/update the managed AI IT House block in `~/.claude/CLAUDE.md`. |
| `--no-codex-agents` | Do not add/update the managed AI IT House block in `~/.codex/AGENTS.md`. |
| `--no-hooks` | Do not install provider hook snippets. |
| `--model-config <file>` | Merge a JSON model-routing override into the package defaults. |

## Managed installation locations

```text
~/.ai/it-role-house/    common runtime, roles, workflows, schemas, tools and policies
~/.claude/              Claude-native agents, commands, skills and hooks
~/.codex/skills/        Codex-native skills and compatibility surfaces
```

The installer does not generate approval keys. Legacy Fabric HMAC records
remain readable for compatibility; their old key is not a credential for a
new formal L0 decision. Configure separate Ed25519 operator signing and
protected public trust only when needed, following
[human authority](../operations/human-authority.md).

## Step 3 — start a fresh provider session

Provider-facing assets are discovered at session start. After installation, open a **new** Claude or Codex session.

## Step 4 — verify the installation

=== "Claude Code"

    ```text
    /demo check
    ```

=== "Codex CLI"

    ```text
    $workflow-demo check
    ```

**Optional administrator/developer diagnostics** (these are **not** required after every successful provider command):

```bash
python3 ~/.ai/it-role-house/demo/demo.py check
python3 ~/.ai/it-role-house/tools/model_router.py self-test
python3 ~/.ai/it-role-house/tools/provider_parity.py
```

## What a successful installation should give you

A successful installation should make these capabilities available immediately:

- role-aware advisory work;
- workflow commands such as `/analyse`, `/review`, `/diagnose`, `/sabsa`, `/publish`, `/layered`;
- demo estate setup;
- managed publication and Fabric tooling;
- stable local paths for the common runtime and provider surfaces.

For complete host-side procedures, see the [exact operator walkthrough](../operations/operator-walkthrough.md).

## Local QA and human intervention

Use A / AUTO for role-authorized local work inside the actual sandbox. B is
an observed native permission request; C is an exact operator host task. Neither
is Fabric L0. D is a separately signed consequential decision; it may precede C.
Every B/C/D request must include the complete action and reason inline before
linking details. See [execution routes and boundaries](../security/product-operations.md)
and the [full operator guide](../operations/operator-walkthrough.md).
