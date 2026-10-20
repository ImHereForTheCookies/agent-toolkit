# R&D units (run when no build ticket is eligible)

`NIGHTLY.md` sends a run here when no POC project has an eligible ticket. Run the **first** unit below whose condition holds, exactly one per run, then return to `NIGHTLY.md` for chaining and the end-of-run steps. The goal of the whole loop: find app ideas that can gather real users at zero running cost, build them, and hand Robert everything he needs to launch them.

Delegate every unit to one Sonnet subagent (Agent tool, `model: sonnet`, foreground) with the brief named below; you only check its reply and the Linear result. Research subagents may use WebSearch/WebFetch freely, but they never post, sign up, message anyone or spend money.

## Linear layout
- **POC projects** (label `POC`, team ROB): one per prototype. Description lines read by machines: `Folder:`, `Idea:`, `Last grow:`, `Launch:`, `Traction:` (see `pocs/README.md` in cajunt). Update them with `save_project`, editing only the line concerned.
- **Idea Lab** project (team ROB): one issue per idea. States: Backlog = candidate, In Progress = being researched, In Review = validated (score ≥ 70), Done = greenlit (links its POC project), Canceled = killed (comment says why).
- Label **Launch** marks a launch-kit issue in a POC project: Robert's hand-off queue (always also labelled Needs Human). Builds skip it.
- "Active POCs" = POC projects not completed, canceled or paused (cajunt counts). Cap: **3**.

## Units, in priority order

### 1. Launch prep
**Condition:** a POC whose MVP is built (its `MVP` milestone has every ticket Done; without milestones, at least 5 Done tickets and no open non-Launch tickets) and whose description says `Launch: not started` (or has no `Launch:` line).
**Do:** subagent with `$TOOLKIT/orchestration/LAUNCH_BRIEF.md` for that project. It files launch-readiness build tickets and one Launch issue. Then set `Launch: kit ready` once readiness tickets exist and the Launch issue is filed.
A POC already at `Launch: kit ready` or `live` whose description says `Traction: yes` and that has no store-packaging tickets yet also qualifies: same brief, "store packaging" mode.

### 2. Grow (feature research for promising POCs)
**Condition:** a POC with at least one Done ticket, at most 2 open non-Launch tickets, `make -C <folder> verify` green on main, and `Last grow:` older than 7 days or `never`. Prefer launched POCs, then the one with the most Done tickets.
**Promising check (do it before dispatching):** skip the POC (and set `Last grow:` to today with a project comment saying why) if its last two QA reports failed, or if it has 2+ open Needs Human tickets. Otherwise dispatch.
**Do:** subagent with `$TOOLKIT/orchestration/GROWTH_BRIEF.md`. It files at most 3 evidence-backed feature tickets and sets `Last grow:` to today. Those tickets are built by the next chained runs (build comes first).

### 3. Greenlight a validated idea
**Condition:** active POCs < 3 and Idea Lab has an In Review idea.
**Do:** take the highest-scoring In Review idea (ties: oldest). Subagent with this task: "Read `$TOOLKIT/plugins/agentic-workflow/skills/decompose-project/SKILL.md` and `$TOOLKIT/plugins/agentic-workflow/skills/ticket-spec/SKILL.md` and `pocs/README.md` in the cajunt repo. Brief: Idea Lab issue <ID>. Decompose its MVP into at most 10 tickets in milestone `MVP`." Override for this unattended run: **skip the approval step**; the validated Idea Lab issue is the approved brief, and Robert can cancel the project. Fixed tickets: (1) harness: create `pocs/<slug>/` following every rule in `pocs/README.md` (Make contract incl. `setup` and `build`, CLAUDE.md, PROGRESS.md, `.gitignore` with `dist/` and `node_modules/`), `make -C pocs/<slug> setup verify` green, `pocs/ci_changed.sh` picks it up; (2) walking skeleton (taste-checkpoint); (3) installable PWA manifest + service worker with offline load (checked by a Playwright test). Lint every ticket with `scripts/lint_ticket.py`.
Then create, in order: the Linear project (team ROB, label `POC`, name = slug, description with `Folder: pocs/<slug>`, `Idea: <Idea Lab issue URL>`, `Last grow: never`, `Launch: not started`, `Traction: no`, then the one-paragraph pitch), milestone `MVP`, the tickets (blockers first; unblocked ones Todo, the rest Backlog). Set the Idea Lab issue Done with a comment linking the project. Flag the greenlight in the night summary as a taste checkpoint.
If the brief turns out too vague to decompose, do not create the project: comment the open questions on the idea, label it Needs Human, leave it In Review.

### 4. Validate a candidate
**Condition:** Idea Lab has a Backlog candidate.
**Do:** oldest candidate → In Progress → subagent with `$TOOLKIT/orchestration/RESEARCH_BRIEF.md`, mode **validate**, idea <ID>. It replaces the description with the scored report. Score ≥ 70 and no hard gate failed → In Review. Otherwise → Canceled with a comment `Killed: <score>/100, <one-line reason>`.

### 5. Ideate
**Condition:** Idea Lab has fewer than 3 Backlog candidates. (Always true when it's empty, so the night never runs out of R&D work; the cutoff and the usage limit end it.)
**Do:** subagent with `$TOOLKIT/orchestration/RESEARCH_BRIEF.md`, mode **ideate**. It files 5 new Backlog candidates in Idea Lab, deduplicated against every existing Idea Lab issue (including Done and Canceled) and every POC project.

## Bookkeeping per unit
- Every unit leaves a trail: a comment on the Idea Lab issue or the POC project (`save_comment` with `projectId`) stating what was done and links to what was created. The end-of-night summary is built from these.
- A unit "made progress" for chaining when it created or changed at least one Linear issue or project. A subagent that fails twice on the same unit: label the issue Needs Human (or comment on the project), move on, and do not retry that unit tonight.
