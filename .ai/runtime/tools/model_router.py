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
EFFORTS = {"none", "minimal", "low", "medium", "high", "xhigh", "max", "ultra"}


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
    kind = mapping.get("model_kind")
    if "model_kind" in mapping and (not isinstance(kind, str) or kind not in {"ai", "deterministic"}):
        problems.append(f"provider {provider}/{workload_class}: invalid model_kind")
    if provider in {"codex", "claude"}:
        if kind == "deterministic":
            problems.append(f"provider {provider}/{workload_class}: native AI cannot be relabeled deterministic")
        if "model_provider" in mapping and mapping["model_provider"] != provider:
            problems.append(f"provider {provider}/{workload_class}: native model_provider must match the native provider")
        if "model_identity" in mapping and mapping["model_identity"] != selector:
            problems.append(f"provider {provider}/{workload_class}: native model_identity must match the selected model")
    elif provider == "json-process/1":
        execution = mapping.get("execution", {})
        if kind is not None and (not isinstance(execution, dict) or execution.get("provider") != "json-process/1"):
            problems.append(f"provider {provider}/{workload_class}: model_kind requires the captured process execution contract")
        if kind == "ai" and (not isinstance(mapping.get("model_provider"), str) or mapping["model_provider"] not in {"codex", "claude"}
                or not isinstance(mapping.get("model_identity"), str) or not mapping["model_identity"].strip()):
            problems.append(f"provider {provider}/{workload_class}: wrapped AI requires explicit model_provider and model_identity")
        if kind != "ai" and any(field in mapping for field in ("model_provider", "model_identity")):
            problems.append(f"provider {provider}/{workload_class}: backend model fields require an explicit AI declaration")
    for i, fallback in enumerate(mapping.get("fallbacks", [])):
        if not isinstance(fallback, dict) or not fallback.get("model_selector"):
            problems.append(f"provider {provider}/{workload_class}: fallback {i} missing model_selector")
            continue
        fe = fallback.get("reasoning_effort")
        if fe is not None and fe not in EFFORTS:
            problems.append(f"provider {provider}/{workload_class}: fallback {i} unsupported reasoning_effort {fe}")
    return problems


def validate_registry(registry):
    """Validate routing vocabulary and an optional pinned execution preference.

    Args:
        registry: Parsed provider-neutral registry with classes and provider mappings.
    Returns:
        Validation problems, empty when structural contracts are consistent.
        This does not prove concrete account/model/client capability or authority.
    """
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
    if "professional_review_constraints" in registry:
        import professional_review
        problems.extend(professional_review.constraints_problems(registry["professional_review_constraints"]))
    preference = registry.get("execution_profile")
    if preference is not None:
        try:
            import execution_profiles
            problems.extend(execution_profiles.validate_snapshot(preference, registry))
        except (ValueError, KeyError, TypeError) as error:
            problems.append("invalid captured execution profile: " + str(error))
    for required in ("claude", "codex"):
        if required not in providers:
            problems.append(f"required provider {required} missing")
    return problems


def resolve(provider, workload_class, override=None):
    registry, _ = effective_registry(override)
    return resolve_snapshot(registry, provider, workload_class)


def resolve_snapshot(registry, provider, workload_class):
    """Resolve an explicit immutable registry without ambient overrides.

    Args:
        registry: Captured and explicitly selected model registry object.
        provider: Exact registered provider identifier.
        workload_class: Exact registered workload class.
    Returns:
        Model selector and independent copy of its declared mapping.
    Raises:
        ValueError: Registry, provider or workload capability is unavailable.
    """
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
