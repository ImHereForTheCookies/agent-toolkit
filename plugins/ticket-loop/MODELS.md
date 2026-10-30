# Model tiers and stages

Every ticket carries one **Model** label: the model and thinking effort for its main stage. The other stages of a skill use fixed defaults from the table below. Cheap stages (exploring, gathering) run on smaller models and hand a short brief to the main stage, so the expensive model spends its tokens on the hard part instead of rediscovering context.

## Tiers (Linear label group `Model`, single-select)

| Label | Agent tool call | Use for |
| --- | --- | --- |
| `haiku-low` | model `haiku`, effort `low` | Fully specified mechanical work: copy or config changes, renames, a fixture, 1-2 files, no logic decisions. Never research, design or plan. |
| `sonnet-medium` | model `sonnet`, effort `medium` | Follows a pattern that already exists in the repo; one module; criteria leave no judgement calls; no data-safety risk. |
| `sonnet-high` | model `sonnet`, effort `high` | **Default for build, research and evaluate.** New logic with edge cases, several files, or tests that need designing. A focused research question. |
| `opus-high` | model `opus`, effort `high` | **Default for design and plan.** Work that sets the architecture others build on (harness, skeleton, registry, interfaces); Escalation `security` or `irreversible`; data loss or migrations; trade-offs across many sources; research that synthesizes a whole topic. |

## Estimating the tier (whoever creates the ticket)
Start from the default for the Skill label. Move **down** one tier only when every acceptance criterion is mechanical or copies an existing pattern. Floor: `sonnet-medium` for design, plan, research and evaluate. Move **up** to `opus-high` when any `opus-high` condition above holds. When unsure, keep the default: a ticket that fails review at too low a tier costs more than one built at the right tier. Add one line to the description: `Model: <label> (<reason in a few words>)`. Bootstrap tickets get the default for their Skill label, except "Address design doc comments" and "Fix red main", which get `sonnet-high`.

**Writing the label.** `labels` replaces the whole set, and the group is single-select. Read the ticket's labels, then `save_issue(labels=[every existing label except any other Model label, <new Model label>])`, and re-read to confirm exactly one Model label. A ticket's tier never changes after creation (a fix round runs one tier higher without relabelling).

## Stage defaults

| Skill | Stage | Model |
| --- | --- | --- |
| build-ticket | explore (read-only context brief) | skipped for `haiku-low`; `haiku`, effort `medium` for `sonnet-medium`; `sonnet-medium` for `sonnet-high` and `opus-high` |
| | implement | the ticket's tier |
| | review | `sonnet-high`; `opus-high` when the ticket is `opus-high` |
| | QA | `sonnet`, effort `high` for `sonnet-high` and up, else `medium` |
| | fix round after a FAIL | implementer one tier above the ticket's; review and QA keep the ticket's tier |
| research-question | gather (one subagent per sub-question, in parallel) | `sonnet-medium` |
| | write (findings rows or library page) | the ticket's tier |
| | citation check (exploratory pages) | `sonnet-medium` |
| design-system | background research | `sonnet-medium` |
| | draft | the ticket's tier |
| | critique (fresh eyes; checks the checklist and contradictions, cannot overrule design decisions) | `sonnet-high` |
| plan-tickets | draft | the ticket's tier |
| evaluate-project | evaluate | the ticket's tier |

## Overrides and calibration
- A scheduled prompt's optional `Models:` line overrides this file. Resolve each Agent call from the tier and stage first, then apply `Models` (for example `never opus`: a forbidden model becomes the nearest allowed one, so `opus-high` runs as `sonnet-high`). The label is not rewritten; note `override` in the run-log entry. A blanket line such as `all stages sonnet high` flattens every stage, including explore and gather, so leave `Models:` out unless you mean that.
- Record the ticket's tier, and `fix round at <tier>` when one ran, in the run-log entry. `review-runs` uses those entries to adjust the rubric above when one tier keeps failing or keeps passing with room to spare.
