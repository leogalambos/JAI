#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Per-stage performance/reproducibility budget with explicit 20% regression policy."""
from __future__ import annotations
import argparse, json, platform, resource, statistics, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; RUNTIME=ROOT/'.ai/runtime'; CONFIG=RUNTIME/'ci/performance-stages.json'; BASE=RUNTIME/'ci/performance-baseline.json'
def environment():
    return {
        'python': platform.python_version(),
        'implementation': platform.python_implementation(),
        'platform': platform.platform(),
    }
def size_count(root):
    files=[p for p in Path(root).rglob('*') if p.is_file() and '__pycache__' not in p.parts and not p.name.endswith('.pyc')]
    return len(files),sum(p.stat().st_size for p in files)
def run_once(stage):
    before=resource.getrusage(resource.RUSAGE_CHILDREN); t=time.perf_counter()
    try: p=subprocess.run(stage['command'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=stage['timeout_seconds'])
    except subprocess.TimeoutExpired:
        count,size=size_count(ROOT); return {'name':stage['name'],'ok':False,'timeout':True,'wall_time':time.perf_counter()-t,'cpu_time':None,'peak_memory_kb':None,'artifact_count':count,'input_size':size,'cache_status':'not-declared','detail':f'timeout at stage {stage["name"]}'}
    after=resource.getrusage(resource.RUSAGE_CHILDREN); count,size=size_count(ROOT)
    return {'name':stage['name'],'ok':p.returncode==0,'timeout':False,'wall_time':time.perf_counter()-t,'cpu_time':(after.ru_utime+after.ru_stime)-(before.ru_utime+before.ru_stime),'peak_memory_kb':after.ru_maxrss,'artifact_count':count,'input_size':size,'cache_status':'not-declared','detail':p.stdout[-1500:] if p.returncode else ''}
def run(profile,samples=9):
    cfg=json.loads(CONFIG.read_text()); rows=[]
    # Nine independent runs mitigate short-stage scheduler noise while retaining
    # the original hard 20% regression threshold and stage timeouts.
    for stage in cfg['profiles'][profile]:
        rs=[run_once(stage) for _ in range(max(1,samples))]
        cpu=[x['cpu_time'] for x in rs if x['cpu_time'] is not None]; mem=[x['peak_memory_kb'] for x in rs if x['peak_memory_kb'] is not None]
        row=dict(rs[-1]); row.update({'ok':all(x['ok'] for x in rs),'timeout':any(x['timeout'] for x in rs),'wall_time':statistics.median(x['wall_time'] for x in rs),'cpu_time':statistics.median(cpu) if cpu else None,'peak_memory_kb':max(mem) if mem else None,'samples':len(rs)})
        if not row['ok']: row['detail']='; '.join(x.get('detail','') for x in rs if not x['ok'])[-3000:]
        rows.append(row)
    return rows
def compare(rows,baseline):
    limit=json.loads(CONFIG.read_text())['regression_limit_percent']/100; probs=[]
    if baseline.get('environment') != environment():
        return ['baseline environment mismatch; record a baseline on this release environment']
    bm={x['name']:x for x in baseline.get('stages',[])}
    for r in rows:
        if not r['ok']: probs.append(f"{r['name']}: failed/timeout"); continue
        b=bm.get(r['name'])
        if not b: probs.append(f"{r['name']}: no baseline"); continue
        if r['wall_time']>b['wall_time']*(1+limit) and not b.get('waiver'):
            probs.append(f"{r['name']}: wall {r['wall_time']:.3f}s > 120% baseline {b['wall_time']:.3f}s")
    return probs
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--profile',choices=['fast','full'],default='fast'); ap.add_argument('--record-baseline',action='store_true'); ap.add_argument('--samples',type=int,default=9); ap.add_argument('--out'); a=ap.parse_args()
    rows=run(a.profile,a.samples); report={'profile':a.profile,'samples':a.samples,'environment':environment(),'stages':rows}
    if a.out: Path(a.out).write_text(json.dumps(report,indent=2)+'\n')
    for r in rows: print(('PASS' if r['ok'] else 'FAIL'),r['name'],f"wall={r['wall_time']:.3f}s cpu={r['cpu_time']} peak_kb={r['peak_memory_kb']} artifacts={r['artifact_count']} input={r['input_size']} cache={r['cache_status']} samples={r['samples']}")
    if a.record_baseline:
        current={'schema_version':'1.2.0','regression_limit_percent':20,'profile':a.profile,'measurement':'median','samples':a.samples,'environment':environment(),'stages':[{'name':r['name'],'wall_time':r['wall_time'],'cpu_time':r['cpu_time'],'peak_memory_kb':r['peak_memory_kb'],'artifact_count':r['artifact_count'],'input_size':r['input_size']} for r in rows]}
        BASE.write_text(json.dumps(current,indent=2)+'\n'); print('recorded',BASE); return 0 if all(r['ok'] for r in rows) else 1
    if not BASE.is_file(): print('FAIL no performance baseline'); return 1
    probs=compare(rows,json.loads(BASE.read_text())); [print('FAIL',x) for x in probs]
    return 1 if probs else 0
if __name__=='__main__': raise SystemExit(main())
