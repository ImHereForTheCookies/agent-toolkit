# Implementer brief

You implement ONE Linear ticket in ONE repo checkout. The orchestrator gives you: ticket ID, repo path, toolkit path ($TOOLKIT, a checkout of agent-toolkit).

1. Read the ticket with the Linear MCP `get_issue` (load via ToolSearch: `select:mcp__Linear__get_issue,mcp__Linear__save_issue,mcp__Linear__save_comment`). Set its state to "In Progress".
2. Start-up ritual in the repo: read CLAUDE.md and PROGRESS.md if present, `git log --oneline -15`. `git fetch -q origin && git checkout -q -B main origin/main` (if origin has no main yet, you are on the scaffold ticket: work on main's first commit directly). Run `make verify` if a Makefile exists, to confirm main is green.
3. Branch name = the ticket identifier lowercased (e.g. `rob-23`). If `origin/<branch>` already exists, check it out and continue that work instead of starting over. Implement only this ticket.
4. Conventions: follow the repo's CLAUDE.md. For agent-toolkit: stdlib Python, tests in tests/, new checks go into scripts/verify.sh before the final `verify: OK` step; SKILL.md frontmatter `name` = folder, `description` starts "Use when", body under ~150 lines.
   If superpowers skills are available, follow `test-driven-development` and `verification-before-completion`; never run `brainstorming` or ask questions (unattended run, the ticket is the approved spec).
5. Append a PROGRESS.md entry (date, ticket, outcome, next step).
6. `make verify` must be green. Commit as `<TICKET>: <ticket title>` and end the message with:
   Co-Authored-By: Claude <noreply@anthropic.com>
7. `git push -u origin <branch>`. Open the PR with the REST helper (never `gh pr create`; GraphQL is blocked): write a body file (Linear link, what changed, verify tail as evidence, "Awaiting independent review."), then from the repo run
   `$TOOLKIT/orchestration/ghpr.sh open <branch> main "<TICKET>: <title>" <bodyfile>`
8. Linear: state "In Review", comment with branch, PR link, verify result.
9. Do NOT merge. If the ticket is ambiguous, contradicts itself or the code, or needs an irreversible/external action: do not guess — decide per `$TOOLKIT/plugins/agentic-workflow/skills/human-in-the-loop/SKILL.md` and reply `ESCALATE: <reason>` and stop.
10. Reply in at most 12 lines: branch, commit, verify result, PR link, deviations.
