#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Remove only AI IS/IT house outputs still matching the recorded install state."""
from __future__ import annotations
import argparse,json,os,shutil,sys,time
from pathlib import Path

def sha(p):
 import hashlib
 try:
  h=hashlib.sha256()
  with open(p,'rb') as f:
   for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
  return h.hexdigest()
 except OSError:return None

def atomic(path,text):
 import tempfile
 path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(prefix='.'+path.name+'.',dir=str(path.parent))
 with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(text)
 os.replace(tmp,path)

def load(p,default):
 try:return json.loads(Path(p).read_text(encoding='utf-8'))
 except FileNotFoundError:return default

def cmds(e): return {h.get('command') for h in e.get('hooks',[]) if isinstance(h,dict) and h.get('command')}
def remove_recorded(cur,rec):
 import copy
 cur=copy.deepcopy(cur)
 for k,vals in (rec.get('permissions') or {}).items():
  have=cur.get('permissions',{}).get(k,[])
  for v in vals:
   while v in have:have.remove(v)
  if not have and 'permissions' in cur:cur['permissions'].pop(k,None)
 if cur.get('permissions')=={}:cur.pop('permissions',None)
 for ev,cs in (rec.get('hooks') or {}).items():
  have=cur.get('hooks',{}).get(ev,[]); cs=set(cs)
  cur['hooks'][ev]=[e for e in have if not(cmds(e)&cs)]
  if not cur['hooks'][ev]:cur['hooks'].pop(ev,None)
 if cur.get('hooks')=={}:cur.pop('hooks',None)
 return cur

def remove_block(text,b,e):
 if b not in text or e not in text:return text
 a,x=text.split(b,1);_,c=x.split(e,1)
 return (a.rstrip()+('\n\n' if a.strip() and c.strip() else '')+c.lstrip()).rstrip()+('\n' if a.strip() or c.strip() else '')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--dry-run',action='store_true');ap.add_argument('--force',action='store_true');ap.add_argument('--remove-key',action='store_true');a=ap.parse_args()
 ai_home=Path(os.path.expanduser(os.environ.get('AI_IT_HOME','~/.ai'))).resolve(); house=Path(os.path.expanduser(os.environ.get('AI_IT_HOUSE',str(ai_home/'it-role-house')))).resolve(); statep=house/'install-state.json'
 if not statep.exists(): print(f'No install state at {statep}; nothing removed.');return 0
 st=load(statep,{}); files=st.get('files',{}); modified=[]; removable=[]
 for p,h in files.items():
  actual=sha(p)
  if actual is None:continue
  (removable if actual==h else modified).append(p)
 print(f"AI IS/IT house {st.get('version','?')} uninstall: {len(removable)} owned file(s), {len(modified)} locally modified managed file(s)")
 if modified:
  print('Locally modified managed files:')
  for p in modified[:40]:print('  '+p)
  if not a.force: print('They will be preserved. Use --force to back them up and remove them too.')
 if a.dry_run: print('Dry run: nothing written.');return 0
 ts=time.strftime('%Y%m%d-%H%M%S'); backup=ai_home/'backups'/('uninstall-'+ts)
 if a.force and modified:
  for ps in modified:
   p=Path(ps); dest=backup/Path(str(p).lstrip('/\\').replace(':','_'));dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
  print(f'Backed up modified managed files to {backup}')
  removable+=modified
 for ps in removable:
  try:Path(ps).unlink()
  except FileNotFoundError:pass
 # Exact mutable additions only.
 mut=st.get('mutable',{}); ch=Path(os.path.expanduser(os.environ.get('CLAUDE_HOME','~/.claude'))).resolve(); co=Path(os.path.expanduser(os.environ.get('CODEX_HOME','~/.codex'))).resolve()
 for p,key in ((ch/'settings.json','claude_settings'),(co/'hooks.json','codex_hooks')):
  if p.exists() and mut.get(key):
   cur=load(p,{});cur=remove_recorded(cur,mut[key]);atomic(p,json.dumps(cur,indent=2,ensure_ascii=False)+'\n')
 for p,key,b,e in ((ch/'CLAUDE.md','claude_md','<!-- BEGIN ai-it-house:claude -->','<!-- END ai-it-house:claude -->'),(co/'AGENTS.md','codex_agents','<!-- BEGIN ai-it-house:codex -->','<!-- END ai-it-house:codex -->')):
  if p.exists() and mut.get(key):
   old=p.read_text(encoding='utf-8');new=remove_block(old,b,e)
   if new.strip():atomic(p,new)
   else:p.unlink()
 if a.remove_key and st.get('key_created'):
  kp=Path(st['key_created'])
  try:kp.unlink();print('Removed package-created authority key.')
  except FileNotFoundError:pass
 # State last, then prune empty package-created directories only.
 try:statep.unlink()
 except FileNotFoundError:pass
 roots=[house,ch/'skills',ch/'agents',ch/'commands',co/'skills']
 for root in roots:
  if not root.exists():continue
  for d,dirs,fs in os.walk(root,topdown=False):
   try:
    if not os.listdir(d):os.rmdir(d)
   except OSError:pass
 print('Uninstall complete. User-created/untracked files were not removed.')
 return 0
if __name__=='__main__':raise SystemExit(main())
