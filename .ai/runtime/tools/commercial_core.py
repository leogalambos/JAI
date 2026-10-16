#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Opt-in commercial canonical snapshots and fail-closed assurance primitives.

This module validates recorded evidence, not the truth of prose. Host isolation,
identity issuance and legal decisions remain external trusted responsibilities.
"""
from __future__ import annotations

import argparse
import base64
import time
import copy
import fcntl
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import tempfile
from datetime import datetime, timezone

PROFILE = "commercial-delivery/1"
TYPES = set("Source Passage Claim Need Attribute Requirement DomainContract ExecutionContract Fragment WorkPackage RoleAllocation Estimate Rate Cost Price Reserve Baseline Forecast Actual Accrual Payment Publication Review AuthorityAct".split())
FORWARD = {"derives", "refines", "supports", "requests", "consolidated_into", "allocation", "disclosure"}
RELATIONS = FORWARD | {"navigation", "review", "supersession"}
LAYERS = ("contextual", "conceptual", "logical", "physical", "component", "operational")
QUESTIONS = ("what", "why", "who", "when", "where", "how")
PHASES = ("qualification", "discovery", "options", "bid-review", "negotiation", "mobilization", "delivery", "acceptance", "operations", "renewal", "exit")
DEPENDENCY_PAIRS = {
    ("Source", "Passage"), ("Passage", "Claim"), ("Claim", "Need"),
    ("Need", "Attribute"), ("Attribute", "Requirement"), ("Claim", "Requirement"),
    ("Requirement", "DomainContract"), ("DomainContract", "ExecutionContract"),
    ("ExecutionContract", "ExecutionContract"), ("ExecutionContract", "Fragment"),
    ("Fragment", "WorkPackage"), ("WorkPackage", "Estimate"),
    ("WorkPackage", "RoleAllocation"), ("Estimate", "RoleAllocation"),
    ("Estimate", "Cost"), ("RoleAllocation", "Cost"), ("Rate", "Cost"),
    ("Cost", "Price"), ("Cost", "Reserve"), ("Reserve", "Price"),
    ("Price", "Baseline"), ("Baseline", "Forecast"), ("Actual", "Forecast"),
    ("Accrual", "Forecast"), ("Payment", "Forecast"), ("Forecast", "Publication"),
    ("Price", "Publication"), ("Review", "Publication"), ("AuthorityAct", "Baseline")
}
MANDATORY = set("scope deliverables price assumptions dependencies acceptance change_control liability ip_data validity payment exit".split())


class CommercialError(ValueError):
    """A profile invariant failed; the candidate must not become current."""


def digest(value):
    """Return SHA256 of canonical JSON value; reject non-JSON values via TypeError."""
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def _require(condition, message):
    if not condition:
        raise CommercialError(message)


def _index(snapshot):
    return {e["version_id"]: e for e in snapshot["entities"]}


def validate_crosswalk(rows):
    """Validate canonical reuse rows; return True or raise CommercialError.

    A source version cannot fork identities, nor lose its original memberships.
    """
    seen = {}
    for row in rows:
        key = (row["source_system"], row["source_id"], row["source_version"])
        canonical = (row["canonical_id"], row["canonical_version"])
        _require(key not in seen or seen[key] == canonical, "duplicate semantic master")
        seen[key] = canonical
        _require(set(row.get("original_membership_ids", [])) <= set(row["membership_ids"]), "lost membership")
        _require(row.get("mapping_state") == "exact", "unresolved identity crosswalk")
    return True


def current_view(snapshot, require_publications=False, audience=None):
    """Return current selected closure while retaining history in the source snapshot.

    Explicit active_roots bind internal and client publication versions. Their
    closure must contain exactly the explicitly scoped active_claims; review
    references are included without turning review/supersession into impact edges.
    Draft gates may instead select active_versions before publications exist.
    Raises CommercialError on missing/ambiguous selection or dangling references.
    """
    index = _index(snapshot)
    roots = snapshot.get("active_roots")
    if roots is not None:
        _require(set(roots) == {"internal", "client"}, "both audience roots required")
        _require(len(set(roots.values())) == 2, "audience roots must be distinct")
        for root_audience, root in roots.items():
            _require(root in index and index[root]["type"] == "Publication", "invalid publication root")
            _require(index[root]["data"].get("audience") == root_audience, "root audience mismatch")
        selected = set()
        for root in roots.values():
            selected.update(trace(snapshot, root, True))
        claims = {key for key in selected if index[key]["type"] == "Claim"}
        _require("active_claims" in snapshot and set(snapshot["active_claims"]) == claims, "active commitment scope/closure mismatch")
        if audience is not None:
            _require(audience in roots, "unknown current audience")
            selected = set(trace(snapshot, roots[audience], True))
    else:
        _require(not require_publications, "explicit current publication roots required")
        selected = set(snapshot.get("active_versions", index.keys()))
        _require(selected <= index.keys(), "dangling active version")
        _require(len({index[k]["id"] for k in selected}) == len(selected), "draft current selection contains historical alternatives")
    for key in list(selected):
        entity = index[key]
        if entity["type"] == "Claim":
            review = entity["data"].get("support_review")
            if review in index:
                selected.add(review)
    view = copy.deepcopy(snapshot)
    view["entities"] = [e for e in snapshot["entities"] if e["version_id"] in selected]
    view["relations"] = [e for e in snapshot.get("relations", []) if e["input"] in selected and e["output"] in selected]
    if audience is not None:
        view.pop("active_roots", None)
        view.pop("active_claims", None)
        view["active_versions"] = sorted(selected)
    return view


def validate_snapshot(snapshot):
    """Validate an explicit opt-in immutable graph; return True or raise CommercialError.

    Endpoints reference exact versions. Forward edges must be acyclic; navigation,
    supersession and review are intentionally excluded from invalidation traversal.
    """
    _require(snapshot.get("profile") == PROFILE, "unsupported or inactive profile")
    _require(snapshot.get("schema_version") == "1", "unsupported schema version")
    entities = snapshot.get("entities", [])
    _require(isinstance(entities, list), "entities must be a list")
    index = {}
    common = {"id", "version_id", "type", "schema_version", "engagement_id", "timestamp", "accountable_owner", "classification", "provenance", "data"}
    for entity in entities:
        _require(common <= entity.keys(), "missing canonical fields")
        _require(entity["type"] in TYPES, "unknown entity type")
        _require(entity["schema_version"] == "1", "unsupported entity schema")
        _require(entity["version_id"] not in index, "duplicate version")
        _require(all(entity[k] for k in ("id", "version_id", "engagement_id", "timestamp", "accountable_owner")), "empty canonical field")
        _require(entity["classification"] in {"public", "client-contract", "internal-commercial", "restricted-personal"}, "unknown classification")
        index[entity["version_id"]] = entity
    if "active_roots" in snapshot:
        roots = snapshot["active_roots"]
        _require(isinstance(roots, dict) and set(roots) == {"internal", "client"}, "both audience roots required")
        _require(len(set(roots.values())) == 2, "audience roots must be distinct")
        for audience, key in roots.items():
            _require(key in index and index[key]["type"] == "Publication" and index[key]["data"].get("audience") == audience, "invalid audience publication root")
        _require(isinstance(snapshot.get("active_claims"), list) and len(set(snapshot["active_claims"])) == len(snapshot["active_claims"]), "explicit unique active claims required")
        _require(all(key in index and index[key]["type"] == "Claim" for key in snapshot["active_claims"]), "invalid active claim")
    graph = {key: [] for key in index}
    for edge in snapshot.get("relations", []):
        _require(edge.get("type") in RELATIONS, "unknown relation type")
        _require(edge.get("input") in index and edge.get("output") in index, "dangling relation")
        if edge["type"] in FORWARD:
            left, right = index[edge["input"]], index[edge["output"]]
            _require((left["type"], right["type"]) in DEPENDENCY_PAIRS, "invalid dependency endpoint types")
            if left["type"] == right["type"] == "ExecutionContract":
                _require(right["data"].get("layer", 0) == left["data"].get("layer", 0) + 1, "nonadjacent execution layers")
            graph[edge["input"]].append(edge["output"])
        if edge["type"] == "review":
            _require(index[edge["input"]]["type"] == "Review", "review endpoint type")
        if edge["type"] == "supersession":
            _require(index[edge["input"]]["id"] == index[edge["output"]]["id"], "supersession changes identity")
    active, done = set(), set()
    def visit(key):
        _require(key not in active, "forward dependency cycle")
        if key in done:
            return
        active.add(key)
        for child in graph[key]:
            visit(child)
        active.remove(key)
        done.add(key)
    for key in graph:
        visit(key)
    validate_crosswalk(snapshot.get("crosswalk", []))
    return True


def trace(snapshot, version_id, reverse=False):
    """Return reachable exact-version IDs, including the start, or raise CommercialError.

    Args: snapshot is a validated graph; reverse selects provenance over impact.
    """
    validate_snapshot(snapshot)
    _require(version_id in _index(snapshot), "unknown version")
    graph = {}
    for edge in snapshot.get("relations", []):
        if edge["type"] in FORWARD:
            start, end = edge["input"], edge["output"]
            if reverse:
                start, end = end, start
            graph.setdefault(start, []).append(end)
    found, todo = set(), [version_id]
    while todo:
        key = todo.pop()
        if key not in found:
            found.add(key)
            todo.extend(graph.get(key, []))
    return sorted(found)


def impact(snapshot, version_ids):
    """Return dependent IDs requiring revalidation without rewriting signed history.

    Args: snapshot is the graph; version_ids identifies changed inputs.
    Raises: CommercialError for unknown versions or malformed graphs.
    """
    affected = set()
    for key in version_ids:
        affected.update(trace(snapshot, key))
    return {"stale_versions": sorted(affected), "historical_snapshots_mutated": False}


def validate_discovery(cells):
    """Require all 36 owned, reviewed discovery cells; return True or raise CommercialError."""
    expected = {(layer, q) for layer in LAYERS for q in QUESTIONS}
    actual = set()
    for cell in cells:
        key = (cell.get("layer"), cell.get("question"))
        _require(key in expected and key not in actual, "invalid or duplicate discovery cell")
        _require(cell.get("owner") and cell.get("review_id"), "unowned/unreviewed discovery")
        _require(bool(cell.get("answer")) != bool(cell.get("na_reason")), "answer or justified N/A required")
        actual.add(key)
    _require(actual == expected, "incomplete 6x6 discovery")
    return True


def transition(state, decision, actor, target=None, snapshot=None):
    """Return new lifecycle state; reject unowned gates and bounded iteration overrun.

    State includes phase, owner, criteria, blockers, rework and reformulations.
    This function cannot authorize scope changes or execute a human authority act.
    """
    result = copy.deepcopy(state)
    _require(actor == state.get("owner"), "gate owner required")
    _require(state.get("phase") in PHASES, "unknown phase")
    _require(decision in {"proceed", "hold", "rework", "stop", "reformulate"}, "unknown decision")
    _require(not state.get("outside_authority"), "human authority escalation required")
    if decision == "proceed":
        _require(snapshot is not None, "gate requires exact input snapshot, not declared criteria")
        gate = commercial_gate(snapshot, state["phase"])
        _require(gate["complete"] and not state.get("blockers"), "gate incomplete: " + "; ".join(gate["blockers"]))
        pos = PHASES.index(state["phase"])
        _require(pos + 1 < len(PHASES) and target == PHASES[pos + 1], "nonadjacent lifecycle transition")
        result["phase"] = target
    if decision in {"rework", "reformulate"}:
        field, limit = ("rework", 3) if decision == "rework" else ("reformulations", 2)
        _require(state.get(field, 0) < limit, "iteration budget exhausted: escalate adjacent layer")
        if decision == "reformulate":
            _require(target and target not in state.get("formulations", []), "repeated formulation")
            result.setdefault("formulations", []).append(target)
        result[field] = state.get(field, 0) + 1
    result["decision"] = decision
    return result


def commercial_gate(snapshot, phase):
    """Derive phase completeness from exact entity records and economic calculators.

    Args: snapshot is canonical input; phase is the lifecycle phase being left.
    Returns: complete/blockers/calculations. A complete gate is not legal approval.
    Declared state.criteria booleans cannot replace required records or quantities.
    """
    validate_snapshot(snapshot)
    snapshot = current_view(snapshot)
    _require(phase in PHASES, "unknown phase")
    requirements = {
        "qualification": {"Need": ("business_need", "stakeholder", "funding_ref", "procurement_constraints", "mandate_ref")},
        "discovery": {"Attribute": ("unit", "baseline", "target", "measurement", "horizon"), "Requirement": ("acceptance", "scope")},
        "options": {"WorkPackage": ("deliverable", "acceptance", "dependencies"), "Estimate": ("economic_input",)},
        "bid-review": {"Price": ("economic_input",), "RoleAllocation": ("capacity_input",), "Reserve": ("risk_id", "amount", "decision_ref")},
        "negotiation": {"Baseline": ("terms_input", "scope_versions", "price_version", "human_decision_ref")},
        "mobilization": {"RoleAllocation": ("capacity_input", "access_evidence", "availability_evidence")},
        "delivery": {"Forecast": ("forecast_input", "stage_acceptance", "deviation_owner")},
        "acceptance": {"Actual": ("accepted_output", "client_acceptance_ref")},
        "operations": {"RoleAllocation": ("service_input", "roster_evidence", "sla_review_ref")},
        "renewal": {"Forecast": ("forecast_input", "renewal_decision_ref")},
        "exit": {"Actual": ("data_return_evidence", "continuity_evidence", "settlement_ref")}}
    blockers, calculations = [], []
    for kind, fields in requirements[phase].items():
        records = [e for e in snapshot["entities"] if e["type"] == kind]
        if not records:
            blockers.append("missing " + kind)
        for record in records:
            for field in fields:
                if field not in record["data"] or record["data"][field] is None or record["data"][field] == "":
                    blockers.append(record["version_id"] + ": missing " + field)
    if phase == "discovery":
        try:
            validate_discovery(snapshot.get("discovery", []))
        except CommercialError as exc:
            blockers.append(str(exc))
    path = Path(__file__).with_name("commercial_economics.py")
    spec = importlib.util.spec_from_file_location("commercial_economics", path)
    economics = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(economics)
    calculators = {"economic_input": {"Estimate": economics.validate_estimate, "Price": economics.price_quote}, "capacity_input": {"RoleAllocation": economics.capacity_plan}, "service_input": {"RoleAllocation": economics.service_sizing}, "forecast_input": {"Forecast": economics.forecast}, "terms_input": {"Baseline": economics.validate_terms}}
    for entity in snapshot["entities"]:
        for field, functions in calculators.items():
            if field in entity["data"] and entity["type"] in functions:
                try:
                    result = functions[entity["type"]](entity["data"][field])
                    calculations.append({"version_id": entity["version_id"], "result": result})
                    for problem in result.get("blockers", []):
                        blockers.append(entity["version_id"] + ": " + str(problem))
                    if result.get("margin_target_met") is False or result.get("feasible") is False:
                        blockers.append(entity["version_id"] + ": commercial/capacity threshold failed")
                except (ValueError, KeyError, TypeError) as exc:
                    blockers.append(entity["version_id"] + ": " + str(exc))
    return {"complete": not blockers, "blockers": blockers, "calculations": calculations, "authority_granted": False, "snapshot_digest": digest(snapshot)}


def _time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def readiness(snapshot, now=None, identity_verifier=None, fabric_resolver=None, enforcement_verifier=None):
    """Return blockers for each commitment; never infer truth from file existence.

    Args: now is an aware datetime; identity_verifier is a trusted dispatcher-owned
        callback returning {principal, subject_digest} for a verified signed attestation.
        subject_digest binds the entity excluding its own attestation field; both
        maker and checker must be authenticated and distinct.
        fabric_resolver verifies ledger-backed exact bindings. enforcement_verifier
        authenticates host evidence for each control; snapshot strings never suffice.
    A callback must be injected by the host, never loaded from snapshot data.
    """
    validate_snapshot(snapshot)
    now = now or datetime.now(timezone.utc)
    blockers = []
    try:
        snapshot = current_view(snapshot, require_publications=True)
    except CommercialError as exc:
        blockers.append(str(exc))
    index = _index(snapshot)
    if not any(e["type"] == "Claim" for e in index.values()):
        blockers.append("no scoped claims; readiness cannot be established")
    if not any(e["type"] == "ExecutionContract" for e in index.values()):
        blockers.append("missing execution chain")
    for key, entity in index.items():
        data = entity["data"]
        if entity["type"] == "Source":
            required = {"content", "content_digest", "author", "licence", "valid_until", "reuse_allowed"}
            if not required <= data.keys() or not data.get("reuse_allowed"):
                blockers.append(f"{key}: source availability/licence incomplete")
            elif hashlib.sha256(data["content"].encode()).hexdigest() != data["content_digest"] or _time(data["valid_until"]) <= now:
                blockers.append(f"{key}: source corrupt or expired")
        if entity["type"] == "Passage":
            source = index.get(data.get("source_version"), {})
            sd = source.get("data", {})
            if source.get("type") != "Source" or not data.get("text") or data.get("text") not in sd.get("content", "") or not data.get("locator") or data.get("digest") != hashlib.sha256(data.get("text", "").encode()).hexdigest():
                blockers.append(f"{key}: unsupported passage")
            elif data["source_version"] not in trace(snapshot, key, True):
                blockers.append(f"{key}: missing source dependency")
        if entity["type"] == "Claim":
            passages = data.get("supporting_passages", [])
            ancestors = trace(snapshot, key, True)
            if not passages or any(p not in ancestors or index.get(p, {}).get("type") != "Passage" for p in passages):
                blockers.append(f"{key}: ungrounded commitment")
            if data.get("evidence_status") != "independently_verified" or not data.get("applicability") or data.get("contradicting_passages"):
                blockers.append(f"{key}: unsupported/disputed claim")
            review = index.get(data.get("support_review"), {})
            rd = review.get("data", {})
            principal = identity_verifier(rd.get("attestation")) if identity_verifier else None
            producer = identity_verifier(data.get("producer_attestation")) if identity_verifier else None
            review_payload = copy.deepcopy(review)
            review_payload.get("data", {}).pop("attestation", None)
            producer_payload = copy.deepcopy(entity)
            producer_payload["data"].pop("producer_attestation", None)
            authenticated = isinstance(principal, dict) and isinstance(producer, dict) and principal.get("principal") and producer.get("principal") and principal.get("subject_digest") == digest(review_payload) and producer.get("subject_digest") == digest(producer_payload)
            distinct = authenticated and principal["principal"] != producer["principal"]
            if review.get("type") != "Review" or rd.get("reviewed_version") != key or rd.get("reviewed_digest") != digest(entity) or not distinct or rd.get("conclusion") != "accepted" or rd.get("blocking_findings"):
                blockers.append(f"{key}: independent authenticated support review required")
        if entity["type"] == "ExecutionContract":
            if data.get("layer") not in range(1, 7) or not data.get("claim_ids") or not data.get("domain_contract_version") or not data.get("fragment_ids"):
                blockers.append(f"{key}: incomplete domain/fabric binding")
            else:
                references = [(data["domain_contract_version"], "DomainContract")] + [(ref, "Claim") for ref in data["claim_ids"]] + [(ref, "Fragment") for ref in data["fragment_ids"]]
                if any(index.get(ref, {}).get("type") != kind for ref, kind in references):
                    blockers.append(f"{key}: unresolved typed binding")
                if not fabric_resolver or not fabric_resolver(entity, snapshot):
                    blockers.append(f"{key}: actual Fabric binding unverified")
    enforcement = snapshot.get("enforcement", {})
    for control in ("identity", "tool_permissions", "mount_isolation", "context_isolation"):
        if not enforcement_verifier or not enforcement_verifier(control, enforcement.get(control)):
            blockers.append(f"enforcement: {control} unverified")
    layers = {e["data"].get("layer") for e in index.values() if e["type"] == "ExecutionContract"}
    if layers != set(range(1, 7)):
        blockers.append("incomplete L1–L6 execution chain")
    if identity_verifier is None:
        blockers.append("enforcement: trusted identity verifier unavailable")
    for required_type in ("Source", "Passage", "Need", "Attribute", "Requirement", "DomainContract", "Fragment", "WorkPackage", "Estimate", "RoleAllocation", "Rate", "Cost", "Price", "Reserve", "Baseline", "Forecast", "Publication"):
        if not any(e["type"] == required_type for e in index.values()):
            blockers.append(f"missing required chain type: {required_type}")
    commitments = [k for k, e in index.items() if e["type"] == "Claim"]
    publications = [k for k, e in index.items() if e["type"] == "Publication"]
    chain_types = {"Source", "Passage", "Claim", "Need", "Attribute", "Requirement", "DomainContract", "ExecutionContract", "Fragment", "WorkPackage", "Estimate", "RoleAllocation", "Rate", "Cost", "Reserve", "Price", "Baseline", "Forecast"}
    for pub in publications:
        closure = trace(snapshot, pub, True)
        if not set(commitments) <= set(closure) or not chain_types <= {index[k]["type"] for k in closure}:
            blockers.append(f"{pub}: incomplete dependency closure")
        contracts = [e for k, e in index.items() if k in closure and e["type"] == "ExecutionContract"]
        for contract in contracts:
            level = contract["data"].get("layer")
            if level and level > 1 and not any(edge["type"] in FORWARD and edge["output"] == contract["version_id"] and index[edge["input"]]["type"] == "ExecutionContract" and index[edge["input"]]["data"].get("layer") == level - 1 for edge in snapshot["relations"]):
                blockers.append(f"{contract['version_id']}: missing adjacent execution dependency")
    if not enforcement_verifier or not enforcement_verifier("operational_recovery", snapshot.get("operational_recovery")):
        blockers.append("operational recovery/retention/legal-hold controls require external deployment qualification")
    return {"ready": not blockers, "blockers": blockers, "authority_granted": False}


def project(snapshot, audience, policy):
    """Produce an allowlisted JSON projection, or reject mandatory disclosure conflict.

    Policy selects fields by entity type and must enumerate surfaces and allowed
    derived combinations. Only this prepared projection may reach an exporter.
    Internal output preserves the whole graph; output confers no release approval.
    """
    validate_snapshot(snapshot)
    _require(audience in {"internal", "client"}, "unknown audience")
    if audience == "internal":
        return copy.deepcopy(snapshot)
    _require(policy.get("version") and MANDATORY <= set(policy.get("mandatory_disclosure", [])), "missing mandatory disclosure policy")
    _require(policy.get("surfaces") == ["json-payload"], "unsupported export surface")
    original_digest = digest(snapshot)
    snapshot = current_view(snapshot, require_publications=True, audience="client")
    fields = policy.get("fields", {})
    result, disclosed = [], set()
    for entity in snapshot["entities"]:
        data = {}
        for field in fields.get(entity["type"], []):
            if field in entity["data"]:
                label = entity["data"].get("field_classification", {}).get(field, entity["classification"])
                _require(label in {"public", "client-contract"} or field in policy.get("open_book_fields", []) and policy.get("legal_decision_ref"), "classified field disclosure blocked")
                _require(isinstance(entity["data"][field], (str, int, bool)) or entity["data"][field] is None, "nested/non-scalar export requires reviewed recursive schema")
                data[field] = entity["data"][field]
                disclosed.add(field)
        if data:
            result.append({"id": entity["id"], "type": entity["type"], "data": data})
    _require(MANDATORY <= disclosed, "mandatory contractual disclosures absent")
    combinations = policy.get("forbidden_combinations", [["effort", "cost_rate"], ["cost", "price"]])
    _require(not any(set(combo) <= disclosed for combo in combinations), "inference disclosure conflict")
    return {"audience": "client", "snapshot_digest": original_digest, "policy_version": policy["version"], "entities": result}


def recovery_check(archive, now=None, access_probe=None, elapsed_seconds=0, content_verifier=None):
    """Validate archive closure, measured RPO/RTO, availability and owner policy.

    Args: archive is the full portable envelope; now is aware UTC; access_probe is
        trusted host code testing actual destination/decrypt access for every blob;
        elapsed_seconds is measured by the restoring store, not archive metadata.
        content_verifier independently checks semantic contents against the graph
        for each attachment kind; labels and hashes alone never establish closure.
    Returns: report with verified and blockers. No authority or release is implied.
    """
    now = now or datetime.now(timezone.utc)
    blockers = []
    snapshot = archive.get("snapshot", {})
    try:
        validate_snapshot(snapshot)
    except (CommercialError, KeyError, TypeError) as exc:
        return {"verified": False, "blockers": [str(exc)]}
    policy = archive.get("recovery_policy", {})
    required = {"owner", "data_owner", "security_owner", "legal_owner", "rpo_seconds", "rto_seconds", "retain_until", "jurisdiction", "access_profile"}
    if not required <= policy.keys() or any(not policy.get(k) for k in required - {"rpo_seconds", "rto_seconds"}):
        blockers.append("incomplete owner recovery/retention policy")
    try:
        age = (now - _time(archive["created_at"])).total_seconds()
        watermark_age = (now - _time(snapshot["captured_at"])).total_seconds()
        if not math.isfinite(float(policy["rpo_seconds"])) or watermark_age < 0 or watermark_age > float(policy["rpo_seconds"]) or age < 0 or age > float(policy["rpo_seconds"]) or float(policy["rpo_seconds"]) < 0:
            blockers.append("backup outside approved RPO")
        if not math.isfinite(float(policy["rto_seconds"])) or not math.isfinite(float(elapsed_seconds)) or elapsed_seconds < 0 or elapsed_seconds > float(policy["rto_seconds"]) or float(policy["rto_seconds"]) < 0:
            blockers.append("restore outside approved RTO")
        if _time(policy["retain_until"]) <= now:
            blockers.append("retention window expired; legal owner disposition required")
    except (KeyError, TypeError, ValueError):
        blockers.append("invalid recovery timing policy")
    required_kinds = {"fabric", "formulas", "internal-projection", "client-projection", "reviews"}
    kinds = set()
    blobs = archive.get("blobs", {})
    for attachment in snapshot.get("attachments", []):
        sha = attachment.get("digest")
        kinds.add(attachment.get("kind"))
        try:
            raw = base64.b64decode(blobs[sha], validate=True)
            if hashlib.sha256(raw).hexdigest() != sha:
                blockers.append("corrupt recovery blob")
            if not content_verifier or not content_verifier(attachment, raw, snapshot):
                blockers.append("attachment semantic closure unverified")
            if not access_probe or not access_probe(attachment, raw, policy):
                blockers.append("attachment unavailable or decrypt/access denied")
        except (KeyError, TypeError, ValueError):
            blockers.append("missing or malformed recovery blob")
    if not required_kinds <= kinds:
        blockers.append("missing Fabric/formulas/reviews/dual-projection archive closure")
    entities = _index(snapshot)
    for entity in entities.values():
        data = entity["data"]
        if entity["type"] == "Source":
            text = data.get("content")
            if not isinstance(text, str) or hashlib.sha256(text.encode()).hexdigest() != data.get("content_digest") or not data.get("reuse_allowed"):
                blockers.append("source content unavailable/corrupt or archive licence absent")
        if entity["type"] == "Passage" and entities.get(data.get("source_version"), {}).get("type") != "Source":
            blockers.append("missing Source in recovery closure")
    return {"verified": not blockers, "blockers": blockers, "elapsed_seconds": elapsed_seconds}


class SnapshotStore:
    """Single-filesystem immutable generations with a locked atomic visibility barrier.

    The containing directory must be access-controlled by the trusted host. The
    lock is advisory between cooperating writers, not a sandbox/security boundary.
    """

    def __init__(self, path):
        """Create a store directory at path; filesystem errors propagate."""
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

    def read(self):
        """Return the complete current revision/snapshot; reject damaged stored bytes."""
        pointer = self.path / "current.json"
        if not pointer.exists():
            return {"revision": 0, "snapshot": None}
        manifest = json.loads(pointer.read_text())
        _require(Path(manifest["file"]).name == manifest["file"], "unsafe manifest path")
        snapshot = json.loads((self.path / manifest["file"]).read_text())
        _require(digest(snapshot) == manifest["digest"], "snapshot integrity failure")
        validate_snapshot(snapshot)
        return {"revision": manifest["revision"], "snapshot": snapshot}

    def commit(self, snapshot, expected_revision, before_commit=None):
        """Commit validated graph using expected_revision CAS; return new revision.

        before_commit is a testable crash hook after durable staging. Exceptions
        leave the prior current generation visible; no historical file is changed.
        """
        candidate = copy.deepcopy(snapshot)
        validate_snapshot(candidate)
        for attachment in candidate.get("attachments", []):
            sha = attachment.get("digest", "")
            _require(len(sha) == 64 and all(c in "0123456789abcdef" for c in sha), "invalid attachment digest")
            blob = self.path / ("blob-" + sha + ".json")
            _require(blob.is_file(), "missing attachment blob")
            raw = base64.b64decode(json.loads(blob.read_text())["base64"], validate=True)
            _require(hashlib.sha256(raw).hexdigest() == sha, "corrupt attachment blob")
        with (self.path / "writer.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            current = self.read()
            _require(current["revision"] == expected_revision, "revision conflict; recompute and re-review")
            if current["snapshot"]:
                prior = _index(current["snapshot"])
                fresh = _index(candidate)
                _require(set(prior) <= set(fresh), "historical versions cannot disappear")
                _require(all(prior[k] == fresh[k] for k in prior), "immutable version modified")
                old_edges = {digest(e) for e in current["snapshot"].get("relations", [])}
                _require(old_edges <= {digest(e) for e in candidate.get("relations", [])}, "historical relation removed")
                old_blobs = {digest(e) for e in current["snapshot"].get("attachments", [])}
                _require(old_blobs <= {digest(e) for e in candidate.get("attachments", [])}, "historical attachment removed")
            revision = expected_revision + 1
            name = f"generation-{revision}-{digest(candidate)}.json"
            self._write(self.path / name, candidate)
            if before_commit:
                before_commit()
            self._write(self.path / "current.json", {"revision": revision, "file": name, "digest": digest(candidate)})
            return revision

    def _write(self, target, value):
        fd, temporary = tempfile.mkstemp(prefix="staged-", dir=self.path)
        try:
            with os.fdopen(fd, "w") as handle:
                json.dump(value, handle, sort_keys=True, ensure_ascii=False, allow_nan=False)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, target)
            directory = os.open(self.path, os.O_DIRECTORY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def put_blob(self, content):
        """Durably store bytes by SHA256; return digest. Access is inherited from store."""
        _require(isinstance(content, bytes), "blob content must be bytes")
        sha = hashlib.sha256(content).hexdigest()
        self._write(self.path / ("blob-" + sha + ".json"), {"base64": base64.b64encode(content).decode("ascii")})
        return sha

    def purge_blob(self, sha, now=None):
        """Reject purge under legal hold/retention or any current historical reference.

        This intentionally conservative local store never destroys referenced
        provenance. External retention disposition remains a human-controlled act.
        """
        _require(len(sha) == 64 and all(c in "0123456789abcdef" for c in sha), "invalid blob digest")
        current = self.read()["snapshot"] or {}
        policy = current.get("recovery_policy", {})
        now = now or datetime.now(timezone.utc)
        _require(not policy.get("legal_hold"), "legal hold prohibits purge")
        _require(policy.get("retain_until") and _time(policy["retain_until"]) <= now, "retention prohibits purge")
        _require(not any(a.get("digest") == sha for a in current.get("attachments", [])), "referenced provenance cannot be purged")
        (self.path / ("blob-" + sha + ".json")).unlink()
        return True

    def archive(self, target, now=None):
        """Write full current closure to target with digest; return archive manifest.

        This archive is plaintext and requires separately managed access controls;
        it does not assert legal retention, encryption, RPO or RTO compliance.
        """
        current = self.read()
        _require(current["snapshot"] is not None, "empty store")
        blobs = {}
        for attachment in current["snapshot"].get("attachments", []):
            sha = attachment["digest"]
            _require(len(sha) == 64 and all(c in "0123456789abcdef" for c in sha), "invalid attachment digest")
            payload = json.loads((self.path / ("blob-" + sha + ".json")).read_text())["base64"]
            _require(hashlib.sha256(base64.b64decode(payload, validate=True)).hexdigest() == sha, "corrupt archive attachment")
            blobs[sha] = payload
        archive = {"format": PROFILE, "revision": current["revision"], "snapshot": current["snapshot"], "digest": digest(current["snapshot"]), "blobs": blobs, "created_at": (now or datetime.now(timezone.utc)).isoformat(), "recovery_policy": current["snapshot"].get("recovery_policy", {})}
        Path(target).write_text(json.dumps(archive, sort_keys=True, ensure_ascii=False))
        return {"digest": archive["digest"], "revision": archive["revision"]}

    def restore(self, archive_path, expected_revision=0, recovery_verifier=None, access_probe=None, now=None, content_verifier=None):
        """Restore exact graph from an integrity-checked archive into an empty store.

        Raises CommercialError for nonempty destinations, corruption or stale CAS.
        Returns a report separating exact model restoration from operational recovery.
        recovery_verifier is a trusted host callback that independently verifies
        source/Fabric/formula/publication closure, key access and owner-set RPO/RTO.
        Without it operational_recovery_verified is always False.
        """
        started = time.monotonic()
        archive = json.loads(Path(archive_path).read_text())
        _require(archive.get("format") == PROFILE and digest(archive["snapshot"]) == archive["digest"], "archive integrity failure")
        _require(expected_revision == 0 and self.read()["revision"] == 0, "restore requires empty destination")
        for sha, payload in archive.get("blobs", {}).items():
            raw = base64.b64decode(payload, validate=True)
            _require(hashlib.sha256(raw).hexdigest() == sha, "restore blob integrity failure")
            self.put_blob(raw)
        revision = self.commit(archive["snapshot"], 0)
        report = recovery_check(archive, now=now, access_probe=access_probe, elapsed_seconds=time.monotonic() - started, content_verifier=content_verifier)
        qualification = report["verified"] and recovery_verifier is not None and recovery_verifier(archive, self.read()["snapshot"]) is True
        return {"revision": revision, "model_integrity_restored": True, "operational_recovery_verified": qualification is True, "blockers": [] if qualification is True else report["blockers"] + ["trusted deployment recovery qualification required"]}


def main(argv=None):
    """Run read-only check/impact/trace commands; return 0 on success or 2 on rejection."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "readiness", "impact", "trace"])
    parser.add_argument("snapshot")
    parser.add_argument("versions", nargs="*")
    args = parser.parse_args(argv)
    try:
        snapshot = json.loads(Path(args.snapshot).read_text())
        if args.command == "check":
            result = {"valid": validate_snapshot(snapshot)}
        elif args.command == "readiness":
            result = readiness(snapshot)
        elif args.command == "impact":
            result = impact(snapshot, args.versions)
        else:
            _require(len(args.versions) == 1, "trace requires one version")
            result = trace(snapshot, args.versions[0], reverse=True)
        print(json.dumps(result, indent=2))
        return 2 if isinstance(result, dict) and result.get("ready") is False else 0
    except (CommercialError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
