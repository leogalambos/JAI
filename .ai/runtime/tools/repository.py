#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Enterprise Architecture repository/interchange runtime for AI IT House.

The EA domain projection repository is JSON owned by AI IT House. ArchiMate Open Exchange is
an interchange boundary, not the authoritative architecture-domain projection store.

Commands:
  repository.py init PATH --id REPO-ID --name NAME
  repository.py validate PATH [--strict]
  repository.py project-set PATH PROJECT-ID --name NAME --owner OWNER [--status STATE]
  repository.py element-set PATH ELEMENT-ID --type TYPE --name NAME --project PROJECT-ID --owner OWNER [--state STATE] [--horizon HORIZON]
  repository.py relationship-set PATH REL-ID --type TYPE --source ELEMENT-ID --target ELEMENT-ID [--project PROJECT-ID] [--owner OWNER]
  repository.py view-set PATH VIEW-ID --name NAME --viewpoint VIEWPOINT --elements ID,ID [--relationships ID,ID] [--projects ID,ID]
  repository.py benefit-set PATH PROJECT-ID BENEFIT-ID --name NAME --owner OWNER --measure MEASURE --baseline BASELINE --target TARGET [--status STATE]
  repository.py lifecycle-set PATH ELEMENT-ID STATE --owner OWNER [--date YYYY-MM-DD]
  repository.py decommission PATH ELEMENT-ID --owner OWNER --date YYYY-MM-DD [--waiver TEXT]
  repository.py impact PATH ELEMENT-ID
  repository.py portfolio PATH [--format md|json] [--out FILE]
  repository.py generate-views PATH --out DIR [--project PROJECT-ID] [--preset all|business|application|technology|data|security|motivation|migration|portfolio|lifecycle]
  repository.py export-open-exchange PATH --out FILE [--project PROJECT-ID] [--language en] [--no-views]
  repository.py import-open-exchange XML --repo PATH [--project-id ID] [--project-name NAME] [--merge]
  repository.py self-test

Open Exchange support deliberately focuses on portable model, relationship and diagram
content. Vendor-specific repository semantics remain properties in the EA projection model.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import html
import json
import math
import re
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RELEASE = (ROOT / 'VERSION').read_text().strip()
LEGACY_SCHEMA_VERSIONS = {'26.10', '26.10.1', '26.10.2', '26.10.3'}
EA_ROOT = ROOT / "ea"
POLICY_FILE = EA_ROOT / "consistency-policy.json"
VIEWPOINT_FILE = EA_ROOT / "viewpoints.json"
PUB_THEME = ROOT / "publication/themes/enterprise-default.json"

ARCHI_NS = "http://www.opengroup.org/xsd/archimate/3.0/"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
XML_NS = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("", ARCHI_NS)
ET.register_namespace("xsi", XSI_NS)

ARCHIMATE_ELEMENT_TYPES = {
    # Strategy
    "Resource", "Capability", "ValueStream", "CourseOfAction",
    # Business
    "BusinessActor", "BusinessRole", "BusinessCollaboration", "BusinessInterface",
    "BusinessProcess", "BusinessFunction", "BusinessInteraction", "BusinessEvent",
    "BusinessService", "BusinessObject", "Contract", "Representation", "Product",
    # Application
    "ApplicationComponent", "ApplicationCollaboration", "ApplicationInterface",
    "ApplicationFunction", "ApplicationInteraction", "ApplicationProcess", "ApplicationEvent",
    "ApplicationService", "DataObject",
    # Technology
    "Node", "Device", "SystemSoftware", "TechnologyCollaboration", "TechnologyInterface",
    "Path", "CommunicationNetwork", "TechnologyFunction", "TechnologyProcess",
    "TechnologyInteraction", "TechnologyEvent", "TechnologyService", "Artifact",
    # Physical
    "Equipment", "Facility", "DistributionNetwork", "Material",
    # Motivation
    "Stakeholder", "Driver", "Assessment", "Goal", "Outcome", "Principle", "Requirement",
    "Constraint", "Meaning", "Value",
    # Implementation & migration
    "WorkPackage", "Deliverable", "ImplementationEvent", "Plateau", "Gap",
    # Composite / connector concepts commonly exchanged
    "Grouping", "Location", "AndJunction", "OrJunction",
}

ARCHIMATE_RELATIONSHIP_TYPES = {
    "Composition", "Aggregation", "Assignment", "Realization", "Serving", "Access",
    "Influence", "Triggering", "Flow", "Specialization", "Association",
}

LIFECYCLE_STATES = {"planned", "active", "transition", "deprecated", "retiring", "retired", "reference"}
HORIZONS = {"current", "transition", "target", "reference", "unspecified"}
PROJECT_STATES = {"proposed", "approved", "delivery", "live", "closing", "closed", "cancelled"}
BENEFIT_STATES = {"planned", "baselined", "in-realisation", "realised", "at-risk", "closed"}
XML_ID = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*$")


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path | str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path | str, obj: Any) -> None:
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def resolve_repo(path: Path | str) -> Path:
    p = Path(path)
    if p.is_dir() or (not p.exists() and p.suffix == ""):
        return p / "repository.json"
    return p


def repository_payload(repo: dict) -> dict:
    x = copy.deepcopy(repo)
    x.get("repository", {}).pop("updated_at", None)
    x.get("repository", {}).pop("revision_hash", None)
    return x


def repository_hash(repo: dict) -> str:
    return hashlib.sha256(canonical(repository_payload(repo))).hexdigest()


def touch(repo: dict) -> None:
    repo.setdefault("repository", {})["updated_at"] = now_utc()
    repo["repository"]["revision_hash"] = repository_hash(repo)


def empty_repository(repo_id: str, name: str) -> dict:
    repo = {
        "schema_version": RELEASE,
        "repository": {
            "id": repo_id,
            "name": name,
            "version": "1.0",
            "created_at": now_utc(),
            "updated_at": now_utc(),
            "default_language": "en",
            "authoritative_for": "ea-domain-projection",
            "global_source_of_truth": False,
            "jai_profile": "ea",
            "semantic_identity_authority": "JAI",
            "revision_hash": "",
        },
        "projects": [],
        "elements": [],
        "relationships": [],
        "views": [],
        "portfolio_links": [],
        "exceptions": [],
    }
    touch(repo)
    return repo


def save_repo(path: Path | str, repo: dict) -> Path:
    p = resolve_repo(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    repo['schema_version'] = RELEASE
    meta=repo.setdefault('repository',{})
    meta['authoritative_for']='ea-domain-projection'
    meta['global_source_of_truth']=False
    meta['jai_profile']='ea'
    meta['semantic_identity_authority']='JAI'
    touch(repo)
    write_json(p, repo)
    return p


def load_repo(path: Path | str) -> tuple[Path, dict]:
    p = resolve_repo(path)
    if not p.is_file():
        raise SystemExit(f"error: repository not found: {p}")
    return p, load_json(p)


def index_by(items: list[dict], key: str = "id") -> dict[str, dict]:
    return {str(x.get(key)): x for x in items if x.get(key) is not None}


def upsert(items: list[dict], obj: dict, key: str = "id") -> None:
    for i, old in enumerate(items):
        if old.get(key) == obj.get(key):
            merged = copy.deepcopy(old)
            merged.update({k: v for k, v in obj.items() if v is not None})
            items[i] = merged
            return
    items.append(obj)


def split_csv(s: str | None) -> list[str]:
    if not s:
        return []
    return [x.strip() for x in s.split(",") if x.strip()]


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def child_text(parent: ET.Element, name: str, default: str = "") -> str:
    for c in list(parent):
        if local_name(c.tag) == name:
            return (c.text or "").strip()
    return default


def children(parent: ET.Element, name: str) -> list[ET.Element]:
    return [c for c in list(parent) if local_name(c.tag) == name]


def first_child(parent: ET.Element, name: str) -> ET.Element | None:
    for c in list(parent):
        if local_name(c.tag) == name:
            return c
    return None


def q(tag: str) -> str:
    return f"{{{ARCHI_NS}}}{tag}"


def xml_lang() -> str:
    return f"{{{XML_NS}}}lang"


def xsi_type() -> str:
    return f"{{{XSI_NS}}}type"


def prop_map_from_xml(obj: ET.Element, prop_defs: dict[str, str]) -> dict[str, str]:
    out: dict[str, str] = {}
    props = first_child(obj, "properties")
    if props is None:
        return out
    for p in children(props, "property"):
        ref = p.attrib.get("propertyDefinitionRef", "")
        name = prop_defs.get(ref, ref)
        val = child_text(p, "value", "")
        if name:
            out[name] = val
    return out


def add_text(parent: ET.Element, tag: str, text: str, lang: str | None = None) -> ET.Element:
    e = ET.SubElement(parent, q(tag))
    if lang:
        e.set(xml_lang(), lang)
    e.text = str(text)
    return e


def add_properties(parent: ET.Element, values: dict[str, Any], prop_ids: dict[str, str], lang: str) -> None:
    clean = {k: v for k, v in values.items() if v not in (None, "", [], {})}
    if not clean:
        return
    ps = ET.SubElement(parent, q("properties"))
    for key in sorted(clean):
        p = ET.SubElement(ps, q("property"), {"propertyDefinitionRef": prop_ids[key]})
        value = clean[key]
        if isinstance(value, (list, dict)):
            value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        add_text(p, "value", str(value), lang)


def archi_properties_for_element(e: dict) -> dict[str, Any]:
    p = dict(e.get("properties") or {})
    p.update({
        "AIITHouse.RepositoryId": e.get("id"),
        "AIITHouse.Project": e.get("project_id"),
        "AIITHouse.Owner": e.get("owner"),
        "AIITHouse.Lifecycle": e.get("lifecycle_state"),
        "AIITHouse.Horizon": e.get("horizon"),
        "AIITHouse.ArtifactRefs": e.get("artifact_refs"),
        "AIITHouse.BenefitRefs": e.get("benefit_refs"),
        "AIITHouse.SourceRefs": e.get("source_refs"),
        "AIITHouse.ValidFrom": e.get("valid_from"),
        "AIITHouse.ValidTo": e.get("valid_to"),
        "AIITHouse.ReviewDue": e.get("review_due"),
        "AIITHouse.Source": e.get("source"),
        "AIITHouse.Projection": e.get("projection"),
    })
    return {k: v for k, v in p.items() if v not in (None, "", [], {})}


def archi_properties_for_relationship(r: dict) -> dict[str, Any]:
    p = dict(r.get("properties") or {})
    p.update({
        "AIITHouse.RepositoryId": r.get("id"),
        "AIITHouse.Project": r.get("project_id"),
        "AIITHouse.Owner": r.get("owner"),
        "AIITHouse.Lifecycle": r.get("lifecycle_state"),
    })
    return {k: v for k, v in p.items() if v not in (None, "", [], {})}


def archi_properties_for_view(v: dict) -> dict[str, Any]:
    p = dict(v.get("properties") or {})
    p.update({
        "AIITHouse.RepositoryId": v.get("id"),
        "AIITHouse.Projects": v.get("project_ids"),
        "AIITHouse.Purpose": v.get("purpose"),
        "AIITHouse.Audience": v.get("audience"),
        "AIITHouse.IncludeRetired": bool(v.get("include_retired", False)),
    })
    return {k: v for k, v in p.items() if v not in (None, "", [], {})}


def parse_maybe_json(value: str) -> Any:
    value = (value or "").strip()
    if not value:
        return value
    if value[:1] in "[{" or value in ("true", "false", "null"):
        try:
            return json.loads(value)
        except Exception:
            return value
    return value


def pop_ai_properties(props: dict[str, str]) -> dict[str, Any]:
    return {k: parse_maybe_json(v) for k, v in props.items() if k.startswith("AIITHouse.")}


def non_ai_properties(props: dict[str, str]) -> dict[str, Any]:
    return {k: parse_maybe_json(v) for k, v in props.items() if not k.startswith("AIITHouse.")}


def validate_repository(repo: dict, strict: bool = False, policy: dict | None = None) -> tuple[list[str], list[str]]:
    policy = policy or (load_json(POLICY_FILE) if POLICY_FILE.is_file() else {})
    errors: list[str] = []
    warnings: list[str] = []
    rmeta = repo.get("repository") or {}
    for k in ("id", "name"):
        if not rmeta.get(k): errors.append(f"repository missing {k}")
    if repo.get("schema_version") not in ({RELEASE} | LEGACY_SCHEMA_VERSIONS): errors.append(f"unsupported schema_version {repo.get('schema_version')!r}")
    elif repo.get("schema_version") != RELEASE: warnings.append(f"legacy schema_version {repo.get('schema_version')!r}; next save upgrades to {RELEASE}")

    projects = repo.get("projects") or []
    elements = repo.get("elements") or []
    relationships = repo.get("relationships") or []
    views = repo.get("views") or []
    links = repo.get("portfolio_links") or []

    def dupes(items: list[dict], label: str) -> dict[str, dict]:
        seen: dict[str, dict] = {}
        for i, x in enumerate(items):
            ident = str(x.get("id", ""))
            if not ident:
                errors.append(f"{label}[{i}] missing id")
                continue
            if ident in seen: errors.append(f"duplicate {label} id {ident}")
            seen[ident] = x
        return seen

    ps = dupes(projects, "project")
    es = dupes(elements, "element")
    rs = dupes(relationships, "relationship")
    vs = dupes(views, "view")
    ls = dupes(links, "portfolio_link")
    all_ids: dict[str, str] = {}
    for label, idx in (("project", ps), ("element", es), ("relationship", rs), ("view", vs), ("portfolio_link", ls)):
        for ident in idx:
            if ident in all_ids: errors.append(f"identifier {ident} reused by {all_ids[ident]} and {label}")
            all_ids[ident] = label
            if not XML_ID.match(ident): warnings.append(f"{label} id {ident!r} is not directly portable as xs:ID")

    for p in projects:
        if not p.get("name"): errors.append(f"project {p.get('id')} missing name")
        if not p.get("owner"): warnings.append(f"project {p.get('id')} has no owner")
        state = p.get("status", "proposed")
        if state not in PROJECT_STATES: errors.append(f"project {p.get('id')} invalid status {state}")
        benefit_ids=set()
        for b in p.get("benefits", []) or []:
            bid=b.get("id")
            if not bid: errors.append(f"project {p.get('id')} has benefit without id"); continue
            if bid in benefit_ids: errors.append(f"project {p.get('id')} duplicate benefit {bid}")
            benefit_ids.add(bid)
            for k in ("name", "owner", "measure", "baseline", "target"):
                if not b.get(k): warnings.append(f"benefit {p.get('id')}:{bid} missing {k}")
            if b.get("status", "planned") not in BENEFIT_STATES: errors.append(f"benefit {p.get('id')}:{bid} invalid status {b.get('status')}")

    benefit_keys = {f"{p['id']}:{b['id']}" for p in projects for b in (p.get("benefits") or []) if p.get("id") and b.get("id")}
    for e in elements:
        ident=e.get("id")
        for k in ("type", "name", "project_id", "owner"):
            if not e.get(k): errors.append(f"element {ident} missing {k}")
        if e.get("project_id") not in ps: errors.append(f"element {ident} references unknown project {e.get('project_id')}")
        if e.get("type") not in ARCHIMATE_ELEMENT_TYPES:
            warnings.append(f"element {ident} uses non-core/unknown ArchiMate type {e.get('type')}")
        state=e.get("lifecycle_state", "active")
        if state not in LIFECYCLE_STATES: errors.append(f"element {ident} invalid lifecycle_state {state}")
        horizon=e.get("horizon", "unspecified")
        if horizon not in HORIZONS: errors.append(f"element {ident} invalid horizon {horizon}")
        for bref in e.get("benefit_refs", []) or []:
            key = bref if ":" in str(bref) else f"{e.get('project_id')}:{bref}"
            if key not in benefit_keys: warnings.append(f"element {ident} references unknown benefit {bref}")
        if state == "retired" and not e.get("valid_to"):
            warnings.append(f"retired element {ident} has no valid_to date")

    active_states = set(policy.get("active_dependency_states", ["planned", "active", "transition", "deprecated", "retiring"]))
    for r in relationships:
        ident=r.get("id")
        for k in ("type", "source", "target"):
            if not r.get(k): errors.append(f"relationship {ident} missing {k}")
        if r.get("source") not in es: errors.append(f"relationship {ident} source missing: {r.get('source')}")
        if r.get("target") not in es: errors.append(f"relationship {ident} target missing: {r.get('target')}")
        if r.get("type") not in ARCHIMATE_RELATIONSHIP_TYPES:
            warnings.append(f"relationship {ident} uses non-core/unknown ArchiMate type {r.get('type')}")
        if r.get("project_id") and r.get("project_id") not in ps: errors.append(f"relationship {ident} unknown project {r.get('project_id')}")
        src=es.get(r.get("source")); tgt=es.get(r.get("target"))
        if src and tgt:
            cross=src.get("project_id") != tgt.get("project_id")
            if cross and not r.get("owner"):
                warnings.append(f"cross-project relationship {ident} has no owner")
            if tgt.get("lifecycle_state") == "retired" and src.get("lifecycle_state") in active_states:
                errors.append(f"active dependency {ident}: {src.get('id')} -> retired {tgt.get('id')}")

    viewed_elements=set()
    for v in views:
        ident=v.get("id")
        if not v.get("name"): errors.append(f"view {ident} missing name")
        refs=v.get("element_refs") or []
        for ref in refs:
            if ref not in es: errors.append(f"view {ident} references missing element {ref}")
            else:
                viewed_elements.add(ref)
                if es[ref].get("lifecycle_state") == "retired" and not v.get("include_retired", False):
                    warnings.append(f"view {ident} includes retired element {ref} without include_retired")
        for ref in v.get("relationship_refs") or []:
            if ref not in rs: errors.append(f"view {ident} references missing relationship {ref}")
        for pid in v.get("project_ids") or []:
            if pid not in ps: errors.append(f"view {ident} references missing project {pid}")

    for e in elements:
        if e.get("lifecycle_state") not in ("retired", "reference") and e.get("id") not in viewed_elements:
            warnings.append(f"element {e.get('id')} is not present in a governed view")

    for l in links:
        ident=l.get("id")
        for k in ("from_project", "to_project", "type", "owner", "status"):
            if not l.get(k): errors.append(f"portfolio_link {ident} missing {k}")
        if l.get("from_project") not in ps: errors.append(f"portfolio_link {ident} unknown from_project")
        if l.get("to_project") not in ps: errors.append(f"portfolio_link {ident} unknown to_project")
        for ref in l.get("element_refs") or []:
            if ref not in es: errors.append(f"portfolio_link {ident} missing element {ref}")

    # Cross-project relationships should be represented in portfolio links or have explicit owner.
    link_pairs={(x.get("from_project"),x.get("to_project")) for x in links}
    for r in relationships:
        src=es.get(r.get("source")); tgt=es.get(r.get("target"))
        if src and tgt and src.get("project_id") != tgt.get("project_id"):
            pair=(src.get("project_id"),tgt.get("project_id"))
            if pair not in link_pairs and (pair[1],pair[0]) not in link_pairs:
                warnings.append(f"cross-project relationship {r.get('id')} has no portfolio_link for {pair[0]} -> {pair[1]}")

    expected = repository_hash(repo)
    stored = rmeta.get("revision_hash")
    if stored and stored != expected:
        warnings.append("repository revision_hash is stale")
    if strict and warnings:
        errors.extend(f"strict: {w}" for w in warnings)
        warnings=[]
    return errors, warnings


def export_open_exchange(repo: dict, out: Path, project: str | None = None, lang: str = "en", include_views: bool = True) -> None:
    errors, warnings = validate_repository(repo)
    if errors:
        raise ValueError("repository invalid: " + "; ".join(errors[:8]))
    projects=index_by(repo.get("projects") or [])
    elements=[e for e in repo.get("elements",[]) if not project or e.get("project_id")==project]
    eids={e["id"] for e in elements}
    relationships=[r for r in repo.get("relationships",[]) if r.get("source") in eids and r.get("target") in eids]
    rids={r["id"] for r in relationships}
    views=[]
    if include_views:
        for v in repo.get("views",[]):
            refs=[x for x in v.get("element_refs",[]) if x in eids]
            if refs:
                vv=copy.deepcopy(v); vv["element_refs"]=refs; vv["relationship_refs"]=[x for x in v.get("relationship_refs",[]) if x in rids]
                views.append(vv)

    model_id = repo["repository"]["id"] if not project else f"{repo['repository']['id']}-{project}"
    if not XML_ID.match(model_id):
        model_id="id-"+hashlib.sha1(model_id.encode()).hexdigest()[:20]
    root=ET.Element(q("model"), {"identifier":model_id,"version":"3.2"})
    name=repo["repository"]["name"] + (f" — {projects.get(project,{}).get('name',project)}" if project else "")
    add_text(root,"name",name,lang)
    add_text(root,"documentation",f"AI IT House {RELEASE} repository exchange; revision {repo['repository'].get('revision_hash','')}",lang)

    # Build property definitions from all exported object properties.
    prop_names=set()
    eprops={e["id"]:archi_properties_for_element(e) for e in elements}
    rprops={r["id"]:archi_properties_for_relationship(r) for r in relationships}
    vprops={v["id"]:archi_properties_for_view(v) for v in views}
    for coll in (eprops,rprops,vprops):
        for p in coll.values(): prop_names.update(p.keys())
    prop_ids={name:f"pd-{hashlib.sha1(name.encode()).hexdigest()[:16]}" for name in sorted(prop_names)}

    if elements:
        ec=ET.SubElement(root,q("elements"))
        for e in sorted(elements,key=lambda x:x["id"]):
            node=ET.SubElement(ec,q("element"),{"identifier":e["id"],xsi_type():e["type"]})
            add_text(node,"name",e["name"],lang)
            if e.get("description"): add_text(node,"documentation",e["description"],lang)
            add_properties(node,eprops[e["id"]],prop_ids,lang)
    if relationships:
        rc=ET.SubElement(root,q("relationships"))
        for r in sorted(relationships,key=lambda x:x["id"]):
            attrs={"identifier":r["id"],"source":r["source"],"target":r["target"],xsi_type():r["type"]}
            if r.get("type")=="Access" and r.get("access_type"): attrs["accessType"]=r["access_type"]
            if r.get("type")=="Influence" and r.get("influence_strength"): attrs["modifier"]=str(r["influence_strength"])
            node=ET.SubElement(rc,q("relationship"),attrs)
            if r.get("name"): add_text(node,"name",r["name"],lang)
            if r.get("description"): add_text(node,"documentation",r["description"],lang)
            add_properties(node,rprops[r["id"]],prop_ids,lang)

    if prop_ids:
        pdc=ET.SubElement(root,q("propertyDefinitions"))
        for name in sorted(prop_ids):
            pd=ET.SubElement(pdc,q("propertyDefinition"),{"identifier":prop_ids[name],"type":"string"})
            add_text(pd,"name",name,lang)

    if views:
        vc=ET.SubElement(root,q("views")); dc=ET.SubElement(vc,q("diagrams"))
        rel_idx=index_by(relationships)
        for v in sorted(views,key=lambda x:x["id"]):
            attrs={"identifier":v["id"],xsi_type():"Diagram"}
            if v.get("viewpoint"): attrs["viewpoint"]=str(v["viewpoint"])
            ve=ET.SubElement(dc,q("view"),attrs); add_text(ve,"name",v["name"],lang)
            if v.get("description"): add_text(ve,"documentation",v["description"],lang)
            refs=v.get("element_refs") or []
            cols=max(1,math.ceil(math.sqrt(len(refs) or 1))); node_map={}
            for i,ref in enumerate(refs):
                nid=f"node-{v['id']}-{ref}"; node_map[ref]=nid
                ET.SubElement(ve,q("node"),{"identifier":nid,"elementRef":ref,xsi_type():"Element","x":str(60+(i%cols)*220),"y":str(80+(i//cols)*110),"w":"180","h":"60"})
            relrefs=v.get("relationship_refs") or []
            if not relrefs:
                relrefs=[r["id"] for r in relationships if r["source"] in node_map and r["target"] in node_map]
            for rid in relrefs:
                r=rel_idx.get(rid)
                if not r or r["source"] not in node_map or r["target"] not in node_map: continue
                ET.SubElement(ve,q("connection"),{"identifier":f"conn-{v['id']}-{rid}","relationshipRef":rid,xsi_type():"Relationship","source":node_map[r["source"]],"target":node_map[r["target"]]})
            add_properties(ve,vprops[v["id"]],prop_ids,lang)

    ET.indent(root, space="  ")
    out.parent.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(root).write(out,encoding="utf-8",xml_declaration=True)


def import_open_exchange(xml_path: Path, repo: dict, project_id: str | None = None, project_name: str | None = None, merge: bool = False) -> dict:
    root=ET.parse(xml_path).getroot()
    if local_name(root.tag)!="model": raise ValueError("Open Exchange root must be model")
    model_name=child_text(root,"name",xml_path.stem)
    project_id=project_id or re.sub(r"[^A-Za-z0-9_.-]+","-",root.attrib.get("identifier",model_name)).strip("-") or "imported-model"
    if not XML_ID.match(project_id): project_id="p-"+hashlib.sha1(project_id.encode()).hexdigest()[:16]
    project_name=project_name or model_name
    if not merge and (repo.get("elements") or repo.get("relationships") or repo.get("views")):
        raise ValueError("repository is not empty; use --merge")
    if project_id not in index_by(repo.get("projects") or []):
        repo.setdefault("projects",[]).append({"id":project_id,"name":project_name,"owner":"import owner required","status":"proposed","benefits":[],"artifacts":[str(xml_path)]})

    prop_defs={}
    pds=first_child(root,"propertyDefinitions")
    if pds is not None:
        for pd in children(pds,"propertyDefinition"):
            prop_defs[pd.attrib.get("identifier","")]=child_text(pd,"name",pd.attrib.get("identifier",""))

    ec=first_child(root,"elements")
    if ec is not None:
        for x in children(ec,"element"):
            props=prop_map_from_xml(x,prop_defs); ai=pop_ai_properties(props)
            ident=str(ai.get("AIITHouse.RepositoryId") or x.attrib.get("identifier"))
            obj={
                "id":ident,"type":x.attrib.get(xsi_type(),"Unknown"),"name":child_text(x,"name",ident),
                "project_id":str(ai.get("AIITHouse.Project") or project_id),"owner":str(ai.get("AIITHouse.Owner") or "import owner required"),
                "lifecycle_state":str(ai.get("AIITHouse.Lifecycle") or "active"),"horizon":str(ai.get("AIITHouse.Horizon") or "unspecified"),
                "description":child_text(x,"documentation",""),"properties":non_ai_properties(props),
                "artifact_refs":ai.get("AIITHouse.ArtifactRefs") or [],"benefit_refs":ai.get("AIITHouse.BenefitRefs") or [],"source_refs":ai.get("AIITHouse.SourceRefs") or [str(xml_path)],
                "valid_from":ai.get("AIITHouse.ValidFrom"),"valid_to":ai.get("AIITHouse.ValidTo"),"review_due":ai.get("AIITHouse.ReviewDue"),
                "source":ai.get("AIITHouse.Source") or {},"projection":ai.get("AIITHouse.Projection") or {},
            }
            if obj["project_id"] not in index_by(repo["projects"]):
                repo["projects"].append({"id":obj["project_id"],"name":obj["project_id"],"owner":"import owner required","status":"proposed","benefits":[],"artifacts":[]})
            upsert(repo.setdefault("elements",[]),obj)

    # Map exchange identifiers to canonical identifiers where AIITHouse.RepositoryId was used.
    exchange_to_repo={}
    if ec is not None:
        for x in children(ec,"element"):
            props=prop_map_from_xml(x,prop_defs); ai=pop_ai_properties(props)
            exchange_to_repo[x.attrib.get("identifier","")]=str(ai.get("AIITHouse.RepositoryId") or x.attrib.get("identifier"))

    rc=first_child(root,"relationships")
    if rc is not None:
        for x in children(rc,"relationship"):
            props=prop_map_from_xml(x,prop_defs); ai=pop_ai_properties(props)
            ident=str(ai.get("AIITHouse.RepositoryId") or x.attrib.get("identifier"))
            source=exchange_to_repo.get(x.attrib.get("source",""),x.attrib.get("source","")); target=exchange_to_repo.get(x.attrib.get("target",""),x.attrib.get("target",""))
            obj={"id":ident,"type":x.attrib.get(xsi_type(),"Unknown"),"source":source,"target":target,"project_id":str(ai.get("AIITHouse.Project") or project_id),"owner":str(ai.get("AIITHouse.Owner") or "import owner required"),"lifecycle_state":str(ai.get("AIITHouse.Lifecycle") or "active"),"name":child_text(x,"name",""),"description":child_text(x,"documentation",""),"properties":non_ai_properties(props)}
            if x.attrib.get("accessType"): obj["access_type"]=x.attrib["accessType"]
            if x.attrib.get("modifier"): obj["influence_strength"]=x.attrib["modifier"]
            upsert(repo.setdefault("relationships",[]),obj)

    vc=first_child(root,"views")
    if vc is not None:
        dc=first_child(vc,"diagrams")
        if dc is not None:
            rel_exchange_to_repo={}
            if rc is not None:
                for x in children(rc,"relationship"):
                    props=prop_map_from_xml(x,prop_defs); ai=pop_ai_properties(props)
                    rel_exchange_to_repo[x.attrib.get("identifier","")]=str(ai.get("AIITHouse.RepositoryId") or x.attrib.get("identifier"))
            for x in children(dc,"view"):
                props=prop_map_from_xml(x,prop_defs); ai=pop_ai_properties(props)
                ident=str(ai.get("AIITHouse.RepositoryId") or x.attrib.get("identifier"))
                erefs=[]; rrefs=[]
                for n in x.iter():
                    if local_name(n.tag)=="node" and n.attrib.get("elementRef"):
                        eref=exchange_to_repo.get(n.attrib["elementRef"],n.attrib["elementRef"])
                        if eref not in erefs: erefs.append(eref)
                    if local_name(n.tag)=="connection" and n.attrib.get("relationshipRef"):
                        rref=rel_exchange_to_repo.get(n.attrib["relationshipRef"],n.attrib["relationshipRef"])
                        if rref not in rrefs: rrefs.append(rref)
                pids=ai.get("AIITHouse.Projects") or sorted({index_by(repo.get("elements") or []).get(e,{}).get("project_id") for e in erefs if index_by(repo.get("elements") or []).get(e,{})})
                pids=[p for p in pids if p]
                obj={"id":ident,"name":child_text(x,"name",ident),"description":child_text(x,"documentation",""),"viewpoint":x.attrib.get("viewpoint","Custom"),"purpose":ai.get("AIITHouse.Purpose") or "Imported view","audience":ai.get("AIITHouse.Audience") or ["Architecture stakeholders"],"project_ids":pids or [project_id],"element_refs":erefs,"relationship_refs":rrefs,"include_retired":bool(ai.get("AIITHouse.IncludeRetired",False)),"properties":non_ai_properties(props)}
                upsert(repo.setdefault("views",[]),obj)
    touch(repo)
    return repo


def type_group(t: str) -> str:
    if t.startswith("Business") or t in {"Product","Contract","Representation"}: return "business"
    if t.startswith("Application"): return "application"
    if t in {"DataObject","BusinessObject","Representation","Artifact"}: return "data"
    if t.startswith("Technology") or t in {"Node","Device","SystemSoftware","Path","CommunicationNetwork","Artifact","Equipment","Facility","DistributionNetwork","Material"}: return "technology"
    if t in {"Stakeholder","Driver","Assessment","Goal","Outcome","Principle","Requirement","Constraint","Meaning","Value"}: return "motivation"
    if t in {"WorkPackage","Deliverable","ImplementationEvent","Plateau","Gap"}: return "migration"
    if t in {"Capability","Resource","ValueStream","CourseOfAction"}: return "strategy"
    return "other"


def generated_view(repo: dict, preset: str, project: str | None = None) -> dict:
    elements=repo.get("elements") or []; relationships=repo.get("relationships") or []
    if project: elements=[e for e in elements if e.get("project_id")==project]
    if preset == "portfolio":
        chosen=elements
    elif preset == "lifecycle":
        chosen=[e for e in elements if e.get("lifecycle_state") in ("transition","deprecated","retiring","retired")]
    elif preset == "security":
        words=("security","identity","access","risk","control","trust","privacy","resilien","certificate","secret")
        chosen=[e for e in elements if any(w in (e.get("name","")+" "+e.get("description","")).lower() for w in words)]
    else:
        chosen=[e for e in elements if type_group(e.get("type",""))==preset]
    ids={e["id"] for e in chosen}; rels=[r for r in relationships if r.get("source") in ids and r.get("target") in ids]
    title_map={"business":"Business architecture","application":"Application architecture","technology":"Technology architecture","data":"Information & data architecture","security":"Security-relevant architecture","motivation":"Motivation & requirements","migration":"Implementation & migration","portfolio":"Portfolio dependency view","lifecycle":"Lifecycle / decommission impact"}
    pid=project or "portfolio"
    return {"id":f"view-{preset}-{pid}","name":title_map.get(preset,preset.title()),"viewpoint":{"business":"Organization","application":"Application Cooperation","technology":"Technology","data":"Information Structure","motivation":"Motivation","migration":"Implementation and Migration"}.get(preset,"Custom"),"purpose":"Generated from the canonical 26.10 repository without adding model facts.","audience":["Architecture stakeholders"],"project_ids":[project] if project else sorted({e.get("project_id") for e in chosen if e.get("project_id")}),"element_refs":[e["id"] for e in chosen],"relationship_refs":[r["id"] for r in rels],"include_retired":preset=="lifecycle","generated":True}


def render_view_svg(repo: dict, view: dict, out: Path) -> None:
    # Self-contained deterministic renderer; layout is presentation-only, not semantic.
    eidx=index_by(repo.get("elements") or []); ridx=index_by(repo.get("relationships") or [])
    refs=[x for x in view.get("element_refs",[]) if x in eidx]
    cols=max(1,math.ceil(math.sqrt(len(refs) or 1))); W,H,hg,vg=190,70,60,60
    pos={ref:(50+(i%cols)*(W+hg),90+(i//cols)*(H+vg)) for i,ref in enumerate(refs)}
    width=max(900,100+cols*(W+hg)); rows=max(1,math.ceil(len(refs)/cols)); height=max(450,160+rows*(H+vg))
    esc=lambda s: html.escape(str(s),quote=True)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#444"/></marker></defs><style>text{{font-family:Arial,sans-serif;fill:#111}}.node{{fill:#fff;stroke:#444;stroke-width:1.5}}.edge{{stroke:#555;stroke-width:1.4;marker-end:url(#arrow)}}</style><text x="50" y="38" font-size="24" font-weight="bold">{esc(view.get("name"))}</text><text x="50" y="62" font-size="12">View ID {esc(view.get("id"))} · repository {esc(repo.get("repository",{}).get("revision_hash","")[:16])}</text>']
    relrefs=view.get("relationship_refs") or [r["id"] for r in repo.get("relationships",[]) if r.get("source") in pos and r.get("target") in pos]
    for rid in relrefs:
        r=ridx.get(rid)
        if not r or r.get("source") not in pos or r.get("target") not in pos: continue
        x1,y1=pos[r["source"]]; x2,y2=pos[r["target"]]; x1+=W/2; y1+=H/2; x2+=W/2; y2+=H/2
        parts.append(f'<line class="edge" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/><text x="{(x1+x2)/2}" y="{(y1+y2)/2-6}" font-size="10">{esc(r.get("type"))}</text>')
    for ref in refs:
        e=eidx[ref]; x,y=pos[ref]
        parts.append(f'<rect class="node" x="{x}" y="{y}" width="{W}" height="{H}" rx="8"/><text x="{x+10}" y="{y+24}" font-size="13" font-weight="bold">{esc(e.get("name"))}</text><text x="{x+10}" y="{y+43}" font-size="10">{esc(e.get("type"))} · {esc(e.get("project_id"))}</text><text x="{x+10}" y="{y+58}" font-size="9">{esc(e.get("lifecycle_state","active"))}</text>')
    parts.append('</svg>'); out.write_text(''.join(parts),encoding='utf-8')


def generate_views(repo: dict, outdir: Path, project: str | None, preset: str) -> list[dict]:
    outdir.mkdir(parents=True,exist_ok=True)
    presets=["business","application","technology","data","security","motivation","migration","portfolio","lifecycle"] if preset=="all" else [preset]
    produced=[]
    for p in presets:
        v=generated_view(repo,p,project)
        if not v["element_refs"]: continue
        write_json(outdir/f"{v['id']}.json",v); render_view_svg(repo,v,outdir/f"{v['id']}.svg"); produced.append(v)
    manifest={"schema_version":RELEASE,"repository_id":repo.get("repository",{}).get("id"),"repository_revision":repo.get("repository",{}).get("revision_hash"),"generated_at":now_utc(),"views":[{"id":v["id"],"name":v["name"],"json":f"{v['id']}.json","svg":f"{v['id']}.svg"} for v in produced]}
    write_json(outdir/"view-set.json",manifest)
    return produced


def impact(repo: dict, element_id: str) -> dict:
    es=index_by(repo.get("elements") or []); rs=repo.get("relationships") or []
    if element_id not in es: raise ValueError(f"unknown element {element_id}")
    inbound=[r for r in rs if r.get("target")==element_id]; outbound=[r for r in rs if r.get("source")==element_id]
    neighbors=[]
    for r in inbound+outbound:
        other=r.get("source") if r.get("target")==element_id else r.get("target")
        if other in es: neighbors.append({"relationship":r.get("id"),"type":r.get("type"),"element":other,"name":es[other].get("name"),"project":es[other].get("project_id"),"lifecycle":es[other].get("lifecycle_state")})
    projects=sorted({x["project"] for x in neighbors if x.get("project")})
    views=[v.get("id") for v in repo.get("views",[]) if element_id in (v.get("element_refs") or [])]
    return {"element":es[element_id],"inbound":inbound,"outbound":outbound,"neighbors":neighbors,"impacted_projects":projects,"views":views}


def portfolio_data(repo: dict) -> dict:
    ps=index_by(repo.get("projects") or []); es=index_by(repo.get("elements") or []); rs=repo.get("relationships") or []
    deps=[]
    for r in rs:
        s=es.get(r.get("source")); t=es.get(r.get("target"))
        if s and t and s.get("project_id")!=t.get("project_id"):
            deps.append({"relationship":r.get("id"),"type":r.get("type"),"from_project":s.get("project_id"),"from_element":s.get("id"),"to_project":t.get("project_id"),"to_element":t.get("id"),"owner":r.get("owner")})
    projects=[]
    for p in repo.get("projects",[]):
        pe=[e for e in repo.get("elements",[]) if e.get("project_id")==p.get("id")]
        projects.append({"id":p.get("id"),"name":p.get("name"),"owner":p.get("owner"),"status":p.get("status"),"element_count":len(pe),"retiring_or_retired":sum(1 for e in pe if e.get("lifecycle_state") in ("retiring","retired")),"benefits":p.get("benefits",[])})
    blockers=[]
    for e in repo.get("elements",[]):
        if e.get("lifecycle_state") in ("retiring","retired"):
            imp=impact(repo,e["id"])
            active=[n for n in imp["neighbors"] if n["relationship"] in {r.get("id") for r in imp["inbound"]} and n.get("lifecycle") not in ("retired","reference")]
            if active: blockers.append({"element":e["id"],"project":e.get("project_id"),"dependencies":active})
    return {"repository":repo.get("repository"),"projects":projects,"cross_project_dependencies":deps,"portfolio_links":repo.get("portfolio_links",[]),"decommission_blockers":blockers}


def portfolio_markdown(data: dict) -> str:
    out=[f"# Portfolio architecture — {data.get('repository',{}).get('name','')}","",f"Repository revision: `{data.get('repository',{}).get('revision_hash','')}`","","## Projects","","| Project | Owner | Status | Elements | Retiring/retired | Benefits |","| --- | --- | --- | ---: | ---: | ---: |"]
    for p in data.get("projects",[]): out.append(f"| {p['id']} — {p['name']} | {p.get('owner','')} | {p.get('status','')} | {p.get('element_count',0)} | {p.get('retiring_or_retired',0)} | {len(p.get('benefits') or [])} |")
    out += ["","## Cross-project dependencies","","| Relationship | Type | From | To | Owner |","| --- | --- | --- | --- | --- |"]
    for d in data.get("cross_project_dependencies",[]): out.append(f"| {d['relationship']} | {d['type']} | {d['from_project']}:{d['from_element']} | {d['to_project']}:{d['to_element']} | {d.get('owner','')} |")
    out += ["","## Decommission blockers",""]
    if not data.get("decommission_blockers"): out.append("None detected.")
    for b in data.get("decommission_blockers",[]): out.append(f"- **{b['element']}** ({b['project']}): {len(b['dependencies'])} active dependency/dependencies")
    out.append("")
    return "\n".join(out)


def set_lifecycle(repo: dict, element_id: str, state: str, owner: str, when: str | None = None) -> None:
    if state not in LIFECYCLE_STATES: raise ValueError(f"invalid lifecycle state {state}")
    es=index_by(repo.get("elements") or [])
    if element_id not in es: raise ValueError(f"unknown element {element_id}")
    e=es[element_id]; e["lifecycle_state"]=state; e["lifecycle_owner"]=owner; e["lifecycle_changed_at"]=when or date.today().isoformat()
    if state=="retired": e["valid_to"]=when or date.today().isoformat()
    touch(repo)


def decommission(repo: dict, element_id: str, owner: str, when: str, waiver: str | None = None) -> list[str]:
    es=index_by(repo.get("elements") or []); rs=repo.get("relationships") or []
    if element_id not in es: raise ValueError(f"unknown element {element_id}")
    blockers=[]
    for r in rs:
        if r.get("target")!=element_id: continue
        src=es.get(r.get("source"))
        if src and src.get("lifecycle_state") not in ("retired","reference"):
            blockers.append(f"{r.get('id')}: active {src.get('id')} -> {element_id}")
    if blockers and not waiver:
        raise ValueError("decommission blocked by active dependencies: " + "; ".join(blockers))
    e=es[element_id]; e["lifecycle_state"]="retired"; e["valid_to"]=when; e["lifecycle_owner"]=owner; e["decommissioned_at"]=when
    if waiver:
        repo.setdefault("exceptions",[]).append({"id":f"EX-{hashlib.sha1((element_id+when+waiver).encode()).hexdigest()[:10]}","type":"decommission-waiver","element_id":element_id,"owner":owner,"date":when,"rationale":waiver,"blockers":blockers})
    touch(repo); return blockers


def self_test() -> int:
    tests=[]
    def ok(name,cond): tests.append((name,bool(cond)))
    repo=empty_repository("repo-test","26.10 Test Repository")
    repo["projects"]=[
        {"id":"P1","name":"Customer Portal","owner":"Business Owner A","status":"delivery","benefits":[{"id":"B1","name":"Reduce service effort","owner":"Benefit Owner","measure":"Minutes/case","baseline":"12","target":"7","status":"baselined"}],"artifacts":[]},
        {"id":"P2","name":"Identity Modernisation","owner":"Business Owner B","status":"delivery","benefits":[],"artifacts":[]},
    ]
    repo["elements"]=[
        {"id":"e-portal","type":"ApplicationComponent","name":"Customer Portal","project_id":"P1","owner":"App Owner","lifecycle_state":"active","horizon":"target","benefit_refs":["B1"],"artifact_refs":[],"source_refs":[]},
        {"id":"e-idp","type":"ApplicationComponent","name":"Identity Provider","project_id":"P2","owner":"IAM Owner","lifecycle_state":"active","horizon":"target","benefit_refs":[],"artifact_refs":[],"source_refs":[]},
        {"id":"e-actor","type":"BusinessActor","name":"Customer","project_id":"P1","owner":"Business Owner A","lifecycle_state":"active","horizon":"current","benefit_refs":[],"artifact_refs":[],"source_refs":[]},
        {"id":"e-old","type":"ApplicationComponent","name":"Legacy Login","project_id":"P2","owner":"IAM Owner","lifecycle_state":"retiring","horizon":"current","benefit_refs":[],"artifact_refs":[],"source_refs":[]},
    ]
    repo["relationships"]=[
        {"id":"r-use","type":"Serving","source":"e-idp","target":"e-portal","project_id":"P2","owner":"Integration Owner","lifecycle_state":"active"},
        {"id":"r-actor","type":"Serving","source":"e-portal","target":"e-actor","project_id":"P1","owner":"App Owner","lifecycle_state":"active"},
        {"id":"r-old","type":"Serving","source":"e-old","target":"e-portal","project_id":"P2","owner":"IAM Owner","lifecycle_state":"active"},
    ]
    repo["portfolio_links"]=[{"id":"pl-1","from_project":"P2","to_project":"P1","type":"shared-service-dependency","owner":"Enterprise Architect","status":"active","element_refs":["e-idp","e-portal"]}]
    repo["views"]=[{"id":"v-app","name":"Application cooperation","viewpoint":"Application Cooperation","purpose":"Decision support","audience":["ARB"],"project_ids":["P1","P2"],"element_refs":["e-portal","e-idp","e-old"],"relationship_refs":["r-use","r-old"],"include_retired":False}]
    touch(repo)
    errs,warns=validate_repository(repo); ok("repository-valid",not errs); ok("revision-hash-64",len(repository_hash(repo))==64)
    ok("portfolio-dependency",len(portfolio_data(repo)["cross_project_dependencies"])>=1)
    ok("impact-project", "P2" in impact(repo,"e-portal")["impacted_projects"])
    try:
        decommission(repo,"e-portal","Owner","2030-01-01"); blocked=False
    except ValueError: blocked=True
    ok("decommission-blocks-active-dependency",blocked)
    blockers=decommission(repo,"e-portal","Owner","2030-01-01","Approved migration waiver")
    ok("decommission-waiver-recorded",bool(blockers) and repo["elements"][0]["lifecycle_state"]=="retired" and repo["exceptions"])
    # reset target for exchange validity check
    repo["elements"][0]["lifecycle_state"]="active"; repo["elements"][0].pop("valid_to",None); touch(repo)
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); xmlp=td/"model.xml"; export_open_exchange(repo,xmlp,lang="en",include_views=True)
        text=xmlp.read_text(encoding="utf-8"); ok("exchange-created",xmlp.stat().st_size>500); ok("exchange-namespace",ARCHI_NS in text); ok("exchange-elements","<elements>" in text); ok("exchange-relationships","<relationships>" in text); ok("exchange-views","<views>" in text and 'xsi:type="Diagram"' in text)
        repo2=empty_repository("repo-import","Imported"); import_open_exchange(xmlp,repo2,project_id="P-IMP",project_name="Imported",merge=False)
        e2,w2=validate_repository(repo2); ok("exchange-import-valid",not e2); ok("roundtrip-element-count",len(repo2["elements"])==len(repo["elements"])); ok("roundtrip-relationship-count",len(repo2["relationships"])==len(repo["relationships"])); ok("roundtrip-view-count",len(repo2["views"])==len(repo["views"])); ok("roundtrip-repository-id",{e['id'] for e in repo2['elements']}=={e['id'] for e in repo['elements']})
        vd=td/"views"; views=generate_views(repo,vd,None,"all"); ok("generated-multiview",len(views)>=3 and (vd/"view-set.json").is_file()); ok("generated-svg",any(vd.glob("*.svg")))
        md=portfolio_markdown(portfolio_data(repo)); ok("portfolio-markdown","Cross-project dependencies" in md and "P1" in md)
    errs2,warns2=validate_repository(repo); ok("post-ops-valid",not errs2)
    for name,res in tests: print(("PASS" if res else "FAIL"),name)
    passed=sum(1 for _,x in tests if x); print(f"{passed}/{len(tests)} PASS"); return 0 if passed==len(tests) else 1


def main() -> None:
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest="cmd",required=True)
    p=sp.add_parser("init"); p.add_argument("path"); p.add_argument("--id",required=True); p.add_argument("--name",required=True)
    p=sp.add_parser("validate"); p.add_argument("path"); p.add_argument("--strict",action="store_true")
    p=sp.add_parser("project-set"); p.add_argument("path"); p.add_argument("project_id"); p.add_argument("--name",required=True); p.add_argument("--owner",required=True); p.add_argument("--status",default="proposed",choices=sorted(PROJECT_STATES))
    p=sp.add_parser("element-set"); p.add_argument("path"); p.add_argument("element_id"); p.add_argument("--type",required=True); p.add_argument("--name",required=True); p.add_argument("--project",required=True); p.add_argument("--owner",required=True); p.add_argument("--state",default="active",choices=sorted(LIFECYCLE_STATES)); p.add_argument("--horizon",default="unspecified",choices=sorted(HORIZONS)); p.add_argument("--description",default="")
    p=sp.add_parser("relationship-set"); p.add_argument("path"); p.add_argument("relationship_id"); p.add_argument("--type",required=True); p.add_argument("--source",required=True); p.add_argument("--target",required=True); p.add_argument("--project"); p.add_argument("--owner",default=""); p.add_argument("--name",default="")
    p=sp.add_parser("view-set"); p.add_argument("path"); p.add_argument("view_id"); p.add_argument("--name",required=True); p.add_argument("--viewpoint",default="Custom"); p.add_argument("--elements",required=True); p.add_argument("--relationships",default=""); p.add_argument("--projects",default=""); p.add_argument("--purpose",default="Architecture decision support"); p.add_argument("--audience",default="Architecture stakeholders"); p.add_argument("--include-retired",action="store_true")
    p=sp.add_parser("benefit-set"); p.add_argument("path"); p.add_argument("project_id"); p.add_argument("benefit_id"); p.add_argument("--name",required=True); p.add_argument("--owner",required=True); p.add_argument("--measure",required=True); p.add_argument("--baseline",required=True); p.add_argument("--target",required=True); p.add_argument("--status",default="planned",choices=sorted(BENEFIT_STATES))
    p=sp.add_parser("lifecycle-set"); p.add_argument("path"); p.add_argument("element_id"); p.add_argument("state",choices=sorted(LIFECYCLE_STATES)); p.add_argument("--owner",required=True); p.add_argument("--date")
    p=sp.add_parser("decommission"); p.add_argument("path"); p.add_argument("element_id"); p.add_argument("--owner",required=True); p.add_argument("--date",required=True); p.add_argument("--waiver")
    p=sp.add_parser("impact"); p.add_argument("path"); p.add_argument("element_id")
    p=sp.add_parser("portfolio"); p.add_argument("path"); p.add_argument("--format",choices=["md","json"],default="md"); p.add_argument("--out")
    p=sp.add_parser("generate-views"); p.add_argument("path"); p.add_argument("--out",required=True); p.add_argument("--project"); p.add_argument("--preset",default="all",choices=["all","business","application","technology","data","security","motivation","migration","portfolio","lifecycle"])
    p=sp.add_parser("export-open-exchange"); p.add_argument("path"); p.add_argument("--out",required=True); p.add_argument("--project"); p.add_argument("--language",default="en"); p.add_argument("--no-views",action="store_true")
    p=sp.add_parser("import-open-exchange"); p.add_argument("xml"); p.add_argument("--repo",required=True); p.add_argument("--project-id"); p.add_argument("--project-name"); p.add_argument("--merge",action="store_true")
    sp.add_parser("self-test")
    a=ap.parse_args()
    if a.cmd=="self-test": raise SystemExit(self_test())
    if a.cmd=="init":
        p=resolve_repo(a.path); p.parent.mkdir(parents=True,exist_ok=True)
        if p.exists(): raise SystemExit(f"error: repository already exists: {p}")
        repo=empty_repository(a.id,a.name); write_json(p,repo); print(p); return
    p,repo=load_repo(a.path) if a.cmd not in ("import-open-exchange",) else (resolve_repo(a.repo), load_json(resolve_repo(a.repo)) if resolve_repo(a.repo).is_file() else empty_repository("repo-import",a.project_name or "Imported repository"))
    if a.cmd=="validate":
        errs,warns=validate_repository(repo,a.strict); [print("WARN",x) for x in warns]; [print("FAIL",x) for x in errs]; print(f"{'PASS' if not errs else 'FAIL'} errors={len(errs)} warnings={len(warns)} revision={repository_hash(repo)}"); raise SystemExit(1 if errs else 0)
    if a.cmd=="project-set": upsert(repo.setdefault("projects",[]),{"id":a.project_id,"name":a.name,"owner":a.owner,"status":a.status,"benefits":[],"artifacts":[]}); save_repo(p,repo); print("OK",a.project_id); return
    if a.cmd=="element-set":
        if a.project not in index_by(repo.get("projects") or []): raise SystemExit(f"error: project not found: {a.project}")
        upsert(repo.setdefault("elements",[]),{"id":a.element_id,"type":a.type,"name":a.name,"project_id":a.project,"owner":a.owner,"lifecycle_state":a.state,"horizon":a.horizon,"description":a.description,"properties":{},"artifact_refs":[],"benefit_refs":[],"source_refs":[]}); save_repo(p,repo); print("OK",a.element_id); return
    if a.cmd=="relationship-set": upsert(repo.setdefault("relationships",[]),{"id":a.relationship_id,"type":a.type,"source":a.source,"target":a.target,"project_id":a.project,"owner":a.owner,"name":a.name,"lifecycle_state":"active","properties":{}}); save_repo(p,repo); print("OK",a.relationship_id); return
    if a.cmd=="view-set": upsert(repo.setdefault("views",[]),{"id":a.view_id,"name":a.name,"viewpoint":a.viewpoint,"purpose":a.purpose,"audience":split_csv(a.audience),"project_ids":split_csv(a.projects),"element_refs":split_csv(a.elements),"relationship_refs":split_csv(a.relationships),"include_retired":a.include_retired}); save_repo(p,repo); print("OK",a.view_id); return
    if a.cmd=="benefit-set":
        pr=index_by(repo.get("projects") or []).get(a.project_id)
        if not pr: raise SystemExit(f"error: project not found: {a.project_id}")
        upsert(pr.setdefault("benefits",[]),{"id":a.benefit_id,"name":a.name,"owner":a.owner,"measure":a.measure,"baseline":a.baseline,"target":a.target,"status":a.status}); save_repo(p,repo); print("OK",a.benefit_id); return
    if a.cmd=="lifecycle-set": set_lifecycle(repo,a.element_id,a.state,a.owner,a.date); save_repo(p,repo); print("OK",a.element_id,a.state); return
    if a.cmd=="decommission":
        try: blockers=decommission(repo,a.element_id,a.owner,a.date,a.waiver)
        except ValueError as e: print("FAIL",e); raise SystemExit(2)
        save_repo(p,repo); print("OK",a.element_id,"retired",f"waived_blockers={len(blockers)}" if blockers else "no_blockers"); return
    if a.cmd=="impact": print(json.dumps(impact(repo,a.element_id),indent=2,ensure_ascii=False)); return
    if a.cmd=="portfolio":
        d=portfolio_data(repo); txt=json.dumps(d,indent=2,ensure_ascii=False)+"\n" if a.format=="json" else portfolio_markdown(d)
        if a.out: Path(a.out).write_text(txt,encoding="utf-8")
        else: print(txt,end="")
        return
    if a.cmd=="generate-views": views=generate_views(repo,Path(a.out),a.project,a.preset); print(f"OK views={len(views)} out={a.out}"); return
    if a.cmd=="export-open-exchange": export_open_exchange(repo,Path(a.out),a.project,a.language,not a.no_views); print(f"OK {a.out}"); return
    if a.cmd=="import-open-exchange":
        try: import_open_exchange(Path(a.xml),repo,a.project_id,a.project_name,a.merge)
        except ValueError as e: print("FAIL",e); raise SystemExit(2)
        save_repo(p,repo); print(f"OK {p}"); return

if __name__=="__main__": main()
