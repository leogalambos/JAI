# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Commercial snapshot schema closure and compatibility at public boundaries."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import jsonschema

from test_commercial_core import complete_snapshot, core, snapshot


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / ".ai/runtime/schema/contracts/commercial-snapshot-v1.schema.json").read_text(encoding="utf-8"))


class CommercialSnapshotSchemaTests(unittest.TestCase):
    def test_critical_root_is_closed_and_unknown_properties_fail(self):
        self.assertIs(SCHEMA.get("additionalProperties"), False)
        bad = snapshot()
        bad["misspelled_qualification"] = True
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(bad, SCHEMA)

    def test_published_examples_complete_graph_and_both_current_views_validate(self):
        paths = sorted((ROOT / ".ai/runtime/commercial/examples").glob("*snapshot*.json"))
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(example=path.name):
                jsonschema.validate(json.loads(path.read_text(encoding="utf-8")), SCHEMA)
        data, _ = complete_snapshot()
        jsonschema.validate(data, SCHEMA)
        for audience in ("internal", "client"):
            jsonschema.validate(core.current_view(data, audience=audience), SCHEMA)
        jsonschema.validate(snapshot(), SCHEMA)

    def test_optional_runtime_fields_are_typed_without_requiring_qualification(self):
        data = snapshot()
        optional = {"crosswalk": [], "discovery": [], "enforcement": {}, "operational_recovery": {}, "captured_at": "2026-10-17T00:00:00Z", "recovery_policy": {}}
        data.update(optional)
        jsonschema.validate(data, SCHEMA)
        for name, wrong in {"crosswalk": {}, "discovery": {}, "enforcement": [], "operational_recovery": [], "captured_at": 42, "recovery_policy": []}.items():
            with self.subTest(field=name):
                bad = copy.deepcopy(data)
                bad[name] = wrong
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.validate(bad, SCHEMA)

    def test_store_and_archive_keep_metadata_outside_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            data, _ = complete_snapshot()
            data["captured_at"] = "2026-10-17T00:00:00Z"
            data["recovery_policy"] = {"owner": "fixture", "legal_hold": True}
            store = core.SnapshotStore(Path(directory) / "store")
            store.commit(data, 0)
            stored = store.read()
            jsonschema.validate(stored["snapshot"], SCHEMA)
            destination = Path(directory) / "archive.json"
            store.archive(destination)
            archive = json.loads(destination.read_text(encoding="utf-8"))
            jsonschema.validate(archive["snapshot"], SCHEMA)
            restored = core.SnapshotStore(Path(directory) / "restored")
            restored.restore(destination)
            self.assertEqual(restored.read()["snapshot"], data)
            self.assertEqual(set(stored), {"revision", "snapshot"})

