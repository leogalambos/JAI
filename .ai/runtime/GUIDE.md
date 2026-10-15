# AI IT House — installed CLI guide

This guide explains the workflows exposed by the library to Claude Code
and Codex CLI, with demos you can run in a few minutes. In Claude Code
use `/guide`; in Codex use `$workflow-guide` (for example review, SABSA
or demo topics).

**Contents**

0. [Operator versus runtime](#operator-versus-runtime-read-this-first)
1. [Before you start](#1-before-you-start)
2. [A 20-minute tour](#2-a-20-minute-tour)
3. [Commands](#3-commands) —
[/demo](#demo) · [/guide](#guide) · [/analyse](#analyse) ·
[/criteria](#criteria) · [/review](#review) · [/rework](#rework) ·
[/diagnose](#diagnose) · [/develop](#develop) · [/govern](#govern) ·
[/research](#research) · [/sabsa](#sabsa) · [/publish](#publish) ·
[/repository](#repository) · [/layered](#layered) ·
[/fabric-report](#fabric-report)
4. [Concepts](#4-concepts)
5. [Direct tools for maintainers](#5-direct-tools-for-maintainers)
6. [Troubleshooting](#6-troubleshooting)

---

## Operator versus runtime: read this first

- **User interface:** type `/command` in **Claude Code** or
  `$workflow-command` in **Codex CLI**, with your task in the provider
  conversation. You do **not** manually start `fabric.py`, `sabsa.py`,
  `publication.py` or any layer agent as a condition of using the
  workflow.
- **Behind the scenes:** the native command/skill instructs the provider
  to route roles and issue permitted runtime tool calls. Python scripts
  implement typed state transitions, survey/validation, publication and
  evidence capture. The orchestrator is model-driven; availability of a
  script does **not** establish that it was executed in a given run.
- **Your approvals:** risk acceptance, scope/mandatory-control
  exceptions, approval and protected releases remain organisational
  authority actions. Claude can use an interactive managed approval
  prompt where supported. In Codex the agent is **denied** permission to
  execute protected L0 authority commands; it must show you the dossier
  and exact command, which **you** execute in a separate trusted
  terminal.
- **Verification:** ask for artifact and evidence IDs, actual test
  status, blockers and review state. `/fabric-report` /
  `$workflow-fabric-report` is an audit interface, **not** an implicit
  release or approval.

These rules also apply to the examples below: the *Try it* snippets show
**provider conversation** input; direct Python code in *Check it worked*
or the final tools section is **optional developer/maintainer
diagnostics**, not an extra task imposed on the operator. For the full
execution sequence, consult `docs/using/layered-engagement.md` and
`docs/operations/human-authority.md` in the source-controlled manual or
published website. These pages are not expected to exist in the compact
installed offline runtime.

---

## 1. Before you start

1. **Install** the package (`install.cmd` on Windows, `bash install.sh`
elsewhere) and **start a new Claude Code or Codex CLI session**. Nothing
else needs setting up.
2. **Create the demo projects:** in Claude Code use `/demo setup`; in
Codex invoke `$workflow-demo` with `setup`. They are copied to
`~/it-role-demo/` (on Windows, `C:\Users\<you>\it-role-demo\`):

   | Project | What it is | Use it with |
   | --- | --- | --- |
   | `invoice-service` | A small Python billing service, with a short git history and deliberate flaws | `/analyse` · `/criteria` · `/review` · `/rework` · `/develop` · `/govern` · `/research` · `/layered` |
   | `policy-docs` | A security policy library with deliberate flaws | `/analyse` · `/review` · `/rework` · `/govern` |
   | `acme-pay` | Notes and an RFP extract about a fictional potential client | `/sabsa` |

3. **Open your AI CLI in `~/it-role-demo`** (`cd ~/it-role-demo`, then
start `claude` or `codex`), so that the paths below work as written.
Anywhere else, give full paths.

**How to read the demos.** Each command's *Try it* gives you the exact
text to type. *What to expect* describes a good result. For the review
demos it also lists the flaws that were planted — the answer key. The
reviewers never see this guide, so if they find the flaws, they found
them in the code. A good review finds most of them, and may find others;
a review that misses the high-severity ones is worth reporting.

**Two things you will see often.**
- *Approval prompts.* Some acts are yours alone: accepting a finding as
a risk instead of fixing it, granting an exception, accepting a product.
Claude can ask you to approve the exact command; Codex deliberately
blocks it and requires you to run the authority command yourself. Read
the command before approving or executing it.
- *Confirmation before work starts.* Reviews show you their criteria and
wait for your yes. That is deliberate: criteria chosen after reading
cannot be defended.

---

## 2. A 20-minute tour

The shortest path through the main ideas, all on the demo projects:

| Step | Type | What you learn |
| --- | --- | --- |
| 1 | `/demo setup` | the demo projects appear in `~/it-role-demo` |
| 2 | `/analyse invoice-service` | the library understands a codebase before judging it |
| 3 | `/criteria invoice-service` | review criteria are a file you own and edit |
| 4 | `/review invoice-service` | located findings, recorded in a ledger |
| 5 | `/rework` | fixes by one agent, verified by another, until complete |
| 6 | `/review policy-docs` | the same discipline for documents |
| 7 | `/diagnose test_charge_is_approved fails now and then` *(in `invoice-service`)* | a defect analysed before it is fixed: last known good, a working analogue, timing |
| 8 | `/sabsa questions acme-pay/sabsa` *(after a short `/sabsa prepare`)* | a SABSA architecture built from client material |

---

## 3. Commands

Every command has the same parts: **what it does**, **syntax**, **what
happens**, **try it**, **what to expect**, **check it worked**.
Arguments in `<angle brackets>` are required; in `[square brackets]`,
optional.

### /demo

**What it does.** Sets up, lists and restores the demo projects, and
checks that the library works.

**Syntax.**

```
/demo setup            copy the demo projects to ~/it-role-demo
/demo list             what each demo project is for
/demo reset <project>  put one project back to its starting state, to repeat a demo
/demo check            verify the demos and tools work, without using Claude's judgement (about ten seconds)
```

**Try it.** `/demo check`, then `/demo setup`.

**What to expect.** `check` reports about a dozen passes, ending "the
demos are ready to use". `setup` lists three folders under
`~/it-role-demo`.

**Check it worked.** `~/it-role-demo/invoice-service` exists and, if git
is installed, has five commits: `git -C ~/it-role-demo/invoice-service
log --oneline`.

### /guide

**What it does.** Shows this guide, or the section for one command, and
offers to run that command's demo.

**Syntax.** `/guide` · `/guide <command>` · `/guide <topic>` (for
example `/guide approvals`, `/guide templates`).

**Try it.** `/guide rework`.

### /analyse

**What it does.** Understands a code repository, a document library or a
SABSA library — what it is, how it is organised, who it serves, where it
is thin — without judging it. Run it before a review, or on anything
unfamiliar.

**Syntax.** `/analyse <path or description>`

**What happens.**
1. The agent works out what kind of library it is.
2. It runs the matching survey: `repo_survey.py` for code (size,
languages, churn hotspots, test ratio, dependencies); `doc_survey.py`
for documents (structure, owners, review dates, links, orphans,
duplicates).
3. The analysis agent (`codebase-reviewer` or `document-reviewer`, in
analysis mode) reads what the survey points to and writes up the
picture.

Nothing is changed, and no verdicts are given.

**Try it.**

```
/analyse invoice-service
/analyse policy-docs
```

**What to expect.**
- *invoice-service:* a Python service of about 80 lines in `app/`, with
API, arithmetic, storage and configuration modules; two tests, both on
`invoices.total`; one pinned dependency; seven commits by two authors.
- *policy-docs:* seven Markdown documents, one index; one link that
points nowhere; documents without an owner or with a passed review date;
two identical documents.

**Check it worked.** You get a description, not a list of defects. If it
starts rating things, it has drifted into `/review`.

### /criteria

**What it does.** Creates or shows the review criteria for a project.
Criteria are what `/review` judges against; they live in
`<project>/.ai/review-criteria.md`, a file you own and edit.

**Syntax.** `/criteria [project path]`

**What happens.** The agent shows which criteria currently apply and
where they come from — see [review criteria](#review-criteria). If they
are the package default, it offers to create the project's own file from
the default, asking the type (software, documents or SABSA). Then it
shows you the file and offers to tailor it.

**Try it.**

```
/criteria invoice-service
```

Accept the offer to create the file. Then add a criterion of your own,
either by asking Claude ("add a criterion C9 on money handling: amounts
must be integer cents or Decimal, never float") or by editing
`invoice-service/.claude/review-criteria.md` yourself:

```markdown
## C9 Money handling
Monetary amounts are integer cents or Decimal, never binary floating point.
- High if money is computed or stored as float
```

**What to expect.** A file with eight criteria, C1 Correctness to C8
Source documentation, plus yours.

**Check it worked.** Run `/criteria invoice-service` again: it now says
the criteria come from the project file, and lists C9. The next `/review
invoice-service` should report float money under C9.

### /review

**What it does.** Reviews code, documents or a SABSA library against
criteria fixed before reading, and records each finding — located to a
file and line, with evidence and a recommendation — in a findings
ledger.

**Syntax.**

```
/review <path>
/review <path> against <criteria file, or the criteria in words>
```

**What happens.**
1. The agent resolves the criteria (see [review
criteria](#review-criteria)) and **shows them to you with where they
came from. It waits for your yes.**
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

**What to expect — invoice-service.** The planted flaws, by criterion:

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

**Check it worked.** The provider report lists findings with locations
and the ledger ID.
**Optional developer check:** the ledger can also be inspected directly
with `python3 ~/.ai/it-role-house/tools/findings.py status
review-<date>` (run in the project folder).

### /rework

**What it does.** Fixes the open findings of a review. One agent fixes;
a different one verifies each fix; it repeats until every finding is
verified — or brings you the ones that will not converge.

**Syntax.** `/rework [ledger]` — without a ledger name, the newest in
`.findings/`.

**What happens.**
1. For each open finding, the author for that kind of library fixes it:
`role-engineer` for code, `docs-author` for documents, `sabsa-architect`
for SABSA.
2. The reviewer — not the author — verifies each fix, and reopens any
that is not right.
3. A finding reopened three times is **stuck**. The agent stops and
shows it to you with its history. You decide: accept it as a risk (**an
approval prompt**), have the reviewer withdraw it, or change the
requirement.
4. It ends when the ledger reports COMPLETE.

**Try it.** After `/review invoice-service`:

```
/rework
```

**What to expect.** Parameterised SQL, an ownership check on delete and
list, the key moved to an environment variable, the discount boundary
fixed with a test, a guard for empty invoices, the swallowed exception
surfaced, `requests` upgraded, a docstring on every public function
stating its contract, and tests: unit tests for the API and the
arithmetic, including the discount boundary, deletion by a non-owner and
an empty invoice, and an integration test running the storage against a
real SQLite database — which is what proves the injection is gone. the
agent cannot finish until those tests exist and a test run after its
last change has passed. The old key remaining in git history cannot be
fixed by editing files — expect it to come back to you as a decision:
rotate the key (a real-world action) and accept the history, or rewrite
the history.

**Check it worked.** `findings.py status <ledger>` says COMPLETE, or
lists stuck findings for you; and the tests pass: in `invoice-service`,
`python -m pytest` (on Windows `py -3 -m pytest`). If pytest is missing,
install it first with `python -m pip install pytest`.

### /diagnose

**What it does.** Finds the root cause of a defect *before* anything is
fixed, through three comparisons that are mandatory: against the **last
known good** state, against a **working analogue**, and against
**timing**. Then, if you agree, fixes it through the rework loop, with a
regression test written first.

**Syntax.** `/diagnose <symptom, failing test or issue>` — and say, if
you know, when it last worked and where something similar works. Both
often save hours.

**What happens.**
1. The agent asks when it last worked and where something similar works,
unless you have said.
2. The `defect-analyst` agent reproduces the defect as a command and
runs it many times: does it fail every time, or only sometimes? An
intermittent failure is itself evidence that timing or ordering take
part.
3. The three comparisons:
   - **A. Last known good** — it bisects the history to the first commit
     at which the defect appears, in a separate git worktree, so your
     working tree is never touched; and lists everything else that
     changed — dependencies, configuration, and infrastructure.
   - **B. Working analogue** — it diffs the failing code against code
     that works (a sibling function, another input
     or environment) and confirms which difference is decisive.
   - **C. Timing** — timeouts against measured durations, asynchronous
     work not awaited, ordering, clocks, schedules, and expiry; it
     varies timing on purpose to see whether the defect follows.
4. It tests at least two competing hypotheses. `defect.py` then
**validates the analysis**: no fix proceeds while a comparison is
missing, a "not applicable" has no reason, timing is dismissed although
the defect is intermittent, or no hypothesis is confirmed.
5. You see the report: the reproduction, the three comparisons, the
hypotheses, the root cause with its location, trigger and contributing
factors, and the proposed fix and regression test.
6. If you agree, `role-engineer` writes the regression test, sees it
fail, fixes the root cause and runs the tests; the `defect-analyst`
verifies.

**Try it.** In `~/it-role-demo/invoice-service`, one at a time:

```
/diagnose An order of exactly 1000 EUR gets no discount, though the README promises 5% from 1000. It was right when the API was first written.
/diagnose Bob can delete Alice's invoice, although he cannot read it.
/diagnose test_charge_is_approved in tests/test_payments.py fails now and then.
```

**What to expect.**

| Defect | What the comparisons should find |
| --- | --- |
| the discount | **A:** it fails every time; bisecting from *Invoice creation, storage and API* finds the first bad commit, *Simplify discount calculation* (21 July 2026), which replaced a loop with `sum()` and quietly turned `>=` into `>`. **C:** not applicable — deterministic in every run, no clock or I/O. Root cause in `app/invoices.py`, `total`; regression test at 999.99, 1000 and 1000.01. |
| deleting another's invoice | **A:** not applicable — it never checked ownership. **B:** the working analogue is `get_invoice`, which checks `row[1] != user`; `delete_invoice` has no such check — the decisive difference. |
| the payment test | it fails in roughly a third of runs — **intermittent**, so timing cannot be dismissed. **C:** `GATEWAY_TIMEOUT_SECONDS = 0.1` against a gateway measured at up to 0.15 s; a timeout is reported as *declined*, so a slow approval becomes a refusal. The fix separates "no answer yet" from "declined" and sets the timeout from measured latency; the regression test uses a fake gateway with a controlled delay, so it fails *every* time on the old code. A longer timeout alone would only make the defect rarer — the standard does not accept that as a fix. |

**Check it worked.** The validated report is shown; after the fix,
`findings.py status defect-<date>` is COMPLETE; the provider should
report the
measured rerun outcome. **Optional engineer verification:**
`python3 ~/.ai/it-role-house/tools/defect.py repeat "<reproduction>" -n
30` reports 0 failures for the payment defect.

### /develop

**What it does.** Builds or changes something in a software product or
document library, through the role that owns that kind of work, on a
branch, reviewed before it is proposed to you for merge.

**Syntax.** `/develop <what to build or change>`

**What happens.** The agent routes the request through `role-router` to
the right role and agent; works on a branch; has the change reviewed as
`/review` would; then proposes it to you. The merge is yours.

**Try it.**

```
/develop add the CSV export of invoices that the invoice-service README promises, with tests
```

**What to expect.** A new branch with an export function — documented
with a docstring that states its parameters, result and exceptions —
tests for it, run and passing, because the hooks will not let it finish
otherwise — including an empty invoice list and a customer name
containing a comma — a review of the change, and a summary asking you to
merge.

**Check it worked.** `git -C invoice-service branch` shows the new
branch; the tests pass on it.

### /govern

**What it does.** Assesses how a repository or document library is
governed — ownership, change control, versioning, currency, policy —
from its files and git history, and proposes a governance model sized to
it. It changes nothing.

**Syntax.** `/govern <path>`

**Try it.**

```
/govern invoice-service
/govern policy-docs
```

**What to expect — invoice-service.** No CODEOWNERS, no changelog, no
version tags; a feature branch merged by its own author two minutes
after it was written; commits straight to `main`; a key rotation at
23:41 that left the old key in the history; the README names no owner. A
proposal: owners, protected `main` with required review, semantic
versioning with a changelog, a secret-handling rule.

**What to expect — policy-docs.** Ownership and review dates incomplete
and partly lapsed; no version or approval record for policies;
duplicates in circulation. A proposal: an owner and review cycle per
policy, an approval record, and a retirement rule.

**Check it worked.** Findings in a ledger, and a proposed model you
could adopt.

### /research

**What it does.** Researches a problem to a decision: frames the
question and the decision it informs, surveys prior art from primary
sources, and — only if needed — runs experiments whose success criteria
are fixed before they run. It ends with adopt, trial, assess or hold.

**Syntax.** `/research <question>`

**What happens.**
1. The agent agrees the question, the decision and a time-box with you.
2. `research-analyst` researches and cites primary sources.
3. If that does not settle it, `experiment-engineer` writes
`experiments/<id>/PLAN.md` — hypothesis and success criteria — and The
agent records its fingerprint **before** anything runs.
4. The experiment runs; `research-analyst`, not the engineer, assesses
the result against the plan.
5. You get a recommendation, its confidence, and what remains unknown.
At most three experiments per question.

**Try it.** In `~/it-role-demo/invoice-service`:

```
/research Should invoice-service compute money with float, Decimal or integer cents? Settle it with a correctness test and a timing benchmark.
```

**What to expect.** Sources on floating-point representation of money;
an experiment showing float sums that drift (for example 0.1 + 0.2), and
the speed cost of Decimal against integer cents; a recommendation of
Decimal or integer cents, with the trade-off.

**Check it worked.** `experiments/<id>/PLAN.md`, `PLAN.sha256`,
`RESULTS.md` and `DECISION.md` exist, and the hash still matches the
plan: `sha256sum -c experiments/<id>/PLAN.sha256`.

### /sabsa

**What it does.** Builds a SABSA security architecture from material
about a client or environment, and updates, reviews, improves and
documents it. The architecture is a library of small files — elements
and the 36 cells of the SABSA matrix — from which the document is
generated.

**Syntax.**

```
/sabsa prepare <library>        start from client material
/sabsa create <library>         derive the architecture in dependency order; complete all six questions per layer
/sabsa update <element> <library>
/sabsa review <library>         findings against the SABSA criteria
/sabsa suggest <library>        ranked gaps, each with the next step
/sabsa questions <library>      the open assumptions, as questions for the client
/sabsa approve <library>         owner-approve the exact clean snapshot
/sabsa approval <library>        verify that the current snapshot still matches the approval
/sabsa document <library> [as docx]
/sabsa template <library>       which document template applies; set up the client's own
```

**What happens in prepare and create.**
1. The library is created, with `00-sources/` for material and `matrix/`
for the 36 questions.
2. The client material goes into `00-sources/`. Public context the
material implies — regulation for the sector, typical threats — is
researched and saved there too, with citations.
3. Business drivers come first. Each cites the file and section it rests
on, and says whether it is **stated** by the client, **inferred** from
what they said, or **assumed**.
4. Build elements in dependency order: drivers → attributes →
risks/opportunities → control objectives → domains → services →
mechanisms → components → operations. Then complete each SABSA layer's
six questions — what, why, how, who, where, when — or "not applicable"
with a reason. Every settled cell states its basis; stated/inferred
cells cite evidence.
5. Run the structural and judgement review. A domain must trace through
a control objective; every operation has a threshold action; all claims
carry provenance. After review, the owner explicitly approves the exact
snapshot with `sabsa approve`; any later input change invalidates that
approval.

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

**Choose the viewpoint and format in ordinary language.** Markdown is
the SABSA workflow default. For example, ask `/sabsa document
acme-pay/sabsa — generate the Logical Security Architecture in English
as LaTeX and PDF, preserving source references and publication gaps`.
In Codex use `$workflow-sabsa document acme-pay/sabsa` with the same
instruction. Request DOCX when the review audience needs Word, or
editable CSV catalogues when managing structured entries. This selects
existing outputs; it does not change a global default or grant approval.

**Author the narrative before rendering.** Six distinct viewpoint
profiles cover business context, security concept, logical architecture,
physical design, component engineering, and operations/assurance. They
combine authored chapters with complete element fields and source
bodies, provenance and typed business paths. Ask JAI to create chapter
skeletons and help author source-backed professional English prose;
missing decisions and narrative remain visible gaps. The renderer does
not translate authoritative text automatically.

The underlying `sabsa.py narrative-init LIB --layer LAYER` creates
missing chapter skeletons under `narratives/LAYER/`, without replacing
existing prose. Chapters record `basis`, `source`, `author` and
`language: en`. They are semantic inputs covered by validation,
citations and snapshot approval; editing them invalidates a prior
approval just as editing an element does. The installed authoring
contract is `~/.ai/it-role-house/sabsa/publication/README.md`.

**Manage catalogues through the canonical source.** Ask JAI to export
CSV, retain stable IDs and schema while editing, validate the proposal,
then import it into the local entries and re-review. Import updates
existing local IDs; CSV is an editable projection rather than a second
authority. Reused entries are managed in their source library. An
export manifest fingerprints the export, not subsequent edits or their
approval.

**Use the dependencies for the requested output.** Markdown needs no
external document renderer. Pandoc emits TeX and DOCX; compiling the
controlled PDF edition adds XeLaTeX, installed TeX packages and DejaVu
Serif. LibreOffice or Word supports independent rendering of Office
outputs for visual QA; the SABSA TeX/PDF renderer does not invoke an
Office renderer. Ask for actual validation and rendered-QA evidence,
not an inferred pass from file existence.

**What to expect.**
- *Drivers* such as doubling partner revenue through PSPs and partners
demanding proof of controls, each citing
`discovery-meeting-2026-10-01.md`.
- *Attributes* from the RFP: attributable privileged actions (R4), 99.9%
availability (R7), credentials rotated within 90 days (R9) — each with a
metric and a target.
- *Risks* such as the shared administrator account, and the static,
manually issued partner API keys.
- *Assumptions* — and therefore questions for the client — such as
whether ACME Pay is a regulated payment institution under PSD2, whether
DORA applies, and data residency beyond eu-central-1.
- *The document:* the selected architecture or viewpoint template,
including its matrix coverage and traceability. It remains DRAFT until
the library has zero errors/warnings, all 36 cells are settled, and the
current snapshot has a valid owner approval; incomplete viewpoint
narrative or source-quality gaps also prevent an approved publication
presentation.

**Optional technical verification (agent or maintainer runs it; not a
required operator step).** `python3 ~/.ai/it-role-house/tools/sabsa.py
check
acme-pay/sabsa` reports the structural state; `sabsa.py matrix
acme-pay/sabsa` shows the 36 cells and how many are settled. A
release-ready library must have zero errors and zero warnings; after the
owner's explicit decision, `sabsa.py approval acme-pay/sabsa` reports
`APPROVED`.

### /publish

**What it does.** Publishes one reviewed semantic artifact into
enterprise-ready views without changing the approved claims. The
publication layer records the semantic SHA-256 and applies the selected
archetype, render targets and Publication Gate.

**Syntax.** `/publish <semantic model> [archetype] [formats]`

**What happens.**
1. The semantic input is validated and fingerprinted.
2. The artifact contract selects its publication archetype and supported
render targets.
3. The publication engine renders the requested HTML, DOCX, PPTX, XLSX
and/or SVG outputs from the same source.
4. The Semantic Gate must already be clear; the Publication Gate then
checks structure, legibility and package integrity.
5. The generated outputs carry the source semantic hash so reviewers can
verify that presentation did not silently change the substance.

**Try it.** Publish an architecture decision or review pack that has
already passed semantic review:

```
/publish architecture-review.json architecture-review-pack docx,pptx,html
```

**Optional technical self-test (agent or maintainer, not approval of
this document).** `python3 ~/.ai/it-role-house/tools/publication.py
self-test` validates the renderer and package integrity.

### /repository

**What it does.** Maintains the canonical enterprise-architecture
repository, exchanges ArchiMate models, generates governed views, checks
cross-project consistency, traces benefits and prevents unsafe
retirement while active dependencies remain.

**Syntax.** `/repository
<init|validate|import|export|views|portfolio|impact|decommission> ...`

**What happens.**
1. The EA domain projection repository JSON remains the authoritative
  architecture-
domain projection store.
2. ArchiMate Open Exchange is used at explicit import/export boundaries
rather than as the persistent repository format.
3. Stable element and relationship IDs are preserved across views and
exchanges.
4. Repository validation checks referential integrity, lifecycle state,
portfolio links, view coverage and cross-project dependencies.
5. Decommission is blocked while active dependencies remain unless an
explicit governed waiver is recorded.

**Try it.**

```
/repository validate architecture-repository.json
/repository views architecture-repository.json all
/repository portfolio architecture-repository.json
/repository export architecture-repository.json model.xml
```

**Optional technical self-test (agent or maintainer, not repository
sign-off).** `python3 ~/.ai/it-role-house/tools/repository.py
self-test` runs the repository, exchange, multi-view and lifecycle
regression suite.

### /layered

**What it does.** Takes a consequential decision through six layers of
agents — intent, meaning, policy, design, realisation, evidence — with
requirements going down and evidence coming back up. Unsupported work is
sent back for rework, problems escalate layer by layer to you, and every
step is recorded so that you can later show why the outcome was allowed.
Use it when you will have to justify a decision; not for routine
changes.

**Syntax.** `/layered <intent, stated as you would to an accountable
team>`

**What happens.**
1. Your intent is recorded verbatim, and the decision log starts in
`.fabric/` of the current folder.
2. Each layer turns the requirement from above into a precise contract
for the layer below.
3. Results come back up and are reviewed by the layer that asked for
them; nothing is built on unreviewed work.
4. When a layer cannot meet its requirement, it reformulates — within a
budget — or escalates. Escalations climb one layer at a time.
5. **When one reaches you**, the agent shows you a decision packet built
from the record: what was tried, real examples of why it failed, and the
the options found. You choose. Claude may propose the guarded operation
for your explicit interactive approval; Codex must show the exact
command for **you** to run separately in a trusted terminal.
6. The result is released only if the record shows it is justified.

**Try it.** In `~/it-role-demo` (expect 20–40 minutes; it is the most
thorough command):

```
/layered Decide whether invoice-service is ready to be exposed to external partners. It must be secure enough for partner traffic and its money calculations must be exact.
```

**What to expect.** The evidence layer finds the injection,
authorisation and secret problems; the policy layer cannot accept them;
the question reaches you with options such as "fix before exposure" or
"expose a read-only subset" — each with its cost. Whatever you choose is
recorded, approved by you.

**Check it worked.** `/fabric-report` gives an independent verdict on
the record.

### /fabric-report

**What it does.** An independent check of a `/layered` decision record:
that it has not been tampered with, that every step followed the rules,
and which outcomes the record actually justifies.

**Syntax.** `/fabric-report [engagement]` — without a name, the newest
record in `.fabric/`.

**Try it.** After the `/layered` demo: `/fabric-report`

**What to expect.** Integrity confirmed; each result marked as justified
or not, with the reason when not; open items; whether the final product
is releasable.

---

## 4. Concepts

### Review criteria

What a review judges against, fixed before reading. They come from the
first of these that exists:

1. criteria in your request — `/review docs against
docs/style-guide.md`;
2. the project's own file `<project>/.ai/review-criteria.md` — created
by `/criteria`, yours to edit and commit;
3. your personal default `~/.ai/review-criteria.md`;
4. the package default for the kind of target: software, documents or
SABSA.

Each criterion is a `## C<n> <title>` heading in the file; findings cite
it by that ID. Each review records which file it used and a fingerprint
of its contents.

### The findings ledger

Every review records its findings in `.findings/<name>.jsonl` in the
project. Each finding is open, resolved, verified, stuck, accepted or
withdrawn. The reviewer never fixes, and the fixer never verifies — the
ledger refuses both. After three failed fixes a finding is stuck and
comes to you. The ledger is append-only and tamper-evident: do not edit
it by hand.

### Approvals

Some acts are reserved for you: accepting a risk, granting an exception,
accepting a product, approving a change to the library itself. They
require a trusted human action. Claude may expose the exact command in
an
interactive permission prompt; when no trusted prompt can appear, that
action is refused. Codex does not turn the denied agent command into a
trusted approval prompt, so it must hand the exact command to the human
for execution in a separate terminal. A chat statement alone is not
a recorded authority event.

### SABSA library layout

```
<library>/
├── library.md          name, organisation, scope, owner, version; its text is the executive summary
├── 00-sources/         what is known about the client; every claim cites a file here
├── 01-contextual/ … 06-service-management/    the elements, by SABSA layer
├── matrix/             36 files: each layer's six questions, answered or marked not applicable
├── narratives/         authored viewpoint chapters with basis/source/author/language provenance
└── templates/          optional: the client's own document template and reference.docx
```

`~/.ai/it-role-house/skills/sabsa-library/references/structure.md`
describes every element and field; `references/templates.md` describes
templates and every field they can use.

### Defect analysis

A defect is analysed before it is fixed, following
`~/.ai/it-role-house/standards/defect-analysis.md`: reproduce it as a
command and measure whether it is intermittent; then compare against the
**last known good state** (when did it work, and what changed?), against
a **working analogue** (where does the same kind of thing work, and what
differs?), and against **timing** (does an operation get the time it
needs? do other timed events — schedules, expiry, ordering, clocks —
take part?). Each comparison is carried out or marked not applicable
with a reason. Hypotheses are tested by experiment; the root cause is
distinguished from the trigger and contributing factors; the fix
addresses the root cause, with a regression test that fails first.
`/diagnose` runs it; the `defect-analyst` agent carries it out;
`defect.py` bisects safely, reports changes, compares code, scans for
timing constructs, repeats runs and validates the analysis.

### Source code documentation

All code the agent writes follows
`~/.ai/it-role-house/standards/code-documentation.md`: a doc comment on
every public element in the language's own format — Javadoc for Java,
docstrings for Python, TSDoc, XML doc, KDoc, godoc — stating its
contract (parameters, result, exceptions); comments that say *why*,
never narrate *what*; no commented-out code. It is enforced in layers:

- a hook checks every source file the agent writes and tells the agent
at once what is missing — for an edit, only the declarations the edit
touched, so changing one method never obliges Claude to document a whole
legacy file;
- the agent cannot finish its turn while public API it wrote is
undocumented (a second attempt is allowed, and you are told what
remains, so a problem it cannot solve never traps the session);
- reviews apply it as criterion C8;
- the standard includes CI configurations — javac doclint and
Checkstyle, Ruff, ESLint, and the equivalents for C#, Kotlin and Go —
that make it a build failure in your own pipeline.

To switch the hook off for one project, create an empty file
`.ai/no-doc-check` in it.

### Tests

Code the agent writes is accompanied by its tests, following
`~/.ai/it-role-house/standards/testing.md`:

- **unit tests** for every public behaviour added or changed — the
normal case, the boundaries, a failure path; for Java, JUnit 5 with
AssertJ and `@ParameterizedTest`, and Mockito for collaborators;
- **integration tests** for every boundary to a database, a service, a
broker or the file system, against the real thing — Testcontainers,
`*IT` classes run by Maven Failsafe;
- **mocks only for collaborators** at the edge of the unit — never the
class under test, never types you do not own;
- **a regression test** for every fixed defect.

The agent then runs the tests. A hook checks that what Claude wrote has
tests, notices every test run and whether it failed, and will not let
Claude finish while its code lacks tests, while the tests have not been
run since its last change, or while the last run failed. Code outside a
project (no `pom.xml`, `package.json`, `pyproject.toml` …) is exempt, as
are prototypes in `experiments/`. Reviews apply this as criterion C4.
The standard includes CI configurations — Surefire and Failsafe, JaCoCo,
pytest-cov, and the equivalents — for your own pipeline.

To switch the test hooks off for one project, create an empty file
`.ai/no-test-check` in it.

### Decision records (`/layered`)

`.fabric/<engagement>.jsonl` in the folder where you ran `/layered`:
every requirement, contract, result, review, escalation and decision,
hash-chained. `/fabric-report` checks it.

---

## 5. Direct tools for maintainers

**Audience:** engineers who are developing an adapter, reproducing a
failure, or operating outside the provider interface intentionally. Most
readers should stay in Claude/Codex CLI and request these checks from
the orchestrator. Shell commands below do not by themselves grant an
approval or make a result releasable.

Everything the commands rely on is a plain Python tool you can run
yourself, in any terminal. On Windows, use `py -3` in place of
`python3` if your Python installation uses the Windows launcher.
The installed guide reproduces this maintained Markdown page.

| Tool | Main commands |
| --- | --- |
| `~/.ai/it-role-house/tools/criteria.py` | `init <project>` · `show <path>` · `check <file>` |
| `~/.ai/it-role-house/tools/findings.py` | `status <ledger>` · `list <ledger>` · `report <ledger>` |
| `~/.ai/it-role-house/tools/doc_survey.py` | `<docs folder>` |
| `~/.ai/it-role-house/tools/doc_check.py` | `<source files or folders>` — documentation against the standard |
| `~/.ai/it-role-house/tools/test_check.py` | `<source files or folders>` — tests against the standard |
| `~/.ai/it-role-house/tools/defect.py` | `repeat` · `bisect` · `changes` · `compare` · `timing` · `analysis validate\|render\|findings` |
| `~/.ai/it-role-house/skills/it-roles-quality-and-testing/scripts/repo_survey.py` | `<repository>` |
| `~/.ai/it-role-house/tools/sabsa.py` | `init` · `new` · `check` · `matrix` · `suggest` · `trace` · `view` · `lifecycle` · `overlays` · `reuse` · `questions` · `sources` · `documents` · `document` · `narrative-init` · `catalogues export\|validate\|import` · `template` · `migrate` |
| `~/.ai/it-role-house/tools/sabsa_publication_demo.py` | `--out DIR --render` — populated fictional English six-viewpoint example in a fresh directory |
| `~/.ai/it-role-house/tools/publication.py` | semantic-model rendering to HTML · DOCX · PPTX · XLSX · SVG; `self-test` |
| `~/.ai/it-role-house/tools/repository.py` | `init` · `validate` · `import-open-exchange` · `export-open-exchange` · `generate-views` · `portfolio` · `impact` · `decommission` · `self-test` |
| `~/.ai/it-role-house/fabric/fabric.py` | `status` · `verify` · `justify` · `report` · `dossier` |
| `~/.ai/it-role-house/demo/demo.py` | `setup` · `reset` · `check` · `list` |

Each tool has `--help`. For example:

```
python3 ~/.ai/it-role-house/tools/doc_survey.py ~/it-role-demo/policy-docs
python3 ~/.ai/it-role-house/tools/sabsa.py matrix ~/it-role-demo/acme-pay/sabsa
```

For a maintainer reproducing SABSA publication operations:

```sh
python3 ~/.ai/it-role-house/tools/sabsa.py narrative-init LIB --layer logical
# Author and review LIB/narratives/logical/ and the canonical elements before rendering.
python3 ~/.ai/it-role-house/tools/sabsa.py document LIB --layer logical --out logical.md
python3 ~/.ai/it-role-house/tools/sabsa.py document LIB --layer logical --out logical.tex
python3 ~/.ai/it-role-house/tools/sabsa.py document LIB --layer logical --out logical.pdf --latex
python3 ~/.ai/it-role-house/tools/sabsa.py document LIB --layer logical --out logical.docx
python3 ~/.ai/it-role-house/tools/sabsa.py catalogues LIB export --directory CSV
# Edit existing local entries in CSV while retaining schema and stable IDs.
python3 ~/.ai/it-role-house/tools/sabsa.py catalogues LIB validate --directory CSV
python3 ~/.ai/it-role-house/tools/sabsa.py catalogues LIB import --directory CSV
```

`--layer` accepts `contextual`, `conceptual`, `logical`, `physical`,
`component` and `service-management`; `operational` aliases the last.
The installed publication contract describes chapter keys, provenance,
language review and source-quality gaps. The example builder's
`--render` emits Markdown, TeX, DOCX and PDF. Successful generation
does not constitute an architecture approval or a product release.

---

## 6. Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| A command is not recognised | Start a new Claude Code or Codex CLI session after installing or upgrading. |
| "Python 3.10 or newer is required" | Install Python from python.org; on Windows tick "Add python.exe to PATH". |
| An authority act is refused, with a message about the permission mode | You are in auto or bypass mode, where no approval prompt can appear. Switch to the default mode. |
| `/sabsa document … as docx` says pandoc is needed | Install pandoc from pandoc.org, or produce Markdown and convert it yourself. |
| Windows: a note that Git for Windows was not found | Claude Code then uses PowerShell. Most things work; install Git for Windows for the full experience. |
| The agent keeps adding Javadoc or docstrings it was not asked for | That is the documentation standard, applied to code the agent wrote or changed. To switch it off for a project, create an empty file `.ai/no-doc-check` in it. |
| The agent says it cannot finish: tests missing, not run, or failing | That is the testing standard, applied to code the agent wrote. Let it write and run the tests. To switch it off for a project, create an empty file `.ai/no-test-check` in it. |
| A demo went wrong and you want to start again | `/demo reset <project>`. |
| You want to check the installation itself | `/demo check`, or `python3 ~/.ai/it-role-house/scripts/check_agent_policy.py ~/.claude`. |

**Uninstalling the managed package:** from the extracted release
directory, run `bash uninstall.sh` (macOS/Linux) or `uninstall.cmd`
(Windows). These wrappers invoke the managed uninstaller under
`.ai/setup/`; personal files, unrelated settings and demo projects
remain outside its removal scope.
