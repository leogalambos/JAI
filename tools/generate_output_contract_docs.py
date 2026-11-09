#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Generate public output contracts and catalogue links from canonical DCS data.

Run with --root CHECKOUT to replace owned marker blocks, or --check to report
stale projections without writing. Manual prose outside the markers is retained.
Only obsolete files carrying this generator's ownership marker are removed.
No engagement, historical approval, private input or runtime permission is changed.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
from content_spec import ContentSpec

START = '<!-- JAI:OUTPUT-CONTRACTS:START -->'
END = '<!-- JAI:OUTPUT-CONTRACTS:END -->'
NAV_START = '# JAI:OUTPUT-CONTRACTS:NAV:START'
NAV_END = '# JAI:OUTPUT-CONTRACTS:NAV:END'
DIRECTORY = 'docs/reference/output-contracts'
GROUPS = {
    'required_information': 'Required information (MUST)',
    'conditional_information': 'Conditionally required information',
    'optional_information': 'Optional information (MAY)',
    'forbidden_information': 'Prohibited content (MUST NOT)',
    'low_value_information': 'Content to omit unless justified',
}
MODES = {'advise': 'Advice and assessment.',
         'author': 'Specifications, models and documents.',
         'execute': 'Implementation, execution and operational evidence.',
         'inspect': 'Read-only technical inspection and evidence analysis.'}


def replace_block(text, content, start=START, end=END):
    """Replace exactly one owned block, preserving surrounding manual prose.

    Args:
        text: Existing UTF-8 document with one ordered marker pair.
        content: Generated text without ownership markers.
        start: Exact opening marker; default identifies Markdown blocks.
        end: Exact closing marker; default identifies Markdown blocks.
    Returns:
        Updated document with original prefix and suffix unchanged.
    Raises:
        ValueError: Markers are missing, repeated or out of order.
    """
    if text.count(start) != 1 or text.count(end) != 1 or text.index(end) < text.index(start):
        raise ValueError('Expected exactly one ordered output-contract marker pair')
    return text[:text.index(start)] + start + '\n' + content.rstrip() + '\n' + text[text.index(end):]


def _cell(value):
    return str(value).replace('|', '&#124;').replace('\n', ' ')


def _slug(value):
    return re.sub(r'[^a-zA-Z0-9-]+', '-', value).strip('-').lower()


def _owned(content):
    return START + '\n' + content.rstrip() + '\n' + END + '\n'


class Projection:
    """Build one public projection with reusable compiled specification metadata.

    Args:
        root: Source checkout with canonical roles, workflows and DCS registry.
    Raises:
        OSError, ValueError: A required source or explicit binding is invalid.
    """

    def __init__(self, root):
        self.root = Path(root)
        self.catalogue = ContentSpec(self.root)
        self.roles = json.loads((self.root / '.ai/runtime/roles.json').read_text())['roles']
        self.workflows = json.loads((self.root / '.ai/runtime/workflows.json').read_text())['workflows']
        self.contracts = {item['id']: item for item in json.loads((self.root / '.ai/runtime/artifacts/contracts/role-deliverables.v3.json').read_text())['contracts']}
        self.handoffs = {(item['workflow_id'], item['step']): item for item in json.loads((self.root / '.ai/runtime/content/workflow-acceptance.json').read_text())['bindings']}
        self.compiled = {}
        self.spec_paths = {}
        for ref, spec in self.catalogue.specs.items():
            cid = spec.get('applies_to', {}).get('contract_id')
            if not cid and ref.startswith('kind/role/'):
                cid = ref[len('kind/role/'):]
            self.spec_paths[ref] = ('role-' + self.contracts[cid]['role_slug'] + '.md#' + self.anchor(cid)
                                    if cid else 'spec-' + _slug(ref) + '.md')
        if len(self.contracts) != len(self.catalogue.bindings) or set(self.contracts) != set(self.catalogue.bindings):
            raise ValueError('Every role output needs exactly one explicit content binding')
        for cid, binding in self.catalogue.bindings.items():
            selected = self.catalogue.kinds[binding['document_kind']]['spec_ref']
            if binding['content_spec_ref'] != selected:
                raise ValueError('Ambiguous selected content specification: ' + cid)

    @staticmethod
    def anchor(cid):
        """Return the deterministic HTML anchor for one canonical output.

        Args:
            cid: Stable canonical role-output contract ID.
        Returns:
            HTML-compatible anchor prefixed to distinguish output sections.
        """
        return 'output-' + _slug(cid)

    def compiled_for(self, ref, overlays=()):
        """Compile each immutable selection once within this projection.

        Args:
            ref: Exact registered specification reference.
            overlays: Explicit bound overlay references, in declared order.
        Returns:
            Existing compiler result including effective inheritance and budgets.
        Raises:
            ValueError: References, conditions or inherited requirements conflict.
        """
        key = (ref, tuple(overlays))
        if key not in self.compiled:
            self.compiled[key] = self.catalogue.compile(ref, overlays=list(overlays))
        return self.compiled[key]

    def spec_body(self, ref, overlays=()):
        """Render local obligations and links to all effective inherited rules.

        Args:
            ref: Registered specification ID.
            overlays: Explicit selection overlays.
        Returns:
            Markdown covering purpose, obligations, conditions, evidence and basis.
        Raises:
            ValueError: Compilation fails or an inherited reference is missing.
        """
        spec = self.catalogue.specs[ref]
        compiled = self.compiled_for(ref, overlays)
        rows = [f"**Specification:** `{ref}`; **content version:** `{spec['version']}`.", '', spec['purpose'], '',
                '**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.', '']
        inherited = [entry['id'] for entry in compiled['inheritance'] if entry['id'] != ref]
        if inherited:
            rows += ['**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:', '']
            rows += [f"- [`{ident}`]({self.spec_paths[ident]})" for ident in inherited]
            rows.append('')
        rows += ['Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.', '']
        form = compiled.get('delivery_form')
        if form:
            rows += ['### Primary work product and evidence', '',
                     '**Primary work product:** `' + form['primary_artifact'] + '`.', '',
                     form['representation'], '', '**Evidence accompanying the work product:**', '']
            rows += ['- ' + item for item in form['evidence']]
            rows += ['', 'The historical artifact-type field is retained for compatibility; '
                     'it does not require replacing this work product with a report or an EA diagram. '
                     + form['authority'], '']
        all_units = [unit for group in GROUPS for unit in spec.get(group, [])]
        policies = {json.dumps(unit.get('evidence_policy', {}), sort_keys=True) for unit in all_units}
        shared_policy = json.loads(next(iter(policies))) if len(policies) == 1 else {}
        if shared_policy:
            rows += ['**Evidence policy for the following units:** ' + '; '.join(str(shared_policy[key]) for key in ('material_claims', 'unknown') if key in shared_policy) + '.', '']
        for group, title in GROUPS.items():
            units = spec.get(group, [])
            if not units:
                continue
            rows += ['### ' + title, '']
            for unit in units:
                rows += [f"**`{unit['id']}`** — `{unit.get('datatype', 'information')}`", '']
                if unit.get('when'):
                    rows += ['Applies when: `' + json.dumps(unit['when'], sort_keys=True) + '`. If the needed context is unknown, resolve it before claiming completeness.', '']
                criteria = unit.get('acceptance_criteria', [unit['rationale']['reason']])
                rows += [f'- {criterion}' for criterion in criteria if criterion != 'A title alone is insufficient; values must identify concrete entities, relations and limitations.']
                policy = unit.get('evidence_policy', {})
                if policy and policy != shared_policy:
                    rows += ['- **Evidence and uncertainty:** ' + '; '.join(str(policy[key]) for key in ('material_claims', 'unknown') if key in policy) + '.']
                if unit.get('rationale', {}).get('reason') and unit['rationale']['reason'] not in criteria:
                    rows += ['- **Why:** ' + unit['rationale']['reason']]
                refs = [item for item in unit.get('rationale', {}).get('source_refs', []) if item.startswith('https://')]
                if refs:
                    rows += ['- **Professional basis:** ' + '; '.join(f'[source]({url})' for url in refs) + ' (informed-by; not a verbatim standard requirement).']
                rows.append('')
        budgets = compiled['blueprint'].get('budgets', {})
        if budgets:
            rows += ['### Proportionate scope', '', 'Inherited size guidance is reproduced below. It is not evidence of substantive completeness; verbosity is not a quality measure.', '', '```json', json.dumps(budgets, indent=2, ensure_ascii=False), '```', '']
        sources = spec.get('sources', {})
        professional = sources.get('professional_references', [])
        if professional:
            rows += ['### Professional sources and their limits', '']
            for source in professional:
                title = f"[{source['title']}]({source['url']})" if source.get('url') else source['title']
                rows += [f"- **{title}** — {source['scope']} Basis: `{source['basis']}`. {source['limits']}"]
            rows.append('')
        frameworks = sources.get('role_framework_context', [])
        if frameworks:
            rows += ['### Role framework context', '']
            for context in frameworks:
                frameworks_text = '; '.join(value.rstrip().rstrip('.;') for value in context['frameworks'])
                rows += ['- **' + context['role'] + ':** ' + frameworks_text + '. ' + context['basis']]
                if context.get('method_focus'):
                    rows += ['  **Practical method:** ' + context['method_focus']]
                if context.get('framework_selection'):
                    rows += ['  **Selection:** ' + context['framework_selection']]
                if context.get('applicability_rule'):
                    rows += ['  **Applicability assessment:** `' + context['applicability_rule'] + '`.']
            rows.append('')
        return '\n'.join(rows)

    def reader_summary(self, ref, overlays=()):
        """Render a short orientation without replacing effective obligations.

        Args:
            ref: Explicit selected content specification.
            overlays: Its declared overlay references.
        Returns:
            Markdown summary with representative duties and unresolved conditions,
            separating declared triggers from the sentence about uncertainty.
        Raises:
            ValueError: Compilation detects an invalid selection or conflict.
        """
        compiled = self.compiled_for(ref, overlays)
        units = compiled['blueprint']['semantic_units']
        required = [unit for unit in units if unit['category'] == 'required_information']
        generic = {'identity', 'delivery_scope', 'receiving_acceptance',
                   'contract_relations', 'decision_purpose_correction'}
        specific = [unit for unit in required
                    if not generic.intersection(unit.get('semantic_fields', []))
                    and not unit['source_spec'].startswith(('global/', 'domain/'))]
        specific.sort(key=lambda unit: (unit['source_spec'] == ref, unit['id']))
        examples = [unit.get('acceptance_criteria', [unit['rationale']['reason']])[0]
                    for unit in (specific or required)[:3]]
        conditions = {json.dumps(unit['when'], sort_keys=True)
                      for unit in units if unit.get('when')}
        labels = {'processes_personal_data': 'personal data are processed',
                  'regulatory_requirement': 'an applicable regulatory requirement exists'}
        condition_labels = []
        for encoded in sorted(conditions):
            condition = json.loads(encoded)
            if condition.get('op') == 'eq' and condition.get('value') is True and condition.get('field') in labels:
                condition_labels.append(labels[condition['field']])
            else:
                condition_labels.append(encoded)
        conditional = ('; '.join(condition_labels) + '.' if condition_labels
                       else 'No additional conditional trigger is declared.')
        optional = [unit for unit in units if unit['category'] == 'optional_information']
        optional_text = (optional[0].get('acceptance_criteria', [optional[0]['rationale']['reason']])[0]
                         if optional else 'No optional extension is declared.')
        return '\n'.join([
            '**At a glance**', '',
            '- **Purpose:** ' + self.catalogue.specs[ref]['purpose'],
            '- **Mandatory examples:** ' + ' '.join(examples),
            '- **Conditions to resolve:** ' + conditional + ' Unknown applicability remains unresolved.',
            '- **Optional example:** ' + optional_text,
            '- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.',
            '',
            'This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.', ''])

    def render(self):
        """Return deterministic target paths and generated Markdown blocks.

        Returns:
            Mapping of checkout-relative paths to marker-owned page/block content.
        Raises:
            ValueError: A link/binding is missing or private provenance would leak.
        """
        result = {}
        grouped = defaultdict(list)
        for cid, contract in self.contracts.items():
            grouped[contract['role_slug']].append((cid, contract))
        role_rows = []
        index = ['# Output contract catalogue', '',
                 'Each contract states what a work product must contain, when additional information is required, what is optional, what must be excluded, and how its content is assessed. Work products include executable code, tests, models, records and performed operations as well as documents.', '',
                 'Read the selected output together with every linked foundation and overlay. These are proposed JAI professional content contracts: structural completeness is distinct from an independent assessment, human acceptance and permission to release. Framework references explain the professional basis; they never replace the explicit criteria.', '',
                 '## Use and maintenance', '',
                 'Select an output from the [role catalogue](../roles.md) or a handoff from the [workflow catalogue](../workflows.md). The author uses its actual required inputs; the reviewer assesses the relevant content and evidence. Missing information remains a declared gap. A new input version requires assessment of the affected output; it does not rewrite historical results.', '',
                 'This catalogue is generated from canonical content definitions and explicit role/workflow bindings. To refresh its owned sections, run `python3 tools/generate_output_contract_docs.py --root .`; use `--check` to detect drift without writing. Prose outside the named generated markers is preserved. No workflow execution or approval is performed by generation.', '',
                 '## Role output contracts', '', '| Role | Specified outputs |', '| --- | ---: |']
        for category in sorted({role['category'] for role in self.roles}):
            role_rows += ['## ' + category, '', '| Role | Professional focus | Concrete primary outputs | Work mode |', '| --- | --- | --- | --- |']
            for role in self.roles:
                if role['category'] != category:
                    continue
                contracts = sorted(grouped[role['slug']], key=lambda pair: pair[1]['deliverable_number'])
                if len(contracts) != len(role['primary_deliverables']):
                    raise ValueError('Role output count differs from bound contracts: ' + role['slug'])
                page = ['# ' + role['name'] + ': output contracts', '', role['mission'], '', '[Full catalogue](index.md)', '']
                links = []
                for label, (cid, contract) in zip(role['primary_deliverables'], contracts):
                    anchor = self.anchor(cid)
                    links.append(f'[{_cell(label)}](output-contracts/role-{role["slug"]}.md#{anchor})')
                    binding = self.catalogue.bindings[cid]
                    ref = binding['content_spec_ref']
                    page += [f'<a id="{anchor}"></a>', '', '## ' + label, '', self.reader_summary(ref, binding.get('overlays', [])), f'**Contract ID:** `{cid}`.', '', '**Required inputs:**', '']
                    page += ['- ' + item for item in contract['jai']['semantics']['required_inputs']]
                    page += ['', self.spec_body(ref, binding.get('overlays', [])), '']
                result[f'{DIRECTORY}/role-{role["slug"]}.md'] = '\n'.join(page)
                index.append(f'| [{_cell(role["name"])}](role-{role["slug"]}.md) | {len(contracts)} |')
                role_rows.append('| ' + ' | '.join([_cell(role['name']), _cell(role['mission']), '; '.join(links), MODES[role['tool_tier']]]) + ' |')
            role_rows.append('')
        index += ['', '## Shared foundations and specialisations', '', 'The links below specify shared requirements. Role pages select the effective foundations and overlays explicitly; a similarly named output is not sufficient to establish applicability.', '']
        for ref, path in sorted(self.spec_paths.items()):
            if path.startswith('role-'):
                continue
            result[f'{DIRECTORY}/{path}'] = '# ' + ref + '\n\n' + self.spec_body(ref)
            index.append(f'- [`{ref}`]({path})')
        result[f'{DIRECTORY}/index.md'] = '\n'.join(index)
        result['docs/reference/roles.md'] = '\n'.join(role_rows)
        workflow_rows = ['| Workflow | Start when | Expected result |', '| --- | --- | --- |']
        for workflow in self.workflows:
            workflow_rows.append(f"| [{_cell(workflow['title'])}](../workflow-library/{workflow['key']}.md) | {_cell(workflow['trigger'])} | {_cell(workflow['outcome'])} |")
        workflow_specific = {}
        for workflow in self.workflows:
            workflow_rows += ['', '## ' + workflow['title'], '', f"**Workflow key:** `{workflow['key']}`.", '', '**Start when:** ' + workflow['trigger'], '', '**Expected result:** ' + workflow['outcome'], '', '**Concrete stage outputs and receiving conditions:**', '']
            for step in workflow['steps']:
                handoff = self.handoffs[(workflow['key'], step['step'])]
                links = []
                for cid in handoff['contract_ids']:
                    contract = self.contracts[cid]
                    links.append(f'[`{cid}`](output-contracts/role-{contract["role_slug"]}.md#{self.anchor(cid)})')
                supplement = handoff.get('handoff_content_contract')
                if supplement:
                    filename = 'workflow-' + workflow['key'] + '.md'
                    anchor = self.anchor(supplement['id'])
                    page = workflow_specific.setdefault(filename, [
                        '# ' + workflow['title'] + ': source-owned handoff contracts', '',
                        '[Catalogue](index.md)', ''])
                    page += [f'<a id="{anchor}"></a>', '', '## ' + step['hands_over'], '',
                             '**Handoff content contract:** `' + supplement['id'] + '`.', '',
                             '**Basis:** ' + supplement['basis'], '',
                             'These requirements supplement the linked role output contracts. '
                             'A related policy or published view does not replace the specific '
                             'decision or repository/interchange records required here.', '',
                             '### Required information (MUST)', '']
                    for unit in supplement['units']:
                        page += ['- **`' + unit['semantic_field'] + '`**: '
                                 + unit['acceptance_criterion'],
                                 '  Required fields: ' + ', '.join(
                                     '`' + field + '`' for field in unit['required_fields']) + '.']
                    page += ['', 'The existing authenticated receiver reviews each required '
                             'unit against this exact handoff. A content record alone does '
                             'not grant acceptance or release.', '']
                    if handoff.get('variant_bindings'):
                        page += ['### Context-selected alternatives', '',
                                 'Alternative bindings replace the base obligations for the '
                                 'selected path. Select the path from the reviewed intake '
                                 'context and the workflow operating profile; requirements '
                                 'from other paths are not cumulative.', '']
                        for path_id, binding in handoff['variant_bindings'].items():
                            next_step = binding['next_step']
                            destination = ('Terminal disposition; no downstream step'
                                           if next_step is None else 'Step ' + str(next_step))
                            page += ['**Selected path:** `' + path_id + '`.', '',
                                     '**Producer:** `' + binding['producer_role'] + '`; '
                                     '**receiver:** `' + binding['receiving_role'] + '`.', '',
                                     '**Receiving condition:** ' + binding['acceptance_criterion'], '',
                                     '**Next:** ' + destination + '.', '',
                                     '**Role output contracts:** ' + (', '.join(
                                         '`' + cid + '`' for cid in binding['contract_ids'])
                                         or 'Source-owned handoff only') + '.', '']
                            for unit in binding['handoff_content_contract']['units']:
                                page += ['- **`' + unit['semantic_field'] + '`**: '
                                         + unit['acceptance_criterion'],
                                         '  Required fields: ' + ', '.join(
                                             '`' + field + '`' for field in unit['required_fields']) + '.']
                            page.append('')
                    links.append(f'[{supplement["id"]}](output-contracts/{filename}#{anchor})')
                if handoff.get('source_content_contract'):
                    source = handoff['source_content_contract']
                    filename = 'workflow-' + workflow['key'] + '.md'
                    anchor = self.anchor(source['id'])
                    page = workflow_specific.setdefault(filename, ['# ' + workflow['title'] + ': source-owned handoff contracts', '', '[Catalogue](index.md)', ''])
                    page += [f'<a id="{anchor}"></a>', '', '## ' + step['hands_over'], '', '**Producer:** ' + step['role'] + '.', '', '**Basis:** ' + source['basis'], '', '### Required information (MUST)', '']
                    page += ['- ' + requirement for requirement in source['required']]
                    page += ['', '### Conditionally required information', '']
                    page += ['- **When:** ' + item['when'] + ' **Required:** ' + item['requirement'] for item in source['conditional']]
                    page += ['', '### Optional information (MAY)', '']
                    page += ['- ' + item for item in source['optional']]
                    page += ['', '**Receiving condition:** ' + step['gate'], '', 'Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.', '']
                    links.append(f'[{source["id"]}](output-contracts/{filename}#{anchor})')
                workflow_rows += [f"{step['step']}. **{step['role']}:** {step['hands_over']}.", f"   **Receiving condition:** {step['gate']}", '   **Output specifications:** ' + '; '.join(links)]
            workflow_rows += ['', f"[Roles, activities and acceptance gates for this chain](../workflow-library/{workflow['key']}.md#workflow-steps-and-gates)."]
        result['docs/reference/workflows.md'] = '\n'.join(workflow_rows)
        index += ['', '## Source-owned workflow handoffs', '']
        for filename, content in sorted(workflow_specific.items()):
            result[f'{DIRECTORY}/{filename}'] = '\n'.join(content)
            index.append(f'- [{content[0][2:]}]({filename})')
        result[f'{DIRECTORY}/index.md'] = '\n'.join(index)
        nav = ['          - Overview: reference/output-contracts/index.md']
        for category in sorted({role['category'] for role in self.roles}):
            nav.append('          - ' + json.dumps(category) + ':')
            nav.extend('              - ' + json.dumps(role['name']) + ': reference/output-contracts/role-' + role['slug'] + '.md' for role in self.roles if role['category'] == category)
        nav.append('          - Shared foundations and specialisations:')
        nav.extend('              - ' + json.dumps(ref) + ': reference/output-contracts/' + path for ref, path in sorted(self.spec_paths.items()) if not path.startswith('role-'))
        nav.append('          - Source-owned workflow handoffs:')
        nav.extend('              - ' + json.dumps(content[0][2:]) + ': reference/output-contracts/' + filename for filename, content in sorted(workflow_specific.items()))
        result['mkdocs.yml'] = '\n'.join(nav)
        for path, content in result.items():
            if re.search(r'(?i)\bINBOX[/\\]|/home/|/tmp/', content):
                raise ValueError('Private provenance cannot be projected: ' + path)
        return result


def generate(root, check=False):
    """Refresh owned documentation or return drift without changing any files.

    Args:
        root: Checkout containing canonical registries and marker-bearing catalogues.
        check: If true, report differences only.
    Returns:
        Zero if generated successfully/current, one when check detects drift.
    Raises:
        OSError, ValueError: Invalid source, ownership markers or output paths.
    """
    root = Path(root)
    if (root / DIRECTORY).is_symlink():
        raise ValueError('Generated documentation directory must not be a symbolic link')
    rendered = Projection(root).render()
    updates = {}
    for relative, content in rendered.items():
        path = root / relative
        if path.is_symlink():
            raise ValueError('Refusing to write through a symbolic link: ' + relative)
        if relative.startswith(DIRECTORY + '/'):
            if path.exists() and START not in path.read_text():
                raise ValueError('Refusing to replace unowned page: ' + relative)
            updates[path] = replace_block(path.read_text(), content) if path.exists() else _owned(content)
        elif relative == 'mkdocs.yml':
            updates[path] = replace_block(path.read_text(), content, NAV_START, NAV_END)
        else:
            updates[path] = replace_block(path.read_text(), content)
    obsolete = {}
    for path in (root / DIRECTORY).glob('*.md'):
        if path in updates:
            continue
        if path.is_symlink():
            raise ValueError('Refusing an obsolete symbolic-link candidate: ' + str(path))
        text = path.read_text()
        if START not in text:
            continue
        replace_block(text, '')  # Validate ownership before calculating removal.
        remainder = text[:text.index(START)] + text[text.index(END) + len(END):]
        obsolete[path] = remainder if remainder.strip() else None
    differences = [str(path.relative_to(root)) for path, content in updates.items() if not path.exists() or path.read_text() != content]
    differences.extend(str(path.relative_to(root)) for path in obsolete)
    if check:
        if differences:
            print('Generated output contract documentation differs: ' + ', '.join(differences))
        else:
            print(f'PASS: {len(rendered)} output contract projections match canonical sources')
        return int(bool(differences))
    for path, content in updates.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    for path, remainder in obsolete.items():
        if remainder is None:
            path.unlink()
        else:
            path.write_text(remainder, encoding='utf-8')
    print(f'Generated {len(rendered)} output contract projections; removed {len(obsolete)} obsolete owned pages')
    return 0


def main(argv=None):
    """Parse --root/--check and return the generation status without publishing.

    Args:
        argv: Optional command-line argument list; None uses process arguments.
    Returns:
        Generation/check exit status.
    Raises:
        OSError, ValueError: Required source or ownership metadata is invalid.
        SystemExit: Command-line arguments are invalid.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    return generate(args.root, args.check)


if __name__ == '__main__':
    raise SystemExit(main())
