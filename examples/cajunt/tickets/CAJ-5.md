Status: Backlog

# CAJ-5 Import a recipe from a URL using schema.org data

Blocked by: CAJ-3, CAJ-4

## Goal
Pasting a recipe URL creates a recipe with normalized ingredients, so favorites do not have to be typed in.

## Context
- Fetch the page, find `<script type="application/ld+json">` containing a `Recipe` (it may sit inside `@graph` or a list), read `name`, `recipeIngredient`, `recipeInstructions`, `recipeYield`.
- Run each `recipeIngredient` through `normalize` (CAJ-4) and store via the CRUD layer (CAJ-3).
- Tests never touch the network: they use saved HTML pages in `tests/data/pages/` (one plain, one with `@graph`, one without a recipe) and an injected fetch function.

## Acceptance criteria
- [ ] `POST /api/recipes/import {"url": ...}` on the plain page creates a recipe with the expected title and ingredient count — checked by: tests/test_import.py::test_import_plain_page
- [ ] A `Recipe` nested in `@graph` is found — checked by: tests/test_import.py::test_import_graph_page
- [ ] A page with no recipe data returns 422 with `no_recipe_found` and creates nothing — checked by: tests/test_import.py::test_import_without_recipe_data
- [ ] A fetch failure returns 502 and creates nothing — checked by: tests/test_import.py::test_import_fetch_failure
- [ ] Importing the same URL twice updates the existing recipe instead of duplicating it — checked by: tests/test_import.py::test_import_same_url_is_idempotent

## Verify
`make verify`

## Out of scope
Sites without schema.org data (HTML scraping), importing from images or PDFs, any UI for the import form.

## Escalation
none
