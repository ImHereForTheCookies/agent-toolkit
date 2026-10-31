#!/usr/bin/env python3
"""Check that the tickets in a directory form a dependency DAG (stdlib only).

CLI:  python3 scripts/check_ticket_graph.py DIR
Reads every *.md in DIR. The ticket ID is the first token after `# ` in the first
heading; `Blocked by: ID, ID` lines (comma-separated) list its blockers.
Exit 0 and print a topological order (blockers first) if valid; exit 1 and print
one problem per line on unknown references, duplicate IDs or cycles.

Library:  check_graph(tickets) -> (order, problems), tickets = {id: [blocker ids]}
          load_tickets(dir) -> (tickets, problems)
"""
import re
import sys
from pathlib import Path

_HEADING_RE = re.compile(r"^#\s+(\S+)")
_BLOCKED_RE = re.compile(r"^\s*Blocked by:\s*(.*)$", re.IGNORECASE)


def parse_ticket(text):
    """Return (ticket_id or None, [blocker ids])."""
    ticket_id = None
    blockers = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if ticket_id is None:
            m = _HEADING_RE.match(line)
            if m:
                ticket_id = m.group(1).rstrip(":")
            continue
        m = _BLOCKED_RE.match(line)
        if m:
            blockers += [b.strip() for b in m.group(1).split(",") if b.strip()]
    return ticket_id, blockers


def load_tickets(directory):
    tickets, problems = {}, []
    for path in sorted(Path(directory).glob("*.md")):
        ticket_id, blockers = parse_ticket(path.read_text(encoding="utf-8"))
        if ticket_id is None:
            problems.append(f"{path.name}: no '# <ID>' heading found")
        elif ticket_id in tickets:
            problems.append(f"{path.name}: duplicate ticket ID {ticket_id}")
        else:
            tickets[ticket_id] = blockers
    return tickets, problems


def check_graph(tickets):
    """Return (topological order, problems). Order is empty if there are problems."""
    problems = []
    for tid, blockers in tickets.items():
        for b in blockers:
            if b not in tickets:
                problems.append(f"{tid}: blocked by unknown ticket {b}")
            elif b == tid:
                problems.append(f"{tid}: blocked by itself")
    if problems:
        return [], problems

    # Kahn's algorithm; ties broken by ID for a stable order.
    remaining = {t: set(bs) for t, bs in tickets.items()}
    order = []
    while remaining:
        ready = sorted(t for t, bs in remaining.items() if not bs)
        if not ready:
            problems.append("dependency cycle among: " + ", ".join(sorted(remaining)))
            return [], problems
        order += ready
        for t in ready:
            del remaining[t]
        for bs in remaining.values():
            bs.difference_update(ready)
    return order, []


def main(argv):
    if len(argv) != 1:
        print("usage: check_ticket_graph.py DIR", file=sys.stderr)
        return 2
    if not Path(argv[0]).is_dir():
        print(f"{argv[0]}: not a directory")
        return 1
    tickets, problems = load_tickets(argv[0])
    if not tickets and not problems:
        problems.append(f"{argv[0]}: no ticket files found")
    order, graph_problems = check_graph(tickets)
    problems += graph_problems
    if problems:
        for p in problems:
            print(p)
        return 1
    print(f"{len(order)} tickets, no missing blockers, no cycles")
    print("order: " + " -> ".join(order))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
