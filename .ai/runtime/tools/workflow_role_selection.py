# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Evaluate compatible producer roles against a pinned workflow handoff.

The caller supplies the validated workflow catalogue, immutable role snapshot,
and authorized review and deployment evidence. This module never creates a
receiving assignment, approves a mapping, or grants execution authority.
"""
from __future__ import annotations

from content_spec import canonical_hash


PROTOCOL = "jai.workflow-role-requirements/1"
_AUTHORITY_ROLES = frozenset({"engagement:named-authority", "engagement:named-acceptance-authority"})
_ENDPOINTS = {"producer": "producer_role", "receiver": "receiving_role"}


def _fields(record, keys):
    if not isinstance(record, dict) or set(record) != set(keys.split()):
        raise ValueError("WORKFLOW_ROLE_SCHEMA")


def _binding(catalogue, handoff, path, endpoint):
    if endpoint not in _ENDPOINTS:
        raise ValueError("WORKFLOW_ROLE_ENDPOINT")
    row = next((value for value in catalogue["bindings"] if value["handoff_id"] == handoff), None)
    if row is None or path not in row["variant_bindings"]:
        raise ValueError("WORKFLOW_ROLE_PATH")
    return row, row["variant_bindings"][path]


def _same_boundary(role, base):
    return all(role[field] == base[field] for field in
               ("operator_agent", "tool_tier", "allowed_tools"))


def compile_requirements(catalogue, reviewed, roles, ancestry, contract_versions):
    """Compile reviewed mappings once for an immutable workflow and role snapshot.

    Args:
        catalogue: Existing runtime-validated workflow acceptance catalogue.
        reviewed: Exact role requirements admitted by an independent review path.
        roles: Captured role rows keyed by exact slug.
        ancestry: Captured professional ancestors keyed by exact slug.
        contract_versions: Captured registered artifact contract versions by ID.
    Returns:
        Exact handoff, path and endpoint keys with validated mapping digests.
    Raises:
        ValueError: Schema, provenance, scope or contract requirements conflict.
    """
    _fields(reviewed, "protocol workflow_catalogue requirements")
    if reviewed["protocol"] != PROTOCOL or reviewed["workflow_catalogue"] != catalogue["catalog_hash"]:
        raise ValueError("WORKFLOW_ROLE_CATALOGUE")
    if not isinstance(reviewed["requirements"], list):
        raise ValueError("WORKFLOW_ROLE_SCHEMA")
    found = {}
    for requirement in reviewed["requirements"]:
        _fields(requirement, "handoff path endpoint base contract responsibility mappings")
        target = (requirement["handoff"], requirement["path"], requirement["endpoint"])
        if not all(isinstance(value, str) and value for value in target):
            raise ValueError("WORKFLOW_ROLE_SCHEMA")
        if target in found:
            raise ValueError("WORKFLOW_ROLE_DUPLICATE")
        found[target] = _compile_requirement(
            catalogue, target, requirement, roles, ancestry, contract_versions)
    return {"workflow_catalogue": catalogue["catalog_hash"], "requirements": found}


def _compile_requirement(catalogue, key, requirement, roles, ancestry, contract_versions):
    from workflow_specialist_profiles import ALL_REQUIRED_PROTOCOL

    row, effective = _binding(catalogue, *key)
    base_slug = requirement["base"]
    contract = requirement["contract"]
    conjunction = isinstance(contract, dict) and contract.get("protocol") == ALL_REQUIRED_PROTOCOL
    if conjunction:
        _fields(contract, "protocol contracts")
        if not isinstance(contract["contracts"], list):
            raise ValueError("WORKFLOW_ROLE_CONTRACT")
        refs = contract["contracts"]
        for ref in refs:
            _fields(ref, "id version digest")
            if not isinstance(ref["digest"], str) or len(ref["digest"]) != 64:
                raise ValueError("WORKFLOW_ROLE_CONTRACT")
        if (len(refs) < 2 or [ref["id"] for ref in refs] != effective["contract_ids"]
                or len({ref["id"] for ref in refs}) != len(refs)
                or "profile" not in effective.get("workflow_role_requirement", {})):
            raise ValueError("WORKFLOW_ROLE_CONTRACT")
    else:
        _fields(contract, "id version")
        refs = [contract]
    if (key[2] != "producer" or base_slug in _AUTHORITY_ROLES or base_slug not in roles
            or effective[_ENDPOINTS[key[2]]] != base_slug or requirement["responsibility"] != "author"):
        raise ValueError("WORKFLOW_ROLE_BOUNDARY")
    if (row["contract_selection"] != "registered-contracts"
            or any(ref["id"] not in effective["contract_ids"]
                   or contract_versions.get(ref["id"]) != ref["version"] for ref in refs)):
        raise ValueError("WORKFLOW_ROLE_CONTRACT")
    required_units = {unit["id"] for unit in effective["handoff_content_contract"]["units"]}
    if not isinstance(requirement["mappings"], list) or not requirement["mappings"]:
        raise ValueError("WORKFLOW_ROLE_SCHEMA")
    mappings = {}
    for mapping in requirement["mappings"]:
        _fields(mapping, "slug product deployments covered_units handoff_contract_hash")
        slug = mapping["slug"]
        if (slug in mappings or slug not in roles or base_slug not in ancestry.get(slug, ())
                or not _same_boundary(roles[slug], roles[base_slug])):
            raise ValueError("WORKFLOW_ROLE_SPECIALTY")
        if (not isinstance(mapping["covered_units"], list)
                or len(mapping["covered_units"]) != len(required_units)
                or set(mapping["covered_units"]) != required_units
                or mapping["handoff_contract_hash"] != canonical_hash(effective["handoff_content_contract"])):
            raise ValueError("WORKFLOW_ROLE_OBLIGATIONS")
        if (not isinstance(mapping["product"], str) or not mapping["product"]
                or not isinstance(mapping["deployments"], list) or not mapping["deployments"]):
            raise ValueError("WORKFLOW_ROLE_APPLICABILITY")
        seen_deployments = set()
        for deployment in mapping["deployments"]:
            _fields(deployment, "edition version deployment")
            if not all(isinstance(value, str) and value for value in deployment.values()):
                raise ValueError("WORKFLOW_ROLE_APPLICABILITY")
            identity = canonical_hash(deployment)
            if identity in seen_deployments:
                raise ValueError("WORKFLOW_ROLE_DUPLICATE")
            seen_deployments.add(identity)
        mappings[slug] = {"product": mapping["product"], "deployments": sorted(seen_deployments),
                          "digest": canonical_hash(mapping)}
    result = {"contract": dict(contract), "responsibility": requirement["responsibility"],
              "digest": canonical_hash(requirement), "mappings": mappings}
    profile = effective.get("workflow_role_requirement", {}).get("profile")
    if profile is not None:
        deployed = {}
        for slug, mapping in mappings.items():
            for deployment in mapping["deployments"]:
                deployed.setdefault((mapping["product"], deployment), {})[slug] = mapping["digest"]
        result.update(profile=profile, deployed=deployed, effective=effective)
    return result


def eligible_roles(catalogue, compiled, *,
                   handoff, path, endpoint, responsibility, scope, available, independent,
                   generic_applicable=False):
    """Return deterministic eligible slugs and pin data for one workflow endpoint.

    Args:
        catalogue: Existing runtime-validated workflow acceptance catalogue.
        compiled: Host-pinned index from compile_requirements. An absent policy
            leaves the selected workflow binding exact.
        handoff: Exact workflow-and-step handoff ID.
        path: Already resolved effective workflow path ID.
        endpoint: Exact producer or receiver side of the effective handoff.
        responsibility: Actual host assignment responsibility.
        scope: Applicable product, edition, version and deployment facts, or
            None if their governed evidence is unavailable.
        available: Exact role slugs currently available to the assignment.
        independent: True only when the host's independence prerequisites hold.
        generic_applicable: Exact admitted evidence that the context is product-neutral.
    Returns:
        Sorted eligible role slugs and evidence identifying the exact binding.
    Raises:
        ValueError: An unknown binding or inconsistent reviewed policy.
    """
    key = (handoff, path, endpoint)
    requirement = compiled["requirements"].get(key) if compiled is not None else None
    profile = requirement.get("profile") if requirement is not None else None
    effective = requirement["effective"] if profile is not None else _binding(catalogue, *key)[1]
    bound_role = effective[_ENDPOINTS[endpoint]]
    evidence = {"workflow_catalogue": catalogue["catalog_hash"], "handoff": handoff,
                "path": path, "endpoint": endpoint, "mode": "exact",
                "bound_role": bound_role, "handoff_contract_hash":
                    canonical_hash(effective["handoff_content_contract"])}
    if compiled is not None and compiled["workflow_catalogue"] != catalogue["catalog_hash"]:
        raise ValueError("WORKFLOW_ROLE_CATALOGUE")
    if requirement is None:
        return ([bound_role] if bound_role in available and independent else []), evidence
    evidence.update(mode="compatible-specialization", contract=requirement["contract"],
                    requirement_hash=requirement["digest"], scope=scope, mapping_hashes={})
    if profile is not None:
        evidence["profile"] = profile
    if not independent:
        evidence["blocker"] = "INDEPENDENT_ASSIGNMENT_REQUIRED"
        return [], evidence
    if responsibility != requirement["responsibility"]:
        evidence["blocker"] = "RESPONSIBILITY_MISMATCH"
        return [], evidence
    if scope is None:
        if (profile is not None and profile["mode"] == "preferred-specialist"
                and generic_applicable is True and bound_role in available):
            reason = "ADMITTED_PRODUCT_NEUTRAL_SCOPE"
            evidence["fallback"] = reason
            evidence["mapping_hashes"] = {bound_role: canonical_hash({
                "requirement": requirement["digest"], "profile": profile["profile_digest"],
                "reason": reason, "base": bound_role})}
            return [bound_role], evidence
        evidence["blocker"] = "PRODUCT_SCOPE_REQUIRED"
        return [], evidence
    if generic_applicable:
        evidence["blocker"] = "PRODUCT_SCOPE_CONFLICT"
        return [], evidence
    _fields(scope, "product edition version deployment")
    if not all(isinstance(value, str) and value for value in scope.values()):
        raise ValueError("WORKFLOW_ROLE_APPLICABILITY")
    deployment = canonical_hash({name: scope[name] for name in ("edition", "version", "deployment")})
    if profile is not None:
        applicable = requirement["deployed"].get((scope["product"], deployment), {})
    else:
        applicable = {slug: mapping["digest"] for slug, mapping in requirement["mappings"].items()
                      if scope["product"] == mapping["product"] and deployment in mapping["deployments"]}
    eligible = sorted(slug for slug in applicable if slug in available)
    evidence["mapping_hashes"] = {slug: applicable[slug] for slug in eligible}
    if not eligible:
        evidence["blocker"] = "SPECIALTY_UNAVAILABLE" if applicable else "PRODUCT_SCOPE_MISMATCH"
    return eligible, evidence


SIEM_PILOT_PROTOCOL = "jai.siem-workflow-staging/1"


def stage_siem_workflow(draft, deployments, baseline, contracts):
    """Compile the explicitly staged SIEM workflow against canonical contracts.

    Args:
        draft: The closed SIEM source declaration.
        deployments: Explicit candidate deployment tuples keyed by product.
        baseline: Validated ordinary workflow catalogue.
        contracts: Authoritative contract rows keyed by contract ID.
    Returns:
        Staged registration, with the exact combined catalogue and the mapping
        candidate. The registration supplies neither deployment evidence nor approval.
    Raises:
        ValueError: Unsupported source, invalid registration, or contract mismatch.
    """
    from copy import deepcopy

    _fields(draft, "schema_version status workflow path scope inputs steps")
    if (type(draft["schema_version"]) is not int or draft["schema_version"] != 1
            or draft["status"] != "proposed"
            or draft["workflow"] != "siem-log-source-integration"
            or draft["path"] != "bounded-validation"
            or not isinstance(draft["scope"], str) or not draft["scope"].strip()
            or not isinstance(draft["inputs"], list) or not draft["inputs"]
            or not all(isinstance(value, str) and value.strip() for value in draft["inputs"])
            or not isinstance(draft["steps"], list) or len(draft["steps"]) != 2):
        raise ValueError("WORKFLOW_PILOT_SOURCE")
    producer, reviewer = draft["steps"]
    _fields(producer, "step endpoint role_requirement artifact mandatory_units proposed_mappings receiving_role")
    _fields(reviewer, "step endpoint role_requirement artifact gate mandatory_units receiving_role")
    compatible, exact = producer["role_requirement"], reviewer["role_requirement"]
    _fields(compatible, "mode base responsibility contract")
    _fields(exact, "mode slug contract")
    base, receiver = compatible["base"], exact["slug"]
    if (type(producer["step"]) is not int or type(reviewer["step"]) is not int
            or producer["step"] != 1 or reviewer["step"] != 2
            or not isinstance(reviewer["gate"], str) or not reviewer["gate"].strip()
            or producer["endpoint"] != "producer" or reviewer["endpoint"] != "producer"
            or compatible["mode"] != "compatible-specialization" or compatible["responsibility"] != "author"
            or exact["mode"] != "exact" or base != "security-engineer"
            or receiver != "security-assurance-and-measurement-architect"
            or producer["receiving_role"] != receiver
            or reviewer["receiving_role"] != "engagement:named-acceptance-authority"):
        raise ValueError("WORKFLOW_PILOT_BOUNDARY")

    name, path = draft["workflow"], draft["path"]
    if name in baseline["profiles"]:
        raise ValueError("WORKFLOW_PILOT_WORKFLOW_ALREADY_REGISTERED")
    profile = {
        "entry_inputs": draft["inputs"], "routes": [{"id": value} for value in ("continue", "rework", "stop", "exit")],
        "variants": [{"id": path}],
        "paths": [{"id": path, "variant": path, "mechanism": path, "steps": [1, 2], "terminal_step": 2}],
    }
    rows = []
    refs = (compatible["contract"], exact["contract"])
    for step, slug, ref in zip(draft["steps"], (base, receiver), refs):
        _fields(ref, "id version")
        if not all(isinstance(value, str) and value for value in ref.values()):
            raise ValueError("WORKFLOW_PILOT_CONTRACT")
        canonical = contracts.get(ref["id"])
        expected_id = f"{base}:4" if step["step"] == 1 else f"{receiver}:2"
        if (ref["id"] != expected_id or not canonical or canonical["version"] != ref["version"]
                or canonical["role_slug"] != slug):
            raise ValueError("WORKFLOW_PILOT_CONTRACT")
        units = step["mandatory_units"]
        if not isinstance(units, list) or not units or not isinstance(step["artifact"], str) or not step["artifact"]:
            raise ValueError("WORKFLOW_PILOT_UNITS")
        for unit in units:
            _fields(unit, "id semantic_field required_fields acceptance_criterion")
            if (not all(isinstance(unit[key], str) and unit[key].strip()
                        for key in ("id", "semantic_field", "acceptance_criterion"))
                    or not isinstance(unit["required_fields"], list) or not unit["required_fields"]
                    or not all(isinstance(field, str) and field for field in unit["required_fields"])
                    or len(set(unit["required_fields"])) != len(unit["required_fields"])):
                raise ValueError("WORKFLOW_PILOT_UNITS")
        if any(len({unit[key] for unit in units}) != len(units) for key in ("id", "semantic_field")):
            raise ValueError("WORKFLOW_PILOT_UNITS")
        handoff_id = f"{name}:{step['step']}"
        contract = {"id": "handoff/" + handoff_id, "version": "1.0.0",
                    "subject": step["artifact"], "workflow_profile_hash": canonical_hash(profile),
                    "units": units}
        effective = {
            "producer_role": slug, "receiving_role": step["receiving_role"], "contract_ids": [ref["id"]],
            "acceptance_criterion": reviewer["gate"], "handoff_content_contract": contract,
            "next_step": 2 if step["step"] == 1 else None,
        }
        rows.append({**effective, "handoff_id": handoff_id, "workflow_id": name, "step": step["step"],
                     "handover": step["artifact"], "contract_selection": "registered-contracts",
                     "variant_bindings": {path: dict(effective)}})

    mappings = []
    expected_products = {"splunk-enterprise-security": "splunk-enterprise-security-specialist",
                         "ibm-qradar-siem": "qradar-siem-specialist"}
    if (not isinstance(deployments, dict) or set(deployments) != set(expected_products)
            or not isinstance(producer["proposed_mappings"], list)
            or len(producer["proposed_mappings"]) != len(expected_products)):
        raise ValueError("WORKFLOW_PILOT_PRODUCTS")
    seen_products = set()
    for proposed in producer["proposed_mappings"]:
        _fields(proposed, "slug product applicability")
        product = proposed["product"]
        if (not isinstance(product, str) or product in seen_products or product not in expected_products
                or expected_products[product] != proposed["slug"]
                or not isinstance(proposed["applicability"], str) or not proposed["applicability"].strip()):
            raise ValueError("WORKFLOW_PILOT_PRODUCTS")
        seen_products.add(product)
        facts = deployments[product]
        if not isinstance(facts, list) or not facts:
            raise ValueError("WORKFLOW_PILOT_DEPLOYMENT")
        for fact in facts:
            _fields(fact, "edition version deployment")
            if not all(isinstance(value, str) and value.strip() for value in fact.values()):
                raise ValueError("WORKFLOW_PILOT_DEPLOYMENT")
        if len({canonical_hash(fact) for fact in facts}) != len(facts):
            raise ValueError("WORKFLOW_PILOT_DEPLOYMENT")
        mappings.append({"slug": proposed["slug"], "product": product, "deployments": facts,
                         "covered_units": [unit["id"] for unit in producer["mandatory_units"]],
                         "handoff_contract_hash": canonical_hash(rows[0]["handoff_content_contract"])})
    binding = {"handoff": rows[0]["handoff_id"], "path": path, "endpoint": "producer",
               "base": base, "responsibility": "author", "contract": refs[0], "mappings": mappings}
    rows[0]["variant_bindings"][path]["workflow_role_requirement"] = {
        "mode": "compatible-specialization", "contract": refs[0], "requirement_hash": canonical_hash(binding),
    }
    catalogue = deepcopy(baseline)
    catalogue.pop("catalog_hash")
    catalogue["schema_version"] = "2.0.0"
    catalogue["workflow_count"] += 1
    catalogue["handoff_count"] += len(rows)
    catalogue["profiles"][name] = profile
    catalogue["bindings"].extend(rows)
    catalogue["catalog_hash"] = canonical_hash(catalogue)
    return {"protocol": SIEM_PILOT_PROTOCOL, "status": "staged",
            "ordinary_catalogue_hash": baseline["catalog_hash"], "source": draft, "deployments": deployments,
            "catalogue": catalogue, "mapping_candidate": binding}
