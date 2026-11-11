# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Private fact storage retention and real-filesystem lifecycle integration tests."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'apps/fabric-explorer/reader'))
from semantic_reader import _FactList


import pytest


@pytest.fixture
def spools(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    owned = []
    def create(*args, **kwargs):
        facts = _FactList(*args, **kwargs)
        owned.append(facts)
        return facts
    try:
        yield create
    finally:
        for facts in owned:
            while not facts.closed: facts.release()


def test_completed_facts_do_not_retain_decoded_dictionaries(spools):
    facts = spools({'maxVertices': 10, 'maxEdges': 10, 'maxEncodedGraphBytes': 4096})
    import weakref
    class WeakFact(dict): pass
    fact = WeakFact(kind='version', sourceId='synthetic-source', label='original')
    reference = weakref.ref(fact)
    facts.append(fact)
    fact['label'] = 'mutated'
    assert not isinstance(facts, list), 'Completed facts must retain framed bytes, not decoded dictionaries'
    assert facts.read(0)[0]['label'] == 'original'
    del fact
    assert reference() is None, 'A completed spool must not retain its decoded input object'
    facts.release()

import errno
import json
import os
import struct

import facts_spool
import semantic_reader
from facts_spool import _Budget, _Pool
from semantic_reader import SemanticReadError, _encoded

LIMITS = {'maxVertices': 100000, 'maxEdges': 500000, 'maxEncodedGraphBytes': 512 * 1024 * 1024}
FACT = {'kind': 'version', 'sourceId': 'synthetic-source', 'label': 'Ω\ud800', 'value': {'type': 'float64', 'bits': '8000000000000000'}}


def test_exact_framed_bytes_and_reference_owned_close(tmp_path, monkeypatch, spools):
    monkeypatch.chdir(tmp_path)
    before = list(tmp_path.iterdir())
    facts = spools(LIMITS)
    facts.append(FACT); facts.seal()
    encoded = _encoded(FACT)
    assert facts.physical == len(encoded) + 4 and facts.encoded == len(encoded)
    facts.handle.seek(0)
    assert facts.handle.read() == struct.pack('>I', len(encoded)) + encoded
    assert facts.read(0) == (FACT, len(encoded) + 4, len(encoded))
    facts.acquire(); facts.release()
    assert not facts.closed and facts.refs == 1
    with pytest.raises(SemanticReadError): facts.append(FACT)
    facts.release(); facts.release()
    assert facts.closed and facts.handle.closed and facts.pool.physical == 0 and not facts.pool.objects
    if sys.platform == 'linux': assert list(tmp_path.iterdir()) == before


@pytest.mark.parametrize('field,maximum', [('maxEncodedGraphBytes', len(_encoded(FACT))), ('maxVertices', 1)])
def test_inclusive_candidate_limits_reserve_before_write(field, maximum, spools):
    limits = {**LIMITS, field: maximum}
    facts = spools(limits)
    facts.append(FACT)
    before = facts.physical, facts.pool.physical, facts.budget.count
    with pytest.raises(SemanticReadError): facts.append(FACT)
    assert (facts.physical, facts.pool.physical, facts.budget.count) == before
    facts.release()


def test_shared_budget_counts_sources_and_edges_without_reencoding(monkeypatch, spools):
    budget = _Budget({**LIMITS, 'maxVertices': 1, 'maxEdges': 1}, SemanticReadError)
    one = spools(LIMITS, budget); two = spools(LIMITS, budget)
    one.append(FACT); one.seal()
    two.append({**FACT, 'kind': 'reference'})
    before = two.physical
    with pytest.raises(SemanticReadError): two.append(FACT)
    assert two.physical == before and budget.count == 2
    one.release(); two.release()


def test_exact_record_count_and_physical_domain_boundaries(monkeypatch, spools):
    facts = spools(LIMITS)
    facts.budget.count = 599999
    facts.append(FACT)
    with pytest.raises(SemanticReadError): facts.append(FACT)
    facts.release()
    physical = len(_encoded(FACT)) + 4
    monkeypatch.setattr(facts_spool, 'PHYSICAL_DOMAIN', physical)
    facts = spools(LIMITS); facts.append(FACT)
    with pytest.raises(SemanticReadError): facts.append(FACT)
    assert facts.physical == physical
    facts.release()


def test_frame_guard_inclusive_and_one_byte_over(monkeypatch, spools):
    size = len(_encoded(FACT)); monkeypatch.setattr(semantic_reader, 'CHUNK', size)
    facts = spools(LIMITS); facts.append(FACT); facts.release()
    monkeypatch.setattr(semantic_reader, 'CHUNK', size - 1)
    facts = spools(LIMITS)
    with pytest.raises(SemanticReadError): facts.append(FACT)
    assert facts.pool.physical == 0
    facts.release()


@pytest.mark.parametrize('corruption', ['zero', 'oversize', 'truncated-prefix', 'truncated-body', 'invalid-json', 'invalid-kind'])
def test_corrupt_private_frames_reject_without_recovery(corruption, spools):
    facts = spools(LIMITS); facts.append(FACT); facts.seal()
    facts.handle.seek(0)
    if corruption == 'zero': facts.handle.write(struct.pack('>I', 0))
    elif corruption == 'oversize': facts.handle.write(struct.pack('>I', 1024 * 1024 + 1))
    elif corruption == 'truncated-prefix': facts.handle.truncate(3)
    elif corruption == 'truncated-body': facts.handle.truncate(facts.physical - 1)
    elif corruption == 'invalid-json': facts.handle.seek(4); facts.handle.write(b'!')
    else:
        encoded = _encoded({**FACT, 'kind': 'unknown'})
        facts.handle.write(struct.pack('>I', len(encoded)) + encoded)
    facts.handle.flush()
    with pytest.raises(SemanticReadError): facts.read(0)
    facts.release()


def test_closed_descriptor_read_and_write_fail_explicitly_and_release_reservations(spools):
    facts = spools(LIMITS); facts.handle.close()
    with pytest.raises(SemanticReadError): facts.append(FACT)
    assert facts.pool.physical == 0 and facts.budget.count == 0
    with pytest.raises(SemanticReadError): facts.read(0)
    facts.release()
    assert not facts.pool.objects


def test_real_disk_full_rejects_at_flush_and_releases_descriptor(monkeypatch, spools):
    if not Path('/dev/full').exists(): pytest.skip('Linux full device unavailable')
    # Exercise actual OS ENOSPC on a real descriptor, preserving the spool class.
    def full_file(**_options): return open('/dev/full', 'w+b')
    monkeypatch.setattr(facts_spool.tempfile, 'TemporaryFile', full_file)
    facts = spools(LIMITS)
    with pytest.raises(SemanticReadError) as failed:
        facts.append(FACT); facts.seal()
    assert isinstance(failed.value.__cause__, OSError)
    assert failed.value.__cause__.errno == errno.ENOSPC
    try: facts.release()
    except OSError as error: assert error.errno == errno.ENOSPC
    assert not facts.pool.objects and facts.pool.physical == 0


def test_descriptor_and_total_physical_reservations_precede_allocation(monkeypatch, spools):
    pool = _Pool(SemanticReadError)
    monkeypatch.setattr(facts_spool, 'DESCRIPTORS', 1)
    one = spools(LIMITS, pool=pool)
    with pytest.raises(SemanticReadError): spools(LIMITS, pool=pool)
    assert len(pool.objects) == 1
    monkeypatch.setattr(facts_spool, 'PHYSICAL_TOTAL', len(_encoded(FACT)) + 4)
    one.append(FACT)
    with pytest.raises(SemanticReadError): one.append(FACT)
    assert pool.physical == one.physical
    one.release()


def test_create_failure_is_private_resource_error(monkeypatch, spools):
    def full_file(**_options): raise OSError(errno.ENOSPC, 'private fault text')
    monkeypatch.setattr(facts_spool.tempfile, 'TemporaryFile', full_file)
    pool = _Pool(SemanticReadError)
    with pytest.raises(SemanticReadError) as failed: spools(LIMITS, pool=pool)
    assert failed.value.diagnostic['code'] == 'resource-limit'
    assert 'private fault text' not in str(failed.value)
    assert not pool.objects and pool.physical == 0


def test_close_failure_does_not_strand_other_owned_spools(spools):
    class FaultOnClose:
        def __init__(self, handle): self.handle = handle
        def close(self):
            self.handle.close()
            raise OSError(errno.ENOSPC, 'deferred close failure')
    pool = _Pool(SemanticReadError)
    objects = [spools(LIMITS, pool=pool) for _ in range(2)]
    for facts in objects: facts.append(FACT)
    objects[0].handle = FaultOnClose(objects[0].handle)
    for facts in objects: facts.release()
    assert not pool.objects and pool.physical == 0 and all(item.closed for item in objects)


def test_helper_process_exit_leaves_no_linux_spool_entries(tmp_path):
    if sys.platform != 'linux': pytest.skip('Linux initial qualification only')
    import subprocess
    script = "from semantic_reader import _FactList; import os; f=_FactList({'maxVertices':1,'maxEdges':1,'maxEncodedGraphBytes':4096}); f.append({'kind':'version','sourceId':'synthetic'}); f.seal(); os._exit(0)"
    completed = subprocess.run([sys.executable, '-c', script], cwd=tmp_path,
                               env={**os.environ, 'PYTHONPATH': str(ROOT / 'apps/fabric-explorer/reader')},
                               timeout=5, capture_output=True)
    assert completed.returncode == 0 and list(tmp_path.iterdir()) == []


def test_exact_semantic_edge_ceiling_precedes_write(spools):
    facts = spools(LIMITS)
    facts.budget.edges = 499999
    facts.budget.count = 499999
    facts.append({**FACT, 'kind': 'reference'})
    before = facts.physical
    with pytest.raises(SemanticReadError): facts.append({**FACT, 'kind': 'reference'})
    assert facts.physical == before and facts.budget.edges == 500000
    facts.release()


def test_short_write_rolls_back_reservation_and_cannot_publish_partial_record(spools):
    class ShortWrite:
        def __init__(self, handle): self.handle = handle
        def seek(self, offset): return self.handle.seek(offset)
        def write(self, data): return self.handle.write(data[:-1])
        def close(self): return self.handle.close()
    facts = spools(LIMITS); facts.handle = ShortWrite(facts.handle)
    with pytest.raises(SemanticReadError): facts.append(FACT)
    assert facts.failed and facts.pool.physical == 0 and facts.budget.count == 0
    with pytest.raises(SemanticReadError): facts.seal()
    facts.release(); assert not facts.pool.objects


def test_read_os_failure_is_redacted_after_successful_seal(spools):
    facts = spools(LIMITS); facts.append(FACT); facts.seal(); facts.handle.close()
    with pytest.raises(SemanticReadError) as failed: facts.read(0)
    assert failed.value.diagnostic['code'] == 'read-failed'
    facts.release(); assert not facts.pool.objects


def test_memoryerror_during_write_rolls_back_exact_physical_reservation(spools):
    class BrokenWrite:
        def __init__(self, handle): self.handle = handle
        def seek(self, *args): return self.handle.seek(*args)
        def write(self, _data): raise MemoryError('controlled write failure')
        def close(self): return self.handle.close()
    pool = _Pool(SemanticReadError); facts = spools(LIMITS, pool=pool)
    facts.handle = BrokenWrite(facts.handle)
    try:
        with pytest.raises(MemoryError): facts.append(FACT)
        assert facts.failed and pool.physical == 0
        with pytest.raises(SemanticReadError): facts.seal()
    finally: facts.release()
    assert not pool.objects and pool.physical == 0


def test_memoryerror_installing_cache_rolls_back_acquired_owner(spools):
    from semantic_reader import SemanticReader
    class BrokenCache(dict):
        def __setitem__(self, _key, _value): raise MemoryError('controlled cache insertion failure')
    reader = SemanticReader(None, None, None)
    facts = spools(LIMITS, pool=reader._pool); facts.append(FACT); facts.seal()
    reader.findings_cache = BrokenCache()
    reader._pending_cache = {('group', 'source'): (b'', 3, (facts,))}
    try:
        with pytest.raises(MemoryError): reader._commit_cache()
        assert facts.refs == 1
    finally:
        while not facts.closed: facts.release()
    assert not reader._pool.objects and reader._pool.physical == 0


@pytest.mark.parametrize('constant', ['NaN', 'Infinity', '-Infinity'])
def test_corrupt_private_nonfinite_json_is_named_read_failure(constant, spools):
    facts = spools(LIMITS); facts.append(FACT); facts.seal()
    data = ('{"kind":"version","value":' + constant + '}').encode()
    facts.handle.seek(0); facts.handle.write(struct.pack('>I', len(data)) + data); facts.handle.flush()
    try:
        with pytest.raises(SemanticReadError) as failed: facts.read(0)
        assert failed.value.diagnostic['code'] == 'read-failed'
    finally: facts.release()


def test_memoryerror_closing_first_source_does_not_strand_other_lease_sources(spools):
    from semantic_reader import SemanticReader
    class BrokenClose:
        def __init__(self, handle): self.handle = handle
        def close(self):
            self.handle.close()
            raise MemoryError('controlled close failure')
    reader = SemanticReader(None, None, None)
    objects = [spools(LIMITS, pool=reader._pool) for _ in range(2)]
    for facts in objects: facts.append(FACT); facts.seal()
    objects[0].handle = BrokenClose(objects[0].handle)
    reader.leases['lease'] = {'group': 'group', 'facts': objects}
    try:
        with pytest.raises(MemoryError): reader.release('group', 'lease')
        assert not reader.leases and not reader._pool.objects and reader._pool.physical == 0
    finally:
        for facts in objects: facts.release()


def test_group_close_memoryerror_releases_all_leases_and_cache_owners(spools):
    from semantic_reader import SemanticReader
    class BrokenClose:
        def __init__(self, handle): self.handle = handle
        def close(self):
            self.handle.close()
            raise MemoryError('controlled close failure')
    reader = SemanticReader(None, None, None)
    objects = [spools(LIMITS, pool=reader._pool) for _ in range(3)]
    for facts in objects: facts.append(FACT); facts.seal()
    objects[0].handle = BrokenClose(objects[0].handle)
    reader.leases['one'] = {'group': 'group', 'facts': [objects[0]]}
    reader.leases['two'] = {'group': 'group', 'facts': [objects[1]]}
    reader.findings_cache[('group', 'source')] = (b'', 3, (objects[2],))
    with pytest.raises(MemoryError): reader.release_group('group')
    assert not reader.leases and not reader.findings_cache and not reader._pool.objects and reader._pool.physical == 0


def test_flush_memoryerror_poisoning_preserves_original_category_and_owner_cleanup(spools):
    class BrokenFlush:
        def __init__(self, handle): self.handle = handle
        def __getattr__(self, name): return getattr(self.handle, name)
        def flush(self): raise MemoryError('controlled flush failure')
    facts = spools(LIMITS); facts.append(FACT); facts.handle = BrokenFlush(facts.handle)
    with pytest.raises(MemoryError): facts.seal()
    assert facts.failed and not facts.sealed
    with pytest.raises(SemanticReadError): facts.acquire()
    facts.release()
    assert not facts.pool.objects and facts.pool.physical == 0
