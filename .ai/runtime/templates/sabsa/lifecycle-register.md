# {{library.name}} — Architecture Lifecycle Register

## Current
{{#current_elements}}
- **{{id}} {{title}}** ({{type}}) — lifecycle {{lifecycle_state}}; valid {{valid_from}} → {{valid_until}}.
{{/current_elements}}

## Transition
{{#transition_elements}}
- **{{id}} {{title}}** ({{type}}) — lifecycle {{lifecycle_state}}; predecessors {{predecessors}}; roadmap {{transition_items}}.
{{/transition_elements}}

## Target
{{#target_elements}}
- **{{id}} {{title}}** ({{type}}) — lifecycle {{lifecycle_state}}; predecessors {{predecessors}}; roadmap {{transition_items}}.
{{/target_elements}}

## Reference
{{#reference_elements}}
- **{{id}} {{title}}** ({{type}}) — {{summary}}.
{{/reference_elements}}

## Unspecified
{{#unspecified_horizon}}
- **{{id}} {{title}}** ({{type}}) — horizon not yet classified.
{{/unspecified_horizon}}
