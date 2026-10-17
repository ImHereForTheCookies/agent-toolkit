# project-template

Scaffolds a new project repo that loads this toolkit. The `harness-init` skill runs `scripts/harness_init.py`, which copies `templates/` (CLAUDE.md, PROGRESS.md, a Makefile with the dev/test/e2e/verify contract, and `.claude/settings.json` that registers this marketplace and enables its plugins) into a project directory without overwriting existing files.

Install: `/plugin marketplace add ImHereForTheCookies/agent-toolkit`, then `/plugin install project-template@agent-toolkit`
