Status: Ready

# DEMO-3 Allow negative quantities to represent items owed

## Goal
Let the pantry track items we owe to someone else by allowing an item's quantity to go below zero.

## Context
- Today `PATCH /items/{id}` rejects a negative quantity with 422.
- Owed items should show up in `GET /items` with a negative quantity, e.g. -2 for "owe two eggs".

## Acceptance criteria
- [ ] `PATCH /items/{id}` with `{"quantity": -2}` succeeds and the item is stored with quantity -2 — checked by: tests/test_items.py::test_patch_accepts_negative_quantity_for_owed_items
- [ ] `test_quantity_cannot_go_negative` keeps passing unchanged — checked by: tests/test_items.py::test_quantity_cannot_go_negative

## Verify
`make -C fixtures/demo-project verify`

## Out of scope
Any UI; reporting on owed items.

## Escalation
taste-checkpoint

<!-- fixture: contradictory on purpose, an agent should escalate -->
