# Expert reference format

Owner: JAI maintainers · Last reviewed: 2026-10-20

Expert references are UTF-8 Markdown documents with YAML front matter.
The separate runtime schema is `content/schema/expert-reference.schema.json`;
this format does not alter Artifact Contract v3 or the DCS specification schema.

## Required metadata

| Field | Meaning |
| --- | --- |
| `reference_id` | Stable reference identifier, preserved for bundled documents. |
| `schema_version` | Literal string `1.0.0`. |
| `document_kind` | Registered supported family, for example `decision-paper`. |
| `complexity` | `simple`, `medium` or `complex`. |
| `language` | Currently `en`. |
| `classification` | `public-synthetic`, `internal`, `confidential` or `restricted`. |
| `provenance` | `ai-authored-proposed` or `user-supplied-proposed`. |
| `fictional_context` | Boolean identifying illustrative rather than actual context. |
| `applicable_dcs` | Exact `kind/<document-kind>` registry reference. |
| `approval_status` | `not-human-approved`; import cannot grant JAI L0 approval. |

A valid bundled example has metadata equivalent to:

```yaml
---
reference_id: example:decision-paper:medium
schema_version: '1.0.0'
document_kind: decision-paper
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/decision-paper
approval_status: not-human-approved
---
```

The body must also meet the checks below. This metadata snippet alone is not
a valid complete reference. Setting `approval_status: approved`, using a
string instead of a Boolean, or mismatching the selected family is invalid.
A plausible reference identifier does not establish authority.

## Stable DCS anchors

Content sections identify exact DCS information-unit IDs. Human-readable
headings and visual presentation may vary. Preserve the supplied anchor
syntax and identifiers when editing; consult the registered kind rather than
inventing identifiers. Duplicate, missing, unknown and inconsistent anchors
are findings with the affected document and rule.

Validation distinguishes four levels:

1. Structural coverage: identifiers link sections to the required units.
2. Content presence and adequacy: empty or placeholder sections do not pass.
3. Evidence and rationale: deterministic diagnostics identify detectable
   unsupported material; unverified professional reasoning remains pending.
4. Professional acceptance: independent competent review and existing JAI
   authority are separate from automatic validation.

**An anchor identifies content; it does not prove its truth or correctness.**
Schema validation and plausible narrative cannot confer professional approval.
The bundled index records public synthetic reference identities and integrity
metadata; private overrides receive sanitized diagnostics.

## Validate a document

```bash
python3 .ai/runtime/tools/expert_references.py validate --root . \
  --source my-medium.md --kind decision-paper --complexity medium
```

See [override configuration](../configuration/expert-document-overrides.md)
for selection and restoration behavior.
