# Enterprise release orchestration

## Trigger

Multiple products/platforms/suppliers must release into a shared business/technology environment and need one dependency, readiness and go/no-go process.

## Intended outcome

The integrated release is sequenced, independently readiness-checked, authorised, executed by technical owners, validated and closed with measurable release performance.


<div class="ai-diagram ai-diagram-inline" role="img" aria-label="Enterprise release orchestration workflow">
<svg class="ai-inline-diagram-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 919 756" role="img" aria-labelledby="t d">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0e3859"/><stop offset="1" stop-color="#0b6b9a"/></linearGradient><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3ba9d6"/></marker></defs>
<title id="t">Enterprise release orchestration</title>
<desc id="d">The integrated release is sequenced, independently readiness-checked, authorised, executed by technical owners, validated and closed with measurable release performance.</desc>
<rect width="100%" height="100%" rx="24" fill="#f6fafc" stroke="#d6e6ee"/>
<text x="42" y="38" font-family="Inter,Arial,sans-serif" font-size="23" font-weight="700" fill="#0b1f33">Enterprise release orchestration</text>
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
<text x="159.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">1 · Enterprise Release</text>
<text x="159.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Manager — integrated</text>
<text x="159.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">release scope/calendar</text>
<text x="159.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">and identifies</text>
<rect x="342" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">2 · Architecture</text>
<text x="459.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Repository and Modelling</text>
<text x="459.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Lead — technical/service</text>
<text x="459.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">dependency graph and</text>
<rect x="642" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">3 · Organisational</text>
<text x="759.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Change and Adoption</text>
<text x="759.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Manager —</text>
<text x="759.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">communications/training/adoption/business</text>
<rect x="642" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">4 · Data Migration and</text>
<text x="759.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Cutover Lead — cutover</text>
<text x="759.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">sequence, data</text>
<text x="759.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">reconciliation,</text>
<rect x="342" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">5 · SIAM Manager —</text>
<text x="459.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">supplier staffing,</text>
<text x="459.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">dependencies, handoffs</text>
<text x="459.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">and escalation readiness</text>
<rect x="42" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">6 · Release Engineer —</text>
<text x="159.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">technical release</text>
<text x="159.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">artefacts, provenance</text>
<text x="159.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">and executable rollback</text>
<rect x="42" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="431.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">7 · Secure Delivery /</text>
<text x="159.5" y="453.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">DevSecOps Architect —</text>
<text x="159.5" y="475.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">checks that release</text>
<text x="159.5" y="497.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">provenance, pipeline</text>
<rect x="342" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="431.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">8 · Release Quality</text>
<text x="459.5" y="453.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Gatekeeper —</text>
<text x="459.5" y="475.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">independently checks</text>
<text x="459.5" y="497.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">mandatory release</text>
<rect x="642" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="431.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">9 · Enterprise Release</text>
<text x="759.5" y="453.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Manager — issues</text>
<text x="759.5" y="475.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">delegated integrated</text>
<text x="759.5" y="497.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">go/no-go or routes</text>
<rect x="642" y="592" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="605.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">10 · Release Engineer —</text>
<text x="759.5" y="627.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">executes the authorised</text>
<text x="759.5" y="649.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">technical release</text>
<text x="759.5" y="671.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">through controlled</text>
<rect x="342" y="592" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="605.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">11 · Site Reliability</text>
<text x="459.5" y="627.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Engineer — monitors</text>
<text x="459.5" y="649.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">agreed technical/service</text>
<text x="459.5" y="671.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">signals and triggers</text>
<rect x="42" y="592" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="605.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">12 · IT Service Owner —</text>
<text x="159.5" y="627.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">confirms</text>
<text x="159.5" y="649.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">business/service outcome</text>
<text x="159.5" y="671.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">and closes or escalates</text>
</svg>
<div class="ai-diagram-caption">Canonical workflow sequence from release 26.10.4 (workflow semantics unchanged from the 26.10.0 GA baseline).</div>
</div>

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Enterprise Release Manager | builds integrated release scope/calendar and identifies cross-system dependencies/blackouts | integrated release calendar | All material releases and blackout/business constraints are represented |
| 2 | Architecture Repository and Modelling Lead | validates technical/service dependency graph and critical sequencing constraints | release dependency register | No critical dependency is missing an owner or sequence |
| 3 | Organisational Change and Adoption Manager | validates communications/training/adoption/business readiness for affected cohorts | business readiness | Affected business cohorts have executable readiness actions/evidence |
| 4 | Data Migration and Cutover Lead | validates cutover sequence, data reconciliation, checkpoints and abort criteria | cutover readiness | Cutover and data reconciliation are rehearsed/evidenced for critical transitions |
| 5 | SIAM Manager | validates supplier staffing, dependencies, handoffs and escalation readiness | supplier readiness | No critical supplier dependency is relying on informal availability |
| 6 | Release Engineer | validates technical release artefacts, provenance and executable rollback | technical/rollback readiness | Release artefacts are traceable and rollback is exercised/feasible |
| 7 | Secure Delivery / DevSecOps Architect | checks that release provenance, pipeline controls, policy-as-code and software supply-chain evidence conform to the approved secure-delivery architecture | secure delivery readiness evidence | Critical secure-delivery controls and provenance are evidenced; deviations are owned, time-bound and visible to independent release assurance |
| 8 | Release Quality Gatekeeper | independently checks mandatory release criteria and evidence | release gate assurance | Producer cannot waive its own failed critical gate |
| 9 | Enterprise Release Manager | issues delegated integrated go/no-go or routes decision to higher authority | go/no-go decision | Decision cites evidence, waivers, residual risk and abort triggers |
| 10 | Release Engineer | executes the authorised technical release through controlled pipelines | release execution evidence | Executed artefacts/plan match what was approved |
| 11 | Site Reliability Engineer | monitors agreed technical/service signals and triggers reversal if thresholds breach | technical post-release validation | Rollback/reversal triggers are acted on, not debated after breach |
| 12 | IT Service Owner | confirms business/service outcome and closes or escalates residual issues | release acceptance | Closure states outcome, impact, residual issues and owners |

## Running this workflow: operator and implementer boundary

In **Claude Code or Codex CLI**, use the prompt in the next section (or adapt it to your programme): it is a **provider conversation request**, not a shell program named after this workflow. **You** supply the source materials, actual owners, gate acceptance and any authorisation for changing real systems. **The provider agent** interprets the registered workflow stages and role contracts, calls supported tools if allowed, and returns explicit evidence and blockers. Stage completion in the diagram or metadata is **not** proof of a successful external tool call, an approved exception or a released system.

For consequential decisions explicitly start `/layered` (Claude) or `$workflow-layered` (Codex); this version does not force every direct/natural-language workflow invocation into Fabric. Human L0 authority remains separate, with Codex requiring the actual human to run any protected authority command in a trusted terminal. See [the interaction model](../using/interaction-model.md), [layered engagement](../using/layered-engagement.md) and [human authority](../operations/human-authority.md).

## How to use this workflow

A practical prompt pattern is:

> Apply the `enterprise-release-orchestration` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../siam-multi-supplier/"><small>← Previous · Workflow library</small><strong>SIAM / multi-supplier service integration</strong></a>
  <a class="ai-next" href="../regulatory-change-to-assurance/"><small>Next · Workflow library →</small><strong>Regulatory change to assurance</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
