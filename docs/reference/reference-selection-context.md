# Reference selection and context delivery

Owner: JAI maintainers · Last reviewed: 2026-10-20

This page describes the inspected JAI 26.10.12 implementation. Use the
[execution
overview](../overview/execution-context-algorithm.md#reading-implementation-status)
for status labels. The bundled v2.3.0 library has 135 Markdown
references across 45 families and three complexity levels. Catalog
discovery, local file validation and LLM context delivery are separate
operations.

## From deliverable to selected reference

**IMPLEMENTED:** the path uses these maintained components:

| Component | Selection behavior |
| --- | --- |
| Artifact Contract v3 and the registry's `binding_map_ref` | Stable role-contract identifiers bind to registered DCS document kinds through `content/migrations/26.10.5-binding-map.json`. |
| `content_spec.py:ContentSpec.resolve()` | Resolves an exact artifact binding or an explicit registered `kind/` selection. Standalone kinds do not grant role authority. |
| `ContentSpec.compile()` | Combines registered inheritance, overlays and typed context applicability; returns a blueprint and compiled hash. |
| `content/expert-reference-bindings.json` | Maps reference families and source anchors to actual registered kinds and units; supplies explicit authoring defaults for ambiguous role mappings. |
| `ExpertReferences.canonical_family()` | Resolves the explicit family, canonical kind or applicable role-contract mapping; rejects unsupported or unresolved ambiguous selection. |
| `ExpertReferences.resolve()` | Selects one applicable file at the highest applicable configured scope and validates it. |

Paths beginning with `content/` in this table are relative to
`.ai/runtime/`. Both Python tools live in `.ai/runtime/tools/`.
`ContentSpec.outline()` connects the compiled DCS and reference
resolver; it returns null semantic fields, a blueprint and sanitized
reference metadata. It discards the resolver's private path and does not
return the reference body or dispatch a provider call.

The library manifest is `content/expert_references/index.json`. It
records identity, kind, complexity, language, provenance, revision,
size, whole-file SHA-256 and stable anchors. It is neither an embedding
index nor an executable context loader. Existing proposed source
namespaces have actual registry mappings; mapping does not promote an
example to an approved standard or change normative MUST/MUST NOT
obligations.

## Applicability and precedence

**IMPLEMENTED:** selection uses exact family/kind mappings and the
requested `simple`, `medium` or `complex` slot. Authoring instructions
default to `medium`; the resolver itself requires an explicit
complexity. `_applicable()` checks valid front matter, slot/DCS
identity, optional `applicability_context` and optional
`target_audiences`. Context constraints require matching JSON value
types and values. An audience-constrained candidate requires the
explicit audience to belong to its declared list. Unconstrained files
need no semantic audience inference.

The resolver searches these scopes in order:

1. Explicitly authorized engagement root.
2. Organisation root, explicit or `JAI_EXPERT_REFERENCES_DIR`.
3. User root, explicit or under `XDG_CONFIG_HOME` / the user config home.
4. Bundled library.

A missing or valid but inapplicable higher-scope candidate can fall
through. A malformed selected candidate fails explicitly; it must not
silently fall back. Multiple applicable candidates at the same scope are
a conflict, not a ranking opportunity. `_candidates()` considers the
canonical slot filename and other Markdown files with readable matching
slot metadata; unreadable unrelated alternate files are not
automatically selected.

There is no implemented semantic similarity ranker, keyword search,
embedding retrieval or inferred complexity score in this resolver.
Language is validated as metadata for these English references, not used
by a multilingual ranking engine. Source access still depends on the
authorized caller and host permissions; a valid path is not
authorization to export project material.

Read-only selection inspection from the repository root:

```bash
python3 .ai/runtime/tools/expert_references.py inspect --root . \
  --kind threat-model --complexity medium
```

This prints a sanitized validation/selection report, not the Markdown
body. See [reference usage](../using/expert-reference-documents.md) and
[override configuration](../configuration/expert-document-overrides.md)
for established selection and installation procedures.

## Whole-file reading versus section validation

**IMPLEMENTED:** `expert_references.py:_read()` reads the entire
selected file as bytes. Validation checks front matter, DCS mappings and
anchored nonempty bodies; bundled validation additionally checks the
manifest's whole-file digest and metadata. Unsafe or symlinked paths are
rejected. `_visible_lines()` excludes code/comment material from
structural coverage. `_structure()` identifies anchor/heading boundaries
to check content presence, duplicate/missing anchors and dangling DCS
links. Its sections result records presence booleans, not provider-ready
excerpts.

**NOT IMPLEMENTED:** DCS-anchor-based section retrieval for LLM context
in the shared resolver/outline path. Structural boundary parsing does
not establish a retrieval API, chunk offsets, excerpt selection, token
ranking or preservation of excerpt-level disclaimers. Selecting one
whole file is not selecting only its task-relevant paragraphs.

**PROPOSED:** if section retrieval is later requested, it needs a
separate design and tests for exact anchor identity, nested headings,
code fences, disclaimer retention, cross-references, provenance and
budget failures. That recommendation adds no runtime feature or new
normative contract.

## Which path actually supplies content?

| Path | What the inspected implementation does | Context-delivery conclusion |
| --- | --- | --- |
| `ExpertReferences.resolve()` | Reads and validates a local candidate; returns `(Path, report)`. | File selection is implemented; no LLM invocation occurs. |
| `ContentSpec.outline()` | Selects the reference and emits a semantic draft/blueprint plus metadata. | No reference body is placed into a provider request. |
| Role-author workflow | Instructs an authorized operator to resolve and privately hand off/read the file. | `PROCEDURAL`; actual reads depend on the host and tool execution. |
| `commercial_proposal.py:plan_package()` | Records resolver selections; proposal generation uses structured project inputs and templates. | Reference validation is not a generic prompt assembly engine. |
| Fabric contract packet | Renders intended layer-scoped fields and their digest. | Implements a bounded dependency packet, not proof of the provider's entire context. |
| `optional_provider_eval.py:prepare_plan()` / `run()` | Validates bundled public-synthetic examples; a separately consented run concatenates an evaluation instruction with the complete Markdown and passes it to a provider CLI. | A specific implemented whole-file prompt path; not normal authoring or mandatory CI. |

The optional harness deliberately excludes overrides. It checks an
explicit model, unchanged plan, consent and invocation/time limits
before running. Although it records a compiled DCS hash, that does not
mean the compiled DCS body is inserted into its evaluation prompt.
Invocation limits do not establish a token or monetary cap. No live
provider run is required to understand or validate this documentation;
see [optional evaluation
boundaries](../validation/optional-provider-evaluation.md).

## Answering “what did the model receive?”

Keep these five claims separate:

1. **Available:** the catalog or installed skill contains an item.
2. **Selected:** the resolver chose an identity and local file.
3. **Read:** an observed host/tool operation read specified content.
4. **Delivered:** invocation evidence establishes content supplied to the
   provider; a selected path or echoed digest alone is insufficient.
5. **Accepted:** review and human authority establish the permitted use of
   an exact output, separately from input delivery.

For a specific engagement, report observed routing, exact contract and
compiled DCS identity, selected reference/scope, actual read
granularity, provider invocation evidence and outstanding
review/authority status. Absent observation is `NOT VERIFIED`; an
unperformed check is `NOT_EXECUTED`. This is reporting guidance, not a
newly implemented trace schema. Do not put confidential paths, source
passages or raw prompts into public logs to make the report more
detailed.

**PROCEDURAL:** keep controlling policy and DCS obligations distinct
from project facts, role methods and synthetic examples. Embedded
instructions in illustrative Markdown grant no authority or tool
permissions. Under context pressure, explicitly split or reduce optional
reference material rather than silently omit mandatory obligations.

**NOT IMPLEMENTED:** a shared general assembler that measures token
usage and guarantees this composition for every provider request. **NOT
VERIFIED:** which files or extra context a particular installed host
actually supplied without session/invocation evidence. These are precise
follow-up boundaries, not claims that every integration lacks context
controls.

## Source and regression references

`tests/test_expert_references.py` covers precedence, invalid selected
overrides, ambiguity, unsafe paths, checksums, anchors, explicit context
and audience, and outline selection without copying example facts.
`tests/test_reference_bindings.py` checks registered mappings;
`tests/test_content_spec.py` checks compilation and resolution. These
tests establish their named behaviors, not section-level retrieval or
professional correctness. Provider harness tests use fake processes;
they do not prove a real model received or understood an example.
