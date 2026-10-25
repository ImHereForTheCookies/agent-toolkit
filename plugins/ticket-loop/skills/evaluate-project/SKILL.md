---
name: evaluate-project
description: Use when a Linear ticket labelled evaluate asks to judge a whole app against its design doc's success criteria and v1 scope, as its target user would meet it, then file build tickets for defects and design tickets for flaws in the design itself. Never changes code or merges.
---

# Evaluate the whole app against the design doc

Per-ticket review and QA already checked each piece. You judge the **product**: does the core loop work end to end for a stranger, and does it meet the doc's Success criteria. Be skeptical by default: a criterion passes only on evidence you observed (screenshot, page state after reload, command output). "Tests pass" is not evidence.

## Prefer existing plugins
- Browser driving: the Python `playwright` package with the preinstalled Chromium, or a Playwright MCP server if one is loaded. `$TOOLKIT/plugins/agentic-workflow/skills/qa-ticket/references/playwright.md` has a minimal script.
- **frontend-design** (Anthropic official, if installed) can inform the Craft row, but taste never fails a criterion.
- `$TOOLKIT/orchestration/PRODUCT_EVAL_BRIEF.md` is the POC-specific ancestor of this skill; this one grades against the design doc instead of a fixed PWA checklist.

## Inputs
Ticket ID, project, Repo, project folder, Design doc URL, Constraints, Models. Run the evaluation in one subagent (model `sonnet`, effort high) that follows this skill and replies in at most 8 lines; you then do steps 4-5.

## Steps
1. **Prepare.** Fetch the design doc: Success criteria, v1 Scope, Key flows, Testing and quality bar, Constraints. Check out `main`, run `make -C <folder> setup` if that target exists (`make -C <folder> -n setup`), start the app the way its `CLAUDE.md` says, with state in a temp dir.
2. **Use it.** Build a checklist: one row per Success criterion and one per v1 scope item. For each, do what a user would do (phone viewport 390x844 plus one desktop pass for UI apps; the documented interface otherwise) and record `PASS/FAIL` with evidence. Then the doc's first-run flow as a script, a reload, the empty state, messy input, and the feature most likely to be half-wired. If the doc promises a static build or offline use, test the built output too.
3. **Classify each FAIL:**
   - *Defect*: the doc is right, the app is wrong → a `build` ticket.
   - *Design flaw*: the app does what the doc says but the result doesn't serve the Success criteria, or two parts of the doc conflict → a `design` ticket that quotes the evidence.
4. **File tickets** (you): defects follow ticket-spec, linted with `python3 $TOOLKIT/scripts/lint_ticket.py`, Todo, label `build`, one per distinct problem, at most 8; design flaws as one `design` ticket listing them. Anything not ticketed is listed in the report with a reason.
5. **Report.** Write the verdict (PASS only if every row passes), date, round (`round <k> for design v<N>`), table and top 3 things a real user hits first into the doc's Evaluation section, and link it in a project comment. Set the project `Stage:` to `done` on PASS, or `building` when you filed fix tickets (run-queue re-evaluates after they merge, at most 3 rounds per design version). A design ticket you filed moves the project back through design and planning on its own. Comment on the evaluate ticket and set it Done.
6. **Release (only when Constraints contain `Releases: <slug>`):** after a PASS, run `$TOOLKIT/orchestration/release.sh <repo path> <Folder or .> <slug>` (it verifies, builds, creates the frozen `release/<slug>-vN` branch and moves `release/<slug>` forward; never force, never tags). Without that Constraints entry, never create release branches: a host may serve them, and publishing is a human step.

## Rules
- Stop the app and leave the repo clean (`git status --short` empty).
- No posting, sign-ups or messages, even to "test" sharing features.
