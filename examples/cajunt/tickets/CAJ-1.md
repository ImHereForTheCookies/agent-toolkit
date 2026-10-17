Status: Ready

# CAJ-1 Scaffold the Cajunt repo from the project template

## Goal
A new `cajunt` repo exists with the standard harness, so every later ticket starts from a green `make verify`.

## Context
- Use the `project-template` plugin's template (Python + FastAPI + SQLite layout, `Makefile`, CI, `CLAUDE.md`).
- Nothing app-specific yet: no routes beyond `/health`, no tables.

## Acceptance criteria
- [ ] `make verify` runs lint, tests and a boot check and exits 0 on a fresh clone — checked by: make verify
- [ ] `GET /health` returns 200 with `{"status": "ok"}` — checked by: tests/test_health.py::test_health_ok
- [ ] `CLAUDE.md` lists the run, test and verify commands — checked by: tests/test_repo_layout.py::test_claude_md_lists_commands

## Verify
`make verify`

## Out of scope
Any Cajunt domain code, UI, database schema, CI beyond what the template provides.

## Escalation
none
