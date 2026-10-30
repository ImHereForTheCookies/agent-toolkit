# The night plan: a new POC every night, leftovers for new features and process improvement

`NIGHTLY.md` sends a run here in two places. Before any build ticket, while no POC has been greenlit tonight, it runs one step of **Part A** (the new-POC pipeline). When no build ticket is eligible, it runs one unit of **Part B**. Each time, run the **first** step or unit whose condition holds, exactly one per run, then return to `NIGHTLY.md` for chaining and the end-of-run steps.

**Target:** every night starts a brand-new POC: research and validate an idea, have a planner write the product spec, break it into tickets, then build it to a working app (product evaluation → release → launch kit → retro follow on the next runs or nights). There is no limit on how many POCs are in progress at once: POCs from earlier nights keep getting built and evaluated after tonight's POC has had its turn. Time and tokens left over go to adding the next best feature to existing POCs, then to keeping validated ideas in reserve, then to improving the loop itself.

**The discovery loop feeds itself.** When no ticket is eligible and no higher unit holds, Part B unit 7 keeps the Idea Lab stocked (it validates a Backlog candidate, or ideates when there is none) until 4 validated ideas are in reserve, and Part A turns a validated idea into the next POC. The reserve target sits above what Part A consumes (one idea per night), so discovery does not stall.

**Always a deployable version.** Every POC that has passed product evaluation has a release: a frozen branch `release/<slug>-vN` per version and a moving branch `release/<slug>`, both at the last commit that passed the release gate (`make verify`, `make build`, and a release check of the whole app). Releases are branches, not git tags, because the scheduled session may only push branches (its GitHub connection refuses tag pushes; never work around that). A version branch is never moved after it is created. Work keeps landing on `main`; `release/<slug>` only moves forward, and only when a new increment passes the gate. Robert hosts from `release/<slug>`, never from `main`, so whatever is mid-build never reaches users. A POC that isn't finished when the usage limit hits simply continues on a later night.

**What pre-launch validation can and can't do.** Desk research (complaint mining, competitor reviews) is a cheap filter for whether the *problem* is real. It cannot show that people want *this* app; LLM "synthetic users" are not evidence of demand either (they flatten and stereotype real preferences). The real test is launching, which only Robert can do. So: research filters ideas, a skeptical evaluator playing the target user checks the product works and makes sense, and grow passes after launch use real feedback only.

Delegate every step and unit to one Sonnet subagent (Agent tool, `model: sonnet`, effort `high`, foreground) with the brief named below; you only check its reply and the Linear result. Every unit obeys `$TOOLKIT/orchestration/HARD_LIMITS.md`.

## Linear layout
- **POC projects** (label `POC`, team ROB): one per prototype. Description lines read by machines: `Folder:`, `Idea:`, `Greenlit: <YYYY-MM-DD>`, `Stage: <building|evaluating|kit ready|live at <url>|parked>`, `Eval: <not run|pass|fail>`, `Release: <none|<slug>-vN (YYYY-MM-DD)>`, `Retro: <not run|done>`, `Last grow:`, `Traction:` (see `pocs/README.md` in cajunt). Update them with `save_project` `patch`, editing only the line concerned.
- **Idea Lab** project (team ROB): one issue per idea. Backlog = candidate, In Progress = being researched, In Review = validated (score ≥ 70), Done = greenlit (links its POC project), Canceled = killed (comment says why).
- Label **Launch** marks a launch-kit issue in a POC project: Robert's hand-off queue (always also labelled Needs Human). Builds skip it.
- Label **Speculative** marks a feature the loop chose on its own with leftover tokens (not requested, not from user feedback). Robert can cancel any of them.
- **Launch queue** = Launch issues still labelled Needs Human (Robert hasn't launched them yet). It is reported in the summary but never stops new POCs.
- "Tonight" = since 03:00 America/Los_Angeles today. A POC was **greenlit tonight** when its project was created tonight (its `Greenlit:` line is today).

## Part A: tonight's new POC (runs before build tickets)
`NIGHTLY.md` runs one of these per run, before any build ticket, until a POC has been greenlit tonight. Each step ends with a comment on the Idea Lab project (`save_comment` with `projectId`) whose first line starts with `New POC pipeline:` so later runs can count tonight's attempts. Count attempts from those comments (and from Idea Lab issues validated or created tonight), but always take the **limits** (validations and ideation passes per night) from this file as it reads now, never from an earlier comment: limits change, and a comment's "of max N" or "last allowed" is stale the moment they do. Write counts without a maximum, e.g. `validation 5 tonight`, never `5 of max 6`.

### A1. Start tonight's POC
**Condition:** no POC was greenlit tonight and Idea Lab has an In Review idea.
**Do:** take the highest-scoring In Review idea; a health idea within 5 points of the top score wins (Robert prefers health); remaining ties: oldest. Two subagents in sequence:
1. **Planner:** "Read the Idea Lab issue <ID>, `pocs/README.md` in the cajunt repo, and `$TOOLKIT/orchestration/LESSONS.md`. Write an ambitious but buildable product spec for an MVP the loop can build within about a week of nightly runs: the first user, the core loop they repeat, as many user-visible features as the MVP needs (often 10-30) (not implementation details), what makes it feel finished rather than a demo (first-run screen, empty states, offline, install), and what is out. Stay at the product level; do not choose file layouts. Reply with the spec as markdown." (A planner prevents the under-scoped apps a lone builder produces.)
2. **Decomposer:** "Read `$TOOLKIT/plugins/agentic-workflow/skills/decompose-project/SKILL.md`, `$TOOLKIT/plugins/agentic-workflow/skills/ticket-spec/SKILL.md`, `pocs/README.md` and `$TOOLKIT/orchestration/LESSONS.md`. Turn this spec into as many feature-sized tickets as the MVP needs (up to about 50) in milestone `MVP`, ordered so the core loop works end to end first, each a working vertical slice a user can see, and include the coverage table from the decompose-project skill (every spec feature mapped to a ticket with a Playwright-checked UI path; fix gaps before creating anything)." Override for this unattended run: **skip the approval step**; the validated idea plus the spec is the approved brief, and Robert can cancel the project. Fixed tickets: (1) harness: create `pocs/<slug>/` following every rule in `pocs/README.md` (Make contract incl. `setup` and `build`, CLAUDE.md, PROGRESS.md, SPEC.md holding the spec, `.gitignore` with `dist/` and `node_modules/`), `make -C pocs/<slug> setup verify` green; (2) walking skeleton (taste-checkpoint); one ticket for the installable PWA (manifest, service worker, offline reload checked by Playwright). Lint every ticket with `scripts/lint_ticket.py`.
Then create, in order: the Linear project (team ROB, label `POC`, name = slug, description with `Folder: pocs/<slug>`, `Idea: <Idea Lab issue URL>`, `Greenlit: <today>`, `Stage: building`, `Eval: not run`, `Release: none`, `Retro: not run`, `Last grow: never`, `Traction: no`, then the spec), milestone `MVP`, the tickets (blockers first; unblocked ones Todo, the rest Backlog). Set the Idea Lab issue Done with a comment linking the project. If the brief is too vague to plan, do not create the project: comment the open questions on the idea, label it Needs Human, set it back to Backlog, and the next run tries the next In Review idea (or validates another one).

### A2. Validate a candidate
**Condition:** no POC was greenlit tonight, Idea Lab has no In Review idea, it has a Backlog candidate, and fewer than **12** validations ran tonight.
**Do:** oldest candidate → In Progress → subagent with `$TOOLKIT/orchestration/RESEARCH_BRIEF.md`, mode **validate**. Score ≥ 70 and no hard gate failed → In Review (the next run greenlights it). Otherwise → Canceled with `Killed: <score>/100, <reason>`.

### A3. Ideate
**Condition:** no POC was greenlit tonight, Idea Lab has no In Review idea and no Backlog candidate, and fewer than **4** ideation passes ran tonight.
**Do:** subagent with `RESEARCH_BRIEF.md`, mode **ideate**, asking for 3-5 candidates (it reads `LESSONS.md` for what kinds of ideas worked or failed).

**No POC tonight:** when no Part A step's condition holds and nothing was greenlit tonight (no idea reached 70 within tonight's limits), tonight has no new POC. Never greenlight an idea below 70 (Robert's rule, 2026-10-21). Post one `New POC pipeline: no POC tonight` comment on Idea Lab listing the ideas killed tonight with their scores, report it in the night summary, and carry on with build tickets and Part B. Do not post it twice in one night.

## Part B: after build tickets, in priority order

### 1. Product evaluation
**Condition:** a POC with `Stage: building` whose MVP milestone tickets are all Done (or Needs Human); for a project without milestones (cajunt), all its non-Launch tickets, and `Eval:` is `not run`, or `fail` with every eval fix ticket now Done (second round).
**Do:** set `Stage: evaluating`. Subagent with `$TOOLKIT/orchestration/PRODUCT_EVAL_BRIEF.md` for that project. The round is 1 + the number of `Product eval round` comments already on the project (count them with `list_comments`; never infer it from `Eval:` alone), and you pass that number to the subagent explicitly. It writes the scored report as a project comment and files fix tickets. Round 1 FAIL → fix tickets go to Todo and are built by the next runs; round 1 PASS or round 2 (either verdict) → set `Eval:` accordingly. A round-2 FAIL on a **core** criterion: set `Stage: parked`, label the newest fix ticket Needs Human with the report, and do not prepare a launch kit.

### 2. Release cut
**Condition:** a POC with `Eval: pass` (or round-2 `fail` on non-core criteria only), no In Progress or In Review tickets, no `Release cut failed` comment on its project tonight, and either `Release: none` or commits in its folder on `main` since its last version branch `release/<slug>-vN` (`git fetch origin release/<slug>-vN` then `git diff --quiet FETCH_HEAD origin/main -- <folder>` fails; for cajunt exclude `pocs/`).
**Do:**
1. First release right after product evaluation: the evaluation just graded this exact `main`, so skip to step 3 if no commits landed in the folder since the eval comment.
2. Otherwise: subagent with `$TOOLKIT/orchestration/PRODUCT_EVAL_BRIEF.md`, mode **release check**, comparing `main` against the last version branch. `RELEASE: BLOCKED` → it files regression fix tickets (Todo); do not cut; the next runs build the fixes and this unit runs again.
3. `RELEASE: OK` (or step 1) → run `bash $TOOLKIT/orchestration/release.sh ~/work/cajunt <folder> <slug> --notes /tmp/notes-<slug>.md` (slug `cajunt` for the root project). Exit 0: set `Release: <slug>-vN (<today>)` and comment on the project with the `release/<slug>-vN` and `release/<slug>` branches and the notes. Exit 3: nothing to release; update nothing. Exit 1, or a push denied by the permission classifier: do not retry or work around it (never create tags or refs another way); comment on the project starting with `**Release cut failed**` and the exact error. That comment makes this unit skip the POC for the rest of the night, so the next run moves on to the next unit instead of stopping. Label it Needs Human only if it fails on two different nights (main is unaffected either way).

### 3. Launch kit
**Condition:** a POC with `Stage: evaluating`, `Eval: pass` (or round-2 `fail` on non-core criteria only), a release (`Release:` not `none`), and no Launch issue yet. Also: a POC with `Traction: yes` and no store tickets (store packaging mode).
**Do:** subagent with `$TOOLKIT/orchestration/LAUNCH_BRIEF.md`. Then set `Stage: kit ready`.

### 4. Retro
**Condition:** a POC that reached `kit ready` or `parked` and has `Retro: not run`, and no retro file `orchestration/retros/????-??-??-<slug>.md` (exact slug, so a slug that ends another slug does not match) exists on agent-toolkit `origin/main` **or** on the head branch of an open `waiting on merge` retro PR (check with `git ls-tree --name-only origin/<branch> orchestration/retros/` after `git fetch`, or `ghpr.sh url <branch>`; see NIGHTLY.md stacking rule 7). If such a file exists, the retro is done: skip the subagent and only retry the Linear update `Retro: not run` -> `Retro: done` (a refused write or an unmerged retro PR must never make a retro run twice).
**Do:** subagent with `$TOOLKIT/orchestration/RETRO_BRIEF.md` for that project. It writes `orchestration/retros/<date>-<slug>.md`, updates `orchestration/LESSONS.md`, and opens at most one PR to agent-toolkit with up to 3 evidence-backed process changes. Take that PR through review (`REVIEWER_BRIEF.md`, plus: "This changes the loop itself. FAIL it if it touches `HARD_LIMITS.md`, weakens any review/QA/eval gate, or lacks retro evidence for a change.") and merge it via `ghpr.sh` (run from `~/work/agent-toolkit`). No QA step for process PRs. Set `Retro: done`. Changes take effect from the next chained run, which re-clones the toolkit.

### 5. Grow a launched POC from real feedback
**Condition:** a POC with `Stage: live at ...` where Robert (or relayed user feedback) commented on the project or its Launch issue after `Last grow:`.
**Do:** subagent with `$TOOLKIT/orchestration/GROWTH_BRIEF.md`. Real feedback outranks research. Feedback-driven tickets always outrank speculative ones (unit 6).

### 6. Speculative next-best feature (leftovers)
**Condition:** some POC has a finished evaluation (`Eval: pass`, or a round-2+ `fail` on non-core criteria only), `Stage` is not `parked`, and it has no open tickets (Todo, In Progress, In Review, or Backlog without Needs Human; Launch issues don't count). There is no nightly cap: this keeps going until tokens run out. Pick the eligible POC with the fewest Speculative tickets filed tonight; tie → the one greenlit most recently.
**Do:** subagent with `$TOOLKIT/orchestration/GROWTH_BRIEF.md`, mode **speculative**. It files exactly one ticket labelled `Speculative`, which the next runs build through the normal implement → review → QA → merge flow; the release-cut unit then puts it through the release check before it can reach `release/<slug>`. A speculative feature that fails the release check twice is reverted on `main` by a fix ticket rather than patched further.

### 7. Keep the idea reserve stocked
**Condition:** Idea Lab has fewer than **4** In Review ideas, and fewer than 12 validations and 4 ideation passes ran tonight (Part A's included).
**Do:** if Idea Lab has a Backlog candidate, validate the oldest one exactly as in A2; otherwise ideate as in A3. This lets tomorrow night greenlight straight away.

### 8. Process research (leftovers)
**Condition:** none of the above holds, the reserve has 4+ validated ideas (or tonight's validation and ideation limits are reached), and no process-research PR was opened tonight (an open `waiting on merge` research PR counts as opened; it is not repeated, see NIGHTLY.md stacking rule 7).
**Do:** subagent with `$TOOLKIT/orchestration/RETRO_BRIEF.md`, mode **research**: look across all retros for the weakest metric and research one concrete fix (published harness/eval practices, agent-building case studies, validation methods), then open one PR through the same review as unit 4. If there are no retros yet, end the night instead.

When no unit's condition holds, the night is done.

## Bookkeeping per unit
- Every step and unit leaves a trail: a comment on the Idea Lab issue or project, or the POC project (`save_comment` with `projectId`), saying what was done, with links and the run's elapsed minutes. Retros and the end-of-night summary are built from these.
- A unit "made progress" for chaining when it created or changed at least one Linear issue, project, project comment, or PR. A `Release cut failed` comment counts, since it moves the next run on to other work. A subagent that fails twice on the same unit: label the issue Needs Human (or comment on the project), move on, and don't retry that unit tonight.
