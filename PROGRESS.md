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
