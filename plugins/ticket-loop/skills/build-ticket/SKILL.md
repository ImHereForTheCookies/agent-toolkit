---
name: build-ticket
description: Use when a Linear ticket labelled build (or an unlabelled ticket that passes the ticket linter) must be implemented unattended - implementer, independent reviewer and QA subagents, then auto-merge on PASS, stacking PRs when a merge is denied, and closing the ticket with evidence.
---

# Build one ticket through merge

You orchestrate; Sonnet subagents implement, review and QA. You never write feature code.

## Prefer existing plugins
- **superpowers**: implementers follow `test-driven-development`, `writing-plans` (for their own step list) and `verification-before-completion` when available; reviewers may use `requesting-code-review`'s checklist. Never `brainstorming` or questions: the ticket is the approved spec.
- Interactive, with a person present: `superpowers:subagent-driven-development` is a good alternative to this pipeline.
- What this skill adds: separate QA that uses the app, Linear evidence, auto-merge and stacking.

## Inputs
Ticket ID, Repo (cloned at `~/work/<name>`), project folder, Design doc URL, Constraints, Models (default `sonnet`, effort high). Every subagent prompt includes: `Repo path: ~/work/<name>`, `Project folder: <folder>`, `TOOLKIT=<path>`, `Design doc: <url>`, `Constraints: <text>`.

## Steps
A. **Implement.** Subagent: "Read and follow `$TOOLKIT/orchestration/IMPLEMENTER_BRIEF.md`. Ticket <ID>. Base branch: <main or stack parent>." Empty repo: the harness ticket commits straight to the first commit of `main` as the brief says. Reply `ESCALATE:` → escalate (below), move on.
B. **Review.** A *different* subagent: "Read and follow `$TOOLKIT/orchestration/REVIEWER_BRIEF.md`. Ticket <ID>, branch <b>, PR <url>, repo, project folder. Also check the change respects the Constraints." Review its own diff only (`git diff <base>...<head>`).
C. **QA** (after review PASS). A separate subagent: "Read and follow `$TOOLKIT/plugins/agentic-workflow/skills/qa-ticket/SKILL.md` for ticket <ID>, branch <b>, repo path <project folder>." For taste checkpoints, attach its screenshot paths to the PR and Linear comments.
D. **Merge** only on review PASS and QA PASS (or SKIPPED with a reason): write verdict + QA report to a file; from the repo run `$TOOLKIT/orchestration/ghpr.sh comment <b> <file>` then `$TOOLKIT/orchestration/ghpr.sh merge <b>`. Linear: evidence comment per `linear-tickets`, state Done.
   - **FAIL** (review or QA): one fresh implementer with "Fix these findings: ...", then review and QA again. Second FAIL → escalate, leave the PR open.
   - **Merge denied or impossible:** not an escalation. Comment the verdict on the PR, set the ticket In Review with `**Review PASS, QA PASS, waiting on merge**` (PR link, head sha), and stack the next ticket on this branch.
E. **After a merge:** `git -C <repo> fetch -q origin && git -C <repo> checkout -q -B main origin/main`, `make -C <folder> setup verify`. Red main → create a `build` ticket "Fix red main: <failure>" (Todo, Urgent), label it Needs Human, and start nothing else in this project this chain.

## Stacking (merges denied unattended)
1. Base for a new ticket = the branch of its newest pending-merge blocker, else the top of the stack, else `main`. The PR body starts `**Stacked on #<parent>; merge after it.**`.
2. Reconcile first in every run: a pending-merge ticket whose PR is merged → Done with evidence; retarget its child PR to `main` with `gh api -X PATCH repos/<repo>/pulls/<n> -f base=main`.
3. Before reviewing a stacked child, confirm the parent head is unchanged; if it moved, `git merge <parent>` into the child (never force-push) and re-review.
4. Cap: 8 open stacked PRs per repo. At the cap, stop building in that project and name the bottom PR to merge in the end-of-chain summary.
5. Try merging the bottom-most reviewed PR first; if denied once, do not retry or work around it this run.

## Escalation
Per `$TOOLKIT/plugins/agentic-workflow/skills/human-in-the-loop/SKILL.md` (six triggers; label Needs Human + comment; never wait). Denied merges and taste are not escalations.

## Known environment facts
- `gh pr create/merge` (GraphQL) are blocked in cloud sessions; `ghpr.sh` uses REST.
- Push from a shallow clone after `git fetch origin main` to avoid HTTP 413.
- `/bin/sh` may be dash; scripts use bash.
