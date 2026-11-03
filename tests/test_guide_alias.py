# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""One Git guide alias becomes regular canonical help in installations and ZIPs."""
import importlib.util
from pathlib import Path
import stat
import sys
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from guide_alias import GUIDE_ALIAS, GUIDE_SOURCE, GUIDE_LINK, guide_bytes
import release_bundle

_spec = importlib.util.spec_from_file_location('guide_installer', ROOT / '.ai/setup/installer.py')
installer = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(installer)


def _package(tmp_path):
    package = tmp_path / 'source'
    for relative, content in ((GUIDE_SOURCE, b'# Canonical fictional operator help.\n'),
                              ('RELEASE-SCOPE.json', (ROOT / 'RELEASE-SCOPE.json').read_bytes()),
                              ('.ai/runtime/schema/release-scope.schema.json',
                               (ROOT / '.ai/runtime/schema/release-scope.schema.json').read_bytes())):
        path = package / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    (package / '.ai/runtime/GUIDE.md').symlink_to(GUIDE_LINK)
    return package


@pytest.mark.parametrize('representation', ['symlink', 'git-stub'])
def test_installer_materializes_canonical_guide_for_git_link_and_windows_stub(tmp_path, representation):
    package = _package(tmp_path)
    alias = package / GUIDE_ALIAS
    if representation == 'git-stub':
        alias.unlink()
        alias.write_bytes(GUIDE_LINK.encode('utf-8'))
    expected = (package / GUIDE_SOURCE).read_bytes()
    assert guide_bytes(package) == expected
    house = tmp_path / 'installed'
    outputs, modes = installer.desired_outputs(package, set(), house, tmp_path / 'claude', tmp_path / 'codex', {})
    target = house / 'GUIDE.md'
    installer.atomic_write(target, outputs[str(target)], modes[str(target)])
    assert target.read_bytes() == expected
    assert target.is_file() and not target.is_symlink()
    assert modes[str(target)] == 0o644
    (package / GUIDE_SOURCE).unlink()
    assert target.read_bytes() == expected


def test_zip_materializes_only_declared_alias_from_selected_canonical_bytes(tmp_path, monkeypatch):
    package = _package(tmp_path)
    private = package / 'INBOX/private-fixture.md'
    private.parent.mkdir()
    private.write_text('Private fictional fixture.\n')
    (package / 'arbitrary-guide.md').symlink_to(private)
    reader = release_bundle._read_resource
    reads = []

    def regular_only(root, relative):
        assert relative not in {GUIDE_ALIAS, 'arbitrary-guide.md'}
        reads.append(relative)
        return reader(root, relative)

    monkeypatch.setattr(release_bundle, '_read_resource', regular_only)
    archive_path = tmp_path / 'archive/package.zip'
    archive_path.parent.mkdir()
    release_bundle.build_zip(package, archive_path, 'package')
    expected = (package / GUIDE_SOURCE).read_bytes()
    assert reads.count(GUIDE_SOURCE) == 2  # Initial and final unchanged-source snapshots.
    with zipfile.ZipFile(archive_path) as archive:
        item = archive.getinfo('package/' + GUIDE_ALIAS)
        assert stat.S_ISREG(item.external_attr >> 16)
        assert archive.read(item) == expected
        assert not any('private-fixture' in name or 'arbitrary-guide' in name for name in archive.namelist())
        extracted = tmp_path / 'extracted'
        archive.extractall(extracted)
    materialized = extracted / 'package'
    assert not (materialized / GUIDE_ALIAS).is_symlink()
    outputs, _ = installer.desired_outputs(materialized, set(), tmp_path / 'house', tmp_path / 'claude', tmp_path / 'codex', {})
    assert outputs[str(tmp_path / 'house/GUIDE.md')] == expected


def test_foreign_guide_alias_is_rejected_without_reading_its_private_target(tmp_path, monkeypatch):
    package = _package(tmp_path)
    private = package / 'INBOX/private-fixture.md'
    private.parent.mkdir()
    private.write_text('Private fictional fixture.\n')
    alias = package / GUIDE_ALIAS
    alias.unlink()
    alias.symlink_to('../../INBOX/private-fixture.md')
    original = Path.read_bytes

    def public_only(path):
        assert path not in {private, alias}
        return original(path)

    monkeypatch.setattr(Path, 'read_bytes', public_only)
    with pytest.raises(ValueError, match='declared relative canonical source'):
        guide_bytes(package)
    output = tmp_path / 'archive/rejected.zip'
    output.parent.mkdir()
    with pytest.raises(ValueError, match='declared relative canonical source'):
        release_bundle.build_zip(package, output, 'package')
    assert not output.exists()
