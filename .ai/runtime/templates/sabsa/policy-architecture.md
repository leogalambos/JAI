# {{library.name}} — Security Policy Architecture

## Security strategies
{{#strategies}}
- **{{id}} {{title}}** — {{statement}}; rationale: {{rationale}}; owner: {{owner}}.
{{/strategies}}

## Policies
| Policy | Statement | Owner | Effective | Review | Objectives | Services |
| --- | --- | --- | --- | --- | --- | --- |
{{#policies}}
| {{id}} {{title}} | {{statement}} | {{owner}} | {{effective_date}} | {{review_date}} | {{objectives}} | {{services}} |
{{/policies}}

## Standards
| Standard | Authority | Version | Requirement | Policies | Mechanisms | Owner |
| --- | --- | --- | --- | --- | --- | --- |
{{#standards}}
| {{id}} {{title}} | {{authority}} | {{version}} | {{requirement}} | {{policies}} | {{mechanisms}} | {{owner}} |
{{/standards}}

## Policy-to-business traceability
| Policy | Objective | Attribute | Driver |
| --- | --- | --- | --- |
{{#policy_traceability}}
| {{policy}} | {{objective}} | {{attribute}} | {{driver}} |
{{/policy_traceability}}
