You run the agent-toolkit ticket loop. Nobody is watching: never ask questions.

1. Clone the toolkit: `git clone --depth 50 https://github.com/ImHereForTheCookies/agent-toolkit ~/work/agent-toolkit` and set TOOLKIT=~/work/agent-toolkit. If it fails, end with the error.
2. Read and follow `$TOOLKIT/plugins/ticket-loop/skills/run-queue/SKILL.md` with this config:
   - Linear team: <TEAM KEY>
   - Project label: Agent
   - Notion home: <URL of the Notion page that holds design docs>
   - Scheduled task name: <exact name of this scheduled task>
   - Timezone: <IANA zone, e.g. America/Los_Angeles>
   - Stop at: <HH:MM, stop starting new units>
   - Models: design/plan drafting opus; implement/review/QA sonnet; effort high
3. Personal rules (optional, one line each; they apply to every project):
   - <e.g. metric units in UI copy>
