# Recorded display labels

Contract identifier `jai.fabric-explorer.recorded-label/1`.

A label is a plain-text presentation value attached to one admitted record
version. It carries `text` and `source`. Source forms are:

| Kind | Fields |
| --- | --- |
| `record-field` | Exact `versionId` and RFC 6901 `pointer` relative to its manifest |
| `companion-excerpt` | Exact `versionId`, material `pointer` relative to its manifest, and `blobId` |
| `unavailable` | Exact `versionId` and `reason` for the typed fallback |

A use inherits the label and source of its exact version. The graph adapter
carries provenance on versions and uses in the optional
`jai.recorded-label` extension. Legacy facts without presentation metadata
retain their existing labels. Use scope, selection,
review and lifecycle status remain distinct facts. Two versions may have
identical text. Search by text can return both. Exact ID lookup, graph keys,
relationships and record hashes retain their existing identities.

## Resolution

1. Prefer a nonempty recorded `display_summary` for an answer, bundle or
   escalation product. For a question or criterion, use the exact recorded
   setter formulation or criterion statement. For findings and escalations,
   prefer the recorded observation, failed criterion or owner reason bound to
   that exact version. For assessments and decisions use the verdict or action
   with the exact subject label or recorded reason, where available. Retain
   the field pointer of the substantive text. When a label uses multiple
   admitted fields or records, retain the primary source in `source` and the remaining entries in
   `additionalSources`, in display order.
2. When structured text is unavailable, consider a single material pointer
   of that exact record with a trusted text designation and a known semantic
   role. The production broker must authorize the exact admitted source and
   companion, verify its lifecycle blob digest, enforce the 16 KiB individual
   limit and decode strict UTF-8. Given eligible Markdown, take the first
   complete, nonempty line other than a heading. Other eligible text uses
   its first complete nonempty line. The prose comes literally from the
   companion. A choice between multiple equally eligible materials is
   ambiguous. The import-wide byte ceiling is 1 MiB, including the journal bytes read to confirm exact companion references.
3. When neither source yields displayable text, emit the layer and dimension
   when recorded, then the record type and `summary unavailable`, such as
   `L1 HOW · answer summary unavailable`. Record one of
   `no-text-source`, `ambiguous-source`, `missing`, `read-denied`,
   `binary`, `oversized`, `digest-mismatch`, `invalid-utf8`,
   `empty-text` or `import-budget-exhausted`. An ineligible companion
   must not supply text or a successful provenance value.

## Text and presentation

Join label parts with ` · `. The context part is `L<layer> <DIMENSION>`
when both are recorded and `L<layer>` when the layer stands alone. Omit
unavailable parts. Questions, criteria, answers, bundles, findings and
escalations use the context and resolved text. Assessments and decisions
use the context, recorded verdict or action, and the subject text or reason.
Use the canonical subject's substantive text without repeating its context.

Normalize display and search with the same procedure. Collapse every run of
Unicode White_Space code points to one ASCII space and trim the resulting
leading and trailing spaces. Preserve other code points and literal markup.
An empty normalized value is unavailable. Limit the normalized summary to
160 Unicode code points and the full label to 192 code points. A truncation
uses `…` as its final code point within the limit. Apply the type-specific
prefix before enforcing the full-label limit. These limits apply to display
and its index. The inspector retains the full authorized source and exact
reference. Use ordinary text rendering and escaping.

The production admission point is the desktop recorded projection and import
model. Companion access uses the existing main-process broker and admitted
byte-handle lifecycle. Bind labels before publishing a candidate import
generation. Refresh can reuse a generation when the admitted journals and
observed companion identities, file metadata and access states are unchanged.
Changed or newly available companions trigger a candidate import even when
the journal bytes are identical; the renderer receives bounded text and provenance.

The [recorded label cases](test/fixtures/recorded-labels.json) use canonical
nested manifests and exact version IDs. The file is an admission input and
expected-result fixture. Production journal routing and live companion access
are exercised in the import and viewer increments.
