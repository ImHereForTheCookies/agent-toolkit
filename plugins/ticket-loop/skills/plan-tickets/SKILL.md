---
name: plan-tickets
description: Use when a Linear ticket labelled plan asks to turn a project's design doc (or a rough idea ticket) into agent-sized build tickets in Linear, or to re-plan after the design doc changed. Produces linted, dependency-ordered tickets with Skill labels and writes a coverage table back to the design doc, without waiting for approval.
---

# Plan: design doc → build tickets

## Prefer existing plugins
- The decomposition method is `$TOOLKIT/plugins/agentic-workflow/skills/decompose-project/SKILL.md` and the ticket contract is `$TOOLKIT/plugins/agentic-workflow/skills/ticket-spec/SKILL.md`. Read both; this skill only changes how they run unattended.
- **superpowers `writing-plans`** works at the level *inside* one ticket (2-5 minute steps with code). Implementers use it; do not write those plans here.
- **Notion plugin**'s spec-to-implementation skill does the same job with tasks stored in Notion. If a project's Constraints say tasks live in Notion, use it instead; otherwise Linear is the task store.

## Inputs
Ticket ID, project, Repo, project folder, Design doc URL, Constraints, Models. Load Notion fetch/update tools and Linear `list_issues,get_issue,save_issue,save_comment,list_issue_labels,list_milestones,save_milestone`.

## Steps
1. Claim the ticket (In Progress). Fetch the design doc. If the ticket is a rough idea with no design doc behind it, plan only that idea (1-5 tickets) and skip step 6's doc write if there is no doc.
2. **Know what exists.** List the project's open and done tickets. In the repo, skim `CLAUDE.md`, `PROGRESS.md`, `git log --oneline -20`. For a re-plan, read the doc's latest Change log entry: plan only the delta.
3. **Draft in a subagent** (model from `Models`, default `opus`, effort high): "Decompose <doc> into tickets per decompose-project steps 1-6 and ticket-spec. Unattended: there is no approval step (step 7); instead self-check. Write one markdown file per ticket to `~/work/plan/<project>/<ID>.md` using placeholder IDs P-1, P-2... and a `coverage.md` table (v1 scope item → ticket → check). Reply in 8 lines."
   Planning rules it must follow:
   - **New repo:** P-1 is the harness ticket (`$TOOLKIT/plugins/project-template/skills/harness-init/SKILL.md`; `CLAUDE.md` gets a `Design doc: <url>` line and the Constraints; the Makefile also gets a `setup` target that installs the stack's dependencies), P-2 the walking skeleton with one end-to-end test. Then vertical slices.
   - Every v1 scope item has a ticket whose criteria drive it through the UI or public interface; no orphan features.
   - At most 8 acceptance criteria per ticket; real blockers only; `taste-checkpoint` on the first UI ticket and the one that sets the visual direction.
   - Testing rules from the doc's "Testing and quality bar" go into each ticket's criteria (unit and integration tests for every piece).
   - Each ticket gets a Skill label: `build` normally; `design` if it needs a design decision first (rare). Never invent other labels.
   - Typical size: 15-25 tickets for a new project, fewer for a re-plan.
4. **Gate (you, not the subagent):** `python3 $TOOLKIT/scripts/lint_ticket.py ~/work/plan/<project>/*.md` and `python3 $TOOLKIT/scripts/check_ticket_graph.py ~/work/plan/<project>` must pass (the graph checker reads `Blocked by:` lines with the placeholder IDs). Check coverage: every v1 item maps to a ticket. Fix or re-dispatch once; a second failure → escalate per human-in-the-loop and stop.
5. **Create in Linear**, idempotently: each description ends with the line `Plan-ID: <plan ticket ID>/P-<n>`. First list the project's tickets and skip any whose description already carries that Plan-ID (a resumed run after a cutoff must not duplicate). Blockers first so their IDs exist: `save_issue(team, project, title, description, labels=[<Skill label>], blockedBy=[...], priority)`. First ticket(s) with no blockers: Todo; the rest Backlog. Replace placeholder IDs in descriptions and `Blocked by:` lines with real IDs (update after creation if needed). Optional milestone per vertical slice. For a re-plan, cancel unstarted tickets the change makes obsolete (comment why) instead of editing their contract.
6. **Write back** to the design doc's Plan section: the coverage table with real ticket IDs and the milestone list. Set project `Stage: building`.
7. Close: comment on the plan ticket (count, first ticket, coverage gaps cut and why) and set it Done.

## Rules
- Never change a ticket's acceptance criteria after it is In Progress; file a new ticket instead.
- The design doc decides scope. If decomposition shows a scope item is not buildable as written, create a `design` ticket explaining why rather than quietly dropping it.
