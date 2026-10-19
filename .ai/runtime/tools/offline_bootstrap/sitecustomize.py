# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Activate Python audits only in explicitly guarded qualification processes."""
import os

if os.environ.get('JAI_OFFLINE_GUARD_ACTIVE') == '1':
    from offline_guard import install_python_audit
    install_python_audit()
