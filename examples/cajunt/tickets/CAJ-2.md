Status: Backlog

# CAJ-2 Walking skeleton: add a recipe in the browser and see it listed

Blocked by: CAJ-1

## Goal
One thin path works end to end (browser, API, SQLite and back) so later tickets extend a running app.

## Context
- Smallest possible slice: one `recipes` table with `id`, `title`; `POST /api/recipes`, `GET /api/recipes`; one HTML page with a title input and a list.
- This is the first UI of the project, so the page layout and look are a taste decision. Stop for a checkpoint with a screenshot.
- Playwright drives the browser test against a server started on a free port.

## Acceptance criteria
- [ ] Posting `{"title": "Pad thai"}` then listing returns that recipe — checked by: tests/test_recipes_api.py::test_create_then_list
- [ ] In the browser, typing a title and pressing Add shows it in the list without a reload — checked by: tests/e2e/skeleton.spec.ts (Playwright)
- [ ] Recipes survive a server restart — checked by: tests/test_recipes_api.py::test_recipes_persist_across_restart
- [ ] A screenshot of the page at 1280px wide is attached to the PR — checked by: reviewer sees the screenshot in the PR description

## Verify
`make verify` and `make e2e`

## Out of scope
Ingredients, editing or deleting recipes, styling beyond a plain readable page, mobile layout.

## Escalation
taste-checkpoint
