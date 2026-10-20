#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Defect analysis tools, for the three comparisons of the defect analysis standard
(it-role-library/standards/defect-analysis.md): last known good, working analogue, timing.

    defect.py repeat  "CMD" [-n 30] [--parallel 1] [--timeout 60] [--cwd DIR]
        run a reproduction many times: failures, failure rate, durations — intermittency is evidence
    defect.py bisect  --good REF [--bad HEAD] --cmd "CMD" [--with FILE ...] [--repo DIR]
        find the first bad commit, in a separate git worktree: your working tree is never touched
    defect.py changes --good REF [--bad HEAD] [--repo DIR]
        everything that changed between two states: code, tests, dependencies, configuration, infrastructure
    defect.py compare WORKING FAILING          (each: FILE or FILE::name)
        diff a working analogue against the failing code: conditions, calls, constants and timing that differ
    defect.py timing  PATH...
        timing-sensitive constructs: timeouts, sleeps, async work, shared state, clocks, schedules and expiry
    defect.py analysis validate|render|findings FILE|-
        check an analysis has every required part; render it as a report; turn its root cause into a finding
    defect.py selftest

The reproduction command exits 0 when the behaviour is correct and non-zero when the defect occurs (125 = skip).
"""
import argparse
import ast
import difflib
import json
import os
import re
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import time

for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]


class DefectError(Exception):
    """A usage or environment problem, reported without a traceback."""


def sh(cmd, cwd=None, timeout=None):
    """Run a shell command; return (exit code, combined output, seconds). A timeout counts as exit code 124."""
    t0 = time.monotonic()
    try:
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, encoding="utf-8", errors="replace",
                           timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or ""), time.monotonic() - t0
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        return 124, out + f"\n[timed out after {timeout}s]", time.monotonic() - t0


def git(repo, *args):
    """Run git in repo and return its output; raise DefectError on failure."""
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise DefectError(f"git {' '.join(args[:3])}: {(r.stderr or r.stdout).strip()[:300]}")
    return r.stdout


# ------------------------------------------------------------------------------------------- repeat
def cmd_repeat(a):
    """Run the reproduction n times and summarise determinism and duration."""
    results = []
    if a.parallel > 1:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(a.parallel) as ex:
            results = list(ex.map(lambda _: sh(a.command, a.cwd, a.timeout), range(a.n)))
    else:
        results = [sh(a.command, a.cwd, a.timeout) for _ in range(a.n)]
    fails = [r for r in results if r[0] != 0]
    durs = [r[2] for r in results]
    first_lines = {}
    for code, out, _ in fails:
        line = next((l.strip() for l in reversed(out.strip().splitlines()) if l.strip()), f"exit {code}")
        first_lines[line[:120]] = first_lines.get(line[:120], 0) + 1
    summary = {"runs": a.n, "failures": len(fails), "failure_rate": round(len(fails) / a.n, 3),
               "parallel": a.parallel, "seconds": {"min": round(min(durs), 3), "median": round(statistics.median(durs), 3),
                                                   "max": round(max(durs), 3)},
               "failure_messages": first_lines}
    if a.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        kind = ("deterministic: fails every time" if len(fails) == a.n else "deterministic: never fails" if not fails
                else "INTERMITTENT: timing, ordering, shared state or the environment take part — examine them")
        print(f"{a.n} runs{f' ({a.parallel} in parallel)' if a.parallel > 1 else ''}: {len(fails)} failed "
              f"({summary['failure_rate']:.0%}) — {kind}")
        print(f"duration: min {summary['seconds']['min']}s, median {summary['seconds']['median']}s, "
              f"max {summary['seconds']['max']}s")
        for msg, n in sorted(first_lines.items(), key=lambda x: -x[1]):
            print(f"  ×{n}  {msg}")
    return 0


# ------------------------------------------------------------------------------------------- bisect
def _first_bad_commit(output):
    """Return the SHA from legacy or Git 2.56 quoted bisect output, or None."""
    match = re.search(r"^([0-9a-f]{40}) is the first (?:bad|'bad') commit", output, re.M)
    return match.group(1) if match else None


def cmd_bisect(a):
    """Find the first bad commit between good and bad, in a temporary worktree."""
    repo = os.path.abspath(a.repo)
    git(repo, "rev-parse", "--git-dir")
    good, bad = git(repo, "rev-parse", a.good).strip(), git(repo, "rev-parse", a.bad).strip()
    tmp = tempfile.mkdtemp(prefix="defect-bisect-")
    wt = os.path.join(tmp, "wt")
    extra = [(os.path.relpath(os.path.abspath(f), repo), open(f, "rb").read()) for f in (a.with_ or [])]
    steps = []

    def run_at(rev=None):
        if rev:
            git(wt, "checkout", "-q", "--detach", rev)
        for rel, data in extra:                     # a reproduction that is not in history is copied in
            os.makedirs(os.path.dirname(os.path.join(wt, rel)) or wt, exist_ok=True)
            open(os.path.join(wt, rel), "wb").write(data)
        code, out, secs = sh(a.cmd, wt, a.timeout)
        return code, out
    try:
        git(repo, "worktree", "add", "-q", "--detach", wt, bad)
        code_good, out_good = run_at(good)
        code_bad, out_bad = run_at(bad)
        if code_good != 0:
            raise DefectError(f"the 'good' state {a.good} also fails (exit {code_good}): pick an earlier good state, or "
                              f"check the command.\n{out_good.strip()[-400:]}")
        if code_bad == 0:
            raise DefectError(f"the 'bad' state {a.bad} passes: the command does not reproduce the defect there.")
        git(wt, "bisect", "start", bad, good)
        first = None
        for _ in range(64):
            rev = git(wt, "rev-parse", "HEAD").strip()
            code, _ = run_at()
            verdict = "skip" if code == 125 else "good" if code == 0 else "bad"
            subject = git(wt, "log", "-1", "--format=%s", rev).strip()
            steps.append((rev[:10], verdict, subject))
            out = git(wt, "bisect", verdict)
            first = _first_bad_commit(out)
            if first:
                break
            if "only skipped commits left" in out:
                break
        if not first:
            raise DefectError("bisection did not converge (too many skipped commits?)")
        info = git(repo, "show", "--stat", "--format=%H%n%an <%ae>%n%ad%n%s%n%n%b", first)
        if a.json:
            print(json.dumps({"good": good, "bad": bad, "first_bad": first, "steps": steps, "commit": info}, indent=2))
        else:
            print(f"good {good[:10]} ({a.good}) passes; bad {bad[:10]} ({a.bad}) fails.")
            for rev, verdict, subject in steps:
                print(f"  {rev}  {verdict:<4}  {subject[:70]}")
            print("\nFIRST BAD COMMIT\n" + "\n".join("  " + l for l in info.strip().splitlines()))
            print("\nThis is where the defect entered; explain why this change causes it before calling it the root cause.")
        return 0
    finally:
        subprocess.run(["git", "-C", wt, "bisect", "reset"], capture_output=True)
        subprocess.run(["git", "-C", repo, "worktree", "remove", "--force", wt], capture_output=True)
        subprocess.run(["git", "-C", repo, "worktree", "prune"], capture_output=True)
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------------------------------- changes
CATEGORIES = [
    ("dependencies", re.compile(r"(^|/)(pom\.xml|build\.gradle(\.kts)?|package(-lock)?\.json|yarn\.lock|pnpm-lock\.yaml|"
                                r"requirements[^/]*\.txt|pyproject\.toml|poetry\.lock|Pipfile(\.lock)?|go\.(mod|sum)|"
                                r"Cargo\.(toml|lock)|[^/]+\.csproj|packages\.lock\.json|Gemfile(\.lock)?)$")),
    ("tests", re.compile(r"(^|/)(src/test|tests?|__tests__|spec)/|(Test|Tests|IT)\.\w+$|(^|/)test_[^/]+$|_test\.\w+$|"
                         r"\.(test|spec)\.\w+$")),
    ("configuration", re.compile(r"\.(ya?ml|properties|ini|cfg|conf|toml|env)$|(^|/)\.env|application[^/]*\.\w+$|"
                                 r"(^|/)(config|conf|settings)/")),
    ("infrastructure", re.compile(r"(^|/)(Dockerfile|docker-compose[^/]*|Jenkinsfile|Makefile)$|\.tf$|(^|/)(k8s|helm|"
                                  r"charts|deploy|\.github/workflows|\.gitlab-ci)[/.]")),
    ("database", re.compile(r"\.sql$|(^|/)(migrations?|db/changelog|flyway|liquibase)/")),
]


def cmd_changes(a):
    """Everything that changed between good and bad, by category, with dependency version changes."""
    repo = os.path.abspath(a.repo)
    rng = f"{a.good}..{a.bad}"
    commits = git(repo, "log", "--format=%h %ad %an: %s", "--date=short", rng).strip().splitlines()
    files = [l.split("\t") for l in git(repo, "diff", "--name-status", a.good, a.bad).strip().splitlines() if l]
    groups = {}
    for parts in files:
        path = parts[-1]
        cat = next((c for c, rx in CATEGORIES if rx.search(path)), "code")
        groups.setdefault(cat, []).append(f"{parts[0][0]} {path}")
    print(f"{len(commits)} commit(s) from {a.good} to {a.bad}:")
    for c in commits[:40]:
        print(f"  {c}")
    for cat in ("code", "tests", "dependencies", "configuration", "infrastructure", "database"):
        if cat in groups:
            print(f"\n{cat} ({len(groups[cat])}):")
            for f in groups[cat][:40]:
                print(f"  {f}")
    for f in groups.get("dependencies", []):
        diff = git(repo, "diff", "-U0", a.good, a.bad, "--", f.split(" ", 1)[1])
        vers = [l for l in diff.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))
                and re.search(r"\d+\.\d+", l)]
        if vers:
            print(f"\nversion changes in {f.split(' ', 1)[1]}:")
            for l in vers[:20]:
                print(f"  {l.strip()}")
    print("\nCode is not the only thing that changes: also compare the runtime, the data and its volume, feature flags "
          "and the environment, which version control does not see.")
    return 0


# ------------------------------------------------------------------------------------------- compare
def extract(spec):
    """The text of FILE, or of the named function or method in FILE::name."""
    path, _, name = spec.partition("::")
    src = open(path, encoding="utf-8", errors="replace").read()
    if not name:
        return src, os.path.basename(path)
    if path.endswith(".py"):
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == name:
                return ast.get_source_segment(src, node), name
        raise DefectError(f"no function or class '{name}' in {path}")
    m = re.search(rf"^[^\n;]*\b(def|func|fun|function)?\s*{re.escape(name)}\s*[(<][^\n]*$", src, re.M)
    if not m:
        raise DefectError(f"no declaration of '{name}' in {path}")
    i = src.find("{", m.start())
    depth, j = 0, i
    while 0 <= j < len(src):
        depth += {"{": 1, "}": -1}.get(src[j], 0)
        if depth == 0:
            break
        j += 1
    return src[m.start():j + 1], name


def normalise(text, name):
    """Lines without comments, blank lines or the unit's own name, so that analogues compare by substance."""
    out = []
    for line in text.splitlines():
        line = re.sub(r"(//|#).*$", "", line).strip()
        line = re.sub(rf"\b{re.escape(name)}\b", "<unit>", line)
        if line and not line.startswith(('"""', "'''", "*", "/*")):
            out.append(re.sub(r"\s+", " ", line))
    return out


TIMING_WORDS = re.compile(r"timeout|sleep|await|async|future|thread|lock|synchron|volatile|atomic|retry|backoff|ttl|"
                          r"expir|schedul|cron|clock|now\(|currentTimeMillis|deadline|Duration|TimeUnit", re.I)


def cmd_compare(a):
    """Diff a working analogue against the failing code, and name the kinds of difference."""
    wt, wn = extract(a.working)
    ft, fn = extract(a.failing)
    w, f = normalise(wt, wn), normalise(ft, fn)
    cond = lambda ls: {l for l in ls if re.match(r"(if|elif|else if|unless|guard|assert|require|check|when)\b|"
                                                 r"(raise|throw|return)\b.*(not found|denied|forbidden|error|None|null)", l, re.I)}
    calls = lambda ls: set(re.findall(r"([A-Za-z_][\w.]*)\s*\(", " ".join(ls))) - {"if", "for", "while", "return", "<unit>"}
    consts = lambda ls: set(re.findall(r"(?<![\w.])(\d+(?:\.\d+)?|\"[^\"]*\"|'[^']*')", " ".join(ls)))
    print(f"working: {a.working}   failing: {a.failing}\n")
    sections = [
        ("conditions and guards only in the working one", cond(w) - cond(f)),
        ("conditions and guards only in the failing one", cond(f) - cond(w)),
        ("calls only in the working one", calls(w) - calls(f)),
        ("calls only in the failing one", calls(f) - calls(w)),
        ("constants that differ (working → failing)", None),
        ("timing-related lines that differ", {l for l in set(w) ^ set(f) if TIMING_WORDS.search(l)}),
    ]
    for title, items in sections:
        if title.startswith("constants"):
            cw, cf = consts(w) - consts(f), consts(f) - consts(w)
            if cw or cf:
                print(f"{title}:\n  {', '.join(sorted(cw)) or '—'}  →  {', '.join(sorted(cf)) or '—'}")
            continue
        if items:
            print(f"{title}:")
            for x in sorted(items):
                print(f"  {x}")
    print("\nfull difference (working → failing):")
    for line in difflib.unified_diff(w, f, "working", "failing", lineterm="", n=1):
        print(f"  {line}")
    print("\nEach difference is a candidate. Confirm the decisive one by transplanting it: introducing it should break "
          "the working case, or removing it should fix the failing one.")
    return 0


# ------------------------------------------------------------------------------------------- timing
TIMING = [
    ("timeout", re.compile(r"(?i:\w*time_?out\w*)\s*[=:(]\s*[\w.]+|[Tt]imeout\(|connectTimeout|readTimeout|socketTimeout|"
                           r"deadline|Duration\.of\w+\(|\.orTimeout\(|setTimeout\("),
     "Is it shorter than the operation's measured duration under real conditions? What happens when it fires?"),
    ("sleep", re.compile(r"Thread\.sleep\(|time\.sleep\(|asyncio\.sleep\(|\bsleep\(\d|TimeUnit\.\w+\.sleep"),
     "A sleep assumes something will be done by then. What if it is not?"),
    ("async work", re.compile(r"CompletableFuture|supplyAsync|runAsync|ExecutorService|\.submit\(|@Async|"
                              r"asyncio\.create_task|ensure_future|threading\.Thread|concurrent\.futures|\bgo func|"
                              r"\bgo \w+\(|Task\.Run|async void|new Promise|\.then\("),
     "Is its completion awaited, joined or checked before its result is used, and before the process ends?"),
    ("shared state", re.compile(r"\bsynchronized\b|\bvolatile\b|Atomic\w+|ReentrantLock|threading\.Lock|"
                                r"ConcurrentHashMap|sync\.Mutex|\bglobal \w+|static (?!final)[\w<>\[\]]+ \w+\s*(=|;)"),
     "Can two threads, requests or consumers interleave here? Is there a check-then-act on shared state?"),
    ("clock", re.compile(r"System\.currentTimeMillis|new Date\(\)|LocalDate(Time)?\.now\(\)|Instant\.now\(\)|"
                         r"ZonedDateTime\.now\(\)|datetime\.(now|utcnow)\(|time\.time\(\)|Date\.now\(\)|DateTime\.Now|"
                         r"time\.Now\(\)"),
     "Wall-clock time: time zones, daylight saving, month and year boundaries, skew between machines. Inject a clock."),
    ("schedule or expiry", re.compile(r"@Scheduled|\bcron\b|\bttl\b|TTL|expir|expiresAt|maxAge|refresh|\bretry|Retry|"
                                      r"backoff|Backoff|evict", re.I),
     "What happens at the boundary: just before, at, and just after the scheduled time or expiry?"),
]


def cmd_timing(a):
    """List timing-sensitive constructs in the given code, each with the question it raises."""
    hits = []
    for p in a.paths:
        files = [os.path.join(dp, f) for dp, ds, fs in os.walk(p) for f in fs] if os.path.isdir(p) else [p]
        for f in files:
            if not re.search(r"\.(java|kt|py|ts|tsx|js|mjs|cs|go|rb|scala)$", f) or re.search(r"[\\/](node_modules|"
                                                                                                r"target|build|\.git)[\\/]", f):
                continue
            for i, line in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
                for cat, rx, q in TIMING:
                    if rx.search(line):
                        hits.append((f, i, cat, line.strip()[:90], q))
    for cat, _, q in TIMING:
        mine = [h for h in hits if h[2] == cat]
        if mine:
            print(f"\n{cat} — {q}")
            for f, i, _, text, _ in mine[:25]:
                print(f"  {f}:{i}  {text}")
    if not hits:
        print("no timing-sensitive constructs found in the given code; timing may still enter through its "
              "dependencies, the network or the environment")
    else:
        print(f"\n{len(hits)} construct(s). Each is a hypothesis to test, not a finding: vary the timing deliberately "
              "(delays, a slow dependency, parallel runs, a fixed clock) and see whether the defect follows.")
    return 0


# ------------------------------------------------------------------------------------------- analysis
LENS_KEYS = {"last_known_good": ("last_good", "first_bad"), "working_analogue": ("analogue", "decisive_difference"),
             "timing": ()}


def validate(doc):
    """Return the list of problems that keep an analysis from going forward to a fix."""
    p = []
    req = lambda obj, path: [f"missing: {path}.{k}" for k in obj[1] if not (isinstance(obj[0], dict)
                                                                         and str(obj[0].get(k, "")).strip())]
    p += req((doc, ("title",)), "analysis")
    p += req((doc.get("symptom"), ("observed", "expected")), "symptom")
    rep = doc.get("reproduction") or {}
    p += req((rep, ("command",)), "reproduction")
    det = rep.get("determinism") or {}
    runs, fails = det.get("runs"), det.get("failures")
    if not isinstance(runs, int) or not isinstance(fails, int) or runs < 1 or not 0 <= fails <= runs:
        p.append("reproduction.determinism needs runs (≥ 1) and failures (0…runs): measure it with 'defect.py repeat'")
    intermittent = isinstance(runs, int) and isinstance(fails, int) and 0 < fails < runs
    lenses = doc.get("lenses") or {}
    for lens, keys in LENS_KEYS.items():
        L = lenses.get(lens)
        if not isinstance(L, dict):
            p.append(f"missing comparison: lenses.{lens} — carry it out, or mark it not-applicable with the reason")
            continue
        st = L.get("status")
        if st == "done":
            if len(str(L.get("evidence", "")).strip()) < 20:
                p.append(f"lenses.{lens}: done, but no evidence")
            p += [f"lenses.{lens}: done, but no {k}" for k in keys if not str(L.get(k, "")).strip()]
        elif st == "not-applicable":
            if len(str(L.get("reason", "")).strip()) < 20:
                p.append(f"lenses.{lens}: not applicable needs a real reason")
            if lens == "timing" and intermittent:
                p.append("lenses.timing cannot be not-applicable: the defect is intermittent "
                         f"({fails} of {runs} runs), which is itself evidence that timing or ordering take part")
            if lens == "timing" and isinstance(runs, int) and runs < 10:
                p.append("lenses.timing: not applicable requires at least 10 repeated runs as evidence")
        else:
            p.append(f"lenses.{lens}.status must be 'done' or 'not-applicable'")
    hyps = doc.get("hypotheses") or []
    if len(hyps) < 2:
        p.append("hypotheses: at least two competing hypotheses, each with a prediction and an experiment")
    for i, h in enumerate(hyps, 1):
        p += req((h, ("hypothesis", "prediction", "experiment", "outcome")), f"hypotheses[{i}]")
        if h.get("outcome") not in ("confirmed", "refuted", "open"):
            p.append(f"hypotheses[{i}].outcome must be confirmed, refuted or open")
    if not any(h.get("outcome") == "confirmed" for h in hyps):
        p.append("no hypothesis is confirmed: the root cause is not yet established")
    rc = doc.get("root_cause") or {}
    p += req((rc, ("statement", "location", "trigger")), "root_cause")
    if rc.get("location") and not re.search(r":\d+", str(rc["location"])):
        p.append("root_cause.location must be file:line")
    p += req((doc.get("fix"), ("proposal", "regression_test")), "fix")
    if doc.get("confidence") not in ("high", "medium", "low"):
        p.append("confidence must be high, medium or low")
    if doc.get("confidence") in ("medium", "low") and not str(doc.get("unknowns", "")).strip():
        p.append("unknowns: say what is still unknown, since confidence is not high")
    return p


def load_doc(src):
    raw = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    return json.loads(raw[raw.find("{"):raw.rfind("}") + 1])


def render(doc):
    """The analysis as a Markdown report."""
    L = doc["lenses"]; det = doc["reproduction"]["determinism"]; rc = doc["root_cause"]
    lens = lambda k, title: (f"### {title}\n\n" + (f"{L[k].get('evidence', '')}\n" + "".join(
        f"\n- **{x.replace('_', ' ')}:** {L[k][x]}" for x in LENS_KEYS[k] if L[k].get(x))
        if L[k]["status"] == "done" else f"_Not applicable:_ {L[k].get('reason', '')}") + "\n")
    out = [f"# Defect analysis: {doc['title']}", "",
           f"**Observed:** {doc['symptom']['observed']}  ", f"**Expected:** {doc['symptom']['expected']}  ",
           f"**Environment:** {doc['symptom'].get('environment', '—')}", "", "## Reproduction", "",
           f"```\n{doc['reproduction']['command']}\n```", "",
           f"Failed **{det['failures']} of {det['runs']}** runs"
           + (" — intermittent." if 0 < det["failures"] < det["runs"] else ".") + (f" {det.get('notes', '')}" if det.get("notes") else ""),
           "", "## The three comparisons", "",
           lens("last_known_good", "A. Against the last known good state"),
           lens("working_analogue", "B. Against a working analogue"),
           lens("timing", "C. Timing and time-dependent behaviour"),
           "## Hypotheses", "", "| Hypothesis | Prediction | Experiment | Outcome |", "| --- | --- | --- | --- |"]
    for h in doc["hypotheses"]:
        out.append("| " + " | ".join(str(h[k]).replace("|", "\\|") for k in ("hypothesis", "prediction", "experiment", "outcome")) + " |")
    out += ["", "## Root cause", "", f"{rc['statement']}", "", f"- **Location:** `{rc['location']}`",
            f"- **Trigger:** {rc['trigger']}"]
    out += [f"- **Contributing:** {c}" for c in rc.get("contributing", [])]
    out += ["", "## Fix", "", doc["fix"]["proposal"], "", f"**Regression test:** {doc['fix']['regression_test']}", "",
            f"**Confidence:** {doc['confidence']}" + (f" — unknowns: {doc['unknowns']}" if doc.get("unknowns") else "")]
    return "\n".join(out) + "\n"


def cmd_analysis(a):
    """validate | render | findings for a defect analysis document."""
    doc = load_doc(a.file)
    problems = validate(doc)
    if a.action == "validate" or problems:
        if problems:
            print("the analysis is not complete:")
            for x in problems:
                print(f"  - {x}")
            return 1
        print("the analysis is complete: all three comparisons answered, a confirmed root cause, a fix and a regression test")
        return 0
    if a.action == "render":
        print(render(doc))
        return 0
    L = doc["lenses"]
    evidence = "; ".join(f"{k.replace('_', ' ')}: " + (L[k].get("decisive_difference") or L[k].get("first_bad") or
                                                       L[k].get("evidence") if L[k]["status"] == "done" else "n/a")
                         for k in LENS_KEYS)
    print(json.dumps({"reviewer": a.reviewer, "target": doc["title"], "criteria": "defect analysis standard: root cause",
                      "findings": [{"title": doc["root_cause"]["statement"][:120], "severity": a.severity, "kind": "defect",
                                    "location": doc["root_cause"]["location"], "criterion": "root cause",
                                    "evidence": evidence[:900],
                                    "recommendation": f"{doc['fix']['proposal']} Regression test: "
                                                      f"{doc['fix']['regression_test']}"}]}, indent=2, ensure_ascii=False))
    return 0


# ------------------------------------------------------------------------------------------- selftest
def selftest(_a=None):
    """Exercise every subcommand on a temporary git repository with a planted regression."""
    import contextlib
    import io
    checks = []
    ok = lambda n, c: checks.append((n, bool(c)))
    NS = argparse.Namespace
    d = tempfile.mkdtemp(prefix="defect-selftest-")

    def run(fn, ns):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = fn(ns)
        return rc, buf.getvalue()

    counter = os.path.join(d, "n.txt")
    flaky = (f'{sys.executable} -c "import os,sys; f=r\'{counter}\'; n=int(open(f).read()) if os.path.exists(f) else 0; '
             f'open(f,\'w\').write(str(n+1)); sys.exit(1 if n % 3 == 0 else 0)"')
    _, out = run(cmd_repeat, NS(command=flaky, n=9, parallel=1, timeout=30, cwd=None, json=False))
    ok("repeat: a defect failing 3 of 9 runs is reported as intermittent", "3 failed" in out and "INTERMITTENT" in out)

    if shutil.which("git"):
        repo = os.path.join(d, "repo"); os.makedirs(repo)
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@x", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@x")
        g = lambda *x: subprocess.run(["git", "-C", repo, *x], env=env, capture_output=True)
        g("init", "-q", "-b", "main")
        calc = os.path.join(repo, "calc.py")
        versions = [("def discount(t):\n    return t * 0.95 if t >= 1000 else t\n", "discount from 1000"),
                    ("def discount(t):\n    return t * 0.95 if t >= 1000 else t\n\n\ndef tax(t):\n    return t * 0.2\n", "add tax"),
                    ("def discount(t):\n    return t * 0.95 if t > 1000 else t\n\n\ndef tax(t):\n    return t * 0.2\n", "tidy discount"),
                    ("def discount(t):\n    return t * 0.95 if t > 1000 else t\n\n\ndef tax(t):\n    return t * 0.21\n", "tax 21%")]
        for text, msg in versions:
            open(calc, "w").write(text)
            g("add", "-A"); g("commit", "-q", "-m", msg)
        open(os.path.join(repo, "requirements.txt"), "w").write("requests==2.31.0\n")
        g("add", "-A"); g("commit", "-q", "-m", "pin requests")
        open(calc, "a").write("# local, uncommitted work\n")
        repro = f'{sys.executable} -c "import calc, sys; sys.exit(0 if calc.discount(1000) == 950 else 1)"'
        rc, out = run(cmd_bisect, NS(repo=repo, good="HEAD~4", bad="HEAD", cmd=repro, with_=None, timeout=60, json=False))
        ok("bisect: the first bad commit is the one that changed >= to >", rc == 0 and "tidy discount" in
           out.split("FIRST BAD COMMIT")[-1])
        ok("bisect: the working tree, with its uncommitted work, is untouched",
           open(calc).read().endswith("# local, uncommitted work\n") and
           len(subprocess.run(["git", "-C", repo, "worktree", "list"], capture_output=True,
                              text=True).stdout.strip().splitlines()) == 1)            # no temporary worktree left
        try:
            run(cmd_bisect, NS(repo=repo, good="HEAD~2", bad="HEAD", cmd=repro, with_=None, timeout=60, json=False))
            ok("bisect: a 'good' state that also fails is refused", False)
        except DefectError as e:
            ok("bisect: a 'good' state that also fails is refused", "also fails" in str(e))
        rc, out = run(cmd_changes, NS(repo=repo, good="HEAD~4", bad="HEAD"))
        ok("changes: commits listed, the dependency file recognised and its version shown",
           "tidy discount" in out and "dependencies" in out and "requests==2.31.0" in out)
    else:
        ok("bisect and changes skipped: git is not installed here", True)

    w = os.path.join(d, "api.py")
    open(w, "w").write("def get_invoice(user, i):\n    row = load(i)\n    if row is None or row.owner != user:\n"
                       "        return None\n    return row\n\n\ndef delete_invoice(user, i):\n    row = load(i)\n"
                       "    remove(i)\n    return True\n")
    rc, out = run(cmd_compare, NS(working=f"{w}::get_invoice", failing=f"{w}::delete_invoice"))
    ok("compare: the ownership check present only in the working analogue is named",
       "conditions and guards only in the working one" in out and "row.owner != user" in out)
    t = os.path.join(d, "pay.py")
    open(t, "w").write("import time\nimport requests\n\nGATEWAY_TIMEOUT_SECONDS = 0.1\n\n\ndef charge(x):\n    time.sleep(0.1)\n"
                       "    return requests.post(URL, timeout=1.0, json=x)\n")
    rc, out = run(cmd_timing, NS(paths=[t]))
    ok("timing: timeouts — including a named constant — and the sleep are listed, each with its question",
       "timeout —" in out and "sleep —" in out and "GATEWAY_TIMEOUT_SECONDS = 0.1" in out)

    good = {"title": "Discount missing at exactly 1000", "symptom": {"observed": "no discount at 1000", "expected": "5% off"},
            "reproduction": {"command": "pytest -q tests/test_invoices.py::test_threshold",
                             "determinism": {"runs": 20, "failures": 20}},
            "lenses": {"last_known_good": {"status": "done", "evidence": "bisect between v1.0 and HEAD",
                                           "last_good": "v1.0", "first_bad": "abc123 tidy discount"},
                       "working_analogue": {"status": "not-applicable", "reason": "no other code applies discounts or thresholds"},
                       "timing": {"status": "not-applicable", "reason": "fails in 20 of 20 single-threaded runs; no clock or I/O"}},
            "hypotheses": [{"hypothesis": "> instead of >=", "prediction": "fails only at exactly 1000",
                            "experiment": "999.99, 1000, 1000.01", "outcome": "confirmed"},
                           {"hypothesis": "float rounding", "prediction": "fails near any boundary",
                            "experiment": "Decimal input", "outcome": "refuted"}],
            "root_cause": {"statement": "the comparison excludes the threshold", "location": "app/invoices.py:14",
                           "trigger": "a refactoring changed >= to >", "contributing": ["no boundary test"]},
            "fix": {"proposal": "use >=", "regression_test": "a parameterised test at 999.99, 1000, 1000.01"},
            "confidence": "high"}
    ok("analysis: a complete analysis is accepted", not validate(good))
    bad = json.loads(json.dumps(good))
    bad["reproduction"]["determinism"] = {"runs": 20, "failures": 6}
    ok("analysis: timing cannot be dismissed when the defect is intermittent",
       any("intermittent" in x for x in validate(bad)))
    bad = json.loads(json.dumps(good)); del bad["lenses"]["working_analogue"]
    ok("analysis: a missing comparison is refused", any("working_analogue" in x for x in validate(bad)))
    bad = json.loads(json.dumps(good)); bad["hypotheses"] = bad["hypotheses"][:1]
    ok("analysis: a single hypothesis is refused", any("two competing" in x for x in validate(bad)))
    rep = render(good)
    ok("analysis: the report carries the three comparisons and the root cause",
       all(x in rep for x in ("A. Against the last known good", "B. Against a working analogue", "C. Timing", "## Root cause")))
    for n, good_ in checks:
        print(f"  {'pass' if good_ else 'FAIL'}  {n}")
    bad_n = sum(1 for _, g_ in checks if not g_)
    print(f"\n{len(checks) - bad_n} of {len(checks)} checks passed")
    return 1 if bad_n else 0


def main():
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description="Defect analysis tools: last known good, working analogue, timing.")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("repeat"); p.add_argument("command"); p.add_argument("-n", type=int, default=30)
    p.add_argument("--parallel", type=int, default=1); p.add_argument("--timeout", type=float, default=60)
    p.add_argument("--cwd"); p.add_argument("--json", action="store_true"); p.set_defaults(fn=cmd_repeat)
    p = sp.add_parser("bisect"); p.add_argument("--good", required=True); p.add_argument("--bad", default="HEAD")
    p.add_argument("--cmd", required=True); p.add_argument("--with", dest="with_", action="append")
    p.add_argument("--repo", default="."); p.add_argument("--timeout", type=float, default=600)
    p.add_argument("--json", action="store_true"); p.set_defaults(fn=cmd_bisect)
    p = sp.add_parser("changes"); p.add_argument("--good", required=True); p.add_argument("--bad", default="HEAD")
    p.add_argument("--repo", default="."); p.set_defaults(fn=cmd_changes)
    p = sp.add_parser("compare"); p.add_argument("working"); p.add_argument("failing"); p.set_defaults(fn=cmd_compare)
    p = sp.add_parser("timing"); p.add_argument("paths", nargs="+"); p.set_defaults(fn=cmd_timing)
    p = sp.add_parser("analysis"); p.add_argument("action", choices=("validate", "render", "findings"))
    p.add_argument("file"); p.add_argument("--reviewer", default="defect-analyst")
    p.add_argument("--severity", default="high", choices=("critical", "high", "medium", "low"))
    p.set_defaults(fn=cmd_analysis)
    sp.add_parser("selftest").set_defaults(fn=selftest)
    a = ap.parse_args()
    try:
        return a.fn(a) or 0
    except DefectError as e:
        print(f"defect: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
