Status: Backlog

# CAJ-8 Week planner backed by an LLM, with a mocked mode

Blocked by: CAJ-3, CAJ-4, CAJ-6

## Goal
Asking for a week plan returns seven proposed meals from saved recipes that reuse ingredients and use perishables first, with or without an API key.

## Context
- New module `app/planner.py`; `POST /api/plan/propose` returns entries and stores them in `meal_plan_entries`.
- The prompt includes the saved recipes, the pantry estimate and each perishable's days left. The response is JSON: a list of `{date, recipe_id}`.
- Behind a `PlannerLLM` interface with two implementations: the real one (used only when `ANTHROPIC_API_KEY` is set) and a mock that returns canned responses from `tests/data/llm/`. With no key the mock is used automatically and the response says `"mode": "mock"`.
- The model output is validated: unknown recipe IDs or malformed JSON trigger one retry, then a 502. Tests cover both with the mock.
- The ranking heuristics (reuse, perishables first) are checked on the prompt contents, not on live model output.

## Acceptance criteria
- [ ] With no API key set, `POST /api/plan/propose` returns 7 entries with `"mode": "mock"` and makes no network call — checked by: tests/test_planner.py::test_mock_mode_without_api_key
- [ ] The prompt lists every perishable with its days left, soonest-expiring first — checked by: tests/test_planner.py::test_prompt_lists_perishables_soonest_first
- [ ] A response naming an unknown recipe ID is retried once and then rejected with 502 — checked by: tests/test_planner.py::test_unknown_recipe_id_retries_then_502
- [ ] Malformed JSON is retried once and then rejected with 502 — checked by: tests/test_planner.py::test_malformed_json_retries_then_502
- [ ] Proposing again replaces the previous uncooked plan entries and keeps cooked ones — checked by: tests/test_planner.py::test_repropose_replaces_uncooked_only

## Verify
`make verify`

## Out of scope
Evaluating plan quality with the real model, user preferences or dietary rules, a plan UI, streaming responses.

## Escalation
none
