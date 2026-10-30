# Settings: values the loop reads, not values baked into the runbooks

The runbooks (`NIGHTLY.md`, `RND.md`, the briefs) refer to setup-specific values as `{{KEY}}`. Nothing about one person's team, repos, paths, caps or thresholds lives in this repo.

## Where the values come from
1. At the start of every run, fetch the page named as `Settings page` in the scheduled task's prompt (a Notion page with a code block of `KEY: value` lines).
2. A key missing there takes the default below. A key with no default and no value is required: end the run with a one-line note naming the missing key.
3. Substitute the values wherever a runbook or brief says `{{KEY}}`. Briefs given to subagents get the substituted text, never raw placeholders.
4. Changing a setting means editing that page. Do not edit values into the runbooks.

## Keys
| Key | Default | Meaning |
|---|---|---|
| `OWNER` | `the owner` | Name used where the briefs say who reviews, launches or is notified |
| `LINEAR_TEAM` | required | Linear team key holding POC projects and the Idea Lab |
| `SCHEDULER_TRIGGER_ID` | required to chain | Scheduled task a finished run fires to start the next run; unset means no chaining (the run continues in-session) |
| `WORK_DIR` | `~/work` | Where repos are cloned |
| `POC_REPO` | required | `owner/name` of the repo that holds the prototypes |
| `TOOLKIT_REPO` | `owner/name` this toolkit was cloned from | `owner/name` of this toolkit |
| `ACTIVE_WINDOW_MINUTES` | `60` | A ticket In Progress and touched within this window means another run is active; `0` disables the guard |
| `STACK_PR_CAP` | `8` | Most open stacked PRs before a run switches to R&D |
| `MIN_IDEA_SCORE` | `70` | Validation score an idea needs to be greenlit |
| `VALIDATIONS_PER_NIGHT` | `12` | Most idea validations per night |
| `IDEATION_PASSES_PER_NIGHT` | `4` | Most ideation passes per night |
| `IDEA_RESERVE_TARGET` | `4` | Validated (In Review) ideas to keep in reserve |
| `SUBAGENT_MODEL` | `sonnet` | Model for R&D unit subagents |
| `SUBAGENT_EFFORT` | `high` | Effort for R&D unit subagents |

Derived: `POC_DIR` = `{{WORK_DIR}}/<name part of POC_REPO>`, `TOOLKIT_DIR` = `{{WORK_DIR}}/<name part of TOOLKIT_REPO>`.

`HARD_LIMITS.md` is deliberately not configurable: it is hash-pinned and no setting can loosen it.
