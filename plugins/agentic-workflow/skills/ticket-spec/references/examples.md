# Ticket examples

## A good ticket

```markdown
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
```

Why it works:

- The Goal is an outcome. The Context points at the exact files and defines the one ambiguous word ("low").
- Each criterion is a behaviour with an exact input and output, and names the test that checks it. The second one guards against regressions.
- Invalid input is specified (422), so the worker does not invent an error format.
- Out of scope names the nearby features a worker might be tempted to add.
- Small: one endpoint, three criteria, one session.

## A bad ticket

```markdown
# Improve the recipe page

## Goal
Make the recipe page better and faster, and also clean up the importer
while you're in there.

## Context
The recipe page is slow and ugly. See the code.

## Acceptance criteria
- [ ] The page loads fast
- [ ] The design looks clean and modern
- [ ] Importer code is refactored
- [ ] Everything works on mobile

## Verify
Check it works.

## Escalation
maybe
```

What is wrong, in order of damage:

1. **Title** has no ID and is not specific ("Improve" names no outcome). Nobody can refer to it or order it among others.
2. **Goal** mixes two unrelated areas (the page and the importer) with "and also". Split into two tickets.
3. **Context** has no file names, no measurements and no decisions. "Slow" and "ugly" are opinions; the worker must guess what to change.
4. **Criteria** have no `checked by:`. "Fast" and "clean and modern" are adjectives with no number or reviewer; "refactored" describes code, not behaviour; "works on mobile" has no viewport. Rewrite as, for example, "the page's largest contentful paint is under 2 s on the 20-recipe fixture — checked by: `make perf`" and "no horizontal scroll at 390 px — checked by: tests/e2e/phone.spec.ts".
5. **Verify** names no command, so there is no gate.
6. **Out of scope** is missing, so the worker may touch anything.
7. **Escalation** is "maybe", which is not a value. The visual part wants `taste-checkpoint`.

The linter catches 4 to 7 mechanically (missing sections, no `checked by:`, invalid escalation). Items 1 to 3 need judgement, which is why the linter is a gate and not the whole review.
