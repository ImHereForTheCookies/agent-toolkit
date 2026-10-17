Status: Backlog

# CAJ-4 Normalize free-text ingredient lines

Blocked by: CAJ-1

## Goal
A pure function turns a line like "1 1/2 cups all-purpose flour, sifted" into a structured ingredient, so import, pantry and grocery math share one representation.

## Context
- New module `app/normalize.py` exposing `normalize(line: str) -> Ingredient(qty: float | None, unit: str | None, name: str, note: str | None)`.
- Convert to canonical units: mass in `g`, volume in `ml`, otherwise `count`. Use fixed conversions (1 cup = 240 ml, 1 tbsp = 15 ml, 1 tsp = 5 ml, 1 oz = 28 g, 1 lb = 454 g).
- Handles mixed fractions ("1 1/2"), unicode fractions, ranges ("2-3", take the upper bound), and lines without a quantity ("salt to taste" gives qty None).
- The check is a fixed set of 50 lines in `tests/data/ingredient_lines.json`, each with its expected output, written before the implementation. Do not edit expected values to make tests pass; if one looks wrong, escalate.

## Acceptance criteria
- [ ] All 50 lines in the fixed set normalize to their expected output — checked by: tests/test_normalize.py::test_fixed_set_of_50_lines
- [ ] The set covers fractions, unicode fractions, ranges, no-quantity lines, parenthetical notes and each unit family — checked by: tests/test_normalize.py::test_fixed_set_covers_all_categories
- [ ] `normalize` never raises; an unparseable line returns the whole line as `name` with qty None — checked by: tests/test_normalize.py::test_never_raises_on_garbage
- [ ] The function does no I/O and makes no network call — checked by: tests/test_normalize.py::test_normalize_is_pure

## Verify
`make verify`

## Out of scope
Ingredient synonyms or fuzzy matching ("scallion" vs "green onion"), non-English lines, density conversions between mass and volume.

## Escalation
none
