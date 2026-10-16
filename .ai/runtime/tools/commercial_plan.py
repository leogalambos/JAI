#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Validate the documented JAI task DAG using only the Python standard library.

Inputs are a marked Markdown plan or a raw JSON fixture. The checker performs
no writes or external calls. Exit 0 reports deterministic topological order;
exit 2 reports an invalid input. Semantic review remains an independent duty.
"""
import argparse
import heapq
import json
import re
import sys
from pathlib import Path


def _reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def load_plan(path, fixture=False):
    """Read UTF-8 JSON from a fixture or exactly one marked Markdown block.

    Args:
        path: Path to the readable input file.
        fixture: Whether the complete file is raw JSON.
    Returns:
        The parsed JSON value, subsequently checked by validate_plan.
    Raises:
        OSError: The file cannot be read.
        ValueError: Markers, encoding or JSON are invalid or duplicated.
    """
    raw = Path(path).read_text(encoding="utf-8")
    if not fixture:
        begin = "<!-- " + "JAI_PLAN_BEGIN" + " -->"
        end = "<!-- " + "JAI_PLAN_END" + " -->"
        _require(raw.count(begin) == 1 and raw.count(end) == 1,
                 "expected exactly one plan marker pair")
        start = raw.index(begin) + len(begin)
        stop = raw.index(end)
        _require(start < stop, "reversed plan markers")
        match = re.fullmatch(r"\s*```json\r?\n(.*?)\r?\n```\s*",
                             raw[start:stop], flags=re.DOTALL)
        _require(match is not None, "expected one JSON fence inside markers")
        raw = match.group(1)
    return json.loads(raw, object_pairs_hook=_reject_duplicates)


def validate_plan(plan):
    """Validate schema, task references, coverage, role separation and DAG.

    Args:
        plan: Parsed JSON object with schema_version 1.0 and 15 to 25 tasks.
    Returns:
        A deterministic lexicographically selected topological list of IDs.
    Raises:
        ValueError: A required field, reference, role separation, coverage
            invariant or acyclicity constraint is violated.
    """
    _require(isinstance(plan, dict), "plan must be an object")
    _require(plan.get("schema_version") == "1.0", "unsupported schema_version")
    tasks = plan.get("tasks")
    _require(isinstance(tasks, list) and 15 <= len(tasks) <= 25,
             "tasks must contain 15 to 25 entries")
    expected = {f"REQ-{i:02d}" for i in range(1, 23)} | {
        f"GAP-{i:02d}" for i in range(1, 8)}
    by_id = {}
    covered = set()
    for task in tasks:
        _require(isinstance(task, dict), "task must be an object")
        for field in ("id", "title", "accountable_owner", "producer", "reviewer"):
            value = task.get(field)
            _require(isinstance(value, str) and bool(value.strip()),
                     "missing or empty task field: " + field)
            _require(value == value.strip(), "surrounding whitespace: " + field)
        task_id = task["id"]
        _require(re.fullmatch(r"T[0-9]{2}(?:[.]v[1-9][0-9]*)?", task_id)
                 is not None, "invalid task ID: " + task_id)
        _require(task_id not in by_id, "duplicate ID: " + task_id)
        _require(task["producer"].casefold() != task["reviewer"].casefold(),
                 "producer equals reviewer: " + task_id)
        for field in ("depends_on", "outputs", "acceptance", "coverage"):
            value = task.get(field)
            _require(isinstance(value, list), "expected array: " + field)
            _require(field == "depends_on" or bool(value), "empty array: " + field)
            _require(all(isinstance(item, str) and bool(item.strip()) and
                         item == item.strip() for item in value),
                     "invalid array entry: " + field)
            _require(len(value) == len(set(value)), "duplicate entry: " + field)
        _require(set(task["coverage"]) <= expected, "unknown coverage ID")
        covered.update(task["coverage"])
        by_id[task_id] = task
    _require(covered == expected, "missing coverage: " + ", ".join(sorted(expected-covered)))
    outgoing = {task_id: [] for task_id in by_id}
    indegree = {task_id: 0 for task_id in by_id}
    for task_id, task in by_id.items():
        for dependency in task["depends_on"]:
            _require(dependency in by_id, "dangling dependency: " + dependency)
            _require(dependency != task_id, "self dependency: " + task_id)
            outgoing[dependency].append(task_id)
            indegree[task_id] += 1
    ready = [task_id for task_id, count in indegree.items() if count == 0]
    heapq.heapify(ready)
    ordered = []
    while ready:
        task_id = heapq.heappop(ready)
        ordered.append(task_id)
        for child in sorted(outgoing[task_id]):
            indegree[child] -= 1
            if indegree[child] == 0:
                heapq.heappush(ready, child)
    _require(len(ordered) == len(tasks), "dependency cycle detected")
    return ordered


def main(argv=None):
    """Run the read-only CLI and return 0 on success or 2 on invalid input.

    Args:
        argv: Optional sequence of command-line arguments; None uses sys.argv.
    Returns:
        Integer exit status. Diagnostics go to stderr; order goes to stdout.
    Raises:
        SystemExit: argparse handles malformed CLI options and help requests.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Markdown plan or raw JSON fixture")
    parser.add_argument("--fixture", action="store_true", help="read raw JSON")
    args = parser.parse_args(argv)
    try:
        order = validate_plan(load_plan(args.path, args.fixture))
    except (OSError, ValueError) as error:
        print("INVALID: " + str(error), file=sys.stderr)
        return 2
    print("VALID: " + " ".join(order))
    return 0


if __name__ == "__main__":
    sys.exit(main())
