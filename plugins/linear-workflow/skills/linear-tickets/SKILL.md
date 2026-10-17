---
name: linear-tickets
description: Use when an agent needs to find Ready work in Linear, claim a ticket, promote Backlog tickets, report evidence, close a ticket, or escalate it to a human. Covers the status mapping, blocker checks, the evidence comment template and the Needs Human label, via the Linear MCP tools. Works unattended.
---

# Working Linear tickets the same way every time

Inputs: a **team** key and a **project** name. The examples use team `ROB`, project `agent-toolkit`. Tickets follow the contract in the `ticket-spec` skill (agentic-workflow plugin).

## Tools

Load them first: `ToolSearch select:mcp__Linear__list_issues,mcp__Linear__get_issue,mcp__Linear__save_issue,mcp__Linear__save_comment`.

Sessions that already have the Linear connector need nothing more. Headless runs use this plugin's `.mcp.json`: it registers `https://mcp.linear.app/mcp` with `Authorization: Bearer ${LINEAR_API_KEY}`, so export `LINEAR_API_KEY` (a Linear personal API key) before starting. Without it the server shows up unauthenticated and every call fails; stop and report that, do not guess.

## Status mapping

| Linear state | Meaning |
|---|---|
| Backlog | Not ready: unrefined, or blocked |
| **Todo** | **Ready**: contract-complete, all blockers Done |
| In Progress | Claimed by an agent; work underway |
| In Review | PR open, waiting for the reviewer |
| Done | Merged and evidenced |
| Canceled, Duplicate | Closed without work; never pick these up |

Label **Needs Human** = escalated. Skip any ticket that has it.

## Find Ready work

1. `list_issues(project="agent-toolkit", state="Todo", fields=["title","status","labels"])`. Drop tickets labeled Needs Human. Oldest/lowest number first.
2. For each candidate `get_issue(id, includeRelations=true)`. `relations.blockedBy` lists blockers but **not their state**, so call `get_issue(blockerId, fields=["status"])` on each one.
3. The ticket is workable only when every blocker is `Done`. A blocker in Canceled or Duplicate does not count as Done: escalate (below) instead of working it.
4. Read the whole description. If it is ambiguous or contradicts the code, escalate; do not guess.

## Promote Backlog to Ready

For each Backlog ticket in the project whose blockers are all Done:

1. Save its description to a file and run `python3 $TOOLKIT/scripts/lint_ticket.py <file>` (`$TOOLKIT` is the agent-toolkit checkout; Linear renders bullets as `*`, the linter accepts `-`, `*` and `+`).
2. Exit 0: `save_issue(id, state="Todo")`.
3. Lint failures: escalate with the linter output as the reason and leave it in Backlog.

## Claim

`save_issue(id, state="In Progress")` before touching code, so two runs never take the same ticket. If it is already In Progress and nobody else is working it (an interrupted run), resume its branch instead of starting over.

## Report progress

* PR opened: `save_issue(id, state="In Review")`, then a comment with branch, PR link and verify result.
* Review passed and PR merged: post the evidence comment below, then `save_issue(id, state="Done")`.
* Review failed: keep In Review, comment the findings, fix, repeat. Two failed gates: escalate.

## Evidence comment

Never set Done without this comment already posted. Use real bullets (`*`) and real newlines.

```
**Evidence**

* PR: <url>
* Verify: `<command>` -> <last line of output, e.g. verify: OK>
* Criteria checked:
  * [x] <criterion text> -> <how it was checked: command, output, file:line>
  * [x] <next criterion> -> <evidence>
* Reviewer verdict: PASS (<one-line summary>)
```

Every acceptance criterion in the ticket appears once. A criterion you could not check is `[ ]` with the reason, and the ticket is not Done: escalate. "Tests pass" alone is not evidence; name the command and the result.

## Escalate

Escalate when criteria are ambiguous, a gate failed twice, an action is irreversible, the change touches security, or a blocker is not Done and will not become Done.

1. `save_issue(id, addLabels=["Needs Human"])`. `addLabels` only appends; do not use `labels`, which replaces the whole set.
2. `save_comment(issueId=id, body=...)`:

```
**Escalated: needs a human**

* Reason: <what blocked you, with the evidence: lint output, failing command, conflicting lines>
* Question: <the one specific question whose answer unblocks the work>
* State: <branch / PR, what is done, what is untouched>
```

3. Leave the state as it was (Todo or In Progress) and move on to the next ticket. A human removes the label after answering.

## Rules

* Never close (Done) without the evidence comment. Never cancel a ticket you did not create.
* One state change per `save_issue` call is fine; `state` accepts the name ("In Review").
* Do not edit a ticket's description to make it pass: that changes the contract. Comment instead.
* Linear renders `-` bullets as `*`; match that in comments so text round-trips.
