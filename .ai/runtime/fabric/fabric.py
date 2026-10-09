#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Traceability fabric runtime for layered, justifiable agent engagements.

Implements the formal model of "Towards Justifiable AI Systems" (Galambos, 2026, sec. 5):
a fabric T = (N, tau, L, rho, s) of typed nodes and labelled edges, a six-layer stack with
an authority level above it, the ordered review states S, and the justifiability predicate
of Definition 2 as a linear-time graph check.

It is the only well-formed transformation procedure on the fabric (Clark-Wilson sense):
agents never write the log; they return typed JSON, and this tool validates and appends.
Free text from agents is stored as opaque data and never interpreted, so an injected
"please escalate" string cannot become an escalation node (threat T3b, T8).

Storage: one append-only JSONL log per engagement, hash-chained (assumption A1). Authority
acts (layer-0 reviews and authority decisions) are signed with an HMAC key kept outside
~/.claude, created automatically, and run only when a person confirms them: in their own
terminal, or through the Claude Code approval prompt the library's hook raises. Each act
records which. That approximates assumption A2; it is a confirmation gate, not a proof of
human presence.

Usage summary (run with -h on any command for details):
    fabric.py init ENG --intent TEXT --owner NAME
    fabric.py req ENG --layer N --from ID --label derives|refines --text TEXT
    fabric.py contract ENG --from REQ --what ... --why ... --who ... --where ... --when ...
                        --how ... --evidence ... --escalate-if ... --sanitise ... [--rework-of CTR --change WHY]
    fabric.py render-contract ENG CTR
    fabric.py context-packet ENG CTR
    fabric.py ingest ENG --contract CTR RESULT.json
    fabric.py failure ENG --contract CTR --state timeout|failed|... --reason TEXT
    fabric.py invalidate ENG --changed REF --reason TEXT
    fabric.py policy
    fabric.py evidence ENG --layer N --supports FRAG --source S --confidence C [--file PATH]
    fabric.py review ENG FRAG --layer N --state STATE --rationale R --reviewer WHO --model M
    fabric.py consolidate ENG FRAG --layer N
    fabric.py conflict ENG --from ID --layer N --text TEXT
    fabric.py escalate ENG FROM --layer N --reason TEXT
    fabric.py authorise ENG ESC --decision accept|exception|revise|reject|terminate --signer NAME
    fabric.py verify ENG | justify ENG [FRAG] [--strict] | status ENG | report ENG | selftest
"""
import argparse
import hashlib
import signal
import hmac
import json
import os
import sys
import tempfile
import time
from collections import defaultdict, deque
for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
# Under a non-UTF-8 locale, arguments arrive surrogate-escaped; recover the real characters (a no-op otherwise).
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]

VERSION = "1.2.0"

# ------------------------------------------------------------------ the formal model
TYPES = ("intent", "req", "frag", "evd", "rev", "conf", "esc", "auth", "ctr", "att")

# rho. The paper defines rho as single-valued; practice needs a few admissible pairs per
# label (a conflict can arise from evidence, from a fragment or from a review; a reviewed
# lower-layer fragment supports a higher-layer one). Every pair is listed explicitly.
RHO = {
    "derives":           {("intent", "req"), ("req", "ctr")},
    "refines":           {("req", "req"), ("ctr", "req")},
    "requests":          {("req", "frag"), ("ctr", "frag")},
    "supports":          {("evd", "frag"), ("frag", "frag")},
    "contradicts":       {("evd", "frag"), ("frag", "frag")},
    "reviewed_by":       {("frag", "rev")},
    "may_create":        {("evd", "conf"), ("frag", "conf"), ("rev", "conf")},
    "escalates":         {("conf", "esc"), ("esc", "esc")},
    "resolved_by":       {("esc", "auth")},
    "revises":           {("auth", "req")},
    "implements":        {("frag", "ctr")},
    "consolidated_into": {("frag", "frag")},
    "attempts":          {("ctr", "att")},
}
FORWARD = {"derives", "refines", "requests", "supports", "consolidated_into", "implements"}

STATES = ("accepts", "accepts_with_constraints", "correlates", "resonates",
          "insufficient", "out_of_scope", "conflicts", "escalate")
RANK = {s: i for i, s in enumerate(STATES)}          # lower index = stronger support
JUSTIFYING = {s for s in STATES if RANK[s] < RANK["insufficient"]}   # Definition 2 (i)
STRICT_JUSTIFYING = {"accepts", "accepts_with_constraints"}

LAYERS = {0: "Authority", 1: "Intent and Context", 2: "Meaning and Domain Model",
          3: "Reasoning, Policy and Control", 4: "Solution Design",
          5: "Realisation and Tooling", 6: "Execution and Evidence"}
CONFIDENCE = ("deterministic", "observation", "interpretation", "ai_derived")
DECISIONS = ("accept", "exception", "revise", "reject", "terminate")
CONTRACT_FIELDS = ("what", "why", "who", "where", "when", "how", "evidence",
                   "escalate_if", "sanitise")
MAX_REWORK = int(os.environ.get("FABRIC_MAX_REWORK", "3"))             # per contract lineage
MAX_REFORMULATE = int(os.environ.get("FABRIC_MAX_REFORMULATE", "2"))   # per layer, per round
MAX_CONTRACTS = int(os.environ.get("FABRIC_MAX_CONTRACTS", "40"))      # per round, all layers
MAX_ROUNDS = int(os.environ.get("FABRIC_MAX_ROUNDS", "5"))             # human revisions before override
MAX_STEPS = int(os.environ.get("FABRIC_MAX_STEPS", "120"))              # shared episode budget
# Why an escalation moves up. outside_authority is sticky: no relay may downgrade it.
ESC_CODES = ("exhausted", "no_viable_reformulation", "outside_authority", "contradiction", "relay", "budget")
# Sticky states survive every relay: an authority matter stays one, and a spent round stays spent.
STICKY = ("outside_authority", "budget")
FAILURE_STATES = ("failed", "unavailable", "timeout", "ambiguous", "insufficient",
                  "contradicted", "conflicting")
RETRYABLE_FAILURES = {"failed", "unavailable", "timeout", "ambiguous", "insufficient"}
STEP_TYPES = {"ctr", "att", "rev", "evd", "esc", "auth"}

FABRIC_DIR = os.environ.get("FABRIC_HOME", os.path.join(os.getcwd(), ".fabric"))
KEY_PATH = os.environ.get("FABRIC_AUTHORITY_KEY",
                          os.path.expanduser("~/.config/justifiable-fabric/authority.key"))
POLICY_PATH = os.path.join(os.path.dirname(__file__), "supervision-policy.json")


class FabricError(Exception):
    pass


def supervision_policy():
    try:
        with open(POLICY_PATH, encoding="utf-8") as fh:
            p = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise FabricError(f"cannot load supervision policy {POLICY_PATH}: {exc}")
    if p.get("schema") != 1 or not p.get("rules"):
        raise FabricError("invalid supervision policy: expected schema 1 with rules")
    return p


def failure_class(state):
    p = supervision_policy()
    if state in p["failure_classes"]["retryable"]:
        return "retryable"
    if state in p["failure_classes"]["contradictory"]:
        return "contradictory"
    raise FabricError(f"failure state {state} is not classified by supervision-policy.json")


# ------------------------------------------------------------------------ storage
def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def norm_text(t):
    return " ".join(str(t).lower().split())


def edge_layer_ok(label, a, b):
    """Layer-direction policy. Adjacency alone is insufficient: requirements move down,
    evidence/support and review move up, and authority is adjacent only to L1."""
    la, lb = a["layer"], b["layer"]
    if label == "derives":
        return la == lb
    if label == "refines":
        return (a["type"] == "ctr" and lb == la + 1) or (a["type"] == "req" and lb == la)
    if label == "requests":
        return (a["type"] == "ctr" and lb == la + 1) or (a["type"] == "req" and lb == la)
    if label in ("supports", "contradicts"):
        return (a["type"] == "evd" and la == lb) or (a["type"] == "frag" and la in (lb, lb + 1))
    if label == "reviewed_by":
        return lb == la - 1
    if label == "may_create":
        return la == lb
    if label == "escalates":
        return (a["type"] == "conf" and la == lb) or (a["type"] == "esc" and lb == la - 1)
    if label == "resolved_by":
        return la == 1 and lb == 0
    if label == "revises":
        return la == 0 and lb == 1
    if label == "implements":
        return a["type"] == "frag" and la == lb + 1
    if label == "consolidated_into":
        return la == lb
    if label == "attempts":
        return a["type"] == "ctr" and b["type"] == "att" and lb == la + 1
    return abs(la - lb) <= 1


def log_path(eng):
    if not eng or any(c in eng for c in "/\\.") or len(eng) > 64:
        raise FabricError("engagement name must be a simple identifier (no dots or slashes)")
    return os.path.join(FABRIC_DIR, f"{eng}.jsonl")


def load(eng):
    path = log_path(eng)
    if not os.path.isfile(path):
        raise FabricError(f"no engagement '{eng}' at {path}")
    entries = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                entries.append(json.loads(line))
    return entries


def authority_key(create=True):
    if os.path.isfile(KEY_PATH):
        return open(KEY_PATH, "rb").read()
    if not create:
        raise FabricError(f"no signing key at {KEY_PATH}")
    os.makedirs(os.path.dirname(KEY_PATH), exist_ok=True)
    key = os.urandom(32)
    fd = os.open(KEY_PATH, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as fh:
        fh.write(key)
    return key


def confirmation_gate_active():
    """True when Claude's PreToolUse authority hook is registered.

    Codex authority attempts are deliberately blocked before this function runs; the human executes them in a terminal.
    """
    home = os.path.expanduser(os.environ.get("CLAUDE_HOME") or "~/.claude")
    for path in (os.path.join(home, "settings.json"), os.path.join(os.getcwd(), ".claude", "settings.json")):
        try:
            if "guard_authority.py" in open(path, encoding="utf-8").read():
                return True
        except OSError:
            pass
    return False


def require_human(act):
    """-> how the act was confirmed. An authority act runs only where a person confirms it: in their own
    terminal, or through Claude's approval prompt raised by the library's hook. Codex uses explicit human terminal execution."""
    if os.environ.get("FABRIC_TEST_AUTHORITY") == "1":
        return "test"
    if sys.stdin.isatty() and sys.stdout.isatty():
        return "terminal"
    if confirmation_gate_active():
        return "claude-code-approval-prompt"
    raise FabricError(
        f"{act} is an authority act, and no confirmation gate is active: the library's hook is not "
        "registered in settings.json, so nobody would be asked to approve it. Install the library, or run "
        "the command in your own terminal. A generative recommendation is not authority.")


class Fabric:
    def __init__(self, eng, entries):
        self.eng = eng
        self.entries = entries
        self.nodes = {}
        self.edges = []
        self.out = defaultdict(list)
        self.inc = defaultdict(list)
        self.seq_of = {}
        for e in entries:
            d = e["data"]
            if e["op"] == "node":
                self.nodes[d["id"]] = d
                self.seq_of[d["id"]] = e["seq"]
            elif e["op"] == "edge":
                self._index(d["src"], d["label"], d["dst"])

    def _index(self, s, p, d):
        self.edges.append((s, p, d))
        self.out[s].append((p, d))
        self.inc[d].append((s, p))

    def next_id(self, typ):
        n = sum(1 for x in self.nodes.values() if x["type"] == typ) + 1
        return f"{typ}-{n:04d}"

    def append(self, op, data, sign=False):
        prev = self.entries[-1]["hash"] if self.entries else "0" * 64
        seq = len(self.entries) + 1
        entry = {"seq": seq, "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "op": op, "data": data,
                 "prev": prev}
        entry["hash"] = hashlib.sha256((prev + canonical(data) + str(seq)).encode()).hexdigest()
        if sign:
            entry["sig"] = hmac.new(authority_key(), entry["hash"].encode(), "sha256").hexdigest()
        os.makedirs(FABRIC_DIR, exist_ok=True)
        with open(log_path(self.eng), "a", encoding="utf-8") as fh:
            fh.write(canonical(entry) + "\n")
        self.entries.append(entry)
        if op == "node":
            self.nodes[data["id"]] = data
            self.seq_of[data["id"]] = seq
        else:
            self._index(data["src"], data["label"], data["dst"])
        return entry

    # -------------------------------------------------------------- guarded mutations
    def add_node(self, typ, layer, text="", sign=False, **meta):
        if typ not in TYPES:
            raise FabricError(f"unknown node type {typ}")
        if layer not in LAYERS:
            raise FabricError(f"layer must be 0..6, got {layer}")
        if (typ == "auth") != (layer == 0) and not (typ == "rev" and layer == 0):
            raise FabricError("only authority decisions and authority reviews live at layer 0")
        node = {"id": self.next_id(typ), "type": typ, "layer": layer, "text": str(text)}
        node.update({k: v for k, v in meta.items() if v is not None})
        # 26.10.3 Native JAI Enforcement: fabric is an assurance ledger, never a
        # second semantic identity system. Every material fragment/evidence write is
        # bound to a deterministic canonical object identity plus the contract/context.
        if typ in ("frag", "evd"):
            if typ == "frag":
                payload = {"type": "semantic", "kind": node.get("kind", "claim"), "text": node["text"]}
                prefix = "semantic:" + str(node.get("kind", "claim")) + ":"
            else:
                payload = {"type": "evidence", "source": node["text"],
                           "confidence": node.get("confidence"), "sha256": node.get("sha256")}
                prefix = "evidence:"
            digest = hashlib.sha256(canonical(payload).encode()).hexdigest()
            node.setdefault("object_ref", prefix + digest)
            node.setdefault("object_hash", "sha256:" + digest)
            contract_ref = node.get("contract") or node.get("requirement") or f"fabric:{self.eng}"
            node.setdefault("contract_ref", str(contract_ref))
            if not node.get("context_digest"):
                ctx = hashlib.sha256(canonical({"contract_ref": str(contract_ref), "layer": layer}).encode()).hexdigest()
                node["context_digest"] = ctx
        self.append("node", node, sign=sign)
        return node

    def add_edge(self, src, label, dst):
        for x in (src, dst):
            if x not in self.nodes:
                raise FabricError(f"unknown node {x}")
        a, b = self.nodes[src], self.nodes[dst]
        if label not in RHO:
            raise FabricError(f"unknown relation {label}")
        if (a["type"], b["type"]) not in RHO[label]:
            raise FabricError(f"ill-typed edge: {label} does not admit {a['type']} -> {b['type']} "
                              f"(admissible: {sorted(RHO[label])})")
        if abs(a["layer"] - b["layer"]) > 1:
            raise FabricError(
                f"adjacency violation: {src} (L{a['layer']}) -{label}-> {dst} (L{b['layer']}). "
                "Layers communicate only with adjacent layers; bypassing intermediate layers "
                "skips their semantic, policy and design controls (threat T4).")
        if not edge_layer_ok(label, a, b):
            raise FabricError(
                f"layer-direction violation: {src} (L{a['layer']}) -{label}-> {dst} (L{b['layer']}). "
                "Adjacency is necessary but not sufficient: requirements/contracts flow down, "
                "support/review/escalation flow upward according to the typed relation policy.")
        if label in FORWARD and self._reaches(dst, src):
            raise FabricError(f"cycle: {src} -{label}-> {dst} would close a forward-chain cycle")
        if label == "revises" and b.get("gen", 0) <= max(
                (n.get("gen", 0) for n in self.nodes.values() if n["type"] == "req"
                 and n["id"] == b.get("supersedes")), default=-1):
            raise FabricError("revision must strictly increase the generation index (Prop. 4)")
        return self.append("edge", {"src": src, "label": label, "dst": dst})

    def _reaches(self, start, goal):
        seen, q = {start}, deque([start])
        while q:
            n = q.popleft()
            if n == goal:
                return True
            for p, d in self.out[n]:
                if p in FORWARD and d not in seen:
                    seen.add(d)
                    q.append(d)
        return False

    # ------------------------------------------------------- rounds and budgets
    def round_start(self):
        revs = [self.seq_of[n] for n, d in self.nodes.items()
                if d["type"] == "auth" and d.get("decision") == "revise"]
        return max(revs, default=0)

    def round_no(self):
        return 1 + sum(1 for d in self.nodes.values() if d["type"] == "auth" and d.get("decision") == "revise")

    def contracts_this_round(self):
        t = self.round_start()
        return sum(1 for n, d in self.nodes.items() if d["type"] == "ctr" and self.seq_of[n] > t)

    def steps_this_round(self):
        """Shared episode budget from the paper: every continuation-capable transition consumes
        from one budget. Node types are deliberately coarse-grained durable transitions."""
        t = self.round_start()
        return sum(1 for n, d in self.nodes.items()
                   if d["type"] in STEP_TYPES and self.seq_of[n] > t)

    def reformulations_this_round(self, layer):
        t = self.round_start()
        return sum(1 for n, d in self.nodes.items() if d["type"] == "req" and d.get("reformulates")
                   and d["layer"] == layer and self.seq_of[n] > t)

    # ------------------------------------------------------- escalation structure
    def esc_open(self, x):
        if any(p in ("escalates", "resolved_by") for p, _ in self.out[x]):
            return False
        return not any(d.get("reformulates") == x for d in self.nodes.values() if d["type"] == "req")

    def esc_chain(self, x):
        """Escalations from x down to the root, and the root conflicts."""
        chain, roots, cur = [], [], [x]
        while cur:
            n = cur.pop()
            if self.nodes[n]["type"] == "conf":
                roots.append(n)
                continue
            chain.append(n)
            cur.extend(s for s, p in self.inc[n] if p == "escalates")
        return chain, roots

    def origin_req(self, nid):
        """The requirement whose contract produced the work a node is about."""
        seen, q = set(), deque([nid])
        while q:
            n = q.popleft()
            if n in seen:
                continue
            seen.add(n)
            t = self.nodes[n]["type"]
            if t == "req":
                return n
            if t == "evd":
                q.extend(d for p, d in self.out[n] if p in ("supports", "contradicts"))
            step = {"conf": "may_create", "rev": "reviewed_by", "frag": "requests",
                    "ctr": "derives", "esc": "escalates"}.get(t)
            q.extend(s2 for s2, p in self.inc[n] if p == step)
        return None

    def ancestry(self, r):
        """Requirement r, its earlier formulations, then each parent layer's, up to layer 1."""
        chain, cur = [], r
        while cur and cur not in chain:
            chain.append(cur)
            nxt = None
            for s2, p in self.inc[cur]:
                if p != "refines":
                    continue
                if self.nodes[s2]["type"] == "req":
                    nxt = s2
                elif self.nodes[s2]["type"] == "ctr":
                    nxt = next((x for x, p2 in self.inc[s2] if p2 == "derives"
                                and self.nodes[x]["type"] == "req"), None)
            cur = nxt
        return chain

    def owned_formulation(self, x):
        """The newest requirement at the escalation's own layer on its path, or None."""
        _, roots = self.esc_chain(x)
        layer = self.nodes[x]["layer"]
        for c in roots:
            r = self.origin_req(c)
            for q in (self.ancestry(r) if r else []):
                if self.nodes[q]["layer"] == layer:
                    return q
        return None

    # ------------------------------------------------------------- justifiability
    def latest_review(self, f):
        revs = [d for p, d in self.out[f] if p == "reviewed_by"]
        if not revs:
            return None
        # Definition 1: highest layer (smallest index); ties -> most recently asserted.
        return min(revs, key=lambda r: (self.nodes[r]["layer"], -self.seq_of[r]))

    def support_graph(self, f):
        g = {f}
        for s, p in self.inc[f]:
            g.add(s)
            if p == "requests":
                g.update(x for x, _ in self.inc[s])
        g.update(d for p, d in self.out[f] if p == "reviewed_by")
        return g

    def conflicts_of(self, f):
        g = self.support_graph(f)
        return {d for n in g for p, d in self.out[n] if p == "may_create"}

    def resolution(self, conf):
        """Follow escalates (relayed upward) to an authority decision; return auth node or None."""
        seen, q = set(), deque(d for p, d in self.out[conf] if p == "escalates")
        while q:
            x = q.popleft()
            if x in seen:
                continue
            seen.add(x)
            for p, d in self.out[x]:
                if p == "resolved_by":
                    return self.nodes[d]
                if p == "escalates":
                    q.append(d)
        return None

    def justify(self, f, strict=False, _memo=None):
        """-> (bool, [reasons]). Paper mode is Definition 2 exactly; strict adds T1's evidence
        requirement and checks what the authority actually decided."""
        memo = {} if _memo is None else _memo
        key = (f, strict)
        if key in memo:
            return memo[key]
        memo[key] = (False, ["cycle guard"])
        why = []
        v = self.latest_review(f)
        if v is None:
            why.append("no review recorded")
        else:
            st = self.nodes[v]["state"]
            allowed = STRICT_JUSTIFYING if strict else JUSTIFYING
            if st not in allowed:
                why.append(f"latest review {v} (L{self.nodes[v]['layer']}) is '{st}'")
        for c in sorted(self.conflicts_of(f)):
            a = self.resolution(c)
            if a is None:
                why.append(f"conflict {c} has no authority decision")
            elif strict:
                if a["decision"] in ("reject", "terminate", "revise"):
                    why.append(f"conflict {c} resolved by {a['id']} as '{a['decision']}'")
                elif a["decision"] == "exception" and float(a.get("expires_epoch", 0)) < time.time():
                    why.append(f"exception {a['id']} expired {a.get('expires')}")
        if strict:
            if not self._evidence_path(f, memo):
                ai_only = any(p == "supports" and self.nodes[x]["type"] == "evd"
                              for x, p in self.inc[f])
                why.append("only AI-derived or interpretive evidence (section 10: an AI output is "
                           "evidential, not a fact)" if ai_only else
                           "no supports path to evidence (threat T1: unsupported fragment)")
        result = (not why, why)
        memo[key] = result
        return result

    def _evidence_path(self, f, memo):
        """Section 10: a subordinate AI output is an evidential fragment, not a fact. Strict mode
        therefore needs deterministic or observed evidence somewhere beneath the fragment."""
        for s, p in self.inc[f]:
            if p != "supports":
                continue
            if self.nodes[s]["type"] == "evd" and \
                    self.nodes[s].get("confidence") in ("deterministic", "observation"):
                return True
            if self.nodes[s]["type"] == "frag" and self.justify(s, True, memo)[0]:
                return True
        return False

    # ------------------------------------------------------------------- integrity
    def verify(self):
        problems, warnings = [], []
        prev = "0" * 64
        key = None
        if os.path.isfile(KEY_PATH):
            key = open(KEY_PATH, "rb").read()
        for i, e in enumerate(self.entries, start=1):
            if e["seq"] != i or e["prev"] != prev:
                problems.append(f"seq {i}: chain broken (entry reordered, removed or inserted)")
            h = hashlib.sha256((e["prev"] + canonical(e["data"]) + str(e["seq"])).encode()).hexdigest()
            if h != e["hash"]:
                problems.append(f"seq {i}: content hash mismatch (entry edited after append)")
            d = e["data"]
            needs_sig = e["op"] == "node" and d.get("layer") == 0
            if needs_sig:
                if "sig" not in e:
                    problems.append(f"{d['id']}: authority act without signature")
                elif key is None:
                    warnings.append(f"{d['id']}: signature present, key unavailable to verify")
                elif not hmac.compare_digest(
                        e["sig"], hmac.new(key, e["hash"].encode(), "sha256").hexdigest()):
                    problems.append(f"{d['id']}: authority signature invalid")
            prev = e["hash"]
        for s, p, d in self.edges:
            a, b = self.nodes[s], self.nodes[d]
            if (a["type"], b["type"]) not in RHO.get(p, ()):
                problems.append(f"ill-typed edge {s} -{p}-> {d}")
            if abs(a["layer"] - b["layer"]) > 1:
                problems.append(f"adjacency violation {s} -{p}-> {d}")
            elif not edge_layer_ok(p, a, b):
                problems.append(f"layer-direction violation {s} -{p}-> {d}")
        # acyclicity of the forward chain (Prop. 3) by DFS colouring
        colour = {}
        def dfs(n):
            colour[n] = 1
            for p, d in self.out[n]:
                if p not in FORWARD:
                    continue
                if colour.get(d) == 1:
                    problems.append(f"forward-chain cycle through {n} -> {d}")
                elif d not in colour:
                    dfs(d)
            colour[n] = 2
        for n in self.nodes:
            if n not in colour:
                dfs(n)
        for n in self.nodes.values():
            if n["type"] == "ctr":
                missing = [f for f in CONTRACT_FIELDS if not n.get("fields", {}).get(f)]
                if missing:
                    problems.append(f"{n['id']}: contract missing {missing}")
            if n["type"] == "att":
                if n.get("state") not in ("success",) + FAILURE_STATES:
                    problems.append(f"{n['id']}: invalid attempt state {n.get('state')}")
                if not n.get("contract") or not n.get("context_digest"):
                    problems.append(f"{n['id']}: attempt is not bound to contract/context")
            if n["type"] == "evd" and n.get("file"):
                try:
                    cur = hashlib.sha256(open(n["file"], "rb").read()).hexdigest()
                    if cur != n.get("sha256"):
                        warnings.append(f"{n['id']}: evidence file {n['file']} changed since recorded")
                except OSError:
                    warnings.append(f"{n['id']}: evidence file {n['file']} no longer readable")
        return problems, warnings


# ------------------------------------------------------------------------ commands
def open_fabric(eng):
    return Fabric(eng, load(eng))


def cmd_init(a):
    path = log_path(a.engagement)
    if os.path.exists(path):
        raise FabricError(f"engagement '{a.engagement}' already exists")
    fb = Fabric(a.engagement, [])
    n = fb.add_node("intent", 1, a.intent, owner=a.owner, success=a.success, boundary=a.boundary,
                    protocol="3.3", episode_budget=MAX_STEPS)
    print(f"{n['id']}  engagement '{a.engagement}' started at {path}")


def cmd_req(a):
    fb = open_fabric(a.engagement)
    src = fb.nodes.get(getattr(a, "from"))
    if src is None:
        raise FabricError(f"unknown node {getattr(a, 'from')}")
    gen = max([src.get("gen", 0)] + [0]) if src["type"] in ("req",) else 0
    n = fb.add_node("req", a.layer, a.text, gen=gen)
    fb.add_edge(src["id"], a.label, n["id"])
    print(n["id"])


def cmd_contract(a):
    fb = open_fabric(a.engagement)
    src = fb.nodes.get(getattr(a, "from"))
    if not src or src["type"] != "req":
        raise FabricError("a contract derives from a requirement node")
    fields = {f: getattr(a, f) for f in CONTRACT_FIELDS}
    missing = [f for f, v in fields.items() if not v]
    if missing:
        raise FabricError(f"contract incomplete, missing {missing}. A layer sends a contract, "
                          "not a free-form prompt.")
    rework_n = 0
    if a.rework_of:
        prior = fb.nodes.get(a.rework_of)
        if not prior or prior["type"] != "ctr":
            raise FabricError("--rework-of must name a contract")
        parent_reqs = [s for s, p in fb.inc[prior["id"]] if p == "derives" and fb.nodes[s]["type"] == "req"]
        if parent_reqs != [src["id"]]:
            raise FabricError("rework must stay on the exact same requirement lineage; use reformulate for a different requirement")
        semantic = ("what", "why", "evidence", "escalate_if")
        changed_semantics = [f for f in semantic if norm_text(fields[f]) != norm_text(prior["fields"][f])]
        if changed_semantics:
            raise FabricError(f"rework changed semantic fields {changed_semantics}; rework is a better attempt at the same "
                              "requirement. Use reformulate when meaning/evidence obligations change.")
        if not getattr(a, "change", None):
            raise FabricError("--change is required for rework: state what implementation/collection approach changes")
        rework_n = prior.get("rework_n", 0) + 1
        if rework_n > MAX_REWORK:
            # Termination (Prop. 4 extended to ordinary rework): non-convergence is a conflict,
            # raised from the latest non-justifying review, and escalated one layer up.
            lineage, cur = [], prior
            while cur is not None:                      # walk rework_of back to the original
                lineage.append(cur["id"])
                cur = fb.nodes.get(cur.get("rework_of")) if cur.get("rework_of") else None
            revs = [d for cid in lineage for p, f in fb.out[cid] if p == "requests"
                    for p2, d in fb.out[f] if p2 == "reviewed_by"]
            if not revs:
                raise FabricError("rework limit reached but no review explains why; review first")
            last = max(revs, key=lambda r: fb.seq_of[r])
            k = fb.add_node("conf", fb.nodes[last]["layer"],
                            f"rework did not converge after {MAX_REWORK} attempts on {a.rework_of}")
            fb.add_edge(last, "may_create", k["id"])
            x = fb.add_node("esc", fb.nodes[last]["layer"], "rework exhausted; reformulate or pass up",
                            code="exhausted", effective="exhausted")
            fb.add_edge(k["id"], "escalates", x["id"])
            print(f"{k['id']}  rework exhausted ({MAX_REWORK}) -> conflict")
            print(f"{x['id']}  escalated at L{x['layer']}: {next_action(fb, x['id'])[1]}")
            return 3
    check_contract_budget(fb, 1)
    check_episode_budget(fb, 1)
    n = fb.add_node("ctr", src["layer"], a.what, target_layer=src["layer"] + 1, fields=fields,
                    rework_of=a.rework_of, rework_n=rework_n, change=getattr(a, "change", None))
    fb.add_edge(src["id"], "derives", n["id"])
    print(n["id"])


def check_contract_budget(fb, needed):
    used = fb.contracts_this_round()
    if used + needed > MAX_CONTRACTS:
        raise FabricError(
            f"contract budget for round {fb.round_no()} is spent ({used}/{MAX_CONTRACTS}). The work is not "
            "converging and more attempts will not change that: raise a conflict if none exists and run "
            "'escalate <conf|esc> --to-top --code budget', then hand the operator the dossier.")


def check_episode_budget(fb, needed=1):
    used = fb.steps_this_round()
    if used + needed > MAX_STEPS:
        raise FabricError(
            f"shared episode budget for round {fb.round_no()} is spent ({used}/{MAX_STEPS}). "
            "All continuation-capable transitions share this budget; do not hide retries in tool calls. "
            "Escalate to the operator with code budget and the mechanically compiled dossier.")


def engagement_protocol(fb):
    intents = [d for d in fb.nodes.values() if d["type"] == "intent"]
    return intents[0].get("protocol", "3.2") if intents else "3.2"


def contract_context_packet(fb, c):
    parents = [s for s, p in fb.inc[c["id"]] if p == "derives" and fb.nodes[s]["type"] == "req"]
    parent = fb.nodes[parents[0]] if len(parents) == 1 else None
    packet = {
        "engagement": fb.eng,
        "contract": c["id"],
        "source_requirement": parent["id"] if parent else None,
        "source_text": parent["text"] if parent else None,
        "target_layer": c["target_layer"],
        "fields": c["fields"],
        "rework_of": c.get("rework_of"),
        "rework_n": c.get("rework_n", 0),
        "change": c.get("change"),
    }
    digest = hashlib.sha256(canonical(packet).encode()).hexdigest()
    return packet, digest


def cmd_render(a):
    fb = open_fabric(a.engagement)
    c = fb.nodes.get(a.contract)
    if not c or c["type"] != "ctr":
        raise FabricError("not a contract")
    f = c["fields"]
    t = c["target_layer"]
    packet, digest = contract_context_packet(fb, c)
    print(f"""CONTRACT {c['id']}  (engagement {fb.eng}; L{c['layer']} {LAYERS[c['layer']]} -> L{t} {LAYERS[t]})
{'REWORK ' + str(c['rework_n']) + ' of ' + c['rework_of'] if c.get('rework_of') else ''}
CONTEXT SHA256 {digest}
WHAT        {f['what']}
WHY         {f['why']}
WHO         {f['who']}
WHERE       {f['where']}
WHEN        {f['when']}
HOW         {f['how']}
EVIDENCE    {f['evidence']}
ESCALATE IF {f['escalate_if']}
SANITISE    {f['sanitise']}

You are a Layer {t} ({LAYERS[t]}) agent. This contract is your whole brief: you have no other
context and must not assume any. Return ONLY a JSON object with these keys:
  "context_digest": "{digest}"   (must echo this exact digest; it binds your answer to this packet)
  "fragments":  [{{"key": "f1", "text": "...", "kind": "claim|design|artefact|finding|hypothesis|recommendation"}}]
  "evidence":   [{{"supports": ["f1"], "contradicts": [], "source": "...", "confidence":
                 "deterministic|observation|interpretation|ai_derived", "file": "optional/path"}}]
  "conflicts":  [{{"raised_by": "f1", "text": "why the contract cannot be met as written"}}]
  "uncertainty": "what remains unknown or out of scope"
  "proposals":  [{{"text": "a requirement you COULD meet", "tradeoff": "what it gives up"}}]
                 (whenever you raise a conflict and can see a version of the contract the evidence supports)
  "derived_requirements": [{{"key": "r1", "text": "...", "contract": {{"what": "...", "why": "...",
                 "who": "...", "where": "...", "when": "...", "how": "...", "evidence": "...",
                 "escalate_if": "...", "sanitise": "..."}}}}]   (going down; not at Layer 6)
  A fragment answering upward may carry "supported_by": ["frag-NNNN"] naming fragments from the
  layer below that this layer has already accepted in review.
Object by evidence, never by silently changing the purpose. If the contract cannot be met, return
a conflict; do not return a weakened fragment that pretends to meet it.""")


def cmd_packet(a):
    fb = open_fabric(a.engagement)
    c = fb.nodes.get(a.contract)
    if not c or c["type"] != "ctr":
        raise FabricError("not a contract")
    packet, digest = contract_context_packet(fb, c)
    print(json.dumps({"context_digest": digest, "packet": packet}, ensure_ascii=False, indent=2))


def cmd_ingest(a):
    """Two-phase and atomic: the whole message is validated before anything is appended, so a
    rejected message leaves no orphan nodes in an append-only log."""
    fb = open_fabric(a.engagement)
    c = fb.nodes.get(a.contract)
    if not c or c["type"] != "ctr":
        raise FabricError("--contract must name a contract")
    raw = sys.stdin.read() if a.result == "-" else open(a.result, encoding="utf-8").read()
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end < start:
        raise FabricError("no JSON object in the agent result")
    doc = json.loads(raw[start:end + 1])
    allowed = {"context_digest", "fragments", "evidence", "conflicts", "uncertainty", "derived_requirements", "proposals"}
    extra = set(doc) - allowed
    if extra:
        raise FabricError(f"unexpected keys {sorted(extra)}: cross-layer messages are typed")
    layer = c["target_layer"]
    expected_digest = contract_context_packet(fb, c)[1]
    if engagement_protocol(fb) >= "3.3" and doc.get("context_digest") != expected_digest:
        raise FabricError("agent result is not bound to the rendered context packet: context_digest missing or mismatched")

    # ---------------- phase 1: validate everything
    if doc.get("derived_requirements"):
        check_contract_budget(fb, len(doc["derived_requirements"]))
    for pr in doc.get("proposals", []):
        if not pr.get("text") or not pr.get("tradeoff"):
            raise FabricError("a proposal needs 'text' (the reformulated requirement) and 'tradeoff' "
                              "(what it gives up): an option without its cost is not an option")
    keys = [fr.get("key") for fr in doc.get("fragments", [])]
    if len(keys) != len(set(keys)):
        raise FabricError("fragment keys must be unique within a message")
    for dr in doc.get("derived_requirements", []):
        if layer >= 6:
            raise FabricError("Layer 6 is the substrate: it returns evidence, not requirements")
        missing = [f for f in CONTRACT_FIELDS if not (dr.get("contract") or {}).get(f)]
        if missing:
            raise FabricError(f"derived requirement '{dr.get('key')}' has an incomplete contract, "
                              f"missing {missing}")
    for fr in doc.get("fragments", []):
        for child in fr.get("supported_by", []):
            ch = fb.nodes.get(child)
            if not ch or ch["type"] != "frag" or ch["layer"] != layer + 1:
                raise FabricError(f"supported_by {child}: must be a fragment from L{layer + 1}")
            v = fb.latest_review(child)
            if v is None or fb.nodes[v]["layer"] != layer or fb.nodes[v]["state"] not in JUSTIFYING:
                raise FabricError(
                    f"{child} has not been accepted by this layer's review, so it cannot support "
                    "an upward fragment. Review it first; build only on qualified outputs.")
    for ev in doc.get("evidence", []):
        conf = ev.get("confidence", "ai_derived")
        if conf not in CONFIDENCE:
            raise FabricError(f"evidence confidence must be one of {CONFIDENCE}")
        if ev.get("file") and not os.path.isfile(ev["file"]):
            raise FabricError(f"evidence file {ev['file']} does not exist")
        if conf == "deterministic" and not ev.get("file"):
            raise FabricError("deterministic evidence must point at a file the runtime can hash")
        for k in ev.get("supports", []) + ev.get("contradicts", []):
            if k not in keys:
                raise FabricError(f"evidence refers to unknown fragment key '{k}'")
    for cf in doc.get("conflicts", []):
        if cf.get("raised_by") is not None and cf["raised_by"] not in keys:
            raise FabricError(f"conflict raised_by unknown fragment key '{cf['raised_by']}'")
    if not (doc.get("fragments") or doc.get("derived_requirements") or doc.get("conflicts")
            or doc.get("proposals")):
        raise FabricError("empty message: return fragments, derived requirements or a conflict")

    # ---------------- phase 2: apply
    check_episode_budget(fb, 1 + len(doc.get("derived_requirements", [])))
    att = fb.add_node("att", layer, "delegated contract execution", state="success",
                      contract=c["id"], context_digest=expected_digest)
    fb.add_edge(c["id"], "attempts", att["id"])
    for dr in doc.get("derived_requirements", []):
        cf = dr["contract"]
        r = fb.add_node("req", layer, dr.get("text", ""), gen=0)
        fb.add_edge(c["id"], "refines", r["id"])
        child = fb.add_node("ctr", layer, cf["what"], target_layer=layer + 1,
                            fields={f: str(cf[f]) for f in CONTRACT_FIELDS}, rework_n=0)
        fb.add_edge(r["id"], "derives", child["id"])
        print(f"{r['id']}  derived requirement  L{layer}  ->  {child['id']}  contract for L{layer + 1}")
    keymap = {}
    for fr in doc.get("fragments", []):
        n = fb.add_node("frag", layer, fr.get("text", ""), kind=fr.get("kind", "claim"),
                        contract=c["id"], uncertainty=doc.get("uncertainty"))
        fb.add_edge(c["id"], "requests", n["id"])
        # No implements edge back to the same contract: requests already records the causal
        # link, and both labels are forward-chain, so the pair would be a 2-cycle (Prop. 3).
        for child in fr.get("supported_by", []):
            fb.add_edge(child, "supports", n["id"])
        keymap[fr.get("key", n["id"])] = n["id"]
        print(f"{n['id']}  fragment  L{layer}")
    for ev in doc.get("evidence", []):
        e = make_evidence(fb, layer, ev.get("source", ""), ev.get("confidence", "ai_derived"),
                          ev.get("file"))
        for k in ev.get("supports", []):
            fb.add_edge(e["id"], "supports", keymap[k])
        for k in ev.get("contradicts", []):
            fb.add_edge(e["id"], "contradicts", keymap[k])
        print(f"{e['id']}  evidence  {e['confidence']}")
    for pr in doc.get("proposals", []):
        n = fb.add_node("frag", layer, pr["text"], kind="reformulation", tradeoff=pr["tradeoff"],
                        contract=c["id"], proposed_by=f"L{layer}")
        fb.add_edge(c["id"], "requests", n["id"])
        print(f"{n['id']}  reformulation proposal  L{layer}")
    for cf in doc.get("conflicts", []):
        src = keymap.get(cf.get("raised_by"))
        if src is None:
            frag = fb.add_node("frag", layer, "conflict raised against the contract",
                               kind="objection", contract=c["id"])
            fb.add_edge(c["id"], "requests", frag["id"])
            src = frag["id"]
        k = fb.add_node("conf", layer, cf.get("text", ""))
        fb.add_edge(src, "may_create", k["id"])
        print(f"{k['id']}  conflict  raised by {src}")


def cmd_failure(a):
    """Record an unsuccessful delegated step as a first-class outcome and select the next legal
    transition deterministically. Retryable failures stay local until bounded rework is exhausted."""
    fb = open_fabric(a.engagement)
    c = fb.nodes.get(a.contract)
    if not c or c["type"] != "ctr":
        raise FabricError("--contract must name a contract")
    check_episode_budget(fb, 1)
    digest = contract_context_packet(fb, c)[1]
    att = fb.add_node("att", c["target_layer"], a.reason, state=a.state, contract=c["id"],
                      actor=a.actor, model=a.model, context_digest=digest)
    fb.add_edge(c["id"], "attempts", att["id"])
    left = MAX_REWORK - c.get("rework_n", 0)
    budget_left = MAX_STEPS - fb.steps_this_round()
    klass = failure_class(a.state)
    if klass == "retryable" and left > 0 and budget_left > 0:
        print(f"{att['id']}  {a.state}; local repair required before escalation")
        print(f"NEXT rework  remaining={left}  shared_budget={budget_left}")
        print("Create --rework-of this contract, preserve what/why/evidence/escalate-if exactly, "
              "and change only the execution/collection approach with --change.")
        return 0
    code = "contradiction" if klass == "contradictory" else \
           ("budget" if budget_left <= 0 else "exhausted")
    reason = (f"{a.state}: {a.reason}; local repair budget exhausted" if code != "contradiction"
              else f"{a.state}: {a.reason}; retry would not resolve contrary evidence")
    k = fb.add_node("conf", c["target_layer"], reason)
    # The contract owner is the accountable source for a failed delegated attempt.
    fb.add_edge(c["id"], "requests", fb.add_node("frag", c["target_layer"],
                f"failed attempt {att['id']}", kind="failure", contract=c["id"])["id"])
    failure_frag = max((n for n, d in fb.nodes.items() if d.get("kind") == "failure" and d.get("contract") == c["id"]),
                       key=fb.seq_of.get)
    fb.add_edge(failure_frag, "may_create", k["id"])
    x = fb.add_node("esc", c["target_layer"], reason, code=code, effective=code)
    fb.add_edge(k["id"], "escalates", x["id"])
    print(f"{att['id']}  {a.state}; {k['id']} -> {x['id']} [{code}]")
    print(f"NEXT {next_action(fb, x['id'])[1]}")
    return 3


def cmd_policy(a):
    print(json.dumps(supervision_policy(), ensure_ascii=False, indent=2))


def impact_dependents(fb, changed):
    """Return fragments whose justification transitively depends on changed through explicit
    support/consolidation/request edges. This is the runtime counterpart of affected/4."""
    q, seen, out = deque([changed]), {changed}, set()
    labels = {"supports", "consolidated_into", "requests"}
    while q:
        cur = q.popleft()
        for p, dst in fb.out[cur]:
            if p not in labels or dst in seen:
                continue
            seen.add(dst); q.append(dst)
            if fb.nodes[dst]["type"] == "frag":
                out.add(dst)
    return sorted(out, key=fb.seq_of.get)


def cmd_invalidate(a):
    fb = open_fabric(a.engagement)
    if a.changed not in fb.nodes:
        raise FabricError(f"unknown changed reference {a.changed}")
    affected = impact_dependents(fb, a.changed)
    if not affected:
        print(f"no dependent fragments for {a.changed}")
        return 0
    for f in affected:
        layer = fb.nodes[f]["layer"]
        k = fb.add_node("conf", layer, f"dependency {a.changed} changed: {a.reason}",
                        changed_ref=a.changed, invalidation=True)
        fb.add_edge(f, "may_create", k["id"])
        print(f"{f} INVALIDATED by {a.changed} -> {k['id']}")
    print("Revalidate affected branches; prior release eligibility is intentionally lost until the new "
          "evidence/review chain resolves these conflicts.")


def cmd_answer(a):
    """A layer answers its own requirement directly (the Intent layer's product, which has no
    contract above it). Supporting fragments must already be accepted by this layer."""
    fb = open_fabric(a.engagement)
    r = fb.nodes.get(a.requirement)
    if not r or r["type"] != "req":
        raise FabricError("answer targets a requirement")
    layer = r["layer"]
    for child in a.supported_by:
        ch = fb.nodes.get(child)
        v = fb.latest_review(child) if ch else None
        if not ch or ch["type"] != "frag" or ch["layer"] != layer + 1:
            raise FabricError(f"{child}: must be a fragment from L{layer + 1}")
        if v is None or fb.nodes[v]["layer"] != layer or fb.nodes[v]["state"] not in JUSTIFYING:
            raise FabricError(f"{child} is not accepted by an L{layer} review; build only on qualified outputs")
    n = fb.add_node("frag", layer, a.text, kind="product", requirement=r["id"])
    fb.add_edge(r["id"], "requests", n["id"])
    for child in a.supported_by:
        fb.add_edge(child, "supports", n["id"])
    print(f"{n['id']}  product fragment  L{layer}")


def cmd_release(a):
    """The release gate: a product leaves the engagement only if the fabric entitles it."""
    fb = open_fabric(a.engagement)
    f = fb.nodes.get(a.fragment)
    if not f or f["type"] != "frag":
        raise FabricError("release names a fragment")
    problems, warnings = fb.verify()
    ok, why = fb.justify(f["id"], strict=True)
    # A product justified on evidence that no longer matches its recorded hash has lost its
    # justification: drift blocks release rather than merely warning.
    why += [f"evidence drift: {w}" for w in warnings if "changed since recorded" in w
            or "no longer readable" in w]
    v = fb.latest_review(f["id"])
    if f["layer"] != 1:
        why.append(f"only an Intent-layer product can be released (this is L{f['layer']})")
    if v is None or fb.nodes[v]["layer"] != 0 or fb.nodes[v]["state"] not in STRICT_JUSTIFYING:
        why.append("no signed authority acceptance (layer-0 review) of this product")
    why += [f"fabric integrity: {p}" for p in problems]
    if why:
        print(f"NOT RELEASABLE  {f['id']}")
        for w in why:
            print(f"  - {w}")
        return 1
    print(f"RELEASABLE  {f['id']}: strict-justifiable, authority-accepted by "
          f"{fb.nodes[v].get('reviewer')}, fabric verified.")
    return 0


def cmd_render_review(a):
    fb = open_fabric(a.engagement)
    c = fb.nodes.get(a.contract)
    if not c or c["type"] != "ctr":
        raise FabricError("not a contract")
    frags = [d for p, d in fb.out[c["id"]] if p == "requests"]
    reviewer = c["layer"]
    print(f"REVIEW for L{reviewer} {LAYERS[reviewer]}: fragments returned by "
          f"L{c['target_layer']} against {c['id']}\n")
    print("Contract they answered:")
    for f in CONTRACT_FIELDS:
        print(f"  {f.upper():<12} {c['fields'][f]}")
    for f in frags:
        n = fb.nodes[f]
        ev = [fb.nodes[s] for s, p in fb.inc[f] if p in ("supports", "contradicts")]
        print(f"\n{f}  [{n.get('kind')}]  {n['text']}")
        for e in ev:
            rel = next(p for s2, p in fb.inc[f] if s2 == e["id"])
            print(f"    {rel:<11} {e['id']}  {e['type']}  {e.get('confidence', '')}  "
                  f"{e.get('source', e['text'])[:90]}" + (f"  file={e['file']}" if e.get("file") else ""))
        if n.get("uncertainty"):
            print(f"    uncertainty: {n['uncertainty']}")
    print(f"""
Review each fragment against the contract above. Assign exactly one state:
  {', '.join(STATES)}
Return ONLY JSON: {{"reviews": [{{"fragment": "frag-NNNN", "state": "...", "rationale": "...",
  "constraints": "required for accepts_with_constraints"}}]}}
A fragment with no evidence cannot be better than 'resonates'. Do not accept on fluency.""")


def cmd_ingest_reviews(a):
    fb = open_fabric(a.engagement)
    raw = sys.stdin.read() if a.result == "-" else open(a.result, encoding="utf-8").read()
    doc = json.loads(raw[raw.find("{"):raw.rfind("}") + 1])
    if set(doc) - {"reviews"}:
        raise FabricError("review messages carry only 'reviews'")
    for rv in doc["reviews"]:
        ns = argparse.Namespace(engagement=a.engagement, fragment=rv.get("fragment"), layer=a.layer,
                                state=rv.get("state"), rationale=rv.get("rationale", ""),
                                reviewer=a.reviewer, model=a.model, constraints=rv.get("constraints"))
        if a.layer == 0:
            raise FabricError("authority reviews are recorded one at a time with 'review --layer 0'")
        cmd_review(ns)



def cmd_dossier(a):
    """A decision packet for the operator, compiled mechanically from the fabric. Nothing in it is
    generated: the examples are the recorded failed attempts, the options are recorded proposals."""
    fb = open_fabric(a.engagement)
    x = fb.nodes.get(a.escalation)
    if not x or x["type"] != "esc":
        raise FabricError("dossier is built for an escalation")
    chain, roots = fb.esc_chain(x["id"])
    path = sorted(chain, key=lambda e: -fb.nodes[e]["layer"])          # bottom first
    intent = next(n for n in fb.nodes.values() if n["type"] == "intent")
    anc = []
    for c in roots:
        r = fb.origin_req(c)
        for q in (fb.ancestry(r) if r else []):
            if q not in anc:
                anc.append(q)
    by_layer = defaultdict(list)
    for q in anc:
        by_layer[fb.nodes[q]["layer"]].append(q)
    ctr_of = {q: [d for p2, d in fb.out[q] if p2 == "derives" and fb.nodes[d]["type"] == "ctr"] for q in anc}
    cut = lambda t, n=280: (str(t).replace("\n", " ")[:n] + ("…" if len(str(t)) > n else ""))

    def attempts(q):
        for c in sorted(ctr_of[q], key=fb.seq_of.get):
            for p2, f in fb.out[c]:
                if p2 == "requests" and fb.nodes[f].get("kind") != "reformulation":
                    yield c, f

    def failed(f):
        v = fb.latest_review(f)
        return v is None or fb.nodes[v]["state"] not in STRICT_JUSTIFYING or bool(fb.conflicts_of(f))

    L = [f"# Decision dossier — {fb.eng} / {x['id']}", ""]
    used = {k: fb.reformulations_this_round(k) for k in range(1, 7)}
    L += [f"Round **{fb.round_no()}** of {MAX_ROUNDS} · contracts this round {fb.contracts_this_round()}/"
          f"{MAX_CONTRACTS} · reformulations used " +
          ", ".join(f"L{k} {v}/{MAX_REFORMULATE}" for k, v in used.items() if v) or "none", ""]

    root_text = "; ".join(cut(fb.nodes[c]["text"], 200) for c in roots)
    L += ["## Decision required", "",
          f"The work cannot meet its requirement as currently formulated: {root_text}", ""]
    if x.get("effective") == "outside_authority":
        L += ["This is an **authority matter**: it needs a decision no layer is entitled to make "
              "(risk acceptance, scope, removing a control, or reinterpreting the intent). The layers relayed "
              "it without attempting reformulation.", ""]

    L += ["## Context", "",
          f"**Intent (verbatim).** {intent['text']}  ",
          f"**Owner.** {intent.get('owner', '-')}", ""]
    for k in sorted(by_layer):
        cur = by_layer[k][0]
        L.append(f"- **L{k} {LAYERS[k]}** currently requires: “{cut(fb.nodes[cur]['text'], 200)}” (`{cur}`)")
    L.append("")

    L += ["## How it got here", "", "| Layer | Escalation | Why the layer passed it up |", "| --- | --- | --- |"]
    for e in path:
        d = fb.nodes[e]
        L.append(f"| L{d['layer']} | `{e}` [{d.get('effective', d.get('code', '?'))}] | {cut(d['text'], 160)} |")
    L.append("")

    L += ["## What was tried, with examples", ""]
    objections = defaultdict(list)
    shown = 0
    for k in sorted(by_layer, reverse=True):
        forms = list(reversed(by_layer[k]))                          # oldest first
        L.append(f"### L{k} {LAYERS[k]} — {len(forms)} formulation{'s' if len(forms) > 1 else ''}")
        L.append("")
        for i, q in enumerate(forms, 1):
            d = fb.nodes[q]
            att = list(attempts(q))
            bad = [(c, f) for c, f in att if failed(f)]
            label = "original" if not d.get("previous") else f"reformulation {d.get('reformulation_n', '?')}"
            L.append(f"{i}. `{q}` ({label}): “{cut(d['text'], 220)}”")
            if d.get("change"):
                L.append(f"   - *What changed:* {cut(d['change'], 220)}")
            L.append(f"   - *Outcome:* {len(att)} attempt{'s' if len(att) != 1 else ''}, {len(bad)} not accepted"
                     if att else "   - *Outcome:* no direct attempts yet; the work under it failed further down")
            for c, f in bad:
                v = fb.latest_review(f)
                if v:
                    objections[norm_text(fb.nodes[v]["text"])].append((f, fb.nodes[v]["text"]))
            if bad and shown < a.examples:
                c, f = bad[-1]                                       # the latest failure is the most informative
                v = fb.latest_review(f)
                cf = fb.nodes[c]["fields"]
                L.append(f"   - *Example — latest failed attempt:*")
                L.append(f"     - asked (`{c}`): {cut(cf['what'], 160)} · how: {cut(cf['how'], 120)} · "
                         f"evidence required: {cut(cf['evidence'], 120)}")
                L.append(f"     - returned (`{f}`, L{fb.nodes[f]['layer']}): {cut(fb.nodes[f]['text'])}")
                if v:
                    vd = fb.nodes[v]
                    L.append(f"     - reviewed by L{vd['layer']} as **{vd['state']}**: {cut(vd['text'])}")
                else:
                    L.append("     - never reviewed")
                for s2, p2 in fb.inc[f]:
                    if fb.nodes[s2]["type"] == "evd":
                        e = fb.nodes[s2]
                        L.append(f"     - evidence {p2} (`{s2}`, {e.get('confidence')}): {cut(e.get('source', ''), 120)}"
                                 + (f" — file `{e['file']}`" if e.get("file") else ""))
                for cc in sorted(fb.conflicts_of(f)):
                    L.append(f"     - conflict `{cc}`: {cut(fb.nodes[cc]['text'], 200)}")
                shown += 1
        L.append("")
    rec = [(len(v), v[0][1]) for v in objections.values() if len(v) > 1]
    if rec:
        L += ["**Recurring objections** (the same review rationale on several attempts usually means the "
              "requirement, not the attempt, is the problem):", ""]
        for n, t in sorted(rec, reverse=True)[:5]:
            L.append(f"- ×{n}: {cut(t, 200)}")
        L.append("")

    tried = {norm_text(fb.nodes[q]["text"]): q for q in anc}
    reqs_and_ctrs = set(anc) | {c for q in anc for c in ctr_of[q]}
    props = [n for n, d in fb.nodes.items() if d.get("kind") == "reformulation"
             and any(s2 in reqs_and_ctrs for s2, p2 in fb.inc[n] if p2 == "requests")]
    L += ["## Options surfaced so far", ""]
    if props:
        L += ["| Proposal | From | Reformulated requirement | Trade-off | Status |", "| --- | --- | --- | --- | --- |"]
        for n in sorted(props, key=fb.seq_of.get):
            d = fb.nodes[n]
            st = f"already tried as `{tried[norm_text(d['text'])]}`" if norm_text(d["text"]) in tried else "adoptable"
            L.append(f"| `{n}` | {d.get('proposed_by', 'L' + str(d['layer']))} | {cut(d['text'], 200)} | "
                     f"{cut(d.get('tradeoff', '-'), 160)} | {st} |")
    else:
        L.append("No layer proposed a reformulation. That itself is information: nobody below can see a "
                 "version of this requirement that the evidence would support.")
    L += ["", "Always available: rewrite the requirement yourself; grant a time-bound **exception** if a "
          "control cannot be met and the risk is acceptable for a period; **reject** the work; or "
          "**terminate** the engagement.", ""]

    prior = [d for d in fb.nodes.values() if d["type"] == "auth" and d.get("decision") == "revise"]
    if prior:
        L += ["## Earlier rounds", ""]
        for d in sorted(prior, key=lambda d: d.get("round", 0)):
            L.append(f"- Round {d.get('round')}: revised by {d.get('signer')}"
                     + (f", adopting `{d['adopted']}`" if d.get("adopted") else "") + f" — {cut(d['text'], 160)}")
        L.append("")

    cmd = f"python3 ~/.ai/it-role-house/fabric/fabric.py authorise {fb.eng} {x['id']}"
    over = " --beyond-round-limit" if fb.round_no() >= MAX_ROUNDS else ""
    L += ["## Your decision", "", "Tell the orchestrator which you choose: it runs that command and Claude Code asks "
          "you to approve it. Or run it yourself in a terminal.", "", "```bash"]
    for n in props:
        if norm_text(fb.nodes[n]["text"]) not in tried:
            L.append(f"{cmd} --decision revise --adopt {n}{over} --signer \"<you>\" --rationale \"<why>\"")
    L += [f"{cmd} --decision revise --revise-text \"<your formulation>\"{over} --signer \"<you>\" --rationale \"<why>\"",
          f"{cmd} --decision exception --expires <days> --signer \"<you>\" --rationale \"<why the risk is acceptable>\"",
          f"{cmd} --decision reject --signer \"<you>\" --rationale \"<why>\"",
          f"{cmd} --decision terminate --signer \"<you>\" --rationale \"<why>\"", "```", ""]
    if x["layer"] != 1:
        L += [f"**Not yet decidable:** `{x['id']}` is at L{x['layer']}. It must be relayed to L1 first; this "
              "dossier is a preview.", ""]
    print("\n".join(L))


def make_evidence(fb, layer, source, confidence, path):
    if confidence not in CONFIDENCE:
        raise FabricError(f"confidence must be one of {CONFIDENCE}")
    meta = {"source": source, "confidence": confidence}
    if path:
        p = os.path.abspath(path)
        if not os.path.isfile(p):
            raise FabricError(f"evidence file {p} does not exist: evidence is not a description of a file")
        meta.update(file=p, sha256=hashlib.sha256(open(p, "rb").read()).hexdigest(),
                    size=os.path.getsize(p))
    elif confidence == "deterministic":
        raise FabricError("deterministic evidence must point at a file or output the tool can hash")
    return fb.add_node("evd", layer, source, **meta)


def cmd_evidence(a):
    fb = open_fabric(a.engagement)
    check_episode_budget(fb, 1)
    e = make_evidence(fb, a.layer, a.source, a.confidence, a.file)
    for f in a.supports or []:
        fb.add_edge(e["id"], "supports", f)
    for f in a.contradicts or []:
        fb.add_edge(e["id"], "contradicts", f)
    print(e["id"])


def cmd_review(a):
    fb = open_fabric(a.engagement)
    f = fb.nodes.get(a.fragment)
    if not f or f["type"] != "frag":
        raise FabricError("review targets a fragment")
    if a.state not in STATES:
        raise FabricError(f"state must be one of {STATES}")
    if a.layer != f["layer"] - 1:
        raise FabricError(f"reviews move exactly one layer upward: fragment is L{f['layer']}, reviewer must be L{f['layer'] - 1}")
    if a.state == "accepts_with_constraints" and not a.constraints:
        raise FabricError("accepts_with_constraints needs --constraints: the conditions are the point")
    sign = a.layer == 0
    via = require_human("an authority review") if sign else None
    check_episode_budget(fb, 1)
    r = fb.add_node("rev", a.layer, a.rationale, state=a.state, reviewer=a.reviewer, model=a.model,
                    constraints=a.constraints, target=f["id"], sign=sign, approved_via=via)
    fb.add_edge(f["id"], "reviewed_by", r["id"])
    print(f"{r['id']}  {a.state}")
    if a.state in ("conflicts", "escalate"):
        k = fb.add_node("conf", a.layer, f"review {r['id']}: {a.rationale}")
        fb.add_edge(r["id"], "may_create", k["id"])
        print(f"{k['id']}  conflict recorded from review")


def cmd_consolidate(a):
    """Same-layer reviews from independent agents: keep the weakest, and surface disagreement
    as a conflict rather than averaging it away (threat T6)."""
    fb = open_fabric(a.engagement)
    revs = [d for p, d in fb.out[a.fragment] if p == "reviewed_by" and fb.nodes[d]["layer"] == a.layer]
    if len(revs) < 2:
        raise FabricError("consolidation needs at least two same-layer reviews")
    states = [fb.nodes[r]["state"] for r in revs]
    weakest = max(states, key=lambda s: RANK[s])
    disagree = len({s in JUSTIFYING for s in states}) > 1
    check_episode_budget(fb, 1)
    r = fb.add_node("rev", a.layer, f"consolidated from {', '.join(revs)}: {states}",
                    state=weakest, reviewer="consolidation", model="n/a", target=a.fragment,
                    consolidated=revs)
    fb.add_edge(a.fragment, "reviewed_by", r["id"])
    print(f"{r['id']}  consolidated as '{weakest}'")
    if disagree:
        k = fb.add_node("conf", a.layer, f"independent reviewers disagree: {dict(zip(revs, states))}")
        fb.add_edge(r["id"], "may_create", k["id"])
        print(f"{k['id']}  disagreement surfaced as a conflict")


def cmd_conflict(a):
    fb = open_fabric(a.engagement)
    k = fb.add_node("conf", a.layer, a.text)
    fb.add_edge(getattr(a, "from"), "may_create", k["id"])
    print(k["id"])


def escalate_one(fb, src_id, layer, code, reason):
    src = fb.nodes.get(src_id)
    if not src or src["type"] not in ("conf", "esc"):
        raise FabricError("escalate from a conflict, or relay an escalation upward")
    if code not in ESC_CODES:
        raise FabricError(f"--code must be one of {ESC_CODES}")
    if src["type"] == "conf":
        if layer != src["layer"]:
            raise FabricError(f"a conflict escalates first at its own layer (L{src['layer']}); that layer "
                              "decides whether it can reformulate before anything moves up")
        if code == "relay":
            raise FabricError("a conflict is escalated for a reason, not relayed: use exhausted, "
                              "no_viable_reformulation, outside_authority or budget")
        effective = code
    else:
        if layer != src["layer"] - 1:
            raise FabricError("L1 is the top of the stack: this escalation is for the operator now; run "
                              "'dossier'" if src["layer"] == 1 else
                              f"escalations move strictly upward: from L{src['layer']} only to "
                              f"L{src['layer'] - 1}. Sideways or downward hops are how a process loops.")
        if not fb.esc_open(src_id):
            raise FabricError(f"{src_id} has already been relayed, resolved or answered by a reformulation")
        prev = src.get("effective")
        if prev in STICKY and code not in ("relay", prev):
            raise FabricError(f"a {prev} escalation can only be relayed: no layer may downgrade it on its "
                              "way up" if prev == "outside_authority" else
                              f"a {prev} escalation can only be relayed until the operator decides")
        effective = prev if prev in STICKY else code
    if src["type"] == "conf" and any(p == "escalates" for p, _ in fb.out[src_id]):
        raise FabricError(f"{src_id} is already escalated")
    x = fb.add_node("esc", layer, reason, code=code, effective=effective)
    fb.add_edge(src_id, "escalates", x["id"])
    return x


def cmd_escalate(a):
    fb = open_fabric(a.engagement)
    src = fb.nodes.get(getattr(a, "from"))
    if not src:
        raise FabricError(f"unknown node {getattr(a, 'from')}")
    if a.to_top:
        cur, layer = src["id"], src["layer"] if src["type"] == "conf" else src["layer"] - 1
        code = a.code
        while layer >= 1:
            if code != "budget":
                check_episode_budget(fb, 1)
            hop = code if fb.nodes[cur]["type"] == "conf" or code in STICKY else "relay"
            x = escalate_one(fb, cur, layer, hop, a.reason)
            print(f"{x['id']}  L{layer}  [{x['effective']}]")
            cur, layer = x["id"], layer - 1
        print("ready for the operator: run 'dossier' and stop")
        return 0
    if a.layer is None:
        raise FabricError("--layer is required unless --to-top")
    if a.code != "budget":
        check_episode_budget(fb, 1)
    x = escalate_one(fb, src["id"], a.layer, a.code, a.reason)
    ok, nxt = next_action(fb, x["id"])
    if a.layer == 1 and not ok:
        nxt = "ready for the operator: run 'dossier' and stop"
    print(f"{x['id']}  L{a.layer}  [{x['effective']}]  {nxt}")


def next_action(fb, x):
    """-> (may_reformulate, reason). The single rule for what an open escalation allows."""
    d, k = fb.nodes[x], fb.nodes[x]["layer"]
    eff = d.get("effective")
    arrived = any(fb.nodes[s2]["type"] == "esc" for s2, p in fb.inc[x] if p == "escalates")
    top = "the operator" if k == 1 else f"L{k - 1}"
    if eff == "outside_authority":
        return False, f"authority matter: relay to {top}; no layer may reformulate it"
    if eff == "budget":
        return False, f"round budget spent: relay to {top}"
    if not arrived and d.get("code") == "no_viable_reformulation":
        return False, f"L{k} declared it cannot reformulate: relay to {top}"
    if fb.owned_formulation(x) is None:
        return False, f"L{k} owns no requirement on this path (it received the infeasible contract): relay to {top}"
    left = MAX_REFORMULATE - fb.reformulations_this_round(k)
    if left <= 0:
        return False, f"L{k} has spent its {MAX_REFORMULATE} reformulations this round: relay to {top}"
    return True, f"L{k} may reformulate ({left} left this round) or relay to {top}"


def cmd_propose(a):
    fb = open_fabric(a.engagement)
    r = fb.nodes.get(a.requirement)
    if not r or r["type"] != "req":
        raise FabricError("a proposal is made against a requirement")
    n = fb.add_node("frag", r["layer"], a.text, kind="reformulation", tradeoff=a.tradeoff,
                    proposed_by=f"L{r['layer']}")
    fb.add_edge(r["id"], "requests", n["id"])
    print(f"{n['id']}  reformulation proposal  L{r['layer']}")


def cmd_reformulate(a):
    """The layer that owns the strained requirement restates it and tries again, within budget."""
    fb = open_fabric(a.engagement)
    x = fb.nodes.get(a.escalation)
    if not x or x["type"] != "esc":
        raise FabricError("reformulate answers an escalation")
    if not fb.esc_open(x["id"]):
        raise FabricError(f"{x['id']} is no longer open")
    k = x["layer"]
    if x.get("effective") == "outside_authority":
        raise FabricError("this is an authority matter (risk acceptance, scope, a control's removal or the "
                          "intent itself). No layer may reformulate it away: relay it upward.")
    cur = fb.owned_formulation(x["id"])
    if cur is None:
        raise FabricError(f"L{k} owns no requirement on this escalation's path: it received an infeasible "
                          f"contract, and you cannot reformulate what you were given. Relay to L{k - 1}.")
    ok, why = next_action(fb, x["id"])
    if not ok and fb.reformulations_this_round(k) < MAX_REFORMULATE:
        raise FabricError(why)
    if any(d.get("previous") == cur for d in fb.nodes.values() if d["type"] == "req"):
        raise FabricError(f"{cur} has already been reformulated; this escalation is stale")
    if fb.reformulations_this_round(k) >= MAX_REFORMULATE:
        if k == 1:
            print(f"L1 has used its {MAX_REFORMULATE} reformulations this round. {x['id']} goes to the "
                  "operator now: run 'dossier' and stop.")
            return 3
        up = escalate_one(fb, x["id"], k - 1, "exhausted",
                          f"L{k} spent its {MAX_REFORMULATE} reformulations this round without convergence")
        print(f"{up['id']}  L{k - 1}  [exhausted]  reformulation budget spent at L{k}; passed up automatically")
        return 3
    tried = [q for q in fb.ancestry(cur) if fb.nodes[q]["layer"] == k]
    if norm_text(a.text) in {norm_text(fb.nodes[q]["text"]) for q in tried}:
        raise FabricError("this wording has already been tried at this layer; a reformulation must differ")
    if not a.change:
        raise FabricError("--change is required: say what is different and why it might succeed where "
                          "the last formulation failed")
    fields = {f: getattr(a, f) for f in CONTRACT_FIELDS}
    missing = [f for f, v in fields.items() if not v]
    if missing:
        raise FabricError(f"the new contract is incomplete, missing {missing}")
    check_contract_budget(fb, 1)
    check_episode_budget(fb, 1)
    n_here = fb.reformulations_this_round(k) + 1
    r = fb.add_node("req", k, a.text, gen=fb.nodes[cur].get("gen", 0) + 1, previous=cur,
                    reformulates=x["id"], change=a.change, round=fb.round_no(), reformulation_n=n_here)
    fb.add_edge(cur, "refines", r["id"])
    c = fb.add_node("ctr", k, fields["what"], target_layer=k + 1, fields=fields, rework_n=0)
    fb.add_edge(r["id"], "derives", c["id"])
    print(f"{r['id']}  reformulation {n_here}/{MAX_REFORMULATE} at L{k} (round {fb.round_no()})  ->  {c['id']}")


def cmd_authorise(a):
    via = require_human("an authority decision")
    fb = open_fabric(a.engagement)
    x = fb.nodes.get(a.escalation)
    if not x or x["type"] != "esc":
        raise FabricError("authorise resolves an escalation")
    if x["layer"] != 1:
        raise FabricError(f"{x['id']} is at L{x['layer']}; relay it up to L1 first. Authority sits "
                          "above the Intent layer and is adjacent only to it.")
    if not fb.esc_open(x["id"]):
        raise FabricError(f"{x['id']} has already been decided or answered")
    if a.adopt:
        p = fb.nodes.get(a.adopt)
        if not p or p.get("kind") != "reformulation":
            raise FabricError("--adopt names a reformulation proposal from the dossier")
        if a.decision != "revise":
            raise FabricError("adopting a proposal is a revise decision")
        a.revise_text = p["text"]
    if a.decision == "revise" and fb.round_no() >= MAX_ROUNDS and not a.beyond_round_limit:
        raise FabricError(
            f"this would start round {fb.round_no() + 1}; the limit is {MAX_ROUNDS}. Repeated revision "
            "that does not converge is itself information. If you still want another round, say so "
            "explicitly with --beyond-round-limit and give the reason in --rationale.")
    if a.decision == "exception" and not a.expires:
        raise FabricError("an exception must be time-bound: pass --expires DAYS")
    exp = time.time() + a.expires * 86400 if a.expires else None
    auth = fb.add_node("auth", 0, a.rationale or a.decision, decision=a.decision, signer=a.signer,
                       round=fb.round_no(), adopted=a.adopt, beyond_round_limit=a.beyond_round_limit or None,
                       approved_via=via,
                       expires_epoch=exp,
                       expires=time.strftime("%Y-%m-%d", time.localtime(exp)) if exp else None,
                       sign=True)
    fb.add_edge(x["id"], "resolved_by", auth["id"])
    print(f"{auth['id']}  {a.decision} by {a.signer}")
    if a.decision == "revise":
        if not a.revise_text:
            raise FabricError("--revise-text is required for a revise decision")
        top = max((n.get("gen", 0) for n in fb.nodes.values() if n["type"] == "req"), default=0)
        target = a.supersedes or next((n["id"] for n in fb.nodes.values()
                                       if n["type"] == "req" and n["layer"] == 1), None)
        r = fb.add_node("req", 1, a.revise_text, gen=top + 1, supersedes=target)
        fb.add_edge(auth["id"], "revises", r["id"])
        print(f"{r['id']}  revised requirement, generation {top + 1}; round {fb.round_no()} begins"
              + (f" (adopted {a.adopt})" if a.adopt else ""))


def cmd_keygen(a):
    """Not normally needed: the installer creates the signing key, and signing creates one if absent."""
    if os.path.isfile(KEY_PATH):
        print(f"signing key already present at {KEY_PATH}")
        return 0
    authority_key(create=True)
    print(f"signing key written to {KEY_PATH} (mode 600)")


def cmd_verify(a):
    fb = open_fabric(a.engagement)
    problems, warnings = fb.verify()
    print(f"engagement : {fb.eng}  ({len(fb.nodes)} nodes, {len(fb.edges)} edges, "
          f"{len(fb.entries)} log entries)")
    for w in warnings:
        print(f"  warning: {w}")
    if problems:
        print(f"FAILED ({len(problems)}):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("OK: chain intact, well-typed, adjacency respected, forward chain acyclic, "
          "authority acts signed, contracts complete.")
    return 0


def cmd_justify(a):
    fb = open_fabric(a.engagement)
    frags = [a.fragment] if a.fragment else sorted(n for n, d in fb.nodes.items() if d["type"] == "frag"
                                                   and d.get("kind") != "reformulation")
    out, bad = [], 0
    memo = {}
    for f in frags:
        ok, why = fb.justify(f, strict=a.strict, _memo=memo)
        bad += not ok
        out.append({"fragment": f, "layer": fb.nodes[f]["layer"], "justifiable": ok, "reasons": why})
    if a.json:
        print(json.dumps(out, indent=2))
    else:
        mode = "strict (Definition 2 + evidence path + authority content)" if a.strict else "Definition 2"
        print(f"mode: {mode}")
        for r in out:
            mark = "JUSTIFIABLE " if r["justifiable"] else "not justified"
            print(f"  {r['fragment']}  L{r['layer']}  {mark}" +
                  ("" if r["justifiable"] else "  - " + "; ".join(r["reasons"])))
        print(f"\n{len(out) - bad} of {len(out)} fragments justifiable")
    return 1 if bad else 0


def cmd_status(a):
    fb = open_fabric(a.engagement)
    by = defaultdict(lambda: defaultdict(int))
    for n in fb.nodes.values():
        if n["type"] == "frag" and n.get("kind") != "reformulation":
            v = fb.latest_review(n["id"])
            by[n["layer"]][fb.nodes[v]["state"] if v else "unreviewed"] += 1
    print(f"engagement {fb.eng}")
    for layer in sorted(by):
        print(f"  L{layer} {LAYERS[layer]:<30} " + ", ".join(f"{k}={v}" for k, v in sorted(by[layer].items())))
    reformulated = {d.get("reformulates") for d in fb.nodes.values() if d["type"] == "req"}

    def superseded(c):
        chain = [d for p, d in fb.out[c] if p == "escalates"]
        while chain:
            e = chain.pop()
            if e in reformulated:
                return True
            chain.extend(d for p, d in fb.out[e] if p == "escalates")
        return False

    confs = [c for c in fb.nodes if fb.nodes[c]["type"] == "conf" and fb.resolution(c) is None]
    sup = [c for c in confs if superseded(c)]
    open_conf = [c for c in confs if c not in sup]
    proposals = sum(1 for d in fb.nodes.values() if d.get("kind") == "reformulation")
    print(f"  round {fb.round_no()}/{MAX_ROUNDS} · shared steps {fb.steps_this_round()}/{MAX_STEPS} · contracts {fb.contracts_this_round()}/{MAX_CONTRACTS}"
          f" · proposals on record {proposals}")
    print(f"  unresolved conflicts : {len(open_conf)}  {' '.join(open_conf[:8])}")
    if sup:
        print(f"  superseded by a reformulation: {' '.join(sup[:8])}")
    open_esc = [x for x in fb.nodes if fb.nodes[x]["type"] == "esc" and fb.esc_open(x)]
    print(f"  open escalations     : {len(open_esc)}")
    for x in open_esc:
        ok, why = next_action(fb, x)
        if fb.nodes[x]["layer"] == 1 and not ok:
            why = "OPERATOR: run dossier, stop, wait for a decision"
        print(f"    {x}  L{fb.nodes[x]['layer']}  [{fb.nodes[x].get('effective', '?')}]  next: {why}")
    rw = [n for n in fb.nodes.values() if n["type"] == "ctr" and n.get("rework_n")]
    if rw:
        print(f"  rework contracts     : " + ", ".join(f"{n['id']}#{n['rework_n']}" for n in rw))
    fails = [n for n in fb.nodes.values() if n["type"] == "att" and n.get("state") != "success"]
    if fails:
        print("  failed attempts      : " + ", ".join(f"{n['id']}:{n['state']}" for n in fails[-8:]))


def cmd_report(a):
    fb = open_fabric(a.engagement)
    intent = next(n for n in fb.nodes.values() if n["type"] == "intent")
    print(f"# Traceability report: {fb.eng}\n\n**Intent.** {intent['text']}  \n"
          f"**Owner.** {intent.get('owner', '-')}\n")
    print("| Record | Parent requirement | Layer | Fragment | Evidence | Review state | Rationale | "
          "Escalation | Decision | Residual uncertainty |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for n in sorted(fb.nodes.values(), key=lambda x: (x["layer"], x["id"])):
        if n["type"] != "frag":
            continue
        f = n["id"]
        parents = [s for s, p in fb.inc[f] if p == "requests"]
        ev = [s for s, p in fb.inc[f] if p in ("supports", "contradicts")]
        v = fb.latest_review(f)
        confs = sorted(fb.conflicts_of(f))
        decs = [fb.resolution(c) for c in confs]
        cell = lambda t: str(t).replace("|", "\\|").replace("\n", " ")[:120]
        print(f"| {f} | {', '.join(parents) or '-'} | L{n['layer']} | {cell(n['text'])} | "
              f"{', '.join(ev) or '-'} | {fb.nodes[v]['state'] if v else 'unreviewed'} | "
              f"{cell(fb.nodes[v]['text']) if v else '-'} | {', '.join(confs) or '-'} | "
              f"{', '.join(d['id'] + ':' + d['decision'] for d in decs if d) or '-'} | "
              f"{cell(n.get('uncertainty') or '-')} |")


# ------------------------------------------------------------------------ selftest
def cmd_selftest(a):
    global FABRIC_DIR, KEY_PATH
    tmp = tempfile.mkdtemp(prefix="fabric-selftest-")
    FABRIC_DIR, KEY_PATH = os.path.join(tmp, "fab"), os.path.join(tmp, "authority.key")
    os.environ["FABRIC_TEST_AUTHORITY"] = "1"
    authority_key(create=True)
    checks = []

    def expect(name, cond):
        checks.append((name, bool(cond)))

    def raises(fn):
        try:
            fn()
            return False
        except FabricError:
            return True

    fb = Fabric("t", [])
    i = fb.add_node("intent", 1, "adapt the secure SDLC library to the client")
    r1 = fb.add_node("req", 1, "preserve the open-source dependency risk objective")
    fb.add_edge(i["id"], "derives", r1["id"])
    c12 = fb.add_node("ctr", 1, "interpret", target_layer=2,
                      fields={k: "x" for k in CONTRACT_FIELDS})
    fb.add_edge(r1["id"], "derives", c12["id"])
    r2 = fb.add_node("req", 2, "client term: SCA = dependency scanning in GitLab CI")
    fb.add_edge(c12["id"], "refines", r2["id"])
    c23 = fb.add_node("ctr", 2, "classify", target_layer=3, fields={k: "x" for k in CONTRACT_FIELDS})
    fb.add_edge(r2["id"], "derives", c23["id"])
    f3 = fb.add_node("frag", 3, "SCA is mandatory; client has no SCA tool")
    fb.add_edge(c23["id"], "requests", f3["id"])
    expect("unreviewed fragment is not justifiable", not fb.justify(f3["id"])[0])
    expect("adjacency: L6 evidence cannot support an L3 fragment directly",
           raises(lambda: fb.add_edge(fb.add_node("evd", 6, "scan", confidence="observation",
                                                  source="s")["id"], "supports", f3["id"])))
    expect("typing: supports cannot point at a requirement",
           raises(lambda: fb.add_edge(f3["id"], "supports", r2["id"])))
    e3 = fb.add_node("evd", 3, "tool inventory export", confidence="observation", source="cmdb")
    fb.add_edge(e3["id"], "supports", f3["id"])
    v2 = fb.add_node("rev", 2, "consistent with inventory", state="accepts", reviewer="l2", model="m",
                     target=f3["id"])
    fb.add_edge(f3["id"], "reviewed_by", v2["id"])
    expect("reviewed and evidenced fragment is justifiable (paper mode)", fb.justify(f3["id"])[0])
    expect("... and in strict mode", fb.justify(f3["id"], strict=True)[0])
    k = fb.add_node("conf", 3, "risk persists without SCA")
    fb.add_edge(e3["id"], "may_create", k["id"])
    expect("unresolved conflict blocks justifiability", not fb.justify(f3["id"])[0])
    x3 = fb.add_node("esc", 3, "removal of a control needs authority")
    fb.add_edge(k["id"], "escalates", x3["id"])
    expect("authority cannot resolve an escalation below L1",
           raises(lambda: fb.add_edge(x3["id"], "resolved_by",
                                      fb.add_node("auth", 0, "no", decision="accept", sign=True)["id"])))
    x2 = fb.add_node("esc", 2, "relay")
    fb.add_edge(x3["id"], "escalates", x2["id"])
    x1 = fb.add_node("esc", 1, "relay")
    fb.add_edge(x2["id"], "escalates", x1["id"])
    au = fb.add_node("auth", 0, "temporary exception", decision="exception",
                     expires_epoch=time.time() + 86400, expires="tomorrow", signer="risk owner", sign=True)
    fb.add_edge(x1["id"], "resolved_by", au["id"])
    expect("conflict resolved by a signed time-bound exception: justifiable", fb.justify(f3["id"], True)[0])
    w = fb.add_node("rev", 4, "lower layer tries to upgrade", state="conflicts", reviewer="l4", model="m",
                    target=f3["id"])
    expect("layer direction: a lower layer cannot review upward",
           raises(lambda: fb.add_edge(f3["id"], "reviewed_by", w["id"])))
    expect("rejected lower-layer review does not change status", fb.justify(f3["id"])[0])
    f_bare = fb.add_node("frag", 3, "fluent but unsupported claim")
    fb.add_edge(c23["id"], "requests", f_bare["id"])
    v_res = fb.add_node("rev", 2, "sounds right", state="resonates", reviewer="l2", model="m",
                        target=f_bare["id"])
    fb.add_edge(f_bare["id"], "reviewed_by", v_res["id"])
    expect("'resonates' passes Definition 2 (i) as written", fb.justify(f_bare["id"])[0])
    expect("... but strict mode rejects it: no evidence, and resonates is not evidence",
           not fb.justify(f_bare["id"], strict=True)[0])
    expect("cycle in the forward chain is rejected",
           raises(lambda: fb.add_edge(r2["id"], "refines", r1["id"]) or
                  fb.add_edge(r1["id"], "refines", r2["id"])))
    p, _ = Fabric("t", load("t")).verify()
    expect("verify passes on the untampered log", not p)
    lines = open(log_path("t"), encoding="utf-8").read().splitlines()
    d = json.loads(lines[3]); d["data"]["text"] = "edited after the fact"; lines[3] = canonical(d)
    open(log_path("t"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    p, _ = Fabric("t", load("t")).verify()
    expect("verify detects an edited entry", any("hash mismatch" in x for x in p))

    # ---- regression and ported cases ---------------------------------------------
    NS = argparse.Namespace
    full = {f: "x" for f in CONTRACT_FIELDS}
    cmd_init(NS(engagement="r", intent="regression", owner="t", success=None, boundary=None))
    cmd_req(NS(engagement="r", layer=1, text="top", label="derives", **{"from": "intent-0001"}))
    cmd_contract(NS(engagement="r", rework_of=None, **full, **{"from": "req-0001"}))
    msg = os.path.join(tmp, "m.json")

    def ingest(doc, ctr="ctr-0001"):
        fbx = open_fabric("r")
        doc = dict(doc)
        doc["context_digest"] = contract_context_packet(fbx, fbx.nodes[ctr])[1]
        open(msg, "w", encoding="utf-8").write(json.dumps(doc))
        cmd_ingest(NS(engagement="r", contract=ctr, result=msg))

    before = len(load("r"))
    expect("atomic ingest: a rejected message appends nothing (regression)",
           raises(lambda: ingest({"fragments": [{"key": "a", "text": "t", "supported_by": ["frag-9999"]}]}))
           and len(load("r")) == before)
    ingest({"fragments": [{"key": "a", "text": "AI says the control exists"}],
            "evidence": [{"supports": ["a"], "source": "another model", "confidence": "ai_derived"}]})
    fr = Fabric("r", load("r"))
    expect("no implements back-edge from ingest, so no requests/implements 2-cycle (regression)",
           not any(p == "implements" for _, p, _ in fr.edges))
    cmd_review(NS(engagement="r", fragment="frag-0001", layer=1, state="accepts", rationale="ok",
                  reviewer="t", model="m", constraints=None))
    fr = Fabric("r", load("r"))
    expect("section 10: AI-derived evidence alone passes Definition 2 ...", fr.justify("frag-0001")[0])
    expect("... but not strict mode", not fr.justify("frag-0001", strict=True)[0])

    for i in range(MAX_REWORK):
        cmd_contract(NS(engagement="r", rework_of=f"ctr-{i + 1:04d}", change=f"repair {i+1}", **full, **{"from": "req-0001"}))
    rc = cmd_contract(NS(engagement="r", rework_of=f"ctr-{MAX_REWORK + 1:04d}", change="repair exhausted", **full,
                         **{"from": "req-0001"}))
    fr = Fabric("r", load("r"))
    expect("Prop. 4 extended: exhausted rework becomes a conflict and an escalation, not a loop",
           rc == 3 and any(n["type"] == "esc" for n in fr.nodes.values()))

    probe = os.path.join(tmp, "probe.txt")
    open(probe, "w", encoding="utf-8").write("p95=241ms")
    cmd_contract(NS(engagement="r", rework_of=None, **full, **{"from": "req-0001"}))
    ctr_last = sorted(i for i in Fabric("r", load("r")).nodes if i.startswith("ctr-"))[-1]
    ingest({"fragments": [{"key": "m", "text": "measured p95 241ms"}],
            "evidence": [{"supports": ["m"], "source": "load test", "confidence": "deterministic",
                          "file": probe}]}, ctr=ctr_last)
    fr = Fabric("r", load("r"))
    mf = sorted(i for i in fr.nodes if i.startswith("frag-"))[-1]
    cmd_review(NS(engagement="r", fragment=mf, layer=1, state="accepts", rationale="measured",
                  reviewer="t", model="m", constraints=None))
    cmd_answer(NS(engagement="r", requirement="req-0001", text="ready", supported_by=[mf]))
    prod = sorted(i for i in Fabric("r", load("r")).nodes if i.startswith("frag-"))[-1]
    cmd_review(NS(engagement="r", fragment=prod, layer=0, state="accepts", rationale="approved",
                  reviewer="owner", model="human", constraints=None))
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        ok_release = cmd_release(NS(engagement="r", fragment=prod)) == 0
    open(probe, "w", encoding="utf-8").write("p95=480ms")
    with contextlib.redirect_stdout(io.StringIO()):
        drift_blocks = cmd_release(NS(engagement="r", fragment=prod)) == 1
    expect("release gate passes a strict-justified, authority-accepted product", ok_release)
    expect("evidence drift after recording blocks release", drift_blocks)

    # Proposition 1: linear-time decision, measured on a large fabric
    big = Fabric("big", [])
    big.entries = []
    t0 = time.time()
    root = {"id": "req-0", "type": "req", "layer": 2, "text": "", "gen": 0}
    big.nodes[root["id"]] = root; big.seq_of[root["id"]] = 0
    for i in range(1700):
        f, e, v = f"frag-{i}", f"evd-{i}", f"rev-{i}"
        big.nodes[f] = {"id": f, "type": "frag", "layer": 3, "text": ""}
        big.nodes[e] = {"id": e, "type": "evd", "layer": 3, "text": "", "confidence": "observation"}
        big.nodes[v] = {"id": v, "type": "rev", "layer": 2, "text": "", "state": "accepts"}
        for n in (f, e, v):
            big.seq_of[n] = i
        big._index(root["id"], "requests", f); big._index(e, "supports", f); big._index(f, "reviewed_by", v)
    memo = {}
    n_ok = sum(big.justify(f"frag-{i}", strict=True, _memo=memo)[0] for i in range(1700))
    elapsed = time.time() - t0
    expect(f"Prop. 1: {len(big.nodes)} nodes, 1700 fragments decided in {elapsed:.2f}s (< 2s)",
           n_ok == 1700 and elapsed < 2.0)

    # ---- the escalation ladder ------------------------------------------------------
    import io, contextlib
    quiet = lambda: contextlib.redirect_stdout(io.StringIO())

    def ladder_setup(eng):
        with quiet():
            cmd_init(NS(engagement=eng, intent="ladder test", owner="t", success=None, boundary=None))
            cmd_req(NS(engagement=eng, layer=1, text="top", label="derives", **{"from": "intent-0001"}))
            cmd_contract(NS(engagement=eng, rework_of=None, **full, **{"from": "req-0001"}))
            ingest_to(eng, "ctr-0001", {"derived_requirements": [{"key": "r", "text": "L2 req", "contract": full}]})
            ingest_to(eng, "ctr-0002", {"fragments": [{"key": "f", "text": "attempt fails"}],
                                        "proposals": [{"text": "a different L2 requirement", "tradeoff": "costs X"}]})
            cmd_review(NS(engagement=eng, fragment="frag-0001", layer=2, state="conflicts",
                          rationale="cannot meet the L2 requirement", reviewer="t", model="m", constraints=None))

    def ingest_to(eng, ctr, doc):
        fbx = open_fabric(eng)
        doc = dict(doc)
        doc["context_digest"] = contract_context_packet(fbx, fbx.nodes[ctr])[1]
        open(msg, "w", encoding="utf-8").write(json.dumps(doc))
        cmd_ingest(NS(engagement=eng, contract=ctr, result=msg))

    def esc(eng, src, layer, code):
        with quiet():
            return cmd_escalate(NS(engagement=eng, layer=layer, code=code, reason="r", to_top=False,
                                   **{"from": src}))

    def last(eng, typ):
        return sorted((i for i, d in Fabric(eng, load(eng)).nodes.items() if d["type"] == typ),
                      key=lambda i: int(i.split("-")[1]))[-1]

    def reform(eng, x, text):
        with quiet():
            return cmd_reformulate(NS(engagement=eng, escalation=x, text=text, change="different", **full))

    ladder_setup("l")                                   # conf-0001 at L2, raised by an L2 review
    esc("l", "conf-0001", 2, "exhausted")               # esc-0001 at L2
    expect("ladder: an escalation may not move sideways", raises(lambda: esc("l", "esc-0001", 2, "relay")))
    expect("ladder: an escalation may not move downward", raises(lambda: esc("l", "esc-0001", 3, "relay")))
    expect("ladder: a conflict escalates first at its own layer", raises(lambda: esc("l", "conf-0001", 1, "exhausted")))
    expect("ladder: a reformulation must differ from every earlier wording",
           raises(lambda: reform("l", "esc-0001", "L2 req")))
    reform("l", "esc-0001", "L2 req, second wording")
    expect("ladder: the owning layer may reformulate within budget",
           any(d.get("reformulates") == "esc-0001" for d in Fabric("l", load("l")).nodes.values()))

    ladder_setup("oa")
    esc("oa", "conf-0001", 2, "outside_authority")
    expect("authority matter: no layer may reformulate it", raises(lambda: reform("oa", "esc-0001", "x")))
    expect("authority matter: no relay may downgrade it", raises(lambda: esc("oa", "esc-0001", 1, "exhausted")))
    esc("oa", "esc-0001", 1, "relay")
    expect("authority matter: the status survives the relay",
           Fabric("oa", load("oa")).nodes["esc-0002"]["effective"] == "outside_authority")

    ladder_setup("nv")
    esc("nv", "conf-0001", 2, "no_viable_reformulation")
    expect("a layer that declared it cannot reformulate is not offered a reformulation",
           raises(lambda: reform("nv", "esc-0001", "x")))
    esc("nv", "esc-0001", 1, "relay")
    expect("... but the layer it passes to may reformulate its own requirement",
           next_action(Fabric("nv", load("nv")), "esc-0002")[0])

    ladder_setup("bud")
    esc("bud", "conf-0001", 2, "exhausted")
    for i in range(MAX_REFORMULATE):
        reform("bud", last("bud", "esc"), f"wording {i}")
        with quiet():
            ingest_to("bud", last("bud", "ctr"), {"fragments": [{"key": "f", "text": "fails again"}]})
            cmd_review(NS(engagement="bud", fragment=last("bud", "frag"), layer=2, state="conflicts",
                          rationale="still fails", reviewer="t", model="m", constraints=None))
        esc("bud", last("bud", "conf"), 2, "exhausted")
    rc = reform("bud", last("bud", "esc"), "one more wording")
    fb_b = Fabric("bud", load("bud"))
    up = fb_b.nodes[last("bud", "esc")]
    expect(f"reformulation budget ({MAX_REFORMULATE}/layer/round) spent: the runtime passes it up itself",
           rc == 3 and up["layer"] == 1 and up["code"] == "exhausted")

    ladder_setup("dos")
    esc("dos", "conf-0001", 2, "no_viable_reformulation")
    esc("dos", "esc-0001", 1, "relay")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        cmd_dossier(NS(engagement="dos", escalation="esc-0002", examples=6))
    d = buf.getvalue()
    expect("dossier carries the verbatim intent, a real failed attempt and its review rationale",
           "ladder test" in d and "attempt fails" in d and "cannot meet the L2 requirement" in d)
    expect("dossier lists each proposal with its trade-off and an --adopt command",
           "a different L2 requirement" in d and "costs X" in d and "--adopt frag-0002" in d)
    with quiet():
        cmd_authorise(NS(engagement="dos", escalation="esc-0002", decision="revise", signer="op",
                         rationale="adopt", expires=None, revise_text=None, supersedes=None,
                         adopt="frag-0002", beyond_round_limit=False))
    fb_d = Fabric("dos", load("dos"))
    newreq = fb_d.nodes[last("dos", "req")]
    expect("operator adopts a proposal: it re-enters at L1 as the next generation, round 2 begins",
           newreq["layer"] == 1 and newreq["text"] == "a different L2 requirement" and fb_d.round_no() == 2)
    expect("a decided escalation cannot be decided again",
           raises(lambda: cmd_authorise(NS(engagement="dos", escalation="esc-0002", decision="reject",
                                           signer="op", rationale="x", expires=None, revise_text=None,
                                           supersedes=None, adopt=None, beyond_round_limit=False))))

    # ---- termination under an adversarial orchestrator ------------------------------
    # Every attempt fails. At every step the orchestrator takes whichever legal action creates
    # the most further work: rework before reformulation, reformulation before relaying.
    def adversary(eng):
        with quiet():
            cmd_init(NS(engagement=eng, intent="always fails", owner="t", success=None, boundary=None))
            cmd_req(NS(engagement=eng, layer=1, text="top", label="derives", **{"from": "intent-0001"}))
            cmd_contract(NS(engagement=eng, rework_of=None, **full, **{"from": "req-0001"}))
        steps, uniq = 0, [0]

        def descend(ctr):                               # contracts flow to L6, which fails; L5 rejects it
            nonlocal steps
            fb = Fabric(eng, load(eng))
            while fb.nodes[ctr]["target_layer"] < 6:
                uniq[0] += 1
                with quiet():
                    ingest_to(eng, ctr, {"derived_requirements": [{"key": "r", "text": f"req {uniq[0]}",
                                                                   "contract": full}]})
                steps += 1
                ctr = last(eng, "ctr")
                fb = Fabric(eng, load(eng))
            with quiet():
                ingest_to(eng, ctr, {"fragments": [{"key": "f", "text": "fails"}]})
                cmd_review(NS(engagement=eng, fragment=last(eng, "frag"), layer=5, state="insufficient",
                              rationale="fails", reviewer="t", model="m", constraints=None))
            steps += 2
            return ctr

        def to_top(src):
            nonlocal steps
            with quiet():
                cmd_escalate(NS(engagement=eng, layer=None, code="budget", reason="budget", to_top=True,
                                **{"from": src}))
            steps += 1

        try:
            cur = descend("ctr-0001")
            while steps < 5000:
                fb = Fabric(eng, load(eng))
                opens = [x for x, d in fb.nodes.items() if d["type"] == "esc" and fb.esc_open(x)]
                if opens:
                    x = max(opens, key=lambda i: fb.seq_of[i])
                    ok, _ = next_action(fb, x)
                    if fb.nodes[x]["layer"] == 1 and not ok:
                        break                                   # only the operator can act now
                    if ok:
                        uniq[0] += 1
                        rc = reform(eng, x, f"wording {uniq[0]}")
                        steps += 1
                        if rc != 3:
                            cur = descend(last(eng, "ctr"))
                    else:
                        esc(eng, x, fb.nodes[x]["layer"] - 1, "relay")
                        steps += 1
                    continue
                owner = next(s2 for s2, p in fb.inc[cur] if p == "derives")
                with quiet():
                    rc = cmd_contract(NS(engagement=eng, rework_of=cur, change="repair same requirement", **full, **{"from": owner}))
                steps += 1
                if rc != 3:
                    cur = descend(last(eng, "ctr"))
        except FabricError as exc:
            if "budget" not in str(exc):
                raise
            fb = Fabric(eng, load(eng))
            opens = [x for x, d in fb.nodes.items() if d["type"] == "esc" and fb.esc_open(x)]
            if opens:
                x = max(opens, key=lambda i: fb.seq_of[i])
                if fb.nodes[x]["layer"] > 1:
                    to_top(x)
            else:
                with quiet():
                    cmd_conflict(NS(engagement=eng, layer=5, text="budget spent", **{"from": last(eng, "rev")}))
                to_top(last(eng, "conf"))
        fb = Fabric(eng, load(eng))
        opens = [x for x, d in fb.nodes.items() if d["type"] == "esc" and fb.esc_open(x)]
        autonomous_left = [x for x in opens if next_action(fb, x)[0] or fb.nodes[x]["layer"] > 1]
        return steps, fb.contracts_this_round(), opens, autonomous_left

    steps, ctrs, opens, left = adversary("adv")
    expect(f"termination: a worst-case orchestrator reaches the operator in {steps} autonomous steps "
           f"({ctrs} contracts, budget {MAX_CONTRACTS}) with no autonomous action left",
           steps < 5000 and ctrs <= MAX_CONTRACTS and opens and not left)
    saved = (MAX_CONTRACTS, MAX_REFORMULATE)
    globals()["MAX_CONTRACTS"], globals()["MAX_REFORMULATE"] = 1000, 2
    steps2, ctrs2, opens2, left2 = adversary("adv2")
    globals()["MAX_CONTRACTS"], globals()["MAX_REFORMULATE"] = saved
    expect(f"termination without the contract cap: reformulation budgets alone stop it in {steps2} steps "
           f"({ctrs2} contracts)", steps2 < 5000 and opens2 and not left2)

    # ---- 3.3 supervision hardening -------------------------------------------------
    expect("policy kernel classifies timeout as retryable and contradiction as non-retryable",
           failure_class("timeout") == "retryable" and failure_class("contradicted") == "contradictory")

    with quiet():
        cmd_init(NS(engagement="f33", intent="failure test", owner="t", success=None, boundary=None))
        cmd_req(NS(engagement="f33", layer=1, text="top", label="derives", **{"from": "intent-0001"}))
        cmd_contract(NS(engagement="f33", rework_of=None, change=None, **full, **{"from": "req-0001"}))
        rc33 = cmd_failure(NS(engagement="f33", contract="ctr-0001", state="timeout",
                              reason="provider timeout", actor="l2", model="m"))
    ff = Fabric("f33", load("f33"))
    expect("first-class failure stays local while repair budget remains",
           rc33 == 0 and any(d["type"] == "att" and d.get("state") == "timeout" for d in ff.nodes.values())
           and not any(d["type"] == "esc" for d in ff.nodes.values()))
    bad = dict(full); bad["what"] = "different meaning"
    expect("rework cannot silently reformulate semantic fields",
           raises(lambda: cmd_contract(NS(engagement="f33", rework_of="ctr-0001", change="retry",
                                         **bad, **{"from": "req-0001"}))))

    dg = contract_context_packet(ff, ff.nodes["ctr-0001"])[1]
    open(msg, "w", encoding="utf-8").write(json.dumps({"context_digest": "wrong",
                                                          "fragments": [{"key": "x", "text": "x"}]}))
    expect("context digest mismatch is rejected before append",
           raises(lambda: cmd_ingest(NS(engagement="f33", contract="ctr-0001", result=msg))))
    open(msg, "w", encoding="utf-8").write(json.dumps({"context_digest": dg,
                                                          "fragments": [{"key": "x", "text": "x"}],
                                                          "evidence": [{"supports": ["x"], "source": "obs",
                                                                        "confidence": "observation"}]}))
    with quiet():
        cmd_ingest(NS(engagement="f33", contract="ctr-0001", result=msg))
        cmd_review(NS(engagement="f33", fragment="frag-0001", layer=1, state="accepts",
                      rationale="ok", reviewer="l1", model="m", constraints=None))
        cmd_invalidate(NS(engagement="f33", changed="evd-0001", reason="superseded"))
    ff = Fabric("f33", load("f33"))
    expect("dependency invalidation creates a blocking conflict on affected output",
           not ff.justify("frag-0001", strict=True)[0] and bool(ff.conflicts_of("frag-0001")))

    width = max(len(n) for n, _ in checks)
    for name, ok in checks:
        print(f"  {'pass' if ok else 'FAIL'}  {name}")
    failed = sum(1 for _, ok in checks if not ok)
    print(f"\n{len(checks) - failed} of {len(checks)} checks passed")
    return 1 if failed else 0


# --------------------------------------------------------------------------- main
def main():
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)   # quiet when piped into head
    ap = argparse.ArgumentParser(description="Traceability fabric for layered justifiable engagements.")
    ap.add_argument("--version", action="version", version=VERSION)
    sp = ap.add_subparsers(dest="cmd", required=True)

    p = sp.add_parser("init"); p.add_argument("engagement"); p.add_argument("--intent", required=True)
    p.add_argument("--owner", required=True); p.add_argument("--success"); p.add_argument("--boundary")
    p.set_defaults(fn=cmd_init)

    p = sp.add_parser("req"); p.add_argument("engagement"); p.add_argument("--layer", type=int, required=True)
    p.add_argument("--from", required=True); p.add_argument("--label", choices=("derives", "refines"),
                                                            required=True)
    p.add_argument("--text", required=True); p.set_defaults(fn=cmd_req)

    p = sp.add_parser("contract"); p.add_argument("engagement"); p.add_argument("--from", required=True)
    for f in CONTRACT_FIELDS:
        p.add_argument(f"--{f.replace('_', '-')}", dest=f)
    p.add_argument("--rework-of"); p.add_argument("--change"); p.set_defaults(fn=cmd_contract)

    p = sp.add_parser("render-contract"); p.add_argument("engagement"); p.add_argument("contract")
    p.set_defaults(fn=cmd_render)

    p = sp.add_parser("context-packet"); p.add_argument("engagement"); p.add_argument("contract")
    p.set_defaults(fn=cmd_packet)

    p = sp.add_parser("ingest"); p.add_argument("engagement"); p.add_argument("--contract", required=True)
    p.add_argument("result", help="JSON file returned by the layer agent, or - for stdin")
    p.set_defaults(fn=cmd_ingest)

    p = sp.add_parser("failure"); p.add_argument("engagement"); p.add_argument("--contract", required=True)
    p.add_argument("--state", choices=FAILURE_STATES, required=True); p.add_argument("--reason", required=True)
    p.add_argument("--actor"); p.add_argument("--model"); p.set_defaults(fn=cmd_failure)

    p = sp.add_parser("invalidate"); p.add_argument("engagement"); p.add_argument("--changed", required=True)
    p.add_argument("--reason", required=True); p.set_defaults(fn=cmd_invalidate)

    sp.add_parser("policy").set_defaults(fn=cmd_policy)

    p = sp.add_parser("answer"); p.add_argument("engagement"); p.add_argument("--requirement", required=True)
    p.add_argument("--text", required=True); p.add_argument("--supported-by", nargs="+", default=[])
    p.set_defaults(fn=cmd_answer)

    p = sp.add_parser("release"); p.add_argument("engagement"); p.add_argument("fragment")
    p.set_defaults(fn=cmd_release)

    p = sp.add_parser("render-review"); p.add_argument("engagement"); p.add_argument("contract")
    p.set_defaults(fn=cmd_render_review)

    p = sp.add_parser("ingest-reviews"); p.add_argument("engagement")
    p.add_argument("--layer", type=int, required=True); p.add_argument("--reviewer", required=True)
    p.add_argument("--model", required=True); p.add_argument("result")
    p.set_defaults(fn=cmd_ingest_reviews)

    p = sp.add_parser("evidence"); p.add_argument("engagement"); p.add_argument("--layer", type=int, required=True)
    p.add_argument("--supports", nargs="*"); p.add_argument("--contradicts", nargs="*")
    p.add_argument("--source", required=True); p.add_argument("--confidence", choices=CONFIDENCE, required=True)
    p.add_argument("--file"); p.set_defaults(fn=cmd_evidence)

    p = sp.add_parser("review"); p.add_argument("engagement"); p.add_argument("fragment")
    p.add_argument("--layer", type=int, required=True); p.add_argument("--state", choices=STATES, required=True)
    p.add_argument("--rationale", required=True); p.add_argument("--reviewer", required=True)
    p.add_argument("--model", required=True); p.add_argument("--constraints")
    p.set_defaults(fn=cmd_review)

    p = sp.add_parser("consolidate"); p.add_argument("engagement"); p.add_argument("fragment")
    p.add_argument("--layer", type=int, required=True); p.set_defaults(fn=cmd_consolidate)

    p = sp.add_parser("conflict"); p.add_argument("engagement"); p.add_argument("--from", required=True)
    p.add_argument("--layer", type=int, required=True); p.add_argument("--text", required=True)
    p.set_defaults(fn=cmd_conflict)

    p = sp.add_parser("escalate"); p.add_argument("engagement"); p.add_argument("from")
    p.add_argument("--layer", type=int); p.add_argument("--reason", required=True)
    p.add_argument("--code", choices=ESC_CODES, required=True)
    p.add_argument("--to-top", action="store_true", help="relay all the way to L1 (budget exhaustion)")
    p.set_defaults(fn=cmd_escalate)

    p = sp.add_parser("reformulate"); p.add_argument("engagement"); p.add_argument("escalation")
    p.add_argument("--text", required=True); p.add_argument("--change", required=True)
    for f in CONTRACT_FIELDS:
        p.add_argument(f"--{f.replace('_', '-')}", dest=f)
    p.set_defaults(fn=cmd_reformulate)

    p = sp.add_parser("propose"); p.add_argument("engagement"); p.add_argument("--requirement", required=True)
    p.add_argument("--text", required=True); p.add_argument("--tradeoff", required=True)
    p.set_defaults(fn=cmd_propose)

    p = sp.add_parser("dossier"); p.add_argument("engagement"); p.add_argument("escalation")
    p.add_argument("--examples", type=int, default=6); p.set_defaults(fn=cmd_dossier)

    p = sp.add_parser("authorise"); p.add_argument("engagement"); p.add_argument("escalation")
    p.add_argument("--decision", choices=DECISIONS, required=True); p.add_argument("--signer", required=True)
    p.add_argument("--rationale"); p.add_argument("--expires", type=float)
    p.add_argument("--revise-text"); p.add_argument("--supersedes"); p.add_argument("--adopt")
    p.add_argument("--beyond-round-limit", action="store_true"); p.set_defaults(fn=cmd_authorise)

    sp.add_parser("keygen").set_defaults(fn=cmd_keygen)
    for name, fn in (("verify", cmd_verify), ("status", cmd_status), ("report", cmd_report)):
        p = sp.add_parser(name); p.add_argument("engagement"); p.set_defaults(fn=fn)
    p = sp.add_parser("justify"); p.add_argument("engagement"); p.add_argument("fragment", nargs="?")
    p.add_argument("--strict", action="store_true"); p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_justify)
    sp.add_parser("selftest").set_defaults(fn=cmd_selftest)

    a = ap.parse_args()
    try:
        return a.fn(a) or 0
    except FabricError as exc:
        print(f"fabric: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
