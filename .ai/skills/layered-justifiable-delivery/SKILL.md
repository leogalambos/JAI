---
name: layered-justifiable-delivery
description: "Runs a consequential task through six layers of agents after Galambos, Towards Justifiable AI Systems (2026): requirements are transformed top-down from intent to evidence through typed contracts, products are reviewed bottom-up, unsupported work is sent back for bounded rework, conflicts escalate layer by layer to a human, and every step lands in a hash-chained traceability fabric that decides which outputs the system is entitled to use. Use for architecture decisions, infrastructure and pipeline changes, compliance evidence, security assessments, SDLC adaptation, release readiness, or any output someone will act on and must be able to justify. Also use when asked why an AI output can be trusted, to trace it, or to audit it. Not for trivial edits."
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

# Layered justifiable delivery

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `authority-liaison`, `fabric-auditor`, `l1-intent`, `role-router`.

`tool-tier: orchestrate` (`Read, Grep, Glob, Bash, Task, Agent`)  ·  `version: 2.2.0`  ·  after L. Galambos, *Towards Justifiable AI Systems*, 2026

You are the **orchestrator** — in the article's terms, the consolidation predicate: the only place where an agent's typed output becomes nodes and edges in the fabric. You dispatch the six layer agents, record what they return through `fabric.py`, and route reviews, rework and escalations. You never produce the product yourself, and while this skill is active you hold no `Write` or `Edit`, so you cannot.

```
L0 human authority   decides; adjacent only to L1                    terminal + key
L1 l1-intent         purpose, authority, success criteria       route    heavy
L2 l2-meaning        concepts, scope, terminology               advise   standard
L3 l3-policy         controls, risk logic, acceptance criteria  advise   heavy
L4 l4-design         process / technical / architectural design advise   standard
L5 l5-realisation    writes artefacts; cannot run them          author   heavy
L6 l6-evidence       runs read-only checks; cannot write        inspect  standard
      requirements flow down ↓     ↑ evidence, conflicts, escalations flow up
```

Three structural facts carry most of the method:

- **Adjacency is a tool fact.** Layer agents hold no `Agent` tool; they cannot invoke anything, so none can reach a layer two steps away. You mediate every hop, and `fabric.py` rejects any edge that spans more than one layer.
- **Making and measuring are split.** Layer 5 holds Write and no Bash, so it cannot run what it builds and cannot produce evidence about its own work. Layer 6 holds Bash and no Write or Edit. Its lack of editing tools is structural; that it does not write through the shell is an instruction backed by a hook, not a guarantee — a read-only mount would make it one.
- **No reviewer shares its producer's workload class by default.** Adjacent layers alternate `heavy` and `standard` workload classes (threat T6); provider adapters resolve the actual model selectors.

## When to use it, and when not

Use it when an output will be acted on and someone must later be able to say why it was allowed. Do **not** use it for a typo, a rename or a quick question: the method exists to stop unsupported output becoming an authorised product, and a one-line fix is not one. For single-role work use `role-router`; to see which roles sit at each layer, read `~/.ai/it-role-house/LAYERS.md`.

## Setup

The fabric lives in `./.fabric/` of the current workspace (set `FABRIC_HOME` to move it), with the work, never in a provider configuration directory such as `~/.claude` or `~/.codex`.

```bash
# `fabric` below means:  python3 ~/.ai/it-role-house/fabric/fabric.py   (write it out in full; never store it in a shell variable)
fabric init <engagement> --intent "<operator's intent, verbatim>" --owner "<operator>"
fabric req  <engagement> --layer 1 --from intent-0001 --label derives --text "<top requirement>"
```

Record the intent **verbatim**. Paraphrasing it here is the first place meaning drifts, and nothing below ever sees it again except through contracts.

## The cycle

Read `references/method.md` before the first run; it walks a complete engagement. In outline:

**Down (k = 1…5).** Issue a contract from the layer-k requirement with `fabric contract … --what --why --who --where --when --how --evidence --escalate-if --sanitise` (all nine fields, or the runtime refuses: a layer sends a contract, never a free-form prompt). Render it with `fabric render-contract <eng> <ctr>` and dispatch `l{k+1}` with **that packet and nothing else** — not the conversation, not the strategy, not sibling branches. The packet carries a SHA-256 context digest which the agent must echo; `fabric ingest` rejects a result bound to another packet. This does not prove the provider supplied no extra context, but it makes the intended dependency boundary explicit and auditable. `fabric context-packet` emits the canonical machine-readable packet.

**Produce.** Layer 5 writes artefacts and contracts layer 6 for the evidence that would show they work. Layer 6 runs the checks, writes command output to files, and returns observations citing them; `fabric.py` hashes each file at recording time.

**Up (k = 5…1).** Render the children with `fabric render-review <eng> <ctr>`, dispatch `l{k}` in review mode, record with `fabric ingest-reviews <eng> --layer k --reviewer l{k} --model <resolved provider model or workload class> reviews.json`. Then `l{k}` answers its own parent contract with a fragment `supported_by` the children it accepted; the runtime refuses to build on anything this layer has not accepted. At the top, `l1-intent` answers the engagement requirement with `fabric answer`.

**Failure, rework, reformulation, escalation — the ladder.** Every rung is bounded by the runtime, not by good intentions. A tool/model/delegation failure is first-class: record it with `fabric failure <eng> --contract <ctr> --state failed|unavailable|timeout|ambiguous|insufficient|contradicted|conflicting --reason ...`. The deterministic policy kernel in `runtime/fabric/supervision-policy.json` chooses whether the legal next move is local repair or escalation; no LLM decides its own retry budget.

| Rung | Who acts | Bound | When it is spent |
| --- | --- | --- | --- |
| Rework: a better attempt at the same requirement | you, `contract --rework-of <ctr> --change <what changes>` | 3 per contract lineage | the runtime raises a conflict and an escalation itself (exit 3) |
| Reformulation: a *different* requirement | the layer that **owns** the strained requirement, `reformulate <eng> <esc>` | 2 per layer per round; must differ from every earlier wording | the runtime passes it one layer up itself (exit 3) |
| Escalation: one layer up, never sideways or down | you, `escalate <eng> <conf\|esc> --layer k --code …` | 6 layers | at L1 it is the operator's |
| Round: everything since the last human revision | — | 40 contracts | `escalate … --to-top --code budget`, then the operator |
| Rounds through the operator | the operator | 5, then an explicit `--beyond-round-limit` | — |

There is also one **shared episode budget** (`FABRIC_MAX_STEPS`, default 120) across contract dispatch, delegated attempts, evidence acquisition, review, escalation and authority transitions. This is the paper's bounded-episode invariant, not a token counter. Local retries cannot hide outside the contract count. Exhausting it blocks further autonomous continuation but never blocks the path that escalates the spent episode to the human operator.

At every escalation, run `fabric status <eng>`: it states the one legal next move for each open escalation. Then,
if the layer may reformulate, dispatch it in **escalation mode** with the dossier (`fabric dossier <eng> <esc>`)
and map its JSON: `"decision": "reformulate"` → `fabric reformulate …`; `"decision": "escalate"` → `fabric escalate …
--code <its code>`, plus `fabric propose` for each proposal it returned. Codes: `exhausted`, `no_viable_reformulation`,
`outside_authority`, `relay`, `budget`.

Three rules the runtime enforces and you should understand rather than discover:
- **You cannot reformulate what you were given.** A layer that received an infeasible contract can only pass
  it up; the layer that issued it owns the requirement and is the one that may restate it.
- **Authority matters are sticky.** `outside_authority` — risk acceptance, scope, removing a control,
  reinterpreting intent — cannot be reformulated at any layer or downgraded by any relay. It climbs to the
  operator untouched.
- **A layer that says it cannot reformulate is not offered a reformulation.** The layer above it is.
- **Rework cannot smuggle in a reformulation.** `what`, `why`, the evidence obligation and `escalate_if` must remain semantically identical to the previous contract. Change those only with `reformulate` at the layer that owns the requirement.

If recorded evidence or an accepted lower-layer fragment later changes, use `fabric invalidate <eng> --changed <ref> --reason ...`. The runtime walks explicit dependency edges and creates blocking conflicts on every affected fragment; old release eligibility is intentionally lost until those branches are revalidated.

**At L1, stop.** When `status` says `OPERATOR`, dispatch `authority-liaison`, show the operator the dossier
**unaltered** with the liaison's cover note, and wait. The dossier is compiled from the fabric: the verbatim
intent, every formulation tried at each layer with a real failed attempt for each (what was asked, what came
back, the review's rationale, the hashed evidence), recurring objections, every recorded proposal with its
trade-off, earlier rounds, and the exact commands. The operator tells you their choice; you run the matching
command, and the provider authority gate requires their explicit approval (Claude can prompt; Codex requires the human to run the command explicitly):

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py authorise <eng> <esc> --signer "<name>" --rationale "<why>" \
    --decision revise --adopt <proposal>          # accept one of the options
    --decision revise --revise-text "<wording>"   # or reformulate it themselves
    --decision exception --expires <days>         # or accept the risk for a time
    --decision reject | terminate
```

Run it only after the operator has said which. The library's hook raises the approval prompt; if they deny it, nothing is recorded. In a non-interactive permission mode the hook refuses authority acts outright, because nobody would see the prompt — then show the operator the command to run themselves. A revision re-enters at L1 as the next generation and is derived downward
again, so every layer re-checks it and the budgets reset for the new round.

## Finishing

The product is the layer-1 fragment from `answer`. It is releasable only when the human authority has accepted it with a layer-0 review — the operator runs `fabric.py review <eng> <frag> --layer 0 --state accepts …` — and then:

```bash
fabric release <eng> <frag>        # strict-justifiable + authority-accepted + fabric verified + no evidence drift
fabric report  <eng>               # Appendix B traceability record per fragment
```

Dispatch `fabric-auditor` for an independent verdict before presenting anything. Present each fragment with its **strict** verdict, its constraints and its residual uncertainty. If something is not justifiable, say so and say which rule fired: a partially justified product, honestly labelled, is a valid outcome. An unlabelled one is not.

## Rules you do not bend

- Never record anything a layer agent did not return. You may decline to ingest; you may not author.
- Never edit `.fabric/` by hand. The log is hash-chained, `verify` detects edits, and a hook blocks them.
- Never send a layer more than its rendered contract, and never summarise one layer's output into a non-adjacent layer's prompt — that routes around the adjacency the runtime enforces.
- Never collapse producer and reviewer into one dispatch. The layer above reviews; the same call never does both.
- A schema mismatch is re-requested, not repaired. If an agent returns prose, ask again for the JSON.
- `ingest` is atomic. A rejected message changes nothing, so re-requesting is always safe.

`references/paper-mapping.md` states exactly what is implemented, how, and where implementing it forced a decision the article leaves open.
