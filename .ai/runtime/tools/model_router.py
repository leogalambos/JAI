#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Project-managed provider-neutral workload-class model routing.

selection_strategy values in the registry are AI IT House policy labels, not
provider-native OpenAI/Anthropic API enums. Provider adapters translate the
resolved model/reasoning mapping at the execution boundary.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import tempfile
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1]
BASE = RUNTIME / "models/model-registry.json"
EFFORTS = {"none", "minimal", "low", "medium", "high", "xhigh", "max"}


def load(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def merge(base, override):
    if not isinstance(base, dict) or not isinstance(override, dict):
        return copy.deepcopy(override)
    out = copy.deepcopy(base)
    for key, value in override.items():
        if key in out and isinstance(out[key], dict) and isinstance(value, dict):
            out[key] = merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def default_override_path(registry):
    env_name = registry.get("configuration", {}).get("override_environment", "AI_HOUSE_MODEL_CONFIG")
    if os.environ.get(env_name):
        return Path(os.path.expanduser(os.environ[env_name]))
    configured = registry.get("configuration", {}).get("override_file_default")
    return Path(os.path.expanduser(configured)) if configured else None


def effective_registry(override=None):
    registry = load(BASE)
    path = Path(override).expanduser() if override else default_override_path(registry)
    if path and path.is_file():
        registry = merge(registry, load(path))
    return registry, path


def _mapping_problems(provider, workload_class, mapping):
    problems = []
    if not isinstance(mapping, dict):
        return [f"provider {provider}/{workload_class}: mapping must be object"]
    selector = mapping.get("model_selector")
    if not isinstance(selector, str) or not selector.strip():
        problems.append(f"provider {provider}/{workload_class}: model_selector missing")
    effort = mapping.get("reasoning_effort")
    if effort is not None and effort not in EFFORTS:
        problems.append(f"provider {provider}/{workload_class}: unsupported reasoning_effort {effort}")
    for i, fallback in enumerate(mapping.get("fallbacks", [])):
        if not isinstance(fallback, dict) or not fallback.get("model_selector"):
            problems.append(f"provider {provider}/{workload_class}: fallback {i} missing model_selector")
            continue
        fe = fallback.get("reasoning_effort")
        if fe is not None and fe not in EFFORTS:
            problems.append(f"provider {provider}/{workload_class}: fallback {i} unsupported reasoning_effort {fe}")
    return problems


def validate_registry(registry):
    problems = []
    classes = registry.get("workload_classes", {})
    providers = registry.get("providers", {})
    fallback = registry.get("fallback_class")
    if fallback not in classes:
        problems.append(f"fallback_class {fallback!r} is not defined")
    orders = []
    for name, spec in classes.items():
        order = spec.get("complexity_order")
        if not isinstance(order, int):
            problems.append(f"workload class {name}: complexity_order must be integer")
        else:
            orders.append((order, name))
        if not spec.get("description"):
            problems.append(f"workload class {name}: description missing")
    if len({order for order, _ in orders}) != len(orders):
        problems.append("workload class complexity_order values must be unique")
    for provider, spec in providers.items():
        if spec.get("strategy_scope") != "project-internal":
            problems.append(f"provider {provider}: strategy_scope must be project-internal")
        mapped = spec.get("classes", {})
        missing = sorted(set(classes) - set(mapped))
        if missing:
            problems.append(f"provider {provider}: missing classes {missing}")
        for name, mapping in mapped.items():
            if name not in classes:
                problems.append(f"provider {provider}: maps unknown class {name}")
            problems.extend(_mapping_problems(provider, name, mapping))
    for required in ("claude", "codex"):
        if required not in providers:
            problems.append(f"required provider {required} missing")
    return problems


def resolve(provider, workload_class, override=None):
    registry, _ = effective_registry(override)
    problems = validate_registry(registry)
    if problems:
        raise ValueError("; ".join(problems))
    if provider not in registry["providers"]:
        raise ValueError(f"unsupported provider {provider}")
    if workload_class not in registry["workload_classes"]:
        raise ValueError(f"unknown workload class {workload_class}")
    mapping = copy.deepcopy(registry["providers"][provider]["classes"][workload_class])
    return mapping["model_selector"], mapping


def candidates(provider, workload_class, override=None):
    selector, mapping = resolve(provider, workload_class, override)
    primary = {"model_selector": selector}
    if mapping.get("reasoning_effort"):
        primary["reasoning_effort"] = mapping["reasoning_effort"]
    return [primary] + copy.deepcopy(mapping.get("fallbacks", []))


def agent_root():
    for candidate in (RUNTIME.parent / "agents", RUNTIME / "agents"):
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError("canonical agent directory not found")


def agent_classes():
    result, problems = {}, []
    for path in sorted(agent_root().glob("*.md")):
        text = path.read_text(encoding="utf-8")
        legacy = re.search(r"^model:\s*([^\s]+)\s*$", text, re.MULTILINE)
        if legacy:
            problems.append(f"{path.name}: hard-coded model selector {legacy.group(1)}")
        match = re.search(r"^model_class:\s*([^\s]+)\s*$", text, re.MULTILINE)
        if not match:
            problems.append(f"{path.name}: model_class missing")
        else:
            result[path.stem] = match.group(1)
    return result, problems


def effective_payload(override=None):
    registry, path = effective_registry(override)
    problems = validate_registry(registry)
    agents, agent_problems = agent_classes()
    problems += agent_problems
    for agent, workload_class in agents.items():
        if workload_class not in registry.get("workload_classes", {}):
            problems.append(f"agent {agent}: unknown workload class {workload_class}")
    if problems:
        raise ValueError("; ".join(problems))
    resolved = {}
    for provider in registry["providers"]:
        resolved[provider] = {agent: candidates(provider, workload_class, override) for agent, workload_class in agents.items()}
    return {
        "registry_version": registry["registry_version"],
        # This is the runtime's installed projection of root VERSION.
        # Registry release is its original baseline, not a current product ID.
        "release": (RUNTIME / "VERSION").read_text(encoding="utf-8").strip(),
        "registry_origin_release": registry.get("release"),
        "override": str(path) if path and path.is_file() else None,
        "workload_classes": registry["workload_classes"],
        "providers": registry["providers"],
        "agents": agents,
        "resolved": resolved,
    }


def self_test():
    registry = load(BASE)
    tests = []
    tests.append(("registry-valid", not validate_registry(registry)))
    agents, problems = agent_classes()
    tests.append(("canonical-agents-use-classes", bool(agents) and not problems))
    tests.append(("four-base-classes", {"light", "standard", "heavy", "research"}.issubset(registry.get("workload_classes", {}))))
    tests.append(("claude-standard-resolves", resolve("claude", "standard")[0] == "sonnet"))
    cstd = candidates("codex", "standard")
    tests.append(("codex-standard-current-default", cstd[0] == {"model_selector": "gpt-6.1-sol", "reasoning_effort": "medium"}))
    tests.append(("codex-research-current-default", candidates("codex", "research")[0] == {"model_selector": "gpt-6-astra", "reasoning_effort": "xhigh"}))
    tests.append(("codex-host-fallback", candidates("codex", "heavy")[-1].get("model_selector") == "inherit"))
    with tempfile.TemporaryDirectory() as td:
        override = Path(td) / "models.json"
        override.write_text(json.dumps({"providers": {"codex": {"classes": {"standard": {"model_selector": "future-openai-model", "reasoning_effort": "high"}}}}}))
        tests.append(("user-override", candidates("codex", "standard", override)[0] == {"model_selector": "future-openai-model", "reasoning_effort": "high"}))
    for name, ok in tests:
        print(("PASS" if ok else "FAIL"), name)
    print(f"{sum(ok for _, ok in tests)}/{len(tests)} PASS")
    return 0 if all(ok for _, ok in tests) else 1


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("self-test")
    resolve_cmd = sub.add_parser("resolve")
    resolve_cmd.add_argument("--provider", required=True)
    resolve_cmd.add_argument("--class", dest="workload_class", required=True)
    resolve_cmd.add_argument("--config")
    effective = sub.add_parser("effective")
    effective.add_argument("--config")
    effective.add_argument("--out")
    args = parser.parse_args()
    if args.cmd == "self-test":
        raise SystemExit(self_test())
    if args.cmd == "resolve":
        registry, _ = effective_registry(args.config)
        provider = registry["providers"].get(args.provider, {})
        print(json.dumps({
            "provider": args.provider,
            "workload_class": args.workload_class,
            "selection_strategy": provider.get("selection_strategy"),
            "strategy_scope": provider.get("strategy_scope"),
            "candidates": candidates(args.provider, args.workload_class, args.config),
        }, indent=2))
        return
    payload = effective_payload(args.config)
    data = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        Path(args.out).write_text(data, encoding="utf-8")
    else:
        print(data, end="")


if __name__ == "__main__":
    main()
