# Production change

## Trigger

A change must reach production: a feature, a fix, an infrastructure change or a configuration change.

## Intended outcome

The change in production, recorded, with a proven way back.


<div class="ai-diagram ai-diagram-inline" role="img" aria-label="Production change workflow">
<svg class="ai-inline-diagram-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 919 582" role="img" aria-labelledby="t d">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0e3859"/><stop offset="1" stop-color="#0b6b9a"/></linearGradient><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3ba9d6"/></marker></defs>
<title id="t">Production change</title>
<desc id="d">The change in production, recorded, with a proven way back.</desc>
<rect width="100%" height="100%" rx="24" fill="#f6fafc" stroke="#d6e6ee"/>
<text x="42" y="38" font-family="Inter,Arial,sans-serif" font-size="23" font-weight="700" fill="#0b1f33">Production change</text>
<path d="M 277 116.0 L 334 116.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 577 116.0 L 634 116.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 759.5 162 L 759.5 192 L 759.5 192 L 759.5 236" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 642 290.0 L 585 290.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 342 290.0 L 285 290.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 159.5 336 L 159.5 366 L 159.5 366 L 159.5 410" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 277 464.0 L 334 464.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<rect x="42" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">1 · Software Engineer —</text>
<text x="159.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">produces the change with</text>
<text x="159.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">its rollback path</text>
<text x="159.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">designed first</text>
<rect x="342" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">2 · Infrastructure as</text>
<text x="459.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Code Engineer — produces</text>
<text x="459.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">any infrastructure</text>
<text x="459.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">change as a reviewed</text>
<rect x="642" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="94.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">3 · Test Analyst — and</text>
<text x="759.5" y="116.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">states what is not</text>
<text x="759.5" y="138.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">covered</text>
<rect x="642" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="268.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">4 · Release Engineer —</text>
<text x="759.5" y="290.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">packages the release and</text>
<text x="759.5" y="312.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">verifies provenance</text>
<rect x="342" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="268.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">5 · Change Manager — at</text>
<text x="459.5" y="290.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">the level the risk class</text>
<text x="459.5" y="312.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">requires</text>
<rect x="42" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">6 · GitOps and</text>
<text x="159.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Continuous Delivery</text>
<text x="159.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Engineer — deploys</text>
<text x="159.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">progressively behind a</text>
<rect x="42" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="431.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">7 · Site Reliability</text>
<text x="159.5" y="453.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Engineer — watches the</text>
<text x="159.5" y="475.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">agreed signals for the</text>
<text x="159.5" y="497.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">agreed window</text>
<rect x="342" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="431.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">8 · Configuration</text>
<text x="459.5" y="453.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Manager — updates the</text>
<text x="459.5" y="475.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">record of what now</text>
<text x="459.5" y="497.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">exists</text>
</svg>
<div class="ai-diagram-caption">Canonical workflow sequence from release 26.10.4 (workflow semantics unchanged from the 26.10.0 GA baseline).</div>
</div>

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Software Engineer | produces the change with its rollback path designed first | reviewed change and rollback plan | Small enough to review in one pass |
| 2 | Infrastructure as Code Engineer | produces any infrastructure change as a reviewed plan | reviewed plan; destructive operations flagged | The applied plan is the reviewed plan |
| 3 | Test Analyst | verifies and states what is not covered | test evidence with coverage and residual risk | Residual risk accepted by a named person |
| 4 | Release Engineer | packages the release and verifies provenance | release manifest with signed provenance | Every artefact traceable to a source commit |
| 5 | Change Manager | authorises at the level the risk class requires | change record and schedule slot | Standard changes pre-authorised and measured, not queued for ceremony |
| 6 | GitOps and Continuous Delivery Engineer | deploys progressively behind a health gate | rollout with automatic reversal armed | Rollback exercised, not merely documented |
| 7 | Site Reliability Engineer | watches the agreed signals for the agreed window | post-release confirmation or a reversal decision | Reversal executed on trigger, not on debate |
| 8 | Configuration Manager | updates the record of what now exists | updated configuration items | Record updated the same day the change lands |

## Running this workflow: operator and implementer boundary

Use the next prompt in the provider conversation, not as a shell command.
You supply permitted inputs, actual owners, gate acceptance and authority for
real-system changes. The agent returns evidence and blockers; a listed stage
is not proof of execution, approval or release.

For consequential work, explicitly start `/layered` or `$workflow-layered`;
natural-language routing does not universally enforce Fabric. L0 authority
remains human, and Codex protected authority commands require the human's
trusted terminal. Follow the [interaction model](../using/interaction-model.md),
[layered engagement](../using/layered-engagement.md) and
[human authority](../operations/human-authority.md). Keep the workflow-specific
stop conditions and gates on this page.

## How to use this workflow

A practical prompt pattern is:

> Apply the `production-change` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
