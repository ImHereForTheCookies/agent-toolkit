---
name: harness-init
description: Use when starting a new project repo, or retrofitting an existing repo, so that agents can start work cold. Creates CLAUDE.md, PROGRESS.md, a Makefile with the dev/test/e2e/verify contract and .claude/settings.json that loads the agent-toolkit plugins.
---

# Harness init

One command gives a repo the files a worker agent needs to start a session with
no chat history: a short `CLAUDE.md`, an append-only `PROGRESS.md`, a Makefile
with a fixed target contract, and project settings that install this toolkit.

## When to use

- You are starting a brand-new project repo (empty directory is fine).
- You are retrofitting an existing repo that has no `CLAUDE.md`, no `make verify`
  or no `PROGRESS.md`. Existing files are left alone, so it is safe to run.

Not for stack-specific scaffolding (app code, dependencies, CI); that is a
separate step after the harness exists.

## Run it

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harness_init.py" <dir> [--name NAME] [--force]
```

- `<dir>`: the project directory; created if missing.
- `--name`: project name written into the templates (default: the directory name).
- `--force`: overwrite files that already exist. Without it, existing files are
  skipped and never modified. Only pass `--force` if the user asked for it.
- Runs `git init` if `<dir>` is not already a git repo.

It prints one line per file: `created`, `overwritten` or `skipped (exists)`, then
the git status. Report that list to the user.

## Files it creates

| File | Purpose |
| --- | --- |
| `CLAUDE.md` | Stack, Commands, Architecture decisions, Gotchas, Workflow (under 60 lines) |
| `PROGRESS.md` | Append-only session log |
| `Makefile` | `dev`, `test`, `e2e`, `verify` (= test then e2e) and `symbols` |
| `.claude/settings.json` | Registers `ImHereForTheCookies/agent-toolkit` and enables its four plugins |

## Fill in afterwards

The templates are deliberately skeletal. After running, do these before the
first ticket:

1. `CLAUDE.md`: replace every `TODO` under Stack, Architecture decisions and
   Gotchas with real content. Keep the file under 60 lines.
2. `Makefile`: replace the `TODO: define <target> for this project` recipes so
   that `make dev` starts the app, `make test` runs unit tests, `make e2e` runs a
   smoke test, and `make verify` is genuinely green only when the project works.
   The stub recipes exit 0, so `verify` passes trivially until you do this.
3. `PROGRESS.md`: append the first entry describing the setup.
4. Commit the files so every worker clone gets the same harness.

Project settings take effect after the user trusts the folder. If the plugins do
not load, tell the user to accept the workspace trust prompt and restart the
session.
