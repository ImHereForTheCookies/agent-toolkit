# The night plan: one full POC per night, leftovers for R&D and process improvement

`NIGHTLY.md` sends a run here when no build ticket is eligible. Run the **first** unit below whose condition holds, exactly one per run, then return to `NIGHTLY.md` for chaining and the end-of-run steps.

**Target:** each night takes one POC from validated idea to a launch kit Robert can act on: plan → build → skeptical product evaluation → first release → launch kit → retro. Time and tokens left over go to keeping validated ideas in reserve, then to speculative next-best features on finished POCs, then to improving the loop itself.

**The discovery loop feeds itself.** When no ticket is eligible and no higher unit holds, units 7 (validate) and 8 (ideate) keep the Idea Lab stocked and unit 5 turns validated ideas into POCs. Discovery is the default sink for leftover time, so it must not stall just because the launch queue is full: the reserve targets in units 7 and 8 sit above what unit 5 consumes.

**Always a deployable version.** Every POC that has passed product evaluation has a release: an annotated git tag `<slug>-vN` and a branch `release/<slug>` pointing at the last commit that passed the release gate (`make verify`, `make build`, and a release check of the whole app). Work keeps landing on `main`; the release branch only moves forward, and only when a new increment passes the gate. Robert hosts from `release/<slug>`, never from `main`, so whatever is mid-build never reaches users. A POC that isn't finished when the usage limit hits simply continues the next night (depth before breadth: never start a second POC while one is mid-build).

**What pre-launch validation can and can't do.** Desk research (complaint mining, competitor reviews) is a cheap filter for whether the *problem* is real. It cannot show that people want *this* app; LLM "synthetic users" are not evidence of demand either (they flatten and stereotype real preferences). The real test is launching, which only Robert can do. So: research filters ideas, a skeptical evaluator playing the target user checks the product works and makes sense, and grow passes after launch use real feedback only.

Delegate every unit to one Sonnet subagent (Agent tool, `model: sonnet`, effort `high`, foreground) with the brief named below; you only check its reply and the Linear result. Every unit obeys `$TOOLKIT/orchestration/HARD_LIMITS.md`.

## Linear layout
- **POC projects** (label `POC`, team ROB): one per prototype. Description lines read by machines: `Folder:`, `Idea:`, `Greenlit: <YYYY-MM-DD>`, `Stage: <building|evaluating|kit ready|live at <url>|parked>`, `Eval: <not run|pass|fail>`, `Release: <none|<slug>-vN (YYYY-MM-DD)>`, `Retro: <not run|done>`, `Last grow:`, `Traction:` (see `pocs/README.md` in cajunt). Update them with `save_project` `patch`, editing only the line concerned.
- **Idea Lab** project (team ROB): one issue per idea. Backlog = candidate, In Progress = being researched, In Review = validated (score ≥ 70), Done = greenlit (links its POC project), Canceled = killed (comment says why).
- Label **Launch** marks a launch-kit issue in a POC project: Robert's hand-off queue (always also labelled Needs Human). Builds skip it.
- Label **Speculative** marks a feature the loop chose on its own with leftover tokens (not requested, not from user feedback). Robert can cancel any of them.
- **Launch queue** = Launch issues still labelled Needs Human (Robert hasn't launched them yet).
- "Tonight" = since 03:00 America/Los_Angeles today.

## Units, in priority order

### 1. Product evaluation
**Condition:** a POC with `Stage: building` whose MVP milestone tickets are all Done (or Needs Human); for a project without milestones (cajunt), all its non-Launch tickets, and `Eval:` is `not run`, or `fail` with every eval fix ticket now Done (second round).
**Do:** set `Stage: evaluating`. Subagent with `$TOOLKIT/orchestration/PRODUCT_EVAL_BRIEF.md` for that project. The round is 1 + the number of `Product eval round` comments already on the project (count them with `list_comments`; never infer it from `Eval:` alone), and you pass that number to the subagent explicitly. It writes the scored report as a project comment and files fix tickets. Round 1 FAIL → fix tickets go to Todo and are built by the next runs; round 1 PASS or round 2 (either verdict) → set `Eval:` accordingly. A round-2 FAIL on a **core** criterion: set `Stage: parked`, label the newest fix ticket Needs Human with the report, and do not prepare a launch kit.

### 2. Release cut
**Condition:** a POC with `Eval: pass` (or round-2 `fail` on non-core criteria only), no In Progress or In Review tickets, and either `Release: none` or commits in its folder on `main` since its last `<slug>-vN` tag (`git diff --quiet <tag> origin/main -- <folder>` fails; for cajunt exclude `pocs/`).
**Do:**
1. First release right after product evaluation: the evaluation just graded this exact `main`, so skip to step 3 if no commits landed in the folder since the eval comment.
2. Otherwise: subagent with `$TOOLKIT/orchestration/PRODUCT_EVAL_BRIEF.md`, mode **release check**, comparing `main` against the last release tag. `RELEASE: BLOCKED` → it files regression fix tickets (Todo); do not cut; the next runs build the fixes and this unit runs again.
3. `RELEASE: OK` (or step 1) → run `bash $TOOLKIT/orchestration/release.sh ~/work/cajunt <folder> <slug> --notes /tmp/notes-<slug>.md` (slug `cajunt` for the root project). Exit 0: set `Release: <tag> (<today>)` and comment on the project with the tag, the `release/<slug>` branch, and the notes. Exit 3: nothing to release; update nothing. Exit 1, or a push denied by the permission classifier: do not retry or work around it; comment the error on the project, label it Needs Human only if it fails twice on different nights, and move on (main is unaffected).

### 3. Launch kit
**Condition:** a POC with `Stage: evaluating`, `Eval: pass` (or round-2 `fail` on non-core criteria only), a release (`Release:` not `none`), and no Launch issue yet. Also: a POC with `Traction: yes` and no store tickets (store packaging mode).
**Do:** subagent with `$TOOLKIT/orchestration/LAUNCH_BRIEF.md`. Then set `Stage: kit ready`.

### 4. Retro
**Condition:** a POC that reached `kit ready` or `parked` and has `Retro: not run`, and no `orchestration/retros/*-<slug>.md` exists on agent-toolkit `origin/main`. If that file already exists, the retro is done: skip the subagent and only retry the Linear update `Retro: not run` -> `Retro: done` (a refused write must never make a retro run twice).
**Do:** subagent with `$TOOLKIT/orchestration/RETRO_BRIEF.md` for that project. It writes `orchestration/retros/<date>-<slug>.md`, updates `orchestration/LESSONS.md`, and opens at most one PR to agent-toolkit with up to 3 evidence-backed process changes. Take that PR through review (`REVIEWER_BRIEF.md`, plus: "This changes the loop itself. FAIL it if it touches `HARD_LIMITS.md`, weakens any review/QA/eval gate, or lacks retro evidence for a change.") and merge it via `ghpr.sh` (run from `~/work/agent-toolkit`). No QA step for process PRs. Set `Retro: done`. Changes take effect from the next chained run, which re-clones the toolkit.

### 5. Start tonight's POC
**Condition:** no POC has `Stage: building` or `evaluating`, no POC was greenlit tonight, Idea Lab has an In Review idea, and the launch queue holds fewer than **2** issues. (If the launch queue is full, skip this unit for the night, and send Robert one PushNotification: "2 launch kits are waiting for you; no new POC until one is launched or canceled." Unlaunched apps teach nothing, so building a third would only add to the pile.)
**Do:** take the highest-scoring In Review idea (ties: oldest). Two subagents in sequence:
1. **Planner:** "Read the Idea Lab issue <ID>, `pocs/README.md` in the cajunt repo, and `$TOOLKIT/orchestration/LESSONS.md`. Write an ambitious but buildable product spec for a one-night build: the first user, the core loop they repeat, 8-14 features as user-visible deliverables (not implementation details), what makes it feel finished rather than a demo (first-run screen, empty states, offline, install), and what is out. Stay at the product level; do not choose file layouts. Reply with the spec as markdown." (A planner prevents the under-scoped apps a lone builder produces.)
2. **Decomposer:** "Read `$TOOLKIT/plugins/agentic-workflow/skills/decompose-project/SKILL.md`, `$TOOLKIT/plugins/agentic-workflow/skills/ticket-spec/SKILL.md`, `pocs/README.md` and `$TOOLKIT/orchestration/LESSONS.md`. Turn this spec into 6-10 feature-sized tickets in milestone `MVP`, each a working vertical slice a user can see, and include the coverage table from the decompose-project skill (every spec feature mapped to a ticket with a Playwright-checked UI path; fix gaps before creating anything)." Override for this unattended run: **skip the approval step**; the validated idea plus the spec is the approved brief, and Robert can cancel the project. Fixed tickets: (1) harness: create `pocs/<slug>/` following every rule in `pocs/README.md` (Make contract incl. `setup` and `build`, CLAUDE.md, PROGRESS.md, SPEC.md holding the spec, `.gitignore` with `dist/` and `node_modules/`), `make -C pocs/<slug> setup verify` green; (2) walking skeleton (taste-checkpoint); one ticket for the installable PWA (manifest, service worker, offline reload checked by Playwright). Lint every ticket with `scripts/lint_ticket.py`.
Then create, in order: the Linear project (team ROB, label `POC`, name = slug, description with `Folder: pocs/<slug>`, `Idea: <Idea Lab issue URL>`, `Greenlit: <today>`, `Stage: building`, `Eval: not run`, `Release: none`, `Retro: not run`, `Last grow: never`, `Traction: no`, then the spec), milestone `MVP`, the tickets (blockers first; unblocked ones Todo, the rest Backlog). Set the Idea Lab issue Done with a comment linking the project. If the brief is too vague to plan, do not create the project: comment the open questions on the idea, label it Needs Human, and try the next In Review idea in the next run.

### 6. Grow a launched POC from real feedback
**Condition:** a POC with `Stage: live at ...` where Robert (or relayed user feedback) commented on the project or its Launch issue after `Last grow:`.
**Do:** subagent with `$TOOLKIT/orchestration/GROWTH_BRIEF.md`. Real feedback outranks research. Feedback-driven tickets always outrank speculative ones (unit 9).

### 7. Keep the idea reserve stocked: validate
**Condition:** Idea Lab has fewer than **4** In Review ideas and has a Backlog candidate.
**Do:** oldest candidate → In Progress → subagent with `$TOOLKIT/orchestration/RESEARCH_BRIEF.md`, mode **validate**. Score ≥ 70 and no hard gate failed → In Review. Otherwise → Canceled with `Killed: <score>/100, <reason>`.

### 8. Ideate
**Condition:** Idea Lab has fewer than **4** In Review ideas and fewer than **5** Backlog candidates.
**Do:** subagent with `RESEARCH_BRIEF.md`, mode **ideate** (reads `LESSONS.md` for what kinds of ideas worked or failed).

### 9. Speculative next-best feature (leftovers)
**Condition:** the idea reserve has 4+ validated ideas (units 7 and 8 no longer hold; or Idea Lab research is exhausted for tonight), fewer than **2** Speculative tickets were filed tonight across all POCs, and some POC has a release, no open tickets, and `Stage` not `parked`. Pick the POC greenlit most recently; tie → the one with the fewest Speculative tickets ever.
**Do:** subagent with `$TOOLKIT/orchestration/GROWTH_BRIEF.md`, mode **speculative**. It files exactly one ticket labelled `Speculative`, which the next runs build through the normal implement → review → QA → merge flow; the release-cut unit then puts it through the release check before it can reach `release/<slug>`. A speculative feature that fails the release check twice is reverted on `main` by a fix ticket rather than patched further.

### 10. Process research (leftovers)
**Condition:** none of the above holds, the reserve has 4+ validated ideas, and no process-research PR was opened tonight.
**Do:** subagent with `$TOOLKIT/orchestration/RETRO_BRIEF.md`, mode **research**: look across all retros for the weakest metric and research one concrete fix (published harness/eval practices, agent-building case studies, validation methods), then open one PR through the same review as unit 3. If there are no retros yet, end the night instead.

When no unit's condition holds, the night is done.

## Bookkeeping per unit
- Every unit leaves a trail: a comment on the Idea Lab issue or POC project (`save_comment` with `projectId`) saying what was done, with links and the run's elapsed minutes. Retros and the end-of-night summary are built from these.
- A unit "made progress" for chaining when it created or changed at least one Linear issue, project, or PR. A subagent that fails twice on the same unit: label the issue Needs Human (or comment on the project), move on, and don't retry that unit tonight.
