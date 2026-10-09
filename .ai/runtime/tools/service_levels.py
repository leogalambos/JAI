#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Validate GA service objectives and the reference support SLA."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1]
PACKAGE = RUNTIME.parents[1]
SERVICE_LEVELS = RUNTIME / "operations/service-levels.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate():
    doc = load(SERVICE_LEVELS)
    problems = []
    slos = doc.get("slos", [])
    ids = [item.get("id") for item in slos]
    if len(ids) != len(set(ids)):
        problems.append("duplicate SLO IDs")
    required = {
        "SLO-REL-001", "SLO-REL-002", "SLO-SEM-001", "SLO-SEM-002",
        "SLO-EVD-001", "SLO-VIS-001", "SLO-PRV-001", "SLO-PERF-001",
    }
    missing = sorted(required - set(ids))
    if missing:
        problems.append(f"required SLOs missing: {missing}")
    valid_gates = set("ABCDEFGH") | {"A-H"}
    for item in slos:
        if item.get("gate") not in valid_gates:
            problems.append(f"{item.get('id')}: invalid gate {item.get('gate')}")
        for key in ("name", "target", "measurement"):
            if not item.get(key):
                problems.append(f"{item.get('id')}: missing {key}")
    sla = doc.get("reference_sla", {})
    if not isinstance(sla.get("contractual"), bool):
        problems.append("reference_sla.contractual must be boolean")
    if not sla.get("response_targets"):
        problems.append("reference SLA response targets missing")
    if not doc.get("error_budget_policy"):
        problems.append("error budget policy missing")
    return problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["check", "self-test"])
    args = parser.parse_args()
    problems = validate()
    if problems:
        print(f"FAILED ({len(problems)} problems)")
        for problem in problems:
            print(" -", problem)
        raise SystemExit(1)
    print("PASS service levels: GA SLOs, reference SLA and error-budget policy are defined")


if __name__ == "__main__":
    main()
