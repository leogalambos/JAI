# {{library.name}} — Security Assurance & Measurement Plan

**Organisation:** {{library.organisation}} · **Scope:** {{library.scope}} · **Version:** {{library.version}}

## Business Attribute Profile
| Attribute | Definition | Metric | Target | Owner |
| --- | --- | --- | --- | --- |
{{#attributes}}
| {{id}} {{title}} | {{definition}} | {{metric}} | {{target}} | {{owner}} |
{{/attributes}}

## Operational measures
| Measure | Metric | Data source | Frequency | Target | Warning | Breach | Owner | Response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
{{#measures}}
| {{id}} {{title}} | {{metric}} | {{data_source}} | {{frequency}} | {{target}} | {{warning_threshold}} | {{breach_threshold}} | {{owner}} | {{threshold_action}} |
{{/measures}}

## Evidence register
| Evidence | Type | Measure(s) | Collector | Location | Collected | Result |
| --- | --- | --- | --- | --- | --- | --- |
{{#evidence}}
| {{id}} {{title}} | {{evidence_type}} | {{measures}} | {{collector}} | {{location}} | {{collected_at}} | {{result}} |
{{/evidence}}

## Evidence-to-business traceability
| Evidence | Measure | Attribute | Driver |
| --- | --- | --- | --- |
{{#assurance_traceability}}
| {{evidence}} | {{measure}} | {{attribute}} | {{driver}} |
{{/assurance_traceability}}
