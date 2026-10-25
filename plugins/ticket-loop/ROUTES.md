# Ticket routes

Each Linear ticket carries one label from the **Skill** label group. `run-queue` reads this table to decide which skill works the ticket. Add rows with the `new-skill` skill; `tests/test_ticket_loop.py` checks every skill named here exists.

| Label | Skill | What it produces |
| --- | --- | --- |
| design | design-system | Notion design doc (new version), then a plan ticket |
| plan | plan-tickets | Linted build tickets in Linear and the doc's Plan section |
| build | build-ticket | Reviewed, QA'd, merged PR and an evidence comment |
| evaluate | evaluate-project | Graded evaluation in the doc, plus build or design tickets |

No Skill label: `build` if the description passes `$TOOLKIT/scripts/lint_ticket.py`, otherwise `plan`.
