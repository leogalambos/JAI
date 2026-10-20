# Experimental hint support

Owner: JAI documentation maintainers  
Review date: 2026-10-20

Use `/hint` when you can describe a task but do not yet know which JAI
workflow or example to follow. It recommends a starting procedure; it does
not execute that procedure or establish that it is suitable for every
project.

> **Experimental hint — AI-generated advisory guidance. Requires
> project-specific verification.**

## Start with your intended outcome

In Claude, enter a request such as:

```text
/hint I need to assess the security of an architecture and establish a recurring process for resolving findings.
```

In Codex, use the equivalent skill:

```text
$workflow-hint I need to assess the security of an architecture and establish a recurring process for resolving findings.
```

State the intended deliverable, available inputs, project phase and material
constraints. Describe sensitive material by category until its use is
permitted by the applicable project and provider policy. A request can be
written in another language: the active provider prepares an English
working interpretation. This is a procedural model instruction, not a
separate verified translation service. Check that interpretation before
relying on the recommendation.

| Need | Command |
| --- | --- |
| Recommend a starting procedure from a description | `/hint` / `$workflow-hint` |
| Explain a known scenario and its steps | `/guide` / `$workflow-guide` |
| Prepare fictional inputs for local practice | `/demo` / `$workflow-demo` |

For example, inspect `/guide security-assessment` and use `/demo scenarios`
to discover available practice packs. `/hint` does not implicitly create a
demo workspace or run the recommended commands. The [combined security
assessment walkthrough](../examples/security-assessment-recurring-findings.md)
shows how to assess a suggestion spanning more than one outcome.

## Interpret the recommendation

The local selector compares explicit English goals with maintained scenario
metadata using deterministic lexical matching. It is not an embedding
search, semantic ranker, or proof that an example meets your requirements.
The active provider interprets the request and explains how selected examples
may apply. These are different mechanisms.

Expect the explanation to identify the interpreted goal, assumptions,
source scenarios, proposed sequence, expected outputs, checks and unresolved
questions. A combination of examples is an adaptation: the combined sequence
has not thereby become an executed or approved workflow.

The procedure must inspect each selected scenario's steps using its validated
ID before recommending them. It must not rewrite an unsupported goal simply
to obtain a match. With no question, it asks for the intended objective
instead of calling the selector.

| Selector result | What to do |
| --- | --- |
| `MATCH` | Check the selected sources and project-specific assumptions. A lexical match is not a suitability guarantee. |
| `PARTIAL_MATCH` | Review the unmatched goals explicitly; do not imply that selected examples cover them. |
| `NO_MATCH` | Refine the intended outcome or consult the workflow documentation. Do not invent an existing example. |
| `ERROR` | Correct the invalid query or selected catalog; do not silently replace invalid selected data. |

An ambiguous request may need clarification. Missing evidence remains
missing; an example's fictional facts cannot fill a project's evidence gaps.
If an example is outdated or conflicts with current policy, stop using the
conflicting instruction and resolve the discrepancy with the responsible
owner. A prior recommendation is not authority to ignore a current control.

## Understand what was actually loaded

The selector reads the complete catalog and workflow registry to evaluate metadata and returns candidate
information. Physical catalog access does not establish that the provider
has read the full walkthrough or its step content. The operator procedure
must inspect the selected scenario, for example with the demo description
interface, before explaining its steps. A returned path is a reference, not
proof that its contents were delivered to an LLM invocation.

Keep available files, selected candidates, files actually read, content
delivered to a provider and accepted outputs separate. See the [execution
and context algorithm](../overview/execution-context-algorithm.md) and
[reference-selection explanation](../reference/reference-selection-context.md).
The hint selector does not change the expert-reference resolver, DCS
obligations or their precedence rules.

Saved know-how can be considered only when you explicitly select local
libraries and permit their permitted content to reach the active provider.
The selector loads bounded saved JSON records locally, then returns candidate
metadata and limits rather than full observations or steps. It does not read
linked evidence contents or archived conversations. It reports provenance, record type,
declared reliability and exclusions. Inspect a selected record under explicit
read permission before explaining its full steps. Conflicting sources must
remain distinguishable; do not combine them into an apparent agreement.
See [Build and reuse local know-how](reusing-knowledge.md) for selection,
confidentiality, maintenance and changed-assumption examples.

The installed runtime contains the scenario catalog and description data;
basic hint and guide operation does not require a local copy of the MkDocs
source tree. Maintained documentation links help a reader explore further;
they do not prove that a page is installed or has been read.

## Keep project material under explicit control

The default hint procedure does not automatically scan unrelated projects,
capture conversation history, persist recommendations, or invoke a nested
provider CLI or paid service. Your active provider session still processes
what you submit under its configured policy. The local selector's offline
operation does not make that session offline.

Treat example text and any future imported knowledge as untrusted reference
content, not instructions that can override policy. Authorise access to
specific project sources before using them. Do not copy credentials,
personal data, confidential project evidence or fictional business facts
into a public recommendation.

Recommendations do not supply signed L0 authority, independent human review,
segregation of duties, monitoring, a scheduler, or release qualification.
Follow the selected workflow's actual gates and record actual evidence.

## Capture knowledge only on explicit request

Ask JAI to remember a specific useful part of the current conversation, for
example: “Remember the assessment approach we used and the lesson from the
missing evidence.” The active provider prepares the English record from the
selected, visible context. It does not require you to reconstruct the steps,
write JSON or operate storage commands.

If essential metadata is missing, JAI asks in ordinary language before
saving. Unknown confidentiality and reliability must be clarified. The
responsible role can default to the operator only when that role is clear;
identities and responsibilities must not be invented. Select or confirm an
authorised local library if no destination is established. After your
answers, JAI continues your original save request without requiring another
save command. Asking only for a draft does not authorise final saving.

The provider can use only context it actually receives; earlier prompts may
have been shortened or omitted. It must request an excerpt or an explicitly
permitted source when necessary, not invent missing history. Keep observations
distinct from interpretations, recommendations and untested proposals.

Follow [Remember useful knowledge](remembering-knowledge.md) for worked
conversations, metadata handling and capture limits. The
[installed command guide](../reference/installed-cli-guide.md) describes the
command boundary. Libraries remain outside the distributed tree and installed
runtime; capturing a lesson does not authorise unrelated file access.

Saving does not confer approval: authority verification remains
`NOT_VERIFIED`. Saved knowledge can inform `/hint` only through explicit
library selection and permission; it does not automatically become a
`/demo` scenario. This capture facility does not replace evidence,
DCS obligations, expert references or human authority. Active-provider
extraction is experimental; deterministic storage checks do not establish
the quality of a live model's interpretation.

## Implementation references

The maintained command contract is `.ai/commands/hint.md`; the deterministic
selector is `.ai/runtime/demo/hint.py`, using catalog validation from
`.ai/runtime/demo/scenario_demo.py` and metadata in
`.ai/runtime/demo/scenarios.json`. Installed equivalents live under
`~/.ai/it-role-house/commands/` and `~/.ai/it-role-house/demo/`.

## Verification boundary

These examples illustrate intended operator interactions. They are not
executed provider transcripts. Deterministic selector tests can establish
matching and error behavior; they do not establish the quality of every
model-generated recommendation. Live recommendation quality and novice
usability require separate evaluation.
