# Expert reference documents

Owner: JAI maintainers · Last reviewed: 2026-10-20

JAI includes 96 complete English Markdown examples: three complexity levels
for each of 32 document families. They work immediately after installation;
customer documents and provider accounts are optional.

The library covers decisions, architecture, requirements, strategy, policy,
implementation, migration, testing, operations, assurance and proposals.
Ten proposal families provide 30 examples for executive, technical, delivery,
commercial, contractual, RFP and optional security-service components.
The installed `list` command reports the complete family inventory.
Each family has `simple`, `medium` and `complex` examples.
Select complexity for the number of dependencies, alternatives and risks,
rather than a target document length.

## What the examples mean

The examples are **AI-authored proposed professional examples** in fictional
contexts. They are neither human-approved standards nor customer evidence.
Illustrative costs, approvals, test results and evidence references describe
the fictional case; they do not establish facts about your project or prove
that a command or test was actually executed.

Use an example to understand information depth, reasoning and useful
presentation. Establish project facts separately, resolve the registered DCS
contract and retain independent review and existing JAI human authority.
Replacing a reference never changes DCS MUST, MAY or MUST NOT obligations.

The complete library replaces the earlier bundled collection. Existing
reference IDs remain stable; revised supplied documents have new integrity
hashes. Updates do not overwrite separately stored user overrides.
See [proposal production](proposal-production.md) for coherent packages and
[colleague evaluation](../validation/proposal-pilot.md) for the pilot rubric.

## Inspect the installed library

From the source checkout:

```bash
python3 .ai/runtime/tools/expert_references.py list --root .
python3 .ai/runtime/tools/expert_references.py validate --root . --all
python3 .ai/runtime/tools/expert_references.py resolve --root . \
  --kind decision-paper --complexity medium
```

In an installation, substitute the actual runtime directory for
`.ai/runtime` and pass that directory as `--root`. Both providers use the
same resolver, registry and validation rules.

The resolver works with bundled defaults alone. [Overrides](../configuration/expert-document-overrides.md)
can replace one slot without changing other references. The
[format reference](../reference/expert-reference-format.md) explains metadata
and stable DCS anchors; [offline qualification](../validation/offline-content-qualification.md)
explains what the automatic checks establish.

## Use a reference during authoring

For a supported family, the shared outline command resolves the active
reference and records sanitized selection status. Select complexity and
optional roots explicitly:

```bash
python3 .ai/runtime/tools/content_spec.py outline --root . \
  --artifact-id enterprise-applications-architect:2 --reference-complexity medium
```

Use an actual registered role contract for your requested output. The CLI
also accepts `--user-root`, `--organisation-root` and `--engagement-root`.
References are untrusted authoring data: neither their prose nor embedded
instructions can replace policy, project evidence or JAI approval. An invalid
selected override stops outline creation. Families without a bundled expert
slot report that the reference is not applicable.
