# Commands and direct tools

The **Claude** column is typed in the Claude Code conversation. The **Codex** column is typed in the Codex CLI conversation; `$workflow-name` denotes a *skill*, not a Unix command. Supply arguments or follow-up context in that conversation, then allow the provider to dispatch permitted tools. Nothing in the table tells a normal user to run `python3` manually.

## Workflow commands

| Claude | Codex equivalent | Purpose |
| --- | --- | --- |
| `/guide` | `$workflow-guide` | Open guidance and command help. |
| `/demo` | `$workflow-demo` | Set up, inspect or reset demonstration workspaces. |
| `/analyse` | `$workflow-analyse` | Understand a repository, document set or architecture input before judging it. |
| `/criteria` | `$workflow-criteria` | Establish review criteria before inspection. |
| `/review` | `$workflow-review` | Conduct an independent review and record findings. |
| `/rework` | `$workflow-rework` | Resolve recorded findings under the right separation of duties. |
| `/diagnose` | `$workflow-diagnose` | Root-cause analysis before remediation. |
| `/develop` | `$workflow-develop` | Controlled implementation or document change work. |
| `/govern` | `$workflow-govern` | Repository or content governance analysis. |
| `/research` | `$workflow-research` | Research to a decision with disciplined evidence handling. |
| `/sabsa` | `$workflow-sabsa` | SABSA library lifecycle. |
| `/publish` | `$workflow-publish` | Render reviewed semantics into enterprise deliverables. |
| `/repository` | `$workflow-repository` | Scoped EA-domain projection repository operations and Open Exchange interoperability. |
| `/layered` | `$workflow-layered` | Consequential JAI L1–L6 flow with typed contracts, bottom-up review, bounded rework/reformulation and L0 escalation. |
| `/fabric-report` | `$workflow-fabric-report` | Independent audit/report view over a Fabric record. |

## Direct tools

The provider workflows are instruction/adaptation surfaces that **may invoke** direct tools under the common runtime. These tools are implementation interfaces for the agent, CI, or developer troubleshooting—not a second end-user procedure. Their availability alone does not prove that a particular run executed them: inspect tool results and evidence. See [the developer reference](../reference/runtime-tools-detailed.md), [interaction patterns](interaction-model.md) and [human authority](../operations/human-authority.md).

- `tools/model_router.py`
- `tools/provider_parity.py`
- `tools/criteria.py`
- `tools/findings.py`
- `tools/publication.py`
- `tools/repository.py`
- `tools/sabsa.py`
- `tools/execution_record.py`
- `tools/native_enforcement_26104.py`
- `fabric/fabric.py`
- `demo/demo.py`
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../layered-engagement/"><small>← Previous · Using the system</small><strong>Running a layered justifiable engagement</strong></a>
  <a class="ai-next" href="../roles/"><small>Next · Using the system →</small><strong>Roles and disciplines</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
