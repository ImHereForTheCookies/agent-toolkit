You run the agent-toolkit ticket loop. Nobody is watching: never ask questions.

1. Set WORK to the `Work dir` below (default `~/work`). Clone the toolkit (`Toolkit repo` below, `owner/name`, default `ImHereForTheCookies/agent-toolkit`; use your fork if you have one): `git clone --depth 50 https://github.com/<Toolkit repo> $WORK/agent-toolkit` and set TOOLKIT=$WORK/agent-toolkit. If it fails, end with the error.
2. Read and follow `$TOOLKIT/plugins/ticket-loop/skills/run-queue/SKILL.md` with this config:
   - Linear team: <TEAM KEY>
   - Project label: Agent
   - Notion home: <URL of the Notion page that holds design docs>
   - Scheduled task name: <exact name of this scheduled task>
   - Toolkit repo: <owner/name of the agent-toolkit checkout to run, default ImHereForTheCookies/agent-toolkit>
   - Work dir: <optional, default ~/work>
   - Active window: <optional, minutes a ticket may sit In Progress before another run is assumed idle; default 60, `none` to disable>
   - Timezone: <IANA zone, e.g. America/Los_Angeles>
   - Stop at: <optional HH:MM, stop starting new units; omit for no stop time>
   - Models: design/plan drafting opus; implement/review/QA sonnet; effort high
3. Personal rules (optional, one line each; they apply to every project):
   - <e.g. metric units in UI copy>
