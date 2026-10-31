# Requirements (for agents)

This is `requirements.txt` for agents. Before doing any work from this repo, an agent checks the lines below against what its session actually has. If a **required** line is not met, stop and report which line failed; do not improvise a substitute. `plugins/ticket-loop/scripts/check_requirements.py` checks the machine-checkable CLI lines; the connector and plugin lines are checked by the agent itself (see Preflight).

## Manifest

```
# kind: name | needed by | how to check
mcp: Linear | ticket-loop, linear-workflow | tools named mcp__Linear__* are listed (load via ToolSearch)
mcp: Notion | ticket-loop | tools named mcp__Notion__* are listed (load via ToolSearch)
plugin: superpowers | ticket-loop, agentic-workflow | skills named superpowers:* are listed
cli: git | all | git --version
cli: gh | ticket-loop, agentic-workflow (ghpr.sh) | gh --version, authenticated for the project repos
cli: python3>=3.10 | all scripts | python3 --version
cli: make | project repos, make verify | make --version
optional mcp: claude-code-remote | ticket-loop (chaining runs, scheduling) | tools named mcp__claude-code-remote__* are listed; without it the run continues in-session and does not chain
optional cli: claude | make verify (plugin validation) | claude --version
optional python: playwright | qa-ticket, evaluate-project (UI checks) | python3 -c "import playwright"
```

`optional` lines never block a run; the "how to check" column says what degrades.

## Per plugin

| Plugin | Needs | Depends on plugins |
|---|---|---|
| agentic-workflow | superpowers, git, gh, python3 | none (owns the ticket linter, graph checker, implementer/reviewer briefs, `ghpr.sh`) |
| code-navigation | python3 | none |
| linear-workflow | Linear | agentic-workflow (ticket linter) |
| project-template | git, python3 | none (enables the other plugins in new projects) |
| ticket-loop | Linear, Notion, superpowers, git, gh, python3 | agentic-workflow, linear-workflow, project-template |

A plugin's skills may reference another plugin only if the table lists it. `tests/test_requirements.py` enforces that.

## Preflight (what an agent does first)

1. Read this file. Note which plugin or skill you are about to run and its row above.
2. Connectors: confirm each required `mcp:` name appears in your tool list (load with ToolSearch if deferred). A missing connector means stop.
3. Plugins: confirm the required `plugin:` skills are listed (for superpowers, any `superpowers:*` skill). Installed-but-not-loaded counts as missing: scheduled runs do not always load every plugin.
4. CLIs: run `python3 plugins/ticket-loop/scripts/check_requirements.py` from a toolkit checkout (or run the "how to check" commands yourself).
5. If anything required is missing, end the run with one message listing the missing lines and how to add them (below). Do not continue partially.

## Adding what is missing

- **Linear / Notion:** connect the connector for your Claude account (Settings, Connectors). Scheduled runs need the connectors attached to the scheduled task.
- **superpowers:** `/plugin install superpowers@<marketplace that provides it>` (upstream: `obra/superpowers`). Enable it for scheduled tasks as well.
- **agent-toolkit itself:** `/plugin marketplace add <owner>/agent-toolkit`, then `/plugin install <plugin>@agent-toolkit` for each plugin you use, honouring the "Depends on plugins" column.
- **CLIs:** install with your package manager; `gh auth login` for GitHub.

## Keeping this file true

Changing what a skill needs means changing this file in the same PR. `tests/test_requirements.py` fails when a skill references a connector or plugin that is not listed here, or a plugin reaches into another plugin that it does not depend on.
