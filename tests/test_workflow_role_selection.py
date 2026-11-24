# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
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


@pytest.mark.parametrize("all_required", [False, True])
def test_reviewed_profile_applies_to_equivalent_endpoints_without_workflow_edits(policy, all_required):
    from workflow_specialist_profiles import (PROFILE_PROTOCOL, compile_profiles, profile_for,
        role_revision, stage_policy, verify_policy)

    catalogue = policy["catalogue"]
    roles = policy["roles"]
    row = catalogue["bindings"][0]
    binding = row["variant_bindings"]["trial"]
    row.update(handover="Versioned source evidence", receiver_checks=["independent-receiver-attestation"])
    binding["acceptance_criterion"] = "Review the exact source evidence."
    binding["handoff_content_contract"]["units"][0]["id"] = "handoff/pilot:1.source"
    second = deepcopy(row)
    second["handoff_id"] = "second:1"
    second_binding = second["variant_bindings"]["trial"]
    second_binding["handoff_content_contract"]["id"] = "handoff/second:1"
    second_binding["handoff_content_contract"]["units"][0]["id"] = "handoff/second:1.source"
    catalogue["bindings"].append(second)
    contract = policy["reviewed"]["requirements"][0]["contract"]
    contracts = {contract["id"]: contract}
    if all_required:
        second_contract = {"id": "security-engineer:2", "version": "3.0.0"}
        contracts[second_contract["id"]] = second_contract
        for endpoint in (binding, second_binding):
            endpoint["contract_ids"] = list(contracts)
    instructions = {slug: "a" * 64 for slug in roles}
    profile = {"id": "siem-ingestion", "version": "1",
               "definition": profile_for(row, binding, roles["security-engineer"],
                                         list(contracts.values()) if all_required else contract)}
    if all_required:
        for invalid in ([contract], [contract, contract]):
            with pytest.raises(ValueError, match="WORKFLOW_PROFILE_CONTRACT"):
                profile_for(row, binding, roles["security-engineer"], invalid)
    endpoints = [{"handoff": key, "path": "trial", "endpoint": "producer",
                  "profile": profile["id"], "version": profile["version"], "mode": "required-specialist"}
                 for key in ("pilot:1", "second:1")]
    source = {"protocol": PROFILE_PROTOCOL, "profiles": [profile], "endpoints": endpoints, "mappings": [], "receipts": []}
    for slug in ("qradar-siem", "splunk-es"):
        mapping = {"profile": profile["id"], "version": profile["version"],
            "profile_digest": canonical_hash(profile), "slug": slug, "author": "fixture-author",
            "role_revision": role_revision(roles[slug], instructions[slug]),
            "product": slug, "deployments": [{"edition": "test", "version": "1", "deployment": "offline"}],
            "covered_units": ["source"]}
        receipt = {"reviewer": "fixture-reviewer", "decision": "approved", "mapping_digest": canonical_hash(mapping)}
        source["receipts"].append(receipt)
        source["mappings"].append({**mapping, "review_receipt": canonical_hash(receipt)})

    previous = deepcopy(source)
    previous["mappings"].pop()
    before, _ = compile_profiles(catalogue, previous, roles, instructions, contracts)
    compiled, pins = compile_profiles(catalogue, source, roles, instructions, contracts)
    assert len(pins) == 2
    assert source["endpoints"] == previous["endpoints"]
    assert [len(row["mappings"]) for row in before["requirements"]] == [1, 1]
    assert [len(row["mappings"]) for row in compiled["requirements"]] == [2, 2]
    if not all_required:
        compile_requirements(catalogue, compiled, roles, policy["ancestry"], policy["contract_versions"])
    assert compiled["requirements"][1]["mappings"][0]["covered_units"] == ["handoff/second:1.source"]
    assert compiled == compile_profiles(catalogue, source, roles, instructions, contracts)[0]
    source["endpoints"][0]["mode"] = "preferred-specialist"
    staged = stage_policy(catalogue, source, roles, instructions, contracts, policy["ancestry"])
    verify_policy(staged, roles, instructions, catalogue=catalogue, contracts=contracts)
    compiled_scope = compile_requirements(staged["catalogue"], staged["reviewed"], roles,
                                          policy["ancestry"], staged["contract_versions"])
    selection = {key: policy[key] for key in ("handoff", "path", "endpoint", "responsibility",
                                             "scope", "available", "independent")}
    def choose(**overrides):
        return eligible_roles(staged["catalogue"], compiled_scope, **{**selection, **overrides})

    selected, evidence = choose()
    assert selected == ["qradar-siem"]
    if all_required:
        assert [ref["id"] for ref in evidence["contract"]["contracts"]] == list(contracts)
        wrong_digest = deepcopy(contracts)
        wrong_digest[second_contract["id"]]["version"] = "older"
        with pytest.raises(ValueError, match="WORKFLOW_PROFILE_OBLIGATIONS"):
            verify_policy(staged, roles, instructions, catalogue=catalogue, contracts=wrong_digest)
    assert evidence["profile"]["mappings"]["qradar-siem"]["review_receipt"] == source["mappings"][0]["review_receipt"]
    fallback, reason = choose(scope=None, generic_applicable=True)
    assert fallback == ["security-engineer"]
    assert reason["fallback"] == "ADMITTED_PRODUCT_NEUTRAL_SCOPE"
    assert choose(scope=None)[0] == []
    assert choose(scope=None, generic_applicable=True, handoff="second:1")[0] == []
    assert choose(generic_applicable=True)[1]["blocker"] == "PRODUCT_SCOPE_CONFLICT"
    assert choose(scope={**selection["scope"], "version": "unsupported"})[0] == []
    assert choose(scope=None, generic_applicable=True, independent=False)[0] == []
    assert choose(endpoint="receiver")[0] == ["assessor"]
    overlapping = deepcopy(source)
    other = overlapping["mappings"][1]
    other["product"] = selection["scope"]["product"]
    reviewed_mapping = {key: value for key, value in other.items() if key != "review_receipt"}
    overlapping["receipts"][1]["mapping_digest"] = canonical_hash(reviewed_mapping)
    other["review_receipt"] = canonical_hash(overlapping["receipts"][1])
    multiple = stage_policy(catalogue, overlapping, roles, instructions, contracts, policy["ancestry"])
    assert eligible_roles(multiple["catalogue"], verify_policy(multiple, roles, instructions),
                          **selection)[0] == ["qradar-siem", "splunk-es"]
    unattested = deepcopy(source)
    unattested["mappings"][0]["deployments"][0]["edition"] = "different"
    with pytest.raises(ValueError, match="WORKFLOW_PROFILE_REVIEW_RECEIPT"):
        compile_profiles(catalogue, unattested, roles, instructions, contracts)
    corrupted = deepcopy(staged)
    corrupted["catalogue"]["bindings"][0]["variant_bindings"]["trial"]["workflow_role_requirement"]["profile"]["version"] = "tampered"
    with pytest.raises(ValueError, match="WORKFLOW_PROFILE_POLICY_DRIFT"):
        verify_policy(corrupted, roles, instructions, catalogue=catalogue, contracts=contracts)

    second_binding["acceptance_criterion"] = "Also verify a separate accountable owner."
    with pytest.raises(ValueError, match="WORKFLOW_PROFILE_OBLIGATIONS"):
        compile_profiles(catalogue, source, roles, instructions, contracts)
    second_binding["acceptance_criterion"] = binding["acceptance_criterion"]
    instructions["qradar-siem"] = "c" * 64
    with pytest.raises(ValueError, match="WORKFLOW_PROFILE_UNREVIEWED_REVISION"):
        compile_profiles(catalogue, source, roles, instructions, contracts)
