You review the agent-toolkit ticket loop's previous night. Nobody is watching: never ask questions.

1. Clone the toolkit: `git clone --depth 50 https://github.com/ImHereForTheCookies/agent-toolkit ~/work/agent-toolkit` and set TOOLKIT=~/work/agent-toolkit. If the loop runs from another branch (see its scheduled prompt), check that branch out. If cloning fails, end with the error.
2. Read and follow `$TOOLKIT/plugins/ticket-loop/skills/review-runs/SKILL.md` with this config:
   - Run log: <URL of the Notion run log page>
   - Loop task name: <exact name of the ticket loop's scheduled task>
   - Linear team: <TEAM KEY>
   - Project label: Agent
   - Timezone: <IANA zone, e.g. America/Los_Angeles>
   - Toolkit branch: main
3. Personal rules (optional, one line each):
   - <e.g. merge toolkit PRs automatically when the independent check passes>
