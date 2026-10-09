#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Read-only survey of a document library, so a review starts from facts rather than impressions.

Reports: formats and size; for Markdown, reStructuredText and AsciiDoc files, the title, heading depth,
ownership metadata (owner, status, version, review date) from front matter, broken relative links,
orphans that nothing links to, exact duplicates, stale files, and marker comments. Writes nothing.

    doc_survey.py DOCS_DIR [--stale-days 365] [--top 15] [--json]
"""
import argparse
import signal
import hashlib
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
# Under a non-UTF-8 locale, arguments arrive surrogate-escaped; recover the real characters (a no-op otherwise).
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]

TEXT = {".md", ".markdown", ".mdx", ".rst", ".adoc", ".txt"}
BINARY_DOCS = {".docx", ".doc", ".pdf", ".odt", ".pptx", ".xlsx", ".vsdx"}
SKIP = {".git", "node_modules", "_build", "site", ".venv", "__pycache__", ".findings", ".fabric"}
META_KEYS = ("owner", "status", "version", "review", "reviewed", "review_date", "next_review", "updated")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s#]+)(?:#[^)]*)?\)")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
MARKERS = ("TODO", "FIXME", "TBD", "XXX", "DRAFT")
DATE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


def front_matter(text):
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    meta = {}
    for line in text[3:end if end > 0 else 0].splitlines():
        k, _, v = line.partition(":")
        if v:
            meta[k.strip().lower()] = v.strip().strip("\"'")
    return meta


def survey(root, stale_days, top):
    files, fmt, size = [], Counter(), 0
    for dp, dirs, fs in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
        for f in fs:
            p = os.path.join(dp, f)
            ext = os.path.splitext(f)[1].lower()
            if ext in TEXT or ext in BINARY_DOCS:
                files.append(p)
                fmt[ext] += 1
                size += os.path.getsize(p)
    now = time.time()
    docs, links_in, hashes, broken, markers = {}, defaultdict(set), defaultdict(list), [], Counter()
    for p in files:
        rel = os.path.relpath(p, root)
        raw = open(p, "rb").read()
        hashes[hashlib.sha256(raw).hexdigest()].append(rel)
        ext = os.path.splitext(p)[1].lower()
        info = {"path": rel, "bytes": len(raw), "mtime_days": int((now - os.path.getmtime(p)) / 86400)}
        if ext in TEXT:
            text = raw.decode("utf-8", errors="ignore")
            meta = front_matter(text)
            heads = [(len(m.group(1)), m.group(2)) for m in (HEADING.match(l) for l in text.splitlines()) if m]
            info.update(words=len(text.split()), title=meta.get("title") or (heads[0][1] if heads else None),
                        h1=sum(1 for d, _ in heads if d == 1), depth=max((d for d, _ in heads), default=0),
                        meta={k: meta[k] for k in META_KEYS if k in meta})
            for m in MARKERS:
                markers[m] += text.count(m)
            for target in LINK.findall(text):
                if re.match(r"^[a-z]+:", target):
                    continue                                  # external URL or mailto
                dest = os.path.normpath(os.path.join(os.path.dirname(p), target))
                if os.path.exists(dest):
                    links_in[os.path.relpath(dest, root)].add(rel)
                else:
                    broken.append((rel, target))
            review = next((meta[k] for k in ("next_review", "review_date", "review") if k in meta), None)
            if review and DATE.search(review):
                y, mo, d = map(int, DATE.search(review).groups())
                info["review_overdue"] = time.mktime((y, mo, d, 0, 0, 0, 0, 0, -1)) < now
        docs[rel] = info

    texty = [d for d in docs.values() if "words" in d]
    index_names = {"readme.md", "index.md", "index.rst", "readme.rst", "summary.md", "_sidebar.md"}
    orphans = sorted(d["path"] for d in texty
                     if d["path"] not in links_in and os.path.basename(d["path"]).lower() not in index_names)
    no_owner = sorted(d["path"] for d in texty if "owner" not in d.get("meta", {}))
    overdue = sorted(d["path"] for d in texty if d.get("review_overdue"))
    stale = sorted((d["path"] for d in docs.values() if d["mtime_days"] > stale_days),
                   key=lambda p: -docs[p]["mtime_days"])
    titles = Counter((d["title"] or "").strip().lower() for d in texty if d.get("title"))
    return {
        "root": os.path.abspath(root), "files": len(files), "bytes": size, "formats": dict(fmt.most_common()),
        "words": sum(d.get("words", 0) for d in texty),
        "binary_documents": sorted(d["path"] for d in docs.values() if "words" not in d),
        "missing_title": sorted(d["path"] for d in texty if not d.get("title")),
        "multiple_h1": sorted(d["path"] for d in texty if d.get("h1", 0) > 1),
        "no_owner": no_owner, "review_overdue": overdue,
        "stale": stale[:top], "stale_total": len(stale),
        "broken_links": [{"in": a, "target": b} for a, b in broken],
        "orphans": orphans,
        "duplicates": [v for v in hashes.values() if len(v) > 1],
        "duplicate_titles": sorted(t for t, n in titles.items() if n > 1 and t),
        "markers": {k: v for k, v in markers.items() if v},
        "largest": sorted(((d["bytes"], d["path"]) for d in docs.values()), reverse=True)[:top],
    }


def main():
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description="Read-only survey of a document library.")
    ap.add_argument("root"); ap.add_argument("--stale-days", type=int, default=365)
    ap.add_argument("--top", type=int, default=15); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.root):
        sys.exit(f"error: {a.root} is not a directory")
    s = survey(a.root, a.stale_days, a.top)
    if a.json:
        print(json.dumps(s, indent=2)); return 0
    print(f"library : {s['root']}")
    print(f"files   : {s['files']} ({s['bytes']:,} bytes, {s['words']:,} words in text formats)")
    print("formats : " + ", ".join(f"{k} {v}" for k, v in s["formats"].items()))
    sec = [("binary documents (review needs extraction)", s["binary_documents"]),
           ("no owner in front matter", s["no_owner"]), ("review date passed", s["review_overdue"]),
           ("missing a title", s["missing_title"]), ("more than one H1", s["multiple_h1"]),
           ("orphans: nothing links to them", s["orphans"]),
           (f"not modified for {a.stale_days}+ days ({s['stale_total']})", s["stale"]),
           ("duplicate titles", s["duplicate_titles"])]
    for name, items in sec:
        if items:
            print(f"\n{name}: {len(items)}")
            for x in items[:a.top]:
                print(f"  {x}")
    if s["broken_links"]:
        print(f"\nbroken relative links: {len(s['broken_links'])}")
        for b in s["broken_links"][:a.top]:
            print(f"  {b['in']} -> {b['target']}")
    if s["duplicates"]:
        print(f"\nidentical files: {len(s['duplicates'])} group(s)")
        for g in s["duplicates"][:a.top]:
            print("  " + "  =  ".join(g))
    if s["markers"]:
        print("\nmarkers: " + ", ".join(f"{k}={v}" for k, v in s["markers"].items()))
    print("\nThis is an inventory, not a review. Nothing here is a finding until it is checked against the "
          "review criteria and located.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
