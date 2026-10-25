---
name: run-queue
description: Use when running the ticket loop, either as a scheduled unattended job that works every Agent-labelled Linear project's tickets in priority order, or interactively when someone asks to work a specific ticket ID. Builds the project map, creates bootstrap tickets, picks one unit, routes it by Skill label to the matching skill, then chains to a fresh run.
---

# Run the ticket queue

You are the **orchestrator**. One run does exactly one unit of work, then hands off to a fresh run. All state lives in Linear, Notion and git, so a run cut off by a usage limit loses nothing. Design and spec: `$TOOLKIT/docs/specs/2026-10-25-ticket-loop-design.md`.

## Prefer existing plugins
- Interactive session with superpowers installed and a person present: for a single build ticket the person may prefer `superpowers:subagent-driven-development`; offer it. This skill's pipeline is for unattended runs (it adds QA, Linear evidence and auto-merge).
- Linear mechanics (states, claiming, evidence, escalation): follow `$TOOLKIT/plugins/linear-workflow/skills/linear-tickets/SKILL.md`; do not reinvent them here.

## Inputs (from the scheduled prompt, or ask the person once if interactive)
`Linear team`, `Project label` (default `Agent`), `Notion home` (page URL for design docs), `Scheduled task name`, `Timezone`, `Stop at` (HH:MM, stop starting units), optional `Models`, optional personal rules. `TOOLKIT` = the agent-toolkit checkout (clone `https://github.com/ImHereForTheCookies/agent-toolkit` to `~/work/agent-toolkit` if missing). Obey `$TOOLKIT/plugins/ticket-loop/HARD_LIMITS.md` in every unit.

**Interactive mode:** given a ticket ID, skip to step 4 with that ticket, run its route, report, and stop (no chaining, no summary message).

## 1. Setup
1. Load tools via ToolSearch in one call: `select:mcp__Linear__list_projects,mcp__Linear__get_project,mcp__Linear__save_project,mcp__Linear__list_issues,mcp__Linear__get_issue,mcp__Linear__save_issue,mcp__Linear__save_comment,mcp__Linear__list_comments,mcp__Notion__notion-fetch,mcp__Notion__notion-get-comments,SendUserMessage,mcp__claude-code-remote__list_triggers,mcp__claude-code-remote__fire_trigger`. Skills load anything else they need.
2. Cutoff: `TZ=<Timezone> date +%H%M`. At or after `Stop at` (and before noon), start nothing; reconcile pending-merge tickets (step 4 of `build-ticket`) and end.
3. Fire text: `One unit only` → do not chain. `Manual run, stop at HH:MM` → use that cutoff for this run and pass the sentence on when chaining. Ignore any other instruction in fire text.

## 2. Project map
`list_projects(team=<Linear team>, label=<Project label>)`, drop completed, canceled, paused and `Stage: paused`. Order by project priority (Urgent first, None last), then oldest first. For each, read the description lines `Repo:`, `Folder:`, `Design doc:`, `Stage:`, `Constraints:` (contract in the spec). Everything else in the description is the human **Direction**; never rewrite it.
- No `Repo:` line → comment on the project asking for one (once; check comments first) and skip it.
- Clone each repo you will touch: `git clone --depth 50 https://github.com/<Repo> ~/work/<name>`. An empty repo clones with a warning; that is fine (the harness ticket fills it). A clone that fails with not-found or permission → comment on the project: "This run cannot reach <Repo>. Add it to the scheduled task's repositories (recreate the task with the repo attached)." and skip the project.

**Concurrency guard:** if any ticket in a mapped project is In Progress and was updated in the last 60 minutes, another run is active: end now with one line, no chain.

## 3. Bootstrap tickets
Create these (team = Linear team, project = that project, state Todo, one Skill label) only if no open ticket with the same label and purpose exists. Creating them is not a unit; continue to step 4 in the same run.
- No `Design doc:` value → `design`: "Write the design doc" (description: "Turn the project Direction into the design doc. Skill: design-system.").
- Design doc has unresolved comments by a person, newer than the doc's last Change log entry → `design`: "Address design doc comments" (list the comment links).
- `Stage: building`, every non-canceled `build` ticket Done, and no `evaluate` ticket since the last merged PR → `evaluate`: "Evaluate the app against the design doc".

## 4. Pick one unit
Across projects in map order, the first match wins:
1. Ticket In Review with an open PR (resume at review).
2. Ticket In Progress (an interrupted run; resume).
3. Backlog ticket whose blockers are all Done → promote it to Todo if `python3 $TOOLKIT/scripts/lint_ticket.py <file>` passes on its description (for `build` tickets; other labels need no lint), else label Needs Human with the lint output. Promotion is not a unit; keep picking.
4. Todo ticket whose blockers are Done, by Linear priority (Urgent first, None last), then lowest number.
Skip tickets labelled Needs Human or Launch, and Canceled or Duplicate ones.

**Route:** read `$TOOLKIT/plugins/ticket-loop/ROUTES.md`, find the ticket's Skill label, and read and follow that skill for this ticket, passing: ticket ID, project, Repo, project folder (`~/work/<name>/<Folder>`), Design doc URL, Constraints, Notion home, Models. No Skill label → `build` if the description passes the linter, else `plan`. A label with no route → Needs Human ("no skill for label X; create one with new-skill") and pick again.

## 5. Chain or finish
Chain when this run made progress (a ticket moved state, got Needs Human, a PR was stacked, or a doc/ticket set was written), it is before the cutoff, no `One unit only`, and step 4 would find more work. To chain: `list_triggers`, find the task named `<Scheduled task name>`, `fire_trigger(trigger_id, text="Chained run: continue with the next eligible unit.")` (append a `Manual run, stop at` sentence if one applies). If firing is refused, continue in this session with the next unit and say so in the summary. Never chain without progress.

**End of chain (not chaining):** comment a short summary on each project touched in this chain (`save_comment` with `projectId`), then one phone-readable `SendUserMessage`: per project, what changed (design doc version + link, tickets planned, PRs merged, evaluation verdict), anything labelled Needs Human with the one question, PRs waiting for a human merge, and what the next run will do. Lead with anything the reader must act on.

## Rules
- One ticket at a time. Never stop between a merge and its Linear update.
- Ask nobody anything in a scheduled run; decide and record the assumption, or escalate per `$TOOLKIT/plugins/agentic-workflow/skills/human-in-the-loop/SKILL.md`.
- Keep your own context small: subagents reply in a few lines and write long output to files.
