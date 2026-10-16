# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Local deterministic host-verifier simulations; no live authority is issued."""
import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest
import warnings
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("commercial_lifecycle", Path(__file__).resolve().parents[1] / ".ai/runtime/tools/commercial_lifecycle.py")
life = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(life)


def source():
    """Return an existing canonical technical engagement fixture."""
    return {"schema_version": "26.10.4", "id": "engagement:test", "profiles": ["technical"], "membership_ids": {"semantic:need": ["technical:member"]}, "objects": [{"id": "semantic:need", "object_type": "Requirement", "version": "1", "jai": {"core_version": "1.0.0", "layer": 1, "layer_name": "Intent and Context", "profile": "technical", "responsibility": "intent", "input_refs": [], "output_refs": [], "authority_ref": None, "acceptance_question": "Why?"}}]}


class LifecycleTest(unittest.TestCase):
    """Exercise real filesystem state with externally configured test trust."""

    def setUp(self):
        """Prepare a deterministic signed-receipt registry simulation."""
        self.trusted = {}
        self.policy = "trusted-policy-sha256"
        self.original = source()
        self.manifest = {"commitment_refs": ["claim:one"], "snapshot": "one"}

    def issue(self, receipt, role, human=False):
        """Register exact bytes in test host; this simulates external signature trust."""
        receipt = copy.deepcopy(receipt)
        self.trusted[life._digest(receipt)] = {"principal": receipt["principal"], "roles": [role], "human": human}
        return receipt

    def verifier(self, receipt):
        """Authenticate exact registered payload, refusing forged receipt fields."""
        return self.trusted.get(life._digest(receipt))

    def scope(self):
        """Create simulated human owner consent bound to original state."""
        return self.issue({"kind": "scope-change", "engagement_id": self.original["id"], "original_digest": life._digest(self.original), "profile": life.PROFILE, "policy_digest": self.policy, "principal": "human-owner"}, "engagement-owner", True)

    def receipt(self, axis, status, **extra):
        """Create a simulated role-authorized exact-manifest receipt."""
        value = {"kind": "assurance-axis", "axis": axis, "status": status, "id": axis + ":one", "manifest_digest": life._digest(self.manifest), "policy_digest": self.policy, "principal": axis + ":person"}
        value.update(extra)
        return self.issue(value, life.ROLES[axis], axis in {"authority_authorisation", "contractual_acceptance"})

    def test_activation_roundtrip_retains_exact_canonical_objects_and_history(self):
        """Activation extends only profile membership; rollback preserves signed history."""
        with patch("urllib.request.urlopen", side_effect=AssertionError("schema validation must remain offline")):
            bundle = life.activate(self.original, self.scope(), self.verifier, self.policy)
        self.assertEqual(bundle["candidate"]["objects"], self.original["objects"])
        self.assertEqual(bundle["crosswalk"][0]["canonical_id"], "semantic:need")
        with tempfile.TemporaryDirectory() as directory:
            store = life.EngagementStore(directory)
            self.assertEqual(store.read()["revision"], 0)
            store.commit(self.original, 0, {"kind": "signed-history", "signature": "preserved"})
            store.activate(bundle, 1, self.verifier, self.policy)
            generation = next(Path(directory).glob("generation-2-*.json"))
            old = generation.read_bytes()
            with self.assertRaises(life.LifecycleError):
                store.rollback(bundle["activation_digest"], 1)
            store.rollback(bundle["activation_digest"], 2)
            self.assertEqual(store.read()["engagement"], self.original)
            self.assertEqual(store.read()["history"][0]["signature"], "preserved")
            self.assertEqual(generation.read_bytes(), old)

    def test_activation_validates_local_schema_without_deprecated_api_or_network(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", DeprecationWarning)
            with patch("socket.create_connection", side_effect=AssertionError("network forbidden")):
                result = life.activate(self.original, self.scope(), self.verifier, self.policy)
        self.assertEqual(result["candidate"]["objects"], self.original["objects"])
        self.assertEqual([str(item.message) for item in caught if issubclass(item.category, DeprecationWarning)], [])

    def test_activation_rejects_invalid_referenced_binding(self):
        import jsonschema
        for mutation in (lambda binding: binding.pop("acceptance_question"), lambda binding: binding.update(layer=7)):
            with self.subTest(mutation=mutation):
                self.original = source()
                mutation(self.original["objects"][0]["jai"])
                with self.assertRaises(jsonschema.ValidationError):
                    life.activate(self.original, self.scope(), self.verifier, self.policy)

    def test_activation_rejects_unknown_schema_reference_without_network(self):
        read_text = Path.read_text

        def schema_with_unknown_reference(path, *args, **kwargs):
            import json
            text = read_text(path, *args, **kwargs)
            if path.name == "jai-object.schema.json":
                schema = json.loads(text)
                schema["properties"]["jai"]["$ref"] = "https://unregistered.invalid/binding.json"
                return json.dumps(schema)
            return text

        with patch.object(Path, "read_text", schema_with_unknown_reference):
            with patch("socket.create_connection", side_effect=AssertionError("network forbidden")):
                with self.assertRaisesRegex(life.LifecycleError, "unknown offline schema reference"):
                    life.activate(self.original, self.scope(), self.verifier, self.policy)

    def test_crash_after_generation_retries_without_overwriting_or_mixing_history(self):
        """Durable orphan generations cannot block a different same-revision retry."""
        def crash():
            raise RuntimeError("simulated process stop before pointer replacement")
        with tempfile.TemporaryDirectory() as directory:
            store = life.EngagementStore(directory)
            store.commit(self.original, 0, {"kind": "original"})
            candidate = copy.deepcopy(self.original)
            candidate["profiles"].append("other-profile")
            with self.assertRaises(RuntimeError):
                store.commit(candidate, 1, {"kind": "orphan"}, _before_pointer=crash)
            self.assertEqual(store.read()["engagement"], self.original)
            orphan = next(Path(directory).glob("generation-2-*.json"))
            orphan_bytes = orphan.read_bytes()
            self.assertEqual(store.commit(self.original, 1, {"kind": "retried"}), 2)
            self.assertEqual(store.read()["history"][-1]["kind"], "retried")
            self.assertEqual(orphan.read_bytes(), orphan_bytes)
            with self.assertRaises(life.LifecycleError):
                store.commit(candidate, 1)

    def test_rollback_rejects_changed_historical_activation_body(self):
        """An injected activation event cannot borrow an authenticated bundle digest."""
        bundle = life.activate(self.original, self.scope(), self.verifier, self.policy)
        with tempfile.TemporaryDirectory() as directory:
            store = life.EngagementStore(directory)
            store.commit(self.original, 0)
            store.activate(bundle, 1, self.verifier, self.policy)
            changed = copy.deepcopy(bundle)
            changed["original"]["profiles"].append("forged-history")
            with self.assertRaises(life.LifecycleError):
                store.activate(changed, 2, self.verifier, self.policy)
            store.commit(bundle["candidate"], 2, {"kind": "activation", "bundle": changed})
            with self.assertRaises(life.LifecycleError):
                store.rollback(bundle["activation_digest"], 3)
            self.assertEqual(store.read()["engagement"], bundle["candidate"])

    def test_migration_rejects_versions_duplicates_missing_membership_and_forgery(self):
        """Invalid migration cannot alter an engagement or manufacture owner consent."""
        for mutation in (lambda v: v.update(schema_version="unknown"), lambda v: v["objects"].append(copy.deepcopy(v["objects"][0])), lambda v: v.update(membership_ids={}), lambda v: v["objects"][0].update(canonical_ref="other")):
            original = copy.deepcopy(self.original)
            mutation(original)
            with self.assertRaises(life.LifecycleError):
                life.activate(original, self.scope(), self.verifier, self.policy)
        receipt = self.scope()
        receipt["principal"] = "forged-owner"
        with self.assertRaises(life.LifecycleError):
            life.activate(self.original, receipt, self.verifier, self.policy)

    def test_all_six_axes_are_independent_and_require_explicit_authenticated_receipts(self):
        """A complete fixture commits; each omitted axis blocks without implying others."""
        receipts = [self.receipt("domain_validity", "valid"), self.receipt("evidence_verification", "verified"), self.receipt("independent_review", "accepted", covered_refs=["claim:one"], blocking_findings=[], constraints_satisfied=True), self.receipt("authority_authorisation", "granted"), self.receipt("contractual_acceptance", "accepted")]
        approval = self.receipt("snapshot_approval", "approved", review_id="independent_review:one")
        receipts = life.approve_snapshot(self.manifest, receipts, approval, self.verifier, self.policy, ["maker"])
        self.assertTrue(life.assess_axes(self.manifest, receipts, self.verifier, self.policy, ["maker"])["commitment_ready"])
        for omitted in life.AXES:
            subset = [r for r in receipts if r["axis"] != omitted and not (omitted == "independent_review" and r["axis"] == "snapshot_approval")]
            result = life.assess_axes(self.manifest, subset, self.verifier, self.policy, ["maker"])
            self.assertFalse(result["commitment_ready"])
            self.assertEqual(result["axes"][omitted], life.AXES[omitted][0])

    def test_stale_manifest_and_policy_invalidate_without_rewriting_receipts(self):
        """Snapshot changes invalidate approval and human authorization bindings."""
        receipt = self.receipt("snapshot_approval", "approved", review_id="review")
        changed = dict(self.manifest, snapshot="two")
        self.assertEqual(life.assess_axes(changed, [receipt], self.verifier, self.policy, ["maker"])["axes"]["snapshot_approval"], "stale")
        with self.assertRaises(life.LifecycleError):
            life.approve_snapshot(changed, [], receipt, self.verifier, self.policy, ["maker"])
        authority = self.receipt("authority_authorisation", "granted")
        self.assertEqual(life.assess_axes(self.manifest, [authority], self.verifier, "new-policy", ["maker"])["axes"]["authority_authorisation"], "absent")

    def test_review_rejects_missing_coverage_self_review_and_identity_forgery(self):
        """Valid signature alone cannot bypass maker/checker or full claim coverage."""
        for extra in ({"covered_refs": []}, {"principal": "maker", "covered_refs": ["claim:one"]}):
            receipt = self.receipt("independent_review", "accepted", blocking_findings=[], constraints_satisfied=True, **extra)
            with self.assertRaises(life.LifecycleError):
                life.assess_axes(self.manifest, [receipt], self.verifier, self.policy, ["maker"])
        forged = self.receipt("domain_validity", "valid")
        forged["principal"] = "impostor"
        with self.assertRaises(life.LifecycleError):
            life.assess_axes(self.manifest, [forged], self.verifier, self.policy, ["maker"])


if __name__ == "__main__":
    unittest.main()
