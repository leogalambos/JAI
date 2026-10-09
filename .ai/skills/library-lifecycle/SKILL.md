---
name: library-lifecycle
description: "Runs the full lifecycle of a software product or a document library: analysis, review, development, rework and governance. Routes each activity to the right agent — codebase-reviewer or document-reviewer to analyse and review, the engineering or documentation agents to develop and rework, artefact-governor for governance — and drives review, rework and verification through a findings ledger until every finding is verified, withdrawn or accepted by you. Use for 'analyse this repository', 'review our documentation', 'rework the findings', 'improve this codebase', 'govern this library', or any multi-step work on an existing body of code or documents. For SABSA libraries use sabsa-library; for research use research-and-development."
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

# Library lifecycle: analyse, review, develop, rework, govern

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `artefact-governor`, `codebase-reviewer`, `docs-author`, `document-reviewer`, `library-approver`, `library-author`, `library-release`, `role-author`, `role-engineer`, `role-router`, `source-docs-engineer`.

`tool-tier: orchestrate` (`Read, Grep, Glob, Bash, Task, Agent`) · `version: 1.0.0`

You orchestrate. Agents do the work; you dispatch them, pass each only what its step needs, and record outcomes
in the findings ledger. You hold no Write or Edit while this skill is active, so you cannot do an agent's work.

## First, what kind of library

| The target is | Use |
| --- | --- |
| A code repository or software product | the **software** column below |
| A folder of documents: guides, policies, a book, articles, web content | the **documents** column |
| A SABSA security architecture library | the `sabsa-library` skill instead |
| This role library itself | `library-author` → `library-approver` → `library-release` |

## The activities

| Activity | Software product | Document library | Output |
| --- | --- | --- | --- |
| **Analyse** — understand, no verdicts | `codebase-reviewer`, analysis mode, after `repo_survey.py` | `document-reviewer`, analysis mode, after `doc_survey.py` | what it is, how it is built, where it is thin |
| **Review** — judge against criteria fixed first | `codebase-reviewer` | `document-reviewer` | located findings in a ledger |
| **Develop** — create or extend | `role-router` → `role-engineer` / `role-author`; `source-docs-engineer` for in-code docs | `docs-author` | the change, on a branch |
| **Rework** — fix findings, then re-verify | `role-engineer` fixes, `codebase-reviewer` verifies | `docs-author` fixes, `document-reviewer` verifies | ledger complete |
| **Govern** — ownership, change control, versioning, currency | `artefact-governor` | `artefact-governor` | assessment, findings, proposed model |

Tools, all read-only except the ledger:

```bash
python3 ~/.ai/it-role-house/skills/it-roles-quality-and-testing/scripts/repo_survey.py <repo>
python3 ~/.ai/it-role-house/tools/doc_survey.py <docs-dir>
python3 ~/.ai/it-role-house/tools/findings.py status|list|report <ledger>
```

Source code written in any activity follows `~/.ai/it-role-house/standards/code-documentation.md`: a hook checks each file as it is written, and
before a change is proposed for review, run `python3 ~/.ai/it-role-house/tools/doc_check.py <changed paths>` and
`python3 ~/.ai/it-role-house/tools/test_check.py <changed paths>` — both must report no errors — and the project's test suite must pass. Tests follow
`~/.ai/it-role-house/standards/testing.md`.

Ledgers live in `.findings/` in the workspace. Name one per review, e.g. `docs-2026-10`.

## Review, then rework, bounded

1. **Criteria first, from a file.** Resolve which criteria apply before the reviewer reads anything:

   ```bash
   python3 ~/.ai/it-role-house/tools/criteria.py show <target>
   ```

   It takes the first that exists: criteria the user gave in the request; the project's own
   `.ai/review-criteria.md`; the user's personal `~/.ai/review-criteria.md`; the package default for the
   kind of target. Show the user the criteria, where they came from and their hash, and get a yes. If the user
   wants to change them, `criteria.py init <project>` writes the project file for them to edit
   (see `references/criteria.md`).
2. **Review.** Dispatch the reviewer with the target, the criteria text, their source and hash, and the ledger
   name. Findings cite criteria by ID (`C2 Security`), and the ledger records which criteria file applied. It records findings
   itself (`findings.py add`).
3. **Rework.** For each open finding, dispatch the author for that library type with the finding text and
   location only. Record each resolution with `findings.py resolve <ledger> <id> --by <author> --note …`.
4. **Verify.** Dispatch the **reviewer** — never the author — to verify each resolved finding
   (`findings.py verify … --ok|--reopen`).
5. **Repeat 3–4** until `findings.py status` says COMPLETE. A finding reopened three times is **stuck**: stop
   reworking it and show it to the user with its history. They decide: accept it as a risk
   (`findings.py accept-risk`, which asks them to approve), have the reviewer withdraw it, or change the
   requirement.

Suggestions never block completion; defects, gaps, risks and inconsistencies do.

## Development and governance

Develop on a branch, never on the default branch. A change is reviewed (step 2) before it is proposed for
merge, and the merge is the user's. For governance, `artefact-governor` assesses current practice from the
git history and files and proposes a model; applying it — CODEOWNERS, branch protection, review cycles — is a
change like any other, reviewed and merged by the owner.

## Rules

- The reviewer never fixes; the author never verifies. The ledger refuses both.
- Pass each agent its step's inputs only: the finding, not the whole review; the criteria, not the conversation.
- Never edit `.findings/` by hand. It is hash-chained, and a hook blocks it.
- For a consequential decision on top of this work — a release, an architecture choice someone must justify —
  use `/layered`, which adds layered review and an auditable record of who decided what.
