# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
from app import invoices


def test_total_without_discount():
    assert invoices.total([{"quantity": 2, "unit_price": 10.0}]) == 20.0


def test_total_with_discount():
    assert invoices.total([{"quantity": 30, "unit_price": 50.0}]) == 1425.0
