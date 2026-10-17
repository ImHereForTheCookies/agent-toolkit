# Fixtures

`demo-project/` is a tiny FastAPI + SQLite pantry API used to test the toolkit itself.

- `seeded-bug.patch` removes the negative-quantity check in `PATCH /items/{id}`; only `test_quantity_cannot_go_negative` should fail. `scripts/check_seeded_bug.sh` asserts this, and the reviewer subagent is dry-run against it.
- `demo-project/tickets/DEMO-1` and `DEMO-2` are clear and implementable.
- `DEMO-3` contradicts itself on purpose: it asks for negative quantities while requiring `test_quantity_cannot_go_negative` to keep passing. The ticket itself carries no hint, so an orchestrator dry run only passes if the agent notices the contradiction and escalates instead of implementing it.
