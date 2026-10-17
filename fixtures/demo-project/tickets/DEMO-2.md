Status: Ready

# DEMO-2 Add POST /items/{id}/consume endpoint

## Goal
Let a client use up some of an item without computing the new quantity itself.

## Context
- Today a client must PATCH the absolute quantity, which races with other clients.
- `POST /items/{id}/consume` with body `{"amount": N}` subtracts N from the stored quantity and returns the updated item.

## Acceptance criteria
- [ ] Consuming 3 from an item with quantity 5 leaves 2 and returns the updated item — checked by: tests/test_items.py::test_consume_subtracts_amount
- [ ] Consuming more than is in stock returns 409 and leaves the quantity unchanged — checked by: tests/test_items.py::test_consume_more_than_stock_is_rejected
- [ ] `amount` must be a positive integer, otherwise 422; unknown id returns 404 — checked by: tests/test_items.py::test_consume_validates_amount_and_id

## Verify
`make verify`

## Out of scope
Bulk consume, an audit log of consumptions, restocking endpoint.

## Escalation
none
