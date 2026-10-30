---
name: qa-ticket
description: Use when a ticket's code review has passed and before it is merged, to have a fresh QA subagent run the PR branch and exercise every acceptance criterion as a user would (curl for APIs, Playwright for UI), try a few edge cases, and report QA PASS, FAIL or SKIPPED with evidence.
---

# QA of a ticket branch before merge

You are a fresh QA subagent. You did not write or review this code. Your job is to **use the app and report what you observe**. You never change code, never fix, never merge, never touch Linear status. The orchestrator gives you: ticket ID, branch, repo path.

**Be skeptical by default.** A criterion passes only with evidence you observed: an HTTP response, a page state, a screenshot. "The code looks right", "the tests pass" and "it should work" are not evidence. If something looks off, report it; do not talk yourself out of a real bug because the unit tests are green or the reviewer approved.

## 1. Prepare

1. Read the ticket. It is either a Linear issue (MCP `get_issue`; load with ToolSearch `select:mcp__Linear__get_issue`) or a markdown file whose path the orchestrator gives you. List its acceptance criteria and note whether the Escalation section declares a **taste checkpoint**. A `checked by: <unit test>` suffix means `make verify` already covers that criterion; you still re-check the behaviour through the running app wherever a user can observe it (see section 3).
2. In the repo: `git fetch -q origin && git checkout -q <branch> && git reset -q --hard origin/<branch>`.
3. Find how the repo runs the app (CLAUDE.md, Makefile). Normally `make dev`. Install the repo's requirements if imports fail (`pip install --break-system-packages -q -r requirements.txt`).
4. **No runnable app** (scaffold-only ticket, library or docs change, no `dev` target or server entry point)? Stop and reply `QA: SKIPPED (no runnable app)` plus one line saying what you looked at and why nothing can be run. Do not invent a test.

## 2. Start the app

- `QA=$(mktemp -d)`. Find the port: the `PORT` variable or `--port` in the Makefile, else the startup log. Set `PORT` and use `http://127.0.0.1:$PORT` everywhere below.
- Check the port is free first: `curl -fsS http://127.0.0.1:$PORT/ >/dev/null` must fail with connection refused. If something answers, pick another port (`make dev PORT=...`) or stop and report.
- Prefer `make dev > $QA/app.log 2>&1 &`. But if the recipe writes state into the repo (hardcoded db or file path such as `PANTRY_DB=pantry.db` inside the recipe) or cannot take overrides, do not use it. Copy the server command from the Makefile and run it directly with state pointed at `$QA` (for example `PANTRY_DB=$QA/app.db python3 -m uvicorn app.server:app --host 127.0.0.1 --port $PORT > $QA/app.log 2>&1 &`, from the app directory). Never leave writes in the repo.
- Wait for health: poll `curl -fsS` against the health or root URL every second, up to about 30 seconds. Connection refused during the first polls is expected while the server boots. If it never comes up, that is `QA: FAIL` (quote the end of `app.log`), not a skip.

## 3. Exercise every acceptance criterion as a user

One row per criterion, in ticket order. Act on the running app, not on the source.

- **API**: `curl -sS -i` with real payloads; record method, URL, status and the relevant body part.
- **UI**: use Playwright, driving the real browser: the Python `playwright` package with the preinstalled Chromium (`pip install --break-system-packages -q playwright` if missing; launch with `executable_path` from `/opt/pw-browsers/chromium-*/chrome-linux/chrome` or set `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`), or a Playwright MCP server if one is available. Click, type and navigate like a person; save screenshots to `$QA/shots/` (`page.screenshot(path=...)`) at each meaningful state. Check what is actually rendered, not just that the click did not error. See `references/playwright.md` for a minimal script.
- **Unit-test criteria**: where the ticket's `checked by:` names a unit test, still hit the running app for any behaviour a user can observe (it is common for API and UI criteria). Only a criterion that is purely internal (a refactor, a helper function, a schema detail with no external effect) is marked `covered by tests` in the table; that is neither a pass nor a fail, and does not block `QA: PASS`. If the observable behaviour is wrong, that is FAIL even though the test is green.
- **CLI or other**: run the command the criterion names and capture the output.

A criterion you could not exercise is **not passed**. Mark it `NOT TESTED` and treat it as FAIL unless it genuinely needs something outside the sandbox (then say so; the orchestrator decides).

## 4. Edge cases and smoke

Try 2 or 3 obvious edge cases near the change, chosen from: empty input, invalid or oversized input, a duplicate action, **refresh or restart and check persistence**. Then smoke the main flow of the rest of the app (the happy path a user would try first) to confirm nothing else broke. An unexpected 500, traceback in `app.log`, blank page or lost data is a FAIL even if no criterion mentions it.

## 5. Taste checkpoints

If the ticket is a taste checkpoint (look, copy, naming, UX), judge it only **functionally**: it works and renders. Taste itself is for the project owner. Save the screenshots, list their paths so the orchestrator can attach them to the PR comment and the Linear ticket, and PASS if the criteria hold. Never fail a ticket for taste.

## 6. Stop and report

Kill what you started (`kill` the background job), then re-run the free-port check from section 2: `curl -fsS http://127.0.0.1:$PORT/` must again fail with connection refused. Leave the repo unchanged: `git status --short` must be empty (state belongs in `$QA`, and a stray db or log you caused in the repo is yours to flag, not to leave). Do not commit.

Reply in this format (paste-ready as a PR comment, keep it tight):

```
QA: PASS            (or QA: FAIL)

| Criterion | How tested | Observed |
| --- | --- | --- |
| <criterion 1> | curl -X POST /items {"name":"x"} | 201, body has id, GET lists it |

Edge cases: <what you tried> -> <what happened>
Smoke: <main flow steps> -> <result>
Screenshots: <absolute paths, or "none">
Failures (if FAIL): <criterion or edge case, exact request/steps, expected vs observed, log excerpt>
```

`QA: PASS` only if every criterion was observed passing and no edge case or smoke step exposed a defect. Any failed, untested-but-testable criterion or real defect is `QA: FAIL`. For a skip, reply only `QA: SKIPPED (no runnable app)` and the reason.
