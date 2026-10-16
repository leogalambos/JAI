# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Regression coverage for the commercial coordinator's least-privilege contract."""
import json
import importlib.util
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
NAME = "commercial-coordinator"


class CommercialPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = json.loads((ROOT / ".ai/runtime/policy.json").read_text(encoding="utf-8"))

    def test_coordinator_is_bound_to_exact_read_only_route_tier(self):
        tier = self.policy["agent_tier"].get(NAME)
        self.assertEqual(tier, "route")
        allowed = {item.strip() for item in self.policy["tiers"][tier].split(",")}
        text = (ROOT / f".ai/agents/{NAME}.md").read_text(encoding="utf-8")
        match = re.search(r"^tools: (.+)$", text, re.MULTILINE)
        self.assertIsNotNone(match)
        actual = {item.strip() for item in match.group(1).split(",")}
        self.assertEqual(actual, {"Read", "Grep", "Glob"})
        self.assertLessEqual(actual, allowed)
        self.assertTrue(actual.isdisjoint({"Write", "Edit", "Bash", "Task", "Agent"}))

    def test_coordinator_explicitly_denies_all_writes(self):
        self.assertEqual(self.policy["write_scope"].get(NAME), {"allow": [], "deny": ["**"]})

    def _declared_agents(self, relative):
        text = (ROOT / relative).read_text(encoding="utf-8")
        declared = set()
        for line in text.splitlines():
            if line.startswith("> **Agents named here**"):
                declared.update(re.findall(r"`([a-z0-9-]+)`", line))
        return declared

    def test_command_names_the_coordinator_as_an_agent(self):
        self.assertIn(NAME, self._declared_agents(".ai/commands/commercial.md"))

    def test_skill_names_the_coordinator_as_an_agent(self):
        self.assertIn(NAME, self._declared_agents(".ai/skills/commercial-delivery/SKILL.md"))

    def test_provider_projections_preserve_read_only_ceiling_and_parent_dispatch(self):
        spec = importlib.util.spec_from_file_location("commercial_policy_installer", ROOT / ".ai/setup/installer.py")
        installer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(installer)
        registry = json.loads((ROOT / ".ai/runtime/models/model-registry.json").read_text(encoding="utf-8"))
        source = ROOT / f".ai/agents/{NAME}.md"
        claude = installer.render_claude_agent(source, registry).decode()
        frontmatter, _ = installer.split_frontmatter(claude)
        self.assertEqual(frontmatter["tools"], "Read, Grep, Glob")
        codex = installer.render_codex_skill(source, "agent", NAME, registry).decode()
        self.assertIn("Source tool ceiling: `Read, Grep, Glob`", codex)
        for rendered in (claude, codex):
            self.assertIn("The parent dispatches fresh role-bounded workers and independent reviewers", rendered)
            self.assertIn("this read-only agent cannot maintain that state", rendered)


if __name__ == "__main__":
    unittest.main()
