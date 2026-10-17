Status: Backlog

# CAJ-6 Pantry estimate with purchase, cooking and perishable decay

Blocked by: CAJ-3, CAJ-4

## Goal
The app keeps an estimated quantity for every pantry item that follows purchases, cooked meals and spoilage.

## Context
- New module `app/pantry.py`. Events: `purchase(item, qty)` adds; `cook(plan_entry)` subtracts the recipe's scaled ingredients and sets the cooked flag; `estimate(item, today)` returns the current quantity.
- Perishables carry `shelf_life_days` (null means non-perishable). A purchased batch loses its whole quantity once `today - purchased_on > shelf_life_days`; subtraction uses the oldest batch first.
- The estimate never goes below 0; cooking more than is on hand empties the item and records a shortfall instead of failing.
- The module takes `today` as an argument, never reads the clock.

## Acceptance criteria
- [ ] A purchase of 500 g flour gives an estimate of 500 g — checked by: tests/test_pantry.py::test_purchase_adds_quantity
- [ ] Cooking a plan entry subtracts the scaled recipe quantities and marks it cooked — checked by: tests/test_pantry.py::test_cook_subtracts_scaled_ingredients
- [ ] Milk with `shelf_life_days=7` bought on day 0 estimates full on day 7 and 0 on day 8 — checked by: tests/test_pantry.py::test_perishable_decays_after_shelf_life
- [ ] Cooking uses the oldest batch first — checked by: tests/test_pantry.py::test_cook_uses_oldest_batch_first
- [ ] Cooking more than is on hand leaves 0 and records the shortfall — checked by: tests/test_pantry.py::test_overdraw_records_shortfall
- [ ] Cooking the same plan entry twice subtracts only once — checked by: tests/test_pantry.py::test_cook_is_idempotent

## Verify
`make verify`

## Out of scope
UI, background jobs that expire items on a timer (estimates are computed on read), partial spoilage, unit conversion between mass and volume.

## Escalation
none
