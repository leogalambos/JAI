# Installation

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

### Required

- Python **3.10 or newer**.
- `jsonschema>=4.26,<5` for packaged DCS and Artifact Contract validation.
  Install requirements.txt into a reviewed virtual environment using that
  environment's `python -m pip`, from the extracted package root.
  DCS schema checks fail closed
  if this dependency is absent; they are never silently skipped.
- A supported provider surface:
  - **Claude Code**, and/or
  - **Codex CLI / compatible OpenAI-oriented execution surface**.
- An extracted AI IT House {{ JAI_VERSION }} release package.

## Optional capabilities and additional setup

AI IT House is ready for normal use after installation of its core dependencies and a supported AI provider (Codex CLI or Claude Code).

**You do not need to generate security keys, configure an approval service, or install an Office renderer to start using JAI.**

Some advanced capabilities require additional tools or an action performed by a human operator.

### Additional tools

| Tool | When do you need it? | Installation requirement |
| --- | --- | --- |
| **WeasyPrint 70 + Pyphen 0.17.x** | Generate PDF documents directly from JAI-produced HTML | Optional; recommended for HTML/PDF publication |
| **LibreOffice** | Render actual Word, PowerPoint and Excel files for visual quality review | Optional; can run outside the AI sandbox |
| **Chromium** | Browser screenshots of approved local pages | Optional; use a disposable profile and the effective sandbox |
| **Poppler** | Convert PDF pages to images for visual inspection | Optional; required for applicable page-image QA |
| **Pandoc** | Produce supported SABSA DOCX and LaTeX outputs | Optional |
| **XeLaTeX and fonts** | Compile LaTeX documents to PDF | Optional |
| **OpenSSL** | Sign and verify human approval decisions using the local L0 workflow | Required only when using signed local L0 approval |

Task-specific validation also uses lxml for EA XSD conformance and Pillow for image QA. Repository release CI is not required for local installation.

#### A clean optional renderer environment

Use the same Python interpreter for installation, doctor and publication.
A system package can provide WeasyPrint 70 with an older Pyphen that still
imports deprecated `pkg_resources`. Checking WeasyPrint alone is insufficient.
JAI's optional requirements select Pyphen 0.17.x; doctor reports the detected
version without importing an older series. It requests setup rather than
claiming that an untested renderer is READY. No warning filters are applied.

From the extracted package root, a human operator may create a disposable
virtual environment (normal user, no sudo):

```sh
python3 -m venv build/render-venv
build/render-venv/bin/python -m pip install -r requirements.txt -r requirements-rendering.txt
build/render-venv/bin/python .ai/runtime/tools/operator_actions.py doctor
```

On Windows, use `build\render-venv\Scripts\python.exe` instead of
`build/render-venv/bin/python`. These commands install packages only into that
virtual environment, downloading from the configured Python package index.
The `build/` location is excluded from release packaging; do not place
custom virtual environments among maintained distribution resources.
Review the requirements first. They do not modify system Python or JAI's
installed files. Use this interpreter for subsequent Python render commands;
creating a venv does not switch an already running provider's interpreter.

Doctor should report actual HTML/PDF conversion READY and Pyphen 0.17.x.
This package-local command checks the selected candidate, not an older public
installation. After installing that candidate, the same venv Python can invoke
`~/.ai/it-role-house/tools/operator_actions.py doctor` instead.
If native libraries or fonts are absent, consult the Fedora examples in
[the publication dependency matrix](../configuration/publication-stack.md#dependencies-by-task).
Fedora package versions vary; installing `python3-weasyprint` alone is not a
promise that its transitive Python dependencies match the supported environment.
Do not downgrade setuptools or edit system site-packages to hide a warning.

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
