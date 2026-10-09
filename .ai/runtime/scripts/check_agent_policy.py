#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Validate that no skill and no agent in this bundle can exceed its declared tool ceiling.

Three things go wrong with a permission model of this size, and all three are silent:
a skill that declares nothing and therefore inherits everything; an agent whose tool list
has quietly drifted wider than the tier it claims to serve; and an advise-tier skill that
can be picked up by an agent holding Write or Bash, which defeats the separation the skill
was written to enforce. This script fails the build on any of them.

Usage
-----
    python3 agents/scripts/check_agent_policy.py [--fast] <bundle-root>

Exit status 0 only when every check passes.
"""
import json
import os
import re
import sys

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
# Task and Agent are the subagent tool under its two names across Claude Code versions.
GLOBAL_ALLOWLIST = {"Read", "Grep", "Glob", "WebSearch", "WebFetch", "Write", "Edit", "Bash", "Task", "Agent"}
MUTATING = {"Write", "Edit", "Bash"}
STD_SKILL_KEYS = {"name", "description", "allowed-tools", "model"}
STD_AGENT_KEYS = {"name", "description", "tools", "model_class"}


# Frontmatter is YAML. A plain (unquoted) value must avoid YAML's indicators: ': ' inside it, ' #', or a
# leading [ { & * ! | > ' " % @ ` - ? : , #. Claude Code parses frontmatter as YAML, so an agent whose
# description breaks these rules may not load at all. These helpers read and write values safely.
_YAML_WORDS = {"true", "false", "yes", "no", "on", "off", "null", "~"}


def yaml_needs_quotes(v):
    return (v == "" or v != v.strip() or v[0] in "-?:,[]{}#&*!|>'\"%@`" or ": " in v or " #" in v
            or v.endswith(":") or v.lower() in _YAML_WORDS
            or re.fullmatch(r"[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?", v) is not None)


def yaml_value(raw):
    """-> (value, problem or None) for one frontmatter value as written."""
    raw = raw.strip()
    if raw.startswith('"'):
        try:
            return json.loads(raw), None
        except ValueError:
            return raw, "a double-quoted value that is not closed or escaped correctly"
    if raw.startswith("'"):
        if len(raw) < 2 or not raw.endswith("'"):
            return raw, "a single-quoted value that is not closed"
        return raw[1:-1].replace("''", "'"), None
    if raw and yaml_needs_quotes(raw):
        return raw, "an unquoted value YAML cannot read as text (it contains ': ' or ' #', or starts with an indicator)"
    return raw, None


FRONTMATTER_PROBLEMS = []


def frontmatter(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        return None, text
    _, raw, body = text.split("---", 2)
    data = {}
    for line in raw.strip().splitlines():
        key, sep, value = line.partition(":")
        if not sep:
            continue
        value, problem = yaml_value(value)
        if problem:
            FRONTMATTER_PROBLEMS.append(f"{os.path.relpath(path)}: {key.strip()}: {problem}")
        data[key.strip()] = value
    return data, body


import re as _re
for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
# Under a non-UTF-8 locale, arguments arrive surrogate-escaped; recover the real characters (a no-op otherwise).
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]

def toolset(value):
    return {t.strip() for t in value.split(",") if t.strip()} if value else set()


def main():
    args = list(sys.argv[1:])
    fast = "--fast" in args
    args = [a for a in args if a != "--fast"]
    root = args[0] if args else "."
    candidates = [os.path.join(root, "it-role-library", "policy.json"),
                  os.path.join(root, "it-role-house", "policy.json"),
                  os.path.join(root, ".ai", "it-role-house", "policy.json"),
                  os.path.join(root, ".ai", "runtime", "policy.json"),
                  os.path.join(root, "runtime", "policy.json"),
                  os.path.join(root, "agents", "policy.json"),
                  os.path.join(root, "policy.json")]
    policy_path = next((c for c in candidates if os.path.isfile(c)), None)
    if policy_path is None:
        sys.exit("error: no AI IT House policy.json found below the supplied root")
    package_root = os.path.dirname(policy_path)
    surface_candidates = [package_root, root, os.path.dirname(package_root)]
    surface_root = next((c for c in surface_candidates
                         if all(os.path.isdir(os.path.join(c, d)) for d in ("agents", "skills", "commands"))), root)
    policy = json.load(open(policy_path, encoding="utf-8"))
    tiers_raw = policy["tiers"]
    tiers = {k: toolset(v) for k, v in tiers_raw.items()}
    agent_tier = policy["agent_tier"]
    operator_for = policy["operator_for_tier"]
    guarded = set(policy["guarded_categories"])

    problems = []
    agents = {}

    # ---------------------------------------------------------------- agents
    # In a real ~/.claude the user's own skills and agents sit beside ours and are not ours to judge.
    # When install.sh has written a manifest, only the files it lists are checked.
    man = os.path.join(package_root, "MANIFEST")
    owned = None
    if os.path.isfile(man):
        owned = {l.strip() for l in open(man, encoding="utf-8") if l.strip() and not l.startswith("#")}

    def ours(rel):
        return owned is None or rel.replace(os.sep, "/") in owned

    agent_dir = os.path.join(surface_root, "agents")
    for fn in sorted(os.listdir(agent_dir)):
        if not ours(f"agents/{fn}"):
            continue
        if not fn.endswith(".md") or fn == "README.md":
            continue
        path = os.path.join(agent_dir, fn)
        data, _ = frontmatter(path)
        if data is None:
            problems.append(f"{fn}: no frontmatter")
            continue
        name = data.get("name", "")
        agents[name] = data
        if not NAME_RE.match(name):
            problems.append(f"{fn}: invalid agent name '{name}'")
        if name != fn[:-3]:
            problems.append(f"{fn}: name '{name}' does not match filename")
        if not data.get("description"):
            problems.append(f"{fn}: missing description")
        elif len(data["description"]) > 1024:
            problems.append(f"{fn}: description {len(data['description'])} chars, limit 1024")
        unknown = set(data) - STD_AGENT_KEYS
        if unknown:
            problems.append(f"{fn}: non-standard frontmatter keys {sorted(unknown)}")
        tools = toolset(data.get("tools", ""))
        if not tools:
            problems.append(f"{fn}: no tools declared, so it inherits everything")
        outside = tools - GLOBAL_ALLOWLIST
        if outside:
            problems.append(f"{fn}: tools outside the allowlist {sorted(outside)}")
        tier = agent_tier.get(name)
        if tier is None:
            problems.append(f"{fn}: not bound to a tier in policy.json")
        elif not tools <= tiers[tier]:
            problems.append(f"{fn}: tools {sorted(tools - tiers[tier])} exceed its '{tier}' tier")

    # ------------------------------------------------- separation of duties
    scopes = policy.get("write_scope", {})
    for name, data in agents.items():
        if name not in scopes:
            problems.append(f"{name}: no write_scope declared in policy.json")
    drafters = [n for n, sc in scopes.items()
                if any("staging" in a for a in sc.get("allow", []))]
    approvers = [n for n, t in agent_tier.items() if n.endswith("-approver")]
    for a in approvers:
        if a in drafters:
            problems.append(f"{a}: approves and also drafts; that is one actor, not a control")
        if toolset(agents.get(a, {}).get("tools", "")) & {"Write", "Edit"}:
            problems.append(f"{a}: an approver must hold no Write or Edit")
    if not approvers:
        problems.append("policy: no approver agent exists, so library changes are self-approved")
    releasers = [n for n, sc in scopes.items() if "~/.claude/**" in sc.get("allow", [])]
    if len(releasers) != 1:
        problems.append(f"policy: expected exactly one agent with write access to the live library, "
                        f"found {releasers}")
    for n in drafters:
        if any(p2.startswith("~/.claude/skills") or p2.startswith("~/.claude/agents")
               for p2 in scopes[n].get("allow", [])):
            problems.append(f"{n}: drafts into staging but also claims the live tree")
    docs = scopes.get("docs-author", {})
    if docs and not any(d.endswith(".java") for d in docs.get("deny", [])):
        problems.append("docs-author: must deny source files; in-source documentation is a code change")

    for name, data in agents.items():
        tier = agent_tier.get(name)
        if tier in ("route", "advise", "inspect", "orchestrate", "research") and toolset(data.get("tools", "")) & {"Write", "Edit"}:
            problems.append(f"{name}: '{tier}' agent must not hold Write or Edit")

    for tier, agent in operator_for.items():
        if agent not in agents:
            problems.append(f"policy: operator '{agent}' for tier '{tier}' does not exist")
        elif toolset(agents[agent].get("tools", "")) != tiers[tier]:
            problems.append(f"policy: operator '{agent}' does not match tier '{tier}' exactly")

    # ---------------------------------------------------------------- skills
    counts = {}
    skills = 0
    for dirpath, _dirs, files in os.walk(surface_root):
        _dirs[:] = [d for d in _dirs if not d.startswith(".")]          # backups, VCS, caches
        if "SKILL.md" not in files or os.sep + "agents" in dirpath:
            continue
        if not ours(os.path.relpath(os.path.join(dirpath, "SKILL.md"), surface_root)):
            continue
        skills += 1
        rel = os.path.relpath(os.path.join(dirpath, "SKILL.md"), surface_root)
        data, body = frontmatter(os.path.join(dirpath, "SKILL.md"))
        if data is None:
            problems.append(f"{rel}: no frontmatter")
            continue
        name = data.get("name", "")
        if not NAME_RE.match(name):
            problems.append(f"{rel}: invalid skill name '{name}'")
        if name != os.path.basename(dirpath):
            problems.append(f"{rel}: name '{name}' does not match its directory")
        desc = data.get("description", "")
        if not desc:
            problems.append(f"{rel}: missing description")
        elif len(desc) > 1024:
            problems.append(f"{rel}: description {len(desc)} chars, limit 1024")
        unknown = set(data) - STD_SKILL_KEYS
        if unknown:
            problems.append(f"{rel}: non-standard frontmatter keys {sorted(unknown)}")
        tools = toolset(data.get("allowed-tools", ""))
        if not tools:
            problems.append(f"{rel}: no allowed-tools, so it inherits the full tool surface")
            continue
        outside = tools - GLOBAL_ALLOWLIST
        if outside:
            problems.append(f"{rel}: allowed-tools outside the allowlist {sorted(outside)}")
        match = [t for t, s in tiers.items() if s == tools]
        if not match:
            problems.append(f"{rel}: allowed-tools {sorted(tools)} match no declared tier")
            continue
        tier = match[0]
        counts[tier] = counts.get(tier, 0) + 1

        # the body must state the same tier it declares, or the two drift apart
        if f"tool-tier: {tier}" not in body and "route" != tier:
            problems.append(f"{rel}: body does not state 'tool-tier: {tier}'")

        # advise-tier skills must be unreachable from a mutating operator
        if tier in ("advise", "route", "inspect") and tools & {"Write", "Edit"}:
            problems.append(f"{rel}: non-authoring tier '{tier}' must not include "
                            f"{sorted(tools & {'Write', 'Edit'})}")

        # offensive categories must be gated
        if any(g in rel for g in guarded) and tier not in ("advise", "route"):
            problems.append(f"{rel}: guarded category must be advise or route tier, found '{tier}'")

        lines = len(body.splitlines())
        if lines > 500:
            problems.append(f"{rel}: {lines} body lines, over the 500-line guidance")

    # ------------------------------------------------------- reference files
    cat_path = os.path.join(package_root, "roles.json")
    refs = 0
    if os.path.isfile(cat_path):
        for r in json.load(open(cat_path, encoding="utf-8"))["roles"]:
            rp = os.path.join(surface_root, r["path"])
            if not os.path.isfile(rp):
                problems.append(f"{r['path']}: reference file missing")
                continue
            refs += 1
            body = open(rp, encoding="utf-8").read()
            if f"tool-tier: {r['tool_tier']}" not in body:
                problems.append(f"{r['path']}: body does not state 'tool-tier: {r['tool_tier']}'")
            if r["allowed_tools"] != tiers_raw.get(r["tool_tier"]):
                problems.append(f"{r['path']}: allowed_tools disagree with tier '{r['tool_tier']}'")
            if r["operator_agent"] != operator_for.get(r["tool_tier"]):
                problems.append(f"{r['path']}: operator '{r['operator_agent']}' is not the "
                                f"'{r['tool_tier']}' operator")

    # ------------------------------------------------- link + workflow graph
    links_total = unresolved = 0
    cat2 = os.path.join(package_root, "roles.json")
    if os.path.isfile(cat2):
        rs = json.load(open(cat2, encoding="utf-8"))["roles"]
        known = {r["slug"] for r in rs}
        for r in rs:
            for group in ("upstream", "downstream"):
                for l in r.get("links", {}).get(group, []):
                    links_total += 1
                    if l.get("kind") == "unresolved":
                        unresolved += 1
                        problems.append(f"{r['slug']}: unresolved {group} link '{l['name']}'")
                    if l.get("kind") == "role" and l.get("slug") not in known:
                        problems.append(f"{r['slug']}: {group} link '{l['name']}' points at an unknown role")
            for o in r.get("links", {}).get("out_of_scope", []):
                links_total += 1
                rt = o.get("route_to", {})
                if rt.get("kind") == "unresolved":
                    unresolved += 1
                    problems.append(f"{r['slug']}: out-of-scope route '{rt.get('name')}' unresolved")

    wf_path = os.path.join(package_root, "workflows.json")
    wf_count = wf_steps = 0
    if os.path.isfile(wf_path):
        wfs = json.load(open(wf_path, encoding="utf-8"))["workflows"]
        wf_count = len(wfs)
        for w in wfs:
            if w.get("path") and not os.path.isfile(os.path.join(surface_root, w["path"])):
                problems.append(f"{w['path']}: workflow reference missing")
            for st in w["steps"]:
                wf_steps += 1
                special = st.get("skill") in ("agent", "dynamic", "external") or st.get("slug") in agents
                if st["slug"] not in known and not special:
                    problems.append(f"workflow {w['key']} step {st['step']}: unknown role {st['role']}")
                if st["operator_agent"] not in agents:
                    problems.append(f"workflow {w['key']} step {st['step']}: operator "
                                    f"{st['operator_agent']} does not exist")
    else:
        problems.append("it-role-library/workflows.json: missing")

    # ------------------------------------------------- layered method
    layers = policy.get("layers", {})
    lay_checked = 0
    if layers and os.path.isfile(cat2):
        for k in range(1, 7):
            L = layers.get(str(k))
            if not L:
                problems.append(f"policy: layer {k} undefined")
                continue
            a = agents.get(L["agent"])
            if not a:
                problems.append(f"layer {k}: agent {L['agent']} missing")
                continue
            if toolset(a.get("tools", "")) != tiers[L["tier"]]:
                problems.append(f"layer {k}: {L['agent']} tools do not equal its '{L['tier']}' tier")
            if a.get("model_class") != L["model_class"]:
                problems.append(f"layer {k}: {L['agent']} model_class {a.get('model_class')} != policy {L['model_class']}")
            if k > 1 and L["model_class"] == layers[str(k - 1)]["model_class"]:
                problems.append(f"layers {k - 1}/{k} share workload class {L['model_class']}: a reviewer would share its "
                                "producer's routing class (T6)")
        if toolset(agents.get("l5-realisation", {}).get("tools", "")) & {"Bash"}:
            problems.append("l5-realisation must not hold Bash: it would produce evidence about its own work")
        if toolset(agents.get("l6-evidence", {}).get("tools", "")) & {"Write", "Edit"}:
            problems.append("l6-evidence must not hold Write or Edit: it could alter what it observes")
        for r in json.load(open(cat2, encoding="utf-8"))["roles"]:
            lay_checked += 1
            k = r.get("layer")
            if k not in range(1, 7):
                problems.append(f"{r['slug']}: layer {k!r} not in 1..6")
                continue
            op = r.get("layer_operator")
            if op not in agents:
                problems.append(f"{r['slug']}: layer_operator {op} does not exist")
                continue
            layer_agents = {v["agent"] for v in layers.values()}
            if op in layer_agents and op != layers[str(k)]["agent"]:
                problems.append(f"{r['slug']}: layer-{k} role operated by another layer's agent {op}")
            opt = toolset(agents[op].get("tools", ""))
            if not opt <= tiers[r["tool_tier"]]:
                problems.append(f"{r['slug']}: {op} is wider than the role's own '{r['tool_tier']}' tier")
            if not opt <= tiers[layers[str(k)]["tier"]]:
                problems.append(f"{r['slug']}: {op} is wider than layer {k}'s agent")

    fab_dir = os.path.join(package_root, "fabric")
    if os.path.isfile(os.path.join(fab_dir, "fabric.py")):
        if fast:
            selftest = "skipped (--fast)"
        else:
            import subprocess
            st = subprocess.run([sys.executable, os.path.join(fab_dir, "fabric.py"), "selftest"],
                                capture_output=True, encoding="utf-8", errors="replace")
            selftest = st.stdout.strip().splitlines()[-1] if st.stdout.strip() else "no output"
            if st.returncode != 0:
                problems.append(f"fabric runtime self-test failed: {selftest}")
    else:
        selftest = "missing"
        problems.append("it-role-library/fabric/fabric.py: missing")

    tool_dir = os.path.join(package_root, "tools")
    tool_tests = []
    for tool in ("findings.py", "sabsa.py", "criteria.py", "doc_check.py", "test_check.py", "defect.py", "doc_survey.py"):
        tp = os.path.join(tool_dir, tool)
        if not os.path.isfile(tp):
            problems.append(f"it-role-library/tools/{tool}: missing")
        elif tool != "doc_survey.py":
            if fast:
                tool_tests.append(f"{tool[:-3]} present")
            else:
                import subprocess
                r = subprocess.run([sys.executable, tp, "selftest"], capture_output=True, encoding="utf-8", errors="replace")
                last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "no output"
                tool_tests.append(f"{tool[:-3]} {last.split(' checks')[0]}")
                if r.returncode != 0:
                    problems.append(f"{tool} self-test failed: {last}")
    # GA baseline: publication, repository and semantic-integrity engines carry deterministic regression suites.
    for tool in ("publication.py", "repository.py"):
        tp = os.path.join(tool_dir, tool)
        if not os.path.isfile(tp):
            problems.append(f"it-role-library/tools/{tool}: missing")
            continue
        if fast:
            tool_tests.append(f"{tool[:-3]} present")
        else:
            import subprocess
            r = subprocess.run([sys.executable, tp, "self-test"], capture_output=True, encoding="utf-8", errors="replace")
            last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "no output"
            tool_tests.append(f"{tool[:-3]} {last}")
            if r.returncode != 0:
                problems.append(f"{tool} self-test failed: {last}")

    # 3.4: every Section 6 role deliverable must resolve to an explicit production contract.
    art = os.path.join(tool_dir, "artifacts.py")
    if not os.path.isfile(art):
        problems.append("it-role-library/tools/artifacts.py: missing")
    else:
        import subprocess
        ar = subprocess.run([sys.executable, art, "check", "--root", root], capture_output=True, encoding="utf-8", errors="replace")
        last = ar.stdout.strip().splitlines()[-1] if ar.stdout.strip() else "no output"
        tool_tests.append("artifacts " + last)
        if ar.returncode != 0:
            problems.append("artifacts production-contract check failed: " + " | ".join(ar.stdout.splitlines()[:8]))

    # GA Semantic Integrity: schemas, SABSA->EA projection, Open Exchange conformance and generated-doc drift.
    import subprocess
    semantic_checks = [
        ("schema_check.py", ["check", "--root", root]),
        ("sabsa_ea.py", ["self-test"]),
        ("ea_conformance.py", ["self-test"]),
        ("artifacts.py", ["golden-test", "--root", root]),
        ("generate_docs.py", ["--root", root, "--check"]),
    ]
    for tool, extra in semantic_checks:
        tp=os.path.join(tool_dir,tool)
        if not os.path.isfile(tp):
            problems.append(f"it-role-library/tools/{tool}: missing")
            continue
        if fast and tool in ("sabsa_ea.py","ea_conformance.py"):
            tool_tests.append(f"{tool[:-3]} present")
            continue
        rr=subprocess.run([sys.executable,tp,*extra],capture_output=True,encoding="utf-8",errors="replace")
        last=rr.stdout.strip().splitlines()[-1] if rr.stdout.strip() else "no output"
        tool_tests.append(f"{tool[:-3]} {last}")
        if rr.returncode != 0:
            problems.append(f"{tool} semantic-integrity check failed: " + " | ".join(rr.stdout.splitlines()[:8]))
    # settings rules: Claude Code matches file permissions only through Edit(path) and Read(path); a
    # Write(path) rule is ignored with a startup warning. And deny beats allow, so an allow inside a denied
    # path never takes effect.
    snip_candidates = [
        os.path.join(package_root, "settings.snippet.json"),
        os.path.join(surface_root, "adapters", "claude", "settings.snippet.json"),
        os.path.join(root, ".claude", "settings.json"),
    ]
    snip_path = next((x for x in snip_candidates if os.path.isfile(x)), snip_candidates[0])
    if os.path.isfile(snip_path):
        perms = json.load(open(snip_path, encoding="utf-8")).get("permissions", {})
        for kind in ("deny", "allow", "ask"):
            for rule in perms.get(kind, []):
                tool = rule.split("(", 1)[0]
                if "(" in rule and tool in ("Write", "MultiEdit", "NotebookEdit"):
                    problems.append(f"settings.snippet.json: {kind} rule {rule} is never matched; "
                                    "file rules must be Edit(path) or Read(path)")
        strip = lambda r: r.split("(", 1)[1].rstrip(")").replace("**", "").rstrip("/") if "(" in r else r
        for a in perms.get("allow", []):
            for d in perms.get("deny", []):
                if a.split("(")[0] == d.split("(")[0] and strip(a).startswith(strip(d)):
                    problems.append(f"settings.snippet.json: allow {a} is overridden by deny {d}")
    # the package meets its own code documentation standard (the demo projects' gaps are deliberate)
    dc = os.path.join(package_root, "tools", "doc_check.py")
    if os.path.isfile(dc) and not fast:
        import subprocess
        own = [os.path.join(package_root, d) for d in ("tools", "hooks", "scripts", "fabric", "setup")]
        own += [os.path.join(package_root, "demo", "demo.py")]
        own += [os.path.join(surface_root, "skills", d, "scripts") for d in os.listdir(os.path.join(surface_root, "skills"))
                if os.path.isdir(os.path.join(surface_root, "skills", d, "scripts"))]
        r = subprocess.run([sys.executable, dc, "--errors-only", *[p for p in own if os.path.exists(p)]],
                           capture_output=True, encoding="utf-8", errors="replace")
        for line in r.stdout.splitlines():
            if ": error [" in line:
                problems.append("own code: " + os.path.relpath(line.split(":")[0], root) + ":" + line.split(":", 1)[1])
    claude_snippet_candidates = [
        os.path.join(package_root, "CLAUDE.snippet.md"),
        os.path.join(surface_root, "adapters", "claude", "CLAUDE.snippet.md"),
        os.path.join(root, ".claude", "CLAUDE.md"),
    ]
    if not any(os.path.isfile(x) for x in claude_snippet_candidates):
        problems.append("Claude routing snippet/output: missing")

    # every command is documented in the guide, and the demo kit works
    guide = os.path.join(package_root, "GUIDE.md")
    if not os.path.isfile(guide):
        problems.append("it-role-library/GUIDE.md: missing")
    else:
        gtext = open(guide, encoding="utf-8").read()
        for fn in sorted(os.listdir(os.path.join(surface_root, "commands"))) if os.path.isdir(os.path.join(surface_root, "commands")) else []:
            if fn.endswith(".md") and ours(f"commands/{fn}") and f"### /{fn[:-3]}\n" not in gtext:
                problems.append(f"GUIDE.md: no section '### /{fn[:-3]}' for commands/{fn}")
    # Canonical product documentation lives in the repository docs/ Markdown tree.
    # The installed runtime intentionally carries GUIDE.md and provider-native
    # command / skill contracts, not a duplicate, hard-coded HTML mini-site.
    # GUIDE coverage is checked above, including every installed /command.
    demo = os.path.join(package_root, "demo", "demo.py")
    if not os.path.isfile(demo):
        problems.append("it-role-library/demo/demo.py: missing")
    else:
        if fast:
            tool_tests.append("demo kit present")
        else:
            import subprocess
            r = subprocess.run([sys.executable, demo, "check"], capture_output=True, encoding="utf-8", errors="replace")
            tool_tests.append("demo kit " + (r.stdout.strip().splitlines()[-1].split(" checks")[0] if r.stdout.strip() else "?"))
            if r.returncode != 0:
                problems.append("demo kit check failed: " + " | ".join(l.strip() for l in r.stdout.splitlines() if "FAIL" in l)[:300])

    cmd_dir = os.path.join(surface_root, "commands")
    if os.path.isdir(cmd_dir):
        for fn in os.listdir(cmd_dir):
            if not ours(f"commands/{fn}"):
                continue                             # the user's own commands are not ours to judge
            d, _ = frontmatter(os.path.join(cmd_dir, fn))
            if not d or not d.get("description"):
                problems.append(f"commands/{fn}: missing description frontmatter")
            elif toolset(d.get("allowed-tools", "")) - GLOBAL_ALLOWLIST:
                problems.append(f"commands/{fn}: allowed-tools outside the allowlist")

    print(f"bundle   : {os.path.abspath(root)}")
    print(f"layers   : 6 agents, {lay_checked} roles mapped, fabric self-test {selftest}")
    print(f"tools    : self-tests " + ", ".join(tool_tests))
    print(f"links    : {links_total} ({unresolved} unresolved)")
    print(f"workflows: {wf_count} chains, {wf_steps} steps")
    print(f"roles    : {refs}")
    print(f"agents   : {len(agents)}")
    for asset in ("hooks/guard_library_write.py",
                  "scripts/approve_change.py", "CHANGE-RECORD.md", "CHANGELOG.md",
                  "VERSION", "workflows.json",
                  "templates/sabsa/architecture.md", "templates/sabsa/client-questions.md",
                  "standards/code-documentation.md", "standards/testing.md", "standards/defect-analysis.md",
                  "hooks/code_gate.py",
                  "hooks/guard_authority.py", "fabric/fabric.py",
                  "tools/artifacts.py", "tools/publication.py", "tools/repository.py",
                  "tools/sabsa_ea.py", "tools/ea_conformance.py", "tools/schema_check.py", "tools/generate_docs.py",
                  "artifacts/schema/artifact-types.json", "artifacts/schema/artifact-contract.schema.json",
                  "artifacts/contracts/role-deliverables.v3.json", "artifacts/contracts/golden-classification.json",
                  "jai/core/native-write-policy.json", "jai/migrations/migrate-26.10.0.py",
                  "jai/migrations/migrate-26.10.1.py", "schema/schema-registry.json", "ea/sabsa-mapping.json", "ea/schema/open-exchange-supported.xsd",
                  "artifacts/schema/generic-document.json", "artifacts/templates/generic-document.md",
                  "artifacts/role-deliverables.json",
                  "ea/schema/repository-model.json", "ea/consistency-policy.json", "ea/viewpoints.json"):
        if not os.path.exists(os.path.join(package_root, asset)):
            problems.append(f"it-role-library/{asset}: enforcement asset missing")

    # CI policy is a source-repository concern: GitHub discovers workflows only
    # under .github/workflows/, not inside an installed CLI runtime. Source checkouts
    # must carry the active policy; managed installations need not ship CI YAML.
    checkout = (os.path.isfile(os.path.join(root, "VERSION")) and
                os.path.isfile(os.path.join(root, ".ai", "runtime", "roles.json")))
    if checkout and not os.path.isfile(os.path.join(root, ".github", "workflows", "validate-library.yml")):
        problems.append("source GitHub validation workflow missing (.github/workflows/validate-library.yml)")

    # Provider-neutral source layout keeps installer/uninstaller and Claude snippets outside runtime/.
    # Installed layouts instead expose generated provider outputs. Accept either representation.
    alternate_assets = {
        "settings": [os.path.join(package_root, "settings.snippet.json"),
                     os.path.join(surface_root, "adapters", "claude", "settings.snippet.json"),
                     os.path.join(root, ".claude", "settings.json")],
        "installer": [os.path.join(package_root, "setup", "installer.py"),
                      os.path.join(surface_root, "setup", "installer.py")],
        "uninstaller.py": [os.path.join(package_root, "setup", "uninstaller.py"),
                           os.path.join(surface_root, "setup", "uninstaller.py")],
        "uninstall.sh": [os.path.join(package_root, "uninstall.sh"),
                         os.path.join(os.path.dirname(surface_root), "uninstall.sh")],
        "uninstall.cmd": [os.path.join(package_root, "uninstall.cmd"),
                          os.path.join(os.path.dirname(surface_root), "uninstall.cmd")],
    }
    for label, choices in alternate_assets.items():
        if not any(os.path.isfile(x) for x in choices):
            # Installed common-runtime checks do not own top-level installer/uninstaller bytes; source checks do.
            if surface_root != package_root or label == "settings":
                problems.append(f"{label}: enforcement asset/output missing")
    print(f"skills   : {skills}")
    print("tiers    : " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    # frontmatter every reader can parse — Claude Code reads it as YAML
    problems.extend(sorted(set(FRONTMATTER_PROBLEMS)))

    # agents are named as agents: in the texts Claude reads to decide how to call something, an agent named
    # in backticks must be declared or typed in place, or it gets called as a skill ("Unknown skill: ...")
    agent_names = {f[:-3] for f in os.listdir(os.path.join(surface_root, "agents")) if f.endswith(".md") and ours(f"agents/{f}")}
    skill_names = {d for d in os.listdir(os.path.join(surface_root, "skills")) if ours(f"skills/{d}/SKILL.md")}
    scan = [os.path.join("commands", f) for f in sorted(os.listdir(os.path.join(surface_root, "commands")))
            if f.endswith(".md") and ours(f"commands/{f}")]
    scan += [os.path.join("skills", d, "SKILL.md") for d in sorted(skill_names)]
    scan += [os.path.join("it-role-library", "CLAUDE.snippet.md")]
    for rel in scan:
        p = os.path.join(surface_root, rel)
        if not os.path.isfile(p):
            continue
        t = open(p, encoding="utf-8").read()
        declared = set()
        for line in t.splitlines():
            if line.startswith("> **Agents named here**"):
                declared |= set(re.findall(r"`([a-z0-9-]+)`", line))
        for m in re.finditer(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", t):
            name = m.group(1)
            if name in agent_names and name not in declared and "agent" not in t[max(0, m.start() - 70):m.end() + 70].lower():
                problems.append(f"{rel}: agent `{name}` is named without saying it is an agent")
        for m in re.finditer(r"`([a-z0-9-]+)` skill\b", t):
            if m.group(1) not in skill_names and not m.group(1).endswith("-"):
                problems.append(f"{rel}: `{m.group(1)}` is called a skill, but no such skill exists")
        for m in re.finditer(r"`([a-z0-9-]+)` \*{0,2}agent\b", t):
            if m.group(1) not in agent_names:
                problems.append(f"{rel}: `{m.group(1)}` is called an agent, but no such agent exists")

    if problems:
        print(f"\nFAILED ({len(problems)} problems):")
        for p in problems[:60]:
            print(f"  - {p}")
        if len(problems) > 60:
            print(f"  ... and {len(problems) - 60} more")
        return 1
    print("\nOK: every skill and agent is inside its declared tool ceiling.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
