# Justifiable Fabric

The **Justifiable Fabric** is the append-only assurance ledger and supervision runtime behind `/layered` engagements.

It is not the global semantic source of truth. Canonical semantic identity belongs to JAI and domain profiles. Fabric records point to the relevant canonical object identities/hashes and record **who did what, under which contract, with which evidence/review/authority state**.

## What the operator uses; what the runtime does

| In a Claude/Codex conversation | Behind the scenes |
| --- | --- |
| Start `/layered <intent>` or `$workflow-layered <intent>`. | The orchestrator creates a Fabric engagement, records intent, issues typed contracts and delegates the work. |
| Ask for blockers, evidence or an independent `/fabric-report` / `$workflow-fabric-report`. | `fabric-auditor` calls `fabric.py` read-only status/report/verification operations and cites actual record IDs. |
| Supply missing material or respond to an escalation. | The agent records failed attempts, reviews and bounded recovery; the deterministic runtime rejects invalid transitions. |
| Make L0 decisions using the provider's trusted mechanism. | Claude may present an interactive gate; Codex intentionally **cannot perform the authority command** and must give it to the human for separate execution. |

**No normal manual Fabric setup is required.** The Python snippets below are the underlying **maintainer/implementation API** and show how a recorded event is reproduced or investigated. Their presence does not mean a user must run them after invoking the provider skill. The runtime is invoked by model-orchestrated tool calls; missing execution or blocked permissions must be surfaced as unresolved work, not reported as success. See [the operator journey](../using/layered-engagement.md) and [human authority](../operations/human-authority.md).

## What it records

A fabric engagement can contain typed records for:

- operator intent and requirements;
- adjacent-layer contracts;
- product fragments/candidates;
- evidence and evidence-file digests;
- reviews and constraints;
- explicit failures;
- conflicts and contradictions;
- escalations and reformulations;
- human authority decisions;
- release decisions and invalidations;
- execution/assurance lineage.

Records are append-only and hash-chained. Corrections create new records rather than rewriting earlier history.

## Layer model

<div class="ai-diagram ai-diagram-inline">
  <img src="../../assets/diagrams/layered-runtime-cycle.svg" alt="Six JAI layers with downward contracts, upward evidence and external human authority">
</div>

**L0 is Human Authority and is not part of the six-layer JAI core.**

Adjacent-layer transformation is the default and enforced relation rules prevent a lower-layer product from being silently promoted across intermediate transformation boundaries.

## Where the record lives

Default engagement record:

```text
<current working directory>/.fabric/<engagement>.jsonl
```

Override the record directory with `FABRIC_HOME`.

Formal L0 uses a separately protected Ed25519 operator key, never an
agent-accessible signing secret. The verifier reads a protected public trust
pin; it validates the exact request/state-bound receipt before applying it.
See [human authority](../operations/human-authority.md) and the
[operator walkthrough](../operations/operator-walkthrough.md) for enrollment,
approval and rejection. Unsupported historical ledgers are archive-only;
a managed hook or provider tool approval does not establish independent L0.
Local ledger hashes do not prevent rollback without separate protected custody.

## Context binding

A layer agent is intended to receive the rendered contract packet rather than the full unconstrained conversation. The packet carries a SHA-256 `context_digest`; ingestion rejects a result that declares a different digest.

This creates an auditable intended context boundary. It does **not** by itself prove that an external provider received no additional context — that remains a provider/host integration property.

## Review before promotion

The upward path is a review path. A layer can build upward only from child fragments it has accepted. This prevents a summariser from laundering an unresolved lower-layer result into a stronger state merely by rewriting it.

Strict release mode distinguishes direct/evidenced support from weaker relations such as correlation or resonance.

## Bounded supervision

The deterministic policy kernel is stored in:

```text
~/.ai/it-role-house/fabric/supervision-policy.json
```

The policy treats retryable failures, contradictions, budget exhaustion and operator-boundary cases differently. A model cannot grant itself additional autonomous attempts.

Default bounds:

- rework: `3` per contract lineage;
- reformulation: `2` per layer per round;
- contracts: `40` per round;
- human revision rounds: `5` before explicit override;
- shared episode transitions: `120`.

See [Running a layered justifiable engagement](../using/layered-engagement.md) for the full recovery ladder.

## Rework is not reformulation

**Rework** is another attempt at the same requirement. The runtime prevents it from changing material semantic fields such as `what`, `why`, evidence obligation and escalation condition.

**Reformulation** creates a new requirement generation and can only be issued by the layer that owns/issued the strained requirement.

**Escalation** moves an unresolved issue one layer upward. Authority matters such as risk acceptance cannot be downgraded into a reformulatable technical problem.

## Evidence drift and invalidation

When an evidence file is recorded, the Fabric stores its digest. If the file later changes, strict release eligibility fails.

When a depended-on Fabric record is superseded or invalidated, the orchestrator (or a maintainer performing recovery) calls the internal API:

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py invalidate <engagement> \
  --changed <record-id> --reason '<reason>' --request-out invalidation-plan.json
```

This prepares a pending lifecycle plan without mutating the ledger. The external
human signs with `lifecycle-update` capability and performs protected
`lifecycle-apply --request invalidation-plan.json --receipt RECEIPT`. Exact effects
cancel affected conclusions and dependent reviews, acceptance and permissions
across scopes. Fresh verification, independent review and new human acceptance
are required; unrelated branches remain. See [recovery](../operations/lifecycle-recovery.md)
for exact installed signing and receipt handling.

## Release eligibility

Finishing generation is not release. The release gate requires, among other things:

- strict justifiability of the product;
- accepted review state;
- appropriate L0 authority acceptance for the consequential product;
- intact fabric hash chain and well-typed relations;
- no current evidence drift/blocking invalidation.

Internal checks run by an agent or maintainer (the ordinary operator asks for `$workflow-fabric-report` or `/fabric-report` instead):

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py verify <engagement>
python3 ~/.ai/it-role-house/fabric/fabric.py justify <engagement> --strict
python3 ~/.ai/it-role-house/fabric/fabric.py release <engagement> <fragment-id>
```

## Human-friendly and direct inspection

=== "Claude Code"

    ```text
    /fabric-report [engagement]
    ```

=== "Codex CLI"

    ```text
    $workflow-fabric-report [engagement]
    ```

Direct CLI:

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py status <engagement>
python3 ~/.ai/it-role-house/fabric/fabric.py verify <engagement>
python3 ~/.ai/it-role-house/fabric/fabric.py justify <engagement> --strict
python3 ~/.ai/it-role-house/fabric/fabric.py report <engagement>
python3 ~/.ai/it-role-house/fabric/fabric.py dossier <engagement> <escalation-id>
```

## Self-test

The shipped Fabric self-test contains **45 checks** covering typing, adjacency, review direction, evidence support, strict release, tamper detection, rework exhaustion, escalation direction, reformulation ownership/budgets, authority stickiness, context-digest mismatch, dependency invalidation and worst-case bounded termination.

Run it with:

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py selftest
```

## Explicit Prolog status

**The current AI IT House runtime does not execute Prolog.**

The paper's Prolog listings are a restricted symbolic model and orchestration specification. The shipped implementation uses deterministic Python state transitions, schemas and provider/runtime controls. This should be described as an implementation of selected architectural mechanisms, not as execution of the paper's illustrative Prolog program.

## Enforcement boundary

Fabric controls are meaningful only on paths that actually use them. Direct role/workflow invocation remains available outside a layered engagement. Deployments that require every consequential task to be Fabric-supervised must enforce that entry-routing rule separately.
