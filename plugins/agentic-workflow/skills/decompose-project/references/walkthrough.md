# Walkthrough: decomposing the Cajunt brief

Brief: `examples/cajunt/brief.md`. Result: `examples/cajunt/tickets/CAJ-1.md` to `CAJ-10.md`.

## 1. Goal in one sentence
A person can plan a week of meals from saved recipes in a local web app and get a grocery list that subtracts what the pantry already holds.

## 2. Milestones (each leaves the app runnable)
| Milestone | Tickets |
|---|---|
| Harness and skeleton: repo runs, one thing works in the browser | CAJ-1, CAJ-2 |
| Recipes: store and import them | CAJ-3, CAJ-4, CAJ-5 |
| Pantry and grocery: the estimate and the list | CAJ-6, CAJ-7 |
| Planning: LLM proposes a week, offline-testable | CAJ-8 |
| Experience: cards UI, phone pass | CAJ-9, CAJ-10 |

## 3. Choices worth copying
- CAJ-1 is the scaffold and CAJ-2 the walking skeleton, as always.
- Normalization (CAJ-4) is its own ticket because import, pantry and grocery all depend on it, and it has a crisp check: a fixed set of 50 ingredient lines with expected output, written before the code.
- The LLM planner (CAJ-8) is checked against a mocked model. Real-model quality is out of scope because it cannot be a pass/fail criterion.
- Brief items became tickets one-to-one only where they were features. "Grocery list", "favorite recipes" and "recipe cards" are not three tickets for three tables; the schema is one ticket (CAJ-3) and each behaviour has its own.

## 4. Dependencies
```
CAJ-1  (none)
CAJ-2  <- CAJ-1
CAJ-3  <- CAJ-2
CAJ-4  <- CAJ-1
CAJ-5  <- CAJ-3, CAJ-4
CAJ-6  <- CAJ-3, CAJ-4
CAJ-7  <- CAJ-6
CAJ-8  <- CAJ-3, CAJ-4, CAJ-6
CAJ-9  <- CAJ-5, CAJ-8
CAJ-10 <- CAJ-7, CAJ-9
```
CAJ-4 only needs the repo, so it can run in parallel with CAJ-2 and CAJ-3. CAJ-5 and CAJ-6 can run in parallel once CAJ-3 and CAJ-4 are done; CAJ-7 and CAJ-8 then follow CAJ-6.

## 5. Taste checkpoints
- CAJ-2: first UI of the project.
- CAJ-9: sets the visual direction of the cards.
Everything else is `none`.

## 6. Gate
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/lint_ticket.py" examples/cajunt/tickets/*.md` and `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/check_ticket_graph.py" examples/cajunt/tickets`. Both are part of `make verify`.
