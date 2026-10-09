# {{library.name}} — Security Mechanism & Component Realisation

## Mechanisms
| Mechanism | Description | Services | Owner | Horizon | Lifecycle |
| --- | --- | --- | --- | --- | --- |
{{#mechanisms}}
| {{id}} {{title}} | {{description}} | {{services}} | {{owner}} | {{horizon}} | {{lifecycle_state}} |
{{/mechanisms}}

## Components
| Component | Product | Configuration | Mechanisms | Standards | Owner | Horizon | Lifecycle |
| --- | --- | --- | --- | --- | --- | --- | --- |
{{#components}}
| {{id}} {{title}} | {{product}} | {{configuration}} | {{mechanisms}} | {{standards}} | {{owner}} | {{horizon}} | {{lifecycle_state}} |
{{/components}}

## End-to-end realisation
| Component | Mechanism | Service | Objective | Attribute | Driver |
| --- | --- | --- | --- | --- | --- |
{{#traceability}}
| {{component}} | {{mechanism}} | {{service}} | {{objective}} | {{attribute}} | {{driver}} |
{{/traceability}}
