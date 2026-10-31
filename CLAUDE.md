# agent-toolkit (repo guide for agents)

This repo is a Claude Code plugin marketplace (`agent-toolkit`) by Robert Meyer. Read `REQUIREMENTS.md` first: it lists what agents need (Linear, Notion, superpowers, git, gh, python3) and the preflight to run.
It lists five plugins (skills, agents and hooks).

## Layout
- `.claude-plugin/marketplace.json` - marketplace manifest, lists the plugins
- `plugins/<name>/.claude-plugin/plugin.json` - one manifest per plugin
- `plugins/<name>/README.md` - one-paragraph purpose of the plugin
- Plugins: `agentic-workflow`, `code-navigation`, `linear-workflow`, `project-template`, `ticket-loop`
- `plugins/ticket-loop/` - the general daily job: `run-queue` routes Linear tickets by Skill label (`ROUTES.md`) to `design-system`, `plan-tickets`, `build-ticket`, `evaluate-project`; `new-skill` adds kinds of work (marketplace search first); `HARD_LIMITS.md`, `templates/` (scheduled prompt, project description, design doc). Spec: `docs/specs/2026-10-25-ticket-loop-design.md`. `orchestration/` is the author's own nightly loop (example, not a dependency; values injected, see `orchestration/SETTINGS.md`).
- `plugins/code-navigation/scripts/repo_map.py` - symbol index writer (`docs/symbols.md`); skill `navigate-codebase`
- `plugins/linear-workflow/skills/linear-tickets/SKILL.md` + `.mcp.json` - Linear status mapping, claiming, evidence and escalation; Linear MCP for headless runs
- `plugins/agentic-workflow/skills/human-in-the-loop/SKILL.md` - the six escalation triggers, comment template, reviewer guard
- `plugins/agentic-workflow/skills/qa-ticket/SKILL.md` - QA subagent protocol run after review PASS, before merge (curl/Playwright, PASS/FAIL/SKIPPED)
- `evals/hitl/` - scenarios + `run_eval.py` for that skill (`make eval-hitl`, costs API calls, not in verify)
- `REQUIREMENTS.md` - requirements for agents (manifest + preflight); `plugins/ticket-loop/scripts/check_requirements.py` checks the CLI lines; `tests/test_requirements.py` keeps it true
- `CONTRIBUTING.md` - setup (`make setup`, `make doctor`), where things go, odd rules
- `plugins/agentic-workflow/{scripts,briefs}/` - ticket linter, graph checker, `ghpr.sh`, implementer/reviewer briefs; `plugins/ticket-loop/scripts/release.sh`
- `scripts/verify.sh` - step runner behind `make verify`; extend at the marked block
- `scripts/smoke_install.sh` - add + install all plugins in a temp CLAUDE_CONFIG_DIR
- `tests/` - pytest tests (`test_*.py`)
- `fixtures/demo-project/` - small FastAPI + SQLite app, sample tickets and `fixtures/seeded-bug.patch` for testing the toolkit (`scripts/check_seeded_bug.sh`)
- `.github/workflows/ci.yml` - runs `make verify` on push and PR
- `orchestration/` - nightly runbook (`NIGHTLY.md`: build first, then one unit per run from `RND.md`), `release.sh` (forwarder to the ticket-loop script; frozen `release/<slug>-vN` branch + fast-forward `release/<slug>` after the release gate; no tags), `HARD_LIMITS.md` (protected, hash-pinned), R&D briefs (`RESEARCH_BRIEF.md`, `GROWTH_BRIEF.md`, `LAUNCH_BRIEF.md`)
- `PROGRESS.md` - append-only session log

## Commands
- `make setup` / `make doctor` - install dev dependencies / check CLI requirements
- `make verify` - validate marketplace and each plugin, run tests if present. Fast; run it often.
- `make eval-hitl` - run the human-in-the-loop eval via `claude -p` (needs login; not part of verify)
- `make smoke` - local marketplace add + install of all plugins. Slower; not part of verify.

## Conventions
- Prefer stdlib Python and POSIX shell; add dependencies only with a good reason.
- Tests live in `tests/` and are discovered by `verify.sh` automatically.
- Every ticket ends green on `make verify`.
- The marketplace entry `name` must equal the plugin's `plugin.json` `name`.
- No `version` field in any manifest, so users track commits.
- Warnings from `claude plugin validate` are acceptable; errors are not.
- `PROGRESS.md` is append-only: add a new entry per session, never rewrite old ones.
