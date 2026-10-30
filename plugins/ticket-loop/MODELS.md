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
Start from the default for the Skill label. Move **down** one tier only when every acceptance criterion is mechanical or copies an existing pattern. Move **up** to `opus-high` when any `opus-high` condition above holds. When unsure, keep the default: a ticket that fails review at too low a tier costs more than one built at the right tier. Add one line to the description: `Model: <label> (<reason in a few words>)`.

## Stage defaults

| Skill | Stage | Model |
| --- | --- | --- |
| build-ticket | explore (read-only context brief) | `haiku`, effort `medium`; `sonnet-medium` when the ticket is `opus-high` |
| | implement | the ticket's tier |
| | review | `sonnet-high`; `opus-high` when the ticket is `opus-high` |
| | QA | `sonnet`, effort `high` for `sonnet-high` and up, else `medium` |
| | fix round after a FAIL | one tier above the ticket's |
| research-question | gather (one subagent per sub-question, in parallel) | `sonnet-medium` |
| | write (findings rows or library page) | the ticket's tier |
| | citation check (exploratory pages) | `sonnet-medium` |
| design-system | background research | `sonnet-medium` |
| | draft | the ticket's tier |
| | critique (fresh eyes) | `sonnet-high` |
| plan-tickets | draft | the ticket's tier |
| evaluate-project | evaluate | the ticket's tier |

## Overrides and calibration
- A scheduled prompt's optional `Models:` line overrides this file, as it words it (for example `never opus`, or `all stages sonnet high`).
- A ticket that fails review or QA at its tier gets its label raised one step for the fix round. Record the tier and any raise in the run-log entry. `review-runs` uses those entries to adjust the rubric above when one tier keeps failing or keeps passing with room to spare.
