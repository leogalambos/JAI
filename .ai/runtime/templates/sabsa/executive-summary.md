# {{library.name}} — Executive Security Architecture Summary

{{#draft}}> **DRAFT / NOT RELEASED.** {{counts.errors}} error(s), {{counts.warnings}} warning(s), {{open_cells}} matrix cell(s) open; approval: {{approval_reason}}.
{{/draft}}

**Organisation:** {{library.organisation}}  
**Scope:** {{library.scope}}  
**Owner:** {{library.owner}}  
**Version:** {{library.version}}  
**Architecture elements:** {{counts.elements}}

## Business security intent
{{library.summary}}

## Business attributes
{{#attributes}}
- **{{id}} {{title}}** — {{definition}}; target: **{{target}}**; owner: {{owner}}.
{{/attributes}}

## Principal risks and opportunities
{{#risks}}
- **{{id}} {{title}}** ({{kind}}) — {{statement}}.
{{/risks}}

## Security strategy and control intent
{{#strategies}}
- **{{id}} {{title}}** — {{statement}}.
{{/strategies}}
{{#objectives}}
- **{{id}} {{title}}** — {{statement}}.
{{/objectives}}

## Material governance decisions and exceptions
{{#decisions}}
- **{{id}} {{title}}** — {{decision}}.
{{/decisions}}
{{#exceptions}}
- **{{id}} {{title}}** — {{rationale}}; expires {{expires}}.
{{/exceptions}}

## Transition priorities
{{#roadmap}}
- **{{id}} {{title}}** — {{target_state}} by {{target_date}} (owner {{owner}}).
{{/roadmap}}

## Assurance position
{{#measures}}
- **{{id}} {{title}}** — target {{target}}, frequency {{frequency}}, owner {{owner}}, action on breach: {{threshold_action}}.
{{/measures}}

**Release state:** {{#approved}}APPROVED{{/approved}}{{^approved}}DRAFT / NOT APPROVED{{/approved}}
