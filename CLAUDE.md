# agent-toolkit (repo guide for agents)

This repo is a Claude Code plugin marketplace (`agent-toolkit`) by Robert Meyer.
It lists four plugins that later tickets fill with skills, agents and hooks.

## Layout
- `.claude-plugin/marketplace.json` - marketplace manifest, lists the plugins
- `plugins/<name>/.claude-plugin/plugin.json` - one manifest per plugin
- `plugins/<name>/README.md` - one-paragraph purpose of the plugin
- Plugins: `agentic-workflow`, `code-navigation`, `linear-workflow`, `project-template`
- `plugins/code-navigation/scripts/repo_map.py` - symbol index writer (`docs/symbols.md`); skill `navigate-codebase`
- `plugins/linear-workflow/skills/linear-tickets/SKILL.md` + `.mcp.json` - Linear status mapping, claiming, evidence and escalation; Linear MCP for headless runs
- `plugins/agentic-workflow/skills/human-in-the-loop/SKILL.md` - the six escalation triggers, comment template, reviewer guard
- `evals/hitl/` - scenarios + `run_eval.py` for that skill (`make eval-hitl`, costs API calls, not in verify)
- `scripts/verify.sh` - step runner behind `make verify`; extend at the marked block
- `scripts/smoke_install.sh` - add + install all plugins in a temp CLAUDE_CONFIG_DIR
- `tests/` - pytest tests (`test_*.py`)
- `fixtures/demo-project/` - small FastAPI + SQLite app, sample tickets and `fixtures/seeded-bug.patch` for testing the toolkit (`scripts/check_seeded_bug.sh`)
- `.github/workflows/ci.yml` - runs `make verify` on push and PR
- `orchestration/` - nightly runbook (`NIGHTLY.md`), implementer/reviewer briefs, REST PR helper `ghpr.sh`
- `PROGRESS.md` - append-only session log

## Commands
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
