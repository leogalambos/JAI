#!/usr/bin/env python3
"""Factual survey of a repository, for the Codebase Reviewer role.

A large codebase cannot be read, and a review built from whichever files were opened first
is not a review, it is an impression. This script produces the measurements that tell you
where to look: size and language mix, test-to-code ratio, churn hotspots from git history,
dependency manifests, and marker comments. Its output enters context; the codebase does not.

It reads only. No file is written, no history is altered, nothing is installed.

Usage
-----
    python3 repo_survey.py /path/to/repo
    python3 repo_survey.py /path/to/repo --since 12.months --top 25
    python3 repo_survey.py /path/to/repo --json
"""
import argparse
import collections
import json
import os
import subprocess
import sys
for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
# Under a non-UTF-8 locale, arguments arrive surrogate-escaped; recover the real characters (a no-op otherwise).
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]

LANGS = {
    ".py": "Python", ".java": "Java", ".kt": "Kotlin", ".scala": "Scala", ".go": "Go",
    ".rs": "Rust", ".c": "C", ".h": "C/C++ header", ".cc": "C++", ".cpp": "C++", ".hpp": "C++ header",
    ".cs": "C#", ".rb": "Ruby", ".php": "PHP", ".js": "JavaScript", ".jsx": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".swift": "Swift", ".m": "Objective-C",
    ".sql": "SQL", ".sh": "Shell", ".ps1": "PowerShell", ".pl": "Perl", ".r": "R",
    ".cbl": "COBOL", ".cob": "COBOL", ".vb": "Visual Basic", ".ex": "Elixir", ".erl": "Erlang",
    ".tf": "Terraform", ".yaml": "YAML", ".yml": "YAML", ".json": "JSON", ".xml": "XML",
    ".md": "Markdown", ".html": "HTML", ".css": "CSS", ".scss": "CSS",
}
CODE = {"Python", "Java", "Kotlin", "Scala", "Go", "Rust", "C", "C++", "C#", "Ruby", "PHP",
        "JavaScript", "TypeScript", "Swift", "Objective-C", "COBOL", "Visual Basic", "Elixir", "Erlang"}
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "target", "out", ".venv", "venv",
             "__pycache__", ".idea", ".gradle", ".terraform", "coverage", ".next", ".tox"}
TEST_HINTS = ("test", "spec", "__tests__", "testing", "it/", "e2e")
MANIFESTS = ["requirements.txt", "pyproject.toml", "Pipfile", "package.json", "pom.xml",
             "build.gradle", "build.gradle.kts", "go.mod", "Cargo.toml", "Gemfile", "composer.json",
             "*.csproj", "Dockerfile", "docker-compose.yml", ".gitlab-ci.yml", "Jenkinsfile"]
MARKERS = ("TODO", "FIXME", "HACK", "XXX", "DEPRECATED", "WORKAROUND")


def is_test(path):
    low = path.lower()
    return any(h in low for h in TEST_HINTS)


def git(repo, *args):
    try:
        out = subprocess.run(["git", "-C", repo, *args], capture_output=True, encoding="utf-8", errors="replace", timeout=120)
        return out.stdout if out.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def survey(repo, since, top):
    by_lang = collections.Counter()
    lines_by_lang = collections.Counter()
    code_lines = test_lines = 0
    biggest = []
    markers = collections.Counter()
    found_manifests = []
    files = 0

    for dirpath, dirs, names in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".git")]
        for n in names:
            full = os.path.join(dirpath, n)
            rel = os.path.relpath(full, repo)
            ext = os.path.splitext(n)[1].lower()
            lang = LANGS.get(ext)
            if n in MANIFESTS or (ext == ".csproj"):
                found_manifests.append(rel)
            if not lang:
                continue
            files += 1
            by_lang[lang] += 1
            try:
                with open(full, encoding="utf-8", errors="ignore") as fh:
                    text = fh.read()
            except OSError:
                continue
            count = text.count("\n") + 1
            lines_by_lang[lang] += count
            if lang in CODE:
                if is_test(rel):
                    test_lines += count
                else:
                    code_lines += count
                    biggest.append((count, rel))
                for m in MARKERS:
                    markers[m] += text.count(m)

    biggest.sort(reverse=True)

    churn = []
    log = git(repo, "log", f"--since={since}", "--name-only", "--pretty=format:")
    if log:
        c = collections.Counter(l.strip() for l in log.splitlines() if l.strip())
        churn = [(n, f) for f, n in c.most_common(top * 3)
                 if os.path.splitext(f)[1].lower() in LANGS and not is_test(f)][:top]

    authors = len({l for l in git(repo, "log", f"--since={since}", "--pretty=format:%ae").splitlines() if l})
    commits = len(git(repo, "log", f"--since={since}", "--pretty=format:%h").splitlines())
    first = git(repo, "log", "--reverse", "--pretty=format:%ad", "--date=short").split("\n")[:1]

    big = {f for _, f in biggest[:top]}
    hot = {f for _, f in churn}
    return {
        "repository": os.path.abspath(repo),
        "window": since,
        "files_counted": files,
        "languages": [{"language": k, "files": v, "lines": lines_by_lang[k]}
                      for k, v in by_lang.most_common()],
        "code_lines": code_lines,
        "test_lines": test_lines,
        "test_to_code_ratio": round(test_lines / code_lines, 3) if code_lines else None,
        "largest_files": [{"lines": n, "path": f} for n, f in biggest[:top]],
        "churn_hotspots": [{"commits": n, "path": f} for n, f in churn],
        "large_and_hot": sorted(big & hot),
        "markers": {k: v for k, v in markers.most_common() if v},
        "manifests": sorted(set(found_manifests)),
        "commits_in_window": commits,
        "distinct_authors_in_window": authors,
        "first_commit": first[0] if first else None,
    }


def main():
    ap = argparse.ArgumentParser(description="Read-only survey of a repository.")
    ap.add_argument("repo")
    ap.add_argument("--since", default="12.months", help="git history window, e.g. 6.months")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not os.path.isdir(args.repo):
        sys.exit(f"error: {args.repo} is not a directory")

    d = survey(args.repo, args.since, args.top)
    if args.json:
        print(json.dumps(d, indent=2))
        return 0

    print(f"repository : {d['repository']}")
    print(f"first commit: {d['first_commit'] or 'unknown (not a git repository?)'}")
    print(f"window     : {d['window']}  ({d['commits_in_window']} commits, "
          f"{d['distinct_authors_in_window']} authors)")
    print(f"code       : {d['code_lines']:,} lines   tests: {d['test_lines']:,} lines   "
          f"ratio: {d['test_to_code_ratio']}")
    print("\nlanguages")
    for l in d["languages"][:10]:
        print(f"  {l['language']:<16} {l['files']:>6} files  {l['lines']:>9,} lines")
    print("\nlargest non-test files")
    for f in d["largest_files"]:
        print(f"  {f['lines']:>7,}  {f['path']}")
    if d["churn_hotspots"]:
        print("\nmost-changed non-test files in the window")
        for f in d["churn_hotspots"]:
            print(f"  {f['commits']:>7}  {f['path']}")
    if d["large_and_hot"]:
        print("\nboth large and frequently changed - read these first")
        for f in d["large_and_hot"]:
            print(f"  {f}")
    if d["markers"]:
        print("\nmarker comments: " + ", ".join(f"{k}={v}" for k, v in d["markers"].items()))
    if d["manifests"]:
        print("\ndependency and pipeline manifests")
        for m in d["manifests"][:20]:
            print(f"  {m}")
    print("\nThis is an inventory, not a judgement. Nothing here is a finding until it is read, "
          "measured against the review criteria and located at a line range.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
