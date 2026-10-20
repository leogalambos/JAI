#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Demo kit for the IS/IT role library: practice projects with known, deliberately planted flaws.

    demo.py list                     the demo projects and which commands each is for
    demo.py setup [--to DIR]         copy them to DIR (default ~/it-role-demo); gives invoice-service a git history
    demo.py reset NAME [--to DIR]    put one project back to its starting state, to repeat a demo
    demo.py check                    verify the demos and the tools work, without Claude (about ten seconds)

The flaws are listed in the guide (~/.ai/it-role-house/GUIDE.md), never inside the projects, so that a
reviewer cannot find them by reading an answer key.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECTS = os.path.join(HERE, "projects")
LIB = os.path.dirname(HERE)
TOOLS = os.path.join(LIB, "tools")
DEFAULT_TO = os.path.join(os.path.expanduser("~"), "it-role-demo")
ABOUT = {
    "invoice-service": "a small Python service with planted flaws — /analyse /criteria /review /rework /develop /govern "
                       "/research /layered",
    "policy-docs": "a security policy library with planted flaws — /analyse /review /rework /govern",
    "acme-pay": "material about a fictional potential client — /sabsa (prepare, create, questions, document)",
}


def git(repo, *args, author=("Dana Developer", "dana@example.com"), date=None):
    """Run git arguments in repo with fictional author/date; return captured process result."""
    env = dict(os.environ, GIT_AUTHOR_NAME=author[0], GIT_AUTHOR_EMAIL=author[1],
               GIT_COMMITTER_NAME=author[0], GIT_COMMITTER_EMAIL=author[1])
    if date:
        env.update(GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    return subprocess.run(["git", "-C", repo, *args], env=env, capture_output=True, encoding="utf-8", errors="replace")


def history(repo):
    """Create a short history in repo with governance gaps: a direct commit to main, a feature merged by its own
    author without review, no tags, no CODEOWNERS, no changelog."""
    if not shutil.which("git"):
        print("  note: git is not installed, so invoice-service has no history; /govern will have less to assess")
        return
    dana, omar = ("Dana Developer", "dana@example.com"), ("Omar Ops", "omar@example.com")
    rd = lambda rel: open(os.path.join(repo, rel), encoding="utf-8").read()
    w = lambda rel, t: open(os.path.join(repo, rel), "w", encoding="utf-8").write(t)
    final = {rel: rd(rel) for rel in ("app/api.py", "app/config.py", "app/invoices.py", "app/payments.py",
                                      "tests/test_payments.py")}
    for rel in ("app/payments.py", "tests/test_payments.py"):            # the payment client comes later
        os.remove(os.path.join(repo, rel))
    # As first written, the discount applied from the threshold inclusive, as the README promises.
    later = ('    subtotal = sum(line_total(l["quantity"], l["unit_price"]) for l in lines)\n'
             '    if subtotal > DISCOUNT_THRESHOLD:')
    first = ('    subtotal = 0\n    for line in lines:\n        subtotal += line_total(line["quantity"], line["unit_price"])\n'
             '    if subtotal >= DISCOUNT_THRESHOLD:')
    if later not in final["app/invoices.py"]:
        raise SystemExit("demo.py: the discount code in app/invoices.py changed; update the history")
    first_invoices = final["app/invoices.py"].replace(later, first)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "add", "README.md", "requirements.txt", ".gitignore")
    git(repo, "commit", "-q", "-m", "Initial project skeleton", author=dana, date="2026-06-02T09:00:00")
    w("app/api.py", final["app/api.py"].split("\n\ndef delete_invoice")[0] + "\n")
    w("app/config.py", final["app/config.py"].replace("demo-gateway-key-7f3a9c2e5b81d4f6", "demo-gateway-key-0b51e27aa94c3d18"))
    w("app/invoices.py", first_invoices)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "Invoice creation, storage and API", author=dana, date="2026-06-20T14:30:00")
    git(repo, "checkout", "-q", "-b", "feature/delete-invoice")
    w("app/api.py", final["app/api.py"])
    git(repo, "commit", "-q", "-am", "Add delete endpoint", author=omar, date="2026-07-08T16:10:00")
    git(repo, "checkout", "-q", "main")
    git(repo, "merge", "-q", "--no-ff", "feature/delete-invoice", "-m", "Merge branch 'feature/delete-invoice'",
        author=omar, date="2026-07-08T16:12:00")                        # merged by its own author, two minutes later
    git(repo, "branch", "-q", "-D", "feature/delete-invoice")
    w("app/invoices.py", final["app/invoices.py"])                      # a "simplification" that moves the boundary
    git(repo, "commit", "-q", "-am", "Simplify discount calculation", author=omar, date="2026-07-21T11:05:00")
    w("app/payments.py", final["app/payments.py"])
    w("tests/test_payments.py", final["tests/test_payments.py"])
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "Add payment client", author=dana, date="2026-08-03T10:20:00")
    w("app/config.py", final["app/config.py"])
    git(repo, "commit", "-q", "-am", "hotfix: rotate gateway key", author=omar, date="2026-08-14T23:41:00")


def copy_project(name, to):
    """Restore legacy fixture name beneath to, replacing it; return its directory path."""
    dst = os.path.join(to, name)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(os.path.join(PROJECTS, name), dst)
    if name == "invoice-service":
        history(dst)
    return dst


def cmd_list(a):
    """Print legacy project descriptions; a is the parsed CLI namespace."""
    for name in sorted(os.listdir(PROJECTS)):
        print(f"  {name:<17} {ABOUT.get(name, '')}")


def cmd_setup(a):
    """Copy legacy projects to a.to; reject existing projects unless a.force is true."""
    os.makedirs(a.to, exist_ok=True)
    existing = [n for n in os.listdir(PROJECTS) if os.path.exists(os.path.join(a.to, n))]
    if existing and not a.force:
        sys.exit(f"{', '.join(existing)} already exist in {a.to}. Use 'reset NAME' to restore one, or --force to "
                 "replace them all.")
    for name in sorted(os.listdir(PROJECTS)):
        print(f"  {copy_project(name, a.to)}")
    print(f"\nDemo projects are in {a.to}. Open Claude Code there and follow the guide:  /guide")


def cmd_reset(a):
    """Explicitly restore legacy a.name beneath a.to; exit for an unknown project."""
    if a.name not in os.listdir(PROJECTS):
        sys.exit(f"no demo project '{a.name}'; choose from {', '.join(sorted(os.listdir(PROJECTS)))}")
    print(f"restored {copy_project(a.name, a.to)} to its starting state")


def run_tool(*args, cwd=None, env=None):
    """Run local Python args in cwd with optional env additions; return captured process result."""
    return subprocess.run([sys.executable, *args], capture_output=True, encoding="utf-8", errors="replace", cwd=cwd,
                          env=dict(os.environ, **(env or {})))


def cmd_check(a):
    """Exercise legacy fixtures in a temporary directory; return zero only when checks pass."""
    work = tempfile.mkdtemp(prefix="it-role-demo-check-")
    results = []
    ok = lambda name, cond: results.append((name, bool(cond)))
    for name in os.listdir(PROJECTS):
        copy_project(name, work)
    s = run_tool(os.path.join(TOOLS, "doc_survey.py"), os.path.join(work, "policy-docs"), "--json").stdout
    import json
    d = json.loads(s) if s.strip().startswith("{") else {}
    ok("policy-docs: the survey finds the broken link", any(b["target"] == "data-classification.md" for b in d.get("broken_links", [])))
    ok("policy-docs: ... the document with no owner", "password-standard.md" in d.get("no_owner", []))
    ok("policy-docs: ... the overdue review", "access-control.md" in d.get("review_overdue", []))
    ok("policy-docs: ... the double H1 and the TODO", "incident-response.md" in d.get("multiple_h1", []) and d.get("markers", {}).get("TODO"))
    ok("policy-docs: ... the orphans and the duplicate", "remote-work.md" in d.get("orphans", []) and d.get("duplicates"))
    rs = os.path.join(LIB, os.pardir, "skills", "it-roles-quality-and-testing", "scripts", "repo_survey.py")
    if os.path.isfile(rs):
        r = run_tool(rs, os.path.join(work, "invoice-service"))
        ok("invoice-service: the repository survey runs" + (" and sees the git history" if shutil.which("git") else ""),
           r.returncode == 0 and ("commits" in r.stdout or not shutil.which("git")))
    r = run_tool(os.path.join(TOOLS, "criteria.py"), "show", os.path.join(work, "invoice-service"),
                 env={"AI_IT_HOME": os.path.join(work, "nohome")})
    ok("invoice-service: review criteria resolve to the software default", "package default for software" in r.stdout)
    lib = os.path.join(work, "acme-pay", "sabsa")
    r = run_tool(os.path.join(TOOLS, "sabsa.py"), "init", lib, "--name", "ACME Pay", "--organisation", "ACME Pay s.r.o.",
                 "--scope", "partner payments API", "--owner", "Chief Security Architect")
    for f in os.listdir(os.path.join(work, "acme-pay", "client-material")):
        shutil.copy(os.path.join(work, "acme-pay", "client-material", f), os.path.join(lib, "00-sources", f))
    r2 = run_tool(os.path.join(TOOLS, "sabsa.py"), "sources", lib)
    ok("acme-pay: a SABSA library initialises and takes the client material in", r.returncode == 0 and "3 source file(s)" in r2.stdout)
    r = run_tool(os.path.join(TOOLS, "sabsa.py"), "document", lib, "--out", os.path.join(work, "A.md"))
    ok("acme-pay: the architecture document renders", r.returncode == 0 and os.path.isfile(os.path.join(work, "A.md")))
    r = run_tool(os.path.join(TOOLS, "sabsa.py"), "documents", lib)
    ok("acme-pay: 3.2 specialised document views are discoverable", r.returncode == 0 and "framework-mapping" in r.stdout and "transition-architecture" in r.stdout)
    r = run_tool(os.path.join(TOOLS, "sabsa.py"), "metamodel")
    ok("acme-pay: 3.2 lifecycle schema is active", r.returncode == 0 and "Lifecycle model 3.2" in r.stdout)
    inv = os.path.join(work, "invoice-service")
    if shutil.which("git"):
        repro = (f'"{sys.executable}" -c "from app.invoices import total; import sys; '
                 'sys.exit(0 if total([{\'quantity\': 1, \'unit_price\': 1000.0}]) == 950.0 else 1)"')
        r = run_tool(os.path.join(TOOLS, "defect.py"), "bisect", "--good", "HEAD~4", "--cmd", repro, "--repo", inv)
        ok("invoice-service: bisecting the discount regression finds 'Simplify discount calculation'",
           r.returncode == 0 and "Simplify discount calculation" in r.stdout.split("FIRST BAD COMMIT")[-1])
    pay = f'"{sys.executable}" -c "from app import payments; import sys; sys.exit(0 if payments.charge(25) == \'approved\' else 1)"'
    r = run_tool(os.path.join(TOOLS, "defect.py"), "repeat", pay, "-n", "20", "--cwd", inv)
    ok("invoice-service: the payment defect is intermittent", "INTERMITTENT" in r.stdout)
    for tool in ("findings.py", "sabsa.py", "criteria.py"):
        r = run_tool(os.path.join(TOOLS, tool), "selftest")
        ok(f"{tool} self-test: {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else 'no output'}", r.returncode == 0)
    shutil.rmtree(work, ignore_errors=True)
    for n, good in results:
        print(f"  {'pass' if good else 'FAIL'}  {n}")
    bad = sum(1 for _, g in results if not g)
    print(f"\n{len(results) - bad} of {len(results)} checks passed" + ("" if bad else " — the demos are ready to use"))
    return 1 if bad else 0


def main():
    """Dispatch legacy demo operations or safe catalog exercises; return exit status."""
    if len(sys.argv) > 1 and sys.argv[1] in {
        "scenarios", "describe", "scenario", "reset-scenario", "check-scenarios"
    }:
        from scenario_demo import main as scenario_main
        return scenario_main(sys.argv[1:])
    ap = argparse.ArgumentParser(description="Demo kit for the IS/IT role library.")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("list").set_defaults(fn=cmd_list)
    p = sp.add_parser("setup"); p.add_argument("--to", default=DEFAULT_TO); p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_setup)
    p = sp.add_parser("reset"); p.add_argument("name"); p.add_argument("--to", default=DEFAULT_TO)
    p.set_defaults(fn=cmd_reset)
    sp.add_parser("check").set_defaults(fn=cmd_check)
    sp.add_parser("selftest").set_defaults(fn=cmd_check)
    a = ap.parse_args()
    return a.fn(a) or 0


if __name__ == "__main__":
    sys.exit(main())
