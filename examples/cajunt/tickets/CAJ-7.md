Status: Backlog

# CAJ-7 Compute the grocery list from the week plan and the pantry

Blocked by: CAJ-6

## Goal
The grocery list shows exactly what to buy: the week's plan needs minus the pantry estimate.

## Context
- New module `app/grocery.py` with `compute(plan_entries, pantry, today) -> list[GroceryLine]`; `POST /api/grocery/recompute` stores the result in `grocery_items`.
- Needs are summed per canonical ingredient name and unit across planned, uncooked entries, scaled by servings.
- A line is `max(0, need - on_hand)` and is omitted when 0. Manually added grocery items are never removed by a recompute.
- Pantry quantities come from `estimate()` (CAJ-6), so expired perishables count as 0.

## Acceptance criteria
- [ ] Two meals needing 200 g and 300 g of rice with 100 g on hand give a line of 400 g — checked by: tests/test_grocery.py::test_sums_needs_and_subtracts_pantry
- [ ] An ingredient fully covered by the pantry is omitted — checked by: tests/test_grocery.py::test_covered_ingredient_omitted
- [ ] An expired perishable in the pantry does not reduce the need — checked by: tests/test_grocery.py::test_expired_perishable_not_counted
- [ ] Cooked entries contribute no needs — checked by: tests/test_grocery.py::test_cooked_entries_ignored
- [ ] Recompute keeps manually added items — checked by: tests/test_grocery.py::test_recompute_keeps_manual_items

## Verify
`make verify`

## Out of scope
Store aisles or grouping, price estimates, ordering integrations (Instacart), UI.

## Escalation
none
