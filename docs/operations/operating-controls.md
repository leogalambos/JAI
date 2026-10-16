# Operating controls

## Recommended operating controls for production use

- keep model-routing overrides under controlled configuration management;
- treat managed policy and the consequential-task classification rule as governed configuration;
- retain `.findings/` and `.fabric/` records according to security, privacy and audit requirements;
- validate provider parity after a model-routing/provider change;
- requalify live provider/model behavior before making provider-specific behavioral claims;
- validate publication and visual QA after renderer/environment changes;
- require explicit L0 authority for consequential acceptance/exception/revision decisions;
- monitor evidence expiry, invalidation and unresolved review queues;
- ensure target-side idempotency/concurrency controls exist for consequential external actions;
- use OS/container/network controls where a hook or prompt alone is not a strong enough enforcement boundary.

## Consequential-task routing policy

The current release strongly supervises work once `/layered` is used, but direct role/workflow paths still exist. A production deployment that wants layered-by-construction behavior should define an entry rule such as:

> If a task can materially change production, approve/accept risk, publish a consequential enterprise statement, create compliance evidence, or drive a high-impact architecture decision, it must open a layered engagement before specialist execution.

Enforce that rule through the host/orchestration entry boundary where possible rather than relying only on user memory.

## Separation-of-duties hot spots

Pay particular attention to:

- generation vs evidence qualification;
- L5 realisation vs L6 evidence collection;
- review vs authoring;
- publication editing vs semantic ownership;
- library author vs library approver/release;
- risk/exception recommendation vs L0 authority decision;
- authority acts in Codex fail-closed contexts;
- policy administration vs the model whose work the policy controls.

## Fabric operational hygiene

**Who performs these checks:** the provider orchestrator should call Fabric through its allowed tools while the layered engagement runs; an engineer/incident responder may reproduce the checks directly for audit or recovery. The ordinary user asks for status and evidence through `/fabric-report` or `$workflow-fabric-report`, rather than manually performing every Python transition. A protected Codex L0 decision still requires the human-operated terminal action.

For long-running consequential work:

- run `fabric.py status` at every open escalation;
- do not retry failed provider/tool calls invisibly — record the failure first;
- invalidate depended-on records when evidence changes materially;
- keep the shared episode budget finite;
- preserve the original intent and all failed/rejected attempts;
- close or explicitly disposition stale escalation queues;
- use `verify` and `justify --strict` before consequential release.

## Human oversight quality

Human oversight is not demonstrated merely by the existence of an approval field. Monitor workload, decision latency, repeated rubber-stamp patterns, expired exceptions and whether operators can actually see decisive evidence/blockers.
