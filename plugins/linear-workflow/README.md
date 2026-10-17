# linear-workflow

How agents read, claim and report on Linear tickets. The `linear-tickets` skill defines the status mapping (Todo = Ready, In Progress, In Review, Done; label Needs Human = escalated), how to find Ready tickets whose blockers are Done, how to promote Backlog tickets after the ticket linter passes, the evidence comment required before Done, and how to escalate. `.mcp.json` registers the Linear MCP server (`https://mcp.linear.app/mcp`, `Authorization: Bearer ${LINEAR_API_KEY}`) for headless runs; sessions that already have the Linear connector do not need it.

Install: `/plugin marketplace add ImHereForTheCookies/agent-toolkit`, then `/plugin install linear-workflow@agent-toolkit`
