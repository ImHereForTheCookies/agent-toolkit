---
name: ticket-spec
description: Use when writing, reviewing or fixing a ticket that an agent will implement unattended, or when a ticket is being moved to Ready. Covers the ticket contract (Goal, Context, Acceptance criteria with `checked by:`, Verify, Out of scope, Escalation), sizing, writing testable criteria, and running the linter gate.
---

# Writing a ticket an agent can finish

A worker agent gets the ticket and nothing else: no chat history, no chance to ask what you meant. A good ticket lets it work alone, prove it is done, and know when to stop and ask. A good example and a bad one with annotations are in [references/examples.md](references/examples.md).

## Title and header lines

```
Status: Ready

# CAJ-5 Import a recipe from a URL using schema.org data

Blocked by: CAJ-3, CAJ-4
```

- Title is `# <ID> <imperative title>`: the ID first (tools read it), then a verb phrase ("Add", "Fix", "Replace"), not a noun pile.
- `Status:` is optional and used by the local tracker (`Backlog`, `Ready`, ...). Linear carries status itself.
- `Blocked by: ID, ID` is optional, comma-separated, and omitted when there are no blockers. `scripts/check_ticket_graph.py` reads it.

## The contract

Every ticket has these `##` sections, in this order.

| Section | Contents | Why it exists |
|---|---|---|
| **Goal** | One or two sentences: the outcome, not the steps. | Lets the worker make sensible calls on anything the ticket did not foresee. |
| **Context** | Files, modules, decisions already made, constraints, links. | Saves the worker from rediscovering (or contradicting) what you already know. |
| **Acceptance criteria** | Checklist; every item ends with `— checked by: <test/command/spec>`. | "Done" becomes something a script can confirm rather than an opinion. |
| **Verify** | The command(s) that run everything, usually `make verify`. | One unambiguous gate the worker and reviewer both run. |
| **Out of scope** | What the worker must not touch, even if tempting. | Stops scope creep and keeps the diff reviewable. |
| **Escalation** | Exactly one of `none`, `taste-checkpoint`, `security`, `irreversible`. | Tells the worker when to stop for a human instead of finishing. |

Escalation values: `taste-checkpoint` for visual or UX judgement calls (stop with a screenshot); `security` for auth, secrets, permissions or user data; `irreversible` for migrations, deletions, publishing, spending money; `none` otherwise. Pick the strongest that applies. Whatever the value, a worker that finds the ticket contradicts itself stops and escalates.

## Sizing

One ticket is one worker session, roughly one feature, ending in one reviewable change. Split when:

- there are more than about 8 acceptance criteria, or
- the work touches unrelated areas (say the importer and the phone layout), or
- you cannot state the Goal in two sentences without "and".

Do not go the other way and write a ticket per file or per function: the worker then spends its session on coordination. Prefer one slice that works end to end.

## Testable criteria

A criterion is testable when someone else could run the named check and get a pass or fail without asking you anything. That needs:

1. **Observable behaviour**: what a user, caller or log can see ("returns 422 with `no_recipe_found`"), not what the code is ("uses a clean parser").
2. **A named check**: a pytest id (`tests/test_x.py::test_name`), a command (`make pwa-check`), or a Playwright spec. If the test does not exist yet, name the file it should have; the worker writes it.
3. **Numbers instead of adjectives**: "fast", "clean", "intuitive" and "robust" mean nothing until they become "p95 under 200 ms on the 1,000-row fixture" or "no horizontal scroll at 390 px".

If a criterion can only be judged by looking, set Escalation to `taste-checkpoint` and make the check "reviewer sees the screenshot in the PR".

## Lint before Ready

From the toolkit repo:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/lint_ticket.py" <file> [<file> ...]
```

It exits non-zero and prints `FILE: problem` for missing sections, criteria without `checked by:` and an invalid Escalation value. **It is the gate before a ticket is marked Ready**: do not move a ticket to Ready, or create it in Linear as Ready, while it reports problems. Passing the linter shows the form is right; you still own whether the criteria are the right ones.

For tickets forming a set, also run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/check_ticket_graph.py" <dir>` to catch unknown blockers and cycles.
