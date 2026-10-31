#!/usr/bin/env python3
"""Lint a ticket against the testable-ticket contract (stdlib only).

CLI:  python3 scripts/lint_ticket.py FILE [FILE...]   ('-' reads stdin)
Prints one `FILE: problem` line per problem; exit 0 if valid, 1 if not.

Library:  lint(text) -> list[str] of problems (empty list means valid).
"""
import re
import sys

REQUIRED_SECTIONS = [
    "Goal",
    "Context",
    "Acceptance criteria",
    "Verify",
    "Out of scope",
    "Escalation",
]
ESCALATION_VALUES = {"none", "taste-checkpoint", "security", "irreversible"}

_ITEM_RE = re.compile(r"^\s*[-*+]\s")
_CHECK_RE = re.compile(r"checked by:\s*\S", re.IGNORECASE)


def parse_sections(text):
    """Map lowercased `## ` heading -> body text (first occurrence wins)."""
    sections = {}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower()
            if current in sections:
                current = None  # duplicate heading: ignore its body
            else:
                sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
    return {name: "\n".join(lines) for name, lines in sections.items()}


def lint(text):
    problems = []
    sections = parse_sections(text)

    for name in REQUIRED_SECTIONS:
        if name.lower() not in sections:
            problems.append(f"missing section: {name}")

    body = sections.get("acceptance criteria")
    if body is not None:
        items = [ln.strip() for ln in body.splitlines() if _ITEM_RE.match(ln)]
        if not items:
            problems.append("Acceptance criteria: no criteria items found")
        for item in items:
            if not _CHECK_RE.search(item):
                problems.append(f"acceptance criterion lacks 'checked by:': {item}")

    body = sections.get("escalation")
    if body is not None:
        first = next((ln for ln in body.splitlines() if ln.strip()), None)
        if first is None:
            problems.append("Escalation: no value given")
        else:
            value = first.replace("`", "").strip().lower()
            if value not in ESCALATION_VALUES:
                allowed = ", ".join(sorted(ESCALATION_VALUES))
                problems.append(
                    f"Escalation: invalid value {value!r} (allowed: {allowed})"
                )
    return problems


def main(argv):
    if not argv:
        print("usage: lint_ticket.py FILE [FILE...]  ('-' reads stdin)", file=sys.stderr)
        return 2
    failed = False
    for path in argv:
        try:
            text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        except OSError as exc:
            print(f"{path}: cannot read file: {exc.strerror or exc}")
            failed = True
            continue
        for problem in lint(text):
            print(f"{path}: {problem}")
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
