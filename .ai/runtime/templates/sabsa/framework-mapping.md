# {{library.name}} — External Framework Mapping

{{#frameworks}}
## {{id}} — {{title}} {{version}}
Source: {{source}}  
Mappings: {{total}} · covered {{covered}} · partial {{partial}} · gap {{gap}} · not applicable {{not_applicable}}.
{{/frameworks}}

| Framework | Requirement | Local label | Status | Architecture elements | Evidence | Roadmap | Exceptions | Owner | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
{{#framework_mappings}}
| {{framework_id}} | {{requirement}} | {{title}} | {{status}} | {{elements}} | {{evidence}} | {{roadmap}} | {{exceptions}} | {{owner}} | {{rationale}} |
{{/framework_mappings}}
