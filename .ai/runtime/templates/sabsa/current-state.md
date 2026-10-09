# {{library.name}} — Current Security Architecture Baseline

**Generated:** {{generated}}

| Element | Type | Layer | Summary | Lifecycle | Valid from | Valid until |
| --- | --- | --- | --- | --- | --- | --- |
{{#current_elements}}
| {{id}} {{title}} | {{type}} | {{layer}} | {{summary}} | {{lifecycle_state}} | {{valid_from}} | {{valid_until}} |
{{/current_elements}}

## Elements without an explicit architecture horizon
The following elements are intentionally not silently classified as current; assign `horizon` explicitly when lifecycle/current-target reporting matters.

{{#unspecified_horizon}}
- **{{id}} {{title}}** ({{type}}, {{layer}}) — {{summary}}
{{/unspecified_horizon}}
