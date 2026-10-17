Status: Ready

# DEMO-1 Add low-stock filter to GET /items

## Goal
Let a client list only the items that are running low.

## Context
- `GET /items` in `app/main.py` returns every item; `app/db.py` has `list_items`.
- "Low" is caller-defined: `GET /items?low_stock=N` returns items with `quantity <= N`.

## Acceptance criteria
- [ ] `GET /items?low_stock=2` returns only items whose quantity is <= 2 — checked by: tests/test_items.py::test_low_stock_filter_returns_items_at_or_below_threshold
- [ ] `GET /items` without the parameter still returns all items — checked by: tests/test_items.py::test_list_items_returns_created_items_in_order
- [ ] A negative or non-integer `low_stock` is rejected with 422 — checked by: tests/test_items.py::test_low_stock_rejects_invalid_values

## Verify
`make verify`

## Out of scope
Pagination, sorting, filtering by name or unit.

## Escalation
none
