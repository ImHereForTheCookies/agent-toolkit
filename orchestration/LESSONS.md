# Lessons (process rules learned from retros)

The retro and research passes (`RETRO_BRIEF.md`) append one line per adopted rule and update its status over later retros. Planners, decomposers and ideation read this file before starting, so rules here shape the next POC.

Format: `<date> | <rule> | <file changed> | <target metric> | status: watch|kept|reverted | evidence: <retro file or source links>`

## Seed rules (from research before the first POC, 2026-10-19)
- 2026-10-19 | A planner expands the idea into an ambitious product spec before tickets are written | RND.md unit 4 | spec coverage at product eval | status: watch | evidence: Anthropic, "Harness design for long-running application development" (a lone builder under-scoped the app; the planner was the component they kept)
- 2026-10-19 | A separate, skeptical evaluator uses the whole app as its target user before launch | PRODUCT_EVAL_BRIEF.md | bugs found after launch | status: watch | evidence: same article (self-evaluation approved broken work; a tuned skeptical evaluator caught wiring bugs)
- 2026-10-19 | Pre-launch POCs are not grown from research; growth waits for real feedback | RND.md unit 5 | features users actually use | status: watch | evidence: synthetic-user validity reviews (MeasuringU; arXiv 2607.26348) show LLM-simulated users are not reliable evidence of demand
- 2026-10-19 | No new POC while 2 launch kits wait for Robert | RND.md unit 4 | POCs launched per week | status: watch | evidence: distribution, not building, is the bottleneck for small apps; unlaunched apps produce no validation
