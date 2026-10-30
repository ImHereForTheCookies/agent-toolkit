# Research findings database (Notion)

One database per project, linked from the Linear project's `Research:` line. People add rows from anywhere (the Notion phone app works); `research-question` adds rows from desk research. The design skill reads every `New` row on its next revision and marks each one `Incorporated` or `Rejected`, so nothing a person contributes is silently dropped.

| Property | Type | Filled by | Meaning |
| --- | --- | --- | --- |
| Finding | title | adder | One sentence: what we learned ("Most people journal at night on their phone, in under 5 minutes") |
| Details | text | adder | What was observed, how many people, quotes paraphrased |
| Evidence | url | adder | Link to notes, recording, survey results, paper, review thread |
| Source type | select | adder | User interview, Survey, Observation, Analytics, Paper, Competitor review, Desk research |
| Confidence | select | adder | High, Medium, Low |
| Implication | text | adder (optional) | What it might mean for the product. On rejection, the designer's reason goes here |
| Status | select | adder sets `New`; designer updates | New, Incorporated, Rejected, Needs human research |
| Design version | text | designer | Doc version that handled it |
| Requirements | text | designer | R-IDs / assumption numbers it changed |

Create it with `notion-create-database` under the design doc page, titled `<Project name> - Research findings`, with exactly these properties.
