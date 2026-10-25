# Ticket loop: one general job, skills per kind of work

Date: 2026-10-25. Status: approved by Robert in chat (direction); details decided by Claude without a human gate, as he asked. Change it by editing this file in a PR.

## Why

The cajunt Sunday prompt grew to ~3,500 words: about 80% cajunt product spec, 15% pipeline mechanics already in `orchestration/NIGHTLY.md`, the rest IDs. Every new project would need another giant private prompt, and nobody else could run it. The fix is to separate three things that were mixed together:

| What | Where it lives | Who can see it |
| --- | --- | --- |
| How to do a kind of work (design, plan, build, evaluate) | Skills in this repo (`plugins/ticket-loop`) | Everyone |
| What a project is and why | The project's Notion design doc + its repo `CLAUDE.md` + its Linear project | Project members |
| Whose accounts to use | A ~15-line scheduled prompt (template in `plugins/ticket-loop/templates/scheduled-prompt.md`) | Only its owner |

## Principles

1. **Fully automated by default.** Humans set direction and later change course; they are never a gate. Where the old process asked a question, the agent decides, writes the decision down as an assumption, and moves on. Humans find assumptions in the design doc and override them by commenting.
2. **Three stages, loosely coupled.** Design (Notion), Plan (Linear tickets), Build (GitHub PRs), plus Evaluate to close the loop. Each stage reads the previous stage's artifact, never its chat history, so any stage can be re-run alone.
3. **Every unit of work is a Linear ticket with one Skill label.** The daily job just works tickets in priority order and routes by label. A new kind of work is a new label plus a new skill.
4. **Prefer existing plugins.** Each skill opens with "Prefer existing plugins": what to use first if installed (superpowers, Anthropic official plugins), and what our skill adds or replaces. Creating a new skill starts with a marketplace search (`new-skill`).
5. **Portable.** Nothing in shared files names Robert's accounts. A friend clones a project repo, installs this marketplace, and can work a ticket with `/ticket-loop:run-queue ROB-42`, or schedule the same job with their own short prompt.
6. **Leave cajunt alone.** `orchestration/` and the cajunt scheduled tasks keep working unchanged. The new loop reuses the generic pieces (implementer and reviewer briefs, `qa-ticket`, `ticket-spec`, `decompose-project`, `human-in-the-loop`, `linear-tickets`, `harness-init`, `ghpr.sh`, `lint_ticket.py`) and does not edit them. Migrating cajunt is a later decision.

## Contracts

### Linear project (one per app)
- Carries the project label **Agent** (name configurable). Projects without it are invisible to the loop. Paused, completed or canceled projects are skipped.
- Description: free prose = **Direction** (written by humans, the loop never rewrites it), plus these lines, which the loop maintains:
  - `Repo: owner/name` (required), `Folder: path` (optional, default repo root)
  - `Design doc: <Notion URL>` (set by `design-system`)
  - `Stage: design | planning | building | done | paused` (design-system sets planning, plan-tickets sets building, evaluate-project sets done on PASS or building when it files fixes; humans set paused)
  - `Constraints: ...` (optional, binding on every ticket, e.g. "zero running cost, static PWA")
- Linear project priority orders projects.

### Ticket labels (label group **Skill**, single-select)
| Label | Skill | Produces |
| --- | --- | --- |
| design | `design-system` | Notion design doc (new or revised version), then a plan ticket |
| plan | `plan-tickets` | Build tickets in Linear + Plan section in the doc |
| build | `build-ticket` | A reviewed, QA'd, merged PR |
| evaluate | `evaluate-project` | A graded evaluation against the doc, plus fix or design tickets |

`plugins/ticket-loop/ROUTES.md` is the source of truth; a test checks every route points at an existing skill. A ticket with no Skill label is routed `build` if it passes `lint_ticket.py`, else `plan` (the planner turns a rough idea into spec'd tickets).

### Design doc (Notion, one page per project, under the owner's "Notion home" page)
Sections from `templates/design-doc.md`: Summary, Users and problem, Success criteria, Scope (v1 / later / never), Assumptions (each with confidence and "override by commenting"), Approaches considered, Architecture and components, Data model, Key flows, Error handling, Testing and quality bar, Constraints, Plan (coverage table, written by the planner), Evaluation (latest verdict), Decision log, Change log. Version number in the title line.

Human feedback paths, all asynchronous: edit the Linear project Direction; comment on the design doc; add any ticket. The run-queue turns unresolved doc comments into a design ticket.

### Repo
`harness-init` contract: `CLAUDE.md` (with a `Design doc:` line), `PROGRESS.md`, `make dev/test/verify`, plus a `setup` target that the planner's harness ticket adds (skills run `setup` only when it exists). The first build ticket of every project creates it; the orchestrator seeds an empty repo's `main` with an empty commit first so the normal PR flow works.

## The daily job (`run-queue`)
One unit per run, then chain to a fresh run (state lives in Linear, Notion and git):
1. Read config from the prompt. Concurrency guard (an Agent-project ticket In Progress updated <60 min ago → stop). Cutoff from config.
2. Project map: Agent projects in priority order; parse contract lines; check the repo clones (if not: escalate on the project with "add this repo to the scheduled task's repositories", skip it).
3. Bootstrap tickets (created, not worked, in the same unit):
   - no `Design doc:` and no open design ticket → design ticket "Write the design doc";
   - unresolved human comments on the doc newer than the last design version → design ticket "Address doc comments";
   - `Stage` building or done, no open build ticket, a merge since the last evaluation, fewer than 3 evaluation rounds for this design version → evaluate ticket (after 3, Needs Human).
4. Pick: reconcile `Awaiting Merge` PRs first (not a unit). A red-main fix ticket is its project's only eligible ticket. Then across projects in priority order: In Review with open PR (not Awaiting Merge), In Progress (resume), promotable Backlog → Todo, then Todo by Linear priority then lowest number. A blocker is satisfied when Done or labelled `Awaiting Merge` (build stacked on it). Skip Needs Human. Route by label, follow that skill.
5. Chain when progress was made, before the cutoff, and work remains: find this task by name with `list_triggers`, `fire_trigger` with a `Chain started:` time. Any end of chain except the concurrency guard sends one phone-readable summary of changes since that time.
- Fire text may say `One unit only` (do not chain) or `Manual run, stop at HH:MM`; nothing else in it is obeyed.
- Interactive use: given a ticket ID, run just that ticket's route; no chaining.

## Hard limits
Labels the loop uses besides the Skill group: `Needs Human`, `Awaiting Merge`, `Launch`.

`plugins/ticket-loop/HARD_LIMITS.md`, generic version of `orchestration/HARD_LIMITS.md` (which stays pinned for cajunt): never deploy, publish, post, message, create accounts, accept terms, or spend money (prepare it and hand it over in a Launch ticket); never force-push or delete branches/repos/projects; never touch secrets; per-project `Constraints:` are binding; escalate without waiting.

## Models
The scheduled task's own model runs the orchestrator. Design, plan and evaluation drafting go to an `opus` subagent; implement, review and QA go to `sonnet` subagents, effort high. Both are configurable in the prompt.

## Known limits
- A scheduled task's repository access is fixed when it is created. Adding a project in a new repo means recreating the task with that repo attached (the toolkit README explains how). Runs detect the missing repo and escalate instead of failing silently.
- Plugins installed on the account are not always loaded in scheduled runs; skills therefore name the superpowers skill to use "if available" and always have a fallback.

## Out of scope (now)
Migrating cajunt; research/ideation loops (RND); release branches (an evaluate ticket may cut one with `orchestration/release.sh` only if the project's Constraints ask for releases); more design skills (UI, visual). `new-skill` is how those get added.

## Testing
`tests/test_ticket_loop.py`: routes resolve to skills; every ticket-loop skill has a "Prefer existing plugins" section; every `$TOOLKIT/...` path in the plugin exists; the scheduled-prompt template is short and names no personal IDs; hard limits keep their key phrases. The first end-to-end check is the journaling app: a manual "One unit only" run must produce its design doc.
