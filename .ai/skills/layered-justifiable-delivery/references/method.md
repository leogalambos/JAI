# Method: one complete engagement

A worked run of the paper's Case 1 — adapting a generic secure SDLC library to a client that has CI/CD but no
dependency-scanning (SCA) tool. Every command is real; the IDs are what the runtime prints.

```bash
# `fabric` below means:  python3 ~/.ai/it-role-house/fabric/fabric.py   (write it out in full; never store it in a shell variable)
```

## 1. Intent and the top requirement

```bash
fabric init sdlc --intent "Adapt the secure SDLC library to what the client can actually operate" --owner "CISO"
fabric req  sdlc --layer 1 --from intent-0001 --label derives --text "Keep open-source dependency risk controlled"
```

## 2. Down: a contract per layer

```bash
fabric contract sdlc --from req-0001 \
   --what "Interpret library terms in client vocabulary" --why "Adaptation must preserve risk objectives" \
   --who "AppSec, platform team" --where "GitLab CI estate" --when "Before the Q4 release train" \
   --how "Map terms; never delete a control" --evidence "Tool inventory export" \
   --escalate-if "Any control would be removed or weakened" --sanitise "No client strategy, no personal data"
fabric render-contract sdlc ctr-0001          # this exact text is the whole brief for l2-meaning
```

Dispatch `l2-meaning` with the rendered text only. It returns JSON; record it:

```bash
fabric ingest sdlc --contract ctr-0001 l2-reply.json
# req-0002  derived requirement  L2  ->  ctr-0002  contract for L3
```

Repeat downward: render `ctr-0002`, dispatch `l3-policy`, ingest; and so on to layer 6.

## 3. The substrate pushes back

`l6-evidence` runs the inventory query, writes the output to `scratch/tools.txt`, and returns:

```json
{"fragments": [{"key": "f1", "text": "CI/CD present (GitLab 17.2); no SCA tool in inventory", "kind": "finding"}],
 "evidence":  [{"supports": ["f1"], "source": "CMDB export", "confidence": "deterministic", "file": "scratch/tools.txt"}]}
```

`fabric.py` hashes `scratch/tools.txt` as it records it. If that file later changes, `release` refuses.

## 4. Up: review, then build only on what was accepted

```bash
fabric render-review sdlc ctr-0005                     # l5-realisation reviews what L6 returned
fabric ingest-reviews sdlc --layer 5 --reviewer l5-realisation --model heavy reviews.json
```

At layer 3 the conflict becomes explicit. `l3-policy` cannot delete the SCA control: it accepts the finding,
records a conflict (risk persists without SCA), and derives a compensating-control requirement — manual review
for critical applications — rather than silently adapting.

```bash
fabric conflict sdlc --from frag-0004 --layer 3 --text "SCA control cannot be met; dependency risk persists"
```

A layer may answer its parent contract only with fragments `supported_by` children it accepted; the runtime
refuses anything else, and refuses atomically, so the log is unchanged and the request can simply be retried.

## 5. Rework, then reformulation, both bounded

If `l4-design` returns a design `l3-policy` reviews as `insufficient`, l3 states the change and you issue
`fabric contract … --rework-of ctr-0004`. A fourth rework of the same lineage is not issued: the runtime raises a
conflict and an escalation at l3 itself and exits 3. Non-convergence is information, not a reason to try harder.

l3 owns the strained requirement, so it gets the next rung. Dispatch it in escalation mode with the dossier; if
it returns a reformulation, record it:

```bash
fabric reformulate sdlc esc-0001 --text "<restated requirement>" --change "<what differs and why>" \
   --what … --why … --who … --where … --when … --how … --evidence … --escalate-if … --sanitise …
```

A layer has two reformulations per round. The third attempt is refused and the runtime escalates one layer up by
itself, exiting 3. If l3 says it has no viable reformulation, record that with `--code no_viable_reformulation`
and pass it up; l2 may then reformulate *its* requirement.

## 6. Escalation, one layer at a time

Removing a mandatory control is not something any layer may decide, so l3 escalates it as an authority matter.
That status survives every relay, and no layer above may reformulate or downgrade it:

```bash
fabric escalate sdlc conf-0001 --layer 3 --code outside_authority --reason "removing a mandatory control needs risk acceptance"
fabric escalate sdlc esc-0001  --layer 2 --code relay --reason "relay"
fabric escalate sdlc esc-0002  --layer 1 --code relay --reason "relay to intent"      # ready for the operator
fabric status sdlc                                                                   # next: OPERATOR
fabric dossier sdlc esc-0003 > dossier.md
```

Escalations move strictly upward; the runtime refuses sideways and downward hops. Authority sits above layer 1
and is adjacent only to it. Dispatch `authority-liaison`, show the operator the dossier unaltered with the
liaison's cover note, and stop. When the operator has chosen, run their choice — the provider authority gate requires their explicit approval (Claude can prompt; Codex requires explicit human execution):

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py authorise sdlc esc-0003 --decision exception \
    --signer "J. Novak, risk owner" --expires 90 --rationale "Manual review for critical apps until SCA is procured"
```

## 7. The product, and the release gate

`l1-intent` answers the top requirement from the layer-2 fragments it accepted:

```bash
fabric answer sdlc --requirement req-0001 --text "Adapted SDLC: 41 controls mapped, 1 under time-bound exception" \
   --supported-by frag-0011
```

The operator accepts it (`review … --layer 0 --state accepts`, interactive). Then:

```bash
fabric release sdlc frag-0012      # RELEASABLE only if strict-justified, accepted, verified, no evidence drift
fabric report  sdlc > traceability.md
```

## Review states and what they lead to

| State | Paper mode (Def. 2) | Strict mode | Usual next step |
| --- | --- | --- | --- |
| `accepts` | justifying | justifying | build upward on it |
| `accepts_with_constraints` | justifying | justifying, constraints required | build upward, carry the constraints |
| `correlates` | justifying | not justifying | rework for direct support |
| `resonates` | justifying | not justifying | rework: obtain evidence |
| `insufficient` | not | not | rework |
| `out_of_scope` | not | not | drop or rescope |
| `conflicts` | not | not | conflict, then escalate or rework |
| `escalate` | not | not | escalate |

Use strict mode for anything released. Paper mode exists so the published definition can be checked as written.

## 8. Failed calls are records, not invisible retries (3.3)

If a model call, tool call or evidence collector fails before it can return the typed JSON above, record the
attempt before doing anything else:

```bash
fabric failure sdlc --contract ctr-0004 --state timeout \
  --actor l4-design --model '<active model>' --reason 'provider request timed out after the configured deadline'
```

For `failed`, `unavailable`, `timeout`, `ambiguous` and `insufficient`, the policy kernel requests a local repair
while rework and shared episode budget remain. Do not call the same provider again invisibly. Create a rework
contract and say what operational approach changes:

```bash
fabric contract sdlc --from req-0004 --rework-of ctr-0004 --change 'use the cached inventory export rather than the live API' \
  --what '<identical what>' --why '<identical why>' --who '...' --where '...' --when '...' --how '...' \
  --evidence '<identical evidence obligation>' --escalate-if '<identical escalation condition>' --sanitise '...'
```

After the local repair budget is spent, the runtime turns non-convergence into a conflict/escalation. Only after
that bounded ladder reaches L1 does the operator receive the dossier. `contradicted` or `conflicting` observations
skip blind retry and enter the escalation/reformulation ladder immediately.

Every 3.3 contract rendering includes `CONTEXT SHA256 ...`; return that value as `context_digest`. Use
`fabric context-packet ENG CTR` when an adapter needs the canonical JSON packet rather than the human-readable
rendering.

When a dependency later changes:

```bash
fabric invalidate sdlc --changed evd-0007 --reason 'inventory export superseded by a new snapshot'
```

Every dependent fragment gets a blocking conflict. Re-run only the affected branch; do not regenerate the whole
engagement unless the changed dependency reaches the top-level requirement.
