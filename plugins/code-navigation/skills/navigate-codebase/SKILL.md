---
name: navigate-codebase
description: Use when you need to find where something is defined or how a part of a repo works, before reading source files or running broad greps. Gives the cheapest-first search order (CLAUDE.md, module notes, docs/symbols.md, LSP, narrow Grep/Glob, ranged Read), how to write a module note, and when to regenerate the repo map. Works in cloud sessions where LSP is unavailable.
---

# Navigate a codebase cheaply

Every file you read costs tokens. Go down this list and stop at the first step that answers the question.

## Search order

1. **Root `CLAUDE.md`.** Stack, commands, architecture decisions, gotchas. Already loaded in most sessions; check it before searching.
2. **Module notes.** A `NOTES.md` inside a folder says what that folder owns and where to enter. `Glob` for `**/NOTES.md`, then read the one for the folder you care about.
3. **`docs/symbols.md`.** The repo map: one line per file, `path: Class(L12), func(L30), Class.method(L40)`. Grep it instead of the source:
   - `Grep pattern="create_item" path="docs/symbols.md"` finds the file and line.
   - `Grep pattern="^app/" path="docs/symbols.md"` lists everything in a folder.
   Missing or stale? Run `make symbols` (see below). It lists top-level definitions and one level of methods, not call sites.
4. **LSP tool, if you have one** (go to definition, find references). It is exact for references, but LSP plugins do not start in cloud sessions; if no LSP tool is listed, go to step 5.
5. **`Grep` / `Glob` with narrow patterns.** Name the symbol, restrict `path` or `glob` (`--glob "*.py"`), and use `output_mode: files_with_matches` first, then `content` with `-C 2` on the one file that matters. Never grep a bare common word across the repo.
6. **`Read` with `offset`/`limit`.** The map gives you a line number: read about 40 lines around it, not the whole file. Read a whole file only when it is small or you must change most of it.

## Wide exploration: delegate

If answering needs more than about five searches or reading many files ("how does auth work end to end?"), hand it to a subagent. Ask for a summary under 15 lines: file paths with line numbers, the control flow, open questions. Do not ask it to paste code. Your context keeps only the answer.

## Writing a module note

Add a `NOTES.md` to a folder when you learn something that cost you more than a few searches to find out. Keep it to 5-10 lines:

```
# app/ - pantry API
Owns: HTTP routes and validation (main.py), sqlite access (db.py).
Entry point: main.py create_app(); server.py runs it under uvicorn.
Invariants: quantity is never negative; all SQL lives in db.py.
Do not import: main.py from db.py (db stays free of FastAPI).
```

Say what is true now, not history. Update the note in the same commit as a change that makes it wrong. A stale note is worse than none.

## Keeping the map fresh

- Regenerate with `make symbols` after merging code that adds, removes or renames definitions, and before starting work on a branch whose map looks old.
- Commit `docs/symbols.md`. Output has no timestamps, so the diff shows only real changes.
- Wire it into `make verify` if you want drift caught automatically: run `make symbols` there and fail on `git diff --exit-code docs/symbols.md`.
- Without the Makefile target: `python3 <toolkit>/plugins/code-navigation/scripts/repo_map.py . --out docs/symbols.md`. Add `--max-bytes 20000` to cap the size on big repos; the file then ends with `... truncated (N more files)` and you should fall back to Grep for the missing files.
- Skipped automatically: `.git`, `.venv`, `venv`, `node_modules`, `__pycache__`, `dist`, `build`, and any dot-directory. Languages: `.py`, `.js`, `.jsx`, `.ts`, `.tsx`.
