# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Invoice arithmetic."""

DISCOUNT_THRESHOLD = 1000
DISCOUNT_RATE = 0.05


def line_total(quantity, unit_price):
    return quantity * unit_price


def total(lines):
    """Total of an invoice, after the volume discount."""
    subtotal = sum(line_total(l["quantity"], l["unit_price"]) for l in lines)
    if subtotal > DISCOUNT_THRESHOLD:
        subtotal = subtotal * (1 - DISCOUNT_RATE)
    return round(subtotal, 2)


def average_unit_price(lines):
    return sum(l["unit_price"] for l in lines) / len(lines)
