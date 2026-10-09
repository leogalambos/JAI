# Review criteria: where they come from and how to set your own

A review applies criteria fixed **before** the reviewer reads anything, so its findings can be defended later.
Each review records which criteria applied — the file and its hash — in its findings ledger.

## Where criteria come from

The first of these that exists:

| | Where | Use it for |
| --- | --- | --- |
| 1 | in the request: `/review docs/ against docs/style-guide.md, accuracy and tone only` | a one-off review |
| 2 | `<project>/.ai/review-criteria.md` | the project's standing criteria, committed with it |
| 3 | `~/.ai/review-criteria.md` | your personal default for every project |
| 4 | the package default for the kind of target: software, documents or SABSA | when you have not set any |

Files 2 and 3 are yours: the package never writes or overwrites them, and upgrades leave them alone.

## Setting your own

```bash
python3 ~/.ai/it-role-house/tools/criteria.py init <project>            # writes <project>/.ai/review-criteria.md from the defaults
python3 ~/.ai/it-role-house/tools/criteria.py show <project or folder>  # which criteria apply to it, from where
python3 ~/.ai/it-role-house/tools/criteria.py check <file>              # is it well formed
```

Or in Claude Code: `/criteria` creates or shows the project's file. Then edit it: add, remove, reword or
re-weight criteria. The file looks like this:

```markdown
---
type: software              # software | documents | sabsa
scope: src/ api/            # empty means the whole target
exclude: vendor/ generated/
sources: docs/requirements.md, https://…   # what claims are checked against
---
## C1 Correctness and robustness
Behaviour matches the stated requirements; failure paths are handled; no silent data loss.
- Critical if it loses or corrupts data; high if a main path is wrong

## C2 Security
…
```

Keep each criterion as a `## C<n> <title>` heading: findings cite it by that ID. Everything under the heading is
free text the reviewer applies — say what to check against, and what makes something critical rather than low.

## The package defaults

`criteria.py init` writes them out in full for you to edit. In summary — **software:** correctness, security
(OWASP ASVS L1), structure, tests against risk, operability, maintainability, supply chain. **Documents:**
accuracy, consistency, fitness for task, completeness, navigation, ownership and currency, plain language.
**SABSA:** traceability, measurability, evidence basis, correctness of links, two-sided risk, matrix coverage,
the assurance loop.
