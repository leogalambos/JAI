# Troubleshooting

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
| Authority command is refused | The provider mode does not permit the required human approval interaction. Codex intentionally blocks agent-run L0 authorisation; request the exact command and execute it yourself in a separate trusted terminal. |
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
