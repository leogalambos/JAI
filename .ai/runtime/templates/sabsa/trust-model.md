# {{library.name}} — Security Domain & Trust Model

## Security domains
| Domain | Scope | Authority | Owner | Objectives |
| --- | --- | --- | --- | --- |
{{#domains}}
| {{id}} {{title}} | {{scope}} | {{authority}} | {{owner}} | {{objectives}} |
{{/domains}}

## Trust relationships
| Trust | Source | Target | Purpose | Trust basis | Assurance requirement | Owner | Expiry |
| --- | --- | --- | --- | --- | --- | --- | --- |
{{#trusts}}
| {{id}} {{title}} | {{source_domain}} | {{target_domain}} | {{purpose}} | {{trust_basis}} | {{assurance_requirement}} | {{owner}} | {{expiry}} |
{{/trusts}}

## Trust-to-business traceability
| Trust | Objective | Attribute | Driver |
| --- | --- | --- | --- |
{{#trust_traceability}}
| {{trust}} | {{objective}} | {{attribute}} | {{driver}} |
{{/trust_traceability}}
