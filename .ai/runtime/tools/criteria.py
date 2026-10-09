#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Review criteria: where they live, and which ones apply.

Criteria are fixed before a reviewer reads anything, so the review can be defended later. They come from the
first of these that exists:

    1. criteria you give in the request itself            ("/review docs/ against docs/style-guide.md")
    2. <project>/.ai/review-criteria.md               your project's own, committed with the project
    3. ~/.ai/review-criteria.md                       your personal default, for every project
    4. the package default for the kind of target          software | documents | sabsa

Files 2 and 3 are yours: the package never writes or overwrites them.

    criteria.py init  <project> [--type software|documents|sabsa]   create .ai/review-criteria.md to edit
    criteria.py show  <target>                                      which criteria apply, from where, with hash
    criteria.py check <file>                                        is a criteria file well formed
"""
import argparse
import hashlib
import os
import re
import signal
import sys

for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]

NAME = "review-criteria.md"
TYPES = ("software", "documents", "sabsa")
CRIT = re.compile(r"^## (C\d+)\s+(.+?)\s*$", re.M)

DEFAULTS = {
"software": """## C1 Correctness and robustness
Behaviour matches the stated requirements; failure paths are handled; no silent data loss.
- Check against: the requirements or issues named in `sources`
- Critical if it loses or corrupts data; high if a main path is wrong

## C2 Security
Every entry point authenticates and authorises; input is validated; secrets are not in source; dependencies have
no known exploited vulnerabilities. OWASP ASVS level 1 as the reference.
- Critical if exploitable without credentials; high if exploitable by an authenticated user

## C3 Structure
Module boundaries hold; change hotspots (from `repo_survey.py`) are understood; no circular dependencies.

## C4 Tests
Every public behaviour has unit tests covering the normal case, the boundaries and a failure path; every boundary to an
external system has an integration test against the real dependency; mocks only for collaborators; tests are
deterministic and fail when the behaviour breaks. `test_check.py` errors are findings. Standard:
it-role-library/standards/testing.md.
- High for untested security, money or data-integrity logic, or an untested external boundary; medium otherwise

## C5 Operability
Logs, metrics and traces suffice to diagnose a failure; configuration is external; a release can be rolled back.

## C6 Maintainability
Readable and consistent; public contracts documented (ISO/IEC 25010 maintainability).

## C7 Supply chain
Licences compatible with how the product is distributed; builds reproducible; artefacts traceable to a commit.

## C8 Source documentation
Every public element has a doc comment in the language's format — Javadoc, docstrings, TSDoc, XML doc, KDoc,
godoc — stating its contract: parameters, result, exceptions, assumptions. Comments explain why, never narrate
what; no commented-out code. `doc_check.py` errors are findings. Standard: it-role-library/standards/code-documentation.md.
- High for undocumented public API of a library or service interface; medium elsewhere; low for narration
""",
"documents": """## C1 Accuracy
Claims, numbers and versions match the sources named in `sources`, and those sources are current.
- Critical if acting on it causes harm or a breach; high if it misleads a reader's task

## C2 Consistency
One term, rule, value and name for one thing, everywhere in the library.

## C3 Fitness for task
Each document serves one reader task — tutorial, how-to, reference or explanation — rather than a mix.

## C4 Completeness
The stated scope is covered; known gaps are stated, not hidden.

## C5 Navigation
Every document has a title and one H1; links resolve; nothing is orphaned without reason.

## C6 Ownership and currency
Every document names an owner and a review date that has not passed.

## C7 Plain language and accessibility
Short sentences, defined terms, headings and image text that make sense on their own.
""",
"sabsa": """## C1 Traceability
Every element traces upward to a business driver; `sabsa.py check` reports no traceability errors.
- High for any untraced element: it is cost without a business reason

## C2 Measurability
Every business attribute has a metric, a measurement method and a target set by the business.

## C3 Evidence basis
Drivers and attributes cite the client material they come from; assumptions are marked `basis: assumed`
and appear on the list of questions for the client.

## C4 Correctness of links
A link is present *and* right: the service really meets the objective it cites; the risk really threatens the
attribute it names. Follow several chains end to end.

## C5 Two-sided risk
Opportunities are considered alongside threats.

## C6 Coverage
Each of the 36 matrix questions — six layers by what, why, how, who, where and when — is answered for this
client, or marked not applicable with a reason that holds up (`sabsa.py matrix`).

## C7 Assurance loop
Every attribute that matters is measured in operation by an owned operation with a threshold action.
""",
}


def template(kind, project_name):
    return f"""---
type: {kind}
scope:            # what is in scope, e.g. src/ docs/ — empty means the whole target
exclude:          # what is out of scope, e.g. vendor/ generated/
sources:          # what claims are checked against, e.g. docs/requirements.md, https://...
---

# Review criteria — {project_name}

Edit freely: add, remove, reword or re-weight. Keep each criterion as a `## C<n> <title>` heading so that
findings can cite it. Severity: **critical** — harm or a breach if acted on; **high** — misleads or blocks the
main task; **medium** — noticeably degrades quality; **low** — polish.

{DEFAULTS[kind]}"""


def front(text):
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    out = {}
    for line in text[3:end].splitlines():
        k, _, v = line.partition(":")
        if _:
            out[k.strip()] = re.sub(r"\s+#.*$", "", v).strip()
    return out


def guess_type(target):
    if os.path.isfile(os.path.join(target, "library.md")) and os.path.isdir(os.path.join(target, "01-contextual")):
        return "sabsa"
    code = docs = 0
    for dp, dirs, fs in os.walk(target):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "vendor")]
        for f in fs:
            e = os.path.splitext(f)[1].lower()
            if e in (".md", ".rst", ".adoc", ".txt", ".docx", ".pdf"):
                docs += 1
            elif e in (".py", ".java", ".ts", ".js", ".go", ".cs", ".rb", ".kt", ".c", ".cpp", ".rs", ".php", ".sql"):
                code += 1
    return "documents" if docs > code else "software"


def resolve(target):
    """-> (kind, source_label, text)"""
    here = os.path.abspath(target if os.path.isdir(target) else os.path.dirname(target))
    d = here
    while True:
        for dot in (".ai", ".claude", ".codex"):
            p = os.path.join(d, dot, NAME)
            if os.path.isfile(p):
                t = open(p, encoding="utf-8").read()
                return front(t).get("type") or guess_type(here), f"project file {p}", t
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    home = os.path.expanduser(os.environ.get("AI_IT_HOME") or "~/.ai")
    p = os.path.join(home, NAME)
    if os.path.isfile(p):
        t = open(p, encoding="utf-8").read()
        return front(t).get("type") or guess_type(here), f"personal default {p}", t
    kind = guess_type(here)
    return kind, f"package default for {kind}", template(kind, os.path.basename(here) or "project")


def problems(text):
    out = []
    ids = CRIT.findall(text)
    if not ids:
        out.append("no criteria found: each one needs a '## C<n> <title>' heading")
    seen = set()
    for cid, _ in ids:
        if cid in seen:
            out.append(f"{cid} appears twice")
        seen.add(cid)
    kind = front(text).get("type")
    if kind and kind not in TYPES:
        out.append(f"type '{kind}' is not one of {', '.join(TYPES)}")
    return out


def cmd_init(a):
    kind = a.type or guess_type(a.project)
    d = os.path.join(a.project, ".ai")
    p = os.path.join(d, NAME)
    if os.path.exists(p):
        sys.exit(f"{p} already exists; edit it, or delete it to start again")
    os.makedirs(d, exist_ok=True)
    open(p, "w", encoding="utf-8").write(template(kind, os.path.basename(os.path.abspath(a.project))))
    print(f"created {p} ({kind}). Edit it; every /review of this project will use it.")


def cmd_show(a):
    kind, label, text = resolve(a.target)
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    print(f"criteria for {os.path.abspath(a.target)}")
    print(f"  from   {label}")
    print(f"  type   {kind}")
    print(f"  sha256 {h}   (recorded with the review, so it shows exactly which criteria were applied)")
    for k in ("scope", "exclude", "sources"):
        v = front(text).get(k)
        if v:
            print(f"  {k:<7}{v}")
    print()
    for cid, title in CRIT.findall(text):
        print(f"  {cid:<4} {title}")
    if a.full:
        print("\n" + text)


def cmd_check(a):
    p = problems(open(a.file, encoding="utf-8").read())
    for x in p:
        print(f"  problem  {x}")
    print("OK" if not p else f"{len(p)} problem(s)")
    return 1 if p else 0


def cmd_selftest(a):
    import tempfile
    root = tempfile.mkdtemp(prefix="criteria-selftest-")
    os.environ["AI_IT_HOME"] = os.path.join(root, "home", ".ai")
    proj = os.path.join(root, "proj"); os.makedirs(os.path.join(proj, "src", "pkg"))
    open(os.path.join(proj, "src", "pkg", "a.py"), "w", encoding="utf-8").write("x = 1\n")
    checks = []
    k, label, t = resolve(os.path.join(proj, "src"))
    checks.append(("with no file, the package default for the guessed type applies",
                   k == "software" and label.startswith("package default")))
    os.makedirs(os.environ["AI_IT_HOME"])
    open(os.path.join(os.environ["AI_IT_HOME"], NAME), "w", encoding="utf-8").write(
        "---\ntype: documents\n---\n## C1 Mine\nx\n")
    checks.append(("a personal default overrides the package default",
                   resolve(proj)[1].startswith("personal default")))
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        cmd_init(argparse.Namespace(project=proj, type=None))
    k, label, t = resolve(os.path.join(proj, "src", "pkg"))
    checks.append(("a project file, found from any subfolder, overrides both", label.startswith("project file")))
    checks.append(("the generated project file is well formed", not problems(t)))
    checks.append(("a malformed file is reported", bool(problems("no headings here\n"))))
    for n, ok in checks:
        print(f"  {'pass' if ok else 'FAIL'}  {n}")
    bad = sum(1 for _, ok in checks if not ok)
    print(f"\n{len(checks) - bad} of {len(checks)} checks passed")
    return 1 if bad else 0


def main():
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description="Review criteria: create, resolve, check.")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("init"); p.add_argument("project"); p.add_argument("--type", choices=TYPES)
    p.set_defaults(fn=cmd_init)
    p = sp.add_parser("show"); p.add_argument("target"); p.add_argument("--full", action="store_true")
    p.set_defaults(fn=cmd_show)
    p = sp.add_parser("check"); p.add_argument("file"); p.set_defaults(fn=cmd_check)
    sp.add_parser("selftest").set_defaults(fn=cmd_selftest)
    a = ap.parse_args()
    return a.fn(a) or 0


if __name__ == "__main__":
    sys.exit(main())
