#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""AI IT House enterprise GA qualification core, gates A-G."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
import re
import shutil
import artifacts as artifact_registry
from offline_guard import run_offline
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[3]
RUNTIME = PACKAGE / ".ai/runtime"
TOOLS = RUNTIME / "tools"
PY = sys.executable
GATE_DIR = RUNTIME / "_meta/gates"
NEW_ROLES = {
    "enterprise-applications-architect",
    "secure-delivery-devsecops-architect",
    "siam-manager",
    "enterprise-release-manager",
    "it-financial-management-tbm-manager",
    "demand-and-intake-manager",
    "application-portfolio-manager",
}
NEW_WORKFLOWS = {
    "cyber-incident-breach-to-recovery",
    "resilience-validation",
    "demand-to-portfolio-to-funding",
    "source-to-contract-to-service",
    "siam-multi-supplier",
    "enterprise-release-orchestration",
    "regulatory-change-to-assurance",
}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def command(name, args, timeout=120):
    """Execute a mandatory local check under inherited offline enforcement.

    Args:
        name: Public check label.
        args: Explicit executable and argument vector; no shell expansion.
        timeout: Positive maximum execution duration in seconds.
    Returns:
        Located PASS, FAIL or NOT_EXECUTED record. The offline runner is always
        applied, including standalone qualification outside CI. Missing tools
        or unavailable OS controls are non-passing; there is no direct fallback.
    """
    print("RUN ", name, flush=True)
    result = run_offline(args, PACKAGE, timeout=timeout)
    state = result['status']
    ok = state == 'PASS' and result['returncode'] == 0
    if state == 'PASS' and not ok:
        state = 'FAIL'
    output = result.get('stdout', '') + result.get('stderr', '')
    if result.get('reason'):
        output += "\n" + result['reason']
    print(("PASS" if ok else state), name, flush=True)
    if not ok:
        print(output[-8000:], flush=True)
    return {"name": name, "ok": ok, "state": state,
            "detail": output[-2000:] if not ok else ""}


def governance_check():
    problems = []
    roles = {
        role["slug"]: role
        for role in json.loads((RUNTIME / "roles.json").read_text())["roles"]
    }
    workflows = json.loads((RUNTIME / "workflows.json").read_text())["workflows"]
    workflow_by_key = {workflow["key"]: workflow for workflow in workflows}
    contracts = [artifact_registry.flatten_v3(c) for c in json.loads(
        (RUNTIME / "artifacts/contracts/role-deliverables.v3.json").read_text()
    )["contracts"]]

    for slug in sorted(NEW_ROLES):
        role = roles.get(slug)
        if not role:
            problems.append(f"missing GA role {slug}")
            continue
        reference = PACKAGE / ".ai" / role["path"]
        if not reference.is_file():
            problems.append(f"{slug}: role reference missing")
        elif "## 13. Authority and limits" not in reference.read_text(
            encoding="utf-8"
        ):
            problems.append(f"{slug}: authority/limits section missing")
        role_contracts = [
            contract for contract in contracts
            if contract.get("role_slug") == slug
        ]
        if len(role_contracts) != 4:
            problems.append(
                f"{slug}: expected 4 artifact contracts, got "
                f"{len(role_contracts)}"
            )
        for contract in role_contracts:
            if not re.fullmatch(r"explicit-ga-[0-9]{2}\.(0[1-9]|1[0-2])\.[0-9]+", str(contract.get("classification_source", ""))):
                problems.append(f"{contract.get('id')}: classification is not explicit GA-reviewed")
            for key in (
                "acceptance_profile",
                "evidence_profile",
                "approver",
                "reviewers",
            ):
                if not contract.get(key):
                    problems.append(f"{contract.get('id')}: missing {key}")
        participants = [
            workflow["key"]
            for workflow in workflows
            if any(step.get("slug") == slug for step in workflow["steps"])
        ]
        if not participants:
            problems.append(f"{slug}: no workflow participation")

    for key in sorted(NEW_WORKFLOWS):
        workflow = workflow_by_key.get(key)
        if not workflow:
            problems.append(f"missing GA workflow {key}")
            continue
        if not workflow.get("mandatory_artifacts"):
            problems.append(f"{key}: mandatory artifacts missing")
        for step in workflow.get("steps", []):
            if not step.get("gate"):
                problems.append(f"{key} step {step.get('step')}: gate missing")
            if not step.get("hands_over"):
                problems.append(f"{key} step {step.get('step')}: handoff missing")

    if problems:
        for problem in problems:
            print("FAIL governance", problem)
        return {
            "name": "GA authorities/workflow governance",
            "ok": False,
            "detail": "; ".join(problems),
        }
    print(
        "PASS GA authorities/workflow governance: "
        "7 roles production-wired, 7 workflows gated"
    )
    return {
        "name": "GA authorities/workflow governance",
        "ok": True,
        "detail": "",
    }


def gate_a():
    """Run structural release checks and the shared DCS development regressions.

    Returns:
        Located check results, including real corpus evaluation and reproducible
        generated policy/workflow/calibration evidence. DCS regressions have a
        bounded 10-minute allowance for the full 12,550-case enterprise corpus.
        Passing this gate does not provide human domain or release approval.
    """
    return [
        *[command("DCS generated " + name + " reproducibility",
                  [PY, str(PACKAGE / "tools" / ("generate_content_" + name + ".py")), "--check"])
          for name in ("catalog", "corpus", "workflows", "calibration")],
        command(
            "DCS semantic and publication regression tests",
            [PY, "-m", "pytest", "-q",
             str(PACKAGE / "tests/test_content_lint.py"),
             str(PACKAGE / "tests/test_content_metrics.py"),
             str(PACKAGE / "tests/test_content_publication.py"),
             str(PACKAGE / "tests/test_content_eval.py"),
             str(PACKAGE / "tests/test_content_provider_parity.py"),
             str(PACKAGE / "tests/test_content_workflow.py"),
             str(PACKAGE / "tests/test_content_migrate.py"),
             str(PACKAGE / "tests/test_content_calibration.py"),
             str(PACKAGE / "tests/test_content_catalog.py"),
             str(PACKAGE / "tests/test_content_spec.py"),
             str(PACKAGE / "tests/test_content_integration.py"),
             str(PACKAGE / "tests/test_expert_references.py"),
             str(PACKAGE / "tests/test_optional_provider_eval.py"),
             str(PACKAGE / "tests/test_evaluation_package.py"),
             str(PACKAGE / "tests/test_content_scenarios.py"),
             str(PACKAGE / "tests/test_offline_guard.py"),
             str(PACKAGE / "tests/test_qualification_dependencies.py")],
            timeout=600,
        ),
        command(
            "DCS deterministic synthetic pilot (not human-gold)",
            [PY, str(TOOLS / "content_eval.py"), "run", "--root", str(PACKAGE)],
            timeout=600,
        ),
        command(
            "bundled expert reference structure and integrity",
            [PY, str(TOOLS / "expert_references.py"), "validate", "--root", str(PACKAGE), "--all"],
        ),
        command(
            "seven deterministic content lifecycle scenarios",
            [PY, str(TOOLS / "content_scenarios.py"), "run", "--root", str(PACKAGE)],
        ),
        command(
            "required local extended evaluation payload integrity",
            [PY, str(TOOLS / "evaluation_package.py"), "check", "--root", str(PACKAGE)],
        ),
        command(
            "Unified Lifecycle GA native enforcement",
            [PY, str(TOOLS / "native_enforcement_26104.py")],
        ),
        command(
            "current release schema resolver",
            [PY, str(TOOLS / "schema_resolver.py"), "self-test"],
        ),
        command(
            "architecture authority/write-path lint",
            [PY, str(TOOLS / "architecture_claim_lint.py")],
        ),
        command(
            "versioned schema + referential integrity",
            [PY, str(TOOLS / "schema_check.py"), "self-test", "--root", str(PACKAGE)],
        ),
        command(
            "artifact contracts",
            [PY, str(TOOLS / "artifacts.py"), "check", "--root", str(PACKAGE)],
        ),
        command(
            "artifact golden corpus",
            [PY, str(TOOLS / "artifacts.py"), "golden-test", "--root", str(PACKAGE)],
        ),
        command(
            "generated documentation",
            [PY, str(TOOLS / "generate_docs.py"), "--root", str(PACKAGE), "--check"],
        ),
        command(
            "canonical Markdown and provider-command documentation contract",
            [PY, str(TOOLS / "docs_contract.py"), "--root", str(PACKAGE)],
        ),
        command(
            "human-facing text width",
            [PY, str(TOOLS / "human_text_width.py"), "--root", str(PACKAGE)],
        ),
        command(
            "structural agent/role/workflow policy",
            [PY, str(RUNTIME / "scripts/check_agent_policy.py"), "--fast", str(PACKAGE)],
            timeout=240,
        ),
    ]


def gate_b():
    return [
        command("SABSA semantic runtime", [PY, str(TOOLS / "sabsa.py"), "selftest"]),
        command(
            "SABSA to JAI-scoped EA profile",
            [PY, str(TOOLS / "sabsa_ea.py"), "self-test"],
        ),
        command(
            "EA interoperability conformance",
            [PY, str(TOOLS / "ea_conformance.py"), "self-test"],
        ),
        command(
            "EA domain projection repository",
            [PY, str(TOOLS / "repository.py"), "self-test"],
        ),
    ]


def gate_c():
    return [
        governance_check(),
        command(
            "immutable execution record",
            [PY, str(TOOLS / "execution_record.py"), "self-test"],
        ),
    ]


def gate_d():
    return [
        command(
            "agent authority enforcement",
            [PY, str(TOOLS / "agent_runtime.py"), "self-test"],
        ),
        command("provider parity", [PY, str(TOOLS / "provider_parity.py")]),
        command(
            "enterprise adapter mutation enforcement",
            [PY, str(TOOLS / "integration_adapters.py"), "self-test"],
        ),
        command(
            "GA enforcement regression",
            [PY, str(TOOLS / "qualification_regression.py"), "--cross-gate"],
            timeout=120,
        ),
    ]


def publication_renderer_check():
    """Run renderer validation only when the required PDF executable is present.

    Returns:
        Mandatory non-passing NOT_EXECUTED record if LibreOffice is missing;
        otherwise the actual renderer self-test outcome. Presence is not PASS.
    """
    if not (shutil.which('libreoffice') or shutil.which('soffice')):
        return {'name': 'enterprise publication renderers', 'ok': False,
                'state': 'NOT_EXECUTED',
                'detail': 'Required PDF renderer dependency LibreOffice is unavailable.'}
    return command('enterprise publication renderers',
                   [PY, str(TOOLS / 'publication.py'), 'self-test'])


def gate_e():
    return [
        command(
            "publication projection contract",
            [PY, str(TOOLS / "projection.py"), "self-test"],
        ),
        publication_renderer_check(),
        command(
            "publication integrity",
            [PY, str(TOOLS / "publication_integrity.py"), "self-test"],
        ),
    ]


def gate_f():
    return [
        command(
            "render-based visual QA",
            [PY, str(TOOLS / "visual_qa.py"), "self-test"],
        )
    ]


def gate_g():
    return [
        command(
            "behavioral adversarial harness",
            [PY, str(TOOLS / "behavioral_eval.py"), "self-test"],
        ),
        command(
            "behavioral golden-corpus threshold conformance (fixture; no provider/model claim)",
            [PY, str(TOOLS / "behavioral_eval.py"), "qualify", "--results", str(RUNTIME / "evals/reference-results"), "--fixture-mode"],
        ),
    ]


GATES = {
    "A": gate_a,
    "B": gate_b,
    "C": gate_c,
    "D": gate_d,
    "E": gate_e,
    "F": gate_f,
    "G": gate_g,
}


def gate_payload(gate, checks):
    return {
        "release": (PACKAGE / "VERSION").read_text().strip(),
        "gate": gate,
        "generated_at": now(),
        "checks": checks,
        "pass": all(item["ok"] for item in checks),
    }


def run_gate(gate, out=None):
    checks = GATES[gate]()
    payload = gate_payload(gate, checks)
    target = Path(out) if out else GATE_DIR / f"gate-{gate}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(("PASS" if payload["pass"] else "FAIL"), f"Gate {gate}")
    return 0 if payload["pass"] else 1


def assemble(gate_dir=GATE_DIR, out=None):
    gate_dir = Path(gate_dir)
    checks = {}
    gates = {}
    problems = []
    for gate in "ABCDEFG":
        path = gate_dir / f"gate-{gate}.json"
        if not path.is_file():
            problems.append(f"missing {path}")
            continue
        data = json.loads(path.read_text())
        if data.get("gate") != gate:
            problems.append(f"{path}: wrong gate identity")
        checks[gate] = data.get("checks", [])
        gates[gate] = bool(data.get("pass"))
    payload = {
        "release": (PACKAGE / "VERSION").read_text().strip(),
        "qualification": "enterprise-release-gates-A-G",
        "generated_at": now(),
        "gates": gates,
        "checks": checks,
        "all_pass": not problems
        and set(gates) == set("ABCDEFG")
        and all(gates.values()),
    }
    target = Path(out) if out else RUNTIME / "_meta/qualification-A-G.json"
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    for problem in problems:
        print("FAIL", problem)
    for gate in "ABCDEFG":
        if gate in gates:
            print(("PASS" if gates[gate] else "FAIL"), f"Gate {gate}")
    return 0 if payload["all_pass"] else 1



def run_all():
    for gate in "ABCDEFG":
        if run_gate(gate):
            return 1
    if assemble():
        return 1
    print("GA qualification A-G: 7/7 enterprise gates PASS")
    return 0


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("qualify")
    gate = sub.add_parser("gate")
    gate.add_argument("name", choices=list("ABCDEFG"))
    gate.add_argument("--out")
    assemble_cmd = sub.add_parser("assemble")
    assemble_cmd.add_argument("--gate-dir", default=str(GATE_DIR))
    assemble_cmd.add_argument("--out")
    args = parser.parse_args()
    if args.cmd == "gate":
        return run_gate(args.name, args.out)
    if args.cmd == "assemble":
        return assemble(args.gate_dir, args.out)
    return run_all()


if __name__ == "__main__":
    raise SystemExit(main())
