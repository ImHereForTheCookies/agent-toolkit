# Cajunt brief

Cajunt is a local proof-of-concept agentic cooking planner. It is a clickable local web app backed by a local SQLite database with:

- a grocery list
- favorite recipes
- an estimated pantry: items are added when purchased, subtracted when a planned meal is cooked, and perishables decay by shelf life
- weekly recipe cards

An LLM planner proposes a week of meals that reuses ingredients and uses perishables first. The grocery list is computed as (the week's plan needs) minus (the pantry estimate).

Recipes can be imported from a URL using schema.org `Recipe` data.

## Stack
Python, FastAPI, SQLite, a simple responsive web UI (PWA-capable).

LLM calls must work against mocked responses when no API key is set, so the whole app runs and is testable offline.

## Out of scope for v0
Auth, sync, Instacart, nutrition, photo inventory.
