# Design to operational readiness

## Trigger

A solution design is becoming build/release ready and must prove it can be operated safely before go-live.

## Intended outcome

The receiving service organisation explicitly accepts an evidenced, supportable and recoverable service.


<div class="ai-diagram ai-diagram-inline" role="img" aria-label="Design to operational readiness workflow">
<svg class="ai-inline-diagram-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 919 582" role="img" aria-labelledby="t d">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0e3859"/><stop offset="1" stop-color="#0b6b9a"/></linearGradient><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3ba9d6"/></marker></defs>
<title id="t">Design to operational readiness</title>
<desc id="d">The receiving service organisation explicitly accepts an evidenced, supportable and recoverable service.</desc>
<rect width="100%" height="100%" rx="24" fill="#f6fafc" stroke="#d6e6ee"/>
<text x="42" y="38" font-family="Inter,Arial,sans-serif" font-size="23" font-weight="700" fill="#0b1f33">Design to operational readiness</text>
<path d="M 277 116.0 L 334 116.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 577 116.0 L 634 116.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 759.5 162 L 759.5 192 L 759.5 192 L 759.5 236" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 642 290.0 L 585 290.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 342 290.0 L 285 290.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 159.5 336 L 159.5 366 L 159.5 366 L 159.5 410" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<rect x="42" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">1 · Solution Architect —</text>
<text x="159.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">the target architecture,</text>
<text x="159.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">NFRs, dependencies and</text>
<text x="159.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">failure modes</text>
<rect x="342" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="94.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">2 · Security Architect —</text>
<text x="459.5" y="116.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">security controls and</text>
<text x="459.5" y="138.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">residual security risks</text>
<rect x="642" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">3 · Operational and</text>
<text x="759.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Technology Resilience</text>
<text x="759.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Architect — the design</text>
<text x="759.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">against failure domains,</text>
<rect x="642" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">4 · Site Reliability</text>
<text x="759.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Engineer — SLOs,</text>
<text x="759.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">observability, alerting</text>
<text x="759.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">and operability signals</text>
<rect x="342" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">5 · Service Transition</text>
<text x="459.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">and Operational</text>
<text x="459.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Readiness Manager — and</text>
<text x="459.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">assesses operational</text>
<rect x="42" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">6 · Change Manager —</text>
<text x="159.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">checks the production</text>
<text x="159.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">change path and</text>
<text x="159.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">risk-class approval</text>
<rect x="42" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="431.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">7 · IT Service Owner —</text>
<text x="159.5" y="453.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">service ownership and</text>
<text x="159.5" y="475.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">residual operational</text>
<text x="159.5" y="497.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">risk</text>
</svg>
<div class="ai-diagram-caption">Canonical workflow sequence from release 26.10.4 (workflow semantics unchanged from the 26.10.0 GA baseline).</div>
</div>

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Solution Architect | defines the target architecture, NFRs, dependencies and failure modes | solution architecture and decision records | Quality attributes and failure modes are explicit and testable |
| 2 | Security Architect | defines security controls and residual security risks | security architecture and control requirements | Controls trace to risks and objectives |
| 3 | Operational and Technology Resilience Architect | tests the design against failure domains, impact tolerances and recovery paths | resilience architecture and validation scenarios | Resilience claims identify dependencies, failure domains and validation method |
| 4 | Site Reliability Engineer | defines SLOs, observability, alerting and operability signals | SLO/monitoring design and runbook requirements | Alerts are actionable and every SLO has a data source |
| 5 | Service Transition and Operational Readiness Manager | assembles and assesses operational acceptance evidence | operational readiness assessment and evidence pack | Every readiness criterion is pass/fail/waived with evidence and owner |
| 6 | Change Manager | checks the production change path and risk-class approval | change authorisation decision | Change risk and readiness evidence match the approval route |
| 7 | IT Service Owner | accepts service ownership and residual operational risk | service acceptance | Support ownership, SLOs and residual risks are explicitly accepted |

## Running this workflow: operator and implementer boundary

In **Claude Code or Codex CLI**, use the prompt in the next section (or adapt it to your programme): it is a **provider conversation request**, not a shell program named after this workflow. **You** supply the source materials, actual owners, gate acceptance and any authorisation for changing real systems. **The provider agent** interprets the registered workflow stages and role contracts, calls supported tools if allowed, and returns explicit evidence and blockers. Stage completion in the diagram or metadata is **not** proof of a successful external tool call, an approved exception or a released system.

For consequential decisions explicitly start `/layered` (Claude) or `$workflow-layered` (Codex); this version does not force every direct/natural-language workflow invocation into Fabric. Human L0 authority remains separate, with Codex requiring the actual human to run any protected authority command in a trusted terminal. See [the interaction model](../using/interaction-model.md), [layered engagement](../using/layered-engagement.md) and [human authority](../operations/human-authority.md).

## How to use this workflow

A practical prompt pattern is:

> Apply the `design-to-operational-readiness` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../business-case-to-benefits/"><small>← Previous · Workflow library</small><strong>Business case to realised benefits</strong></a>
  <a class="ai-next" href="../migration-and-cutover/"><small>Next · Workflow library →</small><strong>Migration and cutover</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
