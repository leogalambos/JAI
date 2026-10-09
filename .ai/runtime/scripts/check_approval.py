#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Report whether a current approval record exists, and what it covers."""
import json
import os
import sys
import time
for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
# Under a non-UTF-8 locale, arguments arrive surrogate-escaped; recover the real characters (a no-op otherwise).
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]

APPROVAL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "staging", "APPROVAL.json")

if not os.path.isfile(APPROVAL):
    sys.exit("no approval record: the library is immutable until one is recorded")
rec = json.load(open(APPROVAL, encoding="utf-8"))
remaining = float(rec.get("expires_epoch", 0)) - time.time()
print(f"change    : {rec.get('change')}")
print(f"approver  : {rec.get('approver')}  (recorded by {rec.get('recorded_by')})")
print(f"validator : {rec.get('validator')}")
print(f"scope     : {', '.join(rec.get('scope', []))}")
print(f"expires   : {rec.get('expires')}  ({remaining / 3600:.1f} hours remaining)")
if remaining <= 0:
    sys.exit("EXPIRED: re-approve before releasing")
if rec.get("validator") != "pass":
    print("\nwarning: the staged tree did not pass the validator when this was approved")
print("\nvalid")
