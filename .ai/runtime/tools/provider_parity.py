#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Claude/Codex parity suite for Agent Contract and workload-class routing."""
from agent_runtime import authorize, contracts, provider_config


def main():
    tests = []
    for contract in contracts().values():
        claude = provider_config(contract, "claude")
        codex = provider_config(contract, "codex")
        tests += [
            (
                contract["id"] + ":mutation-parity",
                bool(claude["sandbox"]["workspace_write"])
                == bool(codex["workspace_write"]),
            ),
            (
                contract["id"] + ":tool-parity",
                set(claude["tools"]) == set(codex["allowed_tools"]),
            ),
            (
                contract["id"] + ":approval-parity",
                set(claude["approval_required_for"])
                == set(codex["approval_required_for"]),
            ),
            (
                contract["id"] + ":workload-class-parity",
                claude["workload_class"] == codex["workload_class"]
                == contract["workload_class"],
            ),
            (
                contract["id"] + ":model-route-resolves",
                bool(claude["model_selector"]) and bool(codex["model_selector"]),
            ),
        ]
        if contract["authority_boundary"] == "read-only-review":
            tests.append(
                (
                    contract["id"] + ":reviewer-isolation",
                    not authorize(contract, "write")[0],
                )
            )
    for name, value in tests:
        print(("PASS" if value else "FAIL"), name)
    print(f"{sum(value for _, value in tests)}/{len(tests)} PASS")
    return 0 if all(value for _, value in tests) else 1


if __name__ == "__main__":
    raise SystemExit(main())
