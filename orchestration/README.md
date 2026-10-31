# orchestration/: the author's nightly loop (example, not a dependency)

This folder is the author's own unattended pipeline for prototypes: every night it validates an idea, plans it, builds it, evaluates it, cuts a release and writes a launch kit (`NIGHTLY.md` and `RND.md` are the runbooks). It is kept as a worked example of a larger loop built from the same plugins. **No plugin depends on it** (a test enforces that); the general, reusable job is `plugins/ticket-loop`.

Setup-specific values (Linear team, repos, work dir, scheduler trigger, owner name, caps) are not written here. They are double-brace placeholders read from a settings page; see `SETTINGS.md`. `HARD_LIMITS.md` is protected and hash-pinned (see `CONTRIBUTING.md`). `LESSONS.md` and `retros/` are history from the author's runs and mention their projects.
