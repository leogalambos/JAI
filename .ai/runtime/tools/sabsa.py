#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""SABSA library tool: build, check and report a security architecture that traces to the business.

A SABSA library is a folder of small Markdown entries, one per element, each with front matter. Element types,
relations, canonical cells and business-justification edges are defined by the versioned declarative metamodel in
`runtime/sabsa/schema/elements.json`; trace views are defined separately in `views.json`. The
structure follows SABSA's layered views; the rule it enforces is SABSA's own discipline: every element
must trace upward to a business driver, and every business attribute must be measurable.

    Contextual          BD driver           why the business needs security at all
                        RO risk/opportunity what threatens or enables the business, and which attribute it touches
    Conceptual          BA attribute        what "secure" means here, with a metric and a target (the profile)
                        CO control objective what must hold, for which attributes and risks
                        DM domain           a scope of authority, and its trust relationships
    Logical             SS security service what is provided, meeting which objectives
    Physical            SM mechanism        how a service is realised
    Component           SC component        which product, standard or tool
    Service Management  SO operation        how an attribute is measured in operation

Every layer also answers six questions — what, why, how, who, where, when — in matrix/<layer>-<question>.md,
so the 36 cells of the SABSA matrix are each answered or explicitly marked not applicable.

Upward links are required (an attribute cites drivers; a service cites objectives; ...). Downward gaps
(a driver no attribute serves, an attribute nothing measures) are what `suggest` reports.

    sabsa.py init     LIB --name N --organisation O --scope S --owner W
    sabsa.py new      LIB TYPE --title T [--set field=value ...]
    sabsa.py check    LIB [--json]             integrity, traceability, measurability (exit 1 on errors)
    sabsa.py suggest  LIB                      ranked gaps, each with the concrete next step
    sabsa.py trace    LIB ID                   upward chain to drivers, downward dependents (impact)
    sabsa.py view     LIB VIEW                 typed trace view (realisation, assurance, policy, trust, roadmap)
    sabsa.py metamodel                           show the active declarative metamodel and lifecycle schema
    sabsa.py lifecycle LIB [ID]                  show current/transition/target and lifecycle state
    sabsa.py lifecycle-set LIB ID [options]      change lifecycle/horizon metadata with transition validation
    sabsa.py overlay-init LIB --id ...           create a framework mapping overlay skeleton
    sabsa.py overlays LIB                        validate/report external framework mappings
    sabsa.py reuse-add LIB ALIAS PATH             add a namespaced reusable SABSA library dependency
    sabsa.py reuse LIB                           report cross-library reuse and source approvals
    sabsa.py report   LIB                      matrix coverage, traceability and measurement tables
    sabsa.py matrix   LIB [--scaffold]         the 6 x 6 matrix: which cells are answered, open or not applicable
    sabsa.py migrate  LIB                      move elements of an older library to where SABSA places them
    sabsa.py sources  LIB                      intake files in 00-sources/ and which elements cite each
    sabsa.py questions LIB                     assumptions to confirm, written as questions for the client
    sabsa.py approve   LIB --by PERSON [--note TEXT] owner-approve the exact clean architecture snapshot
    sabsa.py approval  LIB                     verify whether the current snapshot still matches the approval
    sabsa.py document LIB [--out FILE.md|.docx|.html|.pdf] [--template-name N] [--template F] [--reference DOCX]
                                               render a document from a template (default: the architecture)
    sabsa.py documents LIB                     list specialised document views and intended audiences
    sabsa.py template LIB [--name N] [--init | --fields | --check FILE]
                                               which template applies; copy the default to edit; list fields
    sabsa.py selftest

SABSA is a framework of the SABSA Institute. Its business attribute taxonomy and definitions are not
reproduced here: define attributes in your organisation's terms, or from your licensed SABSA material.
"""
import argparse
import json
import signal
import os
import hashlib
import datetime
import re
import sys
import tempfile
from collections import defaultdict
for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
# Under a non-UTF-8 locale, arguments arrive surrogate-escaped; recover the real characters (a no-op otherwise).
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]

ASPECTS = {"what": "Assets", "why": "Motivation", "how": "Process", "who": "People",
           "where": "Location", "when": "Time"}
LAYERS = ["Contextual", "Conceptual", "Logical", "Physical", "Component", "Service Management"]
SCHEMA_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sabsa", "schema")
REUSE_FILE = "reuse.json"
OVERLAYS_DIR = "overlays"
PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
RELEASE = open(os.path.join(PACKAGE_ROOT, "VERSION"), encoding="utf-8").read().strip()
SABSA_JAI_PROFILE = "sabsa"
SABSA_JAI_LAYER = "2"


def _load_lifecycle_model():
    path = os.path.join(SCHEMA_ROOT, "lifecycle.json")
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot load SABSA lifecycle model {path}: {exc}") from exc
    horizons = tuple(doc.get("horizons", ()))
    states = tuple(doc.get("lifecycle_states", ()))
    transitions = {k: tuple(v) for k, v in doc.get("transitions", {}).items()}
    if not horizons or not states:
        raise RuntimeError(f"{path}: horizons and lifecycle_states must be non-empty")
    for st in states:
        if st not in transitions:
            transitions[st] = ()
        for nxt in transitions[st]:
            if nxt not in states:
                raise RuntimeError(f"{path}: transition {st}->{nxt} names an unknown lifecycle state")
    return doc.get("schema_version", "unknown"), horizons, states, transitions

LIFECYCLE_VERSION, ARCH_HORIZONS, LIFECYCLE_STATES, LIFECYCLE_TRANSITIONS = _load_lifecycle_model()
COMMON_FIELDS = ("horizon", "lifecycle_state", "valid_from", "valid_until", "predecessors", "transition_items")

def _load_metamodel():
    path = os.path.join(SCHEMA_ROOT, "elements.json")
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot load SABSA metamodel {path}: {exc}") from exc
    raw = doc.get("element_types")
    if not isinstance(raw, dict) or not raw:
        raise RuntimeError(f"{path}: element_types must be a non-empty object")
    out = {}
    prefixes = set()
    for name, spec in raw.items():
        required_keys = ("prefix", "dir", "layer", "aspect", "fields", "required", "links", "business_parent")
        missing = [k for k in required_keys if k not in spec]
        if missing:
            raise RuntimeError(f"{path}: {name}: missing {', '.join(missing)}")
        if spec["prefix"] in prefixes:
            raise RuntimeError(f"{path}: duplicate prefix {spec['prefix']}")
        prefixes.add(spec["prefix"])
        links = {}
        for field, rel in spec.get("links", {}).items():
            links[field] = (rel["target"], bool(rel.get("required")))
        out[name] = dict(spec)
        out[name]["fields"] = tuple(spec.get("fields", ())) + tuple(f for f in COMMON_FIELDS if f not in spec.get("fields", ()))
        out[name]["required"] = tuple(spec.get("required", ()))
        out[name]["links"] = links
        out[name]["business_parent"] = tuple(spec.get("business_parent", ()))
    for name, spec in out.items():
        for field, (target, _) in spec["links"].items():
            if target not in out:
                raise RuntimeError(f"{path}: {name}.{field}: unknown target type {target}")
        if spec["layer"] not in LAYERS:
            raise RuntimeError(f"{path}: {name}: unknown layer {spec['layer']}")
        if spec["aspect"] not in ASPECTS:
            raise RuntimeError(f"{path}: {name}: unknown aspect {spec['aspect']}")
    return doc.get("schema_version", "unknown"), out

METAMODEL_VERSION, TYPES = _load_metamodel()
DEFAULT_ASPECT = {name: spec["aspect"] for name, spec in TYPES.items()}
for _t in TYPES.values():
    _t["fields"] = tuple(f for f in _t["fields"] if f != "source") + ("source", "basis")
BASES = ("stated", "inferred", "assumed")
ELEMENT_STATUSES = ("draft", "reviewed", "approved")
SOURCES_DIR = "00-sources"
APPROVAL_DIR = ".sabsa"
APPROVAL_FILE = "approval.json"
BY_PREFIX = {t["prefix"]: k for k, t in TYPES.items()}
ID_RE = re.compile(r"^(" + "|".join(re.escape(p) for p in sorted(BY_PREFIX, key=len, reverse=True)) + r")-(\d{3,4})$")
PLACEHOLDER = re.compile(r"(<[^>]+>|\bTBD\b|\bTODO\b|\?\?\?)")
GUIDE = {
    "statement": "One sentence, in business language: what the business needs or what could happen.",
    "source": "Which client material this comes from: 00-sources/<file>[#section], or a URL. Comma-separate several.",
    "basis": "stated (the client said so) | inferred (follows from what they said) | assumed (to confirm)",
    "category": "Your attribute category (e.g. from your licensed SABSA taxonomy, or your own).",
    "definition": "What this attribute means in THIS organisation, precisely enough to disagree with.",
    "metric": "What is measured.", "measurement": "How, from which source, how often.",
    "target": "The threshold that counts as meeting it.",
    "kind": "threat or opportunity", "likelihood": "low | medium | high", "impact": "low | medium | high",
    "scope": "What this domain covers.", "authority": "Who sets policy within it.",
    "description": "What this provides, in the terms of the layer.", "policy": "The rule the service enforces.",
    "product": "Product, standard or tool, with version where it matters.",
    "configuration": "Settings that matter for the mechanism.", "frequency": "How often it is measured.",
    "threshold_action": "What happens when the target is missed.", "owner": "A named person or role.",
}
GUIDE.update({
    "rationale": "Why this choice exists and which trade-off it resolves.",
    "verification": "How achievement of this objective will be demonstrated.",
    "purpose": "Why the relationship or artefact exists in business/security terms.",
    "trust_basis": "Why the relying party is justified in trusting the other party.",
    "assurance_requirement": "Evidence or assurance required before trust is accepted.",
    "expiry": "Date or condition after which this approval/trust/exception is invalid.",
    "horizon": "Architecture horizon: current | transition | target | reference.",
    "lifecycle_state": "Lifecycle state: proposed | reviewed | approved | implemented | operational | deprecated | retired.",
    "valid_from": "Date/condition from which this element applies.",
    "valid_until": "Date/condition after which this element no longer applies.",
    "predecessors": "Same-type predecessor IDs this target/transition element replaces or evolves from.",
    "transition_items": "Roadmap (RM) IDs that move predecessor/current state toward this element.",
    "decision": "The architecture decision that was made.",
    "decision_date": "Date of the decision (ISO 8601 recommended).",
    "effective_date": "Date from which the policy applies.",
    "review_date": "Next mandatory review date.",
    "population": "People, systems, services or organisations represented by this entity.",
    "lifecycle": "Creation, change, suspension and retirement rules.",
    "privileges": "Allowed actions/capabilities; keep least privilege explicit.",
    "conditions": "Conditions, context or separation-of-duties constraints on privilege.",
    "information": "Information exchanged or stored by this flow.",
    "classification": "Business/security classification of the information.",
    "protection": "Protection required in transit, processing and storage.",
    "service_level": "Security service level / SLO relevant to this service.",
    "version": "Version/revision of an external standard or product where material.",
    "requirement": "The normative requirement this standard imposes.",
    "calculation": "Exact calculation/aggregation used for the measure.",
    "unit": "Unit of measure.",
    "data_source": "System of record or collection source for this measure.",
    "warning_threshold": "Early-warning threshold before target breach.",
    "breach_threshold": "Threshold that constitutes a breach/failure.",
    "evidence_retention": "Retention period/location required for assurance evidence.",
    "evidence_type": "Evidence class, e.g. log extract, test result, attestation, audit record.",
    "location": "Immutable or controlled location of the evidence.",
    "collector": "Role/system that produced or collected the evidence.",
    "collected_at": "Collection timestamp or period.",
    "result": "Observed result/conclusion represented by the evidence.",
    "risk_acceptance": "Explicit residual-risk acceptance and decision authority.",
    "expires": "Expiry date after which the exception is invalid unless renewed.",
    "current_state": "Current architecture/control state.",
    "target_state": "Target architecture/control state.",
    "target_date": "Target completion date/milestone.",
    "acceptance_evidence": "Evidence required to declare the roadmap item complete.",
    "criticality": "Business criticality or impact if the process is unavailable or untrusted.",
    "actor_type": "Organisation, role, customer, supplier, regulator, system or other accountable actor class.",
    "accountability": "What this actor is accountable for in the architecture scope.",
    "jurisdiction": "Legal or regulatory jurisdiction relevant to this location.",
    "constraints": "Residency, legal, threat or operational constraints attached to the location.",
    "event": "Business event, cycle or deadline that creates the time dependency.",
    "deadline": "Concrete date/time or recurring deadline where known.",
    "tolerance": "Permitted timing deviation or business tolerance.",
    "subject": "Security object whose lifetime is constrained, e.g. session, key, certificate or record.",
    "lifetime": "Maximum/minimum lifetime or retention period and its unit.",
    "renewal": "Renewal, rotation, re-certification or expiry rule.",
    "relationship": "Association between security domains and what may cross the boundary.",
    "boundary": "Logical boundary, trust boundary or interface governed by the association.",
    "trigger": "Event that starts the process, procedure or control sequence.",
    "sequence": "Ordered steps or security processing sequence.",
    "review_cycle": "Periodic review or re-certification interval.",
    "technology": "Storage or platform technology and version where material.",
    "data_classes": "Information classes stored or processed here.",
    "retention": "Retention and disposal rule for the data store.",
    "procedure": "Operational or build procedure that implements the policy.",
    "endpoint_type": "Human, application, service, device or external-party endpoint.",
    "interface": "Interface through which the endpoint interacts with the system.",
    "platform": "Hosting platform, environment or infrastructure technology.",
    "network_zone": "Network/security zone or segmentation context.",
    "timing": "Ordering, latency, timeout or execution-time constraint.",
    "failure_action": "Action taken if the control sequence cannot complete as designed.",
    "schema": "Schema, fields or message structure that has security significance.",
    "encoding": "Encoding/serialisation and canonicalisation requirements.",
    "validation": "Validation rules applied to the format.",
    "principal": "User, workload, service or machine identity receiving the entitlement.",
    "entitlement": "Concrete access right, group, role or permission assigned to the principal.",
    "endpoint": "Node or endpoint name / function.",
    "address": "Address, URI, subnet or other locator where material.",
    "port": "Network or service port where applicable.",
    "protocol": "Protocol and security profile/version.",
    "timeout": "Timeout or expiry value at component level.",
    "schedule": "Recurring or event-driven schedule for the component/control.",
    "rotation_interval": "Rotation, renewal or replacement interval.",
    "support_scope": "Users, applications, services and activities covered by the support model.",
    "support_hours": "Support hours, on-call coverage and availability expectations.",
    "escalation_path": "Escalation route and authority chain.",
    "operational_controls": "Controls required to keep the site/platform secure in operation.",
    "maintenance_owner": "Role accountable for maintenance of the location/platform."
})


# ------------------------------------------------------------------------------------- the matrix
# Six layers (SABSA's views) crossed with six questions. Each cell's question is written here in plain words;
# SABSA Institute cell titles can be used instead in your own template, if you hold the licensed material.
LAYER_KEYS = ["contextual", "conceptual", "logical", "physical", "component", "service-management"]
LAYER_INFO = {
    "contextual": ("Contextual", "Business view",
                   "the business itself: what it does, why it needs security, and the constraints it works within"),
    "conceptual": ("Conceptual", "Architect's view",
                   "what security must achieve, expressed as attributes, objectives, strategies and domains"),
    "logical": ("Logical", "Designer's view",
                "the security services, policies, information and entities that deliver the concept"),
    "physical": ("Physical", "Builder's view",
                 "the mechanisms, rules, infrastructure and data structures that implement the design"),
    "component": ("Component", "Tradesman's view",
                  "the products, standards, identities and protocols that make up the mechanisms"),
    "service-management": ("Service Management", "Service manager's view",
                           "how security is operated, measured, supported and kept current"),
}
INTERROGATIVE = {"what": "What", "why": "Why", "how": "How", "who": "Who", "where": "Where", "when": "When"}
QUESTIONS = {
 ("contextual", "what"): ("Which business assets, goals and decisions does security protect or enable?",
                          "Name the valuable things: revenue streams, data, brand, decisions the business must be able to make."),
 ("contextual", "why"):  ("Which business risks — threats and opportunities — matter, and why?",
                          "Both sides: what could go wrong, and what security makes possible that otherwise is not."),
 ("contextual", "how"):  ("Which business processes depend on security, and how?",
                          "The processes that create value, and where trust, integrity or availability is critical to them."),
 ("contextual", "who"):  ("Who is involved: the organisation, its governance, customers, partners and suppliers?",
                          "Roles and relationships, including third parties, and who is accountable for what."),
 ("contextual", "where"):("Where does the business operate: locations, jurisdictions, markets?",
                          "Geography matters for law, data residency and threat exposure."),
 ("contextual", "when"): ("When: which business cycles, deadlines and time dependencies constrain security?",
                          "Peak periods, reporting deadlines, contractual timescales, launch dates."),
 ("conceptual", "what"): ("What does 'secure' mean for this business — its attribute profile?",
                          "The business attributes, each with a definition, a metric and a target. Detailed in the attribute profile."),
 ("conceptual", "why"):  ("Why: which control objectives follow from the risks and attributes?",
                          "What must hold, for which attributes and risks, stated so that it can be tested."),
 ("conceptual", "how"):  ("How: which security strategies and architectural layering will meet the objectives?",
                          "The overall approach — defence in depth, zero trust, segmentation, assurance strategy — and why it fits."),
 ("conceptual", "who"):  ("Who: which entities are trusted, by whom, and on what basis?",
                          "The entity model and trust framework: people, systems, partners, and the trust between them."),
 ("conceptual", "where"):("Where: which security domains exist, and how do they relate?",
                          "Domains of authority and policy, and the trust relationships between them."),
 ("conceptual", "when"): ("When: which security lifetimes, deadlines and time limits apply?",
                          "Session lifetimes, key and certificate lifetimes, retention periods, recovery time objectives."),
 ("logical", "what"):    ("What information needs protecting, and how is it classified?",
                          "The information model: information assets, their classification and handling requirements."),
 ("logical", "why"):     ("Why: which security policies govern the information and services?",
                          "Policy statements the services enforce, traced to control objectives."),
 ("logical", "how"):     ("How: which logical security services deliver the objectives?",
                          "Identification, authentication, authorisation, audit, confidentiality, integrity, availability services."),
 ("logical", "who"):     ("Who: which entities, roles and privilege profiles exist?",
                          "The entity schema: roles, privilege profiles, separation of duties."),
 ("logical", "where"):   ("Where: how are the security domains defined and associated with each other?",
                          "Domain boundaries and the associations and interfaces between domains."),
 ("logical", "when"):    ("When: what is the security processing cycle?",
                          "When checks happen: at login, per transaction, periodically; review and re-certification cycles."),
 ("physical", "what"):   ("What data structures and stores hold the information?",
                          "The data model as built: databases, files, messages, and where each class of information resides."),
 ("physical", "why"):    ("Why: which security rules, practices and procedures apply?",
                          "The concrete rules and procedures that implement the policies."),
 ("physical", "how"):    ("How: which security mechanisms implement the services?",
                          "Encryption, access control, logging, monitoring, backup mechanisms, and how they are combined."),
 ("physical", "who"):    ("Who: which users, applications and interfaces interact with the system?",
                          "The people and systems at the edge, and the interfaces they use."),
 ("physical", "where"):  ("Where: which platforms and network infrastructure carry the system?",
                          "Hosting, networks, segmentation, and the physical and cloud locations."),
 ("physical", "when"):   ("When: in what order and at what times do the controls execute?",
                          "Control sequencing and timing: the order in which mechanisms act in a transaction or process."),
 ("component", "what"):  ("What detailed data structures and formats are used?",
                          "Schemas, fields, formats and encodings that matter for security."),
 ("component", "why"):   ("Why: which security standards apply to the components?",
                          "Standards, benchmarks and configuration baselines (e.g. CIS, ISO, vendor hardening guides)."),
 ("component", "how"):   ("How: which security products and tools are used?",
                          "Products, versions and configuration choices that matter."),
 ("component", "who"):   ("Who: which identities, functions and access rights are configured?",
                          "Accounts, service identities, groups, access control lists."),
 ("component", "where"): ("Where: which nodes, addresses, ports and protocols are involved?",
                          "The technical endpoints and protocols, and where each runs."),
 ("component", "when"):  ("When: what is the timing and sequencing of each security step?",
                          "Timeouts, schedules, rotation intervals, step order at the component level."),
 ("service-management", "what"): ("What assures operational continuity of security?",
                                  "Continuity and recovery of security services: backup, failover, recovery testing."),
 ("service-management", "why"):  ("Why: how is operational security risk managed?",
                                  "Operational risk management: monitoring, incident handling, risk reporting."),
 ("service-management", "how"):  ("How are security services managed and supported?",
                                  "Service management for security: change, problem, configuration, supplier management."),
 ("service-management", "who"):  ("Who is managed and supported, and how?",
                                  "User and application administration: joiners, movers, leavers, access reviews, support."),
 ("service-management", "where"):("Where: how are sites, networks and platforms kept secure in operation?",
                                  "Operational security of locations and infrastructure: patching, vulnerability management, physical security."),
 ("service-management", "when"): ("When: what is the security operations schedule?",
                                  "The calendar: reviews, audits, tests, reports, re-certifications, and who runs each."),
}
LAYER_OF_NAME = {v[0]: k for k, v in LAYER_INFO.items()}
CELL_PLACEHOLDER = "_Not yet answered._"


def cell_path(lib, layer, aspect):
    return os.path.join(lib, "matrix", f"{layer}-{aspect}.md")


def scaffold_cell(lib, layer, aspect):
    q, g = QUESTIONS[(layer, aspect)]
    name, view, _ = LAYER_INFO[layer]
    open(cell_path(lib, layer, aspect), "w", encoding="utf-8").write(
        f"---\nlayer: {layer}\naspect: {aspect}\nquestion: {q}\n"
        "status:    # leave empty; set to not-applicable (with a reason) if this cell does not apply\n"
        "reason:    # required when status is not-applicable\n"
        f"source:    # {GUIDE['source']}\nbasis:     # {GUIDE['basis']}\n---\n\n"
        f"# {name} · {INTERROGATIVE[aspect]} — {view}\n\n**{q}**\n\n_Guidance: {g}_\n\n{CELL_PLACEHOLDER}\n")


def load_cells(lib):
    """-> {(layer, aspect): dict(status=answered|not-applicable|open|missing, answer, meta)}"""
    out = {}
    for layer in LAYER_KEYS:
        for aspect in INTERROGATIVE:
            p = cell_path(lib, layer, aspect)
            if not os.path.isfile(p):
                out[(layer, aspect)] = {"status": "missing", "answer": "", "meta": {}}
                continue
            m = parse(p)
            body = m.get("_body", "")
            lines = [l for l in body.splitlines() if l.strip() and not l.startswith("# ")
                     and not l.startswith("**") and not l.startswith("_Guidance:") and l.strip() != CELL_PLACEHOLDER]
            answer = "\n".join(lines).strip()
            st = "not-applicable" if m.get("status") == "not-applicable" else ("answered" if answer else "open")
            out[(layer, aspect)] = {"status": st, "answer": answer, "meta": m, "path": os.path.relpath(p, lib)}
    return out


# ----------------------------------------------------------------------------- the template engine
# A documented subset of Mustache: {{name}} {{a.b}} {{.}} {{#list}}...{{/list}} {{^empty}}...{{/empty}}
# {{! comment }}. Format-agnostic: Markdown, HTML, AsciiDoc, LaTeX all work. Values are inserted as they are:
# no HTML escaping, so a template for HTML should not be fed untrusted text. Unknown names are reported.
_STANDALONE = re.compile(r"^[ \t]*({{[#^/!][^}]*}})[ \t]*\r?\n", re.M)
_TAG = re.compile(r"{{\s*([#^/!]?)\s*([^}]*?)\s*}}")


def _parse_tpl(text):
    text = _STANDALONE.sub(r"\1", text)            # a section tag alone on its line leaves no blank line
    root, stack, pos = [], [], 0
    cur = root
    for m in _TAG.finditer(text):
        if m.start() > pos:
            cur.append(("text", text[pos:m.start()]))
        kind, name = m.group(1), m.group(2)
        if kind == "!":
            pass
        elif kind in "#^" and kind:
            node = ("section", name, kind == "^", [])
            cur.append(node); stack.append((cur, name)); cur = node[3]
        elif kind == "/":
            if not stack or stack[-1][1] != name:
                raise SabsaError(f"template: closing {{{{/{name}}}}} does not match an open section")
            cur, _ = stack.pop()
        else:
            cur.append(("var", name))
        pos = m.end()
    if stack:
        raise SabsaError(f"template: section {{{{#{stack[-1][1]}}}}} is never closed")
    cur.append(("text", text[pos:]))
    return root


def _lookup(name, ctx, missing):
    if name == ".":
        return ctx[-1]
    head, *rest = name.split(".")
    for frame in reversed(ctx):
        if isinstance(frame, dict) and head in frame:
            v = frame[head]
            for r in rest:
                if not isinstance(v, dict) or r not in v:
                    missing.add(name)               # a typo in the tail is reported too, not rendered blank
                    return None
                v = v[r]
            return v
    missing.add(name)
    return None


def _render_nodes(nodes, ctx, out, missing):
    for n in nodes:
        if n[0] == "text":
            out.append(n[1])
        elif n[0] == "var":
            v = _lookup(n[1], ctx, missing)
            out.append("" if v is None or v is False else str(v))
        else:
            _, name, inverted, kids = n
            v = _lookup(name, ctx, missing)
            empty = v is None or v is False or v == [] or v == "" or v == 0
            if inverted:
                if empty:
                    _render_nodes(kids, ctx, out, missing)
            elif isinstance(v, list):
                for item in v:
                    _render_nodes(kids, ctx + [item], out, missing)
            elif not empty:
                _render_nodes(kids, ctx + [v] if isinstance(v, dict) else ctx, out, missing)


def render_template(text, model):
    missing = set()
    out = []
    _render_nodes(_parse_tpl(text), [model], out, missing)
    return "".join(out), sorted(missing)


# ------------------------------------------------------------------------------- the document model
def summary_of(m):
    return (m.get("statement") or m.get("definition") or m.get("description") or m.get("decision") or
            m.get("purpose") or m.get("rationale") or m.get("information") or m.get("requirement") or
            m.get("target_state") or m.get("result") or m.get("product") or m.get("metric") or "")


def collect_citations(lib, entries=None, cells=None):
    entries = entries if entries is not None else load(lib)[0]
    cells = cells if cells is not None else load_cells(lib)
    cited = defaultdict(list)
    for e, m in entries.items():
        if m.get("_external"):
            continue
        for src in ids(m.get("source")):
            cited[src.split("#", 1)[0]].append(e)
    for (layer, aspect), c in cells.items():
        for src in ids(c["meta"].get("source")):
            cited[src.split("#", 1)[0]].append(f"matrix/{layer}-{aspect}")
    return cited


def build_model(lib):
    entries, errors, warnings = check(lib)
    local_entries = {e: m for e, m in entries.items() if not m.get("_external")}
    reused_entries = {e: m for e, m in entries.items() if m.get("_external")}
    meta = parse(os.path.join(lib, "library.md"))
    cells = load_cells(lib)
    down = children(entries)
    elem = lambda e, m: {**{f: "" for f in TYPES[m["_dirtype"]]["fields"]},
                         **{f: "" for f in TYPES[m["_dirtype"]]["links"]},
                         "id": e, "type": m["_dirtype"], "title": m.get("title", ""), "summary": summary_of(m),
                         "basis": m.get("basis") or "—", "source": m.get("source") or "—",
                         "layer": TYPES[m["_dirtype"]]["layer"], "aspect": aspect_of(m),
                         "external": bool(m.get("_external")), "origin_id": m.get("_origin_id", e),
                         "origin_library": m.get("_origin_library", ""), "reuse_alias": m.get("_reuse_alias", ""),
                         "horizon": m.get("horizon") or "unspecified",
                         "lifecycle_state": m.get("lifecycle_state") or "unspecified",
                         **{k: v for k, v in m.items() if not k.startswith("_")}}
    by_type = {t: [elem(e, local_entries[e]) for e in sorted(local_entries) if local_entries[e]["_dirtype"] == t] for t in TYPES}
    layers = []
    for i, lk in enumerate(LAYER_KEYS, 1):
        name, view, purpose = LAYER_INFO[lk]
        cl = []
        for aspect in INTERROGATIVE:
            c = cells[(lk, aspect)]
            els = [elem(e, m) for e, m in sorted(local_entries.items()) if layer_key(m) == lk and aspect_of(m) == aspect]
            q, g = QUESTIONS[(lk, aspect)]
            cl.append({"aspect": aspect, "interrogative": INTERROGATIVE[aspect], "column": ASPECTS[aspect],
                       "question": q, "guidance": g, "status": c["status"], "answer": c["answer"],
                       "answered": c["status"] == "answered", "not_applicable": c["status"] == "not-applicable",
                       "open": c["status"] in ("open", "missing"), "reason": c["meta"].get("reason", ""),
                       "basis": c["meta"].get("basis") or "—", "source": c["meta"].get("source") or "—",
                       "elements": els, "has_elements": bool(els), "cell": f"{lk}-{aspect}"})
        layers.append({"key": lk, "name": name, "view": view, "purpose": purpose, "number": i,
                       "section": i + 3, "cells": cl})
    trace = []
    for c in sorted(e for e, m in local_entries.items() if m["_dirtype"] == "component"):
        trace += [dict(zip(("component", "mechanism", "service", "objective", "attribute", "driver"), r))
                  for r in trace_chains(entries, c)]
    qs = []
    for layer in LAYERS:
        for e, m in questions(local_entries).get(layer, []):
            qs.append({"n": len(qs) + 1, "id": e, "title": m.get("title", ""), "layer": layer,
                       "assumption": summary_of(m), "is_attribute": m["_dirtype"] == "attribute",
                       "target": m.get("target", ""), "metric": m.get("metric", "")})
    for (lk, aspect), c in cells.items():
        if c["status"] in ("answered", "not-applicable") and c["meta"].get("basis") == "assumed":
            assumption = c["answer"].split("\n")[0] if c["answer"] else c["meta"].get("reason", "")
            qs.append({"n": len(qs) + 1, "id": f"{lk}-{aspect}", "title": QUESTIONS[(lk, aspect)][0],
                       "layer": LAYER_INFO[lk][0], "assumption": assumption, "is_attribute": False})
    srcdir = os.path.join(lib, SOURCES_DIR)
    cited = collect_citations(lib, entries, cells)
    files = sorted(os.path.relpath(os.path.join(dp, f), lib).replace(os.sep, "/") for dp, _, fs in os.walk(srcdir)
                   for f in fs if f != "README.md") if os.path.isdir(srcdir) else []
    basis = defaultdict(int)
    for m in local_entries.values():
        basis[m.get("basis") or "unstated"] += 1
    settled = sum(1 for c in cells.values() if c["status"] in ("answered", "not-applicable"))
    open_cells = 36 - settled
    approval = approval_state(lib)
    draft = bool(errors or warnings or open_cells or not approval.get("valid"))
    trace_views = {}
    for name, view in _load_trace_views().items():
        cols = tuple(view.get("columns", ()))
        trace_views[name] = [dict(zip(cols, row)) for row in _view_chains(entries, view, local_starts=True)]

    # 3.2 architecture horizon / lifecycle model.
    horizon_groups = {h: [] for h in ARCH_HORIZONS}
    lifecycle_groups = {st: [] for st in LIFECYCLE_STATES}
    unspecified_horizon, unspecified_lifecycle = [], []
    for e, m in sorted(local_entries.items()):
        item = elem(e, m)
        h = m.get("horizon", "")
        st = m.get("lifecycle_state", "")
        (horizon_groups[h] if h in horizon_groups else unspecified_horizon).append(item)
        (lifecycle_groups[st] if st in lifecycle_groups else unspecified_lifecycle).append(item)
    ctt = []
    for e, m in sorted(local_entries.items()):
        if m.get("horizon") not in ("transition", "target"):
            continue
        preds = ids(m.get("predecessors")) or ["—"]
        rms = ids(m.get("transition_items")) or ["—"]
        for pred in preds:
            pm = entries.get(pred)
            for rm in rms:
                rmm = entries.get(rm)
                ctt.append({"current": pred,
                            "current_title": pm.get("title", "") if pm else "",
                            "transition": rm,
                            "transition_title": rmm.get("title", "") if rmm else "",
                            "target": e, "target_title": m.get("title", ""),
                            "type": m["_dirtype"], "target_horizon": m.get("horizon", ""),
                            "target_lifecycle": m.get("lifecycle_state", "") or "unspecified"})

    # External framework overlays are mappings, not copies of copyrighted framework content.
    overlays, _ = load_overlays(lib)
    frameworks, mappings = [], []
    for ov in overlays:
        fw = ov.get("framework", {})
        stats = defaultdict(int)
        for mp in ov.get("mappings", []) if isinstance(ov.get("mappings", []), list) else []:
            if not isinstance(mp, dict):
                continue
            st = mp.get("status", "")
            stats[st] += 1
            mappings.append({"framework_id": fw.get("id", ""), "framework_title": fw.get("title", ""),
                             "requirement": mp.get("requirement", ""), "title": mp.get("title", ""),
                             "status": st, "elements": mp.get("elements", ""), "evidence": mp.get("evidence", ""),
                             "roadmap": mp.get("roadmap", ""), "exceptions": mp.get("exceptions", ""),
                             "rationale": mp.get("rationale", ""), "owner": mp.get("owner", "")})
        frameworks.append({"id": fw.get("id", ""), "title": fw.get("title", ""), "version": fw.get("version", ""),
                           "source": fw.get("source", ""), "path": ov.get("_path", ""),
                           "covered": stats["covered"], "partial": stats["partial"], "gap": stats["gap"],
                           "not_applicable": stats["not-applicable"], "total": sum(stats.values())})

    reuse_cfg, _ = load_reuse_config(lib)
    reuse_libraries = []
    for item in reuse_cfg.get("libraries", []):
        if not isinstance(item, dict):
            continue
        src = _resolve_reuse_path(lib, item.get("path"))
        sm = parse(os.path.join(src, "library.md")) if os.path.isfile(os.path.join(src, "library.md")) else {}
        ast = approval_state(src, _seen={os.path.abspath(lib)}) if sm else {"valid": False, "reason": "unavailable"}
        reuse_libraries.append({"alias": item.get("alias", ""), "path": item.get("path", ""),
                                "name": sm.get("name", ""), "version": sm.get("version", ""),
                                "require_approved": item.get("require_approved", True),
                                "approved": bool(ast.get("valid")), "approval_reason": ast.get("reason", ""),
                                "types": ", ".join(item.get("types") or []), "ids": ", ".join(item.get("ids") or [])})
    reused = [elem(e, m) for e, m in sorted(reused_entries.items())]

    return {
        "library": {k: v for k, v in meta.items() if not k.startswith("_")} | {"summary": meta.get("_body", "").strip()},
        "generated": datetime.date.today().isoformat(),
        "draft": draft, "has_errors": bool(errors), "has_warnings": bool(warnings),
        "open_cells": open_cells, "settled_cells": settled,
        "approval": approval, "approved": bool(approval.get("valid")),
        "approval_reason": approval.get("reason", ""),
        "counts": {"elements": len(local_entries), "reused_elements": len(reused_entries), "errors": len(errors),
                   "warnings": len(warnings), "questions": len(qs), "frameworks": len(frameworks),
                   "framework_mappings": len(mappings)},
        "basis": {k: basis.get(k, 0) for k in ("stated", "inferred", "assumed", "unstated")},
        "layers": layers,
        "matrix": [{"name": L["name"], "marks": [{"mark": {"answered": "✓", "not-applicable": "n/a"}.get(c["status"], "·"),
                                                    "count": len(c["elements"])} for c in L["cells"]]} for L in layers],
        "interrogatives": [{"name": INTERROGATIVE[a], "column": ASPECTS[a]} for a in INTERROGATIVE],
        **{TYPES[t].get("collection", f"{t}s"): v for t, v in by_type.items()},
        "traceability": trace, "has_traceability": bool(trace),
        "assurance_traceability": trace_views.get("assurance", []), "has_assurance_traceability": bool(trace_views.get("assurance")),
        "policy_traceability": trace_views.get("policy", []), "has_policy_traceability": bool(trace_views.get("policy")),
        "trust_traceability": trace_views.get("trust", []), "has_trust_traceability": bool(trace_views.get("trust")),
        "roadmap_traceability": trace_views.get("roadmap", []), "has_roadmap_traceability": bool(trace_views.get("roadmap")),
        "current_elements": horizon_groups.get("current", []), "transition_elements": horizon_groups.get("transition", []),
        "target_elements": horizon_groups.get("target", []), "reference_elements": horizon_groups.get("reference", []),
        "unspecified_horizon": unspecified_horizon,
        "current_target_transitions": ctt, "has_current_target_transitions": bool(ctt),
        "lifecycle_states": [{"state": st, "elements": lifecycle_groups[st], "count": len(lifecycle_groups[st])} for st in LIFECYCLE_STATES],
        "unspecified_lifecycle": unspecified_lifecycle,
        "frameworks": frameworks, "framework_mappings": mappings,
        "framework_gaps": [m for m in mappings if m.get("status") in ("partial", "gap")],
        "has_frameworks": bool(frameworks),
        "reuse_libraries": reuse_libraries, "reused_elements": reused, "has_reuse": bool(reuse_libraries),
        "questions": qs, "has_questions": bool(qs),
        "sources": [{"file": f, "cited_by": " ".join(sorted(cited[f])) or "not cited"} for f in files],
        "errors": [{"text": x} for x in errors], "warnings": [{"text": x} for x in warnings],
    }

def _load_document_views():
    path = os.path.join(SCHEMA_ROOT, "documents.json")
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SabsaError(f"cannot load SABSA document-view catalogue {path}: {exc}") from exc
    return doc.get("views", {})


def cmd_documents(a):
    views=_load_document_views()
    print(f"# SABSA document views — {len(views)}\n")
    print("| Template | Purpose | Audience | Available |")
    print("| --- | --- | --- | --- |")
    for name,spec in views.items():
        try:
            path,_=resolve_template(a.lib,name)
            available="yes: " + os.path.basename(path)
        except SabsaError:
            available="no"
        print(f"| {name} | {spec.get('purpose','')} | {spec.get('audience','')} | {available} |")


# ------------------------------------------------------------------------------- templates: resolution
PACKAGE_TEMPLATES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates", "sabsa")


def resolve_template(lib, name, explicit=None):
    """-> (path, label). First of: --template FILE; <lib>/templates/<name>.*; ~/.ai/sabsa-templates/<name>.*;
    the package default."""
    if explicit:
        if not os.path.isfile(explicit):
            raise SabsaError(f"template {explicit} does not exist")
        return explicit, "the template given on the command line"
    home = os.path.expanduser(os.environ.get("AI_IT_HOME") or "~/.ai")
    for d, label in ((os.path.join(lib, "templates"), "the library's own template"),
                     (os.path.join(home, "sabsa-templates"), "your personal template"),
                     (PACKAGE_TEMPLATES, "the package default")):
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if os.path.splitext(f)[0] == name and not f.endswith(".docx"):
                    return os.path.join(d, f), label
    raise SabsaError(f"no template named '{name}' (looked in {lib}/templates, {home}/sabsa-templates, the package)")


def resolve_reference_docx(lib, explicit=None):
    home = os.path.expanduser(os.environ.get("AI_IT_HOME") or "~/.ai")
    for p in ([explicit] if explicit else []) + [os.path.join(lib, "templates", "reference.docx"),
                                                 os.path.join(home, "sabsa-templates", "reference.docx")]:
        if p and os.path.isfile(p):
            return p
    return None


class SabsaError(Exception):
    pass


# --------------------------------------------------------------------------------------- parsing
def parse(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        raise SabsaError(f"{path}: no front matter")
    end = text.find("\n---", 3)
    if end < 0:
        raise SabsaError(f"{path}: front matter not closed")
    meta = {}
    for line in text[3:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        k, sep, v = line.partition(":")
        if not sep:
            raise SabsaError(f"{path}: cannot parse front matter line '{line}'")
        meta[k.strip()] = re.sub(r"\s+#\s.*$", "", v).strip()     # drop inline guidance comments
    meta["_body"] = text[end + 4:].strip()
    return meta


def ids(value):
    return [x.strip() for x in str(value or "").split(",") if x.strip()]


def _load_local(lib):
    if not os.path.isfile(os.path.join(lib, "library.md")):
        raise SabsaError(f"{lib} is not a SABSA library (no library.md); run 'sabsa.py init'")
    entries, errors = {}, []
    for t, spec in TYPES.items():
        dirs = [spec["dir"]] + ([spec["legacy"]] if spec.get("legacy") else [])
        listing = [(dd, f) for dd in dirs if os.path.isdir(os.path.join(lib, dd))
                   for f in sorted(os.listdir(os.path.join(lib, dd)))]
        for dd, f in listing:
            d = os.path.join(lib, dd)
            if not f.endswith(".md") or f.startswith("_"):
                continue
            p = os.path.join(d, f)
            if dd != spec["dir"]:
                errors.append(f"{os.path.relpath(p, lib)}: in the old folder {dd}/; in SABSA this element belongs "
                              f"to the {spec['layer']} layer — run 'sabsa.py migrate' to move it to {spec['dir']}/")
            try:
                m = parse(p)
            except SabsaError as exc:
                errors.append(str(exc)); continue
            m["_path"] = os.path.relpath(p, lib)
            m["_dirtype"] = t
            m["_external"] = False
            m["_origin_library"] = os.path.abspath(lib)
            m["_origin_id"] = m.get("id", "")
            eid = m.get("id", "")
            if eid in entries:
                errors.append(f"{m['_path']}: duplicate id {eid} (also {entries[eid]['_path']})"); continue
            entries[eid] = m
    return entries, errors


def load_reuse_config(lib):
    path = os.path.join(lib, REUSE_FILE)
    if not os.path.isfile(path):
        return {"schema": 1, "libraries": []}, []
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"schema": 1, "libraries": []}, [f"{REUSE_FILE}: cannot parse: {exc}"]
    if not isinstance(doc.get("libraries", []), list):
        return doc, [f"{REUSE_FILE}: 'libraries' must be a list"]
    return doc, []


def _resolve_reuse_path(lib, raw):
    raw = os.path.expanduser(os.path.expandvars(str(raw or "")))
    return os.path.abspath(raw if os.path.isabs(raw) else os.path.join(lib, raw))


def _reuse_alias_ok(alias):
    return bool(re.match(r"^[A-Za-z][A-Za-z0-9_-]{0,63}$", alias or ""))


def _dependency_closure(entries, selected):
    """Include selected source-library elements and every relation they need for a coherent graph."""
    keep, q = set(selected), list(selected)
    while q:
        eid = q.pop()
        m = entries.get(eid)
        if not m:
            continue
        for field in TYPES[m["_dirtype"]]["links"]:
            for ref in ids(m.get(field)):
                if ref in entries and ref not in keep:
                    keep.add(ref); q.append(ref)
        for ref in ids(m.get("predecessors")) + ids(m.get("transition_items")):
            if ref in entries and ref not in keep:
                keep.add(ref); q.append(ref)
    return keep


def _namespace_reused(alias, source_entries, selected):
    out = {}
    keep = _dependency_closure(source_entries, selected)
    for eid in sorted(keep):
        m = dict(source_entries[eid])
        nid = f"{alias}:{eid}"
        m["_external"] = True
        m["_reuse_alias"] = alias
        m["_origin_id"] = eid
        m["_origin_library"] = source_entries[eid].get("_origin_library", "")
        m["id"] = nid
        spec = TYPES[m["_dirtype"]]
        for field in spec["links"]:
            refs = []
            for r in ids(m.get(field)):
                refs.append(f"{alias}:{r}" if r in keep else r)
            if refs:
                m[field] = ", ".join(refs)
        for field in ("predecessors", "transition_items"):
            refs = []
            for r in ids(m.get(field)):
                refs.append(f"{alias}:{r}" if r in keep else r)
            if refs:
                m[field] = ", ".join(refs)
        out[nid] = m
    return out


def load(lib, include_reuse=True, _seen=None):
    local, errors = _load_local(lib)
    if not include_reuse:
        return local, errors
    cfg, cfgerr = load_reuse_config(lib)
    errors.extend(cfgerr)
    seen = set(_seen or ()) | {os.path.abspath(lib)}
    aliases = set()
    for item in cfg.get("libraries", []):
        if not isinstance(item, dict):
            errors.append(f"{REUSE_FILE}: each library entry must be an object"); continue
        alias = str(item.get("alias", "")).strip()
        if not _reuse_alias_ok(alias):
            errors.append(f"{REUSE_FILE}: invalid alias '{alias}'"); continue
        if alias in aliases:
            errors.append(f"{REUSE_FILE}: duplicate alias '{alias}'"); continue
        aliases.add(alias)
        src = _resolve_reuse_path(lib, item.get("path"))
        if src in seen:
            errors.append(f"{REUSE_FILE}: reuse cycle involving {src}"); continue
        if not os.path.isfile(os.path.join(src, "library.md")):
            errors.append(f"{REUSE_FILE}: {alias} path '{item.get('path')}' is not a SABSA library"); continue
        source_entries, source_errors = _load_local(src)
        if source_errors:
            errors.extend(f"reuse {alias}: {e}" for e in source_errors); continue
        wanted_types = set(item.get("types") or [])
        bad_types = sorted(wanted_types - set(TYPES))
        if bad_types:
            errors.append(f"{REUSE_FILE}: {alias} has unknown type(s): {', '.join(bad_types)}"); continue
        wanted_ids = set(item.get("ids") or [])
        missing_ids = sorted(wanted_ids - set(source_entries))
        if missing_ids:
            errors.append(f"{REUSE_FILE}: {alias} has unknown id(s): {', '.join(missing_ids)}"); continue
        selected = {eid for eid, m in source_entries.items()
                    if (not wanted_types and not wanted_ids) or m["_dirtype"] in wanted_types or eid in wanted_ids}
        imported = _namespace_reused(alias, source_entries, selected)
        collision = sorted(set(local) & set(imported))
        if collision:
            errors.append(f"{REUSE_FILE}: namespaced collision(s): {', '.join(collision)}"); continue
        local.update(imported)
    return local, errors


def validate_reuse_config(lib, errors, warnings):
    cfg, cfgerr = load_reuse_config(lib)
    errors.extend(cfgerr)
    aliases = set()
    for item in cfg.get("libraries", []):
        if not isinstance(item, dict):
            continue
        alias = str(item.get("alias", "")).strip()
        if not _reuse_alias_ok(alias) or alias in aliases:
            continue
        aliases.add(alias)
        src = _resolve_reuse_path(lib, item.get("path"))
        if not os.path.isfile(os.path.join(src, "library.md")):
            continue
        local, serr = _load_local(src)
        if serr:
            errors.extend(f"reuse {alias}: {e}" for e in serr)
        if item.get("require_approved", True):
            st = approval_state(src, _seen={os.path.abspath(lib)})
            if not st.get("valid"):
                errors.append(f"reuse {alias}: source library is not currently approved: {st.get('reason', '')}")
        # Source libraries may intentionally have their own overlays/reuse. We validate their local structural
        # content here and bind their full snapshot hash into the consuming library's approval separately.
        if not local:
            warnings.append(f"reuse {alias}: source library contains no architecture elements")
    return cfg

OVERLAY_STATUSES = ("covered", "partial", "gap", "not-applicable")

def load_overlays(lib):
    root = os.path.join(lib, OVERLAYS_DIR)
    out, errors = [], []
    if not os.path.isdir(root):
        return out, errors
    for f in sorted(os.listdir(root)):
        if not f.endswith(".json") or f.startswith("_"):
            continue
        path = os.path.join(root, f)
        try:
            doc = json.load(open(path, encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{OVERLAYS_DIR}/{f}: cannot parse: {exc}"); continue
        if not isinstance(doc, dict):
            errors.append(f"{OVERLAYS_DIR}/{f}: overlay must be a JSON object"); continue
        doc["_path"] = os.path.relpath(path, lib).replace(os.sep, "/")
        out.append(doc)
    return out, errors


def validate_overlays(lib, entries, errors, warnings):
    overlays, parse_errors = load_overlays(lib)
    errors.extend(parse_errors)
    seen_frameworks = set()
    for ov in overlays:
        where = ov.get("_path", OVERLAYS_DIR)
        fw = ov.get("framework")
        if not isinstance(fw, dict):
            errors.append(f"{where}: 'framework' must be an object"); continue
        for k in ("id", "title", "version", "source"):
            if not str(fw.get(k, "")).strip():
                errors.append(f"{where}: framework.{k} is required")
        fid = str(fw.get("id", "")).strip()
        if fid in seen_frameworks:
            errors.append(f"{where}: duplicate framework id '{fid}'")
        seen_frameworks.add(fid)
        mappings = ov.get("mappings", [])
        if not isinstance(mappings, list):
            errors.append(f"{where}: mappings must be a list"); continue
        reqs = set()
        for i, mp in enumerate(mappings, 1):
            loc = f"{where}: mapping {i}"
            if not isinstance(mp, dict):
                errors.append(f"{loc} must be an object"); continue
            req = str(mp.get("requirement", "")).strip()
            if not req:
                errors.append(f"{loc}: requirement is required"); continue
            if req in reqs:
                errors.append(f"{where}: duplicate requirement '{req}'")
            reqs.add(req)
            st = str(mp.get("status", "")).strip()
            if st not in OVERLAY_STATUSES:
                errors.append(f"{loc}: status must be one of {', '.join(OVERLAY_STATUSES)}")
            mapped = ids(mp.get("elements"))
            for eid in mapped:
                if eid not in entries:
                    errors.append(f"{loc}: elements cites {eid}, which does not exist locally or through reuse")
            ev = ids(mp.get("evidence"))
            for eid in ev:
                if eid not in entries:
                    errors.append(f"{loc}: evidence cites {eid}, which does not exist")
                elif entries[eid]["_dirtype"] != "evidence":
                    errors.append(f"{loc}: evidence must cite EV evidence; {eid} is {entries[eid]['_dirtype']}")
            rms = ids(mp.get("roadmap"))
            for eid in rms:
                if eid not in entries:
                    errors.append(f"{loc}: roadmap cites {eid}, which does not exist")
                elif entries[eid]["_dirtype"] != "roadmap":
                    errors.append(f"{loc}: roadmap must cite RM roadmap items; {eid} is {entries[eid]['_dirtype']}")
            exs = ids(mp.get("exceptions"))
            for eid in exs:
                if eid not in entries:
                    errors.append(f"{loc}: exceptions cites {eid}, which does not exist")
                elif entries[eid]["_dirtype"] != "exception":
                    errors.append(f"{loc}: exceptions must cite EX exceptions; {eid} is {entries[eid]['_dirtype']}")
            if st == "covered" and not mapped:
                errors.append(f"{loc}: covered requires at least one mapped architecture element")
            if st == "gap" and not (rms or exs):
                warnings.append(f"{loc}: gap has no roadmap item or approved exception")
            if st == "partial" and not (rms or exs):
                warnings.append(f"{loc}: partial coverage has no roadmap item or exception")
            if st == "not-applicable" and not str(mp.get("rationale", "")).strip():
                errors.append(f"{loc}: not-applicable requires rationale")
            if ov.get("evidence_required") is True and st == "covered" and not ev:
                warnings.append(f"{loc}: framework requires evidence but covered mapping cites no EV artefact")
    return overlays


# ---------------------------------------------------------------------------------------- checks
BUSINESS_PARENT_FIELDS = {name: tuple(spec.get("business_parent", ())) for name, spec in TYPES.items()}


def check(lib):
    entries, errors = load(lib)
    warnings = []
    for eid, m in entries.items():
        if m.get("_external"):
            continue
        t, p = m["_dirtype"], m["_path"]
        spec = TYPES[t]
        if not ID_RE.match(eid):
            errors.append(f"{p}: id '{eid}' is not of the form {spec['prefix']}-NNN"); continue
        if BY_PREFIX[eid.split("-")[0]] != t:
            errors.append(f"{p}: {eid} is a {BY_PREFIX[eid.split('-')[0]]} id inside the {t} folder")
        if os.path.basename(p) != f"{eid}.md":
            errors.append(f"{p}: file name must be {eid}.md")
        if m.get("type") not in (None, t):
            errors.append(f"{p}: type '{m.get('type')}' does not match its folder ({t})")
        for f in spec["required"]:
            if not m.get(f):
                errors.append(f"{eid}: required field '{f}' is empty")
            elif PLACEHOLDER.search(m[f]):
                errors.append(f"{eid}: required field '{f}' still holds placeholder text")
        for field, allowed in spec.get("enums", {}).items():
            if m.get(field) and m.get(field) not in allowed:
                errors.append(f"{eid}: {field} must be one of {', '.join(allowed)}")
        if t == "trust" and m.get("source_domain") and m.get("source_domain") == m.get("target_domain"):
            errors.append(f"{eid}: source_domain and target_domain must differ; use a domain rule, not a self-trust relation")
        if t == "service" and m.get("policy") and not ids(m.get("policies")):
            warnings.append(f"{eid}: legacy inline 'policy' text is present but no PL policy is linked; model the policy as a first-class artefact")
        a = m.get("aspect", "")
        if a and a not in ASPECTS:
            errors.append(f"{eid}: aspect '{a}' is not one of {', '.join(ASPECTS)}")
        for field, (target, mandatory) in spec["links"].items():
            refs = ids(m.get(field))
            if mandatory and not refs:
                errors.append(f"{eid}: '{field}' is empty — a {t} must trace upward to at least one {target}")
            for r in refs:
                if r not in entries:
                    errors.append(f"{eid}: '{field}' cites {r}, which does not exist")
                elif entries[r]["_dirtype"] != target:
                    errors.append(f"{eid}: '{field}' must cite {target} entries; {r} is a {entries[r]['_dirtype']}")
        horizon = m.get("horizon", "")
        if horizon and horizon not in ARCH_HORIZONS:
            errors.append(f"{eid}: horizon '{horizon}' is not one of {', '.join(ARCH_HORIZONS)}")
        life = m.get("lifecycle_state", "")
        if life and life not in LIFECYCLE_STATES:
            errors.append(f"{eid}: lifecycle_state '{life}' is not one of {', '.join(LIFECYCLE_STATES)}")
        for pred in ids(m.get("predecessors")):
            if pred not in entries:
                errors.append(f"{eid}: predecessors cites {pred}, which does not exist")
            elif entries[pred]["_dirtype"] != t:
                errors.append(f"{eid}: predecessor {pred} must be the same type ({t}), not {entries[pred]['_dirtype']}")
            elif pred == eid:
                errors.append(f"{eid}: cannot be its own predecessor")
        for rm in ids(m.get("transition_items")):
            if rm not in entries:
                errors.append(f"{eid}: transition_items cites {rm}, which does not exist")
            elif entries[rm]["_dirtype"] != "roadmap":
                errors.append(f"{eid}: transition_items must cite RM roadmap items; {rm} is {entries[rm]['_dirtype']}")
        if horizon == "target" and ids(m.get("predecessors")) and not ids(m.get("transition_items")):
            warnings.append(f"{eid}: target element has predecessor(s) but no transition_items roadmap link")
        if life == "retired" and horizon == "target":
            errors.append(f"{eid}: a target-horizon element cannot already be retired")
        b = m.get("basis", "")
        if b and b not in BASES:
            errors.append(f"{eid}: basis '{b}' is not one of {', '.join(BASES)}")
        elif not b:
            warnings.append(f"{eid}: no basis — say whether it is stated by the client, inferred, or assumed")
        elif b == "assumed":
            warnings.append(f"{eid}: assumed — confirm with the client (see 'sabsa.py questions')")
        for src in ids(m.get("source")):
            if re.match(r"^[a-z]+://", src):
                continue
            path = src.split("#", 1)[0]
            if not os.path.exists(os.path.join(lib, path)):
                errors.append(f"{eid}: cites source '{src}', which is not in the library")
        if b in ("stated", "inferred") and not m.get("source"):
            errors.append(f"{eid}: basis is {b} but no source is cited — which material supports this claim?")
        st = m.get("status", "draft")
        if st not in ELEMENT_STATUSES:
            errors.append(f"{eid}: status '{st}' is not one of {', '.join(ELEMENT_STATUSES)}")
    check_cells(lib, errors, warnings)
    validate_reuse_config(lib, errors, warnings)
    validate_overlays(lib, entries, errors, warnings)
    untraced = sorted(e for e in entries if not entries[e].get("_external") and entries[e]["_dirtype"] != "driver" and not reaches_driver(entries, e))
    for e in untraced:
        errors.append(f"{e}: does not trace to any business driver — SABSA's first rule")
    return entries, errors, warnings


def aspect_of(m):
    return m.get("aspect") or DEFAULT_ASPECT[m["_dirtype"]]


def layer_key(m):
    return LAYER_OF_NAME[TYPES[m["_dirtype"]]["layer"]]


def check_cells(lib, errors, warnings):
    cells = load_cells(lib)
    for (layer, aspect), c in cells.items():
        where = f"matrix/{layer}-{aspect}.md"
        if c["status"] == "missing":
            warnings.append(f"{where}: missing — run 'sabsa.py matrix <lib> --scaffold' to create the cell")
            continue
        if c["status"] == "open":
            warnings.append(f"{where}: not yet answered")
            continue
        if c["status"] == "not-applicable" and not c["meta"].get("reason"):
            errors.append(f"{where}: marked not-applicable without a reason — say why this question does not apply")
        # Every settled matrix assertion/decision needs provenance. This is especially important because most
        # SABSA matrix cells are narrative views rather than first-class element types in the 3.0.x model.
        if c["status"] in ("answered", "not-applicable"):
            b = c["meta"].get("basis", "")
            if not b:
                errors.append(f"{where}: settled cell has no basis — use stated, inferred, or assumed")
            elif b not in BASES:
                errors.append(f"{where}: basis '{b}' is not one of {', '.join(BASES)}")
            elif b == "assumed":
                warnings.append(f"{where}: assumed — confirm with the client (see 'sabsa.py questions')")
            if b in ("stated", "inferred") and not c["meta"].get("source"):
                errors.append(f"{where}: basis is {b} but no source is cited")
            for src in ids(c["meta"].get("source")):
                if not re.match(r"^[a-z]+://", src) and not os.path.exists(os.path.join(lib, src.split("#", 1)[0])):
                    errors.append(f"{where}: cites source '{src}', which is not in the library")
    return cells


def business_parents(entries, eid):
    """Relations that justify an element upward toward a business driver.

    Supplemental/lateral relations such as service->domain, operation->service and domain->domain trust are
    intentionally excluded. They remain dependencies for impact analysis, but must never substitute for the
    explicit business-justification path.
    """
    m = entries[eid]
    return [r for field in BUSINESS_PARENT_FIELDS[m["_dirtype"]]
            for r in ids(m.get(field)) if r in entries]


def dependency_parents(entries, eid):
    """All declared relations used for downward impact, including lifecycle transition dependencies."""
    m = entries[eid]
    out = [r for field in TYPES[m["_dirtype"]]["links"] for r in ids(m.get(field)) if r in entries]
    out += [r for field in ("predecessors", "transition_items") for r in ids(m.get(field)) if r in entries]
    return out


def parents(entries, eid):
    """Backward-compatible name for the business-justification parent relation."""
    return business_parents(entries, eid)


def trace_chains(entries, component):
    """Typed component -> mechanism -> service -> objective -> attribute -> driver chains.

    The relation field at each hop is explicit. This prevents supplemental relations (notably service->domain)
    from being rendered in the wrong traceability column.
    """
    steps = (("component", "mechanisms", "mechanism"),
             ("mechanism", "services", "service"),
             ("service", "objectives", "objective"),
             ("objective", "attributes", "attribute"),
             ("attribute", "drivers", "driver"))
    rows = [[component]]
    for source_type, field, target_type in steps:
        nxt = []
        for row in rows:
            cur = row[-1]
            if cur == "—":
                nxt.append(row + ["—"]); continue
            m = entries.get(cur)
            if not m or m["_dirtype"] != source_type:
                nxt.append(row + ["—"]); continue
            refs = [r for r in ids(m.get(field)) if r in entries and entries[r]["_dirtype"] == target_type]
            for r in refs or ["—"]:
                nxt.append(row + [r])
        rows = nxt
    return rows


def reaches_driver(entries, eid, seen=None):
    seen = set(seen or ())
    if eid in seen:
        return False
    if entries[eid]["_dirtype"] == "driver":
        return True
    seen.add(eid)
    return any(reaches_driver(entries, p, seen) for p in business_parents(entries, eid))


def children(entries):
    """Reverse dependency graph used for change impact, not only business traceability."""
    down = defaultdict(set)
    for e in entries:
        for p in dependency_parents(entries, e):
            down[p].add(e)
    return down


# --------------------------------------------------------------------------- approval / release gate
def _frontmatter_set(path, key, value):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        raise SabsaError(f"{path}: no front matter")
    end = text.find("\n---", 3)
    if end < 0:
        raise SabsaError(f"{path}: front matter not closed")
    head, tail = text[3:end], text[end:]
    lines = head.splitlines()
    found = False
    out = []
    for line in lines:
        k, sep, _ = line.partition(":")
        if sep and k.strip() == key:
            out.append(f"{key}: {value}"); found = True
        else:
            out.append(line)
    if not found:
        out.append(f"{key}: {value}")
    open(path, "w", encoding="utf-8").write("---" + "\n".join(out) + tail)


def _snapshot_files(lib):
    """Local architecture inputs covered by owner approval; generated documents/templates are excluded."""
    paths = []
    for single in ("library.md", REUSE_FILE):
        p = os.path.join(lib, single)
        if os.path.isfile(p):
            paths.append(p)
    for d in [SOURCES_DIR, "matrix", OVERLAYS_DIR] + sorted({spec["dir"] for spec in TYPES.values()}):
        root = os.path.join(lib, d)
        if not os.path.isdir(root):
            continue
        for dp, _, fs in os.walk(root):
            for f in fs:
                if f.startswith("."):
                    continue
                paths.append(os.path.join(dp, f))
    return sorted(set(paths), key=lambda p: os.path.relpath(p, lib).replace(os.sep, "/"))


def snapshot_sha256(lib, _seen=None):
    """Hash local architecture inputs plus the exact snapshots of reused libraries.

    This deliberately makes an approval stale when a referenced enterprise/reference library changes, even when
    no local file changed. Cross-library reuse therefore cannot silently bypass local release governance.
    """
    root = os.path.abspath(lib)
    seen = set(_seen or ())
    if root in seen:
        # A reuse cycle is separately a validation error. Return a stable marker instead of recursing forever.
        return hashlib.sha256(("reuse-cycle:" + root).encode()).hexdigest(), 0
    seen.add(root)
    h = hashlib.sha256()
    files = _snapshot_files(lib)
    for path in files:
        rel = os.path.relpath(path, lib).replace(os.sep, "/")
        data = open(path, "rb").read()
        h.update(rel.encode("utf-8")); h.update(b"\0")
        h.update(hashlib.sha256(data).digest()); h.update(b"\0")
    cfg, _ = load_reuse_config(lib)
    dep_count = 0
    for item in sorted((x for x in cfg.get("libraries", []) if isinstance(x, dict)), key=lambda x: str(x.get("alias", ""))):
        alias = str(item.get("alias", ""))
        src = _resolve_reuse_path(lib, item.get("path"))
        if not alias or not os.path.isfile(os.path.join(src, "library.md")):
            continue
        dep_hash, dep_files = snapshot_sha256(src, seen)
        h.update(f"reuse:{alias}".encode("utf-8")); h.update(b"\0")
        h.update(dep_hash.encode("ascii")); h.update(b"\0")
        dep_count += dep_files
    return h.hexdigest(), len(files) + dep_count


def approval_state(lib, _seen=None):
    p = os.path.join(lib, APPROVAL_DIR, APPROVAL_FILE)
    meta = parse(os.path.join(lib, "library.md"))
    if not os.path.isfile(p):
        return {"valid": False, "reason": "no owner approval record", "approved_by": "", "approved_at": ""}
    try:
        rec = json.load(open(p, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"valid": False, "reason": f"approval record is unreadable: {exc}", "approved_by": "", "approved_at": ""}
    now_hash, count = snapshot_sha256(lib, _seen)
    if meta.get("status") != "approved":
        return {**rec, "valid": False, "reason": "library status is not approved", "current_snapshot_sha256": now_hash}
    if rec.get("snapshot_sha256") != now_hash:
        return {**rec, "valid": False, "reason": "approval is stale: architecture inputs or reused-library dependencies changed after approval",
                "current_snapshot_sha256": now_hash, "files": count}
    return {**rec, "valid": True, "reason": "current architecture snapshot and reused dependencies are owner-approved",
            "current_snapshot_sha256": now_hash, "files": count}


def cmd_approve(a):
    """Owner approval is a hash-bound decision over the whole architecture snapshot, not a mutable text label."""
    entries, errors, warnings = check(a.lib)
    if errors or warnings:
        print(f"approval refused: {len(errors)} error(s), {len(warnings)} warning(s)")
        for x in errors:
            print(f"  error    {x}")
        for x in warnings:
            print(f"  warning  {x}")
        print("Resolve all findings/assumptions/open cells before owner approval.")
        return 1
    libpath = os.path.join(a.lib, "library.md")
    _frontmatter_set(libpath, "status", "approved")
    snap, count = snapshot_sha256(a.lib)
    meta = parse(libpath)
    rec = {
        "schema": 1,
        "library": meta.get("name", ""),
        "version": meta.get("version", ""),
        "approved_by": a.by,
        "approved_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
        "snapshot_sha256": snap,
        "files": count,
        "note": a.note or "",
    }
    d = os.path.join(a.lib, APPROVAL_DIR); os.makedirs(d, exist_ok=True)
    tmp = os.path.join(d, APPROVAL_FILE + ".tmp")
    open(tmp, "w", encoding="utf-8").write(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
    os.replace(tmp, os.path.join(d, APPROVAL_FILE))
    print(f"approved {meta.get('name', a.lib)} version {meta.get('version', '')} by {a.by}")
    print(f"  snapshot sha256 {snap} ({count} architecture input file(s))")
    print("Any later change to library.md, sources, matrix cells, overlays, architecture elements or reused-library snapshots invalidates this approval.")
    return 0


def cmd_approval(a):
    st = approval_state(a.lib)
    print(("APPROVED" if st.get("valid") else "NOT APPROVED") + f": {st.get('reason', '')}")
    if st.get("approved_by"):
        print(f"  by {st.get('approved_by')} at {st.get('approved_at', '')}")
    if st.get("snapshot_sha256"):
        print(f"  approved snapshot {st.get('snapshot_sha256')}")
    if st.get("current_snapshot_sha256") and st.get("current_snapshot_sha256") != st.get("snapshot_sha256"):
        print(f"  current snapshot  {st.get('current_snapshot_sha256')}")
    return 0 if st.get("valid") else 1


def _ensure_native_jai_frontmatter(path, eid):
    """Upgrade a local SABSA element on write; legacy reads remain unchanged."""
    _frontmatter_set(path, "canonical_ref", f"semantic:sabsa:{eid}")
    _frontmatter_set(path, "jai_profile", SABSA_JAI_PROFILE)
    _frontmatter_set(path, "jai_layer", SABSA_JAI_LAYER)
    _frontmatter_set(path, "jai_release", RELEASE)

def _ensure_native_library_frontmatter(lib):
    path=os.path.join(lib,"library.md")
    if os.path.isfile(path):
        _frontmatter_set(path,"jai_profile",SABSA_JAI_PROFILE)
        _frontmatter_set(path,"jai_layer",SABSA_JAI_LAYER)
        _frontmatter_set(path,"jai_release",RELEASE)
        _frontmatter_set(path,"semantic_identity_authority","JAI")


# --------------------------------------------------------------------------------------- commands
def cmd_init(a):
    if os.path.exists(os.path.join(a.lib, "library.md")):
        raise SabsaError(f"{a.lib} already holds a SABSA library")
    for spec in TYPES.values():
        os.makedirs(os.path.join(a.lib, spec["dir"]), exist_ok=True)
    os.makedirs(os.path.join(a.lib, SOURCES_DIR), exist_ok=True)
    os.makedirs(os.path.join(a.lib, "matrix"), exist_ok=True)
    os.makedirs(os.path.join(a.lib, OVERLAYS_DIR), exist_ok=True)
    for layer in LAYER_KEYS:
        for aspect in INTERROGATIVE:
            scaffold_cell(a.lib, layer, aspect)
    open(os.path.join(a.lib, SOURCES_DIR, "README.md"), "w", encoding="utf-8").write(
        "# Sources\n\nPut everything known about the client and the environment here, as files: the brief or RFP, "
        "meeting and interview notes, their website or annual report as text, organisation chart, regulatory "
        "context, existing architecture or policy documents, incident history. Text formats (Markdown, plain "
        "text) are read directly; convert PDFs and Word files to text first.\n\nEvery architecture claim — elements and settled matrix cells — "
        "states its basis and cites supporting material when stated or inferred (`source: 00-sources/brief.md#goals`). "
        "Use *stated* when the client says it, *inferred* when it follows from evidence, or *assumed* when confirmation is required. Assumptions become the list of questions for "
        "the client: `sabsa.py questions`.\n")
    open(os.path.join(a.lib, OVERLAYS_DIR, "README.md"), "w", encoding="utf-8").write(
        "# External framework overlays\n\nUse `sabsa.py overlay-init` to create mapping files. Overlays store requirement identifiers, "
        "mapping status, architecture element IDs, evidence, exceptions and roadmap links. Do not copy licensed standard text "
        "unless your organisation has the rights to reproduce it.\n")
    _atomic_json(os.path.join(a.lib, REUSE_FILE), {"schema": 1, "libraries": []})
    open(os.path.join(a.lib, "library.md"), "w", encoding="utf-8").write(
        f"---\nname: {a.name}\norganisation: {a.organisation}\nscope: {a.scope}\nowner: {a.owner}\n"
        f"version: 0.1.0\nstatus: draft\njai_profile: {SABSA_JAI_PROFILE}\njai_layer: {SABSA_JAI_LAYER}\njai_release: {RELEASE}\nsemantic_identity_authority: JAI\n---\n\n"
        f"# {a.name}\n\nSABSA security architecture library for {a.organisation}. Scope: {a.scope}.\n\n"
        "Each element is one Markdown file named by its ID, in the folder of its layer. Upward links are "
        "required, so every element traces to a business driver. Run `sabsa.py check` before any change is "
        "accepted, and `sabsa.py suggest` to see what is missing.\n")
    print(f"initialised SABSA library at {a.lib}: " + ", ".join(s["dir"] for s in TYPES.values()))


def next_id(lib, t):
    d = os.path.join(lib, TYPES[t]["dir"])
    nums = [int(m.group(2)) for f in (os.listdir(d) if os.path.isdir(d) else [])
            for m in [ID_RE.match(f[:-3])] if m]
    return f"{TYPES[t]['prefix']}-{max(nums, default=0) + 1:03d}"


def cmd_new(a):
    if a.type not in TYPES:
        raise SabsaError(f"type must be one of {', '.join(TYPES)}")
    load(a.lib)
    spec = TYPES[a.type]
    eid = next_id(a.lib, a.type)
    given = dict(kv.split("=", 1) for kv in (a.set or []))
    unknown = set(given) - set(spec["fields"]) - set(spec["links"]) - {"aspect", "status"}
    if unknown:
        raise SabsaError(f"unknown field(s) {sorted(unknown)} for a {a.type}")
    lines = [f"id: {eid}", f"type: {a.type}", f"title: {a.title}", f"canonical_ref: semantic:sabsa:{eid}", f"jai_profile: {SABSA_JAI_PROFILE}", f"jai_layer: {SABSA_JAI_LAYER}", f"jai_release: {RELEASE}"]
    for f in spec["fields"]:
        if f == "title":
            continue
        if f in ("source", "basis") and f not in given:      # validated fields: empty, with the guidance as a comment
            lines.append(f"{f}:    # {GUIDE[f]}")
            continue
        if f in COMMON_FIELDS and f not in given:
            lines.append(f"{f}:    # optional: {GUIDE.get(f, f)}")
            continue
        lines.append(f"{f}: {given.get(f, '<' + GUIDE.get(f, f) + '>')}")
    for f, (target, mandatory) in spec["links"].items():
        lines.append(f"{f}: {given.get(f, '')}" + ("" if f in given else
                     f"   # {'required' if mandatory else 'optional'}: comma-separated {target} IDs"))
    lines.append(f"aspect: {given['aspect']}" if given.get("aspect") else
                 "aspect:    # what | why | how | who | where | when")
    lines.append(f"status: {given.get('status', 'draft')}")
    path = os.path.join(a.lib, spec["dir"], f"{eid}.md")
    open(path, "w", encoding="utf-8").write("---\n" + "\n".join(lines) + "\n---\n\n"
                                            f"# {eid} {a.title}\n\nRationale and notes.\n")
    print(f"{eid}  {os.path.relpath(path, a.lib)}")


def cmd_check(a):
    entries, errors, warnings = check(a.lib)
    if a.json:
        print(json.dumps({"entries": len(entries), "errors": errors, "warnings": warnings}, indent=2))
    else:
        counts = defaultdict(int)
        for m in entries.values():
            counts[m["_dirtype"]] += 1
        print(f"library {a.lib}: {len(entries)} entries  " + ", ".join(f"{t} {counts[t]}" for t in TYPES if counts[t]))
        for e in errors:
            print(f"  error    {e}")
        for w in warnings:
            print(f"  warning  {w}")
        print(f"\n{'OK' if not errors else 'FAILED'}: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


def cmd_suggest(a):
    entries, errors, warnings = check(a.lib)
    down = children(entries)
    of = lambda t: sorted(e for e, m in entries.items() if m["_dirtype"] == t)
    title = lambda e: entries[e].get("title", "")
    items = []
    for e in errors:
        items.append((1, f"Fix: {e}"))
    for e in of("attribute"):
        m = entries[e]
        if not all(m.get(f) and not PLACEHOLDER.search(m[f]) for f in ("metric", "measurement", "target")):
            items.append((2, f"{e} '{title(e)}' is not yet measurable: give it a metric, a measurement method and a "
                             "target, or it can neither drive design nor prove assurance."))
    gaps = [("driver", "attribute", "no business attribute serves it: define what 'secure' means for this driver"),
            ("attribute", "objective", "no control objective protects it: add a CO citing it and the risks to it"),
            ("risk", "objective", "no control objective addresses it: treat it, or record why it is accepted"),
            ("objective", "service", "no security service meets it: add a logical service citing it"),
            ("service", "mechanism", "no mechanism realises it: add a physical mechanism"),
            ("mechanism", "component", "no component implements it: name the product, standard or tool")]
    for up, dn, what in gaps:
        for e in of(up):
            if not any(entries[c]["_dirtype"] == dn for c in down.get(e, ())):
                items.append((3, f"{e} '{title(e)}': {what}."))
    for e in of("attribute"):
        measured = [c for c in down.get(e, ()) if entries[c]["_dirtype"] in ("measure", "operation")]
        if not measured:
            items.append((4, f"{e} '{title(e)}' is never measured in operation: add a first-class measure (ME) "
                             "with target, data source, owner and threshold action; SO remains supported for 3.0 compatibility."))
    for e in of("measure"):
        if not any(entries[c]["_dirtype"] == "evidence" for c in down.get(e, ())):
            items.append((4, f"{e} '{title(e)}' has no collected evidence: add EV evidence so assurance proves operating effectiveness."))
    cover = defaultdict(int)
    for m in entries.values():
        cover[(TYPES[m["_dirtype"]]["layer"], aspect_of(m))] += 1
    cells = load_cells(a.lib)
    open_cells = [k for k, c in cells.items() if c["status"] in ("open", "missing")]
    for layer, aspect in open_cells:
        q, _ = QUESTIONS[(layer, aspect)]
        items.append((5, f"matrix/{layer}-{aspect}.md — {LAYER_INFO[layer][0]} · {INTERROGATIVE[aspect]}: answer "
                         f"“{q}”, or mark it not-applicable with a reason."))
    if not entries:
        items.append((1, "The library is empty. Start at the top: record the business drivers (BD), then the "
                         "attributes (BA) that say what 'secure' means for each, each with a metric and target."))
    names = {1: "integrity", 2: "measurability", 3: "coverage", 4: "assurance loop", 5: "matrix"}
    for rank in sorted({r for r, _ in items}):
        group = [t for r, t in items if r == rank]
        print(f"\n{rank}. {names[rank]} ({len(group)})")
        for t in group:
            print(f"   - {t}")
    print(f"\n{len(items)} suggestion(s), most important first. These are structural gaps; the reviewer adds "
          "judgement on whether each element is right, not only present.")


def cmd_trace(a):
    entries, _ = load(a.lib)
    if a.id not in entries:
        raise SabsaError(f"no entry {a.id}")
    down = children(entries)

    def up(e, depth=0):
        m = entries[e]
        print(f"{'  ' * depth}{e}  [{TYPES[m['_dirtype']]['layer']}]  {m.get('title', '')}")
        for p in parents(entries, e):
            up(p, depth + 1)

    print("upward, to the business drivers:")
    up(a.id)
    seen, q, impact = set(), [a.id], []
    while q:
        e = q.pop()
        for c in sorted(down.get(e, ())):
            if c not in seen:
                seen.add(c); impact.append(c); q.append(c)
    print(f"\ndownward: {len(impact)} element(s) depend on {a.id} and must be re-checked if it changes")
    for c in impact:
        print(f"  {c}  [{TYPES[entries[c]['_dirtype']]['layer']}]  {entries[c].get('title', '')}")



def _load_trace_views():
    path = os.path.join(SCHEMA_ROOT, "views.json")
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SabsaError(f"cannot load SABSA trace views {path}: {exc}") from exc
    return doc.get("views", {})

def _view_chains(entries, view, local_starts=False):
    steps = view.get("path", [])
    start_type = view.get("start_type")
    starts = sorted(e for e, m in entries.items() if m.get("_dirtype") == start_type and (not local_starts or not m.get("_external")))
    rows = [[e] for e in starts]
    for step in steps:
        nxt = []
        for row in rows:
            cur = row[-1]
            if cur == "—":
                nxt.append(row + ["—"]); continue
            m = entries.get(cur)
            if not m or m.get("_dirtype") != step.get("from"):
                nxt.append(row + ["—"]); continue
            refs = [r for r in ids(m.get(step.get("field")))
                    if r in entries and entries[r].get("_dirtype") == step.get("to")]
            if refs:
                nxt.extend(row + [r] for r in refs)
            else:
                nxt.append(row + ["—"] )
        rows = nxt
    return rows

def cmd_metamodel(a):
    print(f"SABSA metamodel {METAMODEL_VERSION}: {len(TYPES)} element types")
    print(f"Lifecycle model {LIFECYCLE_VERSION}: horizons {', '.join(ARCH_HORIZONS)}; states {', '.join(LIFECYCLE_STATES)}")
    print("\n| Type | Prefix | Layer | Cell | Business-parent relation(s) |")
    print("| --- | --- | --- | --- | --- |")
    for name, spec in TYPES.items():
        bp = ", ".join(spec.get("business_parent", ())) or "—"
        print(f"| {name} | {spec['prefix']} | {spec['layer']} | {spec['aspect']} | {bp} |")
    print("\nCommon lifecycle fields on every element: horizon, lifecycle_state, valid_from, valid_until, predecessors, transition_items")

def cmd_view(a):
    views = _load_trace_views()
    if a.view not in views:
        raise SabsaError(f"view must be one of {', '.join(sorted(views))}")
    entries, errors, _ = check(a.lib)
    if errors:
        raise SabsaError(f"library has {len(errors)} error(s); fix them before relying on trace views")
    view = views[a.view]
    columns = view.get("columns", [])
    print(f"# {view.get('title', a.view)}\n")
    print("| " + " | ".join(c.replace('-', ' ').title() for c in columns) + " |")
    print("| " + " | ".join("---" for _ in columns) + " |")
    rows = _view_chains(entries, view)
    for row in rows:
        print("| " + " | ".join(row) + " |")
    if not rows:
        print("| " + " | ".join(["—"] * max(1, len(columns))) + " |")


def _atomic_json(path, doc):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    open(tmp, "w", encoding="utf-8").write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def cmd_lifecycle(a):
    entries, errors, warnings = check(a.lib)
    if a.id:
        if a.id not in entries:
            raise SabsaError(f"no entry {a.id}")
        m = entries[a.id]
        print(f"# {a.id} {m.get('title','')}\n")
        print(f"type: {m['_dirtype']}")
        print(f"origin: {'reused from ' + m.get('_origin_library','') if m.get('_external') else 'local'}")
        print(f"horizon: {m.get('horizon') or 'unspecified'}")
        print(f"lifecycle_state: {m.get('lifecycle_state') or 'unspecified'}")
        print(f"valid_from: {m.get('valid_from') or '—'}")
        print(f"valid_until: {m.get('valid_until') or '—'}")
        print(f"predecessors: {m.get('predecessors') or '—'}")
        print(f"transition_items: {m.get('transition_items') or '—'}")
        if m.get('lifecycle_state') in LIFECYCLE_TRANSITIONS:
            print("allowed next lifecycle states: " + (", ".join(LIFECYCLE_TRANSITIONS[m['lifecycle_state']]) or "none"))
        return 1 if errors else 0
    print(f"# Architecture horizons and lifecycle — {os.path.basename(os.path.abspath(a.lib))}\n")
    for h in ARCH_HORIZONS:
        rows = [(e, m) for e, m in sorted(entries.items()) if not m.get("_external") and m.get("horizon") == h]
        print(f"## {h.title()} ({len(rows)})")
        for e, m in rows:
            print(f"- {e} [{m['_dirtype']}] {m.get('title','')} — {m.get('lifecycle_state') or 'lifecycle unspecified'}")
        if not rows: print("- —")
        print()
    unspecified = [(e,m) for e,m in sorted(entries.items()) if not m.get('_external') and not m.get('horizon')]
    if unspecified:
        print(f"## Unspecified horizon ({len(unspecified)})")
        for e,m in unspecified:
            print(f"- {e} [{m['_dirtype']}] {m.get('title','')}")
        print()
    print("## Current → transition → target mappings\n")
    print("| Current / predecessor | Roadmap / transition | Target | Type | Lifecycle |")
    print("| --- | --- | --- | --- | --- |")
    anyrow=False
    for e,m in sorted(entries.items()):
        if m.get('_external') or m.get('horizon') not in ('transition','target'):
            continue
        for pred in ids(m.get('predecessors')) or ['—']:
            for rm in ids(m.get('transition_items')) or ['—']:
                print(f"| {pred} | {rm} | {e} | {m['_dirtype']} | {m.get('lifecycle_state') or 'unspecified'} |")
                anyrow=True
    if not anyrow:
        print("| — | — | — | — | — |")
    return 1 if errors else 0


def cmd_lifecycle_set(a):
    entries, load_errors = load(a.lib)
    if load_errors:
        raise SabsaError(f"library has {len(load_errors)} load error(s); fix them before changing lifecycle state")
    if a.id not in entries:
        raise SabsaError(f"no entry {a.id}")
    m = entries[a.id]
    if m.get("_external"):
        raise SabsaError(f"{a.id} is reused from another library; change lifecycle metadata in its source library")
    path = os.path.join(a.lib, m["_path"])
    _ensure_native_jai_frontmatter(path, a.id)
    _ensure_native_library_frontmatter(a.lib)
    changed=[]
    if a.state is not None:
        if a.state not in LIFECYCLE_STATES:
            raise SabsaError(f"state must be one of {', '.join(LIFECYCLE_STATES)}")
        cur=m.get('lifecycle_state','')
        if cur and cur != a.state and a.state not in LIFECYCLE_TRANSITIONS.get(cur, ()):
            raise SabsaError(f"lifecycle transition {cur} -> {a.state} is not allowed; allowed: {', '.join(LIFECYCLE_TRANSITIONS.get(cur,())) or 'none'}")
        _frontmatter_set(path, "lifecycle_state", a.state); changed.append(f"lifecycle_state={a.state}")
    if a.horizon is not None:
        if a.horizon not in ARCH_HORIZONS:
            raise SabsaError(f"horizon must be one of {', '.join(ARCH_HORIZONS)}")
        _frontmatter_set(path, "horizon", a.horizon); changed.append(f"horizon={a.horizon}")
    if a.predecessor is not None:
        for pred in a.predecessor:
            if pred not in entries:
                raise SabsaError(f"predecessor {pred} does not exist")
            if entries[pred]["_dirtype"] != m["_dirtype"]:
                raise SabsaError(f"predecessor {pred} must be the same type ({m['_dirtype']})")
        _frontmatter_set(path, "predecessors", ", ".join(a.predecessor)); changed.append("predecessors=" + ",".join(a.predecessor))
    if a.roadmap is not None:
        for rm in a.roadmap:
            if rm not in entries or entries[rm]["_dirtype"] != "roadmap":
                raise SabsaError(f"transition roadmap {rm} must be an existing RM roadmap item")
        _frontmatter_set(path, "transition_items", ", ".join(a.roadmap)); changed.append("transition_items=" + ",".join(a.roadmap))
    if a.valid_from is not None:
        _frontmatter_set(path, "valid_from", a.valid_from); changed.append(f"valid_from={a.valid_from}")
    if a.valid_until is not None:
        _frontmatter_set(path, "valid_until", a.valid_until); changed.append(f"valid_until={a.valid_until}")
    if not changed:
        raise SabsaError("nothing to change; provide --state, --horizon, --predecessor, --roadmap, --valid-from or --valid-until")
    _frontmatter_set(path, "status", "draft")
    print(f"updated {a.id}: " + "; ".join(changed))
    print("element authoring status set to draft; any existing library approval is now stale")


def cmd_overlay_init(a):
    root=os.path.join(a.lib, OVERLAYS_DIR); os.makedirs(root, exist_ok=True)
    slug=re.sub(r"[^A-Za-z0-9._-]+", "-", a.id).strip("-").lower() or "framework"
    path=os.path.join(root, slug + ".json")
    if os.path.exists(path):
        raise SabsaError(f"{path} already exists")
    doc={"overlay_schema": 1,
         "framework":{"id":a.id,"title":a.title,"version":a.version,"source":a.source},
         "evidence_required": bool(a.evidence_required),
         "mappings":[]}
    _atomic_json(path,doc)
    print(f"created {os.path.relpath(path,a.lib)}")
    print("Add requirement identifiers and your own mapping/rationale only; the package does not reproduce licensed framework text.")


def cmd_overlays(a):
    entries, load_errors = load(a.lib)
    errors=list(load_errors); warnings=[]
    ovs=validate_overlays(a.lib, entries, errors, warnings)
    print(f"# External framework overlays — {len(ovs)} framework(s)\n")
    for ov in ovs:
        fw=ov.get('framework',{})
        stats=defaultdict(int)
        for mp in ov.get('mappings',[]) if isinstance(ov.get('mappings',[]),list) else []:
            if isinstance(mp,dict): stats[mp.get('status','')]+=1
        print(f"## {fw.get('id','?')} — {fw.get('title','')} {fw.get('version','')}")
        print(f"source: {fw.get('source','')} · mappings: {sum(stats.values())} · covered {stats['covered']} · partial {stats['partial']} · gap {stats['gap']} · n/a {stats['not-applicable']}")
        for mp in ov.get('mappings',[]) if isinstance(ov.get('mappings',[]),list) else []:
            if isinstance(mp,dict):
                print(f"- {mp.get('requirement','?')}: {mp.get('status','?')} → {mp.get('elements','—')} evidence {mp.get('evidence','—')}")
        print()
    for e in errors: print(f"error: {e}")
    for w in warnings: print(f"warning: {w}")
    return 1 if errors else 0


def cmd_reuse_add(a):
    cfg, errs=load_reuse_config(a.lib)
    if errs:
        raise SabsaError("; ".join(errs))
    if not _reuse_alias_ok(a.alias):
        raise SabsaError("alias must start with a letter and contain only letters, digits, '_' or '-'")
    if any(isinstance(x,dict) and x.get('alias')==a.alias for x in cfg.get('libraries',[])):
        raise SabsaError(f"reuse alias {a.alias} already exists")
    src=_resolve_reuse_path(a.lib,a.path)
    if not os.path.isfile(os.path.join(src,'library.md')):
        raise SabsaError(f"{a.path} is not a SABSA library")
    rel=os.path.relpath(src,os.path.abspath(a.lib))
    item={"alias":a.alias,"path":rel,"require_approved":not a.allow_unapproved}
    if a.types:
        vals=[x.strip() for x in a.types.split(',') if x.strip()]
        bad=sorted(set(vals)-set(TYPES))
        if bad: raise SabsaError("unknown type(s): " + ", ".join(bad))
        item['types']=vals
    if a.ids:
        item['ids']=[x.strip() for x in a.ids.split(',') if x.strip()]
    cfg.setdefault('schema',1); cfg.setdefault('libraries',[]).append(item)
    _atomic_json(os.path.join(a.lib,REUSE_FILE),cfg)
    print(f"added reusable library {a.alias} -> {rel}")
    print(f"references use namespace '{a.alias}:', e.g. {a.alias}:PL-001")
    if item['require_approved']:
        print("source approval is required; source snapshot drift will also invalidate this library's approval")


def cmd_reuse(a):
    cfg, errs=load_reuse_config(a.lib)
    entries, load_errors=load(a.lib)
    print(f"# Cross-library reuse — {len(cfg.get('libraries',[]))} source library/libraries\n")
    for item in cfg.get('libraries',[]):
        if not isinstance(item,dict): continue
        alias=item.get('alias','?'); src=_resolve_reuse_path(a.lib,item.get('path'))
        sm=parse(os.path.join(src,'library.md')) if os.path.isfile(os.path.join(src,'library.md')) else {}
        st=approval_state(src,_seen={os.path.abspath(a.lib)}) if sm else {'valid':False,'reason':'unavailable'}
        imported=[e for e,m in entries.items() if m.get('_reuse_alias')==alias]
        print(f"- **{alias}** → {item.get('path','')} · {sm.get('name','?')} {sm.get('version','')} · {len(imported)} imported element(s) · approval {'OK' if st.get('valid') else 'NOT OK'}")
        if not st.get('valid'): print(f"  {st.get('reason','')}")
        if item.get('types'): print("  selected types: " + ", ".join(item['types']))
        if item.get('ids'): print("  selected IDs: " + ", ".join(item['ids']))
    allerr=errs+load_errors
    if allerr:
        print("\nIssues:")
        for e in allerr: print(f"- {e}")
    return 1 if allerr else 0


def cmd_report(a):
    entries, errors, warnings = check(a.lib)
    lib = parse(os.path.join(a.lib, "library.md"))
    cover = defaultdict(list)
    for e, m in entries.items():
        cover[(TYPES[m["_dirtype"]]["layer"], aspect_of(m))].append(e)
    approval = approval_state(a.lib)
    print(f"# {lib.get('name')} — SABSA library report\n\n{lib.get('organisation')} · scope: {lib.get('scope')} · "
          f"version {lib.get('version')} · {len(entries)} entries · {len(errors)} error(s), {len(warnings)} warning(s) · "
          f"{'APPROVED' if approval.get('valid') else 'DRAFT / NOT APPROVED'}\n")
    if not approval.get("valid"):
        print(f"Approval gate: {approval.get('reason', 'not approved')}\n")
    print("## Matrix coverage\n\n| Layer | " + " | ".join(f"{v} ({k})" for k, v in ASPECTS.items()) + " |")
    print("| --- |" + " --- |" * 6)
    for l in LAYERS:
        print(f"| {l} | " + " | ".join(", ".join(sorted(cover[(l, k)])) or "·" for k in ASPECTS) + " |")
    print("\n## Traceability, component to driver\n\n| Component | Mechanism | Service | Objective | Attribute | Driver |")
    print("| --- | --- | --- | --- | --- | --- |")
    for c in sorted(e for e, m in entries.items() if m["_dirtype"] == "component"):
        for r in trace_chains(entries, c)[:20]:
            print("| " + " | ".join(r) + " |")
    print("\n## Measurement and evidence\n\n| Attribute | BAP metric / target | First-class measures | Evidence | Legacy operations |\n| --- | --- | --- | --- | --- |")
    down = children(entries)
    for e in sorted(x for x, m in entries.items() if m["_dirtype"] == "attribute"):
        m = entries[e]
        measures = sorted(c for c in down.get(e, ()) if entries[c]["_dirtype"] == "measure")
        ops = sorted(c for c in down.get(e, ()) if entries[c]["_dirtype"] == "operation")
        evidence = sorted(ev for me in measures for ev in down.get(me, ()) if entries[ev]["_dirtype"] == "evidence")
        print(f"| {e} {m.get('title', '')} | {m.get('metric', '')} / {m.get('target', '')} | {', '.join(measures) or '**none**'} | {', '.join(evidence) or '**none**'} | {', '.join(ops) or '—'} |")
    if errors:
        print("\n## Errors\n")
        for x in errors:
            print(f"- {x}")


def cmd_migrate(a):
    """Move elements from folders of earlier versions to where SABSA places them."""
    moved = 0
    for t, spec in TYPES.items():
        old = os.path.join(a.lib, spec.get("legacy", "") or "\0")
        if not spec.get("legacy") or not os.path.isdir(old):
            continue
        new = os.path.join(a.lib, spec["dir"])
        os.makedirs(new, exist_ok=True)
        for f in sorted(os.listdir(old)):
            if f.endswith(".md"):
                if os.path.exists(os.path.join(new, f)):
                    raise SabsaError(f"{spec['dir']}/{f} already exists; resolve by hand")
                os.rename(os.path.join(old, f), os.path.join(new, f)); moved += 1
        if not os.listdir(old):
            os.rmdir(old)
    os.makedirs(os.path.join(a.lib, "matrix"), exist_ok=True)
    made = 0
    for layer in LAYER_KEYS:
        for aspect in INTERROGATIVE:
            if not os.path.exists(cell_path(a.lib, layer, aspect)):
                scaffold_cell(a.lib, layer, aspect); made += 1
    _ensure_native_library_frontmatter(a.lib)
    entries, load_errors = load(a.lib)
    if load_errors:
        raise SabsaError(f"library has {len(load_errors)} load error(s); fix before JAI profile migration")
    profiled=0
    for eid,m in entries.items():
        if m.get("_external"): continue
        _ensure_native_jai_frontmatter(os.path.join(a.lib,m["_path"]),eid); profiled+=1
    print(f"moved {moved} element(s) to their SABSA layer; created {made} missing matrix cell(s); JAI-profiled {profiled} local element(s)")


def cmd_matrix(a):
    if a.scaffold:
        os.makedirs(os.path.join(a.lib, "matrix"), exist_ok=True)
        made = 0
        for layer in LAYER_KEYS:
            for aspect in INTERROGATIVE:
                if not os.path.exists(cell_path(a.lib, layer, aspect)):
                    scaffold_cell(a.lib, layer, aspect); made += 1
        print(f"created {made} missing cell(s)")
    entries, _ = load(a.lib)
    cells = load_cells(a.lib)
    mark = {"answered": "✓", "not-applicable": "n/a", "open": "·", "missing": "?"}
    print(f"{'':<20}" + "".join(f"{INTERROGATIVE[x]:<8}" for x in INTERROGATIVE))
    for layer in LAYER_KEYS:
        row = []
        for aspect in INTERROGATIVE:
            n = sum(1 for m in entries.values() if layer_key(m) == layer and aspect_of(m) == aspect)
            row.append(f"{mark[cells[(layer, aspect)]['status']]}{('+' + str(n)) if n else '':<7}"[:8].ljust(8))
        print(f"{LAYER_INFO[layer][0]:<20}" + "".join(row))
    done = sum(1 for c in cells.values() if c["status"] in ("answered", "not-applicable"))
    print(f"\n✓ answered  n/a not applicable  · open  ? missing   +N elements placed in the cell   ({done}/36 settled)")


def cmd_sources(a):
    entries, _ = load(a.lib)
    cells = load_cells(a.lib)
    d = os.path.join(a.lib, SOURCES_DIR)
    files = sorted(os.path.relpath(os.path.join(dp, f), a.lib).replace(os.sep, "/")
                   for dp, _, fs in os.walk(d) for f in fs if f != "README.md") if os.path.isdir(d) else []
    cited = collect_citations(a.lib, entries, cells)
    print(f"{len(files)} source file(s) in {SOURCES_DIR}/")
    for f in files:
        refs = sorted(cited[f])
        print(f"  {f:<50} cited by {len(refs)}: {' '.join(refs[:12])}" if refs
              else f"  {f:<50} NOT CITED — material not used yet")
    ext = sorted(k for k in cited if re.match(r"^[a-z]+://", k))
    if ext:
        print(f"\n{len(ext)} external source(s): " + ", ".join(ext))
    uncited = sorted(e for e, m in entries.items() if not m.get("_external") and not m.get("source") and m.get("basis") in ("stated", "inferred"))
    if uncited:
        print(f"\nstated/inferred elements citing nothing: {' '.join(uncited)}")


def questions(entries):
    out = defaultdict(list)
    for e, m in sorted(entries.items()):
        if m.get("basis") == "assumed":
            out[TYPES[m["_dirtype"]]["layer"]].append((e, m))
    return out


def cmd_questions(a):
    entries, _ = load(a.lib)
    q = questions(entries)
    cells = load_cells(a.lib)
    cell_q = [((lk, aspect), c) for (lk, aspect), c in cells.items()
              if c["status"] in ("answered", "not-applicable") and c["meta"].get("basis") == "assumed"]
    n = sum(len(v) for v in q.values()) + len(cell_q)
    print(f"# Questions for the client — {n} assumption(s) to confirm\n")
    i = 0
    for layer in LAYERS:
        for e, m in q.get(layer, []):
            i += 1
            what = m.get("statement") or m.get("definition") or m.get("description") or m.get("title", "")
            print(f"{i}. **{e} {m.get('title', '')}** ({layer}). We assumed: {what}")
            if m["_dirtype"] == "attribute":
                print(f"   Is the target **{m.get('target', '?')}** for *{m.get('metric', '?')}* right for you?")
            print("   Is this correct for your organisation? If not, what is the case?\n")
    for (lk, aspect), c in cell_q:
        i += 1
        what = c["answer"].split("\n")[0] if c["answer"] else c["meta"].get("reason", "")
        print(f"{i}. **matrix/{lk}-{aspect}** ({LAYER_INFO[lk][0]} · {INTERROGATIVE[aspect]}). We assumed: {what}")
        print("   Is this correct for your organisation? If not, what is the case?\n")
    if not n:
        print("No open assumptions: every settled element and matrix cell is stated or inferred from cited material.")


def cmd_document(a):
    """Render a document from a template. The output format follows the --out extension: the template's own
    format is written directly; .docx, .odt, .pdf and .html from a Markdown template go through pandoc, with a
    client's reference.docx supplying the Word styling."""
    path, label = resolve_template(a.lib, a.template_name, a.template)
    text, missing = render_template(open(path, encoding="utf-8").read(), build_model(a.lib))
    for name in missing:
        print(f"warning: the template uses '{name}', which the library does not provide (see 'sabsa.py template --fields')",
              file=sys.stderr)
    tpl_ext = os.path.splitext(path)[1].lower()
    out_ext = os.path.splitext(a.out)[1].lower() if a.out else tpl_ext
    if not a.out:
        print(text); return 0
    if out_ext == tpl_ext or out_ext in (".md", ".txt") and tpl_ext in (".md", ".txt"):
        open(a.out, "w", encoding="utf-8").write(text)
    else:
        import shutil, subprocess, tempfile
        if not shutil.which("pandoc"):
            raise SabsaError(f"writing {out_ext} needs pandoc (https://pandoc.org/installing.html); or write .md and "
                             "convert it yourself")
        with tempfile.NamedTemporaryFile("w", suffix=tpl_ext or ".md", delete=False, encoding="utf-8") as fh:
            fh.write(text); tmp = fh.name
        cmd = ["pandoc", tmp, "-o", a.out, "--from", "markdown" if tpl_ext == ".md" else tpl_ext.lstrip(".")]
        ref = resolve_reference_docx(a.lib, a.reference) if out_ext in (".docx", ".odt") else None
        if ref:
            cmd += ["--reference-doc", ref]
        if out_ext == ".html":
            cmd += ["--standalone", "--metadata", f"title={build_model(a.lib)['library'].get('name', 'SABSA')}"]
            css = os.path.join(a.lib, "templates", "style.css")
            if os.path.isfile(css):
                cmd += ["--css", css, "--embed-resources"]
        r = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
        os.remove(tmp)
        if r.returncode:
            raise SabsaError(f"pandoc failed: {r.stderr.strip()[:300]}")
        if ref:
            print(f"styled with {ref}")
    print(f"wrote {a.out} from {label} ({os.path.basename(path)})")
    return 0


def cmd_template(a):
    if a.init:
        src = os.path.join(PACKAGE_TEMPLATES, a.name + ".md")
        if not os.path.isfile(src):
            raise SabsaError(f"the package has no template '{a.name}'")
        d = os.path.join(a.lib, "templates")
        os.makedirs(d, exist_ok=True)
        dst = os.path.join(d, os.path.basename(src))
        if os.path.exists(dst):
            raise SabsaError(f"{dst} already exists; edit it, or delete it to start again")
        import shutil
        shutil.copy(src, dst)
        print(f"copied the default to {dst}. Edit it freely; 'document' now uses it for this library.")
        return 0
    if a.fields:
        def walk(v, name, depth):
            pad = "  " * depth
            if isinstance(v, dict):
                if name:
                    print(f"{pad}{name}  {{ }}")
                for k, x in v.items():
                    walk(x, k, depth + (1 if name else 0))
            elif isinstance(v, list):
                print(f"{pad}{name}  [list]  use {{{{#{name}}}}} ... {{{{/{name}}}}}")
                if v and isinstance(v[0], dict):
                    for k, x in v[0].items():
                        walk(x, k, depth + 1)
            else:
                print(f"{pad}{name}")
        print("Fields a template can use, as this library provides them:\n")
        walk(build_model(a.lib), "", 0)
        return 0
    path, label = resolve_template(a.lib, a.name, a.check)
    _, missing = render_template(open(path, encoding="utf-8").read(), build_model(a.lib))
    print(f"template '{a.name}' for {a.lib}: {path}  ({label})")
    if a.check or missing:
        print("  unknown fields: " + (", ".join(missing) if missing else "none — the template is consistent with the library"))
    return 1 if missing else 0

# -------------------------------------------------------------------------------------- selftest
def cmd_selftest(a):
    lib = os.path.join(tempfile.mkdtemp(prefix="sabsa-selftest-"), "lib")
    checks = []
    NS = argparse.Namespace
    import io, contextlib
    q = lambda: contextlib.redirect_stdout(io.StringIO())

    def expect(n, c):
        checks.append((n, bool(c)))

    def new(t, title, **f):
        with q():
            cmd_new(NS(lib=lib, type=t, title=title, set=[f"{k}={v}" for k, v in f.items()]))

    with q():
        cmd_init(NS(lib=lib, name="Test", organisation="Org", scope="payments", owner="CSA"))
    new("driver", "Customers trust digital payments", statement="Fraud erodes trust", owner="CEO", aspect="why")
    new("attribute", "Attributable", drivers="BD-001", definition="Every privileged action maps to a verified person",
        metric="share of privileged actions attributed", measurement="SIEM monthly", target="100%", owner="CISO", aspect="why")
    new("risk", "Untraceable admin action", kind="threat", statement="Shared admin accounts", attributes="BA-001", aspect="who")
    new("objective", "Privileged activity is attributable", statement="Log, attribute, review", attributes="BA-001",
        risks="RO-001", aspect="what")
    new("domain", "Privileged administration", scope="Privileged administration", authority="CISO", aspect="where")
    _, err, _ = check(lib)
    expect("a security domain must cite at least one control objective",
           any("DM-001" in e and "objectives" in e and "empty" in e for e in err))
    dp = os.path.join(lib, TYPES["domain"]["dir"], "DM-001.md")
    dt = open(dp, encoding="utf-8").read().replace("objectives: ", "objectives: CO-001")
    open(dp, "w", encoding="utf-8").write(dt)
    new("service", "Privileged activity monitoring", description="Collect and correlate", objectives="CO-001", domain="DM-001", aspect="how")
    new("mechanism", "Session recording", description="PAM recording", services="SS-001", aspect="how")
    new("component", "PAM vault", product="Vendor PAM 12", mechanisms="SM-001", aspect="where")
    _, err, _ = check(lib)
    expect("a fully traced chain driver -> component checks clean", not err)
    expect("... and suggest flags the attribute nobody measures in operation",
           "never measured in operation" in run(cmd_suggest, NS(lib=lib)))
    chains = trace_chains(load(lib)[0], "SC-001")
    expect("component-to-driver trace uses typed links and never puts a domain in the objective column",
           all(r[3] == "CO-001" and "DM-001" not in r for r in chains))
    new("operation", "Measure privileged attribution", metric="share attributed", frequency="monthly", owner="CISO",
        attributes="BA-001", aspect="how")
    _, err, _ = check(lib)
    expect("an operation without threshold_action is an error",
           any("SO-001" in e and "threshold_action" in e for e in err))
    op = os.path.join(lib, TYPES["operation"]["dir"], "SO-001.md")
    ot = open(op, encoding="utf-8").read()
    ot = re.sub(r"threshold_action: .*", "threshold_action: Escalate to the CISO and open corrective action", ot)
    open(op, "w", encoding="utf-8").write(ot)

    # ---- 3.1 declarative metamodel and first-class governance/assurance artefacts
    new("strategy", "Identity-first strategy", statement="Prefer attributable identity controls", rationale="Supports attributable administration",
        owner="CISO", attributes="BA-001", objectives="CO-001")
    new("domain", "Security monitoring", scope="Security telemetry", authority="SOC Manager", objectives="CO-001")
    new("trust", "PAM to monitoring trust", purpose="Deliver privileged telemetry", trust_basis="Mutual authenticated service identities",
        assurance_requirement="Certificate and log integrity validation", owner="CISO", source_domain="DM-001", target_domain="DM-002", objectives="CO-001")
    new("decision", "Use centralized PAM", decision="Centralize privileged access mediation", rationale="Consistent attribution and evidence",
        owner="CSA", objectives="CO-001")
    new("policy", "Privileged access policy", statement="Privileged actions require named identity and recording", owner="CISO",
        objectives="CO-001", services="SS-001")
    sp = os.path.join(lib, TYPES["service"]["dir"], "SS-001.md")
    st = open(sp, encoding="utf-8").read().replace("policies: ", "policies: PL-001")
    open(sp, "w", encoding="utf-8").write(st)
    new("entity", "Privileged administrators", population="Named privileged human administrators", owner="IAM Owner",
        objectives="CO-001", domains="DM-001")
    new("privilege", "PAM administrator", privileges="Approve and operate privileged sessions", conditions="No self-approval", owner="IAM Owner",
        entities="ET-001", policies="PL-001", objectives="CO-001")
    new("information-flow", "Privileged session telemetry", information="Session identity and activity telemetry", classification="security-sensitive",
        protection="Authenticated encrypted transport and integrity-protected storage", owner="SOC Manager", source_entity="ET-001", target_entity="ET-001",
        objectives="CO-001", services="SS-001")
    new("standard", "PAM hardening baseline", authority="Security Architecture", version="1.0", requirement="Harden and audit privileged access components",
        owner="Platform Owner", policies="PL-001", mechanisms="SM-001")
    new("measure", "Privileged attribution effectiveness", metric="attributed privileged actions", calculation="attributed/total * 100", unit="percent",
        data_source="SIEM", frequency="monthly", target="100%", warning_threshold="99.9%", breach_threshold="99%",
        threshold_action="Open corrective action and escalate to CISO", owner="CISO", evidence_retention="13 months", attributes="BA-001", services="SS-001")
    new("evidence", "Monthly attribution report", evidence_type="control effectiveness report", location="evidence://siem/monthly", collector="SOC",
        collected_at="monthly", result="measured result", owner="SOC Manager", measures="ME-001")
    new("exception", "Emergency break-glass exception", rationale="Continuity during PAM outage", risk_acceptance="CISO accepts time-bounded residual attribution risk",
        owner="CISO", expires="2027-01-01", review_date="2026-12-01", objectives="CO-001", policies="PL-001")
    new("roadmap", "Retire shared admin accounts", current_state="Some legacy shared accounts remain", target_state="All privileged access attributable",
        owner="IAM Owner", target_date="2027-03-31", acceptance_evidence="ME-001 reaches 100% for three periods", objectives="CO-001", components="SC-001")
    typed_entries, typed_err, _ = check(lib)
    expect("3.1 first-class strategy/policy/trust/entity/privilege/information/standard/measure/evidence/decision/exception/roadmap artefacts validate with typed relations",
           not [e for e in typed_err if any(x in e for x in ("SG-001","TR-001","AD-001","PL-001","ET-001","PV-001","IF-001","ST-001","ME-001","EV-001","EX-001","RM-001"))])
    assurance_rows = _view_chains(typed_entries, _load_trace_views()["assurance"])
    expect("assurance trace view follows only evidence -> measure -> attribute -> driver",
           ["EV-001", "ME-001", "BA-001", "BD-001"] in assurance_rows)
    # ---- 3.4 semantic completeness: previously narrative-only matrix cells are first-class artefacts
    new("business-process", "Payment settlement", description="Settle customer payments", criticality="critical", owner="COO", drivers="BD-001")
    new("business-actor", "Payments operator", actor_type="organisation role", accountability="Own settlement execution", owner="COO", drivers="BD-001", processes="BP-001")
    new("business-location", "EU operations", location="European Union", jurisdiction="EU", constraints="EU data and resilience obligations", owner="COO", drivers="BD-001")
    new("business-time-dependency", "Settlement deadline", event="daily settlement", deadline="17:00 CET", tolerance="15 minutes", owner="COO", drivers="BD-001", processes="BP-001")
    new("security-lifetime", "Privileged session lifetime", subject="privileged session", lifetime="15 minutes", renewal="re-authenticate", owner="CISO", attributes="BA-001", objectives="CO-001")
    new("domain-association", "Admin to platform boundary", relationship="privileged administration crosses platform trust boundary", boundary="administration API", owner="CISO", source_domain="DM-001", target_domain="DM-001", services="SS-001")
    new("processing-cycle", "Per-action authorisation", trigger="privileged action", sequence="authenticate, authorise, execute, record", review_cycle="per action", owner="CISO", services="SS-001")
    new("data-store", "Privileged audit store", technology="append-only log store", data_classes="security audit telemetry", retention="13 months", owner="SOC Manager", information_flows="IF-001", mechanisms="SM-001")
    new("security-procedure", "Privileged access procedure", procedure="request, approve, activate, monitor, revoke", trigger="privileged access request", owner="IAM Owner", policies="PL-001", mechanisms="SM-001")
    new("interaction-endpoint", "Admin workstation", endpoint_type="human workstation", interface="PAM client", owner="IAM Owner", entities="ET-001", services="SS-001")
    new("platform-zone", "PAM control zone", platform="PAM platform", network_zone="restricted admin zone", location="primary region", owner="Platform Owner", mechanisms="SM-001", domains="DM-001")
    new("control-sequence", "Privileged control sequence", sequence="authenticate, authorise, broker, record", timing="synchronous per session", failure_action="deny and alert", owner="IAM Owner", mechanisms="SM-001")
    new("data-format", "Audit event schema", schema="actor/action/resource/result/timestamp", encoding="JSON UTF-8", validation="schema validation", owner="SOC Manager", data_stores="DS-001")
    new("identity-entitlement", "PAM operator entitlement", principal="named administrator", entitlement="PAM operator", conditions="no self approval", owner="IAM Owner", privileges="PV-001", components="SC-001")
    new("endpoint-protocol", "PAM API endpoint", endpoint="PAM API", address="service endpoint", port="443", protocol="TLS HTTPS", owner="Platform Owner", components="SC-001", platform_zones="PZ-001")
    new("component-timing", "PAM rotation schedule", timeout="15 minutes", schedule="per privileged session", rotation_interval="24 hours", owner="IAM Owner", components="SC-001", control_sequences="CQ-001")
    new("support-model", "PAM support model", support_scope="privileged access service", support_hours="24x7", escalation_path="Service Desk -> IAM -> Security", owner="IAM Owner", services="SS-001", operations="SO-001")
    new("operational-location", "PAM operational zone", location="primary admin platform", operational_controls="patching, vulnerability management, physical/cloud controls", maintenance_owner="Platform Owner", owner="Platform Owner", platform_zones="PZ-001", operations="SO-001")
    typed34, err34, _ = check(lib)
    ids34 = ("BP-001","AC-001","BL-001","BT-001","LT-001","DA-001","PC-001","DS-001","PR-001","IN-001","PZ-001","CQ-001","DF-001","IE-001","EP-001","CT-001","SU-001","OL-001")
    expect("3.4 validates first-class artefacts for every matrix cell that was narrative-only in 3.3",
           not [e for e in err34 if any(x in e for x in ids34)] and all(x in typed34 for x in ids34))
    typed_cells = {(LAYER_OF_NAME[spec["layer"]], spec["aspect"]) for spec in TYPES.values()}
    expect("the active 3.4 metamodel is declarative and gives every SABSA matrix cell a first-class typed artefact",
           METAMODEL_VERSION == "3.4" and LIFECYCLE_VERSION == "3.2" and len(TYPES) == 39
           and typed_cells == set(QUESTIONS))

    # ---- 3.2 lifecycle/current-target-transition and external framework overlays
    run(cmd_lifecycle_set, NS(lib=lib, id="PL-001", state="operational", horizon="current", predecessor=None, roadmap=None,
                              valid_from="2026-01-01", valid_until=None))
    new("policy", "Target privileged access policy", statement="All privileged access uses phishing-resistant named identity and recording",
        owner="CISO", objectives="CO-001", services="SS-001", horizon="target", lifecycle_state="approved",
        predecessors="PL-001", transition_items="RM-001")
    life = run(cmd_lifecycle, NS(lib=lib, id=None))
    expect("3.2 models explicit current -> roadmap -> target architecture transitions",
           "PL-001" in life and "RM-001" in life and "PL-002" in life and "Current → transition → target" in life)
    try:
        run(cmd_lifecycle_set, NS(lib=lib, id="PL-001", state="approved", horizon=None, predecessor=None, roadmap=None,
                                  valid_from=None, valid_until=None))
        illegal=False
    except SabsaError:
        illegal=True
    expect("lifecycle-set rejects an invalid backwards transition such as operational -> approved", illegal)
    run(cmd_overlay_init, NS(lib=lib, id="TEST-FW", title="Test framework", version="1.0", source="https://example.invalid/framework",
                             evidence_required=True))
    opath=os.path.join(lib, OVERLAYS_DIR, "test-fw.json")
    odoc=json.load(open(opath,encoding="utf-8"))
    odoc["mappings"]=[{"requirement":"R-1","title":"Test requirement","status":"covered","elements":"PL-001, CO-001",
                       "evidence":"EV-001","roadmap":"","exceptions":"","rationale":"Mapped by design and evidence","owner":"CISO"},
                      {"requirement":"R-2","title":"Future requirement","status":"gap","elements":"","evidence":"",
                       "roadmap":"RM-001","exceptions":"","rationale":"Planned treatment","owner":"CISO"}]
    _atomic_json(opath,odoc)
    oerrs=[]; owarns=[]; validate_overlays(lib, load(lib)[0], oerrs, owarns)
    expect("framework overlays validate covered/gap mappings without embedding framework text", not oerrs and not owarns)
    overlay_report=run(cmd_overlays, NS(lib=lib))
    expect("framework overlay report exposes coverage and gap status", "covered 1" in overlay_report and "gap 1" in overlay_report)

    new("component", "Orphan tool", product="X", aspect="where")
    _, err, _ = check(lib)
    expect("a component citing no mechanism is an error: it traces to nothing",
           any("SC-002" in e and "empty" in e for e in err))
    p = os.path.join(lib, TYPES["component"]["dir"], "SC-002.md")

    def edit(old, new_):
        text = open(p, encoding="utf-8").read()                 # read first: open(p, "w") would truncate before the read
        open(p, "w", encoding="utf-8").write(text.replace(old, new_))

    edit("mechanisms: ", "mechanisms: SM-999")
    _, err, _ = check(lib)
    expect("a dangling link is an error", any("SM-999" in e for e in err))
    edit("SM-999", "BA-001")
    _, err, _ = check(lib)
    expect("a link to the wrong kind of element is an error", any("must cite mechanism" in e for e in err))
    os.remove(p)
    new("attribute", "Available", drivers="BD-001", definition="<x>", metric="", measurement="", target="", owner="COO")
    _, err, _ = check(lib)
    expect("an attribute without metric, measurement and target is an error (not measurable)",
           any("BA-002" in e and "metric" in e for e in err))
    out = run(cmd_trace, NS(lib=lib, id="BA-001"))
    expect("trace shows the downward impact of changing an attribute",
           all(x in out for x in ("CO-001", "SS-001", "SM-001", "SC-001")))

    open(os.path.join(lib, SOURCES_DIR, "brief.md"), "w", encoding="utf-8").write("# Brief\n## Goals\nGrow partners\n")
    new("driver", "Grow through partners", statement="Partner revenue doubles", owner="CEO", aspect="why",
        source="00-sources/brief.md#goals", basis="stated")
    new("driver", "Cited from nowhere", statement="x", owner="CEO", aspect="why", source="00-sources/missing.md",
        basis="stated")
    new("driver", "Said but not sourced", statement="x", owner="CEO", aspect="why", basis="stated")
    new("driver", "Probably regulated", statement="PSD2 applies", owner="CEO", aspect="why", basis="assumed")
    _, err, _ = check(lib)
    expect("a cited source that is not in 00-sources is an error", any("BD-003" in e and "missing.md" in e for e in err))
    expect("'stated' with no source is an error: which material says so?", any("BD-004" in e and "no source" in e for e in err))
    expect("a stated, sourced driver raises no source error", not any("BD-002" in e for e in err))
    qs = run(cmd_questions, NS(lib=lib))
    expect("an assumption becomes a question for the client", "BD-005" in qs and "PSD2 applies" in qs)
    expect("sources shows which elements cite each file", "cited by 1: BD-002" in run(cmd_sources, NS(lib=lib)))
    doc = run(cmd_document, NS(lib=lib, out=None, template_name="architecture", template=None, reference=None))
    expect("the document carries every section, the draft banner and the client questions",
           all(x in doc for x in ("## 3. Basis of this document", "## 4. Contextual layer", "## 10. Business attribute profile",
                                  "## 11. Traceability", "## 13. Open assumptions", "Annex B. Consistency check",
                                  "DRAFT", "PSD2 applies")))

    # ---- the matrix and templates
    expect("init scaffolds all 36 matrix cells, each with its own question",
           len(os.listdir(os.path.join(lib, "matrix"))) == 36
           and "Where does the business operate" in open(cell_path(lib, "contextual", "where"), encoding="utf-8").read())
    open(cell_path(lib, "component", "when"), "w", encoding="utf-8").write(
        "---\nlayer: component\naspect: when\nstatus: not-applicable\n---\n")
    _, err, _ = check(lib)
    expect("a cell marked not-applicable without a reason is an error", any("component-when" in e and "reason" in e for e in err))
    open(cell_path(lib, "contextual", "where"), "w", encoding="utf-8").write(
        "---\nlayer: contextual\naspect: where\nbasis: stated\nsource: 00-sources/brief.md\n---\n# x\n\nPrague; EU-wide.\n")
    cells = load_cells(lib)
    expect("an answered cell is read as answered, with its text", cells[("contextual", "where")]["status"] == "answered"
           and "Prague" in cells[("contextual", "where")]["answer"])
    open(cell_path(lib, "contextual", "how"), "w", encoding="utf-8").write(
        "---\nlayer: contextual\naspect: how\n---\n# x\n\nOnline payment processing.\n")
    _, err, _ = check(lib)
    expect("a settled matrix cell without basis is an error",
           any("contextual-how" in e and "no basis" in e for e in err))
    open(cell_path(lib, "contextual", "how"), "w", encoding="utf-8").write(
        "---\nlayer: contextual\naspect: how\nbasis: assumed\n---\n# x\n\nOnline payment processing.\n")
    expect("an assumed matrix cell becomes a client question",
           "matrix/contextual-how" in run(cmd_questions, NS(lib=lib)))
    open(cell_path(lib, "contextual", "how"), "w", encoding="utf-8").write(
        "---\nlayer: contextual\naspect: how\nbasis: stated\nsource: 00-sources/brief.md\n---\n# x\n\nOnline payment processing.\n")
    expect("source usage includes citations from matrix cells",
           "matrix/contextual-how" in run(cmd_sources, NS(lib=lib)))
    doc = run(cmd_document, NS(lib=lib, out=None, template_name="architecture", template=None, reference=None))
    expect("the default document has all six layer sections, each asking all six questions",
           all(f"layer — {LAYER_INFO[k][1]}" in doc for k in LAYER_KEYS)
           and doc.count("### What") == 6 and doc.count("### When") == 6 and "Prague; EU-wide." in doc)
    legacy = os.path.join(lib, "01-contextual", "attributes"); os.makedirs(legacy, exist_ok=True)
    os.rename(os.path.join(lib, TYPES["attribute"]["dir"], "BA-001.md"), os.path.join(legacy, "BA-001.md"))
    _, err, _ = check(lib)
    flagged = any("old folder" in e for e in err)
    run(cmd_migrate, NS(lib=lib))
    expect("an attribute in the pre-correction folder is flagged, and migrate moves it to the Conceptual layer",
           flagged and os.path.isfile(os.path.join(lib, TYPES["attribute"]["dir"], "BA-001.md")))
    home = os.path.join(os.path.dirname(lib), "home"); os.environ["AI_IT_HOME"] = home
    expect("with no override, the package default template applies",
           resolve_template(lib, "architecture")[1] == "the package default")
    os.makedirs(os.path.join(home, "sabsa-templates"))
    open(os.path.join(home, "sabsa-templates", "architecture.md"), "w", encoding="utf-8").write("# personal {{library.name}}\n")
    expect("a personal template overrides the package default", resolve_template(lib, "architecture")[1] == "your personal template")
    run(cmd_template, NS(lib=lib, name="architecture", init=True, fields=False, check=None))
    expect("the library's own template overrides both", resolve_template(lib, "architecture")[1] == "the library's own template")
    _, missing = render_template("{{library.nmae}} {{library.name}} {{#layers}}{{nme}}{{/layers}}", build_model(lib))
    expect("unknown fields are reported, including a typo after a dot", missing == ["library.nmae", "nme"])
    import shutil
    if shutil.which("pandoc"):
        out = os.path.join(os.path.dirname(lib), "a.docx")
        run(cmd_document, NS(lib=lib, out=out, template_name="architecture", template=None, reference=None))
        import zipfile
        expect("a Word document is produced through pandoc", zipfile.is_zipfile(out))
    del os.environ["AI_IT_HOME"]

    # ---- release governance: approval is explicit and bound to the exact architecture snapshot
    clean = os.path.join(tempfile.mkdtemp(prefix="sabsa-approval-selftest-"), "lib")
    with q():
        cmd_init(NS(lib=clean, name="Approval test", organisation="Org", scope="test", owner="CSA"))
    open(os.path.join(clean, SOURCES_DIR, "brief.md"), "w", encoding="utf-8").write("# Brief\nApproved test basis.\n")
    with q():
        cmd_new(NS(lib=clean, type="driver", title="Business continuity",
                   set=["statement=Business service must continue", "owner=CEO",
                        "source=00-sources/brief.md", "basis=stated"]))
    for lk in LAYER_KEYS:
        for aspect in INTERROGATIVE:
            open(cell_path(clean, lk, aspect), "w", encoding="utf-8").write(
                f"---\nlayer: {lk}\naspect: {aspect}\nstatus: not-applicable\n"
                "reason: Test fixture deliberately limits scope to approval mechanics\n"
                "basis: stated\nsource: 00-sources/brief.md\n---\n")
    _, cerr, cwarn = check(clean)
    expect("a clean fully settled library has no structural warnings before approval", not cerr and not cwarn)
    approve_out = run(cmd_approve, NS(lib=clean, by="CSA", note="selftest approval"))
    expect("owner approval records a hash-bound current snapshot",
           "snapshot sha256" in approve_out and approval_state(clean).get("valid"))
    approved_doc = run(cmd_document, NS(lib=clean, out=None, template_name="architecture", template=None, reference=None))
    expect("an approved clean snapshot renders without a DRAFT banner", "> **DRAFT.**" not in approved_doc)
    drv = os.path.join(clean, TYPES["driver"]["dir"], "BD-001.md")
    open(drv, "a", encoding="utf-8").write("\nChanged after approval.\n")
    expect("any architecture-input change invalidates the recorded approval",
           not approval_state(clean).get("valid") and "stale" in approval_state(clean).get("reason", ""))
    stale_doc = run(cmd_document, NS(lib=clean, out=None, template_name="architecture", template=None, reference=None))
    expect("a stale approval forces the generated document back to DRAFT", "> **DRAFT.**" in stale_doc)

    # ---- 3.2 cross-library reuse: namespaced refs and dependency-bound approval
    src = os.path.join(tempfile.mkdtemp(prefix="sabsa-reuse-source-"), "lib")
    with q(): cmd_init(NS(lib=src, name="Enterprise reference", organisation="Org", scope="enterprise", owner="CSA"))
    open(os.path.join(src,SOURCES_DIR,"brief.md"),"w",encoding="utf-8").write("# Enterprise brief\nShared driver.\n")
    with q(): cmd_new(NS(lib=src,type="driver",title="Shared resilience",set=["statement=Enterprise services require resilience","owner=CEO","basis=stated","source=00-sources/brief.md","horizon=reference","lifecycle_state=approved"]))
    for lk in LAYER_KEYS:
        for aspect in INTERROGATIVE:
            open(cell_path(src,lk,aspect),"w",encoding="utf-8").write(
                f"---\nlayer: {lk}\naspect: {aspect}\nstatus: not-applicable\nreason: Reference-library selftest scope\nbasis: stated\nsource: 00-sources/brief.md\n---\n")
    expect("reference library is clean before reuse approval", not check(src)[1] and not check(src)[2])
    run(cmd_approve, NS(lib=src,by="Enterprise CSA",note="reference approval"))
    consumer = os.path.join(tempfile.mkdtemp(prefix="sabsa-reuse-consumer-"), "lib")
    with q(): cmd_init(NS(lib=consumer,name="Solution",organisation="Org",scope="solution",owner="Solution CSA"))
    open(os.path.join(consumer,SOURCES_DIR,"brief.md"),"w",encoding="utf-8").write("# Solution brief\nSolution inherits enterprise resilience intent.\n")
    run(cmd_reuse_add, NS(lib=consumer,alias="enterprise",path=src,types="driver",ids=None,allow_unapproved=False))
    with q(): cmd_new(NS(lib=consumer,type="attribute",title="Solution resilient",set=["drivers=enterprise:BD-001","definition=Solution tolerates agreed failures","metric=availability","measurement=monthly service report","target=99.9%","owner=Service Owner","basis=inferred","source=00-sources/brief.md","horizon=current","lifecycle_state=operational"]))
    for lk in LAYER_KEYS:
        for aspect in INTERROGATIVE:
            open(cell_path(consumer,lk,aspect),"w",encoding="utf-8").write(
                f"---\nlayer: {lk}\naspect: {aspect}\nstatus: not-applicable\nreason: Reuse selftest scope\nbasis: stated\nsource: 00-sources/brief.md\n---\n")
    ce, cerr, cwarn = check(consumer)
    expect("consumer resolves a namespaced cross-library business-parent reference", not cerr and not cwarn and "enterprise:BD-001" in ce)
    run(cmd_approve, NS(lib=consumer,by="Solution CSA",note="consumer approval"))
    expect("consumer approval is valid while the approved reused snapshot is unchanged", approval_state(consumer).get("valid"))
    spath=os.path.join(src,TYPES["driver"]["dir"],"BD-001.md")
    open(spath,"a",encoding="utf-8").write("\nChanged shared architecture after downstream approval.\n")
    expect("change in a reused source library invalidates the consumer snapshot approval", not approval_state(consumer).get("valid"))

    views = _load_document_views()
    expect("3.2 declares specialised document views and every package template exists",
           len(views) >= 18 and all(os.path.isfile(os.path.join(PACKAGE_TEMPLATES, name + ".md")) for name in views))
    template_missing=[]
    for name in views:
        model = build_model(consumer if name == "reuse-register" else lib)
        _, miss = render_template(open(os.path.join(PACKAGE_TEMPLATES, name + ".md"), encoding="utf-8").read(), model)
        template_missing += [f"{name}:{x}" for x in miss]
    expect("all specialised package document views render against the 3.2 document model without unknown fields",
           not template_missing)

    # ---- regression: a component whose chains end at different depths (one per mechanism it cites)
    new("mechanism", "Dead end", description="cites no service", aspect="how")
    dead = sorted(e for e, m in load(lib)[0].items() if m.get("title") == "Dead end")[0]
    for order in (f"SM-001, {dead}", f"{dead}, SM-001"):
        new("component", f"Two chains ({order})", product="P", mechanisms=order, aspect="where")
    ent = load(lib)[0]
    multi = sorted(e for e, m in ent.items() if m.get("title", "").startswith("Two chains"))
    chains = [trace_chains(ent, c) for c in multi]
    expect("traceability: each chain of a component is followed on its own, whichever is cited first",
           all(any(r[1] == "SM-001" and r[-1].startswith("BD-") for r in ch) and
               any(r[1] == dead and r[2:] == ["—"] * 4 for r in ch) for ch in chains))
    try:
        run(cmd_report, NS(lib=lib))
        run(cmd_document, NS(lib=lib, out=None, template_name="architecture", template=None, reference=None))
        expect("report and document both handle a component whose chains end at different depths", True)
    except KeyError as e:
        expect(f"report and document both handle chains of different depths (KeyError {e})", False)

    for n, ok in checks:
        print(f"  {'pass' if ok else 'FAIL'}  {n}")
    bad = sum(1 for _, ok in checks if not ok)
    print(f"\n{len(checks) - bad} of {len(checks)} checks passed")
    return 1 if bad else 0


def run(fn, ns):
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(ns)
    return buf.getvalue()


def main():
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description="SABSA library tool.")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("init"); p.add_argument("lib")
    for f in ("name", "organisation", "scope", "owner"):
        p.add_argument(f"--{f}", required=True)
    p.set_defaults(fn=cmd_init)
    p = sp.add_parser("new"); p.add_argument("lib"); p.add_argument("type", choices=sorted(TYPES))
    p.add_argument("--title", required=True); p.add_argument("--set", action="append")
    p.set_defaults(fn=cmd_new)
    p = sp.add_parser("check"); p.add_argument("lib"); p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_check)
    for name, fn in (("suggest", cmd_suggest), ("report", cmd_report)):
        p = sp.add_parser(name); p.add_argument("lib"); p.set_defaults(fn=fn)
    p = sp.add_parser("trace"); p.add_argument("lib"); p.add_argument("id"); p.set_defaults(fn=cmd_trace)
    p = sp.add_parser("view"); p.add_argument("lib"); p.add_argument("view", choices=sorted(_load_trace_views())); p.set_defaults(fn=cmd_view)
    sp.add_parser("metamodel").set_defaults(fn=cmd_metamodel)
    p = sp.add_parser("lifecycle"); p.add_argument("lib"); p.add_argument("id", nargs="?"); p.set_defaults(fn=cmd_lifecycle)
    p = sp.add_parser("lifecycle-set"); p.add_argument("lib"); p.add_argument("id")
    p.add_argument("--state", choices=LIFECYCLE_STATES); p.add_argument("--horizon", choices=ARCH_HORIZONS)
    p.add_argument("--predecessor", action="append"); p.add_argument("--roadmap", action="append")
    p.add_argument("--valid-from"); p.add_argument("--valid-until"); p.set_defaults(fn=cmd_lifecycle_set)
    p = sp.add_parser("overlay-init"); p.add_argument("lib"); p.add_argument("--id", required=True)
    p.add_argument("--title", required=True); p.add_argument("--version", required=True); p.add_argument("--source", required=True)
    p.add_argument("--evidence-required", action="store_true"); p.set_defaults(fn=cmd_overlay_init)
    p = sp.add_parser("overlays"); p.add_argument("lib"); p.set_defaults(fn=cmd_overlays)
    p = sp.add_parser("reuse-add"); p.add_argument("lib"); p.add_argument("alias"); p.add_argument("path")
    p.add_argument("--types", help="comma-separated element types to import; dependencies are added automatically")
    p.add_argument("--ids", help="comma-separated element IDs to import; dependencies are added automatically")
    p.add_argument("--allow-unapproved", action="store_true", help="do not require the source library to be owner-approved")
    p.set_defaults(fn=cmd_reuse_add)
    p = sp.add_parser("reuse"); p.add_argument("lib"); p.set_defaults(fn=cmd_reuse)
    p = sp.add_parser("migrate"); p.add_argument("lib"); p.set_defaults(fn=cmd_migrate)
    p = sp.add_parser("matrix"); p.add_argument("lib"); p.add_argument("--scaffold", action="store_true")
    p.set_defaults(fn=cmd_matrix)
    for name, fn in (("sources", cmd_sources), ("questions", cmd_questions), ("approval", cmd_approval)):
        p = sp.add_parser(name); p.add_argument("lib"); p.set_defaults(fn=fn)
    p = sp.add_parser("approve"); p.add_argument("lib"); p.add_argument("--by", required=True)
    p.add_argument("--note", help="approval note / decision reference")
    p.set_defaults(fn=cmd_approve)
    p = sp.add_parser("document"); p.add_argument("lib")
    p.add_argument("--out", help="output file; its extension sets the format (.md .html .docx .odt .pdf)")
    p.add_argument("--template-name", default="architecture", help="which template: architecture, client-questions, ...")
    p.add_argument("--template", help="use this template file instead of resolving one")
    p.add_argument("--reference", help="a .docx whose styles a Word output should use (the client's template)")
    p.set_defaults(fn=cmd_document)
    p = sp.add_parser("documents"); p.add_argument("lib"); p.set_defaults(fn=cmd_documents)
    p = sp.add_parser("template"); p.add_argument("lib"); p.add_argument("--name", default="architecture")
    p.add_argument("--init", action="store_true", help="copy the package default into <lib>/templates/ to edit")
    p.add_argument("--fields", action="store_true", help="list every field a template can use")
    p.add_argument("--check", metavar="FILE", help="render FILE against the library and report unknown fields")
    p.set_defaults(fn=cmd_template)
    sp.add_parser("selftest").set_defaults(fn=cmd_selftest)
    a = ap.parse_args()
    try:
        return a.fn(a) or 0
    except SabsaError as exc:
        print(f"sabsa: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
