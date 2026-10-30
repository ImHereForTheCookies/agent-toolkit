---
name: build-ticket
description: Use when a Linear ticket labelled build (or an unlabelled ticket that passes the ticket linter) must be implemented unattended - implementer, independent reviewer and QA subagents, then auto-merge on PASS, stacking PRs when a merge is denied, and closing the ticket with evidence.
---

# Build one ticket through merge

You orchestrate; subagents explore, implement, review and QA, each on the model `$TOOLKIT/plugins/ticket-loop/MODELS.md` gives its stage. You never write feature code.

## Prefer existing plugins
- **superpowers**: implementers follow `test-driven-development`, `writing-plans` (for their own step list) and `verification-before-completion` when available; reviewers may use `requesting-code-review`'s checklist. Never `brainstorming` or questions: the ticket is the approved spec.
- **Explore stage:** use Claude Code's built-in read-only `Explore` agent type (`subagent_type: Explore`) with the explore-stage model. A code index plugin such as `code-parser`, if installed, can cut what it reads.
- **Review stage:** if Anthropic's official `code-review` plugin is installed, the reviewer also runs it on the diff and weighs its findings against REVIEWER_BRIEF; otherwise superpowers `requesting-code-review`.
- **Fix round:** for a failing test or a QA bug, the implementer follows superpowers `systematic-debugging` before changing code.
- Interactive, with a person present: `superpowers:subagent-driven-development` is a good alternative to this pipeline.
- What this skill adds: separate QA that uses the app, Linear evidence, auto-merge and stacking.

## Inputs
Ticket ID, Repo, repo path, project folder, Design doc URL, Constraints, Tier, Models (an override). Every subagent prompt includes: `Repo path: <repo path>`, `Project folder: <folder>`, `TOOLKIT=<path>`, `Design doc: <url>`, `Constraints: <text>`. "Setup" below means `make -C <folder> setup` only if that target exists (`make -C <folder> -n setup >/dev/null 2>&1`).

## 0. Base branch
- **Empty repo** (no `origin/main`): seed it first so the normal PR flow works: in the repo path, `git checkout -q -b main && git commit -q --allow-empty -m "Initial commit" && git push -q origin main`. Base = `main`.
- Otherwise base = the branch of the ticket's newest blocker labelled `Awaiting Merge` (the top of that stack), else `main`.

## Steps
A0. **Explore** (read-only; explore-stage model). Subagent: "Ticket <ID> in <repo path>, base `<base>`. Do not edit anything. Write `~/work/briefs/<ID>.md`, at most 80 lines: the files and functions this ticket touches or calls (paths and signatures), the existing patterns to copy (one example each), the test files and commands that cover them, and anything in CLAUDE.md, PROGRESS.md or recent commits that constrains the change. Use `$TOOLKIT/plugins/code-navigation/skills/navigate-codebase/SKILL.md` if the repo is large. Reply in 3 lines." Skip for an empty repo (the harness ticket) and for `haiku-low` tickets.
A. **Implement** (the ticket's tier). Subagent: "Read `~/work/briefs/<ID>.md` first (if it exists) for orientation; check any file it names before editing it, and open other files only when the brief doesn't cover something. Read and follow `$TOOLKIT/orchestration/IMPLEMENTER_BRIEF.md` for ticket <ID>, with these overrides, which win over the brief: the base branch is `<base>`: in step 2 run `git fetch -q origin && git checkout -q -B <base> origin/<base>` and the baseline verify on it; create your branch from it; in step 7 open the PR with base `<base>`<, and make the first body line `**Stacked on #<parent PR>; merge after it.**` when base is not main>. Run setup before verify (skip it if the target doesn't exist)." Reply `ESCALATE:` → escalate (below), move on.
B. **Review** (review-stage model). A *different* subagent: "Read and follow `$TOOLKIT/orchestration/REVIEWER_BRIEF.md`. Ticket <ID>, branch <b>, PR <url>, repo, project folder. Override: diff against the base, `git diff origin/<base>...<b>`, not origin/main. Also check the change respects the Constraints."
C. **QA** (after review PASS; QA-stage model). A separate subagent: "Read and follow `$TOOLKIT/plugins/agentic-workflow/skills/qa-ticket/SKILL.md` for ticket <ID>, branch <b>, repo path <project folder>." For taste checkpoints, attach its screenshot paths to the PR and Linear comments.
D. **Merge** only on review PASS and QA PASS (or SKIPPED with a reason). Write verdict + QA report to a file; from the repo run `$TOOLKIT/orchestration/ghpr.sh comment <b> <file>`; then, if base is `main`, `$TOOLKIT/orchestration/ghpr.sh merge <b>`. Merged → evidence comment per `linear-tickets`, state Done.
   - **FAIL** (review or QA): one fresh implementer one tier above the ticket's (`opus-high` stays; the label is not changed; review and QA keep the ticket's tier) with the same overrides plus "Fix these findings: ...", then review and QA again. Second FAIL → escalate, leave the PR open.
   - **Base is not main, or the merge is denied or impossible:** not an escalation. Leave the ticket In Review, add the label `Awaiting Merge`, comment `**Review PASS, QA PASS, waiting on merge**` (PR link, head sha, base, and `Base sha: <sha of origin/<base> the branch was built on>`). run-queue then treats it as a satisfied blocker and never re-picks it.
E. **After a merge:** `git -C <repo> fetch -q origin && git -C <repo> checkout -q -B main origin/main`, setup, `make -C <folder> verify`. Red main → create a ticket "Fix red main: <failure>" (labels `build` and `sonnet-high`, Todo, priority Urgent, failure log in the description, written to pass the linter). Do not label it Needs Human: run-queue makes it the project's only eligible ticket until it is Done.

## Stacking (merges denied unattended)
1. A new ticket whose blocker is pending builds on the newest `Awaiting Merge` branch in that blocker chain (step 0).
2. **Reconcile** (run-queue does this every run): for each `Awaiting Merge` ticket, check its PR. Merged → remove the label, post the evidence comment, set Done, and retarget any child PR whose base was its branch: `gh api -X PATCH repos/<repo>/pulls/<n> -f base=main`. Its base became `main` and it is unmerged → try `ghpr.sh merge` once (bottom of the stack first); success → same as merged. Closed without merge → remove the label, comment, label Needs Human, and label every ticket stacked on it Needs Human too ("parent PR closed; rebase onto main or rebuild").
3. Before reviewing a stacked child, confirm the parent head equals the `Base sha:` recorded on the child (its Awaiting Merge comment or PR body); if it moved, `git merge origin/<parent>` into the child (never force-push) and re-review.
4. Cap: 8 open `Awaiting Merge` PRs per repo. At the cap, build nothing new in that project; the end-of-chain summary names the bottom PR to merge.
5. A merge denied once is not retried or worked around in the same run.

## Escalation
Per `$TOOLKIT/plugins/agentic-workflow/skills/human-in-the-loop/SKILL.md` (six triggers; label Needs Human + comment; never wait). Denied merges and taste are not escalations.

## Known environment facts
- `gh pr create/merge` (GraphQL) are blocked in cloud sessions; `ghpr.sh` uses REST.
- Push from a shallow clone after `git fetch origin main` to avoid HTTP 413.
- `/bin/sh` may be dash; scripts use bash.
