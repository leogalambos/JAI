# Installation

## Audience

This section is written for an engineer, architect or administrator who needs a predictable local installation of AI IT House {{ JAI_VERSION }}.

## Which interface is used at each stage?

| Stage | Person and location | Automatic/runtime responsibility |
| --- | --- | --- |
| Install or update | Administrator runs `install.sh` or `install.cmd` in a **system terminal**, once per relevant installation. | Installer copies shared runtime and renders Claude commands/Codex skills; it does not ask the user to hand-wire each Python tool. |
| Use the product | Operator opens a new Claude/Codex session and types `/demo` / `$workflow-demo`, a named skill, or a natural-language request. | Provider skill/agent selects and executes permitted internal tools; the user receives results and evidence. |
| Diagnose deployment | Developer/admin may run direct self-tests in a **system terminal**, or ask the provider to do so if permitted. | Self-tests verify their technical invariants; they do not approve domain decisions. |
| Authorise L0 | A human decides; Claude may present a trusted interactive gate, but **Codex requires a separate human-run authority command**. | Runtime records the authenticated event or fails closed. |

See [the interaction guide](../using/interaction-model.md) for normal work and [human authority](../operations/human-authority.md) for the reserved exception.

## Prerequisites

### Required

- Python **3.10 or newer**.
- A supported provider surface:
  - **Claude Code**, and/or
  - **Codex CLI / compatible OpenAI-oriented execution surface**.
- An extracted AI IT House {{ JAI_VERSION }} release package.

### Optional but relevant

These dependencies are selected by the task. See [sandbox and environment prerequisites](sandbox-prerequisites.md) when an installed tool fails inside a provider session.

| Component | Minimum / status | Used for |
| --- | --- | --- |
| Pandoc | Optional, detected at runtime | SABSA DOCX and LaTeX source generation |
| XeLaTeX, TeX packages and DejaVu Serif | Optional | Compile SABSA LaTeX to PDF |
| Poppler | Optional | Inspect PDF pages as images/text during visual QA |
| LibreOffice / compatible Office application | Optional for applicable visual QA | Render Office output; Pandoc DOCX generation does not require it |
| lxml | 5.x | EA XSD conformance suite |
| jsonschema | 4.x | Draft 2020-12 semantic schemas |
| Pillow | Runtime-supported | Visual QA fixture rendering |
| GitHub Actions | Tag-triggered release workflow | Repository production publication; not required for local installation |

Full release/development qualification still needs the dependencies of its required gates. Ordinary Markdown authoring does not require the Office or TeX stack.

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

```bash
./install.sh --claude-only
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

The installation can also create and preserve the local Justifiable Fabric authority key:

```text
~/.config/justifiable-fabric/authority.key
```

## Step 3 — start a fresh provider session

Provider-facing assets are discovered at session start. After installation, open a **new** Claude or Codex session.

## Step 4 — verify the installation

Claude:

```text
/demo check
```

Codex:

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
