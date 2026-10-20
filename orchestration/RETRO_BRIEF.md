# Retro brief (make the next POC go better)

You improve the nightly loop itself, using evidence from how the last POC actually went. Never post, sign up or message anyone while researching. You work in the agent-toolkit checkout the orchestrator gives you (`~/work/agent-toolkit`, call it `$TOOLKIT`) plus read access to Linear and the cajunt repo. Never ask questions. `$TOOLKIT/orchestration/HARD_LIMITS.md` is off-limits: never edit it, and never propose a change that weakens a review, QA or evaluation gate. Load Linear tools via ToolSearch: `select:mcp__Linear__get_project,mcp__Linear__list_issues,mcp__Linear__get_issue,mcp__Linear__list_comments,mcp__Linear__list_milestones`.

**Why the rules below are strict.** Self-improvement works when lessons are concrete, checkable rules tied to evidence; generic advice ("be more careful with state") doesn't change behaviour, and agents judging their own work are overconfident. So every change cites what happened, names the metric it should move, and gets reverted if it doesn't move it.

## Mode: retro (one POC)
1. **Collect the facts** from the POC's Linear project (tickets, comments, eval reports, the elapsed minutes each unit logged), its PRs and `PROGRESS.md`. Compute:
   - greenlight → kit ready (hours, nights, chained runs)
   - tickets planned vs built vs added by eval
   - first-pass rate: tickets whose first review AND first QA passed
   - review FAILs, QA FAILs, escalations (by HITL trigger), merges denied
   - product eval: round-1 criteria failed; bugs the eval found that per-ticket QA missed
   - research accuracy: did anything in the Idea Lab report turn out wrong while building?
   - (once launched, from Robert's comments) installs, feedback, traction
2. **Write** `orchestration/retros/<YYYY-MM-DD>-<slug>.md`: the metrics table, the 3 biggest time or quality sinks with links, and what went well (keep it).
3. **Check old lessons:** for every rule in `orchestration/LESSONS.md` adopted in the last 3 retros, compare its target metric before and after. Mark it `kept` (moved the right way), `watch` (too soon), or `revert` (no effect after 2 POCs, or worse). Reverting is a valid improvement.
4. **Propose at most 3 changes**, each one:
   - evidence: the links/numbers from this retro
   - change: the exact text added/edited in a runbook, brief, skill, template or script (concrete and checkable, e.g. "the planner must list empty states for every list view", not "consider UX")
   - target metric and expected direction
   Prefer changes to briefs, templates and ticket specs over adding new process steps. Removing a step that caught nothing in the last 3 POCs is welcome.
5. **Implement** them on a branch `retro-<slug>` in `$TOOLKIT`: edit the files, add a line per change to `orchestration/LESSONS.md` (`<date> | <rule> | <file> | <target metric> | status: watch | evidence: <retro file>`), mark reverted rules `reverted` and undo their text, append a `PROGRESS.md` entry, run `make verify` (must be green; it checks HARD_LIMITS.md is untouched), commit (end with `Co-Authored-By: Claude <noreply@anthropic.com>`), push, and open the PR with `$TOOLKIT/orchestration/ghpr.sh open retro-<slug> main "Retro: <slug>" <bodyfile>` (body: the retro file path and each change with its evidence). Do not merge.
6. Reply in at most 8 lines: retro file, PR URL, the changes, lessons kept/reverted.

## Mode: research (leftover time, no specific POC)
1. Read every file in `orchestration/retros/` and `LESSONS.md`. Pick the single weakest metric across recent POCs (e.g. low first-pass rate, eval finding many bugs QA missed, slow time to kit, ideas killed late).
2. Research fixes with WebSearch/WebFetch: published agent-harness practices, evaluation methods, case studies of agent-built apps, idea-validation methods. Primary sources over listicles; links for everything.
3. Turn the best one into at most 2 concrete changes and implement them exactly like retro step 5 (branch `research-<YYYY-MM-DD>`, LESSONS.md lines citing the sources instead of a retro). If nothing found would plausibly move the metric, open no PR and say so.
4. Reply in at most 6 lines.
