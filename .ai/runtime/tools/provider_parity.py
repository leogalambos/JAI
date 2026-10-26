#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Contract parity with explicit, restrictive provider capability differences."""
from agent_runtime import authorize, contracts, provider_config


def main():
    tests = []
    for contract in contracts().values():
        claude = provider_config(contract, "claude")
        codex = provider_config(contract, "codex")
        # Claude has no established read-only shell boundary in this profile.
        # Codex may project contract-declared Bash into its native read-only mode;
        # this checks configuration consistency, never actual host confinement.
        expected_codex = set(claude["tools"])
        reviewer_shell = (contract["authority_boundary"] == "read-only-review"
                          and "Bash" in contract["allowed_tools"]
                          and "Bash" not in contract.get("denied_tools", []))
        if reviewer_shell:
            expected_codex.add("Bash")
        tests += [
            (
                contract["id"] + ":mutation-parity",
                bool(claude["sandbox"]["workspace_write"])
                == bool(codex["workspace_write"]),
            ),
            (
                contract["id"] + ":role-scoped-tool-projection",
                expected_codex == set(codex["allowed_tools"])
                and (not reviewer_shell or (
                    "Bash" in claude["deny"]
                    and codex["native_codex"]["sandbox_mode"] == "read-only"
                    and not codex["workspace_write"])),
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
