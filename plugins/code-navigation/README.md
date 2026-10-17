# code-navigation

Low-token ways to find code, including in cloud sessions where LSP plugins do not start.

- `navigate-codebase` skill: cheapest-first search order (CLAUDE.md, module notes, `docs/symbols.md`, LSP, narrow Grep/Glob, ranged Read), how to write module notes, when to regenerate the map.
- `scripts/repo_map.py <root> [--out docs/symbols.md] [--max-bytes N]`: stdlib script that writes a symbol index, one line per file (`path: Class(L12), func(L30), Class.method(L40)`). Python via `ast`, JS/TS via regex. Deterministic output.

Install: `/plugin marketplace add ImHereForTheCookies/agent-toolkit`, then `/plugin install code-navigation@agent-toolkit`
