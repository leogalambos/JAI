# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""SQLite storage for invoices."""
import sqlite3

from app.config import DATABASE_PATH


def connect():
    return sqlite3.connect(DATABASE_PATH)


def save(invoice_id, customer, amount):
    with connect() as db:
        db.execute("INSERT INTO invoices VALUES (?, ?, ?)", (invoice_id, customer, amount))


def find_by_customer(customer):
    with connect() as db:
        query = "SELECT id, customer, amount FROM invoices WHERE customer = '%s'" % customer
        return db.execute(query).fetchall()


def get(invoice_id):
    with connect() as db:
        return db.execute("SELECT id, customer, amount FROM invoices WHERE id = ?", (invoice_id,)).fetchone()


def delete(invoice_id):
    with connect() as db:
        db.execute("DELETE FROM invoices WHERE id = ?", (invoice_id,))
