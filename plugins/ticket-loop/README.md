# ticket-loop

One general, unattended job for building apps with agents. Linear holds the work, Notion holds the design docs people read, GitHub holds the code. Every ticket carries one **Skill** label (`design`, `plan`, `build`, `evaluate`) and the job routes it to the matching skill (`ROUTES.md`). Humans give direction and change course later; they are never a gate. Design: `docs/specs/2026-10-25-ticket-loop-design.md`.

## Set up a project (once)
1. GitHub: create an empty repo for the app.
2. Linear: create a project with the project label `Agent` and a description from `templates/project-description.md` (Direction + `Repo:` line). Create the issue label group `Skill` (single-select) with `design`, `plan`, `build`, `evaluate`, plus the labels `Needs Human`, `Awaiting Merge` and `Launch` if your team lacks them. Never put `Agent` on a project another loop already runs (for example the cajunt POC projects).
3. Notion: one page to hold design docs (your "Notion home"); connect the Notion and Linear connectors to Claude.
4. That's it: the next run creates the design ticket itself.

## Run it
- **Scheduled:** create a scheduled task (Claude Code on the web) whose prompt is `templates/scheduled-prompt.md` filled in (about 15 lines, the only private part). Attach the agent-toolkit repo and every project repo; a task's repo access is fixed when it is created, so adding a project in a new repo means recreating the task with that repo attached.
- **By hand:** install this marketplace (`/plugin marketplace add ImHereForTheCookies/agent-toolkit`, then `/plugin install ticket-loop@agent-toolkit`) and ask Claude to run the ticket queue, or to work one ticket ("work ROB-42 with the ticket loop").

## Steer it
- Change what gets built: edit the Linear project's Direction, or comment on the design doc. The next run files a design ticket and revises the doc, then re-plans.
- Add work: create a ticket with a Skill label (or none: rough ideas get planned, spec'd tickets get built).
- Stop a project: set its status to Paused, or `Stage: paused`.

## Add a kind of work
Use the `new-skill` skill: it searches existing plugin marketplaces first, then writes a skill that delegates to the best plugin where one fits.
