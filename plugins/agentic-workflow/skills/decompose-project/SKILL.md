---
name: decompose-project
description: Use when breaking a project brief, PRD or idea into agent-sized tickets, planning a new project's backlog, or asked to "plan", "split up" or "ticket out" a piece of work. Produces dependency-ordered, testable tickets with taste checkpoints marked, and gets approval before anything is created in Linear. Stops with open questions if the brief is too vague.
---

# Decomposing a project into tickets

The output is a small set of tickets that an agent can pick up in dependency order, each finishing with a green `make verify`. Every ticket follows the `ticket-spec` skill's contract; read that first if you have not. A complete worked example (brief and ten tickets) is in `examples/cajunt/` in the toolkit; see [references/walkthrough.md](references/walkthrough.md) for how it was derived.

## Steps

1. **Restate the goal in one sentence.** Who gets what, ending in something observable. If you cannot, the brief is too vague (see below).
2. **List milestones as vertical slices.** Each milestone cuts through every layer (data, logic, UI) for a small piece of behaviour and leaves the app runnable. "All the database tables" is not a milestone; "a user can add a recipe and see it listed" is.
3. **Write tickets per milestone.** One ticket is one worker session, roughly one feature, at most about 8 acceptance criteria. Prefer fewer, well-specified tickets over many tiny ones, and never a ticket per file or per function. A typical small project is 8 to 12 tickets.
   **Coverage table (required).** Split the brief or spec into one line per user-visible feature (every "X can/does Y" sentence, including headline mechanics such as "perishables decay by shelf life"). Next to each, name the ticket whose acceptance criterion drives that feature through the UI, `checked by:` a Playwright spec. A feature with no UI path, or whose only ticket lists its UI under "Out of scope", is a gap: add a ticket or cut the feature from the spec. Do not put the UI of state you introduce (a field, setting, list or log) in "Out of scope" unless the table names the later ticket that adds it. Paste the table into the project description or approval message.
4. **Add dependencies.** Set `Blocked by:` only for real ones: ticket B needs code or data that A creates. Do not chain tickets just to impose an order. Independent tickets can run in parallel. Run `python3 scripts/check_ticket_graph.py <dir>` to catch unknown IDs and cycles.
5. **Mark taste checkpoints.** Set Escalation to `taste-checkpoint` on the first ticket that produces a UI (the first skeleton) and on the one that sets the visual direction. These are the points where a human looks at a screenshot before more work builds on the choice. Use `security` and `irreversible` where they apply.
6. **Lint every ticket**: `python3 scripts/lint_ticket.py <dir>/*.md`. Fix everything it reports. Only tickets with no blockers are `Status: Ready`; the rest are `Backlog` until their blockers are done.
7. **Present the breakdown for approval before creating anything in Linear.** Show a table of ID, title, blocked-by, escalation and a one-line goal, plus any assumptions. Create nothing until the person says yes.

## Fixed opening tickets

- **First ticket of any new project: the harness.** Create the repo from the project template so that `make verify` is green on a fresh clone. Nothing else can be verified before this exists.
- **Second: a walking skeleton.** The thinnest path that runs end to end (for a web app: browser, API, database and back, with one Playwright test). Every later ticket extends something that already runs.

## When the brief is too vague

Stop. Do not guess, and do not create tickets. Return:

- a proposed outline: the one-sentence goal as you understand it, and the milestones you would use;
- the open questions that block a decision, each with your default answer ("Auth? Assuming none for v0.");
- what you would need to answer to proceed.

A brief is too vague when you cannot name a testable outcome for the first milestone, or when a choice would change the ticket structure (stack, single user or multi-user, which external services).

## Creating in Linear (after approval)

Use the Linear MCP tools: `save_project` once for the project, then `save_issue` for each ticket in dependency order, passing the ticket body as the description and `blockedBy` with the Linear IDs of its blockers. Create blockers first so their IDs exist. Put Ready tickets in the team's ready state and the rest in backlog. The `linear-workflow` plugin's skill owns the details (states, labels, ID mapping); follow it rather than this summary.

## Common mistakes

- A "set up the database" ticket with no behaviour a test could observe.
- An API-only ticket ("Out of scope: UI") for a feature nobody later gives a screen: every ticket passes its own tests, yet the product eval finds the feature unreachable (cajunt, `shelf_life_days`).
- UI work with no `taste-checkpoint`, so the agent builds ten screens on an unreviewed look.
- Everything blocked by the previous ticket: a chain, not a graph.
- Skipping step 7 because the breakdown "looks obviously right".
