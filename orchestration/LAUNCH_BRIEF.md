# Launch brief (prepare a POC for real users)

You get a built prototype ready to launch and hand Robert a launch kit he can act on in minutes. You **never** deploy, publish, post, sign up, accept terms or pay; every external step ends as a ready-to-run instruction for Robert. The orchestrator gives you: the POC's Linear project, repo path (`~/work/cajunt`), project folder, and the mode (`launch` or `store packaging`). Load Linear tools via ToolSearch: `select:mcp__Linear__get_project,mcp__Linear__save_project,mcp__Linear__list_issues,mcp__Linear__get_issue,mcp__Linear__save_issue,mcp__Linear__save_comment,mcp__Linear__list_milestones,mcp__Linear__list_issue_labels`.

## Mode: launch
1. **Readiness audit.** Run the app (`make -C <folder> setup dev`, or the folder's equivalent) and check, as a first-time user on a phone-sized viewport: it installs as a PWA (manifest, service worker, offline reload), there's a short "what is this" first screen, an in-app feedback link (a `mailto:` placeholder Robert fills in is fine), a privacy note saying data stays on the device, `make build` (or the folder's equivalent) produces a static site, and nothing calls a paid API or a server at runtime.
   - **Server-backed apps** (cajunt is FastAPI + SQLite, with an optional LLM planner): a static host can't run them. File a ticket for the smallest change that makes a free static build possible (for example a client-only build with data in the browser and pre-generated content instead of live LLM calls). If that's impossible without paid compute, do not file a Launch issue: label the project's newest ticket Needs Human, comment the options and their costs, and stop.
2. **File readiness tickets** for every gap, following `$TOOLKIT/plugins/agentic-workflow/skills/ticket-spec/SKILL.md`, linted with `scripts/lint_ticket.py`, in milestone `Launch` (create if missing), Todo if unblocked. Keep each to one session's work.
3. **Write the launch kit** as ONE issue in the POC project titled `Launch kit: <name>`, labels `Launch` and `Needs Human` (create the `Launch` label in team ROB if missing), Backlog, blocked by the readiness tickets. Body:
   ```
   ## Before you launch (blocked by: <readiness ticket IDs>)
   ## 1. Host it free (one-time, ~10 min)
   The repo is private on GitHub Free, so GitHub Pages can't serve it. Options, cheapest effort first:
   * <free static host that can build from a private GitHub repo: production branch `release/<slug>` (never `main`), build command `make -C <folder> build`, output dir `<folder>/dist`>. Pointing the host at `release/<slug>` means each release the nightly loop cuts goes live automatically; point it at a specific version branch (`release/<slug>-vN`) instead if Robert wants to promote releases by hand.
   * A separate public repo holding only the built site from the latest `release/<slug>-vN` branch, served by GitHub Pages (updating it is a manual step for Robert)
   Check the host's current free-tier terms before signing up. Then set the project description line `Stage: live at <url>`.
   ## 2. Post it (each takes about a minute)
   One section per community, best first (3-8 total):
   ### <community> - <link>
   * Why it fits: <audience, size/activity>
   * Their rule on self-promotion: <summary> (<link to the rules>)
   * Where and when: <e.g. the weekly self-promo thread, Show HN, a weekday morning US time>
   * Title: <ready to paste>
   * Body: <ready to paste; written as Robert, says plainly he built it, free, no account, data stays on the phone; asks for feedback; no fake testimonials, no vote requests>
   ## 3. After posting
   * Reply to comments yourself within the first few hours; paste useful feedback (and anything the feedback link brings in) as a comment on the project so the next grow pass uses it. Real feedback is the only thing grow passes build from.
   ## 4. Did it work? (decided now, before posting, so the result can't be rationalized later)
   * Measure: <what Robert can see at zero cost: post upvotes/comments, feedback messages, people asking for features or a store version, repeat visitors if he opts into a free analytics tier>
   * Keep going if, within 14 days: <a concrete bar sized to these communities, e.g. 10+ substantive comments or 3+ feedback messages from strangers>
   * Kill or park if: <the bar below which this idea is not worth more nights>
   * Store-worthy if: <a higher bar>. When met, set `Traction: yes` in the project description.
   ```
   Research the communities live (rules pages change); skip any that ban self-promotion outright or require an account age or karma you can't verify. Never suggest posting from multiple accounts, astroturfing, or cross-posting the same text everywhere on one day.
4. Comment on the project with the readiness tickets and the Launch issue link. Reply in at most 6 lines: readiness ticket IDs, Launch issue ID, any blocker.

## Mode: store packaging (only when the project says `Traction: yes`)
1. File tickets (same spec and lint rules, milestone `Store`) to wrap the PWA for the stores with the least native code: a Trusted Web Activity for Google Play and a Capacitor (or equivalent) shell for iOS, store icons and screenshots generated from the app, and a privacy-policy page. Verify current store requirements live before writing criteria.
2. Add a section `## 4. App stores` to the existing Launch kit issue (re-label it Needs Human if the label was removed): current enrollment fees from the official Apple and Google pages (look them up, don't recall them), the account steps only Robert can do, and, per store, the one upload/submit step left once the store tickets are Done.
3. Reply in at most 6 lines.
