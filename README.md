# agent-toolkit

A Claude Code plugin marketplace for building software with agents: a spec for tickets an agent can finish alone, a QA and escalation protocol, Linear integration, a project scaffold, and an unattended job (the ticket loop) that ties them together.

**Requirements:** Linear, Notion, the superpowers plugin, plus `git`, `gh` and `python3`. The full list, with how an agent checks each line, is in [`REQUIREMENTS.md`](REQUIREMENTS.md). Run `make doctor` to check the command-line parts.

## Install

```
/plugin marketplace add <owner>/agent-toolkit
/plugin install <plugin>@agent-toolkit
```

`<owner>` is `ImHereForTheCookies` for upstream, or your fork. Install each plugin you use plus the ones it depends on.

## Plugins

| Plugin | What it gives you | Depends on |
|---|---|---|
| `agentic-workflow` | Ticket spec and linter, decomposition, QA (`qa-ticket`), escalation (`human-in-the-loop`), implementer and reviewer briefs, `ghpr.sh` | none |
| `code-navigation` | Cheapest-first code search, symbol map script | none |
| `linear-workflow` | How agents find, claim and report on Linear tickets | `agentic-workflow` |
| `project-template` | `harness-init`: CLAUDE.md, PROGRESS.md, Makefile and settings for a new repo | none |
| `ticket-loop` | The unattended job: Linear tickets routed by Skill label to design, plan, build, evaluate | all of the above |

## Two ways to run builds

- **General path: `plugins/ticket-loop`.** Linear holds the work, Notion the design docs, GitHub the code. Everything setup-specific (team, repos, limits) lives in a short scheduled prompt you write. Start with `plugins/ticket-loop/README.md`.
- **The author's own loop: `orchestration/`.** A nightly R&D pipeline for the author's prototypes (new app idea every night). It is kept as a worked example and is not needed for the plugins. Its values are injected from a settings page; see `orchestration/README.md`.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Short version: `make setup`, then `make verify` before every PR.
