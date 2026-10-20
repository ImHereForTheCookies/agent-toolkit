# Hard limits (protected)

These rules bind every run, unit and subagent of the nightly loop. The process-improvement loop (`RETRO_BRIEF.md`) may never edit, weaken, reword or work around this file; `tests/test_orchestration_refs.py` pins its hash, so only Robert can change it.

1. Never deploy, publish, post online, vote, or message anyone; never create accounts, accept terms or agreements, submit to an app store, or spend money. Those steps are *prepared* (scripts, checklists, ready-to-paste drafts) and handed to Robert as a Launch issue.
2. Never force-push, never delete branches, repos or Linear projects, never touch secrets or credentials.
3. Every POC and every feature keeps the zero-running-cost rule in `pocs/README.md` (cajunt repo): static PWA, data on the device, no backend, no paid API.
4. Never escalate by asking Robert and waiting: label Needs Human with a comment and move on (`plugins/agentic-workflow/skills/human-in-the-loop/SKILL.md`).
5. Changes to the loop itself (runbook, briefs, skills) go through a PR with an independent reviewer, like any ticket, and must cite the retro evidence that motivates them.
6. Release cuts: pushing a `<slug>-vN` tag and moving `release/<slug>` forward with `orchestration/release.sh` is allowed only after that project's release gate passed (`make verify`, `make build`, and the product evaluation or a release check). Never move a release branch backward, never force it, never point it at a commit that skipped the gate. Whether a host serves the release branch is Robert's setting, not the loop's.
