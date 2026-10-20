# Expert document overrides

Owner: JAI maintainers · Last reviewed: 2026-10-20

Overrides replace an authoring reference for one document-kind/complexity
slot. They never modify normative DCS requirements, security restrictions,
approval authority or governance policy. Bundled references remain unchanged.

## Paths and precedence

Resolution selects the highest applicable existing reference:

1. Engagement: explicit `--engagement-root DIRECTORY`.
2. Organisation: `--organisation-root DIRECTORY`, otherwise
   `JAI_EXPERT_REFERENCES_DIR` when configured.
3. User: `--user-root DIRECTORY`, otherwise
   `$XDG_CONFIG_HOME/jai/expert_references`, or
   `~/.config/jai/expert_references` when XDG is unset.
4. Bundled: runtime `content/expert_references/`.

Each root uses `<document-kind>/<complexity>.md`. Higher-level absence is
normal and continues resolution. A selected invalid file fails explicitly;
there is no silent fallback. Ambiguous same-level candidates fail, and
references are never silently merged. Missing every applicable reference
also fails.

Optional `target_audiences` and `applicability_context` metadata constrain
which audience and explicit scalar business-context values a reference
supports. An unconstrained bundled reference remains applicable by default.
Selection does not infer professional fitness from a title or industry name.
A valid non-applicable override is skipped; invalid selected metadata is an
error, not permission to fall back. Two applicable candidates at the same
level remain an explicit conflict.

```bash
python3 .ai/runtime/tools/expert_references.py resolve --root . \
  --kind technical-proposal --complexity medium --audience architecture-review
```

Use `--context ./reference-context.json` for explicit business qualifiers.
Keep context values private. DCS applicability context is a separate typed
contract: business qualifiers do not override security or governance rules.

## Replace one reference

Start with a copy of the bundled English fictional example. Edit its body,
preserve its supported metadata and DCS anchors, then validate before use.
Use a disposable demonstration override root for this walkthrough:

```bash
cp .ai/runtime/content/expert_references/decision-paper/medium.md my-medium.md
python3 .ai/runtime/tools/expert_references.py validate --root . \
  --source my-medium.md --kind decision-paper --complexity medium
python3 .ai/runtime/tools/expert_references.py install --root . \
  --source my-medium.md --kind decision-paper --complexity medium \
  --scope user --user-root ./demo-expert-overrides
python3 .ai/runtime/tools/expert_references.py resolve --root . \
  --kind decision-paper --complexity medium \
  --user-root ./demo-expert-overrides
```

Only `decision-paper/medium` changes. Other slots and the registered DCS
remain unchanged. Directly supplying a valid Markdown file in the same slot
also works without source-code changes. See the
[metadata contract](../reference/expert-reference-format.md) before importing
a document with different provenance or classification.

## Restore the bundled default

```bash
python3 .ai/runtime/tools/expert_references.py reset --root . \
  --kind decision-paper --complexity medium \
  --scope user --user-root ./demo-expert-overrides
```

Reset removes the selected override, allowing lower levels to resolve again.
An engagement or organisation reference still takes priority. Use the
corresponding `--scope` and explicit root to manage those levels. JAI updates
do not overwrite separate override directories.

## Privacy and errors

Invalid metadata, unsupported language, missing/duplicate/unknown anchors,
unsafe paths and conflicting candidates produce explicit diagnostics.
Validation and selection reports omit private content, identifying paths and
hashes. Keep source provenance in an authorized private environment. A local
reference is never automatically exported to an optional provider evaluation.

The supported language is currently English. Other languages are rejected
explicitly rather than claimed to have equivalent professional qualification.
