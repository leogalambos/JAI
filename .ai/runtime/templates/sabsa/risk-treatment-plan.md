# {{library.name}} — Security Risk & Opportunity Treatment Plan

**Organisation:** {{library.organisation}} · **Scope:** {{library.scope}} · **Version:** {{library.version}}

## Risks and opportunities
| Item | Kind | Statement | Likelihood | Impact | Owner | Attributes |
| --- | --- | --- | --- | --- | --- | --- |
{{#risks}}
| {{id}} {{title}} | {{kind}} | {{statement}} | {{likelihood}} | {{impact}} | {{owner}} | {{attributes}} |
{{/risks}}

## Control objectives
| Objective | Statement | Verification | Attributes | Risks | Owner |
| --- | --- | --- | --- | --- | --- |
{{#objectives}}
| {{id}} {{title}} | {{statement}} | {{verification}} | {{attributes}} | {{risks}} | {{owner}} |
{{/objectives}}

## Accepted exceptions / waivers
| Exception | Rationale | Risk acceptance | Owner | Expires | Objectives | Policies |
| --- | --- | --- | --- | --- | --- | --- |
{{#exceptions}}
| {{id}} {{title}} | {{rationale}} | {{risk_acceptance}} | {{owner}} | {{expires}} | {{objectives}} | {{policies}} |
{{/exceptions}}

## Treatment roadmap
| Roadmap item | Current state | Target state | Owner | Date | Acceptance evidence | Objectives |
| --- | --- | --- | --- | --- | --- | --- |
{{#roadmap}}
| {{id}} {{title}} | {{current_state}} | {{target_state}} | {{owner}} | {{target_date}} | {{acceptance_evidence}} | {{objectives}} |
{{/roadmap}}
