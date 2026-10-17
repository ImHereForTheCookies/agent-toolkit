Status: Backlog

# CAJ-3 Add the full schema and CRUD API

Blocked by: CAJ-2

## Goal
The database holds everything v0 needs, and each entity can be created, read, updated and deleted over the API.

## Context
- Tables: `recipes`, `recipe_ingredients`, `pantry_items`, `grocery_items`, `meal_plan_entries` (one row per planned meal: date, recipe, servings, cooked flag).
- Use plain SQL migrations in `app/migrations/`, applied at startup; no ORM.
- Quantities are stored as a number plus a canonical unit (`g`, `ml`, `count`); normalization to those units is CAJ-4.

## Acceptance criteria
- [ ] Starting on an empty DB creates all five tables, and starting twice is a no-op — checked by: tests/test_migrations.py::test_migrations_are_idempotent
- [ ] Each entity supports create, get, list, update and delete under `/api/<entity>` — checked by: tests/test_crud.py (one parametrized case per entity)
- [ ] Deleting a recipe deletes its ingredient rows and unlinks its plan entries — checked by: tests/test_crud.py::test_delete_recipe_cascades
- [ ] A negative quantity is rejected with 422 — checked by: tests/test_crud.py::test_negative_quantity_rejected

## Verify
`make verify`

## Out of scope
Business logic (pantry decay, grocery computation, planning), importing recipes, UI changes.

## Escalation
none
