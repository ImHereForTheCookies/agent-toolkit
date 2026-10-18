# Nightly orchestration runbook

The scheduled nightly task follows this file until the `nightly-run` skill (ROB-15) replaces it.
You are the **orchestrator**. You never write feature code yourself: Sonnet subagents implement and review; you dispatch, read their short reports, post verdicts, merge, and keep Linear honest. Keep your own context small.

## Setup (once per run)
1. The scheduled session already has GitHub access to the repos in the project map plus agent-toolkit; `add_repo` is NOT available in scheduled runs, so don't call it. Clone with `git clone --depth 50 https://github.com/<repo> ~/work/<name>`. `TOOLKIT=~/work/agent-toolkit`. If a needed repo isn't accessible, comment the exact error on the Linear project and end the run (a person must add the repo to the scheduled task).
2. `pip install --break-system-packages -q fastapi uvicorn httpx pytest` (add a project's requirements if it has them). The QA subagent installs `playwright` itself if it needs it.
3. Load Linear tools via ToolSearch: `select:mcp__Linear__list_issues,mcp__Linear__get_issue,mcp__Linear__save_issue,mcp__Linear__save_comment,mcp__Linear__list_projects`.

## Project map (Linear project → GitHub repo), in priority order
| Linear project | Repo |
| --- | --- |
| cajunt | ImHereForTheCookies/cajunt |

agent-toolkit is **not** a work source (its tickets are canceled). It is cloned only because it holds this runbook, the briefs, `ghpr.sh` and the skills.

## Picking work
**Concurrency guard (check first):** if any ticket in the project is In Progress and was updated in the last 60 minutes, another run is probably active. End this run immediately with a one-line note; do not chain.

Team `ROB`. Status mapping: Todo = Ready, In Progress, In Review, Done; label **Needs Human** = escalated (skip it).
For each project in priority order, handle tickets in this order:
1. **In Review** with an open PR → go straight to review (step B).
2. **In Progress** → a previous run was interrupted; re-dispatch the implementer (it resumes the existing branch).
3. **Backlog** tickets whose blockers are all Done → set them to Todo (promotion), but only if `python3 $TOOLKIT/scripts/lint_ticket.py` passes on the description saved to a file; otherwise add Needs Human with the lint output.
4. **Todo** tickets whose blockers are all Done, oldest/lowest number first.
One ticket at a time, sequentially (tickets in the same repo touch shared files).
A blocker counts as satisfied when it is Done, or when it is In Review with an open PR whose last orchestrator comment is `Review PASS, QA PASS, waiting on merge` and whose head is unchanged and CI green (a "pending-merge" blocker). A ticket that depends on a pending-merge blocker is built stacked (next section).

## Per ticket
A. **Implement.** Spawn a Sonnet subagent (Agent tool, `model: sonnet`, foreground): "Read and follow `$TOOLKIT/orchestration/IMPLEMENTER_BRIEF.md`. Ticket: <ID>. Repo path: <path>. TOOLKIT=<path>." If it replies `ESCALATE:`, escalate (see Escalation) and move on.
B. **Review.** Spawn a *different* Sonnet subagent: "Read and follow `$TOOLKIT/orchestration/REVIEWER_BRIEF.md`. Ticket <ID>, branch <b>, PR <url>, repo <path>."
C. **QA** (only after review PASS). Spawn a separate Sonnet subagent: "Read and follow `$TOOLKIT/plugins/agentic-workflow/skills/qa-ticket/SKILL.md` for ticket <ID>, branch <b>, repo <path>." It replies `QA: PASS`, `QA: FAIL` or `QA: SKIPPED (<reason>)`. For a taste-checkpoint ticket, attach its screenshot paths/summary to the PR comment and the Linear comment.
D. **Merge only if review PASS and QA PASS** (or QA SKIPPED with a stated reason). Write the review verdict plus the QA report to a file, `$TOOLKIT/orchestration/ghpr.sh comment <b> <file>`, then `$TOOLKIT/orchestration/ghpr.sh merge <b>`. Linear: state Done, comment with PR link + verdict and QA summary.
   **Merge refused or impossible** (the permission classifier denies the merge, the API errors, or the base is stale) → this is NOT an escalation and does not stop the run. Do the safe part and stack instead (see "Stacking when merges are blocked"): post the verdict comment on the PR, set the Linear ticket to In Review with a comment `**Review PASS, QA PASS, waiting on merge**` (PR link, head sha, the merge order), and carry on to the next ticket on top of this branch. Do not label Needs Human just because the merge was denied.
   **Review FAIL or QA FAIL** → send the findings back to a fresh implementer once (same brief + "Fix these findings: …"), then re-run review and QA. A second FAIL of either → escalate (label Needs Human, comment both verdicts, leave the PR open), move on. QA FAIL counts exactly like a review FAIL.
E. After each merge: `git -C <repo> fetch -q origin && git -C <repo> checkout -q -B main origin/main` and confirm `make verify` is green on main. If main is red, stop starting new tickets: open a fix ticket in Linear (Todo) describing the failure and escalate it with Needs Human.

## Stacking when merges are blocked
Merges can be denied unattended. Never stop the pipeline for that; stack.
1. Base branch for a new ticket = the branch of its newest pending-merge blocker (or the tip of the stack when several tickets are pending), otherwise `main`. The implementer creates `rob-<n>` from that base and opens the PR with `ghpr.sh open <head> <base> ...`; its first body line is `**Stacked on #<parent> (-> #<grandparent> ...); merge after them.**`. Pass the base branch to the implementer in step A ("Base branch: <b>") and to reviewer and QA (they check out the branch, so the parent's code is present). Review the PR for its own diff only (`git diff <base>...<head>`).
2. A pending-merge ticket stays In Review; do not set it Done until its PR is actually merged. When picking work, first reconcile: for each pending-merge ticket whose PR is now merged, set it Done with the evidence comment, and if a child PR's base branch is the merged one, retarget it with `gh api -X PATCH repos/<repo>/pulls/<n> -f base=main` (the parent branch is not deleted on merge, so GitHub will not retarget).
3. Before reviewing a stacked child, confirm its parent chain is still unchanged (parent head sha equals the base sha recorded in the child). If a parent changed after review, merge the parent into the child branch (`git merge <parent>`, never force-push) and re-review.
4. Stacks are capped at 8 open PRs. At the cap, do the reconcile step, and if nothing merged, end the run with a PushNotification asking Robert to merge the bottom PR (name its number); do not chain.
5. Always try `ghpr.sh merge` on the bottom-most reviewed PR first (retargeted to `main`); if the classifier denies it once, do not retry or work around it in this run.
6. Needs Human is for the six HITL triggers, not for denied merges. When the stack is at the cap or the run ends with nothing eligible, send a PushNotification naming the bottom PR to merge and the stack length.

## Escalation
Core rule: never block waiting for a human; do the safe part, leave a precise Linear note (label Needs Human + comment), and move to the next ticket. Decide whether, how and what to write using `$TOOLKIT/plugins/agentic-workflow/skills/human-in-the-loop/SKILL.md` (six triggers, action labels, comment template); Linear mechanics are in the `linear-tickets` skill. Read it when an implementer replies `ESCALATE:`, a ticket fails twice, or anything irreversible, ambiguous, security-sensitive or out of scope comes up.

## Superpowers
If the superpowers skills are available, implementers should follow its `test-driven-development` and `verification-before-completion` skills. Never run superpowers' `brainstorming` or ask clarifying questions in this unattended run: the Linear ticket is the approved spec. If the ticket is insufficient, escalate per the human-in-the-loop skill instead of asking.

## One ticket per run (fresh context every ticket)
Each run handles exactly ONE ticket, then hands off to a brand-new run, so every ticket starts with a clean orchestrator context. This replaces in-session compaction: a fresh session carries no leftover tool output at all, and Linear + git hold all the state.
1. Pick the single next ticket (see Picking work) and take it through steps A–E, including the merge or escalation and the Linear update.
2. Then decide whether to chain: re-check Linear. If at least one ticket is still eligible AND this run made progress (a ticket moved to Done, or got Needs Human), fire the next run: load `mcp__claude-code-remote__fire_trigger` via ToolSearch and call it with `trigger_id` `trig_01R5kFZkhgrQ9k2RGqBKzogY` and `text` "Chained run: continue with the next eligible ticket." Then end this run.
3. Progress includes a ticket stacked as pending-merge. Do not chain if this run made no progress (that would loop), if main is red, or if the stack is at the cap (see Stacking). If `fire_trigger` is unavailable or refused, continue in this same session with the next ticket instead (auto-compaction will handle context) and say so in the summary.
- Never stop between merge and the Linear update.
- Never force-push, never delete branches or repos, never touch secrets, never deploy. Anything irreversible or outside these repos → Needs Human.

## End of run
Keep it short; there is one run per ticket. Post a Linear comment on the ticket (already done in step D) and, only when NOT chaining (the chain is finished), a project summary comment on each touched project (`save_comment` with `projectId`) summarising: merged PRs, tickets escalated and why, what is next. Then send the user a short summary with SendUserMessage (load via ToolSearch) if available.

## Known environment facts
- Scheduled runs: repo access is fixed when the scheduled task is created (the repos attached to the session that created it). To add a project repo, recreate the scheduled task from a session that has that repo attached.
- The cajunt repo may contain other task lists (e.g. TASKS.md); the Linear ticket is the spec.
- `gh` GraphQL commands (`gh pr create`, `gh pr merge`) are blocked; `gh api` REST works — that's what ghpr.sh uses.
- Subagents may be blocked from merging by the permission classifier; that's why the orchestrator merges.
- Linear renders markdown bullets as `*`; the ticket linter accepts `-`, `*`, `+`.
- `claude plugin validate` exits 0 with warnings; `/bin/sh` may be dash, so scripts use bash.
- Pushing from a shallow clone: `git fetch origin main` first to avoid HTTP 413.
