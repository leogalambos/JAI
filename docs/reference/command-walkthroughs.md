# Command walkthroughs and example outcomes

Owner: JAI maintainers · Last reviewed: 2026-10-16

Use this page to look up a single command's exercise and expected outputs. For a first end-to-end engagement, follow [How to use JAI](../examples/how-to-use-JAI/index.md): method, provider interaction, then a complete security, Android or commercial case. The examples below do not imply that every domain command automatically creates a six-layer Fabric engagement.

> **Example compatibility.** This detailed material originated in the 26.10.0 runtime handbook and is retained in the maintained Markdown documentation for its hands-on examples and technical references. AI IT House {{ JAI_VERSION }} has additional capabilities; treat the installed `GUIDE.md`, current `.ai/commands/` contracts, runtime tool `--help`, and versioned schemas as the authoritative behavior. Examples may require adaptation to the deployment context. These notes are not a separate release or documentation system.

## Reading the examples in Codex and Claude

The legacy examples use `/name` notation because they were written for Claude. In **Claude Code**, enter them as shown in the Claude conversation. In **Codex CLI**, invoke `$workflow-name` instead (`/analyse` → `$workflow-analyse`, `/review` → `$workflow-review`, `/layered` → `$workflow-layered`). A prompt/request shown here is not a Bash command. Behind the scenes the provider may call the matching survey, registry, Fabric or publication Python tool; you do not execute each script manually. Run such tools directly only for maintainer automation/diagnostics. **Codex human-authority events remain a deliberate exception** and require a separately executed human command. The older examples are retained for their content, not as a claim that every provider has identical approval interactions; refer to [Human authority](../operations/human-authority.md) and the [current installed guide](installed-cli-guide.md).

## commands : analyse


### /analyse

Use this exercise to practise describing an unfamiliar project without
turning analysis into a defect verdict. For syntax and command behavior,
use the [command reference](commands.md) and
[installed guide](installed-cli-guide.md).

**Try it.**

```
/analyse invoice-service
/analyse policy-docs
```

**What to expect.**

- *invoice-service:* a Python service of about 80 lines in
  `app/`, with API, arithmetic, storage and configuration
  modules; two tests, both on `invoices.total`; one pinned
  dependency; seven commits by two authors.
- *policy-docs:* seven Markdown documents, one index; one link
  that points nowhere; documents without an owner or with a passed review
  date; two identical documents.

**Check it worked.** You get a description, not a list
of defects. If it starts rating things, it has drifted into
`/review`.

## commands : criteria


### /criteria

Use this exercise to make a project-specific money-handling criterion
visible before review. For syntax and criteria precedence, use the
[command reference](commands.md) and
[installed guide](installed-cli-guide.md).

**Try it.**

```
/criteria invoice-service
```

Accept the offer to create the file. Then add a criterion of your
own, either by asking Claude ("add a criterion C9 on money handling:
amounts must be integer cents or Decimal, never float") or by editing
`invoice-service/.claude/review-criteria.md` yourself:

```
#### C9 Money handling
Monetary amounts are integer cents or Decimal, never binary floating point.
- High if money is computed or stored as float
```

**What to expect.** A file with eight criteria, C1
Correctness to C8 Source documentation, plus yours.

**Check it worked.** Run
`/criteria invoice-service` again: it now says the criteria
come from the project file, and lists C9. The next
`/review invoice-service` should report float money under
C9.

## commands : demo


### /demo

Set up, reset or check the demo projects for trying every command

`/demo <setup|list|reset PROJECT|check>`

**What it does.** Sets up, lists and restores the demo
projects, and checks that the library works.

**Syntax.**

```
/demo setup            copy the demo projects to ~/it-role-demo
/demo list             what each demo project is for
/demo reset <project>  put one project back to its starting state, to repeat a demo
/demo check            verify the demos and tools work, without using Claude's judgement (about ten seconds)
```

**Try it.** `/demo check`, then
`/demo setup`.

**What to expect.** `check` reports about a
dozen passes, ending "the demos are ready to use". `setup`
lists three folders under `~/it-role-demo`.

**Check it worked.**
`~/it-role-demo/invoice-service` exists and, if git is
installed, has five commits:
`git -C ~/it-role-demo/invoice-service log --oneline`.

## commands : develop


### /develop

Use this exercise to practise a bounded CSV-export change and its review.
For the current change workflow and command syntax, use the
[command reference](commands.md) and
[installed guide](installed-cli-guide.md).

**Try it.**

```
/develop add the CSV export of invoices that the invoice-service README promises, with tests
```

**What to expect.** A new branch with an export function
— documented with a docstring that states its parameters, result and
exceptions — tests for it, run and passing, because the hooks will not
let it finish otherwise — including an empty invoice list and a customer
name containing a comma — a review of the change, and a summary asking
you to merge.

**Check it worked.**
`git -C invoice-service branch` shows the new branch; the
tests pass on it.

## commands : diagnose


### /diagnose

Find the root cause of a defect before fixing it: last known good, a working analogue, and timing

`/diagnose <symptom, failing test or issue>`

**What it does.** Finds the root cause of a defect
*before* anything is fixed, through three comparisons that are
mandatory: against the **last known good** state, against a
**working analogue**, and against **timing**.
Then, if you agree, fixes it through the rework loop, with a regression
test written first.

**Syntax.**
`/diagnose <symptom, failing test or issue>` — and say,
if you know, when it last worked and where something similar works. Both
often save hours.

**What happens.**

1. Claude asks when it last worked and where something similar works,
   unless you have said.
2. The `defect-analyst` agent reproduces the defect as a
   command and runs it many times: does it fail every time, or only
   sometimes? An intermittent failure is itself evidence that timing or
   ordering take part.
3. The three comparisons:
   - **A. Last known good** — it bisects the history to the
     first commit at which the defect appears, in a separate git worktree, so
     your working tree is never touched; and lists everything else that
     changed — dependencies, configuration, infrastructure.
   - **B. Working analogue** — it diffs the failing code
     against code that works (a sibling function, another input or
     environment) and confirms which difference is decisive.
   - **C. Timing** — timeouts against measured durations,
     asynchronous work not awaited, ordering, clocks, schedules and expiry;
     it varies timing on purpose to see whether the defect follows.
4. It tests at least two competing hypotheses. `defect.py`
   then **validates the analysis**: no fix proceeds while a
   comparison is missing, a "not applicable" has no reason, timing is
   dismissed although the defect is intermittent, or no hypothesis is
   confirmed.
5. You see the report: the reproduction, the three comparisons, the
   hypotheses, the root cause with its location, trigger and contributing
   factors, and the proposed fix and regression test.
6. If you agree, `role-engineer` writes the regression test,
   sees it fail, fixes the root cause and runs the tests; the
   `defect-analyst` verifies.

**Try it.** In
`~/it-role-demo/invoice-service`, one at a time:

```
/diagnose An order of exactly 1000 EUR gets no discount, though the README promises 5% from 1000. It was right when the API was first written.
/diagnose Bob can delete Alice's invoice, although he cannot read it.
/diagnose test_charge_is_approved in tests/test_payments.py fails now and then.
```

Show what to expect — the answer key. Run the demo first.

**What to expect.**

| Defect | What the comparisons should find |
| --- | --- |
| the discount | **A:** it fails every time; bisecting from *Invoice creation, storage and API* finds the first bad commit, *Simplify discount calculation* (21 July 2026), which replaced a loop with `sum()` and quietly turned `>=` into `>`. **C:** not applicable — deterministic in every run, no clock or I/O. Root cause in `app/invoices.py`, `total`; regression test at 999.99, 1000 and 1000.01. |
| deleting another's invoice | **A:** not applicable — it never checked ownership. **B:** the working analogue is `get_invoice`, which checks `row[1] != user`; `delete_invoice` has no such check — the decisive difference. |
| the payment test | it fails in roughly a third of runs — **intermittent**, so timing cannot be dismissed. **C:** `GATEWAY_TIMEOUT_SECONDS = 0.1` against a gateway measured at up to 0.15 s; a timeout is reported as *declined*, so a slow approval becomes a refusal. The fix separates "no answer yet" from "declined" and sets the timeout from measured latency; the regression test uses a fake gateway with a controlled delay, so it fails *every* time on the old code. A longer timeout alone would only make the defect rarer — the standard does not accept that as a fix. |

**Check it worked.** The validated report is shown;
after the fix, `findings.py status defect-<date>` is
COMPLETE; for the payment defect,
`python3 ~/.ai/it-role-house/tools/defect.py repeat "<reproduction>" -n 30`
reports 0 failures.

## commands : fabric-report


### /fabric-report

Independent justifiability report on a traceability fabric

`/fabric-report <engagement> [product fragment]`

**What it does.** An independent check of a
`/layered` decision record: that it has not been tampered
with, that every step followed the rules, and which outcomes the record
actually justifies.

**Syntax.** `/fabric-report [engagement]` —
without a name, the newest record in `.fabric/`.

**Try it.** After the `/layered` demo:
`/fabric-report`

**What to expect.** Integrity confirmed; each result
marked as justified or not, with the reason when not; open items;
whether the final product is releasable.

---

## commands : govern


### /govern

Assess and propose the governance of a repository or document library

`/govern <path>`

**What it does.** Assesses how a repository or document
library is governed — ownership, change control, versioning, currency,
policy — from its files and git history, and proposes a governance model
sized to it. It changes nothing.

**Syntax.** `/govern <path>`

**Try it.**

```
/govern invoice-service
/govern policy-docs
```

Show what to expect — the answer key. Run the demo first.

**What to expect — invoice-service.** No CODEOWNERS, no
changelog, no version tags; a feature branch merged by its own author
two minutes after it was written; commits straight to `main`;
a key rotation at 23:41 that left the old key in the history; the README
names no owner. A proposal: owners, protected `main` with
required review, semantic versioning with a changelog, a secret-handling
rule.

**What to expect — policy-docs.** Ownership and review
dates incomplete and partly lapsed; no version or approval record for
policies; duplicates in circulation. A proposal: an owner and review
cycle per policy, an approval record, and a retirement rule.

**Check it worked.** Findings in a ledger, and a
proposed model you could adopt.

## commands : guide


### /guide

Show the user guide for this library, or the section for one command, with its demo

`/guide [command or topic]`

**What it does.** Shows this guide, or the section for
one command, and offers to run that command's demo.

**Syntax.** `/guide` ·
`/guide <command>` · `/guide <topic>`
(for example `/guide approvals`,
`/guide templates`).

**Try it.** `/guide rework`.

## commands : layered


### /layered

This command may govern creation using a named domain, or assess a new decision using an existing domain model. It does not replace domain methods or automatically reconstruct missing records of prior work. Name `sabsa-library` or `commercial-delivery` explicitly where relevant; see [the decision table and scenarios](../using/methodical-workflows.md).

Run a consequential task through the six-layer justifiable delivery method

`/layered <intent, stated as you would to an accountable team>`

**What it does.** Takes a consequential decision through
six layers of agents — intent, meaning, policy, design, realisation,
evidence — with requirements going down and evidence coming back up.
Unsupported work is sent back for rework, problems escalate layer by
layer to you, and every step is recorded so that you can later show why
the outcome was allowed. Use it when you will have to justify a
decision; not for routine changes.

**Syntax.**
`/layered <intent, stated as you would to an accountable team>`

**What happens.**

1. Your intent is recorded verbatim, and the decision log starts in
   `.fabric/` of the current folder.
2. Each layer turns the requirement from above into a precise contract
   for the layer below.
3. Results come back up and are reviewed by the layer that asked for
   them; nothing is built on unreviewed work.
4. When a layer cannot meet its requirement, the producer reworks the
   unchanged obligation, or returns it to its issuer for owner-controlled
   reformulation within budget. Escalations climb one layer at a time.
5. **When one reaches you**, the provider shows a decision packet built
   from the record: what was tried, the evidence and the options. You make
   the authority decision. In Codex, protected authority commands must be
   executed by the human in a trusted terminal; provider approval interactions
   must not be assumed equivalent.
6. Completion does not itself authorise release. Applicable justification,
   review and human-authority gates must be satisfied for the exact result.

**Try it.** In `~/it-role-demo` (expect 20–40
minutes; it is the most thorough command):

```
/layered Decide whether invoice-service is ready to be exposed to external partners. It must be secure enough for partner traffic and its money calculations must be exact.
```

**What to expect.** The evidence layer finds the
injection, authorisation and secret problems; the policy layer cannot
accept them; the question reaches you with options such as "fix before
exposure" or "expose a read-only subset" — each with its cost. Whatever
you choose is recorded, approved by you.

**Check it worked.** `/fabric-report` gives
an independent verdict on the record.

## commands : publish


### /publish

Publish a reviewed semantic artifact into enterprise-ready views without changing its approved claims.

**Syntax.** `/publish <semantic model> [archetype] [formats]`

1. Validate and fingerprint the semantic source.
2. Select the artifact contract, publication archetype and supported render targets.
3. Render HTML, DOCX, PPTX, XLSX and/or SVG from the same source.
4. Apply the Publication Gate after the Semantic Gate.
5. Preserve the semantic SHA-256 in generated outputs for traceability.

```
/publish architecture-review.json architecture-review-pack docx,pptx,html
```

**Self-test.** `python3 ~/.ai/it-role-house/tools/publication.py self-test`.

## commands : repository


### /repository

Maintain the scoped EA-domain projection repository, exchange ArchiMate models, generate governed views and control portfolio lifecycle.

**Syntax.** `/repository <init|validate|import|export|views|portfolio|impact|decommission> ...`

The JSON repository is authoritative only for the EA-domain projection; JAI owns global semantic identity. ArchiMate Open Exchange is an explicit interchange boundary. Stable IDs are preserved across views and exchange.

```
/repository validate architecture-repository.json
/repository views architecture-repository.json all
/repository portfolio architecture-repository.json
/repository export architecture-repository.json model.xml
```

Validation covers referential integrity, lifecycle state, portfolio links, view coverage and cross-project dependencies. Decommission is blocked while active dependencies remain unless a governed waiver exists.

**Self-test.** `python3 ~/.ai/it-role-house/tools/repository.py self-test`.

## commands : research


### /research

Research a problem to a decision, with experiments if needed

`/research <question>`

This exercise practises a bounded research decision. Use the
[command reference](commands.md) and [installed guide](installed-cli-guide.md)
for current syntax and the research contract.

**What happens.**

1. Claude agrees the question, the decision and a time-box with
   you.
2. `research-analyst` researches and cites primary
   sources.
3. If that does not settle it, `experiment-engineer` writes
   `experiments/<id>/PLAN.md` — hypothesis and success
   criteria — and Claude records its fingerprint **before**
   anything runs.
4. The experiment runs; `research-analyst`, not the
   engineer, assesses the result against the plan.
5. You get a recommendation, its confidence, and what remains unknown.
   At most three experiments per question.

**Try it.** In
`~/it-role-demo/invoice-service`:

```
/research Should invoice-service compute money with float, Decimal or integer cents? Settle it with a correctness test and a timing benchmark.
```

**What to expect.** Sources on floating-point
representation of money; an experiment showing float sums that drift
(for example 0.1 + 0.2), and the speed cost of Decimal against integer
cents; a recommendation of Decimal or integer cents, with the
trade-off.

**Check it worked.**
`experiments/<id>/PLAN.md`, `PLAN.sha256`,
`RESULTS.md` and `DECISION.md` exist, and the hash
still matches the plan:
`sha256sum -c experiments/<id>/PLAN.sha256`.

## commands : review


### /review

Review code, documents or a SABSA library against criteria fixed before reading, with located findings

`/review <path> [against <criteria or a criteria file>]`

Use this exercise to inspect located findings against fixed criteria.
For current syntax and reviewer boundaries, use the
[command reference](commands.md) and [installed guide](installed-cli-guide.md).

**What happens.**

1. Claude resolves the criteria (see review
   criteria) and **shows them to you with where they came from.
   It waits for your yes.**
2. The reviewer reads, samples deliberately, and records findings in
   `.findings/review-<date>.jsonl`.
3. You get the findings report: severity, location, criterion,
   recommendation.

**Try it.**

```
/review invoice-service
/review policy-docs
/review policy-docs against accuracy and consistency only
```

Show what to expect — the answer key. Run the demo first.

**What to expect — invoice-service.** The planted flaws,
by criterion:

| Criterion | Planted flaw | Where |
| --- | --- | --- |
| C2 Security | SQL injection: the customer name is formatted into the query | `app/storage.py`, `find_by_customer` |
| C2 Security | any user can delete any invoice: no ownership check | `app/api.py`, `delete_invoice` |
| C2 Security | any user can list another customer's invoices | `app/api.py`, `list_invoices` |
| C2 Security | a payment gateway key is hardcoded — and the previous key is still in the git history | `app/config.py`; commit `hotfix: rotate gateway key` |
| C1 Correctness | the 5% discount applies above 1000, but the README promises it *from* 1000 | `app/invoices.py`, `total` |
| C1 Correctness | division by zero for an invoice with no lines | `app/invoices.py`, `average_unit_price` |
| C1 Correctness *(or C9, if you added it)* | money computed as float | `app/invoices.py` |
| C5 Operability | a failure to save is swallowed, and the caller is told the invoice was created | `app/api.py`, `create_invoice` |
| C1 Correctness | a payment the gateway approves slowly is reported as declined: the client waits 0.1 s, the gateway can take 0.15 s — so its test fails only sometimes | `app/payments.py`, `charge` |
| C4 Tests | no tests at all for the API or the storage; `line_total` and `average_unit_price` never called by a test; no test at the discount boundary, for deletion or for authorisation | `app/api.py`, `app/storage.py`, `app/invoices.py`, `tests/` |
| C4 Tests | the storage talks to a database (SQLite) with no integration test against a real one | `app/storage.py` |
| C7 Supply chain | `requests==2.19.0` has a published vulnerability (CVE-2018-18074) | `requirements.txt` |
| C8 Source documentation | eleven public functions without a docstring, and one docstring that does not describe its parameter | `app/api.py`, `app/storage.py`, `app/invoices.py` |
| documentation | the README promises CSV export, which does not exist, and requires the long-unsupported Python 3.6 | `README.md` |

**What to expect — policy-docs.**

| Criterion | Planted flaw | Where |
| --- | --- | --- |
| C2 Consistency | minimum password length is 8 in one policy and 12 in another | `access-control.md`, `password-standard.md` |
| C2 Consistency | "2FA" and "MFA" for the same thing; "security event" used where "security incident" is defined | `access-control.md`, `incident-response.md`, `glossary.md` |
| C5 Navigation | the index links to a document that does not exist | `README.md` → `data-classification.md` |
| C5 Navigation | two H1 headings in one document | `incident-response.md` |
| C5 Navigation | a document nothing links to, and an identical copy of it | `remote-work.md`, `old-remote-work.md` |
| C6 Ownership and currency | no owner | `password-standard.md` |
| C6 Ownership and currency | review date has passed | `access-control.md` |
| C4 Completeness | an unfinished TODO in a published procedure | `incident-response.md` |

**Check it worked.** The report lists findings with
locations. The ledger exists:
`python3 ~/.ai/it-role-house/tools/findings.py status review-<date>`
(run in the project folder).

## commands : rework


### /rework

Fix the open findings of a review, with independent verification, until complete

`/rework [ledger]`

Use this exercise to follow repairs and separate verification through the
findings ledger. For current syntax and non-convergence handling, use the
[command reference](commands.md) and [installed guide](installed-cli-guide.md).

**What happens.**

1. For each open finding, the author for that kind of library fixes it:
   `role-engineer` for code, `docs-author` for
   documents, `sabsa-architect` for SABSA.
2. The reviewer — not the author — verifies each fix, and reopens any
   that is not right.
3. A finding reopened three times is **stuck**. Claude
   stops and shows it to you with its history. You decide: accept it as a
   risk (**an approval prompt**), have the reviewer withdraw
   it, or change the requirement.
4. It ends when the ledger reports COMPLETE.

**Try it.** After
`/review invoice-service`:

```
/rework
```

**What to expect.** Parameterised SQL, an ownership
check on delete and list, the key moved to an environment variable, the
discount boundary fixed with a test, a guard for empty invoices, the
swallowed exception surfaced, `requests` upgraded, a
docstring on every public function stating its contract, and tests: unit
tests for the API and the arithmetic, including the discount boundary,
deletion by a non-owner and an empty invoice, and an integration test
running the storage against a real SQLite database — which is what
proves the injection is gone. Claude cannot finish until those tests
exist and a test run after its last change has passed. The old key
remaining in git history cannot be fixed by editing files — expect it to
come back to you as a decision: rotate the key (a real-world action) and
accept the history, or rewrite the history.

**Check it worked.**
`findings.py status <ledger>` says COMPLETE, or lists
stuck findings for you; and the tests pass: in
`invoice-service`, `python -m pytest` (on Windows
`py -3 -m pytest`). If pytest is missing, install it first
with `python -m pip install pytest`.

## commands : commercial

### /commercial

Add the supplier commercial-delivery profile to opportunity, bid or delivery work.

**Syntax:** `/commercial <opportunity, bid or delivery scope>` in Claude Code;
`$workflow-commercial <opportunity, bid or delivery scope>` in Codex.
The remainder is a natural-language scope, not a set of lifecycle subcommands.

**Prerequisites.** Work in the target workspace. Identify the commercial owner,
available sources, existing engagement/canonical model, intended stage and
client/internal disclosure boundary. The coordinator routes expertise; it does
not sign a contract, grant a specialist authority or itself implement a change.

**Try it in Claude Code, one checkpoint at a time:**

```text
/commercial Qualify the managed integration service opportunity from the supplied sources. Reuse the existing engagement where present, identify the commercial owner, and prepare the discovery questions, explicit unknowns and bid/no-bid considerations.
```

After answering discovery questions, continue in ordinary conversation:

```text
Continue engagement <ID>. Incorporate the answers from <source>; develop the solution options, staged work packages, estimates, resource pyramid and commercial economics. Preserve evidence and estimation uncertainty, obtain independent review, and report the current snapshot.
```

Then request the output checkpoint:

```text
Continue engagement <ID>. Prepare separate internal and client proposal projections from the reviewed snapshot. Report required disclosures, unresolved pricing exposure and human decisions. Stop before issue or binding commitment.
```

If a justified bid-issue decision is required, start a distinct engagement:

```text
/layered Decide whether proposal snapshot <reference and digest> is ready to issue, using commercial-delivery. Independently assess its evidence, economics, disclosures and residual exposure; reserve commercial commitments for the human owner.
/fabric-report <decision-engagement-ID>
```

In Codex replace the slash commands with `$workflow-commercial`,
`$workflow-layered` and `$workflow-fabric-report`. Continuation is a
natural-language request against an existing ID, not an implemented `resume`
subcommand. For six-layer control of **creation itself**, start with
`/layered` or `$workflow-layered` and explicitly request `commercial-delivery`
instead of creating domain material first.

**What to expect.** Traceability from source passages and business needs to work
packages, estimate states, staffing, costs, price and subsequent forecasts;
separate internal/client outputs; independent review tied to the current
version; explicit uncertainty treatments and pending human acts. A benchmark
must retain its provenance and applicability rather than becoming an assumed
client fact. Actuals update forecasts without rewriting signed baselines.

**Check it worked.** Inspect actual object/snapshot IDs, calculation evidence,
review and findings records, disclosure checks and unresolved gates. Command
execution is not proof that every gate passed. Strict provider dispatch remains
blocked until deployment controls are qualified: the shipped Codex and Claude
capability records are `not_run`. See [Commercial delivery](../capabilities/commercial-delivery.md)
and [Choosing and running a methodical workflow](../using/methodical-workflows.md).

## commands : sabsa


### /sabsa

This is a domain workflow with architect/reviewer separation and its own
checks. It is not automatically a `/layered` engagement. A subsequent
`/layered` readiness decision is valid when scoped as a new decision; to
govern creation itself through L1–L6, start `/layered` with `sabsa-library`
explicitly named. See [the worked scenarios](../using/methodical-workflows.md).

Build a SABSA security architecture from client material, or update, review, improve or document one

`/sabsa <prepare|create|update ID|review|suggest|questions|approve|approval|document|template> [library path]`

**What it does.** Builds a SABSA security architecture
from material about a client or environment, and updates, reviews,
improves and documents it. The architecture is a library of small files
— elements and the 36 cells of the SABSA matrix — from which the
document is generated.

**Syntax.**

```
/sabsa prepare <library>        start from client material
/sabsa create <library>         derive the architecture in dependency order; complete all six questions per layer
/sabsa update <element> <library>
/sabsa review <library>         findings against the SABSA criteria
/sabsa suggest <library>        ranked gaps, each with the next step
/sabsa questions <library>      the open assumptions, as questions for the client
/sabsa approve <library>        owner-approve the exact clean snapshot
/sabsa approval <library>       verify the current snapshot still matches the approval
/sabsa document <library> [as docx]
/sabsa template <library>       which document template applies; set up the client's own
```

**What happens in prepare and create.**

1. The library is created, with `00-sources/` for material
   and `matrix/` for the 36 questions.
2. The client material goes into `00-sources/`. Public
   context the material implies — regulation for the sector, typical
   threats — is researched and saved there too, with citations.
3. Business drivers come first. Each cites the file and section it
   rests on, and says whether it is **stated** by the client,
   **inferred** from what they said, or
   **assumed**.
4. Build elements in dependency order: drivers → attributes → risks/opportunities → control objectives → domains → services → mechanisms → components → operations; then complete each layer's six questions. Settled cells carry provenance.
5. Review the structural and judgement gates. Domains trace through control objectives; operations define threshold actions. Final owner approval is hash-bound to the exact snapshot, and any later input change invalidates it.

**Try it.** In `~/it-role-demo`:

```
/sabsa prepare acme-pay/sabsa — the client material is in acme-pay/client-material
/sabsa create acme-pay/sabsa
/sabsa questions acme-pay/sabsa
/sabsa document acme-pay/sabsa
```

Then try a client's own format:

```
/sabsa document acme-pay/sabsa as docx
/sabsa template acme-pay/sabsa — copy the default so I can change the section titles
```

**What to expect.**

- *Drivers* such as doubling partner revenue through PSPs and
  partners demanding proof of controls, each citing
  `discovery-meeting-2026-10-01.md`.
- *Attributes* from the RFP: attributable privileged actions
  (R4), 99.9% availability (R7), credentials rotated within 90 days (R9) —
  each with a metric and a target.
- *Risks* such as the shared administrator account, and the
  static, manually issued partner API keys.
- *Assumptions* — and therefore questions for the client — such
  as whether ACME Pay is a regulated payment institution under PSD2,
  whether DORA applies, and data residency beyond eu-central-1.
- *The document:* thirteen sections; each of the six layers
  asks its six questions; DRAFT until all checks and warnings are clear, all 36 cells are settled and the current snapshot is owner-approved.

**Check it worked.**
`python3 ~/.ai/it-role-house/tools/sabsa.py check acme-pay/sabsa`
reports the structural state; `sabsa.py matrix acme-pay/sabsa` shows the 36 cells and how many are settled. A release-ready library also has zero warnings and `sabsa.py approval acme-pay/sabsa` reports `APPROVED`.
