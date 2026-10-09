# {{library.name}} — Framework Coverage & Gap Analysis

> This document reports mappings supplied by the organisation. It does not reproduce or interpret licensed framework text beyond identifiers/local labels provided in overlays.

| Framework | Requirement | Status | Architecture elements | Evidence | Roadmap | Exception | Owner | Treatment rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
{{#framework_gaps}}
| {{framework_id}} | {{requirement}} | {{status}} | {{elements}} | {{evidence}} | {{roadmap}} | {{exceptions}} | {{owner}} | {{rationale}} |
{{/framework_gaps}}

## Relevant transition roadmap
{{#roadmap}}
- **{{id}} {{title}}** — {{current_state}} → {{target_state}} by {{target_date}}; acceptance: {{acceptance_evidence}}.
{{/roadmap}}

## Exceptions / waivers
{{#exceptions}}
- **{{id}} {{title}}** — {{rationale}}; risk acceptance {{risk_acceptance}}; owner {{owner}}; expires {{expires}}.
{{/exceptions}}
