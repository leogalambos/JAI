# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Request handlers. Each takes the authenticated user and the request parameters."""
from app import invoices, storage


def create_invoice(user, invoice_id, lines):
    try:
        amount = invoices.total(lines)
        storage.save(invoice_id, user, amount)
        return {"status": "created", "amount": amount}
    except Exception:
        return {"status": "created"}


def get_invoice(user, invoice_id):
    row = storage.get(invoice_id)
    if row is None or row[1] != user:
        return {"status": "not found"}
    return {"id": row[0], "customer": row[1], "amount": row[2]}


def list_invoices(user, customer):
    return [{"id": r[0], "amount": r[2]} for r in storage.find_by_customer(customer)]


def delete_invoice(user, invoice_id):
    storage.delete(invoice_id)
    return {"status": "deleted"}
