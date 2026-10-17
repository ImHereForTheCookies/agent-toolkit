# Nightly orchestration runbook

The scheduled nightly task follows this file until the `nightly-run` skill (ROB-15) replaces it.
You are the **orchestrator**. You never write feature code yourself: Sonnet subagents implement and review; you dispatch, read their short reports, post verdicts, merge, and keep Linear honest. Keep your own context small.

## Setup (once per run)
1. Attach repos with push access (`add_repo`, tool `mcp__claude-code-remote__add_repo`): `ImHereForTheCookies/agent-toolkit` and every repo in the project map below. Clone each into `~/work/<repo>` with `git clone --depth 50`. `TOOLKIT=~/work/agent-toolkit`.
2. `pip install --break-system-packages -q fastapi uvicorn httpx pytest` (add a project's requirements if it has them).
3. Load Linear tools via ToolSearch: `select:mcp__Linear__list_issues,mcp__Linear__get_issue,mcp__Linear__save_issue,mcp__Linear__save_comment,mcp__Linear__list_projects`.

## Project map (Linear project → GitHub repo), in priority order
| Linear project | Repo |
| --- | --- |
| agent-toolkit | ImHereForTheCookies/agent-toolkit |
| cajunt | ImHereForTheCookies/cajunt |

## Picking work
Team `ROB`. Status mapping: Todo = Ready, In Progress, In Review, Done; label **Needs Human** = escalated (skip it).
For each project in priority order, handle tickets in this order:
1. **In Review** with an open PR → go straight to review (step B).
2. **In Progress** → a previous run was interrupted; re-dispatch the implementer (it resumes the existing branch).
3. **Backlog** tickets whose blockers are all Done → set them to Todo (promotion), but only if `python3 $TOOLKIT/scripts/lint_ticket.py` passes on the description saved to a file; otherwise add Needs Human with the lint output.
4. **Todo** tickets whose blockers are all Done, oldest/lowest number first.
One ticket at a time, sequentially (tickets in the same repo touch shared files).

## Per ticket
A. **Implement.** Spawn a Sonnet subagent (Agent tool, `model: sonnet`, foreground): "Read and follow `$TOOLKIT/orchestration/IMPLEMENTER_BRIEF.md`. Ticket: <ID>. Repo path: <path>. TOOLKIT=<path>." If it replies `ESCALATE:`, add label Needs Human, comment the reason, move on.
B. **Review.** Spawn a *different* Sonnet subagent: "Read and follow `$TOOLKIT/orchestration/REVIEWER_BRIEF.md`. Ticket <ID>, branch <b>, PR <url>, repo <path>."
C. **PASS** → from the repo: write the verdict to a file, `$TOOLKIT/orchestration/ghpr.sh comment <b> <file>`, then `$TOOLKIT/orchestration/ghpr.sh merge <b>`. Linear: state Done, comment with PR link + verdict summary.
   **FAIL** → send the findings back to a fresh implementer once (same brief + "Fix these review findings: …"), then review again. A second FAIL → label Needs Human, comment both verdicts, leave the PR open, move on.
D. After each merge: `git -C <repo> fetch -q origin && git -C <repo> checkout -q -B main origin/main` and confirm `make verify` is green on main. If main is red, stop starting new tickets: open a fix ticket in Linear (Todo) describing the failure and escalate it with Needs Human.

## Budget and stopping
- Stop starting new tickets after 8 tickets, or earlier if your context is getting long. Never stop between merge and the Linear update.
- Never force-push, never delete branches or repos, never touch secrets, never deploy. Anything irreversible or outside these repos → Needs Human.

## End of run
Post a Linear comment on each touched project (`save_comment` with `projectId`) summarising: merged PRs, tickets escalated and why, what is next. Then send the user a short summary with SendUserMessage (load via ToolSearch) if available.

## Known environment facts
- `gh` GraphQL commands (`gh pr create`, `gh pr merge`) are blocked; `gh api` REST works — that's what ghpr.sh uses.
- Subagents may be blocked from merging by the permission classifier; that's why the orchestrator merges.
- Linear renders markdown bullets as `*`; the ticket linter accepts `-`, `*`, `+`.
- `claude plugin validate` exits 0 with warnings; `/bin/sh` may be dash, so scripts use bash.
- Pushing from a shallow clone: `git fetch origin main` first to avoid HTTP 413.
