# agent-toolkit (repo guide for agents)

This repo is a Claude Code plugin marketplace (`agent-toolkit`) by Robert Meyer.
It lists four plugins that later tickets fill with skills, agents and hooks.

## Layout
- `.claude-plugin/marketplace.json` - marketplace manifest, lists the plugins
- `plugins/<name>/.claude-plugin/plugin.json` - one manifest per plugin
- `plugins/<name>/README.md` - one-paragraph purpose of the plugin
- Plugins: `agentic-workflow`, `code-navigation`, `linear-workflow`, `project-template`
- `scripts/verify.sh` - step runner behind `make verify`; extend at the marked block
- `scripts/smoke_install.sh` - add + install all plugins in a temp CLAUDE_CONFIG_DIR
- `tests/` - pytest tests (`test_*.py`)
- `.github/workflows/ci.yml` - runs `make verify` on push and PR
- `PROGRESS.md` - append-only session log

## Commands
- `make verify` - validate marketplace and each plugin, run tests if present. Fast; run it often.
- `make smoke` - local marketplace add + install of all plugins. Slower; not part of verify.

## Conventions
- Prefer stdlib Python and POSIX shell; add dependencies only with a good reason.
- Tests live in `tests/` and are discovered by `verify.sh` automatically.
- Every ticket ends green on `make verify`.
- The marketplace entry `name` must equal the plugin's `plugin.json` `name`.
- No `version` field in any manifest, so users track commits.
- Warnings from `claude plugin validate` are acceptable; errors are not.
- `PROGRESS.md` is append-only: add a new entry per session, never rewrite old ones.
