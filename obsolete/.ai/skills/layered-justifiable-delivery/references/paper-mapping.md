# Mapping to the article

What is implemented, how, and where implementing it forced a decision *Towards Justifiable AI Systems*
(Galambos, 2026) leaves open. The observations are offered for the research programme the article opens,
not against it: most surfaced only because a self-test failed.

## Implemented as specified

| Article | Here |
| --- | --- |
| §5 fabric T = (N, τ, L, ρ, s): typed nodes/labels and eight ordered review states | `fabric.py` keeps the paper vocabulary and adds one implementation-only `att` node plus an `attempts` edge so failed external calls are first-class records |
| §5 well-typedness | rejected at insert time against `RHO` |
| §5 adjacency restriction, T4 | rejected at insert time; also structural: layer agents hold no `Agent` tool |
| Prop. 1, linear-time decision | memoised traversal; self-test decides 1,700 fragments in a 5,101-node fabric in < 0.1 s |
| Prop. 2, T5 — latest review is the highest layer's | `latest_review`; later lower-layer reviews recorded, ignored |
| Prop. 3, forward acyclicity | cycle check on every forward edge, and a DFS in `verify` |
| Prop. 4, generation indices on revision | enforced on `revises`; extended to rework (decision 7) |
| §6 six layers, adjacent communication only | six agents, one per layer, plus authority at L0 adjacent only to L1 |
| §8 review states | the eight states, plus `consolidate` for independent same-layer reviews |
| §9 layer cycle and agentic contract | `contract` (nine mandatory fields) and `render-contract`, which is the whole brief |
| §10 graded evidence confidence | four confidences; strict mode needs observed or deterministic evidence (decision 9) |
| §11 escalation climbs layer by layer; authority explicit | `escalate` moves strictly upward one layer per step; `authorise` only from L1 |
| §11 "a layer must escalate when it lacks authority" | `outside_authority` is sticky: never reformulated, never downgraded |
| §14 separation of generation, review, authorisation | layer k+1 produces, layer k reviews, a human decides |
| §14 context minimisation, T2, T7 | one rendered contract per dispatch into an isolated subagent context |
| T3b typed cross-layer communication; T8 opaque values | `ingest` accepts fixed keys only; text is stored, never interpreted |
| T6 single-model bias | adjacent layers alternate heavy and standard workload classes; provider-specific selectors are resolved independently and the validator rejects an invalid class assignment |
| A1 append-only, tamper-evident store | SHA-256 hash chain; `verify` detects edits, reorders and insertions |
| A2 authority identity | external human signs exact requests using Ed25519; protected schema-2 public trust binds signer and explicit capability; native provider approval is not Fabric authority |
| A3 model per call | `--model` recorded on every review |
| Appendix B minimal record | `report`, one row per fragment |

## Decisions the text leaves open

**1. Definition 2 does not contain the evidence requirement T1 relies on.** T1 says a fragment without
supporting evidence cannot be justifiable "by the supports edge requirement of Definition 2", but conditions
(i) and (ii) mention only the latest review and conflict resolution. As published, an `accepts` review with no
evidence yields a justifiable fragment. Strict mode adds the requirement. *Self-test: "'resonates' passes … but
strict mode rejects it".*

**2. The order of S makes `resonates` and `correlates` justifying.** Condition (i) is s(v̂(f)) ≻ insufficient,
and both sit above `insufficient`, yet §8 defines `resonates` as "not yet evidence" and `correlates` as "not
sufficient by itself". Strict mode requires `accepts` or `accepts_with_constraints`, and the latter must state
its constraints.

**3. Single-hop resolution in Definition 2(ii) against the adjacency restriction.** (ii) asks for edges
(c, escalates, x) and (x, resolved_by, a). With six layers and adjacency, a conflict raised at layer 6 cannot
reach an authority in one hop. `esc → esc` is added to ρ(escalates), and resolution is any authority decision
at the end of the relay chain — the multi-hop reading the §11 example describes.

**4. How qualified output moves upward.** Under adjacency a layer-6 fragment can only be reviewed by layer 5,
so "the highest layer that has reviewed f" is at most one above f, and something must carry qualified output
further. The paper reserves `consolidated_into` for use *within* a layer (Prop. 3's sketch), so this
implementation carries it upward with `supports` from an accepted lower fragment to the higher one — a reviewed
lower-layer product is evidence for the layer above, which matches §10's treatment of subordinate output as
evidential. `ingest` refuses to build on a fragment this layer has not accepted, and strict justifiability
composes down the chain. *An earlier pass used `consolidated_into` across layers; that works, but bends the
intra-layer reading of the label.*

**5. `supports` is in the forward set, but evidence comes from below.** Prop. 3's sketch signs every forward
label so its source is at or above its target, yet evidence originates in layer 6 and supports fragments above
it. Acyclicity is checked directly rather than derived from layer monotonicity.

**6. ρ as a function.** Figure 3 needs more than one source/target pair for several labels (derives from
intent and from requirement; may_create from evidence, fragment and review). ρ is implemented as a relation; each
admissible pair is listed in `RHO`.

**7. Rework is an unbounded loop unless it carries generations too.** Proposition 4 constrains authority
revisions, but the ordinary review loop — insufficient, rework, insufficient — has the same termination problem
and no authority node. Rework contracts carry their lineage; after three, the runtime raises a conflict and an
escalation itself. *Self-test: "Prop. 4 extended".*

**8. `requests` and `implements` on the same pair form a cycle.** Both labels are in L↓, so recording that a
contract requests a fragment *and* that the fragment implements the contract closes a 2-cycle, contradicting
Prop. 3. `requests` already carries the causal link, so the back-edge is not emitted. *Found when the runtime
rejected its own first ingest; now a regression test.*

**9. Evidence must be anchored by the runtime, not asserted by the agent.** The article's substrate anchors
generative reasoning in what "can be directly inspected or reproduced". If an evidence node is only an
agent-supplied excerpt, layer 6 can assert a measurement no artefact backs — the hallucination channel the
substrate exists to close. Deterministic evidence must name a file; `fabric.py` hashes it on recording,
`verify` re-hashes it, and drift blocks release. Separately, §10 says a subordinate AI output "is not a fact",
so strict mode needs observed or deterministic evidence somewhere beneath a fragment; AI-derived evidence alone
does not qualify. *Self-tests: "section 10 …", "evidence drift after recording blocks release".*

**10. Transformations must be atomic.** A Clark–Wilson transformation procedure either completes or does
nothing. In an append-only log, a message validated half-way leaves orphan nodes that can never be removed.
`ingest` validates the whole message before appending anything. *Found when a rejected message left a fragment
behind; now a regression test.*

**11. Where the product ends.** The article does not say which node is "the product". Here it is the layer-1
fragment answering the engagement requirement, accepted by a signed layer-0 review; `release` checks strict
justifiability, that acceptance, fabric integrity and evidence drift together.

**12. Termination needs a bound on every rung, not just on revision.** Proposition 4 makes revision
well-founded, but a working system has three loops the article does not separate: rework of one attempt,
reformulation of a requirement, and repeated rounds through the authority. Each is bounded independently —
three reworks per lineage, two reformulations per layer per round, forty contracts per round, one shared episode step budget, and an explicit
operator override beyond five rounds — and the runtime itself spends each bound by escalating, rather than
trusting the orchestrator to stop. *Self-test: an adversarial orchestrator that always fails and always takes
the most work-generating legal step reaches the operator in 112 autonomous steps; with the contract cap
removed, the reformulation budgets alone stop it in 190.*

**13. Escalation must be monotone, which adjacency alone does not give.** Adjacency permits an escalation to
move to the same layer or one below as easily as one above. The first implementation accepted L2 → L2 → L3 →
L2, a loop the adjacency check cannot see. Escalation edges now go strictly from layer k to k−1, a conflict
escalates first at its own layer, and an escalation can be consumed only once.

**14. Who may reformulate.** The article says a layer may "revise, create new requirements or escalate" but not
which layer may restate a failing requirement. Here it is the layer that **owns** it — the one whose contract
produced the failing work. A layer that received an infeasible contract can only pass it up: it cannot
reformulate what it was given. Budgets are shared per layer per round rather than reset per subtree, which keeps
the worst case roughly linear in depth instead of exponential.

**15. The operator's options must be records, not prose.** For an authority decision to be informed, the
operator needs examples of the failure and the alternatives seen so far. If those are written by a model at
escalation time, the operator cannot tell a recorded failure from a plausible paraphrase. Alternatives are
therefore recorded as they arise — a `proposal` is a product fragment of kind *reformulation*, matching the
article's "a recommendation produced by an agent is not an authority decision" — and `dossier` compiles the
packet mechanically from the fabric. A proposal adopted by the operator re-enters at L1 and is derived downward
again, so no layer is bypassed even by an authorised change.

## Not implemented

- The declarative agent language of §13. Claude Code subagents play the role of `ask` with per-agent memory
  keys; this skill and `fabric.py` play the orchestrator predicates. There is no Prolog runtime.
- Cross-provider model independence (A4). Only Claude models are available here, so T6 is mitigated by
  alternating Claude model families, which is weaker than the article's cross-provider setting.
- Delegated authority. Every authority act is human; no decision type can be delegated to a layer.
- Cryptographic proof of human presence. External Ed25519 receipts and protected
  capability-bearing trust provide local operator attestation, not enterprise
  identity or independent proof that a particular person was present. Native
  prompts, keypresses and agent-accessible secrets cannot grant Fabric authority.
- Adjudication of evidence-source honesty (A5) and adversarial robustness of the models themselves — out of
  scope in the article, and here.

## 3.3 runtime corrections after comparison with the final AIsystemy5 manuscript

The final September 2026 manuscript and its companion Prolog patterns were re-read against the 3.2 runtime.
That comparison exposed six implementation gaps which 3.3 closes:

**16. The episode budget was not actually shared.** 3.2 bounded contracts, rework and reformulation separately,
but a provider/tool retry, evidence collection or review could consume work without spending the contract cap.
3.3 adds `FABRIC_MAX_STEPS` (120 by default) across contracts, delegated attempts, evidence acquisition, reviews,
escalations and authority transitions. Budget exhaustion blocks autonomous continuation but deliberately cannot
block the escalation path to the operator. This is the operational analogue of the paper's bounded-episode
proposition.

**17. Failed external steps were not first-class records.** A timeout, unavailable collector or failed model
call could disappear between orchestration and the fabric or be flattened into an ordinary conflict. 3.3 adds
attempt (`att`) records and `fabric failure`. The states `failed`, `unavailable`, `timeout`, `ambiguous`,
`insufficient`, `contradicted` and `conflicting` remain distinct. The operator dossier can therefore show real
failed attempts instead of reconstructing them from prose.

**18. Rework could silently change meaning.** `--rework-of` previously allowed all nine contract fields to
change, so an orchestrator could call a reformulation a retry. In 3.3, rework must keep `what`, `why`, `evidence`
and `escalate_if` semantically identical and state the changed execution/collection approach in `--change`.
Changing meaning requires `reformulate` at the requirement-owning layer.

**19. Context minimisation lacked a runtime binding.** An isolated subagent context is useful but the resulting
record did not identify the exact packet it answered. `render-contract` now computes a canonical SHA-256 context
digest; 3.3 engagements require the agent result to echo it. `context-packet` exposes the exact machine-readable
packet. This cannot prove a provider injected no extra context, but it makes the intended dependency set explicit,
versioned and checkable instead of merely instructional.

**20. Adjacency did not fully encode direction.** `abs(layerA-layerB) <= 1` prevented jumps but still permits many
wrong-way adjacent edges. 3.3 enforces per-relation direction: requirements/contracts descend, support and review
ascend, escalations are monotone toward L1, and authority remains adjacent only to L1. The same policy is checked
on insertion and by `verify`.

**21. Dependency change did not force layered revalidation.** The SABSA repository had dependency invalidation,
but the per-engagement fabric did not. Current format 2 uses
`fabric invalidate ENG --changed REF --reason TEXT --request-out PLAN` to prepare
the same exact lifecycle plan used by replacement. It grants nothing and changes
no ledger bytes. Human signing with explicit `lifecycle-update` capability and
protected apply cancel affected conclusions, reviews, acceptance and permissions
across scopes. Fresh verification, independent review and new human acceptance
are required. Unsupported ledgers remain archives; no old acceptance is imported.

### Prolog substitution boundary

3.3 still does not embed a Prolog interpreter. Instead, the restricted `next_step/4` role is implemented as a
small deterministic policy kernel described by `runtime/fabric/supervision-policy.json` and enforced by
`fabric.py`. The file classifies retryable versus contradictory failures and declares the finite transition rules.
This preserves the important properties sought from the Prolog sketch—explicit states, inspectable rules, bounded
recovery, deterministic routing and failure as data—without claiming equivalence to arbitrary Prolog programs.
The LLM never decides its own retry count, escalation authority or release eligibility.
