# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Exercise real offline references and adversarial scoped filesystem inputs."""
import copy
import hashlib
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from expert_references import ExpertReferences, ReferenceError, main


@pytest.fixture(scope='session')
def reference_library():
    """Load the immutable source registry once for deterministic offline tests."""
    return ExpertReferences(ROOT)


@pytest.fixture
def library(reference_library):
    """Isolate mutated manifest/root state while reusing immutable DCS data."""
    library = copy.copy(reference_library)
    library.manifest = copy.deepcopy(reference_library.manifest)
    library.entries = library.manifest['entries']
    library.specs = copy.copy(reference_library.specs)
    return library


@pytest.fixture
def original(library):
    """Return the unchanged public-synthetic simple ADR bytes."""
    return (library.base / 'adr/simple.md').read_bytes()


def _put(root, raw, name='simple.md'):
    path = root / 'adr' / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return path


def test_supplied_collection_has_135_unique_verified_slots(library):
    """Manifest bytes, all 45 family IDs and every mandatory anchor agree."""
    result = library.validate_all()
    assert result['status'] == 'PASS'
    assert result['reference_count'] == 135
    assert len({(entry['document_kind'], entry['complexity']) for entry in result['results']}) == 135
    assert all(entry['professional_acceptance'] == 'NOT_APPROVED' for entry in result['results'])
    assert all(entry['content_adequacy'] == 'NOT_EVALUATED' for entry in result['results'])
    assert all(entry['evidence_and_rationale_quality'] == 'NOT_EVALUATED' for entry in result['results'])


def test_headings_are_flexible(library, original, tmp_path):
    """Anchor identity, rather than a fixed heading string, governs coverage."""
    path = _put(tmp_path, original.replace(b'## Context, concern, constraints and status', b'## A freely edited title'))
    assert library.validate(path)['structural_coverage'] == 'PASS'


@pytest.mark.parametrize('before,after,code', [
    (b'language: en', b'language: cs', 'METADATA_SCHEMA_INVALID'),
    (b'fictional_context: true', b'fictional_context: false', 'METADATA_SCHEMA_INVALID'),
    (b'approval_status: not-human-approved', b'approval_status: approved', 'METADATA_SCHEMA_INVALID'),
    (b'applicable_dcs: kind/adr', b'applicable_dcs: kind/hld', 'DCS_IDENTITY_MISMATCH'),
    (b'language: en', b'language: en\nlanguage: en', 'DUPLICATE'),
    (b'language: en', b'language: [en]', 'METADATA_SCHEMA_INVALID'),
    (b'provenance: ai-authored-proposed', b'provenance: human-gold', 'METADATA_SCHEMA_INVALID'),
    (b'language: en', b'language: en\npolicy: relax', 'METADATA_SCHEMA_INVALID'),
    (b'<a id="dcs-adr.decision_context"></a>', b'', 'anchor.missing'),
    (b'<a id="dcs-adr.decision_context"></a>', b'<a id="dcs-adr.forged"></a>', 'anchor.unknown'),
    (b'<a id="dcs-adr.decision_context"></a>', b'<a id="dcs-adr.decision_context"></a>\n<a id="dcs-adr.decision_context"></a>', 'anchor.duplicate'),
    (b'<a id="dcs-adr.decision_context"></a>', b'<div id="dcs-adr.decision_context"></div>', 'anchor.inconsistent'),
    (b'## Context, concern, constraints and status', b'Context without heading', 'anchor.heading_missing'),
])
def test_invalid_metadata_and_anchors_fail_safely(library, original, tmp_path, before, after, code):
    """Reject forged structure and statuses without quoting private input."""
    path = _put(tmp_path, original.replace(before, after))
    with pytest.raises(ReferenceError, match=code) as caught:
        library.validate(path)
    assert str(tmp_path) not in str(caught.value)


@pytest.mark.parametrize('wrapper', [('```html\n', '\n```'), ('<!--\n', '\n-->'), ('    ', '')])
def test_anchors_inside_code_or_comments_do_not_cover_units(library, original, tmp_path, wrapper):
    """A marker shown as an example cannot satisfy the actual document unit."""
    marker = '<a id="dcs-adr.decision_context"></a>'
    path = _put(tmp_path, original.replace(marker.encode(), (wrapper[0] + marker + wrapper[1]).encode()))
    with pytest.raises(ReferenceError, match='anchor.missing'):
        library.validate(path)


@pytest.mark.parametrize('content', ['','TBD','**TODO**','Pending','<!-- invented -->'])
def test_empty_unit_fails(library, original, tmp_path, content):
    """Headings and placeholder-only text are not meaningful content presence."""
    text = original.decode()
    start = text.index('## Context, concern, constraints and status')
    end = text.index('<a id="dcs-adr.architecture_options">')
    text = text[:start] + '## Flexible title\n\n' + content + '\n\n' + text[end:]
    with pytest.raises(ReferenceError, match='content.empty_or_placeholder'):
        library.validate(_put(tmp_path, text.encode()))


def test_precedence_and_missing_fallthrough(library, original, tmp_path, monkeypatch):
    """Resolve engagement, organisation, user, bundled without merging content."""
    user, org, eng = [tmp_path / name for name in ('user', 'org', 'eng')]
    monkeypatch.delenv('JAI_EXPERT_REFERENCES_DIR', raising=False)
    kwargs = dict(user_root=user, organisation_root=org, engagement_root=eng)
    assert library.resolve('adr', 'simple', **kwargs)[1]['scope'] == 'bundled'
    for root, scope in [(user, 'user'), (org, 'organisation'), (eng, 'engagement')]:
        path = _put(root, original)
        selected, result = library.resolve('adr', 'simple', **kwargs)
        assert selected == path and result['scope'] == scope
        assert str(root) not in json.dumps(result)
        assert hashlib.sha256(original).hexdigest() not in json.dumps(result)
        assert 'example:adr' not in json.dumps(result)


def test_invalid_selected_override_never_falls_back(library, original, tmp_path):
    """A present invalid engagement reference blocks otherwise valid defaults."""
    _put(tmp_path, original.replace(b'language: en', b'language: invalid'))
    with pytest.raises(ReferenceError, match='SELECTED_REFERENCE_INVALID:engagement'):
        library.resolve('adr', 'simple', engagement_root=tmp_path, user_root=tmp_path / 'missing')


def test_same_scope_ambiguity_fails(library, original, tmp_path):
    """Two files with the same semantic slot cannot be silently selected."""
    _put(tmp_path, original)
    _put(tmp_path, original, 'alternative.md')
    with pytest.raises(ReferenceError, match='REFERENCE_CONFLICT:engagement'):
        library.resolve('adr', 'simple', engagement_root=tmp_path)


def test_different_complexities_are_not_conflicts(library, original, tmp_path):
    """Multiple applicable slots in one family are normal library contents."""
    _put(tmp_path, original)
    medium = (library.base / 'adr/medium.md').read_bytes()
    _put(tmp_path, medium, 'medium.md')
    assert library.resolve('adr', 'simple', engagement_root=tmp_path)[1]['scope'] == 'engagement'


def test_xdg_and_organisation_environment(library, original, tmp_path, monkeypatch):
    """Configured XDG/user and organization roots follow the approved order."""
    monkeypatch.setenv('XDG_CONFIG_HOME', str(tmp_path / 'xdg'))
    _put(tmp_path / 'xdg/jai/expert_references', original)
    monkeypatch.delenv('JAI_EXPERT_REFERENCES_DIR', raising=False)
    assert library.resolve('adr', 'simple')[1]['scope'] == 'user'
    _put(tmp_path / 'org', original)
    monkeypatch.setenv('JAI_EXPERT_REFERENCES_DIR', str(tmp_path / 'org'))
    assert library.resolve('adr', 'simple')[1]['scope'] == 'organisation'


@pytest.mark.parametrize('which', ['root', 'family', 'file'])
def test_symlink_escape_rejected(library, original, tmp_path, which):
    """No configured scope can redirect resolution through symlinks."""
    actual = tmp_path / 'actual'
    source = _put(actual, original)
    root = tmp_path / 'scope'
    if which == 'root':
        root.symlink_to(actual, target_is_directory=True)
    elif which == 'family':
        root.mkdir()
        (root / 'adr').symlink_to(actual / 'adr', target_is_directory=True)
    else:
        (root / 'adr').mkdir(parents=True)
        (root / 'adr/simple.md').symlink_to(source)
    with pytest.raises(ReferenceError, match='SYMLINK'):
        library.resolve('adr', 'simple', engagement_root=root)


def test_missing_everywhere_fails(library, tmp_path):
    """A genuinely absent required slot never passes just because data is absent."""
    library.base = tmp_path / 'missing-bundle'
    with pytest.raises(ReferenceError, match='REFERENCE_NOT_FOUND'):
        library.resolve('adr', 'simple', user_root=tmp_path / 'user', organisation_root=tmp_path / 'org')


def test_install_backup_reset_and_immutable_bundle(library, original, tmp_path):
    """Overrides install atomically, retain backups, and never edit shipped data."""
    source = _put(tmp_path / 'source', original)
    root = tmp_path / 'user'
    result = library.install(source, 'adr', 'simple', root)
    assert not result['backup_created']
    assert (root / 'adr/simple.md').read_bytes() == original
    changed = original.replace(b'## Options and selection criteria', b'## Alternatives')
    source.write_bytes(changed)
    assert library.install(source, 'adr', 'simple', root)['backup_created']
    assert any(path.read_bytes() == original for path in (root / 'adr').glob('*.backup-*'))
    assert library.reset('adr', 'simple', root) == {'removed': True}
    assert not (root / 'adr/simple.md').exists()
    assert not library.reset('adr', 'simple', root)['removed']
    assert library.resolve('adr', 'simple', user_root=root)[1]['scope'] == 'bundled'
    for target in (library.base, library.base.parent, library.base / 'adr'):
        with pytest.raises(ReferenceError, match='BUNDLED_REFERENCE_IMMUTABLE'):
            library.install(source, 'adr', 'simple', target)


def test_invalid_install_cannot_replace_existing(library, original, tmp_path):
    """Validation failure leaves existing reference bytes untouched."""
    target = _put(tmp_path / 'user', original)
    source = _put(tmp_path / 'source', b'bad metadata')
    with pytest.raises(ReferenceError):
        library.install(source, 'adr', 'simple', tmp_path / 'user')
    assert target.read_bytes() == original
    assert not list(target.parent.glob('*.backup-*'))


def test_bundled_checksum_detects_narrative_tampering(library, original, tmp_path):
    """Still valid anchors do not permit undetected bundled byte changes."""
    source = _put(tmp_path, original.replace(b'managed webhook events', b'changed webhook events'))
    assert library.validate(source)['structural_coverage'] == 'PASS'
    with pytest.raises(ReferenceError, match='BUNDLED_INTEGRITY_MISMATCH'):
        library.validate(source, bundled=True)


def test_cli_never_discloses_private_identifiers(library, original, tmp_path, capsys):
    """Private input paths, markers and raw values never appear in JSON output."""
    source = _put(tmp_path / 'Secret-Customer', original.replace(b'language: en', b'language: customer-sensitive-token'))
    assert main(['validate', '--root', str(ROOT), '--source', str(source)]) == 1
    output = capsys.readouterr().out
    assert str(tmp_path) not in output and 'customer-sensitive-token' not in output
    assert 'Secret-Customer' not in output
    source.write_bytes(original.replace(b'classification: public-synthetic', b'classification: confidential'))
    assert main(['validate', '--root', str(ROOT), '--source', str(source)]) == 0
    output = capsys.readouterr().out
    assert 'reference_id' not in output and 'sha256' not in output
    assert 'NOT_APPROVED' in output


@pytest.mark.parametrize('args', [['validate'], ['install', '--kind', 'adr', '--complexity', 'simple'], ['resolve', '--kind', '../../private', '--complexity', 'simple']])
def test_cli_incomplete_or_unsafe_calls_fail(args, capsys):
    """Unsupported or incomplete requests return machine-readable failure."""
    assert main(args + ['--root', str(ROOT)]) == 1
    assert json.loads(capsys.readouterr().out)['status'] == 'FAIL'


def test_known_optional_and_conditional_anchors_supported(library, original, tmp_path):
    """Additional registered units do not become unknown or implicitly mandatory."""
    extra = b'\n<a id="dcs-adr.technical_annex"></a>\n## Optional calculations\n\nThe operational calculations remain proposed.\n\n<a id="dcs-adr.privacy_analysis"></a>\n## Data handling\n\nPersonal data requires scoped access and retention review.\n'
    assert library.validate(_put(tmp_path, original + extra))['structural_coverage'] == 'PASS'


def test_dangling_dcs_link_is_not_evidence(library, original, tmp_path):
    """Reject cross-reference claims to nonexistent information-unit anchors."""
    source = _put(tmp_path, original + b'\nSee [support](#dcs-adr.privacy_analysis).\n')
    with pytest.raises(ReferenceError, match='reference.dangling_dcs_link'):
        library.validate(source)


def test_pages_not_guessed_and_word_excess_advisory(library, original, tmp_path):
    """Unknown page counts remain unknown and no length minimum gates quality."""
    source = _put(tmp_path / 'source', original)
    assert library.validate(source)['size_budget']['status'] == 'NOT_MEASURED'
    dcs = json.loads((library.specs.base / 'document_kinds/adr.yaml').read_text())
    dcs['size_budget']['metric'] = 'words'
    dcs['size_budget']['soft_max'] = 5
    registry = tmp_path / 'registry'
    (registry / 'document_kinds').mkdir(parents=True)
    (registry / 'document_kinds/adr.yaml').write_text(json.dumps(dcs))
    library.specs.base = registry
    library.specs.specs = dict(library.specs.specs)
    library.specs.specs['kind/adr'] = dcs
    result = library.validate(source)
    assert result['structural_coverage'] == 'PASS'
    assert result['size_budget']['excess']
    assert result['findings'] == [{'rule': 'size.soft_max_exceeded', 'severity': 'advisory', 'blocking': False}]


@pytest.mark.parametrize('field,value', [('path', '../adr/simple.md'), ('reference_id', 'forged'), ('language', 'de'), ('provenance', 'human-gold'), ('anchor_ids', ['adr.decision_context'])])
def test_manifest_metadata_consistency(library, field, value):
    """A correct raw checksum cannot hide inconsistent manifest identity fields."""
    library.entries[0][field] = value
    with pytest.raises(ReferenceError):
        library.validate_all()


def test_invalid_other_slot_does_not_break_selected_reference(library, original, tmp_path):
    """An unrelated malformed file is not the selected applicable override."""
    _put(tmp_path, original)
    _put(tmp_path, b'invalid other slot', 'medium.md')
    assert library.resolve('adr', 'simple', engagement_root=tmp_path)[1]['scope'] == 'engagement'


def test_install_refuses_ambiguous_scope_without_modification(library, original, tmp_path):
    """The convenience installer cannot report success into a conflicting slot."""
    root = tmp_path / 'user'
    other = _put(root, original, 'alternative.md')
    source = _put(tmp_path / 'source', original)
    with pytest.raises(ReferenceError, match='REFERENCE_CONFLICT'):
        library.install(source, 'adr', 'simple', root)
    assert other.read_bytes() == original
    assert not (root / 'adr/simple.md').exists()


def test_outline_selects_default_and_override_without_copying_reference_facts(library, original, tmp_path, monkeypatch):
    """Real authoring consumes reference selection but no fictional project facts."""
    from content_spec import ContentSpec
    engine = ContentSpec(ROOT)
    contract = next(key for key, binding in engine.bindings.items() if binding.get('document_kind') == 'adr')
    monkeypatch.delenv('JAI_EXPERT_REFERENCES_DIR', raising=False)
    default = engine.outline(contract, user_root=tmp_path / 'missing')
    assert default['expert_reference']['scope'] == 'bundled'
    assert default['expert_reference']['complexity'] == 'medium'
    assert default['expert_reference']['status'] == 'SELECTED_PROPOSED_REFERENCE'
    private_root = tmp_path / 'private-customer'
    _put(private_root, original)
    changed = engine.outline(contract, reference_complexity='simple', user_root=private_root)
    assert changed['expert_reference']['scope'] == 'user'
    assert str(private_root) not in json.dumps(changed)
    assert 'Harborline' not in json.dumps(changed)
    assert all(value is None for value in changed['semantic_model']['semantic_units'].values())
    _put(private_root, original.replace(b'approval_status: not-human-approved', b'approval_status: approved'))
    with pytest.raises(ValueError, match='EXPERT_REFERENCE_ERROR:SELECTED_REFERENCE_INVALID:user'):
        engine.outline(contract, reference_complexity='simple', user_root=private_root)


def test_outline_unsupported_family_is_explicit(library, tmp_path):
    """Families without supplied examples retain usable unfilled outlines."""
    from content_spec import ContentSpec
    engine = ContentSpec(ROOT)
    unsupported = []
    for key, binding in engine.bindings.items():
        try:
            library.canonical_family(binding.get('semantic_family', binding['document_kind']), contract_id=key)
        except ReferenceError as exc:
            if str(exc) == 'REFERENCE_SLOT_UNSUPPORTED':
                unsupported.append(key)
    contract = unsupported[0]
    result = engine.outline(contract, user_root=tmp_path / 'missing')
    assert result['expert_reference']['status'] == 'NOT_APPLICABLE'


@pytest.mark.parametrize('alias,family', [('strategy','it-digital-strategy'), ('implementation-specification','implementation-specification-lld'), ('test-strategy','test-strategy-plan'), ('service-design','service-design-sla'), ('benefits-review','benefits-realisation-review'), ('roadmap','transformation-roadmap')])
def test_registered_kind_alias_resolves_original_reference_family(library, tmp_path, alias, family):
    """Canonical DCS aliases select original bytes and stable reference identity."""
    path, report = library.resolve(alias, 'simple', user_root=tmp_path)
    assert path == library.base / family / 'simple.md'
    assert report['reference_family'] == family
    assert report['canonical_document_kind'] == alias
    assert report['mapping_status'] == 'proposed'
    assert report['professional_acceptance'] == 'NOT_APPROVED'


def test_all135_anchor_bindings_match_registered_required_units(library):
    """Every distributed source anchor maps onto an actual kind-owned MUST unit."""
    result = library.validate_all()
    assert result['family_count'] == 45
    assert result['proposal_reference_count'] == 30
    assert len(library.bindings) == 45
    for report in result['results']:
        assert set(report['present_units']) == set(report['required_units'])
        definition = library.specs.specs[report['spec_ref']]
        required = {unit['id'] for unit in definition['required_information'] if unit['obligation'] == 'MUST'}
        assert set(report['required_units']) == required


@pytest.mark.parametrize('before,after,diagnostic', [
    (b'dcs_status: proposed-not-mapped', b'dcs_status: approved', 'METADATA_SCHEMA_INVALID'),
    (b'dcs_status: proposed-not-mapped\n', b'', 'PROPOSED_DCS_STATUS_REQUIRED'),
    (b'proposed/kind/client-proposal', b'proposed/kind/commercial-proposal', 'DCS_IDENTITY_MISMATCH'),
    (b'dcs-proposed-client-proposal.customer_need', b'dcs-client-proposal.customer_need', 'anchor.missing'),
    (b'content_revision: 2.1.0', b'content_revision: approved', 'METADATA_SCHEMA_INVALID'),
    (b'proposal_pack_id:', b'authority_signature:', 'METADATA_SCHEMA_INVALID'),
])
def test_proposed_metadata_and_anchor_errors_cannot_promote_rules(library, tmp_path, before, after, diagnostic):
    """Proposed source namespaces stay explicit and cannot masquerade as approval."""
    raw = (library.base / 'client-proposal/simple.md').read_bytes()
    assert before in raw
    source = tmp_path / 'proposal.md'
    source.write_bytes(raw.replace(before, after))
    with pytest.raises(ReferenceError, match=diagnostic):
        library.validate(source, 'client-proposal', 'simple')


def test_invalid_selected_proposal_override_never_falls_back(library, tmp_path):
    """All newly supported families retain strict higher-precedence failure."""
    source = tmp_path / 'client-proposal/simple.md'
    source.parent.mkdir()
    raw = (library.base / 'client-proposal/simple.md').read_bytes()
    source.write_bytes(raw.replace(b'dcs-proposed-client-proposal.customer_need', b'dcs-proposed-client-proposal.unknown'))
    with pytest.raises(ReferenceError, match='SELECTED_REFERENCE_INVALID:engagement'):
        library.resolve('client-proposal', 'simple', engagement_root=tmp_path)


def test_context_and_audience_selection_is_explicit_and_redacted(library, original, tmp_path):
    """Explicit selectors distinguish same-slot audience variants without guessing."""
    marker = b'approval_status: not-human-approved'
    finance = original.replace(marker, marker + b'\ntarget_audiences: [finance]\napplicability_context: {sector: private-example}')
    engineering = original.replace(marker, marker + b'\ntarget_audiences: [engineering]\napplicability_context: {sector: private-example}')
    _put(tmp_path, finance)
    alternative = _put(tmp_path, engineering, 'engineering.md')
    _, report = library.resolve('adr', 'simple', user_root=tmp_path)
    assert report['scope'] == 'bundled'
    path, report = library.resolve('adr', 'simple', user_root=tmp_path, audience='engineering', context={'sector':'private-example'})
    assert path == alternative
    assert report['scope'] == 'user'
    assert report['selection_context'] == {'context_supplied':True,'audience_supplied':True}
    assert 'private-example' not in json.dumps(report)
    assert 'engineering' not in json.dumps(report)
    assert str(tmp_path) not in json.dumps(report)


def test_context_selector_cannot_turn_invalid_override_into_fallback(library, original, tmp_path):
    """Malformed metadata cannot hide behind a nonmatching audience selector."""
    raw = original.replace(b'language: en', b'language: unsupported\ntarget_audiences: [finance]')
    _put(tmp_path, raw)
    with pytest.raises(ReferenceError, match='SELECTED_REFERENCE_INVALID:user'):
        library.resolve('adr','simple',user_root=tmp_path,audience='engineering')


@pytest.mark.parametrize('contract,family', [('delivery-manager:1','delivery-proposal'), ('bid-proposal-manager:1','rfp-response'), ('bid-proposal-manager:3','client-proposal')])
def test_colliding_role_mappings_have_explicit_authoring_defaults(library, tmp_path, contract, family):
    """Registered explicit choices resolve genuine overlapping role associations."""
    from content_spec import ContentSpec
    assert library.authoring_defaults[contract] == family
    engine = ContentSpec(ROOT)
    result = engine.outline(contract, user_root=tmp_path / 'missing')
    assert result['expert_reference']['reference_family'] == family
    assert result['expert_reference']['professional_acceptance'] == 'NOT_APPROVED'


def test_nonfinite_context_and_unknown_audience_types_fail_safely(library, tmp_path):
    """Selectors cannot accept malformed JSON or echo private context values."""
    for context, audience in [({'secret': float('nan')}, None), (['private'], None), ({}, ['private'])]:
        with pytest.raises(ReferenceError) as caught:
            library.resolve('adr','simple',user_root=tmp_path,context=context,audience=audience)
        assert 'private' not in str(caught.value)


def test_context_filters_cannot_hide_canonical_identity_errors(library, original, tmp_path):
    """Wrong-slot metadata fails before applicability can mask a selected override."""
    raw = original.replace(b'document_kind: adr', b'document_kind: hld').replace(b'approval_status: not-human-approved', b'approval_status: not-human-approved\ntarget_audiences: [finance]')
    _put(tmp_path, raw)
    with pytest.raises(ReferenceError, match='SELECTED_REFERENCE_INVALID:user'):
        library.resolve('adr','simple',user_root=tmp_path,audience='engineering')


ENGINEERING_FAMILIES = (
    'software-engineering-plan', 'api-interface-contract', 'release-readiness-review',
    'transformation-baseline-assessment', 'target-operating-model', 'transformation-execution-plan',
    'security-architecture-assessment', 'threat-model', 'security-control-assessment',
    'devsecops-pipeline-design', 'cicd-pipeline-assurance', 'appsec-verification-report',
    'software-supply-chain-assessment',
)


@pytest.mark.parametrize('family', ENGINEERING_FAMILIES)
@pytest.mark.parametrize('complexity', ('simple', 'medium', 'complex'))
def test_engineering_reference_selection_preserves_proposed_status(library, tmp_path, family, complexity):
    """Every new family selects locally without evidence or authority promotion."""
    path, report = library.resolve(family, complexity, user_root=tmp_path,
                                   audience='engineering reviewer', context={'domain': 'security'})
    assert path == library.base / family / f'{complexity}.md'
    assert report['source_dcs_status'] == 'proposed-not-mapped'
    assert report['professional_acceptance'] == 'NOT_APPROVED'
    assert report['evidence_and_rationale_quality'] == 'NOT_EVALUATED'
    assert report['content_adequacy'] == 'NOT_EVALUATED'


@pytest.mark.parametrize('family', ENGINEERING_FAMILIES)
def test_invalid_selected_engineering_override_never_falls_back(library, tmp_path, family):
    """New domains inherit hard failure for an invalid applicable override."""
    raw = (library.base / family / 'simple.md').read_bytes()
    target = tmp_path / family / 'simple.md'
    target.parent.mkdir()
    target.write_bytes(raw.replace(b'dcs_status: proposed-not-mapped', b'dcs_status: approved'))
    with pytest.raises(ReferenceError, match='SELECTED_REFERENCE_INVALID:engagement'):
        library.resolve(family, 'simple', engagement_root=tmp_path)


@pytest.mark.parametrize('field', ('case_id', 'methodology_context'))
def test_engineering_manifest_case_metadata_must_match(library, field):
    """Correct hashes cannot conceal a contradictory illustrative case identity."""
    entry = next(item for item in library.entries if item['document_kind'] == 'threat-model')
    entry[field] = 'contradictory metadata'
    with pytest.raises(ReferenceError, match='BUNDLED_INTEGRITY_MISMATCH'):
        library.validate_all()


def test_all_established_reference_bytes_remain_unchanged(library):
    """Pin the 96 public example identities and hashes, including 30 proposals."""
    established = [entry for entry in library.entries if entry['document_kind'] not in ENGINEERING_FAMILIES]
    assert len(established) == 96
    fingerprint = hashlib.sha256(json.dumps(sorted((entry['reference_id'], entry['sha256'])
                                                  for entry in established), separators=(',', ':')).encode()).hexdigest()
    assert fingerprint == '0e0ebf739017564a9195328211f884bd6b2038e336648c7d2116e671f3c50a5a'
    for entry in established:
        assert hashlib.sha256((library.base / entry['path']).read_bytes()).hexdigest() == entry['sha256']
