Status: Backlog

# CAJ-9 Weekly recipe cards UI

Blocked by: CAJ-5, CAJ-8

## Goal
The home page shows the week as recipe cards that the user can browse, cook and swap.

## Context
- One card per planned day: title, ingredients, a "Cooked" button (calls `cook`, CAJ-6) and a "Swap" button (re-proposes that day).
- Also on the page: an import-by-URL form (CAJ-5), a "Plan my week" button (CAJ-8) and a link to the grocery list.
- Visual direction (card look, typography, color) is the taste decision. Build one direction, take desktop and phone-width screenshots, and stop for a checkpoint before polishing.
- Playwright drives all browser tests against the mock planner.

## Acceptance criteria
- [ ] Clicking "Plan my week" renders 7 cards — checked by: tests/e2e/cards.spec.ts::plans a week
- [ ] Importing a URL from the form adds the recipe to the list shown — checked by: tests/e2e/cards.spec.ts::imports a recipe
- [ ] Clicking "Cooked" marks the card cooked and the pantry estimate drops — checked by: tests/e2e/cards.spec.ts::cooking updates pantry
- [ ] Desktop (1280px) and phone (390px) screenshots are attached to the PR — checked by: reviewer sees both screenshots in the PR description

## Verify
`make verify` and `make e2e`

## Out of scope
Phone usability fixes beyond not breaking at 390px (CAJ-10), grocery list page content, offline support, animations.

## Escalation
taste-checkpoint
