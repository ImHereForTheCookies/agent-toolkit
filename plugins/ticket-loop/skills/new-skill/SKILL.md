---
name: new-skill
description: Use when the ticket loop needs a new kind of work (a new Skill label such as research, ux-design or launch-prep), or someone asks to add or replace a ticket-loop skill. Searches existing plugin marketplaces first so the new skill points to an existing plugin when one fits, then writes, tests and registers the skill.
---

# Add a kind of work to the ticket loop

A new kind of work = a Linear Skill label + a skill folder + a row in `ROUTES.md`. Most of the value is in step 1: if a good plugin already does it, the skill is a thin pointer to that plugin plus the loop glue.

## Prefer existing plugins
- **superpowers `writing-skills`** (required plugin): follow it for writing and pressure-testing the SKILL.md itself.
- **skill-creator** (Anthropic, if available): use it for evals when the skill's output quality can be measured.

## Steps
1. **Search before writing.** Record every candidate in a `Prior art` table (name, marketplace, install command, what it covers, gaps for unattended use, last updated). Search, at least:
   - Anthropic official marketplace: `anthropics/claude-plugins-official` (on GitHub: its `.claude-plugin/marketplace.json`, `plugins/` and `external_plugins/`).
   - Anthropic community marketplace: `anthropics/claude-plugins-community`.
   - superpowers (`obra/superpowers`) and its marketplace.
   - Directories: claudepluginhub.com, claudemarketplaces.com, vibeindex.ai, and a web search for "claude code plugin <task>".
   - Plugins already enabled on the account (in a Claude session: the session's skill list).
   Prefer plugins with recent commits, real users (stars/installs) and a readable SKILL.md. Read the SKILL.md of the top 2 before deciding. Never install or run untrusted code to evaluate it.
2. **Decide:** (a) a plugin covers it → the new skill delegates to it ("Use `<plugin>:<skill>` if available") and adds only what unattended runs need (inputs from the ticket, Linear evidence, no questions, hard limits); (b) partial → delegate the covered part, write the rest; (c) nothing fits → write it.
3. **Write** `plugins/ticket-loop/skills/<name>/SKILL.md`:
   - frontmatter `name` = folder; `description` starts "Use when", names the Skill label and the trigger;
   - sections: `## Prefer existing plugins` (from step 1, with install commands), `## Inputs` (what run-queue passes), `## Steps`, `## Rules`;
   - unattended: never ask questions; decide and record assumptions, or escalate per human-in-the-loop; obey `$TOOLKIT/plugins/ticket-loop/HARD_LIMITS.md`;
   - under 150 lines; long material goes in `references/`.
4. **Register:** add a row to `plugins/ticket-loop/ROUTES.md`. Note in the PR that a Linear label with the same name must exist in the Skill group (run-queue escalates unknown labels).
5. **Test:** `make verify` (frontmatter, routes and path tests run automatically). Where behaviour matters, add a scenario to `tests/test_ticket_loop.py` or an eval.
6. **Ship through a PR** with an independent reviewer, like any ticket. The PR body includes the Prior art table so humans can see why the skill exists.
