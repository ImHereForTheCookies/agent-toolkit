---
name: research-question
description: Use when a Linear ticket labelled research asks a question to investigate (usually a low-confidence design assumption to test), to gather evidence from public primary sources and record it as findings in the project's Notion research database for the next design revision. Never contacts, surveys or posts to anyone; research that needs real people is written up as a guide for humans.
---

# Answer a research question with evidence

Output is **findings rows**, not a report nobody reads: each row is one claim with evidence, which the design skill must incorporate or reject on its next revision. Findings never change the design directly.

## Prefer existing plugins
- **deep-research** (Anthropic skill, if available in the session): use it for broad multi-source questions, then convert its conclusions into findings rows.
- **Notion plugin** research-documentation skill (if installed): fine for structuring the evidence page.
- What this skill adds: the question comes from a design assumption, results land as typed rows the design loop consumes, and the "humans only" boundary.

## Two tracks
- **Assumption research** (default): tests a design assumption; steps below.
- **Exploratory research**: the ticket has a line `Track: exploratory`. Follow `$TOOLKIT/plugins/ticket-loop/templates/research-library.md` instead of steps 3-5: it publishes a readable page in the project's research library, records findings with Status `Future version`, and files its own follow-up questions. Steps 1-2 and the Rules still apply.

## Inputs
Ticket ID, project, Design doc URL, Research database URL, Constraints, Models. Load `select:mcp__Notion__notion-fetch,mcp__Notion__notion-query-data-sources,mcp__Notion__notion-create-pages,mcp__Notion__notion-update-page` plus WebSearch and WebFetch.

## Steps
1. Claim the ticket (In Progress). Read the question, the assumption it tests (A# in the doc) and what evidence would change the design. Query the database for existing rows on the topic so you don't duplicate them.
2. **Investigate** in one subagent (model `sonnet`, effort high), which writes notes to `~/work/research/<ticket>.md` and replies in at most 10 lines:
   - primary sources first: real users in their own words (forums, app-store reviews, issue trackers), peer-reviewed papers, official statistics; listicles and affiliate pages only to find names;
   - aim for 3 independent sources per claim; older than 2 years counts half; note disagreement instead of averaging it away;
   - paraphrase; at most one short quote per source; link everything;
   - never post, comment, vote, sign up, message, or survey anyone, and never collect personal data.
3. **Record findings:** one row per distinct claim (usually 1-5): Finding, Details, Evidence, Source type `Desk research` (or `Paper`, `Competitor review`), honest Confidence, Implication (which R-IDs or A# it bears on), Status `New`.
4. **Research only humans can do** (interviews, usability tests, surveys): add one row with Status `Needs human research`, whose Details hold a ready-to-run guide: who to talk to, 5-8 open questions, what answer would change which requirement. People run it and add their results as `New` rows.
5. Close: comment on the ticket (rows added with links, one-line answer to the question, confidence) and set it Done. The run-queue bootstrap turns the `New` rows into a design revision.

## Rules
- A finding states what the evidence shows, not what to build; the design skill decides.
- If the evidence is thin, say so with Low confidence rather than stretching it.
