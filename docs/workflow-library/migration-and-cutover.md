# Migration and cutover

## Trigger

A project must move data/services from a current state to a target state through a controlled production cutover.

## Intended outcome

Migration completes with reconciled data, controlled rollback boundaries, operational acceptance and owned residual defects.


<div class="ai-diagram ai-diagram-inline" role="img" aria-label="Migration and cutover workflow">
<svg class="ai-inline-diagram-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 919 582" role="img" aria-labelledby="t d">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0e3859"/><stop offset="1" stop-color="#0b6b9a"/></linearGradient><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3ba9d6"/></marker></defs>
<title id="t">Migration and cutover</title>
<desc id="d">Migration completes with reconciled data, controlled rollback boundaries, operational acceptance and owned residual defects.</desc>
<rect width="100%" height="100%" rx="24" fill="#f6fafc" stroke="#d6e6ee"/>
<text x="42" y="38" font-family="Inter,Arial,sans-serif" font-size="23" font-weight="700" fill="#0b1f33">Migration and cutover</text>
<path d="M 277 116.0 L 334 116.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 577 116.0 L 634 116.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 759.5 162 L 759.5 192 L 759.5 192 L 759.5 236" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 642 290.0 L 585 290.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 342 290.0 L 285 290.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 159.5 336 L 159.5 366 L 159.5 366 L 159.5 410" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<path d="M 277 464.0 L 334 464.0" fill="none" stroke="#3ba9d6" stroke-width="3" marker-end="url(#a)"/>
<rect x="42" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">1 · Data Architect —</text>
<text x="159.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">source/target models,</text>
<text x="159.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">authoritative ownership</text>
<text x="159.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">and data constraints</text>
<rect x="342" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">2 · Data Migration and</text>
<text x="459.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Cutover Lead — migration</text>
<text x="459.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">strategy, reconciliation</text>
<text x="459.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">rules and integrated</text>
<rect x="642" y="70" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="83.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">3 · Data Engineer — and</text>
<text x="759.5" y="105.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">rehearses migration</text>
<text x="759.5" y="127.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">pipelines against</text>
<text x="759.5" y="149.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">production-like volume</text>
<rect x="642" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="759.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">4 · Test Manager —</text>
<text x="759.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">independently assesses</text>
<text x="759.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">migration,</text>
<text x="759.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">reconciliation and</text>
<rect x="342" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">5 · Service Transition</text>
<text x="459.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">and Operational</text>
<text x="459.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">Readiness Manager —</text>
<text x="459.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">confirms monitoring,</text>
<rect x="42" y="244" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="257.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">6 · Release Engineer —</text>
<text x="159.5" y="279.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">integrates deployment</text>
<text x="159.5" y="301.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">artefacts with the</text>
<text x="159.5" y="323.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">cutover critical path</text>
<rect x="42" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="159.5" y="442.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">7 · Change Manager — the</text>
<text x="159.5" y="464.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">production window and</text>
<text x="159.5" y="486.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">stop/go governance</text>
<rect x="342" y="418" width="235" height="92" rx="16" fill="url(#g)"/>
<text x="459.5" y="431.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">8 · IT Service Owner —</text>
<text x="459.5" y="453.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">the migrated service</text>
<text x="459.5" y="475.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">after stability and</text>
<text x="459.5" y="497.0" text-anchor="middle" dominant-baseline="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="650" fill="#fff">reconciliation checks</text>
</svg>
<div class="ai-diagram-caption">Canonical workflow sequence from release 26.10.4 (workflow semantics unchanged from the 26.10.0 GA baseline).</div>
</div>

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Data Architect | defines source/target models, authoritative ownership and data constraints | migration data model and ownership boundaries | Every migrated domain has an accountable data owner and target definition |
| 2 | Data Migration and Cutover Lead | builds migration strategy, reconciliation rules and integrated cutover sequence | migration plan, cutover runbook and rollback plan | Every object has mapping, acceptance and rollback/restore semantics |
| 3 | Data Engineer | implements and rehearses migration pipelines against production-like volume | migration execution evidence and exceptions | Rehearsal proves throughput, error handling and repeatability |
| 4 | Test Manager | independently assesses migration, reconciliation and business acceptance evidence | test and residual-risk report | Exit criteria were defined before execution and are met or explicitly waived |
| 5 | Service Transition and Operational Readiness Manager | confirms monitoring, support, recovery and receiving-team readiness | operational cutover constraints and acceptance evidence | No critical operational readiness gap is unowned |
| 6 | Release Engineer | integrates deployment artefacts with the cutover critical path | release manifest and deployment/rollback evidence | Exact artefact versions and rollback steps are known |
| 7 | Change Manager | authorises the production window and stop/go governance | production change authorisation | Rehearsal, reconciliation and operational evidence are available to the decision |
| 8 | IT Service Owner | accepts the migrated service after stability and reconciliation checks | service acceptance and residual issues | Service, data and ownership acceptance are explicit before legacy retirement |

## Running this workflow: operator and implementer boundary

In **Claude Code or Codex CLI**, use the prompt in the next section (or adapt it to your programme): it is a **provider conversation request**, not a shell program named after this workflow. **You** supply the source materials, actual owners, gate acceptance and any authorisation for changing real systems. **The provider agent** interprets the registered workflow stages and role contracts, calls supported tools if allowed, and returns explicit evidence and blockers. Stage completion in the diagram or metadata is **not** proof of a successful external tool call, an approved exception or a released system.

For consequential decisions explicitly start `/layered` (Claude) or `$workflow-layered` (Codex); this version does not force every direct/natural-language workflow invocation into Fabric. Human L0 authority remains separate, with Codex requiring the actual human to run any protected authority command in a trusted terminal. See [the interaction model](../using/interaction-model.md), [layered engagement](../using/layered-engagement.md) and [human authority](../operations/human-authority.md).

## How to use this workflow

A practical prompt pattern is:

> Apply the `migration-and-cutover` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../design-to-operational-readiness/"><small>← Previous · Workflow library</small><strong>Design to operational readiness</strong></a>
  <a class="ai-next" href="../organisational-change-and-adoption/"><small>Next · Workflow library →</small><strong>Organisational change and adoption</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
