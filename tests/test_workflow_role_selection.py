# SPDX-License-Identifier: BSD-4-Clause
"""Check exact endpoint, contract, scope and authority boundaries for role eligibility."""
from copy import deepcopy
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".ai/runtime/tools"))
from content_spec import canonical_hash
from workflow_role_selection import PROTOCOL, compile_requirements, eligible_roles


@pytest.fixture
def policy():
    """Supply two synthetic product mappings for one versioned producer boundary."""
    handoff_contract = {"id": "handoff/pilot:1", "version": "1.0.0", "units": [{"id": "source"}]}
    role_contract = {"id": "security-engineer:4", "version": "3.0.0"}
    row = {"handoff_id": "pilot:1", "contract_selection": "registered-contracts"}
    binding = {"producer_role": "security-engineer", "receiving_role": "assessor",
               "contract_ids": [role_contract["id"]], "handoff_content_contract": handoff_contract}
    row["variant_bindings"] = {"trial": binding, "reserved": {
        **binding, "producer_role": "engagement:named-authority",
        "receiving_role": "engagement:named-acceptance-authority"}}
    catalogue = {"catalog_hash": "pinned-fixture", "bindings": [row]}
    deployment = {"edition": "test", "version": "1", "deployment": "offline"}
    mapping = {"covered_units": ["source"], "deployments": [deployment],
               "handoff_contract_hash": canonical_hash(handoff_contract)}
    requirement = {"handoff": "pilot:1", "path": "trial", "endpoint": "producer",
                   "base": "security-engineer", "responsibility": "author", "contract": role_contract,
                   "mappings": [{**mapping, "slug": product, "product": product}
                                for product in ["splunk-es", "qradar-siem"]]}
    base = {"tool_tier": "execute", "allowed_tools": "Read, Bash", "operator_agent": "role-engineer"}
    roles = {slug: dict(base) for slug in ("security-engineer", "qradar-siem", "splunk-es")}
    ancestry = {slug: ["security-engineer"] for slug in ("qradar-siem", "splunk-es")}
    return dict(catalogue=catalogue,
                reviewed={"protocol": PROTOCOL, "workflow_catalogue": catalogue["catalog_hash"],
                          "requirements": [requirement]},
                roles=roles, ancestry=ancestry, contract_versions={role_contract["id"]: role_contract["version"]},
                handoff="pilot:1", path="trial", endpoint="producer", responsibility="author",
                scope={"product": "qradar-siem", **deployment},
                available=[*roles, "assessor", "engagement:named-authority",
                           "engagement:named-acceptance-authority"], independent=True)


def _evaluate(policy):
    inputs = dict(policy)
    catalogue = inputs.pop("catalogue")
    reviewed = inputs.pop("reviewed")
    roles = inputs.pop("roles")
    ancestry = inputs.pop("ancestry")
    versions = inputs.pop("contract_versions")
    compiled = compile_requirements(catalogue, reviewed, roles, ancestry, versions) if reviewed else None
    return eligible_roles(catalogue, compiled, **inputs)


@pytest.mark.parametrize("product", ["splunk-es", "qradar-siem"])
def test_selects_product_only_for_the_exact_contract(policy, product):
    policy["scope"]["product"] = product
    roles, evidence = _evaluate(policy)
    assert roles == [product]
    assert evidence["path"] == "trial"
    assert evidence["contract"] == {"id": "security-engineer:4", "version": "3.0.0"}
    assert set(evidence["mapping_hashes"]) == {product}


@pytest.mark.parametrize("input_name,value", [
    ("scope", None), ("scope", {"product": "other", "edition": "test", "version": "1",
                              "deployment": "offline"}),
    ("responsibility", "reviewer"), ("available", []), ("independent", False),
])
def test_rejects_inapplicable_or_unavailable_specialties(policy, input_name, value):
    policy[input_name] = value
    assert _evaluate(policy)[0] == []


@pytest.mark.parametrize("change,expected", [
    ("version", "WORKFLOW_ROLE_CONTRACT"),
    ("units", "WORKFLOW_ROLE_OBLIGATIONS"),
    ("ancestry", "WORKFLOW_ROLE_SPECIALTY"),
    ("authority", "WORKFLOW_ROLE_SPECIALTY"),
    ("hash", "WORKFLOW_ROLE_CATALOGUE"),
])
def test_inconsistent_mapping_fails_closed(policy, change, expected):
    requirement = policy["reviewed"]["requirements"][0]
    if change == "version":
        requirement["contract"]["version"] = "2.0.0"
    if change == "units":
        requirement["mappings"][0]["covered_units"] = []
    if change == "ancestry":
        policy["ancestry"] = {}
    if change == "authority":
        policy["roles"]["splunk-es"]["allowed_tools"] = "Read, Bash, WebSearch"
    if change == "hash":
        policy["reviewed"]["workflow_catalogue"] = "stale"
    with pytest.raises(ValueError, match=expected):
        _evaluate(policy)


@pytest.mark.parametrize("path,endpoint,expected", [
    ("trial", "receiver", "assessor"),
    ("reserved", "producer", "engagement:named-authority"),
    ("reserved", "receiver", "engagement:named-acceptance-authority"),
])
def test_other_endpoints_remain_exact(policy, path, endpoint, expected):
    policy.update(path=path, endpoint=endpoint)
    roles, evidence = _evaluate(policy)
    assert roles == [expected]
    assert evidence["mode"] == "exact"


def test_mapping_cannot_move_to_the_receiver_or_other_path(policy):
    policy["path"] = "unknown"
    with pytest.raises(ValueError, match="WORKFLOW_ROLE_PATH"):
        _evaluate(policy)
    policy.update(path="trial", endpoint="receiver")
    requirement = policy["reviewed"]["requirements"][0]
    moved = deepcopy(requirement)
    moved["endpoint"] = "receiver"
    policy["reviewed"]["requirements"].append(moved)
    with pytest.raises(ValueError, match="WORKFLOW_ROLE_BOUNDARY"):
        _evaluate(policy)


def test_no_policy_preserves_exact_default(policy):
    policy["reviewed"] = None
    roles, evidence = _evaluate(policy)
    assert roles == ["security-engineer"]
    assert evidence["mode"] == "exact"
