# {{library.name}} — Cross-Library Reuse Register

## Reused libraries
| Alias | Library | Version | Configured path | Approved | Approval state | Type filter | ID filter |
| --- | --- | --- | --- | --- | --- | --- | --- |
{{#reuse_libraries}}
| {{alias}} | {{name}} | {{version}} | {{path}} | {{approved}} | {{approval_reason}} | {{types}} | {{ids}} |
{{/reuse_libraries}}

## Imported/reused elements
| Namespaced ID | Source ID | Alias | Type | Layer | Title | Source library |
| --- | --- | --- | --- | --- | --- | --- |
{{#reused_elements}}
| {{id}} | {{origin_id}} | {{reuse_alias}} | {{type}} | {{layer}} | {{title}} | {{origin_library}} |
{{/reused_elements}}

A consumer approval is bound to the source-library snapshot hashes. Changes in a reused library therefore make the consumer approval stale until impact analysis and re-approval are completed.
