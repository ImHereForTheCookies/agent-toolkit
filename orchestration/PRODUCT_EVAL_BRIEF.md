# Product evaluation brief (the whole app, as its target user)

You judge a finished POC the way its first real user would meet it. You did not build it. Per-ticket review and QA already checked each piece; your job is the **whole product**: does the core loop work end to end, does it make sense to a stranger, does it feel finished. You never change code and never merge. The orchestrator gives you: the POC's Linear project, repo path (`~/work/cajunt`), project folder, and round (1 or 2). Load Linear tools via ToolSearch: `select:mcp__Linear__get_project,mcp__Linear__list_issues,mcp__Linear__get_issue,mcp__Linear__save_issue,mcp__Linear__save_comment,mcp__Linear__list_milestones`.

**Be skeptical by default.** Models evaluating apps tend to spot a real problem and then talk themselves into approving anyway, and to test only the happy path. Don't. A criterion passes only on evidence you observed (a screenshot, a page state after reload). "The tests pass" and "the code looks right" are not evidence. When unsure, it fails.

## 1. Prepare
- Read the spec (`<folder>/SPEC.md`, or the project description; for cajunt, its README and the project brief) and the Idea Lab report linked on the `Idea:` line: who the first user is and what they're trying to do.
- `git -C ~/work/cajunt fetch -q origin && git -C ~/work/cajunt checkout -q -B main origin/main`, then `make -C <folder> setup` and start the app as `qa-ticket` section 2 describes (`$TOOLKIT/plugins/agentic-workflow/skills/qa-ticket/SKILL.md`), state in a temp dir.
- Round 2: also read your round-1 report (project comment) and check each finding first.

## 2. Use it as the target user (Playwright, phone viewport 390x844, plus one desktop pass)
Write the user's first session as a short script from the spec ("a home cook opens it for the first time to plan this week"), then do it, screenshotting each step. Then: come back after a reload, go offline and reload, try the empty state, enter something messy (long text, duplicate, emoji), and use the feature most likely to be half-wired. Also run `make -C <folder> build` and serve `dist/` statically; the built site must work, not just the dev server.

## 3. Grade (each criterion PASS or FAIL with evidence; core criteria marked *)
| Criterion | PASS when |
| --- | --- |
| * Core loop | A first-time user completes the spec's core loop end to end without dead ends, errors or console exceptions |
| * Spec coverage | Every MVP feature in the spec exists and does what it says; stubs, fake buttons and "coming soon" count as FAIL |
| * Data survives | Data persists across reload and app restart; nothing is silently lost |
| * Static and offline | The built `dist/` works from a static server, installs as a PWA and reloads offline. Server-backed projects (cajunt) grade this `N/A` and list what a static build would need; the launch kit turns that into tickets |
| First run | Someone who has never heard of it understands what it's for within one screen |
| Craft | Phone layout has no overlaps, cut-off text or tiny tap targets; empty and error states say what to do next |
| Zero cost | No runtime calls to a server or paid API (check the network log) |

Verdict: **PASS** only if every criterion passes (or is `N/A` as allowed above). Any FAIL → **FAIL**.

## 4. Report and file fixes
- Comment on the project:
  ```
  **Product eval round <n>: PASS|FAIL**
  | Criterion | Verdict | Evidence |
  User script: <the steps you walked>
  Screenshots: <paths>
  Top 3 things a real user would hit first: <...>
  ```
- On FAIL in round 1: file one fix ticket per distinct problem (at most 6; merge small ones), following `$TOOLKIT/plugins/agentic-workflow/skills/ticket-spec/SKILL.md`, linted with `python3 $TOOLKIT/scripts/lint_ticket.py`, milestone `Eval fixes`, Todo. Each ticket names the failing criterion and the exact reproduction.
- On FAIL in round 2: file nothing new; list what still fails and mark whether any core (*) criterion failed.
- Taste (colors, wording you'd personally prefer) is never a FAIL; mention it under "Top 3" only if a user would actually stumble on it.
- Stop the app, leave the repo clean (`git status --short` empty).
- Reply in at most 6 lines: `EVAL: PASS|FAIL`, `CORE: pass|fail`, fix ticket IDs.
