#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Findings ledger: the record behind review -> rework -> verification, for any library.

A reviewer records findings, each located (file and line range) and tied to a criterion. An author
resolves them. A different actor verifies each resolution, or reopens it. After MAX_ROUNDS reopenings
a finding is "stuck": no further rework is accepted, and only the user can decide what happens next
(accept it as a risk, or the reviewer withdraws it). That is what stops review and rework looping.

The ledger is append-only and hash-chained, like the fabric: state is derived from events, never edited.

    findings.py add      LEDGER review.json          record a reviewer's findings (atomic)
    findings.py list     LEDGER [--state S]          open | resolved | verified | stuck | accepted | withdrawn
    findings.py resolve  LEDGER ID --by WHO --note "what changed" [--ref COMMIT_OR_PATH]
    findings.py verify   LEDGER ID --by WHO (--ok | --reopen) --note "..."
    findings.py withdraw LEDGER ID --by WHO --note "why the finding was wrong"
    findings.py accept-risk LEDGER ID --by WHO --rationale "..." --expires DAYS    (yours: asks you first)
    findings.py status   LEDGER                      what blocks completion, what is stuck
    findings.py report   LEDGER                      markdown
    findings.py archive-private LEDGER --exclusive-maintenance
                                                   move a COMPLETE ledger intact to INBOX/private-audit
    findings.py selftest

Ledgers live in .findings/<LEDGER>.jsonl under the current directory, or FINDINGS_HOME.
"""
import argparse
import signal
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import time
from collections import Counter
for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
# Under a non-UTF-8 locale, arguments arrive surrogate-escaped; recover the real characters (a no-op otherwise).
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]

HOME = os.environ.get("FINDINGS_HOME", os.path.join(os.getcwd(), ".findings"))
MAX_ROUNDS = int(os.environ.get("FINDINGS_MAX_ROUNDS", "3"))
SEVERITIES = ("critical", "high", "medium", "low")
KINDS = ("defect", "gap", "risk", "inconsistency", "suggestion")
BLOCKING = {"open", "resolved", "stuck"}          # states that keep a non-suggestion finding unfinished


class LedgerError(Exception):
    pass


def canonical(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def path(name):
    if not name or any(c in name for c in "/\\.") or len(name) > 64:
        raise LedgerError("ledger name must be a simple identifier")
    return os.path.join(HOME, f"{name}.jsonl")


def _parse_events(data, name):
    """Validate a ledger byte snapshot without rewriting its event serialization."""
    events, prev = [], "0" * 64
    try:
        for i, line in enumerate(data.decode("utf-8").splitlines(), 1):
            e = json.loads(line)
            h = hashlib.sha256((prev + canonical(e["data"]) + str(e["seq"])).encode()).hexdigest()
            if e["prev"] != prev or e["hash"] != h or e["seq"] != i:
                raise LedgerError(f"ledger {name} is corrupt at entry {i}: it has been edited outside findings.py")
            prev = e["hash"]
            events.append(e)
    except (UnicodeError, ValueError, KeyError, TypeError) as exc:
        raise LedgerError(f"ledger {name} has invalid event serialization") from exc
    return events


def load(name):
    """Read and validate a named ledger's existing hash chain.

    Args:
        name: Simple ledger identifier resolved under HOME.
    Returns:
        Ordered event dictionaries, or an empty list if the ledger does not exist.
    Raises:
        LedgerError: If the identifier, event serialization or hash chain is invalid.
        OSError: If an existing ledger cannot be read.
    """
    p = path(name)
    if not os.path.isfile(p):
        return []
    with open(p, "rb") as stream:
        return _parse_events(stream.read(), name)


def append(name, events, datas):
    os.makedirs(HOME, exist_ok=True)
    prev = events[-1]["hash"] if events else "0" * 64
    out = []
    for d in datas:
        seq = len(events) + len(out) + 1
        h = hashlib.sha256((prev + canonical(d) + str(seq)).encode()).hexdigest()
        out.append({"seq": seq, "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "data": d, "prev": prev, "hash": h})
        prev = h
    with open(path(name), "a", encoding="utf-8") as fh:
        for e in out:
            fh.write(canonical(e) + "\n")
    events.extend(out)


def state(events):
    """-> {id: finding dict with derived state, rounds, last resolver, history}"""
    f = {}
    for e in events:
        d = e["data"]
        if d["op"] == "add":
            for x in d["findings"]:
                f[x["id"]] = dict(x, state="open", rounds=0, resolver=None, history=[], reviewer=d["reviewer"],
                                  target=d.get("target"))
            continue
        x = f[d["id"]]
        x["history"].append({"op": d["op"], "by": d.get("by"), "note": d.get("note") or d.get("rationale"),
                             "ts": e["ts"]})
        if d["op"] == "resolve":
            x["state"], x["resolver"] = "resolved", d["by"]
        elif d["op"] == "verify":
            if d["ok"]:
                x["state"] = "verified"
            else:
                x["rounds"] += 1
                x["state"] = "stuck" if x["rounds"] >= MAX_ROUNDS else "open"
        elif d["op"] == "withdraw":
            x["state"] = "withdrawn"
        elif d["op"] == "accept-risk":
            x["state"], x["expires"] = "accepted", d.get("expires")
    return f


def require_person():
    """Accepting a finding as a risk is the user's decision: a terminal, or the hook's approval prompt."""
    if os.environ.get("FINDINGS_TEST_AUTHORITY") == "1":
        return "test"
    if sys.stdin.isatty() and sys.stdout.isatty():
        return "terminal"
    homes = [
        os.path.expanduser(os.environ.get("CLAUDE_HOME") or "~/.claude"),
        os.path.expanduser(os.environ.get("CODEX_HOME") or "~/.codex"),
    ]
    candidates = [os.path.join(homes[0], "settings.json"), os.path.join(os.getcwd(), ".claude", "settings.json"),
                  os.path.join(homes[1], "config.toml"), os.path.join(os.getcwd(), ".codex", "config.toml")]
    for p in candidates:
        try:
            with open(p, encoding="utf-8") as stream:
                if "guard_authority.py" in stream.read():
                    return "claude-code-approval-prompt"
        except OSError:
            pass
    raise LedgerError("accepting a finding as a risk is the user's decision, and no approval gate is active; "
                      "run it in your own terminal")


def get(events, fid):
    f = state(events)
    if fid not in f:
        raise LedgerError(f"no finding {fid}")
    return f[fid]


# ------------------------------------------------------------------------------------- commands
def cmd_add(a):
    events = load(a.ledger)
    if a.file == "-":
        raw = sys.stdin.read()
    else:
        with open(a.file, encoding="utf-8") as stream:
            raw = stream.read()
    doc = json.loads(raw[raw.find("{"):raw.rfind("}") + 1])
    if set(doc) - {"reviewer", "target", "criteria", "findings"}:
        raise LedgerError(f"unexpected keys {sorted(set(doc) - {'reviewer', 'target', 'criteria', 'findings'})}")
    if not doc.get("reviewer") or not doc.get("criteria"):
        raise LedgerError("a review states its reviewer and the criteria it applied, fixed before reading")
    n = len(state(events))
    items = []
    for i, x in enumerate(doc.get("findings", []), 1):
        for k in ("title", "severity", "kind", "location", "criterion", "evidence", "recommendation"):
            if not x.get(k):
                raise LedgerError(f"finding {i} lacks '{k}'")
        if x["severity"] not in SEVERITIES or x["kind"] not in KINDS:
            raise LedgerError(f"finding {i}: severity in {SEVERITIES}, kind in {KINDS}")
        if ":" not in x["location"] and x["kind"] != "gap":
            raise LedgerError(f"finding {i}: location must be 'file:line' or 'file:start-end' (gaps may name a "
                              "path only). A finding that cannot be located is an opinion.")
        items.append({k: str(x[k]) for k in ("title", "severity", "kind", "location", "criterion",
                                              "evidence", "recommendation")} | {"id": f"F-{n + i:04d}"})
    append(a.ledger, events, [{"op": "add", "reviewer": doc["reviewer"], "target": doc.get("target"),
                               "criteria": doc["criteria"], "findings": items}])
    for x in items:
        print(f"{x['id']}  {x['severity']:<8} {x['kind']:<13} {x['location']}  {x['title'][:60]}")


def cmd_resolve(a):
    events = load(a.ledger)
    x = get(events, a.id)
    if x["state"] == "stuck":
        raise LedgerError(f"{a.id} is stuck after {MAX_ROUNDS} rework rounds. More rework will not converge: "
                          "the user decides (accept-risk), or the reviewer withdraws it.")
    if x["state"] != "open":
        raise LedgerError(f"{a.id} is {x['state']}, not open")
    if a.by == x["reviewer"]:
        raise LedgerError("the reviewer who raised a finding does not also fix it")
    append(a.ledger, events, [{"op": "resolve", "id": a.id, "by": a.by, "note": a.note, "ref": a.ref}])
    print(f"{a.id}  resolved by {a.by}; awaiting verification")


def cmd_verify(a):
    events = load(a.ledger)
    x = get(events, a.id)
    if x["state"] != "resolved":
        raise LedgerError(f"{a.id} is {x['state']}; only a resolved finding can be verified")
    if a.by == x["resolver"]:
        raise LedgerError("whoever resolved a finding does not also verify it")
    append(a.ledger, events, [{"op": "verify", "id": a.id, "by": a.by, "ok": a.ok, "note": a.note}])
    y = get(load(a.ledger), a.id)
    print(f"{a.id}  {'verified' if a.ok else 'reopened'}"
          + (f"  round {y['rounds']}/{MAX_ROUNDS}" if not a.ok else "")
          + ("  -> STUCK: hand to the user" if y["state"] == "stuck" else ""))


def cmd_withdraw(a):
    events = load(a.ledger)
    x = get(events, a.id)
    if x["state"] in ("verified", "withdrawn", "accepted"):
        raise LedgerError(f"{a.id} is already {x['state']}")
    append(a.ledger, events, [{"op": "withdraw", "id": a.id, "by": a.by, "note": a.note}])
    print(f"{a.id}  withdrawn")


def cmd_accept(a):
    events = load(a.ledger)
    x = get(events, a.id)
    if x["state"] in ("verified", "withdrawn", "accepted"):
        raise LedgerError(f"{a.id} is already {x['state']}")
    if not a.expires:
        raise LedgerError("an accepted risk is time-bound: pass --expires DAYS")
    via = require_person()
    exp = time.strftime("%Y-%m-%d", time.localtime(time.time() + a.expires * 86400))
    append(a.ledger, events, [{"op": "accept-risk", "id": a.id, "by": a.by, "rationale": a.rationale,
                               "expires": exp, "approved_via": via}])
    print(f"{a.id}  accepted as a risk by {a.by} until {exp}")


def cmd_list(a):
    for fid, x in sorted(state(load(a.ledger)).items()):
        if a.state and x["state"] != a.state:
            continue
        print(f"{fid}  {x['state']:<9} r{x['rounds']}  {x['severity']:<8} {x['kind']:<13} {x['location']}  "
              f"{x['title'][:56]}")


def summary(f):
    blocking = [x for x in f.values() if x["kind"] != "suggestion" and x["state"] in BLOCKING]
    return blocking, Counter(x["state"] for x in f.values())


def cmd_status(a):
    f = state(load(a.ledger))
    blocking, c = summary(f)
    print(f"ledger {a.ledger}: {len(f)} findings  " + ", ".join(f"{k}={v}" for k, v in sorted(c.items())))
    stuck = [x for x in f.values() if x["state"] == "stuck"]
    awaiting = [x for x in f.values() if x["state"] == "resolved"]
    if stuck:
        print(f"  STUCK ({len(stuck)}): rework did not converge; the user decides:")
        for x in stuck:
            print(f"    {x['id']}  {x['location']}  {x['title'][:70]}")
    if awaiting:
        print(f"  awaiting verification by someone other than the resolver: {' '.join(x['id'] for x in awaiting)}")
    if not blocking:
        print("  COMPLETE: every defect, gap, risk and inconsistency is verified, withdrawn or accepted "
              "(open suggestions do not block)")
        return 0
    print(f"  not complete: {len(blocking)} blocking finding(s)")
    return 1


def cmd_report(a):
    f = state(load(a.ledger))
    blocking, c = summary(f)
    print(f"# Findings: {a.ledger}\n\n{len(f)} findings · " + " · ".join(f"{k} {v}" for k, v in sorted(c.items()))
          + f" · {'complete' if not blocking else str(len(blocking)) + ' blocking'}\n")
    print("| ID | State | Rounds | Severity | Kind | Location | Finding | Recommendation |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    order = {s: i for i, s in enumerate(SEVERITIES)}
    for x in sorted(f.values(), key=lambda x: (order[x["severity"]], x["id"])):
        cell = lambda t: str(t).replace("|", "\\|").replace("\n", " ")[:140]
        print(f"| {x['id']} | {x['state']} | {x['rounds']} | {x['severity']} | {x['kind']} | `{cell(x['location'])}` | "
              f"{cell(x['title'])} | {cell(x['recommendation'])} |")


def _directory_fd(parent_fd, parts, create=False):
    """Open descendant directories without following symlinks; close the caller's copy only."""
    current = os.dup(parent_fd)
    try:
        for part in parts:
            if part in ("", ".", ".."):
                raise LedgerError("archive paths must not contain traversal components")
            if create:
                try:
                    os.mkdir(part, mode=0o700, dir_fd=current)
                except FileExistsError:
                    pass
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current)
            os.close(current)
            current = child
        return current
    except BaseException:
        os.close(current)
        raise


def _read_archive_fd(descriptor):
    """Read an opened regular ledger without changing or reserializing event bytes."""
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks = []
    while True:
        chunk = os.read(descriptor, 65536)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


def _rename_noreplace(source_dir, name, destination_dir):
    """Atomically move one directory entry without overwriting any destination.

    Linux renameat2 is required: a copy/delete or overwrite-capable fallback
    would reintroduce the pathname deletion race this operation must avoid.
    """
    import ctypes
    if not sys.platform.startswith("linux"):
        raise LedgerError("private archival requires Linux no-overwrite atomic rename")
    library = ctypes.CDLL(None, use_errno=True)
    try:
        rename = library.renameat2
    except AttributeError as exc:
        raise LedgerError("private archival requires renameat2 support") from exc
    rename.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint)
    rename.restype = ctypes.c_int
    encoded = os.fsencode(name)
    if rename(source_dir, encoded, destination_dir, encoded, 1) != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))


def cmd_archive_private(a):
    """Archive a COMPLETE ledger intact within the current workspace's private inbox.

    Args:
        a: CLI namespace with ledger and exclusive_maintenance. The caller must
            explicitly confirm that all other workspace ledger writers are stopped.
    Returns:
        Zero after preserving the exact validated bytes in INBOX/private-audit and
        removing the original directory entry. No event or authority state is changed.
    Raises:
        LedgerError: For invalid, active, corrupt, symlinked or out-of-workspace inputs,
            destination collisions, missing maintenance confirmation, unsupported
            no-follow/atomic-rename operations or filesystem failures. Cross-filesystem
            moves fail without fallback. A failed preflight leaves the source unchanged.

    An advisory directory lock serializes cooperating archival commands. It does not
    prevent an uncooperative same-user process from renaming files. No pathname is
    unlinked: a changed entry is restored by another no-overwrite atomic rename. If
    concurrent writers prevent restoration, both entries remain intact and the command
    reports a maintenance violation for the operator to reconcile.
    """
    if not getattr(a, "exclusive_maintenance", False):
        raise LedgerError("stop other workspace ledger writers and confirm --exclusive-maintenance")
    source = Path(path(a.ledger))
    workspace = Path.cwd()
    if ".." in source.parts:
        raise LedgerError("archive paths must not contain traversal components")
    source = Path(os.path.abspath(source))
    try:
        relative = source.relative_to(workspace)
    except ValueError as exc:
        raise LedgerError("private archival source must be inside the current workspace") from exc
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise LedgerError("private archival requires no-follow directory and file handles")
    root_fd = source_dir = source_fd = archive_dir = archived_fd = None
    moved = False
    identity = None
    try:
        root_fd = os.open(workspace, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        source_dir = _directory_fd(root_fd, relative.parts[:-1])
        import fcntl
        fcntl.flock(source_dir, fcntl.LOCK_EX | fcntl.LOCK_NB)
        source_fd = os.open(relative.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=source_dir)
        original_stat = os.fstat(source_fd)
        if not stat.S_ISREG(original_stat.st_mode) or original_stat.st_nlink != 1:
            raise LedgerError("private archival requires a regular, singly linked source ledger")
        identity = (original_stat.st_dev, original_stat.st_ino)
        original = _read_archive_fd(source_fd)
        events = _parse_events(original, a.ledger)
        if not events:
            raise LedgerError("an empty ledger cannot be archived as COMPLETE")
        try:
            blocking, _ = summary(state(events))
        except (KeyError, TypeError, ValueError) as exc:
            raise LedgerError("ledger state is invalid") from exc
        if blocking:
            raise LedgerError("only a COMPLETE ledger may be archived")
        archive_dir = _directory_fd(root_fd, ("INBOX", "private-audit"), create=True)
        source_directory_stat = os.fstat(source_dir)
        archive_directory_stat = os.fstat(archive_dir)
        if ((source_directory_stat.st_dev, source_directory_stat.st_ino)
                == (archive_directory_stat.st_dev, archive_directory_stat.st_ino)):
            raise LedgerError("ledger is already in the private archive")
        current = os.stat(relative.name, dir_fd=source_dir, follow_symlinks=False)
        if (current.st_dev, current.st_ino) != identity or _read_archive_fd(source_fd) != original:
            raise LedgerError("ledger changed during archival preflight")
        _rename_noreplace(source_dir, relative.name, archive_dir)
        moved = True
        archived_fd = os.open(relative.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=archive_dir)
        archived_stat = os.fstat(archived_fd)
        archived = _read_archive_fd(archived_fd)
        if ((archived_stat.st_dev, archived_stat.st_ino) != identity or archived != original
                or _parse_events(archived, a.ledger) != events):
            raise LedgerError("archived ledger failed byte identity or hash-chain verification")
        if _read_archive_fd(source_fd) != original:
            raise LedgerError("ledger changed before archival completion")
        os.fsync(archive_dir)
        os.fsync(source_dir)
        moved = False
    except (OSError, ValueError) as exc:
        raise LedgerError("private archival failed; no overwrite or copy/delete fallback was attempted") from exc
    finally:
        restoration_failed = False
        if moved and archive_dir is not None:
            try:
                _rename_noreplace(archive_dir, relative.name, source_dir)
                os.fsync(source_dir)
                os.fsync(archive_dir)
            except (OSError, LedgerError):
                restoration_failed = True
        for descriptor in (archived_fd, archive_dir, source_fd, source_dir, root_fd):
            if descriptor is not None:
                os.close(descriptor)
        if restoration_failed:
            raise LedgerError("maintenance violation: verification failed and restoration collided or failed; preserve and reconcile both source and archive entries")
    print(f"archived COMPLETE ledger {a.ledger} intact to INBOX/private-audit/{relative.name}")
    return 0


# ------------------------------------------------------------------------------------- selftest
def cmd_selftest(a):
    global HOME
    HOME = tempfile.mkdtemp(prefix="findings-selftest-")
    os.environ["FINDINGS_TEST_AUTHORITY"] = "1"
    checks = []
    NS = argparse.Namespace

    def expect(n, c):
        checks.append((n, bool(c)))

    def raises(fn):
        try:
            fn()
            return False
        except LedgerError:
            return True

    import io, contextlib
    q = lambda: contextlib.redirect_stdout(io.StringIO())
    rv = os.path.join(HOME, "r.json")
    good = {"reviewer": "document-reviewer", "target": "docs/", "criteria": "accuracy, links, ownership",
            "findings": [{"title": "Broken link", "severity": "medium", "kind": "defect",
                          "location": "docs/a.md:12", "criterion": "links resolve", "evidence": "x.md missing",
                          "recommendation": "fix the link"},
                         {"title": "Add a glossary", "severity": "low", "kind": "suggestion",
                          "location": "docs/:1", "criterion": "terminology", "evidence": "terms vary",
                          "recommendation": "add glossary.md"}]}
    bad = dict(good, findings=[dict(good["findings"][0], location="somewhere in the docs")])
    with open(rv, "w", encoding="utf-8") as stream:
        stream.write(json.dumps(bad))
    expect("an unlocated finding is refused, and nothing is written",
           raises(lambda: cmd_add(NS(ledger="t", file=rv))) and load("t") == [])
    with open(rv, "w", encoding="utf-8") as stream:
        stream.write(json.dumps(good))
    with q():
        cmd_add(NS(ledger="t", file=rv))
    expect("the reviewer may not fix its own finding",
           raises(lambda: cmd_resolve(NS(ledger="t", id="F-0001", by="document-reviewer", note="x", ref=None))))
    with q():
        cmd_resolve(NS(ledger="t", id="F-0001", by="docs-author", note="fixed link", ref=None))
    expect("the resolver may not verify its own fix",
           raises(lambda: cmd_verify(NS(ledger="t", id="F-0001", by="docs-author", ok=True, note="ok"))))
    for i in range(MAX_ROUNDS):
        with q():
            cmd_verify(NS(ledger="t", id="F-0001", by="document-reviewer", ok=False, note="still broken"))
            if i < MAX_ROUNDS - 1:
                cmd_resolve(NS(ledger="t", id="F-0001", by="docs-author", note="again", ref=None))
    expect(f"after {MAX_ROUNDS} failed rework rounds the finding is stuck, and more rework is refused",
           get(load("t"), "F-0001")["state"] == "stuck"
           and raises(lambda: cmd_resolve(NS(ledger="t", id="F-0001", by="docs-author", note="x", ref=None))))
    with q():
        rc = cmd_status(NS(ledger="t"))
    expect("a stuck finding keeps the ledger incomplete", rc == 1)
    with q():
        cmd_accept(NS(ledger="t", id="F-0001", by="owner", rationale="tolerable", expires=30))
        rc = cmd_status(NS(ledger="t"))
    expect("once the user accepts it, an open suggestion does not block completion", rc == 0)
    with open(path("t"), encoding="utf-8") as stream:
        lines = stream.read().splitlines()
    d = json.loads(lines[0]); d["data"]["criteria"] = "changed"; lines[0] = canonical(d)
    with open(path("t"), "w", encoding="utf-8") as stream:
        stream.write("\n".join(lines) + "\n")
    expect("an edited ledger is detected", raises(lambda: load("t")))

    for n, ok in checks:
        print(f"  {'pass' if ok else 'FAIL'}  {n}")
    bad = sum(1 for _, ok in checks if not ok)
    print(f"\n{len(checks) - bad} of {len(checks)} checks passed")
    return 1 if bad else 0


def main():
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description="Findings ledger for review -> rework -> verification.")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("add"); p.add_argument("ledger"); p.add_argument("file"); p.set_defaults(fn=cmd_add)
    p = sp.add_parser("list"); p.add_argument("ledger"); p.add_argument("--state"); p.set_defaults(fn=cmd_list)
    p = sp.add_parser("resolve"); p.add_argument("ledger"); p.add_argument("id")
    p.add_argument("--by", required=True); p.add_argument("--note", required=True); p.add_argument("--ref")
    p.set_defaults(fn=cmd_resolve)
    p = sp.add_parser("verify"); p.add_argument("ledger"); p.add_argument("id"); p.add_argument("--by", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--ok", dest="ok", action="store_true"); g.add_argument("--reopen", dest="ok", action="store_false")
    p.add_argument("--note", required=True); p.set_defaults(fn=cmd_verify)
    p = sp.add_parser("withdraw"); p.add_argument("ledger"); p.add_argument("id")
    p.add_argument("--by", required=True); p.add_argument("--note", required=True); p.set_defaults(fn=cmd_withdraw)
    p = sp.add_parser("accept-risk"); p.add_argument("ledger"); p.add_argument("id")
    p.add_argument("--by", required=True); p.add_argument("--rationale", required=True)
    p.add_argument("--expires", type=float, required=True); p.set_defaults(fn=cmd_accept)
    p = sp.add_parser("archive-private"); p.add_argument("ledger")
    p.add_argument("--exclusive-maintenance", action="store_true", help="confirm all other workspace ledger writers are stopped")
    p.set_defaults(fn=cmd_archive_private)
    for name, fn in (("status", cmd_status), ("report", cmd_report)):
        p = sp.add_parser(name); p.add_argument("ledger"); p.set_defaults(fn=fn)
    sp.add_parser("selftest").set_defaults(fn=cmd_selftest)
    a = ap.parse_args()
    try:
        return a.fn(a) or 0
    except LedgerError as exc:
        print(f"findings: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
