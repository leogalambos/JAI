#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Opt-in commercial-economics/1 calculators; outputs are advice, never authority.

All quantities use decimal strings. Records retain input versions and calculation
policy; accounting recognition, tax policy and contractual decisions remain with
human owners. No network or project master data is accessed by this module.
"""
from __future__ import annotations

import argparse
import copy
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN, localcontext
import json
from pathlib import Path

FORMULA = "commercial-economics/1"
ZERO = Decimal("0")
ONE = Decimal("1")


def _decimal(value, name, minimum=ZERO, maximum=None):
    if not isinstance(value, (str, Decimal)):
        raise ValueError(f"{name}: decimal string required")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{name}: invalid decimal") from exc
    if not result.is_finite() or (minimum is not None and result < minimum):
        raise ValueError(f"{name}: finite value >= {minimum} required")
    if maximum is not None and result > maximum:
        raise ValueError(f"{name}: value > {maximum}")
    return result


def _required(record, fields):
    for field in fields:
        if field not in record or record[field] is None or record[field] == "":
            raise ValueError(f"{field}: required")


def _result(operation, inputs, **values):
    def encode(value):
        if isinstance(value, Decimal):
            return str(value)
        if isinstance(value, dict):
            return {key: encode(item) for key, item in value.items()}
        if isinstance(value, list):
            return [encode(item) for item in value]
        return value
    return encode({"formula_version": FORMULA, "operation": operation,
                   "inputs": copy.deepcopy(inputs), **values})


def validate_estimate(record):
    """Validate estimate state/provenance and return fixed-price gate blockers.

    Args:
        record: Estimate mapping with state, unit, owner, method, gate deadline,
            input_versions and (for numeric states) interval and provenance.
    Returns:
        Copy of the validated estimate and explicit blockers, never a probability.
    Raises:
        ValueError: Unknown states, unsupported quantiles or invalid intervals.
    """
    _required(record, ["id", "state", "unit", "owner", "method", "gate_deadline", "input_versions", "as_of"])
    states = {"missing", "requested", "declined", "provisional", "supported", "conflicting", "obsolete"}
    if record["state"] not in states:
        raise ValueError("unknown estimate state")
    date.fromisoformat(record["gate_deadline"])
    blockers = []
    numeric = record["state"] in {"provisional", "supported", "conflicting", "obsolete"}
    if numeric:
        _required(record, ["interval", "source_ids", "passage_ids", "applicability", "assumptions", "valid_until", "input_role"])
        if record["input_role"] not in {"client", "supplier", "expert", "public_benchmark", "history"}:
            raise ValueError("unknown estimate input_role")
        interval = record["interval"]
        low, high = (_decimal(interval[key], key) for key in ("low", "high"))
        if low > high:
            raise ValueError("inverted estimate interval")
        date.fromisoformat(record["valid_until"])
        if not record["source_ids"] or not record["passage_ids"] or not record["applicability"]:
            raise ValueError("numeric estimate requires supporting passages and applicability")
        if record["state"] == "conflicting" and len(record.get("alternatives", [])) < 2:
            raise ValueError("conflicting estimate must retain both alternatives")
    elif "interval" in record:
        raise ValueError("missing/requested/declined estimate cannot invent values")
    if "quantile" in record:
        calibration = record.get("calibration", {})
        _required(calibration, ["distribution", "sample_size", "sample_provenance", "correlation_model", "model_version", "seed", "independent_review_id"])
        if not isinstance(calibration["sample_size"], int) or isinstance(calibration["sample_size"], bool) or calibration["sample_size"] < 2:
            raise ValueError("quantile requires calibration sample")
        _decimal(record["quantile"], "quantile", ZERO, ONE)
    if record["state"] != "supported":
        blockers.append("estimate_not_supported")
    if record.get("as_of") and numeric and date.fromisoformat(record["as_of"]) > date.fromisoformat(record["valid_until"]):
        blockers.append("estimate_expired")
    return _result("estimate", record, blockers=blockers, fixed_price_eligible=not blockers)


def learning_update(record):
    """Create an immutable stage-learning forecast without rewriting baseline.

    Args:
        record: Baseline reference, old forecast, actual and next estimate records,
            stage acceptance evidence, learning cost and decision gate.
    Returns:
        New forecast proposal and risk-treatment alternatives; human gate remains.
    Raises:
        ValueError: Missing measured/accepted stage data or unchanged forecast ID.
    """
    _required(record, ["baseline_id", "previous_forecast_id", "forecast_id", "stage_acceptance_id", "actual_id", "actual_effort", "next_estimate", "decision_gate", "learning_cost"])
    if record["forecast_id"] == record["previous_forecast_id"]:
        raise ValueError("learning requires a new forecast identity")
    _decimal(record["actual_effort"], "actual_effort")
    _decimal(record["learning_cost"], "learning_cost")
    estimate = validate_estimate(record["next_estimate"])
    alternatives = [
        {"mechanism": "paid_discovery_or_pilot", "effect": "uncertainty_reduction", "gate": record["decision_gate"]},
        {"mechanism": "capped_time_and_materials", "effect": "exposure_limit", "gate": record["decision_gate"]},
        {"mechanism": "unit_price_bands", "effect": "volume_risk_allocation", "gate": record["decision_gate"]},
        {"mechanism": "target_cost_pain_gain", "effect": "contractual_risk_sharing", "gate": record["decision_gate"]},
        {"mechanism": "verified_scope_fixed_price_with_continuation_option", "effect": "bounded_commitment", "gate": record["decision_gate"]}]
    return _result("learning", record, baseline_id=record["baseline_id"], next_estimate=estimate,
                   alternatives=alternatives, human_required=True, automatic_continuation=False)


def capacity_plan(record):
    """Check shared resource capacity for exact calendar buckets and role pyramid.

    Args:
        record: Pools with unique pool_id/period, calendar hours and deductions;
            allocations include engagement, role, seniority, sourcing and effort.
    Returns:
        Available/allocated hours by shared pool and conflicts across engagements.
    Raises:
        ValueError: Missing calendar provenance, duplicate pools or double losses.
    """
    pools = {}
    for pool in record.get("pools", []):
        _required(pool, ["pool_id", "period", "calendar_source", "calendar_work_hours"])
        key = (pool["pool_id"], pool["period"])
        if key in pools:
            raise ValueError("duplicate pool/period")
        deductions = sum((_decimal(pool.get(field, "0"), field) for field in ("leave", "other_committed_hours", "non_delivery_hours")), ZERO)
        available = _decimal(pool["calendar_work_hours"], "calendar_work_hours") - deductions
        if "utilization" in pool:
            if deductions:
                raise ValueError("utilization and explicit calendar losses cannot overlap")
            available *= _decimal(pool["utilization"], "utilization", ZERO, ONE)
        if available < ZERO:
            raise ValueError("calendar deductions exceed hours")
        pools[key] = {"pool_id": key[0], "period": key[1], "available_hours": available, "allocated_hours": ZERO, "engagements": []}
    for allocation in record.get("allocations", []):
        _required(allocation, ["pool_id", "period", "engagement_id", "role", "seniority", "sourcing", "work_package_id", "effort_hours", "mix_rationale"])
        key = (allocation["pool_id"], allocation["period"])
        if key not in pools:
            raise ValueError("allocation references unknown calendar bucket")
        pools[key]["allocated_hours"] += _decimal(allocation["effort_hours"], "effort_hours")
        if allocation["engagement_id"] not in pools[key]["engagements"]:
            pools[key]["engagements"].append(allocation["engagement_id"])
    conflicts = [dict(pool) for pool in pools.values() if pool["allocated_hours"] > pool["available_hours"]]
    return _result("capacity", record, pools=list(pools.values()), conflicts=conflicts,
                   feasible=not conflicts, duration_proven=False, human_required=bool(conflicts))


def service_sizing(record):
    """Calculate bucket-specific roster minima, never response-time SLA proof.

    Args:
        record: Interchangeable skill/time/region buckets with workload classes,
            coverage, utilization, shrinkage, cost rate and optional roster hours.
    Returns:
        Paid hours/cost minima and peak/coverage blockers for each bucket.
    Raises:
        ValueError: Non-interchangeable pooled work or overlapping loss/cost drivers.
    """
    rows, blockers = [], []
    seen = set()
    for bucket in record.get("buckets", []):
        _required(bucket, ["id", "period", "skill_pool", "region", "interchangeable", "utilization_limit", "shrinkage", "service_window_hours", "concurrent_seats", "cost_rate", "currency"])
        if bucket["id"] in seen:
            raise ValueError("duplicate service bucket")
        seen.add(bucket["id"])
        if bucket["interchangeable"] is not True:
            raise ValueError("split non-interchangeable workers into separate buckets")
        if bucket.get("calendar_losses_already_deducted") or bucket.get("workload_labour_cost"):
            raise ValueError("double counted shrinkage/workload cost")
        utilization = _decimal(bucket["utilization_limit"], "utilization_limit", ZERO, ONE)
        shrinkage = _decimal(bucket["shrinkage"], "shrinkage", ZERO, ONE)
        if not utilization or shrinkage == ONE:
            raise ValueError("utilization > 0 and shrinkage < 1 required")
        workload = sum((_decimal(item["volume"], "volume") * _decimal(item["handle_hours"], "handle_hours") for item in bucket.get("classes", [])), ZERO) + _decimal(bucket.get("planned_service_hours", "0"), "planned_service_hours")
        coverage = _decimal(bucket["concurrent_seats"], "concurrent_seats") * _decimal(bucket["service_window_hours"], "service_window_hours")
        available = max(workload / utilization, coverage)
        paid = available / (ONE - shrinkage)
        if "roster_paid_hours" not in bucket:
            blockers.append({"bucket": bucket["id"], "reason": "roster_not_verified"})
        elif _decimal(bucket["roster_paid_hours"], "roster_paid_hours") < paid:
            blockers.append({"bucket": bucket["id"], "reason": "insufficient_roster"})
        if bucket.get("on_call_only") and coverage:
            blockers.append({"bucket": bucket["id"], "reason": "on_call_is_not_active_coverage"})
        rows.append({"id": bucket["id"], "workload_hours": workload, "coverage_seat_hours": coverage,
                     "required_available_hours": available, "paid_roster_hours": paid,
                     "roster_cost": paid * _decimal(bucket["cost_rate"], "cost_rate"), "currency": bucket["currency"]})
    return _result("service", record, buckets=rows, blockers=blockers, sla_proven=False,
                   roster_proven=False, human_required=True)


def price_quote(record):
    """Price one currency using separate cost, reserve and invoice-line waterfalls.

    Args:
        record: Currency, input_versions, validity, author/reviewer references,
            labour cost lines, explicit costs/reserves and list-price invoice lines.
    Returns:
        Decimal-string costs, required revenue, net price, profit, margin/markup.
    Raises:
        ValueError: Floats/nonfinite inputs, double counted costs, invalid discounts.
    """
    _required(record, ["currency", "input_versions", "valid_until", "author", "reviewer", "target_margin"])
    date.fromisoformat(record["valid_until"])
    if record["author"] == record["reviewer"]:
        raise ValueError("pricing author and reviewer references must differ; authenticate externally")
    quantum = _decimal(record.get("rounding_quantum", "0.01"), "rounding_quantum")
    if quantum <= ZERO or quantum.normalize().as_tuple().digits != (1,):
        raise ValueError("rounding_quantum must be a positive power of ten")
    labour = ZERO
    loaded = set()
    for line in record.get("labour", []):
        if line.get("currency", record["currency"]) != record["currency"]:
            raise ValueError("mixed currencies require explicit FX conversion first")
        if line.get("sourcing") == "subcontract" and line.get("purchase_price_includes_effort"):
            raise ValueError("subcontract purchase cost cannot duplicate labour")
        loaded.update(line.get("loaded_components", []))
        labour += _decimal(line["effort_hours"], "effort_hours") * _decimal(line["cost_rate"], "cost_rate")
    overhead = _decimal(record.get("explicit_overhead", "0"), "explicit_overhead")
    if overhead and "overhead" in loaded:
        raise ValueError("explicit overhead duplicates loaded cost rate")
    base = labour + _decimal(record.get("non_labour", "0"), "non_labour") + overhead
    reserve_ids, contingency, management = set(), ZERO, ZERO
    for reserve in record.get("reserves", []):
        _required(reserve, ["risk_id", "kind", "amount", "decision_ref"])
        if reserve["risk_id"] in reserve_ids:
            raise ValueError("duplicate full risk allocation")
        reserve_ids.add(reserve["risk_id"])
        amount = _decimal(reserve["amount"], "reserve")
        if reserve["kind"] == "contingency":
            contingency += amount
        elif reserve["kind"] == "management":
            management += amount
        else:
            raise ValueError("unknown reserve kind")
    risk_cost = base + contingency
    scenario_cost = risk_cost + (management if record.get("include_management_scenario") else ZERO)
    target = _decimal(record["target_margin"], "target_margin", ZERO, ONE)
    if target == ONE:
        raise ValueError("target_margin must be < 1")
    lines = []
    for line in record.get("invoice_lines", []):
        listed = _decimal(line["billable_hours"], "billable_hours") * _decimal(line["sell_rate"], "sell_rate") if "billable_hours" in line else _decimal(line["list_price"], "list_price")
        volume = _decimal(line.get("volume_discount", "0"), "volume_discount", ZERO, ONE)
        strategic = _decimal(line.get("strategic_discount", "0"), "strategic_discount", ZERO, ONE)
        net = listed * (ONE - volume) * (ONE - strategic) - _decimal(line.get("fixed_rebate", "0"), "fixed_rebate")
        if net < ZERO:
            raise ValueError("negative line requires separate credit-note profile")
        lines.append(net.quantize(quantum, rounding=ROUND_HALF_EVEN))
    net_price = sum(lines, ZERO)
    profit = net_price - scenario_cost
    with localcontext() as context:
        context.prec = 40
        required = scenario_cost / (ONE - target)
        margin = profit / net_price if net_price else None
        markup = profit / scenario_cost if scenario_cost else None
    bid = _decimal(record.get("sunk_bid_cost", "0"), "sunk_bid_cost")
    return _result("price", record, currency=record["currency"], rounding="ROUND_HALF_EVEN/invoice-line",
                   direct_labour_cost=labour, base_cost=base, contingency=contingency,
                   management_reserve=management, risk_adjusted_cost=risk_cost,
                   scenario_cost=scenario_cost, required_net_revenue=required,
                   invoice_line_totals=lines, net_price=net_price, gross_profit=profit,
                   margin=margin, markup=markup, lifetime_profit_after_sunk_bid=profit-bid,
                   margin_target_met=net_price >= required, authorisation_granted=False)


def classify_quantity(record):
    """Allocate one quantity across a single reporting dimension with exact weights.

    Args:
        record: Quantity, unit, period, source_id, dimension, basis and allocations.
    Returns:
        Reconciled targets preserving source classification and original quantity.
    Raises:
        ValueError: Missing units/provenance or weights not summing exactly to one.
    """
    _required(record, ["quantity", "unit", "period", "source_id", "dimension", "allocation_basis", "allocations"])
    quantity = _decimal(record["quantity"], "quantity")
    weights = [_decimal(item["weight"], "weight", ZERO, ONE) for item in record["allocations"]]
    if sum(weights, ZERO) != ONE:
        raise ValueError("allocation weights must sum exactly to one")
    if len({item["target"] for item in record["allocations"]}) != len(weights):
        raise ValueError("duplicate allocation target")
    return _result("allocation", record, targets=[{"target": item["target"], "quantity": quantity * weight,
                   "unit": record["unit"]} for item, weight in zip(record["allocations"], weights)], reconciled=True)


def map_classification(record):
    """Preserve source taxonomy and expose ambiguous/lossy/unmapped mapping.

    Args:
        record: Source/target dimensions, rule_id/version, state and evidence.
    Returns:
        A separate reporting projection, never a rewritten source classification.
    Raises:
        ValueError: Invented CTB-to-Grow/Transform certainty or absent mapping reason.
    """
    _required(record, ["source_dimension", "target_dimension", "source_value", "rule_id", "rule_version", "state", "reason", "quantity", "unit"])
    _decimal(record["quantity"], "quantity")
    state = record["state"]
    if state not in {"exact", "unmapped", "ambiguous", "lossy"}:
        raise ValueError("unknown taxonomy mapping state")
    if state == "exact":
        _required(record, ["target_value", "evidence_ids"])
        if not record["evidence_ids"]:
            raise ValueError("exact mapping needs evidence")
    if record["source_value"] == "CTB" and record.get("target_value") in {"Grow", "Transform"} and not record.get("disambiguating_evidence_ids"):
        if state == "exact":
            raise ValueError("CTB does not distinguish Grow from Transform")
    if state == "lossy":
        _required(record, ["lost_distinctions"])
    return _result("taxonomy", record, source_preserved=True,
                   unmapped_quantity=record["quantity"] if state in {"unmapped", "ambiguous"} else "0")


def forecast(record):
    """Compute EAC/VAC with paired accrual reversals and separate cash accounting.

    Args:
        record: Baseline/forecast IDs, currency, approved_budget, ETC, actuals,
            accruals and explicit reversal amounts referencing existing accrual IDs.
    Returns:
        To-date incurred cost, unreversed accrual, EAC and VAC; baseline unchanged.
    Raises:
        ValueError: Unknown/duplicate entries, over-reversals or currency mismatch.
    """
    _required(record, ["baseline_id", "forecast_id", "currency", "approved_budget", "etc"])
    ids, actual_total, accruals = set(), ZERO, {}
    for kind in ("actuals", "accruals"):
        for item in record.get(kind, []):
            _required(item, ["id", "amount", "currency", "period", "evidence_id"])
            if item["id"] in ids:
                raise ValueError("duplicate accounting entry")
            ids.add(item["id"])
            if item["currency"] != record["currency"]:
                raise ValueError("accounting currency mismatch")
            amount = _decimal(item["amount"], "amount")
            if kind == "actuals":
                actual_total += amount
            else:
                accruals[item["id"]] = amount
    reversal_ids = set()
    invoice_reversed = {}
    actual_amounts = {entry["id"]: _decimal(entry["amount"], "actual amount") for entry in record.get("actuals", [])}
    for reversal in record.get("reversals", []):
        _required(reversal, ["id", "accrual_id", "actual_id", "amount"])
        if reversal["id"] in reversal_ids:
            raise ValueError("duplicate reversal")
        reversal_ids.add(reversal["id"])
        if reversal["accrual_id"] not in accruals or reversal["actual_id"] not in {entry["id"] for entry in record.get("actuals", [])}:
            raise ValueError("reversal must pair existing accrual and actual invoice")
        reversed_amount = _decimal(reversal["amount"], "reversal amount")
        invoice_id = reversal["actual_id"]
        invoice_reversed[invoice_id] = invoice_reversed.get(invoice_id, ZERO) + reversed_amount
        if invoice_reversed[invoice_id] > actual_amounts[invoice_id]:
            raise ValueError("aggregate reversal exceeds actual invoice amount")
        accruals[reversal["accrual_id"]] -= reversed_amount
        if accruals[reversal["accrual_id"]] < ZERO:
            raise ValueError("accrual over-reversal")
    remaining = sum(accruals.values(), ZERO)
    to_date = actual_total + remaining
    eac = to_date + _decimal(record["etc"], "etc")
    return _result("forecast", record, actual_cost=actual_total, unreversed_accruals=remaining,
                   cost_to_date=to_date, eac=eac, vac=_decimal(record["approved_budget"], "approved_budget")-eac,
                   baseline_id=record["baseline_id"], baseline_unchanged=True)


def cashflow(record):
    """Compute dated cash projection with explicit directional FX and payment delay.

    Args:
        record: Base currency, opening_cash and events with amount, currency,
            expected_date, direction; foreign events require dated FX provenance.
    Returns:
        Cash balances/financing minimum independent from accounting profit.
    Raises:
        ValueError: Missing FX policy/source, invalid dates or cash direction.
    """
    _required(record, ["currency", "opening_cash"])
    balance = _decimal(record["opening_cash"], "opening_cash", None)
    minimum, rows = balance, []
    for item in sorted(record.get("events", []), key=lambda event: (event["expected_date"], event["id"])):
        _required(item, ["id", "amount", "currency", "expected_date", "direction", "invoice_ref"])
        date.fromisoformat(item["expected_date"])
        amount = _decimal(item["amount"], "amount")
        if item["currency"] != record["currency"]:
            fx = item.get("fx", {})
            _required(fx, ["rate", "source", "as_of", "from_currency", "to_currency", "risk_owner", "rounding_policy"])
            if (fx["from_currency"], fx["to_currency"]) != (item["currency"], record["currency"]):
                raise ValueError("FX direction mismatch")
            date.fromisoformat(fx["as_of"])
            rate = _decimal(fx["rate"], "fx.rate")
            if not rate:
                raise ValueError("FX rate must be positive")
            amount *= rate
        if item["direction"] not in {"in", "out"}:
            raise ValueError("cash direction must be in/out")
        balance += amount if item["direction"] == "in" else -amount
        minimum = min(minimum, balance)
        rows.append({"id": item["id"], "date": item["expected_date"], "balance": balance})
    return _result("cashflow", record, events=rows, closing_cash=balance,
                   financing_required=max(-minimum, ZERO), profit_inferred=False)


_TERM_FIELDS = ("scope_exclusions", "acceptance", "sla_credits_cap", "dependencies", "change_control", "fx", "tax_jurisdiction", "indexation_validity", "payment", "liability", "warranty", "ip_licences_data", "privacy_residency_retention", "subcontract_flowdown", "continuity_exit")


def validate_terms(record):
    """Block binding commercial terms with unknown/unreviewed material conditions.

    Args:
        record: Terms keyed by required category, each with owner/deadline/state,
            and a human legal/commercial review reference for agreed or N/A terms.
    Returns:
        Per-category blockers; tax, liability and SLA are never inferred.
    Raises:
        ValueError: Invalid term states, deadlines or missing accountability.
    """
    blockers = []
    for field in _TERM_FIELDS:
        item = record.get(field)
        if item is None:
            blockers.append(field + ":missing")
            continue
        _required(item, ["owner", "deadline", "state"])
        date.fromisoformat(item["deadline"])
        if item["state"] not in {"unknown", "proposed", "agreed", "not_applicable"}:
            raise ValueError("unknown contractual term state")
        if item["state"] in {"agreed", "not_applicable"}:
            if not item.get("human_review_ref") or not item.get("reason"):
                blockers.append(field + ":human_review_required")
        else:
            blockers.append(field + ":unresolved")
    return _result("terms", record, blockers=blockers, binding_gate_ready=not blockers,
                   contractual_authorisation=False)


def uncertainty_analysis(record):
    """Evaluate explicit stress scenarios and historical error/interval coverage.

    Args:
        record: Named scenarios with common driver groups, cost/revenue; optional
            comparable historical forecasts including failed engagements.
    Returns:
        Scenario margins/break-even, calibration bias/error/coverage, no quantiles.
    Raises:
        ValueError: Claimed percentile without model or inconsistent driver groups.
    """
    if "quantiles" in record or "monte_carlo" in record:
        raise ValueError("this deterministic scenario engine does not produce calibrated quantiles")
    scenarios = []
    names = set()
    for scenario in record.get("scenarios", []):
        _required(scenario, ["name", "drivers", "correlation_groups", "cost", "revenue"])
        if scenario["name"] in names:
            raise ValueError("duplicate scenario name")
        names.add(scenario["name"])
        covered = [driver for group in scenario["correlation_groups"] for driver in group]
        if set(covered) != set(scenario["drivers"]) or len(covered) != len(set(covered)):
            raise ValueError("each driver needs exactly one explicit correlation group")
        cost, revenue = _decimal(scenario["cost"], "cost"), _decimal(scenario["revenue"], "revenue")
        scenarios.append({"name": scenario["name"], "profit": revenue-cost,
                          "margin": (revenue-cost)/revenue if revenue else None, "break_even_revenue": cost})
    errors, coverage = [], []
    for history in record.get("history", []):
        _required(history, ["forecast", "actual", "low", "high", "comparability", "source_id", "outcome"])
        estimated, actual = _decimal(history["forecast"], "forecast"), _decimal(history["actual"], "actual")
        low, high = _decimal(history["low"], "low"), _decimal(history["high"], "high")
        if low > high:
            raise ValueError("history interval inverted")
        errors.append(estimated-actual)
        coverage.append(low <= actual <= high)
    count = Decimal(len(errors))
    return _result("uncertainty", record, scenarios=scenarios, sample_size=len(errors),
                   directional_bias=sum(errors, ZERO)/count if count else None,
                   mean_absolute_error=sum((abs(error) for error in errors), ZERO)/count if count else None,
                   interval_coverage=Decimal(sum(coverage))/count if count else None,
                   selection_bias_review_required=True, calibrated_quantiles=False)


def monitor(record):
    """Emit deviations and block automatic commitments at owner-defined thresholds.

    Args:
        record: Metrics, threshold owner/reference, baseline/previous forecast IDs,
            current EAC/budget/margin/cash/capacity/acceptance/SLA and deadline.
    Returns:
        Alerts and human decision requirements, never automatic stop-loss or notice.
    Raises:
        ValueError: Missing human threshold provenance or nonfinite metrics.
    """
    _required(record, ["baseline_id", "previous_forecast_id", "threshold_owner", "threshold_decision_ref", "owner", "deadline", "thresholds", "metrics"])
    date.fromisoformat(record["deadline"])
    metrics, thresholds, alerts = record["metrics"], record["thresholds"], []
    rules = {"eac": "maximum", "margin": "minimum", "overdue_days": "maximum", "capacity_shortfall_hours": "maximum", "acceptance_failures": "maximum", "sla_breaches": "maximum"}
    for metric, direction in rules.items():
        if metric not in thresholds:
            raise ValueError(f"missing human threshold: {metric}")
        value = _decimal(metrics[metric], metric, None)
        threshold = _decimal(thresholds[metric], metric + " threshold", None)
        exceeded = value > threshold if direction == "maximum" else value < threshold
        if exceeded:
            alerts.append({"metric": metric, "value": value, "threshold": threshold, "owner": record["owner"], "deadline": record["deadline"], "cause": record.get("causes", {}).get(metric, "requires_investigation")})
    return _result("monitor", record, deviations=alerts, block_automatic_commitment=bool(alerts),
                   human_required=bool(alerts), stop_loss_decided=False, client_notice_authorised=False)


_OPERATIONS = {"estimate": validate_estimate, "learning": learning_update, "capacity": capacity_plan,
               "service": service_sizing, "price": price_quote, "allocation": classify_quantity,
               "taxonomy": map_classification, "forecast": forecast, "cashflow": cashflow,
               "terms": validate_terms, "uncertainty": uncertainty_analysis, "monitor": monitor}


def main(argv=None):
    """Run one calculator against JSON input, printing JSON advice to stdout.

    Args:
        argv: Optional argument list; defaults to process arguments.
    Returns:
        Zero on success, two on invalid JSON/calculation input.
    Raises:
        SystemExit: argparse usage or help request.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=sorted(_OPERATIONS))
    parser.add_argument("input", type=Path)
    args = parser.parse_args(argv)
    try:
        result = _OPERATIONS[args.operation](json.loads(args.input.read_text()))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError, InvalidOperation) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
