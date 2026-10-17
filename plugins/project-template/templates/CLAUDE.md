# {{PROJECT_NAME}}

Repo guide for agents. Keep this file under 60 lines; link out for detail.

## Stack
- Language / runtime: TODO
- Frameworks and key libraries: TODO
- Data stores and external services: TODO

## Commands
- `make dev` - start the app locally
- `make test` - fast unit tests
- `make e2e` - end-to-end smoke test against a running app
- `make verify` - `test` then `e2e`; the gate every ticket must pass
- `make symbols` - regenerate the repo map (symbol index) for code navigation

Targets that still print "TODO: define <target> for this project" are not
wired up yet; define them before relying on `make verify`.

## Architecture decisions
Record each decision as one line: what was chosen, why, date.
- TODO: first decision

## Gotchas
Traps that cost time once; add new ones as you hit them.
- TODO: none recorded yet

## Workflow
Session start, in this order:
1. Read `PROGRESS.md` and the last 20 commits (`git log --oneline -20`).
2. Run `make dev` and a smoke test to confirm the app actually works.
3. Only then read your ticket and start on it.

Rules:
- One ticket per session; do not start a second one.
- Finish green: `make verify` must pass before you commit.
- Append an entry to `PROGRESS.md` (date, ticket, outcome, next step). Never
  rewrite old entries.
- If the ticket is ambiguous or contradicts itself, stop and escalate rather
  than guess.
