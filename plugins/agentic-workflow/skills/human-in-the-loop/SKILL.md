---
name: human-in-the-loop
description: Use when an unattended agent hits a gate or review that failed twice, criteria that are ambiguous or contradict each other, an irreversible or external action, scope growth, a security-sensitive change, or a taste checkpoint, and must decide whether to escalate, stop, file a follow-up, flag, or carry on.
---

# Escalating to a human without blocking the night

**Core rule: never block waiting for a human.** Nobody is watching. When a trigger fires, do the safe part, leave a precise note in Linear, and move to the next ticket. A human answers later; the work resumes from the note.

Most tickets trigger nothing. Escalating a ticket that was fine wastes the human's morning, so check the table before you act, and if no row matches, carry on (`proceed`).

## The six triggers

| # | Trigger | What to do | Action label |
|---|---|---|---|
| 1 | The same ticket failed the gate (`make verify`) or the reviewer **twice** | Put the branch back at the last green commit (if the failing commits are already pushed, add `git revert` commits; never force-push). Label Needs Human; comment with both failure logs. Leave the PR open. Next ticket. | `escalate_needs_human` |
| 2 | Acceptance criteria are ambiguous, or two criteria / the ticket and the code contradict each other | Do not pick a reading. Label Needs Human; comment the specific question and the two readings. Write no code for the disputed part. | `escalate_needs_human` |
| 3 | The next step is irreversible or external: deploy, delete data, spend money, send messages, create external accounts | Prepare everything up to the step (script, dry run, draft, checklist), do not run it. Open the PR for the prepared work but do not merge it or move the ticket to Done (a criterion is unchecked). Label Needs Human; comment exactly what is ready and the one command or click left. | `stop_before_action` |
| 4 | Scope growth: you find work that is needed or tempting but not in the criteria | Finish the ticket as written. File a new Backlog ticket for the extra work and link it. Do not widen this PR. Keep going. | `file_followup_ticket_and_continue` |
| 5 | Security-sensitive change: auth, secrets, permissions, access control | Work on the branch and open the PR, but never merge without human review. Label Needs Human, comment what to look at. | `pr_without_merge` |
| 6 | Taste checkpoint (the ticket's Escalation section says so): look, copy, naming, UX | Once the gate and reviewer pass, merge with sensible defaults, post screenshots or output in the ticket, and continue. The human adjusts afterward. | `merge_and_flag_taste` |
| - | None of the above, including one failed attempt that you then fixed | Carry on and finish the ticket normally. | `proceed` |

Rows 1 and 2 stop the ticket. Rows 3 and 5 stop one step of it (the action, the merge). Rows 4 and 6 do not stop anything: they only leave a trail. If two rows fire, take the stricter one (1 and 2 over 3 and 5, those over 4 and 6).

Not triggers: a single failed gate you can fix; a reviewer style opinion; an unfamiliar library; a slow test. Fix, retry, or note it in the evidence comment.

## Reviewer guard

Reviewers flag only gaps in **correctness** or in the **stated criteria**, plus anything that would mislead a future agent (wrong command, wrong syntax). Style, naming preferences, "could also", and ideas for later are not findings. A reviewer who fails a PR for those has overreached: that FAIL does not count toward the two-failure limit and should be re-run with this guard restated. If you are the reviewer, put such ideas in a follow-up ticket (row 4), not in the verdict.

## How to escalate in Linear

Mechanics (loading the tools, `addLabels` rather than `labels`, leaving the state unchanged) live in the `linear-tickets` skill of the linear-workflow plugin, section "Escalate". Follow it; do not copy it. Short version: `save_issue(id, addLabels=["Needs Human"])` then `save_comment`.

Comment template (replace the angle-bracket parts; use real bullets and newlines):

```
**Escalated: needs a human**

* Trigger: <1-6 from the table, by name>
* Reason: <what blocked you, with evidence: both failure logs, the conflicting lines, the action you stopped before>
* Question: <the one specific question whose answer unblocks the work; for ambiguity give both readings as "A: ..." and "B: ...">
* State: <branch / PR, last green commit, what is done, what is untouched>
* Default if no answer: <what you would do, so the human can just say "yes">
```

For row 4 (follow-up ticket) use a short comment on the original ticket instead: "Out of scope, filed as <TEAM>-nn: <title>". For row 6, post the screenshots or sample output and the line "Taste checkpoint: merged with defaults, please review".

## After escalating

1. Confirm the branch is in the state the comment says (reverted to green for row 1, no half-written code for row 2).
2. Move on to the next ticket. Do not poll, sleep, or ask the orchestrator for an answer.
3. Never remove the Needs Human label yourself; a human does that after answering.
