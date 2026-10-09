# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
from app import payments


def test_gateway_approves_a_charge():
    assert payments.Gateway().authorise(25) == "approved"


def test_charge_is_approved():
    assert payments.charge(25) == "approved"
