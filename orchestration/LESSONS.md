# Lessons (process rules learned from retros)

The retro and research passes (`RETRO_BRIEF.md`) append one line per adopted rule and update its status over later retros. Planners, decomposers and ideation read this file before starting, so rules here shape the next POC.

Format: `<date> | <rule> | <file changed> | <target metric> | status: watch|kept|reverted | evidence: <retro file or source links>`

## Seed rules (from research before the first POC, 2026-10-19)
- 2026-10-19 | A planner expands the idea into an ambitious product spec before tickets are written | RND.md unit 5 | spec coverage at product eval | status: watch | evidence: Anthropic, "Harness design for long-running application development" (a lone builder under-scoped the app; the planner was the component they kept)
- 2026-10-19 | A separate, skeptical evaluator uses the whole app as its target user before launch | PRODUCT_EVAL_BRIEF.md | bugs found after launch | status: watch | evidence: same article (self-evaluation approved broken work; a tuned skeptical evaluator caught wiring bugs)
- 2026-10-19 | Feedback-driven growth waits for launch; before that, at most 2 labelled Speculative features per night from leftovers (Robert's call), each gated by a release check | RND.md units 6 and 9 | features users actually use; speculative features reverted | status: watch | evidence: synthetic-user validity reviews (MeasuringU; arXiv 2607.26348) show LLM-simulated users are not reliable evidence of demand
- 2026-10-19 | No new POC while 2 launch kits wait for Robert | RND.md unit 5 | POCs launched per week | status: watch | evidence: distribution, not building, is the bottleneck for small apps; unlaunched apps produce no validation
- 2026-10-19 | Every evaluated POC keeps a release: `<slug>-vN` tag + `release/<slug>` branch moved forward only after verify, build and a release check; hosts serve the release branch, never main | RND.md unit 2, release.sh | release checks blocked; regressions reaching a release | status: watch | evidence: Robert's request (always a deployable version while work continues)
