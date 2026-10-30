---
name: review-runs
description: Use when reviewing the ticket loop's previous night (usually as a scheduled job shortly before the loop starts) to find recurring friction in its skills, templates and prompts and make small, evidence-backed fixes that improve clarity and quality. Leans toward no change when unsure.
---

# Review last night's runs and make small fixes

You improve the loop's **instructions**, not the apps it builds. Optimize for clarity and quality of the skills, templates, briefs and prompts. The default outcome of a review is **no change**: most friction is a one-off, and every rule added makes the instructions longer and harder to follow. A good night is one where you change nothing and write down what you are watching.

Scheduled runs cannot read each other's conversations. Your evidence is what the loop leaves behind: the run log, Linear, git and PRs, and the scheduled task's run status.

## Prefer existing plugins
- **superpowers `writing-skills`** (if available): follow it when editing a skill, especially its advice to keep skills short and to test that a change fixes the observed failure.
- **superpowers `receiving-code-review`** mindset for your own candidate fixes: verify each against evidence before acting, and push back on yourself.
- **superpowers `diagnosing-superpowers`**: if the friction is inside a superpowers skill, write its bug report for the person instead of patching around it here.

## Inputs (from the scheduled prompt)
`Run log` (Notion page URL), `Loop task name` (the ticket loop's scheduled task), `Linear team`, `Project label`, `Timezone`, optional `Toolkit branch` (the branch the loop runs from, default `main`), optional personal rules. `TOOLKIT` = an agent-toolkit checkout of that branch. Obey `$TOOLKIT/plugins/ticket-loop/HARD_LIMITS.md`.

## 1. Gather evidence (window: since the last review entry on the run log, else the last 24 hours)
1. Load tools in one call: `select:mcp__Notion__notion-fetch,mcp__Notion__notion-update-page,mcp__Linear__list_projects,mcp__Linear__list_issues,mcp__Linear__get_issue,mcp__Linear__list_comments,mcp__Linear__save_issue,mcp__Linear__save_comment,mcp__claude-code-remote__list_triggers,mcp__claude-code-remote__update_trigger,SendUserMessage`.
2. **Run log:** the entries in the window, plus the Reviews section (past changes and the Watching list).
3. **Scheduled task status:** `list_triggers`; for the loop task note `last_run` status and `failure_reason` (usage limit, failure) and how long it ran.
4. **Linear:** for projects with the project label, tickets updated in the window: state changes, `Needs Human` escalations and their questions, evaluate verdicts, tickets that went In Progress and never finished, repeated reviewer or QA failures in comments.
5. **Git:** PRs opened, merged or closed in the window on the toolkit and on each project's `Repo:` (`gh api repos/<repo>/pulls?state=all&sort=updated`), and review or QA FAIL comments on them.
6. Read the current text of every instruction file you might change before judging it.

Keep your own context small: one subagent (model `sonnet`) may gather and summarize items 4 and 5 into `~/work/review/evidence.md` and reply in at most 12 lines.

## 2. Find candidate problems
List each friction point with its evidence (run log entry, ticket, PR, error text). Group the same cause together. For each group decide:

- **Change** only when all of these hold: it happened in 2 or more units or nights, or it stopped or stalled a unit outright; the evidence shows the cause, not just the symptom; and a small edit to an instruction would plausibly have prevented it.
- **No change** for one-off environment events (usage limits, network blips, an outage), for things the model handled well anyway, for taste, and whenever you are unsure. Add the item to **Watching** with its evidence. Drop a Watching item after 7 nights without a repeat.
- Do not undo or reverse a change made in the last 7 nights unless the evidence shows that change caused a failure. Flip-flopping is worse than either version.
- Model tiers: compare each unit's `Model` label with its outcome. A tier that keeps failing review, or a tier above `sonnet-medium` that keeps passing first time on small tickets, is evidence for adjusting the rubric in `$TOOLKIT/plugins/ticket-loop/MODELS.md` (same bar as any other change).
- At most **3 changes** per review. Pick the ones with the largest cost in lost work.

## 3. Choose where each fix lives
- **Shared** (would help anyone running the toolkit): edit the skill, template, brief or script in agent-toolkit. Prefer clarifying or deleting text over adding rules. Generalize from the incident: never name a person, project, ticket or private URL in shared files.
- **Personal** (only this person's setup): the loop's scheduled prompt, via `update_trigger`. Keep its personal rules few. If a personal rule has become useful to everyone, move it into the toolkit and delete it from the prompt in the same review.
- **One project**: a PR to that project's `CLAUDE.md`, or a Linear ticket. Never rewrite a project's Direction (the human prose in its Linear description).
- **Human-review only**: `HARD_LIMITS.md`, this skill, `templates/review-prompt.md`, `templates/run-log.md`, and anything that would weaken review, QA, tests or safety. Never change these yourself: open a PR, never merge it, and name it in the message for a human.

## 4. Make each change
1. Toolkit: branch `review/<YYYY-MM-DD>-<slug>` from the `Toolkit branch`, edit, `make verify` must pass, add a `PROGRESS.md` entry (what was observed, the change, how to tell next week if it worked).
2. **Independent check** (a fresh subagent, model `sonnet`, that has not seen your reasoning): give it the diff and the evidence and ask: does this address the observed failure; is the instruction clearer than before; could it break another project or user; is it the smallest change that works? Any "no" or doubt → drop the change and move the item to Watching.
3. Open the PR with `$TOOLKIT/orchestration/ghpr.sh open` against the `Toolkit branch`, body = evidence + change + check verdict. Merge it with `ghpr.sh merge` only if the personal rules allow automatic merges; if the merge is denied, leave it open.
4. Scheduled prompt: change it only if the loop has not started tonight (no run log entry for tonight, and no loop ticket In Progress updated in the last 60 minutes); otherwise defer to the next review and say so.

## 5. Record and report
1. On the run log page, add at the top of the **Reviews** section: date; nights reviewed; changes made (PR or prompt edit, one line each with the evidence); considered but not changed, with the reason; the Watching list. Roll run log nights older than 14 days into one summary line each.
2. Send one `SendUserMessage` only if something changed or needs a human (an unmerged PR, a HARD_LIMITS proposal, a superpowers bug report): at most 6 phone-readable lines, leading with what the person must do. Nothing changed → no message.

## Rules
- Never edit app code, tickets' acceptance criteria, or design docs: those belong to the loop's own skills.
- Never start or fire the loop. The only scheduled-task change allowed is the loop's prompt text (step 4.4): never its schedule, repositories, model or enabled state, and never any other task.
