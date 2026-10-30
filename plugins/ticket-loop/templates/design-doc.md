# Design doc template

Use these sections, in this order, as `##` headings. The first line under the title is `Version <N> · <YYYY-MM-DD> · written by the ticket loop; comment anywhere to change it.`

## Summary
One paragraph: what the app is, for whom, the one thing it must do well, and what v1 includes.

## Users and problem
Who uses it, in what situation, what they do today instead, and what hurts. Cite research in Sources.

## Success criteria
3-6 observable outcomes for v1 ("a first-time user writes and finds an entry within 60 seconds on a phone"), each checkable by the evaluator.

## Scope
- **v1:** requirements with stable IDs, one sentence each: `R1. A user can ...` (cite findings that drove them: `(F: <finding title>)`). Never renumber; retire an ID instead of reusing it.
- **Later:** worth doing after v1.
- **Never (for now):** explicitly excluded, with a reason.

## Assumptions
Table: A# | Assumption | Confidence (high/medium/low) | Why | What changes if wrong | Evidence (finding links or research ticket). Every decision made without a human goes here. End with: "Disagree? Comment on the row; the next run revises the doc."

## Research and evidence
Table: Finding (link) | Source type | What it changed (R-IDs, A#) | Decision (incorporated / rejected, why). Also: open research questions and their tickets, and any research only humans can do (interview guides, surveys to run), written so a person can pick it up.

## Approaches considered
2-3 options with trade-offs and the one chosen (and why). Keep it short.

## Architecture and components
The units of the system, one line each: purpose, interface, depends on. A small diagram in a code block if it helps. Tech stack and why.

## Data model
Entities, key fields, where data lives, retention, export/backup.

## Key flows
Step lists for the 2-4 flows that matter most (first run, the core loop, recovery from an error).

## Error handling
What can fail (storage, network, bad input) and what the user sees each time.

## Testing and quality bar
Unit and integration test expectations, what end-to-end checks prove the success criteria, devices/viewports, accessibility basics, performance budget.

## Constraints
Copied from the Linear project's `Constraints:` line plus any the design adds (privacy, cost, platform).

## Plan
Written by the planner: coverage table (v1 scope item → ticket ID → check), milestone list.

## Evaluation
Written by the evaluator: latest verdict, date, link to the full report.

## Decision log
Dated one-liners for decisions made after v1 of the doc.

## Change log
`v<N> (<date>): <what changed and why, naming the comment, finding or direction that caused it>`

## Sources
Links for every research claim.
