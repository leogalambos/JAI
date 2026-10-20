# New service onboarding

## Trigger

A new service or component needs to exist, be deployable and be operable.

## Intended outcome

A service with codified infrastructure, a pipeline, environments, observability and an on-call owner.


<div class="ai-diagram ai-diagram-inline" role="img" aria-label="New service onboarding workflow">
<svg class="ai-inline-diagram-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 919 756" role="img" aria-labelledby="t d">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0e3859"/><stop offset="1" stop-color="#0b6b9a"/></linearGradient><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3ba9d6"/></marker></defs>
<title id="t">New service onboarding</title>
<desc id="d">A service with codified infrastructure, a pipeline, environments, observability and an on-call owner.</desc>
<rect width="100%" height="100%" rx="24" fill="#f6fafc" stroke="#d6e6ee"/>
<text x="42" y="38" font-family="Inter,Arial,sans-serif" font-size="23" font-weight="700" fill="#0b1f33">New service onboarding</text>
<path d="M 277 116.0 L 334 116.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 577 116.0 L 634 116.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 759.5 162 L 759.5 192 L 759.5 192 L 759.5 236" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 642 290.0 L 585 290.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 342 290.0 L 285 290.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 159.5 336 L 159.5 366 L 159.5 366 L 159.5 410" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 277 464.0 L 334 464.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 577 464.0 L 634 464.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 759.5 510 L 759.5 540 L 759.5 540 L 759.5 584" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 642 638.0 L 585 638.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 342 638.0 L 285 638.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<rect x="42" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">1 · Cloud Architect —</text>
<text x="159.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">sets the landing zone,</text>
<text x="159.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">resilience and residency</text>
<text x="159.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">constraints</text>
<rect x="342" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">2 · Infrastructure as</text>
<text x="459.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Code Engineer — codifies</text>
<text x="459.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">the infrastructure and</text>
<text x="459.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">its guardrails</text>
<rect x="642" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">3 · Container Platform</text>
<text x="759.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Engineer — establishes</text>
<text x="759.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">the image build chain</text>
<text x="759.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">and base image lineage</text>
<rect x="642" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">4 · CI/CD Platform</text>
<text x="759.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Engineer — wires the</text>
<text x="759.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">service onto the shared</text>
<text x="759.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">pipeline platform</text>
<rect x="342" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">5 · Secrets and</text>
<text x="459.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Configuration Management</text>
<text x="459.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Engineer — issues the</text>
<text x="459.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">service&#x27;s credentials</text>
<rect x="42" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">6 · Environment Manager</text>
<text x="159.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">— provisions the</text>
<text x="159.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">non-production</text>
<text x="159.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">environments and their</text>
<rect x="42" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="431.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">7 · GitOps and</text>
<text x="159.5" y="453.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Continuous Delivery</text>
<text x="159.5" y="475.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Engineer — promotion and</text>
<text x="159.5" y="497.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">rollback across</text>
<rect x="342" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="431.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">8 · Observability</text>
<text x="459.5" y="453.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Engineer — instruments</text>
<text x="459.5" y="475.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">the service against its</text>
<text x="459.5" y="497.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">objectives</text>
<rect x="642" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="431.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">9 · Site Reliability</text>
<text x="759.5" y="453.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Engineer — agrees the</text>
<text x="759.5" y="475.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">service objective and</text>
<text x="759.5" y="497.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">the error budget policy</text>
<rect x="642" y="592" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="605.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">10 · Application Support</text>
<text x="759.5" y="627.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Analyst — the service</text>
<text x="759.5" y="649.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">into support with a</text>
<text x="759.5" y="671.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">runbook</text>
<rect x="342" y="592" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="605.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">11 · Configuration</text>
<text x="459.5" y="627.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Manager — records the</text>
<text x="459.5" y="649.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">service, its</text>
<text x="459.5" y="671.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">relationships and its</text>
<rect x="42" y="592" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="605.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">12 · IT Service Owner —</text>
<text x="159.5" y="627.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">takes end-to-end</text>
<text x="159.5" y="649.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">ownership of value, cost</text>
<text x="159.5" y="671.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">and risk</text>
</svg>
<div class="ai-diagram-caption">Canonical workflow sequence from release 26.10.4 (workflow semantics unchanged from the 26.10.0 GA baseline).</div>
</div>

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Cloud Architect | sets the landing zone, resilience and residency constraints | target platform design | Resilience claims substantiated by a tested failure scenario |
| 2 | Infrastructure as Code Engineer | codifies the infrastructure and its guardrails | versioned modules, remote locked state, policy-as-code | Applies idempotently from clean; plan reviewed before apply |
| 3 | Container Platform Engineer | establishes the image build chain and base image lineage | signed images with SBOM, immutable tags | Non-root, no build secrets, pinned digests |
| 4 | CI/CD Platform Engineer | wires the service onto the shared pipeline platform | pipeline with federated identity and signed provenance | No static cloud credentials in the CI system |
| 5 | Secrets and Configuration Management Engineer | issues the service's credentials with a lifecycle | dynamic short-lived credentials and a tested revocation path | Static credentials only as a time-bound exception |
| 6 | Environment Manager | provisions the non-production environments and their data | environments with owners, refresh cadence and masked data | No unmasked production personal data anywhere |
| 7 | GitOps and Continuous Delivery Engineer | defines promotion and rollback across environments | desired-state repositories and promotion model | The same immutable artefact is promoted, never rebuilt |
| 8 | Observability Engineer | instruments the service against its objectives | dashboards and owned, actionable alerts | Every alert has an owner, an action and a runbook |
| 9 | Site Reliability Engineer | agrees the service objective and the error budget policy | SLOs and error budget policy | Exhausting the budget changes something, or the SLO is decorative |
| 10 | Application Support Analyst | accepts the service into support with a runbook | runbook and known-error entries | A competent on-call engineer who has never seen it can follow it |
| 11 | Configuration Manager | records the service, its relationships and its owner | configuration items with verified relationships | Owner, lifecycle status and verified-by date present |
| 12 | IT Service Owner | takes end-to-end ownership of value, cost and risk | service definition and service level agreement | Named business contact and an agreed SLA exist |

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

> Apply the `new-service-onboarding` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
