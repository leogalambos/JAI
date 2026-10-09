# Resilience validation

## Trigger

A critical service or architecture needs evidence that resilience, RTO/RPO and dependency assumptions work under realistic failure.

## Intended outcome

Business criticality, dependencies and recovery objectives are validated through exercised failure scenarios, findings are remediated and retested, and residual resilience risk is accepted by the correct authority.


<div class="ai-diagram ai-diagram-inline" role="img" aria-label="Resilience validation workflow">
<svg class="ai-inline-diagram-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 919 756" role="img" aria-labelledby="t d">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0e3859"/><stop offset="1" stop-color="#0b6b9a"/></linearGradient><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3ba9d6"/></marker></defs>
<title id="t">Resilience validation</title>
<desc id="d">Business criticality, dependencies and recovery objectives are validated through exercised failure scenarios, findings are remediated and retested, and residual resilience risk is accepted by the correct authority.</desc>
<rect width="100%" height="100%" rx="24" fill="#f6fafc" stroke="#d6e6ee"/>
<text x="42" y="38" font-family="Inter,Arial,sans-serif" font-size="23" font-weight="700" fill="#0b1f33">Resilience validation</text>
<path d="M 277 116.0 L 334 116.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 577 116.0 L 634 116.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 759.5 162 L 759.5 192 L 759.5 192 L 759.5 236" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 642 290.0 L 585 290.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 342 290.0 L 285 290.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 159.5 336 L 159.5 366 L 159.5 366 L 159.5 410" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 277 464.0 L 334 464.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 577 464.0 L 634 464.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 759.5 510 L 759.5 540 L 159.5 540 L 159.5 584" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<rect x="42" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">1 · Business Continuity</text>
<text x="159.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Manager — confirms</text>
<text x="159.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">business criticality,</text>
<text x="159.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">impact tolerances and</text>
<rect x="342" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">2 · Operational and</text>
<text x="459.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Technology Resilience</text>
<text x="459.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Architect —</text>
<text x="459.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">technical/supplier/data</text>
<rect x="642" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">3 · Disaster Recovery</text>
<text x="759.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Coordinator — RTO/RPO</text>
<text x="759.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">and recovery sequencing</text>
<text x="759.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">against dependency</text>
<rect x="642" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">4 · Operational and</text>
<text x="759.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Technology Resilience</text>
<text x="759.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Architect —</text>
<text x="759.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">resilience/recovery</text>
<rect x="342" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">5 · Test Manager — the</text>
<text x="459.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">exercise plan,</text>
<text x="459.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">entry/exit criteria,</text>
<text x="459.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">injects and evidence</text>
<rect x="42" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">6 · Chaos and Resilience</text>
<text x="159.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Engineer — executes</text>
<text x="159.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">authorised failure</text>
<text x="159.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">experiments/exercises</text>
<rect x="42" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="431.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">7 · Control Tester —</text>
<text x="159.5" y="453.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">independently evaluates</text>
<text x="159.5" y="475.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">evidence and records</text>
<text x="159.5" y="497.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">control/resilience</text>
<rect x="342" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="431.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">8 · Operational and</text>
<text x="459.5" y="453.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Technology Resilience</text>
<text x="459.5" y="475.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Architect — owned</text>
<text x="459.5" y="497.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">remediation across</text>
<rect x="642" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="431.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">9 · Test Manager —</text>
<text x="759.5" y="453.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">retests failed claims</text>
<text x="759.5" y="475.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">after remediation using</text>
<text x="759.5" y="497.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">comparable criteria</text>
<rect x="42" y="592" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="605.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">10 · IT Service Owner —</text>
<text x="159.5" y="627.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">demonstrated resilience</text>
<text x="159.5" y="649.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">or explicitly accepts</text>
<text x="159.5" y="671.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">residual risk within</text>
</svg>
<div class="ai-diagram-caption">Canonical workflow sequence from release 26.10.4 (workflow semantics unchanged from the 26.10.0 GA baseline).</div>
</div>

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Business Continuity Manager | confirms business criticality, impact tolerances and priority services/processes | business criticality baseline | Criticality and tolerances have business ownership |
| 2 | Operational and Technology Resilience Architect | maps technical/supplier/data dependencies and correlated failure domains | dependency/failure-domain model | No critical path has an unknown/unowned dependency |
| 3 | Disaster Recovery Coordinator | validates RTO/RPO and recovery sequencing against dependency reality | validated recovery objectives | Objectives are feasible end to end, not only per component |
| 4 | Operational and Technology Resilience Architect | defines resilience/recovery architecture and degradation patterns | resilience design with failure assumptions | Design addresses single/shared failure modes and measurable outcomes |
| 5 | Test Manager | builds the exercise plan, entry/exit criteria, injects and evidence capture method | approved exercise plan | Test design can falsify the resilience claims and protects production safety |
| 6 | Chaos and Resilience Engineer | executes authorised failure experiments/exercises and captures telemetry | exercise evidence | Execution matches approved scope and evidence is attributable |
| 7 | Control Tester | independently evaluates evidence and records control/resilience findings | findings register | Findings distinguish observation, criterion, impact and evidence |
| 8 | Operational and Technology Resilience Architect | coordinates owned remediation across architecture, operations and suppliers | remediation plan | Every material finding has owner/date/design response |
| 9 | Test Manager | retests failed claims after remediation using comparable criteria | retest result | Critical findings are demonstrated fixed, not administratively closed |
| 10 | IT Service Owner | accepts demonstrated resilience or explicitly accepts residual risk within authority | resilience acceptance | Acceptance states evidence, residual risk and next validation date |

## Running this workflow: operator and implementer boundary

In **Claude Code or Codex CLI**, use the prompt in the next section (or adapt it to your programme): it is a **provider conversation request**, not a shell program named after this workflow. **You** supply the source materials, actual owners, gate acceptance and any authorisation for changing real systems. **The provider agent** interprets the registered workflow stages and role contracts, calls supported tools if allowed, and returns explicit evidence and blockers. Stage completion in the diagram or metadata is **not** proof of a successful external tool call, an approved exception or a released system.

For consequential decisions explicitly start `/layered` (Claude) or `$workflow-layered` (Codex); this version does not force every direct/natural-language workflow invocation into Fabric. Human L0 authority remains separate, with Codex requiring the actual human to run any protected authority command in a trusted terminal. See [the interaction model](../using/interaction-model.md), [layered engagement](../using/layered-engagement.md) and [human authority](../operations/human-authority.md).

## How to use this workflow

A practical prompt pattern is:

> Apply the `resilience-validation` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../cyber-incident-breach-to-recovery/"><small>← Previous · Workflow library</small><strong>Cyber incident / breach to recovery</strong></a>
  <a class="ai-next" href="../demand-to-portfolio-to-funding/"><small>Next · Workflow library →</small><strong>Demand to portfolio to funding</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
