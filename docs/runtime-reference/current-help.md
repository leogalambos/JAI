# Documentation and installed CLI help — {{ JAI_VERSION }}

## The maintained documentation source

**The `docs/` Markdown tree is the authoritative product manual.** `mkdocs.yml` defines navigation and presentation; GitHub Actions builds and deploys that material to Pages. No HTML content is stored in `.ai/runtime/` and no second site is maintained. The site's HTML is an ephemeral GitHub Actions build output, **not** an input or a runtime dependency.

The product also contains executable, provider-facing **command contracts** in `.ai/commands/*.md`, agent contracts in `.ai/agents/*.md`, and skill instructions in `.ai/skills/*/SKILL.md`. These files are runtime inputs and must stay with the product. Their operational behavior is documented through [the command reference](../reference/commands.md), [extended walkthroughs](../reference/command-walkthroughs.md), and [the technical CLI reference](../reference/runtime-tools-detailed.md). The installed `~/.ai/it-role-house/GUIDE.md` is generated from the [canonical Markdown CLI guide](../reference/installed-cli-guide.md), providing offline help independent of any HTML viewer.

| Task | Maintained source | Access path |
| --- | --- | --- |
| Concepts, installation, governance, examples | `docs/**/*.md` | MkDocs site or local source checkout |
| Execute `/guide` without a browser | `docs/reference/installed-cli-guide.md` | Generated `~/.ai/it-role-house/GUIDE.md` after installation |
| Execute Claude commands | `.ai/commands/*.md` | Provider-installed commands |
| Execute Codex workflows | `.ai/commands/*.md` and skill adapter | Provider-installed `workflow-*` skills |
| Check operational tool syntax | `.ai/runtime/tools/*.py` / `fabric/fabric.py` | Run each tool's `--help` or documented subcommand |
| Publish website | `docs/` + `mkdocs.yml` | `.github/workflows/pages.yml` |

## Installation, offline behavior and URL resolution

1. Install normally with `install.sh` or `install.cmd`; the installer installs runtime and provider command/skill contracts. It does not need to copy a website into the runtime.
2. `/guide` reads the installed `GUIDE.md`, including command syntax and the 20-minute demo. No static HTML pages are necessary to make `/guide` work.
3. When a complete manual is requested, use `docs/index.md` in a local source checkout or the project's configured GitHub Pages site. **Do not guess a website URL.** The `site_url` value may be set in `mkdocs.yml` when a verified public deployment URL exists.
4. If neither a source checkout nor a verified website is available, `/guide` provides its installed `GUIDE.md` content and explains that the full manual is not installed locally. This is a deliberate compact-runtime boundary, not a broken installation.

## Editorial contract: every example declares who acts

| Documentation audience | First show | Then explain | Explicitly distinguish |
| --- | --- | --- | --- |
| User guide / examples | Exact Claude `/command` and Codex `$workflow-command` or a copyable natural-language prompt. | Inputs, expected results, blockers, role/accountable owner, independent verification. | User decisions vs agent tool calls; a tool proposal vs an executed tool call. |
| Capabilities / governance | What the operator asks or sees in the provider conversation. | Typed contracts, layer boundaries, policy, logs, evidence and failure modes. | Advisory output vs verified/released output; agent recommendation vs L0 action. |
| Developer/runtime reference | Actual Python CLI syntax, schema/record locations and reproducibility. | Who calls the API, expected effects, error handling and validator boundaries. | Internal/CI commands are not extra ordinary-user steps; Codex L0 remains human-run. |
| Release documentation | How a reader assesses published package and qualification evidence. | CI/build commands, provenance and scope of qualification. | Fixture tests vs live-provider evidence; historical PASS vs current candidate. |

Author new workflow pages with this **operator → behind-the-scenes → evidence/authority** distinction. Maintained examples must not imply that Codex can run the protected L0 authorisation command. A generated Markdown `GUIDE.md` and provider command/skill contracts are separate *execution surfaces*, not competing documentation trees.

## Validation and synchronization

From the repository root:

```bash
python3 .ai/runtime/tools/docs_contract.py --root .
python3 .ai/runtime/tools/generate_docs.py --check --root .
python3 -m mkdocs build --strict
python3 .ai/runtime/scripts/check_agent_policy.py --fast .
```

`docs_contract.py` checks that the Markdown navigation includes every authored page, that Markdown, HTML navigation and local assets resolve, that every command has a documented entry, that operator-vs-runtime sections remain present in user scenarios/workflows, that no runtime HTML is bundled and that obsolete generated-help dependencies have not reappeared. `generate_docs.py` verifies that release numbers and inventories are derived from canonical runtime registries, not hand-maintained counts, and that the installed `GUIDE.md` exactly matches the maintained CLI-guide Markdown. A pull request must pass both checks. A Pages push additionally builds the site; the runtime itself has no HTML regeneration stage.

## Operational boundaries

- **Knowledge is not authority.** Markdown, `GUIDE.md`, and a rendered website cannot bypass an Agent Contract, sandbox, provider-specific permission boundary, policy approval or execution evidence requirement.
- **Treat examples as examples.** The extended walkthroughs originated with the original product and retain their explanatory value. Use current installed command contracts and `--help` as the source for supported options. For an irreversible operation, inspect the exact action and its authority gate first.
- **Release compatibility is not a documentation version.** Older schema identifiers such as `26.10.0` remain where they define real migration inputs or historical records. Current product instructions and the documentation site correspond to `VERSION` (**{{ JAI_VERSION }}**).
- **Distribution authenticity is separate.** Published releases include SHA-256, provenance and SBOM. Where GitHub artifact attestations are available, verify the attestation for the exact ZIP. A checksum alone does not authenticate the publisher; semantic evidence checks remain independent.

## Common diagnostics

| Symptom | Verification |
| --- | --- |
| `/guide` cannot find its manual | Check `~/.ai/it-role-house/GUIDE.md`, then reinstall from the complete package |
| A provider command is missing | Check the installed `.claude/commands` or `.codex/skills/workflow-*` surface; start a fresh provider session |
| Site navigation has a broken link | Run `docs_contract.py --root .`, then `mkdocs build --strict` |
| Published docs do not match the source | Check the deployment branch, workflow run and Pages URL; rerun source checks |
| Review seems to approve its own output | Check Agent/Policy Contracts and actual native provider tool permission settings, not a help file |

For demonstrations, consult the [concepts and tour](../using/concepts-and-tour.md), [command walkthroughs](../reference/command-walkthroughs.md) and [detailed runtime tools](../reference/runtime-tools-detailed.md). All their substantive content is Markdown under the same source-controlled documentation tree.
