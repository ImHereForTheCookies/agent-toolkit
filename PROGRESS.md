# PROGRESS

Append-only log of work sessions. Add new entries at the bottom; do not edit old ones.

## 2026-10-17 - ROB-5: Scaffold the marketplace repo
- Ticket: ROB-5
- Outcome: repo is a valid Claude Code marketplace listing four plugins (agentic-workflow, code-navigation, linear-workflow, project-template); `make verify` and `make smoke` added; CI runs `make verify` on push and PR.
- Next step: fill in plugin contents (skills, agents, hooks) and the full README in later tickets.

## 2026-10-17 - ROB-6: Ticket linter script
- Ticket: ROB-6
- Outcome: `scripts/lint_ticket.py` (stdlib) rejects tickets lacking the testable-ticket contract (six required `##` sections, `checked by:` on every acceptance criterion, escalation in none/taste-checkpoint/security/irreversible); exposes `lint(text)` and a CLI (files or `-`, exit 1 on problems). Tests in `tests/test_lint_ticket.py`; `make verify` gains step 4, which lints every `*.md` under any `tickets/` directory (skips when none).
- Next step: add real tickets under `tickets/` (or wire the linter into the Linear ticket-creation flow) so the verify step has something to check.

## 2026-10-17 - ROB-7: Fixture project for testing the toolkit
- Ticket: ROB-7
- Outcome: `fixtures/demo-project/` (FastAPI + SQLite pantry API, 15 pytest tests, `make dev|test|e2e|verify`, e2e smoke over HTTP on a free port) with three sample tickets DEMO-1..3 in contract format (DEMO-3 is contradictory on purpose, to exercise escalation). `fixtures/seeded-bug.patch` removes the negative-quantity check in PATCH; `scripts/check_seeded_bug.sh` asserts exactly `test_quantity_cannot_go_negative` fails. `make verify` gains step 5 (fixture verify) and step 6 (seeded bug); step 4 lints the fixture tickets automatically.
- Next step: use the fixture in end-to-end tests of the workflow skills/agents (implement DEMO-1/2, confirm DEMO-3 escalates).

## 2026-10-17 - ROB-8: decompose-project and ticket-spec skills
- Ticket: ROB-8
- Outcome: `plugins/agentic-workflow/skills/ticket-spec` (contract, sizing, testable criteria, linter gate; good/bad examples in `references/examples.md`) and `skills/decompose-project` (goal -> milestones -> tickets -> dependencies -> taste checkpoints -> lint -> approval before Linear; walkthrough in `references/`). Worked example `examples/cajunt/` (brief + CAJ-1..10, a DAG; only CAJ-1 is Ready). `scripts/check_ticket_graph.py` (stdlib; unknown blockers, duplicates, cycles; prints topological order) with `tests/test_check_ticket_graph.py`; `make verify` gains step 7. Step 4 already lints the example tickets. `claude plugin validate` does not inspect SKILL.md frontmatter (verified by deleting `name:`), so `tests/test_skills_frontmatter.py` checks name == folder, a `Use when...` description and the 150-line cap.
- Next step: dry-run decompose-project on a fresh brief in a scratch session, and wire `check_ticket_graph.py` into the Linear creation flow in the linear-workflow plugin.

## 2026-10-17 - ROB-9: harness-init skill and project template
- Ticket: ROB-9
- Outcome: `plugins/project-template/` now ships `templates/` (CLAUDE.md under 60 lines with Stack/Commands/Architecture decisions/Gotchas/Workflow, PROGRESS.md, Makefile with dev/test/e2e/verify plus a `symbols` stub, `.claude/settings.json` registering `ImHereForTheCookies/agent-toolkit` via `extraKnownMarketplaces` and enabling all four plugins via `enabledPlugins`; schema checked against the Claude Code docs), `scripts/harness_init.py <dir> [--name] [--force]` (stdlib; substitutes `{{PROJECT_NAME}}`, never overwrites without `--force`, `git init` only when `.git` is missing, prints created/skipped list) and the `harness-init` skill. Tests in `tests/test_harness_init.py`; `make verify` gains step 8 (init an empty temp dir, run its `make verify`).
- Next step: ROB-10 fills the `symbols` target stub with the repo-map script. Note project `extraKnownMarketplaces` only applies after the user trusts the folder.

## 2026-10-17 - ROB-10: navigate-codebase skill and repo-map script
- Ticket: ROB-10
- Outcome: `plugins/code-navigation/scripts/repo_map.py <root> [--out] [--max-bytes]` (stdlib; Python via `ast` with methods one level deep, JS/TS via regex on unindented declarations; sorted, timestamp-free output with a "generated, do not edit" header; `--max-bytes` cuts at a whole line and appends `... truncated (N more files)`; skips `.git`, `.venv`, `venv`, `node_modules`, `__pycache__`, `dist`, `build` and dot-directories). `navigate-codebase` skill (search order, delegation, module notes, map refresh). The project-template Makefile `symbols` target runs the script when `TOOLKIT=<checkout>` or `REPO_MAP=<path>` points at it and otherwise prints a skip message, so a fresh project's `make verify` stays green. Tests in `tests/test_repo_map.py` plus a symbols case in `tests/test_harness_init.py`; `make verify` gains step 9 (map the fixture).
- Next step: have the harness-init flow suggest setting `TOOLKIT`, and optionally add a drift check (`git diff --exit-code docs/symbols.md`) to projects that commit the map.

## 2026-10-17 - ROB-11: linear-tickets skill
- Ticket: ROB-11
- Outcome: `plugins/linear-workflow/skills/linear-tickets/SKILL.md` (status mapping Todo = Ready and Needs Human = escalated, finding Ready work with a per-blocker `get_issue` state check because `relations.blockedBy` carries no state, Backlog promotion gated by `scripts/lint_ticket.py`, claiming, evidence comment template, escalation via `addLabels` + comment, never Done without evidence) and `plugins/linear-workflow/.mcp.json` (http server `https://mcp.linear.app/mcp`, `Authorization: Bearer ${LINEAR_API_KEY}`; schema checked against the Claude Code MCP docs). Tests in `tests/test_linear_workflow.py`; the frontmatter test now expects the skill. Live check in project agent-toolkit: ROB-28 went Todo -> In Progress -> In Review -> Done with an evidence comment, ROB-29 got Needs Human + comment (label removed again); both ended Canceled.
- Next step: ROB-15 (nightly-run) should call this skill instead of the inline picking rules in `orchestration/NIGHTLY.md`.

## 2026-10-17 - ROB-12: human-in-the-loop skill
- Ticket: ROB-12
- Outcome: `plugins/agentic-workflow/skills/human-in-the-loop/SKILL.md` (six triggers with action and label, stricter-row precedence, "not triggers" list, reviewer-overreach guard, escalation comment template; Linear mechanics are delegated to `linear-tickets`). `evals/hitl/scenarios.json` (6 new scenarios, one per action label, incl. a DEMO-3 contradiction and a `proceed` over-escalation check), `evals/hitl/run_eval.py` (`claude -p` with no tools/settings in an empty cwd, label-only answer, table + score, exit 0 at >= 5/6), `evals/hitl/README.md` procedure, `make eval-hitl`, and `tests/test_hitl_scenarios.py` (structure only, runs in verify). Eval run: 6/6.
- Next step: ROB-15 nightly-run should cite this skill; consider re-running `make eval-hitl` whenever the skill text changes.

## 2026-10-17 - qa-ticket skill and nightly runbook rewiring
- Ticket: none (direct request from Robert after cutting the toolkit down; superpowers now covers the per-ticket build loop)
- Outcome: `plugins/agentic-workflow/skills/qa-ticket/SKILL.md` (+ `references/playwright.md`): fresh QA subagent runs the PR branch (`make dev`, wait for health), exercises each acceptance criterion with curl or Playwright (preinstalled Chromium in /opt/pw-browsers), tries 2-3 edge cases plus a smoke of the main flow, is skeptical by default, passes taste checkpoints functionally with screenshots, stops the app, makes no code changes, and replies `QA: PASS|FAIL` with a per-criterion table or `QA: SKIPPED (no runnable app)`. `orchestration/NIGHTLY.md`: agent-toolkit removed as a work source (still cloned for runbook/briefs/skills), per-ticket loop is implement -> review -> QA -> merge only on review PASS and QA PASS/SKIPPED (QA FAIL = review FAIL, one fix round), escalation delegated to the human-in-the-loop skill, new Superpowers section (TDD + verification yes; no brainstorming or questions unattended). Briefs updated accordingly. Frontmatter test expects the new skill.
- Next step: dry-run the nightly loop on the fixture project to see the QA agent against `fixtures/demo-project` (`make dev`, port 8765).

## 2026-10-18 - Nightly runbook: stack PRs when merges are blocked
- Ticket: none (direct request from Robert, approved, after the ROB-19 merge was denied by the permission classifier)
- Outcome: `orchestration/NIGHTLY.md`: a denied or failed merge no longer escalates or stops the run. The ticket stays In Review as "waiting on merge", pending-merge tickets count as satisfied blockers, the next ticket is built stacked on the newest pending branch, merged parents trigger a reconcile and base retarget, stack cap of 8, the chain continues.
- Next step: watch the first chained run to see it stack correctly.

## 2026-10-19 - Nightly loop: build first, then R&D (idea lab, grow, launch prep)
- Ticket: none (direct request from Robert: turn the 3 AM build job into a loop that also researches and validates new app ideas, grows promising POCs and prepares launches, at zero cost beyond tokens)
- Outcome: `orchestration/NIGHTLY.md` now builds a dynamic project map from Linear projects labelled `POC` (each with a `Folder:` line; all POCs live in the cajunt repo, `pocs/<slug>/`), passes the project folder to every subagent, and when no ticket is eligible runs one R&D unit from the new `orchestration/RND.md` (priority: launch prep, grow, greenlight, validate, ideate; Idea Lab project in Linear holds ideas; max 3 active POCs). New briefs: `RESEARCH_BRIEF.md` (ideate/validate with a 100-point rubric and hard gates, primary-source evidence only), `GROWTH_BRIEF.md` (max 3 evidence-backed tickets per POC per 7 days, max 8 open), `LAUNCH_BRIEF.md` (readiness tickets + a `Launch kit` issue with free-hosting steps and ready-to-paste community posts; store packaging only after Robert sets `Traction: yes`). Hard limits: never post, deploy, sign up, accept terms or spend money. Chaining continues per unit until nothing is eligible or 08:30 PT. Implementer/reviewer briefs handle project folders. `harness_init.py` no longer runs `git init` inside an existing work tree (monorepo subfolders). Tests: `tests/test_orchestration_refs.py`, new harness-init case.
- Next step: watch the first night's R&D units (ideate → validate → greenlight) and tune the 70-point greenlight bar.

## 2026-10-19 - Nightly loop: one full POC per night, self-improving
- Ticket: none (direct request from Robert after the R&D loop landed: go depth-first, one fleshed-out POC per night, spend leftovers on stocking ideas and improving the loop itself, iterate on the process after each POC)
- Outcome: `orchestration/RND.md` rewritten as a night plan: product evaluation → launch kit → retro → start tonight's POC (planner spec, then 6-10 feature-sized tickets; gated on fewer than 2 launch kits waiting for Robert) → grow launched POCs from real feedback only → validate/ideate to keep 2 validated ideas in reserve → process research. New `PRODUCT_EVAL_BRIEF.md` (skeptical whole-app evaluator as the target user, core criteria, max 2 rounds), `RETRO_BRIEF.md` (metrics, lessons kept/reverted, at most 3 evidence-backed process changes per PR; research mode for leftovers), `LESSONS.md` (seeded from research), `retros/`, and `HARD_LIMITS.md` (protected; hash pinned in `tests/test_orchestration_refs.py` so the retro loop can't change it). Launch kits now pre-register success/kill bars before posting. POC project description uses `Stage:`/`Eval:`/`Retro:`/`Greenlit:` lines.
- Next step: first retro after the first kit; check whether the eval catches bugs per-ticket QA missed.

## 2026-10-19 - Release cuts and speculative features
- Ticket: none (direct request from Robert: always keep a deployable version between validated and tested increments; spend leftover tokens on the next best feature)
- Outcome: `orchestration/release.sh` (verify + build, annotated `<slug>-vN` tag, fast-forward `release/<slug>`; exit 3 when nothing changed; root project excludes `pocs/`; never forces) with `tests/test_release_script.py` (6 cases on a throwaway repo + bare remote). `RND.md`: new unit 2 "Release cut" (first release right after product eval; later ones gated by a new PRODUCT_EVAL_BRIEF "release check" mode that blocks on core regressions or lost data and files fix tickets) and unit 9 "Speculative next-best feature" (max 2 per night, one ticket each via GROWTH_BRIEF "speculative" mode, label `Speculative`). Launch kits host from `release/<slug>`, never `main`. HARD_LIMITS.md gains rule 6 (release cuts only after the gate, never backward); hash updated at Robert's request. LESSONS.md and the night summary updated.
- Next step: first `cajunt-v1` cut after tonight's product eval of cajunt.

## 2026-10-20 - Retro: cajunt
- Ticket: none (retro mode, RETRO_BRIEF.md, project cajunt P-ROB-2, parked after eval round 2)
- Outcome: `orchestration/retros/2026-10-20-cajunt.md` (metrics, three sinks, what went well). Three changes, logged in `LESSONS.md`: decompose-project coverage table (also in the RND.md decomposer prompt), product-eval feature checklist with no un-ticketed findings (fix-ticket cap 6 to 8), and an explicit eval round number in RND.md unit 1. No old lessons were adoptable for review (seed rules only), none reverted. HARD_LIMITS.md untouched.
- Next step: when the next POC finishes round 1 eval, compare its Spec coverage failures and eval-added ticket count with cajunt's (2 core failures, 6 tickets) and set the three rules to kept or revert.

## 2026-10-21 - New POC every night; releases as branches
- Ticket: none (direct request from Robert after the 2026-10-21 night built cajunt fixes but started no POC)
- Cause found: (1) RND.md unit 5 only started a POC when no other POC was `building`/`evaluating`, and cajunt sat in `evaluating`; (2) Idea Lab was empty and ideate/validate ranked below release cut and launch kit; (3) the `cajunt-v1` release cut failed with HTTP 403 (cloud sessions may only push branches, never tags), and the next unit was the same release cut, so the chain stopped at 04:54.
- Outcome: `RND.md` split into Part A (start tonight's POC, validate, ideate; runs before any build ticket until a POC is greenlit tonight; caps of 6 validations and 2 ideation passes per night) and Part B (eval, release cut, launch kit, retro, grow, speculative features with no nightly cap, reserve stocking, process research). No cap on POCs in progress or on launch kits waiting. A `Release cut failed` comment skips that POC's release for the rest of the night. `release.sh` now creates a frozen `release/<slug>-vN` branch and fast-forwards `release/<slug>`, never tags, and repairs a cut whose second push was lost; tests updated (8 cases). `HARD_LIMITS.md` rule 6 reworded for branch releases and hash re-pinned at Robert's request. `NIGHTLY.md`, `PRODUCT_EVAL_BRIEF.md`, `LAUNCH_BRIEF.md`, `LESSONS.md`, `CLAUDE.md` updated.
- Next step: tonight's run should cut cajunt's first release as `release/cajunt-v1` and start a new POC from Part A.

## 2026-10-21 - idealab.ai as an ideation lead source; manual daytime runs
- Ticket: none (direct request from Robert)
- Outcome: `RESEARCH_BRIEF.md` ideate mode may seed candidates from idealab.ai (no login; filtered for low capital, solo, fast time to market, client-side fit) and records the idea's source; AI-generated idea databases never count as demand evidence. `NIGHTLY.md` gains a manual daytime run: fire text `Manual run requested by Robert, stop at HH:MM` replaces the 08:30 cutoff for that chain (or `..., no stop time` removes it, running until the usage limit) and is passed on when chaining.
- Next step: daytime test run to confirm Part A greenlights a POC and cajunt's first release cuts as `release/cajunt-v1`.
