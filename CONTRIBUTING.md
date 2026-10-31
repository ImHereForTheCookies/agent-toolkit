# Contributing

## Set up
```
make setup      # pytest, fastapi, httpx, uvicorn for tests and the demo fixture
make doctor     # checks git, gh, python3, make (see REQUIREMENTS.md)
make verify     # validates the marketplace and each plugin, runs tests and fixtures
```
`make verify` also needs the `claude` CLI (`npm install -g @anthropic-ai/claude-code`) for plugin validation. Fast: run it often. Every PR ends green on `make verify`.

## Where things go
- A skill or script belongs to exactly one plugin and may reference another plugin only if `REQUIREMENTS.md` lists it under "Depends on plugins". A test enforces this.
- Inside a plugin, reference its own files with `${CLAUDE_PLUGIN_ROOT}`. Reference other plugins through `$TOOLKIT/plugins/<name>/` (a checkout) only where a dependency allows it.
- Never put a person's name, team key, repo, tracker ID, path or numeric cap into a plugin. Use a placeholder or an optional config key (see `plugins/ticket-loop/templates/scheduled-prompt.md`).
- If a skill needs a new connector, plugin or CLI, add it to `REQUIREMENTS.md` in the same PR.

## Adding things
- **A new kind of work for the ticket loop:** follow `plugins/ticket-loop/skills/new-skill/SKILL.md` (search for an existing plugin first, write the skill, add a row to `ROUTES.md`).
- **A new plugin:** `plugins/<name>/.claude-plugin/plugin.json`, a README, an entry in `.claude-plugin/marketplace.json` (same `name`), a row in `REQUIREMENTS.md` and the README table. No `version` field in manifests.
- **A new project convention (for example a `pocs/<slug>` folder layout):** put it in the project repo, and tell the loop about it in that Linear project's description (`Repo:`, `Folder:`, `Constraints:`).

## Rules that look odd
- `PROGRESS.md` is an append-only session log. Add an entry; never rewrite old ones.
- `orchestration/HARD_LIMITS.md` is hash-pinned by `tests/test_orchestration_refs.py` so the self-improving retro loop cannot loosen its own rules. Change it only in a PR a maintainer asks for, explain why in the description, and update `HARD_LIMITS_SHA256` in the same PR. Anything that merely needs its path or wording kept stable should be forwarded, not edited (see `orchestration/release.sh`).
- Warnings from `claude plugin validate` are acceptable; errors are not.
- Prefer stdlib Python and POSIX shell; add dependencies only with a good reason.
