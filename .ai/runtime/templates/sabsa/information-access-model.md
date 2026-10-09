# {{library.name}} — Information, Entity & Privilege Architecture

## Entities
| Entity | Population | Owner | Lifecycle | Domains | Objectives |
| --- | --- | --- | --- | --- | --- |
{{#entities}}
| {{id}} {{title}} | {{population}} | {{owner}} | {{lifecycle}} | {{domains}} | {{objectives}} |
{{/entities}}

## Privilege profiles
| Profile | Privileges | Conditions / SoD | Owner | Entities | Policies | Objectives |
| --- | --- | --- | --- | --- | --- | --- |
{{#privileges}}
| {{id}} {{title}} | {{privileges}} | {{conditions}} | {{owner}} | {{entities}} | {{policies}} | {{objectives}} |
{{/privileges}}

## Information flows
| Flow | Information | Classification | Protection | Source | Target | Services | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
{{#information_flows}}
| {{id}} {{title}} | {{information}} | {{classification}} | {{protection}} | {{source_entity}} | {{target_entity}} | {{services}} | {{owner}} |
{{/information_flows}}
