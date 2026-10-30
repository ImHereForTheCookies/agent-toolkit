# Run log (Notion page)

One page per person or team running the loop, created under the Notion home and passed to the loop as `Run log:` and to the review as `Run log:`. Scheduled runs cannot read each other's conversations, so this page is how one night's experience reaches the review that runs before the next night.

Page body:

```
## Reviews
(newest first; written by review-runs)

## Nights
(newest first; one heading per night: ## YYYY-MM-DD)
```

A night is the date, in the loop's timezone, on which its chain started. Each loop unit adds one entry at the top of its night's heading, 3 to 6 short lines:

- **Unit:** ticket ID, Skill label, outcome (Done, Awaiting Merge, Needs Human, cut off, failed)
- **Friction:** anything that cost time or went wrong: a failing command and its error, a retry, an unclear or contradictory instruction, a missing tool or permission, a step that turned out useless. "none" when there was none.
- **Guess at cause:** one line, or "unknown"

The review keeps the last 14 nights and rolls older ones into one summary line each.
