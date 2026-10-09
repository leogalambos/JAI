# External framework overlays

An overlay maps external requirement **identifiers** to SABSA
architecture elements, evidence, roadmap items and exceptions. It
deliberately does not bundle requirement text from ISO, PCI, regulatory
or other licensed sources. Organisations may add titles/text when they
have the right to reproduce that content.

Supported mapping states: `covered`, `partial`, `gap`, `not-applicable`.
A `gap` or `partial` mapping should normally cite an `RM-*` roadmap item
or an `EX-*` exception. Set `evidence_required: true` when `covered`
mappings must cite first-class `EV-*` evidence.
