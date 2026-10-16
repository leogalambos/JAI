# Human authority and escalation

AI IT House treats **Human Authority (L0)** as an external decision boundary. It is not another agent and not a seventh JAI layer.

The authority model states the rule directly: JAI agents may prepare, review, recommend and record, but they cannot synthesize L0 authority.

## What the human does in Claude/Codex

**Operator workflow:** request the consequential work with `/layered` (Claude) or `$workflow-layered` (Codex), inspect the escalation dossier delivered in the conversation, and specify one of the five supported decisions below with its scope/rationale. This is a **decision**, not consent for the assistant to invent a signer or bypass a tool restriction.

**Claude interactive mode:** an authority operation can be put through the managed provider permission prompt (`ask`), where the human inspects the complete proposed command and approves or denies it. If an interactive prompt is unavailable, the operation is denied.

**Codex CLI:** the agent **must not** execute the L0 operation itself: the managed guard refuses it because this provider path cannot generate the required trusted interactive approval. Ask Codex to display the exact command and dossier, then **run that command yourself in a separate trusted system terminal** after verifying signer, decision, record IDs, rationale, scope and expiry. Return to Codex and request a fresh `/fabric-report`-equivalent (`$workflow-fabric-report`) to verify that the authority record and release state actually changed. Typing "approved" in chat is not itself an authority event.

The same principle applies to final L0 acceptance of a product: do not interpret a favourable review or a chat acknowledgement as a recorded authority act. If no supported trusted human action is available, stop with an explicit pending-authority status.

## When work reaches L0

An escalation eventually requires the operator when one or more of these conditions apply:

- an authority matter such as risk acceptance, scope change, removal of a mandatory control or reinterpretation of intent;
- the responsible JAI layer cannot find a viable reformulation;
- the reformulation or shared episode budget is exhausted;
- a round reaches its autonomous termination condition;
- a final consequential product requires authority acceptance before release.

The system preserves the escalation chain. A lower-layer authority problem cannot be converted into an ordinary technical issue by relaying it upward.

## Decision dossier

Before a human decision, **the orchestrating agent normally generates** the dossier (or a maintainer can reproduce it using the read-only runtime API):

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py dossier <engagement> <escalation-id>
```

The dossier is mechanically compiled from the fabric and should expose:

- original operator intent;
- requirement/contract lineage;
- failed attempts and their states;
- evidence and review rationale;
- unresolved conflict;
- proposals and their trade-offs;
- the exact authority action available to the operator.

`authority-liaison` may prepare a cover note and make the dossier easier to read. It cannot decide.

## Authority decisions

The `authorise` command supports:

| Decision | Meaning |
| --- | --- |
| `accept` | accept the authority decision within its bound scope |
| `exception` | permit a constrained exception, normally with rationale and expiry |
| `revise` | require a revised L1 generation and a new round |
| `reject` | refuse the proposal/use |
| `terminate` | end the engagement without further autonomous work |

Example **protected human authority action** (not a general-purpose command for the agent to run; in Codex it is executed by the human in a separate trusted terminal):

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py authorise sdlc esc-0003 \
  --decision exception \
  --signer "J. Novak, risk owner" \
  --expires 90 \
  --rationale "Manual review for critical applications until SCA is procured"
```

**Final product acceptance is distinct from an escalation decision.** The Fabric also has an L0 product-review operation. If a final product requires human acceptance, the actual decision owner reviews the specific fragment and the provider must not fabricate that review. The following is an illustrative **human-controlled** API call (real IDs and decision must be taken from the verified dossier; the authority guard must permit the authenticated human path):

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py review <engagement> <fragment-id> \
  --layer 0 --state accepts --reviewer "<actual human approver>" \
  --model human --rationale "<decision basis and accepted constraints>"
```

In Codex, the human performs this protected action separately; Claude may prompt through the trusted interactive mechanism. **Neither a natural-language approval in chat nor a Fabric self-test records this acceptance.** Confirm the new record and strict release eligibility afterwards.

A `revise` decision does not edit history. It creates a new L1 requirement generation and starts a new round while retaining the earlier attempts, evidence, reviews and authority record.

## Provider behavior

### Claude Code

The managed authority hook can return `ask` for an authority command in normal interactive permission mode. The operator sees the proposed authority action and may approve or deny it.

In non-interactive permission modes where an approval prompt would not reliably be shown, the hook fails closed instead of silently allowing the authority act.

### Codex

The corresponding PreToolUse path cannot elevate an authority command into an interactive approval prompt. The hook therefore denies the attempted authority command and instructs the human to run it manually.

This difference is intentional: provider convenience must not become authority impersonation.

## Protected records

The authority hook also protects:

- `.fabric/` logs;
- `.findings/` ledgers;
- the Fabric authority key under `~/.config/justifiable-fabric/`.

Ordinary file-write tools are denied for protected Fabric/findings records. They are expected to be changed only through the controlling runtime tools.

## Important security boundary

`guard_authority.py` explicitly describes itself as a **string-level guard**. It protects the ordinary provider/tool path and makes bypass deliberate, but it is not a complete operating-system sandbox against a determined adversary with unrestricted shell access.

For higher-assurance deployments combine it with host-level controls such as:

- least-privilege service identities;
- read-only mounts for evidence-only execution roles;
- sandboxed execution;
- restricted shells/commands;
- network allowlists;
- centrally managed provider/tool policy;
- audit collection independent of the model session.

## Human authority is not a truth oracle

A person may accept a stated residual risk or approve a bounded use. That act does not prove the technical premises are true. Evidence, qualification and authority are separate responsibilities.

The operator interface should therefore foreground blockers, missing evidence, dissent and consequences rather than show only a polished recommendation.

## Operational metrics

A healthy human-oversight process monitors at least:

- number and age of open escalations;
- percentage of escalations caused by evidence gaps versus authority boundaries;
- operator decision latency;
- expired exceptions;
- revisited/revised decisions;
- repeated escalations caused by the same policy or requirement;
- escalation queue growth and backpressure.

A queue that never resolves is not successful human oversight simply because no unsafe release occurred.
