# {{library.name}} — Current → Target Transition Architecture

## Mapped transitions
| Current / predecessor | Current title | Roadmap / transition | Transition title | Target | Target title | Type | Target lifecycle |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
{{#current_target_transitions}}
| {{current}} | {{current_title}} | {{transition}} | {{transition_title}} | {{target}} | {{target_title}} | {{type}} | {{target_lifecycle}} |
{{/current_target_transitions}}

## Transition-horizon elements
{{#transition_elements}}
- **{{id}} {{title}}** ({{type}}) — {{summary}}; lifecycle {{lifecycle_state}}; predecessor(s) {{predecessors}}; roadmap {{transition_items}}.
{{/transition_elements}}

## Roadmap
{{#roadmap}}
- **{{id}} {{title}}** — {{current_state}} → {{target_state}} by {{target_date}}; owner {{owner}}; acceptance: {{acceptance_evidence}}.
{{/roadmap}}
