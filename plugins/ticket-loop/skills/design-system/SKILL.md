---
name: design-system
description: Use when a Linear ticket labelled design asks for a project's system design doc to be written or revised, from the project's Direction, human comments on the doc, or an evaluation finding. Works without a human gate - decides, records assumptions in the Notion design doc, then queues a plan ticket.
---

# Write or revise the design doc

Output: one Notion page per project, written for humans who drop in when curious, and complete enough that the planner needs nothing else. Nobody approves it first. Every open question becomes a written **assumption** that a human can override later by commenting.

## Prefer existing plugins
- **superpowers `brainstorming`** (if available): use its *content* (purpose, constraints, success criteria, 2-3 approaches with a recommendation, architecture, components, data flow, error handling, testing, units with one clear purpose and clean interfaces). Do **not** run its question-and-approval flow: nobody is there to answer. Where it would ask, you decide and write an assumption.
- **Notion plugin** (`makenotion/claude-code-notion-plugin`, if installed): its research-documentation skill is a fine guide for the research subsection. Page writes still follow this skill.
- What this skill adds: the autonomous assumption log, the fixed doc template, version and change log, and the hand-off to `plan-tickets`.

## Inputs
Ticket ID, Linear project (Direction, `Constraints:`, `Design doc:`), Notion home URL, the repo (may be empty), Models. Load: `select:mcp__Notion__notion-fetch,mcp__Notion__notion-search,mcp__Notion__notion-create-pages,mcp__Notion__notion-update-page,mcp__Notion__notion-get-comments,mcp__Notion__notion-create-comment,mcp__Notion__notion-set-discussion-resolved` plus the Linear tools from `run-queue`.

## Steps
1. **Claim:** ticket In Progress.
2. **Gather direction.** The project Direction (human prose), `Constraints:`, the ticket body, and for a revision: the current doc, its unresolved comments, and any evaluation report the ticket links. If the repo has code, skim its `CLAUDE.md`, `PROGRESS.md` and layout so the design matches reality. Personal rules from the scheduled prompt apply.
3. **Research (short, optional).** If the direction names a product category, one research subagent (Agent tool, model `sonnet`) may look for how existing apps solve it and what real users complain about (primary sources over listicles). It writes to `~/work/research/<project>-design.md` and replies in at most 10 lines. Never post, sign up or message anyone.
4. **Draft.** Dispatch one drafting subagent (model from `Models`, default `opus`, effort high): "Write the design doc for <project> following `$TOOLKIT/plugins/ticket-loop/templates/design-doc.md` exactly, from these inputs: <paths and text>. Fully autonomous: never ask; every decision you were unsure about goes in Assumptions with a confidence (high, medium, low) and why. Keep v1 scope to what a small team of agents can ship and test in about 15-25 tickets. Respect the Constraints. Write the markdown to `~/work/design/<project>-v<N>.md` and reply in 8 lines: version, scope summary, top 3 assumptions." For a revision, pass the current doc and say: change only what the direction, comments or findings require, and add a Change log entry naming each.
5. **Self-check** the draft before publishing (fix it yourself or re-dispatch once):
   - every template section present; no "TBD"; success criteria are observable;
   - each v1 scope item is testable and traceable to the Direction or an assumption;
   - nothing contradicts `Constraints:` or the hard limits (no paid services, deploys or accounts unless Constraints allow them);
   - the architecture names units with one purpose and an interface each.
6. **Publish to Notion.**
   - New: create the page under Notion home, titled `<Project name> - System design`, body = the draft. Put `Design doc: <page URL>` on the Linear project (patch that line; add it if missing) and set `Stage: planning`.
   - Revision: replace the changed sections, bump the version in the title line, append the Change log entry. For every comment you handled, reply on it ("Handled in v<N>: <what changed>", or why you kept the original, citing the evidence) and resolve it.
7. **Queue planning.** Create a `plan` ticket in the same project, state Todo: "Plan from design doc v<N>" with the doc URL and, for revisions, the Change log entry. Set `Stage: planning`.
8. **Close:** comment on the design ticket (doc link, version, top assumptions, plan ticket ID) and set it Done.

## Rules
- Never escalate for a missing answer. Escalate (human-in-the-loop) only when the Direction itself is contradictory in a way that would change the whole architecture, and even then publish the doc with your best reading and say so at the top.
- Write for humans first: plain words, short sections, a one-paragraph Summary at the top that a phone reader can take in at a glance.
- The doc is the source of truth for scope; repo docs link to it instead of copying it.
