#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Explicit canonical engagement activation and independent C3 assurance axes.

Host callbacks authenticate receipts against externally configured trust. No
function issues human authority or changes installed provider policy.
"""
from __future__ import annotations

import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import tempfile

PROFILE = "commercial-delivery/1"
AXES = {
    "domain_validity": ("unknown", {"valid", "invalid", "stale"}),
    "evidence_verification": ("unverified", {"verified", "failed", "stale"}),
    "independent_review": ("pending", {"accepted", "constrained", "rejected", "stale"}),
    "snapshot_approval": ("unapproved", {"approved", "stale"}),
    "authority_authorisation": ("absent", {"granted", "revoked"}),
    "contractual_acceptance": ("not_offered", {"pending", "accepted", "disputed", "rejected"}),
}
ROLES = dict(zip(AXES, ("domain-validator", "evidence-validator", "reviewer", "approver", "human-authority", "contract-signatory")))


class LifecycleError(ValueError):
    """A migration or assurance contract failed before current state changed."""


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def _require(condition, message):
    if not condition:
        raise LifecycleError(message)


def _validate(engagement):
    import jsonschema
    from referencing import Registry, Resource
    from referencing.exceptions import NoSuchResource, Unresolvable

    schema_path = Path(__file__).resolve().parents[1] / "schema/26.10.4/jai-object.schema.json"
    schema = json.loads(schema_path.read_text())
    binding_path = schema_path.parent / "jai-layer-binding.schema.json"
    binding = json.loads(binding_path.read_text())

    def reject_unregistered(uri):
        raise NoSuchResource(ref=uri)

    # Explicit retrieval prevents validator defaults from fetching untrusted refs.
    registry = Registry(retrieve=reject_unregistered)
    for path, document in ((schema_path, schema), (binding_path, binding)):
        resource = Resource.from_contents(document)
        registry = registry.with_resources(((document["$id"], resource), (path.as_uri(), resource)))
    validator_type = jsonschema.validators.validator_for(schema)
    validator_type.check_schema(schema)
    validator = validator_type(schema, registry=registry)
    _require(engagement.get("schema_version") == "26.10.4", "unsupported engagement schema")
    _require(bool(engagement.get("id")), "engagement identity required")
    objects = engagement.get("objects", [])
    ids = []
    for obj in objects:
        try:
            validator.validate(obj)
        except Unresolvable as error:
            raise LifecycleError("unknown offline schema reference: " + error.ref) from error
        _require(not obj.get("canonical_ref") or obj["canonical_ref"] == obj["id"], "ambiguous canonical mapping")
        ids.append(obj["id"])
    _require(len(ids) == len(set(ids)), "duplicate canonical identity")
    _require(set(engagement.get("membership_ids", {})) == set(ids), "missing or foreign membership")
    _require(all(isinstance(v, list) and v and len(set(v)) == len(v) for v in engagement["membership_ids"].values()), "invalid membership")
    _require(len(set(engagement.get("profiles", []))) == len(engagement.get("profiles", [])), "duplicate profile")


def activate(engagement, scope_receipt, verifier, policy_digest):
    """Return an activation bundle without mutating canonical engagement objects.

    Args:
        engagement: Existing 26.10.4 engagement, canonical JAIObject objects,
            membership_ids keyed by canonical ID, and profile names.
        scope_receipt: Human scope-change receipt bound to original digest.
        verifier: Trusted host callable(receipt), returning authenticated principal
            and roles; never selected from engagement content.
        policy_digest: Current trusted configuration digest.
    Returns:
        Original/candidate engagements, exact identity crosswalk and receipt.
    Raises:
        LifecycleError: Invalid version, identities, scope, membership or an
            unregistered schema reference. Schema validation is offline only.
        jsonschema.ValidationError: Invalid existing canonical JAIObject.
    """
    _validate(engagement)
    _require(PROFILE not in engagement.get("profiles", []), "profile already active")
    expected = {"kind": "scope-change", "engagement_id": engagement["id"], "original_digest": _digest(engagement), "profile": PROFILE, "policy_digest": policy_digest}
    _authenticate(scope_receipt, verifier, expected, "engagement-owner", human=True)
    candidate = copy.deepcopy(engagement)
    candidate.setdefault("profiles", []).append(PROFILE)
    crosswalk = [{"source_system": "jai", "source_schema_version": "26.10.4", "source_id": obj["id"], "source_version": obj["version"], "canonical_id": obj["id"], "canonical_version": obj["version"], "original_membership_ids": engagement["membership_ids"][obj["id"]], "membership_ids": candidate["membership_ids"][obj["id"]], "profile_extensions": [PROFILE], "mapping_state": "exact"} for obj in engagement["objects"]]
    bundle = {"original": copy.deepcopy(engagement), "candidate": candidate, "crosswalk": crosswalk, "scope_receipt": copy.deepcopy(scope_receipt), "profile_version": PROFILE, "original_digest": _digest(engagement), "candidate_digest": _digest(candidate)}
    bundle["activation_digest"] = _digest(bundle)
    return bundle


def _authenticate(receipt, verifier, expected, role, human=False):
    _require(callable(verifier), "trusted host verifier required")
    _require(all(receipt.get(k) == v for k, v in expected.items()), "receipt binding mismatch")
    identity = verifier(copy.deepcopy(receipt))
    _require(isinstance(identity, dict) and identity.get("principal") and role in identity.get("roles", []), "unauthenticated or unauthorized receipt")
    _require(receipt.get("principal") == identity["principal"], "forged principal")
    if human:
        _require(identity.get("human") is True, "human-supplied authenticated receipt required")
    return identity


def assess_axes(manifest, receipts, verifier, policy_digest, makers):
    """Return six independent statuses and commitment gate from authenticated receipts.

    Args:
        manifest: Exact snapshot manifest being assessed.
        receipts: At most one receipt per axis, including signed status and bindings.
        verifier: Trusted host authentication callback, independent of manifest.
        policy_digest: Trusted current policy hash, invalidating older receipts.
        makers: Host-authenticated producer principal IDs, never snapshot claims.
    Returns:
        Axis states, authenticated receipt IDs, and commitment_ready boolean.
    Raises:
        LifecycleError: Forged, duplicate, unauthorized or incomplete review receipts.
    """
    states = {axis: default for axis, (default, _) in AXES.items()}
    ids = {}
    _require(bool(makers) and len(set(makers)) == len(makers), "trusted producer identity set required")
    for receipt in receipts:
        axis = receipt.get("axis")
        _require(axis in AXES and axis not in ids, "unknown or duplicate axis")
        identity = _authenticate(receipt, verifier, {"kind": "assurance-axis", "axis": axis}, ROLES[axis], human=axis in {"authority_authorisation", "contractual_acceptance"})
        _require(receipt.get("id") and receipt.get("status") in AXES[axis][1], "invalid axis receipt")
        ids[axis] = receipt["id"]
        if receipt.get("manifest_digest") != _digest(manifest) or receipt.get("policy_digest") != policy_digest:
            states[axis] = "stale" if axis not in {"authority_authorisation", "contractual_acceptance"} else AXES[axis][0]
            continue
        if axis in {"independent_review", "snapshot_approval"}:
            _require(identity["principal"] not in makers, "maker cannot review or approve own work")
        if axis == "independent_review" and receipt["status"] in {"accepted", "constrained"}:
            _require(receipt.get("covered_refs") == sorted(manifest.get("commitment_refs", [])) and bool(manifest.get("commitment_refs")), "review coverage incomplete")
            _require(receipt.get("blocking_findings") == [] and receipt.get("constraints_satisfied") is True, "unresolved review findings or constraints")
        states[axis] = receipt["status"]
    approvals = [r for r in receipts if r.get("axis") == "snapshot_approval" and states["snapshot_approval"] == "approved"]
    for approval in approvals:
        _require(states["independent_review"] == "accepted" and approval.get("review_id") == ids.get("independent_review"), "approval lacks current exact review")
    ready = all(states[k] == v for k, v in zip(AXES, ("valid", "verified", "accepted", "approved", "granted", "accepted")))
    return {"axes": states, "receipt_ids": ids, "commitment_ready": ready}


def approve_snapshot(manifest, receipts, approval_receipt, verifier, policy_digest, makers):
    """Validate supplied exact approval and return copied receipts; never sign an act.

    Args: manifest, receipts, verifier, policy_digest and makers follow assess_axes;
        approval_receipt is an externally authenticated approver receipt.
    Returns: Copied receipt list with independently validated approval appended.
    Raises: LifecycleError when approval is stale, forged or lacks accepted review.
    """
    _require(approval_receipt.get("axis") == "snapshot_approval", "approval receipt required")
    candidate = copy.deepcopy(receipts) + [copy.deepcopy(approval_receipt)]
    result = assess_axes(manifest, candidate, verifier, policy_digest, makers)
    _require(result["axes"]["snapshot_approval"] == "approved", "approval is not current")
    return candidate


class EngagementStore:
    """Atomic CAS current engagement plus immutable activation/rollback history.

    Directory access is a trusted host responsibility. Locking coordinates local
    cooperating writers and is not a security sandbox.
    """

    def __init__(self, path):
        """Create store directory at path; OS errors propagate."""
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

    def read(self):
        """Return current generation or revision zero; reject corrupt current data."""
        pointer = self.path / "current.json"
        if not pointer.exists():
            return {"revision": 0, "engagement": None, "history": []}
        value = json.loads(pointer.read_text())
        _require(value.pop("digest") == _digest(value), "current state digest mismatch")
        return value

    def commit(self, engagement, expected_revision, event=None, _before_pointer=None):
        """Atomically persist valid engagement and append event using revision CAS.

        Args: engagement is canonical source state; expected_revision is last read;
            event is an immutable history record, never a replacement of history.
            _before_pointer is a private deterministic crash-injection callback.
        Returns: New monotonically increasing revision.
        Raises: LifecycleError on conflicts, invalid state or historical alteration.
        """
        _validate(engagement)
        with (self.path / "writer.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            current = self.read()
            _require(current["revision"] == expected_revision, "revision conflict")
            value = {"revision": expected_revision + 1, "engagement": copy.deepcopy(engagement), "history": current["history"] + ([copy.deepcopy(event)] if event else [])}
            value["digest"] = _digest(value)
            generation = self.path / ("generation-" + str(value["revision"]) + "-" + value["digest"] + ".json")
            encoded = json.dumps(value, sort_keys=True)
            if generation.exists():
                _require(generation.read_text() == encoded, "immutable generation collision")
            else:
                with generation.open("x") as stream:
                    stream.write(encoded)
                    stream.flush()
                    os.fsync(stream.fileno())
            if _before_pointer is not None:
                _before_pointer()
            fd, name = tempfile.mkstemp(dir=self.path, prefix="pointer-")
            with os.fdopen(fd, "w") as stream:
                json.dump(value, stream, sort_keys=True)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, self.path / "current.json")
            directory = os.open(self.path, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
            return value["revision"]

    def activate(self, bundle, expected_revision, verifier, policy_digest):
        """Commit an intact activation bundle against unchanged original engagement.

        Returns: New revision. Raises LifecycleError for tampering or stale source.
        verifier and policy_digest authenticate the original owner scope receipt again.
        """
        rebuilt = activate(bundle["original"], bundle["scope_receipt"], verifier, policy_digest)
        _require(rebuilt == bundle, "activation bundle is not exact authenticated migration")
        body = {k: v for k, v in bundle.items() if k != "activation_digest"}
        _require(_digest(body) == bundle.get("activation_digest"), "activation receipt changed")
        _require(_digest(bundle["original"]) == bundle["original_digest"] and _digest(bundle["candidate"]) == bundle["candidate_digest"], "activation state changed")
        _require(self.read()["engagement"] == bundle["original"], "original engagement changed")
        return self.commit(bundle["candidate"], expected_revision, {"kind": "activation", "bundle": bundle})

    def rollback(self, activation_digest, expected_revision):
        """Restore exact preactivation engagement while retaining all history.

        Rollback rejects postactivation canonical changes and concurrent writers.
        It does not remove signed acts or imply cancellation of contractual duties.
        Returns: New revision. Raises LifecycleError on stale/missing activation.
        """
        current = self.read()
        matches = [e["bundle"] for e in current["history"] if e.get("kind") == "activation" and e["bundle"].get("activation_digest") == activation_digest]
        _require(len(matches) == 1, "activation not unique or absent")
        bundle = matches[0]
        body = {k: v for k, v in bundle.items() if k != "activation_digest"}
        _require(_digest(body) == activation_digest, "historical activation digest mismatch")
        _require(_digest(bundle["original"]) == bundle["original_digest"] and _digest(bundle["candidate"]) == bundle["candidate_digest"], "historical activation bytes changed")
        _validate(bundle["original"])
        _require(current["engagement"] == bundle["candidate"], "postactivation changes require explicit reconciliation")
        return self.commit(bundle["original"], expected_revision, {"kind": "rollback", "activation_digest": activation_digest})
