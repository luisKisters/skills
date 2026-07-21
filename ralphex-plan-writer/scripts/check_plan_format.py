#!/usr/bin/env python3
"""Validate common Ralphex/executr Markdown plan formatting pitfalls."""

from __future__ import annotations

import re
import sys
from pathlib import Path


TASK_RE = re.compile(r"^### (Task|Iteration) (\d+):\s+.+")
WRONG_TASK_RE = re.compile(r"^## (Task|Iteration) \d+:")
CHECKBOX_RE = re.compile(r"^\s*([-*]) \[[ xX]\]\s+")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_plan_format.py <plan.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []

    if not any(line.strip() == "## Validation Commands" for line in lines):
        errors.append("missing required '## Validation Commands' section")

    task_numbers: list[int] = []
    current_task_line: int | None = None
    task_checkbox_counts: dict[int, int] = {}

    for index, line in enumerate(lines, start=1):
        task_match = TASK_RE.match(line)
        if task_match:
            number = int(task_match.group(2))
            task_numbers.append(number)
            current_task_line = index
            task_checkbox_counts[index] = 0
            continue

        if WRONG_TASK_RE.match(line):
            errors.append(
                f"line {index}: task headings must use level 3, e.g. '### Task N:'"
            )
            current_task_line = None
            continue

        if line.startswith("### "):
            current_task_line = None

        checkbox_match = CHECKBOX_RE.match(line)
        if checkbox_match:
            bullet = checkbox_match.group(1)
            if current_task_line is None:
                errors.append(f"line {index}: checkbox appears outside a task section")
            else:
                task_checkbox_counts[current_task_line] += 1
            if bullet != "-":
                errors.append(f"line {index}: use '- [ ]', not '* [ ]'")

    if not task_numbers:
        errors.append("no executable task sections found")
    else:
        expected = list(range(1, len(task_numbers) + 1))
        if task_numbers != expected:
            errors.append(
                f"task numbers should be sequential from 1; found {task_numbers}"
            )

    for task_line, count in task_checkbox_counts.items():
        if count == 0:
            errors.append(f"line {task_line}: task section has no checkboxes")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"ok: {path} looks Ralphex-compatible")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
