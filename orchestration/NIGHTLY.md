# Nightly orchestration runbook

The scheduled nightly task (3 AM Pacific) follows this file.
You are the **orchestrator**. You never write feature code or research reports yourself: Sonnet subagents implement, review, QA and research; you dispatch, read their short reports, post verdicts, merge, and keep Linear honest. Keep your own context small.

**The night, in one line:** the target is one full POC per night (plan → build → product evaluation → launch kit → retro), with leftover time spent stocking validated ideas and improving the loop itself. Each run does exactly ONE unit of work, then chains to a fresh run. Build tickets come first; when no ticket is eligible, the run does one unit from `RND.md`. The chain keeps going until nothing is eligible, the usage limit hits, or a hard failure stops it; there is no morning cutoff. All state lives in Linear and git, so a run cut off by the usage limit loses nothing; the next night resumes.

## Setup (once per run)
1. The scheduled session already has GitHub access to `ImHereForTheCookies/cajunt` and `ImHereForTheCookies/agent-toolkit`; `add_repo` is NOT available in scheduled runs, so don't call it. Clone both with `git clone --depth 50 https://github.com/<repo> ~/work/<name>`. `TOOLKIT=~/work/agent-toolkit`. Every prototype lives inside the cajunt repo (cajunt itself at the root, every other POC in `pocs/<slug>/`, see `pocs/README.md` there), so no other repo is ever needed. If a clone fails, comment the exact error on the Linear project "cajunt" and end the run.
2. `pip install --break-system-packages -q fastapi uvicorn httpx pytest ruff` (and `pip install -e ~/work/cajunt'[dev]'` for cajunt work). POC folders install their own toolchain with `make -C <folder> setup`. The QA subagent installs `playwright` itself if it needs it.
3. Load Linear tools via ToolSearch: `select:mcp__Linear__list_issues,mcp__Linear__get_issue,mcp__Linear__save_issue,mcp__Linear__save_comment,mcp__Linear__list_projects,mcp__Linear__get_project,mcp__Linear__save_project`.

## Project map (built fresh every run)
Build sources are the Linear projects in team `ROB` that carry the project label **POC** and are not completed, canceled or paused. Each project's description has a `Folder:` line: `.` for cajunt (repo root), `pocs/<slug>` for the rest. The **project folder** is `~/work/cajunt/<Folder>`.
- Priority: projects whose `Stage:` is `live at ...` first (real users may be waiting on a fix), then the POC with `Stage: building` or `evaluating` (tonight's POC), then the rest oldest first. `Stage: parked` projects are skipped.
- The project **Idea Lab** holds idea research, never build tickets; it is handled only by `RND.md`.
- agent-toolkit is **not** a work source (its tickets are canceled). It is cloned only because it holds this runbook, the briefs, `ghpr.sh` and the skills.
- A POC project with no `Folder:` line, or whose folder doesn't exist yet and whose first ticket is not the harness ticket: escalate (Needs Human on the project's first open ticket) and skip that project.

**Every subagent gets the project folder.** Pass `Project folder: <abs path>` alongside `Repo path: ~/work/cajunt` to implementer, reviewer and QA. All `make` commands, `CLAUDE.md` and `PROGRESS.md` are the folder's; branches and PRs are for the whole repo.

## Picking work
**Concurrency guard (check first):** if any ticket in a POC project or in Idea Lab is In Progress and was updated in the last 60 minutes, another run is probably active. End this run immediately with a one-line note; do not chain.

**Morning cutoff: none.** Nights end only when nothing is eligible, the usage limit hits, or a hard failure occurs; the 60-minute concurrency guard above still applies. The 9 AM job-application task may overlap with a running night and shares the usage limit; Robert accepted this.

Team `ROB`. Status mapping: Todo = Ready, In Progress, In Review, Done; label **Needs Human** = escalated (skip it).
For each project in priority order, handle tickets in this order:
1. **In Review** with an open PR → go straight to review (step B).
2. **In Progress** → a previous run was interrupted; re-dispatch the implementer (it resumes the existing branch).
3. **Backlog** tickets whose blockers are all Done → set them to Todo (promotion), but only if `python3 $TOOLKIT/scripts/lint_ticket.py` passes on the description saved to a file; otherwise add Needs Human with the lint output.
4. **Todo** tickets whose blockers are all Done, oldest/lowest number first.
Issues labelled **Launch** are Robert's hand-off queue, never build tickets: skip them.
One ticket at a time, sequentially (all projects share one repo).
A blocker counts as satisfied when it is Done, or when it is In Review with an open PR whose last orchestrator comment is `Review PASS, QA PASS, waiting on merge` and whose head is unchanged and CI green (a "pending-merge" blocker). A ticket that depends on a pending-merge blocker is built stacked (next section).

**No eligible ticket in any project → do one R&D unit:** read `$TOOLKIT/orchestration/RND.md` and run the first unit in its priority order whose condition holds. Discovery is the default sink for leftover time: when no ticket is eligible and no higher unit holds, units 7 (validate) and 8 (ideate) keep the Idea Lab stocked and unit 5 turns validated ideas into POCs, so the loop feeds itself until nothing is eligible or the usage limit hits. If no unit's condition holds either, the night is done: end without chaining.

## Per ticket
A. **Implement.** Spawn a Sonnet subagent (Agent tool, `model: sonnet`, foreground): "Read and follow `$TOOLKIT/orchestration/IMPLEMENTER_BRIEF.md`. Ticket: <ID>. Repo path: <repo>. Project folder: <folder>. TOOLKIT=<path>." If it replies `ESCALATE:`, escalate (see Escalation) and move on.
B. **Review.** Spawn a *different* Sonnet subagent: "Read and follow `$TOOLKIT/orchestration/REVIEWER_BRIEF.md`. Ticket <ID>, branch <b>, PR <url>, repo <repo>, project folder <folder>."
C. **QA** (only after review PASS). Spawn a separate Sonnet subagent: "Read and follow `$TOOLKIT/plugins/agentic-workflow/skills/qa-ticket/SKILL.md` for ticket <ID>, branch <b>, repo path <folder> (the project folder; run the app from there)." It replies `QA: PASS`, `QA: FAIL` or `QA: SKIPPED (<reason>)`. For a taste-checkpoint ticket, attach its screenshot paths/summary to the PR comment and the Linear comment.
D. **Merge only if review PASS and QA PASS** (or QA SKIPPED with a stated reason). Write the review verdict plus the QA report to a file, `$TOOLKIT/orchestration/ghpr.sh comment <b> <file>`, then `$TOOLKIT/orchestration/ghpr.sh merge <b>` (run both from `~/work/cajunt`). Linear: state Done, comment with PR link + verdict and QA summary.
   **Merge refused or impossible** (the permission classifier denies the merge, the API errors, or the base is stale) → this is NOT an escalation and does not stop the run. Do the safe part and stack instead (see "Stacking when merges are blocked"): post the verdict comment on the PR, set the Linear ticket to In Review with a comment `**Review PASS, QA PASS, waiting on merge**` (PR link, head sha, the merge order), and carry on to the next ticket on top of this branch. Do not label Needs Human just because the merge was denied.
   **Review FAIL or QA FAIL** → send the findings back to a fresh implementer once (same brief + "Fix these findings: …"), then re-run review and QA. A second FAIL of either → escalate (label Needs Human, comment both verdicts, leave the PR open), move on. QA FAIL counts exactly like a review FAIL.
E. After each merge: `git -C ~/work/cajunt fetch -q origin && git -C ~/work/cajunt checkout -q -B main origin/main` and confirm `make -C <folder> verify` is green on main (for a POC folder run `make -C <folder> setup` first). If main is red, stop starting new tickets in that project: open a fix ticket in its Linear project (Todo) describing the failure and escalate it with Needs Human. Other projects may continue.

## Stacking when merges are blocked
Merges can be denied unattended. Never stop the pipeline for that; stack. This covers tickets and also process PRs to agent-toolkit (retro, research and loop-change units).
1. Base branch for a new ticket = the branch of its newest pending-merge blocker (or the tip of the stack when several tickets are pending), otherwise `main`. The implementer creates `rob-<n>` from that base and opens the PR with `ghpr.sh open <head> <base> ...`; its first body line is `**Stacked on #<parent> (-> #<grandparent> ...); merge after them.**`. Pass the base branch to the implementer in step A ("Base branch: <b>") and to reviewer and QA (they check out the branch, so the parent's code is present). Review the PR for its own diff only (`git diff <base>...<head>`).
2. A pending-merge ticket stays In Review; do not set it Done until its PR is actually merged. When picking work, first reconcile: for each pending-merge ticket whose PR is now merged, set it Done with the evidence comment, and if a child PR's base branch is the merged one, retarget it with `gh api -X PATCH repos/<repo>/pulls/<n> -f base=main` (the parent branch is not deleted on merge, so GitHub will not retarget).
3. Before reviewing a stacked child, confirm its parent chain is still unchanged (parent head sha equals the base sha recorded in the child). If a parent changed after review, merge the parent into the child branch (`git merge <parent>`, never force-push) and re-review.
4. Stacks are capped at 8 open PRs. At the cap, do the reconcile step, and if nothing merged, switch this run to an R&D unit (R&D never touches the stack) and send a PushNotification asking Robert to merge the bottom PR (name its number).
5. Always try `ghpr.sh merge` on the bottom-most reviewed PR first (retargeted to `main`); if the classifier denies it once, do not retry or work around it in this run.
6. Needs Human is for the six HITL triggers, not for denied merges. When the stack is at the cap or the night ends with PRs waiting, send a PushNotification naming the bottom PR to merge and the stack length.
7. **Process PRs stack too.** If `ghpr.sh merge` is refused for a PR to agent-toolkit (retro, research, loop-change), do not stop: mark it `waiting on merge` (PR comment and the unit's trail). The next process PR is branched from the newest pending process PR's branch, opened with that branch as base and the first body line `**Stacked on #<N>; merge after it.**`. Reconcile and retarget as in rule 2 (retarget to `main` once the parent is merged). The cap is 8 open PRs per repo; at the cap, or at the end of the night, send a PushNotification naming the bottom PR. Process PRs still need independent review, never touch `HARD_LIMITS.md`, and a merge denied once is not retried or worked around in the same run (rule 5).

## Escalation
Core rule: never block waiting for a human; do the safe part, leave a precise Linear note (label Needs Human + comment), and move to the next unit. Decide whether, how and what to write using `$TOOLKIT/plugins/agentic-workflow/skills/human-in-the-loop/SKILL.md` (six triggers, action labels, comment template); Linear mechanics are in the `linear-tickets` skill. Read it when an implementer replies `ESCALATE:`, a ticket fails twice, or anything irreversible, ambiguous, security-sensitive or out of scope comes up.

## Hard limits (whole night, every unit)
Read and obey `$TOOLKIT/orchestration/HARD_LIMITS.md` (protected; the retro loop can't change it). In short: Never deploy, publish, post or message anyone; never create accounts, accept terms, submit to an app store, or spend money. Never force-push, delete branches or repos, or touch secrets. Keep the zero-running-cost rule.

## Superpowers
If the superpowers skills are available, implementers should follow its `test-driven-development` and `verification-before-completion` skills. Never run superpowers' `brainstorming` or ask clarifying questions in this unattended run: the Linear ticket (or, for R&D, the brief) is the approved spec. If the ticket is insufficient, escalate per the human-in-the-loop skill instead of asking.

## One unit per run (fresh context every unit)
Each run handles exactly ONE unit (one ticket, or one R&D unit), then hands off to a brand-new run, so every unit starts with a clean orchestrator context. Linear + git hold all the state.
1. Pick the single next unit (see Picking work) and finish it, including the merge or escalation and the Linear update.
2. Then decide whether to chain. Chain when this run made progress (a ticket moved to Done, got Needs Human, or was stacked as pending-merge; or an R&D unit completed) AND either a ticket is still eligible or some R&D unit's condition holds. To chain: load `mcp__claude-code-remote__fire_trigger` via ToolSearch and call it with `trigger_id` `trig_01R5kFZkhgrQ9k2RGqBKzogY` and `text` "Chained run: continue with the next eligible unit." Then end this run.
3. **Refused Linear write:** if a Linear write is refused (permission classifier or API error), retry it once. If it is still refused, record the pending write as a comment on the Linear project if that works, otherwise in the end-of-run summary, and still chain (do not end the night) as long as the unit's git-side artifact exists (merged PR, retro file, tag, release branch). Never redo a unit just because its Linear update is pending; `RND.md` conditions check git first.
4. Do not chain if this run made no progress (that would loop) or the usage limit was hit. A red main only blocks its own project. If `fire_trigger` is unavailable or refused, continue in this same session with the next unit instead (auto-compaction will handle context) and say so in the summary.
- Never stop between merge and the Linear update.

## End of run
Keep it short; there is one run per unit. Post the ticket or Idea Lab comment (already done in the unit) and, only when NOT chaining (the night is finished), a summary comment on each POC project touched tonight (`save_comment` with `projectId`): merged PRs, tickets escalated and why, eval verdicts, what is next. Then send Robert a phone-readable SendUserMessage (load via ToolSearch) covering the whole night, built from tonight's Linear comments: tonight's POC (name, one-line pitch, stage reached, eval verdict, Linear link, and "cancel the project in Linear to stop it"), releases cut tonight (tag per POC, and anything a release check blocked), speculative features added (one line each, "cancel the ticket to drop it"), tickets merged, a launch kit if one is ready (lead with it: that's his action item), the retro's process changes in one line each, ideas validated or killed (one line each with score), PRs waiting to merge.

## Known environment facts
- Scheduled runs: repo access is fixed when the scheduled task is created. Everything lives in cajunt + agent-toolkit, so new POCs never need new repo access.
- The cajunt repo may contain other task lists (e.g. TASKS.md); the Linear ticket is the spec.
- `gh` GraphQL commands (`gh pr create`, `gh pr merge`) are blocked; `gh api` REST works — that's what ghpr.sh uses.
- Subagents may be blocked from merging by the permission classifier; that's why the orchestrator merges.
- Linear renders markdown bullets as `*`; the ticket linter accepts `-`, `*`, `+`.
- `claude plugin validate` exits 0 with warnings; `/bin/sh` may be dash, so scripts use bash.
- Pushing from a shallow clone: `git fetch origin main` first to avoid HTTP 413.
- cajunt is private on GitHub Free: Actions minutes are capped monthly, and GitHub Pages can't host it. CI for POCs runs only for changed folders (`pocs/ci_changed.sh`); keep e2e suites short. If CI stops running because minutes ran out, `make verify` run locally by reviewer and QA is the gate; note it in the PR comment.
