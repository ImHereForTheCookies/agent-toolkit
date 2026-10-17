# human-in-the-loop eval

Checks that an agent with fresh context, given only `plugins/agentic-workflow/skills/human-in-the-loop/SKILL.md` and a situation, picks the expected action.

## Files
- `scenarios.json` - 6 scenarios: `id`, `situation`, `expected_action`. Each action label appears once; `fixed-typo` is the over-escalation check (the right answer is `proceed`), `contradictory-ticket` mirrors `fixtures/demo-project/tickets/DEMO-3.md`.
- `run_eval.py` - runs `claude -p` per scenario with no tools, no settings and an empty working directory, so only the skill text and the situation are visible. Prints a table and the score; exit 0 when score >= 5/6.

## Procedure
1. `make eval-hitl` (needs the `claude` CLI logged in; about 6 short API calls). Optional: `python3 evals/hitl/run_eval.py --model <model>`.
2. Pass = score of 5/6 or more. Record the score and the table in the ticket / PR.
3. If a scenario fails, read the skill row it should have matched. Fix the skill wording first; change a scenario only when the situation really was ambiguous. Do not add the answer label to the situation text.

Not part of `make verify` because it costs API calls. `tests/test_hitl_scenarios.py` (in verify) only validates the structure of `scenarios.json`.
