# PROGRESS

Append-only log of work sessions. Add new entries at the bottom; do not edit old ones.

## 2026-10-17 - ROB-5: Scaffold the marketplace repo
- Ticket: ROB-5
- Outcome: repo is a valid Claude Code marketplace listing four plugins (agentic-workflow, code-navigation, linear-workflow, project-template); `make verify` and `make smoke` added; CI runs `make verify` on push and PR.
- Next step: fill in plugin contents (skills, agents, hooks) and the full README in later tickets.

## 2026-10-17 - ROB-6: Ticket linter script
- Ticket: ROB-6
- Outcome: `scripts/lint_ticket.py` (stdlib) rejects tickets lacking the testable-ticket contract (six required `##` sections, `checked by:` on every acceptance criterion, escalation in none/taste-checkpoint/security/irreversible); exposes `lint(text)` and a CLI (files or `-`, exit 1 on problems). Tests in `tests/test_lint_ticket.py`; `make verify` gains step 4, which lints every `*.md` under any `tickets/` directory (skips when none).
- Next step: add real tickets under `tickets/` (or wire the linter into the Linear ticket-creation flow) so the verify step has something to check.

## 2026-10-17 - ROB-7: Fixture project for testing the toolkit
- Ticket: ROB-7
- Outcome: `fixtures/demo-project/` (FastAPI + SQLite pantry API, 15 pytest tests, `make dev|test|e2e|verify`, e2e smoke over HTTP on a free port) with three sample tickets DEMO-1..3 in contract format (DEMO-3 is contradictory on purpose, to exercise escalation). `fixtures/seeded-bug.patch` removes the negative-quantity check in PATCH; `scripts/check_seeded_bug.sh` asserts exactly `test_quantity_cannot_go_negative` fails. `make verify` gains step 5 (fixture verify) and step 6 (seeded bug); step 4 lints the fixture tickets automatically.
- Next step: use the fixture in end-to-end tests of the workflow skills/agents (implement DEMO-1/2, confirm DEMO-3 escalates).

## 2026-10-17 - ROB-8: decompose-project and ticket-spec skills
- Ticket: ROB-8
- Outcome: `plugins/agentic-workflow/skills/ticket-spec` (contract, sizing, testable criteria, linter gate; good/bad examples in `references/examples.md`) and `skills/decompose-project` (goal -> milestones -> tickets -> dependencies -> taste checkpoints -> lint -> approval before Linear; walkthrough in `references/`). Worked example `examples/cajunt/` (brief + CAJ-1..10, a DAG; only CAJ-1 is Ready). `scripts/check_ticket_graph.py` (stdlib; unknown blockers, duplicates, cycles; prints topological order) with `tests/test_check_ticket_graph.py`; `make verify` gains step 7. Step 4 already lints the example tickets. `claude plugin validate` does not inspect SKILL.md frontmatter (verified by deleting `name:`), so `tests/test_skills_frontmatter.py` checks name == folder, a `Use when...` description and the 150-line cap.
- Next step: dry-run decompose-project on a fresh brief in a scratch session, and wire `check_ticket_graph.py` into the Linear creation flow in the linear-workflow plugin.
