# Troubleshooting

## Tools installed later or missing after an upgrade

Run `python3 ~/.ai/it-role-house/tools/operator_actions.py configure --refresh`.
Check the reported `python` and PATH-resolved executables before reinstalling
anything. For virtual environments, invoke that environment's Python explicitly.
No stale discovery cache needs deleting. AVAILABLE means version discovery,
not verified rendering or sandbox access. See the
[refresh examples](../getting-started/install.md#reconfigure-jai-after-installing-additional-tools).

## Experimental hint recommendations

See [the hint guide](../using/experimental-hint.md) for the recommendation
boundary. For `PARTIAL_MATCH`, inspect unmatched goals and keep them explicit;
for `NO_MATCH`, clarify the objective without inventing an available example.
For `ERROR`, correct the invalid query or catalog before continuing: do not
silently fall back to other data. Ambiguous advice needs clarification, and
outdated advice needs checking against current project requirements and policy.

If `/hint` or `$workflow-hint` is not recognised, update the installation and
start a new provider session. A successful offline selector check does not
verify the active model's English interpretation or the suitability of its
recommended procedure.

**For a normal user:** first ask Claude or Codex to diagnose the failure and show which tool/agent/gate failed, without granting extra permissions or manually editing `.fabric/` or `.findings/`. Use `/fabric-report` (Claude) or `$workflow-fabric-report` (Codex) to inspect assurance evidence. **For a maintainer:** the table and self-test commands below show what can be checked in a system terminal. A self-test PASS is not approval to release.

| Symptom | Likely cause or action |
| --- | --- |
| Workflow command is not recognised | Start a new provider session after installation or update. |
| `mkdocs` landing page shows twice the footer | Remove any manually embedded copyright strip and rely on the theme footer only. |
| Mermaid diagrams show as code blocks | Ensure `pymdownx.superfences` uses `fence_div_format` and Mermaid JS is loaded. |
| Update stops on conflict | Inspect the managed-file conflict and use `--force` only after review. |
| PDF publication fails | Identify the route: SABSA LaTeX PDF needs Pandoc, XeLaTeX, TeX packages and fonts; Office conversion needs its Office renderer. Check resource access and writable temporary/output paths in the provider sandbox; see [sandbox prerequisites](../getting-started/sandbox-prerequisites.md). |
| SABSA DOCX asks for Pandoc | Install Pandoc or use an alternate publication route. |
| Installed tool works in a terminal but fails in the provider | Check the active filesystem policy and readable dependency trees before reinstalling; see [dependency paths](../getting-started/sandbox-prerequisites.md#add-only-the-paths-your-installation-uses). |
| DNS fails despite network authorisation | Check resolver configuration access separately from network permission; systemd-resolved paths apply only to hosts using that resolver. See [network and DNS](../getting-started/sandbox-prerequisites.md#network-and-dns). |
| Temporary-file or Office profile creation fails | Verify the selected writable directory and application profile; see [temporary files](../getting-started/sandbox-prerequisites.md#temporary-files). |
| Branch creation fails while project edits work | Protected Git metadata may be read-only by policy. Report the operation and use the approved human/administrator path; do not bypass the protection. |
| Authority command is refused | Prepare an exact request, then have the external operator sign or decline with the reviewed host helper. Fabric requires a valid Ed25519 receipt, protected public pin and unchanged snapshot. Native approval is not L0. |
| `.fabric/` looks inconsistent | Do not edit it manually; request an audit report in the CLI; a maintainer can run `fabric.py verify` and `report`. |
| You want to undo the installation | Use `uninstall.sh` / `uninstall.cmd` from an extracted release package. |

## Useful direct diagnostics — maintainer/CI only

These commands are implementation checks, not the ordinary user interaction. Run from an environment with the correct installed runtime and permissions; retain failed output and return it to the provider if needed.

```bash
python3 ~/.ai/it-role-house/tools/model_router.py self-test
python3 ~/.ai/it-role-house/tools/provider_parity.py
python3 ~/.ai/it-role-house/tools/publication.py self-test
python3 ~/.ai/it-role-house/tools/repository.py self-test
python3 ~/.ai/it-role-house/fabric/fabric.py selftest
```

## Local QA and human intervention

Use A / AUTO for role-authorized local work inside the actual sandbox. B is
an observed native permission request; C is an exact operator host task. Neither
is Fabric L0. D is a separately signed consequential decision; it may precede C.
Every B/C/D request must include the complete action and reason inline before
linking details. See [execution routes and boundaries](../security/product-operations.md)
and the [full operator guide](../operations/operator-walkthrough.md).

The installer prints the full capability observation, including the interpreter,
PATH and probe failures. Keep both stdout and stderr when reproducing an install
problem. A detected executable can still report `UNAVAILABLE` if its version
probe exits nonzero or exceeds ten seconds; this is distinct from a missing
executable. `doctor_probe` retains subprocess diagnostics and
`html_pdf_diagnostic` retains a failed conversion's exception type/message.
Output streams are limited to 8000 characters each. Reports contain local paths;
review them before sharing. See the [macOS renderer environment guidance](../getting-started/install.md#macos-and-separate-python-environments)
for optional WeasyPrint/Pyphen setup without global shell activation.

Check `renderer_dependencies.selected_renderer` for the actual execution mode
and CLI executable/version or Python used by doctor. Every OS tries the CLI on
PATH first, then the current Python module if its CLI version/startup probe is
unavailable or incompatible. CLI-managed Python/Pyphen metadata is unknown;
caller metadata does not describe the CLI environment. Version probes have ten
seconds and CLI conversion has twenty seconds. Resource denials and conversion
failures remain diagnostic and never trigger a weaker fallback. No packages are
installed and OS-specific Python discovery is not required.
