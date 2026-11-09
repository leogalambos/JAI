#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Build explicit proposed workflow acceptance bindings from editorial mappings."""
from pathlib import Path
import argparse
import copy
import json
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_spec import canonical_hash

from content_workflow import HANDOFF_CONTENT_CONTRACTS, SELECTIONS
from workflow_professional_definitions import (HANDOFF_REQUIREMENTS, WORKFLOW_PROFILES,
    WORKFLOW_VARIANT_CONDITIONS, WORKFLOW_MECHANISMS, WORKFLOW_PATH_STEPS,
    VARIANT_HANDOFF_REQUIREMENTS, ONBOARDING_MECHANISMS, ONBOARDING_OVERLAYS,
    VARIANT_SCOPE_ASSESSMENTS, ONBOARDING_OVERLAY_REQUIREMENTS)


# Explicit source-owned publication contracts; these stages intentionally have no
# professional role-deliverable ID. Their requirements remain canonical here.
SOURCE_HANDOFF_CONTENT = {
    'ai-system-approval:6': {
        'required': [
            'Identify the named human authority, exact candidate version, intended use, deployment scope and reviewed risk and assurance evidence.',
            'Record the actual approval, rejection or conditional decision before the corresponding production effects; an agent recommendation is not authority.',
            'Identify conditions, unresolved evidence, monitoring obligations, validity and change triggers; reference verified external approval where the governing profile requires it.'],
        'conditional': [{'when': 'Evidence requires a bounded pilot before final approval.', 'requirement': 'Reference prior authority for that exact pilot scope, safeguards and stop conditions; pilot evidence does not authorise broader production use.'}],
        'optional': ['Decision communication within the authorised scope.']},
    'semantic-to-enterprise-publication:1': {
        'required': [
            'Identify the exact semantic model version, intended audience, purpose, scope and requested publication formats.',
            'State claims, decisions, alternatives and rationale; link material claims to evidence and distinguish facts, assumptions and unresolved questions.',
            'Identify acceptance criteria, source references, classification, disclosure limits and the owners of unresolved items.'],
        'conditional': [{'when': 'The publication requests a consequential decision.', 'requirement': 'Identify the accountable decision authority, exact decision requested and residual risks requiring disposition.'}],
        'optional': ['Supporting calculations and detailed source annexes referenced by material claims.']},
    'semantic-to-enterprise-publication:2': {
        'required': [
            'Identify reviewer, independence, exact source version and the criteria and evidence actually assessed.',
            'Locate each finding against a claim or criterion; record significance, evidence limits and required resolution.',
            'State a bounded semantic verdict, unresolved findings and any explicit waiver reference without treating missing evidence as a pass.'],
        'conditional': [{'when': 'The governing policy permits a waiver and one is relied upon.', 'requirement': 'Reference prior explicit authority for that exact criterion, scope, rationale, limits and expiry where specified; a reviewer cannot create permission to waive a mandatory gate.'}],
        'optional': ['Comparative recommendations that do not alter the underlying decision.']},
    'semantic-to-enterprise-publication:3': {
        'required': [
            'Identify the approved semantic input version and digest, selected publication archetype, audience and requested formats.',
            'Supply the actual rendered files with a manifest linking every rendition to the same semantic source; preserve claims, caveats and decisions.',
            'Record document identity, classification, references, generation limitations and dependencies needed to reproduce the projection.'],
        'conditional': [{'when': 'A required renderer or format is unavailable.', 'requirement': 'Identify the missing rendition and blocking limitation; do not claim it was produced or inspected.'}],
        'optional': ['Additional audience projections whose semantic equivalence is established.']},
    'semantic-to-enterprise-publication:4': {
        'required': [
            'Identify reviewer, exact rendered files, source binding, inspected formats and actual viewing or rendering method.',
            'Record located findings for legibility, hierarchy, density, tables, diagrams, document control and package integrity.',
            'State the publication verdict and limitations, defect disposition, and any explicit waiver; distinguish static checks from observed visual inspection.'],
        'conditional': [{'when': 'An output format or part of the package could not be inspected.', 'requirement': 'Record the missing inspection and its impact; retain the blocked state unless the governing policy permits and the exact authority explicitly approves a scoped disposition before release.'}],
        'optional': ['Annotated previews and presentation recommendations supporting the findings.']},
    'semantic-to-enterprise-publication:5': {
        'required': [
            'Identify the actual accountable authority, exact publication version and files, permitted audience and release scope.',
            'Reference the applicable semantic and publication reviews, unresolved risks and any authorised conditions or waivers.',
            'Record the explicit decision and its effective conditions using the existing authority mechanism; a drafted request or agent assertion is not approval.'],
        'conditional': [{'when': 'The governing decision requires an L0 signature.', 'requirement': 'Reference the actual operator-signed decision bound to these effects; do not manufacture a signature or inherit another output approval.'}],
        'optional': ['Communication instructions that stay within the approved audience and scope.']},
}


def professional_workflows(root=ROOT):
    """Return canonical workflows enriched by exact authored professional profiles.

    Args:
        root: Checkout containing canonical workflow rows.
    Returns:
        A copy of the complete workflow registry with explicit intake, route and
        handoff requirements. Shared intake evidence is referenced, not repeated.
    Raises:
        ValueError: An authored workflow/step is missing or has an invalid field list.
        OSError: The canonical source cannot be read.
    """
    document = json.loads((Path(root) / '.ai/runtime/workflows.json').read_text())
    workflows = document['workflows']
    keys = {workflow['key'] for workflow in workflows}
    if keys != set(HANDOFF_REQUIREMENTS) or keys != set(WORKFLOW_PROFILES) or keys != set(SELECTIONS):
        raise ValueError('WORKFLOW_PROFESSIONAL_PROFILE_COVERAGE')
    for workflow in workflows:
        key = workflow['key']
        if key == 'new-service-onboarding':
            workflow['outcome'] = 'An owned service with controlled configuration and change, proportionate validation, observability, support, recovery and service-level evidence.'
            neutral = {
                2: ('controlled service configuration baseline and verification evidence', 'Service configuration is versioned, reviewed and verified against the selected mechanism and applicable guardrails'),
                3: ('service dependency and supply-chain assurance evidence', 'Critical dependencies have provenance, accountable ownership, controlled privileges and bounded assurance'),
                4: ('controlled service change path with identity and provenance evidence', 'Changes use governed identities, traceable inputs and an authorised observable change path'),
                7: ('service promotion or supplier-change model and recovery evidence', 'Change identity and sequence are traceable; recovery and escalation limits are explicit and validated'),
            }
            for step in workflow['steps']:
                if step['step'] in neutral:
                    step['hands_over'], step['gate'] = neutral[step['step']]
        definitions = HANDOFF_REQUIREMENTS[key]
        if len(definitions) != len(workflow['steps']):
            raise ValueError('WORKFLOW_PROFESSIONAL_STEP_COVERAGE: ' + key)
        if len(SELECTIONS[key]) != len(workflow['steps']):
            raise ValueError('WORKFLOW_PROFESSIONAL_SELECTION_COVERAGE: ' + key)
        inputs, variants, rework, stop, exit_rule = WORKFLOW_PROFILES[key]
        profile = {
            'id': 'workflow-profile/' + key, 'version': '1.0.0',
            'basis': 'JAI-authored professional intake and route practice; independent professional qualification remains separate.',
            'entry_inputs': inputs,
            'variants': [{'id': name, 'mechanisms': mechanisms, 'evidence': evidence}
                         for name, mechanisms, evidence in variants],
            'routes': [
                {'id': 'continue', 'trigger': 'The current handoff criteria and applicable prerequisites are satisfied.',
                 'action': 'Continue to the registered receiving duty with exact output and evidence references.'},
                {'id': 'rework', 'trigger': 'A current criterion fails or required information changes.', 'action': rework},
                {'id': 'stop', 'trigger': 'An applicable authority, legal, safety or mandatory-control boundary forbids the effect.', 'action': stop},
                {'id': 'exit', 'trigger': 'The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope.', 'action': exit_rule}],
            'context_policy': 'Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.',
            'scope_assessment': VARIANT_SCOPE_ASSESSMENTS[key],
            'paths': [],
        }
        for variant in profile['variants']:
            name = variant['id']
            mechanisms = (ONBOARDING_MECHANISMS if key == 'new-service-onboarding' and name in ONBOARDING_OVERLAYS
                          else WORKFLOW_MECHANISMS.get(key, [None]))
            if key == 'vulnerability-to-remediation' and name == 'risk-acceptance':
                mechanisms = [None]
            for mechanism in mechanisms:
                path_steps = WORKFLOW_PATH_STEPS.get((key, name), list(range(1, len(workflow['steps']) + 1)))
                profile['paths'].append({'id': name + '/' + mechanism if mechanism else name,
                    'variant': name, 'mechanism': mechanism or name,
                    'steps': path_steps, 'terminal_step': path_steps[-1]})
        workflow['operating_profile'] = profile
        for variant in profile['variants']:
            condition = WORKFLOW_VARIANT_CONDITIONS.get((key, variant['id']))
            if condition:
                variant['when'] = copy.deepcopy(condition)
        if key != 'new-service-onboarding':
            workflow['applicability'] = {
                'selection_rule': 'Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.',
                'invariant_outcomes': [workflow['outcome'], 'Retain source-version traceability, accountable receiving duties and every applicable existing gate.'],
                'variants': [{'context': name, 'mechanisms': mechanisms, 'evidence': evidence}
                             for name, mechanisms, evidence in variants],
                'disposition_rule': rework + ' ' + stop + ' ' + exit_rule + ' Mechanism selection is not a waiver of security, legal or acceptance obligations.',
            }
        for step, (record, fields) in zip(workflow['steps'], definitions):
            fields = fields.split()
            if len(fields) != len(set(fields)) or len(fields) < 4:
                raise ValueError('WORKFLOW_PROFESSIONAL_FIELDS: ' + key)
            ident = f"{key}:{step['step']}"
            contract = copy.deepcopy(HANDOFF_CONTENT_CONTRACTS.get(ident, {
                'id': 'handoff/' + ident, 'version': '1.0.0',
                'basis': 'JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.',
                'units': [{
                    'id': 'handoff/' + ident + '.' + record,
                    'semantic_field': 'handoff_' + record,
                    'required_fields': fields,
                    'acceptance_criterion': 'For ' + step['hands_over'] + ', supply the actual versioned ' + record.replace('_', ' ') + ' record, including ' + ', '.join(fields) + '. Independently assess the evidence against this exact criterion: ' + step['gate'] + '. Do not substitute a related policy, plan or claimed execution for the required work product and observations.'}]}))
            contract['subject'] = step['hands_over']
            contract['workflow_profile_hash'] = canonical_hash(profile)
            contract['units'].append({
                'id': 'handoff/' + ident + '.workflow_context',
                'semantic_field': 'workflow_context',
                'required_fields': ['context_ref', 'route', 'input_refs', 'route_evidence'],
                'acceptance_criterion': 'Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.'})
            step['handoff_content_contract'] = contract
        for step in workflow['steps']:
            step['variant_bindings'] = {}
            for path in profile['paths']:
                if step['step'] not in path['steps']:
                    continue
                mechanism = path['mechanism']
                selector = (mechanism if key in WORKFLOW_MECHANISMS or key == 'new-service-onboarding'
                            else path['variant'])
                override = VARIANT_HANDOFF_REQUIREMENTS.get((key, step['step'], selector))
                chosen = copy.deepcopy(step['handoff_content_contract'])
                criterion = step['gate']
                contract_role = {'architecture-repository-engineer': 'architecture-repository-and-modelling-lead',
                                 'model-consistency-reviewer': 'architecture-repository-and-modelling-lead'}.get(step['slug'], step['slug'])
                choice = SELECTIONS[key][step['step'] - 1]
                ids = [] if choice == 'source' else [f'{contract_role}:{number}' for number in choice.split(',')]
                producer = ('agent:' if step['skill'] == 'agent' else 'engagement:' if step['skill'] in ('dynamic', 'external') else '') + step['slug']
                if override:
                    record, fields, criterion, ids, producer = override
                    chosen['units'] = [{
                        'id': chosen['id'] + '.' + record,
                        'semantic_field': 'handoff_' + record,
                        'required_fields': fields.split(),
                        'acceptance_criterion': criterion}, copy.deepcopy(chosen['units'][-1])]
                if key == 'new-service-onboarding' and mechanism == 'cloud-native':
                    criterion = {2: 'Applies idempotently from clean; plan reviewed before apply',
                                 3: 'Non-root, no build secrets, pinned digests',
                                 4: 'No static cloud credentials in the CI system',
                                 7: 'The same immutable artefact is promoted, never rebuilt'}.get(step['step'], criterion)
                    chosen['units'][0]['acceptance_criterion'] += ' Cloud-native mechanism criterion: ' + criterion + '.'
                overlay = ONBOARDING_OVERLAY_REQUIREMENTS.get((path['variant'], step['step'])) if key == 'new-service-onboarding' else None
                if overlay:
                    record, fields, acceptance = overlay
                    chosen['units'].insert(-1, {'id': chosen['id'] + '.' + record,
                        'semantic_field': 'handoff_' + record, 'required_fields': fields.split(),
                        'acceptance_criterion': acceptance})
                next_steps = [number for number in path['steps'] if number > step['step']]
                if next_steps:
                    next_step = workflow['steps'][next_steps[0] - 1]
                    next_override = VARIANT_HANDOFF_REQUIREMENTS.get((key, next_step['step'], selector))
                    receiver = next_override[4] if next_override else ('agent:' if next_step['skill'] == 'agent' else 'engagement:' if next_step['skill'] in ('dynamic', 'external') else '') + next_step['slug']
                else:
                    receiver = 'engagement:named-authority'
                step['variant_bindings'][path['id']] = {
                    'contract_ids': ids, 'producer_role': producer, 'receiving_role': receiver,
                    'acceptance_criterion': criterion, 'handoff_content_contract': chosen,
                    'next_step': next_steps[0] if next_steps else None}
    return document


def build(root=ROOT):
    """Return proposed bindings with source hashes and exact registered contract IDs.

    Args:
        root: Repository containing canonical workflow references and contracts.
    Returns:
        JSON-compatible 24-workflow catalogue covering every explicit selected
        stage exactly once; the handoff total follows the canonical chains.
    Raises:
        ValueError: If source rows, roles or editorial selections no longer match.
    """
    root = Path(root)
    contracts = {c['id']:c for c in json.loads((root/'.ai/runtime/artifacts/contracts/role-deliverables.v3.json').read_text())['contracts']}
    rows = []
    workflows=professional_workflows(root)['workflows']
    source_keys = [source['key'] for source in workflows]
    if len(source_keys) != 24 or len(set(source_keys)) != 24 or set(source_keys) != set(SELECTIONS):
        raise ValueError('WORKFLOW_KEY_COVERAGE: canonical chains and explicit selections must cover the same 24 workflows')
    for source in sorted(workflows,key=lambda item:item['key']):
        workflow=source['key']
        selections=SELECTIONS[workflow]
        path=root/'.ai/runtime/workflows.json'
        chain=[]
        for step in source['steps']:
            role=step['slug']
            if step['skill']=='agent':
                role='agent:'+role
            elif step['skill'] in ('dynamic','external'):
                role='engagement:'+role
            cells=[str(step['step']),step['role'],step['does'],step['hands_over'],step['gate']]
            chain.append((cells,role))
        if len(chain)!=len(selections):
            raise ValueError(f'WORKFLOW_SOURCE_CHANGED: {workflow}')
        for index,((cells,role),choice) in enumerate(zip(chain,selections)):
            contract_role = {'agent:architecture-repository-engineer':'architecture-repository-and-modelling-lead',
                             'agent:model-consistency-reviewer':'architecture-repository-and-modelling-lead'}.get(role,role)
            ids=[] if choice=='source' else [f'{contract_role}:{n}' for n in choice.split(',')]
            if any(c not in contracts for c in ids):
                raise ValueError(f'UNKNOWN_CONTRACT: {workflow}:{index+1}')
            rows.append({'handoff_id':f'{workflow}:{index+1}','workflow_id':workflow,'step':index+1,
                'producer_role':role,'receiving_role':chain[index+1][1] if index+1<len(chain) else 'engagement:named-authority',
                'handover':cells[3],'acceptance_criterion':cells[4], 'contract_ids':ids,
                'contract_selection':'explicit-source-contract' if choice=='source' else 'registered-contracts',
                'artifact_types':sorted({contracts[c]['jai']['semantics']['artifact_type'] for c in ids}),
                'source_ref':str(path.relative_to(root)), 'source_hash':canonical_hash(source),
                'obligation_basis':'Existing workflow handover/gate and explicit professional contract mapping; proposed, pending domain approval.',
                'receiver_checks':['exact-contract-binding','content-qa-replay','existing-gates-preserved','independent-receiver-attestation','specific-gate-evidence']})
            rows[-1]['handoff_content_contract'] = copy.deepcopy(source['steps'][index]['handoff_content_contract'])
            rows[-1]['variant_bindings'] = copy.deepcopy(source['steps'][index]['variant_bindings'])
    for row in rows:
        if row['contract_selection'] == 'explicit-source-contract':
            row['source_content_contract'] = {
                'id': row['handoff_id'], 'version': '1.0.0',
                'basis': 'JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.',
                **SOURCE_HANDOFF_CONTENT[row['handoff_id']]}
    expected_handoffs = sum(len(SELECTIONS[key]) for key in source_keys)
    if len(rows) != expected_handoffs or len({row['handoff_id'] for row in rows}) != expected_handoffs:
        raise ValueError(f'WORKFLOW_COUNT_CHANGED: {len(rows)}')
    result={'schema_version':'1.0.0','status':'proposed','workflow_count':len(SELECTIONS),'handoff_count':len(rows),
            'profiles': {source['key']: source['operating_profile'] for source in workflows}, 'bindings':rows}
    result['catalog_hash']=canonical_hash(result)
    return result


def professional_projection(root=ROOT):
    """Return the source-owned enriched workflow registry as deterministic JSON.

    Args:
        root: Checkout containing the registry and exact maintained definitions.
    Returns:
        Mapping with the single canonical workflow-registry path and JSON text.
    Raises:
        ValueError, OSError: Source definitions are incomplete or unreadable.
    """
    return {'.ai/runtime/workflows.json': json.dumps(professional_workflows(root), indent=2, ensure_ascii=False) + '\n'}


def summary_projections(root=ROOT):
    """Return routing summaries with counts derived from canonical catalogues.

    Args:
        root: Repository containing workflow/role registries and existing skills.
    Returns:
        Relative skill paths mapped to complete updated text. Manual prose,
        role rows and workflow triggers are retained; only owned counts change.
    Raises:
        ValueError: If a required projection or expected count location is absent.
        OSError: If a canonical registry cannot be read.

    This projection runs at catalogue generation/check boundaries, never on a
    productive handoff. Canonical records, rather than a second count registry,
    determine the summaries.
    """
    root = Path(root)
    workflows = json.loads((root / '.ai/runtime/workflows.json').read_text())['workflows']
    roles = json.loads((root / '.ai/runtime/roles.json').read_text())['roles']
    result = {}

    def read(relative):
        path = root / relative
        if not path.is_file():
            raise ValueError(f'SUMMARY_PROJECTION_MISSING: {relative}')
        return path.read_text()

    def replace(pattern, replacement, text, location):
        updated, count = re.subn(pattern, replacement, text, flags=re.M)
        if count != 1:
            raise ValueError(f'SUMMARY_COUNT_LOCATION: {location}')
        return updated

    relative = '.ai/skills/it-role-workflows/SKILL.md'
    text = read(relative)
    text = replace(r'`workflows: \d+`', f'`workflows: {len(workflows)}`', text, relative)
    text = replace(r'across \d+ end-to-end workflow chains',
                   f'across {len(workflows)} end-to-end workflow chains', text, relative)
    for workflow in workflows:
        pattern = rf'^(\| \[[^\n]+\]\(references/{re.escape(workflow["key"])}\.md\) \| )\d+( \|[^\n]+)$'
        text = replace(pattern, lambda match: match[1] + str(len(workflow['steps'])) + match[2],
                       text, workflow['key'])
    result[relative] = text
    for skill in sorted({role['skill'] for role in roles}):
        selected = [role for role in roles if role['skill'] == skill]
        relative = f'.ai/skills/{skill}/SKILL.md'
        text = read(relative)
        text = replace(r'role skills: \d+ defined roles', f'role skills: {len(selected)} defined roles', text, relative)
        text = replace(r'`roles: \d+`', f'`roles: {len(selected)}`', text, relative)
        advises = sum(role['tool_tier'] == 'advise' for role in selected)
        if advises:
            text = replace(r'\d+ of the \d+ roles here', f'{advises} of the {len(selected)} roles here', text, relative)
        result[relative] = text
    return result


def applicability_projections(root=ROOT):
    """Return workflow skill and public guidance with canonical context rules.

    Args:
        root: Repository root containing workflows and maintained references.
    Returns:
        Relative skill/public paths mapped to text. Public guidance precedes
        the reference diagram or step table. Only workflows with an explicit
        applicability record participate; no branch is inferred from a title.
    Raises:
        ValueError: If an owned marker is incomplete or duplicated.
        OSError: If a participating reference cannot be read.
    """
    root = Path(root)
    workflows = json.loads((root / '.ai/runtime/workflows.json').read_text())['workflows']
    if {workflow['key'] for workflow in workflows} == set(WORKFLOW_PROFILES):
        workflows = professional_workflows(root)['workflows']
    start = '<!-- BEGIN workflow-applicability -->'
    end = '<!-- END workflow-applicability -->'
    result = {}
    for workflow in workflows:
        if 'applicability' not in workflow:
            continue
        profile = workflow['applicability']
        lines = [start, '## Context and mechanism applicability', '', profile['selection_rule'], '',
                 '**Invariant outcomes:**', '']
        lines.extend('- ' + outcome for outcome in profile['invariant_outcomes'])
        lines += ['', '| Context | Mechanisms | Required evidence |', '| --- | --- | --- |']
        lines.extend('| ' + ' | '.join(variant[key] for key in ('context', 'mechanisms', 'evidence')) + ' |'
                     for variant in profile['variants'])
        lines += ['', profile['disposition_rule'], end]
        operating = workflow.get('operating_profile')
        if operating:
            lines[-1:-1] = ['', '**Entry information (selected once per actual context version):**', '',
                *['- ' + value for value in operating['entry_inputs']], '',
                operating['context_policy'], '', '**Continuation, rework, stop and exit:**', '',
                *['- **' + route['id'] + '** — ' + route['trigger'] + ' ' + route['action']
                  for route in operating['routes']]]
            guarded = [variant for variant in operating['variants'] if variant.get('when')]
            lines[-1:-1] = ['', '**Bounded paths and scope:**', '', operating['scope_assessment'], '',
                '| Selected path | Applicable stages | Terminal stage |', '| --- | --- | ---: |',
                *['| ' + path['id'] + ' | ' + ', '.join(str(step) for step in path['steps'])
                  + ' | ' + str(path['terminal_step']) + ' |' for path in operating['paths']],
                '', 'A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.']
            if guarded:
                labels = {'processes_personal_data': 'personal data are processed',
                          'regulatory_requirement': 'a regulatory requirement applies'}
                lines[-1:-1] = ['', '**Context guards:**', '',
                    *['- **' + variant['id'] + '** requires evidence that the statement "'
                      + labels[variant['when']['field']] + '" is '
                      + str(variant['when']['value']).lower()
                      + '; unknown applicability remains pending.' for variant in guarded]]
        block = '\n'.join(lines)
        for relative in (f".ai/skills/it-role-workflows/references/{workflow['key']}.md",
                         f"docs/workflow-library/{workflow['key']}.md"):
            text = (root / relative).read_text()
            if workflow.get('operating_profile'):
                by_number = {step['step']: step for step in workflow['steps']}
                def source_row(match):
                    step = by_number.get(int(match.group(1)))
                    if step is None:
                        return match.group(0)
                    cells = [str(step[field]) for field in ('step', 'role', 'does', 'hands_over', 'gate')]
                    if relative.startswith('.ai/') and step['skill'].startswith('it-roles-'):
                        cells[1] = '[' + step['role'] + '](../../' + step['skill'] + '/references/' + step['slug'] + '.md)'
                    return '| ' + ' | '.join(cells) + ' |'
                text = re.sub(r'^\|\s*(\d+)\s*\|[^\n]+$', source_row, text, flags=re.M)
                if relative.startswith('docs/'):
                    text = re.sub(r'(## Intended outcome\s*\n\s*\n)[^\n]+',
                                  lambda match: match.group(1) + workflow['outcome'], text, count=1)
            if start not in text and end not in text:
                anchors = ('<!-- JAI:WORKFLOW-DIAGRAM:START -->', '## Workflow steps and gates') if relative.startswith('docs/') else ()
                anchor = next((anchor for anchor in anchors if anchor in text), None)
                if anchor:
                    text = text.replace(anchor, block + '\n\n' + anchor, 1)
                else:
                    text = text.rstrip() + '\n\n' + block + '\n'
            elif text.count(start) == text.count(end) == 1 and text.index(start) < text.index(end):
                text = text[:text.index(start)] + block + text[text.index(end) + len(end):]
            else:
                raise ValueError(f'WORKFLOW_APPLICABILITY_MARKERS: {workflow["key"]}')
            result[relative] = text
    return result


def main(argv=None):
    """Write/check the generated catalogue; return one on drift or invalid source.

    Args:
        argv: Optional command arguments.
    Returns:
        Zero on success, one on source/catalogue mismatch.
    """
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args(argv)
    payloads = {**professional_projection(), '.ai/runtime/content/workflow-acceptance.json': json.dumps(build(),indent=2,ensure_ascii=False)+'\n',
                **summary_projections(), **applicability_projections()}
    if args.check:
        return 0 if all((ROOT/path).is_file() and (ROOT/path).read_text()==payload
                        for path,payload in payloads.items()) else 1
    for path,payload in payloads.items():
        if (ROOT/path).read_text() != payload:
            (ROOT/path).write_text(payload)
    return 0

if __name__=='__main__':
    raise SystemExit(main())
