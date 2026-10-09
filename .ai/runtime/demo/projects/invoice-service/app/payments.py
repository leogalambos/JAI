# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Charging customers through the payment gateway."""
import random
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeout

GATEWAY_TIMEOUT_SECONDS = 0.1

_executor = ThreadPoolExecutor(max_workers=4)


class Gateway:
    """The payment gateway; in this demo it approves every charge after a network delay."""

    def authorise(self, amount):
        """Authorise a charge of amount euros and return "approved" or "declined"."""
        time.sleep(random.uniform(0.02, 0.15))
        return "approved"


def charge(amount, gateway=None):
    """Charge amount euros and return "approved" or "declined".

    Args:
        amount: the amount to charge, in euros.
        gateway: the gateway to use; a default Gateway if omitted.
    """
    gateway = gateway or Gateway()
    future = _executor.submit(gateway.authorise, amount)
    try:
        return future.result(timeout=GATEWAY_TIMEOUT_SECONDS)
    except FutureTimeout:
        return "declined"
