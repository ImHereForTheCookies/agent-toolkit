# The night plan: one full POC per night, leftovers for R&D and process improvement

`NIGHTLY.md` sends a run here when no build ticket is eligible. Run the **first** unit below whose condition holds, exactly one per run, then return to `NIGHTLY.md` for chaining and the end-of-run steps.

**Target:** each night takes one POC from validated idea to a launch kit Robert can act on: plan → build → skeptical product evaluation → launch kit → retro. Time and tokens left over go to keeping validated ideas in reserve for the next night and to improving the loop itself. A POC that isn't finished when the usage limit or the cutoff hits simply continues the next night (depth before breadth: never start a second POC while one is mid-build).

**What pre-launch validation can and can't do.** Desk research (complaint mining, competitor reviews) is a cheap filter for whether the *problem* is real. It cannot show that people want *this* app; LLM "synthetic users" are not evidence of demand either (they flatten and stereotype real preferences). The real test is launching, which only Robert can do. So: research filters ideas, a skeptical evaluator playing the target user checks the product works and makes sense, and grow passes after launch use real feedback only.

Delegate every unit to one Sonnet subagent (Agent tool, `model: sonnet`, effort `high`, foreground) with the brief named below; you only check its reply and the Linear result. Every unit obeys `$TOOLKIT/orchestration/HARD_LIMITS.md`.

## Linear layout
- **POC projects** (label `POC`, team ROB): one per prototype. Description lines read by machines: `Folder:`, `Idea:`, `Greenlit: <YYYY-MM-DD>`, `Stage: <building|evaluating|kit ready|live at <url>|parked>`, `Eval: <not run|pass|fail>`, `Retro: <not run|done>`, `Last grow:`, `Traction:` (see `pocs/README.md` in cajunt). Update them with `save_project` `patch`, editing only the line concerned.
- **Idea Lab** project (team ROB): one issue per idea. Backlog = candidate, In Progress = being researched, In Review = validated (score ≥ 70), Done = greenlit (links its POC project), Canceled = killed (comment says why).
- Label **Launch** marks a launch-kit issue in a POC project: Robert's hand-off queue (always also labelled Needs Human). Builds skip it.
- **Launch queue** = Launch issues still labelled Needs Human (Robert hasn't launched them yet).
- "Tonight" = since 03:00 America/Los_Angeles today.

## Units, in priority order

### 1. Product evaluation
**Condition:** a POC with `Stage: building` whose MVP milestone tickets are all Done (or Needs Human); for a project without milestones (cajunt), all its non-Launch tickets, and `Eval:` is `not run`, or `fail` with every eval fix ticket now Done (second round).
**Do:** set `Stage: evaluating`. Subagent with `$TOOLKIT/orchestration/PRODUCT_EVAL_BRIEF.md` for that project, round 1 or 2. It writes the scored report as a project comment and files fix tickets. Round 1 FAIL → fix tickets go to Todo and are built by the next runs; round 1 PASS or round 2 (either verdict) → set `Eval:` accordingly. A round-2 FAIL on a **core** criterion: set `Stage: parked`, label the newest fix ticket Needs Human with the report, and do not prepare a launch kit.

### 2. Launch kit
**Condition:** a POC with `Stage: evaluating`, `Eval: pass` (or round-2 `fail` on non-core criteria only), and no Launch issue yet. Also: a POC with `Traction: yes` and no store tickets (store packaging mode).
**Do:** subagent with `$TOOLKIT/orchestration/LAUNCH_BRIEF.md`. Then set `Stage: kit ready`.

### 3. Retro
**Condition:** a POC that reached `kit ready` or `parked` and has `Retro: not run`.
**Do:** subagent with `$TOOLKIT/orchestration/RETRO_BRIEF.md` for that project. It writes `orchestration/retros/<date>-<slug>.md`, updates `orchestration/LESSONS.md`, and opens at most one PR to agent-toolkit with up to 3 evidence-backed process changes. Take that PR through review (`REVIEWER_BRIEF.md`, plus: "This changes the loop itself. FAIL it if it touches `HARD_LIMITS.md`, weakens any review/QA/eval gate, or lacks retro evidence for a change.") and merge it via `ghpr.sh` (run from `~/work/agent-toolkit`). No QA step for process PRs. Set `Retro: done`. Changes take effect from the next chained run, which re-clones the toolkit.

### 4. Start tonight's POC
**Condition:** no POC has `Stage: building` or `evaluating`, no POC was greenlit tonight, Idea Lab has an In Review idea, and the launch queue holds fewer than **2** issues. (If the launch queue is full, skip this unit for the night, and send Robert one PushNotification: "2 launch kits are waiting for you; no new POC until one is launched or canceled." Unlaunched apps teach nothing, so building a third would only add to the pile.)
**Do:** take the highest-scoring In Review idea (ties: oldest). Two subagents in sequence:
1. **Planner:** "Read the Idea Lab issue <ID>, `pocs/README.md` in the cajunt repo, and `$TOOLKIT/orchestration/LESSONS.md`. Write an ambitious but buildable product spec for a one-night build: the first user, the core loop they repeat, 8-14 features as user-visible deliverables (not implementation details), what makes it feel finished rather than a demo (first-run screen, empty states, offline, install), and what is out. Stay at the product level; do not choose file layouts. Reply with the spec as markdown." (A planner prevents the under-scoped apps a lone builder produces.)
2. **Decomposer:** "Read `$TOOLKIT/plugins/agentic-workflow/skills/decompose-project/SKILL.md`, `$TOOLKIT/plugins/agentic-workflow/skills/ticket-spec/SKILL.md`, `pocs/README.md` and `$TOOLKIT/orchestration/LESSONS.md`. Turn this spec into 6-10 feature-sized tickets in milestone `MVP`, each a working vertical slice a user can see." Override for this unattended run: **skip the approval step**; the validated idea plus the spec is the approved brief, and Robert can cancel the project. Fixed tickets: (1) harness: create `pocs/<slug>/` following every rule in `pocs/README.md` (Make contract incl. `setup` and `build`, CLAUDE.md, PROGRESS.md, SPEC.md holding the spec, `.gitignore` with `dist/` and `node_modules/`), `make -C pocs/<slug> setup verify` green; (2) walking skeleton (taste-checkpoint); one ticket for the installable PWA (manifest, service worker, offline reload checked by Playwright). Lint every ticket with `scripts/lint_ticket.py`.
Then create, in order: the Linear project (team ROB, label `POC`, name = slug, description with `Folder: pocs/<slug>`, `Idea: <Idea Lab issue URL>`, `Greenlit: <today>`, `Stage: building`, `Eval: not run`, `Retro: not run`, `Last grow: never`, `Traction: no`, then the spec), milestone `MVP`, the tickets (blockers first; unblocked ones Todo, the rest Backlog). Set the Idea Lab issue Done with a comment linking the project. If the brief is too vague to plan, do not create the project: comment the open questions on the idea, label it Needs Human, and try the next In Review idea in the next run.

### 5. Grow a launched POC from real feedback
**Condition:** a POC with `Stage: live at ...` where Robert (or relayed user feedback) commented on the project or its Launch issue after `Last grow:`.
**Do:** subagent with `$TOOLKIT/orchestration/GROWTH_BRIEF.md`. Real feedback outranks research. Pre-launch POCs are never grown; the product evaluation is their quality pass.

### 6. Keep the idea reserve stocked: validate
**Condition:** Idea Lab has fewer than 2 In Review ideas and has a Backlog candidate.
**Do:** oldest candidate → In Progress → subagent with `$TOOLKIT/orchestration/RESEARCH_BRIEF.md`, mode **validate**. Score ≥ 70 and no hard gate failed → In Review. Otherwise → Canceled with `Killed: <score>/100, <reason>`.

### 7. Ideate
**Condition:** Idea Lab has fewer than 2 In Review ideas and fewer than 3 Backlog candidates.
**Do:** subagent with `RESEARCH_BRIEF.md`, mode **ideate** (reads `LESSONS.md` for what kinds of ideas worked or failed).

### 8. Process research (leftovers)
**Condition:** none of the above holds, the reserve has 2+ validated ideas, and no process-research PR was opened tonight.
**Do:** subagent with `$TOOLKIT/orchestration/RETRO_BRIEF.md`, mode **research**: look across all retros for the weakest metric and research one concrete fix (published harness/eval practices, agent-building case studies, validation methods), then open one PR through the same review as unit 3. If there are no retros yet, end the night instead.

When no unit's condition holds, the night is done.

## Bookkeeping per unit
- Every unit leaves a trail: a comment on the Idea Lab issue or POC project (`save_comment` with `projectId`) saying what was done, with links and the run's elapsed minutes. Retros and the end-of-night summary are built from these.
- A unit "made progress" for chaining when it created or changed at least one Linear issue, project, or PR. A subagent that fails twice on the same unit: label the issue Needs Human (or comment on the project), move on, and don't retry that unit tonight.
